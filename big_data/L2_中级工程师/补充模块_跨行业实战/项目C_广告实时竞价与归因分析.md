# 项目C：广告实时竞价与归因分析

> **所属阶段**：L2 中级工程师 | **模块**：补充模块_跨行业实战 | **预计时长**：25h | **难度**：★★★★☆
>
> **技术栈**：Kafka → Flink → ClickHouse + Redis → Spark → Grafana
>
> **前置要求**：完成L2课时17-18（Kafka深入）+ 课时19-21（Flink流处理）+ 项目7（实时交易监控大屏）

---

## 一、项目描述

构建广告场景的实时竞价数据处理和归因分析系统。项目覆盖广告数据模拟、实时竞价处理、多模型归因分析、报表优化全流程，让学员掌握数字营销大数据的核心应用模式。

### 业务价值

```
广告实时竞价与归因分析系统解决的问题：

  问题1: "广告实时效果如何监控？"
    → 以前: T+1报表，无法实时调整出价
    → 现在: 实时CTR/CPC/CPM，秒级决策

  问题2: "广告预算花在哪里了？"
    → 以前: 只看末次点击，高估部分渠道
    → 现在: 4种归因模型对比，真实贡献度

  问题3: "如何识别作弊流量？"
    → 以前: 事后分析，预算已浪费
    → 现在: 实时反作弊，自动过滤

  问题4: "如何自动优化广告投放？"
    → 以前: 人工调价，反应慢效率低
    → 现在: 基于ROI的自动调价策略
```

---

## 二、整体架构

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                     广告实时竞价与归因分析系统                                  │
│                                                                              │
│  ┌──────────┐   ┌───────────┐   ┌───────────────────────────────────────┐  │
│  │ 广告SDK  │──→│   Kafka   │──→│              Flink                    │  │
│  │(竞价/曝光│   │ (消息队列) │   │  ┌──────────┐  ┌────────────────┐   │  │
│  │ /点击/   │   │           │   │  │实时竞价   │  │  实时归因      │   │  │
│  │  转化)   │   │           │   │  │处理引擎   │  │  (触点窗口)    │   │  │
│  └──────────┘   └───────────┘   │  └─────┬────┘  └───────┬────────┘   │  │
│                                  └────────┼───────────────┼────────────┘  │
│                                           │               │                │
│                    ┌──────────────────────┼───────────────┘                │
│                    │                      │                                 │
│             ┌──────▼──────┐       ┌───────▼────────┐    ┌──────────────┐ │
│             │ ClickHouse  │       │     Redis      │    │    Spark     │ │
│             │(OLAP存储)   │       │ (实时画像+指标) │    │ (批量归因)   │ │
│             └──────┬──────┘       └───────┬────────┘    └──────┬───────┘ │
│                    │                      │                     │         │
│             ┌──────▼──────────────────────▼─────────────────────▼──────┐ │
│             │                      Grafana                            │ │
│             │              (广告大屏+报表+优化)                       │ │
│             └────────────────────────────────────────────────────────┘ │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 三、阶段1 - 广告数据模拟（4h）

### 3.1 广告数据模型

```sql
-- ============================================
-- 广告实时竞价数据模型 DDL
-- ============================================

CREATE DATABASE IF NOT EXISTS ad_bidding;

CREATE TABLE ad_bidding.ads (
    ad_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    ad_name VARCHAR(100) NOT NULL,
    advertiser_id BIGINT NOT NULL,
    campaign_id BIGINT NOT NULL,
    ad_type TINYINT COMMENT '1-横幅 2-信息流 3-视频 4-开屏',
    bid_price DECIMAL(10, 4) NOT NULL COMMENT '出价(CPM)',
    daily_budget DECIMAL(12, 2) NOT NULL,
    total_budget DECIMAL(12, 2) NOT NULL,
    status TINYINT DEFAULT 1 COMMENT '0-暂停 1-投放中 2-已结束',
    target_audience JSON COMMENT '定向条件',
    create_time DATETIME NOT NULL,
    update_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_advertiser (advertiser_id),
    INDEX idx_campaign (campaign_id),
    INDEX idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE ad_bidding.advertisers (
    advertiser_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    company_name VARCHAR(100) NOT NULL,
    industry VARCHAR(50),
    balance DECIMAL(14, 2) DEFAULT 0,
    create_time DATETIME NOT NULL,
    INDEX idx_industry (industry)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE ad_bidding.impressions (
    impression_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    ad_id BIGINT NOT NULL,
    user_id BIGINT NOT NULL,
    media VARCHAR(50) NOT NULL COMMENT '媒体名称',
    position VARCHAR(30) NOT NULL COMMENT '广告位',
    device VARCHAR(20) NOT NULL COMMENT 'iOS/Android/PC',
    impression_time DATETIME(3) NOT NULL,
    cost DECIMAL(10, 4) COMMENT '实际花费',
    is_fraud TINYINT DEFAULT 0 COMMENT '0-正常 1-作弊',
    INDEX idx_ad_id (ad_id),
    INDEX idx_user_id (user_id),
    INDEX idx_impression_time (impression_time),
    INDEX idx_media (media)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE ad_bidding.clicks (
    click_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    impression_id BIGINT NOT NULL,
    click_time DATETIME(3) NOT NULL,
    INDEX idx_impression_id (impression_id),
    INDEX idx_click_time (click_time)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE ad_bidding.conversions (
    conversion_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    click_id BIGINT NOT NULL,
    conversion_type TINYINT NOT NULL COMMENT '1-注册 2-下单 3-付费',
    amount DECIMAL(12, 2) COMMENT '转化金额',
    conversion_time DATETIME(3) NOT NULL,
    INDEX idx_click_id (click_id),
    INDEX idx_conversion_time (conversion_time),
    INDEX idx_conversion_type (conversion_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE ad_bidding.bid_requests (
    request_id VARCHAR(64) PRIMARY KEY,
    ad_id BIGINT NOT NULL,
    bid_amount DECIMAL(10, 4) NOT NULL,
    is_won TINYINT NOT NULL COMMENT '0-未中标 1-中标',
    request_time DATETIME(3) NOT NULL,
    INDEX idx_ad_id (ad_id),
    INDEX idx_request_time (request_time),
    INDEX idx_is_won (is_won)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

### 3.2 广告数据模拟器

```python
"""
ad_data_simulator.py

广告数据模拟生成器
1000个广告、100万用户、1亿曝光、1000万点击、100万转化（30天）
竞价日志: 每秒1000条竞价请求
"""
import pymysql
import random
import time
import json
import hashlib
from datetime import datetime, timedelta
from kafka import KafkaProducer
import threading

DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'root123',
    'database': 'ad_bidding',
    'charset': 'utf8mb4'
}

KAFKA_BROKER = 'localhost:9092'

MEDIAS = ['今日头条', '抖音', '微信朋友圈', '微博', '百度', '快手',
          'B站', '小红书', '知乎', 'QQ空间']
POSITIONS = ['信息流', '开屏', '详情页底部', '搜索结果', '视频前贴', '横幅']
DEVICES = ['iOS', 'Android', 'PC']
CATEGORIES = ['电商', '游戏', '金融', '教育', '旅游', '餐饮', '汽车', '房产']
AD_TYPES = [1, 2, 3, 4]


class AdDataSimulator:

    def __init__(self):
        self.conn = pymysql.connect(**DB_CONFIG)
        self.cursor = self.conn.cursor()
        self.producer = KafkaProducer(
            bootstrap_servers=KAFKA_BROKER,
            value_serializer=lambda v: json.dumps(v, ensure_ascii=False).encode('utf-8')
        )
        self.advertiser_ids = []
        self.ad_ids = []
        self.user_ids = list(range(1, 1000001))
        self.impression_count = 0
        self.click_count = 0
        self.conversion_count = 0
        self.bid_count = 0

    def generate_advertisers(self, count=100):
        print(f"生成 {count} 个广告主...")
        batch = []
        for i in range(count):
            company = f"广告主_{i+1:04d}"
            industry = random.choice(CATEGORIES)
            balance = round(random.uniform(100000, 10000000), 2)
            create_time = datetime(2024, 1, 1) + timedelta(days=random.randint(0, 180))
            batch.append((company, industry, balance, create_time))

            if len(batch) >= 1000:
                self.cursor.executemany(
                    "INSERT INTO advertisers (company_name, industry, balance, create_time) VALUES (%s,%s,%s,%s)",
                    batch
                )
                self.conn.commit()
                self.advertiser_ids.extend(
                    range(self.cursor.lastrowid - len(batch) + 1, self.cursor.lastrowid + 1)
                )
                batch = []

        if batch:
            self.cursor.executemany(
                "INSERT INTO advertisers (company_name, industry, balance, create_time) VALUES (%s,%s,%s,%s)",
                batch
            )
            self.conn.commit()
            self.advertiser_ids.extend(
                range(self.cursor.lastrowid - len(batch) + 1, self.cursor.lastrowid + 1)
            )

        print(f"广告主生成完成: {len(self.advertiser_ids)}")

    def generate_ads(self, count=1000):
        print(f"生成 {count} 个广告...")
        batch = []
        for i in range(count):
            advertiser_id = random.choice(self.advertiser_ids)
            campaign_id = random.randint(1, 500)
            ad_type = random.choice(AD_TYPES)
            bid_price = round(random.uniform(5, 200), 4)
            daily_budget = round(random.uniform(5000, 500000), 2)
            total_budget = daily_budget * random.randint(7, 90)
            ad_name = f"广告_{i+1:06d}"
            target_audience = json.dumps({
                'age_min': random.choice([18, 20, 25, 30]),
                'age_max': random.choice([35, 40, 45, 55, 65]),
                'gender': random.choice(['all', 'male', 'female']),
                'cities': random.sample(['北京', '上海', '广州', '深圳', '杭州', '成都'], k=random.randint(1, 4)),
                'interests': random.sample(CATEGORIES, k=random.randint(1, 3))
            }, ensure_ascii=False)
            create_time = datetime(2024, 1, 1) + timedelta(days=random.randint(0, 60))
            batch.append((ad_name, advertiser_id, campaign_id, ad_type, bid_price,
                          daily_budget, total_budget, target_audience, create_time))

            if len(batch) >= 1000:
                self.cursor.executemany(
                    """INSERT INTO ads (ad_name, advertiser_id, campaign_id, ad_type,
                       bid_price, daily_budget, total_budget, target_audience, create_time)
                       VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                    batch
                )
                self.conn.commit()
                self.ad_ids.extend(
                    range(self.cursor.lastrowid - len(batch) + 1, self.cursor.lastrowid + 1)
                )
                batch = []

        if batch:
            self.cursor.executemany(
                """INSERT INTO ads (ad_name, advertiser_id, campaign_id, ad_type,
                   bid_price, daily_budget, total_budget, target_audience, create_time)
                   VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                batch
            )
            self.conn.commit()
            self.ad_ids.extend(
                range(self.cursor.lastrowid - len(batch) + 1, self.cursor.lastrowid + 1)
            )

        print(f"广告生成完成: {len(self.ad_ids)}")

    def generate_impression_stream(self, duration_seconds=3600, rate_per_second=3000):
        print(f"开始生成曝光流: {rate_per_second}/s, 持续{duration_seconds}s")
        start_time = time.time()

        while time.time() - start_time < duration_seconds:
            batch_start = time.time()
            for _ in range(rate_per_second):
                ad_id = random.choice(self.ad_ids)
                user_id = random.choice(self.user_ids)
                media = random.choice(MEDIAS)
                position = random.choice(POSITIONS)
                device = random.choice(DEVICES)
                impression_time = datetime.now()

                is_fraud = 1 if random.random() < 0.02 else 0

                impression = {
                    'event_type': 'impression',
                    'ad_id': ad_id,
                    'user_id': user_id,
                    'media': media,
                    'position': position,
                    'device': device,
                    'impression_time': impression_time.isoformat(timespec='milliseconds'),
                    'is_fraud': is_fraud
                }

                self.producer.send('ad.events.impression', impression)
                self.impression_count += 1

                click_prob = 0.08 if not is_fraud else 0.3
                if random.random() < click_prob:
                    click_delay = random.uniform(0.5, 30)
                    click_time = impression_time + timedelta(seconds=click_delay)
                    click = {
                        'event_type': 'click',
                        'ad_id': ad_id,
                        'user_id': user_id,
                        'impression_time': impression_time.isoformat(timespec='milliseconds'),
                        'click_time': click_time.isoformat(timespec='milliseconds'),
                        'is_fraud': is_fraud
                    }
                    self.producer.send('ad.events.click', click)
                    self.click_count += 1

                    conversion_prob = 0.1 if not is_fraud else 0.01
                    if random.random() < conversion_prob:
                        conv_delay = random.uniform(60, 86400)
                        conv_time = click_time + timedelta(seconds=conv_delay)
                        conv_type = random.choices([1, 2, 3], weights=[40, 45, 15])[0]
                        amount = round(random.uniform(10, 5000), 2) if conv_type in [2, 3] else 0
                        conversion = {
                            'event_type': 'conversion',
                            'ad_id': ad_id,
                            'user_id': user_id,
                            'click_time': click_time.isoformat(timespec='milliseconds'),
                            'conversion_type': conv_type,
                            'amount': amount,
                            'conversion_time': conv_time.isoformat(timespec='milliseconds')
                        }
                        self.producer.send('ad.events.conversion', conversion)
                        self.conversion_count += 1

            elapsed = time.time() - batch_start
            if elapsed < 1.0:
                time.sleep(1.0 - elapsed)

            if self.impression_count % 100000 < rate_per_second:
                print(f"  曝光: {self.impression_count}, 点击: {self.click_count}, "
                      f"转化: {self.conversion_count}")

    def generate_bid_stream(self, duration_seconds=3600, rate_per_second=1000):
        print(f"开始生成竞价流: {rate_per_second}/s, 持续{duration_seconds}s")
        start_time = time.time()

        while time.time() - start_time < duration_seconds:
            batch_start = time.time()
            for _ in range(rate_per_second):
                ad_id = random.choice(self.ad_ids)
                bid_amount = round(random.uniform(5, 200), 4)
                is_won = 1 if random.random() < 0.3 else 0
                request_time = datetime.now()

                request_id = hashlib.md5(
                    f"{ad_id}_{request_time.timestamp()}_{random.random()}".encode()
                ).hexdigest()

                bid = {
                    'request_id': request_id,
                    'ad_id': ad_id,
                    'bid_amount': bid_amount,
                    'is_won': is_won,
                    'request_time': request_time.isoformat(timespec='milliseconds')
                }

                self.producer.send('ad.events.bid', bid)
                self.bid_count += 1

            elapsed = time.time() - batch_start
            if elapsed < 1.0:
                time.sleep(1.0 - elapsed)

            if self.bid_count % 50000 < rate_per_second:
                print(f"  竞价请求: {self.bid_count}")

    def run(self, duration_seconds=3600):
        self.generate_advertisers(count=100)
        self.generate_ads(count=1000)

        impression_thread = threading.Thread(
            target=self.generate_impression_stream,
            args=(duration_seconds, 3000)
        )
        bid_thread = threading.Thread(
            target=self.generate_bid_stream,
            args=(duration_seconds, 1000)
        )

        impression_thread.start()
        bid_thread.start()

        impression_thread.join()
        bid_thread.join()

        self.producer.flush()
        self.cursor.close()
        self.conn.close()

        print(f"\n数据生成完成:")
        print(f"  曝光: {self.impression_count}")
        print(f"  点击: {self.click_count}")
        print(f"  转化: {self.conversion_count}")
        print(f"  竞价: {self.bid_count}")


if __name__ == '__main__':
    sim = AdDataSimulator()
    sim.run(duration_seconds=3600)
```

---

## 四、阶段2 - 实时竞价数据处理（8h）

### 4.1 Kafka Topic设计

| Topic名称 | 数据内容 | 分区数 | 副本数 | Retention |
|-----------|----------|--------|--------|-----------|
| ad.events.impression | 曝光事件 | 12 | 3 | 168h |
| ad.events.click | 点击事件 | 12 | 3 | 168h |
| ad.events.conversion | 转化事件 | 6 | 3 | 720h |
| ad.events.bid | 竞价请求 | 12 | 3 | 72h |
| ad.metrics.realtime | 实时指标 | 6 | 3 | 24h |
| ad.fraud.alerts | 作弊告警 | 6 | 3 | 720h |

### 4.2 Flink实时竞价处理

```java
package com.example.ad.bidding;

import org.apache.flink.api.common.eventtime.WatermarkStrategy;
import org.apache.flink.api.common.state.ValueState;
import org.apache.flink.api.common.state.ValueStateDescriptor;
import org.apache.flink.api.common.state.ListState;
import org.apache.flink.api.common.state.ListStateDescriptor;
import org.apache.flink.configuration.Configuration;
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.datastream.SingleOutputStreamOperator;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.streaming.api.functions.KeyedProcessFunction;
import org.apache.flink.streaming.api.windowing.assigners.TumblingEventTimeWindows;
import org.apache.flink.streaming.api.windowing.time.Time;
import org.apache.flink.streaming.connectors.kafka.FlinkKafkaConsumer;
import org.apache.flink.streaming.connectors.kafka.FlinkKafkaProducer;
import org.apache.flink.api.common.serialization.SimpleStringSchema;
import org.apache.flink.util.Collector;
import com.alibaba.fastjson.JSON;
import com.alibaba.fastjson.JSONObject;

import java.time.Duration;
import java.util.ArrayList;
import java.util.List;
import java.util.Properties;

public class AdRealTimeProcessor {

    public static void main(String[] args) throws Exception {
        StreamExecutionEnvironment env =
            StreamExecutionEnvironment.getExecutionEnvironment();

        env.enableCheckpointing(60000);

        Properties kafkaProps = new Properties();
        kafkaProps.setProperty("bootstrap.servers", "localhost:9092");
        kafkaProps.setProperty("group.id", "ad-processor-group");
        kafkaProps.setProperty("auto.offset.reset", "latest");

        DataStream<ImpressionEvent> impressionStream = env
            .addSource(new FlinkKafkaConsumer<>(
                "ad.events.impression",
                new SimpleStringSchema(),
                kafkaProps
            ))
            .map(line -> JSON.parseObject(line, ImpressionEvent.class))
            .assignTimestampsAndWatermarks(
                WatermarkStrategy.<ImpressionEvent>forBoundedOutOfOrderness(Duration.ofSeconds(5))
                    .withTimestampAssigner((e, ts) -> e.impressionTime)
            );

        DataStream<ClickEvent> clickStream = env
            .addSource(new FlinkKafkaConsumer<>(
                "ad.events.click",
                new SimpleStringSchema(),
                kafkaProps
            ))
            .map(line -> JSON.parseObject(line, ClickEvent.class))
            .assignTimestampsAndWatermarks(
                WatermarkStrategy.<ClickEvent>forBoundedOutOfOrderness(Duration.ofSeconds(5))
                    .withTimestampAssigner((e, ts) -> e.clickTime)
            );

        DataStream<ConversionEvent> conversionStream = env
            .addSource(new FlinkKafkaConsumer<>(
                "ad.events.conversion",
                new SimpleStringSchema(),
                kafkaProps
            ))
            .map(line -> JSON.parseObject(line, ConversionEvent.class))
            .assignTimestampsAndWatermarks(
                WatermarkStrategy.<ConversionEvent>forBoundedOutOfOrderness(Duration.ofSeconds(5))
                    .withTimestampAssigner((e, ts) -> e.conversionTime)
            );

        DataStream<BidEvent> bidStream = env
            .addSource(new FlinkKafkaConsumer<>(
                "ad.events.bid",
                new SimpleStringSchema(),
                kafkaProps
            ))
            .map(line -> JSON.parseObject(line, BidEvent.class))
            .assignTimestampsAndWatermarks(
                WatermarkStrategy.<BidEvent>forBoundedOutOfOrderness(Duration.ofSeconds(5))
                    .withTimestampAssigner((e, ts) -> e.requestTime)
            );

        DataStream<AdMetrics> ctrMetrics = clickStream
            .keyBy(ClickEvent::getAdId)
            .window(TumblingEventTimeWindows.of(Time.minutes(1)))
            .aggregate(new CTRAggregator());

        DataStream<FraudAlert> fraudAlerts = clickStream
            .keyBy(e -> e.userId + "_" + e.adId)
            .process(new FraudDetectorFunction());

        DataStream<BidStats> bidStats = bidStream
            .keyBy(BidEvent::getAdId)
            .window(TumblingEventTimeWindows.of(Time.minutes(1)))
            .aggregate(new BidStatsAggregator());

        FlinkKafkaProducer<String> metricsSink = new FlinkKafkaProducer<>(
            "ad.metrics.realtime",
            new SimpleStringSchema(),
            kafkaProps
        );

        FlinkKafkaProducer<String> fraudSink = new FlinkKafkaProducer<>(
            "ad.fraud.alerts",
            new SimpleStringSchema(),
            kafkaProps
        );

        ctrMetrics.map(m -> JSON.toJSONString(m)).addSink(metricsSink);
        bidStats.map(s -> JSON.toJSONString(s)).addSink(metricsSink);
        fraudAlerts.map(a -> JSON.toJSONString(a)).addSink(fraudSink);

        env.execute("Ad Real-Time Processor");
    }

    static class CTRAggregator implements org.apache.flink.api.common.functions.AggregateFunction<
            ClickEvent, CTRAccumulator, AdMetrics> {

        @Override
        public CTRAccumulator createAccumulator() {
            return new CTRAccumulator();
        }

        @Override
        public CTRAccumulator add(ClickEvent click, CTRAccumulator acc) {
            acc.adId = click.adId;
            acc.clickCount++;
            return acc;
        }

        @Override
        public AdMetrics getResult(CTRAccumulator acc) {
            AdMetrics metrics = new AdMetrics();
            metrics.adId = acc.adId;
            metrics.metricType = "CTR";
            metrics.clickCount = acc.clickCount;
            return metrics;
        }

        @Override
        public CTRAccumulator merge(CTRAccumulator a, CTRAccumulator b) {
            a.clickCount += b.clickCount;
            return a;
        }
    }

    static class FraudDetectorFunction extends KeyedProcessFunction<
            String, ClickEvent, FraudAlert> {

        private ListState<Long> clickTimes;

        @Override
        public void open(Configuration parameters) {
            clickTimes = getRuntimeContext().getListState(
                new ListStateDescriptor<>("clickTimes", Long.class));
        }

        @Override
        public void processElement(ClickEvent event, Context ctx, Collector<FraudAlert> out)
                throws Exception {
            List<Long> times = new ArrayList<>();
            for (Long t : clickTimes.get()) {
                if (event.clickTime - t < 60000) {
                    times.add(t);
                }
            }
            times.add(event.clickTime);
            clickTimes.update(times);

            if (times.size() > 3) {
                FraudAlert alert = new FraudAlert();
                alert.userId = event.userId;
                alert.adId = event.adId;
                alert.fraudType = "CLICK_SPAM";
                alert.clickCount = times.size();
                alert.windowSeconds = 60;
                alert.alertTime = System.currentTimeMillis();
                out.collect(alert);
            }
        }
    }

    static class BidStatsAggregator implements org.apache.flink.api.common.functions.AggregateFunction<
            BidEvent, BidAccumulator, BidStats> {

        @Override
        public BidAccumulator createAccumulator() {
            return new BidAccumulator();
        }

        @Override
        public BidAccumulator add(BidEvent bid, BidAccumulator acc) {
            acc.adId = bid.adId;
            acc.totalBids++;
            if (bid.isWon == 1) {
                acc.wonBids++;
                acc.totalCost += bid.bidAmount;
            }
            return acc;
        }

        @Override
        public BidStats getResult(BidAccumulator acc) {
            BidStats stats = new BidStats();
            stats.adId = acc.adId;
            stats.totalBids = acc.totalBids;
            stats.wonBids = acc.wonBids;
            stats.winRate = acc.totalBids > 0 ? (double) acc.wonBids / acc.totalBids : 0;
            stats.totalCost = acc.totalCost;
            return stats;
        }

        @Override
        public BidAccumulator merge(BidAccumulator a, BidAccumulator b) {
            a.totalBids += b.totalBids;
            a.wonBids += b.wonBids;
            a.totalCost += b.totalCost;
            return a;
        }
    }

    static class ImpressionEvent {
        public Long adId;
        public Long userId;
        public String media;
        public String position;
        public String device;
        public Long impressionTime;
        public Integer isFraud;
    }

    static class ClickEvent {
        public Long adId;
        public Long userId;
        public Long impressionTime;
        public Long clickTime;
        public Integer isFraud;
        public Long getAdId() { return adId; }
    }

    static class ConversionEvent {
        public Long adId;
        public Long userId;
        public Long clickTime;
        public Integer conversionType;
        public Double amount;
        public Long conversionTime;
    }

    static class BidEvent {
        public String requestId;
        public Long adId;
        public Double bidAmount;
        public Integer isWon;
        public Long requestTime;
        public Long getAdId() { return adId; }
    }

    static class CTRAccumulator {
        public Long adId;
        public long clickCount = 0;
    }

    static class BidAccumulator {
        public Long adId;
        public long totalBids = 0;
        public long wonBids = 0;
        public double totalCost = 0;
    }

    static class AdMetrics {
        public Long adId;
        public String metricType;
        public long clickCount;
    }

    static class FraudAlert {
        public Long userId;
        public Long adId;
        public String fraudType;
        public int clickCount;
        public int windowSeconds;
        public Long alertTime;
    }

    static class BidStats {
        public Long adId;
        public long totalBids;
        public long wonBids;
        public double winRate;
        public double totalCost;
    }
}
```

### 4.3 Flink SQL实时指标计算

```sql
-- Flink SQL: 广告实时指标计算

CREATE TABLE ad_impressions (
    ad_id BIGINT,
    user_id BIGINT,
    media STRING,
    position STRING,
    device STRING,
    impression_time TIMESTAMP(3),
    is_fraud INT,
    WATERMARK FOR impression_time AS impression_time - INTERVAL '5' SECOND
) WITH (
    'connector' = 'kafka',
    'topic' = 'ad.events.impression',
    'properties.bootstrap.servers' = 'localhost:9092',
    'properties.group.id' = 'ad-metrics-group',
    'format' = 'json',
    'scan.startup.mode' = 'latest-offset'
);

CREATE TABLE ad_clicks (
    ad_id BIGINT,
    user_id BIGINT,
    impression_time TIMESTAMP(3),
    click_time TIMESTAMP(3),
    is_fraud INT,
    WATERMARK FOR click_time AS click_time - INTERVAL '5' SECOND
) WITH (
    'connector' = 'kafka',
    'topic' = 'ad.events.click',
    'properties.bootstrap.servers' = 'localhost:9092',
    'properties.group.id' = 'ad-metrics-group',
    'format' = 'json',
    'scan.startup.mode' = 'latest-offset'
);

CREATE TABLE ad_conversions (
    ad_id BIGINT,
    user_id BIGINT,
    click_time TIMESTAMP(3),
    conversion_type INT,
    amount DECIMAL(12, 2),
    conversion_time TIMESTAMP(3),
    WATERMARK FOR conversion_time AS conversion_time - INTERVAL '5' SECOND
) WITH (
    'connector' = 'kafka',
    'topic' = 'ad.events.conversion',
    'properties.bootstrap.servers' = 'localhost:9092',
    'properties.group.id' = 'ad-metrics-group',
    'format' = 'json',
    'scan.startup.mode' = 'latest-offset'
);

CREATE TABLE ad_bids (
    request_id STRING,
    ad_id BIGINT,
    bid_amount DECIMAL(10, 4),
    is_won INT,
    request_time TIMESTAMP(3),
    WATERMARK FOR request_time AS request_time - INTERVAL '5' SECOND
) WITH (
    'connector' = 'kafka',
    'topic' = 'ad.events.bid',
    'properties.bootstrap.servers' = 'localhost:9092',
    'properties.group.id' = 'ad-metrics-group',
    'format' = 'json',
    'scan.startup.mode' = 'latest-offset'
);

-- CTR实时计算: 最近1小时各广告的点击率
CREATE VIEW ad_ctr_1h AS
SELECT
    i.ad_id,
    COUNT(DISTINCT c.click_time) AS click_count,
    COUNT(DISTINCT i.impression_time) AS impression_count,
    CAST(COUNT(DISTINCT c.click_time) AS DOUBLE) /
        NULLIF(CAST(COUNT(DISTINCT i.impression_time) AS DOUBLE), 0) AS ctr
FROM ad_impressions i
LEFT JOIN ad_clicks c
    ON i.ad_id = c.ad_id AND i.user_id = c.user_id
    AND c.click_time BETWEEN i.impression_time AND i.impression_time + INTERVAL '1' HOUR
WHERE i.impression_time >= NOW - INTERVAL '1' HOUR
GROUP BY i.ad_id;

-- CPC/CPM实时统计: 每分钟各广告的花费
CREATE TABLE ad_cost_minute (
    ad_id BIGINT,
    window_start TIMESTAMP(3),
    window_end TIMESTAMP(3),
    impression_count BIGINT,
    click_count BIGINT,
    total_cost DECIMAL(12, 4),
    cpm DECIMAL(10, 4),
    cpc DECIMAL(10, 4),
    PRIMARY KEY (ad_id, window_start) NOT ENFORCED
) WITH (
    'connector' = 'upsert-kafka',
    'topic' = 'ad.metrics.realtime',
    'properties.bootstrap.servers' = 'localhost:9092',
    'key.format' = 'json',
    'value.format' = 'json'
);

INSERT INTO ad_cost_minute
SELECT
    b.ad_id,
    TUMBLE_START(b.request_time, INTERVAL '1' MINUTE) AS window_start,
    TUMBLE_END(b.request_time, INTERVAL '1' MINUTE) AS window_end,
    0L AS impression_count,
    0L AS click_count,
    SUM(CASE WHEN b.is_won = 1 THEN b.bid_amount ELSE 0 END) AS total_cost,
    SUM(CASE WHEN b.is_won = 1 THEN b.bid_amount ELSE 0 END) * 1000 AS cpm,
    CASE WHEN SUM(CASE WHEN b.is_won = 1 THEN 1 ELSE 0 END) > 0
         THEN SUM(CASE WHEN b.is_won = 1 THEN b.bid_amount ELSE 0 END) /
              SUM(CASE WHEN b.is_won = 1 THEN 1 ELSE 0 END)
         ELSE 0 END AS cpc
FROM ad_bids b
GROUP BY
    b.ad_id,
    TUMBLE(b.request_time, INTERVAL '1' MINUTE);

-- 竞价成功率
CREATE VIEW ad_bid_win_rate AS
SELECT
    ad_id,
    COUNT(*) AS total_bids,
    SUM(CASE WHEN is_won = 1 THEN 1 ELSE 0 END) AS won_bids,
    CAST(SUM(CASE WHEN is_won = 1 THEN 1 ELSE 0 END) AS DOUBLE) / COUNT(*) AS win_rate
FROM ad_bids
WHERE request_time >= NOW - INTERVAL '1' HOUR
GROUP BY ad_id;

-- 反作弊: 同一用户1分钟内点击同一广告>3次
CREATE TABLE ad_fraud_alerts (
    user_id BIGINT,
    ad_id BIGINT,
    fraud_type STRING,
    click_count BIGINT,
    window_start TIMESTAMP(3),
    window_end TIMESTAMP(3),
    alert_time TIMESTAMP(3),
    PRIMARY KEY (user_id, ad_id, window_start) NOT ENFORCED
) WITH (
    'connector' = 'upsert-kafka',
    'topic' = 'ad.fraud.alerts',
    'properties.bootstrap.servers' = 'localhost:9092',
    'key.format' = 'json',
    'value.format' = 'json'
);

INSERT INTO ad_fraud_alerts
SELECT
    user_id,
    ad_id,
    'CLICK_SPAM' AS fraud_type,
    COUNT(*) AS click_count,
    TUMBLE_START(click_time, INTERVAL '1' MINUTE) AS window_start,
    TUMBLE_END(click_time, INTERVAL '1' MINUTE) AS window_end,
    CURRENT_TIMESTAMP AS alert_time
FROM ad_clicks
WHERE is_fraud = 0
GROUP BY
    user_id, ad_id,
    TUMBLE(click_time, INTERVAL '1' MINUTE)
HAVING COUNT(*) > 3;
```

### 4.4 Redis实时服务

```python
"""
ad_redis_service.py

Redis实时广告服务
用户实时画像 / 广告实时指标 / 竞价辅助
"""
import redis
import json
from datetime import datetime

r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

USER_PROFILE_PREFIX = "ad:user:"
AD_METRICS_PREFIX = "ad:metrics:"
BID_ASSIST_PREFIX = "ad:bid:assist:"


def update_user_profile(user_id, event_data):
    key = f"{USER_PROFILE_PREFIX}{user_id}"
    pipe = r.pipeline()

    if event_data.get('event_type') == 'impression':
        category = event_data.get('media', '')
        pipe.lpush(f"{key}:recent_views", category)
        pipe.ltrim(f"{key}:recent_views", 0, 49)
        pipe.expire(f"{key}:recent_views", 86400 * 7)

    elif event_data.get('event_type') == 'click':
        category = event_data.get('media', '')
        pipe.lpush(f"{key}:recent_clicks", category)
        pipe.ltrim(f"{key}:recent_clicks", 0, 49)
        pipe.expire(f"{key}:recent_clicks", 86400 * 7)

    pipe.hset(key, mapping={
        'last_active': datetime.now().isoformat(),
        'device': event_data.get('device', ''),
    })
    pipe.expire(key, 86400 * 7)
    pipe.execute()


def update_ad_metrics(ad_id, metrics):
    key = f"{AD_METRICS_PREFIX}{ad_id}"
    pipe = r.pipeline()
    pipe.hset(key, mapping={
        'ctr': str(metrics.get('ctr', 0)),
        'cpc': str(metrics.get('cpc', 0)),
        'cpm': str(metrics.get('cpm', 0)),
        'impression_count': str(metrics.get('impression_count', 0)),
        'click_count': str(metrics.get('click_count', 0)),
        'total_cost': str(metrics.get('total_cost', 0)),
        'win_rate': str(metrics.get('win_rate', 0)),
        'budget_consumed': str(metrics.get('budget_consumed', 0)),
        'update_time': datetime.now().isoformat(),
    })
    pipe.expire(key, 3600)
    pipe.execute()


def get_bid_suggestion(user_id, ad_id):
    user_key = f"{USER_PROFILE_PREFIX}{user_id}"
    recent_clicks = r.lrange(f"{user_key}:recent_clicks", 0, 9)
    recent_views = r.lrange(f"{user_key}:recent_views", 0, 9)

    ad_key = f"{AD_METRICS_PREFIX}{ad_id}"
    ad_metrics = r.hgetall(ad_key)

    ctr = float(ad_metrics.get('ctr', 0))
    base_bid = float(ad_metrics.get('cpc', 0))

    click_boost = len(recent_clicks) * 0.05
    view_boost = min(len(recent_views) * 0.02, 0.2)

    suggested_bid = base_bid * (1 + click_boost + view_boost)

    if ctr > 0.05:
        suggested_bid *= 1.2
    elif ctr < 0.01:
        suggested_bid *= 0.8

    return {
        'user_id': user_id,
        'ad_id': ad_id,
        'suggested_bid': round(suggested_bid, 4),
        'current_ctr': ctr,
        'user_click_count': len(recent_clicks),
        'user_view_count': len(recent_views),
        'bid_reason': f"click_boost={click_boost:.2f}, view_boost={view_boost:.2f}"
    }


def get_user_profile(user_id):
    key = f"{USER_PROFILE_PREFIX}{user_id}"
    profile = r.hgetall(key)
    recent_clicks = r.lrange(f"{key}:recent_clicks", 0, 9)
    recent_views = r.lrange(f"{key}:recent_views", 0, 9)

    return {
        'user_id': user_id,
        'last_active': profile.get('last_active', ''),
        'device': profile.get('device', ''),
        'recent_clicks': recent_clicks,
        'recent_views': recent_views,
    }


def get_ad_realtime_metrics(ad_id):
    key = f"{AD_METRICS_PREFIX}{ad_id}"
    return r.hgetall(key)
```

### 4.5 ClickHouse广告数据存储

```sql
-- ============================================
-- ClickHouse 广告数据存储 DDL
-- ============================================

CREATE TABLE ad_impressions_realtime ON CLUSTER default (
    impression_id UInt64,
    ad_id UInt64,
    user_id UInt64,
    media String,
    position String,
    device String,
    impression_time DateTime64(3),
    cost Decimal(10, 4),
    is_fraud UInt8,
    create_time DateTime64(3) DEFAULT now64(),
    INDEX idx_ad_id ad_id TYPE bloom_filter GRANULARITY 1,
    INDEX idx_user_id user_id TYPE bloom_filter GRANULARITY 1,
    INDEX idx_media media TYPE set(20) GRANULARITY 1
) ENGINE = ReplicatedMergeTree(
    '/clickhouse/tables/{shard}/ad_impressions_realtime',
    '{replica}'
)
PARTITION BY toYYYYMMDD(impression_time)
ORDER BY (impression_time, ad_id, user_id)
TTL impression_time + INTERVAL 30 DAY
SETTINGS index_granularity = 8192;

CREATE TABLE ad_clicks_realtime ON CLUSTER default (
    click_id UInt64,
    impression_id UInt64,
    ad_id UInt64,
    user_id UInt64,
    click_time DateTime64(3),
    is_fraud UInt8,
    create_time DateTime64(3) DEFAULT now64(),
    INDEX idx_ad_id ad_id TYPE bloom_filter GRANULARITY 1,
    INDEX idx_user_id user_id TYPE bloom_filter GRANULARITY 1
) ENGINE = ReplicatedMergeTree(
    '/clickhouse/tables/{shard}/ad_clicks_realtime',
    '{replica}'
)
PARTITION BY toYYYYMMDD(click_time)
ORDER BY (click_time, ad_id, user_id)
TTL click_time + INTERVAL 30 DAY
SETTINGS index_granularity = 8192;

CREATE TABLE ad_conversions_realtime ON CLUSTER default (
    conversion_id UInt64,
    click_id UInt64,
    ad_id UInt64,
    user_id UInt64,
    conversion_type UInt8,
    amount Decimal(12, 2),
    conversion_time DateTime64(3),
    create_time DateTime64(3) DEFAULT now64()
) ENGINE = ReplicatedMergeTree(
    '/clickhouse/tables/{shard}/ad_conversions_realtime',
    '{replica}'
)
PARTITION BY toYYYYMMDD(conversion_time)
ORDER BY (conversion_time, ad_id, user_id)
TTL conversion_time + INTERVAL 90 DAY
SETTINGS index_granularity = 8192;

CREATE TABLE ad_metrics_minute ON CLUSTER default (
    window_start DateTime64(3),
    window_end DateTime64(3),
    ad_id UInt64,
    impression_count UInt64,
    click_count UInt64,
    conversion_count UInt64,
    total_cost Decimal(14, 4),
    total_revenue Decimal(14, 2),
    ctr Float64,
    cpc Decimal(10, 4),
    cpm Decimal(10, 4),
    roi Float64
) ENGINE = ReplicatedSummingMergeTree(
    '/clickhouse/tables/{shard}/ad_metrics_minute',
    '{replica}',
    (impression_count, click_count, conversion_count, total_cost, total_revenue)
)
PARTITION BY toYYYYMM(window_start)
ORDER BY (window_start, ad_id)
TTL window_start + INTERVAL 90 DAY
SETTINGS index_granularity = 8192;

CREATE TABLE ad_fraud_events ON CLUSTER default (
    user_id UInt64,
    ad_id UInt64,
    fraud_type String,
    click_count UInt64,
    window_start DateTime64(3),
    window_end DateTime64(3),
    alert_time DateTime64(3),
    create_time DateTime64(3) DEFAULT now64()
) ENGINE = MergeTree()
PARTITION BY toYYYYMMDD(alert_time)
ORDER BY (alert_time, fraud_type, user_id)
TTL alert_time + INTERVAL 30 DAY;

CREATE TABLE ad_attribution_results ON CLUSTER default (
    conversion_id UInt64,
    ad_id UInt64,
    user_id UInt64,
    attribution_model String,
    attribution_weight Float64,
    attributed_revenue Decimal(12, 2),
    touchpoint_time DateTime64(3),
    conversion_time DateTime64(3),
    stat_date Date
) ENGINE = MergeTree()
PARTITION BY toYYYYMM(stat_date)
ORDER BY (stat_date, attribution_model, ad_id)
TTL stat_date + INTERVAL 180 DAY;
```

---

## 五、阶段3 - 归因分析（8h）

### 5.1 Spark批量归因计算

```python
"""
ad_attribution_spark.py

Spark批量归因分析
4种归因模型: 末次点击/首次点击/线性/时间衰减
每日运行，对比不同归因模型的ROI差异
"""
from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col, count, sum as spark_sum, avg, max as spark_max, min as spark_min,
    first, last, when, lit, collect_list, struct, sort_array, explode,
    row_number, desc, asc, size, expr, datediff, hour
)
from pyspark.sql.window import Window
from pyspark.sql.types import DoubleType, ArrayType, StructType, StructField, StringType, LongType
import math

spark = SparkSession.builder \
    .appName("AdAttributionAnalysis") \
    .enableHiveSupport() \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")


def load_touchpoint_data():
    print("=== 加载触点数据 ===")

    impressions = spark.sql("""
        SELECT ad_id, user_id, impression_time AS touchpoint_time,
               'impression' AS touchpoint_type, media, cost
        FROM ad_bidding.impressions
        WHERE impression_time >= date_sub(current_date(), 30)
    """)

    clicks = spark.sql("""
        SELECT ad_id, user_id, click_time AS touchpoint_time,
               'click' AS touchpoint_type, media, 0 AS cost
        FROM ad_bidding.clicks
        WHERE click_time >= date_sub(current_date(), 30)
    """)

    conversions = spark.sql("""
        SELECT conversion_id, user_id, conversion_type, amount,
               conversion_time
        FROM ad_bidding.conversions
        WHERE conversion_time >= date_sub(current_date(), 30)
    """)

    touchpoints = impressions.unionByName(clicks)

    return touchpoints, conversions


def build_user_journeys(touchpoints, conversions):
    print("=== 构建用户触点旅程 ===")

    user_touchpoints = touchpoints.groupBy("user_id").agg(
        sort_array(collect_list(
            struct("touchpoint_time", "ad_id", "touchpoint_type", "media", "cost")
        )).alias("touchpoints")
    )

    user_conversions = conversions.groupBy("user_id").agg(
        collect_list(
            struct("conversion_id", "conversion_type", "amount", "conversion_time")
        ).alias("conversions")
    )

    user_journeys = user_touchpoints.join(user_conversions, "user_id", "inner")

    user_journeys = user_journeys.select(
        "user_id",
        col("touchpoints").alias("touchpoints"),
        explode(col("conversions")).alias("conversion")
    ).select(
        "user_id",
        "touchpoints",
        col("conversion.conversion_id").alias("conversion_id"),
        col("conversion.conversion_type").alias("conversion_type"),
        col("conversion.amount").alias("conversion_amount"),
        col("conversion.conversion_time").alias("conversion_time")
    )

    user_journeys = user_journeys.filter(
        size(col("touchpoints")) > 0
    )

    print(f"用户旅程数: {user_journeys.count()}")
    return user_journeys


def last_click_attribution(user_journeys):
    print("=== 末次点击归因 ===")

    def compute_last_click(touchpoints, conversion_time):
        click_touchpoints = [tp for tp in touchpoints
                             if tp['touchpoint_type'] == 'click'
                             and tp['touchpoint_time'] < conversion_time]
        if not click_touchpoints:
            return None
        return click_touchpoints[-1]

    last_click_udf = spark.udf.register(
        "last_click",
        compute_last_click,
        StructType([
            StructField("touchpoint_time", LongType()),
            StructField("ad_id", LongType()),
            StructField("touchpoint_type", StringType()),
            StructField("media", StringType()),
            StructField("cost", DoubleType())
        ])
    )

    result = user_journeys.withColumn(
        "attributed_touchpoint",
        last_click_udf(col("touchpoints"), col("conversion_time"))
    ).filter(
        col("attributed_touchpoint").isNotNull()
    ).select(
        "conversion_id",
        col("attributed_touchpoint.ad_id").alias("ad_id"),
        "user_id",
        lit("last_click").alias("attribution_model"),
        lit(1.0).alias("attribution_weight"),
        "conversion_amount".alias("attributed_revenue"),
        col("attributed_touchpoint.touchpoint_time").alias("touchpoint_time"),
        "conversion_time"
    )

    return result


def first_click_attribution(user_journeys):
    print("=== 首次点击归因 ===")

    def compute_first_click(touchpoints, conversion_time):
        click_touchpoints = [tp for tp in touchpoints
                             if tp['touchpoint_type'] == 'click'
                             and tp['touchpoint_time'] < conversion_time]
        if not click_touchpoints:
            return None
        return click_touchpoints[0]

    first_click_udf = spark.udf.register(
        "first_click",
        compute_first_click,
        StructType([
            StructField("touchpoint_time", LongType()),
            StructField("ad_id", LongType()),
            StructField("touchpoint_type", StringType()),
            StructField("media", StringType()),
            StructField("cost", DoubleType())
        ])
    )

    result = user_journeys.withColumn(
        "attributed_touchpoint",
        first_click_udf(col("touchpoints"), col("conversion_time"))
    ).filter(
        col("attributed_touchpoint").isNotNull()
    ).select(
        "conversion_id",
        col("attributed_touchpoint.ad_id").alias("ad_id"),
        "user_id",
        lit("first_click").alias("attribution_model"),
        lit(1.0).alias("attribution_weight"),
        "conversion_amount".alias("attributed_revenue"),
        col("attributed_touchpoint.touchpoint_time").alias("touchpoint_time"),
        "conversion_time"
    )

    return result


def linear_attribution(user_journeys):
    print("=== 线性归因 ===")

    def compute_linear(touchpoints, conversion_time, conversion_amount):
        valid_touchpoints = [tp for tp in touchpoints
                             if tp['touchpoint_time'] < conversion_time]
        if not valid_touchpoints:
            return []

        weight = 1.0 / len(valid_touchpoints)
        return [(tp['ad_id'], weight, conversion_amount * weight, tp['touchpoint_time'])
                for tp in valid_touchpoints]

    linear_schema = ArrayType(StructType([
        StructField("ad_id", LongType()),
        StructField("weight", DoubleType()),
        StructField("revenue", DoubleType()),
        StructField("touchpoint_time", LongType())
    ]))

    linear_udf = spark.udf.register("linear_attr", compute_linear, linear_schema)

    result = user_journeys.withColumn(
        "attributions",
        linear_udf(col("touchpoints"), col("conversion_time"), col("conversion_amount"))
    ).select(
        "conversion_id", "user_id", "conversion_time", "conversion_amount",
        explode(col("attributions")).alias("attr")
    ).select(
        "conversion_id",
        col("attr.ad_id").alias("ad_id"),
        "user_id",
        lit("linear").alias("attribution_model"),
        col("attr.weight").alias("attribution_weight"),
        col("attr.revenue").alias("attributed_revenue"),
        col("attr.touchpoint_time").alias("touchpoint_time"),
        "conversion_time"
    )

    return result


def time_decay_attribution(user_journeys, decay_rate=0.5, window_days=7):
    print("=== 时间衰减归因 ===")

    def compute_time_decay(touchpoints, conversion_time, conversion_amount, decay_rate, window_days):
        window_ms = window_days * 86400000
        valid_touchpoints = [tp for tp in touchpoints
                             if tp['touchpoint_time'] < conversion_time
                             and (conversion_time - tp['touchpoint_time']) <= window_ms]

        if not valid_touchpoints:
            return []

        weights = []
        for tp in valid_touchpoints:
            time_diff_hours = (conversion_time - tp['touchpoint_time']) / 3600000.0
            weight = math.pow(decay_rate, time_diff_hours / 24.0)
            weights.append(weight)

        total_weight = sum(weights)
        normalized_weights = [w / total_weight for w in weights]

        return [(tp['ad_id'], nw, conversion_amount * nw, tp['touchpoint_time'])
                for tp, nw in zip(valid_touchpoints, normalized_weights)]

    decay_schema = ArrayType(StructType([
        StructField("ad_id", LongType()),
        StructField("weight", DoubleType()),
        StructField("revenue", DoubleType()),
        StructField("touchpoint_time", LongType())
    ]))

    time_decay_udf = spark.udf.register("time_decay_attr", compute_time_decay, decay_schema)

    result = user_journeys.withColumn(
        "attributions",
        time_decay_udf(col("touchpoints"), col("conversion_time"),
                       col("conversion_amount"), lit(decay_rate), lit(window_days))
    ).select(
        "conversion_id", "user_id", "conversion_time", "conversion_amount",
        explode(col("attributions")).alias("attr")
    ).select(
        "conversion_id",
        col("attr.ad_id").alias("ad_id"),
        "user_id",
        lit("time_decay").alias("attribution_model"),
        col("attr.weight").alias("attribution_weight"),
        col("attr.revenue").alias("attributed_revenue"),
        col("attr.touchpoint_time").alias("touchpoint_time"),
        "conversion_time"
    )

    return result


def compare_attribution_models(all_results):
    print("=== 归因模型对比 ===")

    ad_level = all_results.groupBy("attribution_model", "ad_id").agg(
        spark_sum("attribution_weight").alias("total_weight"),
        spark_sum("attributed_revenue").alias("total_revenue"),
        count("conversion_id").alias("conversion_count")
    )

    ad_level.orderBy("attribution_model", desc("total_revenue")).show(50, truncate=False)

    model_summary = all_results.groupBy("attribution_model").agg(
        spark_sum("attributed_revenue").alias("total_revenue"),
        count("conversion_id").alias("total_conversions"),
        avg("attribution_weight").alias("avg_weight")
    )

    model_summary.show(truncate=False)

    media_level = all_results.join(
        spark.sql("SELECT ad_id, media FROM ad_bidding.ads"),
        "ad_id"
    ).groupBy("attribution_model", "media").agg(
        spark_sum("attributed_revenue").alias("total_revenue"),
        count("conversion_id").alias("conversion_count")
    ).orderBy("attribution_model", desc("total_revenue"))

    media_level.show(50, truncate=False)

    return ad_level, model_summary, media_level


def run_attribution_pipeline():
    touchpoints, conversions = load_touchpoint_data()
    user_journeys = build_user_journeys(touchpoints, conversions)

    last_click_result = last_click_attribution(user_journeys)
    first_click_result = first_click_attribution(user_journeys)
    linear_result = linear_attribution(user_journeys)
    time_decay_result = time_decay_attribution(user_journeys)

    all_results = last_click_result.unionByName(first_click_result) \
        .unionByName(linear_result) \
        .unionByName(time_decay_result)

    all_results.cache()

    all_results.write.mode("overwrite") \
        .partitionBy("attribution_model") \
        .saveAsTable("ad_bidding.attribution_results")

    ad_level, model_summary, media_level = compare_attribution_models(all_results)

    print("=== 归因分析完成 ===")


if __name__ == "__main__":
    run_attribution_pipeline()
    spark.stop()
```

### 5.2 Flink实时归因

```java
package com.example.ad.attribution;

import org.apache.flink.api.common.state.ListState;
import org.apache.flink.api.common.state.ListStateDescriptor;
import org.apache.flink.api.common.state.ValueState;
import org.apache.flink.api.common.state.ValueStateDescriptor;
import org.apache.flink.configuration.Configuration;
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.streaming.api.functions.KeyedProcessFunction;
import org.apache.flink.streaming.connectors.kafka.FlinkKafkaConsumer;
import org.apache.flink.streaming.connectors.kafka.FlinkKafkaProducer;
import org.apache.flink.api.common.serialization.SimpleStringSchema;
import org.apache.flink.util.Collector;
import com.alibaba.fastjson.JSON;
import com.alibaba.fastjson.JSONObject;

import java.util.ArrayList;
import java.util.List;
import java.util.Properties;
import java.util.concurrent.TimeUnit;

public class RealTimeAttribution {

    public static void main(String[] args) throws Exception {
        StreamExecutionEnvironment env =
            StreamExecutionEnvironment.getExecutionEnvironment();

        env.enableCheckpointing(60000);

        Properties kafkaProps = new Properties();
        kafkaProps.setProperty("bootstrap.servers", "localhost:9092");
        kafkaProps.setProperty("group.id", "ad-attribution-group");
        kafkaProps.setProperty("auto.offset.reset", "latest");

        DataStream<ClickEvent> clickStream = env
            .addSource(new FlinkKafkaConsumer<>(
                "ad.events.click", new SimpleStringSchema(), kafkaProps))
            .map(line -> JSON.parseObject(line, ClickEvent.class));

        DataStream<ConversionEvent> conversionStream = env
            .addSource(new FlinkKafkaConsumer<>(
                "ad.events.conversion", new SimpleStringSchema(), kafkaProps))
            .map(line -> JSON.parseObject(line, ConversionEvent.class));

        DataStream<AttributionResult> attributionResults = conversionStream
            .keyBy(e -> e.userId)
            .process(new RealTimeAttributionFunction(clickStream));

        FlinkKafkaProducer<String> sink = new FlinkKafkaProducer<>(
            "ad.attribution.realtime",
            new SimpleStringSchema(),
            kafkaProps
        );

        attributionResults.map(r -> JSON.toJSONString(r)).addSink(sink);

        env.execute("Real-Time Ad Attribution");
    }

    static class RealTimeAttributionFunction
            extends KeyedProcessFunction<Long, ConversionEvent, AttributionResult> {

        private ListState<Touchpoint> touchpointWindow;
        private ValueState<Long> lastCleanupTime;

        @Override
        public void open(Configuration parameters) {
            touchpointWindow = getRuntimeContext().getListState(
                new ListStateDescriptor<>("touchpoints", Touchpoint.class));
            lastCleanupTime = getRuntimeContext().getState(
                new ValueStateDescriptor<>("lastCleanup", Long.class));
        }

        @Override
        public void processElement(ConversionEvent conversion, Context ctx,
                                   Collector<AttributionResult> out) throws Exception {
            long sevenDaysAgo = conversion.conversionTime - TimeUnit.DAYS.toMillis(7);

            List<Touchpoint> validTouchpoints = new ArrayList<>();
            for (Touchpoint tp : touchpointWindow.get()) {
                if (tp.touchpointTime > sevenDaysAgo &&
                    tp.touchpointTime < conversion.conversionTime) {
                    validTouchpoints.add(tp);
                }
            }

            if (validTouchpoints.isEmpty()) {
                return;
            }

            validTouchpoints.sort((a, b) -> Long.compare(a.touchpointTime, b.touchpointTime));

            Touchpoint lastClick = null;
            for (int i = validTouchpoints.size() - 1; i >= 0; i--) {
                if ("click".equals(validTouchpoints.get(i).touchpointType)) {
                    lastClick = validTouchpoints.get(i);
                    break;
                }
            }

            if (lastClick != null) {
                AttributionResult result = new AttributionResult();
                result.conversionId = conversion.conversionId;
                result.adId = lastClick.adId;
                result.userId = conversion.userId;
                result.attributionModel = "realtime_last_click";
                result.attributionWeight = 1.0;
                result.attributedRevenue = conversion.amount;
                result.touchpointTime = lastClick.touchpointTime;
                result.conversionTime = conversion.conversionTime;
                result.touchpointCount = validTouchpoints.size();
                out.collect(result);
            }

            long lastCleanup = lastCleanupTime.value() != null ? lastCleanupTime.value() : 0;
            if (conversion.conversionTime - lastCleanup > TimeUnit.HOURS.toMillis(1)) {
                List<Touchpoint> allTouchpoints = new ArrayList<>();
                for (Touchpoint tp : touchpointWindow.get()) {
                    allTouchpoints.add(tp);
                }
                List<Touchpoint> cleaned = new ArrayList<>();
                for (Touchpoint tp : allTouchpoints) {
                    if (tp.touchpointTime > sevenDaysAgo) {
                        cleaned.add(tp);
                    }
                }
                touchpointWindow.update(cleaned);
                lastCleanupTime.update(conversion.conversionTime);
            }
        }
    }

    static class Touchpoint {
        public Long adId;
        public String touchpointType;
        public Long touchpointTime;
        public String media;
    }

    static class ClickEvent {
        public Long adId;
        public Long userId;
        public Long clickTime;
    }

    static class ConversionEvent {
        public Long conversionId;
        public Long adId;
        public Long userId;
        public Integer conversionType;
        public Double amount;
        public Long conversionTime;
    }

    static class AttributionResult {
        public Long conversionId;
        public Long adId;
        public Long userId;
        public String attributionModel;
        public Double attributionWeight;
        public Double attributedRevenue;
        public Long touchpointTime;
        public Long conversionTime;
        public Integer touchpointCount;
    }
}
```

---

## 六、阶段4 - 报表与优化（5h）

### 6.1 Grafana广告大屏

```json
{
  "dashboard": {
    "title": "广告实时竞价与归因分析",
    "refresh": "5s",
    "panels": [
      {
        "title": "实时花费",
        "type": "stat",
        "targets": [{
          "rawSql": "SELECT sum(total_cost) AS total_cost FROM ad_metrics_minute WHERE window_start >= today()",
          "format": "table"
        }],
        "fieldConfig": {
          "defaults": {
            "unit": "currencyCNY",
            "decimals": 2
          }
        }
      },
      {
        "title": "实时曝光/点击/转化",
        "type": "timeseries",
        "targets": [{
          "rawSql": "SELECT window_start, sum(impression_count) AS impressions, sum(click_count) AS clicks, sum(conversion_count) AS conversions FROM ad_metrics_minute WHERE window_start >= now() - INTERVAL 1 HOUR GROUP BY window_start ORDER BY window_start",
          "format": "time_series"
        }]
      },
      {
        "title": "各广告主ROI排名",
        "type": "table",
        "targets": [{
          "rawSql": "SELECT m.ad_id, a.ad_name, a.advertiser_id, sum(m.total_cost) AS total_cost, sum(m.total_revenue) AS total_revenue, CASE WHEN sum(m.total_cost) > 0 THEN sum(m.total_revenue) / sum(m.total_cost) ELSE 0 END AS roi FROM ad_metrics_minute m JOIN ads a ON m.ad_id = a.ad_id WHERE m.window_start >= today() GROUP BY m.ad_id, a.ad_name, a.advertiser_id ORDER BY roi DESC LIMIT 20",
          "format": "table"
        }]
      },
      {
        "title": "反作弊拦截统计",
        "type": "stat",
        "targets": [{
          "rawSql": "SELECT count() AS fraud_count FROM ad_fraud_events WHERE alert_time >= now() - INTERVAL 1 HOUR",
          "format": "table"
        }],
        "fieldConfig": {
          "defaults": {
            "color": {"mode": "thresholds"},
            "thresholds": {
              "steps": [
                {"color": "green", "value": null},
                {"color": "yellow", "value": 100},
                {"color": "red", "value": 500}
              ]
            }
          }
        }
      },
      {
        "title": "归因模型对比",
        "type": "barchart",
        "targets": [{
          "rawSql": "SELECT attribution_model, sum(attributed_revenue) AS total_revenue, count() AS conversion_count FROM ad_attribution_results WHERE stat_date = today() GROUP BY attribution_model ORDER BY total_revenue DESC",
          "format": "table"
        }]
      },
      {
        "title": "各渠道归因贡献度",
        "type": "piechart",
        "targets": [{
          "rawSql": "SELECT a.media, sum(ar.attributed_revenue) AS revenue FROM ad_attribution_results ar JOIN ads a ON ar.ad_id = a.ad_id WHERE ar.attribution_model = 'time_decay' AND ar.stat_date = today() GROUP BY a.media ORDER BY revenue DESC",
          "format": "table"
        }]
      },
      {
        "title": "CTR趋势",
        "type": "timeseries",
        "targets": [{
          "rawSql": "SELECT window_start, avg(ctr) AS avg_ctr FROM ad_metrics_minute WHERE window_start >= now() - INTERVAL 6 HOUR GROUP BY window_start ORDER BY window_start",
          "format": "time_series"
        }],
        "fieldConfig": {
          "defaults": {
            "unit": "percentunit"
          }
        }
      },
      {
        "title": "竞价胜率分布",
        "type": "histogram",
        "targets": [{
          "rawSql": "SELECT ad_id, sum(CASE WHEN is_won = 1 THEN 1 ELSE 0 END) / count(*) AS win_rate FROM ad_bidding.bid_requests WHERE request_time >= now() - INTERVAL 1 HOUR GROUP BY ad_id",
          "format": "table"
        }]
      }
    ]
  }
}
```

### 6.2 自动优化策略

```python
"""
ad_optimization.py

广告自动优化策略
低CTR广告自动降价 / 高ROI广告自动加价 / 作弊流量自动过滤
"""
import redis
import pymysql
import json
from datetime import datetime, timedelta

r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'root123',
    'database': 'ad_bidding',
    'charset': 'utf8mb4'
}

AD_METRICS_PREFIX = "ad:metrics:"
OPTIMIZATION_LOG_PREFIX = "ad:optimization:"


class AdOptimizer:

    def __init__(self):
        self.conn = pymysql.connect(**DB_CONFIG)
        self.cursor = self.conn.cursor()

    def optimize_low_ctr_ads(self, ctr_threshold=0.01, price_cut_ratio=0.8):
        print("=== 低CTR广告降价 ===")

        self.cursor.execute("""
            SELECT ad_id, ad_name, bid_price
            FROM ads WHERE status = 1
        """)
        ads = self.cursor.fetchall()

        optimized = 0
        for ad_id, ad_name, current_price in ads:
            key = f"{AD_METRICS_PREFIX}{ad_id}"
            metrics = r.hgetall(key)
            if not metrics:
                continue

            ctr = float(metrics.get('ctr', 0))
            if ctr < ctr_threshold and ctr > 0:
                new_price = round(current_price * price_cut_ratio, 4)
                new_price = max(new_price, 1.0)

                self.cursor.execute(
                    "UPDATE ads SET bid_price = %s WHERE ad_id = %s",
                    (new_price, ad_id)
                )

                log_key = f"{OPTIMIZATION_LOG_PREFIX}{ad_id}"
                r.lpush(log_key, json.dumps({
                    'action': 'PRICE_CUT',
                    'old_price': current_price,
                    'new_price': new_price,
                    'ctr': ctr,
                    'reason': f'CTR {ctr:.4f} < {ctr_threshold}',
                    'timestamp': datetime.now().isoformat()
                }, ensure_ascii=False))
                r.ltrim(log_key, 0, 99)

                optimized += 1
                print(f"  广告{ad_id}({ad_name}): CTR={ctr:.4f}, "
                      f"出价 {current_price}→{new_price}")

        self.conn.commit()
        print(f"低CTR广告降价完成: {optimized}个")
        return optimized

    def optimize_high_roi_ads(self, roi_threshold=3.0, price_boost_ratio=1.2):
        print("=== 高ROI广告加价 ===")

        self.cursor.execute("""
            SELECT ad_id, ad_name, bid_price, daily_budget
            FROM ads WHERE status = 1
        """)
        ads = self.cursor.fetchall()

        optimized = 0
        for ad_id, ad_name, current_price, daily_budget in ads:
            key = f"{AD_METRICS_PREFIX}{ad_id}"
            metrics = r.hgetall(key)
            if not metrics:
                continue

            total_cost = float(metrics.get('total_cost', 0))
            budget_consumed = float(metrics.get('budget_consumed', 0))

            if total_cost > 0:
                revenue = float(metrics.get('total_revenue', 0))
                roi = revenue / total_cost if total_cost > 0 else 0

                if roi > roi_threshold and budget_consumed < daily_budget * 0.8:
                    new_price = round(current_price * price_boost_ratio, 4)

                    self.cursor.execute(
                        "UPDATE ads SET bid_price = %s WHERE ad_id = %s",
                        (new_price, ad_id)
                    )

                    log_key = f"{OPTIMIZATION_LOG_PREFIX}{ad_id}"
                    r.lpush(log_key, json.dumps({
                        'action': 'PRICE_BOOST',
                        'old_price': current_price,
                        'new_price': new_price,
                        'roi': roi,
                        'reason': f'ROI {roi:.2f} > {roi_threshold}',
                        'timestamp': datetime.now().isoformat()
                    }, ensure_ascii=False))
                    r.ltrim(log_key, 0, 99)

                    optimized += 1
                    print(f"  广告{ad_id}({ad_name}): ROI={roi:.2f}, "
                          f"出价 {current_price}→{new_price}")

        self.conn.commit()
        print(f"高ROI广告加价完成: {optimized}个")
        return optimized

    def filter_fraud_traffic(self):
        print("=== 作弊流量自动过滤 ===")

        fraud_users = set()
        fraud_ads = set()

        for key in r.scan_iter(match="ad:fraud:*"):
            data = r.hgetall(key)
            if data:
                user_id = data.get('user_id')
                ad_id = data.get('ad_id')
                if user_id:
                    fraud_users.add(int(user_id))
                if ad_id:
                    fraud_ads.add(int(ad_id))

        fraud_user_key = "ad:fraud:user_blacklist"
        if fraud_users:
            pipe = r.pipeline()
            for uid in fraud_users:
                pipe.sadd(fraud_user_key, str(uid))
            pipe.execute()

        fraud_ad_key = "ad:fraud:ad_blacklist"
        if fraud_ads:
            pipe = r.pipeline()
            for aid in fraud_ads:
                pipe.sadd(fraud_ad_key, str(aid))
            pipe.execute()

        print(f"作弊流量过滤: {len(fraud_users)}个用户, {len(fraud_ads)}个广告加入黑名单")
        return len(fraud_users), len(fraud_ads)

    def generate_daily_report(self):
        print("=== 生成每日广告效果日报 ===")

        self.cursor.execute("""
            SELECT
                COUNT(DISTINCT i.impression_id) AS total_impressions,
                COUNT(DISTINCT c.click_id) AS total_clicks,
                COUNT(DISTINCT cv.conversion_id) AS total_conversions,
                SUM(cv.amount) AS total_revenue,
                COUNT(DISTINCT i.ad_id) AS active_ads
            FROM impressions i
            LEFT JOIN clicks c ON i.impression_id = c.impression_id
            LEFT JOIN conversions cv ON c.click_id = cv.click_id
            WHERE i.impression_time >= DATE_SUB(CURDATE(), INTERVAL 1 DAY)
        """)

        row = self.cursor.fetchone()
        report = {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'total_impressions': row[0] or 0,
            'total_clicks': row[1] or 0,
            'total_conversions': row[2] or 0,
            'total_revenue': float(row[3] or 0),
            'active_ads': row[4] or 0,
            'ctr': (row[1] or 0) / (row[0] or 1),
            'cvr': (row[2] or 0) / (row[1] or 1),
        }

        report_key = f"ad:report:daily:{report['date']}"
        r.setex(report_key, 86400 * 30, json.dumps(report, ensure_ascii=False))

        print(f"日报已生成: {json.dumps(report, ensure_ascii=False, indent=2)}")
        return report

    def close(self):
        self.cursor.close()
        self.conn.close()


if __name__ == '__main__':
    optimizer = AdOptimizer()
    optimizer.optimize_low_ctr_ads(ctr_threshold=0.01, price_cut_ratio=0.8)
    optimizer.optimize_high_roi_ads(roi_threshold=3.0, price_boost_ratio=1.2)
    optimizer.filter_fraud_traffic()
    optimizer.generate_daily_report()
    optimizer.close()
```

### 6.3 Docker Compose部署

```yaml
# docker-compose-ad-bidding.yml
version: '3.8'

services:
  zookeeper:
    image: confluentinc/cp-zookeeper:7.5.0
    environment:
      ZOOKEEPER_CLIENT_PORT: 2181

  kafka:
    image: confluentinc/cp-kafka:7.5.0
    depends_on:
      - zookeeper
    ports:
      - "9092:9092"
    environment:
      KAFKA_BROKER_ID: 1
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://localhost:9092
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
      KAFKA_TRANSACTION_STATE_LOG_REPLICATION_FACTOR: 1
      KAFKA_TRANSACTION_STATE_LOG_MIN_ISR: 1

  mysql:
    image: mysql:8.0
    ports:
      - "3306:3306"
    environment:
      MYSQL_ROOT_PASSWORD: root123
      MYSQL_DATABASE: ad_bidding
    volumes:
      - ./sql:/docker-entrypoint-initdb.d

  redis:
    image: redis:7.2
    ports:
      - "6379:6379"
    command: redis-server --maxmemory 4gb --maxmemory-policy allkeys-lru

  flink-jobmanager:
    image: flink:1.17.1-scala_2.12
    ports:
      - "8081:8081"
    command: jobmanager
    environment:
      - JOB_MANAGER_RPC_ADDRESS=flink-jobmanager

  flink-taskmanager:
    image: flink:1.17.1-scala_2.12
    depends_on:
      - flink-jobmanager
    command: taskmanager
    environment:
      - JOB_MANAGER_RPC_ADDRESS=flink-jobmanager
    deploy:
      replicas: 3

  clickhouse:
    image: clickhouse/clickhouse-server:23.8
    ports:
      - "8123:8123"
      - "9000:9000"
    volumes:
      - ./clickhouse/init.sql:/docker-entrypoint-initdb.d/init.sql

  spark-master:
    image: bitnami/spark:3.5
    ports:
      - "8080:8080"
      - "7077:7077"
    environment:
      - SPARK_MODE=master

  spark-worker:
    image: bitnami/spark:3.5
    depends_on:
      - spark-master
    environment:
      - SPARK_MODE=worker
      - SPARK_MASTER_URL=spark://spark-master:7077
    deploy:
      replicas: 2

  grafana:
    image: grafana/grafana:10.1
    ports:
      - "3000:3000"
    environment:
      GF_INSTALL_PLUGINS: vertamedia-clickhouse-datasource
    volumes:
      - ./grafana/dashboards:/etc/grafana/provisioning/dashboards
      - ./grafana/datasources:/etc/grafana/provisioning/datasources
```

---

## 七、验收标准

| 验收项 | 标准 | 验证方法 |
|--------|------|----------|
| 数据模拟 | 1000广告+100万用户数据生成完成 | MySQL表记录数 |
| 实时竞价 | CTR/CPC/CPM指标实时计算 | Kafka Consumer验证 |
| 反作弊 | 同用户1分钟3次点击标记作弊 | 注入作弊点击验证 |
| Redis服务 | 用户画像+广告指标可查询 | redis-cli验证 |
| 归因分析 | 4种归因模型结果可对比 | Spark输出验证 |
| 实时归因 | 转化事件到达时实时归因 | Flink输出验证 |
| 自动优化 | 降价/加价/过滤策略可执行 | Redis日志验证 |
| Grafana | 8个面板实时刷新 | 目视检查 |

---

## 八、交付物清单

| 序号 | 交付物 | 文件 | 要求 |
|------|--------|------|------|
| 1 | 广告数据模拟器 | `ad_data_simulator.py` | 曝光+点击+转化+竞价流 |
| 2 | Flink实时竞价处理 | `AdRealTimeProcessor.java` | CTR+反作弊+竞价统计 |
| 3 | Flink SQL指标计算 | `ad_metrics_sql.sql` | 实时指标+反作弊SQL |
| 4 | Redis实时服务 | `ad_redis_service.py` | 用户画像+广告指标+竞价辅助 |
| 5 | ClickHouse建表 | `ad_clickhouse_ddl.sql` | 5张表含TTL和索引 |
| 6 | Spark归因分析 | `ad_attribution_spark.py` | 4种归因模型+对比 |
| 7 | Flink实时归因 | `RealTimeAttribution.java` | 触点窗口+实时归因 |
| 8 | 自动优化策略 | `ad_optimization.py` | 降价+加价+反作弊 |
| 9 | Grafana Dashboard | `ad_bidding_dashboard.json` | 8面板广告大屏 |
| 10 | Docker Compose | `docker-compose-ad-bidding.yml` | 一键启动全栈环境 |

---

## 九、评分标准

| 评分项 | 权重 | 要求 |
|--------|------|------|
| 数据模拟 | 10% | 模拟器可运行，4种事件流完整 |
| 实时竞价处理 | 25% | Flink实时指标+反作弊全部实现 |
| Redis实时服务 | 10% | 用户画像+竞价辅助可查询 |
| 归因分析 | 25% | 4种归因模型结果正确，对比清晰 |
| 报表与优化 | 20% | Grafana大屏+自动优化策略 |
| 代码质量 | 10% | 代码规范，异常处理完善，可复现 |
