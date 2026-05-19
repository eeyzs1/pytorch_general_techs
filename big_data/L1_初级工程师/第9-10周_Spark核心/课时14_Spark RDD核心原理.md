# 课时14：Spark RDD核心原理

> **课时时长**：8小时（理论3h + 编码实战3h + 练习2h）
>
> **难度等级**：⭐⭐⭐⭐⭐ 核心重点（L1阶段最关键的课时）

---

## 一、教学目标

1. **理解Spark vs MapReduce的本质差异**：能从内存计算、DAG调度、编程抽象三个维度解释Spark为什么快
2. **掌握RDD五大特性**：能背出并解释分区列表、计算函数、依赖关系、分区器、优先位置
3. **理解Transformation vs Action**：掌握惰性求值(Lazy Evaluation)机制，能判断一个操作是Transformation还是Action
4. **理解宽依赖vs窄依赖**：能判断Shuffle的触发条件，能手动画出Stage划分
5. **能手写RDD代码**：独立完成WordCount、PV/UV统计、TopN等核心程序
6. **能看懂Spark UI**：通过DAG图理解作业的执行过程

---

## 二、教学内容

### 2.1 为什么Spark比MapReduce快？（30min）

**MapReduce的痛点：**

```
MapReduce迭代计算的问题（例如PageRank、K-Means）：

  迭代1: HDFS读取 → Map → Reduce → HDFS写入
  迭代2: HDFS读取 → Map → Reduce → HDFS写入
  迭代3: HDFS读取 → Map → Reduce → HDFS写入
  ...
  
  每次迭代都要读写磁盘！
  - 磁盘IO是瓶颈
  - 序列化/反序列化开销大
  - 每次都要重新启动Map/Reduce Task

Spark的解决方案——内存计算：

  迭代1: HDFS读取 → 计算 → 内存缓存(RDD)
  迭代2: 内存读取 → 计算 → 内存缓存(RDD)  ← 直接从内存读！
  迭代3: 内存读取 → 计算 → 内存缓存(RDD)
  ...
  
  只有第一次从HDFS读，后续都在内存中
  → 快10-100倍！
```

**Spark快在哪里？（三个层面）：**

```
层面1: 内存计算 vs 磁盘计算
  MapReduce: 每次Shuffle都写磁盘
  Spark: Shuffle写磁盘但中间结果优先内存，迭代计算优势巨大

层面2: DAG执行引擎 vs 固定Map-Reduce模式
  MapReduce: 每个作业 = Map + Reduce，复杂逻辑需要多个MR作业串联
  Spark: 一个作业可以有任意多个操作，DAG一次调度完成

层面3: 线程模型 vs 进程模型
  MapReduce: 每个Task启动一个新JVM进程（启动开销大）
  Spark: Executor是常驻JVM进程，Task是线程（启动开销小）
```

---

### 2.2 RDD核心概念（60min）

**RDD（Resilient Distributed Dataset）弹性分布式数据集：**

```
RDD = 一个不可变的、分区的、可并行操作的数据集合

拆解"弹性分布式"四个字:
  - 弹性(Resilient): 数据丢失可以自动从Lineage(血统)重建
  - 分布式(Distributed): 数据分布在集群多个节点上
  - 数据集(Dataset): 存储数据的集合
```

**RDD五大特性（必背！面试高频）：**

```
1. 分区列表(A list of partitions)
   → RDD由多个Partition组成，Partition是数据的最小单元
   → 每个Partition被一个Task处理
   → 分区数决定并行度

2. 计算函数(A function for computing each split)
   → 每个Partition上的计算逻辑
   → 如: map(f), flatMap(f), filter(f)

3. 依赖关系(A list of dependencies on other RDDs)
   → 记录父RDD → 子RDD的转换关系
   → 用于容错重建(Lineage)

4. 分区器(Optionally, a Partitioner for key-value RDDs)
   → 控制数据如何分布到各个Partition
   → 如: HashPartitioner, RangePartitioner

5. 优先位置(Optionally, a list of preferred locations)
   → 数据在哪个节点上，就在哪个节点上计算
   → "移动计算比移动数据更划算"
```

**RDD创建方式：**

```python
from pyspark import SparkContext, SparkConf

conf = SparkConf().setAppName("RDDBasics").setMaster("local[*]")
sc = SparkContext(conf=conf)

# 方式1: 从集合创建（用于学习和测试）
rdd_from_list = sc.parallelize([1, 2, 3, 4, 5], numSlices=3)
# 分区情况: [1,2] [3,4] [5]

# 方式2: 从外部存储读取（生产环境最常用）
rdd_from_hdfs = sc.textFile("hdfs://namenode:9000/data/sample.txt")
rdd_from_local = sc.textFile("file:///home/data/sample.txt")

# 方式3: 从其他RDD转换而来
rdd_transformed = rdd_from_list.map(lambda x: x * 2)
```

---

### 2.3 Transformation vs Action（40min）

**核心概念——惰性求值（Lazy Evaluation）：**

```
Transformation（转换操作）: 返回新RDD，延迟执行
  → map, flatMap, filter, reduceByKey, groupByKey, join, ...
  → 只是"记录"了要做什么，并不真正计算

Action（行动操作）: 返回结果到Driver或写入外部存储，触发计算
  → collect, count, take, reduce, saveAsTextFile, foreach, ...
  → 真正触发DAG执行

类比理解:
  Transformation = 写菜谱（告诉厨师要做什么菜）
  Action = 下单（厨师才真正开始做菜）
```

**常见Transformation和Action对比：**

| Transformation | 说明 | 是否Shuffle | Action | 说明 |
|---------------|------|------------|--------|------|
| map(func) | 对每个元素应用func | 否(窄) | collect() | 返回所有元素到Driver |
| flatMap(func) | 对每个元素应用func并扁平化 | 否(窄) | count() | 返回元素总数 |
| filter(func) | 过滤元素 | 否(窄) | take(n) | 返回前n个元素 |
| reduceByKey | 按Key聚合 | 是(宽) | first() | 返回第一个元素 |
| groupByKey | 按Key分组 | 是(宽) | saveAsTextFile | 写入文件 |
| sortBy | 排序 | 是(宽) | foreach(func) | 对每个元素执行func |
| join | 连接两个RDD | 可能宽 | reduce(func) | 聚合所有元素 |
| distinct | 去重 | 是(宽) | top(n) | 返回最大的n个 |

**惰性求值验证实验：**

```python
# 实验：观察Transformation和Action的执行时机

# 步骤1: 创建RDD
rdd = sc.parallelize([1, 2, 3, 4, 5])
print("创建RDD — 不会执行")  # 立即打印

# 步骤2: Transformation — 不会执行！
rdd2 = rdd.map(lambda x: x * 2)
print("map Transformation — 不会执行")  # 立即打印

rdd3 = rdd2.filter(lambda x: x > 5)
print("filter Transformation — 不会执行")  # 立即打印

# 步骤3: Action — 此时才真正执行！
result = rdd3.collect()  # 触发所有Transformation的执行
print(f"collect Action — 触发执行, 结果: {result}")
```

---

### 2.4 宽依赖 vs 窄依赖（40min）

**窄依赖（Narrow Dependency）：**

```
定义: 父RDD的每个Partition最多被子RDD的一个Partition使用

特点:
  - 不需要Shuffle（数据不需要跨节点移动）
  - 可以在同一个Stage内流水线执行(Pipeline)
  - 可以合并执行（编译器优化）

示例操作: map, flatMap, filter, mapPartitions, union

图解:
  父RDD:   [P0] [P1] [P2] [P3]
            │    │    │    │
            ▼    ▼    ▼    ▼
  子RDD:   [P0] [P1] [P2] [P3]
  
  一对一的关系，无Shuffle！
```

**宽依赖（Wide Dependency / Shuffle Dependency）：**

```
定义: 父RDD的Partition被多个子RDD的Partition使用

特点:
  - 需要Shuffle（数据需要跨节点重新分配）
  - Stage的边界，必须等待Shuffle完成
  - 性能瓶颈所在

示例操作: reduceByKey, groupByKey, sortBy, join(非broadcast), distinct

图解:
  父RDD:   [P0] [P1] [P2] [P3]
            │╲  ╱│╲  ╱│╲  ╱│
            ▼  ▼ ▼  ▼ ▼  ▼ ▼
  子RDD:   [P0] [P1] [P2] [P3]
  
  多对多的关系，需要Shuffle！
```

**关键判断——map和reduceByKey的区别：**

```python
# map — 窄依赖（每个元素独立转换，不需要看其他元素）
rdd.map(lambda x: x * 2)

# reduceByKey — 宽依赖（需要把相同Key的数据汇集到一起）
rdd.reduceByKey(lambda a, b: a + b)
# 疑问: 为什么需要汇集？因为reduceByKey需要知道所有相同Key的值！
```

---

### 2.5 DAG调度与Stage划分（40min）

**DAG是什么？**

```
DAG = Directed Acyclic Graph（有向无环图）

Spark将所有的RDD操作组成一个DAG:
  - 节点 = RDD
  - 边 = Transformation

当遇到Action时，DAG被提交给DAGScheduler:
  1. DAGScheduler从后往前回溯DAG
  2. 遇到宽依赖就划分一个Stage
  3. 每个Stage包含一连串的窄依赖操作（可Pipeline执行）
```

**Stage划分图解（必画）：**

```
代码:
  lines = sc.textFile("hdfs://...")           # RDD1
  words = lines.flatMap(lambda l: l.split())  # RDD2, 窄
  pairs = words.map(lambda w: (w, 1))         # RDD3, 窄
  counts = pairs.reduceByKey(lambda a,b:a+b)  # RDD4, 宽(Shuffle!)
  filtered = counts.filter(lambda x: x[1]>10) # RDD5, 窄
  sorted_result = filtered.sortBy(lambda x:-x[1]) # RDD6, 宽(Shuffle!)

DAG图:
  RDD1 ──窄──→ RDD2 ──窄──→ RDD3 ──宽──→ RDD4 ──窄──→ RDD5 ──宽──→ RDD6

Stage划分:
  ┌──────── Stage0 ─────────┐  ┌── Stage1 ──┐  ┌── Stage2 ──┐
  │ RDD1 → RDD2 → RDD3     │  │ RDD4→RDD5  │  │    RDD6    │
  └─────────────────────────┘  └─────────────┘  └────────────┘
           │                         │                │
     Shuffle Write            Shuffle Read      Shuffle Write
                              Shuffle Write     Shuffle Read
  
  每个Stage内部: 窄依赖可以合并成一个Task流水线执行
  Stage之间: 必须等待Shuffle完成
```

---

### 2.6 RDD 完整代码实战（90min）

**实战1：经典WordCount（理解每个操作）**

```python
from pyspark import SparkContext, SparkConf

conf = SparkConf() \
    .setAppName("WordCount") \
    .setMaster("local[*]") \
    .set("spark.driver.memory", "2g")
sc = SparkContext(conf=conf)

# 读取文本文件
lines = sc.textFile("hdfs://namenode:9000/data/sample.txt")

# WordCount — 理解每一步
word_counts = (lines
    # 1. flatMap: 按空格分割每行，返回所有单词的扁平列表
    #    输入: "Hello World" → 输出: ["Hello", "World"]
    .flatMap(lambda line: line.split())
    
    # 2. map: 将每个单词转换为 (word, 1)
    #    输入: "Hello" → 输出: ("hello", 1)
    .map(lambda word: (word.lower(), 1))
    
    # 3. reduceByKey: 按Key(word)聚合Value(计数)
    #    Shuffle发生在这里！
    #    输入: ("hello", [1,1,1,1]) → 输出: ("hello", 4)
    .reduceByKey(lambda a, b: a + b)
    
    # 4. filter: 过滤低频词（出现次数>5的才保留）
    .filter(lambda x: x[1] > 5)
    
    # 5. sortBy: 按计数降序排序
    #    Shuffle发生在这里！
    .sortBy(lambda x: -x[1])
)

# 查看DAG（非常重要！）
print("=" * 50)
print("RDD DAG (Lineage):")
print(word_counts.toDebugString())
print("=" * 50)

# Action: 触发计算
results = word_counts.collect()

print("\nTop 20 words:")
for word, count in results[:20]:
    print(f"  {word:20s} → {count}")

# 保存结果到HDFS
word_counts.saveAsTextFile("hdfs://namenode:9000/output/wordcount")

sc.stop()
```

**实战2：PV/UV统计（面试必考）**

```python
from pyspark import SparkContext, SparkConf

conf = SparkConf().setAppName("PV_UV").setMaster("local[*]")
sc = SparkContext(conf=conf)

# 模拟日志数据格式: IP,URL,TIMESTAMP
log_data = [
    "192.168.1.1,/index.html,2024-01-01 10:00:00",
    "192.168.1.2,/index.html,2024-01-01 10:01:00",
    "192.168.1.1,/products.html,2024-01-01 10:02:00",
    "192.168.1.3,/index.html,2024-01-01 10:03:00",
    "192.168.1.2,/cart.html,2024-01-01 10:04:00",
    "192.168.1.1,/index.html,2024-01-01 10:05:00",
]

logs_rdd = sc.parallelize(log_data)

# ===== PV统计（Page View） =====
# PV = 每个页面的访问次数
pv = (logs_rdd
    .map(lambda line: line.split(","))           # 解析CSV格式
    .map(lambda fields: (fields[1], 1))          # (URL, 1)
    .reduceByKey(lambda a, b: a + b)             # 按URL聚合
    .sortBy(lambda x: -x[1])                      # 按PV降序
)

print("=== PV统计 ===")
for url, count in pv.collect():
    print(f"  {url:30s} PV: {count}")

# ===== UV统计（Unique Visitor） =====
# UV = 每个页面的独立访客数
uv = (logs_rdd
    .map(lambda line: line.split(","))
    .map(lambda fields: ((fields[1], fields[0]), 1))  # ((URL, IP), 1)
    .reduceByKey(lambda a, b: a + b)                   # 去重 ⇒ 每个(URL,IP)只有一条
    .map(lambda x: (x[0][0], 1))                       # (URL, 1)
    .reduceByKey(lambda a, b: a + b)                   # 按URL聚合
    .sortBy(lambda x: -x[1])
)

print("\n=== UV统计 ===")
for url, count in uv.collect():
    print(f"  {url:30s} UV: {count}")

# ===== 按小时统计 =====
hourly_pv = (logs_rdd
    .map(lambda line: line.split(","))
    .map(lambda fields: (fields[2][:13], 1))           # 提取小时: "2024-01-01 10"
    .reduceByKey(lambda a, b: a + b)
    .sortBy(lambda x: x[0])
)

print("\n=== 每小时PV ===")
for hour, count in hourly_pv.collect():
    print(f"  {hour}:00  PV: {count}")

sc.stop()
```

**实战3：TopN问题 — 两种实现方式**

```python
"""
TopN问题: 找出每个品类销售额最高的N个商品

数据格式: category_id, product_id, sales_amount
"""

data = [
    "1,P001,1000.00", "1,P002,800.00", "1,P003,1200.00", "1,P004,500.00",
    "2,P005,2000.00", "2,P006,1500.00", "2,P007,1800.00",
    "3,P008,300.00", "3,P009,400.00", "3,P010,350.00", "3,P011,250.00",
]
N = 2  # Top 2

# ===== 方式1: groupByKey + 排序（数据量大时容易OOM） =====
topn_method1 = (sc.parallelize(data)
    .map(lambda line: line.split(","))
    .map(lambda fields: (fields[0], (fields[1], float(fields[2]))))  # (cat, (prod, amount))
    .groupByKey()  # 注意：groupByKey可能导致OOM
    .mapValues(lambda products: sorted(products, key=lambda x: -x[1])[:N])
    .flatMapValues(lambda x: x)
)

print("=== TopN 方式1: groupByKey ===")
for category, (product, amount) in topn_method1.collect():
    print(f"  Category {category}: {product} = ¥{amount}")

# ===== 方式2: reduceByKey + 本地TopN（推荐，更高效） =====
def merge_topn(list1, list2, n):
    """合并两个TopN列表，保持TopN"""
    merged = list1 + list2
    merged.sort(key=lambda x: -x[1])
    return merged[:n]

# 先将每条记录转换为单元素列表
topn_method2 = (sc.parallelize(data)
    .map(lambda line: line.split(","))
    .map(lambda fields: (fields[0], [(fields[1], float(fields[2]))]))
    # 在Map端先做聚合，减少Shuffle的数据量！
    .reduceByKey(lambda a, b: merge_topn(a, b, N))
    .mapValues(lambda products: [f"{p[0]}:¥{p[1]}" for p in products])
)

print("\n=== TopN 方式2: reduceByKey + 本地TopN ===")
for category, products in topn_method2.collect():
    print(f"  Category {category}: {products}")

sc.stop()
```

**实战4：RDD Join操作**

```python
"""
场景: 关联用户表和订单表

用户表(user_id, name, city):
  101,张三,北京
  102,李四,上海
  103,王五,广州

订单表(order_id, user_id, amount):
  O001,101,299.00
  O002,101,150.00
  O003,102,500.00
  O004,104,100.00  (注意: 用户104在用户表中不存在)
"""

users_data = ["101,张三,北京", "102,李四,上海", "103,王五,广州"]
orders_data = ["O001,101,299.00", "O002,101,150.00", "O003,102,500.00", "O004,104,100.00"]

users_rdd = sc.parallelize(users_data) \
    .map(lambda l: l.split(",")) \
    .map(lambda f: (f[0], (f[1], f[2])))  # (user_id, (name, city))

orders_rdd = sc.parallelize(orders_data) \
    .map(lambda l: l.split(",")) \
    .map(lambda f: (f[1], (f[0], float(f[2]))))  # (user_id, (order_id, amount))

# ===== Inner Join: 只保留两表都有的Key =====
inner_join = users_rdd.join(orders_rdd)
print("=== Inner Join ===")
for user_id, (user_info, order_info) in inner_join.collect():
    name, city = user_info
    order_id, amount = order_info
    print(f"  {user_id} | {name} | {city} | {order_id} | ¥{amount}")

# ===== Left Outer Join: 保留左表所有Key =====
left_join = users_rdd.leftOuterJoin(orders_rdd)
print("\n=== Left Outer Join ===")
for user_id, (user_info, order_info) in left_join.collect():
    name, city = user_info
    if order_info is not None:
        order_id, amount = order_info
        print(f"  {user_id} | {name} | {city} | {order_id} | ¥{amount}")
    else:
        print(f"  {user_id} | {name} | {city} | (无订单)")

# ===== 统计每个用户的总消费金额 =====
user_total = orders_rdd \
    .mapValues(lambda x: x[1]) \
    .reduceByKey(lambda a, b: a + b) \
    .join(users_rdd) \
    .map(lambda x: (x[1][1][0], x[0], x[1][0]))  # (name, user_id, total)

print("\n=== 用户总消费 ===")
for name, user_id, total in user_total.sortBy(lambda x: -x[2]).collect():
    print(f"  {name}({user_id}): ¥{total:.2f}")

sc.stop()
```

---

### 2.7 查看Spark UI与DAG（实验20min）

```python
"""
在运行Spark作业时，打开Spark Web UI查看DAG:

1. 本地模式: http://localhost:4040
2. YARN模式: 通过ResourceManager跳转

重点关注:
  - Jobs页面: 每个Action对应一个Job
  - Stages页面: 每个Job包含多个Stage
  - DAG Visualization: 可以看到RDD的转换链
  - Storage页面: 查看缓存的RDD
  - Executors页面: 查看资源使用

模拟长时间运行的任务，便于观察UI:
"""
import time
from pyspark import SparkContext, SparkConf

conf = SparkConf() \
    .setAppName("SparkUI_Demo") \
    .setMaster("local[*]")
sc = SparkContext(conf=conf)

# 创建一个有多个Stage的任务
rdd = sc.parallelize(range(1, 10000001), numSlices=8)

result = (rdd
    .map(lambda x: (x % 100, x))           # Stage 0
    .reduceByKey(lambda a, b: a + b)       # Stage 1 (Shuffle)
    .map(lambda x: (x[0], x[1] * 2))       # Stage 1 (合并到同一Stage)
    .sortBy(lambda x: -x[1])               # Stage 2 (Shuffle)
)

# 触发Action
print("作业开始，请打开 http://localhost:4040 观察...")
top10 = result.take(10)
print(f"Top 10: {top10}")

# 保持应用运行，便于观察UI
print("\n应用保持运行60秒，请抓紧观察Spark UI...")
print("观察完按Ctrl+C退出")
time.sleep(60)

sc.stop()
```

---

## 三、课堂练习（90min）

### 练习1：手动画Stage划分图（20min）

```python
# 给定以下代码，在纸上画出完整的Stage划分图
rdd1 = sc.textFile("hdfs://...")
rdd2 = rdd1.flatMap(lambda x: x.split())
rdd3 = rdd2.map(lambda x: (x, 1))
rdd4 = rdd3.reduceByKey(lambda a, b: a + b)
rdd5 = rdd4.filter(lambda x: x[1] > 10)
rdd6 = rdd4.map(lambda x: (x[1], x[0]))
rdd7 = rdd6.sortByKey(ascending=False)
rdd8 = rdd7.take(100)

# 要求:
# 1. 标注每个RDD的编号
# 2. 标注窄依赖(N)和宽依赖(W)
# 3. 画出Stage边界
# 4. 标注每个Stage包含哪些RDD
```

### 练习2：完整RDD编程（40min）

```yaml
题目: 日志分析系统

数据格式(sample.log):
  IP 时间 方法 URL 协议 状态码 响应大小 响应时间

任务:
  1. 读取日志文件，解析每条记录
  2. 统计每个URL的PV（访问量）
  3. 统计每个URL的UV（独立IP数）
  4. 统计每个HTTP状态码的数量
  5. 找出响应时间最长的10个请求
  6. 统计每小时的QPS（每秒请求数 ≈ 该小时请求总数/3600）
  7. 找出访问量最多的5个IP地址

要求:
  - 全部使用RDD API
  - 每个统计结果格式化输出
  - 绘制DAG图
```

### 练习3：RDD操作分类竞赛（15min）

```
将以下操作分为 Transformation(T)、Action(A)、宽依赖(W)、窄依赖(N):

1.  map        2.  filter        3.  flatMap
4.  collect    5.  count         6.  reduceByKey
7.  groupByKey 8.  sortBy        9.  join
10. take       11. saveAsTextFile 12. distinct
13. union      14. sample        15. foreach

答案示例: map: T, N
```

### 练习4：对比reduceByKey和groupByKey（15min）

```python
"""
写两个程序分别用reduceByKey和groupByKey做WordCount，
对比两个程序在Spark UI上的差异:
  1. Stage数量
  2. Shuffle Read/Write数据量
  3. 执行时间

哪一个更好？为什么？
"""
```

---

## 四、课后作业

### 作业1：RDD API实现日志分析系统（必做）

完成课堂练习2的所有任务，提交：
1. 完整的Python代码
2. 运行结果截图
3. Spark UI的DAG图截图
4. 每个阶段的Stage解释

### 作业2：对比MapReduce和Spark的WordCount（必做）

```
任务:
  1. 用Java MapReduce实现WordCount（使用课时12的代码）
  2. 用PySpark RDD实现WordCount
  3. 使用不同的文件大小(1MB, 10MB, 100MB, 1GB)测试
  4. 记录两个版本的执行时间
  5. 画出性能对比图表
  6. 分析Spark快在哪里

输出: 对比实验报告（含数据、图表、分析）
```

### 作业3：RDD五大特性理解（必做）

用自己的话写出RDD的五大特性，并各举一个代码示例说明该特性的体现。每个特性不少于200字。

### 作业4：思考题（选做）

```yaml
Q1: 如果reduceByKey时某个Key的数据量特别大（几GB），会发生什么？
Q2: 既然Spark比MapReduce快，为什么还要学MapReduce？
Q3: RDD的Lineage(血统)越长越好吗？会有什么问题？
Q4: 什么是"Stage内Pipeline执行"？请举例说明。
```

---

## 五、参考资料

1. **RDD论文**：*Resilient Distributed Datasets: A Fault-Tolerant Abstraction for In-Memory Cluster Computing (2012)*
2. **Spark官方RDD文档**：https://spark.apache.org/docs/latest/rdd-programming-guide.html
3. **《Spark快速大数据分析》**：第3-5章
4. **Spark UI分析指南**：https://spark.apache.org/docs/latest/web-ui.html