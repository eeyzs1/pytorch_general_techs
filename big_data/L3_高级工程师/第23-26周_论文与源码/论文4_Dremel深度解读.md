# 论文4：Dremel 深度解读

> **论文**：Dremel: Interactive Analysis of Web-Scale Datasets (VLDB 2010)
>
> **作者**：Sergey Melnik, Andrey Gubichev, Jing Jing Long, Geoffrey Romer, Shiva Shivakumar, Matt Tolton, Theo Vassilakis (Google)
>
> **一句话核心**：通过列式存储嵌套数据（Repetition Level + Definition Level）与多级服务树执行架构，实现万亿行嵌套数据的秒级交互式SQL分析
>
> **对应技术栈**：Apache Parquet、Apache Drill、Trino/Presto、Google BigQuery、Apache Arrow

---

## 一、背景与动机

### 1.1 Google面临的交互式分析困境

2010年前后，Google内部积累了海量嵌套数据（网页索引、日志、爬虫结果），这些数据普遍采用Protocol Buffers格式存储，单表规模动辄达到万亿行、PB级别。当时的分析手段主要有两类，但都难以满足"交互式"需求：

```
方案A: MapReduce
  - 优点: 能处理PB级数据, 容错好
  - 缺点: 单次查询分钟到小时级, 无法交互
  - 适合: ETL、离线报表
  - 不适合: 数据探索、Ad-hoc查询

方案B: 传统并行数据库 (如Vertica/Greenplum)
  - 优点: 秒级响应
  - 缺点: 难以扩展到数千节点, 不支持嵌套数据模型
  - 适合: 结构化关系数据
  - 不适合: Web规模的嵌套数据
```

业务方的真实诉求是：**"我想在30秒内知道过去一周搜索日志中某个查询词的出现次数分布"**。MapReduce太慢，传统数仓又处理不了Protocol Buffers这种嵌套结构。Dremel正是为填补这一空白而设计。

### 1.2 嵌套数据的列式存储难题

列式存储对扁平关系表很自然——把每一列单独存即可。但Protocol Buffers的Schema是嵌套的，包含`repeated`字段（重复字段）和`optional`字段（可选字段），例如：

```protobuf
message Document {
  required int64 DocId = 1;
  optional group Links {
    repeated int64 Backward = 2;
    repeated int64 Forward = 3;
  }
  repeated group Name {
    repeated group Language {
      required string Code = 4;
      optional string Country = 5;
    }
    optional string Url = 6;
  }
}
```

一条记录中`Name.Language.Code`可能出现多次（每个文档有多个名称，每个名称有多种语言），且某些层级可能缺失（`Country`是optional）。**如何把这种深度嵌套、含重复的字段拆成列式存储，并且能无损地重组回原记录？** 这是Dremel要解决的核心难题。

### 1.3 设计目标

| 目标 | 具体要求 |
|------|----------|
| **交互式延迟** | 万亿行数据查询在秒级返回 |
| **嵌套数据原生支持** | 直接处理Protocol Buffers，不需要flatten |
| **大规模扩展** | 支持数千节点并行 |
| **SQL友好** | 分析师用SQL即可，不需写MapReduce |
| **高吞吐聚合** | 适合Scan+Aggregate，不适合复杂事务 |

---

## 二、核心设计一：Repetition Level 与 Definition Level

这是Dremel论文最核心、也是最难理解的概念。两个Level是嵌套数据列式存储的"灵魂"。

### 2.1 为什么需要两个Level？

考虑`Name.Language.Code`这一列。要把它单独存成列，必须能回答两个问题：

1. **这条值属于哪一层重复？** —— Repetition Level回答
   - 同一个`Name`下新增的`Language`？还是新的`Name`下的第一个`Language`？
2. **这条值缺失在哪一层？** —— Definition Level回答
   - `Code`本身缺失？还是`Language`缺失？还是`Name`缺失？

只用一个Level无法同时表达"重复结构"和"缺失层级"这两种信息。

### 2.2 Repetition Level（重复级别）

**定义**：当前值在路径上"从哪一层开始重复"。

```
路径: Name.Language.Code
层级:  0     1     2

Document 1:
  Name: "http://A"  Language: {Code: "en", Country: "us"}
                    Language: {Code: "en"}              ← 同一Name下新增Language → r=1
  Name: "http://B"  Language: {Code: "en", Country: "gb"} ← 新的Name下的Language → r=0

Code列的值与Repetition Level:
  "en"  r=0  (第一个Name的第一个Language)
  "en"  r=1  (同一个Name的第二个Language)
  "en"  r=0  (新的Name的第一个Language)
```

**关键**：r=0表示"新记录或新Name"，r=1表示"同一Name内的新Language"。重组记录时，看到r=0就知道要开一个新的Name，看到r=1就知道在当前Name下追加Language。

### 2.3 Definition Level（定义级别）

**定义**：在路径上"实际定义到了哪一层"（用于表达optional字段的缺失）。

```
路径: Name.Language.Code.Country (假设Country是optional)
层级:  0    1    2    3

如果Country有值 → d=4 (全部4层都定义了)
如果Country缺失但Language存在 → d=3 (定义到第3层Code)
如果Language缺失 → d=2 (定义到第2层Language)
如果Name缺失 → d=1
```

**关键**：Definition Level记录"缺失发生在哪一层"，重组时据此补全结构。

### 2.4 完整例子（论文Figure 3/4）

```
原始记录 r1:
  DocId: 10
  Links.Forward: 20, 40, 60
  Name.Language.Code: "en", "en", "en"
  Name.Language.Country: "us", null, "gb"
  Name.Url: "http://A", "http://B"

列式存储(每列单独存储, 带r/d level):

Links.Forward列:
  值    r  d
  20    0  2    (新Name... 实际是Links层, d=2表示Forward定义)
  40    1  2    (同一Links下重复Forward)
  60    1  2    (同一Links下重复Forward)

Name.Language.Code列:
  值    r  d
  "en"  0  2    (新Name的第一个Language)
  "en"  1  2    (同一Name的第二个Language)
  "en"  0  2    (新Name的第一个Language)

Name.Language.Country列:
  值    r  d
  "us"  0  3    (新Name的第一个Language, Country有值)
  null  1  2    (同一Name的第二个Language, Country缺失→d=2)
  "gb"  0  3    (新Name的第一个Language, Country有值)
```

**核心洞察**：通过r/d两个Level，每一列都能独立存储，且能无损还原原始嵌套结构。这是Dremel对列式存储的根本贡献。

---

## 三、核心设计二：Record Shredding 与 Assembly

### 3.1 Shredding（拆分）

Shredding是把一条嵌套记录拆成多列的过程。算法核心是深度优先遍历Schema树，为每个叶子字段输出`(value, r, d)`三元组：

```
function shred(record, schema):
    for each field in schema (DFS):
        emit_column_values(field, record, current_r, current_d)
        
关键: 遇到repeated字段时更新r, 遇到optional字段缺失时记录d
```

### 3.2 Assembly（重组）

Assembly是从列式数据重建记录的过程，这是查询执行时必须做的。Dremel用**有限状态机（FSM）**驱动重组：

```
Assembly的核心挑战:
  读取多列的(value, r, d)流, 同步推进, 重建嵌套结构

FSM的状态:
  - 每个字段一个状态
  - 状态转移由"当前字段的r level"决定
  - 当某列的r=0 → 开启新的记录/重复组
  - 当某列的r=k → 在第k层追加

伪代码:
function assemble(columns):
    while not all_columns_eof:
        # 找到r最小的列(决定下一步开哪一层)
        next_field = argmin_r(among_active_columns)
        emit_field_value(next_field)
        advance_column(next_field)
```

**为什么用FSM？** 因为重组逻辑是确定性的——给定输入列的r/d序列，输出记录的结构完全确定。FSM把这种确定性编码为状态转移表，避免运行时的递归和回溯，性能极高。

### 3.3 重组的工程优化

```
1. 延迟Assembly: 
   聚合查询(如COUNT, SUM)不需要完整重组记录
   → 只读取需要的列, 在列上直接计算
   → 这就是"列式存储对聚合友好"的本质

2. 谓词下推:
   WHERE Name.Language.Code = 'en'
   → 只在Code列上过滤, 不需要读取其他列
   → 过滤后再Assembly需要的字段

3. 批量重组:
   不是逐条重组, 而是批量(如1024行)重组
   → 减少函数调用开销, 利于SIMD
```

---

## 四、核心设计三：多级服务树执行架构

### 4.1 树状执行模型

Dremel不用MapReduce的DAG执行，而是用**多级服务树**：

```
                    ┌──────────────┐
                    │  Root Server │  ← 接收SQL, 协调结果
                    │  (1个)       │
                    └──────┬───────┘
                           │
              ┌────────────┼────────────┐
              │            │            │
        ┌─────▼─────┐ ┌───▼─────┐ ┌───▼─────┐
        │Intermediate│ │Intermed.│ │Intermed.│  ← 中间层, 聚合下层结果
        │  Server    │ │ Server  │ │ Server  │
        └─────┬─────┘ └────┬────┘ └────┬────┘
              │            │            │
         ┌────┴────┐  ┌────┴────┐  ┌────┴────┐
         │Leaf Svr1│  │Leaf Svr2│  │Leaf SvrN│  ← 叶子节点, 扫描数据
         └─────────┘  └─────────┘  └─────────┘
              │            │            │
         ┌────▼────┐  ┌────▼────┐  ┌────▼────┐
         │Colossus │  │Colossus │  │Colossus │  ← 底层文件系统
         │(GFS2)   │  │         │  │         │
         └─────────┘  └─────────┘  └─────────┘
```

### 4.2 为什么用树状架构？

```
问题: 万亿行数据, 单次扫描需要数千节点并行
     但Root节点不能直接聚合数千个节点的结果(网络/内存瓶颈)

解决: 多级聚合
  - 叶子节点: 扫描本地数据, 做局部聚合(如COUNT, SUM)
  - 中间节点: 聚合下层N个节点的结果
  - 根节点: 聚合中间节点结果, 返回给客户端

效果: 
  - 每层扇出(Fan-out)约100-300
  - 3层树可覆盖 300^3 = 2700万节点
  - 每层延迟约100ms, 3层总延迟约300ms-1s
```

### 4.3 查询执行流程

```
SQL: SELECT Country, COUNT(*) FROM Documents GROUP BY Country

1. Root解析SQL, 生成执行计划
2. Root将计划下发给中间层
3. 中间层下发给叶子节点
4. 叶子节点:
   - 扫描本地Colossus上的列式数据
   - 只读取Country列(列式优势!)
   - 本地做GROUP BY Country, COUNT
   - 返回部分聚合结果给中间层
5. 中间层:
   - 合并下层节点的部分聚合结果
   - 再次GROUP BY(因为不同叶子可能有相同Country)
   - 返回给Root
6. Root:
   - 最终合并, 返回给客户端
```

**关键优势**：聚合在每一层都做了"部分计算"，网络传输的只是聚合后的少量结果，而非原始数据。这与MapReduce的Shuffle（传输全部中间结果）形成鲜明对比。

### 4.4 与MapReduce的本质区别

| 维度 | MapReduce | Dremel |
|------|-----------|--------|
| **执行模型** | DAG (Map→Shuffle→Reduce) | 多级服务树 |
| **中间结果** | 物化到磁盘 | 流式传递，不落盘 |
| **数据扫描** | 行式或需自定义 | 列式原生 |
| **聚合位置** | Reduce端集中 | 每层都部分聚合 |
| **延迟** | 分钟~小时 | 秒级 |
| **适用场景** | 复杂ETL、多阶段 | 交互式Scan+Aggregate |
| **容错** | Task级重试 | 查询级重试(快，重跑) |

---

## 五、工程实现细节

### 5.1 列式存储格式

Dremel的列式格式直接催生了**Parquet**（开源版）：

```
文件结构:
  Row Group (约128MB)
    ├── Column Chunk 1 (DocId列)
    │   ├── Page 1 (数据页, 含r/d level + 值)
    │   ├── Page 2
    │   └── Dictionary Page (字典编码)
    ├── Column Chunk 2 (Links.Forward列)
    │   └── ...
    └── Column Chunk N

关键编码:
  - r/d level用RLE/Hybrid编码(高度重复, 压缩率高)
  - 字符串用Dictionary编码
  - 数值用Delta编码
  - 整体用Snappy/Gzip压缩
```

### 5.2 查询调度与容错

```
调度策略:
  - 叶子节点优先调度到数据所在机器(Locality)
  - 每个叶子节点处理1个或多个Stripe(约几百MB)
  - 同一Stripe可被多个查询并发读(无锁, 列式只读)

容错:
  - 叶子节点慢/失败 → Root重新调度该Stripe到其他节点
  - 不像MapReduce那样持久化中间结果
  - 查询失败 → 整个查询重跑(因为秒级查询, 重跑成本低)
  
Straggler处理:
  - 对慢节点, 启动Backup查询(类似MapReduce的Speculative Task)
  - 谁先完成用谁的结果
```

### 5.3 SQL方言与限制

Dremel支持SQL子集，但有明确边界：

```
支持:
  - SELECT/FROM/WHERE/GROUP BY/ORDER BY
  - 聚合函数: COUNT, SUM, AVG, MIN, MAX
  - JOIN (但限制较多, 大表JOIN小表用Broadcast)
  - 嵌套字段访问: Name.Language.Code

不支持/弱支持:
  - UPDATE/DELETE (列式存储天然只读, 不支持原地更新)
  - 复杂多表JOIN (服务树架构对大表JOIN不友好)
  - 事务 (分析系统, 非OLTP)
```

---

## 六、与相关技术的对比

### 6.1 Dremel vs Parquet vs ORC

```
Dremel: Google内部系统, 闭源, 含执行引擎+存储格式
Parquet: 开源存储格式(源自Dremel论文), 与执行引擎解耦
ORC:   Hive的列式格式, 类似设计但r/d level实现不同

关系:
  Dremel论文 → Parquet格式 → 被Spark/Trino/Presto/Hive采用
  Dremel系统 → Google BigQuery(云服务)
```

### 6.2 Dremel vs Presto/Trino

```
Presto/Trino继承了Dremel的思想:
  - 列式存储(读Parquet/ORC)
  - 多级服务树(Coordinator → Worker → Split)
  - 流式执行, 不落盘
  - 交互式延迟

差异:
  - Presto支持更多数据源(Connector架构, 不只Colossus)
  - Presto的JOIN能力更强(支持多种Join策略)
  - Dremel与Colossus/GFS深度集成, Locality更好
```

### 6.3 Dremel vs Spark SQL

```
Spark SQL:
  - 基于RDD/DataFrame, 有DAG调度
  - 适合复杂ETL + 交互查询
  - 中间结果可缓存(内存)
  - 延迟: 秒~分钟

Dremel:
  - 纯查询引擎, 不做ETL
  - 服务树架构, 更低延迟
  - 延迟: 秒级
  - 但JOIN和复杂转换能力弱于Spark
```

---

## 七、批判性分析

### 7.1 假设的局限性

```
假设1: "数据是嵌套的(Protocol Buffers)"
  局限: 关系型数据(扁平表)用Dremel的r/d level是过度设计
        扁平表根本不需要Repetition Level
        现代Parquet对扁平表有优化路径

假设2: "查询以Scan+Aggregate为主"
  局限: 多表大JOIN场景, 服务树架构不如DAG灵活
        Dremel论文承认JOIN是弱项
        复杂分析仍需MapReduce/Spark

假设3: "秒级重跑可接受"
  局限: 对几十秒的查询重跑OK
        但对接近超时边界(如30秒)的查询, 重跑可能超时
        生产环境需要更细粒度的容错
```

### 7.2 论文未回答的问题

```
1. r/d level的存储开销到底多大?
   论文给了压缩比, 但没分析r/d level本身占多少
   实际中r/d level用RLE编码后开销很小, 但论文未量化

2. Assembly的FSM状态爆炸问题?
   深度嵌套(10层以上)的Schema, FSM状态数指数增长
   论文的例子只有3-4层, 没讨论深层嵌套

3. 多级服务树的负载均衡?
   如果某些中间节点下挂的叶子数据量远超其他
   → 中间节点成为瓶颈
   论文未讨论如何动态调整树结构

4. 与索引的关系?
   Dremel强调Scan, 但某些点查询(查特定DocId)用索引更快
   论文未讨论索引(后续BigQuery加入了索引能力)
```

### 7.3 设计替代思路

```
替代方案1: 把嵌套数据flatten成关系表
  优点: 可用传统列式数据库
  缺点: 1条嵌套记录可能展开成多行, 数据膨胀; 丢失嵌套语义
  
替代方案2: 用JSON路径直接查询(如JSONPath)
  优点: 不需要r/d level, 实现简单
  缺点: 无法列式存储, 性能差; 无法高效压缩

替代方案3: Dremel的r/d level + Apache Arrow的内存格式
  现代演进: Arrow的嵌套类型正是Dremel思想的延续
  Arrow用更紧凑的内存布局, 支持零拷贝传递
```

---

## 八、对现代大数据系统的启发

### 8.1 列式存储成为标配

Dremel证明了列式存储对分析负载的巨大优势，直接催生了：
- **Parquet**：事实上的列式存储标准
- **ORC**：Hive生态的列式格式
- **Arrow**：内存中的列式格式（零拷贝）

现代数据湖（Lakehouse）几乎全部基于Parquet/ORC，其根基正是Dremel。

### 8.2 服务树 → MPP架构的普及

Dremel的服务树思想演化为现代MPP查询引擎：
- **Presto/Trino**：Coordinator + Worker，流式执行
- **ClickHouse**：类似的多级聚合
- **BigQuery**：Dremel的直接继承者

### 8.3 嵌套数据的一等公民地位

Dremel让嵌套数据（Protobuf/JSON/Avro）成为分析系统的一等公民，而非"先flatten再分析"。现代Parquet/ORC原生支持嵌套Schema，Arrow也支持List/Struct类型。

### 8.4 Scan vs Index的权衡

Dremel选择"暴力Scan + 列式 + 部分聚合"而非索引。这在PB级数据下是正确的——索引维护成本太高，而列式Scan足够快。现代系统（如BigQuery的Search Index）在Scan基础上补充索引，是Dremel思想的演进。

---

## 九、总结

Dremel论文的核心贡献是两个洞察：

1. **嵌套数据可以高效列式存储**：通过Repetition Level和Definition Level两个维度，任何嵌套结构都能无损拆成列、再无损重组。这一思想直接催生了Parquet，成为数据湖的存储基石。

2. **多级服务树实现交互式延迟**：通过树状聚合，把"万亿行扫描"压缩到秒级，开创了交互式大数据分析的范式。

Dremel的局限同样清晰：不适合复杂JOIN、不支持更新、对扁平表过度设计。但这些局限不影响其历史地位——它定义了"列式 + MPP + 嵌套数据"这一分析系统的基本范式，至今仍是BigQuery/Presto/Spark SQL的共同基础。

> **核心Takeaway**：Dremel告诉我们，列式存储不只是"把列分开存"，而是要解决"嵌套结构如何无损列化"这一根本问题。Repetition Level和Definition Level是这一问题的优雅解，也是理解现代列式格式（Parquet/Arrow）的钥匙。

---

## 第一性原理连接

> **本文验证的矛盾**：矛盾7（读写/存储引擎，列存优化）。

Dremel 证明了：当分析负载以"Scan + 聚合"为主时，列式存储是对存储引擎的根本性优化。通过 Repetition Level 和 Definition Level 把嵌套数据无损列化，Dremel 将矛盾7的"读放大"问题推向极致——只读所需列，压缩率提升、Cache 命中率提升、SIMD 向量化执行成为可能。这一选择牺牲了单行更新的能力（不适合 OLTP），但在分析场景下性能提升数十倍，直接催生了 Parquet/ORC/Arrow 等列式格式标准。

> **框架映射**：详见 [大数据第一性原理](../../大数据第一性原理.md) 矛盾7。深度原理见 [原理深潜1：存储引擎](../../原理深潜/原理深潜1_存储引擎.md)。
