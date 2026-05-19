# 课时22：Iceberg与Delta Lake实战

> **所属阶段**：L2 中级工程师 | **模块**：补充模块_数据湖仓实战 | **课时**：4h | **难度**：★★★★☆

---

## 一、教学目标

1. 理解数据湖的核心痛点以及数据湖仓架构如何解决这些痛点
2. 掌握Apache Iceberg的核心机制：快照隔离、元数据分层、分区演化、Schema演化、行级删除
3. 掌握Delta Lake的核心机制：事务日志、OPTIMIZE/Z-ORDER、与Spark深度集成
4. 了解Apache Hudi的COW/MOR模型与Upsert场景
5. 能根据业务场景在Iceberg、Delta Lake、Hudi之间做出合理选型

---

## 二、数据湖的痛点

### 2.1 传统数据湖的四大痛点

```
传统数据湖（HDFS + Parquet/ORC）的痛点：

  痛点1: 无ACID事务
    ┌──────────────────────────────────────────────────────────┐
    │  Job A: 写入50% ──────→ 崩溃!                            │
    │  Job B: 读取 ──────→ 读到一半脏数据!                      │
    │                                                          │
    │  结果: 数据不一致，下游报表错误                             │
    └──────────────────────────────────────────────────────────┘

  痛点2: 无Schema演进
    ┌──────────────────────────────────────────────────────────┐
    │  业务需求: 给订单表加一个"优惠券金额"字段                    │
    │                                                          │
    │  Hive做法: ALTER TABLE ADD COLUMN → 只对后续分区生效       │
    │           历史分区的数据无法读取新字段                       │
    │           改列类型? 几乎不可能，需要重建整张表               │
    └──────────────────────────────────────────────────────────┘

  痛点3: 无法Upsert
    ┌──────────────────────────────────────────────────────────┐
    │  场景: 订单状态从"待支付"变为"已支付"                       │
    │                                                          │
    │  Hive做法: 只能整分区覆盖写(INSERT OVERWRITE)              │
    │           或读取全表→修改→写回（极慢）                      │
    │           无法做到行级更新                                  │
    └──────────────────────────────────────────────────────────┘

  痛点4: 无法时间旅行
    ┌──────────────────────────────────────────────────────────┐
    │  场景: "昨天上午10点的数据是什么样？"                       │
    │                                                          │
    │  Hive做法: 无法回答！数据已被覆盖写，历史版本丢失           │
    │           只能靠备份恢复，耗时数小时                        │
    └──────────────────────────────────────────────────────────┘
```

### 2.2 数据湖仓架构：解决一切痛点

```
数据湖仓 = 数据湖的存储成本 + 数据仓库的ACID能力

  ┌───────────────────────────────────────────────────────────────────┐
  │                        数据湖仓架构                                │
  │                                                                   │
  │  ┌─────────────────────────────────────────────────────────────┐ │
  │  │                    多引擎访问层                               │ │
  │  │   Spark / Flink / Trino / Presto / Dremio / StarRocks       │ │
  │  └──────────────────────────┬──────────────────────────────────┘ │
  │                             │ 统一API                            │
  │  ┌──────────────────────────▼──────────────────────────────────┐ │
  │  │                    元数据管理层                               │ │
  │  │   Iceberg / Delta Lake / Hudi                               │ │
  │  │   ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────┐ │ │
  │  │   │ ACID事务 │ │ Schema  │ │ 分区演化 │ │ 时间旅行     │ │ │
  │  │   │ 快照隔离 │ │  演进   │ │          │ │ 版本回溯     │ │ │
  │  │   └──────────┘ └──────────┘ └──────────┘ └──────────────┘ │ │
  │  └──────────────────────────┬──────────────────────────────────┘ │
  │                             │                                    │
  │  ┌──────────────────────────▼──────────────────────────────────┐ │
  │  │                    开放存储格式层                             │ │
  │  │   Parquet / ORC / Avro + 对象存储(S3/OSS/HDFS/MinIO)       │ │
  │  └─────────────────────────────────────────────────────────────┘ │
  │                                                                   │
  └───────────────────────────────────────────────────────────────────┘
```

---

## 三、Apache Iceberg

### 3.1 Iceberg核心架构

```
Iceberg元数据分层结构（关键创新）：

  ┌──────────────────────────────────────────────────────────┐
  │  Catalog                                                  │
  │  └── current-snapshot-id = 38291028374                    │
  │       │                                                   │
  │       ▼                                                   │
  │  ┌────────────────────────────────────────────────────┐  │
  │  │  metadata/v38.metadata.json  (当前版本元数据)       │  │
  │  │  ├── schema: 字段定义                              │  │
  │  │  ├── partition-spec: 分区策略                       │  │
  │  │  ├── snapshots: 快照列表                            │  │
  │  │  │   ├── snapshot-1 (2024-01-01 10:00)              │  │
  │  │  │   ├── snapshot-2 (2024-01-02 10:00)              │  │
  │  │  │   └── snapshot-3 (2024-01-03 10:00) ← current    │  │
  │  │  └── current-snapshot-id: snapshot-3                │  │
  │  └────────────────────────────────────────────────────┘  │
  │       │                                                   │
  │       ▼ snapshot-3                                        │
  │  ┌────────────────────────────────────────────────────┐  │
  │  │  manifest-list (快照→清单列表的映射)                 │  │
  │  │  ├── manifest-A.avro (分区范围: 2024-01-01~01-10)   │  │
  │  │  ├── manifest-B.avro (分区范围: 2024-01-11~01-20)   │  │
  │  │  └── manifest-C.avro (分区范围: 2024-01-21~01-31)   │  │
  │  └────────────────────────────────────────────────────┘  │
  │       │                                                   │
  │       ▼ manifest-A                                        │
  │  ┌────────────────────────────────────────────────────┐  │
  │  │  manifest-file (数据文件清单)                        │  │
  │  │  ├── data-001.parquet (行数:50000, 大小:128MB)      │  │
  │  │  ├── data-002.parquet (行数:48000, 大小:125MB)      │  │
  │  │  └── data-003.parquet (行数:52000, 大小:130MB)      │  │
  │  └────────────────────────────────────────────────────┘  │
  │                                                           │
  └──────────────────────────────────────────────────────────┘

关键设计:
  1. 快照隔离: 每次写入产生新快照，读操作只看某个快照，读写互不干扰
  2. 元数据分层: Catalog → Metadata → ManifestList → Manifest → DataFile
  3. 计划下推: 查询时在Manifest层就能过滤掉不相关的数据文件，无需扫描数据
```

### 3.2 Spark + Iceberg实战

#### 3.2.1 环境配置

```sql
-- Spark SQL中配置Iceberg Catalog
-- 方式1: Hive Metastore作为Catalog
CREATE DATABASE IF NOT EXISTS iceberg_db;

-- 在spark-defaults.conf中配置:
-- spark.sql.catalog.iceberg=org.apache.iceberg.spark.SparkCatalog
-- spark.sql.catalog.iceberg.type=hive
-- spark.sql.catalog.iceberg.uri=thrift://hive-metastore:9083
-- spark.sql.catalog.iceberg.warehouse=s3a://warehouse/iceberg
-- spark.sql.extensions=org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions
```

#### 3.2.2 创建Iceberg表

```sql
-- 创建Iceberg表（使用Spark SQL）
CREATE TABLE iceberg_db.orders (
    order_id BIGINT,
    user_id BIGINT,
    order_status STRING,
    total_amount DECIMAL(12, 2),
    payment_amount DECIMAL(12, 2),
    shipping_province STRING,
    shipping_city STRING,
    create_time TIMESTAMP,
    pay_time TIMESTAMP,
    finish_time TIMESTAMP
)
USING iceberg
PARTITIONED BY (days(create_time))
TBLPROPERTIES (
    'write.format.default' = 'parquet',
    'write.parquet.compression-codec' = 'snappy',
    'read.split.target-size' = '134217728',
    'write.metadata.delete-after-commit.enabled' = 'true',
    'write.metadata.previous-versions-max' = '10',
    'history.expire.max-snapshot-age-ms' = '604800000'
);
```

#### 3.2.3 写入数据

```sql
-- 批量写入
INSERT INTO iceberg_db.orders
SELECT
    order_id,
    user_id,
    order_status,
    total_amount,
    payment_amount,
    shipping_province,
    shipping_city,
    create_time,
    pay_time,
    finish_time
FROM hive_db.ods_order_info
WHERE dt = '2024-01-15';

-- 追加写入（产生新快照）
INSERT INTO iceberg_db.orders
VALUES
    (999901, 5001, '待支付', 299.00, 0, '北京', '朝阳区', TIMESTAMP '2024-01-16 10:30:00', NULL, NULL),
    (999902, 5002, '已支付', 1580.50, 1580.50, '上海', '浦东新区', TIMESTAMP '2024-01-16 11:00:00', TIMESTAMP '2024-01-16 11:05:00', NULL);

-- 覆盖写入（产生新快照，旧快照保留）
INSERT OVERWRITE iceberg_db.orders
SELECT * FROM iceberg_db.orders WHERE create_time >= TIMESTAMP '2024-01-01 00:00:00';
```

#### 3.2.4 快照查询与时间旅行

```sql
-- 查看表的快照历史
SELECT snapshot_id, committed_at, operation, summary
FROM iceberg_db.orders.snapshots
ORDER BY committed_at DESC;

-- 查看某个快照的数据（时间旅行）
SELECT * FROM iceberg_db.orders VERSION AS OF 38291028374;

-- 基于时间戳的时间旅行
SELECT * FROM iceberg_db.orders TIMESTAMP AS OF '2024-01-15 10:00:00';

-- 查看两次快照之间的变更
SELECT * FROM iceberg_db.orders.incremental
WHERE snapshot_id BETWEEN 38291028370 AND 38291028374;

-- 查看数据文件信息
SELECT file_path, file_format, record_count, file_size_in_bytes, partition
FROM iceberg_db.orders.files;

-- 查看表的历史变更
SELECT made_current_at, snapshot_id, is_current_ancestor
FROM iceberg_db.orders.history;
```

#### 3.2.5 Schema演化

```sql
-- 加列（不影响已有数据，无需重写）
ALTER TABLE iceberg_db.orders ADD COLUMN coupon_amount DECIMAL(10, 2) DEFAULT 0;

-- 加嵌套列
ALTER TABLE iceberg_db.orders ADD COLUMN shipping_address STRUCT<
    province: STRING,
    city: STRING,
    district: STRING,
    detail: STRING
>;

-- 改列名
ALTER TABLE iceberg_db.orders RENAME COLUMN order_status TO status;

-- 改列类型（Iceberg支持安全的类型拓宽）
ALTER TABLE iceberg_db.orders ALTER COLUMN total_amount TYPE DECIMAL(20, 2);

-- 删列（逻辑删除，旧数据仍可读取）
ALTER TABLE iceberg_db.orders DROP COLUMN coupon_amount;

-- 列顺序调整
ALTER TABLE iceberg_db.orders ALTER COLUMN payment_amount FIRST;
ALTER TABLE iceberg_db.orders ALTER COLUMN total_amount AFTER order_id;

-- 验证Schema演化后旧数据仍可查询
SELECT order_id, total_amount, status
FROM iceberg_db.orders TIMESTAMP AS OF '2024-01-15 10:00:00'
LIMIT 10;
```

#### 3.2.6 分区演化

```sql
-- 查看当前分区策略
SELECT * FROM iceberg_db.orders.partitions;

-- 从按天分区改为按月分区（无需重写数据！）
ALTER TABLE iceberg_db.orders REPLACE PARTITION FIELD days(create_time) WITH months(create_time);

-- 新数据按月分区写入，旧数据仍按天分区存储
-- 查询时Iceberg自动处理两种分区布局

-- 添加分区字段（多级分区）
ALTER TABLE iceberg_db.orders ADD PARTITION FIELD bucket(16, user_id);

-- 删除分区字段
ALTER TABLE iceberg_db.orders DROP PARTITION FIELD months(create_time);
```

#### 3.2.7 行级更新与删除

```sql
-- 行级更新（Iceberg通过Morally操作实现，不需要重写整个文件）
UPDATE iceberg_db.orders
SET status = '已支付', pay_time = CURRENT_TIMESTAMP()
WHERE order_id = 999901;

-- 行级删除
DELETE FROM iceberg_db.orders
WHERE status = '已取消' AND create_time < TIMESTAMP '2024-01-01 00:00:00';

-- 条件更新（批量更新订单状态）
UPDATE iceberg_db.orders
SET status = '已完成', finish_time = CURRENT_TIMESTAMP()
WHERE status = '已支付' AND pay_time < CURRENT_TIMESTAMP() - INTERVAL 7 DAYS;

-- 合并写入（MERGE INTO，类似UPSERT）
MERGE INTO iceberg_db.orders t
USING (SELECT * FROM incremental_orders) s
ON t.order_id = s.order_id
WHEN MATCHED THEN UPDATE SET *
WHEN NOT MATCHED THEN INSERT *;
```

### 3.3 Flink + Iceberg实时写入

```sql
-- Flink SQL: 实时写入Iceberg表

-- 1. 创建Kafka源表
CREATE TABLE kafka_orders (
    order_id BIGINT,
    user_id BIGINT,
    order_status STRING,
    total_amount DECIMAL(12, 2),
    create_time TIMESTAMP(3),
    WATERMARK FOR create_time AS create_time - INTERVAL '5' SECOND,
    PRIMARY KEY (order_id) NOT ENFORCED
) WITH (
    'connector' = 'upsert-kafka',
    'topic' = 'orders',
    'properties.bootstrap.servers' = 'localhost:9092',
    'key.format' = 'json',
    'value.format' = 'json'
);

-- 2. 创建Iceberg Sink表
CREATE TABLE iceberg_sink_orders (
    order_id BIGINT,
    user_id BIGINT,
    order_status STRING,
    total_amount DECIMAL(12, 2),
    create_time TIMESTAMP(3)
) WITH (
    'connector' = 'iceberg',
    'catalog-name' = 'iceberg',
    'catalog-type' = 'hive',
    'uri' = 'thrift://hive-metastore:9083',
    'warehouse' = 's3a://warehouse/iceberg',
    'write.format.default' = 'parquet',
    'write.upsert.enabled' = 'true'
);

-- 3. 实时写入（Upsert模式）
INSERT INTO iceberg_sink_orders
SELECT order_id, user_id, order_status, total_amount, create_time
FROM kafka_orders;
```

```java
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.table.api.bridge.java.StreamTableEnvironment;

public class FlinkIcebergSink {
    public static void main(String[] args) throws Exception {
        StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
        env.enableCheckpointing(60000);
        StreamTableEnvironment tEnv = StreamTableEnvironment.create(env);

        tEnv.executeSql(
            "CREATE TABLE kafka_orders (" +
            "  order_id BIGINT," +
            "  user_id BIGINT," +
            "  order_status STRING," +
            "  total_amount DECIMAL(12, 2)," +
            "  create_time TIMESTAMP(3)," +
            "  PRIMARY KEY (order_id) NOT ENFORCED" +
            ") WITH (" +
            "  'connector' = 'upsert-kafka'," +
            "  'topic' = 'orders'," +
            "  'properties.bootstrap.servers' = 'localhost:9092'," +
            "  'key.format' = 'json'," +
            "  'value.format' = 'json'" +
            ")"
        );

        tEnv.executeSql(
            "CREATE TABLE iceberg_sink_orders (" +
            "  order_id BIGINT," +
            "  user_id BIGINT," +
            "  order_status STRING," +
            "  total_amount DECIMAL(12, 2)," +
            "  create_time TIMESTAMP(3)" +
            ") WITH (" +
            "  'connector' = 'iceberg'," +
            "  'catalog-name' = 'iceberg'," +
            "  'catalog-type' = 'hive'," +
            "  'uri' = 'thrift://hive-metastore:9083'," +
            "  'warehouse' = 's3a://warehouse/iceberg'," +
            "  'write.upsert.enabled' = 'true'" +
            ")"
        );

        tEnv.executeSql(
            "INSERT INTO iceberg_sink_orders " +
            "SELECT order_id, user_id, order_status, total_amount, create_time " +
            "FROM kafka_orders"
        );

        env.execute("Flink Iceberg Sink Job");
    }
}
```

### 3.4 Trino查询Iceberg表

```sql
-- Trino中查询Iceberg表
-- 需要在Trino中配置Iceberg Catalog:
-- connector.name=iceberg
-- iceberg.catalog.type=hive_metastore
-- hive.metastore.uri=thrift://hive-metastore:9083

-- 查询数据
SELECT
    shipping_province,
    COUNT(*) AS order_count,
    SUM(total_amount) AS total_amount
FROM iceberg_db.orders
WHERE create_time >= TIMESTAMP '2024-01-01'
GROUP BY shipping_province
ORDER BY total_amount DESC;

-- 时间旅行查询
SELECT * FROM iceberg_db.orders
WHERE create_time >= TIMESTAMP '2024-01-01'
VERSION AS OF 38291028374;

-- 查看快照
SELECT snapshot_id, committed_at, operation
FROM iceberg_db.orders.snapshots;

-- 查看数据文件
SELECT file_path, record_count, file_size_in_bytes
FROM iceberg_db.orders.files;
```

---

## 四、Delta Lake

### 4.1 Delta Lake核心机制

```
Delta Lake事务日志（_delta_log）：

  ┌──────────────────────────────────────────────────────────┐
  │  _delta_log/                                             │
  │  ├── 00000000000000000000.json  ← 版本0（首次创建）       │
  │  ├── 00000000000000000001.json  ← 版本1（第一次写入）     │
  │  ├── 00000000000000000002.json  ← 版本2（第二次写入）     │
  │  ├── ...                                                 │
  │  ├── 00000000000000000010.checkpoint.parquet  ← 检查点    │
  │  └── 00000000000000000011.json  ← 版本11                 │
  │                                                          │
  │  每个JSON文件记录:                                        │
  │  {                                                       │
  │    "commitInfo": {"timestamp": 1705306425, ...},         │
  │    "add": {                                              │
  │      "path": "part-00000.parquet",                       │
  │      "size": 134217728,                                  │
  │      "partitionValues": {"dt": "2024-01-15"},            │
  │      "stats": {"numRecords": 50000, ...}                 │
  │    },                                                    │
  │    "remove": {                                           │
  │      "path": "part-00001.parquet",                       │
  │      "deletionTimestamp": 1705306425                     │
  │    }                                                     │
  │  }                                                       │
  │                                                          │
  │  事务日志的核心作用:                                       │
  │  1. 原子性: 写入时先写日志，再写数据文件                    │
  │  2. 一致性: 读操作只看已提交的版本                          │
  │  3. 时间旅行: 每个版本号对应一个完整快照                    │
  │  4. 审计: 所有变更都有记录                                 │
  └──────────────────────────────────────────────────────────┘
```

### 4.2 Spark + Delta Lake实战

#### 4.2.1 创建Delta表

```sql
-- 创建Delta表
CREATE TABLE delta_db.orders (
    order_id BIGINT,
    user_id BIGINT,
    order_status STRING,
    total_amount DECIMAL(12, 2),
    payment_amount DECIMAL(12, 2),
    shipping_province STRING,
    shipping_city STRING,
    create_time TIMESTAMP,
    pay_time TIMESTAMP
)
USING delta
PARTITIONED BY (dt STRING)
TBLPROPERTIES (
    'delta.logRetentionDuration' = 'interval 30 days',
    'delta.checkpointInterval' = '10',
    'delta.autoOptimize.autoCompact' = 'true',
    'delta.autoOptimize.optimizeWrite' = 'true'
);

-- 基于路径创建Delta表
CREATE TABLE delta_db.orders_path
USING delta
LOCATION 's3a://warehouse/delta/orders';
```

#### 4.2.2 ACID写入

```sql
-- 追加写入
INSERT INTO delta_db.orders
SELECT
    order_id, user_id, order_status, total_amount,
    payment_amount, shipping_province, shipping_city,
    create_time, pay_time, DATE(create_time) AS dt
FROM staging_orders;

-- 原子性覆盖写（整个操作要么全部成功，要么全部失败）
INSERT OVERWRITE delta_db.orders
SELECT * FROM refined_orders WHERE dt = '2024-01-15';

-- 行级更新
UPDATE delta_db.orders
SET order_status = '已支付', pay_time = CURRENT_TIMESTAMP()
WHERE order_id = 999901;

-- 行级删除
DELETE FROM delta_db.orders
WHERE order_status = '已取消' AND create_time < TIMESTAMP '2024-01-01';

-- MERGE INTO（Upsert）
MERGE INTO delta_db.orders t
USING staging_orders s
ON t.order_id = s.order_id
WHEN MATCHED AND s.order_status != t.order_status THEN
    UPDATE SET *
WHEN NOT MATCHED THEN INSERT *;
```

#### 4.2.3 OPTIMIZE与Z-ORDER

```sql
-- OPTIMIZE: 合并小文件，提升查询性能
OPTIMIZE delta_db.orders;

-- 只优化特定分区
OPTIMIZE delta_db.orders
WHERE dt >= '2024-01-01' AND dt <= '2024-01-31';

-- Z-ORDER: 按指定列排序数据，加速过滤查询
-- Z-ORDER将相关数据放在同一文件中，跳过不相关文件
OPTIMIZE delta_db.orders
ZORDER BY (user_id, shipping_province);

-- Z-ORDER的原理:
--   查询 WHERE user_id = 5001
--   无Z-ORDER: 扫描所有文件 → 慢
--   有Z-ORDER: 只扫描user_id=5001所在文件 → 快

-- 查看OPTIMIZE效果
DESCRIBE HISTORY delta_db.orders;
```

#### 4.2.4 时间旅行

```sql
-- 查看表历史
DESCRIBE HISTORY delta_db.orders;

-- 基于版本号的时间旅行
SELECT * FROM delta_db.orders VERSION AS OF 5;

-- 基于时间戳的时间旅行
SELECT * FROM delta_db.orders TIMESTAMP AS OF '2024-01-15 10:00:00';

-- 回滚到指定版本
RESTORE TABLE delta_db.orders TO VERSION AS OF 5;

-- 查看两个版本之间的变更
SELECT * FROM delta_db.orders VERSION AS OF 5
EXCEPT
SELECT * FROM delta_db.orders VERSION AS OF 4;

-- 设置数据保留时间（默认7天，生产建议30天）
ALTER TABLE delta_db.orders SET TBLPROPERTIES (
    'delta.logRetentionDuration' = 'interval 30 days',
    'delta.deletedFileRetentionDuration' = 'interval 7 days'
);
```

#### 4.2.5 Delta Lake工具命令

```sql
-- 查看表详情
DESCRIBE DETAIL delta_db.orders;

-- 查看Delta日志
DESCRIBE HISTORY delta_db.orders;

-- 查看文件列表
SELECT * FROM delta_db.orders_files;

-- 真空清理（删除不再被引用的旧文件）
VACUUM delta_db.orders RETAIN 168 HOURS;

-- 转换Parquet表为Delta表
CONVERT TO DELTA parquet.`s3a://warehouse/parquet/orders`
PARTITIONED BY (dt STRING);

-- 转换Hive表为Delta表
CONVERT TO DELTA hive_db.ods_order_info;
```

---

## 五、Apache Hudi

### 5.1 Hudi核心概念

```
Hudi的两种表类型:

  COW (Copy On Write - 写时复制):
  ┌──────────────────────────────────────────────────────────┐
  │  写入: 每次更新 → 读取旧Parquet文件 → 合并 → 写新Parquet │
  │  读取: 直接读Parquet文件，性能最好                        │
  │                                                          │
  │  适合: 读多写少，批量写入场景                              │
  │                                                          │
  │  ┌──────┐   UPDATE    ┌──────────┐   ┌──────┐           │
  │  │ V1   │ ──────────→ │ 合并V1+Δ │ → │ V2   │           │
  │  └──────┘             └──────────┘   └──────┘           │
  │                                                          │
  │  缺点: 写放大严重（改一行要重写整个文件）                   │
  └──────────────────────────────────────────────────────────┘

  MOR (Merge On Read - 读时合并):
  ┌──────────────────────────────────────────────────────────┐
  │  写入: 更新 → 追加到Log文件(Avro)，不修改基础文件          │
  │  读取: 基础Parquet文件 + Log文件 → 运行时合并              │
  │                                                          │
  │  适合: 写多读少，频繁Upsert场景                            │
  │                                                          │
  │  ┌──────┐                                               │
  │  │ V1   │ ← 基础文件(Parquet)                            │
  │  └──┬───┘                                               │
  │     │  +                                                 │
  │  ┌──▼───┐                                               │
  │  │ Δ1   │ ← 增量Log(Avro)                               │
  │  └──┬───┘                                               │
  │     │  +                                                 │
  │  ┌──▼───┐                                               │
  │  │ Δ2   │ ← 增量Log(Avro)                               │
  │  └──────┘                                               │
  │                                                          │
  │  优点: 写入快（追加Log即可）                               │
  │  缺点: 读取时需要合并，查询性能略低                        │
  └──────────────────────────────────────────────────────────┘

Compaction策略（MOR表的Log合并）:
  - 基于提交次数: 每5次提交触发一次Compaction
  - 基于Log文件大小: Log文件超过阈值时触发
  - 基于时间: 每小时触发一次
```

### 5.2 Spark + Hudi实战

```sql
-- 创建Hudi COW表
CREATE TABLE hudi_db.orders_cow (
    order_id BIGINT,
    user_id BIGINT,
    order_status STRING,
    total_amount DECIMAL(12, 2),
    create_time TIMESTAMP,
    ts TIMESTAMP
)
USING hudi
TBLPROPERTIES (
    'primaryKey' = 'order_id',
    'type' = 'cow',
    'preCombineField' = 'ts',
    'hoodie.upsert.shuffle.parallelism' = '200',
    'hoodie.insert.shuffle.parallelism' = '200'
);

-- 创建Hudi MOR表
CREATE TABLE hudi_db.orders_mor (
    order_id BIGINT,
    user_id BIGINT,
    order_status STRING,
    total_amount DECIMAL(12, 2),
    create_time TIMESTAMP,
    ts TIMESTAMP
)
USING hudi
TBLPROPERTIES (
    'primaryKey' = 'order_id',
    'type' = 'mor',
    'preCombineField' = 'ts',
    'hoodie.compact.inline' = 'true',
    'hoodie.compact.inline.max.delta.commits' = '5',
    'hoodie.upsert.shuffle.parallelism' = '200'
);

-- Upsert写入
MERGE INTO hudi_db.orders_cow t
USING staging_orders s
ON t.order_id = s.order_id
WHEN MATCHED THEN UPDATE SET *
WHEN NOT MATCHED THEN INSERT *;

-- 增量查询（只看变更数据）
SELECT * FROM hudi_db.orders_cow
WHERE `_hoodie_commit_time` >= '20240115100000';

-- 时间旅行
SELECT * FROM hudi_db.orders_cow TIMESTAMP AS OF '2024-01-15 10:00:00';
```

---

## 六、三者对比

### 6.1 功能对比

| 特性 | Iceberg | Delta Lake | Hudi |
|------|---------|------------|------|
| ACID事务 | ✅ 快照隔离 | ✅ 事务日志 | ✅ MVCC |
| Schema演化 | ✅ 最强（加/删/改名/改类型/重排） | ✅ 支持（部分限制） | ✅ 支持 |
| 分区演化 | ✅ 隐藏分区，无需重写数据 | ❌ 需要重写 | ❌ 需要重写 |
| 行级更新 | ✅ Position/Delete文件 | ✅ 直接支持 | ✅ 最强（COW/MOR） |
| 时间旅行 | ✅ 快照ID/时间戳 | ✅ 版本号/时间戳 | ✅ 提交时间 |
| 多引擎支持 | ✅ Spark/Flink/Trino/Presto/Dremio | ⚠️ 主要Spark生态 | ⚠️ Spark/Flink/Presto |
| 增量读取 | ✅ 增量快照 | ❌ 不原生支持 | ✅ 最强（原生增量查询） |
| 小文件合并 | ✅ Rewrite Data File | ✅ OPTIMIZE | ✅ Clustering |
| 数据压缩 | ✅ Parquet/ORC/Avro | ✅ Parquet | ✅ Parquet + Avro Log |
| 开源治理 | Apache基金会 | Linux基金会（Databricks主导） | Apache基金会 |
| 社区活跃度 | 高（Netflix/Apple/腾讯等） | 高（Databricks主导） | 高（Uber/阿里等） |

### 6.2 选型建议

```
选型决策树:

  你的主要计算引擎是什么？
  │
  ├─→ 主要是Spark，且深度使用Databricks平台
  │     → Delta Lake（与Spark/Databricks深度集成，开箱即用）
  │
  ├─→ 多引擎混合（Spark + Flink + Trino）
  │     → Iceberg（引擎中立，开放性最好）
  │
  └─→ 高频Upsert场景（CDC同步、实时更新）
        → Hudi（Upsert性能最强，增量查询原生支持）

  特殊场景:
  - 需要频繁改分区策略 → Iceberg（唯一支持分区演化）
  - 需要Z-ORDER加速查询 → Delta Lake
  - 需要增量消费变更 → Hudi或Iceberg
  - 需要Avro格式支持 → Iceberg或Hudi
  - 已有Hive数仓想迁移 → Iceberg（兼容性最好）
```

### 6.3 性能对比参考

```
测试场景: 1亿行订单数据，TPC-DS风格查询

  查询性能（相对值，越低越好）:
  ┌──────────────────────────────────────────────────┐
  │  查询类型      Iceberg   Delta   Hudi(COW)        │
  │  ─────────────────────────────────────────────── │
  │  全表扫描      1.0x      1.0x    1.0x             │
  │  分区裁剪      1.0x      1.0x    1.0x             │
  │  点查询        1.2x      1.0x    1.5x             │
  │  聚合查询      1.0x      1.1x    1.2x             │
  │  Upsert写入   1.5x      1.3x    1.0x（最快）      │
  │                                                  │
  │  注: 实际性能因数据特征、集群配置而异              │
  └──────────────────────────────────────────────────┘
```

---

## 七、课堂练习（60min）

### 练习1：Docker启动Spark + Iceberg环境（15min）

```yaml
# docker-compose-iceberg.yml
version: '3.8'

services:
  minio:
    image: minio/minio:latest
    ports:
      - "9000:9000"
      - "9001:9001"
    environment:
      MINIO_ROOT_USER: admin
      MINIO_ROOT_PASSWORD: admin123456
    command: server /data --console-address ":9001"
    volumes:
      - minio_data:/data

  hive-metastore:
    image: apache/hive:3.1.3
    ports:
      - "9083:9083"
    environment:
      SERVICE_NAME: metastore
      IS_RESUME: "true"
    volumes:
      - hive_data:/opt/hive/data

  spark:
    image: tabulario/spark-iceberg:latest
    depends_on:
      - minio
      - hive-metastore
    ports:
      - "8080:8080"
      - "7077:7077"
      - "10000:10000"
    environment:
      - SPARK_HOME=/opt/spark
    volumes:
      - ./notebooks:/home/iceberg/notebooks

  trino:
    image: trinodb/trino:435
    ports:
      - "8081:8080"
    volumes:
      - ./trino/catalog:/etc/trino/catalog

volumes:
  minio_data:
  hive_data:
```

```bash
# 启动环境
docker-compose -f docker-compose-iceberg.yml up -d

# 进入Spark SQL
docker exec -it spark-iceberg spark-sql \
    --conf spark.sql.catalog.iceberg=org.apache.iceberg.spark.SparkCatalog \
    --conf spark.sql.catalog.iceberg.type=hive \
    --conf spark.sql.catalog.iceberg.uri=thrift://hive-metastore:9083 \
    --conf spark.sql.catalog.iceberg.warehouse=s3a://warehouse/iceberg \
    --conf spark.sql.extensions=org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions \
    --conf spark.hadoop.fs.s3a.endpoint=http://minio:9000 \
    --conf spark.hadoop.fs.s3a.access.key=admin \
    --conf spark.hadoop.fs.s3a.secret.key=admin123456 \
    --conf spark.hadoop.fs.s3a.path.style.access=true
```

### 练习2：创建Iceberg表，执行CRUD操作（15min）

```sql
-- 创建数据库
CREATE DATABASE IF NOT EXISTS iceberg_db;
USE iceberg_db;

-- 创建Iceberg表
CREATE TABLE iceberg_db.products (
    product_id BIGINT,
    product_name STRING,
    category STRING,
    price DECIMAL(10, 2),
    stock INT,
    status STRING,
    update_time TIMESTAMP
)
USING iceberg
PARTITIONED BY (category)
TBLPROPERTIES ('write.format.default' = 'parquet');

-- 插入数据
INSERT INTO iceberg_db.products VALUES
    (1, 'iPhone 15', '手机数码', 6999.00, 500, '上架', CURRENT_TIMESTAMP()),
    (2, 'MacBook Pro', '电脑办公', 14999.00, 200, '上架', CURRENT_TIMESTAMP()),
    (3, 'AirPods Pro', '手机数码', 1899.00, 1000, '上架', CURRENT_TIMESTAMP()),
    (4, '戴森吹风机', '家用电器', 3190.00, 300, '上架', CURRENT_TIMESTAMP()),
    (5, 'Nike跑鞋', '运动户外', 899.00, 800, '上架', CURRENT_TIMESTAMP());

-- 查询数据
SELECT * FROM iceberg_db.products;

-- 更新数据
UPDATE iceberg_db.products SET price = 6799.00 WHERE product_id = 1;

-- 删除数据
DELETE FROM iceberg_db.products WHERE product_id = 5;

-- 查看快照
SELECT snapshot_id, committed_at, operation FROM iceberg_db.products.snapshots;
```

### 练习3：体验Schema演化（15min）

```sql
-- 加列
ALTER TABLE iceberg_db.products ADD COLUMN brand STRING;

-- 验证旧数据仍可查询（新列为NULL）
SELECT product_id, product_name, brand FROM iceberg_db.products;

-- 更新新列的值
UPDATE iceberg_db.products SET brand = 'Apple' WHERE product_id IN (1, 2, 3);
UPDATE iceberg_db.products SET brand = 'Dyson' WHERE product_id = 4;

-- 改列名
ALTER TABLE iceberg_db.products RENAME COLUMN status TO product_status;

-- 改列类型
ALTER TABLE iceberg_db.products ALTER COLUMN price TYPE DECIMAL(12, 2);

-- 验证所有数据仍可正常查询
SELECT * FROM iceberg_db.products;
```

### 练习4：体验时间旅行（15min）

```sql
-- 记录当前快照ID
SELECT snapshot_id, committed_at, operation
FROM iceberg_db.products.snapshots
ORDER BY committed_at;

-- 继续修改数据
INSERT INTO iceberg_db.products VALUES
    (6, 'iPad Air', '电脑办公', 4799.00, 600, '上架', CURRENT_TIMESTAMP(), 'Apple');

UPDATE iceberg_db.products SET stock = 450 WHERE product_id = 1;

-- 查看最新数据
SELECT * FROM iceberg_db.products;

-- 时间旅行：回到修改前的快照
SELECT * FROM iceberg_db.products VERSION AS OF <之前的snapshot_id>;

-- 基于时间戳的时间旅行
SELECT * FROM iceberg_db.products TIMESTAMP AS OF '2024-01-15 10:00:00';

-- 查看表的历史变更
SELECT made_current_at, snapshot_id, is_current_ancestor
FROM iceberg_db.products.history;
```

---

## 八、课后作业

### 必做

1. **Hive→Iceberg迁移**：将L1项目4的Hive数仓迁移到Iceberg格式，至少完成ODS和DWD两层
2. **性能对比**：对比Hive vs Iceberg在相同查询下的性能差异（至少5个查询），记录查询时间
3. **技术Blog**：写一篇"Iceberg vs Delta Lake选型分析"技术Blog（1500字以上），包含：
   - 各自的核心机制对比
   - 适用场景分析
   - 选型决策建议
   - 生产环境注意事项

### 选做

1. 搭建Delta Lake环境，体验OPTIMIZE和Z-ORDER
2. 搭建Hudi环境，对比COW和MOR的写入与查询性能
3. 实现Flink CDC → Iceberg的实时数据管道

---

## 九、参考资料

- [Apache Iceberg官方文档](https://iceberg.apache.org/docs/latest/)
- [Delta Lake官方文档](https://docs.delta.io/latest/index.html)
- [Apache Hudi官方文档](https://hudi.apache.org/docs/latest/)
- [Iceberg Delta Hudi对比论文: Data Lakehouse Systems](https://dl.acm.org/doi/10.14778/3551793.3551803)
- [Tabulario Spark-Iceberg Docker镜像](https://hub.docker.com/r/tabulario/spark-iceberg)
