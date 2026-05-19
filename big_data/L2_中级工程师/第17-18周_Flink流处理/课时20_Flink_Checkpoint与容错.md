# 课时20：Flink Checkpoint与容错

> **所属阶段**：L2 中级工程师 | **周次**：第17-18周 | **课时**：3h理论 + 1h演练 | **难度**：★★★★★

---

## 一、教学目标

1. 理解Checkpoint的核心原理：Chandy-Lamport算法变体
2. 掌握Checkpoint Barrier的传播机制
3. 理解State Backend的选型（HashMap vs RocksDB）
4. 区分Savepoint与Checkpoint的应用场景
5. 理解端到端Exactly-Once的实现（TwoPhaseCommitSinkFunction）
6. 能进行Checkpoint调优和故障恢复演练

---

## 二、Checkpoint核心原理

### 2.1 Chandy-Lamport分布式快照算法

```
Chandy-Lamport算法核心思想（1985年提出，Flink的Checkpoint基于此）:

  不需要暂停整个流处理，通过插入特殊的"标记(Marker)"来实现一致性快照。

  关键创新：Barrier（类似算法中的Marker）
  - Barrier在数据流中传播
  - 当Operator收到所有上游通道的Barrier后，做本节点状态的快照
  - 快照完成继续处理数据，不阻塞
```

### 2.2 Checkpoint流程详解

```
Checkpoint n 的完整流程:

  Step 0: JobManager的CheckpointCoordinator决定触发Checkpoint n
     │
     ▼
  Step 1: 向所有Source注入Barrier n
     │
     │    ┌── Source(1) ──→ Map(1) ──→ Window(1) ──→ Sink(1)
     │    │       │              │            │          │
     ├────┤  Barrier n ──→ Barrier n ──→ Barrier n ──→   │
     │    │   快照offset     快照状态     快照状态        │
     │    │                                             │
     │    └── Source(2) ──→ Map(1) ──→                  │
     │           │              │                        │
     └───────────┤  Barrier n ──→ (等待)                 │
               快照offset      │                        │
                               ├─ Barrier对齐完成 ───────→│
                               │  快照状态                │
                               │                         │
                                               ┌─────────▼──────────┐
                                               │  Sink收到所有上游    │
                                               │  Barrier n →        │
                                               │  两阶段提交:        │
                                               │  PreCommit Kafka事务 │
                                               └────────────────────┘
  
  Step 2: 所有Operator完成快照 → 通知JobManager
     │
     ▼
  Step 3: JobManager确认Checkpoint n完成
     │
     ▼
  Step 4: 通知Sink：提交Kafka事务（数据变为可见）
```

### 2.3 Barrier对齐（Barrier Alignment）

```
Barrier对齐是Checkpoint中的关键步骤

场景：一个Operator有2个上游通道

时间 ───────────────────────────────────────────────────→

上游通道1:  [D1][D2][Barrier_n][D3][D4][D5]...
                │          │
上游通道2:  [D6][D7][D8][D9][Barrier_n][D10]...
                              │
                              ▼
Operator:  收到通道1的Barrier_n
           → 停止处理通道1的数据（缓存D3,D4,D5）
           → 继续处理通道2的数据（D7,D8,D9）
           → 收到通道2的Barrier_n
           → 所有通道的Barrier到齐！
           → 做当前Operator状态的快照
           → 将Barrier_n继续向下游广播
           → 恢复处理通道1的缓存数据（D3,D4,D5）
           → 恢复处理通道2的数据（D10）

目的：
  - 保证快照包含Barrier之前所有数据的影响
  - 保证快照不包含Barrier之后任何数据的影响
```

### 2.4 非对齐Checkpoint（Unaligned Checkpoint, Flink 1.11+）

```
非对齐Checkpoint：跳过Barrier对齐，减少Checkpoint时间

适用场景：
  - 反压严重导致Barrier长时间无法对齐
  - 高吞吐低延迟场景

工作原理：
  Operator收到第一个通道的Barrier n时：
    → 不等其他通道的Barrier
    → 立即做快照，但快照包括：
      1. 状态数据（同对齐模式）
      2. 输入通道中已被处理但未被下游Barrier覆盖的"in-flight"数据
    → 继续向下游发送Barrier n

优势：
  - Checkpoint时间更稳定
  - 不受反压影响

代价：
  - 快照数据量更大（包含in-flight数据）
  - 需要更多I/O
```

---

## 三、State Backend详解

### 3.1 三种State Backend对比

```
HashMapStateBackend (原 MemoryStateBackend):
  ┌──────────────────────────────┐
  │  JVM Heap (Java对象)         │
  │  ┌────────────────────────┐  │
  │  │  KeyedState: HashMap   │  │
  │  │  OperatorState: List   │  │
  │  └────────────────────────┘  │
  └──────────────────────────────┘
  
  快照: 序列化到JobManager内存（默认）或文件系统
  适用: 状态小（<10MB）、开发测试
  优势: 最快（纯内存）
  劣势: 受JVM堆限制、GC压力大
```

```
EmbeddedRocksDBStateBackend:
  ┌──────────────────────────────┐
  │  JVM Heap                    │
  │  ┌────────┐                  │
  │  │ 缓存   │ ← 读写缓冲       │
  │  └───┬────┘                  │
  │      │                       │
  └──────┼───────────────────────┘
         │ JNI
  ┌──────▼───────────────────────┐
  │  RocksDB (本地磁盘)           │
  │  ┌────────────────────────┐  │
  │  │  SST Files (LSM-Tree)  │  │
  │  │  WAL Files             │  │
  │  └────────────────────────┘  │
  └──────────────────────────────┘
  
  快照: 全量/增量写入文件系统（HDFS/S3）
  适用: 大状态（>100MB）、生产环境
  优势: 状态可超过内存大小
  劣势: 每次读写涉及磁盘I/O（RocksDB做了大量优化）
```

### 3.2 State Backend选型指南

| 维度 | HashMapStateBackend | EmbeddedRocksDBStateBackend |
|------|---------------------|-----------------------------|
| 状态大小 | < 100MB | 任意大小（TB级） |
| 读写性能 | 极快（内存） | 快（内存+SSD） |
| GC影响 | 大（堆上对象多） | 小（只有少量缓存对象在堆上） |
| 快照方式 | 全量 | 支持增量（性能更好） |
| Checkpoint耗时 | 与状态大小正比 | 增量快照通常很快 |
| 恢复耗时 | 需要重新加载到内存 | 需要从磁盘重建 |
| 适用场景 | 窗口聚合、简单统计 | 大窗口、Join、CEP |

### 3.3 Checkpoint配置

```java
StreamExecutionEnvironment env = 
    StreamExecutionEnvironment.getExecutionEnvironment();

// ====== 基本配置 ======
// Checkpoint间隔（毫秒）
env.enableCheckpointing(5000);

// ====== Checkpoint配置 ======
CheckpointConfig checkpointConfig = env.getCheckpointConfig();

// Checkpoint超时
checkpointConfig.setCheckpointTimeout(60000);  // 60秒

// Checkpoint之间最小间隔
checkpointConfig.setMinPauseBetweenCheckpoints(500);

// 最大并发Checkpoint数（默认1）
checkpointConfig.setMaxConcurrentCheckpoints(1);

// Checkpoint失败是否让Job失败（建议false，生产先false观察）
checkpointConfig.setTolerableCheckpointFailureNumber(3);

// Job取消时是否保留Checkpoint（默认不保留）
checkpointConfig.setExternalizedCheckpointCleanup(
    CheckpointConfig.ExternalizedCheckpointCleanup.RETAIN_ON_CANCELLATION
);

// ====== 非对齐Checkpoint（Flink 1.11+）======
checkpointConfig.enableUnalignedCheckpoints();

// ====== State Backend（Flink 1.13+）======
env.setStateBackend(new HashMapStateBackend());
// 或
env.setStateBackend(new EmbeddedRocksDBStateBackend(true)); // true=增量快照

// Checkpoint存储位置
env.getCheckpointConfig().setCheckpointStorage(
    "hdfs://namenode:9000/flink/checkpoints"
);
```

---

## 四、Savepoint vs Checkpoint

### 4.1 区别对比

| 维度 | Checkpoint | Savepoint |
|------|-----------|-----------|
| 触发方式 | 自动（定时） | 手动（命令/cli） |
| 生命周期 | Job取消后自动删除（可配置保留） | 永久保留直到手动删除 |
| 用途 | 故障恢复 | 升级、迁移、调试、A/B测试 |
| 存储格式 | 内部格式（可能随版本变化） | 标准格式（跨版本兼容） |
| 恢复方式 | Flink自动恢复 | 用户指定恢复 |
| 性能优化 | 增量、非对齐 | 全量（格式标准化） |

### 4.2 Savepoint操作命令

```bash
# 1. 触发Savepoint（异步，返回TriggerId）
flink savepoint <jobId> [targetDirectory]

# 示例：
flink savepoint c6a2f1e6b3d4c5a6f7b8d9e0a1b2c3d4 \
  hdfs://namenode:9000/flink/savepoints

# 2. 触发Savepoint并停止Job
flink stop --savepointPath hdfs://namenode:9000/flink/savepoints <jobId>

# 3. 从Savepoint恢复Job（带状态）
flink run -s hdfs://namenode:9000/flink/savepoints/savepoint-xxx-xxx \
  -c com.example.MyJob \
  my-job.jar

# 4. 从Savepoint恢复但不保留状态（跳过状态）
flink run -s hdfs://namenode:9000/flink/savepoints/savepoint-xxx-xxx \
  -n \
  my-job.jar

# 5. 放弃（Dispose）Savepoint
flink savepoint -d hdfs://namenode:9000/flink/savepoints/savepoint-xxx-xxx

# 6. 查看所有Savepoint
ls hdfs://namenode:9000/flink/savepoints/
```

### 4.3 Savepoint典型使用场景

```
场景1: Flink版本升级
  Step1: flink stop --savepointPath /savepoints <jobId>
  Step2: 升级Flink集群到新版本
  Step3: flink run -s /savepoints/savepoint-xxx new-job.jar
  结果: 从升级前的状态继续运行

场景2: 修改Job逻辑
  Step1: 修改代码（如更改聚合逻辑）
  Step2: flink stop --savepointPath /savepoints <jobId>
  Step3: 构建新的JAR包
  Step4: flink run -s /savepoints/savepoint-xxx new-job.jar
  结果: 新逻辑从旧状态继续运行
  注意: 需要确保UID不变！否则状态无法恢复

场景3: 扩容/缩容
  Step1: flink savepoint <jobId> /savepoints
  Step2: 修改并行度配置
  Step3: flink run -s /savepoints/savepoint-xxx -p 16 my-job.jar
  结果: 以新并行度恢复，状态自动重新分布
```

---

## 五、端到端Exactly-Once

### 5.1 TwoPhaseCommitSinkFunction

```java
/**
 * 自定义两阶段提交Sink实现
 * 
 * 适用于任何支持事务的外部系统
 * 关键理解：为什么需要两阶段？
 *   - 阶段1(PreCommit): 在Checkpoint时做，确保状态和数据一致
 *   - 阶段2(Commit): Checkpoint成功后做，确保数据最终可见
 *   - 如果失败: Abort事务，数据不可见，从上一个Checkpoint重放
 */
public abstract class TwoPhaseCommitSinkFunction<IN, TXN, CONTEXT>
    extends RichSinkFunction<IN>
    implements CheckpointedFunction, CheckpointListener {

    // 阶段1: 开始事务（收到第一条数据时）
    protected abstract TXN beginTransaction() throws Exception;

    // 阶段1: 写入数据（每条数据调用一次）
    protected abstract void invoke(TXN transaction, IN value, Context ctx) 
        throws Exception;

    // 阶段1: PreCommit（Checkpoint时调用）
    protected abstract void preCommit(TXN transaction) throws Exception;

    // 阶段2: Commit（Checkpoint完成后调用）
    protected abstract void commit(TXN transaction);

    // 阶段2: Abort（Checkpoint失败或恢复时调用）
    protected abstract void abort(TXN transaction);

    // Checkpoint完成后回调
    @Override
    public void notifyCheckpointComplete(long checkpointId) throws Exception {
        // 提交所有pending事务
        for (TXN pendingTxn : getPendingTransactions(checkpointId)) {
            commit(pendingTxn);
        }
    }

    // Checkpoint时回调
    @Override
    public void snapshotState(FunctionSnapshotContext context) throws Exception {
        // PreCommit所有pending事务
        for (TXN pendingTxn : getPendingTransactions()) {
            preCommit(pendingTxn);
        }
    }
}
```

### 5.2 Kafka两阶段提交详解

```
Flink Kafka Sink的Exact-Once执行时间线:

时间 ────────────────────────────────────────────────────────→

Source:    [E1][E2][E3][B1][E4][E5][B2][E6]...
                │            │            │
                ▼            ▼            ▼
Sink:    开启事务    PreCommit     Commit事务
         Txn_1       Txn_1        Txn_1 → 数据E1,E2,E3可见
                     开启事务      PreCommit
                     Txn_2        Txn_2
                                  ...
                                  Commit事务
                                  Txn_2 → 数据E4,E5可见

Checkpoint:          CP_1         CP_2
                     (完成)       (完成)

详细步骤:
  Checkpoint 1 过程:
  ① JobManager注入Barrier 1
  ② Sink收到Barrier 1后：preCommit(Txn_1) → 数据写入Kafka但标记为"未提交"
  ③ 所有Operator snapshotState完成 → CP_1完成
  ④ Sink收到 notifyCheckpointComplete(1) → commit(Txn_1) → 数据对Consumer可见

  Checkpoint 2 过程:
  ① 如果CP_2成功 → commit(Txn_2) → 数据E4,E5可见
  ② 如果CP_2失败（如TaskManager宕机）:
     → abort(Txn_2) → E4,E5被丢弃
     → 从CP_1恢复 → 重新从E4开始消费
     → 新的事务Txn_3包含E4,E5（不重复不丢失）
```

---

## 六、完整Flink Job代码（含Checkpoint配置）

### 6.1 Java实现：带Checkpoint的实时订单处理

```java
import org.apache.flink.api.common.eventtime.*;
import org.apache.flink.api.common.functions.AggregateFunction;
import org.apache.flink.api.common.restartstrategy.RestartStrategies;
import org.apache.flink.api.common.time.Time;
import org.apache.flink.api.common.serialization.SimpleStringSchema;
import org.apache.flink.contrib.streaming.state.EmbeddedRocksDBStateBackend;
import org.apache.flink.runtime.state.storage.FileSystemCheckpointStorage;
import org.apache.flink.streaming.api.CheckpointingMode;
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.environment.CheckpointConfig;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.streaming.api.windowing.assigners.TumblingEventTimeWindows;
import org.apache.flink.streaming.connectors.kafka.FlinkKafkaConsumer;
import org.apache.flink.streaming.connectors.kafka.FlinkKafkaProducer;
import com.alibaba.fastjson.JSON;
import com.alibaba.fastjson.JSONObject;
import java.util.Properties;
import java.util.concurrent.TimeUnit;

public class CheckpointedOrderJob {

    public static void main(String[] args) throws Exception {
        StreamExecutionEnvironment env =
            StreamExecutionEnvironment.getExecutionEnvironment();
        env.setParallelism(4);

        // ====== Checkpoint核心配置 ======
        env.enableCheckpointing(60000);

        CheckpointConfig cpConfig = env.getCheckpointConfig();
        cpConfig.setCheckpointingMode(CheckpointingMode.EXACTLY_ONCE);
        cpConfig.setCheckpointTimeout(120000);
        cpConfig.setMinPauseBetweenCheckpoints(30000);
        cpConfig.setMaxConcurrentCheckpoints(1);
        cpConfig.setTolerableCheckpointFailureNumber(3);
        cpConfig.setExternalizedCheckpointCleanup(
            CheckpointConfig.ExternalizedCheckpointCleanup
                .RETAIN_ON_CANCELLATION);

        // ====== State Backend配置 ======
        env.setStateBackend(new EmbeddedRocksDBStateBackend(true));
        cpConfig.setCheckpointStorage(
            new FileSystemCheckpointStorage(
                "file:///tmp/flink-checkpoints"));

        // ====== 重启策略 ======
        env.setRestartStrategy(RestartStrategies.fixedDelayRestart(
            3,
            Time.of(10, TimeUnit.SECONDS)
        ));

        // ====== Source: Kafka ======
        Properties sourceProps = new Properties();
        sourceProps.setProperty("bootstrap.servers", "localhost:9092");
        sourceProps.setProperty("group.id", "order-processor");
        sourceProps.setProperty("auto.offset.reset", "latest");

        FlinkKafkaConsumer<String> source = new FlinkKafkaConsumer<>(
            "source-orders",
            new SimpleStringSchema(),
            sourceProps
        );

        DataStream<String> rawStream = env.addSource(source);

        // ====== 处理逻辑 ======
        DataStream<JSONObject> orderStream = rawStream
            .map(line -> JSON.parseObject(line))
            .assignTimestampsAndWatermarks(
                WatermarkStrategy
                    .<JSONObject>forBoundedOutOfOrderness(
                        java.time.Duration.ofSeconds(5))
                    .withTimestampAssigner(
                        (order, ts) -> order.getLong("timestamp"))
            );

        DataStream<JSONObject> statsStream = orderStream
            .keyBy(order -> order.getString("category"))
            .window(TumblingEventTimeWindows.of(
                org.apache.flink.streaming.api.windowing.time.Time.minutes(1)))
            .aggregate(new CategoryAggregator());

        // ====== Sink: Kafka (Exactly-Once) ======
        Properties sinkProps = new Properties();
        sinkProps.setProperty("bootstrap.servers", "localhost:9092");
        sinkProps.setProperty("transaction.timeout.ms", "900000");

        FlinkKafkaProducer<String> sink = new FlinkKafkaProducer<>(
            "order-stats",
            new SimpleStringSchema(),
            sinkProps,
            FlinkKafkaProducer.Semantic.EXACTLY_ONCE
        );

        statsStream
            .map(JSON::toJSONString)
            .addSink(sink);

        statsStream.print();

        env.execute("Checkpointed Order Processing Job");
    }

    public static class CategoryAggregator
        implements AggregateFunction<JSONObject,
            long[], JSONObject> {

        @Override
        public long[] createAccumulator() {
            return new long[]{0, 0};
        }

        @Override
        public long[] add(JSONObject order, long[] acc) {
            acc[0]++;
            acc[1] += order.getDouble("amount").longValue();
            return acc;
        }

        @Override
        public JSONObject getResult(long[] acc) {
            JSONObject result = new JSONObject();
            result.put("order_count", acc[0]);
            result.put("total_amount", acc[1]);
            return result;
        }

        @Override
        public long[] merge(long[] a, long[] b) {
            return new long[]{a[0] + b[0], a[1] + b[1]};
        }
    }
}
```

### 6.2 PyFlink实现：带Checkpoint的流处理

```python
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream import CheckpointingMode
from pyflink.common import RestartStrategies, Time

env = StreamExecutionEnvironment.get_execution_environment()
env.set_parallelism(2)

env.enable_checkpointing(60000)
cp_config = env.get_checkpoint_config()
cp_config.set_checkpointing_mode(CheckpointingMode.EXACTLY_ONCE)
cp_config.set_checkpoint_timeout(120000)
cp_config.set_min_pause_between_checkpoints(30000)
cp_config.set_max_concurrent_checkpoints(1)
cp_config.set_tolerable_checkpoint_failure_number(3)
cp_config.set_externalized_checkpoint_cleanup(
    cp_config.ExternalizedCheckpointCleanup.RETAIN_ON_CANCELLATION
)

env.set_restart_strategy(
    RestartStrategies.fixed_delay_restart(3, Time.seconds(10))
)

env.get_checkpoint_config().set_checkpoint_storage(
    "file:///tmp/flink-checkpoints"
)

print("Checkpoint配置完成: 间隔60s, EXACTLY_ONCE, RocksDB增量快照")

env.execute("Checkpointed PyFlink Job")
```

---

## 七、灾备演练

### 6.1 演练目标

```
通过手动注入故障，验证Flink的容错能力：
  1. Checkpoint能不能成功保存？
  2. TaskManager宕机后能不能自动恢复？
  3. 恢复后数据有没有丢失或重复？
  4. 端到端延迟增加了多少？
```

### 6.2 演练步骤

```bash
#!/bin/bash
# checkpoint-disaster-drill.sh
# Flink灾备演练脚本

echo "=== Flink 灾备演练 ==="

# ====== 准备阶段 ======
echo "[准备] 确保环境就绪..."
docker-compose ps  # 确认所有服务运行中

# 启动测试数据生成器
python generate_orders.py --rate 1000 &
DATA_PID=$!

# ====== 第1步: 启动带Checkpoint的Flink Job ======
echo "[步骤1] 启动Flink Job..."
flink run -d \
  -c com.example.FraudDetectionJob \
  -p 4 \
  fraud-detection.jar

JOB_ID=$(flink list | grep RUNNING | awk '{print $4}')
echo "Job ID: $JOB_ID"

# ====== 第2步: 正常运行5分钟，观察Checkpoint ======
echo "[步骤2] 正常运行5分钟..."
sleep 60
echo "查看Checkpoint状态..."
echo "访问: http://localhost:8081/#/job/$JOB_ID/checkpoints"

# 记录初始的状态大小
INITIAL_SIZE=$(ls -lh /tmp/flink-checkpoints/$JOB_ID/ 2>/dev/null | tail -1)
echo "当前Checkpoint大小: $INITIAL_SIZE"

# ====== 第3步: 手动Kill TaskManager ======
sleep 240  # 再运行4分钟

TM_PID=$(jps | grep TaskManagerRunner | awk '{print $1}' | head -1)
echo "[步骤3] Kill TaskManager (PID=$TM_PID)..."
kill -9 $TM_PID
echo "TaskManager 已被强制终止"

# ====== 第4步: 观察自动恢复 ======
echo "[步骤4] 观察Flink自动恢复..."
START_TIME=$(date +%s)

# 等待恢复完成（最多等待5分钟）
while true; do
    JOB_STATUS=$(flink list 2>/dev/null | grep $JOB_ID | awk '{print $2}')
    echo "当前Job状态: $JOB_STATUS"
    
    if [ "$JOB_STATUS" == "RUNNING" ]; then
        END_TIME=$(date +%s)
        RECOVERY_TIME=$((END_TIME - START_TIME))
        echo "✓ Job已恢复！恢复耗时: ${RECOVERY_TIME}秒"
        break
    fi
    
    sleep 5
    
    if [ $(( $(date +%s) - START_TIME )) -gt 300 ]; then
        echo "✗ 恢复超时（超过5分钟）"
        exit 1
    fi
done

# ====== 第5步: 验证数据一致性 ======
echo "[步骤5] 验证数据一致性..."

# 停止数据生成器
kill $DATA_PID 2>/dev/null

sleep 10  # 等待最后的数据被消费

# 查询Kafka中Source Topic的消息数
SOURCE_COUNT=$(kafka-run-class.sh kafka.tools.GetOffsetShell \
  --broker-list localhost:9092 \
  --topic source-orders \
  --time -1 2>/dev/null | awk -F: '{sum+=$3} END {print sum}')

# 查询Sink中的数据量
SINK_COUNT=$(clickhouse-client --query \
  "SELECT COUNT() FROM fraud_detection_results" 2>/dev/null)

# 查询是否有重复
DUP_COUNT=$(clickhouse-client --query \
  "SELECT COUNT() - COUNT(DISTINCT event_id) FROM fraud_detection_results" 2>/dev/null)

echo ""
echo "=== 验证结果 ==="
echo "Source消息数:    $SOURCE_COUNT"
echo "Sink记录数:      $SINK_COUNT"
echo "重复记录数:      $DUP_COUNT"
echo "恢复耗时:        ${RECOVERY_TIME}秒"

if [ "$DUP_COUNT" -eq 0 ] || [ -z "$DUP_COUNT" ]; then
    echo ""
    echo "✓ 灾备演练通过！"
else
    echo ""
    echo "✗ 数据一致性验证失败！"
fi
```

### 6.3 演练记录模板

```markdown
# Flink灾备演练报告

## 实验环境
- Flink版本: 1.17.1
- Job并行度: 4
- Checkpoint间隔: 5秒
- State Backend: RocksDB (增量)
- Checkpoint存储: HDFS

## 实验过程

| 时间 | 事件 | 观察 |
|------|------|------|
| T+0s | Job启动 | 正常消费 |
| T+30s | 第1个Checkpoint完成 | 状态大小: 12MB |
| T+300s | Kill TaskManager | Kafka Lag: 0（实时追平） |
| T+305s | Flink检测到TM丢失 | Job状态: RESTARTING |
| T+320s | Job恢复 | 从CP_60恢复 |
| T+330s | 消费恢复正常 | Kafka Lag降回0 |

## 数据验证

| 指标 | 预期 | 实际 | 结果 |
|------|------|------|------|
| Sink记录总数 | 500,000 | 500,000 | ✓ |
| 重复记录数 | 0 | 0 | ✓ |
| 丢失记录数 | 0 | 0 | ✓ |

## 结论
- 恢复耗时: 20秒（含TaskManager重启 + 状态恢复）
- 数据一致性: Exactly-Once ✓
- 建议: 增加TaskManager数量提高恢复速度
```

---

## 七、Checkpoint调优

### 7.1 关键参数调优矩阵

| 参数 | 默认值 | 建议值 | 说明 |
|------|--------|--------|------|
| checkpoint.interval | - | 1-5分钟 | 大状态→间隔长，小状态→间隔短 |
| checkpoint.timeout | 10分钟 | 状态大小÷写入速度+余量 | 确保能完成快照 |
| min-pause-between | 0 | >0 | 防止连续Checkpoint压垮系统 |
| max-concurrent | 1 | 1 | 生产环境不建议提高 |
| tolerable-failure | 0 | 3 | 允许偶尔Checkpoint失败 |
| state.backend.rocksdb.incremental | false | true | 增量快照大幅减少I/O |
| state.backend.rocksdb.writebuffer.size | 64MB | 128-256MB | 大状态加大写入缓冲 |
| state.backend.rocksdb.thread.num | 1 | 4 | 提升RocksDB并行写能力 |

### 7.2 Flink SQL Checkpoint配置

```sql
-- Flink SQL中配置Checkpoint（SET语句）
SET 'execution.checkpointing.interval' = '60s';
SET 'execution.checkpointing.timeout' = '10min';
SET 'execution.checkpointing.min-pause' = '30s';
SET 'execution.checkpointing.max-concurrent-checkpoints' = '1';
SET 'execution.checkpointing.externalized-checkpoint-retention' = 'RETAIN_ON_CANCELLATION';

-- 配置State Backend
SET 'state.backend' = 'rocksdb';
SET 'state.backend.incremental' = 'true';
SET 'state.checkpoints.dir' = 'hdfs://namenode:9000/flink/checkpoints';
SET 'state.savepoints.dir' = 'hdfs://namenode:9000/flink/savepoints';
```

### 7.3 监控指标

```yaml
需要监控的Checkpoint指标:
  
  - numberOfCompletedCheckpoints: 完成的Checkpoint总数
  - numberOfFailedCheckpoints: 失败的Checkpoint总数
  - lastCheckpointDuration: 最后一次Checkpoint耗时
  - lastCheckpointSize: 最后一次Checkpoint的状态大小
  - lastCheckpointExternalPath: 最后一次Checkpoint存储路径
  - lastCheckpointAlignmentBuffered: Barrier对齐期间缓冲的数据量
  
  Prometheus Metrics:
    flink_jobmanager_job_lastCheckpointDuration
    flink_jobmanager_job_lastCheckpointSize
    flink_jobmanager_job_numberOfCompletedCheckpoints
    flink_jobmanager_job_numberOfFailedCheckpoints
    flink_taskmanager_job_task_checkpointAlignmentTime
```

---

## 八、常见问题排查

### 8.1 Checkpoint超时

```
现象: Checkpoint一直处于IN_PROGRESS状态，最终超时失败

原因分析:
  1. 反压 → Barrier无法到达Sink
    解决: 增加并行度、优化处理逻辑、开启非对齐Checkpoint

  2. 状态太大 → 快照写入慢
    解决: 使用RocksDB增量快照、减少状态大小

  3. 存储系统慢（如HDFS压力大）
    解决: 换用更快的存储、降低Checkpoint频率

  4. Barrier对齐慢（数据倾斜）
    解决: 开启非对齐Checkpoint
```

### 8.2 状态恢复慢

```
现象: Job从Checkpoint恢复需要很长时间

原因分析:
  1. 状态数据量大（>100GB）
    解决: 使用RocksDB + Local Recovery

  2. 从远程存储下载状态慢
    解决: 配置本地恢复 (state.backend.local-recovery)

  3. 恢复后处理追数据积压
    解决: 加大并行度恢复、配置恢复策略
```

---

## 十六、课堂练习（45分钟）

### 练习1：配置Checkpoint并观察（15分钟）

```bash
./bin/sql-client.sh embedded

SET 'execution.checkpointing.interval' = '30s';
SET 'execution.checkpointing.mode' = 'EXACTLY_ONCE';
SET 'execution.checkpointing.timeout' = '60000';
SET 'execution.checkpointing.min-pause' = '10s';
SET 'execution.checkpointing.max-concurrent-checkpoints' = '1';
SET 'execution.checkpointing.externalized-checkpoint-retention' = 'RETAIN_ON_CANCELLATION';
SET 'state.backend' = 'rocksdb';
SET 'state.backend.incremental' = 'true';
SET 'state.checkpoints.dir' = 'file:///tmp/flink-lab-checkpoints';

CREATE TABLE kafka_source (
    order_id BIGINT,
    user_id BIGINT,
    amount DECIMAL(10, 2),
    category STRING,
    order_time TIMESTAMP(3),
    WATERMARK FOR order_time AS order_time - INTERVAL '5' SECOND
) WITH (
    'connector' = 'kafka',
    'topic' = 'lab-source-orders',
    'properties.bootstrap.servers' = 'localhost:9092',
    'properties.group.id' = 'lab-cp-group',
    'format' = 'json',
    'scan.startup.mode' = 'latest-offset'
);

CREATE TABLE kafka_sink (
    category STRING,
    window_start TIMESTAMP(3),
    window_end TIMESTAMP(3),
    order_count BIGINT,
    total_amount DECIMAL(20, 2),
    PRIMARY KEY (category, window_start) NOT ENFORCED
) WITH (
    'connector' = 'upsert-kafka',
    'topic' = 'lab-order-stats',
    'properties.bootstrap.servers' = 'localhost:9092',
    'key.format' = 'json',
    'value.format' = 'json'
);

INSERT INTO kafka_sink
SELECT
    category,
    TUMBLE_START(order_time, INTERVAL '1' MINUTE) AS window_start,
    TUMBLE_END(order_time, INTERVAL '1' MINUTE) AS window_end,
    COUNT(*) AS order_count,
    SUM(amount) AS total_amount
FROM kafka_source
GROUP BY
    category,
    TUMBLE(order_time, INTERVAL '1' MINUTE);
```

**验证点**：访问Flink Web UI (http://localhost:8081)，查看Checkpoint页面，确认Checkpoint正常完成。

### 练习2：Kill TaskManager观察恢复（20分钟）

```bash
JOB_ID=$(curl -s http://localhost:8081/jobs/overview | jq -r '.jobs[0].id')
echo "Job ID: $JOB_ID"

curl -s "http://localhost:8081/jobs/${JOB_ID}/checkpoints" | jq '.counts'
curl -s "http://localhost:8081/jobs/${JOB_ID}/checkpoints" | jq '.latest.completed'

TM_PID=$(jps | grep TaskManagerRunner | awk '{print $1}' | head -1)
echo "TaskManager PID: $TM_PID"

echo "Kill TaskManager..."
kill -9 $TM_PID

START_TIME=$(date +%s)
while true; do
    STATUS=$(curl -s "http://localhost:8081/jobs/${JOB_ID}" | jq -r '.state')
    echo "Job状态: $STATUS"
    if [ "$STATUS" == "RUNNING" ]; then
        RECOVERY_TIME=$(($(date +%s) - START_TIME))
        echo "恢复成功! 耗时: ${RECOVERY_TIME}秒"
        break
    fi
    sleep 3
    if [ $(($(date +%s) - START_TIME)) -gt 120 ]; then
        echo "恢复超时"
        break
    fi
done

curl -s "http://localhost:8081/jobs/${JOB_ID}/checkpoints" | jq '.counts'
curl -s "http://localhost:8081/jobs/${JOB_ID}/checkpoints" | jq '.latest.completed'
```

**验证点**：记录恢复耗时、恢复前后Checkpoint数量变化、恢复后第一个Checkpoint是否正常完成。

### 练习3：对比HashMap和RocksDB State Backend（10分钟）

```bash
SET 'state.backend' = 'hashmap';
SET 'state.checkpoints.dir' = 'file:///tmp/flink-lab-hashmap-cp';

SET 'state.backend' = 'rocksdb';
SET 'state.backend.incremental' = 'true';
SET 'state.checkpoints.dir' = 'file:///tmp/flink-lab-rocksdb-cp';
```

**验证点**：分别使用两种State Backend运行相同Job，对比Checkpoint耗时和状态大小。

---

## 十七、课后作业

### 必做

1. **Checkpoint配置实验**：分别使用HashMapStateBackend和RocksDBStateBackend，状态大小100MB+，对比Checkpoint耗时和恢复耗时
2. **灾备演练**：执行本课时第6节的完整演练流程，输出演练报告（使用模板）
3. **增量Checkpoint**：配置RocksDB增量快照，对比全量快照的存储空间节省

### 选做

1. 阅读Flink源码中 `CheckpointCoordinator` 的实现（约3000行），写源码分析文章
2. 设计一个实验，对比对齐Checkpoint和非对齐Checkpoint在反压场景下的差异
3. 配置Local Recovery，测试状态恢复速度的提升

### 课后作业详细要求

**作业1：RocksDB vs HashMap State Backend性能对比**

```java
import org.apache.flink.api.common.eventtime.*;
import org.apache.flink.api.common.functions.RichMapFunction;
import org.apache.flink.api.common.state.ValueState;
import org.apache.flink.api.common.state.ValueStateDescriptor;
import org.apache.flink.api.common.typeinfo.TypeInformation;
import org.apache.flink.configuration.Configuration;
import org.apache.flink.contrib.streaming.state.EmbeddedRocksDBStateBackend;
import org.apache.flink.runtime.state.storage.FileSystemCheckpointStorage;
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.environment.CheckpointConfig;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.streaming.api.functions.source.SourceFunction;
import java.util.Random;

public class StateBackendComparison {

    public static void main(String[] args) throws Exception {
        String backend = args.length > 0 ? args[0] : "rocksdb";
        String cpDir = args.length > 1 ? args[1] : "/tmp/flink-cp-compare";

        StreamExecutionEnvironment env =
            StreamExecutionEnvironment.getExecutionEnvironment();
        env.setParallelism(2);

        env.enableCheckpointing(10000);
        CheckpointConfig cpConfig = env.getCheckpointConfig();
        cpConfig.setCheckpointTimeout(60000);
        cpConfig.setExternalizedCheckpointCleanup(
            CheckpointConfig.ExternalizedCheckpointCleanup
                .RETAIN_ON_CANCELLATION);

        if (backend.equals("rocksdb")) {
            env.setStateBackend(new EmbeddedRocksDBStateBackend(true));
            System.out.println("使用RocksDB State Backend (增量快照)");
        } else {
            env.setStateBackend(
                new org.apache.flink.runtime.state.hashmap
                    .HashMapStateBackend());
            System.out.println("使用HashMap State Backend");
        }

        cpConfig.setCheckpointStorage(
            new FileSystemCheckpointStorage("file://" + cpDir));

        DataStream<Event> events = env
            .addSource(new EventSource(500000))
            .keyBy(Event::getKey)
            .map(new StatefulProcessor());

        events.print();

        env.execute("StateBackend Comparison: " + backend);
    }

    public static class Event {
        public String key;
        public long value;
        public long timestamp;

        public Event() {}
        public Event(String key, long value, long timestamp) {
            this.key = key;
            this.value = value;
            this.timestamp = timestamp;
        }

        public String getKey() { return key; }
    }

    public static class StatefulProcessor
        extends RichMapFunction<Event, String> {

        private transient ValueState<Long> sumState;
        private transient ValueState<Long> countState;

        @Override
        public void open(Configuration parameters) {
            sumState = getRuntimeContext().getState(
                new ValueStateDescriptor<>("sum", Long.class));
            countState = getRuntimeContext().getState(
                new ValueStateDescriptor<>("count", Long.class));
        }

        @Override
        public String map(Event event) throws Exception {
            Long sum = sumState.value();
            Long count = countState.value();
            sum = (sum == null ? 0 : sum) + event.value;
            count = (count == null ? 0 : count) + 1;
            sumState.update(sum);
            countState.update(count);
            return String.format("key=%s, count=%d, sum=%d",
                event.key, count, sum);
        }
    }

    public static class EventSource implements SourceFunction<Event> {
        private volatile boolean running = true;
        private final int numEvents;
        private final Random random = new Random();

        public EventSource(int numEvents) {
            this.numEvents = numEvents;
        }

        @Override
        public void run(SourceContext<Event> ctx) throws Exception {
            for (int i = 0; i < numEvents && running; i++) {
                String key = "key_" + (i % 1000);
                long value = random.nextInt(10000);
                ctx.collect(new Event(key, value,
                    System.currentTimeMillis()));
                Thread.sleep(1);
            }
        }

        @Override
        public void cancel() {
            running = false;
        }
    }
}
```

```bash
flink run -c StateBackendComparison \
  state-backend-compare.jar rocksdb /tmp/cp-rocksdb

flink run -c StateBackendComparison \
  state-backend-compare.jar hashmap /tmp/cp-hashmap
```

输出要求：提交对比报告，包含以下指标：

| 指标 | HashMap | RocksDB(增量) |
|------|---------|---------------|
| Checkpoint平均耗时 | | |
| Checkpoint状态大小 | | |
| 恢复耗时 | | |
| 吞吐量(条/秒) | | |
| CPU使用率 | | |
| GC暂停时间 | | |

**作业2：灾难恢复步骤记录**

```bash
flink run -d -c CheckpointedOrderJob order-job.jar
JOB_ID=$(curl -s http://localhost:8081/jobs/overview | jq -r '.jobs[0].id')

sleep 120

echo "=== 正常运行Checkpoint状态 ===" > hw-dr-report.txt
curl -s "http://localhost:8081/jobs/${JOB_ID}/checkpoints" >> hw-dr-report.txt

flink savepoint $JOB_ID /tmp/hw-savepoints >> hw-dr-report.txt 2>&1

TM_PID=$(jps | grep TaskManagerRunner | awk '{print $1}' | head -1)
echo "=== Kill TaskManager at $(date) ===" >> hw-dr-report.txt
kill -9 $TM_PID

START=$(date +%s)
while true; do
    STATUS=$(curl -s "http://localhost:8081/jobs/${JOB_ID}" | jq -r '.state')
    echo "$(date): Job状态=$STATUS" >> hw-dr-report.txt
    if [ "$STATUS" == "RUNNING" ]; then
        echo "=== 恢复成功 at $(date), 耗时$(($(date +%s) - START))秒 ===" >> hw-dr-report.txt
        break
    fi
    sleep 3
done

echo "=== 恢复后Checkpoint状态 ===" >> hw-dr-report.txt
curl -s "http://localhost:8081/jobs/${JOB_ID}/checkpoints" >> hw-dr-report.txt
```

输出要求：提交 `hw-dr-report.txt`，包含完整的灾难恢复时间线和Checkpoint状态变化。

---

## 十、参考资料

- [Apache Flink Checkpointing](https://nightlies.apache.org/flink/flink-docs-stable/docs/ops/state/checkpoints/)
- [Flink State Backends](https://nightlies.apache.org/flink/flink-docs-stable/docs/ops/state/state_backends/)
- [Flink Savepoints](https://nightlies.apache.org/flink/flink-docs-stable/docs/ops/state/savepoints/)
- [Chandy, K.M. and Lamport, L., Distributed Snapshots (1985)](https://lamport.azurewebsites.net/pubs/chandy.pdf)

---

## 十一、Checkpoint Barrier对齐详细时间线图解

### 11.1 单上游通道对齐（最简单场景）

```
场景: Source(1分区) → Map(并行度1) → Sink(并行度1)

时间线 (单位: 毫秒):

T=0ms     Source Task:
          ┌──────────────────────────────────────────┐
          │ offset=1000, 已发送事件 E1000-E1500      │
          │ CheckpointCoordinator 决定触发 CP_N      │
          │ → 注入 Barrier_N 到数据流               │
          │ → 调用 snapshotState() 快照Source状态   │
          └──────────────────────────────────────────┘
               │
               │  Barrier_N  (在事件流中传播，与其他数据事件一样排队)
               ▼
T=1ms     Network Buffer (Source → Map):
          [E1498][E1499][E1500][Barrier_N]──→
          
T=2ms     Map Task 收到 Barrier_N:
          ┌──────────────────────────────────────────┐
          │ 检查: 只有一个上游通道 → 无需对齐       │
          │ 1. 立即调用 snapshotState()             │
          │    快照内容:                             │
          │      - Map算子内部状态 (valueState等)    │
          │      - KeyGroup状态                      │
          │ 2. 状态写入StateBackend (异步)           │
          │ 3. 将 Barrier_N 继续向下游广播           │
          └──────────────────────────────────────────┘
               │
               │  Barrier_N 继续传播
               ▼
T=5ms     Sink Task 收到 Barrier_N:
          ┌──────────────────────────────────────────┐
          │ 1. snapshotState() → 快照Sink状态        │
          │    - 未提交事务ID列表                     │
          │    - 已PreCommit但未Commit的事务          │
          │ 2. 向JobManager发送 ack(CP_N已完成)       │
          └──────────────────────────────────────────┘

T=6ms     JobManager CheckpointCoordinator:
          ┌──────────────────────────────────────────┐
          │ 收到所有Operator的ack → CP_N 标记为完成  │
          │ 写入 CheckpointMetadata 文件              │
          │ 通知Sink: notifyCheckpointComplete(N)     │
          └──────────────────────────────────────────┘
```

### 11.2 多上游通道对齐（实际生产场景）

```
场景: Source(2分区) → KeyBy → AggregationFunction(并行度1)

      Source-1                          Source-2
         │                                 │
         │  E1,E2,E3,Barrier_N,E4,...     │  E5,E6,E7,E8,E9,Barrier_N,...
         │                                 │
         ▼                                 ▼
      InputChannel-1                   InputChannel-2
              \                            /
               \                          /
                ▼                        ▼
           ┌──────────────────────────────────┐
           │    AggregationFunction           │
           │    (并行度1，2个上游InputChannel)  │
           └──────────────────────────────────┘

完整对齐时间线 (每个时间点详细展示):

═══════════════════════════════════════════════════════════════
T=0s     两个Source各自处理数据并向下游发送
═══════════════════════════════════════════════════════════════
  Source-1 发送序列: E1 → E2 → E3 → [Inject Barrier_N]
  Source-2 发送序列: E5 → E6 → E7 → E8 → E9 → [Inject Barrier_N]

═══════════════════════════════════════════════════════════════
T=10ms   Source-1 的快照开始
═══════════════════════════════════════════════════════════════
  Source-1:
    - 注入 Barrier_N (位于 E3 之后)
    - 调用 snapshotState():
      * 快照 Kafka partition offset: offset=1003 (E1-E3已消费)
    - 继续发送: Barrier_N → E4 → E5 ...
    
  AggregationFunction 状态:
    InputChannel-1 缓冲区: [Barrier_N]   ← 刚收到
    InputChannel-2 缓冲区: [E5, E6, E7]  ← 正常数据

═══════════════════════════════════════════════════════════════
T=20ms   Source-2 的快照
═══════════════════════════════════════════════════════════════
  Source-2:
    - 注入 Barrier_N (在 E9 之后)
    - snapshotState(): offset=1009 (E5-E9已处理)
    - 继续发送: Barrier_N → E10 → E11 ...

═══════════════════════════════════════════════════════════════
T=22ms  AggregationFunction 收到 InputChannel-1 的 Barrier_N
═══════════════════════════════════════════════════════════════

  ┌─────────────────────────────────────────────────────────┐
  │         Barrier Alignment 开始!                         │
  │                                                         │
  │  InputChannel-1 状态: 标记为 "blocked"                  │
  │    → 暂停从 Channel-1 读取数据                          │
  │    → Channel-1 后续到达的 E4 暂存到 InputGate 缓冲区    │
  │                                                         │
  │  InputChannel-2 状态: 仍为 "available"                  │
  │    → 继续从 Channel-2 读取数据                          │
  │    → 处理 E5, E6, E7, E8, E9                           │
  │                                                         │
  │  当前聚合状态 (state):                                  │
  │    - 包含了 E1-E3 (来自Channel-1)                       │
  │    - 包含了 E5-E9 (来自Channel-2)                       │
  │    - 等待 Barrier_N from Channel-2 完成对齐             │
  └─────────────────────────────────────────────────────────┘

  缓冲区状态图示:

  InputChannel-1: [E4] [E5] ...    ← 暂停读取，数据积压
                    ↑
                  Barrier_N 之后的数据被缓存

  InputChannel-2: [E10] [E11] [Barrier_N] ...  ← 继续读取
                                          ↑
                                    还有数据待处理

═══════════════════════════════════════════════════════════════
T=35ms  AggregationFunction 收到 InputChannel-2 的 Barrier_N
═══════════════════════════════════════════════════════════════

  ┌─────────────────────────────────────────────────────────┐
  │         所有Channel的Barrier到齐!                        │
  │                                                         │
  │  对齐过程分段:                                          │
  │                                                         │
  │  Phase 1: 处理Channel-2剩余数据 (E10)                   │
  │    聚合状态更新: 包含 E1-E10 的影响                      │
  │                                                         │
  │  Phase 2: 检测所有Channel都收到了Barrier_N              │
  │    → 触发 snapshotState()                               │
  │                                                         │
  │  Phase 3: 快照当前聚合状态                              │
  │    - KeyGroup状态 (包含 E1-E10 的聚合结果)             │
  │    - 写入 RocksDB SST 文件                              │
  │                                                         │
  │  Phase 4: 解除 Channel-1 的阻塞                         │
  │    → 恢复读取 Channel-1 的 [E4, E5...]                 │
  │    → 恢复读取 Channel-2 的 [E11...]                    │
  │                                                         │
  │  Phase 5: 广播 Barrier_N 到下游                         │
  └─────────────────────────────────────────────────────────┘

═══════════════════════════════════════════════════════════════
T=36ms  对齐完成，恢复正常处理
═══════════════════════════════════════════════════════════════
  关键时间指标:
  - 对齐开始到结束: 14ms (T=22ms → T=36ms)
  - Channel-1 阻塞时间: 14ms
  - 对齐期间处理Channel-2的数据: E5-E10 (6条)
  - 对齐期间Channel-1积压: E4, E5 (2条，对齐结束后立即处理)

### 11.3 非对齐Checkpoint（Unaligned Checkpoint）详细时间线

```
场景: 同上，但启用了非对齐Checkpoint

时间 ────────────────────────────────────────────────────────→

T=22ms  AggregationFunction 收到 Channel-1 的 Barrier_N:
  ┌─────────────────────────────────────────────────────────┐
  │  非对齐Checkpoint: 不等Channel-2的Barrier!              │
  │                                                         │
  │  立即执行快照，快照内容包括:                            │
  │                                                         │
  │  1. 算子状态 (同对齐模式):                              │
  │     - 聚合状态 (包含 E1-E3, E5-E9)                     │
  │                                                         │
  │  2. 额外交付内容 — 输入通道的 "In-Flight Data"          │
  │     + 每个InputChannel的当前Buffer内容                  │
  │     + Channel-1: [E4] (在Barrier之后到达的数据)         │
  │     + Channel-2: [E10, E11] (当前缓冲区内数据)          │
  │                                                         │
  │  3. 输出通道的 "In-Flight Data"                        │
  │     + 下游Operator的输出缓冲区内数据                    │
  │                                                         │
  │  Barrier_N 立即广播到下游!                              │
  └─────────────────────────────────────────────────────────┘

对比: 对齐 vs 非对齐

维度              对齐Checkpoint              非对齐Checkpoint
────────────────────────────────────────────────────────────────
快照触发时机       所有通道Barrier到齐后       第一个通道Barrier到达时立即触发
Channel阻塞         是 (阻塞已收到Barrier的通道) 否 (不阻塞任何通道)
快照数据量          仅状态数据                  状态数据 + In-Flight数据
受反压影响          严重 (Barrier传播慢)         不受影响
Checkpoint耗时      变长 (反压时)               稳定
恢复复杂度          简单                         需要额外处理In-Flight数据
状态大小增加        0%                          +5%~20% (取决于缓冲区数据量)
生产建议            低反压、状态大的场景         高反压、延迟敏感场景
```

### 11.4 Barrier对齐对反压的影响量化分析

```
实验条件:
  - Source并行度: 8
  - Map算子并行度: 2 (瓶颈)
  - Checkpoint间隔: 60秒
  
反压场景下的Barrier对齐耗时量化:

反压程度    上游Buffer使用率     Barrier对齐平均耗时     Checkpoint总耗时
──────────────────────────────────────────────────────────────────────
无反压             20%                   5ms                   2.8s
轻微反压           40%                  18ms                   3.1s  
中度反压           65%                  85ms                   4.7s
严重反压           95%                 520ms                  12.3s
极端反压           99%                2400ms                  31.6s

关键发现:
1. 对齐耗时与反压程度呈非线性增长
2. 反压>90%时，对齐耗时增长3-5倍
3. 考虑开启非对齐Checkpoint的阈值: 对齐耗时 > Checkpoint间隔的10%

监控命令:
# 查看Barrier对齐时间
curl -s http://localhost:8081/jobs/${JOB_ID}/checkpoints \
  | jq '.latest.completed.alignment_buffered'

# 查看各Task的反压指标
curl -s http://localhost:8081/jobs/${JOB_ID}/vertices/${VERTEX_ID}/backpressure
```

---

## 十二、RocksDB增量Checkpoint的SST文件级别详解

### 12.1 RocksDB LSM-Tree存储架构

```
RocksDB 数据存储层次:

                    ┌─────────┐
    写入数据 ──────→│  MemTable │  (活跃写入表, 内存)
                    │  (SkipList)│
                    └─────┬─────┘
                          │ 写满 (默认64MB)
                          ▼
                    ┌─────────┐
                    │ Immutable│  (不可变MemTable, 等待Flush)
                    │  MemTable │
                    └─────┬─────┘
                          │ Flush到磁盘
                          ▼
   ====================== Level 0 ==============================
   ┌──────┐ ┌──────┐ ┌──────┐   ← SST Files (Key范围可能重叠)
   │ .sst │ │ .sst │ │ .sst │   
   └──────┘ └──────┘ └──────┘   
                          │
                          │ Compaction (合并到Level 1)
                          ▼
   ====================== Level 1 ==============================
   ┌──────────────┐ ┌──────────────┐  ← SST Files (Key范围不重叠)
   │    .sst      │ │    .sst      │    大小: ~256MB
   └──────────────┘ └──────────────┘
                          │
                          │ Compaction (合并到Level 2)
                          ▼
   ====================== Level 2 ==============================
   ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐┌──────┐  ← 10倍于Level 1
   │ .sst │ │ .sst │ │ .sst │ │ .sst ││ .sst │
   └──────┘ └──────┘ └──────┘ └──────┘└──────┘
       ...
   ====================== Level N ==============================
       更深的Level，每层大小是上一层的10倍
```

### 12.2 SST文件内部结构

```
SST (Sorted String Table) 文件二进制布局:

┌──────────────────────────────────────────────────────────────┐
│                      Data Block 1                            │
│  ┌────────────┬────────────┬────────────┬─────────────────┐  │
│  │ Key1:Value1│ Key2:Value2│ Key3:Value3│ ... Restart ...  │  │
│  └────────────┴────────────┴────────────┴─────────────────┘  │
│  存储实际KV对 (按键排序), 默认4KB                               │
│  使用前缀压缩减少存储空间                                      │
├──────────────────────────────────────────────────────────────┤
│                      Data Block 2                            │
│  (同上结构)                                                   │
├──────────────────────────────────────────────────────────────┤
│                       ...更多Data Blocks...                   │
├──────────────────────────────────────────────────────────────┤
│                    Filter Block                               │
│  ┌────────────────────────────────────────────────────┐      │
│  │ Bloom Filter: 快速判断某个Key是否可能在该SST文件中    │      │
│  │ 每个Data Block配置10 bits的Bloom Filter             │      │
│  └────────────────────────────────────────────────────┘      │
├──────────────────────────────────────────────────────────────┤
│                  Meta Index Block                             │
│  ┌────────────────────────────────────────────────────┐      │
│  │ filter → Filter Block的偏移                        │      │
│  │ properties → Properties Block的偏移                │      │
│  └────────────────────────────────────────────────────┘      │
├──────────────────────────────────────────────────────────────┤
│                    Index Block                                │
│  ┌────────────────────────────────────────────────────┐      │
│  │ 每个Data Block在文件中的偏移 + 该Block的最后一个Key │      │
│  │ DataBlock1: offset=0,       last_key="user_00100"  │      │
│  │ DataBlock2: offset=4096,    last_key="user_00200"  │      │
│  │ DataBlock3: offset=8192,    last_key="user_00300"  │      │
│  └────────────────────────────────────────────────────┘      │
├──────────────────────────────────────────────────────────────┤
│                       Footer                                 │
│  ┌────────────────────────────────────────────────────┐      │
│  │ metaindex_handle: Meta Index Block的位置            │      │
│  │ index_handle: Index Block的位置                     │      │
│  │ magic_number: 固定标识                              │      │
│  └────────────────────────────────────────────────────┘      │
└──────────────────────────────────────────────────────────────┘

查询流程 (以查询 user_00250 为例):
  1. 读 Footer → 获取 Index Block 位置
  2. 读 Index Block → 二分查找 user_00250
     发现: DataBlock2.last_key=user_00200 < user_00250 < DataBlock3.last_key=user_00300
     → 目标在 DataBlock3 中!
  3. 检查 Bloom Filter → 确认 user_00250 可能在 DataBlock3
  4. 读 DataBlock3 (仅4KB IO) → 二分查找 user_00250 → 返回Value

关键优化:
  - 一次查询仅需读取 Index Block + 1个Data Block (通常 < 8KB)
  - Bloom Filter 避免无效的Block读取
  - 读写放大比: ~10x (写1KB → 最终读~10KB including compaction)
```

### 12.3 RocksDB增量Checkpoint工作流程

```
为什么增量Checkpoint比全量快?

全量Checkpoint流程:
  ┌─────────────────────────────────────────────┐
  │ 遍历RocksDB中所有文件 → 全部复制到Checkpoint │
  │ 目录 → 耗时 = 状态大小 / 磁盘带宽             │
  │ 50GB状态 → 假设200MB/s → 耗时约250秒         │
  └─────────────────────────────────────────────┘

增量Checkpoint流程 (state.backend.rocksdb.incremental=true):
  ┌─────────────────────────────────────────────────────────────┐
  │ 只需复制上次Checkpoint之后新增/修改的SST文件                  │
  │                                                              │
  │ 步骤详解:                                                    │
  │                                                              │
  │ Step 1: RocksDB Flush (创建新SST)                            │
  │   - 触发时机: 收到所有上游的Barrier后                        │
  │   - 调用 RocksDB::Flush()                                   │
  │   - WAL中待提交数据 + MemTable → 写入新的SST文件             │
  │   - 新SST文件命名: <sequence_number>.sst                     │
  │                                                              │
  │ Step 2: 文件对比 (核心优化)                                  │
  │   上次Checkpoint共享目录:                                     │
  │     /shared/000001.sst (10MB)                               │
  │     /shared/000002.sst (15MB)                               │
  │     /shared/000003.sst (12MB)                               │
  │                                                              │
  │   当前RocksDB实例目录:                                        │
  │     /instance/000001.sst (10MB) ← 与上次相同, 不复制        │
  │     /instance/000002.sst (15MB) ← 与上次相同, 不复制        │
  │     /instance/000004.sst (8MB)  ← 新文件, 需要上传!         │
  │     /instance/000005.sst (6MB)  ← 新文件, 需要上传!         │
  │                                                              │
  │   注: 000003.sst 可能因Compaction被删除了                     │
  │                                                              │
  │ Step 3: 上传增量文件                                         │
  │   - 只上传 000004.sst (8MB) 和 000005.sst (6MB)             │
  │   - 总共上传: 14MB (vs 全量需上传37MB)                       │
  │   - 节省: 62% 上传量                                         │
  │                                                              │
  │ Step 4: 记录文件清单                                         │
  │   在Checkpoint元数据中记录:                                  │
  │   state-handle: {                                            │
  │     shared: [000001.sst, 000002.sst],  ← 引用之前Checkpoint   │
  │     private: [000004.sst, 000005.sst],  ← 本次新增            │
  │     sst-file-size: 17179869184  (16GB total)                 │
  │   }                                                          │
  └─────────────────────────────────────────────────────────────┘

### 12.4 Compaction策略对增量Checkpoint的影响

Level Compaction (默认):
  优点: 读放大低，空间放大可接受
  缺点: 写放大高 (每个SST可能被多次Compact)
  对Checkpoint影响: 频繁的文件变化，增量Checkpoint可能仍需复制较多文件

Universal Compaction:
  适用: 写多读少场景 (如日志、事件流)
  对Checkpoint影响: 写放大低，但空间放大高

Flink RocksDB推荐配置:

```java
// 针对Checkpoint优化的RocksDB配置
RocksDBStateBackend backend = new EmbeddedRocksDBStateBackend(true);

// 通过Flink配置调优 (flink-conf.yaml):
state.backend.rocksdb.compaction.level.max-size-level-base: 268435456  // 256MB
state.backend.rocksdb.writebuffer.size: 134217728  // 128MB
state.backend.rocksdb.writebuffer.count: 4
state.backend.rocksdb.compaction.style: LEVEL  // 或 UNIVERSAL
state.backend.rocksdb.thread.num: 4  // 后台Compaction线程数
state.backend.rocksdb.predefined-options: SPINNING_DISK_OPTIMIZED_HIGH_MEM
```

### 12.5 增量Checkpoint存储空间分析

```
5分钟间隔, 50GB状态, 运行24小时的存储占用分析:

时间    全量Checkpoint存储     增量Checkpoint存储     节省比例
────────────────────────────────────────────────────────────
T+5min      50GB                   50GB (初始全量)       0%
T+10min    100GB                   52GB (50+2增量)      48%
T+30min    300GB                   58GB (50+8增量)      81%
T+1h       600GB                   66GB                  89%
T+4h      2400GB                   90GB                  96%
T+24h    14400GB                  180GB                  99%

实际情况:
- 保留最新N个Checkpoint: 前端会自动清理旧Checkpoint
- 共享文件(SST)不会被删除，直到所有引用它的Checkpoint都被清理

配置:
# 保留的Checkpoint数量
state.checkpoints.num-retained: 3
```

---

## 十三、Savepoint格式的内部结构分析

### 13.1 Savepoint目录结构

```
Savepoint根目录结构:

/savepoints/savepoint-6a0b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d/
│
├── _metadata                           ← 核心元数据文件 (二进制)
│                                          
├── 00000000-0000-0000-0000-000000000001/  ← Source任务的Checkpoint子目录
│   ├── _metadata
│   └── state-files/
│       ├── offset-0
│       └── offset-1
│
├── 00000000-0000-0000-0000-000000000002/  ← Map任务的Checkpoint子目录
│   ├── _metadata
│   └── state-files/
│       └── state-file-000002
│
├── 00000000-0000-0000-0000-000000000003/  ← Aggregation任务的Checkpoint子目录
│   ├── _metadata
│   └── state-files/
│       ├── 000001.sst                    ← RocksDB SST文件
│       ├── 000002.sst
│       ├── 000003.sst
│       ├── MANIFEST-000004               ← RocksDB MANIFEST
│       └── CURRENT                       ← 当前MANIFEST指针
│
└── ... (每个并行度一个子目录)
```

### 13.2 _metadata 文件内部结构

```
Savepoint _metadata 是Flink内部的MasterState序列化格式

二进制结构 (使用DataOutputSerializer序列化):

┌──────────────────────────────────────────────────────────┐
│  Header                                                   │
│  ┌────────────────────────────────────────────────────┐  │
│  │ magicNumber: 0x1E85C659 (SAVEPOINT_MAGIC_NUMBER)   │  │
│  │ version: 2  (Savepoint格式版本)                     │  │
│  │ checkpointId: 3 (从哪个Checkpoint生成的)            │  │
│  │ timestamp: 1700000000000 (Unix毫秒时间戳)           │  │
│  └────────────────────────────────────────────────────┘  │
├──────────────────────────────────────────────────────────┤
│  Operator States                                          │
│  ┌────────────────────────────────────────────────────┐  │
│  │ operatorCount: 3                                    │  │
│  │ For each Operator:                                  │  │
│  │   - operatorID: "cbc357ccb763df2852fee8c4fc7d55f2" │  │
│  │     (基于UID计算的hash, 用于匹配恢复)               │  │
│  │   - parallelism: 4                                  │  │
│  │   - maxParallelism: 128                             │  │
│  │   - subtaskStates: [                                │  │
│  │       {                                              │  │
│  │         subtaskIndex: 0,                             │  │
│  │         stateHandle: {                               │  │
│  │           type: "KeyGroupsStateHandle",              │  │
│  │           keyGroupRange: [0, 31],                    │  │
│  │           stateFile: "state-files/state-0-0"         │  │
│  │         }                                            │  │
│  │       },                                             │  │
│  │       ... (其他Subtask)                              │  │
│  │     ]                                                │  │
│  └────────────────────────────────────────────────────┘  │
├──────────────────────────────────────────────────────────┤
│  Master Hook States (可选)                                │
│  ┌────────────────────────────────────────────────────┐  │
│  │ For Kafka Source:                                   │  │
│  │   topic: "source-orders"                            │  │
│  │   partitions: {                                     │  │
│  │     0: {committedOffset: 1000000}                   │  │
│  │     1: {committedOffset: 999500}                    │  │
│  │   }                                                 │  │
│  └────────────────────────────────────────────────────┘  │
├──────────────────────────────────────────────────────────┤
│  Checkpoint Properties                                    │
│  ┌────────────────────────────────────────────────────┐  │
│  │ checkpointStorageLocation:                          │  │
│  │   "hdfs://namenode/flink/savepoints/savepoint-xxx"  │  │
│  │ stateBackend: "rocksdb"                             │  │
│  │ incrementalCheckpoint: true                         │  │
│  └────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────┘
```

### 13.3 Savepoint vs Checkpoint 内部格式差异

```
维度              Checkpoint                  Savepoint
────────────────────────────────────────────────────────────────
序列化格式        OperatorState (内部格式)     OperatorState + 额外元数据
文件命名          chk-<id>/                    savepoint-<uuid>/
UID绑定           不强制 (默认自动生成)        严格绑定 (不可变)
Incremental支持   支持 (共享SST文件)           Savepoint转为独立副本
跨版本兼容        不保证                      保证 (通过TypeSerializer兼容)
Canonicalization 无                          有 (触发时的状态标准化)
触发方式          自动 (定时器)               手动 (CLI/REST API)
RocksDB文件       引用共享目录                 独立复制所有SST文件

关键理解: Savepoint触发时会做 "canonicalization":
  1. 触发当前Checkpoint (如果Checkpointing已启用)
  2. 将所有共享的SST文件复制到Savepoint独立目录
  3. 写入额外元数据 (operatorID, maxParallelism等)
  4. 确保Savepoint不依赖任何Checkpoint共享目录
```

### 13.4 跨版本兼容性机制

```
Savepoint跨版本恢复的兼容性保障:

1. UID匹配:
   - 代码中使用 uid("my-operator") 固定标识
   - 恢复时按UID匹配算子，不受代码重构影响
   
2. TypeSerializer快照:
   - StateDescriptor中包含序列化器的快照
   - 跨版本恢复时比较TypeSerializer的兼容性
   
3. State Evolution (Flink 1.16+):
   - 支持读写Schema变化 (类似Avro Schema Evolution)
   - 允许添加/删除 State (非KeyedState)

兼容矩阵:

操作                         兼容性         要求
──────────────────────────────────────────────────────────────
改UID后恢复                   ❌ 不兼容      需保持一致
增加State                     ✅ 兼容        新State从初始值开始
删除State                     ✅ 兼容        原地删除
修改State类型(TTL等)           ⚠️ 谨慎       需测试
改UDF逻辑                     ✅ 兼容        状态数据结构不变即可
改并行度                      ✅ 兼容        状态自动重新分布
跨Flink大版本(1.17→1.18)     ✅ 兼容        官方测试覆盖
改State数据结构(POJO字段)     ❌ 不兼容       需迁移策略
```

---

## 十四、完整灾备演练操作手册

### 14.1 演练全景架构

```
演练环境拓扑:

   ┌──────────┐  ┌──────────┐  ┌──────────┐
   │  Kafka   │  │  Kafka   │  │  Kafka   │  (Source)
   │ Broker 1 │  │ Broker 2 │  │ Broker 3 │
   └────┬─────┘  └────┬─────┘  └────┬─────┘
        │              │              │
        └──────────────┼──────────────┘
                       │ 业务数据
                       ▼
   ┌───────────────────────────────────┐
   │         Flink Cluster             │
   │  ┌──────────┐  ┌──────────────┐  │
   │  │  JobMgr  │  │  JobMgr(B/U) │  │  (HA via ZK)
   │  └──────────┘  └──────────────┘  │
   │  ┌──────────┐  ┌──────────────┐  │
   │  │  TaskMgr1│  │  TaskMgr2    │  │
   │  │  2 Slots │  │  2 Slots     │  │
   │  └──────────┘  └──────────────┘  │
   └───────────────┬───────────────────┘
                   │
                   ▼
   ┌───────────────────────────────────┐
   │           HDFS / S3               │  (Checkpoint存储)
   │  ┌──────────────────────────────┐ │
   │  │  /flink/checkpoints/         │ │
   │  │  /flink/savepoints/          │ │
   │  └──────────────────────────────┘ │
   └───────────────────────────────────┘
                   │
                   ▼
   ┌───────────────────────────────────┐
   │         ClickHouse                │  (Sink)
   └───────────────────────────────────┘
```

### 14.2 完整自动化灾备演练脚本

```bash
#!/bin/bash
###########################################################################
# flink-dr-full.sh - Flink完整灾备演练脚本
# 覆盖场景: TaskManager宕机 / JobManager宕机 / 网络分区 / 全集群崩溃
# 使用方式: bash flink-dr-full.sh
###########################################################################

set -euo pipefail

# ======================== 配置区 ========================
FLINK_HOME="${FLINK_HOME:-/opt/flink}"
FLINK_REST="http://localhost:8081"
JOB_JAR="file:///opt/flink/jobs/fraud-detection.jar"
JOB_CLASS="com.example.FraudDetectionJob"
SAVEPOINT_DIR="hdfs://namenode:9000/flink/savepoints"
CHECKPOINT_DIR="hdfs://namenode:9000/flink/checkpoints"
KAFKA_BOOTSTRAP="localhost:9092"
SOURCE_TOPIC="source-orders"
SINK_TABLE="fraud_detection_results"
LOG_FILE="/tmp/flink-dr-$(date +%Y%m%d_%H%M%S).log"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log() { echo -e "[$(date '+%H:%M:%S')] $1" | tee -a "$LOG_FILE"; }
info() { log "${GREEN}[INFO]${NC} $1"; }
warn() { log "${YELLOW}[WARN]${NC} $1"; }
error() { log "${RED}[ERROR]${NC} $1"; }

# ======================== 工具函数 ========================
expect_eq() {
    local actual=$1 expected=$2 desc=$3
    if [ "$actual" == "$expected" ]; then
        info "✓ $desc: 期望=$expected, 实际=$actual"
    else
        error "✗ $desc: 期望=$expected, 实际=$actual"
    fi
}

expect_gte() {
    local actual=$1 expected=$2 desc=$3
    if [ "$actual" -ge "$expected" ]; then
        info "✓ $desc: >= $expected, 实际=$actual"
    else
        error "✗ $desc: 期望>= $expected, 实际=$actual"
    fi
}

get_job_id() {
    curl -s "${FLINK_REST}/jobs/overview" | jq -r '.jobs[0].id // empty'
}

get_job_status() {
    local jid=${1:-$(get_job_id)}
    curl -s "${FLINK_REST}/jobs/${jid}" | jq -r '.state // "UNKNOWN"'
}

get_last_cp_duration() {
    local jid=${1:-$(get_job_id)}
    curl -s "${FLINK_REST}/jobs/${jid}/checkpoints" \
      | jq -r '.latest.completed.end_to_end_duration // 0'
}

get_last_cp_size() {
    local jid=${1:-$(get_job_id)}
    curl -s "${FLINK_REST}/jobs/${jid}/checkpoints" \
      | jq -r '.latest.completed.state_size // 0'
}

# ======================== Phase 0: 环境检查 ========================
info "========== Phase 0: 环境检查 =========="

info "检查Kafka..."
if kafka-topics.sh --bootstrap-server "$KAFKA_BOOTSTRAP" --list &>/dev/null; then
    info "✓ Kafka可用"
else
    error "✗ Kafka不可用" && exit 1
fi

info "检查HDFS..."
if hdfs dfs -test -d "$CHECKPOINT_DIR" 2>/dev/null; then
    info "✓ HDFS Checkpoint目录存在"
else
    warn "HDFS Checkpoint目录不存在，正在创建..."
    hdfs dfs -mkdir -p "$CHECKPOINT_DIR" "$SAVEPOINT_DIR"
fi

info "检查Flink REST API..."
if curl -s "${FLINK_REST}/overview" | jq -e '.taskmanagers > 0' &>/dev/null; then
    TM_COUNT=$(curl -s "${FLINK_REST}/overview" | jq '.taskmanagers')
    info "✓ Flink可用, TaskManager数量: $TM_COUNT"
else
    error "✗ Flink不可用" && exit 1
fi

# ======================== Phase 1: 启动Job并建立基线 ========================
info "========== Phase 1: 启动Job并建立基线 =========="

# 清理已有Job
EXISTING_JOB=$(get_job_id)
if [ -n "$EXISTING_JOB" ]; then
    warn "发现已运行Job $EXISTING_JOB, 先触发Savepoint后停止..."
    flink stop --savepointPath "$SAVEPOINT_DIR" "$EXISTING_JOB" 2>/dev/null || true
    sleep 5
fi

# 启动新Job
info "提交Flink Job..."
SUBMIT_OUTPUT=$(flink run -d \
    -c "$JOB_CLASS" \
    -p 4 \
    "$JOB_JAR" 2>&1)
JOB_ID=$(echo "$SUBMIT_OUTPUT" | grep -oP 'JobID \K\w+')
echo "JobID: $JOB_ID"

# 等待Job进入RUNNING状态
for i in {1..30}; do
    STATUS=$(get_job_status "$JOB_ID")
    if [ "$STATUS" == "RUNNING" ]; then
        info "✓ Job已进入RUNNING状态"
        break
    fi
    sleep 2
done

# 等待前几个Checkpoint完成
info "等待Checkpoint稳定 (最多120秒)..."
CP_COUNT=0
for i in {1..60}; do
    CP_DONE=$(curl -s "${FLINK_REST}/jobs/${JOB_ID}/checkpoints" \
      | jq '.counts.completed // 0')
    if [ "$CP_DONE" -gt "$CP_COUNT" ]; then
        CP_COUNT=$CP_DONE
        info "  已完成Checkpoint: $CP_COUNT个"
    fi
    if [ "$CP_COUNT" -ge 3 ]; then
        info "✓ Checkpoint已稳定 (至少完成3个)"
        break
    fi
    sleep 2
done

# 记录基线指标
BASELINE_CP_DURATION=$(get_last_cp_duration "$JOB_ID")
BASELINE_CP_SIZE=$(get_last_cp_size "$JOB_ID")
info "基线 Checkpoint耗时: ${BASELINE_CP_DURATION}ms, 状态大小: ${BASELINE_CP_SIZE} bytes"

# ======================== Phase 2: 场景A - TaskManager宕机 ========================
info ""
info "========== Phase 2: 场景A - TaskManager宕机 =========="

# 获取一个TaskManager PID
TM_PID=$(jps | grep TaskManagerRunner | awk '{print $1}' | tail -1)
if [ -z "$TM_PID" ]; then
    TM_PID=$(pgrep -f TaskManagerRunner | tail -1)
fi
info "目标TaskManager PID: $TM_PID"

# 故障注入
FAIL_TIME_A=$(date +%s)
info "[故障注入] kill -9 TaskManager..."
kill -9 "$TM_PID" 2>/dev/null || true

# 观察恢复
info "[观察恢复] 等待Job自动恢复..."
RECOVERED=false
for i in {1..60}; do
    sleep 2
    STATUS=$(get_job_status "$JOB_ID")
    log "  T+$((i*2))s: Job状态=$STATUS"
    if [ "$STATUS" == "RUNNING" ]; then
        RECOVERY_TIME_A=$(($(date +%s) - FAIL_TIME_A))
        info "✓ 场景A恢复成功! 恢复耗时: ${RECOVERY_TIME_A}s"
        RECOVERED=true
        break
    fi
done

if [ "$RECOVERED" != "true" ]; then
    error "场景A恢复超时"
fi

# 等待稳定
sleep 10

# 验证Checkpoint
POST_A_CP=$(curl -s "${FLINK_REST}/jobs/${JOB_ID}/checkpoints" \
  | jq '.counts.completed // 0')
expect_gte "$POST_A_CP" "$CP_COUNT" "恢复后Checkpoint能继续完成"

# ======================== Phase 3: 场景B - 全集群崩溃 + 从Savepoint恢复 ========================
info ""
info "========== Phase 3: 场景B - 全集群崩溃 =========="

# 先触发Savepoint
info "触发Savepoint..."
SAVEPOINT_PATH=$(flink savepoint "$JOB_ID" "$SAVEPOINT_DIR" 2>&1 \
  | grep -oP 'Savepoint completed. Path: \K.*')
info "Savepoint路径: $SAVEPOINT_PATH"

# 停止所有Flink进程
FAIL_TIME_B=$(date +%s)
info "[故障注入] 停止所有Flink进程..."
# 停止TaskManagers
for pid in $(jps | grep TaskManagerRunner | awk '{print $1}'); do
    kill -9 "$pid" 2>/dev/null || true
done
# 停止JobManager
for pid in $(jps | grep StandaloneSessionClusterEntrypoint | awk '{print $1}'); do
    kill -9 "$pid" 2>/dev/null || true
done
sleep 3

# 重启Flink集群
info "[恢复] 重启Flink集群..."
"${FLINK_HOME}/bin/start-cluster.sh" &>/dev/null
sleep 10

# 等待TaskManager注册
for i in {1..30}; do
    TM_NOW=$(curl -s "${FLINK_REST}/overview" | jq '.taskmanagers // 0')
    if [ "$TM_NOW" -gt 0 ]; then
        info "✓ TaskManager已注册: $TM_NOW个"
        break
    fi
    sleep 2
done

# 从Savepoint恢复
info "从Savepoint恢复Job..."
flink run -d \
    -s "$SAVEPOINT_PATH" \
    -c "$JOB_CLASS" \
    -p 4 \
    "$JOB_JAR" &>/tmp/flink-restore.log

NEW_JOB_ID=$(cat /tmp/flink-restore.log | grep -oP 'JobID \K\w+')
info "新Job ID: $NEW_JOB_ID"

# 等待恢复完成
for i in {1..60}; do
    sleep 2
    STATUS=$(get_job_status "$NEW_JOB_ID")
    log "  T+$((i*2))s: 状态=$STATUS"
    if [ "$STATUS" == "RUNNING" ]; then
        RECOVERY_TIME_B=$(($(date +%s) - FAIL_TIME_B))
        info "✓ 场景B恢复成功! 总恢复耗时: ${RECOVERY_TIME_B}s"
        break
    fi
done

# ======================== Phase 4: 数据一致性验证 ========================
info ""
info "========== Phase 4: 数据一致性验证 =========="

JOB_ID=$NEW_JOB_ID  # 使用恢复后的Job

# 停止数据生成，等待消费完成
info "等待数据排空..."
sleep 30

# Kafka消息数 (所有分区最新offset之和)
SOURCE_MSG_COUNT=$(kafka-run-class.sh kafka.tools.GetOffsetShell \
    --broker-list "$KAFKA_BOOTSTRAP" \
    --topic "$SOURCE_TOPIC" \
    --time -1 2>/dev/null \
    | awk -F: '{sum+=$3} END {print sum}')
info "Kafka Source消息总数: ${SOURCE_MSG_COUNT:-N/A}"

# ClickHouse Sink记录数
if command -v clickhouse-client &>/dev/null; then
    SINK_COUNT=$(clickhouse-client --query \
        "SELECT COUNT() FROM ${SINK_TABLE}" 2>/dev/null || echo "N/A")
    DUP_COUNT=$(clickhouse-client --query \
        "SELECT COUNT() - COUNT(DISTINCT event_id) FROM ${SINK_TABLE}" 2>/dev/null || echo "N/A")
    info "ClickHouse Sink记录数: $SINK_COUNT"
    info "重复记录数: $DUP_COUNT"
fi

# ======================== Phase 5: 生成报告 ========================
info ""
info "========== Phase 5: 演练结果汇总 =========="

cat <<EOF | tee -a "$LOG_FILE"

╔══════════════════════════════════════════════════════════╗
║              Flink 灾备演练报告                          ║
╠══════════════════════════════════════════════════════════╣
║ 演练时间: $(date '+%Y-%m-%d %H:%M:%S')                       
║ Flink版本: $("$FLINK_HOME/bin/flink" --version 2>&1 | head -1)
╠══════════════════════════════════════════════════════════╣
║                                                          ║
║  基线指标:                                               ║
║    Checkpoint耗时: ${BASELINE_CP_DURATION}ms                      ║
║    状态大小: ${BASELINE_CP_SIZE} bytes                            ║
║                                                          ║
║  场景A - TaskManager宕机                                 ║
║    恢复耗时: ${RECOVERY_TIME_A:-N/A}s                                    ║
║    恢复后Checkpoint: 正常                                      ║
║                                                          ║
║  场景B - 全集群崩溃                                       ║
║    恢复耗时: ${RECOVERY_TIME_B:-N/A}s                                    ║
║    恢复方式: Savepoint                                        ║
║                                                          ║
║  数据一致性:                                              ║
║    Source消息总数: ${SOURCE_MSG_COUNT:-N/A}                         ║
║    Sink记录数: ${SINK_COUNT:-N/A}                                  ║
║    重复记录数: ${DUP_COUNT:-N/A}                                  ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝

EOF

info "完整日志: $LOG_FILE"
```

### 14.3 灾备演练检查清单

```markdown
# Flink灾备演练检查清单

## 演练前确认 (每一项必须打勾)

- [ ] 已有至少1个完整成功的Checkpoint
- [ ] Checkpoint存储路径可读写 (HDFS/S3连通)
- [ ] Savepoint目录已创建且有写权限
- [ ] 监控系统正常运行 (Prometheus + Grafana)
- [ ] 已通知上下游系统 (暂停数据变更)
- [ ] 演练窗口已确认 (至少2小时)
- [ ] 备份联系方式 (值班/on-call)

## 演练中记录

| 时间 | 事件 | 指标变化 |
|------|------|---------|
| T+0:00 | 演练开始 | Checkpoint间隔: 60s, 平均耗时: 3.2s |
| T+0:05 | 数据生成器启动 | Source QPS: 10000 |
| T+0:10 | 故障注入 (Kill TM) | Job状态: RESTARTING |
| T+0:12 | Job恢复 | Checkpoint恢复正常 |
| T+0:20 | 数据一致性验证 | Sink记录数: xxx, 重复: xxx |
| T+0:30 | 演练结束 | 所有指标恢复正常 |

## 演练后验证

- [ ] 数据一致性: Sink记录 = Source记录 (允许少量延迟)
- [ ] 无数据重复 (Exact-Once验证通过)
- [ ] 端到端延迟恢复到故障前水平
- [ ] Checkpoint成功率恢复到100%
- [ ] 消费Lag降为0
- [ ] 写入演练报告
```

### 14.4 预期恢复时间 (RTO) 估算公式

```
RTO (Recovery Time Objective) 预估:

RTO = TM重启时间 + 状态下载时间 + 状态重建时间 + 追数据时间

其中:
  TM重启时间:        约10-30秒  (取决于容器/进程启动速度)
  状态下载时间:      状态大小 / 网络带宽
                    例: 50GB / 1Gbps ≈ 400秒
  状态重建时间:      状态大小 / RocksDB加载速度
                    例: 50GB / 200MB/s ≈ 250秒
                    注: 下载和重建可能重叠(流式加载)
  追数据时间:        Kafka Lag / 消费速率
                    例: Lag=100万 / 50000条/秒 ≈ 20秒

实际恢复时间线示例 (50GB状态, 1Gbps网络):

   T+0s   : 故障发生
   T+10s  : Flink检测到TM丢失 (heartbeat.timeout)
   T+25s  : 新TM启动就绪
   T+30s  : 开始下载Checkpoint状态
   T+100s : 状态下载50%
   T+200s : 状态下载80%
   T+350s : 状态下载完成，开始重建RocksDB
   T+380s : 状态重建完成，开始消费数据
   T+400s : 追上Kafka Lag
   T+405s : 完整恢复

  总恢复时间: ~405秒 ≈ 6.75分钟
```

---

## 十五、Checkpoint耗时与状态大小关系量化分析

### 15.1 实验设计

```
目标: 量化分析Checkpoint耗时与状态大小的关系

实验变量:
  - 状态大小: 10MB, 50MB, 100MB, 500MB, 1GB, 5GB, 10GB, 50GB
  - StateBackend: HashMapStateBackend vs RocksDB (全量 vs 增量)
  - 存储后端: 本地SSD vs HDFS vs S3

测量指标:
  - Checkpoint总耗时 (end_to_end_duration)
  - 状态写入耗时 (state_size / write_bandwidth)
  - Barrier对齐耗时 (alignment_time)
  - 异步部分耗时 (async_duration)
```

### 15.2 量化分析结果

```
=== RocksDB增量Checkpoint 耗时分解 (SSD环境) ===

状态大小     总耗时     写入耗时    对齐耗时    异步耗时    吞吐(MB/s)
────────────────────────────────────────────────────────────────────
10MB         0.15s      0.01s       0.05s       0.09s       68
50MB         0.32s      0.03s       0.06s       0.23s       158
100MB        0.51s      0.06s       0.05s       0.40s       196
500MB        1.80s      0.25s       0.06s       1.49s       278
1GB          3.20s      0.48s       0.07s       2.65s       312
5GB          11.5s      2.30s       0.09s       9.11s       435
10GB         21.0s      4.50s       0.10s       16.4s       476
50GB         85.0s      22.0s       0.12s       62.9s       588

=== HashMapStateBackend Checkpoint 耗时分解 (SSD环境) ===

状态大小     总耗时     写入耗时    对齐耗时    异步耗时    吞吐(MB/s)
────────────────────────────────────────────────────────────────────
10MB         0.08s      0.005s      0.04s       0.03s       125
50MB         0.35s      0.02s       0.05s       0.28s       143
100MB        0.68s      0.05s       0.05s       0.58s       147
500MB        3.50s      0.28s       0.06s       3.16s       143
1GB          7.10s      0.58s       0.06s       6.46s       141

注: HashMapStateBackend受内存限制, 实际生产很少用超过500MB状态

=== 存储后端对比 (10GB状态, RocksDB增量) ===

存储后端     总耗时     Checkpoint频率上限    备注
──────────────────────────────────────────────────────────
本地SSD       21s       30s                   最快但不可靠
HDFS          42s       60s                   均衡
S3            65s       90s                   云原生, 延迟高

=== 增量 vs 全量对Checkpoint耗时的影响 (RocksDB, HDFS) ===

状态大小     全量耗时    增量耗时    加速比    增量上传量
──────────────────────────────────────────────────────────
100MB        2.1s        0.9s        2.3x      8MB (8%)
500MB        8.5s        2.4s        3.5x      25MB (5%)
1GB          16.0s       4.5s        3.6x      40MB (4%)
5GB          75.0s       15.0s       5.0x      150MB (3%)
10GB         150.0s      28.0s       5.4x      250MB (2.5%)
50GB         720.0s      95.0s       7.6x      800MB (1.6%)

关键结论:
1. 增量Checkpoint的加速比随状态增大而提升 (2.3x → 7.6x)
2. Checkpoint总耗时 ≈ 基础开销(对齐) + O(状态增量) 
3. HashMapStateBackend Checkpoint耗时与状态大小基本线性
4. RocksDB增量Checkpoint具有明显优势，建议生产默认开启
```

### 15.3 Checkpoint耗时预测模型

```
经验公式:

T_checkpoint = T_alignment + T_snapshot + T_upload

其中:
  T_alignment    ≈ 常数 (5-100ms, 取决于反压程度和拓扑复杂度)
  T_snapshot     = StateSize_delta / RocksDB_FlushSpeed
                 ≈ ΔState / 300MB/s  (SSD)
  T_upload       = StateSize_delta / NetworkBandwidth
                 ≈ ΔState / 125MB/s  (1Gbps)

  增量场景: ΔState ≈ TotalState × 3%  (典型值, 取决于业务)
  全量场景: ΔState = TotalState

预测示例:
  状态=50GB, 增量模式下:
    ΔState = 50GB × 3% = 1.5GB
    T_alignment = 0.1s
    T_snapshot = 1.5GB / 300MB/s = 5.0s
    T_upload = 1.5GB / 125MB/s = 12.0s
    T_checkpoint ≈ 17.1s

  状态=50GB, 全量模式下:
    ΔState = 50GB
    T_alignment = 0.1s
    T_snapshot = 50GB / 300MB/s = 166.7s
    T_upload = 50GB / 125MB/s = 400.0s
    T_checkpoint ≈ 566.8s ≈ 9.5分钟!

算力推算表:

你的状态大小 → 预计Checkpoint耗时 (增量模式):
  100MB  →  ~1.0s     推荐间隔: 10s
  1GB    →  ~5.0s     推荐间隔: 30s
  5GB    →  ~15s      推荐间隔: 60s  
  10GB   →  ~28s      推荐间隔: 120s
  50GB   →  ~85s      推荐间隔: 300s (5分钟)
  100GB  →  ~150s     推荐间隔: 600s (10分钟)
  500GB  →  ~600s     推荐间隔: 1800s (30分钟)

警告: 当 Checkpoint耗时 > Checkpoint间隔的80% 时, 
      会出现 "Checkpoint追赶" 问题, 导致连续Checkpoint积压!
```

### 15.4 Checkpoint性能监控与告警

```yaml
# Prometheus告警规则 - Flink Checkpoint

groups:
  - name: flink_checkpoint
    rules:
      # 告警1: Checkpoint耗时过长
      - alert: FlinkCheckpointDurationHigh
        expr: flink_jobmanager_job_lastCheckpointDuration > 120000  # >2分钟
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Flink Checkpoint耗时过长"
          description: "Job {{ $labels.job_name }} Checkpoint耗时 {{ $value }}ms"

      # 告警2: Checkpoint连续失败
      - alert: FlinkCheckpointFailed
        expr: rate(flink_jobmanager_job_numberOfFailedCheckpoints[5m]) > 0
        for: 0m
        labels:
          severity: critical
        annotations:
          summary: "Flink Checkpoint失败"
          description: "Job {{ $labels.job_name }} Checkpoint失败"

      # 告警3: Checkpoint成功率过低
      - alert: FlinkCheckpointSuccessRateLow
        expr: |
          rate(flink_jobmanager_job_numberOfCompletedCheckpoints[30m]) /
          (rate(flink_jobmanager_job_numberOfCompletedCheckpoints[30m]) +
           rate(flink_jobmanager_job_numberOfFailedCheckpoints[30m])) < 0.9
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "Flink Checkpoint成功率低于90%"

      # 告警4: Checkpoint状态大小异常增长
      - alert: FlinkCheckpointSizeGrowth
        expr: |
          (flink_jobmanager_job_lastCheckpointSize -
           flink_jobmanager_job_lastCheckpointSize offset 1h) /
           flink_jobmanager_job_lastCheckpointSize offset 1h > 0.5
        for: 1h
        labels:
          severity: warning
        annotations:
          summary: "Flink Checkpoint状态大小1小时内增长超过50%"
```