# 项目10：Spark/Flink生产级调优攻坚

> **项目定位**：L3阶段核心实战项目，直面生产环境"烂任务"，从倾斜→Shuffle→GC→Cache一路调优至生产标准
>
> **周期**：第27-30周（4周，共40h） | **数据规模**：100TB模拟输入 | **核心要求**：每个优化步骤必须有对比数据

---

## 项目概述

### 初始任务（故意构造的问题任务）

| 问题维度 | 具体表现 | 影响 |
|----------|----------|------|
| 数据倾斜 | 1个Key占80%的数据量 | 某个Task跑2小时，其他Task只需2分钟 |
| Shuffle配置 | 默认200分区（spark.sql.shuffle.partitions=200） | 数据量大时单Task处理数据过多 |
| UDF实现 | Python UDF逐行处理 | 序列化开销大、无法利用Catalyst优化 |
| Cache策略 | 没有任何Cache | 重复计算相同的中间结果 |
| Executor配置 | 内存过小（executor-memory=2g） | 频繁GC、甚至OOM |
| 序列化 | 默认Java序列化 | 序列化速度慢、占用空间大 |
| 数据格式 | 输入为CSV TextFile | 无列式存储优势、无谓词下推 |

**初始运行指标**（作为Baseline）：

| 指标 | 初始值 | 说明 |
|------|--------|------|
| 总运行时间 | 预估8-12小时 | 无法完成/频繁失败 |
| 数据倾斜程度 | 最慢Task/中位数Task = 50x+ | 极端不均衡 |
| Shuffle数据量 | 预估20TB+ | 严重膨胀 |
| GC时间占比 | >30% | 大量时间花在GC上 |
| 成功率 | <20% | 经常因为OOM/超时失败 |

---

## 调优步骤详细说明

### 第1步：数据倾斜解决（8h）

#### 1.1 倾斜诊断（2h）

**任务**：先诊断，再开药

**诊断方法**：
1. 打开Spark UI → Stage页面 → 查看Task数据量分布
2. 筛选出Shuffle Read Size最大的Task
3. 通过 `df.groupBy("key").count().orderBy($"count".desc).show(20)` 确认倾斜Key
4. 使用 `df.groupBy("key").count().describe()` 查看数据分布统计

**诊断记录模板**：
```yaml
倾斜诊断报告:
  Stage ID: 3（Shuffle阶段）
  Task总数: 200
  Task处理数据量分布:
    最小值: 5MB
    P25: 20MB
    P50: 50MB
    P75: 100MB
    P95: 500MB
    最大值: 8GB ← 这是倾斜的Task
  倾斜Key: key="user_id_00001"
  倾斜Key占比: 78.3%
  受影响的Task: Task 42, Task 87, Task 156
```

#### 1.2 方案A：加盐（Salt）重分区（2h）

**原理**：给倾斜Key加随机前缀，打散到多个分区处理，最后去前缀聚合

**实施代码**：
```scala
// 加盐重分区方案
val saltNum = 100  // 将倾斜Key打散为100份

// Step 1: 给倾斜Key加随机盐值
val salted = df.withColumn(
  "salt",
  when(col("user_id") === "user_id_00001",  // 只给倾斜Key加盐
    (rand() * saltNum).cast("int")
  ).otherwise(0)
).withColumn(
  "salted_key",
  concat(col("user_id"), lit("_"), col("salt"))
)

// Step 2: 第一次聚合（在加盐的Key上）
val partialResult = salted
  .groupBy("salted_key")
  .agg(sum("amount").as("partial_sum"))

// Step 3: 去盐，最终聚合
val finalResult = partialResult
  .withColumn("original_key", 
    split(col("salted_key"), "_")(0))
  .groupBy("original_key")
  .agg(sum("partial_sum").as("total_sum"))
```

**对比数据记录表**：

| 指标 | 倾斜解决前 | 加盐方案 | 改善比例 |
|------|-----------|----------|----------|
| 最慢Task耗时 | | | |
| Task耗时标准差 | | | |
| Shuffle Write大小 | | | |
| 总运行时间 | | | |
| 数据均匀度 | | | |

#### 1.3 方案B：Broadcast Join（2h）

**适用条件**：倾斜发生在Join操作中，且小表可以放入内存

**实施代码**：
```scala
import org.apache.spark.sql.functions.broadcast

// 小表：维度表（几千到几百万行）
val smallDimTable = spark.read.parquet("dim_table")  // 1000行

// 大表：事实表（包含倾斜Key）
val bigFactTable = spark.read.parquet("fact_table")   // 1亿行

// Broadcast Join：小表被广播到每个Executor，避免Shuffle
val result = bigFactTable.join(
  broadcast(smallDimTable),
  "key"
)
```

**Broadcast条件检查**：
```scala
// 验证小表是否足够小（默认阈值10MB）
val smallTableSize = spark.sessionState
  .executePlan(smallDimTable.queryExecution.logical)
  .optimizedPlan.stats.sizeInBytes
println(s"小表预估大小: ${smallTableSize / 1024 / 1024} MB")
println(s"Broadcast阈值: ${spark.conf.get("spark.sql.autoBroadcastJoinThreshold")}")

// 如果超过阈值但内存足够，手动调大阈值
spark.conf.set("spark.sql.autoBroadcastJoinThreshold", 
  (100L * 1024 * 1024).toString)  // 调大到100MB
```

**对比数据记录表**：

| 指标 | SortMergeJoin | BroadcastHashJoin | 改善比例 |
|------|---------------|-------------------|----------|
| Shuffle Write大小 | | | |
| Join阶段耗时 | | | |
| 内存使用 | | | |
| 总运行时间 | | | |

#### 1.4 方案C：AQE自动倾斜处理（2h）

**原理**：Spark 3.0+的AQE在运行时检测倾斜Partition，自动拆分

**启用AQE倾斜处理**：
```scala
spark.conf.set("spark.sql.adaptive.enabled", "true")
spark.conf.set("spark.sql.adaptive.coalescePartitions.enabled", "true")
spark.conf.set("spark.sql.adaptive.skewJoin.enabled", "true")
spark.conf.set("spark.sql.adaptive.skewJoin.skewedPartitionFactor", "5")  // 超过中位数5倍视为倾斜
spark.conf.set("spark.sql.adaptive.skewJoin.skewedPartitionThresholdInBytes", "256MB")  // 至少256MB
```

**验证AQE是否生效**：
```scala
// 在Spark UI中查看：
// 1. SQL/DataFrame Tab → 点击具体的查询
// 2. 查看是否有 "OptimizeSkewedJoin" 标记
// 3. 查看Partition是否被自动拆分

// 或者在日志中搜索
grep "OptimizeSkewedJoin" spark-executor.log
```

**三种方案对比总结**：

| 方案 | 适用场景 | 优点 | 缺点 | 推荐指数 |
|------|----------|------|------|----------|
| 加盐重分区 | GroupBy聚合倾斜 | 完全解决倾斜 | 需要修改代码，增加一次Shuffle | ★★★★ |
| Broadcast Join | Join小表 | 性能最好，无Shuffle | 小表必须能放入内存 | ★★★★★ |
| AQE自动处理 | 运行时不可预测的倾斜 | 无需修改代码 | 依赖Spark 3.0+，效果不如手动精细控制 | ★★★ |

#### 第1步强制输出
- 倾斜诊断报告（包含Spark UI截图 + Task分布数据）
- 至少2种方案的对比数据（运行时间、Task分布、Shuffle数据量）
- 选择最优方案的理由

---

### 第2步：Shuffle优化（8h）

#### 2.1 分区数调优实验（3h）

**实验矩阵**：

```scala
// 固定数据量不变，变化 spark.sql.shuffle.partitions
val partitions = Seq(200, 400, 800, 1600, 3200)

for (p <- partitions) {
  spark.conf.set("spark.sql.shuffle.partitions", p.toString)
  
  val start = System.currentTimeMillis()
  val result = df
    .groupBy("key")
    .agg(sum("amount").as("total"))
  result.count()  // 触发计算
  
  val elapsed = System.currentTimeMillis() - start
  println(s"Partitions=$p, Time=${elapsed}ms")
}
```

**最佳分区数估算公式**：
```
推荐分区数 = Shuffle数据总量 / 每个Task的理想处理量（128-256MB）

例如: Shuffle数据总量 = 200GB
  推荐分区数 = 200GB / 200MB ≈ 1000
  建议设为 800-1200 之间（留有余地）
```

**对比数据记录表**：

| 分区数 | 总运行时间 | Shuffle Write | Shuffle Read | 平均Task数据量 | 最大Task数据量 | Task数 |
|--------|-----------|---------------|-------------|---------------|---------------|--------|
| 200 | | | | | | |
| 400 | | | | | | |
| 800 | | | | | | |
| 1600 | | | | | | |
| 3200 | | | | | | |

#### 2.2 Shuffle压缩对比（2h）

```scala
// 对比不同压缩算法
val compressCodecs = Seq("lz4", "snappy", "zstd")

for (codec <- compressCodecs) {
  spark.conf.set("spark.io.compression.codec", codec)
  spark.conf.set("spark.shuffle.compress", "true")
  // 运行相同任务，记录：
  // 1. Shuffle文件总大小
  // 2. Shuffle Write/Read时间
  // 3. 压缩和解压缩的CPU使用率
}
```

#### 2.3 Shuffle其他参数调优（3h）

| 参数 | 默认值 | 推荐范围 | 原理 |
|------|--------|----------|------|
| `spark.shuffle.file.buffer` | 32KB | 64KB-128KB | 增大缓冲区可减少磁盘Seek次数 |
| `spark.reducer.maxSizeInFlight` | 48MB | 96MB | 增大Reduce端拉取数据的内存缓冲 |
| `spark.shuffle.io.maxRetries` | 3 | 5-10 | 网络不稳定时增加重试 |
| `spark.shuffle.io.retryWait` | 5s | 10s-30s | 重试等待间隔 |
| `spark.shuffle.sort.bypassMergeThreshold` | 200 | 根据分区数调整 | 分区数少时跳过排序，直接用Hash |

```scala
// 实验：调整shuffle.file.buffer
val buffers = Seq("32k", "64k", "128k", "256k")
for (buf <- buffers) {
  spark.conf.set("spark.shuffle.file.buffer", buf)
  // 运行任务，记录Shuffle Write时间和磁盘IO
}
```

#### 第2步强制输出
- 分区数 vs 运行时间的折线图
- 最佳分区数的计算过程
- Shuffle压缩算法对比报告
- 最终推荐的Shuffle参数配置

---

### 第3步：UDF优化（8h）

#### 3.1 识别低效UDF（2h）

**如何找出低效UDF**：
```scala
// 1. 在Spark UI的SQL Tab中查看执行计划
// 存在 "BatchEvalPython" 或 "ArrowEvalPython" 节点的 → 有UDF

// 2. 用SparkListener收集每个算子的耗时
spark.sparkContext.addSparkListener(new SparkListener() {
  override def onTaskEnd(taskEnd: SparkListenerTaskEnd) {
    // 记录每个Task在不同阶段的耗时
  }
})
```

**UDF效率对比测试**：
```scala
// 场景：将字符串转换为大写并去除空格
// 方案A：Python UDF
val pythonUpper = udf((s: String) => s.trim.toUpperCase)
val resultA = df.withColumn("clean", pythonUpper($"text"))

// 方案B：Pandas UDF（向量化）
val pandasUpper = pandas_udf((s: pd.Series) => s.str.strip().str.upper(), StringType)
val resultB = df.withColumn("clean", pandasUpper($"text"))

// 方案C：内置函数
val resultC = df.withColumn("clean", upper(trim($"text")))

// 对比三种方案的执行时间
```

#### 3.2 Python UDF → 内置函数（2h）

**常见Python UDF的可替代方案**：

| Python UDF操作 | 等价的内置函数 | 备注 |
|----------------|---------------|------|
| `s.strip()` | `trim(col)` | 完全等价 |
| `s.upper()` / `s.lower()` | `upper(col)` / `lower(col)` | 完全等价 |
| `len(s)` | `length(col)` | 完全等价 |
| `s.replace("a", "b")` | `regexp_replace(col, "a", "b")` | 等价 |
| `s.startswith("prefix")` | `col.startsWith("prefix")` | 等价 |
| `datetime.strptime(s, fmt)` | `to_timestamp(col, fmt)` | 等价 |
| `float(s)` | `col.cast("double")` | 等价 |
| `hash(s)` | `hash(col)` | 等价 |

**自查清单**：
- [ ] 我在用Python UDF做字符串操作吗？→ 找对应的内置函数
- [ ] 我在用Python UDF做类型转换吗？→ 用 `cast()`
- [ ] 我在用Python UDF做日期处理吗？→ 用 `to_date()`/`date_format()`
- [ ] 我在用Python UDF做数学运算吗？→ 直接用 `col + col` / `col * col`

#### 3.3 Python UDF → Pandas UDF（2h）

**当必须使用UDF时的选择**：

```scala
// Python UDF（逐行处理）— 最慢
val slowUDF = udf((x: Int) => {
  Thread.sleep(1)  // 模拟复杂处理
  x * 2
})
// 处理100万行需要: 100万 × 1ms = 1000秒！

// Pandas UDF（向量化处理）— 快10-100倍
val fastUDF = pandas_udf((x: pd.Series) => {
  x * 2  // Pandas的向量化操作，一次处理一批
}, IntegerType)
// 处理100万行需要: 每批10000行 × 100批 × ~2ms = ~200ms
```

**Pandas UDF的三种类型**：

| 类型 | 输入 | 输出 | 用途 |
|------|------|------|------|
| Series to Series | `pd.Series` | `pd.Series` | 逐列变换（如标准化） |
| Iterator of Series | `Iterator[pd.Series]` | `Iterator[pd.Series]` | 有状态的变换 |
| Iterator of Tuple | `Iterator[Tuple]` | `Iterator[pd.Series]` | 多列输入，单列输出 |

#### 3.4 避免UDF的架构层面优化（2h）

**在数据源头解决问题**：
- 如果UDF是在做数据清洗 → 能否在数据入库时就清理好？
- 如果UDF是在做特征工程 → 能否用Spark SQL表达式或者ML Pipeline替代？
- 如果UDF是在调用外部服务 → 能否批量化调用而不是逐条调用？

#### 第3步强制输出
- UDF效率对比报告（Python UDF vs Pandas UDF vs 内置函数）
- 列出优化前使用的所有UDF，以及优化后的替代方案
- 如果无法替代，说明原因和最优选择

---

### 第4步：内存与GC调优（8h）

#### 4.1 GC日志收集与分析（2h）

**启用GC日志**：
```bash
# spark-submit时添加
--conf "spark.executor.extraJavaOptions=-XX:+PrintGCDetails 
  -XX:+PrintGCDateStamps 
  -Xloggc:/tmp/gc-executor-%p.log 
  -XX:+UseGCLogFileRotation 
  -XX:NumberOfGCLogFiles=10 
  -XX:GCLogFileSize=10M"
```

**GCViewer分析**：
1. 下载 GCViewer (https://github.com/chewiebug/GCViewer)
2. 导入GC日志文件
3. 分析以下指标：
   - GC次数/时间分布
   - Full GC频率
   - 堆内存使用趋势
   - GC暂停时间

#### 4.2 GC策略对比（3h）

**对比G1GC和ParallelGC**：

```scala
// 方案A：ParallelGC（Spark默认）
--conf "spark.executor.extraJavaOptions=-XX:+UseParallelGC 
  -XX:ParallelGCThreads=4"

// 方案B：G1GC（推荐生产环境）
--conf "spark.executor.extraJavaOptions=-XX:+UseG1GC 
  -XX:MaxGCPauseMillis=200   // 目标：每次GC暂停不超过200ms
  -XX:G1HeapRegionSize=8M     // G1 Region大小
  -XX:InitiatingHeapOccupancyPercent=35  // 堆占用达到35%时触发并发标记
  -XX:ConcGCThreads=4"
```

**GC策略对比数据记录表**：

| 指标 | ParallelGC | G1GC | 改善 |
|------|-----------|------|------|
| Young GC次数 | | | |
| Young GC总耗时 | | | |
| Full GC次数 | | | |
| Full GC总耗时 | | | |
| 最大GC暂停时间 | | | |
| GC时间占总运行时间比例 | | | |
| 堆内存使用峰值 | | | |

#### 4.3 Executor内存配置优化（3h）

**内存分配公式**：
```
Executor总内存 = spark.executor.memory
  ├── Reserved Memory (300MB)
  ├── User Memory (40% of remaining)
  │    └── 用户自定义数据结构
  └── Spark Memory (60% of remaining, 由 spark.memory.fraction 控制)
       ├── Storage Memory (50%, 由 spark.memory.storageFraction 控制)
       │    └── Cache、Broadcast变量
       └── Execution Memory (50%)
            └── Shuffle、Join、Sort、Aggregation

示例: executor-memory=8g
  Reserved: 300MB
  可用: 8g - 300MB ≈ 7.7g
  User Memory: 7.7g × 0.4 ≈ 3.1g
  Spark Memory: 7.7g × 0.6 ≈ 4.6g
    Storage Memory: ~2.3g
    Execution Memory: ~2.3g
```

**内存调优参数**：

| 参数 | 默认值 | 调整建议 |
|------|--------|----------|
| `spark.executor.memory` | 1g | 按需上调至4g-16g |
| `spark.memory.fraction` | 0.6 | 如果Cache多，降至0.4给User更多空间 |
| `spark.memory.storageFraction` | 0.5 | 如果Shuffle大，降至0.3给Execution更多空间 |
| `spark.executor.memoryOverhead` | max(384MB, 0.1×executor-memory) | 如果频繁OOM，增大到0.15-0.2 |
| `spark.executor.cores` | 1(YARN) | 建议3-5个（过多cores竞用内存） |

#### 第4步强制输出
- GC日志分析报告（附GCViewer截图）
- GC策略对比数据（至少对比2种GC策略）
- 最终推荐的Executor内存配置和理由

---

### 第5步：Cache策略对比（8h）

#### 5.1 Cache策略实验矩阵（4h）

```scala
import org.apache.spark.storage.StorageLevel

// 场景：一个被多次使用的中间DataFrame
val midDF = df
  .filter($"status" === "completed")
  .groupBy("user_id")
  .agg(sum("amount").as("total_amount"))

// 策略1：不Cache（Baseline）
// 每次Action都会重新计算

// 策略2：MEMORY_ONLY
midDF.persist(StorageLevel.MEMORY_ONLY)

// 策略3：MEMORY_AND_DISK
midDF.persist(StorageLevel.MEMORY_AND_DISK)

// 策略4：MEMORY_AND_DISK_SER（使用Kryo序列化）
midDF.persist(StorageLevel.MEMORY_AND_DISK_SER)

// 策略5：DISK_ONLY
midDF.persist(StorageLevel.DISK_ONLY)

// 策略6：Checkpoint
spark.sparkContext.setCheckpointDir("hdfs:///checkpoint/")
midDF.checkpoint()
```

**每种策略执行3次Action，记录每次耗时**：

| 策略 | 第1次Action耗时 | 第2次Action耗时 | 第3次Action耗时 | Storage内存使用 | 磁盘使用 |
|------|----------------|----------------|----------------|----------------|----------|
| 不Cache | | | | 0 | 0 |
| MEMORY_ONLY | | | | | |
| MEMORY_AND_DISK | | | | | |
| MEMORY_AND_DISK_SER | | | | | |
| DISK_ONLY | | | | | |
| Checkpoint | | | | | |

#### 5.2 Cache vs Checkpoint的选择（2h）

```
Cache (persist):
  触发: 第一次Action时计算并缓存
  存储: Memory/Disk（按StorageLevel）
  Lineage: 保留完整Lineage（如果缓存丢失，可重算）
  用途: 在同一个Job中被反复使用的中间结果

Checkpoint:
  触发: 显式调用 checkpoint() + Action
  存储: 外部可靠存储（HDFS/S3）
  Lineage: 截断Lineage（恢复时直接从Checkpoint读取）
  用途: 
    - Lineage特别长的迭代计算
    - 需要跨Job复用的中间结果
    - 实现断点续跑
```

**选择决策树**：
```
这个中间结果会被用几次？
  ├── 1次 → 不需要Cache
  ├── 2-3次 → Cache(MEMORY_AND_DISK_SER)
  └── 多次 + Lineage过长 → 考虑Checkpoint

数据量有多大？
  ├── < 可用内存 → MEMORY_ONLY 或 MEMORY_AND_DISK_SER
  ├── > 可用内存 → MEMORY_AND_DISK_SER
  └── ≫ 可用内存 → DISK_ONLY 或 Checkpoint

需要跨Job复用？
  └── 是 → Checkpoint（Cache在Application结束后失效）
```

#### 5.3 Kryo序列化优化（2h）

```scala
// 默认Java序列化 vs Kryo序列化
spark.conf.set("spark.serializer", 
  "org.apache.spark.serializer.KryoSerializer")
spark.conf.set("spark.kryo.registrationRequired", "true")  // 严格模式

// 注册常用类
spark.conf.set("spark.kryo.classesToRegister",
  "org.apache.spark.sql.Row,scala.collection.immutable.Map")
```

**序列化对比实验**：

| 序列化方式 | 序列化后大小 | 序列化耗时 | 反序列化耗时 | 备注 |
|-----------|-------------|-----------|-------------|------|
| Java Serialization | | | | 默认 |
| Kryo (未注册类) | | | | |
| Kryo (已注册类) | | | | 最快 |

#### 第5步强制输出
- Cache策略对比数据表（6种策略 × 3次Action的完整数据）
- Cache vs Checkpoint选择决策树
- 序列化对比报告
- 针对当前任务的最佳Cache方案及理由

---

## 最终调优报告

### 报告结构

```markdown
# Spark生产级调优攻坚报告

## 1. 初始状态
- 任务描述
- 数据规模和特征
- 初始运行指标（时间、资源、成功率）
- 发现的问题列表（按严重程度排序）

## 2. 调优过程记录
### 2.1 第一步：数据倾斜解决
- 倾斜诊断结果
- 尝试的方案及数据对比
- 最终选择方案及理由

### 2.2 第二步：Shuffle优化
- 分区数实验数据
- 压缩算法对比
- 最终Shuffle配置

### 2.3 第三步：UDF优化
- 定位的低效UDF列表
- 替代方案及性能对比
- 最终UDF使用清单

### 2.4 第四步：内存与GC调优
- GC问题诊断
- GC策略对比
- 最终JVM参数配置

### 2.5 第五步：Cache策略
- 各策略性能数据
- 最终Cache方案

## 3. 最终运行状态
- 运行时间（优化前 → 优化后）
- 资源使用（优化前 → 优化后）
- 成功率（优化前 → 优化后）

## 4. 调优Checklist（可直接用于生产评审）
- [ ] 数据倾斜检查
- [ ] Shuffle分区数检查
- [ ] UDF效率检查
- [ ] GC策略检查
- [ ] Cache策略检查
- [ ] 序列化方式检查
- [ ] 数据格式检查

## 5. 通用调优方法论总结
- 不要什么场景下都适用的银弹
- 哪些优化有副作用需要注意
- 调优的优先级排序框架
```

### 必须包含的对比数据模板

```yaml
数据对比模板:
  实验环境:
    集群规模: X台 × Y核 × Z GB
    Spark版本: 3.x.x
    数据量: xxx TB
    
  指标对比:
    总运行时间:
      优化前: xxx min → 优化后: xxx min (缩短 xx%)
    Shuffle数据量:
      优化前: xxx GB → 优化后: xxx GB (减少 xx%)
    Task时间分布:
      优化前: 最慢/中位数 = xx → 优化后: 最慢/中位数 = xx
    GC时间占比:
      优化前: xx% → 优化后: xx%
    内存使用峰值:
      优化前: xx GB → 优化后: xx GB
    成功率:
      优化前: xx% → 优化后: 100%
```

### 调优优先级排序框架

```
紧急程度:
  P0 (立即修复): 导致任务无法完成的
    - OOM → 内存配置
    - 任务超时 → 数据倾斜
  P1 (本周内): 严重影响性能但不阻塞的
    - 数据倾斜不严重但明显影响
    - shuffle分区数不合理
  P2 (本月内): 性能优化
    - UDF优化
    - Cache策略优化
  P3 (有需要时): 锦上添花
    - Kryo序列化
    - 数据格式优化

优化投入产出比:
  高投入产出比: 加几个参数就能显著提升
    - spark.sql.shuffle.partitions
    - spark.sql.adaptive.enabled
    - broadcast()
  中投入产出比: 需要少量代码修改
    - 加盐重分区
    - 内置函数替代UDF
  低投入产出比: 需要大量修改或基础设施升级
    - 数据格式从CSV改为Parquet
    - 改变整体计算架构
```

---

## 评分标准

| 评分维度 | 权重 | 优秀（90-100） | 合格（70-89） | 不合格（<70） |
|----------|------|---------------|--------------|--------------|
| 数据完整性 | 30% | 每步优化有完整对比数据，多种方案交叉验证 | 大部分步有对比数据 | 数据不完整或只有"感觉变快了" |
| 原理分析深度 | 25% | 能解释每个优化为什么有效，原理层面剖析 | 能说出原因但不深入 | 只说改了参数，不知道为什么 |
| 方法论提炼 | 20% | 提炼出可复用的调优方法论和Checklist | 有针对这个任务的方法论 | 只针对当前任务，缺乏通用性 |
| 最终优化效果 | 15% | 运行时间缩短90%+，成功率100% | 缩短50%+，成功率>90% | 改善不明显 |
| 报告质量 | 10% | 结构清晰，图表完整，结论有说服力 | 报告完整 | 报告混乱 |

---

## 交付物清单

- [ ] 倾斜诊断报告（含Spark UI截图）
- [ ] 3种倾斜解决方案的对比数据
- [ ] Shuffle分区数实验数据（含折线图）
- [ ] Shuffle压缩算法对比报告
- [ ] UDF效率对比报告
- [ ] GC日志分析报告（含GCViewer分析截图）
- [ ] GC策略对比数据表
- [ ] 6种Cache策略的完整对比数据
- [ ] 序列化方式对比报告
- [ ] 完整的最终调优报告（Markdown格式）
- [ ] 生产环境调优Checklist
- [ ] 通用的调优方法论文档