# 课时13：Hive数据仓库入门

> **课时时长**：8小时（理论3h + 实验3h + 练习2h）
>
> **难度等级**：⭐⭐⭐ 重要基础

---

## 一、教学目标

1. **理解Hive架构与设计思想**：Hive如何将SQL翻译成MapReduce/Tez/Spark作业
2. **掌握HiveQL与SQL的异同**：能用HiveQL完成日常数据开发任务
3. **精通分区表和分桶表**：理解分区裁剪原理，能设计高效的分区策略
4. **掌握文件格式选择**：能对比TextFile、Parquet、ORC的性能差异并做出合理选择
5. **理解内部表vs外部表**：清楚两者的区别和各自适用场景
6. **能独立完成数据分析**：从建表到查询到优化，全流程掌握

---

## 二、教学内容

### 2.1 Hive的设计哲学（30min）

**Hive不是什么：**

```
Hive ❌ 不是传统的关系型数据库！
  - 不支持行级更新（或效率极低）
  - 不支持事务（Hive 3.0+有ACID支持但不推荐用于OLTP）
  - 查询延迟高（秒级到分钟级，不是毫秒级）
  - 不支持索引（或者说索引和RDBMS完全不同）

Hive ✅ 是什么：
  - 构建在HDFS之上的数据仓库工具
  - 将SQL(HiveQL)翻译成MapReduce/Tez/Spark作业
  - 适合大规模批量数据处理（ETL、报表）
  - 适合"一次写入，多次读取"的场景
```

**Hive架构图：**

```
┌────────────────────────────────────────────────────────────┐
│                       用户接口层                             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌───────────┐ │
│  │  Hive    │  │  JDBC    │  │  ODBC    │  │  Hive     │ │
│  │  CLI     │  │  Client  │  │  Client  │  │  Web UI   │ │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └─────┬─────┘ │
└───────┼──────────────┼─────────────┼─────────────┼───────┘
        └──────────────┼─────────────┼─────────────┘
                       ▼             ▼
┌────────────────────────────────────────────────────────────┐
│                     Driver（驱动器）                          │
│  ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌─────────┐ │
│  │ SQL解析器   │→│ 编译器      │→│ 优化器      │→│ 执行器   │ │
│  │(Parser)    │ │(Compiler)  │ │(Optimizer) │ │(Executor)│ │
│  └────────────┘ └────────────┘ └────────────┘ └────┬────┘ │
└────────────────────────────────────────────────────┼───────┘
                                                     │
        ┌────────────────────────────────────────────┼───┐
        │                Metastore                    │   │
        │  ┌──────────────────────────────────────┐  │   │
        │  │  MySQL/PostgreSQL (存储元数据)         │  │   │
        │  │  - 表结构(列名、类型)                  │  │   │
        │  │  - 分区信息                           │  │   │
        │  │  - HDFS存储路径                       │  │   │
        │  │  - SerDe序列化信息                    │  │   │
        │  └──────────────────────────────────────┘  │   │
        └────────────────────────────────────────────┘   │
                                                         ▼
┌────────────────────────────────────────────────────────────┐
│                     执行引擎层                               │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐                 │
│  │MapReduce │  │   Tez    │  │  Spark   │   (可插拔)       │
│  └──────────┘  └──────────┘  └──────────┘                 │
└────────────────────────────────────────────────────────────┘
        │             │             │
        ▼             ▼             ▼
┌────────────────────────────────────────────────────────────┐
│                  HDFS (数据存储层)                           │
│  /warehouse/db_name/table_name/                            │
│  /warehouse/db_name/table_name/dt=2024-01-01/              │
└────────────────────────────────────────────────────────────┘
```

**一条HiveQL的旅程：**

```sql
SELECT category_id, COUNT(*) 
FROM products 
WHERE price > 100 
GROUP BY category_id;

↓ Hive Driver接收

1. Parser（解析器）: 
   解析SQL语法 → 生成AST(抽象语法树)

2. Compiler（编译器）: 
   AST → 逻辑执行计划 → 查询Block树

3. Optimizer（优化器）: 
   - 谓词下推(Predicate Pushdown): WHERE提前执行
   - 列裁剪(Column Pruning): 只读需要的列
   - 分区裁剪(Partition Pruning): 只扫描需要的分区
   - Join优化: Map Join vs Reduce Join

4. Executor（执行器）: 
   优化后的计划 → 提交给执行引擎(MapReduce/Tez/Spark)
   执行引擎 → 读取HDFS数据 → 执行计算 → 写回HDFS
```

---

### 2.2 内部表 vs 外部表（30min）

| 特性 | 内部表 (MANAGED_TABLE) | 外部表 (EXTERNAL_TABLE) |
|------|----------------------|------------------------|
| 数据存储位置 | 由Hive管理（默认在/warehouse/） | 用户指定LOCATION |
| 删除表行为 | 删除元数据 + 删除HDFS数据 | 只删除元数据，HDFS数据保留 |
| 适用场景 | ETL中间表、临时表 | ODS层原始数据、与其他组件共享 |
| 权限控制 | Hive完全控制 | 可以外部管理 |

```sql
-- 内部表示例
CREATE TABLE managed_orders (
    order_id BIGINT,
    user_id BIGINT,
    amount DECIMAL(10,2)
)
STORED AS ORC;

-- 删除内部表 → 元数据和HDFS数据都被删除
DROP TABLE managed_orders;


-- 外部表示例
CREATE EXTERNAL TABLE external_orders (
    order_id BIGINT,
    user_id BIGINT,
    amount DECIMAL(10,2)
)
STORED AS PARQUET
LOCATION '/data/external/orders';

-- 删除外部表 → 只删除元数据，HDFS数据保留
DROP TABLE external_orders;

-- 查看表类型
DESCRIBE FORMATTED orders;
-- 查找 Table Type 字段: MANAGED_TABLE 或 EXTERNAL_TABLE
```

---

### 2.3 分区表（Partition Table）（60min）

**为什么需要分区？**

```
没有分区:
  SELECT * FROM orders WHERE dt = '2024-01-01';
  → 需要扫描整个orders表（可能包含365天×数百GB的数据）
  → 耗时: 数十分钟

有分区:
  SELECT * FROM orders WHERE dt = '2024-01-01';
  → 只扫描 dt='2024-01-01' 这一个分区
  → 耗时: 数秒
```

**分区表DDL和操作：**

```sql
-- ============================================
-- 1. 创建分区表（生产标准写法）
-- ============================================
CREATE EXTERNAL TABLE user_behavior (
    user_id BIGINT COMMENT '用户ID',
    item_id BIGINT COMMENT '商品ID',
    category_id INT COMMENT '品类ID',
    behavior STRING COMMENT '行为类型: pv/buy/cart/fav',
    ts BIGINT COMMENT '行为时间戳'
)
COMMENT '用户行为日志表'
PARTITIONED BY (
    dt STRING COMMENT '日期分区 yyyy-MM-dd',
    hr STRING COMMENT '小时分区 HH'
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe'
STORED AS PARQUET
LOCATION '/warehouse/user_behavior'
TBLPROPERTIES (
    'parquet.compression'='SNAPPY',
    'creator'='data_team',
    'created_date'='2024-01-01'
);


-- ============================================
-- 2. 加载分区数据
-- ============================================

-- 方式1: 从HDFS目录加载分区
ALTER TABLE user_behavior 
ADD PARTITION (dt='2024-01-01', hr='00')
LOCATION '/data/user_behavior/dt=2024-01-01/hr=00';

ALTER TABLE user_behavior 
ADD PARTITION (dt='2024-01-01', hr='01')
LOCATION '/data/user_behavior/dt=2024-01-01/hr=01';

-- 方式2: 批量添加分区
ALTER TABLE user_behavior ADD
    PARTITION (dt='2024-01-01', hr='02') LOCATION '/data/user_behavior/dt=2024-01-01/hr=02'
    PARTITION (dt='2024-01-01', hr='03') LOCATION '/data/user_behavior/dt=2024-01-01/hr=03'
    PARTITION (dt='2024-01-02', hr='00') LOCATION '/data/user_behavior/dt=2024-01-02/hr=00';

-- 方式3: 使用MSCK修复分区（自动发现HDFS目录中的分区）
MSCK REPAIR TABLE user_behavior;

-- 方式4: 动态分区插入（从其他表加载数据）
SET hive.exec.dynamic.partition=true;
SET hive.exec.dynamic.partition.mode=nonstrict;

INSERT OVERWRITE TABLE user_behavior PARTITION (dt, hr)
SELECT 
    user_id, item_id, category_id, behavior, ts,
    dt, hr
FROM user_behavior_staging;


-- ============================================
-- 3. 查看分区信息
-- ============================================

-- 查看所有分区
SHOW PARTITIONS user_behavior;

-- 查看特定日期的分区
SHOW PARTITIONS user_behavior PARTITION(dt='2024-01-01');

-- 查看分区详细信息
DESCRIBE FORMATTED user_behavior PARTITION(dt='2024-01-01', hr='00');


-- ============================================
-- 4. 删除分区
-- ============================================

-- 删除单个分区
ALTER TABLE user_behavior DROP PARTITION (dt='2024-01-01', hr='00');

-- 删除范围分区（删除2024年1月1日的所有小时分区）
ALTER TABLE user_behavior DROP PARTITION (dt='2024-01-01', hr<='23');


-- ============================================
-- 5. 分区查询（分区裁剪）
-- ============================================

-- ✅ 好查询：指定了分区条件，只扫描选定分区
SELECT category_id, COUNT(*) as pv
FROM user_behavior
WHERE dt = '2024-01-01' 
  AND hr BETWEEN '08' AND '22'
  AND behavior = 'buy'
GROUP BY category_id
ORDER BY pv DESC;

-- ❌ 坏查询：没有指定分区条件，全表扫描
SELECT category_id, COUNT(*) as pv
FROM user_behavior
WHERE behavior = 'buy'
GROUP BY category_id;

-- 查看查询是否使用了分区裁剪
EXPLAIN 
SELECT category_id, COUNT(*) as pv
FROM user_behavior
WHERE dt = '2024-01-01' AND hr = '12'
GROUP BY category_id;
-- 输出中查找 "partition" 关键词，确认只扫描了1个分区
```

---

### 2.4 分桶表（Bucket Table）（20min）

**分桶 vs 分区：**

```
分区(Partition): 按字段值切分 → 形成子目录
  示例: dt=2024-01-01/hr=00/

分桶(Bucket): 按字段Hash值切分 → 形成子文件
  示例: /dt=2024-01-01/hr=00/000000_0
        /dt=2024-01-01/hr=00/000001_0
        /dt=2024-01-01/hr=00/000002_0
```

```sql
-- 创建分桶表
CREATE TABLE user_bucketed (
    user_id BIGINT,
    username STRING,
    city STRING,
    age INT
)
CLUSTERED BY (user_id) INTO 32 BUCKETS
STORED AS ORC;

-- 分桶的用途:
-- 1. 提高JOIN效率（Bucket Map Join — 两个表按相同字段分桶，Join时直接对应Bucket）
-- 2. 提高Sampling效率（TABLESAMPLE快速抽样）
-- 3. 数据均匀分布，避免倾斜

-- 抽样查询
SELECT * FROM user_bucketed TABLESAMPLE(BUCKET 3 OUT OF 32 ON user_id);
```

---

### 2.5 文件格式深度对比（40min）

**TextFile vs Parquet vs ORC vs Avro：**

| 特性 | TextFile | Parquet | ORC | Avro |
|------|----------|---------|-----|------|
| 存储方式 | 行存储 | 列存储 | 列存储 | 行存储 |
| 压缩率 | 低 | 高(5-10x) | 最高(10-15x) | 中 |
| 查询速度(列) | 慢 | 快 | 最快 | 慢 |
| Schema演化 | 无 | 支持 | 支持 | 支持 |
| 可读性 | 人可读 | 二进制 | 二进制 | 二进制 |
| 适用场景 | 原始日志 | Spark分析 | Hive分析 | Kafka消息 |

**为什么列存储查询快？**

```
假设表有100列，查询只需要其中3列：

行存储(TextFile):
  → 必须读取每一行的所有100列
  → 读取的数据量: 100%

列存储(Parquet/ORC):
  → 只读取需要的3列
  → 读取的数据量: 3%

再加上列存储的压缩优化:
  → 同一列的数据类型相同，压缩率高
  → 可以应用更高效的编码(Delta/Run-Length/Dictionary)
```

**Parquet vs ORC 深入对比：**

```sql
-- Parquet 表
CREATE TABLE data_parquet (
    user_id BIGINT,
    event STRING,
    amount DOUBLE,
    ts TIMESTAMP
)
STORED AS PARQUET
TBLPROPERTIES ('parquet.compression'='SNAPPY');

-- ORC 表
CREATE TABLE data_orc (
    user_id BIGINT,
    event STRING,
    amount DOUBLE,
    ts TIMESTAMP
)
STORED AS ORC
TBLPROPERTIES ('orc.compress'='ZLIB', 'orc.bloom.filter.columns'='user_id');

-- 实验对比SQL
-- 1. 存储空间对比
SELECT 
    'parquet' as format_type,
    SUM(size) / 1024 / 1024 AS size_mb
FROM (
    SELECT 
        SUM(PARQUET_FILE_SIZE) as size
    FROM data_parquet
);

-- 2. 查询性能对比（需分别执行并计时）
SELECT category_id, COUNT(*), SUM(amount)
FROM data_parquet
WHERE dt = '2024-01-01'
GROUP BY category_id;
-- VS
SELECT category_id, COUNT(*), SUM(amount)
FROM data_orc
WHERE dt = '2024-01-01'
GROUP BY category_id;
```

**实际对比数据（参考）：**

```
场景: 100GB原始TEXT数据

| 格式     | 存储空间 | 压缩率 | 全表扫描 | 列查询(3列) |
|----------|---------|--------|---------|------------|
| TextFile | 100GB   | 1x     | 180s    | 180s       |
| Parquet  | 18GB    | 5.5x   | 120s    | 15s        |
| ORC      | 12GB    | 8.3x   | 95s     | 10s        |
```

---

### 2.6 HiveQL常用操作大全（60min）

```sql
-- ============================================
-- 第一部分：建表大全
-- ============================================

-- 1. 直接建表
CREATE TABLE orders (
    order_id BIGINT COMMENT '订单ID',
    user_id BIGINT COMMENT '用户ID',
    product_id BIGINT COMMENT '商品ID',
    amount DECIMAL(10,2) COMMENT '订单金额',
    status STRING COMMENT '订单状态',
    create_time TIMESTAMP COMMENT '创建时间'
)
COMMENT '订单表'
PARTITIONED BY (dt STRING COMMENT '日期')
CLUSTERED BY (user_id) INTO 16 BUCKETS
STORED AS ORC
TBLPROPERTIES (
    'orc.compress'='SNAPPY',
    'orc.create.index'='true'
);

-- 2. CREATE TABLE AS SELECT（从查询结果创建表）
CREATE TABLE daily_order_stats AS
SELECT 
    dt,
    status,
    COUNT(*) as order_count,
    SUM(amount) as total_amount,
    AVG(amount) as avg_amount
FROM orders
WHERE dt BETWEEN '2024-01-01' AND '2024-01-07'
GROUP BY dt, status;

-- 3. CREATE TABLE LIKE（复制表结构）
CREATE TABLE orders_backup LIKE orders;

-- 4. 创建临时表（会话级别，退出后自动删除）
CREATE TEMPORARY TABLE tmp_result AS
SELECT user_id, SUM(amount) as total_spent
FROM orders WHERE dt='2024-01-01'
GROUP BY user_id;


-- ============================================
-- 第二部分：数据导入
-- ============================================

-- 1. 从本地文件加载
LOAD DATA LOCAL INPATH '/home/data/orders.csv' 
OVERWRITE INTO TABLE orders PARTITION (dt='2024-01-01');

-- 2. 从HDFS文件加载
LOAD DATA INPATH 'hdfs:///data/orders/dt=2024-01-01/' 
INTO TABLE orders PARTITION (dt='2024-01-01');

-- 3. INSERT INTO（追加）
INSERT INTO TABLE orders PARTITION (dt='2024-01-02')
VALUES
    (1001, 2001, 3001, 299.99, 'completed', '2024-01-02 10:00:00'),
    (1002, 2002, 3002, 199.99, 'pending', '2024-01-02 10:30:00');

-- 4. INSERT OVERWRITE（覆盖分区）
INSERT OVERWRITE TABLE orders PARTITION (dt='2024-01-02')
SELECT order_id, user_id, product_id, amount, status, create_time
FROM orders_staging
WHERE dt = '2024-01-02';

-- 5. 多分区插入
FROM orders_staging
INSERT OVERWRITE TABLE orders PARTITION (dt='2024-01-01')
SELECT * WHERE dt='2024-01-01' AND status='completed'
INSERT OVERWRITE TABLE orders PARTITION (dt='2024-01-02')
SELECT * WHERE dt='2024-01-02' AND status='completed';


-- ============================================
-- 第三部分：数据导出
-- ============================================

-- 1. 导出到HDFS
INSERT OVERWRITE DIRECTORY '/tmp/export/orders_20240101'
ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
SELECT * FROM orders WHERE dt='2024-01-01';

-- 2. 导出到本地（需要LOCAL关键字）
INSERT OVERWRITE LOCAL DIRECTORY '/tmp/export_orders'
ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t'
SELECT * FROM orders WHERE dt='2024-01-01';


-- ============================================
-- 第四部分：Hive窗口函数（与SQL基本一致）
-- ============================================

-- 1. 排名：每个品类按销售额排名
SELECT 
    category_id,
    product_id,
    amount,
    ROW_NUMBER() OVER (PARTITION BY category_id ORDER BY amount DESC) as rn,
    RANK() OVER (PARTITION BY category_id ORDER BY amount DESC) as rank,
    DENSE_RANK() OVER (PARTITION BY category_id ORDER BY amount DESC) as dense_rnk
FROM product_sales
WHERE dt = '2024-01-01';

-- 2. 偏移：计算环比增长率
SELECT 
    dt,
    daily_amount,
    LAG(daily_amount, 1) OVER (ORDER BY dt) as prev_day_amount,
    ROUND(
        (daily_amount - LAG(daily_amount, 1) OVER (ORDER BY dt)) 
        / LAG(daily_amount, 1) OVER (ORDER BY dt) * 100, 
        2
    ) as growth_rate_pct
FROM daily_stats
WHERE dt >= '2024-01-01'
ORDER BY dt;

-- 3. 累积：计算累计销售额
SELECT 
    dt,
    daily_amount,
    SUM(daily_amount) OVER (
        ORDER BY dt 
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) as cumulative_amount
FROM daily_stats
WHERE dt >= '2024-01-01'
ORDER BY dt;


-- ============================================
-- 第五部分：复杂查询实战
-- ============================================

-- 查询1: 用户行为漏斗分析（浏览→加购→下单→支付）
WITH behavior_funnel AS (
    SELECT 
        user_id,
        SUM(CASE WHEN behavior = 'pv' THEN 1 ELSE 0 END) as pv_count,
        SUM(CASE WHEN behavior = 'cart' THEN 1 ELSE 0 END) as cart_count,
        SUM(CASE WHEN behavior = 'buy' THEN 1 ELSE 0 END) as buy_count,
        SUM(CASE WHEN behavior = 'pay' THEN 1 ELSE 0 END) as pay_count
    FROM user_behavior
    WHERE dt = '2024-01-01'
    GROUP BY user_id
)
SELECT 
    COUNT(DISTINCT CASE WHEN pv_count > 0 THEN user_id END) as pv_users,
    COUNT(DISTINCT CASE WHEN cart_count > 0 THEN user_id END) as cart_users,
    COUNT(DISTINCT CASE WHEN buy_count > 0 THEN user_id END) as buy_users,
    COUNT(DISTINCT CASE WHEN pay_count > 0 THEN user_id END) as pay_users,
    ROUND(COUNT(DISTINCT CASE WHEN cart_count > 0 THEN user_id END) * 100.0 
          / COUNT(DISTINCT CASE WHEN pv_count > 0 THEN user_id END), 2) as pv_to_cart_rate,
    ROUND(COUNT(DISTINCT CASE WHEN buy_count > 0 THEN user_id END) * 100.0 
          / COUNT(DISTINCT CASE WHEN cart_count > 0 THEN user_id END), 2) as cart_to_buy_rate,
    ROUND(COUNT(DISTINCT CASE WHEN pay_count > 0 THEN user_id END) * 100.0 
          / COUNT(DISTINCT CASE WHEN buy_count > 0 THEN user_id END), 2) as buy_to_pay_rate
FROM behavior_funnel;

-- 查询2: 商品关联分析（被一起购买的商品对）
WITH order_products AS (
    SELECT o.order_id, oi.product_id
    FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    WHERE o.dt = '2024-01-01' AND o.status = 'completed'
)
SELECT 
    a.product_id as product_a,
    b.product_id as product_b,
    COUNT(*) as co_occurrence_count
FROM order_products a
JOIN order_products b ON a.order_id = b.order_id AND a.product_id < b.product_id
GROUP BY a.product_id, b.product_id
HAVING COUNT(*) >= 3
ORDER BY co_occurrence_count DESC
LIMIT 20;

-- 查询3: 用户生命周期价值(LTV)计算
WITH user_orders AS (
    SELECT 
        user_id,
        MIN(create_time) as first_order_date,
        MAX(create_time) as last_order_date,
        COUNT(DISTINCT order_id) as order_count,
        SUM(amount) as total_spent
    FROM orders
    WHERE status = 'completed'
    GROUP BY user_id
)
SELECT 
    user_id,
    DATEDIFF(last_order_date, first_order_date) as lifecycle_days,
    order_count,
    total_spent,
    ROUND(total_spent / NULLIF(DATEDIFF(last_order_date, first_order_date), 0), 2) as daily_value,
    CASE 
        WHEN total_spent >= 10000 THEN '高价值'
        WHEN total_spent >= 5000 THEN '中价值'
        WHEN total_spent >= 1000 THEN '低价值'
        ELSE '潜力用户'
    END as value_segment
FROM user_orders
ORDER BY total_spent DESC
LIMIT 100;
```

---

### 2.7 Hive性能优化基础（20min）

```sql
-- ===== 优化1: 使用EXPLAIN查看执行计划 =====
EXPLAIN 
SELECT category_id, COUNT(*) 
FROM user_behavior 
WHERE dt='2024-01-01' 
GROUP BY category_id;

EXPLAIN EXTENDED  -- 更详细的计划
SELECT category_id, COUNT(*) 
FROM user_behavior 
WHERE dt='2024-01-01' 
GROUP BY category_id;


-- ===== 优化2: 开启矢量查询 =====
SET hive.vectorized.execution.enabled = true;
SET hive.vectorized.execution.reduce.enabled = true;


-- ===== 优化3: 开启CBO(Cost-Based Optimizer) =====
SET hive.cbo.enable = true;
SET hive.compute.query.using.stats = true;
SET hive.stats.fetch.column.stats = true;
SET hive.stats.fetch.partition.stats = true;

-- 先收集统计信息
ANALYZE TABLE user_behavior PARTITION(dt='2024-01-01') COMPUTE STATISTICS;
ANALYZE TABLE user_behavior PARTITION(dt='2024-01-01') COMPUTE STATISTICS FOR COLUMNS;


-- ===== 优化4: 小表Join大表的Map Join优化 =====
SET hive.auto.convert.join = true;
SET hive.mapjoin.smalltable.filesize = 25000000; -- 25MB

-- Hive自动判断: 当一个小表<25MB时，自动使用Map Join
-- Map Join: 将小表加载到内存，在Map端完成Join，避免Shuffle

-- 手动指定Map Join
SELECT /*+ MAPJOIN(c) */ 
    u.*, c.category_name
FROM user_log u
JOIN category_info c ON u.category_id = c.category_id;


-- ===== 优化5: 合理设置Reduce数量 =====
SET mapreduce.job.reduces = 50;  -- 根据数据量合理设置

-- 经验公式:
-- Reduce数 ≈ (总输入数据量 / 每个Reduce处理的数据量)
-- 每个Reduce推荐处理: 256MB ~ 1GB


-- ===== 优化6: 开启并行执行 =====
SET hive.exec.parallel = true;
SET hive.exec.parallel.thread.number = 8;

-- 作用: 如果多个Stage没有依赖关系，可以并行执行


-- ===== 优化7: 数据倾斜处理 =====
SET hive.groupby.skewindata = true;
SET hive.optimize.skewjoin = true;

-- 原理: 生成两个MR Job
-- Job1: Map输出随机分发到Reduce，做一次局部聚合
-- Job2: 基于Job1的结果再做最终聚合
```

---

## 三、实验任务

### 3.1 环境准备（通过Docker启动Hive）

```bash
# 启动Hive Server
docker exec -it hive-server bash

# 进入Hive CLI
beeline -u jdbc:hive2://localhost:10000

# 或直接使用hive命令
hive
```

### 3.2 完整实验流程

```bash
# 步骤1: 启动Hive
hive

# 步骤2: 创建数据库
CREATE DATABASE IF NOT EXISTS ecommerce;
USE ecommerce;

# 步骤3: 创建TextFile格式的原始表
CREATE EXTERNAL TABLE user_log_text (
    user_id BIGINT,
    item_id BIGINT,
    category_id INT,
    behavior STRING,
    ts BIGINT
)
ROW FORMAT DELIMITED 
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
LOCATION '/data/user_log/';

# 步骤4: 创建Parquet格式的分区表
CREATE EXTERNAL TABLE user_log_parquet (
    user_id BIGINT,
    item_id BIGINT,
    category_id INT,
    behavior STRING,
    ts BIGINT
)
PARTITIONED BY (dt STRING)
STORED AS PARQUET
LOCATION '/warehouse/user_log_parquet/';

# 步骤5: 从TextFile表转换数据到Parquet分区表
INSERT OVERWRITE TABLE user_log_parquet PARTITION (dt='2024-01-01')
SELECT user_id, item_id, category_id, behavior, ts
FROM user_log_text;

# 步骤6: 对比存储空间
# 在HDFS上查看两个表的存储大小
# hdfs dfs -du -h /data/user_log/
# hdfs dfs -du -h /warehouse/user_log_parquet/

# 步骤7: 对比查询性能
# 使用EXPLAIN查看执行计划差异
EXPLAIN SELECT category_id, COUNT(*) FROM user_log_text WHERE behavior='buy' GROUP BY category_id;
EXPLAIN SELECT category_id, COUNT(*) FROM user_log_parquet WHERE dt='2024-01-01' AND behavior='buy' GROUP BY category_id;
```

---

## 四、课堂练习（60min）

### 练习1：分区表建表（15min）

```sql
-- 题目：为电商平台设计订单分区表

-- 要求：
-- 1. 创建外部表，包含以下字段：
--    order_id, user_id, product_id, quantity, unit_price, total_amount, status, create_time
-- 2. 按日期(dt)分区
-- 3. 存储格式为ORC
-- 4. 添加适当的表注释和字段注释
-- 5. 写出添加3个分区(2024-01-01 ~ 2024-01-03)的语句
```

### 练习2：数据分析查询（25min）

```sql
-- 基于上面的订单表，写出以下查询：

-- Q1: 2024年1月每天的订单量和销售额
-- Q2: 销售额TOP 10的用户及其购买品类分布
-- Q3: 每周的环比增长率（需要用到窗口函数LAG）
-- Q4: 被取消订单占比超过10%的用户（异常用户检测）
-- Q5: 客单价（平均每单金额）的分布（分段统计）
```

### 练习3：文件格式对比实验（20min）

```
任务:
  1. 创建3个表，分别使用TextFile、Parquet、ORC格式
  2. 向3个表导入相同的数据(至少100万行)
  3. 对比:
     a. 存储空间占用
     b. 全表扫描时间
     c. 单列查询时间
     d. 聚合查询时间

输出: 填写对比报告表格
```

---

## 五、课后作业

### 作业1：HQL练习题20道（必做）

完成以下20道HQL练习题，提交SQL源码和执行结果：

```yaml
基础操作(5题):
  1. 创建含3个分区的订单外部表（Parquet格式）
  2. 向分区表插入100万行模拟数据
  3. 修改表，添加一个新的列
  4. 删除指定分区
  5. 将查询结果导出为CSV文件

JOIN查询(5题):
  6. INNER JOIN: 关联订单表和用户表
  7. LEFT JOIN: 找出没有订单的用户
  8. 多表JOIN: 订单-用户-商品三表关联
  9. 自JOIN: 找出同一用户连续两天的行为
  10. Semi Join: 使用LEFT SEMI JOIN优化IN子查询

窗口函数(5题):
  11. ROW_NUMBER: 每个用户消费金额排名
  12. LAG: 计算每日GMV环比变化
  13. SUM OVER: 计算7天移动平均
  14. NTILE: 将用户按消费金额分为10个等级
  15. FIRST_VALUE: 每个用户的第一笔订单金额

性能优化(5题):
  16. 使用EXPLAIN分析一个复杂查询
  17. 将TextFile表转换为Parquet表
  18. 开启Map Join后对比性能
  19. 使用分区裁剪优化查询
  20. 使用ANALYZE收集统计信息
```

### 作业2：TextFile vs Parquet对比报告（必做）

```
要求:
  1. 使用生成脚本创建100万行测试数据
  2. 分别导入TextFile和Parquet格式的Hive表
  3. 对比6种查询场景的性能:
     - SELECT COUNT(*)
     - SELECT single_column
     - WHERE filter
     - GROUP BY + COUNT
     - GROUP BY + SUM + ORDER BY
     - JOIN
  4. 记录每次查询的时间（执行3次取平均）
  5. 计算存储空间节省比例
  6. 得出结论：什么场景下Parquet优势最明显？
```

### 作业3：设计数据仓库分层方案（选做）

```
场景: 你是电商公司的数据工程师，需要设计数据仓库

数据源:
  - MySQL: 用户表(10万行)、订单表(500万行)、商品表(5万行)
  - Nginx日志: 每天约200GB的访问日志
  - 第三方数据: 天气数据(每天100MB)

要求:
  1. 设计ODS层→DWD层→DWS层→ADS层的表结构
  2. 每层的存储格式选择及理由
  3. 分区策略设计及理由
  4. 写出每层建表的HiveQL DDL
```

---

## 六、参考资料

1. **Hive官方文档**：https://cwiki.apache.org/confluence/display/Hive/
2. **《Hadoop权威指南》**：第12章 Hive
3. **《数据仓库工具箱》**：维度建模指南
4. **Parquet官方文档**：https://parquet.apache.org/
5. **ORC官方文档**：https://orc.apache.org/