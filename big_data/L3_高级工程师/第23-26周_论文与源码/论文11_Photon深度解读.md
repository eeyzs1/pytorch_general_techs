# 论文11：Photon 深度解读

> **论文**：Photon: A Fast Query Engine for Lakehouse Systems (SIGMOD 2022)
>
> **作者**：Alexander Behm, Shoumik Palkar, Csaba Csági, Yiming Liu, Jerry Shao, Stavros Sotiropoulos, Parth Malani, Pranav Subramaniam, Liang Jin, Xinyu Liu, Haojun Liu, Jason Lee, Carlos Rondon, Aman Sharma, Mingwei Tang, Shriram Rajagopalan, Pritesh Shah, Min Chu, Jose Cambronero, Joseph Tatwawadi, Cheng Su, Davies Liu, Daniel Mancuso, Matei Zaharia, Reynold Xin (Databricks)
>
> **一句话核心**：用C++重写Spark的执行层（保留Catalyst优化层），通过向量化执行、SIMD指令、Runtime Filter，在兼容Spark SQL的前提下将查询性能提升3-8倍
>
> **对应技术栈**：Databricks Photon、Meta Velox、Apache Arrow DataFusion、ClickHouse

---

## 一、背景与动机

### 1.1 Spark的JVM瓶颈

2020年前后，Databricks的Lakehouse架构已经成熟，但Spark的执行引擎面临性能瓶颈：

```
Spark执行引擎的问题(基于JVM):

1. GC暂停
   - 大数据量产生大量Java对象 → Full GC → 暂停数百ms~秒级
   - 影响长查询的尾延迟(P99)

2. 内存开销
   - Java对象头(16-24字节) + 引用 → 内存利用率低
   - 1GB数据可能膨胀到2-3GB堆内存

3. SIMD支持受限
   - JVM的JIT难以自动向量化
   - HotSpot的Auto-Vectorization不稳定
   - 无法充分利用CPU的SIMD指令(AVX2/AVX-512)

4. 抽象开销
   - 虚函数调用 → 分支预测失败
   - Iterator模式 → 频繁方法调用
   - 对象分配 → GC压力

结果: Spark的执行效率远低于原生(C++)引擎
     → Lakehouse需要更高性能的查询引擎
```

### 1.2 为什么不全部重写？

```
完全重写的代价:
  - Spark生态庞大(数千Connector、UDF、库)
  - 用户代码依赖Spark API
  - Catalyst优化器成熟且复杂
  → 重写 = 失去生态

Photon的策略: 只重写"执行层"
  ┌─────────────────────────────────────┐
  │  Spark SQL (Catalyst优化器)  ← 保留  │
  │  - SQL解析                           │
  │  - 逻辑计划优化                       │
  │  - 物理计划生成                       │
  └──────────────┬──────────────────────┘
                 │ 物理计划
  ┌──────────────▼──────────────────────┐
  │  Photon执行引擎 (C++)  ← 重写        │
  │  - 向量化执行                        │
  │  - SIMD指令                          │
  │  - 堆外内存管理                       │
  └─────────────────────────────────────┘

优势:
  - 保留Spark生态(SQL/UDF/Connector)
  - 只优化性能瓶颈(执行层)
  - 用户无感知(同一Spark API)
```

### 1.3 设计目标

| 目标 | 具体要求 |
|------|----------|
| **高性能** | 比Spark SQL快3-8倍 |
| **兼容性** | 100%兼容Spark SQL语法和语义 |
| **通用性** | 不只优化特定查询, 全场景提升 |
| **可维护** | C++代码可维护, 可扩展 |
| **Lakehouse优化** | 针对Parquet/Delta Lake深度优化 |

---

## 二、核心设计一：向量化执行

### 2.1 行式执行 vs 向量化执行

```
传统行式执行 (Row-at-a-time, Volcano模型):
  while (input.hasNext()) {
      Row row = input.next();      // 一次一行
      if (filter(row)) {           // 逐行判断
          output.emit(row);
      }
  }

  问题:
  - 每行一次函数调用 → 开销大
  - 无法SIMD(一次处理一个值)
  - Cache不友好(行内多列跳跃)

向量化执行 (Vector-at-a-time):
  while (input.hasNextBatch()) {
      VectorBatch batch = input.nextBatch();  // 一次2048行
      BitVector mask = filter(batch);         // 整批过滤(SIMD!)
      output.emit(batch, mask);
  }

  优势:
  - 减少函数调用(1次/2048行 vs 2048次)
  - SIMD并行(一条指令处理多个值)
  - Cache友好(连续内存, 列式布局)
```

### 2.2 为什么是2048行？

```
Batch Size = 2048 的选择理由:

1. Cache利用率
   - 2048 × 8字节(一个long) = 16KB
   - 正好放入L1 Cache(通常32-64KB)
   - 太大 → L1 Cache Miss
   - 太小 → 函数调用开销占比高

2. SIMD效率
   - AVX2: 256位 = 32字节 = 4个long
   - 2048 / 4 = 512次SIMD操作
   - 足够摊销SIMD启动开销

3. 内存占用
   - 2048行 × 多列 → 几十KB
   - 不会占用过多内存

4. 与Arrow兼容
   - Apache Arrow默认Batch也是1024-2048行
   - 便于与Arrow生态互操作
```

### 2.3 SIMD加速示例

```
过滤操作: WHERE age > 18

行式执行:
  for (i = 0; i < 2048; i++) {
      if (age[i] > 18) {           // 2048次比较
          result[count++] = i;
      }
  }

SIMD执行 (AVX2, 一次4个int):
  for (i = 0; i < 2048; i += 4) {
      __m256i v = _mm256_loadu_si256(&age[i]);  // 加载4个值
      __m256i cmp = _mm256_cmpgt_epi32(v, _mm256_set1_epi32(18));
      int mask = _mm256_movemask_ps((__m256)cmp);
      // mask的4位表示哪几个满足条件
      if (mask & 1) result[count++] = i;
      if (mask & 2) result[count++] = i+1;
      if (mask & 4) result[count++] = i+2;
      if (mask & 8) result[count++] = i+3;
  }

  → 2048次比较 → 512次SIMD指令 → 4倍加速
  → AVX-512(512位) → 8倍加速
```

### 2.4 列式内存布局

```
Photon使用列式内存布局(类似Arrow):

行式布局 (JVM对象):
  [Row1: id=1, name="Alice", age=30]
  [Row2: id=2, name="Bob", age=25]
  → 每行一个对象, 列间跳跃

列式布局 (Photon):
  id列:   [1, 2, 3, 4, ...]     ← 连续内存
  name列: ["Alice", "Bob", ...]  ← 连续内存
  age列:  [30, 25, 28, 35, ...]  ← 连续内存

  → 同列数据类型一致 → SIMD友好
  → 连续内存 → Cache友好
  → 无对象头 → 内存紧凑
```

---

## 三、核心设计二：Runtime Filter

### 3.1 静态优化 vs 运行时优化

```
静态优化 (Catalyst优化器, 编译时):
  - 谓词下推: WHERE x > 10 → 下推到Scan
  - 列裁剪: 只读需要的列
  - Join重排: 小表Broadcast
  - 局限: 不知道实际数据分布

Runtime Filter (运行时, 执行时):
  - 根据实际数据动态生成过滤条件
  - 例: Join时, 用右表的实际值构造Bloom Filter
  - 在左表Scan时应用 → 跳过不匹配的数据
```

### 3.2 Broadcast Hash Join中的Runtime Filter

```
场景: SELECT * FROM orders o JOIN dim_customers c ON o.customer_id = c.id
      dim_customers是小表(100万行), orders是大表(100亿行)

传统Broadcast Hash Join:
  1. Broadcast dim_customers到所有Worker
  2. 构建Hash Table (customer_id → customer记录)
  3. 扫描orders, 对每行用Hash Table探测

  问题: 仍然要扫描全部100亿行orders
        (即使只有100万customer匹配)

Photon的Runtime Filter:
  1. Broadcast dim_customers
  2. 构建Hash Table
  3. 额外构建Bloom Filter (基于customer_id集合)
     → Bloom Filter: "customer_id是否可能在dim_customers中?"
  4. 扫描orders时, 先用Bloom Filter过滤:
     - Bloom Filter说"不存在" → 一定不存在 → 跳过
     - Bloom Filter说"可能存在" → 查Hash Table确认
  5. 如果orders的customer_id只有10%匹配 → 跳过90%的数据

  效果: 
  - Scan的数据量减少90%
  - Hash Table探测减少90%
  - 整体查询快3-5倍
```

### 3.3 Runtime Filter的类型

```
1. Bloom Filter
   - 位数组 + 多哈希函数
   - 优点: 紧凑(几MB), 快速
   - 缺点: 有假阳性(说"可能"但实际不存在)

2. Range Filter (Min/Max)
   - 记录右表的min/max值
   - 左表值不在[min, max] → 跳过
   - 适合数值范围过滤

3. IN List Filter
   - 右表值不多时(如<10万), 直接构建IN列表
   - 精确(无假阳性), 但内存大

4. Hash Filter
   - 完整的Hash Set
   - 精确, 但内存最大

Photon根据数据量自动选择Filter类型
```

---

## 四、核心设计三：内存管理

### 4.1 堆外内存

```
JVM的内存问题:
  - 对象在堆上 → GC管理 → 暂停
  - 大对象 → 老年代 → Full GC

Photon的堆外内存:
  - 用C++直接分配(malloc/mmap)
  - 不受JVM GC管理
  - 显式释放(或RAII)

  优势:
  - 无GC暂停
  - 内存紧凑(无对象头)
  - 可用大页(Huge Pages)减少TLB Miss

  挑战:
  - 内存泄漏需手动管理(RAII/智能指针)
  - 与JVM交互需拷贝(或用DirectByteBuffer)
```

### 4.2 内存池

```
Photon的内存池设计:

  ┌─────────────────────────────────────┐
  │       Photon Memory Pool            │
  │  ┌──────────┐  ┌──────────┐        │
  │  │ Arena 1  │  │ Arena 2  │  ...   │ ← 按算子分配Arena
  │  │ (4MB)    │  │ (4MB)    │        │
  │  └──────────┘  └──────────┘        │
  └─────────────────────────────────────┘

  - 每个算子有自己的Arena(内存区域)
  - Arena内部分配 → 无锁(单线程)
  - Arena释放 → 整体归还(无碎片)
  - 超过Arena大小 → 申请新Arena

  优势:
  - 无malloc/free开销(批量分配)
  - 无内存碎片(Arena整体回收)
  - 无锁竞争(每线程独立Arena)
```

---

## 五、核心设计四：与Spark的集成

### 5.1 执行计划桥接

```
Spark物理计划 → Photon执行计划 的转换:

  Spark物理计划 (RDD-based):
    ScanExec → FilterExec → HashJoinExec → AggregateExec

  Photon转换:
    1. 识别可Photon化的算子
    2. 转换为Photon算子(C++实现)
    3. 不可Photon化的算子(如UDF) → 回退到Spark

  混合执行:
    PhotonScan → PhotonFilter → PhotonHashJoin → SparkUDF → PhotonAggregate
    (前3个用Photon, UDF回退Spark, 最后回到Photon)

  → 渐进式迁移, 不要求100% Photon化
```

### 5.2 数据交换

```
Spark(JVM)与Photon(C++)的数据交换:

  方式1: 共享内存(零拷贝)
    - Photon写入堆外内存
    - Spark用DirectByteBuffer引用
    - 无数据拷贝

  方式2: Arrow格式
    - 双方都支持Arrow列式格式
    - 标准化的内存布局
    - 便于与外部系统互操作

  方式3: 序列化(回退)
    - 当无法共享内存时
    - 序列化为UnsafeRow
    - 有拷贝开销(尽量避免)
```

---

## 六、工程实现细节

### 6.1 编译时优化

```
Photon利用C++的编译时优化:

1. 模板特化
   - 数据类型在编译时确定 → 生成特化代码
   - 例: filter<int32> vs filter<int64> → 不同代码
   - 消除运行时类型判断

2. 内联
   - 小函数内联 → 减少调用开销
   - 算子的next()方法内联

3. 分支消除
   - 编译时已知条件 → 消除分支
   - 例: 固定Batch Size → 循环展开

4. SIMD自动向量化
   - 编译器(-O3 -march=native)自动向量化简单循环
   - 关键路径手写intrinsics
```

### 6.2 Parquet扫描优化

```
Photon对Parquet扫描的深度优化:

1. 异步预读
   - 当前Batch处理时, 异步读取下一Batch
   - I/O与计算重叠

2. 谓词下推 + Runtime Filter
   - 静态谓词 → 下推到Parquet(跳过Row Group)
   - Runtime Filter → 在解码前过滤

3. 字典解码向量化
   - Parquet用字典编码 → 批量解码
   - SIMD加速字典查找

4. 延迟物化
   - 只在需要时才物化列
   - 过滤后只物化匹配的行
   - 减少内存分配和拷贝
```

---

## 七、与相关技术的对比

### 7.1 Photon vs Velox vs DataFusion

```
| 维度        | Photon          | Velox (Meta)    | DataFusion (Arrow) |
|------------|-----------------|-----------------|---------------------|
| 来源        | Databricks      | Meta            | Apache Arrow        |
| 语言        | C++             | C++             | Rust                |
| 集成方式    | 嵌入Spark       | 独立库           | 独立库              |
| SQL兼容     | Spark SQL       | Presto SQL      | ANSI SQL            |
| 向量化      | ✓               | ✓               | ✓                   |
| SIMD        | ✓               | ✓               | ✓                   |
| Runtime Filter | ✓            | ✓               | 部分                |
| 生态        | Spark生态       | Presto/Spark    | Arrow生态           |

共同点: 都是"用系统语言重写执行层"的趋势
        都采用向量化 + SIMD
        都基于列式内存布局
```

### 7.2 Photon vs 原生C++引擎(ClickHouse)

```
ClickHouse: 从头用C++设计, 无JVM包袱
  优势: 极致性能, 无JVM开销
  劣势: 生态小, SQL方言, 无Spark集成

Photon: 在Spark生态内重写执行层
  优势: 兼容Spark生态, 渐进迁移
  劣势: 仍有JVM交互开销(部分算子)

性能对比:
  - 纯Scan+Aggregate: ClickHouse略快(无JVM)
  - 复杂查询: Photon更全(有Catalyst优化器)
  - 生态集成: Photon完胜(Spark生态)
```

---

## 八、批判性分析

### 8.1 假设的局限性

```
假设1: "执行层是瓶颈, 优化层(Catalyst)不需要重写"
  局限: 某些查询的瓶颈在优化器(如复杂Join重排)
  → Photon不优化Catalyst, 这些查询提升有限

假设2: "向量化适合所有算子"
  局限: 某些算子天然是行式的(如复杂UDF)
  → 这些算子回退Spark, 性能不提升

假设3: "SIMD普遍可用"
  局限: 不同CPU的SIMD支持不同(AVX2/AVX-512)
  → 需要运行时检测, 或编译多个版本
```

### 8.2 论文未回答的问题

```
1. C++开发的工程成本?
   - C++比Scala开发慢(无GC, 但需手动管理内存)
   - 调试困难(内存泄漏、段错误)
   → 团队需要C++专家

2. 与Spark UDF的兼容性?
   - UDF是Scala/Java, 无法Photon化
   - UDF成为性能瓶颈(回退JVM)
   → 需要推广SQL原生函数

3. 内存管理的稳定性?
   - C++内存错误(泄漏、越界)比JVM严重
   - 生产环境的长期稳定性?
   → 需要完善的测试和监控

4. 开源策略?
   - Photon是Databricks闭源商业产品
   - 开源社区无法使用
   → Velox/DataFusion成为开源替代
```

### 8.3 Benchmark的公平性

```
论文的Benchmark可能有的偏向:

1. 测试查询选择
   - 可能选择了Photon优势的查询(Scan+Aggregate)
   - 弱势查询(复杂UDF)可能未测试

2. 调优程度
   - Photon可能深度调优, Spark可能未充分调优
   - 公平对比应都做最佳调优

3. 硬件利用
   - Photon用AVX-512, Spark未用
   - 这是"实现差异"还是"架构优势"?

4. 尾延迟
   - 论文报告平均/中位数
   - P99/P999(受GC影响)可能差异更大
```

---

## 九、对现代大数据系统的启发

### 9.1 "用系统语言重写执行层"的趋势

Photon代表了一个行业趋势：
- **Photon** (Databricks): C++重写Spark执行层
- **Velox** (Meta): C++通用执行引擎
- **DataFusion** (Apache): Rust执行引擎
- **Gluten** (Intel): 让Spark调用Velox/ClickHouse

这一趋势的驱动力：JVM在大数据分析上的固有劣势。

### 9.2 向量化成为标配

Photon证明了向量化的巨大价值：
- **ClickHouse**: 一直是向量化
- **DuckDB**: 嵌入式向量化
- **Apache Arrow**: 内存中的列式标准
- 现代查询引擎几乎都采用向量化

### 9.3 Runtime Optimization的兴起

Runtime Filter代表了"运行时优化"的方向：
- 静态优化(Catalyst)有上限(不知道数据分布)
- 运行时优化(基于实际数据)更精准
- 未来趋势: AI驱动的自适应查询优化

---

## 十、总结

Photon论文的核心贡献是三个洞察：

1. **执行层是性能瓶颈，优化层不需要重写**：通过保留Catalyst、重写执行层，Photon在兼容Spark生态的前提下实现了原生引擎的性能。这是"渐进式重写"的经典案例。

2. **向量化 + SIMD是现代查询引擎的标配**：通过批量处理(2048行)和SIMD指令，Photon将CPU利用率提升数倍。这一思路已被整个行业采纳。

3. **Runtime Filter弥补静态优化的不足**：基于实际数据动态生成过滤条件，在Join场景下大幅减少数据扫描。这是"运行时优化"的典范。

Photon的局限在于：闭源商业产品、C++开发成本高、UDF回退JVM。但其设计思想(向量化+SIMD+Runtime Filter+堆外内存)已成为现代查询引擎的共同基础。

> **核心Takeaway**：Photon告诉我们，JVM不是大数据分析的终点——通过用C++重写执行层，可以在保留生态兼容性的同时获得原生引擎的性能。向量化执行、SIMD指令、Runtime Filter是现代查询引擎性能的三大支柱，这一范式正在从Databricks扩展到整个数据行业。
