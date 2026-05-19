# 课时16：Spark性能调优基础

> **课时时长**：8小时（理论3h + 调优实战3h + 练习2h）
>
> **难度等级**：⭐⭐⭐⭐⭐ 实战进阶（面试重点）

---

## 一、教学目标

1. **能诊断数据倾斜**：通过Spark UI识别倾斜Task，分析倾斜Key
2. **掌握3种以上倾斜解决方案**：加盐、Broadcast Join、AQE，能根据场景选择合适方案
3. **理解Shuffle优化**：掌握分区数设置、压缩算法选择、AQE自适应优化
4. **理解内存管理**：掌握Cache/Persist策略，理解Storage和Execution内存分配
5. **能独立完成性能调优**：给定一个慢任务，能系统性诊断并优化
6. **理解序列化选择**：对比Java序列化、Kryo、Tungsten的适用场景

---

## 二、教学内容

### 2.1 数据倾斜诊断（40min）

**什么是数据倾斜？**

```
数据倾斜 = 数据分布不均匀，导致某些Task处理的数据量远多于其他Task

直观表现（Spark UI → Stages → 查看Task）:
  ┌──────────────────────────────────────────────┐
  │ Task 0:   ████   (2 MB)                     │
  │ Task 1:   ███    (1.5 MB)                    │
  │ Task 2:   ████████████████████████ (500 MB!) │  ← 倾斜Task!
  │ Task 3:   ███    (1.8 MB)                    │
  │ Task 4:   ████   (2.1 MB)                    │
  └──────────────────────────────────────────────┘
  
  后果:
  - 倾斜Task执行时间远超其他Task → 总耗时 = 倾斜Task的耗时
  - 倾斜Task可能OOM（内存溢出）
  - 其他Task早早完成后，资源空闲等待
```

**诊断步骤：**

```
步骤1: 打开Spark UI → Stages页面
步骤2: 查看每个Stage的Task分布
步骤3: 找到 Duration(耗时) 和 Shuffle Read Size(输入数据量)
      远超其他Task的Task
步骤4: 点击倾斜Task → 查看Metrics
步骤5: 对比: Median(中位数) vs Max(最大值)
       如果 Max/Median > 3 → 存在数据倾斜
```

**诊断代码示例：**

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import *

spark = SparkSession.builder \
    .appName("SkewDetection") \
    .getOrCreate()

df = spark.read.parquet("hdfs:///data/user_behavior")

# 检测每个Key的数据量（可能倾斜的Key的特征）
key_distribution = df.groupBy("category_id") \
    .count() \
    .orderBy(col("count").desc())

print("=== Key分布（检查倾斜） ===")
key_distribution.show(20, truncate=False)

# 计算倾斜度
stats = key_distribution.agg(
    max("count").alias("max_count"),
    avg("count").alias("avg_count"),
    (max("count") / avg("count")).alias("skew_ratio")
).collect()[0]

print(f"\n最大Key数据量: {stats['max_count']}")
print(f"平均Key数据量: {stats['avg_count']:.2f}")
print(f"倾斜比: {stats['skew_ratio']:.2f}")
print(f"结论: {'存在严重倾斜!' if stats['skew_ratio'] > 5 else '分布较均匀'}")
```

---

### 2.2 数据倾斜解决方案 — 方案1：加盐打散（60min）

**原理：**

```
问题: category_id=100的数据有1000万条，其他category_id只有几百条
      → groupBy("category_id") 时，处理category_id=100的Task特别慢

方案: 将倾斜Key的数据打散到多个Task中处理

原始数据:
  category_id=100,   data_1
  category_id=100,   data_2
  category_id=100,   data_3
  ...

加盐后:
  category_id=100_salt_0,   data_1
  category_id=100_salt_1,   data_2
  category_id=100_salt_2,   data_3
  category_id=100_salt_0,   data_4
  ...
  
  每个加盐后的Key均匀分布到不同Task
```

**完整代码实现：**

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import *

spark = SparkSession.builder \
    .appName("SkewSolution_Salt") \
    .config("spark.sql.adaptive.enabled", "false") \
    .getOrCreate()

# 模拟倾斜数据
df = spark.read.parquet("hdfs:///data/user_behavior")

# ================================================================
# 方案1: 加盐打散（适用于groupBy + agg操作）
# ================================================================

SALT_NUM = 100  # 加盐数量（将倾斜Key打散到100个Task）

# 步骤1: 添加盐值列
# 对于倾斜Key使用随机盐值，对于非倾斜Key使用固定盐值(0)
# 这样非倾斜Key不受影响，倾斜Key被均匀分散

# 先识别倾斜的Key（这里假设category_id=100和200是倾斜Key）
SKEW_KEYS = [100, 200]

skewed_df = df.withColumn(
    "salt",
    when(col("category_id").isin(SKEW_KEYS), 
         (rand() * SALT_NUM).cast("int"))
    .otherwise(lit(0))
)

# 步骤2: 使用加盐后的Key进行聚合
# 第一次聚合: 使用(salt, category_id)作为Key
salted_result = skewed_df \
    .groupBy("salt", "category_id") \
    .agg(
        count("*").alias("cnt"),
        sum(when(col("behavior") == "buy", 1).otherwise(0)).alias("buy_cnt")
    )

# 步骤3: 去除盐值，做最终聚合
final_result = salted_result \
    .groupBy("category_id") \
    .agg(
        sum("cnt").alias("total_pv"),
        sum("buy_cnt").alias("total_buy"),
        (sum("buy_cnt") / sum("cnt") * 100).alias("buy_rate")
    ) \
    .orderBy(col("total_pv").desc())

final_result.show(20)

print("\n加盐打散 — 完成！请查看Spark UI对比Task分布。")
```

**加盐的优缺点：**

```
优点:
  - 有效解决groupBy类操作的倾斜问题
  - 实现简单，效果明显

缺点:
  - 需要两次聚合（加盐聚合 + 去盐聚合）
  - 增加了计算量（通常可接受，因为并行度大幅提升）
  - 需要预先知道哪些Key是倾斜的
```

---

### 2.3 数据倾斜解决方案 — 方案2：Broadcast Join（40min）

**原理：**

```
问题: 大表(1亿行) JOIN 小表(1000行) on category_id
      → 如果使用SortMergeJoin，大表数据需要Shuffle，某个Key倾斜会导致Task倾斜

方案: 将小表广播到每个Executor的内存中
      → 大表不需要Shuffle！直接在Map端完成Join
      → 完全避免了数据倾斜！

适用条件: 小表 < 广播阈值（默认10MB，可调整到更大）
```

**完整代码实现：**

```python
from pyspark.sql.functions import broadcast

# ================================================================
# 方案2: Broadcast Join（小表Join大表）
# ================================================================

# 小表: 品类信息（1000行，约100KB）
category_df = spark.read.parquet("hdfs:///dim/category_info")
print(f"小表大小: {category_df.count()} 行")

# 大表: 用户行为数据（1亿行，约10GB）
behavior_df = spark.read.parquet("hdfs:///warehouse/user_behavior")
print(f"大表大小: {behavior_df.count()} 行")

# === 错误方式: 普通Join（会触发Shuffle，可能倾斜） ===
# result = behavior_df.join(category_df, "category_id")  # 默认SortMergeJoin

# === 正确方式: Broadcast Join ===
result = behavior_df.join(
    broadcast(category_df),  # 关键: 使用broadcast()函数
    "category_id"
)

# 验证: 查看执行计划
result.explain()
# 应该看到: BroadcastHashJoin 而不是 SortMergeJoin

result.show(10)

print("\nBroadcast Join — 完成！")

# === 调大广播阈值（如果小表在10MB~100MB之间） ===
spark.conf.set("spark.sql.autoBroadcastJoinThreshold", 100 * 1024 * 1024)  # 100MB
# 此后，Spark会自动判断：小于100MB的表自动使用Broadcast Join
```

**Broadcast Join的优缺点：**

```
优点:
  - 完全避免Shuffle，彻底解决倾斜
  - 性能极高（大表数据不需要重新分布）
  - Spark 3.0+自动判断（无需手动处理）

缺点:
  - 小表必须能放进Executor内存
  - 小表过大会导致OOM
  - 不适用于两个大表Join的场景
```

**广播阈值经验值：**

```
spark.sql.autoBroadcastJoinThreshold 设置建议:
  - Executor内存 4GB  → 阈值 100MB
  - Executor内存 8GB  → 阈值 200MB
  - Executor内存 16GB → 阈值 500MB
  
  注意: 不要超过 Executor内存的10%
```

---

### 2.4 数据倾斜解决方案 — 方案3：AQE自适应查询（30min）

**AQE（Adaptive Query Execution）是什么？**

```
Spark 3.0引入的重大特性:
  - 在运行时根据实际数据统计信息动态优化执行计划
  - 而不是依赖编译时的预估（往往不准确）

AQE三大功能:
  1. 动态合并小分区 (Coalesce Partitions)
  2. 动态切换Join策略 (Switch Join Strategy)
  3. 动态优化倾斜Join (Optimize Skew Join)
```

**完整代码实现：**

```python
# ================================================================
# 方案3: AQE自适应查询执行（Spark 3.0+）
# ================================================================

spark = SparkSession.builder \
    .appName("SkewSolution_AQE") \
    .config("spark.sql.adaptive.enabled", "true") \              # 启用AQE
    .config("spark.sql.adaptive.coalescePartitions.enabled", "true") \  # 合并小分区
    .config("spark.sql.adaptive.skewJoin.enabled", "true") \     # 倾斜Join优化
    .config("spark.sql.adaptive.skewJoin.skewedPartitionFactor", "5") \  # 倾斜判定系数
    .config("spark.sql.adaptive.skewJoin.skewedPartitionThresholdInBytes", "256MB") \  # 倾斜阈值
    .config("spark.sql.adaptive.localShuffleReader.enabled", "true") \  # 本地Shuffle读取
    .config("spark.sql.shuffle.partitions", "200") \            # 初始分区数
    .getOrCreate()

# 读取数据（可能包含倾斜的数据）
big_table = spark.read.parquet("hdfs:///data/big_table")
small_table = spark.read.parquet("hdfs:///data/small_table")

# 无需任何特殊代码！AQE自动检测倾斜并优化
result = big_table.join(small_table, "key_col")

result.show()

# 观察: 打开Spark UI → SQL/DataFrame页面
# 如果AQE介入，会看到:
#   - "OptimizeSkewedJoin" 标记
#   - 倾斜的分区被自动拆分
#   - 拆分成的小分区与另一侧的分区副本分别Join

print("\nAQE方式 — 完成！代码不需要任何特殊处理。")
```

**AQE自动优化倾斜Join的过程：**

```
检测到倾斜的分区A（数据量 > 256MB * 5 = 目标分区大小）:
  
  优化前:
    分区A(2GB) ←→ 分区B(10MB)
    1个Task处理 → 耗时极长
  
  AQE自动拆分:
    分区A_1(256MB) ←→ 分区B_副本1(10MB)
    分区A_2(256MB) ←→ 分区B_副本2(10MB)
    分区A_3(256MB) ←→ 分区B_副本3(10MB)
    ...
    8个Task并行处理 → 每个Task处理量大幅减少！
```

---

### 2.5 三种方案对比总结（20min）

| 方案 | 原理 | 适用场景 | 代码复杂度 | 效果 | 局限性 |
|------|------|----------|-----------|------|--------|
| 加盐打散 | 给倾斜Key加随机后缀 | groupBy聚合倾斜 | 中 | 好 | 需预知倾斜Key，两次聚合 |
| Broadcast Join | 小表广播到内存 | 小表Join大表 | 低 | 极好 | 小表必须能放进内存 |
| AQE自动处理 | 运行时动态优化 | Spark 3.0+，通用场景 | 极低 | 好 | 依赖Spark版本，不完全可控 |

**选择建议：**

```python
# 决策树:
if 小表 < 广播阈值:
    使用 Broadcast Join  # 最简单，效果最好
elif Spark版本 >= 3.0:
    使用 AQE  # 自动处理，零代码
else:
    使用 加盐打散  # 手动控制，最稳定
```

---

### 2.6 Shuffle优化（40min）

**2.6.1 分区数设置**

```python
# spark.sql.shuffle.partitions 是Spark最重要的性能参数之一！

# 默认: 200（对这个时代来说太小了！）
# 问题: 200个分区处理100GB数据 → 每个分区500MB → Task太大，GC频繁

# 经验设置公式:
# 分区数 = 总Shuffle数据量 / 目标分区大小
# 目标分区大小: 128MB ~ 256MB

# 示例:
# 总Shuffle数据量 100GB → 分区数 = 100GB/200MB = 500
# 总Shuffle数据量 1TB   → 分区数 = 1TB/200MB = 5000

spark.conf.set("spark.sql.shuffle.partitions", "500")  # 根据数据量调整

# 或者开启AQE让Spark自动调整:
spark.conf.set("spark.sql.adaptive.enabled", "true")
spark.conf.set("spark.sql.adaptive.coalescePartitions.enabled", "true")
spark.conf.set("spark.sql.adaptive.advisoryPartitionSizeInBytes", "256MB")
```

**2.6.2 压缩配置**

```python
# Shuffle数据压缩（减少网络IO和磁盘IO）
spark.conf.set("spark.shuffle.compress", "true")            # 压缩Shuffle输出
spark.conf.set("spark.shuffle.spill.compress", "true")      # 压缩溢写到磁盘的数据
spark.conf.set("spark.io.compression.codec", "snappy")      # 压缩算法

# 压缩算法对比:
# lz4:    最快，压缩率一般
# snappy: 平衡（推荐，Spark默认）
# zstd:   高压缩率，稍慢
```

**2.6.3 Shuffle机制选择**

```python
# Sort Shuffle vs Hash Shuffle
# Spark自动选择，一般不需要手动设置

# Sort Shuffle（默认，推荐）:
#   - 先写入内存缓冲区
#   - 内存满后排序并溢写到磁盘
#   - 最后合并多个溢写文件
#   - 优势: 磁盘文件少，已排序便于Reduce端Merge

spark.conf.set("spark.shuffle.sort.bypassMergeThreshold", "200")
# 当分区数<200时，使用BypassMergeSortShuffle（更快）
```

---

### 2.7 内存管理与Cache策略（40min）

**Spark内存模型：**

```
Executor总内存 (例如: 8GB):
├── Reserved Memory (保留内存, 300MB)
│   └── 用于Spark内部使用
│
├── User Memory (用户内存, 占总内存的 (1 - spark.memory.fraction))
│   └── 用户数据结构、Spark内部元数据
│
└── Spark Memory (统一内存池, 占总内存的 spark.memory.fraction, 默认0.6)
    ├── Storage Memory (存储内存, 50%)
    │   └── Cache数据、Broadcast变量
    │
    └── Execution Memory (执行内存, 50%)
        └── Shuffle、Sort、Aggregation、Join
```

**Cache和Persist策略对比：**

```python
from pyspark import StorageLevel

# Cache = persist(StorageLevel.MEMORY_AND_DISK)

# 策略对比:
# MEMORY_ONLY:            只在内存，不序列化 → 最快但内存占用大
# MEMORY_AND_DISK:        优先内存，不够溢写到磁盘 → 推荐！
# MEMORY_ONLY_SER:        内存中序列化 → 省内存但有CPU开销
# MEMORY_AND_DISK_SER:    序列化 + 磁盘溢写 → 最安全
# DISK_ONLY:              只存磁盘 → 最慢

df = spark.read.parquet("hdfs:///data/big_table")

# 示例1: 中间结果被多次使用 — 应该Cache
filtered_df = df.filter(col("dt") == "2024-01-01").cache()

# 第一次使用: 触发计算并缓存
result1 = filtered_df.groupBy("category_id").count()

# 第二次使用: 直接从缓存读取
result2 = filtered_df.groupBy("user_id").count()

# 第三次使用: 直接从缓存读取
result3 = filtered_df.agg(sum("amount"))

# 使用完毕后释放缓存
filtered_df.unpersist()

# 示例2: 使用Checkpoint（截断RDD Lineage，避免重算链过长）
spark.sparkContext.setCheckpointDir("hdfs:///checkpoint/")
# checkpoint需要Action触发，且会计算两次
# 更好的方式: 先cache，再checkpoint
important_df = df.filter(...).cache()
important_df.count()  # 先触发cache
# checkpoint_df = important_df.checkpoint() # 可选
```

**Cache最佳实践：**

```yaml
应该Cache:
  - 被多次使用的DataFrame
  - 经过昂贵计算（Shuffle/Join）的中间结果
  - 迭代算法中的中间状态

不应该Cache:
  - 只用一次的DataFrame（浪费内存）
  - 数据量超过可用内存的DataFrame（会导致频繁GC）
  - 流式数据（数据持续变化）
```

---

### 2.8 序列化优化（15min）

```python
# Kryo序列化（比Java序列化快10倍）
spark.conf.set("spark.serializer", "org.apache.spark.serializer.KryoSerializer")
spark.conf.set("spark.kryo.registrationRequired", "true")

# 注册自定义类（提升性能）
spark.conf.set("spark.kryo.classesToRegister", 
    "com.example.UserBehavior,com.example.OrderInfo")

# 注意:
# - RDD: 使用Kryo序列化
# - DataFrame: 使用Tungsten二进制格式（堆外内存），不需要Kryo
# - PySpark UDF: 涉及Python↔JVM数据交换，序列化开销大
```

---

## 三、实验任务：调优对比实验

### 3.1 制造倾斜数据

```python
"""
生成倾斜的测试数据
"""
import random

def generate_skewed_data(output_path, num_records=10_000_000):
    """生成倾斜的模拟数据"""
    with open(output_path, 'w') as f:
        for i in range(num_records):
            # 80%的数据集中在2个Key上（模拟倾斜）
            if random.random() < 0.4:
                category_id = 100  # 倾斜Key 1（40%数据）
            elif random.random() < 0.6:
                category_id = 200  # 倾斜Key 2（40%数据 → 80% total）
            else:
                category_id = random.randint(1, 1000)  # 其他Key（20%数据）
            
            user_id = random.randint(1, 100000)
            behavior = random.choice(['pv', 'pv', 'pv', 'buy', 'cart', 'fav'])
            
            f.write(f"{user_id},{category_id},{behavior},{random.randint(1, 500)}\n")

# 生成1000万行测试数据
generate_skewed_data("/tmp/skewed_data.csv", 10_000_000)
```

### 3.2 对比三种方案

```python
"""
对比实验: 三种倾斜处理方案

运行每个方案，记录:
  1. 总执行时间
  2. Stage数量
  3. Shuffle Write/Read数据量
  4. 最慢Task耗时 vs 中位数Task耗时
  5. Task数量分布
"""

import time

# ===== 方案0: 不处理倾斜（基线） =====
print("=" * 60)
print("方案0: 不处理倾斜（基线）")
print("=" * 60)

df = spark.read.option("header", "false").csv("file:///tmp/skewed_data.csv") \
    .toDF("user_id", "category_id", "behavior", "amount")

start = time.time()
result0 = df.groupBy("category_id").count().orderBy(col("count").desc())
result0.show(5)
elapsed0 = time.time() - start
print(f"方案0 耗时: {elapsed0:.2f}s")
print("请打开Spark UI查看Task分布...")

# ===== 方案1: 加盐打散 =====
print("\n" + "=" * 60)
print("方案1: 加盐打散")
print("=" * 60)

SALT = 100
start = time.time()

salted = df.withColumn("salt", (rand() * SALT).cast("int"))

result1 = salted.groupBy("salt", "category_id").count() \
    .groupBy("category_id").agg(sum("count").alias("total")) \
    .orderBy(col("total").desc())

result1.show(5)
elapsed1 = time.time() - start
print(f"方案1 耗时: {elapsed1:.2f}s")
print("请打开Spark UI查看Task分布...")

# ===== 方案2: AQE自动处理 =====
print("\n" + "=" * 60)
print("方案2: AQE自动处理")
print("=" * 60)

# 需要重启SparkSession或恢复默认配置
spark.conf.set("spark.sql.adaptive.enabled", "true")
spark.conf.set("spark.sql.adaptive.coalescePartitions.enabled", "true")

start = time.time()
result2 = df.groupBy("category_id").count().orderBy(col("count").desc())
result2.show(5)
elapsed2 = time.time() - start
print(f"方案2 耗时: {elapsed2:.2f}s")
print("请打开Spark UI查看Task分布...")

# ===== 汇总对比 =====
print("\n" + "=" * 60)
print("性能对比汇总")
print("=" * 60)
print(f"{'方案':<20} {'耗时(s)':<15} {'改善':<15}")
print("-" * 50)
print(f"{'方案0: 不处理':<20} {elapsed0:<15.2f} {'基准':<15}")
print(f"{'方案1: 加盐打散':<20} {elapsed1:<15.2f} {((1-elapsed1/elapsed0)*100):<15.1f}%")
print(f"{'方案2: AQE':<20} {elapsed2:<15.2f} {((1-elapsed2/elapsed0)*100):<15.1f}%")
```

---

## 四、课堂练习（60min）

### 练习1：诊断倾斜（20min）

```
给你一组Spark UI截图（讲师准备），请判断:
  1. 是否存在数据倾斜？
  2. 倾斜发生在哪个Stage？
  3. 倾斜的Key可能是哪个？
  4. 推荐使用哪种解决方案？为什么？
```

### 练习2：手写倾斜解决方案（20min）

```python
"""
场景: 用户行为表 user_behavior (10亿行)
      商品信息表 product_info (5万行)
      
  需要计算: 每个品类的销售额 = SUM(amount)
  
  已知: 品类100的销售额占总额的60%（严重倾斜）
  
任务: 
  1. 写出不使用广播Join的处理代码
  2. 写出使用广播Join的处理代码
  3. 分析两种方案的优劣
"""
```

### 练习3：Cache策略决策（20min）

```python
"""
以下哪些DataFrame应该Cache？为什么？

场景: ETL Pipeline
  步骤A: 读取原始数据 → df_a (100GB)
  步骤B: df_a.filter() → df_b (10GB)
  步骤C: df_b.join(dim_table) → df_c (10GB) 
  步骤D: df_c.groupBy() → df_d (1GB)
  
  后续使用:
  - df_c 被用于3种不同的聚合分析
  - df_d 被写入Hive
  - df_b 不再使用
"""
```

---

## 五、课后作业

### 作业1：数据倾斜实验报告（必做）

```
任务:
  1. 编写脚本生成1000万行倾斜数据（1个Key占70%数据）
  2. 分别用三种方案处理:
     a. 不处理（基线）
     b. 加盐打散
     c. AQE（如果是Spark3.0+）
  3. 每种方案运行3次取平均时间
  4. 截图每种方案的Spark UI Task分布
  5. 填写对比报告:

| 方案 | 总耗时 | Shuffle Write | Shuffle Read | 最慢Task | 中位数Task |
|------|--------|---------------|--------------|----------|-----------|
| 不处理 | | | | | |
| 加盐   | | | | | |
| AQE   | | | | | |

分析:
  - 哪种方案效果最好？
  - 哪种方案最省心？
  - 你推荐使用哪种？为什么？
```

### 作业2：内存Cache实验（必做）

```
任务:
  1. 创建一个被多次使用的DataFrame
  2. 对比以下4种策略的性能:
     - 不Cache
     - Cache(MEMORY_ONLY)
     - Cache(MEMORY_AND_DISK)  
     - Cache + Checkpoint
  3. 每种策略运行3次取平均
  4. 观察Spark UI Storage页面
  5. 输出对比报告
```

### 作业3：分区数实验（必做）

```
任务:
  1. 处理100MB的Shuffle数据
  2. 分别设置分区数为: 1, 10, 50, 200, 500, 1000
  3. 记录每种配置的执行时间
  4. 找出最佳分区数
  5. 解释为什么分区数不是越多越好
```

### 作业4：综合诊断（选做）

```
场景: 你的同事写了一个Spark任务，运行了2小时还没出结果。
      请按照以下步骤进行系统性诊断:

  1. 打开Spark UI检查各个Stage
  2. 检查是否存在数据倾斜
  3. 检查Shuffle数据量是否过大
  4. 检查是否有不必要的Shuffle操作
  5. 检查Cache使用是否合理
  6. 检查资源配置是否合理
  7. 给出优化建议和预期效果
  
  输出: 诊断报告（包含问题、证据、建议、预期改善）
```

---

## 六、Spark性能调优检查清单（Checklist）

```yaml
数据层面:
  ☐ 是否存在数据倾斜？(Max Task / Median Task > 3？)
  ☐ 文件格式是否为列式存储(Parquet/ORC)？
  ☐ 是否使用了分区表并按分区过滤？
  ☐ 是否需要抽样而不是全量处理？

配置层面:
  ☐ spark.sql.shuffle.partitions 是否合理？
  ☐ spark.sql.adaptive.enabled 是否开启？（Spark 3.0+）
  ☐ spark.sql.autoBroadcastJoinThreshold 是否合理？
  ☐ spark.serializer 是否使用Kryo？
  ☐ spark.memory.fraction 配置是否合理？

Cache层面:
  ☐ 被多次使用的DataFrame是否已Cache？
  ☐ Cache的StorageLevel是否合理？
  ☐ 不再使用的DataFrame是否已unpersist？

代码层面:
  ☐ 是否使用了broadcast()给小表？
  ☐ reduceByKey vs groupByKey：是否选择了前者？
  ☐ filter是否前置（尽早减少数据量）？
  ☐ UDF是否可用内置函数替代？
  ☐ 是否有不必要的distinct或orderBy？

资源层面:
  ☐ Executor数量和内存是否合理？
  ☐ 是否启用了动态资源分配？
```

---

## 七、参考资料

1. **Spark性能调优官方指南**：https://spark.apache.org/docs/latest/tuning.html
2. **AQE设计文档**：https://issues.apache.org/jira/browse/SPARK-23128
3. **《Spark快速大数据分析》**：第8章 Spark调优与调试
4. **Databricks Blog**：https://www.databricks.com/blog/2020/05/29/adaptive-query-execution-in-speeding-up-spark-sql-at-runtime.html