# Spark SQL Catalyst源码深潜路线

> **目标**：深入Spark SQL Catalyst优化器源码，理解从DataFrame API调用到最终RDD执行的完整流程
>
> **周期**：4周 | **总代码量**：约5000行核心代码（Catalyst + Tungsten） | **强制输出**：每周1篇源码分析文章（2000+字）

---

## 总体路线图

```
                    ┌─────────────┐
                    │ DataFrame/  │  ← 第1周：API表层
                    │  Dataset    │
                    └──────┬──────┘
                           │
                    ┌──────▼──────┐
                    │ Unresolved  │
                    │ LogicalPlan │
                    └──────┬──────┘
                           │  Catalog + Analysis Rules
                    ┌──────▼──────┐
                    │  Resolved   │
                    │ LogicalPlan │
                    └──────┬──────┘
                           │  ← 第2周：逻辑优化层
                    ┌──────▼──────┐
                    │  Optimized  │
                    │ LogicalPlan │  (RuleExecutor + 20+优化Rule)
                    └──────┬──────┘
                           │
                    ┌──────▼──────┐  ← 第3周：物理计划层
                    │  SparkPlan  │  (SparkPlanner + Strategy)
                    └──────┬──────┘
                           │
                    ┌──────▼──────┐
                    │   Selected  │
                    │  Physical   │  (Cost-Based Optimization)
                    │    Plan     │
                    └──────┬──────┘
                           │
                    ┌──────▼──────┐  ← 第4周：代码生成
                    │ WholeStage  │
                    │  CodeGen    │  (Janino编译 → RDD执行)
                    └─────────────┘
```

---

## 第1周：DataFrame API表层 — 从API调用到LogicalPlan

### 本周目标
理解`df.select().filter().groupBy()`等API调用如何构建LogicalPlan树

### 阅读文件清单

| 优先级 | 文件 | 行数估计 | 阅读时间 | 关键类 |
|--------|------|----------|----------|--------|
| ★★★ | `sql/core/src/main/scala/org/apache/spark/sql/Dataset.scala` | ~6000行 | 重点阅读300行 | Dataset |
| ★★★ | `sql/core/src/main/scala/org/apache/spark/sql/DataFrame.scala` | ~200行 | 全读 | DataFrame |
| ★★ | `sql/catalyst/src/main/scala/org/apache/spark/sql/catalyst/plans/logical/basicLogicalOperators.scala` | ~1000行 | 读核心5个 | Project, Filter, Aggregate, Join, Sort |
| ★★ | `sql/catalyst/src/main/scala/org/apache/spark/sql/catalyst/plans/logical/LogicalPlan.scala` | ~400行 | 全读 | LogicalPlan, QueryPlan |
| ★ | `sql/core/src/main/scala/org/apache/spark/sql/SparkSession.scala` | ~500行 | 读createDataFrame相关 | SparkSession |
| ★ | `sql/catalyst/src/main/scala/org/apache/spark/sql/catalyst/trees/TreeNode.scala` | ~600行 | 了解 | TreeNode |

### 每日任务拆解

#### Day 1（3h）：搭建源码阅读环境
```bash
# 1. Clone Spark源码（选择一个稳定的Tag，如v3.5.0）
git clone https://github.com/apache/spark.git
cd spark
git checkout v3.5.0

# 2. 构建项目（跳过测试加速）
./build/mvn -DskipTests clean package

# 3. 导入IntelliJ IDEA
# 安装Scala插件
# Open as Maven项目
# 等待索引完成
```

**环境验证任务**：
- 找到 `Dataset.scala` 中 `select()` 方法的实现
- 在 `select()` 方法的第一行打断点
- 写一个简单的 `spark.range(10).select("id").show()` 测试
- Debug模式运行，观察调用栈

#### Day 2（3h）：深入Dataset.scala — 核心API入口
**阅读重点**：

1. **`select()` 方法**（找源码中的定义行）
   - 参数类型：`Column*`
   - 内部如何将 `Column` 转换为 `Expression`
   - 最终调用 `selectUntyped()` → `Project`
   - 关键代码路径：`select()` → `withPlan(Project(...))`

2. **`filter()` / `where()` 方法**
   - 参数类型：`Column` 或 `String`
   - 内部如何构建 `Filter` LogicalPlan节点
   - 注意：`filter(condition: Column)` 和 `filter(conditionExpr: String)` 的实现差异

3. **`groupBy()` 方法**
   - 返回类型：`RelationalGroupedDataset`（不是Dataset！）
   - `RelationalGroupedDataset` 和 `Dataset` 的关系
   - `agg()` 如何构造 `Aggregate` 逻辑计划

4. **`join()` 方法**
   - 多种重载：等值Join、条件Join、Cross Join
   - 内部如何构建 `Join` LogicalPlan节点
   - Join类型枚举（Inner/LeftOuter/RightOuter/FullOuter/...）

**强制实验——跟踪一条语句的完整调用链**：
```scala
// 在REPL或IDEA中执行以下代码，逐步Debug跟踪每个方法调用
val df = spark.range(100).toDF("id")
val result = df
  .select($"id", ($"id" % 10).as("bucket"))
  .filter($"bucket" > 3)
  .groupBy("bucket")
  .count()

result.explain(true)  // 查看完整的LogicalPlan树
// result.queryExecution.logical  — 未解析的逻辑计划
// result.queryExecution.analyzed — 解析后的逻辑计划
```

**输出任务**：写一篇"一个 `DataFrame.select().filter().groupBy()` 到底做了什么"的源码分析文章，必须包含：
- 调用链路图（从API调用到LogicalPlan节点创建）
- 关键代码片段（带你标注的注释）
- 对应的LogicalPlan树结构图

#### Day 3（3h）：深入LogicalPlan树结构
**阅读重点**：

1. **TreeNode.scala**
   - `children` 方法：每个节点如何访问子节点
   - `transformDown` / `transformUp`：树的遍历方式
   - `mapChildren`：子节点的替换（用于规则优化）
   - `foreach` / `collect` / `collectFirst`：树的查询方法
   - **为什么用递归遍历而不是迭代？**

2. **LogicalPlan vs SparkPlan**
   - `LogicalPlan`（catalyst包）：描述"做什么"（What）
   - `SparkPlan`（execution包）：描述"怎么做"（How）
   - 为什么需要将逻辑和物理分开？

3. **关键LogicalPlan节点**
   - `Project`：SELECT子句 → `projectList: Seq[NamedExpression]`
   - `Filter`：WHERE子句 → `condition: Expression`
   - `Aggregate`：GROUP BY → `groupingExpressions` + `aggregateExpressions`
   - `Join`：JOIN → `left` + `right` + `joinType` + `condition`
   - `Sort`：ORDER BY → `order: Seq[SortOrder]`
   - `LocalRelation`：本地数据（如 `spark.range()`）

**课堂练习**：
- 给定一个SQL语句，手写对应的LogicalPlan树结构
- 给定一个LogicalPlan树，还原对应的SQL语句

#### Day 4（3h）：QueryExecution — 从DataFrame到执行的桥梁
**阅读文件**：`sql/core/src/main/scala/org/apache/spark/sql/execution/QueryExecution.scala`

**阅读重点**：
1. **QueryExecution的懒执行机制**
   - `logical` → `analyzed` → `optimizedPlan` → `sparkPlan` → `executedPlan`
   - 每个步骤的触发时机
   - `assertAnalyzed()`：何时触发Analysis阶段

2. **阶段转换**
   ```
   logical ──Analyzer──→ analyzed ──Optimizer──→ optimizedPlan
                                                        ↓
   executedPlan ←─preparations── sparkPlan ←─Planner──
   ```
   每个阶段的输入/输出类型

3. **`explain()` 方法**
   - `explain()` / `explain(true)` / `explain("extended")` 的区别
   - 如何从explain的输出中判断优化是否生效

**实验任务**：
```scala
// 对同一个DataFrame执行不同的Action，观察QueryExecution的复用
val df = spark.read.parquet("...")
val qe1 = df.filter($"id" > 10).queryExecution
val result1 = df.filter($"id" > 10).count()  // 触发了什么？
val result2 = df.filter($"id" > 10).collect()  // 复用了什么？
// 观察 qe1 中的各阶段状态变化
```

### 第1周强制输出
- **源码分析文章**："从DataFrame.select()到LogicalPlan的完整调用链"（2000+字）
- **架构图**：DataFrame API → LogicalPlan节点的映射关系图
- **代码提交**：包含至少5个Debug截图的源码阅读笔记

### 第1周常见陷阱
1. **不要迷失在Scala语法中**：`implicit`、`type class`、`implicit conversion`等——先理解意图，再理解语法
2. **Dataset.scala有6000+行**：不要试图全读完，只读select/filter/groupBy/join/agg等核心方法
3. **不要跳过TreeNode**：不理解树的遍历机制，后面的Optimizer会看不懂

---

## 第2周：Catalyst逻辑优化 — RuleExecutor与优化Rule

### 本周目标
理解Catalyst的Rule-Based Optimization（RBO），深入3个经典优化Rule的源码

### 阅读文件清单

| 优先级 | 文件 | 行数估计 | 阅读时间 | 关键类 |
|--------|------|----------|----------|--------|
| ★★★ | `sql/catalyst/src/main/scala/org/apache/spark/sql/catalyst/rules/RuleExecutor.scala` | ~200行 | 全读 | RuleExecutor |
| ★★★ | `sql/catalyst/src/main/scala/org/apache/spark/sql/catalyst/optimizer/Optimizer.scala` | ~2000行 | 读核心20个Rule | Optimizer, 各种Rule |
| ★★★ | `sql/catalyst/src/main/scala/org/apache/spark/sql/catalyst/optimizer/PushDownPredicates.scala` | ~200行 | 全读 | PushDownPredicate |
| ★★ | `sql/catalyst/src/main/scala/org/apache/spark/sql/catalyst/optimizer/ColumnPruning.scala` | ~200行 | 全读 | ColumnPruning |
| ★★ | `sql/catalyst/src/main/scala/org/apache/spark/sql/catalyst/optimizer/ConstantFolding.scala` | ~100行 | 全读 | ConstantFolding |
| ★★ | `sql/catalyst/src/main/scala/org/apache/spark/sql/catalyst/optimizer/JoinReorder.scala` | ~150行 | 全读 | CostBasedJoinReorder |
| ★ | `sql/catalyst/src/main/scala/org/apache/spark/sql/catalyst/optimizer/NullPropagation.scala` | ~150行 | 了解 | NullPropagation |
| ★ | `sql/catalyst/src/main/scala/org/apache/spark/sql/catalyst/optimizer/SimplifyConditionals.scala` | ~100行 | 了解 | SimplifyConditionals |

### 每日任务拆解

#### Day 1（3h）：RuleExecutor — 优化引擎的"心脏"

**阅读文件**：`RuleExecutor.scala`

**核心数据结构**：
```scala
abstract class RuleExecutor[TreeType <: TreeNode[_]] {
  // Batch：一组优化Rule的集合
  // Rule：对一棵树进行变换的规则
  // Strategy：规则应用策略（Once / FixedPoint）
  
  def execute(plan: TreeType): TreeType = {
    // 核心逻辑：对每个Batch，依次应用其中的Rule
    // FixedPoint策略：不断应用规则直到树不再变化
    // Once策略：每个规则只应用一次
  }
}
```

**关键问题（必须能回答）**：
1. `FixedPoint(100)` 中的100是什么意思？为什么需要一个上限？
2. Batch之间的执行顺序重要吗？为什么？
3. 一个Batch内部的多个Rule是按什么顺序执行的？
4. 如果Rule A的输出是Rule B的输入（A触发B），但A和B在不同Batch中，怎么办？
5. RuleExecutor如何知道"树已经不再变化"？（SideEffect-Free + 比较变换前后的树）

**动手实验**：
```scala
// 在IDEA中，给 Optimizer.defaultBatches 的每个Rule打断点
// 运行一个简单的SQL：SELECT count(*) FROM table
// 观察：
// 1. 哪些Rule被触发了？
// 2. 每个Rule被应用了多少次？
// 3. Rule的应用顺序是什么？
```

#### Day 2（3h）：Predicate Pushdown — 谓词下推（最经典的优化Rule）

**阅读文件**：`PushDownPredicates.scala`

**核心理解**：
```
优化前:
  Filter(age > 18)
    └── Join(users, orders, users.id = orders.user_id)

优化后:
  Join(users, orders, users.id = orders.user_id)
    ├── Filter(age > 18) ── users
    └── orders
```

**源码阅读路径**：
1. `PushDownPredicate` 对象中的 `apply` 方法
2. 如何处理 `Filter` + `Join` 的组合？
   - 哪些条件可以被推到Join的左侧？
   - 哪些条件可以被推到Join的右侧？
   - 哪些条件只能在Join之后执行？
3. 如何处理 `Filter` + `Project` 的组合？
4. 如何处理 `Filter` + `Aggregate` 的组合？
   - HAVING vs WHERE的区别在这里如何体现？

**实验任务**：
```sql
-- 实验1：观察PushDownPredicate的效果
EXPLAIN EXTENDED
SELECT u.name, o.total
FROM users u JOIN orders o ON u.id = o.user_id
WHERE u.age > 18 AND o.total > 100 AND u.city = 'Beijing';
-- 问题：哪些Filter条件被下推了？下推到了哪个表？
-- 问题：哪些Filter条件留在了Join之后？为什么？
```

#### Day 3（3h）：Column Pruning + Constant Folding

**Column Pruning（列剪裁）**：
```
优化前:
  Project(name, age)
    └── Scan(users: id, name, age, city, email, phone)

优化后:
  Project(name, age)
    └── Scan(users: name, age)  ← 只读需要的列！
```

**阅读重点**：
1. 如何确定"哪些列被使用了"？
2. `Project` → `Aggregate` → `Join` 的列需求是如何逐层向上传递的？
3. 如果我写了 `SELECT *`，列剪裁还有效果吗？

**Constant Folding（常量折叠）**：
```
优化前:
  SELECT price * (1 + 0.1) FROM products
优化后:
  SELECT price * 1.1 FROM products
```

**阅读重点**：
1. `Literal` 是什么类型？
2. 哪些运算是可以折叠的？（算术、逻辑、Cast）
3. 为什么不把 `SELECT * FROM table WHERE dt = date_sub(current_date(), 1)` 中的 `date_sub(current_date(), 1)` 也折叠掉？

**实验任务**：
```scala
val df = spark.read.parquet("users")  // 100个字段
val result = df.select("name", "age").filter($"age" > 18)
result.explain(true)
// 观察：列剪裁是否生效？（看Scan节点的输出字段数）
```

#### Day 4（3h）：Join优化 + Cost-Based Optimization

**阅读文件**：`JoinReorder.scala`, `CostBasedJoinReorder.scala`

**核心问题**：
```
三个表Join: A ⋈ B ⋈ C
假如:
  A有100行，B有10000行，C有1000000行
  A和B Join后产生500行，B和C Join后产生80000行

两种Join顺序：
  (A ⋈ B) ⋈ C: 500 + 500⋈1M = ?
  (B ⋈ C) ⋈ A: 80000 + 80000⋈100 = ?
哪个更优？
```

**阅读重点**：
1. 如何估算Join后的行数？（统计信息的作用）
2. `reorder(joins: Seq[LogicalPlan], conditions: Seq[Expression])` 的核心逻辑
3. Cost-Based Join Reorder vs Rule-Based Join Reorder的区别
4. 启用条件：`spark.sql.cbo.enabled=true` + 统计信息已收集

**实验任务**：
```sql
-- 三表Join的性能对比
SELECT /*+ REBALANCE */ *
FROM big_table a
JOIN medium_table b ON a.key = b.key
JOIN small_table c ON b.key = c.key;
-- 对比：JOIN顺序不同时，Shuffle数据量的差异
```

### 第2周强制输出
- **源码分析文章**："Catalyst优化器：3个核心优化Rule的原理与实战"（2000+字）
- 内容必须包含：
  - PushDownPredicate的完整流程分析（带源码注释）
  - 优化前后的LogicalPlan树对比图
  - 一个实际SQL的优化效果对比（运行时 + Shuffle数据量）
- **架构图**：Optimizer的所有Batch和Rule的分类图

---

## 第3周：物理计划 — Strategy + SparkPlan执行

### 本周目标
理解从Optimized LogicalPlan到SparkPlan（物理执行计划）的转换过程

### 阅读文件清单

| 优先级 | 文件 | 行数估计 | 阅读时间 | 关键类 |
|--------|------|----------|----------|--------|
| ★★★ | `sql/core/src/main/scala/org/apache/spark/sql/execution/SparkStrategies.scala` | ~500行 | 全读Strategy部分 | 各种Strategy |
| ★★★ | `sql/core/src/main/scala/org/apache/spark/sql/execution/SparkPlanner.scala` | ~100行 | 全读 | SparkPlanner |
| ★★★ | `sql/core/src/main/scala/org/apache/spark/sql/execution/joins/SortMergeJoinExec.scala` | ~600行 | 重点读核心方法 | SortMergeJoinExec |
| ★★★ | `sql/core/src/main/scala/org/apache/spark/sql/execution/joins/BroadcastHashJoinExec.scala` | ~300行 | 重点读核心方法 | BroadcastHashJoinExec |
| ★★ | `sql/core/src/main/scala/org/apache/spark/sql/execution/aggregate/HashAggregateExec.scala` | ~600行 | 读核心流程 | HashAggregateExec |
| ★★ | `sql/core/src/main/scala/org/apache/spark/sql/execution/exchange/ShuffleExchangeExec.scala` | ~300行 | 了解 | ShuffleExchangeExec |
| ★ | `sql/core/src/main/scala/org/apache/spark/sql/execution/DataSourceScanExec.scala` | ~400行 | 了解 | FileSourceScanExec |

### 每日任务拆解

#### Day 1（3h）：Strategy模式 — 逻辑到物理的翻译官

**阅读文件**：`SparkStrategies.scala` + `SparkPlanner.scala`

**核心概念**：
- `Strategy`：一种模式匹配规则，输入是LogicalPlan，输出是Seq[SparkPlan]
- `SparkPlanner`：持有所有Strategy，按顺序尝试匹配

**关键Strategy列表**：
```scala
// 1. JoinSelection Strategy
//    - 根据Join Hint和表大小选择:
//      BroadcastHashJoinExec / SortMergeJoinExec / ShuffledHashJoinExec / CartesianProductExec

// 2. Aggregation Strategy  
//    - HashAggregateExec vs ObjectHashAggregateExec vs SortAggregateExec

// 3. BasicOperators Strategy
//    - ProjectExec / FilterExec / SortExec / RangeExec / ...

// 4. DataSource Strategy
//    - FileSourceScanExec / RowDataSourceScanExec / ...
```

**必须回答的问题**：
1. Strategy的匹配顺序重要吗？如果多个Strategy都能匹配同一个LogicalPlan怎么办？
2. JoinSelection如何决定用BroadcastJoin还是SortMergeJoin？
3. `spark.sql.autoBroadcastJoinThreshold` 默认值是多少？什么时候应该调大/调小？

**实验任务**：
```scala
// 对比同一个Join在不同配置下的物理计划
val df1 = spark.range(1000000)
val df2 = spark.range(100)

// 默认行为
df1.join(df2, "id").explain()

// 强制Broadcast Join
df1.join(broadcast(df2), "id").explain()

// 禁用Broadcast Join
spark.conf.set("spark.sql.autoBroadcastJoinThreshold", -1)
df1.join(df2, "id").explain()
```

#### Day 2（3h）：SortMergeJoinExec vs BroadcastHashJoinExec

**SortMergeJoinExec源码深潜**：

1. **`doExecute()` 方法**：核心执行逻辑
2. **排序阶段**：两个子表分别按Join Key排序（ExternalSorter）
3. **Merge阶段**：两个已排序的迭代器合并
4. **处理数据倾斜**：`spark.sql.join.skewedPartitionFactor` 和 AQE如何参与
5. **为什么SortMergeJoin可以处理任意大小的表？**

**BroadcastHashJoinExec源码深潜**：

1. **`doExecute()` 方法**：核心执行逻辑
2. **Broadcast阶段**：将小表广播到所有Executor
3. **HashJoin阶段**：在每个Executor上构建HashTable（`HashedRelation`），Probe大表
4. **内存要求**：小表必须能完全放入Driver和每个Executor的内存
5. **为什么BroadcastJoin不需要Shuffle？** （最大的优势！）

**对比分析（必做实验）**：
```scala
// 实验: 对比两种Join在不同数据量下的性能
// 场景1: 大表(100M行) JOIN 小表(1000行) — 预期BroadcastJoin A
// 场景2: 大表(100M行) JOIN 中表(10M行) — 预期SortMergeJoin
// 场景3: 两个大表(各100M行) — 必须SortMergeJoin

// 记录: 执行时间、Shuffle Write/Read大小、Task数量分布
```

#### Day 3（3h）：HashAggregateExec — 聚合算子的核心实现

**阅读文件**：`HashAggregateExec.scala`

**核心流程**：
```
Input → HashMap聚合（预聚合阶段）
  ↓ 如果内存不够
  ↓ Spill to disk（溢写到磁盘）
  ↓
  ↓ Shuffle（按Group Key重分区）
  ↓
Input → HashMap聚合（最终聚合阶段）
  ↓
Output
```

**需要理解的关键点**：
1. **Partial → Final 的两阶段聚合**（decodeAggregateExpressions）
2. **TungstenAggregationIterator**：基于UnsafeRow的高性能HashMap实现
3. **Spill机制**：当内存不足时，如何将HashMap的一部分溢写到磁盘？
4. **Distinct聚合的特殊处理**：`count(distinct col1, col2)`

**实验任务**：
```scala
// 验证Partial + Final聚合的存在
spark.sql("""
  SELECT category, COUNT(*), SUM(amount)
  FROM sales
  GROUP BY category
""").explain("extended")

// 观察结果中:
// 1. HashAggregate(partial) 和 HashAggregate(final) 是否都存在？
// 2. groupByExpressions 在partial和final中是否相同？
// 3. aggregateExpressions 在partial和final中有何不同？
```

#### Day 4（3h）：AQE（Adaptive Query Execution）— 运行时的自适应优化

**阅读文件**：`sql/core/src/main/scala/org/apache/spark/sql/execution/adaptive/`

**AQE的三大优化**：

1. **动态合并Shuffle分区**（`OptimizeShuffleWithLocalRead`）
   - 运行时发现某个Stage的输出只有10MB，自动合并为更少的Task
   - 避免200个Task每个只处理50KB数据的浪费

2. **动态切换Join策略**（`OptimizeJoinStrategy`）
   - 运行前认为是SortMergeJoin，运行时发现右侧表只有5MB
   - 自动切换为BroadcastJoin！

3. **动态处理数据倾斜**（`OptimizeSkewedJoin`）
   - 运行时发现有Partition特别大（超过所有Partition中位数的5倍）
   - 自动将该Partition拆分为多个小Partition

**实验任务**：
```scala
// 启用/禁用AQE的性能对比
spark.conf.set("spark.sql.adaptive.enabled", true)
// vs
spark.conf.set("spark.sql.adaptive.enabled", false)

// 同一个查询跑两遍，对比：
// 1. 总运行时间
// 2. Task数量分布
// 3. 是否存在倾斜处理的迹象
```

### 第3周强制输出
- **源码分析文章**："SortMergeJoin vs BroadcastHashJoin：从源码看懂Spark Join的抉择"（2000+字）
- 必须包含：
  - SortMergeJoinExec和BroadcastHashJoinExec的doExecute()源码注解
  - 两种Join的数据流向图
  - 实验对比数据（不同表大小组合的性能对比）

---

## 第4周：WholeStageCodegen — 代码生成与向量化执行

### 本周目标
理解Spark如何通过运行时Java代码生成来消除虚函数调用和中间数据物化

### 阅读文件清单

| 优先级 | 文件 | 行数估计 | 阅读时间 | 关键类 |
|--------|------|----------|----------|--------|
| ★★★ | `sql/core/src/main/scala/org/apache/spark/sql/execution/WholeStageCodegenExec.scala` | ~400行 | 全读 | WholeStageCodegenExec |
| ★★★ | `sql/catalyst/src/main/scala/org/apache/spark/sql/catalyst/expressions/codegen/CodeGenerator.scala` | ~300行 | 全读 | CodegenContext |
| ★★ | `sql/catalyst/src/main/scala/org/apache/spark/sql/catalyst/expressions/codegen/GenerateUnsafeProjection.scala` | ~200行 | 重点读 | GenerateUnsafeProjection |
| ★★ | `sql/core/src/main/scala/org/apache/spark/sql/execution/BufferedRowIterator.java` | ~100行 | 全读 | BufferedRowIterator |
| ★ | `sql/core/src/main/scala/org/apache/spark/sql/execution/vectorized/ColumnarBatch.scala` | ~200行 | 了解 | ColumnarBatch |

### 每日任务拆解

#### Day 1（3h）：WholeStageCodegen — 为什么需要代码生成？

**核心问题**：传统的Volcano Iterator Model有什么问题？

```
传统方式（Volcano Model）:
for each row in input:
    row = filter.eval(row)     // ← 虚函数调用
    if row != null:
        row = project.eval(row) // ← 虚函数调用
        row = hashAgg.eval(row) // ← 虚函数调用

问题:
  1. 每行数据的每个操作都是虚函数调用（CPU分支预测失败）
  2. 中间结果需要通过Row对象传递（大量对象创建和GC）
  3. 无法利用SIMD指令
```

**WholeStageCodegen的解决思路**：
```java
// 生成的Java代码（简化版）
while (input.hasNext()) {        // ← 展开为一个大的while循环
    Row row = input.next();
    // filter逻辑（内联）
    if (row.getInt(0) > 10) {
        // project逻辑（内联）
        int id = row.getInt(0);
        String name = row.getString(1);
        // hashAgg逻辑（内联）
        int bucket = id % 10;
        aggregateBuffer[bucket].count++;
    }
}
// 优势: 无虚函数调用 + 无中间对象分配 + 更好的JIT编译
```

**阅读文件**：`WholeStageCodegenExec.scala`

**源码阅读路径**：
1. `doExecute()` → 触发代码生成和编译
2. `doCodeGen()` → 生成Java源代码字符串
3. Janino编译器：将Java源代码字符串编译为字节码
4. 生成的代码如何与Spark的执行框架集成

#### Day 2（3h）：CodegenContext — 代码生成的上下文

**阅读文件**：`CodeGenerator.scala`

**核心数据结构**：
```scala
class CodegenContext {
  // 1. 代码片段缓冲区
  val references: ArrayBuffer[Any]       // 需要传递到生成代码中的对象引用
  val mutableStates: ArrayBuffer[String] // 生成的类中的成员变量
  
  // 2. 代码生成辅助方法
  def addNewFunction(): String           // 添加新的辅助函数
  def freshName(prefix: String): String  // 生成唯一的变量名
  def addMutableState(): String          // 添加可变状态
  
  // 3. Janino编译
  def compile(): Class[_]                // 编译Java源代码
}
```

**关键理解**：
1. `CodegenContext` 如何避免变量名冲突？
2. 如何将Spark的Expression（如Add、Multiply等）转换为Java代码？
3. `UnsafeRow` 在这里扮演什么角色？（堆外内存管理）

#### Day 3（3h）：查看生成的代码 + 分析性能

**实验任务**：
```bash
# 打开DEBUG日志，查看生成的Java代码
spark.conf.set("org.apache.spark.sql.execution.debug", "true")

# 或者直接在代码中打印
val df = spark.range(1000000).select($"id" + 1 as "new_id")
df.queryExecution.debug.codegen()
```

**观察重点**：
1. 生成的代码有多长？（通常几百到几千行）
2. 代码中是否有虚函数调用？
3. `UnsafeRow` 的读写方式
4. 变量命名规则（能看出CodegenContext的作用）

**性能对比实验**：
```scala
// 禁用WholeStageCodegen
spark.conf.set("spark.sql.codegen.wholeStage", false)

// 对比：
// 1. 简单过滤+投影的性能
// 2. 复杂表达式（嵌套CASE WHEN）的性能
// 3. GroupBy聚合的性能

// 记录：执行时间、GC次数、CPU使用率
```

#### Day 4（3h）：Tungsten内存管理 + ColumnarBatch

**核心概念**：
1. **UnsafeRow**：直接操作堆外内存，避免Java对象的GC开销
2. **ColumnarBatch**：列式内存布局，更适合SIMD和向量化
3. **Tungsten的排序/聚合**：基于指针的直接比较（避免反序列化）

**阅读文件**：
- `sql/core/src/main/scala/org/apache/spark/sql/execution/vectorized/ColumnarBatch.scala`
- `sql/core/src/main/scala/org/apache/spark/sql/execution/vectorized/ColumnVector.scala`

**与Photon论文的联系**：
- Spark的WholeStageCodegen → 生成Java代码
- Photon → C++ Native引擎
- 两者都是通过编译时/运行时的代码优化来提升性能
- 但Photon能用SIMD、能精确管理内存、不受JVM限制

### 第4周强制输出
- **源码分析文章**"WholeStageCodegen：Spark如何用代码生成碾压Volcano模型"（2000+字）
- 必须包含：
  - Volcano Iterator Model的问题分析
  - WholeStageCodegen的解决思路（配图）
  - 一份实际生成的Java代码（annotated）
  - 启用/禁用WholeStageCodegen的性能对比数据

---

## 源码阅读工具箱

### IDEA快捷键（提高阅读效率）
| 快捷键 | 功能 | 用途 |
|--------|------|------|
| Ctrl+N | 查找类 | 快速定位源码文件 |
| Ctrl+Shift+N | 查找文件 | 查找配置文件等 |
| Ctrl+H | 类型层次 | 查看类的继承树 |
| Ctrl+Alt+H | 调用层次 | 查看方法被谁调用/调用了谁 |
| Ctrl+F12 | 文件结构 | 查看类中所有方法 |
| Ctrl+B | 跳转到定义 | 跳到变量/方法/类的定义处 |
| Alt+F7 | 查找使用 | 查找方法/变量在哪里被使用 |

### 源码阅读辅助脚本
```bash
# 统计本周阅读的代码行数
find . -name "*.scala" -newer /tmp/last_week_marker -exec wc -l {} + | tail -1

# 生成某个包的类图（需要scala-graph工具）
# 快速找到某个方法的所有调用者
grep -rn "def select" --include="*.scala" sql/core/src/main/scala/
```

## 关键代码片段：Catalyst优化Rule示例

### PushDownPredicate核心逻辑（伪代码还原）

```scala
object PushDownPredicate extends Rule[LogicalPlan] {
  def apply(plan: LogicalPlan): LogicalPlan = plan transform {
    case Filter(condition, child) =>
      child match {
        case Filter(innerCondition, innerChild) =>
          Filter(innerCondition, Filter(condition, innerChild))

        case Project(projectList, child) =>
          val (pushDown, stayUp) = splitConjunctivePredicates(condition)
            .partition(canPushThroughProject(_, projectList))
          if (pushDown.nonEmpty) {
            Project(projectList, 
              Filter(stayUp.reduceLeft(And), 
                Filter(pushDown.reduceLeft(And), child)))
          } else {
            Filter(condition, Project(projectList, child))
          }

        case Join(left, right, joinType, joinCondition) =>
          val (leftCondition, rightCondition, joinCondition2) = 
            splitJoinConditions(condition, left, right)
          val newLeft = leftCondition.map(c => Filter(c, left)).getOrElse(left)
          val newRight = rightCondition.map(c => Filter(c, right)).getOrElse(right)
          Join(newLeft, newRight, joinType, joinCondition2.orElse(joinCondition))

        case Aggregate(groupingExprs, aggExprs, child) =>
          val (pushDown, stayUp) = splitConjunctivePredicates(condition)
            .partition(canPushThroughAggregate)
          if (pushDown.nonEmpty) {
            Aggregate(groupingExprs, aggExprs, 
              Filter(pushDown.reduceLeft(And), child))
              .withNewCondition(stayUp)
          } else {
            Filter(condition, Aggregate(groupingExprs, aggExprs, child))
          }
      }
  }
}
```

### ColumnPruning核心逻辑（伪代码还原）

```scala
object ColumnPruning extends Rule[LogicalPlan] {
  def apply(plan: LogicalPlan): LogicalPlan = plan transform {
    case Project(projectList, Project(childProjectList, child)) =>
      val referencedAttrs = projectList.flatMap(_.references).toSet
      val prunedChildProjectList = childProjectList
        .filter(attr => referencedAttrs.contains(attr.toAttribute))
      Project(projectList, Project(prunedChildProjectList, child))

    case Project(projectList, child) =>
      val referencedAttrs = projectList.flatMap(_.references).toSet
      child match {
        case Scan(_, outputAttrs, _) =>
          val prunedOutput = outputAttrs.filter(referencedAttrs.contains)
          Project(projectList, Scan(_, prunedOutput, _))
        case _ => plan
      }

    case Filter(condition, Project(projectList, child)) =>
      val condRefs = condition.references.toSet
      val projRefs = projectList.flatMap(_.references).toSet
      val allNeeded = condRefs ++ projRefs
      Project(projectList, Filter(condition, Project(prune(child, allNeeded), child)))
  }
}
```

### 优化前后对比示例

```
SQL: SELECT name, age FROM users WHERE age > 18 AND city = 'Beijing'

优化前 (Unoptimized LogicalPlan):
  Filter (age > 18 AND city = 'Beijing')
    └── Project [name, age]
          └── Scan [id, name, age, city, email, phone, address]
                                 ↑ 扫描了7列, 包含不需要的id/email/phone/address

优化后 (Optimized LogicalPlan):
  Project [name, age]
    └── Filter (city = 'Beijing')        ← city条件下推到Scan之前
          └── Filter (age > 18)           ← age条件下推到Scan之前
                └── Scan [name, age, city] ← 只扫描3列! ColumnPruning生效
```

---

## 调试技巧：如何用Spark UI和EXPLAIN查看优化过程

### 1. EXPLAIN命令详解

```scala
val df = spark.read.parquet("users")
  .select("name", "age", "city")
  .filter($"age" > 18 && $"city" === "Beijing")
  .groupBy("city")
  .agg(avg("age").as("avg_age"))

df.explain()          // 只显示物理计划
df.explain(true)      // 显示所有阶段: Parsed → Analyzed → Optimized → Physical
df.explain("formatted") // 格式化显示物理计划(最易读)
df.explain("cost")    // 显示代价估算(需开启CBO)
df.explain("codegen") // 显示生成的Java代码
```

**EXPLAIN输出解读**：

```
== Parsed Logical Plan ==
  'Filter ('age > 18)                    ← 未解析, 列名带引号
  'UnresolvedRelation [users]

== Analyzed Logical Plan ==
  Filter (age#1 > 18)                    ← 已解析, 列名带#id
  SubqueryAlias users
  Relation[id#0,name#1,age#2,city#3]     ← 所有列都在

== Optimized Logical Plan ==
  Filter (city#3 = Beijing)              ← 条件已拆分
  Filter (age#2 > 18)                    ← 条件下推
  Project [name#1, age#2, city#3]        ← 列剪裁生效
  Relation[name#1,age#2,city#3]          ← 只读3列!

== Physical Plan ==
  *(1) HashAggregate(keys=[city#3], ...)
  +- Exchange hashpartitioning(city#3, 200)
     +- *(1) HashAggregate(keys=[city#3], ...)
        +- *(1) Project [name#1, age#2, city#3]
           +- *(1) Filter (isnotnull(city#3) && (city#3 = Beijing))
           +- *(1) Filter (age#2 > 18)
              +- *(1) ColumnarToRow
                 +- FileScan parquet [name#1,age#2,city#3]
                    PartitionFilters: []
                    PushedFilters: [IsNotNull(city), EqualTo(city,Beijing), 
                                    GreaterThan(age,18)]
                    ReadSchema: struct<name:string,age:int,city:string>
```

### 2. Spark UI查看优化效果

```
Spark UI路径:
  http://localhost:4040 → SQL Tab → 点击Job ID

关键信息:
  ┌───────────────────────────────────────────────────┐
  │  SQL Execution Details                             │
  │                                                    │
  │  1. 查看执行DAG图:                                 │
  │     - 每个节点是一个SparkPlan算子                   │
  │     - 节点上的数字是数据行数                        │
  │     - 红色节点表示有Shuffle                         │
  │                                                    │
  │  2. 查看Scan节点:                                  │
  │     - PartitionFilters: 分区级过滤(已下推)          │
  │     - PushedFilters: 文件级过滤(已下推)             │
  │     - ReadSchema: 实际读取的列(列剪裁效果)          │
  │                                                    │
  │  3. 查看Shuffle信息:                               │
  │     - Shuffle Read/Write大小                       │
  │     - Partition数量                                │
  │     - 是否有数据倾斜(某Partition特别大)             │
  │                                                    │
  │  4. 查看AQE效果:                                   │
  │     - 是否合并了小Partition                        │
  │     - 是否切换了Join策略                           │
  │     - 是否处理了数据倾斜                           │
  └───────────────────────────────────────────────────┘
```

### 3. Debug Catalyst优化过程

```scala
spark.conf.set("spark.sql.optimizer.showOptimizations", "true")

df.queryExecution.debug.logical()
df.queryExecution.debug.analyzed()
df.queryExecution.debug.optimizedPlan()

df.queryExecution.debug.codegen()

spark.conf.set("spark.sql.adaptive.enabled", "true")
spark.conf.set("spark.sql.adaptive.logLevel", "INFO")
```

### 4. 常见优化验证清单

| 优化类型 | 验证方法 | 期望看到 |
|---------|---------|---------|
| 谓词下推 | EXPLAIN中Filter在Scan之前 | PushedFilters非空 |
| 列剪裁 | ReadSchema只有需要的列 | 列数 < 原始列数 |
| 常量折叠 | EXPLAIN中无1+0.1 | 直接显示1.1 |
| Join选择 | BroadcastHashJoin vs SortMergeJoin | 小表用Broadcast |
| 聚合优化 | Partial + Final两阶段 | 两个HashAggregate |
| AQE生效 | 运行时计划变化 | 自适应合并/切换 |

---

## 每周强制输出模板

```markdown
# Catalyst源码深潜 - 第X周输出

## 本周阅读概要
- 阅读文件数: X个
- 代码行数: X行
- 耗时: X小时
- 核心收获: (一句话)

## 关键代码分析

### 代码片段1: [类名.方法名]
- 文件路径: [完整路径]
- 行号: [起始行-结束行]
- 功能说明: [这段代码做什么]
- 设计模式: [使用了什么设计模式]
- 关键发现: [你发现了什么非显而易见的东西]

```scala
// 原始代码 + 你的逐行注释
```

### 代码片段2: [类名.方法名]
(同上格式)

## 架构理解
- 画一个本周阅读代码的架构图(ASCII或手绘拍照)
- 标注核心类之间的关系

## 实验验证
- 实验目标: [验证什么]
- 实验配置: [Spark配置/数据集]
- 实验结果: [截图/数据]
- 结论: [验证了什么/发现了什么]

## 与DDIA的关联
- 本周代码与DDIA第X章的Y概念相关
- 具体关联: [解释]

## 仍不理解的问题
1. [问题1]
2. [问题2]

## 下周计划
- 重点阅读: [文件/类/方法]
- 期望理解: [什么问题]
```

### 每周总结记录表
| 周次 | 阅读文件数 | 代码行数 | 写笔记字数 | 核心收获 |
|------|-----------|----------|-----------|----------|
| 第1周 | | | | |
| 第2周 | | | | |
| 第3周 | | | | |
| 第4周 | | | | |