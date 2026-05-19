# 课时21：Flink SQL与CDC

> **所属阶段**：L2 中级工程师 | **周次**：第17-18周 | **课时**：3h | **难度**：★★★★☆

---

## 一、教学目标

1. 理解Flink SQL的核心概念：动态表、时态表、Changelog Stream
2. 掌握Flink SQL CDC（Change Data Capture）
3. 能使用Flink SQL CDC实现MySQL到Kafka/Doris/ClickHouse的实时同步
4. 理解时态表Join（Temporal Table Join）
5. 能实现多流Join构建实时宽表

---

## 二、Flink SQL核心概念

### 2.1 动态表（Dynamic Table）

```
Flink SQL的核心抽象：动态表

静态表 vs 动态表:
  静态表(传统SQL): 查询时数据是固定的
    SELECT * FROM orders WHERE status = 'paid';
    → 查询那一刻的付费订单

  动态表(Flink SQL): 数据随时间持续变化
    INSERT INTO paid_orders
    SELECT * FROM orders WHERE status = 'paid';
    → 每当有新订单变成paid，自动写入paid_orders

动态表的本质：
  对Dynamic Table的查询 = 在对一个持续更新的流上执行查询
  每次有新的变更数据到达时，查询结果会增量更新
```

### 2.2 Changelog Stream

```
Flink SQL内部使用Changelog Stream来表示动态表的变更

Changelog Stream = 带有RowKind的数据流

RowKind的类型:
  +I (INSERT):   新数据插入
  -U (UPDATE_BEFORE): 更新前旧值
  +U (UPDATE_AFTER):  更新后新值
  -D (DELETE):   数据删除

示例: 订单状态变化在Changelog中的表示

原始数据: order_id=1, status='created'
  → (+I, {id:1, status:'created'})

更新: order_id=1, status='paid'
  → (-U, {id:1, status:'created'})   ← 撤回旧值
  → (+U, {id:1, status:'paid'})      ← 插入新值

删除: order_id=1被取消
  → (-D, {id:1, status:'paid'})
```

---

## 三、Docker Compose部署Flink SQL + MySQL CDC环境

### 3.1 docker-compose.yml

```yaml
version: '3.8'
services:
  mysql:
    image: mysql:8.0
    hostname: mysql
    container_name: mysql
    ports:
      - "3306:3306"
    environment:
      MYSQL_ROOT_PASSWORD: root123
      MYSQL_DATABASE: ecommerce
      MYSQL_USER: flink_user
      MYSQL_PASSWORD: flink_password
    command: >
      --server-id=1
      --log-bin=mysql-bin
      --binlog-format=ROW
      --binlog-row-image=FULL
      --gtid-mode=ON
      --enforce-gtid-consistency=ON
    volumes:
      - mysql-data:/var/lib/mysql
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql

  kafka-broker:
    image: confluentinc/cp-kafka:7.5.0
    hostname: kafka-broker
    container_name: kafka-broker
    ports:
      - "9092:9092"
    environment:
      KAFKA_BROKER_ID: 1
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: PLAINTEXT:PLAINTEXT,PLAINTEXT_HOST:PLAINTEXT
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://kafka-broker:29092,PLAINTEXT_HOST://localhost:9092
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
      KAFKA_TRANSACTION_STATE_LOG_REPLICATION_FACTOR: 1
      KAFKA_TRANSACTION_STATE_LOG_MIN_ISR: 1

  zookeeper:
    image: confluentinc/cp-zookeeper:7.5.0
    hostname: zookeeper
    container_name: zookeeper
    ports:
      - "2181:2181"
    environment:
      ZOOKEEPER_CLIENT_PORT: 2181
      ZOOKEEPER_TICK_TIME: 2000

  clickhouse:
    image: clickhouse/clickhouse-server:23.8
    hostname: clickhouse
    container_name: clickhouse
    ports:
      - "8123:8123"
      - "9000:9000"
    volumes:
      - clickhouse-data:/var/lib/clickhouse
      - ./clickhouse-init.sql:/docker-entrypoint-initdb.d/init.sql

  flink-jobmanager:
    image: flink:1.17.1-java11
    hostname: flink-jobmanager
    container_name: flink-jobmanager
    ports:
      - "8081:8081"
    command: jobmanager
    environment:
      FLINK_PROPERTIES: |
        jobmanager.rpc.address: flink-jobmanager
        state.backend: rocksdb
        state.backend.incremental: true
        state.checkpoints.dir: file:///tmp/flink-checkpoints
        execution.checkpointing.interval: 60s
        execution.checkpointing.mode: EXACTLY_ONCE
    volumes:
      - ./flink-sql-jobs:/opt/flink/usrlib
      - ./flink-cdc-connector:/opt/flink/plugins/cdc

  flink-taskmanager:
    image: flink:1.17.1-java11
    hostname: flink-taskmanager
    container_name: flink-taskmanager
    depends_on:
      - flink-jobmanager
    command: taskmanager
    environment:
      FLINK_PROPERTIES: |
        jobmanager.rpc.address: flink-jobmanager
        taskmanager.numberOfTaskSlots: 4
        state.backend: rocksdb
        state.backend.incremental: true
        state.checkpoints.dir: file:///tmp/flink-checkpoints
    volumes:
      - ./flink-cdc-connector:/opt/flink/plugins/cdc

volumes:
  mysql-data:
  clickhouse-data:
```

### 3.2 MySQL初始化SQL

```sql
CREATE DATABASE IF NOT EXISTS ecommerce;
USE ecommerce;

CREATE TABLE orders (
    order_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT NOT NULL,
    product_id BIGINT NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    status VARCHAR(20) DEFAULT 'created',
    create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE users (
    user_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    city VARCHAR(50),
    age INT,
    register_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE products (
    product_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL,
    category VARCHAR(50),
    price DECIMAL(10, 2) NOT NULL
);

INSERT INTO users (username, city, age) VALUES
('张三', '北京', 28), ('李四', '上海', 35),
('王五', '广州', 22), ('赵六', '深圳', 31);

INSERT INTO products (product_name, category, price) VALUES
('iPhone 15', '电子', 7999.00), ('Nike运动鞋', '服装', 899.00),
('三体全集', '图书', 128.00), ('机械键盘', '电子', 599.00);

INSERT INTO orders (user_id, product_id, amount, status) VALUES
(1, 1, 7999.00, 'completed'), (2, 2, 899.00, 'completed'),
(3, 3, 128.00, 'created'), (1, 4, 599.00, 'paid');
```

### 3.3 ClickHouse初始化SQL

```sql
CREATE DATABASE IF NOT EXISTS ecommerce;

CREATE TABLE ecommerce.trade_stats_minute (
    window_start DateTime,
    window_end DateTime,
    category String,
    city String,
    order_count UInt64,
    total_amount Decimal(20, 2),
    avg_amount Decimal(10, 2),
    user_count UInt64
) ENGINE = MergeTree()
ORDER BY (window_start, category, city);

CREATE TABLE ecommerce.orders_sink (
    order_id UInt64,
    user_id UInt64,
    username String,
    city String,
    product_id UInt64,
    product_name String,
    category String,
    amount Decimal(10, 2),
    status String,
    order_time DateTime,
    sync_time DateTime
) ENGINE = ReplacingMergeTree()
ORDER BY order_id;
```

### 3.4 环境启动命令

```bash
docker-compose up -d

docker-compose ps

docker exec -it mysql mysql -uroot -proot123 -e "SHOW DATABASES;"

docker exec -it clickhouse clickhouse-client --query "SHOW DATABASES"

docker exec -it flink-jobmanager ./bin/sql-client.sh embedded
```

---

## 四、CDC (Change Data Capture)

### 3.1 CDC原理

```
CDC = 实时捕获数据库的变更数据

MySQL CDC原理:
  MySQL主从复制协议 → Binlog
                    ↓
          Flink CDC Connector
          (模拟MySQL Slave)
                    ↓
          Binlog Event → Flink Changelog Stream

Binlog Event类型:
  - INSERT → RowKind.+I
  - UPDATE → RowKind.-U + RowKind.+U
  - DELETE → RowKind.-D
```

### 3.2 CDC Connector配置详解

```sql
-- MySQL CDC Connector核心参数
CREATE TABLE mysql_source (
    -- 业务字段
    id BIGINT,
    name STRING,
    amount DECIMAL(10, 2),
    status STRING,
    update_time TIMESTAMP(3),
    -- 主键定义（用于Changelog去重）
    PRIMARY KEY (id) NOT ENFORCED
) WITH (
    'connector' = 'mysql-cdc',        -- CDC连接器类型
    'hostname' = '192.168.1.100',     -- MySQL主机
    'port' = '3306',                  -- MySQL端口
    'username' = 'flink_user',        -- 数据库用户名
    'password' = 'flink_password',    -- 数据库密码
    'database-name' = 'ecommerce',    -- 数据库名
    'table-name' = 'orders',          -- 表名（支持正则）
    -- 高级参数
    'server-id' = '5400-5404',        -- 模拟Slave的Server ID（每个Job唯一）
    'server-time-zone' = 'Asia/Shanghai', -- 时区
    'scan.startup.mode' = 'initial',  -- 启动模式
    -- startup mode选项:
    --   'initial': 先全量快照，再增量Binlog（默认，最常用）
    --   'latest-offset': 只读最新的Binlog（跳过历史数据）
    --   'earliest-offset': 从最早的可用Binlog开始
    --   'specific-offset': 从指定Binlog位置开始
    --   'timestamp': 从指定时间戳开始
    'debezium.snapshot.mode' = 'initial',  -- Debezium快照模式
    'connect.timeout' = '30s',
    'connect.max-retries' = '3'
);
```

### 3.3 CDC启动模式选择

```
Initial模式 (最常用):
  ┌─────────────────────────────────────────────────────────┐
  │ 历史阶段              实时阶段                           │
  │ ──────────            ─────────                         │
  │ 全量快照读取          读取Binlog增量                     │
  │ SELECT * FROM         Binlog Position: xxx              │
  │ ecommerce.orders      ──→ 持续读取                      │
  │                                                         │
  │ 优势: 一条SQL完成历史+实时，无缝衔接                      │
  │ 注意: 全量阶段会锁表（可用 read-only 减少影响）           │
  └─────────────────────────────────────────────────────────┘

Latest-Offset模式 (纯增量):
  ┌─────────────────────────────────────────────────────────┐
  │ 只读最新的Binlog Position                                │
  │                                                         │
  │ 适用: 历史数据已通过其他方式导入                          │
  │ 注意: 会丢失启动前的所有变更                              │
  └─────────────────────────────────────────────────────────┘

Timestamp模式 (指定时间点恢复):
  ┌─────────────────────────────────────────────────────────┐
  │ 从 '2024-01-01 00:00:00' 开始读Binlog                    │
  │                                                         │
  │ 适用: 恢复到某个时间点                                   │
  └─────────────────────────────────────────────────────────┘
```

---

## 四、完整Flink SQL CDC代码

### 4.1 实时同步：MySQL → Kafka

```sql
-- ============================================================
-- 场景：MySQL订单表 → Kafka 实时同步
-- 使用Flink SQL CDC，零代码实现数据实时采集
-- ============================================================

-- 步骤1: 创建MySQL CDC源表
CREATE TABLE mysql_orders (
    order_id BIGINT,
    user_id BIGINT,
    product_id BIGINT,
    amount DECIMAL(10, 2),
    status STRING,
    create_time TIMESTAMP(3),
    update_time TIMESTAMP(3),
    PRIMARY KEY (order_id) NOT ENFORCED
) WITH (
    'connector' = 'mysql-cdc',
    'hostname' = 'mysql',
    'port' = '3306',
    'username' = 'root',
    'password' = 'root123',
    'database-name' = 'ecommerce',
    'table-name' = 'orders',
    'server-id' = '5400-5404',
    'server-time-zone' = 'Asia/Shanghai',
    'scan.startup.mode' = 'initial'
);

-- 步骤2: 创建Kafka Sink表 (Upsert模式)
CREATE TABLE kafka_orders (
    order_id BIGINT,
    user_id BIGINT,
    product_id BIGINT,
    amount DECIMAL(10, 2),
    status STRING,
    create_time TIMESTAMP(3),
    update_time TIMESTAMP(3),
    sync_time TIMESTAMP(3),
    PRIMARY KEY (order_id) NOT ENFORCED
) WITH (
    'connector' = 'upsert-kafka',
    'topic' = 'mysql-ecommerce-orders',
    'properties.bootstrap.servers' = 'localhost:9092',
    'key.format' = 'json',
    'value.format' = 'json',
    'properties.enable.idempotence' = 'true'
);

-- 步骤3: 实时同步（加上同步时间）
INSERT INTO kafka_orders
SELECT 
    order_id,
    user_id,
    product_id,
    amount,
    status,
    create_time,
    update_time,
    CURRENT_TIMESTAMP AS sync_time
FROM mysql_orders;
```

### 4.2 实时宽表构建：CDC + Kafka Join

```sql
-- ============================================================
-- 场景：构建订单实时宽表
-- 数据源：
--   1. MySQL orders 表（CDC实时）
--   2. MySQL users 表（CDC实时）
--   3. MySQL products 表（CDC实时）
-- 输出：Kafka 宽表 Topic
-- ============================================================

-- 1. 订单CDC源表
CREATE TABLE cdc_orders (
    order_id BIGINT,
    user_id BIGINT,
    product_id BIGINT,
    amount DECIMAL(10, 2),
    status STRING,
    order_time TIMESTAMP(3),
    PRIMARY KEY (order_id) NOT ENFORCED
) WITH (
    'connector' = 'mysql-cdc',
    'hostname' = 'mysql',
    'port' = '3306',
    'username' = 'root',
    'password' = 'root123',
    'database-name' = 'ecommerce',
    'table-name' = 'orders',
    'server-id' = '5500-5504',
    'server-time-zone' = 'Asia/Shanghai',
    'scan.startup.mode' = 'initial'
);

-- 2. 用户CDC源表
CREATE TABLE cdc_users (
    user_id BIGINT,
    username STRING,
    city STRING,
    age INT,
    register_time TIMESTAMP(3),
    PRIMARY KEY (user_id) NOT ENFORCED
) WITH (
    'connector' = 'mysql-cdc',
    'hostname' = 'mysql',
    'port' = '3306',
    'username' = 'root',
    'password' = 'root123',
    'database-name' = 'ecommerce',
    'table-name' = 'users',
    'server-id' = '5600-5604',
    'server-time-zone' = 'Asia/Shanghai',
    'scan.startup.mode' = 'initial'
);

-- 3. 商品CDC源表
CREATE TABLE cdc_products (
    product_id BIGINT,
    product_name STRING,
    category STRING,
    price DECIMAL(10, 2),
    PRIMARY KEY (product_id) NOT ENFORCED
) WITH (
    'connector' = 'mysql-cdc',
    'hostname' = 'mysql',
    'port' = '3306',
    'username' = 'root',
    'password' = 'root123',
    'database-name' = 'ecommerce',
    'table-name' = 'products',
    'server-id' = '5700-5704',
    'server-time-zone' = 'Asia/Shanghai',
    'scan.startup.mode' = 'initial'
);

-- 4. Kafka宽表Sink
CREATE TABLE kafka_order_wide (
    order_id BIGINT,
    user_id BIGINT,
    username STRING,
    city STRING,
    age INT,
    product_id BIGINT,
    product_name STRING,
    category STRING,
    amount DECIMAL(10, 2),
    unit_price DECIMAL(10, 2),
    status STRING,
    order_time TIMESTAMP(3),
    build_time TIMESTAMP(3),
    PRIMARY KEY (order_id) NOT ENFORCED
) WITH (
    'connector' = 'upsert-kafka',
    'topic' = 'order-wide-table',
    'properties.bootstrap.servers' = 'localhost:9092',
    'key.format' = 'json',
    'value.format' = 'json'
);

-- 5. 三表Join构建宽表
INSERT INTO kafka_order_wide
SELECT
    o.order_id,
    o.user_id,
    u.username,
    u.city,
    u.age,
    o.product_id,
    p.product_name,
    p.category,
    o.amount,
    p.price AS unit_price,
    o.status,
    o.order_time,
    CURRENT_TIMESTAMP AS build_time
FROM cdc_orders o
LEFT JOIN cdc_users AS u 
    ON o.user_id = u.user_id
LEFT JOIN cdc_products AS p 
    ON o.product_id = p.product_id;
```

### 4.3 实时聚合写入ClickHouse

```sql
-- ============================================================
-- 场景：实时统计每分钟交易指标 → ClickHouse
-- 数据源：Kafka中的订单宽表
-- 输出：ClickHouse汇总表
-- ============================================================

-- 1. Kafka源表（读取订单宽表）
CREATE TABLE kafka_order_source (
    order_id BIGINT,
    user_id BIGINT,
    username STRING,
    city STRING,
    age INT,
    product_id BIGINT,
    product_name STRING,
    category STRING,
    amount DECIMAL(10, 2),
    unit_price DECIMAL(10, 2),
    status STRING,
    order_time TIMESTAMP(3),
    -- 定义Watermark（基于event time）
    WATERMARK FOR order_time AS order_time - INTERVAL '5' SECOND,
    PRIMARY KEY (order_id) NOT ENFORCED
) WITH (
    'connector' = 'upsert-kafka',
    'topic' = 'order-wide-table',
    'properties.bootstrap.servers' = 'localhost:9092',
    'key.format' = 'json',
    'value.format' = 'json'
);

-- 2. ClickHouse Sink表
CREATE TABLE ch_trade_stats (
    window_start TIMESTAMP(3),
    window_end TIMESTAMP(3),
    category STRING,
    city STRING,
    order_count BIGINT,
    total_amount DECIMAL(20, 2),
    avg_amount DECIMAL(10, 2),
    user_count BIGINT,
    PRIMARY KEY (window_start, window_end, category, city) NOT ENFORCED
) WITH (
    'connector' = 'jdbc',
    'url' = 'jdbc:clickhouse://clickhouse:8123/ecommerce',
    'table-name' = 'trade_stats_minute',
    'username' = 'default',
    'password' = '',
    'sink.buffer-flush.max-rows' = '1000',
    'sink.buffer-flush.interval' = '5s',
    'sink.max-retries' = '3'
);

-- 3. 实时聚合
INSERT INTO ch_trade_stats
SELECT
    TUMBLE_START(order_time, INTERVAL '1' MINUTE) AS window_start,
    TUMBLE_END(order_time, INTERVAL '1' MINUTE) AS window_end,
    category,
    city,
    COUNT(*) AS order_count,
    SUM(amount) AS total_amount,
    AVG(amount) AS avg_amount,
    COUNT(DISTINCT user_id) AS user_count
FROM kafka_order_source
WHERE status = 'completed'
GROUP BY 
    TUMBLE(order_time, INTERVAL '1' MINUTE),
    category,
    city;
```

### 4.4 异常检测：实时风控

```sql
-- ============================================================
-- 场景：实时检测异常交易行为
-- 规则：
--   1. 同一用户1分钟内下单超过3次 → 标记为高频交易
--   2. 单笔金额超过10000 → 标记为大额交易
--   3. 同一IP短时间多账号下单 → 标记为疑似刷单
-- 输出：Kafka 告警Topic
-- ============================================================

-- 1. 高频交易检测
CREATE TABLE high_frequency_alerts (
    user_id BIGINT,
    window_start TIMESTAMP(3),
    window_end TIMESTAMP(3),
    order_count BIGINT,
    total_amount DECIMAL(20, 2),
    alert_type STRING,
    alert_time TIMESTAMP(3),
    PRIMARY KEY (user_id, window_start) NOT ENFORCED
) WITH (
    'connector' = 'upsert-kafka',
    'topic' = 'fraud-alerts-high-frequency',
    'properties.bootstrap.servers' = 'localhost:9092',
    'key.format' = 'json',
    'value.format' = 'json'
);

INSERT INTO high_frequency_alerts
SELECT
    user_id,
    TUMBLE_START(order_time, INTERVAL '1' MINUTE) AS window_start,
    TUMBLE_END(order_time, INTERVAL '1' MINUTE) AS window_end,
    COUNT(*) AS order_count,
    SUM(amount) AS total_amount,
    'HIGH_FREQUENCY' AS alert_type,
    CURRENT_TIMESTAMP AS alert_time
FROM kafka_order_source
GROUP BY 
    user_id,
    TUMBLE(order_time, INTERVAL '1' MINUTE)
HAVING COUNT(*) > 3;

-- 2. 大额交易检测
CREATE TABLE large_amount_alerts (
    order_id BIGINT PRIMARY KEY NOT ENFORCED,
    user_id BIGINT,
    amount DECIMAL(10, 2),
    category STRING,
    order_time TIMESTAMP(3),
    alert_type STRING,
    alert_time TIMESTAMP(3)
) WITH (
    'connector' = 'upsert-kafka',
    'topic' = 'fraud-alerts-large-amount',
    'properties.bootstrap.servers' = 'localhost:9092',
    'key.format' = 'json',
    'value.format' = 'json'
);

INSERT INTO large_amount_alerts
SELECT
    order_id,
    user_id,
    amount,
    category,
    order_time,
    'LARGE_AMOUNT' AS alert_type,
    CURRENT_TIMESTAMP AS alert_time
FROM kafka_order_source
WHERE amount > 10000;
```

---

## 五、时态表Join

### 5.1 概念

```
时态表(Temporal Table): 记录数据随时间变化的表

普通表Join vs 时态表Join:

  普通Join(不考虑时间):
    orders JOIN products ON orders.product_id = products.product_id
    → 总是用products的最新版本来Join
    → 问题：如果商品价格变化了，历史订单会被错误计算

  时态表Join(考虑时间):
    orders JOIN products FOR SYSTEM_TIME AS OF orders.order_time
    → 用订单发生时那个时间点的商品信息来Join
    → 正确：价格上升前的订单用旧价格，上升后用新价格
```

### 5.2 时态表Join代码

```sql
-- ============================================================
-- 时态表Join：订单关联时态版本的商品价格
-- ============================================================

-- 1. 定义时态表（商品价格Changelog）
-- 注意：主键 + WATERMARK 是时态表的必要条件
CREATE TABLE product_price_changelog (
    product_id BIGINT,
    price DECIMAL(10, 2),
    update_time TIMESTAMP(3),
    PRIMARY KEY (product_id) NOT ENFORCED,
    WATERMARK FOR update_time AS update_time - INTERVAL '5' SECOND
) WITH (
    'connector' = 'mysql-cdc',
    'hostname' = 'mysql',
    'port' = '3306',
    'username' = 'root',
    'password' = 'root123',
    'database-name' = 'ecommerce',
    'table-name' = 'product_prices',
    'server-id' = '5800-5804',
    'server-time-zone' = 'Asia/Shanghai'
);

-- 2. 时态表Join查询
SELECT
    o.order_id,
    o.order_time,
    o.product_id,
    p.price AS price_at_order_time,
    o.amount,
    -- 计算实付金额与当时单价的比值
    o.amount / p.price AS quantity_at_order_time
FROM cdc_orders o
LEFT JOIN product_price_changelog 
    FOR SYSTEM_TIME AS OF o.order_time AS p
    ON o.product_id = p.product_id
WHERE o.status = 'completed';
```

---

## 六、多流Join构建实时宽表

### 6.1 Join类型对比

| Join类型 | 语法 | 适用场景 | 状态要求 |
|----------|------|----------|----------|
| Regular Join | `A JOIN B ON ...` | 两个流都保留完整历史 | 无限增长状态（谨慎使用） |
| Interval Join | `A JOIN B ON ... AND A.time BETWEEN B.time-1h AND B.time+1h` | 有时间窗口关联的流 | 状态有界（推荐） |
| Temporal Join | `A JOIN B FOR SYSTEM_TIME AS OF A.time` | 关联维度表的时态版本 | B是Changelog Stream |
| Lookup Join | `A JOIN B FOR SYSTEM_TIME AS OF A.proctime` | 关联外部数据库（维表） | B是外部系统 |

### 6.2 Interval Join

```sql
-- ============================================================
-- Interval Join：关联订单流和支付流
-- 订单和支付通常在5分钟内完成
-- ============================================================

-- 支付流（CDC）
CREATE TABLE cdc_payments (
    payment_id BIGINT,
    order_id BIGINT,
    pay_amount DECIMAL(10, 2),
    pay_method STRING,
    pay_time TIMESTAMP(3),
    PRIMARY KEY (payment_id) NOT ENFORCED,
    WATERMARK FOR pay_time AS pay_time - INTERVAL '5' SECOND
) WITH (
    'connector' = 'mysql-cdc',
    'hostname' = 'mysql',
    'port' = '3306',
    'username' = 'root',
    'password' = 'root123',
    'database-name' = 'ecommerce',
    'table-name' = 'payments',
    'server-id' = '5900-5904',
    'server-time-zone' = 'Asia/Shanghai'
);

-- Interval Join查询
SELECT
    o.order_id,
    o.user_id,
    o.amount AS order_amount,
    p.pay_amount,
    p.pay_method,
    o.order_time,
    p.pay_time,
    -- 支付耗时（分钟）
    TIMESTAMPDIFF(MINUTE, o.order_time, p.pay_time) AS pay_duration_minutes
FROM cdc_orders o
JOIN cdc_payments p
    ON o.order_id = p.order_id
    -- 关键：时间区间约束，状态有界！
    AND p.pay_time BETWEEN o.order_time - INTERVAL '1' MINUTE 
                       AND o.order_time + INTERVAL '30' MINUTE
WHERE o.status = 'completed';
```

### 6.3 Lookup Join（维表关联）

```sql
-- ============================================================
-- Lookup Join：实时流关联MySQL维表
-- 适用：维表变更不频繁，数据量可控
-- ============================================================

-- 订单流（Kafka）
CREATE TABLE kafka_order_stream (
    order_id BIGINT,
    user_id BIGINT,
    product_id BIGINT,
    amount DECIMAL(10, 2),
    status STRING,
    order_time TIMESTAMP(3),
    -- 使用Processing Time作为Join的时间维度
    proc_time AS PROCTIME()
) WITH (
    'connector' = 'kafka',
    'topic' = 'orders',
    'properties.bootstrap.servers' = 'localhost:9092',
    'format' = 'json',
    'scan.startup.mode' = 'latest-offset'
);

-- MySQL维表（用于Lookup）
CREATE TABLE dim_users (
    user_id BIGINT,
    username STRING,
    city STRING,
    vip_level INT,
    PRIMARY KEY (user_id) NOT ENFORCED
) WITH (
    'connector' = 'jdbc',
    'url' = 'jdbc:mysql://mysql:3306/ecommerce',
    'table-name' = 'users',
    'username' = 'root',
    'password' = 'root123',
    -- Lookup缓存
    'lookup.cache.max-rows' = '10000',
    'lookup.cache.ttl' = '10min',
    'lookup.max-retries' = '3'
);

-- Lookup Join（用proctime做时间维度）
SELECT
    o.order_id,
    o.user_id,
    u.username,
    u.city,
    u.vip_level,
    o.amount,
    o.status,
    o.order_time
FROM kafka_order_stream o
LEFT JOIN dim_users 
    FOR SYSTEM_TIME AS OF o.proc_time AS u
    ON o.user_id = u.user_id;
```

---

## 七、Flink SQL Job提交

### 7.1 SQL Client提交

```bash
# 启动SQL Client
./bin/sql-client.sh embedded

# 在SQL Client中执行
Flink SQL> SET 'execution.runtime-mode' = 'streaming';
Flink SQL> SET 'sql-client.execution.result-mode' = 'tableau';

# 加载SQL文件
Flink SQL> SOURCE /path/to/cdc_job.sql;

# 或通过命令行直接提交SQL文件
./bin/sql-client.sh embedded -f /path/to/cdc_job.sql
```

### 7.2 通过Java提交SQL Job

```java
import org.apache.flink.table.api.EnvironmentSettings;
import org.apache.flink.table.api.TableEnvironment;

public class FlinkSQLJobSubmitter {

    public static void main(String[] args) {
        // 流模式
        EnvironmentSettings settings = EnvironmentSettings
            .newInstance()
            .inStreamingMode()
            .build();

        TableEnvironment tEnv = TableEnvironment.create(settings);

        // 配置Checkpoint
        tEnv.getConfig().getConfiguration().setString(
            "execution.checkpointing.interval", "60s");

        // 执行一条SQL
        tEnv.executeSql("CREATE TABLE mysql_orders (...) WITH (...)");

        // 或执行SQL文件
        String sql = new String(
            java.nio.file.Files.readAllBytes(
                java.nio.file.Paths.get("/path/to/cdc_job.sql")));

        // 按分号分割并执行每条SQL
        for (String stmt : sql.split(";")) {
            stmt = stmt.trim();
            if (!stmt.isEmpty()) {
                System.out.println("Executing: " + stmt.substring(0, 
                    Math.min(80, stmt.length())) + "...");
                tEnv.executeSql(stmt);
            }
        }

        System.out.println("Flink SQL Job 提交完成");
    }
}
```

### 7.3 Python提交Flink SQL

```python
"""
通过PyFlink提交Flink SQL作业
"""
from pyflink.table import (
    EnvironmentSettings, TableEnvironment, StatementSet
)
from pyflink.table.expressions import col

def submit_cdc_job():
    # 创建流处理环境
    env_settings = EnvironmentSettings.in_streaming_mode()
    t_env = TableEnvironment.create(env_settings)

    # 配置Checkpoint
    t_env.get_config().get_configuration().set_string(
        "execution.checkpointing.interval", "60s"
    )
    t_env.get_config().get_configuration().set_string(
        "execution.checkpointing.timeout", "10min"
    )

    # 配置State Backend
    t_env.get_config().get_configuration().set_string(
        "state.backend", "rocksdb"
    )

    # 执行SQL文件中的所有语句
    with open('cdc_job.sql', 'r', encoding='utf-8') as f:
        sql_content = f.read()

    statement_set = t_env.create_statement_set()

    for statement in sql_content.split(';'):
        statement = statement.strip()
        if not statement:
            continue

        # DDL语句直接执行
        if any(keyword in statement.upper() for keyword in 
               ['CREATE TABLE', 'CREATE VIEW', 'CREATE FUNCTION']):
            print(f"Executing DDL...")
            t_env.execute_sql(statement)
        # INSERT语句加入StatementSet
        elif statement.upper().startswith('INSERT'):
            print(f"Adding INSERT to StatementSet...")
            statement_set.add_insert_sql(statement)

    # 一次提交所有INSERT语句
    print("Submitting Flink SQL Job...")
    statement_set.execute()

if __name__ == '__main__':
    submit_cdc_job()
```

---

## 八、CDC生产最佳实践

### 8.1 Server ID规划

```yaml
重要: 每个CDC Job必须有唯一的Server ID

规划方案:
  flink-cdc-orders-prod:    server-id = 5400-5404
  flink-cdc-users-prod:     server-id = 5500-5504
  flink-cdc-payments-prod:  server-id = 5600-5604

规则:
  - 每个并行度需要一个Server ID
  - Server ID范围 = [server-id, server-id + parallelism - 1]
  - 不同Job的Server ID范围不能重叠
  - Server ID 1-1000 通常保留给真正的MySQL Slave
```

### 8.2 全量快照优化

```sql
-- 大表全量快照优化参数
CREATE TABLE mysql_source (...) WITH (
    ...
    'debezium.snapshot.fetch.size' = '10240',       -- 每批拉取行数
    'debezium.snapshot.lock.timeout.ms' = '30000',  -- 锁超时
    'debezium.snapshot.locking.mode' = 'minimal',   -- 最小锁模式
    -- locking.mode选项:
    --   'minimal': 只在快照开始时短暂锁表（推荐）
    --   'minimal_percona': MySQL Percona版本优化
    --   'none': 不锁表（可能数据不一致）
    'debezium.poll.interval.ms' = '500',
    'debezium.max.queue.size' = '8192'
);
```

### 8.3 监控与告警

```yaml
CDC Job监控指标:

  Binlog延迟:
    - debezium_metrics:SecondsBehindMaster
    - 告警阈值: > 10秒

  快照进度:
    - debezium_metrics:SnapshotCompleted
    - debezium_metrics:SnapshotRunning
    - debezium_metrics:TotalNumberOfEventsSeen

  Flink Checkpoint:
    - numberOfFailedCheckpoints > 0 → 告警
    - lastCheckpointDuration > 60s → 告警

  Kafka Lag（如果输出到Kafka）:
    - kafka_consumer_group_lag > 10000 → 告警
```

---

## 九、完整MySQL→Flink CDC→Kafka→ClickHouse端到端管道

### 9.1 管道架构

```
MySQL (Binlog) → Flink CDC Source → Kafka (Upsert) → Flink SQL → ClickHouse
     │                  │                  │                │            │
  orders表          CDC采集           中间缓冲层        实时聚合       最终存储
  users表           Changelog         解耦+缓冲        窗口计算       分析查询
  products表        全量+增量         多下游消费        维表Join       报表展示
```

### 9.2 完整SQL脚本（cdc_pipeline.sql）

```sql
SET 'execution.checkpointing.interval' = '60s';
SET 'execution.checkpointing.mode' = 'EXACTLY_ONCE';
SET 'execution.checkpointing.timeout' = '10min';
SET 'execution.checkpointing.min-pause' = '30s';
SET 'execution.checkpointing.externalized-checkpoint-retention' = 'RETAIN_ON_CANCELLATION';
SET 'state.backend' = 'rocksdb';
SET 'state.backend.incremental' = 'true';
SET 'state.checkpoints.dir' = 'file:///tmp/flink-checkpoints';
SET 'pipeline.name' = 'MySQL-CDC-Kafka-ClickHouse-Pipeline';

CREATE TABLE cdc_orders (
    order_id BIGINT,
    user_id BIGINT,
    product_id BIGINT,
    amount DECIMAL(10, 2),
    status STRING,
    create_time TIMESTAMP(3),
    update_time TIMESTAMP(3),
    PRIMARY KEY (order_id) NOT ENFORCED
) WITH (
    'connector' = 'mysql-cdc',
    'hostname' = 'mysql',
    'port' = '3306',
    'username' = 'root',
    'password' = 'root123',
    'database-name' = 'ecommerce',
    'table-name' = 'orders',
    'server-id' = '5400-5404',
    'server-time-zone' = 'Asia/Shanghai',
    'scan.startup.mode' = 'initial'
);

CREATE TABLE cdc_users (
    user_id BIGINT,
    username STRING,
    city STRING,
    age INT,
    register_time TIMESTAMP(3),
    PRIMARY KEY (user_id) NOT ENFORCED
) WITH (
    'connector' = 'mysql-cdc',
    'hostname' = 'mysql',
    'port' = '3306',
    'username' = 'root',
    'password' = 'root123',
    'database-name' = 'ecommerce',
    'table-name' = 'users',
    'server-id' = '5500-5504',
    'server-time-zone' = 'Asia/Shanghai',
    'scan.startup.mode' = 'initial'
);

CREATE TABLE cdc_products (
    product_id BIGINT,
    product_name STRING,
    category STRING,
    price DECIMAL(10, 2),
    PRIMARY KEY (product_id) NOT ENFORCED
) WITH (
    'connector' = 'mysql-cdc',
    'hostname' = 'mysql',
    'port' = '3306',
    'username' = 'root',
    'password' = 'root123',
    'database-name' = 'ecommerce',
    'table-name' = 'products',
    'server-id' = '5600-5604',
    'server-time-zone' = 'Asia/Shanghai',
    'scan.startup.mode' = 'initial'
);

CREATE TABLE kafka_orders (
    order_id BIGINT,
    user_id BIGINT,
    username STRING,
    city STRING,
    product_id BIGINT,
    product_name STRING,
    category STRING,
    amount DECIMAL(10, 2),
    unit_price DECIMAL(10, 2),
    status STRING,
    order_time TIMESTAMP(3),
    sync_time TIMESTAMP(3),
    PRIMARY KEY (order_id) NOT ENFORCED
) WITH (
    'connector' = 'upsert-kafka',
    'topic' = 'ecommerce-orders-wide',
    'properties.bootstrap.servers' = 'kafka-broker:9092',
    'key.format' = 'json',
    'value.format' = 'json'
);

INSERT INTO kafka_orders
SELECT
    o.order_id,
    o.user_id,
    u.username,
    u.city,
    o.product_id,
    p.product_name,
    p.category,
    o.amount,
    p.price AS unit_price,
    o.status,
    o.create_time AS order_time,
    CURRENT_TIMESTAMP AS sync_time
FROM cdc_orders o
LEFT JOIN cdc_users AS u ON o.user_id = u.user_id
LEFT JOIN cdc_products AS p ON o.product_id = p.product_id;

CREATE TABLE ch_orders_sink (
    order_id BIGINT,
    user_id BIGINT,
    username STRING,
    city STRING,
    product_id BIGINT,
    product_name STRING,
    category STRING,
    amount DECIMAL(10, 2),
    unit_price DECIMAL(10, 2),
    status STRING,
    order_time TIMESTAMP(3),
    sync_time TIMESTAMP(3),
    PRIMARY KEY (order_id) NOT ENFORCED
) WITH (
    'connector' = 'jdbc',
    'url' = 'jdbc:clickhouse://clickhouse:8123/ecommerce',
    'table-name' = 'orders_sink',
    'username' = 'default',
    'password' = '',
    'sink.buffer-flush.max-rows' = '500',
    'sink.buffer-flush.interval' = '5s',
    'sink.max-retries' = '3'
);

INSERT INTO ch_orders_sink
SELECT * FROM kafka_orders;

CREATE TABLE ch_trade_stats (
    window_start TIMESTAMP(3),
    window_end TIMESTAMP(3),
    category STRING,
    city STRING,
    order_count BIGINT,
    total_amount DECIMAL(20, 2),
    avg_amount DECIMAL(10, 2),
    user_count BIGINT,
    PRIMARY KEY (window_start, window_end, category, city) NOT ENFORCED
) WITH (
    'connector' = 'jdbc',
    'url' = 'jdbc:clickhouse://clickhouse:8123/ecommerce',
    'table-name' = 'trade_stats_minute',
    'username' = 'default',
    'password' = '',
    'sink.buffer-flush.max-rows' = '1000',
    'sink.buffer-flush.interval' = '10s',
    'sink.max-retries' = '3'
);

INSERT INTO ch_trade_stats
SELECT
    TUMBLE_START(order_time, INTERVAL '1' MINUTE) AS window_start,
    TUMBLE_END(order_time, INTERVAL '1' MINUTE) AS window_end,
    category,
    city,
    COUNT(*) AS order_count,
    SUM(amount) AS total_amount,
    AVG(amount) AS avg_amount,
    COUNT(DISTINCT user_id) AS user_count
FROM kafka_orders
WHERE status = 'completed'
GROUP BY
    TUMBLE(order_time, INTERVAL '1' MINUTE),
    category,
    city;
```

### 9.3 数据验证脚本

```bash
echo "=== MySQL数据 ==="
docker exec -it mysql mysql -uroot -proot123 \
  -e "SELECT COUNT(*) AS total FROM ecommerce.orders;"

echo "=== Kafka数据 ==="
docker exec -it kafka-broker kafka-run-class.sh kafka.tools.GetOffsetShell \
  --broker-list localhost:9092 \
  --topic ecommerce-orders-wide | awk -F: '{sum+=$3} END {print "Kafka消息总数: " sum}'

echo "=== ClickHouse数据 ==="
docker exec -it clickhouse clickhouse-client --query \
  "SELECT COUNT() AS total FROM ecommerce.orders_sink"

echo "=== 数据一致性验证 ==="
MYSQL_COUNT=$(docker exec mysql mysql -uroot -proot123 -N \
  -e "SELECT COUNT(*) FROM ecommerce.orders" 2>/dev/null)
CH_COUNT=$(docker exec clickhouse clickhouse-client --query \
  "SELECT COUNT() FROM ecommerce.orders_sink" 2>/dev/null)
echo "MySQL: $MYSQL_COUNT, ClickHouse: $CH_COUNT"

docker exec -it clickhouse clickhouse-client --query \
  "SELECT category, city, SUM(order_count) AS total_orders, SUM(total_amount) AS total_amount FROM ecommerce.trade_stats_minute GROUP BY category, city ORDER BY total_amount DESC LIMIT 10"
```

---

## 十、课堂练习（45分钟）

### 练习1：搭建Flink SQL CDC环境（10分钟）

```bash
docker-compose up -d
sleep 30

docker exec -it flink-jobmanager ./bin/sql-client.sh embedded

SET 'execution.checkpointing.interval' = '30s';
SET 'state.backend' = 'rocksdb';

CREATE TABLE mysql_orders (
    order_id BIGINT,
    user_id BIGINT,
    product_id BIGINT,
    amount DECIMAL(10, 2),
    status STRING,
    create_time TIMESTAMP(3),
    update_time TIMESTAMP(3),
    PRIMARY KEY (order_id) NOT ENFORCED
) WITH (
    'connector' = 'mysql-cdc',
    'hostname' = 'mysql',
    'port' = '3306',
    'username' = 'root',
    'password' = 'root123',
    'database-name' = 'ecommerce',
    'table-name' = 'orders',
    'server-id' = '5400-5404',
    'server-time-zone' = 'Asia/Shanghai',
    'scan.startup.mode' = 'initial'
);

SELECT * FROM mysql_orders LIMIT 10;
```

**验证点**：确认能读取到MySQL中的初始数据（4条订单）。

### 练习2：构建实时同步管道MySQL→Kafka（20分钟）

```sql
CREATE TABLE kafka_orders_sync (
    order_id BIGINT,
    user_id BIGINT,
    amount DECIMAL(10, 2),
    status STRING,
    sync_time TIMESTAMP(3),
    PRIMARY KEY (order_id) NOT ENFORCED
) WITH (
    'connector' = 'upsert-kafka',
    'topic' = 'lab-orders-sync',
    'properties.bootstrap.servers' = 'kafka-broker:9092',
    'key.format' = 'json',
    'value.format' = 'json'
);

INSERT INTO kafka_orders_sync
SELECT
    order_id,
    user_id,
    amount,
    status,
    CURRENT_TIMESTAMP AS sync_time
FROM mysql_orders;
```

```bash
docker exec -it mysql mysql -uroot -proot123 -e \
  "INSERT INTO ecommerce.orders (user_id, product_id, amount, status) VALUES (1, 1, 299.00, 'created');"

docker exec -it mysql mysql -uroot -proot123 -e \
  "UPDATE ecommerce.orders SET status = 'paid' WHERE order_id = 3;"

docker exec -it kafka-broker kafka-console-consumer.sh \
  --topic lab-orders-sync \
  --bootstrap-server localhost:9092 \
  --from-beginning \
  --max-messages 10
```

**验证点**：确认INSERT和UPDATE操作都能实时同步到Kafka，UPDATE产生-U/+U两条Changelog记录。

### 练习3：验证端到端数据一致性（15分钟）

```bash
docker exec -it mysql mysql -uroot -proot123 -e \
  "INSERT INTO ecommerce.orders (user_id, product_id, amount, status) VALUES (2, 3, 256.00, 'completed');"

docker exec -it mysql mysql -uroot -proot123 -e \
  "DELETE FROM ecommerce.orders WHERE order_id = 1;"

sleep 10

docker exec -it clickhouse clickhouse-client --query \
  "SELECT * FROM ecommerce.orders_sink ORDER BY order_id"

docker exec -it clickhouse clickhouse-client --query \
  "SELECT * FROM ecommerce.trade_stats_minute ORDER BY window_start DESC LIMIT 5"
```

**验证点**：确认MySQL的INSERT/UPDATE/DELETE操作都能在ClickHouse中正确反映。

---

## 十一、课后作业

### 必做

1. **CDC管道搭建**：在本机Docker环境搭建 MySQL → Flink CDC → Kafka → Flink SQL → ClickHouse 的完整实时同步管道
2. **宽表构建**：实现4.2节的订单实时宽表（至少关联2个CDC源表）
3. **实时聚合**：实现按品类、按城市的每分钟交易统计（如4.3节）

### 选做

1. 实现时态表Join，验证商品价格变化时历史订单使用正确价格
2. 尝试Oracle CDC Connector（如果环境中有Oracle）
3. 实现实时风控告警系统（包含至少3种检测规则）

### 课后作业详细要求

**作业1：MySQL→Flink CDC→Kafka→ClickHouse端到端管道**

```bash
docker-compose up -d
sleep 30

docker exec -it flink-jobmanager ./bin/sql-client.sh embedded -f /opt/flink/usrlib/cdc_pipeline.sql

sleep 60

docker exec -it mysql mysql -uroot -proot123 ecommerce <<'EOF'
INSERT INTO orders (user_id, product_id, amount, status) VALUES
(1, 1, 1599.00, 'completed'),
(2, 2, 1798.00, 'completed'),
(3, 4, 599.00, 'paid'),
(4, 1, 7999.00, 'completed'),
(1, 3, 128.00, 'completed');

UPDATE orders SET status = 'completed' WHERE order_id = 3;

INSERT INTO users (username, city, age) VALUES
('孙七', '杭州', 26), ('周八', '成都', 33);

INSERT INTO products (product_name, category, price) VALUES
('AirPods Pro', '电子', 1899.00), ('编程珠玑', '图书', 69.00);
EOF

sleep 30

docker exec -it clickhouse clickhouse-client --query \
  "SELECT COUNT() AS total FROM ecommerce.orders_sink"

docker exec -it clickhouse clickhouse-client --query \
  "SELECT * FROM ecommerce.orders_sink ORDER BY order_id FORMAT Vertical"

docker exec -it clickhouse clickhouse-client --query \
  "SELECT category, city, SUM(order_count) AS total_orders, SUM(total_amount) AS total_amount FROM ecommerce.trade_stats_minute GROUP BY category, city ORDER BY total_amount DESC"

docker exec -it mysql mysql -uroot -proot123 -N \
  -e "SELECT COUNT(*) FROM ecommerce.orders" 2>/dev/null

docker exec -it clickhouse clickhouse-client --query \
  "SELECT COUNT() FROM ecommerce.orders_sink" 2>/dev/null
```

输出要求：提交以下内容：
1. 端到端管道运行截图（Flink Web UI显示Job运行中）
2. ClickHouse中的查询结果截图
3. MySQL和ClickHouse的数据一致性验证结果

**作业2：CDC数据变更验证脚本**

```bash
#!/bin/bash
echo "=== CDC数据变更验证 ==="

echo "[1] 插入新订单..."
docker exec -it mysql mysql -uroot -proot123 -e \
  "INSERT INTO ecommerce.orders (user_id, product_id, amount, status) VALUES (2, 1, 7999.00, 'completed');"

sleep 10

echo "[2] 验证Kafka..."
docker exec -it kafka-broker kafka-console-consumer.sh \
  --topic ecommerce-orders-wide \
  --bootstrap-server localhost:9092 \
  --from-beginning --max-messages 1 --timeout-ms 5000 2>/dev/null

echo "[3] 验证ClickHouse..."
docker exec -it clickhouse clickhouse-client --query \
  "SELECT * FROM ecommerce.orders_sink WHERE order_id = (SELECT MAX(order_id) FROM ecommerce.orders_sink) FORMAT Vertical"

echo "[4] 更新订单状态..."
docker exec -it mysql mysql -uroot -proot123 -e \
  "UPDATE ecommerce.orders SET status = 'shipped' WHERE status = 'paid' LIMIT 1;"

sleep 10

echo "[5] 验证更新已同步..."
docker exec -it clickhouse clickhouse-client --query \
  "SELECT order_id, status FROM ecommerce.orders_sink WHERE status = 'shipped'"

echo "[6] 删除订单..."
docker exec -it mysql mysql -uroot -proot123 -e \
  "DELETE FROM ecommerce.orders WHERE status = 'created' LIMIT 1;"

sleep 10

echo "[7] 最终数据统计..."
echo "MySQL订单数:"
docker exec -it mysql mysql -uroot -proot123 -N \
  -e "SELECT COUNT(*) FROM ecommerce.orders" 2>/dev/null
echo "ClickHouse订单数:"
docker exec -it clickhouse clickhouse-client --query \
  "SELECT COUNT() FROM ecommerce.orders_sink"

echo "=== 验证完成 ==="
```

输出要求：提交验证脚本运行结果，展示INSERT/UPDATE/DELETE三种操作都能正确同步到ClickHouse。

---

## 十、参考资料

- [Flink CDC Connectors](https://ververica.github.io/flink-cdc-connectors/)
- [Flink SQL Documentation](https://nightlies.apache.org/flink/flink-docs-stable/docs/dev/table/sql/overview/)
- [MySQL Binlog Documentation](https://dev.mysql.com/doc/refman/8.0/en/binary-log.html)
- [Debezium Documentation](https://debezium.io/documentation/)