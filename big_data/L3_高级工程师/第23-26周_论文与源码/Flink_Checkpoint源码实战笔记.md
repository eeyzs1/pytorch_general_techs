# Flink Checkpoint 源码实战笔记

> **目标**：深入Flink Checkpoint机制的源码实现，理解CheckpointCoordinator触发流程、Barrier对齐过程、RocksDB增量Checkpoint和端到端Exactly-Once的实现
>
> **源码版本**：Apache Flink 1.18 | **阅读范围**：Checkpointing核心模块

---

## 一、Checkpoint架构全景图

```
┌─────────────────────────────────────────────────────────────────┐
│                      JobManager                                 │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │         CheckpointCoordinator (★★★★★ 核心类)              │  │
│  │                                                          │  │
│  │  triggerCheckpoint()   ← 定时器/手动触发                   │  │
│  │  receiveAcknowledge()  ← 收集各Task的Ack                  │  │
│  │  completePendingCheckpoint() → 提交到CompletedCheckpointStore│
│  │  restoreSavepoint()    ← 故障恢复入口                      │  │
│  └──────────┬───────────────────────────────────────────────┘  │
│             │ RPC                                              │
│             ▼                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │         CheckpointBarrierHandler                          │  │
│  │         (在TaskManager上)                                  │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                             │  RPC
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                     TaskManager                                 │
│                                                                 │
│  ┌──────────────────────┐     ┌──────────────────────────────┐ │
│  │  CheckpointBarrier   │     │  StateBackend (★★★★★)        │ │
│  │  Aligner (对齐)       │     │                              │ │
│  │                      │     │  HashMapStateBackend          │ │
│  │  processBarrier()    │     │  EmbeddedRocksDBStateBackend  │ │
│  │  notifyCheckpoint()  │     │                              │ │
│  └──────────┬───────────┘     │  snapshotState()  ← 创建快照  │ │
│             │                 │  restoreState()   ← 恢复快照  │ │
│             ▼                 └──────────────┬───────────────┘ │
│  ┌──────────────────────┐                    │                 │
│  │  SubTask             │                    ▼                 │
│  │  Checkpointable      │     ┌──────────────────────────────┐ │
│  │  (算子的Snapshot)     │     │  RocksDB Incremental         │ │
│  │                      │     │  Snapshot Strategy            │ │
│  │  snapshotState()     │     │  (增量Checkpoint)             │ │
│  └──────────────────────┘     └──────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

---

## 二、CheckpointCoordinator —— 核心协调器

### 2.1 源码路径

```
flink-runtime/src/main/java/org/apache/flink/runtime/checkpoint/CheckpointCoordinator.java
```

### 2.2 triggerCheckpoint() 核心源码注释

```java
public class CheckpointCoordinator {
    
    // ========== 核心成员变量 ==========
    private final ScheduledExecutor timer;             // 定时器(用于定期Checkpoint)
    private final long baseInterval;                   // Checkpoint间隔(如60秒)
    private final long checkpointTimeout;              // Checkpoint超时(如10分钟)
    private final int maxConcurrentCheckpointAttempts; // 最大并发Checkpoint数(默认1)
    private final List<ExecutionVertex> tasksToTrigger; // 需要触发Checkpoint的Source Task
    private final List<ExecutionVertex> tasksToWaitFor; // 需要等待Ack的所有Task
    
    private long checkpointIdCounter;                  // 递增的Checkpoint ID
    private final Map<Long, PendingCheckpoint> pendingCheckpoints; // 进行中的Checkpoint
    
    // ========== triggerCheckpoint() - 触发流程 ==========
    public CompletableFuture<CompletedCheckpoint> triggerCheckpoint(
            long timestamp,                    // 触发时间戳
            CheckpointProperties props,        // 属性(Checkpoint vs Savepoint)
            @Nullable String externalPath) {   // 外部存储路径(Savepoint用)
        
        // Step 1: 检查并发Checkpoint限制
        //   如果 maxConcurrentCheckpointAttempts = 1 (默认)
        //   且有一个Checkpoint正在进行中 → 拒绝本次触发
        synchronized (lock) {
            if (pendingCheckpoints.size() >= maxConcurrentCheckpointAttempts) {
                LOG.info("Too many pending checkpoints, declining checkpoint {}", 
                         checkpointIdCounter);
                throw new CheckpointException(
                    CheckpointFailureReason.TOO_MANY_CONCURRENT_CHECKPOINTS);
            }
        }
        
        // Step 2: 生成新的Checkpoint ID
        long checkpointId = checkpointIdCounter++;
        
        // Step 3: 在Source Task上注入Checkpoint Barrier
        //   ★ 核心: 向所有Source算子的输入端注入Barrier
        //   注意: checkpointId是单调递增的, 确保Barrier的顺序
        final CheckpointOptions checkpointOptions = 
            CheckpointOptions.forConfig(
                CheckpointType.CHECKPOINT,       // 对齐模式
                locationProvider,                // 状态存储位置
                isExactlyOnceMode,               // 是否Exactly-Once
                isUnalignedCheckpoint,           // 是否非对齐Checkpoint
                alignmentTimeout);               // 对齐超时
        
        // Step 4: 创建 PendingCheckpoint 对象追踪本次Checkpoint
        final PendingCheckpoint pendingCheckpoint = new PendingCheckpoint(
            jobId,
            checkpointId,
            timestamp,
            tasksToWaitFor.size(),    // 需要等待的Ack总数
            operatorCoordinatorsToWaitFor.size(),
            props,
            checkpointOptions,
            completionFuture);
        
        synchronized (lock) {
            pendingCheckpoints.put(checkpointId, pendingCheckpoint);
        }
        
        // Step 5: 向所有Source Task发送触发消息
        //   ★ 每个Source Task会收到 triggerCheckpoint 的RPC调用
        for (ExecutionVertex ev : tasksToTrigger) {
            Execution execution = ev.getCurrentExecutionAttempt();
            execution.triggerCheckpoint(checkpointId, timestamp, checkpointOptions);
        }
        
        // Step 6: 设置超时定时器
        //   如果在checkpointTimeout内没有完成 → 标记为失败/过期
        scheduleCheckpointTimeout(checkpointId, checkpointTimeout);
        
        return pendingCheckpoint.getCompletionFuture();
    }

    // ========== receiveAcknowledgeMessage() - 接收Ack ==========
    public boolean receiveAcknowledgeMessage(
            AcknowledgeCheckpoint message,    // 来自TaskManager的Ack
            TaskManagerLocation location) {
        
        synchronized (lock) {
            // Step 1: 找到对应的PendingCheckpoint
            long checkpointId = message.getCheckpointId();
            PendingCheckpoint pending = pendingCheckpoints.get(checkpointId);
            
            if (pending == null) {
                // Checkpoint可能已经被丢弃(过期/超时/失败)
                LOG.info("Received late ack for expired checkpoint {}", checkpointId);
                return false;
            }
            
            // Step 2: 记录这个Task的Ack
            //   Ack中包含:
            //     - subtaskState: 该Task的状态Handle(指向状态存储位置)
            //     - checkpointMetrics: 该Task的Checkpoint耗时/状态大小等指标
            boolean hasAllAcks = pending.acknowledgeTask(
                message.getTaskExecutionId(),
                message.getSubtaskState(),
                message.getCheckpointMetrics(),
                location);
            
            // Step 3: 如果所有Task都Ack了 → 完成Checkpoint!
            if (hasAllAcks) {
                completePendingCheckpoint(pending);
                return true;
            }
            return false;
        }
    }

    // ========== completePendingCheckpoint() - 最终完成 ==========
    private void completePendingCheckpoint(PendingCheckpoint pending) {
        // Step 1: 收集所有SubtaskState, 组装为CompletedCheckpoint
        CompletedCheckpoint completed = pending.finalizeCheckpoint();
        
        // Step 2: 存储到 CompletedCheckpointStore
        //   ZooKeeperCompletedCheckpointStore: 持久化到ZooKeeper
        //   StandaloneCompletedCheckpointStore: 仅存JobManager内存
        completedCheckpointStore.addCheckpoint(
            completed, 
            checkpointsCleaner, 
            () -> {/* 清理旧Checkpoint */});
        
        // Step 3: 通知所有Task Checkpoint已完成
        //   → Task可以释放本地临时状态备份
        for (ExecutionVertex ev : tasksToNotify) {
            ev.notifyCheckpointComplete(checkpointId);
        }
        
        // Step 4: 完成CompletableFuture → 外部调用者获知Checkpoint完成
        pending.getCompletionFuture().complete(completed);
        
        LOG.info("Completed checkpoint {} (in {} ms)", 
                 checkpointId, completed.getDuration());
    }
}
```

### 2.3 Checkpoint触发时机

```
触发方式:
  1. 定时触发(Periodic Checkpoint):
     Execution.enableCheckpointing(60000)  // 每60秒
     → CheckpointCoordinator启动定时器
     → timer.scheduleAtFixedRate(triggerTask, interval, interval)
     
  2. 手动触发(Savepoint):
     bin/flink savepoint <jobId> [savepointPath]
     → REST API → Dispatcher → CheckpointCoordinator.triggerSavepoint()
     
  3. 故障恢复触发:
     从最近的成功Checkpoint恢复 → restoreLatestCheckpointedState()

MinPauseBetweenCheckpoints:
  如果上一个Checkpoint耗时30秒, 且间隔60秒
  实际间隔: max(60 - 30, minPauseBetweenCheckpoints)
  确保系统不会因为Checkpoint而完全阻塞数据处理
```

---

## 三、Barrier对齐过程 —— Checkpoint的核心机制

### 3.1 Barrier对齐时序图

```
Source并行度=2, Map并行度=2，对齐Checkpoint模式

时间轴 ────────────────────────────────────────────────────────────►

Source A ──[data1][data2]──[Barrier#1]──[data3][data4]──
Source B ──[data5]─────────[Barrier#1]──[data6][data7]──

Map Op A (接收 Source A 和 Source B 的数据):

  Step 1: 收到 Source A 的 Barrier#1
    ┌──────────────────────────────────────────┐
    │ Map Op A 的 BarrierHandler:               │
    │   upstream_channel_0 (Source A): 收到Barrier│
    │   → 暂停处理 channel_0 的后续数据            │
    │   → 将 channel_0 后续到达的 data3/data4 缓存  │
    │   → 继续等待 channel_1 (Source B) 的Barrier │
    │                                          │
    │   upstream_channel_1 (Source B): 未收到    │
    │   → 继续正常处理 channel_1 的数据            │
    │   → data5 正常通过 → 被Map Op A处理         │
    └──────────────────────────────────────────┘

  Step 2: 收到 Source B 的 Barrier#1
    ┌──────────────────────────────────────────┐
    │ Map Op A 的 BarrierHandler:               │
    │   所有channel都收到了 Barrier#1!            │
    │   → 对齐完成! ←                            │
    │   → 触发 Checkpoint (snapshotState)       │
    │   → 向下游发送 Barrier#1                   │
    │   → 恢复 channel_0 的处理(处理缓存的data3/4) │
    └──────────────────────────────────────────┘

  Step 3: Checkpoint完成
    Map Op A 的状态被快照并存储 → Ack发回CheckpointCoordinator
```

### 3.2 CheckpointBarrierAligner 源码注释

```java
// flink-runtime/src/main/java/org/apache/flink/runtime/io/network/api/checkpoint/CheckpointBarrierAligner.java

public class CheckpointBarrierAligner implements CheckpointBarrierHandler {
    
    // ========== 核心状态 ==========
    private final String taskName;
    private final int totalNumberOfInputChannels;      // 总输入通道数
    private int numBarriersReceived;                   // 已收到Barrier的通道数
    
    // ★ 对齐期间缓存的数据
    //   Key: channelIndex, Value: 该通道被阻塞后到达的Buffer队列
    private final BufferStorage bufferStorage;
    
    // 当前正在处理的Checkpoint
    private CheckpointBarrierData currentCheckpoint;
    
    // ========== processBarrier() - 核心方法 ==========
    @Override
    public void processBarrier(
            CheckpointBarrier receivedBarrier,    // 收到的Barrier
            InputChannelInfo channelInfo,         // Barrier来自哪个通道
            boolean isRpcTriggered) throws Exception {
        
        long barrierId = receivedBarrier.getId();
        
        synchronized (lock) {
            // Case 1: 这是第一个Barrier(还在等待其他通道)
            if (numBarriersReceived == 0) {
                // ★ 初始化：开始一个新的对齐周期
                numBarriersReceived = 1;
                
                // 记录第一个Barrier的信息
                currentCheckpoint = new CheckpointBarrierData(receivedBarrier);
                
                // ★ 阻塞当前通道!(暂停该通道的后续数据处理)
                //   来自该通道的数据将被缓存在 bufferStorage 中
                barrierChannelStates[channelInfo.getGateIndex()]
                    .setBlocked(barrierId);
                
                LOG.debug("{}: Received first barrier {} from channel {}. Blocking channel.", 
                          taskName, barrierId, channelInfo);
            }
            // Case 2: 还在等待其他通道的Barrier
            else if (numBarriersReceived < totalNumberOfInputChannels) {
                numBarriersReceived++;
                
                // 阻塞当前通道
                barrierChannelStates[channelInfo.getGateIndex()]
                    .setBlocked(currentCheckpoint.getId());
                
                LOG.debug("{}: Received barrier {} from channel {}. "
                         + "Waiting for {} more channels.",
                         taskName, barrierId, channelInfo, 
                         totalNumberOfInputChannels - numBarriersReceived);
            }
            // Case 3: 最后一个Barrier → 对齐完成!
            else {
                // ★ 所有通道都收到了Barrier → 开始Snapshot!
                
                // ① 触发Checkpoint (快照当前算子的状态)
                notifyCheckpoint(receivedBarrier);
                
                // ② 释放所有被阻塞的通道
                for (int i = 0; i < barrierChannelStates.length; i++) {
                    barrierChannelStates[i].setBlocked(null);
                }
                
                // ③ 处理被缓存的数据
                //   bufferStorage 中缓存了对齐期间被阻塞的数据
                //   现在按时间顺序释放它们
                bufferStorage.resumeConsumption();
                
                // ④ 向下游转发Barrier
                controller.triggerBarrier(receivedBarrier);
                
                // ⑤ 重置计数器 → 准备下一个Checkpoint
                numBarriersReceived = 0;
                
                LOG.debug("{}: Alignment complete for checkpoint {}. "
                         + "Starting snapshot and unblocking channels.",
                         taskName, barrierId);
            }
        }
    }
    
    // ========== 对齐期间的数据缓存 ==========
    @Override
    public Buffer processNonBarrier(Buffer buffer, InputChannelInfo channelInfo) {
        // 检查当前通道是否被阻塞
        if (barrierChannelStates[channelInfo.getGateIndex()].isBlocked()) {
            // ★ 通道被阻塞 → 缓存数据, 等对齐完成后处理
            bufferStorage.add(buffer, channelInfo);
            return null;  // 不处理(缓存)
        } else {
            // 通道未被阻塞 → 正常处理
            return buffer;
        }
    }
}
```

### 3.3 Barrier对齐 vs 不对齐的性能对比

```
Barrier对齐 (Aligned Checkpoint):
  
  优点:
    ✓ 状态最小(只包含算子状态)
    ✓ 实现简单, 确定性高
    ✓ 适合大多数场景
    
  缺点:
    ✗ 如果有反压, 对齐时间可能很长
      (等待最慢的上游通道发送Barrier)
    ✗ 被阻塞通道的缓存可能溢出(触发反压)
    

Barrier不对齐 (Unaligned Checkpoint):
  
  优点:
    ✓ 不阻塞任何通道 → 即使在反压下也能快速完成Checkpoint
    ✓ Barrier传递速度更快(不等待), 适合高吞吐+反压场景
  
  缺点:
    ✗ 状态更大(包含in-flight的buffer数据作为Channel State)
    ✗ Checkpoint文件更大 → 更多存储
    ✗ 恢复时需要处理in-flight数据 → 恢复更复杂

不对齐的实现(CheckpointBarrierUnaligner):
  收到第一个Barrier:
    ① 不阻塞任何通道!
    ② 每个通道独立追踪: 
       "收到Barrier前处理了哪些数据" (Channel State)
    ③ 到达的Barrier立即向下游转发!
  
  收到最后一个Barrier:
    ① 触发Snapshot(状态 = 算子状态 + 每个通道的in-flight数据)
    ② Channel State: 记录"这个通道在第一个Barrier到达最后一个Barrier之间
       收到的所有数据" → 恢复时重新消费
```

---

## 四、RocksDB增量Checkpoint

### 4.1 源码路径

```
flink-state-backends/flink-statebackend-rocksdb/src/main/java/org/apache/flink/
  contrib/streaming/state/RocksDBKeyedStateBackend.java
  contrib/streaming/state/snapshot/RocksIncrementalSnapshotStrategy.java
```

### 4.2 增量Checkpoint的核心原理

```
全量Checkpoint (每次上传所有SST文件):
  
  Checkpoint 1: 上传 SST1.data (100MB)
  Checkpoint 2: 上传 SST1.data + SST2.data (200MB)
  Checkpoint 3: 上传 SST1.data + SST2.data + SST3.data (300MB)
  → 每次上传全部数据, 存储成本线性增长

增量Checkpoint (只上传新增的SST文件):

  Checkpoint 1:
    当前SST文件: [sst_001, sst_002] (共200MB)
    上传: sst_001 (100MB) + sst_002 (100MB)  ← 首轮全量
    共享状态注册表: {sst_001: 1, sst_002: 1}

  Checkpoint 2:
    当前SST文件: [sst_001, sst_002, sst_003] (RocksDB Compaction产生)
    上传: 只上传 sst_003 (新增, 100MB)  ← 增量!
    共享状态注册表: {sst_001: 2, sst_002: 2, sst_003: 1}
    → 节省了200MB的上传!

  Checkpoint 3:
    当前SST文件: [sst_004, sst_005] (sst_001-003被Compact成一个文件)
    上传: sst_004 (150MB) + sst_005 (50MB)
    共享状态注册表更新: {sst_004: 1, sst_005: 1}
    → 旧SST文件(sst_001/002/003)在没有Checkpoint引用它时被清理

增量Checkpoint的共享引用:
  ┌─────────────────────────────────────────┐
  │  共享状态注册表(SharedStateRegistry)     │
  │                                         │
  │  sst_001: 引用计数=2                    │
  │    ← Checkpoint#1引用 + Checkpoint#2引用 │
  │                                         │
  │  sst_003: 引用计数=1                    │
  │    ← Checkpoint#2引用                   │
  │                                         │
  │  当Checkpoint#1过期被清理 → sst_001引用减1 │
  │  当Checkpoint#2过期被清理 → sst_001引用为0 │
  │  → sst_001可以被物理删除!                 │
  └─────────────────────────────────────────┘
```

### 4.3 RocksIncrementalSnapshotStrategy 源码注释

```java
public class RocksIncrementalSnapshotStrategy {

    @Override
    public RunnableFuture<SnapshotResult<KeyedStateHandle>> snapshot(
            long checkpointId,
            long timestamp,
            CheckpointStreamFactory streamFactory,
            CheckpointOptions options) throws Exception {
        
        // Step 1: 触发RocksDB Flush
        //   ★ 调用 RocksDB.flush() 确保所有MemTable数据刷到SST文件
        //   这是"同步点"——Flush之后创建的SST文件就是本次Checkpoint需要上传的
        rocksDB.flush(flushOptions);
        
        // Step 2: 获取当前所有SST文件列表
        //   RocksDB的 current() 方法返回当前活跃的SST文件
        List<LiveFileMetaData> liveFiles = rocksDB.getLiveFiles();
        
        // Step 3: 对比上次Checkpoint的SST文件列表
        //   找出哪些SST文件是新的(本次新增的)
        //   哪些SST文件已存在(共享引用)
        Set<String> lastSstFiles = lastCompletedCheckpointSstFiles;
        Set<String> currentSstFiles = liveFiles.stream()
            .map(f -> f.fileName())
            .collect(Collectors.toSet());
        
        // 新增的SST文件 = 当前 - 上次
        Set<String> newSstFiles = new HashSet<>(currentSstFiles);
        newSstFiles.removeAll(lastSstFiles);
        
        // Step 4: 上传新增的SST文件到Checkpoint存储
        List<StateHandle> uploadedHandles = new ArrayList<>();
        for (String sstFile : newSstFiles) {
            // 从RocksDB本地目录读取SST文件
            Path localPath = instanceBasePath.resolve(sstFile);
            
            // 上传到分布式存储(如S3/HDFS)
            StreamStateHandle handle = streamFactory
                .createStateHandle(sstFile, localPath);
            
            uploadedHandles.add(handle);
        }
        
        // Step 5: 上传Meta信息(MANIFEST, CURRENT文件)
        //   这些文件用于恢复时重建RocksDB
        uploadMetaFiles(streamFactory);
        
        // Step 6: 注册共享状态
        //   ★ 通知SharedStateRegistry: 本次Checkpoint引用了这些SST文件
        for (String sstFile : currentSstFiles) {
            sharedStateRegistry.registerReference(
                sstFile, checkpointId);
        }
        
        // Step 7: 构建 IncrementalRemoteKeyedStateHandle
        return new IncrementalRemoteKeyedStateHandle(
            backendUID,
            keyGroupRange,
            checkpointId,
            uploadedHandles,       // 本次新增上传的SST文件
            sharedStateHandles,    // 共享引用的SST文件(之前已上传)
            metaStateHandle        // Meta信息
        );
    }
}
```

### 4.4 增量Checkpoint何时退化为全量？

```
退化触发条件:

1. RocksDB实例重建(Restart)
   Task重启 → RocksDB重新打开 → SST文件列表与之前完全不同
   → 即使文件名相同, RocksDB也认为它们是"新文件"
   → 触发全量上传

2. Compaction导致所有旧SST被替换
   如果Major Compaction将所有旧SST文件合并为全新的SST文件
   → 从增量角度看, 所有SST文件都是"新增的"
   → 实际上等同于全量上传

3. 共享状态过期清理
   最后一个引用旧SST的Checkpoint被删除
   → 该SST文件的共享引用归零
   → 当新的Checkpoint再次产生相同的SST时, 视为"新文件"

4. 恢复后首次Checkpoint
   从Savepoint/Checkpoint恢复的Task
   → 首次Checkpoint总是全量(因为没有"上一次"做增量对比)
```

---

## 五、端到端Exactly-Once实现

### 5.1 TwoPhaseCommitSinkFunction

```java
// flink-streaming-java/src/main/java/org/apache/flink/streaming/api/functions/sink/
// TwoPhaseCommitSinkFunction.java

public abstract class TwoPhaseCommitSinkFunction<IN, TXN, CONTEXT>
    extends RichSinkFunction<IN>
    implements CheckpointedFunction, CheckpointListener {

    // ========== 事务状态 ==========
    private transient TransactionHolder<TXN> currentTransaction;  // 当前事务
    private final List<TransactionHolder<TXN>> pendingCommitTransactions; // 待提交
    private final Set<TransactionHolder<TXN>> pendingCommitFromPrevCp;     // 上个CP待提交

    // ========== Phase 1: beginTransaction() ==========
    // 在收到每个数据之前调用, 或在上一个事务提交后调用
    protected abstract TXN beginTransaction() throws Exception;
    
    // ========== Phase 2: preCommit() ==========
    // Checkpoint时调用: 预提交当前事务(但不最终提交)
    protected abstract void preCommit(TXN transaction) throws Exception;
    
    // ========== Phase 3: commit() ==========
    // Checkpoint完成后调用: 最终提交事务
    protected abstract void commit(TXN transaction);
    
    // ========== Phase 4: abort() ==========
    // Checkpoint失败时调用: 回滚事务
    protected abstract void abort(TXN transaction);

    // ========== invoke() - 处理每条数据 ==========
    @Override
    public void invoke(IN value, Context context) throws Exception {
        // 每条数据通过当前事务写入
        currentTransaction = ensureTransaction();
        currentTransaction.process(value);  // 写入Kafka事务中的一条消息
    }

    // ========== snapshotState() - Checkpoint时调用 ==========
    @Override
    public void snapshotState(FunctionSnapshotContext context) throws Exception {
        // Step 1: 预提交当前事务
        //   Kafka: producer.flush() + producer.preCommit()
        //   作用: 刷新所有缓冲数据, 标记事务为"待提交"
        preCommit(currentTransaction.handle);
        
        // Step 2: 将当前事务移到 pendingCommitTransactions
        pendingCommitTransactions.add(currentTransaction);
        
        // Step 3: 创建新事务(用于后续数据)
        currentTransaction = new TransactionHolder(beginTransaction());
        
        // Step 4: 将 pendingCommitTransactions 的IDs保存到State
        //   恢复时可以根据这些IDs决定: commit 还是 abort
        List<Long> transactionIds = pendingCommitTransactions.stream()
            .map(t -> t.getCheckpointId())
            .collect(Collectors.toList());
        // 存入Operator State(如ListState)
    }

    // ========== notifyCheckpointComplete() - Checkpoint完成时调用 ==========
    @Override
    public void notifyCheckpointComplete(long checkpointId) throws Exception {
        // ★ 只有Checkpoint成功完成, 才最终提交事务!
        // 这保证了 Exactly-Once:
        //   如果Checkpoint成功 → 数据被Commit → 下游可见
        //   如果Checkpoint失败 → 数据被Abort  → 下游不可见
        //   一致性边界 = Checkpoint边界!
        
        Iterator<TransactionHolder<TXN>> it = pendingCommitTransactions.iterator();
        while (it.hasNext()) {
            TransactionHolder<TXN> txn = it.next();
            if (txn.getCheckpointId() <= checkpointId) {
                commit(txn.handle);     // ★ 提交到Kafka!
                it.remove();
            }
        }
    }

    // ========== notifyCheckpointAborted() - Checkpoint失败时调用 ==========
    @Override
    public void notifyCheckpointAborted(long checkpointId) throws Exception {
        // Checkpoint失败 → 回滚对应的事务
        // 这些数据不会被下游消费(Exactly-Once)
        Iterator<TransactionHolder<TXN>> it = pendingCommitTransactions.iterator();
        while (it.hasNext()) {
            TransactionHolder<TXN> txn = it.next();
            if (txn.getCheckpointId() == checkpointId) {
                abort(txn.handle);      // ★ 回滚!
                it.remove();
            }
        }
    }
}
```

### 5.2 Kafka的端到端Exactly-Once时序

```
时间轴 ────────────────────────────────────────────────────────────►

  Source → Map → TwoPhaseCommitSink(Kafka Producer)

  1. 开始事务 T1
     producer.beginTransaction()
     
  2. 处理数据 [msg1, msg2, msg3]
     producer.send(msg1); producer.send(msg2); producer.send(msg3)
     
  3. Checkpoint#1 触发:
     a. Source/Map的State快照
     b. Kafka Producer: 
        producer.flush()
        producer.preCommit()  ← ★ 预提交(数据已写入Kafka Broker,
                                 但标记为"未提交", 消费者看不到!)
     c. 记录 "T1 = Checkpoint#1" → 写入Operator State
     d. 开启新事务 T2
     
  4. Checkpoint#1 成功完成:
     → notifyCheckpointComplete(1)
     → producer.commitTransaction(T1)  ← ★ 最终提交! 消费者可见!
     
  5. Checkpoint#2 触发(但失败了):
     → notifyCheckpointAborted(2)
     → producer.abortTransaction(T2)   ← ★ T2的数据回滚! 消费者不可见!
     
  6. 故障恢复: 从Checkpoint#1恢复
     → 恢复后状态: T2未提交 → abort T2
     → 重新处理Checkpoint#1之后的数据
     → 开启新事务 T3 → 这些数据不会重复!
```

---

## 六、Checkpoint调优实战

### 6.1 关键配置参数

```yaml
# flink-conf.yaml 中的Checkpoint配置

# 基础配置
execution.checkpointing.interval: 60s           # Checkpoint间隔
execution.checkpointing.mode: EXACTLY_ONCE       # Exactly-Once/AT_LEAST_ONCE
execution.checkpointing.timeout: 10min           # Checkpoint超时
execution.checkpointing.max-concurrent-checkpoints: 1  # 最大并发Checkpoint
execution.checkpointing.min-pause: 30s           # Checkpoint间最小间隔
execution.checkpointing.tolerable-failed-checkpoints: 3  # 容忍失败次数

# 不对齐Checkpoint
execution.checkpointing.unaligned.enabled: false       # 启用不对齐
execution.checkpointing.alignment-timeout: 30s         # 对齐超时(超时后切换为不对齐)

# State Backend
state.backend: rocksdb                                 # HashMap/rocksdb
state.backend.rocksdb.localdir: /data/flink/rocksdb     # RocksDB本地目录
state.backend.incremental: true                         # 增量Checkpoint
state.backend.rocksdb.timer-service.factory: HEAP       # Timer存储在堆中(默认RocksDB)

# Checkpoint存储
state.checkpoints.dir: hdfs://namenode:8020/flink/checkpoints
state.savepoints.dir: hdfs://namenode:8020/flink/savepoints

# 外部化Checkpoint(Job取消后保留)
execution.checkpointing.externalized-checkpoint-retention: 
  RETAIN_ON_CANCELLATION   # 取消后保留 (或 DELETE_ON_CANCELLATION)

# 状态TTL
table.exec.state.ttl: 86400000  # 状态过期时间(24小时)
```

### 6.2 Checkpoint性能分析

```
Checkpoint耗时 = t_barrier_propagate + t_snapshot + t_upload

1. Barrier传播时间 (t_barrier_propagate):
   影响: 算子链长度、反压程度、对齐等待
   优化:
     - 启用不对齐Checkpoint(反压场景)
     - 减少算子链长度(合并算子)
     - 确保Source并行度均匀

2. Snapshot时间 (t_snapshot):
   影响: State大小、State Backend类型
   优化:
     - RocksDB: 使用增量Checkpoint
     - 设置 State TTL(清理过期状态)
     - 避免在KeyedState中存大对象

3. 上传时间 (t_upload):
   影响: State大小、网络带宽、存储系统性能
   优化:
     - 使用增量Checkpoint → 减少上传量
     - 使用本地SSD做RocksDB → 减少快照延迟
     - 选择近的Checkpoint存储节点

Checkpoint超时排查:
  1. Flink UI → Checkpoints → Checkpoint History
     - 看哪个SubTask的"Sync Duration"最长
     - 看哪个SubTask的"Async Duration"最长
  
  2. 日志关键词: "checkpoint", "barrier", "timeout"
  
  3. 常见问题:
     - 反压导致Barrier传播慢 → 扩大并行度或使用不对齐
     - RocksDB Compaction和Checkpoint冲突 → 设置rocksdb.compaction.style=FIFO
     - 大State导致Snapshot慢 → 使用State TTL
     - 网络带宽不足导致上传慢 → 增量Checkpoint
```

---

## 七、关键类调用关系图（文字版）

```
JobManager 侧:
  CheckpointCoordinator
    ├── triggerCheckpoint()
    │     └── Execution.triggerCheckpoint()  ← RPC到TaskManager
    ├── receiveAcknowledgeMessage()
    │     └── PendingCheckpoint.acknowledgeTask()
    │           └── completePendingCheckpoint()
    │                 ├── CompletedCheckpointStore.addCheckpoint()
    │                 └── Execution.notifyCheckpointComplete()  ← RPC
    └── restoreSavepoint()
          └── CompletedCheckpointStore.getLatestCheckpoint()

TaskManager 侧:
  Task
    └── StreamTask
          ├── triggerCheckpoint()  ← 来自JobManager的RPC
          │     └── CheckpointBarrierHandler (对齐/不对齐)
          │           └── notifyCheckpoint()
          │                 └── operator.snapshotState()
          │                       └── StateBackend.snapshotState()
          │                             ├── HashMapStateBackend: 序列化到文件
          │                             └── EmbeddedRocksDBStateBackend:
          │                                   └── RocksIncrementalSnapshotStrategy
          │                                         ├── rocksDB.flush()
          │                                         ├── uploadNewSstFiles()
          │                                         └── SharedStateRegistry.register()
          │
          └── notifyCheckpointComplete()  ← 来自JobManager的RPC
                └── TwoPhaseCommitSinkFunction.notifyCheckpointComplete()
                      └── KafkaProducer.commitTransaction()
```

---

## 八、练习题

**1. 解释Flink Checkpoint的Barrier对齐过程。为什么需要对齐？不对齐模式又是如何工作的？**

<details>
<summary>参考答案</summary>

Barrier对齐过程：当一个算子有多个上游通道时，第一个收到Barrier的通道被阻塞，后续数据被缓存。等到所有通道都收到同一次Checkpoint的Barrier后，触发本算子的State Snapshot。对齐确保了Snapshot包含的是"同一逻辑时刻"的状态。

不对齐模式：收到第一个Barrier时不阻塞，Barrier立即向下游传递，同时追踪每个通道从第一个Barrier到最后一个Barrier之间到达的数据（作为Channel State）。Snapshot包含：算子State + 每个通道的Channel State。恢复时先恢复State，然后重放Channel State中的数据。

</details>

**2. RocksDB增量Checkpoint是如何工作的？什么情况下会退化为全量Checkpoint？**

参考上文第四节。

**3. 描述端到端Exactly-Once的TwoPhaseCommitSinkFunction实现原理。为什么需要preCommit + commit两个阶段？**

<details>
<summary>参考答案</summary>

preCommit阶段（在Checkpoint时）：数据已写入Kafka Broker但标记为事务未提交，消费者不可见。preCommit的状态被保存到Operator State中。

commit阶段（在Checkpoint完成后）：最终提交事务，消费者可见。

需要两个阶段的原因：如果preCommit和commit之间发生故障，可以从Operator State中恢复事务ID，决定是commit还是abort。这保证了Exactly-Once——要么数据完全不出现，要么恰好出现一次。

</details>

---

> **核心Takeaway**：Flink的Checkpoint机制 = Chandy-Lamport分布式快照算法 + 异步State快照 + 两阶段提交。理解Checkpoint不是理解一个API，而是理解"如何在不停机的情况下，给一个运行中的分布式流处理系统拍一张一致的快照"——这是分布式系统中最优雅的算法之一。