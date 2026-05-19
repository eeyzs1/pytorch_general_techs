# 课时18：Kafka Exactly-Once与事务

> **所属阶段**：L2 中级工程师 | **周次**：第15-16周 | **课时**：3h | **难度**：★★★★★

---

## 一、教学目标

1. 理解消息投递的三种语义：At-Most-Once、At-Least-Once、Exactly-Once
2. 掌握Producer幂等性的实现原理（PID + Sequence Number）
3. 深入理解Kafka事务机制与Transaction Coordinator
4. 理解两阶段提交(2PC)在Kafka和Flink中的应用
5. 能编写使用事务的Producer/Consumer代码

---

## 二、消息投递三种语义

### 2.1 概念对比

```
At-Most-Once (最多一次):
  Producer → Broker: 发完就忘，不等确认
  结果: 消息可能丢失，但绝不重复
  适用: 日志收集、监控指标等可容忍少量丢失的场景
  
  Producer.send(msg)  // 不等ACK
  // 如果网络断了，消息丢了也不知道

==================================================

At-Least-Once (至少一次):
  Producer → Broker: 发送 → 等ACK → 超时 → 重试 → 等ACK
  结果: 消息不丢，但可能重复
  适用: 大多数场景（配合幂等Consumer处理重复）
  
  Producer.send(msg)  // 等待ACK
  // 如果ACK丢失但Broker已写入 → Producer重试 → 消息重复

==================================================

Exactly-Once (精确一次):
  Producer → Broker: 发送(带幂等标识) → 等ACK → 超时 → 重试(幂等)
  Broker: 识别重复请求，只写入一次
  结果: 消息既不丢也不重复
  适用: 金融交易、订单处理、计费等
```

### 2.2 为什么Exactly-Once很难

```
根本原因：分布式系统中的"两军问题"

问题场景：
  Producer发出消息 → 网络中断 → Producer不知道Broker是否收到

  情况A: Broker收到了但ACK丢失
    → Producer重试 → Broker收到重复消息 → 需要去重

  情况B: Broker没收到
    → Producer重试 → Broker收到新消息 → 正常

  Producer无法区分情况A和情况B！

解决方案：
  - 给每条消息一个唯一ID（PID + Sequence Number）
  - Broker端基于ID去重
  - 这就是幂等性Producer的核心思想
```

---

## 三、Producer幂等性

### 3.1 实现原理

```
幂等性Producer的实现机制:

每次Producer初始化时:
  1. 向Broker申请一个PID (Producer ID)，全局唯一
  2. PID在该Producer实例的生命周期内不变

每条消息发送时:
  1. 带上 (PID, Sequence Number)
  2. Sequence Number从0开始单调递增
  3. 每个<Topic, Partition>独立维护一个Sequence Number

Broker端去重逻辑:
  1. 收到消息 (PID=100, Seq=5, TopicPartition=orders-0)
  2. 查找内存中该PID对应该Partition的最近Seq
  3. 如果Seq == lastSeq + 1 → 正常追加，更新lastSeq=5
  4. 如果Seq <= lastSeq → 重复消息，丢弃
  5. 如果Seq > lastSeq + 1 → 消息乱序/丢失，抛出OutOfOrderSequenceException
```

### 3.2 幂等性代码示例

```java
Properties props = new Properties();
props.put("bootstrap.servers", "localhost:9092");
props.put("key.serializer", "org.apache.kafka.common.serialization.StringSerializer");
props.put("value.serializer", "org.apache.kafka.common.serialization.StringSerializer");

// 开启幂等性（自动设置以下参数）
props.put("enable.idempotence", "true");
// enable.idempotence=true 会自动设置:
//   acks=all
//   retries=Integer.MAX_VALUE
//   max.in.flight.requests.per.connection=5 (Kafka >= 1.1)

KafkaProducer<String, String> producer = new KafkaProducer<>(props);

// 即使在重试过程中，Broker也能正确去重
for (int i = 0; i < 1000; i++) {
    ProducerRecord<String, String> record = new ProducerRecord<>(
        "orders",
        "key-" + i,
        "value-" + i
    );
    producer.send(record, (metadata, exception) -> {
        if (exception != null) {
            System.err.println("发送失败: " + exception.getMessage());
        } else {
            System.out.println("发送成功: offset=" + metadata.offset());
        }
    });
}

producer.close();
```

### 3.3 Python幂等性Producer

```python
from kafka import KafkaProducer
import json

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    acks='all',
    retries=5,
    # 关键配置：开启幂等性
    enable_idempotence=True,
    # enable_idempotence=True 时，max_in_flight_requests_per_connection 自动设为5
    # 确保消息顺序
    compression_type='lz4',
    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
    key_serializer=lambda k: str(k).encode('utf-8') if k else None,
)

print("幂等性Producer已启动")

for i in range(100):
    future = producer.send(
        'idempotent-test',
        key=f'order-{i}',
        value={'order_id': i, 'data': f'message-{i}'}
    )
    try:
        metadata = future.get(timeout=10)
        print(f"发送成功: partition={metadata.partition}, offset={metadata.offset}")
    except Exception as e:
        print(f"发送失败: {e}")

producer.close()
```

### 3.4 幂等性的局限性

```
幂等性只能保证"单分区 + 单Producer会话"内的Exactly-Once

不能解决的问题：
  1. Producer重启后PID变化 → 无法和新PID之前的消息去重
  2. 跨多个Topic/Partition的原子写入
  3. "消费-转换-生产"场景中的端到端Exactly-Once

解决方法：事务（下一节）
```

---

## 四、Kafka事务

### 4.1 事务角色

```
Kafka事务涉及的组件:

                    ┌──────────────────────┐
                    │ Transaction          │
                    │ Coordinator (TC)     │  ← 每个Broker都可能担任TC
                    │ (位于__transaction_  │
                    │  _state内部Topic     │
                    │  的Leader上)         │
                    └──────────┬───────────┘
                               │
              ┌────────────────┼────────────────┐
              │                │                │
        ┌─────▼─────┐   ┌─────▼─────┐   ┌─────▼─────┐
        │ Producer  │   │  Broker   │   │ Consumer  │
        │ (事务ID)  │   │ (存储消息)│   │ (隔离级别)│
        └───────────┘   └───────────┘   └───────────┘

关键概念:
  - Transactional ID (transactional.id):
    用于标识一个Producer实例，跨会话唯一
    PID是临时的，transactional.id是永久的

  - Transaction Coordinator:
    管理事务状态的Broker节点
    通过 transactional.id 的哈希值确定由哪个Broker担任TC

  - __transaction_state (内部Topic):
    存储事务元数据，默认50个Partition
```

### 4.2 事务Producer代码（Java）

```java
import org.apache.kafka.clients.producer.*;
import org.apache.kafka.common.KafkaException;

import java.util.Properties;

public class TransactionalProducerExample {

    public static void main(String[] args) {
        Properties props = new Properties();
        props.put("bootstrap.servers", "localhost:9092");
        props.put("key.serializer", 
            "org.apache.kafka.common.serialization.StringSerializer");
        props.put("value.serializer", 
            "org.apache.kafka.common.serialization.StringSerializer");
        
        // ====== 事务必须配置 ======
        // 1. 设置事务ID（重要！生产环境每个实例用不同的ID）
        props.put("transactional.id", "order-service-tx-01");
        
        // 2. 事务需要幂等性，自动开启
        // enable.idempotence 自动设为 true
        
        // 3. 事务超时时间（默认60秒）
        props.put("transaction.timeout.ms", "60000");

        KafkaProducer<String, String> producer = new KafkaProducer<>(props);
        
        // ====== 初始化事务 ======
        producer.initTransactions();

        try {
            // ====== 开始事务 ======
            producer.beginTransaction();
            
            // 发送消息到Topic A
            producer.send(new ProducerRecord<>(
                "topic-A", "key-1", "value-1"
            ));
            
            // 发送消息到Topic B
            producer.send(new ProducerRecord<>(
                "topic-B", "key-2", "value-2"
            ));
            
            // 发送消息到Topic C
            producer.send(new ProducerRecord<>(
                "topic-C", "key-3", "value-3"
            ));
            
            // ====== 提交事务 ======
            // 所有消息要么全部可见，要么全部不可见
            producer.commitTransaction();
            System.out.println("事务提交成功：3条消息原子写入");
            
        } catch (KafkaException e) {
            // ====== 回滚事务 ======
            producer.abortTransaction();
            System.err.println("事务回滚：" + e.getMessage());
        } finally {
            producer.close();
        }
    }
}
```

### 4.3 事务代码（Python实现）

```python
"""
Kafka事务Producer示例（Python）
注意：使用 confluent-kafka-python 库，因为原生 kafka-python 不完全支持事务
安装: pip install confluent-kafka
"""
from confluent_kafka import Producer
import json
import uuid
import time


class TransactionalOrderService:
    """订单服务：使用Kafka事务保证原子性写入"""

    def __init__(self, bootstrap_servers='localhost:9092'):
        self.conf = {
            'bootstrap.servers': bootstrap_servers,
            'transactional.id': f'order-service-{uuid.uuid4().hex[:8]}',
            'enable.idempotence': True,
            'acks': 'all',
            'transaction.timeout.ms': 60000,
        }
        self.producer = Producer(self.conf)
        self.producer.init_transactions()

    def create_order(self, order_id, user_id, items, amount):
        """创建订单：原子写入订单表和订单明细表"""
        try:
            self.producer.begin_transaction()

            # 写入订单主表
            order_msg = {
                'order_id': order_id,
                'user_id': user_id,
                'amount': amount,
                'status': 'created',
                'timestamp': int(time.time() * 1000)
            }
            self.producer.produce(
                topic='orders',
                key=str(order_id),
                value=json.dumps(order_msg),
            )

            # 写入订单明细表（每个商品一行）
            for item in items:
                item_msg = {
                    'order_id': order_id,
                    'product_id': item['product_id'],
                    'quantity': item['quantity'],
                    'unit_price': item['unit_price'],
                    'timestamp': int(time.time() * 1000)
                }
                self.producer.produce(
                    topic='order_items',
                    key=f"{order_id}-{item['product_id']}",
                    value=json.dumps(item_msg),
                )

            # 原子提交：订单和订单明细要么都成功，要么都失败
            self.producer.commit_transaction()
            print(f"订单 {order_id} 创建成功（事务提交）")
            return True

        except Exception as e:
            self.producer.abort_transaction()
            print(f"订单 {order_id} 创建失败（事务回滚）: {e}")
            return False

    def close(self):
        self.producer.flush()


if __name__ == '__main__':
    service = TransactionalOrderService()

    # 正常场景
    service.create_order(
        order_id=1001,
        user_id=42,
        items=[
            {'product_id': 101, 'quantity': 2, 'unit_price': 99.00},
            {'product_id': 102, 'quantity': 1, 'unit_price': 49.50},
        ],
        amount=247.50
    )

    # 模拟异常场景（编写时会故意让某条记录出错来测试回滚）
    # 如果订单明细写入失败，订单主表也不会被写入

    service.close()
```

### 4.4 事务Consumer配置

```java
// 读取事务消息时的隔离级别
Properties consumerProps = new Properties();
consumerProps.put("bootstrap.servers", "localhost:9092");
consumerProps.put("group.id", "analytics-group");

// ====== 关键配置：隔离级别 ======
// read_committed: 只读取已提交事务的消息（默认行为）
// read_uncommitted: 读取所有消息（包括未提交的）
consumerProps.put("isolation.level", "read_committed");

// 如果使用 read_committed：
//  - 事务未提交的消息不会被Consumer看到
//  - 事务回滚的消息不会被Consumer看到
//  - 事务提交后，消息立即可见
```

```python
# Python Consumer 的事务隔离配置
from confluent_kafka import Consumer

consumer_config = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'analytics-group',
    'auto.offset.reset': 'earliest',
    # 只消费已提交的事务消息
    'isolation.level': 'read_committed',
    # 关闭自动提交（在事务场景下通常手动管理）
    'enable.auto.commit': False,
}

consumer = Consumer(consumer_config)
consumer.subscribe(['orders'])

try:
    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            print(f"消费错误: {msg.error()}")
            continue

        print(f"收到消息: topic={msg.topic()}, "
              f"partition={msg.partition()}, "
              f"offset={msg.offset()}, "
              f"value={msg.value().decode('utf-8')}")

except KeyboardInterrupt:
    pass
finally:
    consumer.close()
```

---

## 五、两阶段提交(2PC)详解

### 5.1 经典两阶段提交

```
传统分布式事务的2PC流程:

                    协调者                   参与者A        参与者B
                     │                        │              │
  阶段1: 准备(VOTE)   │                        │              │
     ├───────────────┤                        │              │
     │ 发送Prepare请求│───────────────────────→│              │
     │               │────────────────────────────────────────→│
     │               │                        │              │
     │               │    ←─── YES/NO ────────│              │
     │               │    ←───────────── YES/NO ──────────────│
     │               │                        │              │
  阶段2: 提交(COMMIT) │                        │              │
     │               │                        │              │
     │  如果全部YES:  │                        │              │
     │  发送Commit   │───────────────────────→│ (正式写入)    │
     │               │────────────────────────────────────────→│ (正式写入)
     │               │                        │              │
     │  如果有NO:    │                        │              │
     │  发送Abort    │───────────────────────→│ (回滚)       │
     │               │────────────────────────────────────────→│ (回滚)

问题：
  - 协调者单点故障 → 整个事务阻塞
  - 参与者故障 → 协调者永久的阻塞等待
  - 性能差：需要两轮网络通信 + 日志持久化
```

### 5.2 Flink + Kafka 两阶段提交

```
Flink实现端到端Exactly-Once的方案:

场景: Flink消费Kafka → 处理 → 写回Kafka

                       Flink Job
  ┌──────────┐      ┌──────────────┐      ┌──────────┐
  │  Kafka   │─────→│  Source      │      │  Kafka   │
  │ (Input)  │      │  (读取Offset)│      │ (Output) │
  └──────────┘      └──────┬───────┘      └──────┬───┘
                           │                     │
                           ├──→ Map ──→ KeyBy ──→┤
                           │                     │
                           └──→ Window ──────────→┤
                                                 │
                                    ┌────────────▼───────────┐
                                    │  TwoPhaseCommitSink    │
                                    │                        │
                                    │  阶段1: PreCommit      │
                                    │    - Flink做Checkpoint  │
                                    │    - Kafka Sink开启事务 │
                                    │    - 写入数据但标记为   │
                                    │      "未提交"          │
                                    │                        │
                                    │  阶段2: Commit         │
                                    │    - Checkpoint成功    │
                                    │    - 提交Kafka事务      │
                                    │    - 数据变为可见      │
                                    │                        │
                                    │  如果失败: Abort       │
                                    │    - 回滚Kafka事务      │
                                    │    - Checkpoint恢复     │
                                    │    - 重新消费           │
                                    └────────────────────────┘

Checkpoint Barrier传播过程:

时间 ────────────────────────────────────────────────────────→

Source:     [msg1][msg2][BARRIER][msg3][msg4]...
                    │         │
Map:        [m1] [m2]  [BARRIER]  [m3] [m4]...
                         │
KeyBy:      ...  [BARRIER]对齐等待...
                         │
Window:     ...  触发窗口计算 → 输出结果 → [BARRIER]
                                              │
Sink:       ...  开启Kafka事务 → 写入 → [BARRIER]
                                       │
                                       ├→ 快照状态到StateBackend
                                       ├→ PreCommit Kafka事务
                                       └→ 通知JobManager

JobManager收到所有Operator的ACK:
  → Checkpoint n 完成
  → 通知Sink提交Kafka事务
  → 数据对下游Consumer可见
```

### 5.3 Flink两阶段提交代码示例

```java
// Flink Kafka Sink 的 Exactly-Once 语义配置
Properties sinkProps = new Properties();
sinkProps.put("bootstrap.servers", "localhost:9092");
sinkProps.put("transaction.timeout.ms", "900000"); // 15分钟

KafkaSink<String> sink = KafkaSink.<String>builder()
    .setBootstrapServers("localhost:9092")
    .setRecordSerializer(
        KafkaRecordSerializationSchema.builder()
            .setTopic("output-topic")
            .setValueSerializationSchema(new SimpleStringSchema())
            .build()
    )
    // ====== 关键：设置投递语义 ======
    .setDeliveryGuarantee(DeliveryGuarantee.EXACTLY_ONCE)
    // 等同于开启了两阶段提交
    // DeliveryGuarantee.AT_LEAST_ONCE → 不开启事务
    // DeliveryGuarantee.EXACTLY_ONCE → 开启两阶段提交
    .setTransactionalIdPrefix("flink-sink-")
    .build();

stream.sinkTo(sink);
```

```python
# PyFlink Kafka Sink 的 Exactly-Once 配置
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.connectors.kafka import (
    KafkaSink,
    KafkaRecordSerializationSchema,
    DeliveryGuarantee
)
from pyflink.common.serialization import SimpleStringSchema

env = StreamExecutionEnvironment.get_execution_environment()
env.enable_checkpointing(5000)  # 每5秒做一次Checkpoint

# 构建Kafka Sink
kafka_sink = (
    KafkaSink.builder()
    .set_bootstrap_servers("localhost:9092")
    .set_record_serializer(
        KafkaRecordSerializationSchema.builder()
        .set_topic("output-topic")
        .set_value_serialization_schema(SimpleStringSchema())
        .build()
    )
    .set_delivery_guarantee(DeliveryGuarantee.EXACTLY_ONCE)
    .set_transactional_id_prefix("pyflink-sink-")
    .build()
)

# 将DataStream输出到Kafka
ds.sink_to(kafka_sink)

env.execute("Flink Exactly-Once Job")
```

---

## 六、端到端Exactly-Once验证实验

### 6.1 实验设计

```
验证目标：证明在Checkpoint恢复后，Sink端数据不重复不丢失

实验步骤：
  1. 启动Flink作业（带Checkpoint，EXACTLY_ONCE Sink）
  2. 持续发送数据到Kafka source topic
  3. 运行5分钟后，Kill TaskManager
  4. 观察Flink自动从Checkpoint恢复
  5. 对比：恢复前后的Sink端数据
     - 总行数不应有跳跃（不丢失）
     - 每条数据唯一（不重复）

验证SQL：
  在ClickHouse中查询：
  SELECT COUNT(*) FROM sink_table;  -- 总行数应等于 source记录数
  SELECT COUNT(*) - COUNT(DISTINCT order_id) FROM sink_table;  -- 应等于0
```

### 6.2 验证脚本

```bash
#!/bin/bash
# exactly-once-verification.sh
# 端到端Exactly-Once验证脚本

echo "=== Exactly-Once 验证实验 ==="

# 1. 启动Flink Job
echo "[1] 启动Flink作业..."
flink run -d \
  -c com.example.ExactlyOnceJob \
  exactly-once-job.jar

# 2. 持续发送数据
echo "[2] 开始发送测试数据 (60秒)..."
python generate_test_data.py --duration 60 --rate 1000 &
DATA_PID=$!

# 3. 运行30秒后Kill TaskManager
sleep 30
echo "[3] Kill TaskManager..."
TM_CONTAINER=$(docker ps --filter "name=flink-taskmanager" -q | head -1)
docker kill $TM_CONTAINER
echo "TaskManager 已Kill，等待恢复..."

# 4. 等待Flink自动恢复
sleep 30
echo "[4] 检查Job状态..."
flink list

# 5. 验证数据一致性
echo "[5] 开始验证数据一致性..."

# 查询Source端的记录数（Kafka 中的消息数）
SOURCE_COUNT=$(kafka-run-class.sh kafka.tools.GetOffsetShell \
  --broker-list localhost:9092 \
  --topic source-topic \
  --time -1 | awk -F: '{sum+=$3} END {print sum}')

# 查询Sink端的记录数（ClickHouse中的行数）
SINK_COUNT=$(clickhouse-client --query \
  "SELECT COUNT() FROM sink_table")

# 查询Sink端的重复数
DUP_COUNT=$(clickhouse-client --query \
  "SELECT COUNT() - COUNT(DISTINCT order_id) FROM sink_table")

echo ""
echo "=== 验证结果 ==="
echo "Source端消息总数: $SOURCE_COUNT"
echo "Sink端记录总数:   $SINK_COUNT"
echo "Sink端重复记录数: $DUP_COUNT"
echo ""

if [ "$SOURCE_COUNT" -eq "$SINK_COUNT" ] && [ "$DUP_COUNT" -eq 0 ]; then
    echo "✓ Exactly-Once验证通过！"
else
    echo "✗ Exactly-Once验证失败！"
    echo "  Source-Sink差异: $((SOURCE_COUNT - SINK_COUNT))"
fi

wait $DATA_PID
```

### 6.3 生成测试数据脚本

```python
"""
generate_test_data.py - 测试数据生成器
"""
import time
import json
import random
import argparse
from kafka import KafkaProducer

parser = argparse.ArgumentParser()
parser.add_argument('--duration', type=int, default=60)
parser.add_argument('--rate', type=int, default=1000)
args = parser.parse_args()

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    acks='all',
    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
    compression_type='lz4',
)

end_time = time.time() + args.duration
order_id = 0
batch = []
BATCH_INTERVAL = 0.1  # 100ms一批

print(f"开始生成数据: duration={args.duration}s, rate={args.rate}/s")

while time.time() < end_time:
    order_id += 1
    batch.append({
        'order_id': order_id,
        'user_id': random.randint(1, 10000),
        'amount': round(random.uniform(10, 5000), 2),
        'category': random.choice(['电子', '服装', '食品', '图书', '家居']),
        'event_time': int(time.time() * 1000),
    })

    # 按速率发送
    if len(batch) >= args.rate * BATCH_INTERVAL:
        for msg in batch:
            producer.send('source-topic', value=msg)
        producer.flush()
        batch = []
        time.sleep(BATCH_INTERVAL)

# 发送剩余数据
for msg in batch:
    producer.send('source-topic', value=msg)
producer.flush()

print(f"数据生成完成: 共 {order_id} 条")
producer.close()
```

---

## 七、acks参数性能对比实验

### 7.1 Java对比代码

```java
import org.apache.kafka.clients.producer.*;
import org.apache.kafka.common.serialization.StringSerializer;
import java.util.Properties;
import java.util.concurrent.atomic.AtomicLong;

public class AcksComparison {

    static final String BOOTSTRAP = "localhost:9092";
    static final String TOPIC = "acks-comparison";
    static final int NUM_RECORDS = 500000;
    static final int RECORD_SIZE = 512;

    public static void main(String[] args) {
        String[] acksValues = {"0", "1", "all"};
        for (String acks : acksValues) {
            runBenchmark(acks);
        }
    }

    static void runBenchmark(String acks) {
        Properties props = new Properties();
        props.put("bootstrap.servers", BOOTSTRAP);
        props.put("key.serializer", StringSerializer.class.getName());
        props.put("value.serializer", StringSerializer.class.getName());
        props.put("acks", acks);
        props.put("batch.size", "65536");
        props.put("linger.ms", "5");
        props.put("compression.type", "lz4");
        props.put("buffer.memory", "67108864");

        KafkaProducer<String, String> producer = new KafkaProducer<>(props);

        AtomicLong successCount = new AtomicLong(0);
        AtomicLong totalLatency = new AtomicLong(0);
        long startTime = System.currentTimeMillis();

        String payload = new String(new char[RECORD_SIZE]).replace('\0', 'x');

        for (int i = 0; i < NUM_RECORDS; i++) {
            long sendStart = System.nanoTime();
            producer.send(new ProducerRecord<>(TOPIC, "key-" + i, payload),
                (metadata, exception) -> {
                    if (exception == null) {
                        successCount.incrementAndGet();
                        totalLatency.addAndGet(
                            (System.nanoTime() - sendStart) / 1_000_000);
                    }
                });
        }

        producer.flush();
        long elapsed = System.currentTimeMillis() - startTime;

        System.out.println("=== acks=" + acks + " ===");
        System.out.println("  发送数: " + NUM_RECORDS);
        System.out.println("  成功数: " + successCount.get());
        System.out.println("  总耗时: " + elapsed + "ms");
        System.out.printf("  吞吐量: %.0f 条/s%n",
            NUM_RECORDS * 1000.0 / elapsed);
        System.out.printf("  平均延迟: %.2f ms%n",
            totalLatency.get() * 1.0 / successCount.get());
        System.out.println();

        producer.close();
    }
}
```

### 7.2 Python对比代码

```python
import json
import time
import statistics
from kafka import KafkaProducer

BOOTSTRAP = ['localhost:9092']
TOPIC = 'acks-comparison'
NUM_RECORDS = 100000
RECORD_SIZE = 512

payload = 'x' * RECORD_SIZE

def run_benchmark(acks_value):
    producer = KafkaProducer(
        bootstrap_servers=BOOTSTRAP,
        acks=acks_value,
        batch_size=65536,
        linger_ms=5,
        compression_type='lz4',
        buffer_memory=67108864,
        value_serializer=lambda v: v.encode('utf-8'),
        key_serializer=lambda k: k.encode('utf-8') if k else None,
    )

    latencies = []
    start_time = time.time()

    for i in range(NUM_RECORDS):
        send_start = time.time()
        future = producer.send(TOPIC, key=f'key-{i}', value=payload)
        try:
            future.get(timeout=10)
            latency = (time.time() - send_start) * 1000
            latencies.append(latency)
        except Exception as e:
            pass

    producer.flush()
    elapsed = time.time() - start_time

    latencies.sort()
    p50 = latencies[int(len(latencies) * 0.50)]
    p95 = latencies[int(len(latencies) * 0.95)]
    p99 = latencies[int(len(latencies) * 0.99)]

    print(f"=== acks={acks_value} ===")
    print(f"  发送数: {NUM_RECORDS}")
    print(f"  成功数: {len(latencies)}")
    print(f"  总耗时: {elapsed:.1f}s")
    print(f"  吞吐量: {NUM_RECORDS / elapsed:.0f} 条/s")
    print(f"  平均延迟: {statistics.mean(latencies):.2f}ms")
    print(f"  P50: {p50:.2f}ms, P95: {p95:.2f}ms, P99: {p99:.2f}ms")
    print()

    producer.close()

if __name__ == '__main__':
    for acks in ['0', '1', 'all']:
        run_benchmark(acks)
```

### 7.3 预期对比结果

```
=== acks=0 ===
  吞吐量: ~420,000 条/s
  平均延迟: ~3ms
  P99: ~8ms
  可靠性: 可能丢数据，Leader写入前返回ACK

=== acks=1 ===
  吞吐量: ~320,000 条/s
  平均延迟: ~8ms
  P99: ~25ms
  可靠性: Leader确认写入，Follower未确认

=== acks=all ===
  吞吐量: ~250,000 条/s
  平均延迟: ~15ms
  P99: ~45ms
  可靠性: 所有ISR确认写入，最可靠

结论:
  acks=0 → acks=1: 吞吐下降约24%, 延迟增加约2.7倍
  acks=1 → acks=all: 吞吐下降约22%, 延迟增加约1.8倍
  acks=0 → acks=all: 吞吐下降约40%, 延迟增加约5倍
```

---

## 八、常见问题与最佳实践

### 7.1 事务ID（transactional.id）的设计

```yaml
最佳实践:
  # 格式: <service-name>-<instance-id>
  # 确保即使Pod重启，同一个逻辑实例使用相同的transactional.id
  
  # 好的例子:
  transactional.id: order-service-pod-0
  transactional.id: order-service-pod-1
  transactional.id: order-service-pod-2
  
  # 坏的例子（重启后ID变化）:
  transactional.id: order-service-<random-uuid>
  
  # 为什么重要：
  # 1. 事务ID相同的Producer重启后，可以Fence掉旧实例
  # 2. 旧实例的pending事务会被Abort
  # 3. 避免"僵尸Producer"问题
```

### 7.2 事务超时配置

```yaml
关键参数:
  transaction.timeout.ms: 60000  # Broker端，默认60秒
  transaction.max.timeout.ms: 900000  # Broker端最大值，默认15分钟
  # Producer端的 transaction.timeout.ms 不能超过 Broker端的 max

建议:
  - 单次事务不超过30秒
  - 大事务拆分为多个小事务
  - 对于长流程，使用"事务 + Offset提交"分开管理
```

### 7.3 性能影响

```
事务的性能代价:

开启事务 vs 不开启事务:
  - 延迟增加: 约5-10%（事务提交的额外开销）
  - 吞吐下降: 约3-5%
  - 额外IO：__transaction_state Topic的写入

优化建议:
  - 只在需要跨Topic/Partition原子写入时使用事务
  - 单Topic单Partition场景，使用幂等性即可
  - 事务内的消息数不要过少（每次提交都有开销）
```

---

## 九、课堂练习（45分钟）

### 练习1：编写事务性Producer（20分钟）

```python
from confluent_kafka import Producer
import json
import uuid
import time

producer_conf = {
    'bootstrap.servers': 'localhost:9092',
    'transactional.id': f'lab-tx-producer-{uuid.uuid4().hex[:8]}',
    'enable.idempotence': True,
    'acks': 'all',
    'transaction.timeout.ms': 60000,
}

producer = Producer(producer_conf)
producer.init_transactions()

try:
    producer.begin_transaction()

    for i in range(100):
        order = {
            'order_id': 1000 + i,
            'user_id': i % 50,
            'amount': round(100 + i * 1.5, 2),
            'status': 'created',
            'timestamp': int(time.time() * 1000)
        }
        producer.produce(
            topic='lab-tx-orders',
            key=str(order['order_id']),
            value=json.dumps(order),
        )

        if i == 50:
            detail = {
                'order_id': 1000 + i,
                'product_id': 2001,
                'quantity': 3,
                'unit_price': 99.00,
            }
            producer.produce(
                topic='lab-tx-order-items',
                key=f"{order['order_id']}-2001",
                value=json.dumps(detail),
            )

    producer.commit_transaction()
    print("事务提交成功: 100条订单 + 明细原子写入")

except Exception as e:
    producer.abort_transaction()
    print(f"事务回滚: {e}")

producer.flush()
```

**验证点**：用 `kafka-console-consumer.sh` 分别消费两个Topic，确认两个Topic要么都有数据，要么都没有。

### 练习2：观察Exactly-Once行为（15分钟）

```python
from confluent_kafka import Consumer, Producer, KafkaError
import json
import uuid

consumer_conf = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'lab-eos-consumer',
    'auto.offset.reset': 'earliest',
    'isolation.level': 'read_committed',
    'enable.auto.commit': False,
}

consumer = Consumer(consumer_conf)
consumer.subscribe(['lab-tx-orders'])

committed_count = 0
uncommitted_count = 0

try:
    for i in range(200):
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                break
            continue

        headers = msg.headers()
        is_committed = True
        if headers:
            for key, val in headers:
                if key == 'commitLatencyMs' or key == 'abortReason':
                    is_committed = False

        if is_committed:
            committed_count += 1
        else:
            uncommitted_count += 1

        order = json.loads(msg.value().decode('utf-8'))
        print(f"  offset={msg.offset()}, "
              f"order_id={order['order_id']}, "
              f"status={order.get('status', 'N/A')}")

except KeyboardInterrupt:
    pass
finally:
    consumer.close()

print(f"\n已提交事务消息: {committed_count}条")
print(f"未提交事务消息: {uncommitted_count}条")
```

**验证点**：使用 `isolation.level=read_committed` 时，只能看到已提交事务的消息；切换为 `read_uncommitted` 可以看到所有消息。

### 练习3：acks性能对比（10分钟）

```bash
kafka-topics.sh --create \
  --topic lab-acks-test \
  --partitions 6 \
  --replication-factor 3 \
  --bootstrap-server localhost:9092

for acks in 0 1 all; do
  echo "=== acks=$acks ==="
  kafka-producer-perf-test.sh \
    --topic lab-acks-test \
    --num-records 1000000 \
    --record-size 256 \
    --throughput -1 \
    --producer-props \
      bootstrap.servers=localhost:9092 \
      acks=$acks \
      batch.size=65536 \
      linger.ms=5 \
      compression.type=lz4 \
    --print-metrics 2>&1 | grep -E "records/sec|MB/sec|latency"
  echo ""
done
```

**验证点**：记录三种acks配置的吞吐量和延迟数据，填写对比表格。

---

## 十、课后作业

### 必做

1. **acks对比实验**：编写Producer程序，分别测试 acks=0 / acks=1 / acks=all 的吞吐量和延迟差异，生成对比报告（至少包含表格和图表）
2. **事务Producer代码**：用Java或Python编写事务Producer，原子写入2个不同Topic（模拟订单表+订单明细表），验证回滚场景
3. **端到端验证**：运行6.2节的验证脚本，确认Kill TaskManager后Exactly-Once成立

### 选做

1. 阅读Kafka源码中 `TransactionCoordinator` 类的实现（约2000行），写一篇源码分析文章
2. 搭建3节点Kafka集群，测试事务在不同Broker上的Transaction Coordinator分布
3. 设计一个实验，验证 `transactional.id` 相同的Producer实例重启后的Fencing机制

### 课后作业详细要求

**作业1：Consume-Transform-Produce Exactly-Once实现**

```python
from confluent_kafka import Consumer, Producer, KafkaError, TopicPartition
import json
import uuid

CONSUME_TOPIC = 'hw-source-orders'
PRODUCE_TOPIC = 'hw-enriched-orders'
BOOTSTRAP = 'localhost:9092'

consumer_conf = {
    'bootstrap.servers': BOOTSTRAP,
    'group.id': 'hw-ctp-group',
    'auto.offset.reset': 'earliest',
    'isolation.level': 'read_committed',
    'enable.auto.commit': False,
}

producer_conf = {
    'bootstrap.servers': BOOTSTRAP,
    'transactional.id': 'hw-ctp-producer-01',
    'enable.idempotence': True,
    'acks': 'all',
}

consumer = Consumer(consumer_conf)
producer = Producer(producer_conf)
producer.init_transactions()

consumer.subscribe([CONSUME_TOPIC])

BATCH_SIZE = 100
batch = []
offsets = []

try:
    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                continue
            print(f"消费错误: {msg.error()}")
            continue

        order = json.loads(msg.value().decode('utf-8'))

        enriched = {
            'order_id': order['order_id'],
            'user_id': order['user_id'],
            'amount': order['amount'],
            'category': order.get('category', 'unknown'),
            'amount_with_tax': round(order['amount'] * 1.13, 2),
            'is_large_order': order['amount'] > 1000,
            'process_time': int(__import__('time').time() * 1000),
        }

        batch.append(enriched)
        offsets.append(TopicPartition(msg.topic(), msg.partition(), msg.offset()))

        if len(batch) >= BATCH_SIZE:
            producer.begin_transaction()

            for enriched_order in batch:
                producer.produce(
                    topic=PRODUCE_TOPIC,
                    key=str(enriched_order['order_id']),
                    value=json.dumps(enriched_order),
                )

            for tp in offsets:
                producer.send_offsets_to_transaction(
                    [tp], consumer.consumer_group_metadata()
                )

            producer.commit_transaction()
            print(f"事务提交: {len(batch)}条消息, 原子写入+Offset提交")
            batch = []
            offsets = []

except KeyboardInterrupt:
    pass
except Exception as e:
    producer.abort_transaction()
    print(f"事务回滚: {e}")
finally:
    if batch:
        producer.begin_transaction()
        for enriched_order in batch:
            producer.produce(
                topic=PRODUCE_TOPIC,
                key=str(enriched_order['order_id']),
                value=json.dumps(enriched_order),
            )
        for tp in offsets:
            producer.send_offsets_to_transaction(
                [tp], consumer.consumer_group_metadata()
            )
        producer.commit_transaction()
    consumer.close()
    producer.flush()
```

输出要求：提交代码和运行截图，展示消费-转换-生产的完整流程，以及Kill Broker后恢复无重复的验证结果。

**作业2：事务回滚验证**

```python
from confluent_kafka import Producer, Consumer, KafkaError
import json
import uuid

producer_conf = {
    'bootstrap.servers': 'localhost:9092',
    'transactional.id': 'hw-rollback-test',
    'enable.idempotence': True,
    'acks': 'all',
}

producer = Producer(producer_conf)
producer.init_transactions()

producer.begin_transaction()

for i in range(50):
    producer.produce(
        topic='hw-rollback-topic',
        key=str(i),
        value=json.dumps({'id': i, 'data': f'normal-{i}'}),
    )

producer.abort_transaction()
print("事务1回滚: 50条消息不应被消费到")

producer.begin_transaction()

for i in range(30):
    producer.produce(
        topic='hw-rollback-topic',
        key=str(i),
        value=json.dumps({'id': i, 'data': f'committed-{i}'}),
    )

producer.commit_transaction()
print("事务2提交: 30条消息应被消费到")

producer.flush()

consumer_conf = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'hw-rollback-verifier',
    'auto.offset.reset': 'earliest',
    'isolation.level': 'read_committed',
    'enable.auto.commit': True,
}

consumer = Consumer(consumer_conf)
consumer.subscribe(['hw-rollback-topic'])

count = 0
try:
    for i in range(100):
        msg = consumer.poll(2.0)
        if msg is None:
            if count > 0:
                break
            continue
        if msg.error():
            continue
        data = json.loads(msg.value().decode('utf-8'))
        print(f"  消费到: id={data['id']}, data={data['data']}")
        count += 1
except KeyboardInterrupt:
    pass
finally:
    consumer.close()

print(f"\n共消费到 {count} 条消息 (预期30条，来自已提交事务)")
```

输出要求：提交运行截图，验证回滚事务的消息不可见，只有提交事务的消息被消费到。

---

## 九、参考资料

- [Kafka Exactly-Once Semantics (Confluent Blog)](https://www.confluent.io/blog/exactly-once-semantics-are-possible-heres-how-apache-kafka-does-it/)
- [Kafka Transactions (Confluent Blog)](https://www.confluent.io/blog/transactions-apache-kafka/)
- [Flink End-to-End Exactly-Once](https://flink.apache.org/features/2018/03/01/end-to-end-exactly-once-apache-flink.html)
- [KIP-98: Exactly Once Delivery and Transactional Messaging](https://cwiki.apache.org/confluence/display/KAFKA/KIP-98+-+Exactly+Once+Delivery+and+Transactional+Messaging)
- [KIP-129: Streams Exactly-Once Semantics](https://cwiki.apache.org/confluence/display/KAFKA/KIP-129%3A+Streams+Exactly-Once+Semantics)