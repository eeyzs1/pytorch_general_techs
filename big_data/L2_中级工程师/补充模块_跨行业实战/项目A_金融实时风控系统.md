# 项目A：金融实时风控系统

> **所属阶段**：L2 中级工程师 | **模块**：补充模块_跨行业实战 | **预计时长**：30h | **难度**：★★★★☆
>
> **技术栈**：MySQL → Kafka → Flink → Redis + ClickHouse + Neo4j → Grafana
>
> **前置要求**：完成L2课时17-18（Kafka深入）+ 课时19-21（Flink流处理）+ 项目7（实时交易监控大屏）

---

## 一、项目描述

构建金融场景的实时交易风控系统，检测欺诈交易和异常行为。项目覆盖金融数据建模、实时风控管道、图风控分析、监控报告全流程，让学员掌握金融行业大数据的核心应用模式。

### 业务价值

```
金融实时风控系统解决的问题：

  问题1: "如何实时识别欺诈交易？"
    → 以前: T+1离线分析，欺诈已发生无法挽回
    → 现在: 实时规则引擎，毫秒级拦截

  问题2: "如何发现团伙欺诈？"
    → 以前: 单笔单账户分析，看不到关联关系
    → 现在: 图风控，识别共用设备/IP的资金团伙

  问题3: "风控规则效果如何评估？"
    → 以前: 凭经验调参，缺乏量化指标
    → 现在: 精确率/召回率/F1实时评估，持续优化

  问题4: "误报和漏报如何平衡？"
    → 以前: 规则太严误报多，太松漏报多
    → 现在: 分级决策（放行/验证/拦截），精细化管理
```

---

## 二、整体架构

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                           金融实时风控系统                                     │
│                                                                              │
│  ┌─────────┐    ┌───────────┐    ┌──────────────┐    ┌────────────────────┐ │
│  │  MySQL  │───→│   Kafka   │───→│    Flink     │───→│  Redis + ClickHouse│ │
│  │(交易数据)│    │ (消息队列) │    │(实时风控引擎)│    │ (实时特征+OLAP)    │ │
│  └─────────┘    └───────────┘    └──────┬───────┘    └────────┬───────────┘ │
│                                         │                     │             │
│                    ┌────────────────────┼─────────────────────┘             │
│                    │                    │                                    │
│             ┌──────▼──────┐    ┌───────▼────────┐    ┌──────────────────┐  │
│             │   Neo4j     │    │    Grafana      │    │     Spark        │  │
│             │  (图风控)    │    │  (风控大屏)     │    │  (批量图计算)    │  │
│             └─────────────┘    └────────────────┘    └──────────────────┘  │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 三、阶段1 - 金融数据模拟与建模（5h）

### 3.1 金融数据模型设计

```sql
-- ============================================
-- 金融风控数据模型 DDL
-- 三张核心表：账户表、交易表、用户表
-- ============================================

CREATE DATABASE IF NOT EXISTS finance_risk;

-- 1. 用户表
CREATE TABLE finance_risk.users (
    user_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL,
    id_card VARCHAR(18) NOT NULL UNIQUE,
    phone VARCHAR(11) NOT NULL UNIQUE,
    risk_level TINYINT DEFAULT 0 COMMENT '0-正常 1-低风险 2-中风险 3-高风险',
    register_time DATETIME NOT NULL,
    update_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_phone (phone),
    INDEX idx_id_card (id_card),
    INDEX idx_risk_level (risk_level)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 2. 账户表
CREATE TABLE finance_risk.accounts (
    account_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT NOT NULL,
    account_type TINYINT NOT NULL COMMENT '1-储蓄卡 2-信用卡 3-理财账户',
    balance DECIMAL(20, 2) DEFAULT 0.00,
    open_time DATETIME NOT NULL,
    status TINYINT DEFAULT 1 COMMENT '0-冻结 1-正常 2-注销',
    update_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_user_id (user_id),
    INDEX idx_account_type (account_type),
    INDEX idx_status (status),
    FOREIGN KEY (user_id) REFERENCES finance_risk.users(user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 3. 交易表
CREATE TABLE finance_risk.transactions (
    transaction_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    account_id BIGINT NOT NULL,
    transaction_type TINYINT NOT NULL COMMENT '1-转账 2-消费 3-提现 4-充值',
    amount DECIMAL(20, 2) NOT NULL,
    merchant VARCHAR(100) COMMENT '商户名称',
    transaction_time DATETIME NOT NULL,
    ip VARCHAR(45) NOT NULL,
    device_id VARCHAR(64) NOT NULL,
    city VARCHAR(50),
    is_fraud TINYINT DEFAULT 0 COMMENT '0-正常 1-欺诈',
    fraud_type VARCHAR(20) COMMENT '欺诈类型',
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_account_id (account_id),
    INDEX idx_transaction_time (transaction_time),
    INDEX idx_is_fraud (is_fraud),
    INDEX idx_device_id (device_id),
    INDEX idx_ip (ip),
    FOREIGN KEY (account_id) REFERENCES finance_risk.accounts(account_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 4. 风控决策记录表
CREATE TABLE finance_risk.risk_decisions (
    decision_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    transaction_id BIGINT NOT NULL,
    account_id BIGINT NOT NULL,
    risk_level VARCHAR(10) NOT NULL COMMENT 'LOW/MEDIUM/HIGH',
    risk_score INT COMMENT '0-100',
    rule_hits VARCHAR(500) COMMENT '命中的规则列表',
    action VARCHAR(20) NOT NULL COMMENT 'PASS/VERIFY/BLOCK',
    decision_time DATETIME NOT NULL,
    reviewer VARCHAR(50) COMMENT '人工审核人',
    review_result TINYINT COMMENT '0-确认拦截 1-放行',
    review_time DATETIME,
    INDEX idx_transaction_id (transaction_id),
    INDEX idx_risk_level (risk_level),
    INDEX idx_decision_time (decision_time)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

### 3.2 模拟数据生成脚本

```python
"""
finance_data_generator.py

金融交易数据模拟生成器
生成100万账户、5000万交易（3个月）
正常交易模式 + 欺诈交易模式
"""
import pymysql
import random
import time
import hashlib
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor

DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'root123',
    'database': 'finance_risk',
    'charset': 'utf8mb4'
}

CITIES = ['北京', '上海', '广州', '深圳', '杭州', '成都', '武汉', '南京',
          '重庆', '西安', '苏州', '天津', '长沙', '郑州', '东莞', '青岛']

MERCHANTS = {
    2: ['淘宝', '京东', '拼多多', '美团', '饿了么', '滴滴', '星巴克', '沃尔玛',
        '盒马鲜生', '全家便利店', '中石化', '中国电信', '中国移动'],
    1: ['张三', '李四', '王五', '赵六', '钱七', '孙八']
}

FRAUD_TYPES = ['盗刷', '套现', '洗钱', '钓鱼', '团伙欺诈']

SURNAMES = ['张', '李', '王', '刘', '陈', '杨', '赵', '黄', '周', '吴',
            '徐', '孙', '胡', '朱', '高', '林', '何', '郭', '马', '罗']
GIVEN_NAMES = ['伟', '芳', '娜', '秀英', '敏', '静', '丽', '强', '磊', '军',
               '洋', '勇', '艳', '杰', '娟', '涛', '明', '超', '秀兰', '霞']


def generate_id_card():
    area_code = random.choice(['110101', '310101', '440103', '500103',
                                '330102', '510104', '420102', '320102'])
    birth = f"{random.randint(1960, 2002)}{random.randint(1,12):02d}{random.randint(1,28):02d}"
    seq = f"{random.randint(0,999):03d}"
    base = area_code + birth + seq
    weights = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
    check_chars = '10X98765432'
    total = sum(int(base[i]) * weights[i] for i in range(17))
    return base + check_chars[total % 11]


def generate_phone():
    prefixes = ['130', '131', '132', '133', '135', '136', '137', '138',
                '139', '150', '151', '152', '155', '156', '158', '159',
                '170', '176', '177', '178', '180', '181', '182', '185']
    return random.choice(prefixes) + ''.join([str(random.randint(0, 9)) for _ in range(8)])


def generate_device_id(user_id, is_fraud=False):
    if is_fraud and random.random() < 0.7:
        return f"DEV_FRAUD_{random.randint(1, 500)}"
    base = f"DEV_{user_id}_{random.randint(1, 3)}"
    return hashlib.md5(base.encode()).hexdigest()[:16]


def generate_ip(city, is_fraud=False):
    city_ips = {
        '北京': ['116.24', '116.25', '123.120', '123.121'],
        '上海': ['114.80', '114.81', '116.228', '116.229'],
        '广州': ['113.108', '113.109', '119.75', '119.76'],
        '深圳': ['113.116', '113.117', '183.14', '183.15'],
        '杭州': ['115.236', '115.237', '122.224', '122.225'],
        '成都': ['118.112', '118.113', '171.208', '171.209'],
        '武汉': ['119.36', '119.37', '171.80', '171.81'],
        '南京': ['114.212', '114.213', '122.192', '122.193'],
    }
    if is_fraud and random.random() < 0.6:
        fraud_city = random.choice([c for c in CITIES if c != city])
        prefix = random.choice(city_ips.get(fraud_city, ['10.0']))
    else:
        prefix = random.choice(city_ips.get(city, ['10.0']))
    return f"{prefix}.{random.randint(1,254)}.{random.randint(1,254)}"


class FinanceDataGenerator:

    def __init__(self):
        self.conn = pymysql.connect(**DB_CONFIG)
        self.cursor = self.conn.cursor()
        self.user_count = 0
        self.account_count = 0
        self.transaction_count = 0
        self.fraud_count = 0
        self.user_city_map = {}
        self.user_device_map = {}

    def generate_users(self, count=1000000):
        print(f"开始生成 {count} 个用户...")
        batch_size = 5000
        batch = []

        for i in range(count):
            name = random.choice(SURNAMES) + random.choice(GIVEN_NAMES)
            id_card = generate_id_card()
            phone = generate_phone()
            risk_level = random.choices([0, 1, 2, 3], weights=[90, 7, 2, 1])[0]
            register_time = datetime(2023, 1, 1) + timedelta(
                days=random.randint(0, 729),
                hours=random.randint(0, 23),
                minutes=random.randint(0, 59)
            )
            city = random.choice(CITIES)
            self.user_city_map[i + 1] = city

            batch.append((name, id_card, phone, risk_level, register_time))

            if len(batch) >= batch_size:
                self.cursor.executemany(
                    "INSERT INTO users (name, id_card, phone, risk_level, register_time) VALUES (%s,%s,%s,%s,%s)",
                    batch
                )
                self.conn.commit()
                self.user_count += len(batch)
                batch = []
                if self.user_count % 50000 == 0:
                    print(f"  已生成 {self.user_count} 个用户")

        if batch:
            self.cursor.executemany(
                "INSERT INTO users (name, id_card, phone, risk_level, register_time) VALUES (%s,%s,%s,%s,%s)",
                batch
            )
            self.conn.commit()
            self.user_count += len(batch)

        print(f"用户生成完成: {self.user_count}")

    def generate_accounts(self):
        print("开始生成账户...")
        self.cursor.execute("SELECT user_id FROM users")
        user_ids = [row[0] for row in self.cursor.fetchall()]

        batch_size = 5000
        batch = []

        for user_id in user_ids:
            num_accounts = random.choices([1, 2, 3], weights=[60, 30, 10])[0]
            for _ in range(num_accounts):
                account_type = random.choices([1, 2, 3], weights=[50, 30, 20])[0]
                if account_type == 1:
                    balance = round(random.uniform(100, 500000), 2)
                elif account_type == 2:
                    balance = round(random.uniform(1000, 100000), 2)
                else:
                    balance = round(random.uniform(1000, 1000000), 2)

                open_time = datetime(2023, 1, 1) + timedelta(
                    days=random.randint(0, 729)
                )
                batch.append((user_id, account_type, balance, open_time))

            if len(batch) >= batch_size:
                self.cursor.executemany(
                    "INSERT INTO accounts (user_id, account_type, balance, open_time) VALUES (%s,%s,%s,%s)",
                    batch
                )
                self.conn.commit()
                self.account_count += len(batch)
                batch = []
                if self.account_count % 50000 == 0:
                    print(f"  已生成 {self.account_count} 个账户")

        if batch:
            self.cursor.executemany(
                "INSERT INTO accounts (user_id, account_type, balance, open_time) VALUES (%s,%s,%s,%s)",
                batch
            )
            self.conn.commit()
            self.account_count += len(batch)

        print(f"账户生成完成: {self.account_count}")

    def generate_transactions(self, days=90, fraud_rate=0.001):
        print(f"开始生成交易数据（{days}天）...")
        self.cursor.execute("SELECT account_id, user_id, account_type FROM accounts")
        accounts = self.cursor.fetchall()

        start_date = datetime(2024, 1, 1)
        batch_size = 10000
        batch = []

        for day in range(days):
            current_date = start_date + timedelta(days=day)
            is_weekend = current_date.weekday() >= 5

            daily_transactions = random.randint(500000, 700000)
            if is_weekend:
                daily_transactions = int(daily_transactions * 0.6)

            for _ in range(daily_transactions):
                account = random.choice(accounts)
                account_id, user_id, account_type = account
                city = self.user_city_map.get(user_id, '北京')

                is_fraud = random.random() < fraud_rate

                if is_fraud:
                    txn = self._generate_fraud_transaction(
                        account_id, user_id, current_date, city
                    )
                    self.fraud_count += 1
                else:
                    txn = self._generate_normal_transaction(
                        account_id, user_id, account_type, current_date, city, is_weekend
                    )

                batch.append(txn)

                if len(batch) >= batch_size:
                    self.cursor.executemany(
                        """INSERT INTO transactions
                           (account_id, transaction_type, amount, merchant,
                            transaction_time, ip, device_id, city, is_fraud, fraud_type)
                           VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                        batch
                    )
                    self.conn.commit()
                    self.transaction_count += len(batch)
                    batch = []

            if self.transaction_count % 1000000 < daily_transactions:
                print(f"  {current_date.strftime('%Y-%m-%d')}: 已生成 {self.transaction_count} 条交易, 欺诈 {self.fraud_count} 条")

        if batch:
            self.cursor.executemany(
                """INSERT INTO transactions
                   (account_id, transaction_type, amount, merchant,
                    transaction_time, ip, device_id, city, is_fraud, fraud_type)
                   VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                batch
            )
            self.conn.commit()
            self.transaction_count += len(batch)

        print(f"交易生成完成: 总计 {self.transaction_count}, 欺诈 {self.fraud_count}, 欺诈率 {self.fraud_count/self.transaction_count*100:.3f}%")

    def _generate_normal_transaction(self, account_id, user_id, account_type, date, city, is_weekend):
        hour = random.choices(range(24), weights=[
            1, 0.5, 0.3, 0.3, 0.3, 0.5, 2, 5, 8, 10, 12, 12,
            10, 8, 10, 12, 12, 10, 8, 6, 4, 3, 2, 1.5
        ])[0]

        if is_weekend:
            hour = random.choices(range(24), weights=[
                2, 1, 0.5, 0.5, 0.5, 1, 2, 3, 5, 8, 10, 12,
                12, 10, 10, 10, 12, 12, 10, 8, 6, 4, 3, 2
            ])[0]

        txn_time = date + timedelta(
            hours=hour,
            minutes=random.randint(0, 59),
            seconds=random.randint(0, 59)
        )

        txn_type = random.choices([1, 2, 3, 4], weights=[30, 50, 10, 10])[0]

        if txn_type == 2:
            amount = round(random.uniform(10, 5000), 2)
            merchant = random.choice(MERCHANTS[2])
        elif txn_type == 1:
            amount = round(random.uniform(100, 50000), 2)
            merchant = random.choice(MERCHANTS[1])
        elif txn_type == 3:
            amount = round(random.uniform(100, 20000), 2)
            merchant = None
        else:
            amount = round(random.uniform(100, 100000), 2)
            merchant = None

        device_id = generate_device_id(user_id)
        ip = generate_ip(city)

        return (account_id, txn_type, amount, merchant, txn_time, ip, device_id, city, 0, None)

    def _generate_fraud_transaction(self, account_id, user_id, date, home_city):
        fraud_type = random.choice(FRAUD_TYPES)

        if fraud_type == '盗刷':
            hour = random.choices([0, 1, 2, 3, 4, 5], weights=[3, 3, 3, 3, 2, 1])[0]
            amount = round(random.uniform(10000, 100000), 2)
            txn_type = 2
            merchant = random.choice(MERCHANTS[2])
            city = random.choice([c for c in CITIES if c != home_city])
        elif fraud_type == '套现':
            hour = random.randint(9, 17)
            amount = round(random.uniform(10000, 50000), 2)
            txn_type = 2
            merchant = random.choice(MERCHANTS[2])
            city = home_city
        elif fraud_type == '洗钱':
            hour = random.randint(0, 23)
            amount = round(random.uniform(50000, 500000), 2)
            txn_type = 1
            merchant = random.choice(MERCHANTS[1])
            city = random.choice(CITIES)
        elif fraud_type == '钓鱼':
            hour = random.randint(6, 22)
            amount = round(random.uniform(5000, 30000), 2)
            txn_type = 2
            merchant = random.choice(MERCHANTS[2])
            city = home_city
        else:
            hour = random.randint(0, 23)
            amount = round(random.uniform(1000, 50000), 2)
            txn_type = random.choice([1, 2])
            merchant = random.choice(MERCHANTS.get(txn_type, MERCHANTS[2]))
            city = random.choice(CITIES)

        txn_time = date + timedelta(
            hours=hour,
            minutes=random.randint(0, 59),
            seconds=random.randint(0, 59)
        )

        device_id = generate_device_id(user_id, is_fraud=True)
        ip = generate_ip(home_city, is_fraud=True)

        return (account_id, txn_type, amount, merchant, txn_time, ip, device_id, city, 1, fraud_type)

    def close(self):
        self.cursor.close()
        self.conn.close()


if __name__ == '__main__':
    gen = FinanceDataGenerator()
    gen.generate_users(count=1000000)
    gen.generate_accounts()
    gen.generate_transactions(days=90, fraud_rate=0.001)
    gen.close()
```

---

## 四、阶段2 - 实时风控管道（10h）

### 4.1 Kafka Topic设计

| Topic名称 | 数据内容 | 分区数 | 副本数 | Retention |
|-----------|----------|--------|--------|-----------|
| finance.transactions | 交易事件 | 12 | 3 | 72h |
| finance.risk-decisions | 风控决策结果 | 6 | 3 | 168h |
| finance.fraud-alerts | 欺诈告警 | 6 | 3 | 168h |

### 4.2 Flink实时特征计算

```java
package com.example.finance.risk;

import org.apache.flink.api.common.eventtime.WatermarkStrategy;
import org.apache.flink.api.common.state.ValueState;
import org.apache.flink.api.common.state.ValueStateDescriptor;
import org.apache.flink.api.common.state.ListState;
import org.apache.flink.api.common.state.ListStateDescriptor;
import org.apache.flink.api.common.time.Time;
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

import java.time.Duration;
import java.util.ArrayList;
import java.util.List;
import java.util.Properties;

public class RealTimeRiskEngine {

    public static void main(String[] args) throws Exception {
        StreamExecutionEnvironment env =
            StreamExecutionEnvironment.getExecutionEnvironment();

        env.enableCheckpointing(60000);
        env.getCheckpointConfig().setCheckpointTimeout(120000);

        Properties kafkaProps = new Properties();
        kafkaProps.setProperty("bootstrap.servers", "localhost:9092");
        kafkaProps.setProperty("group.id", "risk-engine-group");
        kafkaProps.setProperty("auto.offset.reset", "latest");

        FlinkKafkaConsumer<String> source = new FlinkKafkaConsumer<>(
            "finance.transactions",
            new SimpleStringSchema(),
            kafkaProps
        );

        DataStream<TransactionEvent> transactionStream = env.addSource(source)
            .map(line -> JSON.parseObject(line, TransactionEvent.class))
            .assignTimestampsAndWatermarks(
                WatermarkStrategy
                    .<TransactionEvent>forBoundedOutOfOrderness(Duration.ofSeconds(5))
                    .withTimestampAssigner((event, ts) -> event.transactionTime)
            );

        DataStream<RiskDecision> riskDecisions = transactionStream
            .keyBy(TransactionEvent::getAccountId)
            .process(new RiskRuleEngineFunction());

        DataStream<String> decisionJson = riskDecisions
            .map(decision -> JSON.toJSONString(decision));

        FlinkKafkaProducer<String> sink = new FlinkKafkaProducer<>(
            "finance.risk-decisions",
            new SimpleStringSchema(),
            kafkaProps
        );

        decisionJson.addSink(sink);

        env.execute("Finance Real-Time Risk Engine");
    }

    static class RiskRuleEngineFunction
            extends KeyedProcessFunction<Long, TransactionEvent, RiskDecision> {

        private ValueState<Long> lastTransactionTime;
        private ListState<TransactionEvent> recentTransactions;
        private ValueState<String> lastCity;
        private ValueState<Long> lastCityTime;
        private ValueState<String> lastDevice;
        private ValueState<Integer> transactionCount1h;

        @Override
        public void open(Configuration parameters) {
            lastTransactionTime = getRuntimeContext().getState(
                new ValueStateDescriptor<>("lastTxnTime", Long.class));
            recentTransactions = getRuntimeContext().getListState(
                new ListStateDescriptor<>("recentTxns", TransactionEvent.class));
            lastCity = getRuntimeContext().getState(
                new ValueStateDescriptor<>("lastCity", String.class));
            lastCityTime = getRuntimeContext().getState(
                new ValueStateDescriptor<>("lastCityTime", Long.class));
            lastDevice = getRuntimeContext().getState(
                new ValueStateDescriptor<>("lastDevice", String.class));
            transactionCount1h = getRuntimeContext().getState(
                new ValueStateDescriptor<>("txnCount1h", Integer.class));
        }

        @Override
        public void processElement(
                TransactionEvent event,
                KeyedProcessFunction<Long, TransactionEvent, RiskDecision>.Context ctx,
                Collector<RiskDecision> out) throws Exception {

            List<String> hitRules = new ArrayList<>();
            int riskScore = 0;

            if (event.amount > 50000) {
                hitRules.add("RULE_01:单笔金额>5万");
                riskScore += 40;
            }

            long oneHourAgo = event.transactionTime - 3600000L;
            List<TransactionEvent> validTxns = new ArrayList<>();
            int count1h = 0;
            for (TransactionEvent txn : recentTransactions.get()) {
                if (txn.transactionTime > oneHourAgo) {
                    validTxns.add(txn);
                    count1h++;
                }
            }
            recentTransactions.update(validTxns);

            if (count1h > 10) {
                hitRules.add("RULE_02:1小时内交易>10次");
                riskScore += 30;
            }

            int hour = new java.util.Date(event.transactionTime).getHours();
            if (hour >= 2 && hour <= 5 && event.amount > 10000) {
                hitRules.add("RULE_03:凌晨2-5点大额消费");
                riskScore += 25;
            }

            String prevCity = lastCity.value();
            Long prevCityTime = lastCityTime.value();
            if (prevCity != null && !prevCity.equals(event.city) && prevCityTime != null) {
                long hoursDiff = (event.transactionTime - prevCityTime) / 3600000L;
                if (hoursDiff < 2) {
                    hitRules.add("RULE_04:2小时内异地消费");
                    riskScore += 45;
                }
            }

            String prevDevice = lastDevice.value();
            if (prevDevice != null && !prevDevice.equals(event.deviceId) && event.amount > 10000) {
                hitRules.add("RULE_05:新设备首次大额消费");
                riskScore += 25;
            }

            riskScore = Math.min(riskScore, 100);

            String riskLevel;
            String action;
            if (riskScore >= 60) {
                riskLevel = "HIGH";
                action = "BLOCK";
            } else if (riskScore >= 30) {
                riskLevel = "MEDIUM";
                action = "VERIFY";
            } else {
                riskLevel = "LOW";
                action = "PASS";
            }

            RiskDecision decision = new RiskDecision();
            decision.transactionId = event.transactionId;
            decision.accountId = event.accountId;
            decision.riskLevel = riskLevel;
            decision.riskScore = riskScore;
            decision.ruleHits = String.join(";", hitRules);
            decision.action = action;
            decision.decisionTime = System.currentTimeMillis();

            out.collect(decision);

            recentTransactions.add(event);
            lastCity.update(event.city);
            lastCityTime.update(event.transactionTime);
            lastDevice.update(event.deviceId);
        }
    }

    static class TransactionEvent {
        public Long transactionId;
        public Long accountId;
        public Integer transactionType;
        public Double amount;
        public String merchant;
        public Long transactionTime;
        public String ip;
        public String deviceId;
        public String city;

        public Long getAccountId() { return accountId; }
    }

    static class RiskDecision {
        public Long transactionId;
        public Long accountId;
        public String riskLevel;
        public Integer riskScore;
        public String ruleHits;
        public String action;
        public Long decisionTime;
    }
}
```

### 4.3 Flink SQL实时特征聚合

```sql
-- Flink SQL: 实时风控特征计算

-- 1. Kafka源表
CREATE TABLE kafka_transactions (
    transaction_id BIGINT,
    account_id BIGINT,
    transaction_type INT,
    amount DECIMAL(20, 2),
    merchant STRING,
    transaction_time TIMESTAMP(3),
    ip STRING,
    device_id STRING,
    city STRING,
    is_fraud INT,
    WATERMARK FOR transaction_time AS transaction_time - INTERVAL '5' SECOND
) WITH (
    'connector' = 'kafka',
    'topic' = 'finance.transactions',
    'properties.bootstrap.servers' = 'localhost:9092',
    'properties.group.id' = 'risk-feature-group',
    'format' = 'json',
    'scan.startup.mode' = 'latest-offset'
);

-- 2. 滑动窗口统计: 最近1小时交易次数和金额
CREATE VIEW account_stats_1h AS
SELECT
    account_id,
    HOP_START(transaction_time, INTERVAL '5' MINUTE, INTERVAL '1' HOUR) AS window_start,
    HOP_END(transaction_time, INTERVAL '5' MINUTE, INTERVAL '1' HOUR) AS window_end,
    COUNT(*) AS txn_count,
    SUM(amount) AS total_amount,
    MAX(amount) AS max_amount,
    COUNT(DISTINCT city) AS city_count,
    COUNT(DISTINCT device_id) AS device_count
FROM kafka_transactions
GROUP BY
    account_id,
    HOP(transaction_time, INTERVAL '5' MINUTE, INTERVAL '1' HOUR);

-- 3. 滑动窗口统计: 最近6小时
CREATE VIEW account_stats_6h AS
SELECT
    account_id,
    HOP_START(transaction_time, INTERVAL '30' MINUTE, INTERVAL '6' HOUR) AS window_start,
    HOP_END(transaction_time, INTERVAL '30' MINUTE, INTERVAL '6' HOUR) AS window_end,
    COUNT(*) AS txn_count,
    SUM(amount) AS total_amount,
    COUNT(DISTINCT merchant) AS merchant_count
FROM kafka_transactions
GROUP BY
    account_id,
    HOP(transaction_time, INTERVAL '30' MINUTE, INTERVAL '6' HOUR);

-- 4. 实时异常检测输出到Kafka
CREATE TABLE kafka_risk_features (
    account_id BIGINT,
    window_start TIMESTAMP(3),
    window_end TIMESTAMP(3),
    txn_count BIGINT,
    total_amount DECIMAL(20, 2),
    max_amount DECIMAL(20, 2),
    city_count BIGINT,
    device_count BIGINT,
    PRIMARY KEY (account_id, window_start) NOT ENFORCED
) WITH (
    'connector' = 'upsert-kafka',
    'topic' = 'finance.risk-features',
    'properties.bootstrap.servers' = 'localhost:9092',
    'key.format' = 'json',
    'value.format' = 'json'
);

INSERT INTO kafka_risk_features
SELECT account_id, window_start, window_end,
       txn_count, total_amount, max_amount, city_count, device_count
FROM account_stats_1h;
```

### 4.4 Redis实时特征服务

```python
"""
redis_feature_service.py

Redis实时特征缓存服务
供风控引擎实时查询账户特征
"""
import redis
import json
from datetime import datetime

r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

ACCOUNT_FEATURE_PREFIX = "risk:account:"
DEVICE_ACCOUNT_PREFIX = "risk:device:"
IP_ACCOUNT_PREFIX = "risk:ip:"


def update_account_features(account_id, features):
    key = f"{ACCOUNT_FEATURE_PREFIX}{account_id}"
    pipe = r.pipeline()
    pipe.hset(key, mapping={
        'txn_count_1h': features.get('txn_count_1h', 0),
        'total_amount_1h': features.get('total_amount_1h', 0),
        'max_amount_1h': features.get('max_amount_1h', 0),
        'city_count_1h': features.get('city_count_1h', 0),
        'device_count_1h': features.get('device_count_1h', 0),
        'txn_count_6h': features.get('txn_count_6h', 0),
        'total_amount_6h': features.get('total_amount_6h', 0),
        'last_city': features.get('last_city', ''),
        'last_device': features.get('last_device', ''),
        'last_txn_time': features.get('last_txn_time', ''),
        'risk_score': features.get('risk_score', 0),
        'risk_level': features.get('risk_level', 'LOW'),
    })
    pipe.expire(key, 86400)
    pipe.execute()


def update_device_account(device_id, account_id):
    key = f"{DEVICE_ACCOUNT_PREFIX}{device_id}"
    r.sadd(key, str(account_id))
    r.expire(key, 604800)


def update_ip_account(ip, account_id):
    key = f"{IP_ACCOUNT_PREFIX}{ip}"
    r.sadd(key, str(account_id))
    r.expire(key, 604800)


def get_account_features(account_id):
    key = f"{ACCOUNT_FEATURE_PREFIX}{account_id}"
    data = r.hgetall(key)
    if not data:
        return None
    return {
        'txn_count_1h': int(data.get('txn_count_1h', 0)),
        'total_amount_1h': float(data.get('total_amount_1h', 0)),
        'max_amount_1h': float(data.get('max_amount_1h', 0)),
        'city_count_1h': int(data.get('city_count_1h', 0)),
        'device_count_1h': int(data.get('device_count_1h', 0)),
        'last_city': data.get('last_city', ''),
        'last_device': data.get('last_device', ''),
        'risk_score': int(data.get('risk_score', 0)),
        'risk_level': data.get('risk_level', 'LOW'),
    }


def get_device_accounts(device_id):
    key = f"{DEVICE_ACCOUNT_PREFIX}{device_id}"
    members = r.smembers(key)
    return [int(m) for m in members]


def get_ip_accounts(ip):
    key = f"{IP_ACCOUNT_PREFIX}{ip}"
    members = r.smembers(key)
    return [int(m) for m in members]


def get_high_risk_accounts(top_n=10):
    pattern = f"{ACCOUNT_FEATURE_PREFIX}*"
    accounts = []
    for key in r.scan_iter(match=pattern):
        account_id = key.replace(ACCOUNT_FEATURE_PREFIX, '')
        risk_score = r.hget(key, 'risk_score')
        risk_level = r.hget(key, 'risk_level')
        if risk_level in ('HIGH', 'MEDIUM'):
            accounts.append({
                'account_id': int(account_id),
                'risk_score': int(risk_score or 0),
                'risk_level': risk_level
            })
    accounts.sort(key=lambda x: x['risk_score'], reverse=True)
    return accounts[:top_n]
```

### 4.5 ClickHouse风控数据存储

```sql
-- ============================================
-- ClickHouse 风控数据存储 DDL
-- ============================================

CREATE TABLE risk_decisions_realtime ON CLUSTER default (
    transaction_id UInt64,
    account_id UInt64,
    risk_level String,
    risk_score UInt8,
    rule_hits String,
    action String,
    decision_time DateTime64(3),
    amount Decimal(20, 2),
    transaction_type UInt8,
    city String,
    device_id String,
    ip String,
    is_fraud UInt8 DEFAULT 0,
    create_time DateTime64(3) DEFAULT now64(),
    INDEX idx_account account_id TYPE bloom_filter GRANULARITY 1,
    INDEX idx_risk_level risk_level TYPE set(3) GRANULARITY 1,
    INDEX idx_action action TYPE set(3) GRANULARITY 1
) ENGINE = ReplicatedMergeTree(
    '/clickhouse/tables/{shard}/risk_decisions_realtime',
    '{replica}'
)
PARTITION BY toYYYYMMDD(decision_time)
ORDER BY (decision_time, account_id, transaction_id)
TTL decision_time + INTERVAL 30 DAY
SETTINGS index_granularity = 8192;

CREATE TABLE risk_stats_minute ON CLUSTER default (
    window_start DateTime64(3),
    window_end DateTime64(3),
    total_transactions UInt64,
    blocked_count UInt64,
    verified_count UInt64,
    passed_count UInt64,
    fraud_detected UInt64,
    block_rate Float64,
    fraud_rate Float64,
    avg_risk_score Float64
) ENGINE = ReplicatedSummingMergeTree(
    '/clickhouse/tables/{shard}/risk_stats_minute',
    '{replica}',
    (total_transactions, blocked_count, verified_count, passed_count, fraud_detected)
)
PARTITION BY toYYYYMM(window_start)
ORDER BY (window_start)
TTL window_start + INTERVAL 90 DAY
SETTINGS index_granularity = 8192;

CREATE MATERIALIZED VIEW risk_stats_mv ON CLUSTER default
ENGINE = SummingMergeTree()
PARTITION BY toYYYYMM(window_start)
ORDER BY (window_start, risk_level)
AS SELECT
    toStartOfMinute(decision_time) AS window_start,
    risk_level,
    count() AS total_transactions,
    sum(if(action = 'BLOCK', 1, 0)) AS blocked_count,
    sum(if(action = 'VERIFY', 1, 0)) AS verified_count,
    sum(if(action = 'PASS', 1, 0)) AS passed_count,
    sum(is_fraud) AS fraud_detected,
    avg(risk_score) AS avg_risk_score
FROM risk_decisions_realtime
GROUP BY window_start, risk_level;

CREATE TABLE fraud_analysis_daily ON CLUSTER default (
    stat_date Date,
    fraud_type String,
    fraud_count UInt64,
    total_amount Decimal(20, 2),
    detected_count UInt64,
    missed_count UInt64,
    precision_rate Float64,
    recall_rate Float64,
    f1_score Float64
) ENGINE = ReplicatedMergeTree(
    '/clickhouse/tables/{shard}/fraud_analysis_daily',
    '{replica}'
)
PARTITION BY toYYYYMM(stat_date)
ORDER BY (stat_date, fraud_type)
TTL stat_date + INTERVAL 180 DAY;
```

---

## 五、阶段3 - 图风控（8h）

### 5.1 Neo4j交易关联图构建

```cypher
// ============================================
// Neo4j 图风控 - 数据模型与索引
// ============================================

// 创建索引
CREATE CONSTRAINT FOR (a:Account) REQUIRE a.account_id IS UNIQUE;
CREATE CONSTRAINT FOR (d:Device) REQUIRE d.device_id IS UNIQUE;
CREATE CONSTRAINT FOR (i:IP) REQUIRE i.ip IS UNIQUE;
CREATE CONSTRAINT FOR (m:Merchant) REQUIRE m.name IS UNIQUE;

// 导入账户节点
LOAD CSV WITH HEADERS FROM 'file:///accounts.csv' AS row
CREATE (:Account {
    account_id: toInteger(row.account_id),
    user_id: toInteger(row.user_id),
    account_type: toInteger(row.account_type),
    risk_level: 0
});

// 导入设备节点
LOAD CSV WITH HEADERS FROM 'file:///devices.csv' AS row
CREATE (:Device {
    device_id: row.device_id,
    device_type: row.device_type
});

// 导入IP节点
LOAD CSV WITH HEADERS FROM 'file:///ips.csv' AS row
CREATE (:IP {
    ip: row.ip,
    city: row.city
});

// 导入商户节点
LOAD CSV WITH HEADERS FROM 'file:///merchants.csv' AS row
CREATE (:Merchant {
    name: row.merchant,
    category: row.category
});

// 创建交易关系
LOAD CSV WITH HEADERS FROM 'file:///transactions.csv' AS row
MATCH (a:Account {account_id: toInteger(row.account_id)})
MATCH (d:Device {device_id: row.device_id})
MATCH (i:IP {ip: row.ip})
MATCH (m:Merchant {name: row.merchant})
CREATE (a)-[:TRANSACTED {
    transaction_id: toInteger(row.transaction_id),
    amount: toFloat(row.amount),
    txn_time: datetime(row.transaction_time),
    is_fraud: toInteger(row.is_fraud)
}]->(m)
CREATE (a)-[:USED_DEVICE {txn_time: datetime(row.transaction_time)}]->(d)
CREATE (a)-[:USED_IP {txn_time: datetime(row.transaction_time)}]->(i);

// 创建共用设备关系（同设备不同账户）
MATCH (d:Device)<-[:USED_DEVICE]-(a1:Account)
MATCH (d:Device)<-[:USED_DEVICE]-(a2:Account)
WHERE a1.account_id < a2.account_id
MERGE (a1)-[:SHARED_DEVICE {device_id: d.device_id}]-(a2);

// 创建共用IP关系
MATCH (i:IP)<-[:USED_IP]-(a1:Account)
MATCH (i:IP)<-[:USED_IP]-(a2:Account)
WHERE a1.account_id < a2.account_id
MERGE (a1)-[:SHARED_IP {ip: i.ip}]-(a2);
```

### 5.2 图算法检测

```cypher
// ============================================
// 图算法检测 - 欺诈模式识别
// ============================================

// 1. 团伙欺诈: 社区发现(Louvain算法)
// 需要安装APOC和GDS插件
CALL gds.graph.project(
    'fraud_network',
    ['Account', 'Device', 'IP'],
    {
        SHARED_DEVICE: {orientation: 'UNDIRECTED'},
        SHARED_IP: {orientation: 'UNDIRECTED'}
    }
);

CALL gds.louvain.write('fraud_network', {
    writeProperty: 'communityId'
});

MATCH (a:Account)
WHERE a.communityId IS NOT NULL
WITH a.communityId AS community, collect(a) AS members, count(*) AS size
WHERE size >= 3
RETURN community, size,
       [m IN members | m.account_id] AS account_ids,
       [m IN members WHERE m.risk_level >= 2 | m.account_id] AS high_risk_accounts
ORDER BY size DESC
LIMIT 20;

// 2. 异常中心度: PageRank识别关键节点
CALL gds.pageRank.write('fraud_network', {
    writeProperty: 'pagerank'
});

MATCH (a:Account)
WHERE a.pagerank IS NOT NULL
RETURN a.account_id, a.pagerank, a.risk_level
ORDER BY a.pagerank DESC
LIMIT 20;

// 高PageRank + 高风险 = 欺诈核心节点
MATCH (a:Account)
WHERE a.pagerank > 1.5 AND a.risk_level >= 2
SET a.risk_level = 3;

// 3. 资金环路检测: 环形转账
MATCH path = (a1:Account)-[:TRANSACTED*2..5]->(a1)
WHERE ALL(r IN relationships(path) WHERE r.amount > 10000)
RETURN [n IN nodes(path) | n.account_id] AS ring_accounts,
       [r IN relationships(path) | r.amount] AS amounts,
       length(path) AS ring_length
LIMIT 50;

// 4. 共用设备/IP的欺诈关联
MATCH (fraud_account:Account {risk_level: 3})-[:SHARED_DEVICE]-(suspicious:Account)
WHERE suspicious.risk_level < 3
SET suspicious.risk_level = suspicious.risk_level + 1
RETURN fraud_account.account_id, suspicious.account_id, suspicious.risk_level;

MATCH (fraud_account:Account {risk_level: 3})-[:SHARED_IP]-(suspicious:Account)
WHERE suspicious.risk_level < 3
SET suspicious.risk_level = suspicious.risk_level + 1
RETURN fraud_account.account_id, suspicious.account_id, suspicious.risk_level;

// 5. 查询某账户的关联网络（深度2）
MATCH (center:Account {account_id: 12345})-[:SHARED_DEVICE|SHARED_IP*1..2]-(connected:Account)
RETURN center, connected,
       length(shortestPath((center)-[:SHARED_DEVICE|SHARED_IP*]-(connected))) AS distance;

// 清理图投影
CALL gds.graph.drop('fraud_network');
```

### 5.3 Spark批量图计算

```python
"""
spark_graph_risk.py

Spark批量图计算 - 每日构建全量交易图
计算图特征写入Redis供实时使用
"""
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, countDistinct, sum, avg, max as spark_max, collect_list
from graphframes import GraphFrame

spark = SparkSession.builder \
    .appName("FinanceGraphRisk") \
    .config("spark.jars.packages", "graphframes:graphframes:0.8.3-spark3.5-s_2.12") \
    .enableHiveSupport() \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")


def build_transaction_graph():
    print("=== 构建交易关联图 ===")

    transactions = spark.sql("""
        SELECT account_id, device_id, ip, merchant, amount,
               transaction_time, is_fraud
        FROM finance_risk.transactions
        WHERE transaction_time >= date_sub(current_date(), 30)
    """)

    account_vertices = transactions.select(
        col("account_id").alias("id")
    ).distinct().withColumn("type", col("id") * 0 + 1)

    device_vertices = transactions.select(
        col("device_id").alias("id")
    ).distinct().withColumn("type", col("id") * 0 + 2)

    ip_vertices = transactions.select(
        col("ip").alias("id")
    ).distinct().withColumn("type", col("id") * 0 + 3)

    vertices = account_vertices.unionByName(device_vertices).unionByName(ip_vertices)

    account_device_edges = transactions.select(
        col("account_id").alias("src"),
        col("device_id").alias("dst"),
        col("amount").alias("weight")
    ).groupBy("src", "dst").agg(
        count("*").alias("weight")
    ).withColumn("relationship", col("weight") * 0 + 1)

    account_ip_edges = transactions.select(
        col("account_id").alias("src"),
        col("ip").alias("dst"),
        col("amount").alias("weight")
    ).groupBy("src", "dst").agg(
        count("*").alias("weight")
    ).withColumn("relationship", col("weight") * 0 + 2)

    edges = account_device_edges.unionByName(account_ip_edges)

    g = GraphFrame(vertices, edges)

    return g, account_vertices


def compute_page_rank(g):
    print("=== 计算PageRank ===")
    pr = g.pageRank(resetProbability=0.15, maxIter=20)
    return pr.vertices.select("id", "pagerank")


def compute_connected_components(g, account_vertices):
    print("=== 计算连通分量（团伙检测）===")
    cc = g.connectedComponents(algorithm="graphx", checkpointInterval=2)
    account_cc = cc.join(account_vertices, cc.id == account_vertices.id) \
        .select(cc.id.alias("account_id"), "component")
    return account_cc


def compute_triangle_count(g):
    print("=== 计算三角形计数 ===")
    tc = g.triangleCount()
    return tc.select("id", "count")


def compute_graph_features():
    g, account_vertices = build_transaction_graph()

    page_rank_df = compute_page_rank(g)
    cc_df = compute_connected_components(g, account_vertices)
    triangle_df = compute_triangle_count(g)

    account_features = account_vertices \
        .join(page_rank_df, account_vertices.id == page_rank_df.id, "left") \
        .join(cc_df, account_vertices.id == cc_df.account_id, "left") \
        .join(triangle_df, account_vertices.id == triangle_df.id, "left") \
        .select(
            account_vertices.id.alias("account_id"),
            col("pagerank").alias("graph_pagerank"),
            col("component").alias("graph_community"),
            col("count").alias("graph_triangle_count")
        )

    account_features.cache()
    print(f"图特征计算完成，账户数: {account_features.count()}")

    return account_features


def write_features_to_redis(features_df):
    print("=== 写入Redis ===")
    import redis

    r = redis.Redis(host='localhost', port=6379, db=1, decode_responses=True)
    GRAPH_FEATURE_PREFIX = "risk:graph:"

    collected = features_df.collect()
    pipe = r.pipeline()

    for row in collected:
        key = f"{GRAPH_FEATURE_PREFIX}{row.account_id}"
        pipe.hset(key, mapping={
            'pagerank': str(row.graph_pagerank or 0),
            'community': str(row.graph_community or 0),
            'triangle_count': str(row.graph_triangle_count or 0)
        })
        pipe.expire(key, 86400)

    pipe.execute()
    print(f"已写入 {len(collected)} 个账户的图特征到Redis")


def detect_fraud_communities(cc_df):
    print("=== 检测欺诈团伙 ===")

    community_stats = cc_df.groupBy("component").agg(
        count("*").alias("member_count"),
        collect_list("account_id").alias("account_ids")
    ).filter(col("member_count") >= 3)

    community_stats.show(20, truncate=False)
    return community_stats


if __name__ == "__main__":
    features = compute_graph_features()
    write_features_to_redis(features)

    g, account_vertices = build_transaction_graph()
    cc_df = compute_connected_components(g, account_vertices)
    detect_fraud_communities(cc_df)

    spark.stop()
```

---

## 六、阶段4 - 监控与报告（7h）

### 6.1 Grafana风控大屏

```json
{
  "dashboard": {
    "title": "金融实时风控大屏",
    "refresh": "5s",
    "panels": [
      {
        "title": "实时交易量",
        "type": "stat",
        "targets": [{
          "rawSql": "SELECT count() AS total FROM risk_decisions_realtime WHERE decision_time >= now() - INTERVAL 1 MINUTE",
          "format": "table"
        }],
        "fieldConfig": {
          "defaults": {
            "unit": "short",
            "color": {"mode": "thresholds"},
            "thresholds": {
              "steps": [
                {"color": "green", "value": null},
                {"color": "yellow", "value": 5000},
                {"color": "red", "value": 10000}
              ]
            }
          }
        }
      },
      {
        "title": "拦截率",
        "type": "gauge",
        "targets": [{
          "rawSql": "SELECT sum(if(action = 'BLOCK', 1, 0)) / count() * 100 AS block_rate FROM risk_decisions_realtime WHERE decision_time >= now() - INTERVAL 5 MINUTE",
          "format": "table"
        }],
        "fieldConfig": {
          "defaults": {
            "unit": "percent",
            "min": 0,
            "max": 10,
            "thresholds": {
              "steps": [
                {"color": "green", "value": null},
                {"color": "yellow", "value": 2},
                {"color": "red", "value": 5}
              ]
            }
          }
        }
      },
      {
        "title": "风险等级分布",
        "type": "piechart",
        "targets": [{
          "rawSql": "SELECT risk_level, count() AS cnt FROM risk_decisions_realtime WHERE decision_time >= now() - INTERVAL 5 MINUTE GROUP BY risk_level ORDER BY cnt DESC",
          "format": "table"
        }]
      },
      {
        "title": "欺诈类型分布",
        "type": "barchart",
        "targets": [{
          "rawSql": "SELECT rule_hits, count() AS cnt FROM risk_decisions_realtime WHERE is_fraud = 1 AND decision_time >= now() - INTERVAL 1 HOUR GROUP BY rule_hits ORDER BY cnt DESC LIMIT 10",
          "format": "table"
        }]
      },
      {
        "title": "高风险账户TOP10",
        "type": "table",
        "targets": [{
          "rawSql": "SELECT account_id, count() AS fraud_count, sum(amount) AS fraud_amount, max(risk_score) AS max_score FROM risk_decisions_realtime WHERE risk_level = 'HIGH' AND decision_time >= now() - INTERVAL 1 HOUR GROUP BY account_id ORDER BY fraud_count DESC LIMIT 10",
          "format": "table"
        }]
      },
      {
        "title": "实时交易趋势",
        "type": "timeseries",
        "targets": [{
          "rawSql": "SELECT toStartOfMinute(decision_time) AS time, count() AS total, sum(if(action = 'BLOCK', 1, 0)) AS blocked, sum(if(is_fraud = 1, 1, 0)) AS fraud FROM risk_decisions_realtime WHERE decision_time >= now() - INTERVAL 1 HOUR GROUP BY time ORDER BY time",
          "format": "time_series"
        }]
      },
      {
        "title": "规则命中统计",
        "type": "bargauge",
        "targets": [{
          "rawSql": "SELECT rule_hits, count() AS hit_count FROM risk_decisions_realtime WHERE rule_hits != '' AND decision_time >= now() - INTERVAL 1 HOUR GROUP BY rule_hits ORDER BY hit_count DESC LIMIT 10",
          "format": "table"
        }]
      },
      {
        "title": "误报率趋势",
        "type": "timeseries",
        "targets": [{
          "rawSql": "SELECT toStartOfMinute(decision_time) AS time, sum(if(action = 'BLOCK' AND is_fraud = 0, 1, 0)) / nullIf(sum(if(action = 'BLOCK', 1, 0)), 0) * 100 AS false_positive_rate FROM risk_decisions_realtime WHERE decision_time >= now() - INTERVAL 1 HOUR GROUP BY time ORDER BY time",
          "format": "time_series"
        }],
        "fieldConfig": {
          "defaults": {
            "unit": "percent"
          }
        }
      }
    ]
  }
}
```

### 6.2 风控效果评估脚本

```python
"""
risk_evaluation.py

风控规则效果评估
计算精确率/召回率/F1
分析误报和漏报
"""
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, sum as spark_sum, when, lit, avg
from pyspark.sql.window import Window

spark = SparkSession.builder \
    .appName("RiskEvaluation") \
    .enableHiveSupport() \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")


def evaluate_rules():
    print("=== 风控规则效果评估 ===")

    decisions = spark.sql("""
        SELECT d.transaction_id, d.account_id, d.risk_level, d.risk_score,
               d.rule_hits, d.action, d.decision_time,
               t.is_fraud, t.fraud_type, t.amount
        FROM finance_risk.risk_decisions d
        JOIN finance_risk.transactions t ON d.transaction_id = t.transaction_id
        WHERE d.decision_time >= date_sub(current_date(), 1)
    """)

    decisions.cache()
    total = decisions.count()
    fraud_total = decisions.filter(col("is_fraud") == 1).count()
    normal_total = decisions.filter(col("is_fraud") == 0).count()

    print(f"总交易: {total}")
    print(f"欺诈交易: {fraud_total} ({fraud_total/total*100:.3f}%)")
    print(f"正常交易: {normal_total}")

    blocked = decisions.filter(col("action") == "BLOCK")
    tp = blocked.filter(col("is_fraud") == 1).count()
    fp = blocked.filter(col("is_fraud") == 0).count()

    not_blocked = decisions.filter(col("action") != "BLOCK")
    fn = not_blocked.filter(col("is_fraud") == 1).count()
    tn = not_blocked.filter(col("is_fraud") == 0).count()

    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0

    print(f"\n=== 整体效果 ===")
    print(f"精确率(Precision): {precision:.4f}")
    print(f"召回率(Recall):    {recall:.4f}")
    print(f"F1分数:            {f1:.4f}")
    print(f"误报数(FP):        {fp}")
    print(f"漏报数(FN):        {fn}")

    print(f"\n=== 混淆矩阵 ===")
    print(f"              预测欺诈    预测正常")
    print(f"  实际欺诈    {tp:<12}{fn:<12}")
    print(f"  实际正常    {fp:<12}{tn:<12}")

    return decisions, precision, recall, f1


def evaluate_by_rule(decisions):
    print("\n=== 各规则效果评估 ===")

    rules = [
        ("RULE_01", "单笔金额>5万"),
        ("RULE_02", "1小时内交易>10次"),
        ("RULE_03", "凌晨2-5点大额消费"),
        ("RULE_04", "2小时内异地消费"),
        ("RULE_05", "新设备首次大额消费"),
    ]

    for rule_code, rule_name in rules:
        rule_decisions = decisions.filter(col("rule_hits").contains(rule_code))
        rule_total = rule_decisions.count()
        if rule_total == 0:
            continue

        rule_fraud = rule_decisions.filter(col("is_fraud") == 1).count()
        rule_precision = rule_fraud / rule_total

        all_fraud = decisions.filter(col("is_fraud") == 1).count()
        rule_recall = rule_fraud / all_fraud if all_fraud > 0 else 0

        print(f"  {rule_name}: 命中{rule_total}次, 精确率={rule_precision:.4f}, 召回率={rule_recall:.4f}")


def analyze_false_positives(decisions):
    print("\n=== 误报分析（被拦截的正常交易）===")

    false_positives = decisions.filter(
        (col("action") == "BLOCK") & (col("is_fraud") == 0)
    )

    fp_by_rule = false_positives.groupBy("rule_hits").agg(
        count("*").alias("fp_count"),
        avg("amount").alias("avg_amount"),
        spark_sum("amount").alias("total_amount")
    ).orderBy(col("fp_count").desc())

    fp_by_rule.show(20, truncate=False)

    fp_by_hour = false_positives.withColumn(
        "hour", col("decision_time").substr(12, 2).cast("int")
    ).groupBy("hour").agg(
        count("*").alias("fp_count")
    ).orderBy("hour")

    fp_by_hour.show(24, truncate=False)


def analyze_false_negatives(decisions):
    print("\n=== 漏报分析（未被拦截的欺诈交易）===")

    false_negatives = decisions.filter(
        (col("action") != "BLOCK") & (col("is_fraud") == 1)
    )

    fn_by_type = false_negatives.groupBy("fraud_type").agg(
        count("*").alias("fn_count"),
        avg("amount").alias("avg_amount"),
        spark_sum("amount").alias("total_amount")
    ).orderBy(col("fn_count").desc())

    fn_by_type.show(20, truncate=False)

    fn_by_action = false_negatives.groupBy("action").agg(
        count("*").alias("fn_count")
    )
    fn_by_action.show()


def generate_daily_report():
    decisions, precision, recall, f1 = evaluate_rules()
    evaluate_by_rule(decisions)
    analyze_false_positives(decisions)
    analyze_false_negatives(decisions)

    print("\n=== 评估完成 ===")


if __name__ == "__main__":
    generate_daily_report()
    spark.stop()
```

### 6.3 Docker Compose部署

```yaml
# docker-compose-finance-risk.yml
version: '3.8'

services:
  zookeeper:
    image: confluentinc/cp-zookeeper:7.5.0
    environment:
      ZOOKEEPER_CLIENT_PORT: 2181
    ports:
      - "2181:2181"

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
      MYSQL_DATABASE: finance_risk
    command:
      - --default-authentication-plugin=mysql_native_password
      - --binlog-format=ROW
      - --binlog-row-image=FULL
      - --server-id=1
      - --log-bin=mysql-bin
    volumes:
      - ./sql:/docker-entrypoint-initdb.d

  redis:
    image: redis:7.2
    ports:
      - "6379:6379"
    command: redis-server --maxmemory 2gb --maxmemory-policy allkeys-lru

  neo4j:
    image: neo4j:5.13
    ports:
      - "7474:7474"
      - "7687:7687"
    environment:
      NEO4J_AUTH: neo4j/risk12345
      NEO4J_PLUGINS: '["apoc", "graph-data-science"]'
      NEO4J_server_memory_heap_max__size: 2G
    volumes:
      - neo4j_data:/data
      - neo4j_import:/var/lib/neo4j/import

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
      GF_INSTALL_PLUGINS: vertamedia-clickhouse-datasource,neo4j-datasource
    volumes:
      - ./grafana/dashboards:/etc/grafana/provisioning/dashboards
      - ./grafana/datasources:/etc/grafana/provisioning/datasources

volumes:
  neo4j_data:
  neo4j_import:
```

---

## 七、验收标准

| 验收项 | 标准 | 验证方法 |
|--------|------|----------|
| 数据模拟 | 100万账户+5000万交易生成完成 | `SELECT COUNT(*) FROM transactions` |
| 实时风控延迟 | 交易到风控决策 < 500ms | Flink UI Metrics |
| 规则命中率 | 5条规则均可触发 | 注入欺诈交易验证 |
| 图风控 | Neo4j社区发现+PageRank可执行 | Cypher查询验证 |
| Redis特征 | 实时特征可查询 | `redis-cli HGETALL` |
| ClickHouse | 风控数据实时写入可查 | SQL查询验证 |
| Grafana大屏 | 所有面板实时刷新 | 目视检查 |
| 效果评估 | 精确率>80% 召回率>70% | 评估脚本输出 |

---

## 八、交付物清单

| 序号 | 交付物 | 文件 | 要求 |
|------|--------|------|------|
| 1 | 金融数据模型DDL | `finance_risk_ddl.sql` | 账户表/交易表/用户表/决策表 |
| 2 | 数据生成脚本 | `finance_data_generator.py` | 100万账户+5000万交易+欺诈标注 |
| 3 | Flink风控作业 | `RealTimeRiskEngine.java` | 实时特征+规则引擎 |
| 4 | Flink SQL特征 | `risk_feature_sql.sql` | 滑动窗口统计 |
| 5 | Redis特征服务 | `redis_feature_service.py` | 实时特征读写 |
| 6 | Neo4j图风控 | `neo4j_graph_risk.cypher` | 图构建+社区发现+PageRank |
| 7 | Spark图计算 | `spark_graph_risk.py` | 批量图特征+写入Redis |
| 8 | Grafana Dashboard | `finance_risk_dashboard.json` | 风控大屏8个面板 |
| 9 | 效果评估脚本 | `risk_evaluation.py` | 精确率/召回率/F1+误报漏报分析 |
| 10 | Docker Compose | `docker-compose-finance-risk.yml` | 一键启动全栈环境 |

---

## 九、评分标准

| 评分项 | 权重 | 要求 |
|--------|------|------|
| 数据建模与生成 | 15% | DDL正确，数据生成完整，欺诈模式合理 |
| 实时风控管道 | 30% | Flink规则引擎5条规则全部实现，延迟<500ms |
| 图风控 | 20% | Neo4j图构建+社区发现+PageRank+环路检测 |
| 监控与报告 | 20% | Grafana大屏完整，效果评估脚本可运行 |
| 代码质量 | 15% | 代码规范，异常处理完善，可复现 |
