# Kafka源码深潜路线

> **目标**：深入Kafka Producer和Broker核心源码，理解高吞吐和持久化的底层实现
>
> **周期**：第25周（与Flink源码并行） | **强制输出**：1篇源码分析文章（2000+字）

---

## Kafka源码整体架构

```
┌─────────────────────────────────────────────────────┐
│                     Kafka Cluster                    │
│                                                      │
│  ┌──────────────────┐   ┌──────────────────┐        │
│  │    Broker 1      │   │    Broker 2      │  ...   │
│  │  ┌────────────┐  │   │  ┌────────────┐  │        │
│  │  │LogManager  │  │   │  │LogManager  │  │        │
│  │  │┌──────────┐│  │   │  │┌──────────┐│  │        │
│  │  ││   Log    ││  │   │  ││   Log    ││  │        │
│  │  ││┌────────┐││  │   │  ││┌────────┐││  │        │
│  │  │││Segment │││  │   │  │││Segment │││  │        │
│  │  ││└────────┘││  │   │  ││└────────┘││  │        │
│  │  │└──────────┘│  │   │  │└──────────┘│  │        │
│  │  └────────────┘  │   │  └────────────┘  │        │
│  │  ┌────────────┐  │   │  ┌────────────┐  │        │
│  │  │ReplicaMgr │  │   │  │ReplicaMgr  │  │        │
│  │  └────────────┘  │   │  └────────────┘  │        │
│  └──────────────────┘   └──────────────────┘        │
│           ▲                       ▲                  │
│           │                       │                  │
│  ┌────────┴───────────────────────┴──────────┐      │
│  │              Network Layer                 │      │
│  │         (SocketServer + Processor)         │      │
│  └───────────────────────────────────────────┘      │
│           ▲                       ▲                  │
└───────────┼───────────────────────┼──────────────────┘
            │                       │
    ┌───────┴────────┐    ┌────────┴─────────┐
    │ Producer Client│    │ Consumer Client   │
    │  ┌──────────┐  │    │  ┌─────────────┐  │
    │  │Sender    │  │    │  │Fetcher      │  │
    │  │Thread    │  │    │  │Thread       │  │
    │  └──────────┘  │    │  └─────────────┘  │
    │  ┌──────────┐  │    │  ┌─────────────┐  │
    │  │RecordAccu│  │    │  │ConsumerCoord│  │
    │  │mulator   │  │    │  │inator       │  │
    │  └──────────┘  │    │  └─────────────┘  │
    └────────────────┘    └───────────────────┘
```

---

## 路线图总览

```
第1天: Producer发送流程 — 一条消息的旅程
  阅读: KafkaProducer.java, RecordAccumulator.java, Sender.java
  重点: 异步发送模型、批量发送、RecordAccumulator内存管理
  实验: 跟踪一条消息从send()到Broker ACK的完整路径

第2天: Broker存储机制 — 零拷贝与Page Cache
  阅读: Log.scala, LogSegment.scala, LogManager.scala
  重点: Log Segment、Index文件、时间索引、零拷贝(sendfile)
  实验: 观察Broker磁盘上的Segment文件和Index文件

第3天: 副本同步与ISR机制
  阅读: ReplicaManager.scala, Partition.scala
  重点: ISR管理、Leader epoch、HW(High Watermark)推进
  实验: Kill一个Broker观察ISR变化和Leader切换

第4天: 网络层与请求处理
  阅读: SocketServer.scala, KafkaApis.scala, Processor.scala
  重点: Reactor模式、请求队列、零拷贝网络传输
  实验: 压测 + 监控网络IO和请求队列
```

---

## 环境准备

```bash
# 1. Clone Kafka源码
git clone https://github.com/apache/kafka.git
cd kafka
git checkout 3.6.0

# 2. 构建项目
./gradlew jar

# 3. 导入IntelliJ IDEA
# File → Open → 选择kafka根目录
# 等待Gradle依赖解析完成

# 4. 启动本地Kafka（用于Debug）
./bin/zookeeper-server-start.sh config/zookeeper.properties &
./bin/kafka-server-start.sh config/server.properties &

# 5. Debug模式启动Broker
# 在IDEA中配置Remote Debug (默认端口5005)
export KAFKA_DEBUG=y; export DEBUG_SUSPEND_FLAG=y
./bin/kafka-server-start.sh config/server.properties
```

### 关键源码目录
```
kafka/
├── clients/src/main/java/org/apache/kafka/clients/
│   ├── producer/                     ← Producer客户端
│   │   ├── KafkaProducer.java       ← Producer入口
│   │   ├── RecordAccumulator.java   ← 内存缓冲区
│   │   └── internals/
│   │       └── Sender.java          ← 发送线程
│   └── consumer/                     ← Consumer客户端
│       └── internals/
│           └── Fetcher.java         ← 拉取线程
├── core/src/main/scala/kafka/
│   ├── server/
│   │   ├── KafkaApis.scala          ← 请求处理入口
│   │   ├── ReplicaManager.scala     ← 副本管理
│   │   └── KafkaRequestHandler.scala
│   ├── log/
│   │   ├── Log.scala                ← Topic Partition的日志
│   │   ├── LogSegment.scala         ← 日志分段
│   │   ├── LogManager.scala         ← 日志管理器
│   │   └── LogOffsetSnapshot.scala
│   └── network/
│       ├── SocketServer.scala       ← 网络层
│       └── Processor.scala
└── storage/src/main/java/org/apache/kafka/storage/internals/
    └── log/                          ← 存储内部实现
```

---

## 第1天：Producer发送流程 — 一条消息的旅程

### 阅读目标
跟踪 `producer.send()` 到收到Broker ACK的完整数据流

### 整体流程图

```
用户调用 producer.send(record)
         │
         ▼
┌─────────────────┐
│ 1. 拦截器链      │  → ProducerInterceptor.onSend()
│   (Interceptor) │
└────────┬────────┘
         ▼
┌─────────────────┐
│ 2. 序列化        │  → KeySerializer / ValueSerializer
│   (Serializer)  │
└────────┬────────┘
         ▼
┌─────────────────┐
│ 3. 分区路由      │  → Partitioner.partition()
│   (Partitioner) │  → 决定消息去哪个Partition
└────────┬────────┘
         ▼
┌─────────────────┐
│ 4. RecordAccum- │  → append() 追加到对应Partition的Deque
│    ulator       │  → ProducerBatch 累积多条消息
│   (内存缓冲区)   │  → 如果Batch满了或创建了新的Batch → 唤醒Sender
└────────┬────────┘
         ▼
┌─────────────────┐
│ 5. Sender线程   │  → 定期轮询RecordAccumulator
│   (后台线程)    │  → 取出就绪的Batch
│                 │  → 按Broker分组（目标Broker相同的Batch合并）
└────────┬────────┘
         ▼
┌─────────────────┐
│ 6. 网络发送      │  → NetworkClient.send()
│                 │  → 创建ProduceRequest
│                 │  → 发送到目标Broker
└────────┬────────┘
         ▼
┌─────────────────┐
│ 7. Broker处理   │  → 写入Page Cache
│                 │  → 返回ProduceResponse (含Offset)
└────────┬────────┘
         ▼
┌─────────────────┐
│ 8. 回调处理      │  → 根据acks配置决定何时认为"发送成功"
│                 │  → 调用 Callback.onCompletion()
└─────────────────┘
```

### 核心文件

#### 文件1：`KafkaProducer.java`
**路径**：`clients/src/main/java/org/apache/kafka/clients/producer/KafkaProducer.java`

**核心方法**：

1. **`send(ProducerRecord<K, V> record, Callback callback)`**
   - 异步发送的入口
   - 返回 `Future<RecordMetadata>`
   - 内部调用 `doSend()`

2. **`doSend()`** — 核心流程
   ```java
   // 简化后的流程：
   // 1. 等待元数据更新（确保知道目标Partition的Leader Broker）
   // 2. 序列化 Key 和 Value
   // 3. 计算目标Partition
   // 4. 验证消息大小是否超过限制
   // 5. 追加到 RecordAccumulator
   // 6. 如果Batch满了或创建了新Batch → 唤醒Sender线程
   ```

3. **`close()` / `flush()`**
   - flush：强制将Accumulator中的所有数据发送出去
   - close：flush + 关闭Producer（等待Sender线程结束）

**必须回答的问题**：
1. `send()` 是异步的，如何知道消息真的发送成功了？
2. `max.block.ms` 的含义：什么时候send会被阻塞？
3. `acks=0` / `acks=1` / `acks=all` 在Producer端有什么不同的行为？

#### 文件2：`RecordAccumulator.java`
**路径**：`clients/src/main/java/org/apache/kafka/clients/producer/internals/RecordAccumulator.java`

**核心数据结构**：
```java
// TopicPartition → Deque<ProducerBatch>
// 每个TopicPartition对应一个Batch队列
private final ConcurrentMap<TopicPartition, Deque<ProducerBatch>> batches;

// 总内存缓冲大小（buffer.memory配置，默认32MB）
private final long totalMemorySize;

// 当前已使用的内存
private final BufferPool free;
```

**核心方法**：

1. **`append()`** — 追加消息
   - 找到对应TopicPartition的Deque
   - 尝试追加到最后一个未满的Batch
   - 如果最后一个Batch满了 → 创建新Batch
   - 如果内存不够 → 等待（直到有Batch发送完毕释放内存，或超时）

2. **`drain()`** — Sender线程调用，取出就绪的Batch
   - 返回 `Map<Integer, List<ProducerBatch>>`（BrokerId → Batch列表）
   - 哪些Batch是"就绪"的？
     - Batch满了（batch.size）
     - 或者等待时间超过了 linger.ms
     - 或者被强制flush

**关键配置理解**：
| 参数 | 作用 | 增大→效果 | 减小→效果 |
|------|------|----------|----------|
| `batch.size` | 单个Batch的最大字节数 | 吞吐↑、延迟↑ | 吞吐↓、延迟↓ |
| `linger.ms` | Batch等待时间 | 吞吐↑、延迟↑ | 吞吐↓、延迟↓ |
| `buffer.memory` | RecordAccumulator总内存 | 可缓存更多 | 易触发阻塞 |
| `max.block.ms` | 等待内存的最长时间 | 更容忍内存不足 | 更快报异常 |

#### 文件3：`Sender.java`
**路径**：`clients/src/main/java/org/apache/kafka/clients/producer/internals/Sender.java`

**核心流程**：
```java
// Sender.run() — 主循环（简化版）
void run(long now) {
    // 1. 从RecordAccumulator取出就绪的Batch
    Map<Integer, List<ProducerBatch>> batches = accumulator.drain(...);
    
    // 2. 为每个Broker创建ProduceRequest
    for (Map.Entry<Integer, List<ProducerBatch>> entry : batches.entrySet()) {
        ProduceRequest request = createProduceRequest(entry.getValue());
        
        // 3. 发送请求（异步）
        client.send(request, new RequestCompletionHandler() {
            public void onComplete(Response response) {
                // 4. 处理响应：调用每个Batch的callback
                handleProduceResponse(response, entry.getValue());
            }
        });
    }
}
```

### 第1天实验任务

```java
// 实验1：跟踪一条消息的发送路径
// 在 KafkaProducer.doSend() 打断点，逐步Debug
// 观察：
// 1. 消息进入RecordAccumulator的位置
// 2. Sender线程何时被唤醒
// 3. 网络请求的创建和发送
// 4. Broker返回的Offset

// 实验2：批量发送的效果验证
Properties props = new Properties();
props.put("batch.size", 16384);    // 16KB
props.put("linger.ms", 100);       // 100ms

KafkaProducer<String, String> producer = new KafkaProducer<>(props);

// 快速连续发送100条消息（每条100字节）
for (int i = 0; i < 100; i++) {
    producer.send(new ProducerRecord<>("test", "key" + i, "value" + i));
}

// 观察WireShark或Kafka日志：
// 1. 实际发送了几个ProduceRequest？（应该被合并为1个或少数几个）
// 2. 每个Request中包含多少条消息？
```

### 第1天强制输出
- 画Producer发送的完整流程图（8步，标注每步涉及的类和方法）
- RecordAccumulator内存管理示意图

---

## 第2天：Broker存储机制 — 零拷贝与Page Cache

### 阅读目标
理解Kafka如何通过零拷贝和Page Cache实现高吞吐的持久化

### 存储层级结构

```
Topic: "user-events"
  └── Partition 0
        └── Log (数据目录: /kafka-logs/user-events-0/)
              ├── 00000000000000000000.log     ← 数据文件
              ├── 00000000000000000000.index   ← 偏移量索引
              ├── 00000000000000000000.timeindex ← 时间索引
              ├── 00000000000000012345.log
              ├── 00000000000000012345.index
              ├── 00000000000000012345.timeindex
              ├── ...
              └── leader-epoch-checkpoint      ← Leader Epoch信息

每个Segment:
  .log文件: 存储实际的消息数据（顺序写）
  .index文件: 稀疏索引（Offset → .log文件中的物理位置）
  .timeindex文件: 时间索引（Timestamp → Offset）
```

### 核心文件

#### 文件1：`Log.scala`
**路径**：`core/src/main/scala/kafka/log/Log.scala`

**核心职责**：
- 管理一个Partition的所有Segment
- 处理追加消息、读取消息、Segment滚动

**核心数据结构**：
```scala
class Log {
    // 所有LogSegment的有序列表（按BaseOffset排序）
    val segments: ConcurrentNavigableMap[java.lang.Long, LogSegment]
    
    // 当前活跃的Segment（正在写入的）
    var activeSegment: LogSegment
    
    // 配置
    val config: LogConfig  // segment.bytes, retention.ms, etc.
}
```

**关键方法**：

1. **`appendAsLeader()` / `appendAsFollower()`** — 消息追加
   - Leader和Follower的追加逻辑不同
   - 检查消息的Offset是否单调递增
   - 如果当前Segment满了 → 创建新Segment（Roll）

2. **`read()`** — 消息读取
   - 根据Offset定位到对应的Segment
   - 在Segment内使用Index文件定位到消息的物理位置
   - 返回 `FetchDataInfo`（包含消息记录）

3. **`deleteOldSegments()`** — 过期Segment清理
   - 基于Retention时间或大小清理
   - 找到所有过期的Segment，标记删除

#### 文件2：`LogSegment.scala`
**路径**：`core/src/main/scala/kafka/log/LogSegment.scala`

**核心数据结构**：
```scala
class LogSegment {
    val log: FileRecords          // 实际的数据文件(.log)
    val offsetIndex: OffsetIndex  // 偏移量索引(.index)
    val timeIndex: TimeIndex      // 时间索引(.timeindex)
    val baseOffset: Long          // 该Segment的起始Offset
    val maxTimestampSoFar: Long   // 该Segment中的最大时间戳
}
```

**稀疏索引的查找过程**：
```
查找 Offset=1000 的消息:
1. 通过 Log.segments 找到 baseOffset ≤ 1000 的最大Segment
   (假设Segment baseOffset=800, baseOffset=1200)
   → 选中 baseOffset=800 的Segment

2. 在Index文件中查找 Offset=1000 的位置
   Index文件(稀疏索引):
     Offset 800  → 物理位置 0
     Offset 900  → 物理位置 4096
     Offset 1000 → ? (不在索引中)
     Offset 1100 → 物理位置 12288
   
   → 找到 ≤1000 的最大索引条目: Offset=900, 物理位置=4096

3. 从 .log 文件的物理位置 4096 开始顺序扫描
   直到找到 Offset=1000 的消息
```

**为什么用稀疏索引？**
- 减少Index文件大小（全量索引会非常大）
- 牺牲一点查找时间（最多顺序扫描 `log.index.interval.bytes` 字节的数据）
- 利用顺序读的高性能

#### 文件3：零拷贝的实现

**Kafka使用 `FileChannel.transferTo()` 实现零拷贝**：

```java
// 传统方式（4次拷贝 + 2次DMA + 2次CPU拷贝）
磁盘 → OS Read Buffer → 应用Buffer → Socket Buffer → 网卡

// Kafka零拷贝（2次拷贝 + 2次DMA + 0次CPU拷贝）
磁盘 → OS Read Buffer ───→ Socket Buffer → 网卡
                 └── sendfile() ──→ DMA gather copy
// 应用层完全不参与数据拷贝！
```

**源码位置**：`FileRecords.java` 中的 `writeTo()` 方法
```java
public long writeTo(TransferableChannel destChannel, long offset, int length) {
    // 调用 FileChannel.transferTo()
    return channel.transferTo(offset, length, destChannel);
}
```

### 第2天实验任务

```bash
# 实验1：观察磁盘上的Segment文件
# 1. 创建一个Topic并发送大量数据
kafka-topics.sh --create --topic test-segment --partitions 1 --replication-factor 1
kafka-producer-perf-test.sh --topic test-segment --num-records 1000000 \
    --record-size 1000 --throughput -1

# 2. 查看数据目录
ls -la /tmp/kafka-logs/test-segment-0/
# 观察:
#   - 产生了多少个.log文件？
#   - 每个.log文件的大小？（是否接近 segment.bytes=1GB）
#   - .index文件的大小？(.log文件的1/10? 1/100?)

# 实验2：验证稀疏索引的查找效率
# 使用 kafka-dump-log.sh 查看Index文件内容
kafka-dump-log.sh --files /tmp/kafka-logs/test-segment-0/00000000000000000000.index
# 观察：Index中的offset间隔是多少？
```

### 第2天强制输出
- 画Kafka存储层级图：Topic → Partition → Log → Segment → .log/.index/.timeindex
- 零拷贝的数据流图（对比传统4次拷贝）
- 稀疏索引查找过程图解

---

## 第3天：副本同步与ISR机制

### 阅读目标
理解Kafka的副本同步机制、ISR管理和HW推进

### 核心概念

```
Topic: "orders", 3 Partitions, Replication Factor = 3

Partition 0:
  Broker 1 (Leader) ←── 所有读写
  Broker 2 (Follower) ←── 从Leader同步数据
  Broker 3 (Follower) ←── 从Leader同步数据

ISR = {Broker 1, Broker 2, Broker 3}  ← 所有跟上Leader的副本

关键概念:
  LEO (Log End Offset): 副本的日志末尾Offset
  HW  (High Watermark): ISR中所有副本LEO的最小值 → 只有HW之前的消息对Consumer可见！
```

**HW推进过程**：
```
初始状态:
  Leader:    [m1][m2][m3][m4]  LEO=4
  Follower1: [m1][m2]          LEO=2
  Follower2: [m1][m2][m3]      LEO=3
  HW = min(4,2,3) = 2 → 只有m1,m2对Consumer可见！

Follower1 Fetch请求 → Leader返回m3:
  Leader:    [m1][m2][m3][m4]  LEO=4
  Follower1: [m1][m2][m3]      LEO=3
  Follower2: [m1][m2][m3]      LEO=3
  HW = min(4,3,3) = 3 → m3现在对Consumer可见！
```

### 核心文件

#### 文件1：`ReplicaManager.scala`
**路径**：`core/src/main/scala/kafka/server/ReplicaManager.scala`

**核心职责**：
- 管理所有Partition的Leader/Follower副本
- 处理Producer的Produce请求和Consumer的Fetch请求
- ISR管理：哪些副本应该加入/移出ISR

**关键方法**：

1. **`appendRecords()`** — 处理Leader的消息追加
   - 写入本地Log
   - 更新LEO
   - 尝试推进HW

2. **`fetchMessages()`** — 处理Follower的Fetch请求
   - Follower携带自己的LEO来Fetch
   - Leader返回LEO之后的数据
   - Follower写入本地后更新自己的LEO

3. **`maybeShrinkIsr()` / `maybeExpandIsr()`** — ISR管理
   - 如果Follower在 `replica.lag.time.max.ms` 内没有Fetch请求 → 从ISR移出
   - 如果Follower的LEO追上了Leader的LEO → 重新加入ISR

#### 文件2：Leader Epoch机制

**为什么需要Leader Epoch？**
```
传统HW的问题:
  场景: Leader宕机，旧Follower成为新Leader
  
  旧Leader: [m1][m2][m3][m4]  LEO=4, HW=3
  旧Follower(新Leader): [m1][m2][m3]  LEO=3, HW=3
  
  问题: 新Leader的HW=3，但旧Leader曾经HW=4
        新Leader如果截断HW之后的数据 → m3还在
        但旧Leader如果恢复，可能丢失m4
  
  Leader Epoch的解决方案:
  每个Leader任期有Epoch编号
  新Leader就职时，在leader-epoch-checkpoint文件中记录：
    Epoch=5 起始Offset=3（新Leader的LEO）
  通过Leader Epoch可以准确知道哪些数据是"安全"的！
```

### 第3天实验任务

```bash
# 实验1：观察ISR变化
# 1. 创建一个3副本的Topic
kafka-topics.sh --create --topic test-isr --partitions 1 --replication-factor 3

# 2. 查看初始ISR
kafka-topics.sh --describe --topic test-isr
# ISR: 0,1,2

# 3. Kill一个Broker
kill -9 <broker_pid>

# 4. 观察ISR变化（几秒后）
kafka-topics.sh --describe --topic test-isr
# ISR: 1,2  (被Kill的Broker从ISR中移出)

# 5. 重启Broker，观察ISR恢复
kafka-topics.sh --describe --topic test-isr
# ISR: 0,1,2  (重新加入ISR)

# 实验2：观察Leader切换
# 如果Kill的是Leader Broker，观察:
# 1. 谁成为了新Leader？
# 2. 切换用了多少时间？(通过Producer的retry次数估算)
# 3. Consumer是否有感知？（可能有短暂停顿）
```

### 第3天强制输出
- 画ISR、LEO、HW三者关系的示意图
- 写清楚HW推进的触发条件和步骤
- Leader Epoch解决的问题和解决方案

---

## 第4天：网络层与请求处理

### 阅读目标
理解Kafka Broker如何高效处理海量并发请求

### 网络层架构 — Reactor模式

```
                     ┌──────────────────┐
                     │   Acceptor       │   ← 接受新连接
                     │   Thread (1个)   │
                     └────────┬─────────┘
                              │ 新连接
              ┌───────────────┼───────────────┐
              ▼               ▼               ▼
     ┌────────────┐  ┌────────────┐  ┌────────────┐
     │ Processor  │  │ Processor  │  │ Processor  │  ← 网络读写
     │ Thread     │  │ Thread     │  │ Thread     │
     │ (num.netwo│  │ (num.netwo│  │ (num.netwo│
     │  rk.thread│  │  rk.thread│  │  rk.thread│
     │  s个)     │  │  s个)     │  │  s个)     │
     └─────┬──────┘  └─────┬──────┘  └─────┬──────┘
           │               │               │
           └───────────────┼───────────────┘
                           │ 请求放入队列
                    ┌──────▼──────┐
                    │   Request   │
                    │   Queue     │
                    └──────┬──────┘
                           │ 取出请求
           ┌───────────────┼───────────────┐
           ▼               ▼               ▼
    ┌────────────┐  ┌────────────┐  ┌────────────┐
    │ Request    │  │ Request    │  │ Request    │  ← 业务处理
    │ Handler    │  │ Handler    │  │ Handler    │
    │ Thread     │  │ Thread     │  │ Thread     │
    │ (num.io.th│  │ (num.io.th│  │ (num.io.th│
    │  reads个) │  │  reads个) │  │  reads个) │
    └────────────┘  └────────────┘  └────────────┘
```

### 核心文件

#### 文件1：`SocketServer.scala`
**路径**：`core/src/main/scala/kafka/network/SocketServer.scala`

**核心组件**：
- **Acceptor**：接受TCP连接，分配给Processor
- **Processor**：处理网络IO（读取请求、发送响应）
- **RequestChannel**：Processor和Handler之间传递请求的队列

#### 文件2：`KafkaApis.scala`
**路径**：`core/src/main/scala/kafka/server/KafkaApis.scala`

**核心方法**：`handle()` — 请求分发
```scala
def handle(request: RequestChannel.Request) {
    request.header.apiKey match {
        case ApiKeys.PRODUCE => handleProduceRequest(request)
        case ApiKeys.FETCH => handleFetchRequest(request)
        case ApiKeys.LIST_OFFSETS => handleListOffsetRequest(request)
        case ApiKeys.METADATA => handleTopicMetadataRequest(request)
        case ApiKeys.JOIN_GROUP => handleJoinGroupRequest(request)
        // ... 30+种请求类型
    }
}
```

**PRODUCE请求的处理流程**：
```scala
def handleProduceRequest(request: RequestChannel.Request) {
    // 1. 验证：客户端是否有写权限
    // 2. 对于每个Partition的数据：
    //    a. 检查是否是Leader（不是Leader→返回错误，客户端重试）
    //    b. 调用 ReplicaManager.appendRecords()
    //    c. 记录到本地Log
    // 3. 根据 acks 配置决定何时返回响应
    //    acks=0: 立即返回（不等待落盘）
    //    acks=1: Leader写入后返回
    //    acks=all/-1: 等待所有ISR写入后返回
}
```

### 第4天实验任务

```bash
# 实验1：观察网络层的线程
# 查找Kafka Broker进程
jps | grep Kafka
jstack <kafka_pid> | grep -E "kafka-network|kafka-request|kafka-socket"

# 观察:
# - 有多少个 network-thread？
# - 有多少个 kafka-request-handler？
# - 线程的当前状态（RUNNABLE / WAITING / BLOCKED）

# 实验2：压测观察请求队列
# 使用 kafka-producer-perf-test.sh 进行高压测
kafka-producer-perf-test.sh \
    --topic test-perf \
    --num-records 10000000 \
    --record-size 100 \
    --throughput -1 \
    --producer-props acks=all

# 同时通过JMX观察:
# - RequestQueueSize: 请求队列大小（如果持续>0，说明Handler不够）
# - ResponseQueueSize: 响应队列大小
# - NetworkProcessorAvgIdlePercent: 网络线程空闲率
```

### 第4天强制输出
- Reactor模式的网络层架构图
- PRODUCE请求从Processor到Handler到ReplicaManager的完整路径图
- 压测结果分析：瓶颈在哪里？（网络/CPU/磁盘IO）

---

## 综合输出要求

### 源码分析文章模板
同Flink源码路线中的模板格式。

### 最小阅读代码清单（必须完成）
- [ ] `KafkaProducer.doSend()`
- [ ] `RecordAccumulator.append()`
- [ ] `Sender.run()`
- [ ] `Log.appendAsLeader()`
- [ ] `LogSegment` 的结构
- [ ] `FileRecords.writeTo()`（零拷贝）
- [ ] `ReplicaManager.appendRecords()`
- [ ] `ReplicaManager.maybeShrinkIsr()`
- [ ] `KafkaApis.handleProduceRequest()`
- [ ] `SocketServer` 的Reactor结构

### Kafka与Flink/Spark的关联思考

阅读完Kafka源码后，思考以下问题：
1. Flink的Kafka Source如何利用Kafka的Offset机制实现Checkpoint？
2. Spark Streaming的Direct模式与Kafka的Consumer Group有什么关联？
3. 如果Kafka不使用零拷贝，对Flink/Spark的读取性能有多大影响？
4. ISR机制与Flink的Checkpoint Barrier对齐有什么相似之处？

---

## Controller选举流程源码深潜

### Controller的角色

```
Kafka集群中的Controller是"超级Broker":
  ┌──────────────────────────────────────────────────┐
  │                 Controller (Broker X)              │
  │  ┌────────────────────────────────────────────┐  │
  │  │  Partition Leader选举                       │  │
  │  │  - 检测Broker故障 → 重新选举受影响Partition  │  │
  │  │  - 优先选择ISR中的副本                       │  │
  │  ├────────────────────────────────────────────┤  │
  │  │  Topic/Partition管理                        │  │
  │  │  - 创建/删除Topic                           │  │
  │  │  - 分区分配(新Topic的副本放置)               │  │
  │  │  - 分区重新分配(迁移)                        │  │
  │  ├────────────────────────────────────────────┤  │
  │  │  ISR管理                                    │  │
  │  │  - 接收Leader的ISR变更请求                   │  │
  │  │  - 更新ZooKeeper中的ISR元数据                │  │
  │  │  - 通知所有Broker元数据变更                   │  │
  │  ├────────────────────────────────────────────┤  │
  │  │  Preferred Leader选举                       │  │
  │  │  - 定期检查是否需要Preferred Leader          │  │
  │  │  - 触发Leader切换(优先使用原始Leader)         │  │
  │  └────────────────────────────────────────────┘  │
  └──────────────────────────────────────────────────┘
```

### Controller选举流程（ZooKeeper模式）

```
ZooKeeper临时节点选举:

  Broker启动时:
    ┌─────────┐     ┌─────────┐     ┌─────────┐
    │Broker 1 │     │Broker 2 │     │Broker 3 │
    └────┬────┘     └────┬────┘     └────┬────┘
         │               │               │
         │ 尝试创建       │ 尝试创建       │ 尝试创建
         │ /controller   │ /controller   │ /controller
         │ 临时节点       │ 临时节点       │ 临时节点
         │               │               │
    ┌────▼────────────────────────────────────────┐
    │              ZooKeeper                       │
    │  /controller = {"brokerid": 1}  ← Broker1先到│
    │  /controller_epoch = 5                       │
    └──────────────────────────────────────────────┘
    
  Broker1成功创建/controller → 成为Controller!
  Broker2和Broker3创建失败 → 监听/controller节点变化

  Controller故障时:
    ZooKeeper检测到Broker1的会话超时
    → /controller临时节点被自动删除
    → Broker2和Broker3收到Watcher通知
    → 重新竞争创建/controller
    → 新Controller产生!
```

### 核心源码路径

```
Controller选举相关源码:

KafkaController.scala (核心类)
  路径: core/src/main/scala/kafka/controller/KafkaController.scala
  关键方法:
    - elect(): 选举入口
    - onControllerFailover(): 当选Controller后的初始化
    - onControllerResignation(): 放弃Controller角色的清理
    - processBrokerChange(): 处理Broker上下线
    - processPartitionChange(): 处理Partition Leader选举

ZooKeeperClient.scala (ZK交互)
  路径: core/src/main/scala/kafka/zk/ZooKeeperClient.scala
  关键方法:
    - createController(): 创建/controller临时节点
    - getController(): 获取当前Controller信息
    - registerControllerChangeHandler(): 注册Controller变更监听

PartitionStateMachine.scala (分区状态机)
  路径: core/src/main/scala/kafka/controller/PartitionStateMachine.scala
  关键方法:
    - handleStateChanges(): 分区状态转换
    - initializeLeaderAndIsr(): 初始化Leader和ISR
    - electLeaderForPartitions(): 为无Leader分区选举Leader

ReplicaStateMachine.scala (副本状态机)
  路径: core/src/main/scala/kafka/controller/ReplicaStateMachine.scala
  关键方法:
    - handleStateChanges(): 副本状态转换
    - handleOfflineReplica(): 处理下线副本
```

### KRaft模式下的Controller选举

```
KRaft模式 (Kafka 3.x+, 无ZooKeeper):

  ┌─────────────────────────────────────────────┐
  │           KRaft Quorum (3个Controller)       │
  │  ┌───────────┐ ┌───────────┐ ┌───────────┐ │
  │  │Controller │ │Controller │ │Controller │ │
  │  │(Leader)   │ │(Voter)    │ │(Voter)    │ │
  │  │           │ │           │ │           │ │
  │  │Raft Leader│ │Raft Foll. │ │Raft Foll. │ │
  │  └───────────┘ └───────────┘ └───────────┘ │
  │       │                                       │
  │  Raft Leader = Active Controller              │
  │  Raft Follower = Standby Controller           │
  └─────────────────────────────────────────────┘

  选举流程:
    1. 3个Controller节点启动
    2. 通过Raft协议选举Leader
    3. Raft Leader成为Active Controller
    4. 元数据变更通过Raft日志复制

  与ZooKeeper模式的关键差异:
    - 无外部ZooKeeper依赖
    - 元数据存储在Raft日志中(而非ZK)
    - Controller选举 = Raft Leader选举(更简洁)
    - 元数据更新延迟更低(无需ZK通知链路)
```

---

## 调试技巧：如何本地Debug Kafka源码

### 1. IDEA远程Debug Kafka Broker

```bash
# 设置Debug参数后启动Kafka
export KAFKA_DEBUG=y
export DEBUG_SUSPEND_FLAG=n
export JAVA_DEBUG_PORT=5005
./bin/kafka-server-start.sh config/server.properties

# IDEA中配置:
# Run → Edit Configurations → + → Remote JVM Debug
# Host: localhost, Port: 5005
```

### 2. 单元测试Debug（推荐方式）

```scala
// Kafka源码中有大量测试, 直接Debug即可
// 示例: Debug Producer发送流程

// 测试类: KafkaProducerTest.java
// 路径: clients/src/test/java/org/apache/kafka/clients/producer/KafkaProducerTest.java

@Test
public void testSend() throws Exception {
    // 在这里打断点
    ProducerRecord<String, String> record = new ProducerRecord<>("test", "key", "value");
    Future<RecordMetadata> future = producer.send(record);
    // 跟踪doSend()的每一步
}

// 示例: Debug Replica同步
// 测试类: ReplicaManagerTest.scala
// 路径: core/src/test/scala/unit/kafka/server/ReplicaManagerTest.scala
```

### 3. 本地单节点Debug

```bash
# 1. 启动ZooKeeper (单节点)
./bin/zookeeper-server-start.sh config/zookeeper.properties

# 2. 以Debug模式启动Kafka Broker
export KAFKA_DEBUG=y
export JAVA_DEBUG_PORT=5005
./bin/kafka-server-start.sh config/server.properties

# 3. 创建Topic并发送消息
./bin/kafka-topics.sh --create --topic debug-test --partitions 1 --replication-factor 1
./bin/kafka-console-producer.sh --topic debug-test --bootstrap-server localhost:9092

# 4. 在IDEA中打断点并attach
# 可以在KafkaApis.handleProduceRequest()打断点
# 发送消息后会命中断点
```

### 4. 关键断点位置

| 调试目标 | 断点位置 | 说明 |
|---------|---------|------|
| Producer发送 | `KafkaProducer.doSend()` | 跟踪消息从send()到RecordAccumulator |
| 批量发送 | `Sender.run()` | 跟踪Sender线程如何取出Batch并发送 |
| Broker接收 | `KafkaApis.handleProduceRequest()` | 跟踪Broker如何处理Produce请求 |
| 日志写入 | `Log.appendAsLeader()` | 跟踪消息写入Log Segment |
| 副本同步 | `ReplicaManager.fetchMessages()` | 跟踪Follower的Fetch请求处理 |
| ISR变更 | `ReplicaManager.maybeShrinkIsr()` | 跟踪ISR收缩逻辑 |
| Controller选举 | `KafkaController.elect()` | 跟踪Controller选举过程 |
| Leader切换 | `PartitionStateMachine.electLeaderForPartitions()` | 跟踪Partition Leader选举 |
| 零拷贝 | `FileRecords.writeTo()` | 跟踪sendfile()调用 |

### 5. 日志级别调整

```properties
# log4j.properties
log4j.logger.kafka.request.logger=DEBUG
log4j.logger.kafka.controller=TRACE
log4j.logger.kafka.server.ReplicaManager=DEBUG
log4j.logger.kafka.log.Log=DEBUG
log4j.logger.org.apache.kafka.clients.producer=DEBUG
```

---

## 每周强制输出模板

```markdown
# Kafka源码深潜 - 第X天输出

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
- 实验配置: [Kafka配置/数据集]
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