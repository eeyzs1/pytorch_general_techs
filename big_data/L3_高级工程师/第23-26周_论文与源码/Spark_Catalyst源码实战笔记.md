# Spark SQL Catalyst 源码实战笔记

> **目标**：通过实际阅读Spark SQL Catalyst优化器源码，记录核心类的调用链、关键代码注释、调试技巧和设计模式分析
>
> **源码版本**：Apache Spark 3.5.0 | **阅读范围**：Catalyst优化器核心模块 + Tungsten执行层

---

## 一、核心类调用关系总图（文字版）

```
                         ┌─────────────────────────────┐
                         │     SparkSession / Dataset    │  ← API入口
                         │     Dataset.scala:27 (select) │
                         └─────────────┬───────────────┘
                                       │ .select()/.filter()/.groupBy()
                                       ▼
                         ┌─────────────────────────────┐
                         │    QueryExecution (桥梁)      │  ★ 类1
                         │    懒执行, 串联所有阶段         │
                         └─────────────┬───────────────┘
                                       │
                    ┌──────────────────┼──────────────────┐
                    │                  │                  │
                    ▼                  ▼                  ▼
          ┌─────────────────┐ ┌───────────────┐ ┌─────────────────┐
          │  Analyzer        │ │  Optimizer    │ │  SparkPlanner   │
          │  (RuleExecutor)  │ │  (RuleExecutor)│ │  (Strategies)   │
          │  ★ 类2           │ │  ★ 类3         │ │  ★ 类6          │
          │  ResolveRelations│ │  PushDownPred  │ │  JoinSelection  │
          │  ResolveFunctions│ │  ColumnPruning │ │  Aggregation    │
          └────────┬────────┘ └───────┬───────┘ └────────┬────────┘
                   │                  │                  │
                   ▼                  ▼                  ▼
          ┌─────────────────┐ ┌───────────────┐ ┌─────────────────┐
          │  LogicalPlan     │ │  Optimized    │ │  SparkPlan      │
          │  (★★★★★ 类4)    │ │  LogicalPlan  │ │  (★★★★★ 类7)   │
          │  Project/Filter  │ │               │ │  SMJExec/BHJExec│
          │  Join/Aggregate  │ │               │ │  HashAggExec    │
          └─────────────────┘ └───────────────┘ └────────┬────────┘
                                                         │
                                                         ▼
                                              ┌─────────────────────┐
                                              │ WholeStageCodegenExec│ ← ★ 类8
                                              │  CollapseCodegenStages│
                                              └──────────┬──────────┘
                                                         │
                                                         ▼
                                              ┌─────────────────────┐
                                              │   RDD Execution     │
                                              │   (最终执行)         │
                                              └─────────────────────┘
```

---

## 二、类1：Dataset —— API入口与LogicalPlan构建

### 2.1 源码路径

```
sql/core/src/main/scala/org/apache/spark/sql/Dataset.scala
```

### 2.2 关键代码注释

```scala
// Dataset.scala (简化核心结构)

class Dataset[T] private[sql](
    @transient val sparkSession: SparkSession,
    @DeveloperApi @Unstable val queryExecution: QueryExecution,
    encoder: Encoder[T])
  extends Serializable {

  // ========== select() 的实现 ==========
  def select(cols: Column*): DataFrame = {
    // Column → NamedExpression 的转换
    // 如 $"name" → UnresolvedAttribute("name")
    //    $"age" + 1 → Add(UnresolvedAttribute("age"), Literal(1))
    //    $"age".as("new_age") → Alias(UnresolvedAttribute("age"), "new_age")
    val namedExpressions = cols.map(_.named)
    
    // selectUntyped 构建 Project LogicalPlan 节点
    selectUntyped(namedExpressions: _*)
  }

  private def selectUntyped(columns: TypedColumn[_, _]*): DataFrame = {
    val expressions = columns.map(_.expr)
    // ★ 关键调用: withPlan 创建新的 DataFrame, 携带 Project LogicalPlan
    //   这不会触发任何计算! 只是构建 LogicalPlan 树
    withPlan {
      Project(expressions.toList, logicalPlan)  // Project 是 LogicalPlan 子类
    }
  }

  // ========== filter() 的实现 ==========
  def filter(condition: Column): Dataset[T] = {
    // condition 也是 Column 类型, 转为 Expression
    withTypedPlan {
      Filter(condition.expr, logicalPlan)  // Filter 也是 LogicalPlan 子类
    }
  }

  // ========== groupBy() 的实现 ==========
  def groupBy(cols: Column*): RelationalGroupedDataset = {
    // groupBy 不直接返回 Dataset，而是返回 RelationalGroupedDataset
    // 因为聚合函数(agg/count/sum等)定义在 RelationalGroupedDataset 上
    RelationalGroupedDataset(
      toDF(), 
      cols.map(_.expr), 
      RelationalGroupedDataset.GroupByType)
  }

  // ========== withPlan ==========
  // ★ 核心方法: 每次 Transformation 都调用此方法
  //   创建新的 Dataset, 带着新的 LogicalPlan
  //   旧 Dataset 的 LogicalPlan 成为新 LogicalPlan 的 child
  @inline private def withPlan(logicalPlan: LogicalPlan): DataFrame = {
    // 注意: 这里用 copy constructor 而不是 new Dataset(…)
    // 确保 sparkSession、encoder 等属性被正确传递
    Dataset.ofRows(sparkSession, logicalPlan)
  }

  // ========== lazy val queryExecution ==========
  // ★ 关键: 直到第一个 Action(count/collect/show) 被调用
  //   才会通过 queryExecution 触发 Analysis→Optimization→Planning→Execution
  @transient lazy val queryExecution: QueryExecution = {
    sparkSession.sessionState.executePlan(logicalPlan)
  }
}
```

### 2.3 调用链追踪

```
spark.range(10).select($"id" + 1).filter($"id" > 5).show()

调用链:
  spark.range(10)
    → Dataset.ofRows(sparkSession, Range(0, 10, 1, ...))
    
  .select($"id" + 1)
    → Column("id") + Column(1) → Add(UnresolvedAttribute("id"), Literal(1))
    → Column("(id + 1)").named → Alias(Add(UnresolvedAttribute("id"), Literal(1)), "(id + 1)")
    → withPlan(Project(Alias(...), Range(...)))
    → 返回新 Dataset(logicalPlan = Project(Alias(...), Range(...)))
    
  .filter($"id" > 5)
    → Column("id") > Column(5) → GreaterThan(UnresolvedAttribute("id"), Literal(5))
    → withTypedPlan(Filter(GreaterThan(...), Project(Alias(...), Range(...))))
    → 返回新 Dataset(logicalPlan = Filter(..., Project(..., Range(...))))
    
  .show()  ← 第一个 Action! 触发计算
    → queryExecution (lazy val, 此时才创建)
    → QueryExecution.executePlan(logicalPlan)
    → Analyzer → Optimizer → Planner → execute()
```

### 2.4 设计模式分析

**Builder模式**：每次Transformation返回新的Dataset（携带新的LogicalPlan），形成链式调用。这本质上是不可变（Immutable）设计——原始Dataset的LogicalPlan永远不会被修改。

---

## 三、类2：RuleExecutor —— 优化引擎的"心脏"

### 3.1 源码路径

```
sql/catalyst/src/main/scala/org/apache/spark/sql/catalyst/rules/RuleExecutor.scala
```

### 3.2 核心源码注释

```scala
abstract class RuleExecutor[TreeType <: TreeNode[_]] {

  // ========== Batch ==========
  // 一组优化 Rule 的集合, 具有固定的应用策略
  case class Batch(
      name: String,                           // Batch名称(如"PushDownPredicates")
      strategy: Strategy,                     // Once 或 FixedPoint
      rules: Rule[TreeType]*)                 // 包含的规则列表
  
  // ========== Strategy ==========
  sealed trait Strategy
  case object Once extends Strategy           // 每个Rule只应用一次
  case class FixedPoint(maxIterations: Int) extends Strategy  
      // 反复应用直到树不再变化, 或达到最大迭代次数

  // ========== Rule ==========
  abstract class Rule[TreeType <: TreeNode[_]] {
    val ruleName: String                      // Rule名称, 用于调试和日志
    
    def apply(plan: TreeType): TreeType       // ★ 核心: 对一棵树进行变换
    // apply 接收一棵树, 返回一棵新树(不可变设计)
  }

  // ========== execute() - 核心方法 ==========
  def execute(plan: TreeType): TreeType = {
    var currentPlan = plan
    
    for (batch <- batches) {                  // 遍历每个Batch
      val batchStartPlan = currentPlan
      var iteration = 1
      var continue = true
      
      batch.strategy match {
        case Once =>
          // Once策略: 顺序应用每个Rule, 只用一次
          for (rule <- batch.rules) {
            val result = rule(currentPlan)     // 应用规则
            if (!result.fastEquals(currentPlan)) {
              // ★ 规则改变了树 → 记录日志
              logRuleApplication(rule, currentPlan, result)
              currentPlan = result
            }
          }
          
        case FixedPoint(maxIterations) =>
          // FixedPoint策略: 反复应用所有Rule, 直到树不再变化
          while (continue && iteration <= maxIterations) {
            var changed = false
            for (rule <- batch.rules) {
              val result = rule(currentPlan)
              if (!result.fastEquals(currentPlan)) {
                // 树发生了变化 → 继续迭代
                logRuleApplication(rule, currentPlan, result)
                currentPlan = result
                changed = true
              }
            }
            iteration += 1
            continue = changed  // 没变化就退出循环
          }
          
          // 达到最大迭代次数检查
          if (iteration > maxIterations) {
            logWarning(s"Batch ${batch.name} reached max iterations ($maxIterations)")
          }
      }
    }
    
    currentPlan  // 返回优化后的树
  }
}
```

### 3.3 关键调试技巧

```scala
// 技巧1: 打印每个Rule应用前后的LogicalPlan变化
// 在IDEA中给 logRuleApplication 设置断点
// 观察:
//   哪个Rule被触发了?
//   LogicalPlan树发生了什么变化?
//   同一个Rule被应用了多少次?

// 技巧2: 查看完整的Optimizer Batch列表
// 在SparkSession初始化后执行:
spark.sessionState.optimizer.defaultBatches.foreach { batch =>
  println(s"Batch: ${batch.name} (${batch.strategy})")
  batch.rules.foreach(r => println(s"  - ${r.ruleName}"))
}

// 输出示例:
// Batch: Finish Analysis (Once)
//   - EliminateSubqueryAliases
//   - ReplaceExpressions
// Batch: Union (Once)
//   - CombineUnions
// Batch: Subquery (Once)
//   - OptimizeSubqueries
// Batch: Replace Operators (FixedPoint(100))
//   - ...
// Batch: Operator Optimization before Inferring Filters (FixedPoint(100))
//   - PushDownPredicates
//   - PushPredicateThroughNonJoin
//   - ...

// 技巧3: 捕获触发频率最高的Rule
// 在Rule.apply方法入口处打断点, 条件是: this.ruleName == "PushDownPredicates"
```

---

## 四、类3：PushDownPredicate —— 谓词下推

### 4.1 源码路径

```
sql/catalyst/src/main/scala/org/apache/spark/sql/catalyst/optimizer/PushDownPredicates.scala
```

### 4.2 核心源码注释

```scala
object PushDownPredicates extends Rule[LogicalPlan] with PredicateHelper {
  
  // ========== apply() - Rule入口 ==========
  def apply(plan: LogicalPlan): LogicalPlan = plan transform {
    // ★ 核心: transform 递归遍历整棵 LogicalPlan 树
    //   对每个节点, 尝试应用模式匹配
    
    // 情况1: Filter 上面有 Join
    case filter @ Filter(condition, join @ Join(left, right, _, _, _)) =>
      // 拆分 condition 为:
      //   能下推到左表的, 能下推到右表的, 两个都不能下推的
      val (leftPredicates, rightPredicates, remaining) = 
        splitConjunctivePredicates(condition)          // 拆分AND连接的多个条件
          .partition(_.references.subsetOf(left.outputSet))  // 属于左表?
      
      val (rightOnly, commonPredicates) = 
        remaining.partition(_.references.subsetOf(right.outputSet))
      
      // 构建下推后的树:
      // 原树: Filter(cond, Join(left, right, joinCond))
      // 新树: Filter(commonCond, Join(Filter(leftCond, left), Filter(rightCond, right), joinCond))
      
      val newLeft = leftPredicates.reduceOption(And).map(Filter(_, left)).getOrElse(left)
      val newRight = rightOnly.reduceOption(And).map(Filter(_, right)).getOrElse(right)
      
      // 如果所有条件都下推了, 不再需要外层的Filter
      if (commonPredicates.isEmpty && rightOnly.isEmpty && leftPredicates.isEmpty) {
        // 所有条件都被推到了Join的某一侧 → 不需要外层Filter!
        filter
      } else if (commonPredicates.isEmpty) {
        // 所有剩余条件都在Join一侧 → 保留Filter但推到相应侧
        join.copy(left = newLeft, right = newRight)
      } else {
        // 存在无法下推的条件(如引用两表列的条件)
        Filter(commonPredicates.reduce(And), join.copy(left = newLeft, right = newRight))
      }
    
    // 情况2: Filter嵌套Filter → 展平
    case filter @ Filter(_, childFilter: Filter) =>
      Filter(And(filter.condition, childFilter.condition), childFilter.child)
    
    // 情况3: Filter在Aggregate之上
    case filter @ Filter(condition, aggregate: Aggregate) =>
      // 拆分条件为:
      //   在GROUP BY之前执行的条件(只引用分组列) → 下推到Aggregate之前
      //   在GROUP BY之后执行的条件(引用聚合函数) → 转换为HAVING, 留在Aggregate之后
      val (pushdownPredicates, postAggPredicates) = 
        splitConjunctivePredicates(condition)
          .partition(isGroupingOnly(_, aggregate))
      // ...构建新的树
      
    // 情况4: Filter + Project
    case filter @ Filter(condition, project @ Project(fields, grandChild)) =>
      // 尝试把Filter推到Project之下
      // 注意: 如果Filter引用了Project中的别名列, 不能下推!
      // 如: SELECT a+1 AS x FROM t WHERE x > 5
      //     → Filter的条件引用了Project的别名 "x"
      //     → 不能下推到Project之下 (Project之下的列是 "a" 不是 "x")
      // ...
  }
}
```

### 4.3 优化效果可视化

```
优化前:                         优化后:
Filter(age>18 AND city='BJ')    Join(on: user.id=order.user_id)
  │                             ├── Filter(age>18)── users
Join(on: user.id=order.user_id) │                    (age条件只涉及users表)
  ├── users                     └── Filter(city='BJ')── orders  
  └── orders                                         (city条件只涉及orders表)

节省的IO:
  优化前: Join读取所有users数据(包括age≤18的), 读取所有orders数据(包括city≠BJ的)
  优化后: users只读age>18的, orders只读city='BJ'的
  → 大幅减少Shuffle数据量!
```

---

## 五、类4：ColumnPruning —— 列剪裁

### 5.1 源码路径

```
sql/catalyst/src/main/scala/org/apache/spark/sql/catalyst/optimizer/ColumnPruning.scala
```

### 5.2 核心逻辑

```scala
object ColumnPruning extends Rule[LogicalPlan] {
  
  def apply(plan: LogicalPlan): LogicalPlan = {
    // ★ 核心: 从根节点(顶部)向下传递"需要的列"信息
    //   每个节点根据子节点需要的列, 决定自己需要从父节点获取哪些列
    
    val rootFields = plan.references  // 根节点(最终输出)需要的列
    
    plan transformUp {
      // 自底向上转换(从叶子节点向根节点)
      
      // Project: 根据Project需要哪些列, 告诉child只需要这些列
      case Project(projectList, child) =>
        val requiredColumns = projectList.flatMap(_.references)
        // 递归剪裁child
        val newChild = pruneChild(child, requiredColumns)
        Project(projectList, newChild)
      
      // Aggregate: 只保留分组列和聚合函数引用的列
      case Aggregate(grouping, aggregations, child) =>
        val requiredColumns = 
          grouping.flatMap(_.references) ++ aggregations.flatMap(_.references)
        val newChild = pruneChild(child, requiredColumns)
        Aggregate(grouping, aggregations, newChild)
      
      // Join: 左子节点只需要左表被引用的列, 右子节点只需要右表被引用的列
      case join @ Join(left, right, joinType, condition, hint) =>
        val leftColumns = join.references.filter(_.find(_.resolved == left.outputSet))
        val rightColumns = join.references.filter(_.find(_.resolved == right.outputSet))
        val newLeft = pruneChild(left, leftColumns)
        val newRight = pruneChild(right, rightColumns)
        join.copy(left = newLeft, right = newRight)
        
      // 叶子节点(DataSource): 告诉Scan只需要读某些列
      case scan @ LogicalRelation(relation, output, catalogTable, isStreaming) =>
        // 只读取需要的列 → 减少磁盘IO + 减少内存 + 减少网络
        // PrunedFilteredScan / PrunedScan 接口
        scan
    }
  }
}
```

### 5.3 优化效果示例

```
优化前:                           优化后:
Project(name, age)                Project(name, age)
  │                                │
Join(on: user.id=order.user_id)   Join(on: user.id=order.user_id)
  ├── users (id,name,age,city,     ├── users (id,name,age)
  │          email,phone,etc.)     │         ↑ 只读3列!
  └── orders (order_id,user_id,    └── orders (user_id)
              amount,date,etc.)            ↑ 只读1列!
  
  users: 10列 → 3列 (节省70% IO)
  orders: 5列 → 1列 (节省80% IO)
  总Shuffle数据量 → 减少80%以上!
```

---

## 六、类5：BroadcastHashJoinExec —— 广播Join执行

### 6.1 源码路径

```
sql/core/src/main/scala/org/apache/spark/sql/execution/joins/BroadcastHashJoinExec.scala
```

### 6.2 核心源码注释

```scala
case class BroadcastHashJoinExec(
    leftKeys: Seq[Expression],       // 左表Join Key
    rightKeys: Seq[Expression],      // 右表Join Key
    joinType: JoinType,
    buildSide: BuildSide,            // 哪一侧被Broadcast
    condition: Option[Expression],
    left: SparkPlan,                 // 左子节点(物理计划)
    right: SparkPlan)                // 右子节点(物理计划)
  extends BinaryExecNode 
  with HashJoin 
  with CodegenSupport {

  // ========== doExecute() - 核心执行方法 ==========
  protected override def doExecute(): RDD[InternalRow] = {
    // Step 1: 确定哪一侧是 "build侧" (被广播的) 和 "stream侧" (流式扫描的)
    val (streamedPlan, buildPlan) = buildSide match {
      case BuildLeft  => (right, left)
      case BuildRight => (left, right)
    }
    
    // Step 2: 从build侧收集数据 → 构建HashTable
    val buildSideRDD = buildPlan.execute()
    // ★ 注意: buildPlan.execute() 在Driver端执行!
    //   build侧的RDD被collect()到Driver → 序列化 → broadcast
    
    val broadcastRelation = {
      val buildRows = buildSideRDD.collect()  // ★ Driver端collect
      // 构建 HashedRelation (HashMap<JoinKey, Row>)
      val hashedRelation = HashedRelation(
        buildRows.iterator, 
        buildKeys,
        sizeEstimate = buildRows.length * 100)  // 估算大小
      
      // ★ Broadcast变量 → 每个Executor缓存一份(减少网络传输)
      val broadcastHashed = sparkContext.broadcast(hashedRelation)
      broadcastHashed
    }
    
    // Step 3: stream侧在每个Executor上创建HashJoin迭代器
    streamedPlan.execute().mapPartitions { streamIter =>
      // ★ 每个Partition获取广播变量的本地副本
      val hashedRelation = broadcastRelation.value
      val joinKeys = streamSideKeys  // 用stream侧的Join Key去Probe
      
      // ★ HashJoin核心: 对stream侧的每一行, 用Join Key查找HashTable
      new Iterator[InternalRow] {
        private var currentStreamRow: InternalRow = _
        private var currentMatches: Iterator[InternalRow] = Iterator.empty
        
        override def hasNext: Boolean = {
          while (!currentMatches.hasNext && streamIter.hasNext) {
            currentStreamRow = streamIter.next()
            val key = joinKeys.map(_.eval(currentStreamRow))
            // ★ Probe HashTable → O(1)查找
            currentMatches = hashedRelation.get(key)
          }
          currentMatches.hasNext
        }
        
        override def next(): InternalRow = {
          val matched = currentMatches.next()
          // ★ 将stream侧Row和build侧Row合并为一行(Join结果)
          joinRow(currentStreamRow, matched)
        }
      }
    }
  }

  // ========== 广播大小的阈值检查 ==========
  // 在 SparkStrategies.JoinSelection 中:
  //   if (right.stats.sizeInBytes <= conf.autoBroadcastJoinThreshold) {
  //     chooseBroadcastHashJoin(left, right, ...)
  //   }
  // autoBroadcastJoinThreshold 默认: 10MB (10 * 1024 * 1024)
}
```

---

## 七、类6：SortMergeJoinExec —— 排序合并Join

### 7.1 源码路径

```
sql/core/src/main/scala/org/apache/spark/sql/execution/joins/SortMergeJoinExec.scala
```

### 7.2 核心执行流程

```scala
case class SortMergeJoinExec(
    leftKeys: Seq[Expression],
    rightKeys: Seq[Expression],
    joinType: JoinType,
    condition: Option[Expression],
    left: SparkPlan,
    right: SparkPlan,
    isSkewJoin: Boolean = false)
  extends BinaryExecNode with HashJoin with CodegenSupport {

  protected override def doExecute(): RDD[InternalRow] = {
    // Step 1: 左右两表都执行Shuffle + Sort
    //   Shuffle按Join Key分区 → 相同Key的行去同一个Partition
    //   Sort在每个Partition内按Join Key排序
    val leftRDD = left.execute()
    val rightRDD = right.execute()
    // 这两者内部已经包含了 ShuffleExchangeExec + SortExec
    
    // Step 2: Zipper合并两个已排序的迭代器
    leftRDD.zipPartitions(rightRDD) { (leftIter, rightIter) =>
      // 每个Partition内, 两边的数据都已按Join Key排序
      // 用类似 MergeSort 的方式合并
      
      new SortMergeJoinIterator(leftIter, rightIter, joinType, ...)
    }
  }
}

// ========== SortMergeJoinIterator (简化的核心逻辑) ==========
class SortMergeJoinScanner(leftIter, rightIter, joinType) {
  
  def findNextMatch(): Option[(InternalRow, InternalRow)] = {
    // 类似 MergeSort 的合并过程
    
    while (leftIter.hasNext && rightIter.hasNext) {
      val cmp = compare(leftKey, rightKey)  // 比较Join Key
      
      if (cmp < 0) {
        // 左Key < 右Key → 左前进 (没有匹配)
        advanceLeft()
      } else if (cmp > 0) {
        // 左Key > 右Key → 右前进 (没有匹配)
        advanceRight()
      } else {
        // ★ 匹配! 左Key == 右Key
        // 处理多行同Key的情况:
        //   可能与右侧的多行匹配 (如左[1,1], 右[1,1,1])
        return matchAllSameKeys()
      }
    }
  }
}
```

---

## 八、类7：WholeStageCodegenExec —— 全阶段代码生成

### 8.1 源码路径

```
sql/core/src/main/scala/org/apache/spark/sql/execution/WholeStageCodegenExec.scala
```

### 8.2 核心机制

```scala
case class WholeStageCodegenExec(child: SparkPlan)
  extends UnaryExecNode with CodegenSupport {

  // ========== doExecute() ==========
  override def doExecute(): RDD[InternalRow] = {
    val ctx = new CodegenContext()  // ★ 代码生成上下文
    val (parent, code) = doCodeGen(ctx)  // ★ 生成Java代码字符串!
    
    // ★ 使用Janino编译器将Java源代码编译为字节码
    val compiledClass = ctx.compile(code)
    
    // 通过反射实例化生成的类, 包装为RDD执行
    val bufferredIter = compiledClass
      .getConstructor(classOf[BufferedRowIterator])
      .newInstance(parent.asInstanceOf[AnyRef])
    
    child.execute().mapPartitionsInternal { iter =>
      bufferredIter.setInput(iter)
      new Iterator[InternalRow] {
        override def hasNext: Boolean = bufferredIter.hasNext
        override def next(): InternalRow = bufferredIter.next()
      }
    }
  }

  // ========== doCodeGen() 的核心逻辑 ==========
  def doCodeGen(ctx: CodegenContext): (CodegenSupport, String) = {
    // Step 1: 找到可以被合并到一个WholeStage的所有物理算子
    //   规则: 所有连续的、不支持Codegen的算子之间的算子可以合并
    //   如: ProjectExec → FilterExec → HashAggregateExec 可以合并为一个Stage
    
    val mergedPlan = collapseOperations(child)
    
    // Step 2: 为每个算子生成Java代码片段
    //   每个算子生成 produce() 或 consume() 方法
    //   produce(): 向上游产生数据
    //   consume(): 从下游消费数据
    
    val code = new StringBuilder()
    code.append(ctx.addMutableState("...", "..."))
    code.append("""
      |while (input.hasNext()) {
      |  InternalRow row = input.next();
      |  
      |  // ====== Filter 逻辑 ======
      |  if (row.getInt(0) > 10) {
      |    // ====== Project 逻辑 ======
      |    int newId = row.getInt(0) + 1;
      |    
      |    // ====== Aggregate 逻辑 ======
      |    int bucket = newId % 10;
      |    aggregateBuffer[bucket].count++;
      |  }
      |}
      """.stripMargin)
    
    (child, code.toString())
  }
}
```

### 8.3 为什么WholeStageCodegen比Volcano模型快？

```
Volcano Iterator Model (传统方式):
  for each row:                        // 1000万行
    row = project.next()              // ← 虚函数调用 1000万次
    row = filter.next()               // ← 虚函数调用 1000万次
    row = aggregate.next()            // ← 虚函数调用 1000万次
    → 总共3000万次虚函数调用!
    → 每次虚函数调用: 1次间接跳转 + 可能的分支预测失败

WholeStageCodegen (代码生成):
  while (input.hasNext()) {           // 1000万次循环
    int id = input.getInt(0);         // ← 直接字段访问
    int newId = id + 1;               // ← 内联表达式计算
    if (newId > 5) {                  // ← 内联过滤
      aggBuf[newId % 10].count++;     // ← 内联聚合
    }
  }
  → 0次虚函数调用!
  → JIT可以深度优化这个大循环(循环展开、向量化等)
```

---

## 九、类8：AQE —— 自适应查询执行

### 9.1 源码路径

```
sql/core/src/main/scala/org/apache/spark/sql/execution/adaptive/AdaptiveSparkPlanExec.scala
sql/core/src/main/scala/org/apache/spark/sql/execution/adaptive/OptimizeSkewedJoin.scala
sql/core/src/main/scala/org/apache/spark/sql/execution/adaptive/OptimizeShuffleWithLocalRead.scala
```

### 9.2 AQE的三大优化

```scala
// ========== 优化1: 动态合并Shuffle分区 ==========
object OptimizeShuffleWithLocalRead {
  
  def apply(plan: SparkPlan): SparkPlan = {
    // 问题: spark.sql.shuffle.partitions = 200 (默认)
    //   如果某个Stage的输出只有10MB
    //   200个Task每个只处理 50KB → 极低效!
    
    // 方案: 运行时检测每个Shuffle分区的实际大小
    //   将小分区合并为更大的分区(目标: 每个分区64MB-128MB)
    
    // 实现: 
    //   1. 收集所有MapStatus(每个Map输出的分区大小)
    //   2. 按目标大小(advisoryPartitionSizeInBytes)合并分区
    //   3. 生成CoalescedShuffleReader替换原来的ShuffleReader
    plan transform {
      case shuffle: ShuffleQueryStageExec =>
        val mapOutputStatistics = shuffle.mapStats
        val coalescedPartitionSpec = 
          CoalescedPartitionSpec(mapOutputStatistics, targetSize)
        // ...
    }
  }
}

// ========== 优化2: 动态切换Join策略 ==========
object OptimizeJoinStrategy {
  
  def optimize(plan: SparkPlan): SparkPlan = {
    // 问题: 编译时不知道表的实际大小
    //   基于统计信息判断要 SortMergeJoin
    //   但运行时发现右表只有5MB → 应该用 BroadcastJoin!
    
    // 方案: 在Shuffle阶段完成后, 检查子Stage的实际输出大小
    //   如果符合条件 → 将 SortMergeJoin 降级为 BroadcastHashJoin
    
    plan transformUp {
      case smj @ SortMergeJoinExec(_, _, _, _, 
           left @ SortExec(_, _, ShuffleQueryStageExec(leftStage), _),
           right @ SortExec(_, _, ShuffleQueryStageExec(rightStage), _), _) =>
        
        // 检查右侧Stage的输出大小
        val rightSize = rightStage.getRuntimeStatistics.sizeInBytes
        if (rightSize <= conf.autoBroadcastJoinThreshold) {
          // ★ 降级为BroadcastJoin!
          BroadcastHashJoinExec(
            leftKeys, rightKeys, joinType, BuildRight,
            condition, leftStage, broadcastRightStage)
        } else {
          smj  // 保持SortMergeJoin
        }
    }
  }
}

// ========== 优化3: 动态处理数据倾斜 ==========
object OptimizeSkewedJoin {
  
  def optimize(plan: SparkPlan): SparkPlan = {
    // 问题: 某个Partition数据量是中位数的5倍以上
    //   → 该Partition的Task成为瓶颈
    
    // 方案: 将倾斜的Partition拆分为多个小Partition
    //   在Join的另一侧复制对应数据
    
    // 实现:
    //   1. 检测倾斜Partition: size > medianSize * skewFactor ∧ size > minSize
    //   2. 拆分倾斜Partition为N个(目标: 每份 = advisorySize)
    //   3. 另一侧复制对应数据N份
    plan transformUp {
      case smj @ SortMergeJoinExec(_, _, _, _, left, right, _) =>
        val skewedPartitions = detectSkewedPartitions(left, right)
        if (skewedPartitions.nonEmpty) {
          // 构建 SkewedPartition shuffle reader
          SkewJoinShuffleReader(smj, skewedPartitions)
        } else {
          smj
        }
    }
  }
}
```

---

## 十、调试技巧汇总

### 10.1 查看执行计划

```scala
// 方式1: explain()
df.explain()           // 只显示物理计划
df.explain(true)       // 显示: 解析后的逻辑计划 + 优化后的逻辑计划 + 物理计划
df.explain("extended") // 显示: 所有4个阶段 + 代码生成细节

// 方式2: 通过QueryExecution访问
df.queryExecution.logical        // 未解析的逻辑计划
df.queryExecution.analyzed       // 解析后的逻辑计划
df.queryExecution.optimizedPlan  // 优化后的逻辑计划
df.queryExecution.sparkPlan      // 物理计划
df.queryExecution.executedPlan   // 准备执行的物理计划(经过preparations)
```

### 10.2 查看生成的代码

```scala
// 方法1: DEBUG级别日志
spark.conf.set("org.apache.spark.sql.execution.debug", "true")

// 方法2: 直接打印
df.queryExecution.debug.codegen()
// 输出完整的Java源代码(可能数千行!)

// 方法3: 只查看某个算子的代码
df.queryExecution.executedPlan.foreach {
  case w: WholeStageCodegenExec => println(w.doCodeGen())
  case _ =>
}
```

### 10.3 IDEA调试配置

```
1. 打断点技巧:
   - RuleExecutor.execute() 入口: 观察所有Batch的执行顺序
   - PushDownPredicates.apply() 入口: 观察谓词下推的触发
   - Dataset.select() / filter() 入口: 观察LogicalPlan树的构建
   
2. 条件断点:
   - this.ruleName == "PushDownPredicates" (特定Rule才停)
   - plan.toString().contains("users") (特定表才停)

3. Evaluate Expression:
   - 在断点处使用 Evaluate Expression:
     plan.treeString  → 查看当前LogicalPlan树
     plan.children    → 查看子节点

4. 远程调试:
   spark-submit --conf spark.driver.extraJavaOptions="-agentlib:jdwp=transport=dt_socket,server=y,suspend=y,address=5005"
```

### 10.4 关键分析SQL

```sql
-- 查看表统计信息(CBO需要)
ANALYZE TABLE sales COMPUTE STATISTICS;
ANALYZE TABLE sales COMPUTE STATISTICS FOR COLUMNS user_id, order_date;

-- 查看执行计划中的Join策略
EXPLAIN EXTENDED
SELECT /*+ BROADCAST(s) */ *
FROM large_table l JOIN small_table s ON l.id = s.id;

-- 对比不同Join Hint的效果
SELECT /*+ BROADCAST(s) */ * FROM l JOIN s ...  -- 强制Broadcast
SELECT /*+ MERGE(l) */   * FROM l JOIN s ...    -- 强制SortMerge
SELECT /*+ SHUFFLE_HASH(l) */ * FROM l JOIN s ... -- 强制ShuffleHash
```

---

## 十一、十大关键类的设计模式总结

| 序号 | 类名 | 设计模式 | 核心职责 |
|------|------|----------|----------|
| 1 | **Dataset** | Builder / Immutable | API入口, 构建LogicalPlan, 惰性求值 |
| 2 | **RuleExecutor** | Strategy / Template Method | 规则应用引擎(FixedPoint/Once) |
| 3 | **PushDownPredicates** | Visitor (transform模式) | 谓词下推优化 |
| 4 | **ColumnPruning** | Visitor (transformUp) | 列剪裁优化 |
| 5 | **Optimizer** | Composite (Batch+Rule聚合) | 所有优化规则的编排器 |
| 6 | **SparkStrategies** | Strategy (模式匹配) | LogicPlan→SparkPlan转换 |
| 7 | **BroadcastHashJoinExec** | Command (doExecute模式) | 广播Hash Join物理执行 |
| 8 | **SortMergeJoinExec** | Command (doExecute模式) | 排序合并Join物理执行 |
| 9 | **WholeStageCodegenExec** | Decorator (包装子计划) | 运行时代码生成 |
| 10 | **AdaptiveSparkPlanExec** | Proxy (代理原计划) | 运行时动态优化 |

---

> **核心Takeaway**：阅读Spark源码的关键不是"读完每一行"，而是**理解调用链中的关键跳转点**——
> 从 `Dataset.select()` 到 `Project LogicalPlan` 的构建，从 `RuleExecutor.execute()` 到每个优化Rule的触发，
> 从 `SparkStrategies` 到物理算子的选择，最终到 `doExecute()` 的RDD构建。这些关键跳转点构成了Catalyst的骨架。