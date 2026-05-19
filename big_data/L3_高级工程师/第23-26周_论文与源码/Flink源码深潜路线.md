# Flink源码深潜路线

> **目标**：深入Flink Checkpoint和StateBackend源码，理解容错机制的底层实现
>
> **周期**：第25周（与Spark Catalyst第3-4周并行） | **建议先完成Spark源码阅读** | **强制输出**：1篇源码分析文章（2000+字）

---

## Flink源码整体架构速览

```
┌────────────────────────────────────────────────────┐
│                   Flink Runtime                     │
│  ┌──────────┐  ┌──────────┐  ┌──────────────────┐ │
│  │ JobMaster│  │TaskManager│  │ResourceManager   │ │
│  │(JM)      │  │(TM)      │  │                   │ │
│  └────┬─────┘  └────┬─────┘  └──────────────────┘ │
│       │              │                               │
│  ┌────▼──────────────▼─────────────────────────┐   │
│  │              TaskExecutor                     │   │
│  │  ┌──────────┐  ┌──────────┐  ┌────────────┐ │   │
│  │  │  Source  │→ │  Operator│→ │    Sink    │ │   │
│  │  │  Task    │  │  Task    │  │    Task    │ │   │
│  │  └──────────┘  └────┬─────┘  └────────────┘ │   │
│  │                      │                         │   │
│  │              ┌───────▼────────┐               │   │
│  │              │  StateBackend  │← 本路线重点    │   │
│  │              └───────┬────────┘               │   │
│  └──────────────────────┼─────────────────────────┘   │
│                         │                              │
│  ┌──────────────────────▼─────────────────────────┐   │
│  │              CheckpointCoordinator              │   │
│  │            ← 本路线重点                          │   │
│  └────────────────────────────────────────────────┘   │
└────────────────────────────────────────────────────┘
```

---

## 路线图总览

```
第1天: Checkpoint Coordinator — 谁在触发Checkpoint？
  阅读: CheckpointCoordinator.java, CheckpointBarrierHandler.java
  重点: 触发时机、Barrier注入、对齐机制
  实验: 手动触发Checkpoint并观察日志

第2天: Checkpoint Barrier对齐 — 最精妙的设计
  阅读: CheckpointBarrierAligner.java, CheckpointBarrierUnaligner.java
  重点: Barrier对齐 vs 不对齐、异步Snapshot
  实验: 对比对齐/不对齐的性能差异

第3天: StateBackend — 状态存在哪里？
  阅读: StateBackend.java, HashMapStateBackend.java, EmbeddedRocksDBStateBackend.java
  重点: Heap vs RocksDB、增量Checkpoint
  实验: 对比两种Backend在100MB+状态下的性能

第4天: Savepoint与端到端Exactly-Once
  阅读: Savepoint相关代码 + TwoPhaseCommitSinkFunction.java
  重点: Savepoint兼容性、Kafka事务集成
  实验: Savepoint恢复 + 数据一致性验证
```

---

## 环境准备

```bash
# 1. Clone Flink源码
git clone https://github.com/apache/flink.git
cd flink
git checkout release-1.18.0

# 2. 构建项目（跳过测试）
mvn clean package -DskipTests -Dfast

# 3. 导入IntelliJ IDEA
# File → Open → 选择flink根目录
# 等待Maven依赖解析完成

# 4. 验证环境
# 运行 flink-examples 中的 WordCount
# Debug: 在 StreamExecutionEnvironment.execute() 打断点
```

### 关键源码目录
```
flink/
├── flink-runtime/                    ← 核心Runtime
│   └── src/main/java/org/apache/flink/runtime/
│       ├── checkpoint/               ← Checkpoint机制
│       │   ├── CheckpointCoordinator.java
│       │   ├── CheckpointBarrierHandler.java
│       │   ├── CheckpointBarrierAligner.java
│       │   └── CheckpointBarrierUnaligner.java
│       ├── state/                    ← State管理
│       │   ├── StateBackend.java
│       │   ├── CheckpointStorage.java
│       │   └── TaskStateManager.java
│       └── taskmanager/              ← TaskManager
│           └── Task.java
├── flink-state-backends/             ← State Backend实现
│   ├── flink-statebackend-heap/      ← Heap (HashMapStateBackend)
│   └── flink-statebackend-rocksdb/   ← RocksDB
└── flink-streaming-java/             ← DataStream API
    └── src/main/java/org/apache/flink/streaming/api/
        ├── checkpoint/               ← Checkpoint配置
        └── functions/                ← TwoPhaseCommitSinkFunction等
```

---

## 第1天：Checkpoint Coordinator — 谁在触发Checkpoint？

### 阅读目标
理解Checkpoint从"触发"到"完成"的完整流程

### 核心文件

#### 文件1：`CheckpointCoordinator.java`
**路径**：`flink-runtime/src/main/java/org/apache/flink/runtime/checkpoint/CheckpointCoordinator.java`

**阅读重点（按优先级）**：

1. **`triggerCheckpoint()` 方法** — Checkpoint的入口
   ```
   触发时机:
   - 定时触发: 基于 checkpointInterval
   - 手动触发: 用户通过 REST API 或 CLI 触发
   - 作业结束: 带 --checkpointOnFinish 的最后一次
   ```
   - 入参：`CheckpointProperties`（区分Regular Checkpoint和Savepoint）
   - 出参：`CompletableFuture<CompletedCheckpoint>`
   - 内部流程：检查是否可以触发 → 生成CheckpointID → 通知所有Source Task → 等待完成

2. **`receiveAcknowledgeMessage()` 方法** — 接收各Task的ACK
   - 每个Task完成自己的Checkpoint后，向Coordinator发送ACK
   - Coordinator如何判断"所有Task都完成了"？
   - 如果有Task没有ACK怎么办？（超时处理）

3. **`completePendingCheckpoint()` 方法** — Checkpoint完成后的清理
   - 通知所有Task "本次Checkpoint已完成"（可以清理旧Checkpoint文件了）
   - 更新作业的Checkpoint计数
   - 保存CompletedCheckpoint到外部存储

**必须能回答的问题**：
1. CheckpointCoordinator如何知道有哪些Source Task？
2. 如果Checkpoint进行中，下一次自动Checkpoint到时间了怎么办？
3. 并发Checkpoint的配置（`maxConcurrentCheckpoints`）的含义是什么？

#### 文件2：`CheckpointBarrierHandler.java`
**路径**：`flink-runtime/src/main/java/org/apache/flink/runtime/checkpoint/CheckpointBarrierHandler.java`

**核心职责**：
- 处理从上游传过来的Checkpoint Barrier
- 协调多个输入通道的Barrier对齐
- 在对齐/不对齐完成后触发本地State Snapshot

**子类**：
- `CheckpointBarrierAligner`：严格对齐模式
- `CheckpointBarrierUnaligner`：不对齐模式（Flink 1.11+）

**强制实验**：
```java
// 1. 启动一个带Checkpoint的Flink任务
env.enableCheckpointing(5000);  // 每5秒一次Checkpoint
env.setStateBackend(new HashMapStateBackend());
env.getCheckpointConfig().setCheckpointStorage("file:///tmp/flink-checkpoints");

// 2. 观察Flink Web UI中的Checkpoint历史
// http://localhost:8081/#/job/{jobId}/checkpoints

// 3. 观察日志中的Checkpoint触发和完成
// 关键字: "Triggering checkpoint", "Completed checkpoint"
```

### 第1天强制输出
- 画CheckpointCoordinator的触发→ACK→完成的时序图
- 标注每个阶段涉及的组件和方法调用

---

## 第2天：Checkpoint Barrier对齐 — 最精妙的设计

### 阅读目标
深入理解Barrier对齐机制（对齐和不对齐两种模式）

### 核心概念可视化

```
场景: 2个上游Source → 1个下游Map Operator

时间 ──────────────────────────────────────────→

Source 1:  [1][2][Barrier_1][3][4][5][6]...
Source 2:  [A][B][C][D][Barrier_1][E]...

            │                │
            ▼                ▼
        Map Operator (2个输入通道)

对齐模式 (Aligner):
  当通道1收到 Barrier_1:
    通道1被"阻塞" → 记录3、4被缓存但不处理
    通道2继续接收数据 → A、B、C、D被正常处理
  当通道2也收到 Barrier_1:
    两个通道都收到了Barrier → 触发State Snapshot
    Snapshot完成后 → 释放通道1的缓存数据(3、4)

不对齐模式 (Unaligner):
  通道1收到 Barrier_1:
    通道1继续处理（不阻塞！）
    但: 在State中记录"通道1在Barrier后的第一条数据是3"
  通道2收到 Barrier_1:
    数据在State中记录"已处理到D"
  随着Barrier一起向下游传递:
    下游的State Snapshot会包含"已超前处理的数据"的状态
```

### 核心文件

#### 文件1：`CheckpointBarrierAligner.java`
**路径**：`flink-runtime/src/main/java/org/apache/flink/runtime/checkpoint/CheckpointBarrierAligner.java`

**核心数据结构**：
```java
// 每个输入通道的状态
private int numBarriersReceived;           // 已收到Barrier的通道数
private int numClosedChannels;             // 已关闭的通道数
private BufferBlocker blockedChannels;    // 被阻塞通道的Buffer缓存
```

**核心方法**：
1. `processBarrier()` — 当收到一个Barrier时
2. `processNonRecordData()` — 当收到被阻塞通道的非记录数据时
3. `notifyCheckpoint()` — 当所有通道都收到Barrier后，触发Checkpoint

**关键设计问题**：
1. 为什么阻塞通道需要缓存数据？不能直接丢弃吗？
2. Blocked Buffer存储在哪里？（内存 → 满了怎么办？→ 反压上游！）
3. 如果某个通道长时间没有Barrier（上游太慢），会怎样？

#### 文件2：`CheckpointBarrierUnaligner.java`
**路径**：`flink-runtime/src/main/java/org/apache/flink/runtime/checkpoint/CheckpointBarrierUnaligner.java`

**核心思想**：
- "我不等慢的通道了，直接在Barrier到达时做Snapshot"
- 但Snapshot中要包含"已经超前处理的数据"

**关键数据结构**：
```java
// 记录哪些数据是"在Barrier之前被处理的"
// 用于恢复时正确回滚
private final Set<InputChannel> prioritisedChannels;
private final ChannelState channelState;
```

**对比实验（必须做）**：
```java
// 实验设置：故意让一个Source产生延迟

// 配置1: 对齐模式
env.getCheckpointConfig().enableUnalignedCheckpoints(false);

// 配置2: 不对齐模式
env.getCheckpointConfig().enableUnalignedCheckpoints(true);

// 对比指标:
// 1. Checkpoint耗时分布
// 2. 端到端延迟
// 3. State Size（不对齐模式的State更大！）
```

### 第2天强制输出
- 画Barrier对齐和不对齐的对比流程图
- 标注2种模式下的优缺点
- 实验数据：对比对齐/不对齐的Checkpoint耗时和State大小

---

## 第3天：StateBackend — 状态存在哪里？

### 阅读目标
深入理解HashMapStateBackend和EmbeddedRocksDBStateBackend的核心差异

### 核心文件

#### 文件1：`StateBackend.java`（接口定义）
**路径**：`flink-runtime/src/main/java/org/apache/flink/runtime/state/StateBackend.java`

**核心方法**：
```java
public interface StateBackend extends java.io.Serializable {
    // 创建KeyedStateBackend（处理KeyedState）
    <K> AbstractKeyedStateBackend<K> createKeyedStateBackend(...);
    
    // 创建OperatorStateBackend（处理OperatorState）
    OperatorStateBackend createOperatorStateBackend(...);
    
    // 是否支持Savepoint
    boolean supportsSavepoint();
}
```

#### 文件2：`HashMapStateBackend.java`（堆内存Backend）
**路径**：`flink-state-backends/flink-statebackend-heap/`

**核心特点**：
```
优势:
  - 访问速度极快（纯内存访问，无磁盘IO）
  - 不需要序列化/反序列化（状态以Java对象形式存在）
  - 适合状态较小的场景（如几MB到几百MB）

劣势:
  - 状态完全在JVM Heap中 → GC压力大
  - 状态大小受JVM Heap大小限制
  - 每个Backend独立维护自己的状态（不能共享）

数据流:
  读写请求 → HashMapStateBackend → Java HashMap → JVM Heap
  Checkpoint → 序列化到磁盘 → 写入Checkpoint文件
```

**源码阅读重点**：
1. `createKeyedStateBackend()` 如何创建工作Backend
2. 各种State（ValueState/ListState/MapState）的HashMap实现
3. Checkpoint时如何做Snapshot（全量序列化）

#### 文件3：`EmbeddedRocksDBStateBackend.java`（RocksDB Backend）
**路径**：`flink-state-backends/flink-statebackend-rocksdb/`

**核心特点**：
```
优势:
  - 状态存在磁盘上（RocksDB本地文件）
  - 不受JVM Heap限制，可以支持TB级状态
  - 支持增量Checkpoint（只写变化的部分）
  - 写缓存(MemTable)仍然在内存中，读写不慢

劣势:
  - 每次读写需要序列化/反序列化（Java对象 ⇄ bytes）
  - RocksDB本身的内存管理（需要单独配置block cache等）
  - 磁盘IO可能成为瓶颈（需要SSD）

数据流:
  写入: Java对象 → 序列化 → RocksDB MemTable → SST File
  读取: SST File → Block Cache → 反序列化 → Java对象
  Checkpoint: 新创建的SST文件 → Copy到Checkpoint目录（增量）
```

**增量Checkpoint的核心原理**：
```
首次Checkpoint:
  RocksDB SST Files: [sst1, sst2, sst3]
  Checkpoint文件: 全部复制

第二次Checkpoint:
  RocksDB SST Files: [sst1, sst2, sst4(新), sst5(新)]  ← sst3被Compaction了
  Checkpoint文件: 只上传 sst4、sst5（增量！）+ 删除sst3的标记
  Checkpoint大小远小于全量！
```

**源码阅读重点**：
1. `RocksDBKeyedStateBackend` 如何将Key分组到不同的Column Family
2. `RocksDBWriteBatchWrapper` 的批量写入优化
3. `RocksIncrementalSnapshotStrategy` 的增量上传逻辑

### 对比实验（必须做）

```java
// 实验1: 对比Heap vs RocksDB在不同State大小下的性能
// 配置A: HashMapStateBackend
env.setStateBackend(new HashMapStateBackend());

// 配置B: EmbeddedRocksDBStateBackend
env.setStateBackend(new EmbeddedRocksDBStateBackend(true)); // true=增量Checkpoint

// 实验场景: 使用KeyedState记录每个用户的操作次数
// Key数量: [1000, 10000, 100000, 1000000]
// 对比指标:
//   1. Checkpoint耗时
//   2. Checkpoint大小（全量vs增量）
//   3. 读写吞吐量（ops/s）
//   4. JVM GC情况（GCViewer分析）
```

**实验结果记录表**：

| State大小 | HashMap Checkpoint耗时 | RocksDB全量Checkpoint | RocksDB增量Checkpoint | HashMap GC次数 | RocksDB GC次数 |
|-----------|----------------------|---------------------|---------------------|---------------|---------------|
| 10MB | | | | | |
| 100MB | | | | | |
| 1GB | | | | | |
| 10GB | | | | | |

### 第3天强制输出
- HashMapStateBackend vs EmbeddedRocksDBStateBackend的对比分析
- 增量Checkpoint原理图解
- 实验数据报告（上述表格 + 结论）

---

## 第4天：Savepoint与端到端Exactly-Once

### 阅读目标
理解Savepoint的兼容性设计 + Flink + Kafka的端到端Exactly-Once实现

### 第一部分：Savepoint vs Checkpoint

| 对比维度 | Checkpoint | Savepoint |
|----------|-----------|-----------|
| 触发方式 | 自动（定时） | 手动（CLI/API） |
| 生命周期 | 故障恢复后可能被删除 | 长期保存，用户主动删除 |
| 恢复能力 | 恢复到最新状态 | 恢复到任意历史点 |
| 格式兼容性 | 不保证跨版本兼容 | 需要保证跨版本兼容 |
| 存储路径 | 配置的Checkpoint目录 | 用户指定的目录 |
| 所有权 | Flink系统管理 | 用户管理 |

**关键源码**：
- `CheckpointProperties.isSavepoint()` — 判断是否为Savepoint
- Savepoint的额外处理：状态映射（当Job拓扑发生变化时）

**Savepoint兼容性实验**：
```bash
# 1. 运行一个Flink作业
flink run -d my_job.jar

# 2. 触发Savepoint
flink savepoint <jobId> file:///tmp/savepoints/

# 3. 修改作业代码（增加/删除一个算子）

# 4. 从Savepoint恢复
flink run -s file:///tmp/savepoints/savepoint-xxx my_job_v2.jar
# 观察: 哪些算子的状态被恢复了？哪些丢失了？
```

### 第二部分：TwoPhaseCommitSinkFunction — 端到端Exactly-Once

**核心文件**：`flink-streaming-java/src/main/java/org/apache/flink/streaming/api/functions/sink/TwoPhaseCommitSinkFunction.java`

**两阶段提交流程**：
```
阶段1: Pre-Commit（预提交）
  时机: Checkpoint开始时
  操作:
    1. Flush所有待发送的数据（到Kafka的Producer Buffer）
    2. 调用 beginTransaction() 开启Kafka事务
    3. 将所有属于当前Checkpoint的数据写入Kafka（标记为未提交）
    4. 调用 preCommit() 
  
阶段2: Commit（正式提交）  
  时机: Checkpoint完成时（Coordinator通知所有Task）
  操作:
    1. 调用 commit() → Kafka事务提交
    2. 数据变为可见（Consumer可以消费）
  
回滚: Abort
  时机: Checkpoint失败时
  操作:
    1. 调用 abort() → Kafka事务回滚
    2. 未提交的数据被丢弃
```

**具体到Kafka的实现**：`FlinkKafkaProducer.java` 中的 `KafkaTransactionContext`

**一致性验证实验**：
```java
// 实验：验证Exactly-Once
// 1. Flink从Kafka读取1-1000000的数字
// 2. 每个数字写入MySQL（幂等：INSERT ... ON DUPLICATE KEY UPDATE）
// 3. 同时写入Kafka另一个Topic

// 验证方法：
// 在Checkpoint完成后、Commit前，手动Kill TaskManager
// 从上一个Checkpoint恢复
// 检查：
//   1. MySQL中的数据量 = 1,000,000？（无重复无丢失）
//   2. Kafka Sink Topic中的数据量 = 1,000,000？
```

### 端到端Exactly-Once的条件

要使Flink实现端到端Exactly-Once，需要满足：

| 组件 | 条件 | 说明 |
|------|------|------|
| Source | 支持重放 + 可重置Offset | Kafka Source + Checkpoint记录Offset |
| Flink | Checkpoint开启 + State持久化 | 故障后从Checkpoint恢复状态 |
| Sink | 支持事务（两阶段提交）或幂等写入 | Kafka事务Producer / MySQL INSERT ON DUPLICATE |

### 第4天强制输出
- Savepoint兼容性规则总结
- 两阶段提交流程时序图（标注每个阶段的Flink和Kafka交互）
- Exactly-Once验证实验报告

---

## 综合输出要求

### 源码分析文章模板

```markdown
# Flink Checkpoint源码深潜：[本周主题]

## 1. 概述
（一段话总结）

## 2. 核心架构图
（手绘或工具绘制）

## 3. 关键代码分析
### 3.1 代码片段1（带注释）
```java
// 原始代码 + 你的注释
```

### 3.2 代码片段2（带注释）

## 4. 设计模式分析
（这段代码体现了什么设计模式？为什么选择这个模式？）

## 5. 实验验证
- 实验设置：
- 实验数据：
- 结论：

## 6. 与DDIA的关联
（这个设计与DDIA第X章的什么概念相关？）

## 7. 一个仍不理解的问题
```

### 最小阅读代码清单（必须完成）
- [ ] `CheckpointCoordinator.triggerCheckpoint()` 
- [ ] `CheckpointCoordinator.receiveAcknowledgeMessage()`
- [ ] `CheckpointBarrierAligner.processBarrier()` 
- [ ] `CheckpointBarrierUnaligner.processBarrier()`
- [ ] `HashMapStateBackend.createKeyedStateBackend()`
- [ ] `RocksDBKeyedStateBackend` 核心方法
- [ ] `RocksIncrementalSnapshotStrategy` 
- [ ] `TwoPhaseCommitSinkFunction.beginTransaction()` / `preCommit()` / `commit()` / `abort()`

### 进阶阅读（选做，加分的）
- `ChangelogStateBackend`：Flink 1.15+的新StateBackend
- `StateTTL`相关代码：状态过期清理
- `LatencyMarker`机制：端到端延迟测量

---

## 调试技巧：如何本地Debug Flink源码

### 1. IDEA远程Debug Flink集群

```bash
# 在flink-conf.yaml中添加Debug配置
env.java.opts: -agentlib:jdwp=transport=dt_socket,server=y,suspend=n,address=5005

# 或者启动时指定
export FLINK_ENV_JAVA_OPTS="-agentlib:jdwp=transport=dt_socket,server=y,suspend=n,address=5005"
./bin/start-cluster.sh

# IDEA中配置:
# Run → Edit Configurations → + → Remote JVM Debug
# Host: localhost, Port: 5005
```

### 2. 单元测试Debug（推荐方式）

```java
// Flink源码中已有大量单元测试, 直接Debug测试类即可
// 不需要启动完整集群!

// 示例: Debug Checkpoint流程
// 测试类: CheckpointCoordinatorTest.java
// 路径: flink-runtime/src/test/java/org/apache/flink/runtime/checkpoint/

@Test
public void testTriggerCheckpoint() throws Exception {
    // 在这里打断点, 逐步跟踪Checkpoint触发流程
    CheckpointCoordinator coord = new CheckpointCoordinator(...);
    coord.triggerCheckpoint(false);
    // 观察每个步骤的状态变化
}

// 示例: Debug Barrier对齐
// 测试类: CheckpointBarrierAlignerTest.java
@Test
public void testAlignment() throws Exception {
    // 模拟Barrier到达和数据处理
    // 观察通道阻塞和释放过程
}
```

### 3. MiniCluster本地Debug

```java
// 使用Flink的MiniCluster在本地运行完整作业
// 无需启动外部集群, 所有组件在同一个JVM中

StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
env.setParallelism(2);
env.enableCheckpointing(1000);

// 在IDEA中直接Debug运行以下代码
env.fromElements(1, 2, 3, 4, 5)
    .map(x -> x * 2)
    .keyBy(x -> x % 2)
    .sum(0)
    .print();

env.execute("Debug Test");
// 可以在任意算子/Checkpoint代码处打断点
```

### 4. 关键断点位置

| 调试目标 | 断点位置 | 说明 |
|---------|---------|------|
| Checkpoint触发 | `CheckpointCoordinator.triggerCheckpoint()` | 观察触发条件和CheckpointID生成 |
| Barrier注入 | `StreamTask.performCheckpoint()` | 观察Barrier如何注入数据流 |
| Barrier对齐 | `CheckpointBarrierAligner.processBarrier()` | 观察通道阻塞和释放 |
| 状态快照 | `RocksDBKeyedStateBackend.snapshot()` | 观察RocksDB快照过程 |
| 增量Checkpoint | `RocksIncrementalSnapshotStrategy.snapshot()` | 观察增量文件上传 |
| 两阶段提交 | `TwoPhaseCommitSinkFunction.preCommit()` | 观察Kafka事务流程 |
| Task调度 | `Execution.deploy()` | 观察Task如何分配到TaskManager |

### 5. 日志级别调整

```bash
# log4j.properties中调整日志级别
logger.checkpoint.name = org.apache.flink.runtime.checkpoint
logger.checkpoint.level = DEBUG

logger.barrier.name = org.apache.flink.runtime.io.network.api
logger.barrier.level = TRACE

logger.rocksdb.name = org.apache.flink.contrib.streaming.state
logger.rocksdb.level = DEBUG
```

---

## 每周强制输出模板

```markdown
# Flink源码深潜 - 第X天输出

## 本天阅读概要
- 阅读文件数: X个
- 代码行数: X行
- 耗时: X小时
- 核心收获: (一句话)

## 关键代码分析

### 代码片段1: [类名.方法名]
- 文件路径: [完整路径]
- 行号: [起始行-结束行]
- 功能说明: [这段代码做什么]
- 设计模式: [使用了什么设计模式]
- 关键发现: [你发现了什么非显而易见的东西]

```java
// 原始代码 + 你的逐行注释
```

### 代码片段2: [类名.方法名]
(同上格式)

## 架构理解
- 画一个本天阅读代码的架构图(ASCII或手绘拍照)
- 标注核心类之间的关系

## 实验验证
- 实验目标: [验证什么]
- 实验配置: [Flink配置/数据集]
- 实验结果: [截图/数据]
- 结论: [验证了什么/发现了什么]

## 与DDIA的关联
- 本天代码与DDIA第X章的Y概念相关
- 具体关联: [解释]

## 仍不理解的问题
1. [问题1]
2. [问题2]

## 下天计划
- 重点阅读: [文件/类/方法]
- 期望理解: [什么问题]
```

### 每天总结记录表
| 天次 | 阅读文件数 | 代码行数 | 写笔记字数 | 核心收获 |
|------|-----------|----------|-----------|----------|
| 第1天 | | | | |
| 第2天 | | | | |
| 第3天 | | | | |
| 第4天 | | | | |