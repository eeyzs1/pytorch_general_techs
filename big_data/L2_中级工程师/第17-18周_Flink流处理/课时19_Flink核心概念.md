# 课时19：Flink核心概念

> **所属阶段**：L2 中级工程师 | **周次**：第17-18周 | **课时**：3h | **难度**：★★★★☆

---

## 一、教学目标

1. 理解Flink vs Spark Streaming的架构差异（真流 vs 微批）
2. 掌握DataStream API核心抽象
3. 理解Event Time vs Processing Time vs Ingestion Time
4. 深入理解Watermark机制：解决乱序数据问题
5. 掌握Window类型及使用场景

---

## 二、Flink vs Spark Streaming：架构差异

### 2.1 处理模型对比

```
Spark Streaming (微批处理):

时间轴 ──────────────────────────────────────────────→
Batch1    Batch2    Batch3    Batch4    Batch5
  │         │         │         │         │
  ▼         ▼         ▼         ▼         ▼
[DStream] [DStream] [DStream] [DStream] [DStream]
 Batch1    Batch2    Batch3    Batch4    Batch5
 (1秒)     (1秒)     (1秒)     (1秒)     (1秒)

特点：
  - 每个Batch是一个小的RDD作业
  - 延迟受Batch间隔限制（最小~100ms）
  - 编程模型和批处理一致（简单）
  - 延迟不适用于毫秒级场景
```

```
Flink (真正的流处理):

时间轴 ──────────────────────────────────────────────→
event1 event2 event3 event4 event5 event6 event7 ...
  │      │      │      │      │      │      │
  ▼      ▼      ▼      ▼      ▼      ▼      ▼
[算子链] → → → → → → → → → → → → → → → → → → → → → →

特点：
  - 每条数据到达后立即处理
  - 延迟低至毫秒级
  - 天然支持Event Time
  - 同一个引擎处理流和批（批是有界的流）
```

### 2.2 关键区别总结

| 维度 | Spark Streaming | Flink |
|------|----------------|-------|
| 处理模型 | 微批(Micro-Batch) | 逐条事件(Event-by-Event) |
| 延迟 | 秒级(最低100ms) | 毫秒级 |
| 时间语义 | Processing Time为主 | Event Time原生支持 |
| Checkpoint | 基于RDD Lineage | 基于Chandy-Lamport算法 |
| 状态管理 | updateStateByKey/MapWithState | Managed State + StateBackend |
| 窗口 | 固定间隔滑动窗口 | Tumbling/Sliding/Session/Global |
| 背压 | 天然（微批天然限流） | 基于Credit的流量控制 |
| API | DStream(旧)/Structured Streaming(新) | DataStream API + Table API/SQL |

---

## 三、Flink核心编程模型

### 3.1 编程抽象层次

```
Flink API 层级金字塔:

         SQL / Table API          ← 最高级（声明式）
       ───────────────────
       DataStream / DataSet API   ← 核心API（程序式）
     ───────────────────────
     ProcessFunction              ← 底层API（精细控制）
   ─────────────────────────
   State & Time                  ← 基础能力（状态+时间）
```

### 3.2 DataStream API核心组件

```
┌─────────────────────────────────────────────────────┐
│                  Flink Job                          │
│                                                     │
│  Source ──→ Transform ──→ Transform ──→ Sink        │
│    │            │             │            │         │
│  Kafka       Map           Window      Kafka        │
│  File        FlatMap       KeyBy       File         │
│  Socket      Filter        聚合        JDBC         │
│  Custom      Process       Join       Custom        │
│                                                     │
│  ① 数据输入   ② 数据转换    ③ 窗口聚合   ④ 数据输出   │
└─────────────────────────────────────────────────────┘
```

---

## 四、时间语义深度解析

### 4.1 三种时间

```
Event Time (事件时间):
  - 数据真正产生的时间（最常用）
  - 嵌入在数据本身中（如日志中的时间戳）
  - 不受网络延迟影响
  - 挑战：乱序和延迟数据

Processing Time (处理时间):
  - Flink算子处理该数据时的系统时间
  - 最简单，性能最好
  - 缺点：结果不确定，重跑结果不一样

Ingestion Time (摄入时间):
  - 数据进入Flink的时间（Source算子记录）
  - Event Time和Processing Time的折中
  - 较少使用
```

### 4.2 为什么需要Event Time

```
场景：计算每分钟的交易额

Processing Time的问题:
  10:00:00~10:01:00窗口:
    收到 event(09:59:50, 金额100) → 计入窗口
    收到 event(10:00:30, 金额200) → 计入窗口
  
  重放数据(不一样的结果!):
  09:59:50~10:00:50窗口:
    收到 event(09:59:50, 金额100) → 计入窗口
    收到 event(10:00:30, 金额200) → 计入窗口
  
  Processing Time下，相同数据重跑可能得到不同结果！

Event Time的解决:
  10:00:00~10:01:00窗口（按事件时间）:
    event(09:59:50, 金额100) → 窗口[09:59:00~10:00:00]
    event(10:00:30, 金额200) → 窗口[10:00:00~10:01:00]
  
  无论数据何时到达，结果始终一致！
```

---

## 五、Watermark机制详解

### 5.1 Watermark概念

```
Watermark = "Flink告诉你，Event Time为T的数据已经全部到了"

工作原理:
  Watermark = Max(已见EventTime) - 允许延迟(OutOfOrderness)

示例（允许延迟=5秒）:
  时间轴 ────────────────────────────────────────────→

  到达事件:  E(12:00:01)  E(12:00:03)  E(12:00:05)  E(11:59:58)
  事件时间:   12:00:01     12:00:03     12:00:05     11:59:58

  Watermark变化:
  E(12:00:01)到达:  Max=12:00:01, WM=12:00:01-5s=11:59:56
  E(12:00:03)到达:  Max=12:00:03, WM=12:00:03-5s=11:59:58
  E(12:00:05)到达:  Max=12:00:05, WM=12:00:05-5s=12:00:00
  E(11:59:58)到达:  Max=12:00:05, WM=12:00:00（迟到数据不推进WM）

  窗口触发:
  窗口 [11:59:00~12:00:00] → WM>=12:00:00时触发
```

### 5.2 Watermark完整图解

```
场景: 1分钟滚动窗口，允许5秒延迟

数据到达顺序（乱序）:
  序号  到达时间      事件时间    内容
  ─────────────────────────────────
  1    10:00:01     10:00:01    事件A
  2    10:00:02     10:00:04    事件C  ← 比A晚到但事件时间更晚
  3    10:00:03     10:00:02    事件B  ← 顺序来了！事件时间在A和C之间
  4    10:01:05     10:01:05    事件E  ← Watermark推进！
  5    10:01:06     10:01:03    事件D  ← 迟到数据（事件时间比Watermark小）

处理过程:
  Step1: E(A)到达, ts=10:00:01, Max=10:00:01, WM=09:59:56
         窗口[10:00:00~10:01:00)尚未触发（WM<10:01:00）

  Step2: E(C)到达, ts=10:00:04, Max=10:00:04, WM=09:59:59
         窗口[10:00:00~10:01:00)尚未触发

  Step3: E(B)到达, ts=10:00:02, Max=10:00:04, WM=09:59:59
         ts=10:00:02 < Max, WM不推进

  Step4: E(E)到达, ts=10:01:05, Max=10:01:05, WM=10:01:00
         WM=10:01:00 >= 窗口结束时间10:01:00
         → 触发窗口[10:00:00~10:01:00)计算
         → 包含事件: A(10:00:01), B(10:00:02), C(10:00:04)

  Step5: E(D)到达, ts=10:01:03, Max=10:01:05, WM=10:01:00
         ts=10:01:03 < WM=10:01:00 → 迟到数据!
         处理方式取决于Side Output配置
```

### 5.3 Watermark生成策略

```java
// 策略1: 固定延迟Watermark（最常用）
WatermarkStrategy
    .<OrderEvent>forBoundedOutOfOrderness(Duration.ofSeconds(5))
    .withTimestampAssigner((event, timestamp) -> event.getEventTime());

// 策略2: 单调递增Watermark（数据严格有序）
WatermarkStrategy
    .<OrderEvent>forMonotonousTimestamps()
    .withTimestampAssigner((event, timestamp) -> event.getEventTime());

// 策略3: 自定义Watermark生成器
WatermarkStrategy
    .<OrderEvent>forGenerator(new WatermarkGenerator<OrderEvent>() {
        private long maxTimestamp = Long.MIN_VALUE;
        
        @Override
        public void onEvent(OrderEvent event, long eventTimestamp, 
                           WatermarkOutput output) {
            maxTimestamp = Math.max(maxTimestamp, eventTimestamp);
        }
        
        @Override
        public void onPeriodicEmit(WatermarkOutput output) {
            output.emitWatermark(new Watermark(maxTimestamp - 5000));
        }
    })
    .withTimestampAssigner((event, timestamp) -> event.getEventTime());
```

---

## 六、Window类型详解

### 6.1 四种窗口对比

```
Tumbling Windows (滚动窗口):
  窗口大小固定，不重叠
  
  Window Size = 10秒
  ├── Window1 ──┤├── Window2 ──┤├── Window3 ──┤
  0            10            20            30
  [0,10)       [10,20)       [20,30)

Sliding Windows (滑动窗口):
  窗口大小固定，可以重叠
  
  Window Size = 10秒, Slide = 5秒
  ├── Window1 ──┤
     ├── Window2 ──┤
        ├── Window3 ──┤
  0    5    10   15   20
  [0,10) [5,15) [10,20)

Session Windows (会话窗口):
  基于活动间隔，动态窗口
  
  事件: event1 event2      event3    event4 event5
  间隔:     ├─2s─┤   ├─20s──┤   ├─3s─┤
  
  如果 Gap > 10秒 → 新Session
  Session1 = [event1, event2]  (间隔2s < 10s)
  Session2 = [event3]           (与前一个间隔20s > 10s → 新窗口)
  Session3 = [event4, event5]  (间隔3s < 10s)

Global Windows (全局窗口):
  所有数据放入一个窗口，不自动触发
  需要自定义Trigger
```

### 6.2 窗口API示例

```java
DataStream<OrderEvent> stream = ...;

// 滚动窗口：每分钟统计
stream
    .keyBy(OrderEvent::getCategory)
    .window(TumblingEventTimeWindows.of(Time.minutes(1)))
    .aggregate(new OrderAggregator());

// 滑动窗口：每30秒统计过去60秒的数据
stream
    .keyBy(OrderEvent::getCategory)
    .window(SlidingEventTimeWindows.of(Time.seconds(60), Time.seconds(30)))
    .aggregate(new OrderAggregator());

// 会话窗口：30秒无数据则新建窗口
stream
    .keyBy(OrderEvent::getUserId)
    .window(EventTimeSessionWindows.withGap(Time.seconds(30)))
    .aggregate(new SessionAggregator());

// 全局窗口 + 自定义Trigger
stream
    .keyBy(OrderEvent::getCategory)
    .window(GlobalWindows.create())
    .trigger(CountTrigger.of(100))  // 每100条触发一次
    .aggregate(new OrderAggregator());
```

### 6.3 窗口类型对比表与完整代码示例

| 维度 | Tumbling Window | Sliding Window | Session Window | Global Window |
|------|----------------|----------------|----------------|---------------|
| 窗口大小 | 固定 | 固定 | 动态(由Gap决定) | 无限大 |
| 重叠 | 无 | 有(Slide < Size) | 无 | N/A |
| 触发条件 | Watermark越过窗口结束 | Watermark越过窗口结束 | Gap超时 | 自定义Trigger |
| 适用场景 | 每分钟/每小时统计 | 滑动平均、趋势分析 | 用户会话分析 | 自定义聚合 |
| 状态大小 | 小(无重叠) | 中(有重叠) | 不确定 | 大(需手动清理) |
| 数据归属 | 每条数据属于1个窗口 | 每条数据可能属于多个窗口 | 每条数据属于1个窗口 | 所有数据同一窗口 |

**Tumbling Window 完整代码：每分钟按品类统计交易额**

```java
DataStream<OrderEvent> eventStream = ...;

DataStream<CategoryStats> tumblingResult = eventStream
    .keyBy(OrderEvent::getCategoryId)
    .window(TumblingEventTimeWindows.of(Time.minutes(1)))
    .aggregate(new AggregateFunction<OrderEvent, Tuple2<Long, Double>, CategoryStats>() {
        @Override
        public Tuple2<Long, Double> createAccumulator() {
            return Tuple2.of(0L, 0.0);
        }

        @Override
        public Tuple2<Long, Double> add(OrderEvent event, Tuple2<Long, Double> acc) {
            return Tuple2.of(acc.f0 + 1, acc.f1 + event.getAmount());
        }

        @Override
        public CategoryStats getResult(Tuple2<Long, Double> acc) {
            return new CategoryStats(0, 0, 0, acc.f0, 0);
        }

        @Override
        public Tuple2<Long, Double> merge(Tuple2<Long, Double> a, Tuple2<Long, Double> b) {
            return Tuple2.of(a.f0 + b.f0, a.f1 + b.f1);
        }
    });

tumblingResult.print();
```

**Sliding Window 完整代码：每30秒统计过去1分钟的交易额**

```java
DataStream<CategoryStats> slidingResult = eventStream
    .keyBy(OrderEvent::getCategoryId)
    .window(SlidingEventTimeWindows.of(Time.minutes(1), Time.seconds(30)))
    .aggregate(new AggregateFunction<OrderEvent, Tuple2<Long, Double>, CategoryStats>() {
        @Override
        public Tuple2<Long, Double> createAccumulator() {
            return Tuple2.of(0L, 0.0);
        }

        @Override
        public Tuple2<Long, Double> add(OrderEvent event, Tuple2<Long, Double> acc) {
            return Tuple2.of(acc.f0 + 1, acc.f1 + event.getAmount());
        }

        @Override
        public CategoryStats getResult(Tuple2<Long, Double> acc) {
            return new CategoryStats(0, 0, 0, acc.f0, 0);
        }

        @Override
        public Tuple2<Long, Double> merge(Tuple2<Long, Double> a, Tuple2<Long, Double> b) {
            return Tuple2.of(a.f0 + b.f0, a.f1 + b.f1);
        }
    });

slidingResult.print();
```

**Session Window 完整代码：用户会话分析**

```java
DataStream<UserSessionStats> sessionResult = eventStream
    .keyBy(OrderEvent::getUserId)
    .window(EventTimeSessionWindows.withGap(Time.minutes(5)))
    .process(new ProcessWindowFunction<OrderEvent, UserSessionStats, Long, TimeWindow>() {
        @Override
        public void process(Long userId,
                           Context context,
                           Iterable<OrderEvent> events,
                           Collector<UserSessionStats> out) {
            long count = 0;
            double totalAmount = 0;
            Set<Integer> categories = new HashSet<>();
            for (OrderEvent e : events) {
                count++;
                totalAmount += e.getAmount();
                categories.add(e.getCategoryId());
            }
            out.collect(new UserSessionStats(
                userId,
                context.window().getStart(),
                context.window().getEnd(),
                count,
                totalAmount,
                categories.size()
            ));
        }
    });

sessionResult.print();
```

---

## 七、完整DataStream代码：实时PV/UV统计

### 7.1 Java实现

```java
import org.apache.flink.api.common.eventtime.*;
import org.apache.flink.api.common.functions.AggregateFunction;
import org.apache.flink.api.common.serialization.SimpleStringSchema;
import org.apache.flink.api.java.tuple.Tuple2;
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.streaming.api.windowing.assigners.TumblingEventTimeWindows;
import org.apache.flink.streaming.api.windowing.time.Time;
import org.apache.flink.streaming.connectors.kafka.FlinkKafkaConsumer;
import org.apache.flink.streaming.connectors.kafka.FlinkKafkaProducer;
import com.alibaba.fastjson.JSON;
import com.alibaba.fastjson.JSONObject;

import java.time.Duration;
import java.util.HashSet;
import java.util.Properties;

public class RealTimePVUV {

    public static void main(String[] args) throws Exception {
        StreamExecutionEnvironment env = 
            StreamExecutionEnvironment.getExecutionEnvironment();
        
        // 设置Checkpoint（容错）
        env.enableCheckpointing(5000);
        env.getCheckpointConfig().setCheckpointTimeout(60000);

        // ====== 1. Source: 从Kafka读取数据 ======
        Properties kafkaProps = new Properties();
        kafkaProps.setProperty("bootstrap.servers", "localhost:9092");
        kafkaProps.setProperty("group.id", "flink-pv-uv-consumer");
        kafkaProps.setProperty("auto.offset.reset", "latest");

        FlinkKafkaConsumer<String> kafkaSource = new FlinkKafkaConsumer<>(
            "user-behavior",
            new SimpleStringSchema(),
            kafkaProps
        );

        DataStream<String> sourceStream = env.addSource(kafkaSource);

        // ====== 2. 解析数据 + 设置Watermark ======
        DataStream<UserBehaviorEvent> eventStream = sourceStream
            .map(line -> {
                JSONObject obj = JSON.parseObject(line);
                return new UserBehaviorEvent(
                    obj.getLong("user_id"),
                    obj.getLong("item_id"),
                    obj.getInteger("category_id"),
                    obj.getString("behavior"),
                    obj.getLong("timestamp")
                );
            })
            .assignTimestampsAndWatermarks(
                WatermarkStrategy
                    .<UserBehaviorEvent>forBoundedOutOfOrderness(
                        Duration.ofSeconds(5))
                    .withTimestampAssigner(
                        (event, ts) -> event.getTimestamp())
            );

        // ====== 3. 按品类分组 → 1分钟滚动窗口 → 计算PV/UV ======
        DataStream<CategoryStats> statsStream = eventStream
            .keyBy(UserBehaviorEvent::getCategoryId)
            .window(TumblingEventTimeWindows.of(Time.minutes(1)))
            .aggregate(new PvUvAggregateFunction());

        // ====== 4. 打印结果（生产环境改为Sink到ClickHouse/Kafka）=====
        statsStream
            .map(stats -> JSON.toJSONString(stats))
            .print();

        // ====== 5. 写入Kafka Sink（供下游消费）======
        FlinkKafkaProducer<String> kafkaSink = new FlinkKafkaProducer<>(
            "category-stats",
            new SimpleStringSchema(),
            kafkaProps
        );

        statsStream
            .map(stats -> JSON.toJSONString(stats))
            .addSink(kafkaSink);

        env.execute("Real-Time PV/UV Statistics");
    }

    // ====== 数据模型 ======
    public static class UserBehaviorEvent {
        private long userId;
        private long itemId;
        private int categoryId;
        private String behavior;
        private long timestamp;

        public UserBehaviorEvent() {}
        
        public UserBehaviorEvent(long userId, long itemId, int categoryId,
                                 String behavior, long timestamp) {
            this.userId = userId;
            this.itemId = itemId;
            this.categoryId = categoryId;
            this.behavior = behavior;
            this.timestamp = timestamp;
        }

        public long getUserId() { return userId; }
        public long getItemId() { return itemId; }
        public int getCategoryId() { return categoryId; }
        public String getBehavior() { return behavior; }
        public long getTimestamp() { return timestamp; }
    }

    public static class CategoryStats {
        private int categoryId;
        private long windowStart;
        private long windowEnd;
        private long pv;
        private long uv;

        public CategoryStats() {}

        public CategoryStats(int categoryId, long windowStart, long windowEnd,
                            long pv, long uv) {
            this.categoryId = categoryId;
            this.windowStart = windowStart;
            this.windowEnd = windowEnd;
            this.pv = pv;
            this.uv = uv;
        }

        public int getCategoryId() { return categoryId; }
        public long getWindowStart() { return windowStart; }
        public long getWindowEnd() { return windowEnd; }
        public long getPv() { return pv; }
        public long getUv() { return uv; }

        @Override
        public String toString() {
            return String.format(
                "CategoryStats{category=%d, window=[%d,%d], PV=%d, UV=%d}",
                categoryId, windowStart, windowEnd, pv, uv);
        }
    }

    // ====== 聚合函数 ======
    public static class PvUvAggregateFunction 
        implements AggregateFunction<UserBehaviorEvent, PvUvAccumulator, CategoryStats> {

        @Override
        public PvUvAccumulator createAccumulator() {
            return new PvUvAccumulator();
        }

        @Override
        public PvUvAccumulator add(UserBehaviorEvent event, PvUvAccumulator acc) {
            acc.pv += 1;
            acc.userIds.add(event.getUserId());
            return acc;
        }

        @Override
        public CategoryStats getResult(PvUvAccumulator acc) {
            return new CategoryStats(0, 0, 0, acc.pv, acc.userIds.size());
        }

        @Override
        public PvUvAccumulator merge(PvUvAccumulator a, PvUvAccumulator b) {
            PvUvAccumulator merged = new PvUvAccumulator();
            merged.pv = a.pv + b.pv;
            merged.userIds.addAll(a.userIds);
            merged.userIds.addAll(b.userIds);
            return merged;
        }
    }

    public static class PvUvAccumulator {
        long pv = 0;
        HashSet<Long> userIds = new HashSet<>();
    }
}
```

### 7.2 Python（PyFlink）实现

```python
"""
实时PV/UV统计 - PyFlink DataStream API实现
安装依赖: pip install apache-flink==1.17.1
"""
import json
from pyflink.datastream import StreamExecutionEnvironment, RuntimeContext
from pyflink.datastream.functions import (
    MapFunction, AggregateFunction, ProcessWindowFunction
)
from pyflink.common import WatermarkStrategy, Duration, Time, Types
from pyflink.common.watermark_strategy import TimestampAssigner
from pyflink.datastream.window import TumblingEventTimeWindows
from pyflink.datastream.connectors.kafka import (
    FlinkKafkaConsumer, FlinkKafkaProducer
)
from pyflink.common.serialization import SimpleStringSchema


class UserBehaviorEvent:
    def __init__(self, user_id=None, item_id=None, category_id=None,
                 behavior=None, timestamp=None):
        self.user_id = user_id
        self.item_id = item_id
        self.category_id = category_id
        self.behavior = behavior
        self.timestamp = timestamp


class CategoryStats:
    def __init__(self, category_id=0, window_start=0, window_end=0,
                 pv=0, uv=0):
        self.category_id = category_id
        self.window_start = window_start
        self.window_end = window_end
        self.pv = pv
        self.uv = uv

    def __str__(self):
        return (f"CategoryStats(category={self.category_id}, "
                f"window=[{self.window_start},{self.window_end}], "
                f"PV={self.pv}, UV={self.uv})")


class JsonToEventMap(MapFunction):
    def map(self, value):
        obj = json.loads(value)
        return UserBehaviorEvent(
            user_id=obj['user_id'],
            item_id=obj['item_id'],
            category_id=obj['category_id'],
            behavior=obj['behavior'],
            timestamp=obj['timestamp']
        )


class EventTimestampAssigner(TimestampAssigner):
    def extract_timestamp(self, element, record_timestamp):
        return element.timestamp


class PvUvAggregate(AggregateFunction):
    def create_accumulator(self):
        return {'pv': 0, 'user_ids': set()}

    def add(self, value, accumulator):
        accumulator['pv'] += 1
        accumulator['user_ids'].add(value.user_id)
        return accumulator

    def get_result(self, accumulator):
        return CategoryStats(
            pv=accumulator['pv'],
            uv=len(accumulator['user_ids'])
        )

    def merge(self, a, b):
        return {
            'pv': a['pv'] + b['pv'],
            'user_ids': a['user_ids'] | b['user_ids']
        }


def create_kafka_source(env):
    """创建Kafka Source"""
    kafka_props = {
        'bootstrap.servers': 'localhost:9092',
        'group.id': 'flink-pv-uv-consumer',
        'auto.offset.reset': 'latest',
    }

    kafka_source = FlinkKafkaConsumer(
        topics='user-behavior',
        deserialization_schema=SimpleStringSchema(),
        properties=kafka_props
    )
    kafka_source.set_start_from_latest()

    return env.add_source(kafka_source)


def main():
    env = StreamExecutionEnvironment.get_execution_environment()
    env.set_parallelism(2)

    # Checkpoint配置
    env.enable_checkpointing(5000)
    env.get_checkpoint_config().set_checkpoint_timeout(60000)

    # Source
    source_stream = create_kafka_source(env)

    # 解析事件 + 设置Watermark
    event_stream = (source_stream
        .map(JsonToEventMap(), output_type=Types.PICKLED_BYTE_ARRAY())
        .assign_timestamps_and_watermarks(
            WatermarkStrategy
            .for_bounded_out_of_orderness(Duration.of_seconds(5))
            .with_timestamp_assigner(EventTimestampAssigner())
        )
    )

    # 按品类分组 → 1分钟滚动窗口 → 计算PV/UV
    stats_stream = (event_stream
        .key_by(lambda e: e.category_id)
        .window(TumblingEventTimeWindows.of(Time.minutes(1)))
        .aggregate(PvUvAggregate())
    )

    # 输出到控制台
    stats_stream.map(
        lambda s: str(s),
        output_type=Types.STRING()
    ).print()

    env.execute("Real-Time PV/UV Statistics (PyFlink)")


if __name__ == '__main__':
    main()
```

---

## 八、迟到数据处理

### 8.1 Side Output（侧输出）

```java
// 定义侧输出标签
final OutputTag<OrderEvent> lateOutputTag = 
    new OutputTag<OrderEvent>("late-data") {};

DataStream<CategoryStats> result = eventStream
    .keyBy(OrderEvent::getCategoryId)
    .window(TumblingEventTimeWindows.of(Time.minutes(1)))
    // 允许迟到数据（窗口触发后仍允许迟到的数据更新结果）
    .allowedLateness(Time.seconds(30))
    // 超过allowedLateness的数据进入侧输出
    .sideOutputLateData(lateOutputTag)
    .aggregate(new OrderAggregator());

// 获取迟到数据，写入死信队列
DataStream<OrderEvent> lateStream = result.getSideOutput(lateOutputTag);
lateStream
    .map(event -> "LATE: " + event.toString())
    .addSink(new FlinkKafkaProducer<>("late-data-topic", 
        new SimpleStringSchema(), kafkaProps));
```

### 8.2 迟到数据三级处理策略

```
第一级: Watermark容忍
  forBoundedOutOfOrderness(Duration.ofSeconds(5))
  → 迟到5秒内的数据正常处理

第二级: allowedLateness
  .allowedLateness(Time.seconds(30))
  → 窗口触发后，额外等待30秒，迟到的数据仍可更新结果
  → 代价：需要保持窗口状态30秒

第三级: Side Output
  .sideOutputLateData(lateOutputTag)
  → 超过allowedLateness的数据进入侧输出
  → 可写入死信队列供后续分析
```

---

## 九、课堂练习（45分钟）

### 练习1：编写Flink Job使用Event Time和Tumbling Window（20分钟）

```java
import org.apache.flink.api.common.eventtime.*;
import org.apache.flink.api.common.functions.AggregateFunction;
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.streaming.api.windowing.assigners.TumblingEventTimeWindows;
import org.apache.flink.streaming.api.windowing.time.Time;
import org.apache.flink.streaming.api.functions.source.SourceFunction;
import java.util.Random;
import java.util.concurrent.TimeUnit;

public class LabTumblingWindowJob {

    public static void main(String[] args) throws Exception {
        StreamExecutionEnvironment env =
            StreamExecutionEnvironment.getExecutionEnvironment();
        env.setParallelism(1);
        env.enableCheckpointing(5000);

        DataStream<ClickEvent> clicks = env
            .addSource(new ClickEventSource())
            .assignTimestampsAndWatermarks(
                WatermarkStrategy
                    .<ClickEvent>forBoundedOutOfOrderness(
                        java.time.Duration.ofSeconds(5))
                    .withTimestampAssigner(
                        (event, ts) -> event.getTimestamp())
            );

        DataStream<WindowResult> result = clicks
            .keyBy(ClickEvent::getPage)
            .window(TumblingEventTimeWindows.of(Time.seconds(30)))
            .aggregate(new ClickAggregateFunction());

        result.print();

        env.execute("Lab: Tumbling Window with Event Time");
    }

    public static class ClickEvent {
        public String page;
        public String userId;
        public long timestamp;

        public ClickEvent() {}

        public ClickEvent(String page, String userId, long timestamp) {
            this.page = page;
            this.userId = userId;
            this.timestamp = timestamp;
        }

        public String getPage() { return page; }
        public String getUserId() { return userId; }
        public long getTimestamp() { return timestamp; }

        @Override
        public String toString() {
            return String.format("ClickEvent{page=%s, user=%s, ts=%d}",
                page, userId, timestamp);
        }
    }

    public static class WindowResult {
        public String page;
        public long windowStart;
        public long windowEnd;
        public long pv;
        public long uv;

        public WindowResult() {}

        public WindowResult(String page, long windowStart,
                           long windowEnd, long pv, long uv) {
            this.page = page;
            this.windowStart = windowStart;
            this.windowEnd = windowEnd;
            this.pv = pv;
            this.uv = uv;
        }

        @Override
        public String toString() {
            return String.format(
                "WindowResult{page=%s, window=[%d,%d], PV=%d, UV=%d}",
                page, windowStart, windowEnd, pv, uv);
        }
    }

    public static class ClickAggregateFunction
        implements AggregateFunction<ClickEvent,
            java.util.Set<String>, WindowResult> {

        @Override
        public java.util.Set<String> createAccumulator() {
            return new java.util.HashSet<>();
        }

        @Override
        public java.util.Set<String> add(ClickEvent event,
                                         java.util.Set<String> acc) {
            acc.add(event.getUserId() + "@" + event.timestamp);
            return acc;
        }

        @Override
        public WindowResult getResult(java.util.Set<String> acc) {
            return new WindowResult("", 0, 0, acc.size(), acc.size());
        }

        @Override
        public java.util.Set<String> merge(java.util.Set<String> a,
                                           java.util.Set<String> b) {
            a.addAll(b);
            return a;
        }
    }

    public static class ClickEventSource implements SourceFunction<ClickEvent> {
        private volatile boolean running = true;
        private final Random random = new Random();
        private final String[] pages = {"home", "product", "cart", "checkout"};
        private final String[] users = {"u1", "u2", "u3", "u4", "u5"};

        @Override
        public void run(SourceContext<ClickEvent> ctx) throws Exception {
            long baseTime = System.currentTimeMillis() - 60000;
            while (running) {
                long eventTime = baseTime +
                    random.nextInt(120000) - 60000;
                String page = pages[random.nextInt(pages.length)];
                String user = users[random.nextInt(users.length)];
                ctx.collect(new ClickEvent(page, user, eventTime));
                Thread.sleep(100);
            }
        }

        @Override
        public void cancel() {
            running = false;
        }
    }
}
```

**验证点**：观察30秒滚动窗口的触发时机，确认窗口在Watermark推进后触发。

### 练习2：观察Watermark推进与窗口触发（15分钟）

```python
import json
import time
import random
from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    acks='all',
    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
)

base_time = int(time.time() * 1000)

for i in range(200):
    event = {
        "user_id": f"user_{random.randint(1, 20)}",
        "page": random.choice(["home", "product", "cart", "checkout"]),
        "action": random.choice(["click", "scroll", "purchase"]),
        "timestamp": base_time + i * 500 + random.randint(-3000, 3000),
    }
    producer.send('lab-user-behavior', value=event)

for i in range(50):
    event = {
        "user_id": f"user_{random.randint(1, 20)}",
        "page": random.choice(["home", "product"]),
        "action": "click",
        "timestamp": base_time + 100000 + i * 500,
    }
    producer.send('lab-user-behavior', value=event)

producer.flush()
print("250条用户行为数据已发送（含乱序数据）")
producer.close()
```

**验证点**：观察Flink日志中Watermark的推进，确认乱序数据被正确处理，窗口在Watermark到达后触发。

### 练习3：对比Tumbling和Sliding窗口输出（10分钟）

```java
DataStream<ClickEvent> eventStream = ...;

DataStream<String> tumblingResult = eventStream
    .keyBy(ClickEvent::getPage)
    .window(TumblingEventTimeWindows.of(Time.minutes(1)))
    .aggregate(new ClickAggregateFunction())
    .map(r -> "[Tumbling] " + r.toString());

DataStream<String> slidingResult = eventStream
    .keyBy(ClickEvent::getPage)
    .window(SlidingEventTimeWindows.of(Time.minutes(1), Time.seconds(30)))
    .aggregate(new ClickAggregateFunction())
    .map(r -> "[Sliding] " + r.toString());

tumblingResult.union(slidingResult).print();
```

**验证点**：对比Tumbling和Sliding窗口的输出频率和内容差异，Sliding窗口每30秒输出一次，Tumbling窗口每60秒输出一次。

---

## 十、课后作业

### 必做

1. **PV/UV编程**：用Java或Python实现本课时的完整PV/UV统计程序，从Kafka读取数据并输出
2. **乱序实验**：故意向Kafka发送乱序数据（事件时间随机偏移±10秒），观察Watermark和窗口触发行为，截图记录
3. **窗口对比**：用相同数据源分别实现Tumbling/Sliding/Session窗口，对比三种窗口的输出差异

### 选做

1. 实现完整的迟到数据处理三级策略，监控各策略处理的数据量
2. 阅读Flink源码中 `WatermarkGenerator` 和 `InternalTimerService` 的实现
3. 测试不同并行度下Watermark的对齐行为（多并行度时Watermark取最小值）

### 课后作业详细要求

**作业1：实现Session Window用户行为分析**

```java
import org.apache.flink.api.common.eventtime.*;
import org.apache.flink.api.common.functions.MapFunction;
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.datastream.SingleOutputStreamOperator;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.streaming.api.functions.source.SourceFunction;
import org.apache.flink.streaming.api.windowing.assigners.EventTimeSessionWindows;
import org.apache.flink.streaming.api.windowing.time.Time;
import org.apache.flink.streaming.api.functions.ProcessFunction;
import org.apache.flink.util.Collector;
import org.apache.flink.util.OutputTag;
import java.util.*;

public class SessionWindowUserAnalysis {

    public static void main(String[] args) throws Exception {
        StreamExecutionEnvironment env =
            StreamExecutionEnvironment.getExecutionEnvironment();
        env.setParallelism(2);
        env.enableCheckpointing(5000);

        final OutputTag<UserEvent> lateOutputTag =
            new OutputTag<UserEvent>("late-events") {};

        DataStream<UserEvent> events = env
            .addSource(new UserEventSource())
            .assignTimestampsAndWatermarks(
                WatermarkStrategy
                    .<UserEvent>forBoundedOutOfOrderness(
                        java.time.Duration.ofSeconds(10))
                    .withTimestampAssigner(
                        (event, ts) -> event.getTimestamp())
            );

        SingleOutputStreamOperator<SessionStats> sessionStats = events
            .keyBy(UserEvent::getUserId)
            .window(EventTimeSessionWindows.withGap(Time.minutes(5)))
            .allowedLateness(Time.minutes(1))
            .sideOutputLateData(lateOutputTag)
            .process(new SessionProcessFunction());

        sessionStats.print();

        DataStream<UserEvent> lateEvents =
            sessionStats.getSideOutput(lateOutputTag);
        lateEvents.map(e -> "[LATE] " + e.toString()).print();

        env.execute("Session Window User Behavior Analysis");
    }

    public static class UserEvent {
        public String userId;
        public String action;
        public String page;
        public long timestamp;

        public UserEvent() {}

        public UserEvent(String userId, String action,
                        String page, long timestamp) {
            this.userId = userId;
            this.action = action;
            this.page = page;
            this.timestamp = timestamp;
        }

        public String getUserId() { return userId; }
        public String getAction() { return action; }
        public String getPage() { return page; }
        public long getTimestamp() { return timestamp; }

        @Override
        public String toString() {
            return String.format(
                "UserEvent{user=%s, action=%s, page=%s, ts=%d}",
                userId, action, page, timestamp);
        }
    }

    public static class SessionStats {
        public String userId;
        public long sessionStart;
        public long sessionEnd;
        public long eventCount;
        public Set<String> pages;
        public Set<String> actions;
        public long sessionDurationMs;

        public SessionStats() {}

        @Override
        public String toString() {
            return String.format(
                "SessionStats{user=%s, duration=%dms, events=%d, "
                + "pages=%s, actions=%s}",
                userId, sessionDurationMs, eventCount,
                pages, actions);
        }
    }

    public static class SessionProcessFunction extends
        org.apache.flink.streaming.api.functions.windowing
            .ProcessWindowFunction<UserEvent, SessionStats, String,
                org.apache.flink.streaming.api.windowing.windows.TimeWindow> {

        @Override
        public void process(String userId,
                           Context context,
                           Iterable<UserEvent> events,
                           Collector<SessionStats> out) {
            SessionStats stats = new SessionStats();
            stats.userId = userId;
            stats.sessionStart = context.window().getStart();
            stats.sessionEnd = context.window().getEnd();
            stats.sessionDurationMs =
                stats.sessionEnd - stats.sessionStart;
            stats.pages = new HashSet<>();
            stats.actions = new HashSet<>();
            stats.eventCount = 0;

            for (UserEvent e : events) {
                stats.eventCount++;
                stats.pages.add(e.getPage());
                stats.actions.add(e.getAction());
            }

            out.collect(stats);
        }
    }

    public static class UserEventSource
        implements SourceFunction<UserEvent> {
        private volatile boolean running = true;
        private final Random random = new Random();
        private final String[] pages =
            {"home", "product", "cart", "checkout", "profile"};
        private final String[] actions =
            {"click", "scroll", "purchase", "add_to_cart", "logout"};
        private final String[] users =
            {"user_1", "user_2", "user_3", "user_4", "user_5"};

        @Override
        public void run(SourceContext<UserEvent> ctx) throws Exception {
            long baseTime = System.currentTimeMillis();
            while (running) {
                String userId = users[random.nextInt(users.length)];
                String action = actions[random.nextInt(actions.length)];
                String page = pages[random.nextInt(pages.length)];
                long eventTime = baseTime + random.nextInt(600000);
                ctx.collect(new UserEvent(userId, action, page, eventTime));
                Thread.sleep(50);
            }
        }

        @Override
        public void cancel() {
            running = false;
        }
    }
}
```

输出要求：提交代码和运行截图，展示Session Window的触发行为，包括会话时长、事件数、访问页面数等统计信息，以及迟到数据的处理结果。

---

## 十、参考资料

- [Apache Flink Documentation - Time and Watermarks](https://nightlies.apache.org/flink/flink-docs-stable/docs/concepts/time/)
- [Apache Flink Documentation - Windowing](https://nightlies.apache.org/flink/flink-docs-stable/docs/dev/datastream/operators/windows/)
- 《基于Apache Flink的流处理》第3-5章, Fabian Hueske 等
- [Stream Processing with Apache Flink (O'Reilly 书籍)](https://www.oreilly.com/library/view/stream-processing-with/9781491974285/)