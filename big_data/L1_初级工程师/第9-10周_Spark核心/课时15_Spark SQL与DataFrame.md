# 课时15：Spark SQL与DataFrame

> **课时时长**：8小时（理论3h + 编码实战3h + 练习2h）
>
> **难度等级**：⭐⭐⭐⭐ 核心重点

---

## 一、教学目标

1. **理解DataFrame vs RDD的区别**：从性能、易用性、优化器三个维度对比
2. **掌握SparkSession统一入口**：替换SparkContext成为Spark 2.0+的标准入口
3. **精通DataFrame API**：select、filter、groupBy、agg、join等核心操作
4. **掌握Spark SQL编程**：临时视图 + SQL查询的混合编程模式
5. **理解Catalyst优化器**：逻辑计划→优化→物理计划的全流程
6. **能完成完整的数据分析流程**：读取→清洗→分析→写入全链路

---

## 二、教学内容

### 2.1 RDD vs DataFrame vs DataSet（30min）

**三者对比：**

| 维度 | RDD | DataFrame | Dataset |
|------|-----|-----------|---------|
| 数据抽象 | 分布式对象集合 | 分布式行对象集合(带Schema) | 类型化的分布式对象集合 |
| 优化器 | 无（手动优化） | Catalyst自动优化 | Catalyst自动优化 |
| 序列化 | Java序列化 | Tungsten(堆外内存) | Encoder |
| 类型安全 | 编译时安全 | 运行时检查 | 编译时安全 |
| 性能 | 最低 | 高（列式+代码生成） | 高 |
| API易用性 | 函数式 | 声明式(SQL-like) | 函数式+声明式 |
| Python支持 | ✅ | ✅ | ❌(仅Scala/Java) |

**为什么DataFrame比RDD快？**

```
数据：
  RDD[Person] → 每个Person是一个Java对象 → Java序列化 → GC压力大

  DataFrame → 数据存储在堆外内存(off-heap) → 二进制格式
  → 不需要Java序列化/反序列化 → 没有GC压力
  → 列式存储 → 只读取需要的列 → I/O减少
  → Tungsten代码生成 → 将表达式编译为Java字节码 → 接近手写代码性能
```

**DataFrame = RDD + Schema：**

```python
# RDD: 没有Schema，元素是Python对象
rdd = sc.parallelize([
    ("张三", 25, "北京"),
    ("李四", 30, "上海"),
])

# DataFrame: 有Schema，每列有名称和类型
df = spark.createDataFrame(
    [("张三", 25, "北京"), ("李四", 30, "上海")],
    schema=["name", "age", "city"]
)

df.printSchema()
# root
#  |-- name: string (nullable = true)
#  |-- age: long (nullable = true)
#  |-- city: string (nullable = true)
```

---

### 2.2 SparkSession - 统一入口（20min）

```python
from pyspark.sql import SparkSession

# Spark 2.0+ 标准创建方式
spark = SparkSession.builder \
    .appName("DataAnalysisApp") \              # 应用名称
    .master("local[*]") \                       # 本地模式（生产环境去掉）
    .config("spark.sql.adaptive.enabled", "true") \  # 开启AQE
    .config("spark.sql.adaptive.coalescePartitions.enabled", "true") \
    .config("spark.sql.shuffle.partitions", "200") \   # Shuffle分区数
    .config("spark.driver.memory", "2g") \
    .config("spark.executor.memory", "4g") \
    .enableHiveSupport() \                     # 启用Hive支持
    .getOrCreate()

# SparkSession包含了:
# - spark.sparkContext   → 底层的SparkContext
# - spark.sql()          → 执行SQL
# - spark.read           → 读取数据
# - spark.createDataFrame() → 创建DataFrame

# 使用完毕后关闭
spark.stop()
```

---

### 2.3 DataFrame API核心操作（90min）

**2.3.1 读取数据**

```python
# 读取各种格式
df_csv = spark.read \
    .option("header", "true") \
    .option("inferSchema", "true") \
    .option("delimiter", ",") \
    .csv("hdfs:///data/users.csv")

df_json = spark.read.json("hdfs:///data/users.json")

df_parquet = spark.read.parquet("hdfs:///warehouse/user_behavior")

df_jdbc = spark.read \
    .format("jdbc") \
    .option("url", "jdbc:mysql://mysql:3306/ecommerce") \
    .option("dbtable", "orders") \
    .option("user", "root") \
    .option("password", "xxx") \
    .load()

df_hive = spark.table("ecommerce.orders")
```

**2.3.2 常用操作速查**

```python
# ===== select: 选择列 =====
df.select("user_id", "behavior", "amount")
df.select(col("user_id"), col("behavior"), col("amount") * 1.1)

# ===== filter/where: 过滤行 =====
df.filter(col("amount") > 100)
df.filter((col("amount") > 100) & (col("behavior") == "buy"))
df.where("amount > 100 AND behavior = 'buy'")

# ===== groupBy + agg: 分组聚合 =====
df.groupBy("category_id").agg(
    count("*").alias("pv"),
    countDistinct("user_id").alias("uv"),
    sum("amount").alias("total_amount"),
    avg("amount").alias("avg_amount")
)

# ===== orderBy/sort: 排序 =====
df.orderBy(col("amount").desc())
df.orderBy(col("dt").desc(), col("amount").asc())

# ===== withColumn: 添加/修改列 =====
df.withColumn("amount_with_tax", col("amount") * 1.13)
df.withColumn("behavior_cn", 
    when(col("behavior") == "buy", "购买")
    .when(col("behavior") == "cart", "加购")
    .otherwise("其他")
)

# ===== withColumnRenamed: 重命名列 =====
df.withColumnRenamed("amount", "price")

# ===== drop: 删除列 =====
df.drop("unnecessary_column")

# ===== distinct/dropDuplicates: 去重 =====
df.distinct()
df.dropDuplicates(["user_id", "dt"])

# ===== limit: 限制行数 =====
df.limit(100)

# ===== sample: 抽样 =====
df.sample(fraction=0.1, seed=42)
```

**2.3.3 JOIN操作**

```python
# INNER JOIN (默认)
df_orders.join(df_users, "user_id")
df_orders.join(df_users, df_orders.user_id == df_users.user_id, "inner")

# LEFT JOIN
df_orders.join(df_users, "user_id", "left")

# RIGHT JOIN
df_orders.join(df_users, "user_id", "right")

# FULL OUTER JOIN
df_orders.join(df_users, "user_id", "outer")

# LEFT SEMI JOIN (相当于 WHERE EXISTS)
df_orders.join(df_users, "user_id", "left_semi")

# LEFT ANTI JOIN (相当于 WHERE NOT EXISTS)
df_orders.join(df_users, "user_id", "left_anti")

# CROSS JOIN (笛卡尔积，慎用！)
df_orders.crossJoin(df_users)

# Broadcast Join (小表广播)
from pyspark.sql.functions import broadcast
df_big.join(broadcast(df_small), "category_id")
```

**2.3.4 窗口函数**

```python
from pyspark.sql.window import Window

# 排名窗口
window_spec = Window.partitionBy("category_id").orderBy(col("amount").desc())

df.withColumn("rank", row_number().over(window_spec)) \
  .withColumn("dense_rank", dense_rank().over(window_spec)) \
  .filter(col("rank") <= 10)

# 偏移窗口 — 计算环比
window_spec = Window.partitionBy("category_id").orderBy("dt")
df.withColumn("prev_amount", lag("amount", 1).over(window_spec)) \
  .withColumn("growth_rate", 
      (col("amount") - col("prev_amount")) / col("prev_amount") * 100)

# 聚合窗口 — 累计值
window_spec = Window.partitionBy("user_id").orderBy("dt") \
    .rowsBetween(Window.unboundedPreceding, Window.currentRow)
df.withColumn("cumulative_amount", sum("amount").over(window_spec))

# 移动平均
window_spec = Window.partitionBy("category_id").orderBy("dt") \
    .rowsBetween(-6, 0)  # 前6行到当前行 = 7天移动平均
df.withColumn("moving_avg_7d", avg("amount").over(window_spec))
```

---

### 2.4 Spark SQL编程（40min）

**临时视图与全局视图：**

```python
# 创建临时视图（当前SparkSession有效）
df.createOrReplaceTempView("orders")

# 创建全局临时视图（跨SparkSession，存储在global_temp数据库）
df.createOrReplaceGlobalTempView("orders_global")

# 使用SQL查询
result = spark.sql("""
    SELECT 
        category_id,
        COUNT(*) as order_count,
        SUM(amount) as total_amount
    FROM orders
    WHERE dt = '2024-01-01'
    GROUP BY category_id
    ORDER BY total_amount DESC
""")

result.show()
```

**SQL vs DataFrame API — 哪种方式更好？**

```python
# 场景: 用户行为漏斗分析

# DataFrame API版本（链式调用，适合复杂逻辑）
funnel_df = df.filter(col("dt") == "2024-01-01") \
    .groupBy("user_id") \
    .agg(
        sum(when(col("behavior") == "pv", 1).otherwise(0)).alias("pv"),
        sum(when(col("behavior") == "cart", 1).otherwise(0)).alias("cart"),
        sum(when(col("behavior") == "buy", 1).otherwise(0)).alias("buy"),
    ) \
    .agg(
        count(when(col("pv") > 0, 1)).alias("pv_users"),
        count(when(col("cart") > 0, 1)).alias("cart_users"),
        count(when(col("buy") > 0, 1)).alias("buy_users"),
    )

# SQL版本（更直观，适合业务人员阅读）
df.createOrReplaceTempView("behavior")
funnel_sql = spark.sql("""
    WITH user_stats AS (
        SELECT user_id,
            SUM(CASE WHEN behavior='pv' THEN 1 ELSE 0 END) as pv,
            SUM(CASE WHEN behavior='cart' THEN 1 ELSE 0 END) as cart,
            SUM(CASE WHEN behavior='buy' THEN 1 ELSE 0 END) as buy
        FROM behavior WHERE dt='2024-01-01'
        GROUP BY user_id
    )
    SELECT
        COUNT(CASE WHEN pv>0 THEN 1 END) as pv_users,
        COUNT(CASE WHEN cart>0 THEN 1 END) as cart_users,
        COUNT(CASE WHEN buy>0 THEN 1 END) as buy_users,
        ROUND(COUNT(CASE WHEN cart>0 THEN 1 END)*100.0/COUNT(CASE WHEN pv>0 THEN 1 END),2) as pv_to_cart,
        ROUND(COUNT(CASE WHEN buy>0 THEN 1 END)*100.0/COUNT(CASE WHEN cart>0 THEN 1 END),2) as cart_to_buy
    FROM user_stats
""")

# 建议: 简单的用SQL，复杂的用DataFrame API，可以混用！
```

---

### 2.5 Catalyst优化器（20min）

**Catalyst的工作流程：**

```
SQL/DataFrame API
       │
       ▼
┌─────────────────┐
│ 1. 解析(Parser)  │  生成未解析的逻辑计划(Unresolved Logical Plan)
└────────┬────────┘
         ▼
┌─────────────────┐
│ 2. 分析(Analyzer)│  通过Catalog解析表名/列名/类型 → 解析后的逻辑计划
└────────┬────────┘
         ▼
┌─────────────────┐
│ 3. 优化(Optimizer)│  应用优化规则: 谓词下推/列裁剪/常量折叠/...
└────────┬────────┘
         ▼
┌─────────────────┐
│ 4. 物理计划      │  选择最优物理执行策略: BroadcastHashJoin vs SortMergeJoin
│   (Planner)      │  选择聚合策略: HashAggregate vs SortAggregate
└────────┬────────┘
         ▼
┌─────────────────┐
│ 5. 代码生成      │  WholeStageCodegen: 将多个算子合并为一个函数
│   (CodeGen)      │  生成Janino编译的Java代码
└────────┬────────┘
         ▼
      执行
```

**查看执行计划：**

```python
# 查看逻辑计划
df.explain(extended=True)
# 输出:
# == Parsed Logical Plan ==
# == Analyzed Logical Plan ==
# == Optimized Logical Plan ==
# == Physical Plan ==

# 示例：观察谓词下推
df = spark.read.parquet("hdfs:///data/orders")
result = df.filter(col("dt") == "2024-01-01") \
    .filter(col("amount") > 100) \
    .select("user_id", "amount")

result.explain(True)
# 观察优化后的计划：两个filter合并了！select只读需要的列！
```

---

### 2.6 完整数据分析实战代码（90min）

```python
"""
场景: 电商用户行为数据分析全流程
数据: user_behavior (用户行为日志)

完整流程:
  1. 数据读取
  2. 数据探索与质量检查
  3. 数据清洗与转换
  4. 多维度分析
  5. 结果写入
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
from pyspark.sql.window import Window

spark = SparkSession.builder \
    .appName("EcommerceAnalysis") \
    .config("spark.sql.adaptive.enabled", "true") \
    .getOrCreate()

# ============================================================
# 第一步：数据读取
# ============================================================

schema = StructType([
    StructField("user_id", LongType(), True),
    StructField("item_id", LongType(), True),
    StructField("category_id", IntegerType(), True),
    StructField("behavior", StringType(), True),
    StructField("ts", LongType(), True),
])

df = spark.read \
    .option("header", "false") \
    .option("delimiter", ",") \
    .schema(schema) \
    .csv("hdfs:///data/user_behavior/*.csv")

# 或从Parquet读取
# df = spark.read.parquet("hdfs:///warehouse/user_behavior")

# ============================================================
# 第二步：数据探索与质量检查
# ============================================================

print("=== Schema ===")
df.printSchema()

print("=== 行数 ===")
print(f"总行数: {df.count()}")

print("=== 前5行 ===")
df.show(5, truncate=False)

print("=== 基本统计 ===")
df.describe(["user_id", "item_id", "category_id"]).show()

print("=== 各行为类型分布 ===")
df.groupBy("behavior").count().orderBy(col("count").desc()).show()

print("=== 空值检查 ===")
df.select([count(when(col(c).isNull(), c)).alias(c) for c in df.columns]).show()

# ============================================================
# 第三步：数据清洗与转换
# ============================================================

cleaned_df = df \
    .filter(col("user_id").isNotNull()) \
    .filter(col("item_id").isNotNull()) \
    .filter(col("behavior").isin("pv", "buy", "cart", "fav")) \
    .withColumn("dt", from_unixtime(col("ts"), "yyyy-MM-dd")) \
    .withColumn("hour", from_unixtime(col("ts"), "HH")) \
    .withColumn("behavior_cn", 
        when(col("behavior") == "pv", "浏览")
        .when(col("behavior") == "buy", "购买")
        .when(col("behavior") == "cart", "加购")
        .when(col("behavior") == "fav", "收藏")
        .otherwise("未知")
    )

print("=== 清洗后行数 ===")
print(f"清洗后: {cleaned_df.count()}")
print(f"清洗掉: {df.count() - cleaned_df.count()}")

# ============================================================
# 第四步：多维度分析
# ============================================================

# --- 分析1: 每日PV/UV统计 ---
print("\n=== 每日PV/UV ===")
daily_pv_uv = cleaned_df \
    .groupBy("dt") \
    .agg(
        count("*").alias("pv"),
        countDistinct("user_id").alias("uv")
    ) \
    .withColumn("pv_per_uv", round(col("pv") / col("uv"), 2)) \
    .orderBy("dt")
daily_pv_uv.show(30)

# --- 分析2: 品类热度排行 ---
print("\n=== 品类PV TOP10 ===")
category_stats = cleaned_df \
    .groupBy("category_id") \
    .agg(
        count("*").alias("total_pv"),
        countDistinct("user_id").alias("total_uv"),
        sum(when(col("behavior") == "buy", 1).otherwise(0)).alias("buy_count"),
        sum(when(col("behavior") == "cart", 1).otherwise(0)).alias("cart_count"),
        sum(when(col("behavior") == "fav", 1).otherwise(0)).alias("fav_count")
    ) \
    .withColumn("buy_rate", round(col("buy_count") / col("total_pv") * 100, 2)) \
    .orderBy(col("total_pv").desc())
category_stats.show(10)

# --- 分析3: 每小时行为分布（热力图数据） ---
print("\n=== 每小时行为分布 ===")
hourly_behavior = cleaned_df \
    .groupBy("hour") \
    .agg(
        count("*").alias("total"),
        sum(when(col("behavior") == "pv", 1).otherwise(0)).alias("pv"),
        sum(when(col("behavior") == "buy", 1).otherwise(0)).alias("buy"),
        sum(when(col("behavior") == "cart", 1).otherwise(0)).alias("cart"),
    ) \
    .orderBy("hour")
hourly_behavior.show(24)

# --- 分析4: 用户活跃度分层 ---
print("\n=== 用户活跃度分层 ===")
user_activity = cleaned_df \
    .groupBy("user_id") \
    .agg(count("*").alias("action_count")) \
    .withColumn("activity_level",
        when(col("action_count") >= 100, "高活跃")
        .when(col("action_count") >= 30, "中活跃")
        .when(col("action_count") >= 5, "低活跃")
        .otherwise("沉默用户")
    )

user_activity.groupBy("activity_level") \
    .agg(count("*").alias("user_count")) \
    .orderBy(col("user_count").desc()) \
    .show()

# --- 分析5: 用户行为漏斗 ---
print("\n=== 行为转化漏斗 ===")
funnel = cleaned_df \
    .groupBy("user_id") \
    .agg(
        max(when(col("behavior") == "pv", 1).otherwise(0)).alias("has_pv"),
        max(when(col("behavior") == "cart", 1).otherwise(0)).alias("has_cart"),
        max(when(col("behavior") == "fav", 1).otherwise(0)).alias("has_fav"),
        max(when(col("behavior") == "buy", 1).otherwise(0)).alias("has_buy"),
    ) \
    .agg(
        sum("has_pv").alias("pv_users"),
        sum("has_cart").alias("cart_users"),
        sum("has_fav").alias("fav_users"),
        sum("has_buy").alias("buy_users"),
    )
funnel.show()

# --- 分析6: 用户连续活跃天数（窗口函数） ---
print("\n=== 用户连续活跃天数 TOP10 ===")

# 获取每个用户活跃的日期
user_active_days = cleaned_df \
    .select("user_id", "dt") \
    .distinct()

# 计算连续活跃天数
window_spec = Window.partitionBy("user_id").orderBy("dt")
consecutive_days = user_active_days \
    .withColumn("prev_dt", lag("dt", 1).over(window_spec)) \
    .withColumn("is_consecutive", 
        when(datediff(col("dt"), col("prev_dt")) == 1, 1).otherwise(0)
    ) \
    .filter(col("is_consecutive") == 1) \
    .groupBy("user_id") \
    .agg((count("*") + 1).alias("consecutive_days")) \
    .orderBy(col("consecutive_days").desc())

consecutive_days.show(10)

# --- 分析7: RFM分析 ---
print("\n=== RFM用户分层 ===")

# 计算R(最近一次行为距今天数), F(行为频率), M(购买次数)
rfm = cleaned_df \
    .groupBy("user_id") \
    .agg(
        max("dt").alias("last_active_date"),
        count("*").alias("frequency"),
        sum(when(col("behavior") == "buy", 1).otherwise(0)).alias("monetary")
    ) \
    .withColumn("recency_days", 
        datediff(current_date(), col("last_active_date"))
    )

# RMF评分（1-5分）
rfm_scored = rfm \
    .withColumn("r_score", 
        ntile(5).over(Window.orderBy(col("recency_days").desc()))
    ) \
    .withColumn("f_score",
        ntile(5).over(Window.orderBy("frequency"))
    ) \
    .withColumn("m_score",
        ntile(5).over(Window.orderBy("monetary"))
    )

rfm_scored.select("user_id", "recency_days", "frequency", "monetary",
                    "r_score", "f_score", "m_score").show(20)

# ============================================================
# 第五步：结果写入
# ============================================================

# 写入Parquet文件（按日期分区）
daily_pv_uv.write \
    .mode("overwrite") \
    .partitionBy("dt") \
    .parquet("hdfs:///output/daily_pv_uv")

# 写入Hive表
category_stats.write \
    .mode("overwrite") \
    .format("parquet") \
    .saveAsTable("ecommerce.category_stats")

# 写入MySQL（通过JDBC）
category_stats.write \
    .mode("overwrite") \
    .format("jdbc") \
    .option("url", "jdbc:mysql://mysql:3306/reports") \
    .option("dbtable", "category_stats") \
    .option("user", "root") \
    .option("password", "xxx") \
    .save()

print("\n=== 分析完成! ===")
spark.stop()
```

---

### 2.7 写入模式详解

```python
# mode参数说明
# "append":   追加到已有数据（保留旧数据）
# "overwrite": 覆盖已有数据（删除旧数据）
# "ignore":   如果数据已存在则跳过
# "error":    如果数据已存在则报错（默认）

# 示例
df.write.mode("append").parquet("hdfs:///data/output/")
df.write.mode("overwrite").parquet("hdfs:///data/output/")

# 分区写入（高效！）
df.write \
    .mode("overwrite") \
    .partitionBy("dt", "category_id") \
    .bucketBy(16, "user_id") \
    .sortBy("amount") \
    .format("parquet") \
    .saveAsTable("partitioned_orders")
```

---

## 三、课堂练习（90min）

### 练习1：DataFrame API操作闯关（30min）

```python
"""
使用以下数据完成所有操作:

数据:
orders_df 包含列: order_id, user_id, amount, status, dt
users_df 包含列: user_id, name, city, level

关卡:
  1. 只选择已完成(status='completed')的订单
  2. 计算每个用户的总消费金额和订单数
  3. 关联用户信息，输出: 用户名, 城市, 总消费, 订单数
  4. 按城市统计总销售额，并添加排名列
  5. 计算每个城市每天的销售额相较于前一天的增长率
  6. 找出每个城市销售额最高的前3个用户
"""

# 参考实现框架
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.window import Window

spark = SparkSession.builder.appName("Exercise").master("local[*]").getOrCreate()

# 创建模拟数据
orders_data = [
    ("O001", "U001", 299.00, "completed", "2024-01-01"),
    ("O002", "U001", 150.00, "completed", "2024-01-01"),
    ("O003", "U002", 500.00, "completed", "2024-01-02"),
    ("O004", "U001", 200.00, "cancelled", "2024-01-02"),
    ("O005", "U003", 800.00, "completed", "2024-01-02"),
    ("O006", "U002", 350.00, "completed", "2024-01-03"),
    ("O007", "U003", 100.00, "completed", "2024-01-03"),
    ("O008", "U001", 450.00, "completed", "2024-01-03"),
]
orders_df = spark.createDataFrame(orders_data, 
    ["order_id", "user_id", "amount", "status", "dt"])

users_data = [
    ("U001", "张三", "北京", "VIP"),
    ("U002", "李四", "上海", "普通"),
    ("U003", "王五", "北京", "VIP"),
]
users_df = spark.createDataFrame(users_data, 
    ["user_id", "name", "city", "level"])

# TODO: 完成6个关卡
```

### 练习2：SQL vs DataFrame对比（30min）

```
同一个分析需求，分别用DataFrame API和Spark SQL实现：

需求: 
  1. 每个品类每天的购买转化率(购买数/浏览数)
  2. 找出连续3天转化率下降的品类

要求:
  - 左边写DataFrame API版本
  - 右边写SQL版本
  - 对比两种写法的可读性和代码量
```

### 练习3：EXPLAIN分析（30min）

```python
# 对以下查询执行explain，分析优化器做了什么
df1 = spark.read.parquet("hdfs:///data/orders")

# 查询A: 先filter再select vs 先select再filter
explain_a1 = df1.filter(col("dt") == "2024-01-01") \
    .select("user_id", "amount").explain(True)

explain_a2 = df1.select("user_id", "amount") \
    .filter(col("dt") == "2024-01-01").explain(True)

# 查询B: 两个小filter vs 一个合并filter
explain_b1 = df1.filter(col("amount") > 100) \
    .filter(col("status") == "completed").explain(True)

explain_b2 = df1.filter(
    (col("amount") > 100) & (col("status") == "completed")
).explain(True)

# 观察: 优化后的计划是否相同？
```

---

## 四、课后作业

### 作业1：完整数据分析Pipeline（必做）

```
使用DataFrame API完成以下分析（基于用户行为数据）:

1. 数据清洗:
   - 删除空值行
   - 过滤无效行为类型
   - 添加日期和时间维度列

2. 分析指标:
   a. 每日PV/UV及PV/UV比
   b. 各品类PV/UV/购买转化率排名
   c. 每小时PV分布（热力图数据）
   d. 用户活跃度分层(按PV数分为4层)
   e. 行为转化漏斗(PV→加购→收藏→购买)
   f. 用户连续活跃天数分布
   g. Top 100高频用户的特征分析

3. 输出:
   - 每个指标保存为独立的Parquet文件
   - 创建Hive外部表指向分析结果
```

### 作业2：对比RDD和DataFrame的WordCount（必做）

```
任务:
  1. 用RDD API实现WordCount
  2. 用DataFrame API实现WordCount
  3. 分别处理1MB, 10MB, 100MB的文本文件
  4. 记录执行时间和Shuffle数据量
  5. 对比代码量、可读性、性能

输出: 对比报告
```

### 作业3：窗口函数专项练习（必做）

```sql
完成以下5个窗口函数练习:

1. ROW_NUMBER: 每个品类按销售额排名
2. LAG/LEAD: 日销售额环比增长率
3. SUM OVER: 用户累计消费金额
4. NTILE: 将用户按消费金额分5层
5. 移动平均: 7天滑动窗口销售额
```

### 作业4：Catalyst优化器研究（选做）

```
任务:
  1. 在Spark源码中阅读RuleExecutor.scala
  2. 找出5个常用的优化规则
  3. 每个规则写一个示例并对比优化前后的执行计划
```


---

## 五、参考资料

1. **Spark SQL官方文档**：https://spark.apache.org/sql/
2. **《Spark快速大数据分析》**：第6-9章
3. **Catalyst优化器论文**：*Spark SQL: Relational Data Processing in Spark (2015)*
4. **Databricks Blog**：https://www.databricks.com/blog/category/engineering/spark-sql