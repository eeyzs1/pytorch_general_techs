# 论文3：Bigtable 深度解读

> **论文**：Bigtable: A Distributed Storage System for Structured Data (OSDI 2006)
>
> **作者**：Fay Chang, Jeffrey Dean, Sanjay Ghemawat 等 (Google)
>
> **一句话核心**：在GFS之上构建了一个稀疏的、分布式的、持久化的多维有序Map，支持PB级结构化数据的存储和实时访问
>
> **对应技术栈**：HBase、Cassandra（部分思想）、TiKV、LevelDB、RocksDB

---

## 一、论文背景与核心问题

### 1.1 Google为什么需要Bigtable？

在2004年前后，Google发现GFS + MapReduce的组合无法满足以下需求：

| 需求 | GFS能解决吗？ | MapReduce能解决吗？ | Bigtable的解决方案 |
|------|-------------|-------------------|-------------------|
| 存储网页爬取数据 | ✅ 大文件存储 | ✅ 批处理 | ✅ 按URL行键快速查找 |
| 实时点查（按URL查网页） | ❌ GFS没有索引 | ❌ 延时太长 | ✅ Row Key索引 + Bloom Filter |
| 范围扫描（按域名遍历） | ❌ 只能顺序读整个文件 | ❌ 延时太长 | ✅ Sorted Row Key |
| 单行原子更新 | ❌ 追加写不保证原子性 | ❌ 批量只读 | ✅ 单行事务 |
| 每秒百万级读写 | ❌ Master瓶颈 | ❌ 不适合在线服务 | ✅ Tablet分布+内存MemTable |
| 存储半结构化数据 | ❌ 只有文件和目录 | ❌ 扁平KV | ✅ Column Family + Timestamp |

### 1.2 Bigtable的数据模型

Bigtable的核心数据模型可以总结为：

```
(row:string, column:string, timestamp:int64) → value:string
```

这是一个**三维有序Map**：

```
┌──────────────────────────────────────────────────────────┐
│                     Column Family                         │
│                   ┌─────────────────┐                    │
│                   │ Column Qualifier│                    │
│                   │  ┌────────────┐ │                    │
│  Row Key          │  │ Timestamp  │ │ → Value            │
│                   │  └────────────┘ │                    │
│  ┌──────────────┐ │  ┌────────────┐ │  ┌──────────────┐  │
│  │"com.cnn.www" │→│  │ t5: "CNN"  │→│  │ (contents:,  │  │
│  │              │ │  │ t3: "CNN"  │→│  │  t5, "<html>  │  │
│  │              │ │  │            │  │  │  ...</html>") │  │
│  │              │ │  │ t9: "anchor│  │  │ (anchor:cnnsi │  │
│  │              │ │  │ .cnnsi.com"│→│  │ .com, t9,     │  │
│  │              │ │  │            │  │  │ "CNN")        │  │
│  │              │ │  │ t8: "anchor│  │  │ (anchor:my.lo │  │
│  │              │ │  │ .my.look.ca│→│  │ ok.ca, t8,    │  │
│  │              │ │  │            │  │  │ "CNN.com")    │  │
│  └──────────────┘ │  └────────────┘  │  └──────────────┘  │
│                   └─────────────────┘                    │
└──────────────────────────────────────────────────────────┘
```

**关键特性**：

1. **稀疏性**：不是每个Row都有所有Column的数据（不同于关系型数据库的NULL填充）
2. **多维有序**：
   - Row Key：按字典序排序（范围扫描的基础）
   - Column：在Column Family内按Column Qualifier排序
   - Timestamp：倒序排列（最新版本在前）
3. **多版本**：每个Cell可以有多个Timestamp版本

---

## 二、核心设计一：SSTable + MemTable —— LSM-Tree的经典实现

### 2.1 LSM-Tree（Log-Structured Merge Tree）概述

Bigtable的存储引擎基于LSM-Tree。这是在论文发表前就已存在的思想（Patrick O'Neil, 1996），但Bigtable将其大规模工业化了。

```
LSM-Tree的核心思想：牺牲读性能换取写性能

传统B-Tree:           LSM-Tree:
  写: 随机磁盘IO(慢)    写: 顺序磁盘IO(快!)
         ↓                    ↓
  读: 随机磁盘IO(快)    读: 可能需要查多个文件(慢, 但可控)
```

**LSM-Tree的写路径（Bigtable的具体实现）**：

```
写入请求: put("com.cnn.www", "contents:", t5, "<html>...</html>")

  Step 1: 写入Commit Log (WAL)
    ┌─────────────────────────────┐
    │  Commit Log (on GFS)        │  ← 持久化, 顺序追加, 用于崩溃恢复
    │  file: /bt/log/commit_00012 │
    └─────────────────────────────┘

  Step 2: 写入MemTable (内存)
    ┌─────────────────────────────┐
    │  MemTable (in RAM)          │  ← 内存中的有序结构(SkipList/RedBlack)
    │  com.cnn.www:contents:t5 →  │
    │  "<html>...</html>"         │
    └─────────────────────────────┘

  Step 3: MemTable满了? → Flush到SSTable
    ┌─────────────────────────────┐
    │  SSTable #17 (on GFS)       │  ← 不可变的持久化文件
    │  Row范围: "a"-"m"           │
    │  文件大小: ~64MB            │
    └─────────────────────────────┘
```

### 2.2 SSTable文件格式详解（必画图！）

```
SSTable物理布局:

  ┌────────────────────────────────────────────────────┐
  │                     Data Blocks                     │
  │  ┌──────────────────────────────────────────────┐  │
  │  │ Block 0: (64KB, 压缩后~25KB)                  │  │
  │  │  com.aaa/page:t1 → val1                       │  │
  │  │  com.aaa/page:t2 → val2                       │  │
  │  │  com.aaa/title:t1 → val3                      │  │
  │  │  ...                                          │  │
  │  └──────────────────────────────────────────────┘  │
  │  ┌──────────────────────────────────────────────┐  │
  │  │ Block 1:                                      │  │
  │  │  com.bbb/contents:t5 → val4                   │  │
  │  │  com.bbb/title:t2 → val5                      │  │
  │  │  ...                                          │  │
  │  └──────────────────────────────────────────────┘  │
  │  ...更多Data Blocks...                              │
  ├────────────────────────────────────────────────────┤
  │                   Index Block                       │
  │  ┌──────────────────────────────────────────────┐  │
  │  │ com.aaa  → Block 0 offset                      │  │
  │  │ com.bbb  → Block 1 offset                      │  │
  │  │ com.ccc  → Block 2 offset                      │  │
  │  │ ...                                            │  │
  │  └──────────────────────────────────────────────┘  │
  ├────────────────────────────────────────────────────┤
  │                    Footer                           │
  │  ┌──────────────────────────────────────────────┐  │
  │  │ Index Block offset + size                      │  │
  │  │ Bloom Filter offset + size (可选)               │  │
  │  │ Magic Number: 0xDBDBDBDB                       │  │
  │  └──────────────────────────────────────────────┘  │
  └────────────────────────────────────────────────────┘
```

**查找流程**：
```
查找 Key: "com.bbb/contents", Timestamp: t5

Step 1: 读Footer(文件末尾固定大小) → 获取Index Block位置
Step 2: 读Index Block → 二分查找 "com.bbb"
         → 定位到Block 1
Step 3: (可选) 检查Bloom Filter → "com.bbb/contents:t5"是否可能存在?
         → 如果Bloom Filter说"不存在" → 直接返回NOT_FOUND(不用读Data Block!)
Step 4: 读Block 1 → 在Block内二分查找 → 返回val4
```

### 2.3 Bloom Filter —— SSTable的加速引擎

```
Bloom Filter是什么?
  一个概率性数据结构，可以快速回答:
    "Key X 是否可能存在于这个SSTable中?"
  
  回答: "可能" (有概率误报) 或 "绝对不在" (100%准确)
  
  为什么在SSTable中很重要?
    一个Tablet可能有数百个SSTable文件
    查找一个Key需要检查每个SSTable
    如果没有Bloom Filter → 每个SSTable都要读Index Block
    有了Bloom Filter → 99%的SSTable直接跳过!

Bloom Filter的实现原理(简化):
  输入: Key → hash1→bit7, hash2→bit13, hash3→bit42
  检查: bit7 && bit13 && bit42 都是1?
    是 → "可能"存在(继续读Index Block验证)
    否 → "绝对"不存在(跳过此SSTable)

误报率公式:
  对于m位, k个hash函数, n个key:
  False Positive Rate ≈ (1 - e^(-kn/m))^k
  
  通常: 10 bits/key, 7个hash函数 → ~1%误报率
        → 100个SSTable中只有1个需要实际查找!
```

### 2.4 MemTable → SSTable 的转换过程

```
MemTable切换到SSTable的详细流程:

  1. MemTable到达阈值(如128MB):
     - 当前MemTable变为"Immutable MemTable"
     - 创建新的空MemTable接收写入
     
  2. Flush Immutable MemTable → GFS:
     - 遍历Immutable MemTable(有序结构)
     - 每64KB形成一个Data Block(压缩)
     - 构建Index Block(每个Data Block的起始Key→offset映射)
     - 构建Bloom Filter
     - 写入Footer
     - 完成后, SSTable文件大小约原先的30%(压缩后)
     
  3. 更新元数据:
     - 在METADATA表中记录新的SSTable文件
     - 释放Immutable MemTable内存

MemTable本身的内存结构(通常是SkipList):
  每个SkipList节点:
    ┌──────────────────────┐
    │ Key: com.cnn.www:contents:t5  │
    │ Value: <html>...</html>       │
    │ Forward Pointers(多级)         │
    └──────────────────────┘
  
  SkipList查询复杂度: O(log n)
  SkipList插入复杂度: O(log n) (平均)
  内存开销: 比红黑树更简单, 适合并发访问
```

---

## 三、核心设计二：Compaction策略

### 3.1 为什么需要Compaction？

```
没有Compaction会发生什么?

  SSTable #1:  com.aaa → val1
  SSTable #2:  com.aaa → val2  (更新版本)
  SSTable #3:  com.aaa → DELETE (删除标记)
  SSTable #4:  com.aaa → val3  (再次更新)
  ...数百个SSTable...

读取 com.aaa:
  需要检查每个SSTable!
  → 数百次I/O操作(即使Bloom Filter过滤一些)
  → 读性能极度下降
  → 存储空间浪费(旧版本仍在占用空间)
```

### 3.2 Minor Compaction vs Major Compaction

```
Minor Compaction (小合并):
  ┌──────────┐  ┌──────────┐  ┌──────────┐
  │SSTable A │  │SSTable B │  │SSTable C │  (最近几个小SSTable)
  └────┬─────┘  └────┬─────┘  └────┬─────┘
       │              │              │
       └──────────────┴──────┬───────┘
                             │
                      ┌──────▼──────┐
                      │ SSTable ABC │  (合并为1个较大SSTable)
                      └─────────────┘
  
  触发条件: MemTable Flush产生多个小SSTable(每个~64MB)
  过程:
    1. 读入几个MemTable生成的SSTable(都在内存/Page Cache)
    2. 多路归并排序(所有输入SSTable都已排序)
    3. 重复Key保留最新Timestamp
    4. 删除已标记DELETE的Key
    5. 写出1个新的SSTable
  开销: 小(I/O量 = 输入SSTable总大小 + 输出SSTable大小)
  频率: 高频(每次MemTable Flush后可能触发)

Major Compaction (大合并):
  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌───────────────┐
  │SSTable 1│ │SSTable 2│ │SSTable 3│ │SSTable N(大的)│  (所有SSTable)
  └────┬────┘ └────┬────┘ └────┬────┘ └───────┬───────┘
       │           │           │               │
       └───────────┴─────┬─────┴───────────────┘
                         │
                  ┌──────▼──────┐
                  │ SSTable New │  (合并为1个SSTable)
                  └─────────────┘

  触发条件: 定期(如每天一次) 或 SSTable数量超过阈值
  过程: 同Minor, 但涉及所有SSTable
  开销: 大(I/O量可能是Tablet总数据的数倍)
  效果: 彻底清理旧版本数据, 去重, 删除已标记的行, 回收存储空间
```

### 3.3 Write Amplification（写放大）问题

```
写放大 = 实际写入磁盘的数据 / 应用写入的数据

为什么LSM-Tree有Write Amplification?
  1次写入: MemTable(1×写) → Flush SSTable(1×写) → Minor Compaction(重写) → Major Compaction(再次重写)
  计算: 应用写1MB → 最终磁盘写2-10MB → 写放大2-10倍!

写放大的来源:
  ┌──────────────────────────────────────┐
  │ 原始写入: 1MB                         │
  │ MemTable → SSTable: 1MB (压缩后可能300KB) │
  │ 第1次Minor Compaction: 读300KB + 写300KB │
  │ 第2次Minor Compaction: 读600KB + 写600KB │
  │ ...                                   │
  │ Major Compaction: 读2MB + 写2MB        │
  │ 总写入量: 约3-5MB → 写放大3-5×         │
  └──────────────────────────────────────┘

如何降低写放大?
  - 分层Compaction(如LevelDB/RocksDB): 类似多级Minor Compaction
  - 通用Compaction(如Cassandra): 按SSTable大小分组, 同大小组内Compaction
  - 调大MemTable: 减少Flush频率 → 减少需要Compaction的SSTable数量
  - 异步Compaction: 不影响前台写入延迟
```

### 3.4 Compaction对读写性能的影响

| 方面 | 无Compaction | 有Compaction | 最佳实践 |
|------|-------------|-------------|----------|
| **写延迟(P99)** | 极低(只写MemTable) | 略高(Compaction消耗IO带宽) | 限制Compaction带宽 |
| **读延迟(P50)** | 极高(需查数百SSTable) | 低(只需查少量SSTable) | 保持SSTable数<50 |
| **存储空间** | 极大(多版本+墓碑) | 正常 | 定期GC旧版本 |
| **Compaction开销** | 零 | 高(IO+CPU密集) | 低峰期触发Major |
| **系统稳定性** | 稳定(无后台负载) | 可能波动(Compaction争IO) | 隔离Compaction IO |

---

## 四、核心设计三：Tablet分裂与迁移

### 4.1 Tablet —— Bigtable的数据分片单元

```
Bigtable = 多个Tablet组成的Sorted Map

Tablet分裂过程:
  一个Tablet存储Row Key范围 ["a", "m")
  Tablet大小增长到200MB(可配置阈值)
  ↓
  Tablet分裂:
    Tablet 1: ["a", "g")  (约100MB)
    Tablet 2: ["g", "m")  (约100MB)
  ↓
  两个Tablet可以分布到不同的Tablet Server上!

Tablet的Row Key边界是动态的:
  - 初始: 1个Tablet覆盖整个Row Key空间
  - 负载增长: Tablet自动分裂
  - 写入集中某个Row范围 → 该范围Tablet更频繁分裂
```

### 4.2 METADATA三层结构（经典设计！）

```
Bigtable的元数据查找链(特殊的"俄罗斯套娃"设计):

  Level 0: Chubby File
    Chubby(类似ZooKeeper)存储:
    /bigtable/root_tablet_location → "Root Tablet在TabletServer-5上"
    
  Level 1: Root Tablet
    唯一的特殊Tablet
    记录所有METADATA Tablet的位置
    内容: (METADATA_tablet_begin_key → TabletServer_location)
    从不分裂!

  Level 2: Other METADATA Tablets
    记录所有User Tablet的位置
    内容: (user_table:begin_row_key → TabletServer_location + Log信息)
    每个METADATA Tablet约128MB → 可定位约2^34个User Tablet(约2^61字节数据)

  Level 3: User Tablets
    真正的用户数据

查询链(3次网络往返):
  Client → Chubby: "Root Tablet在哪?"
  Chubby → Client: "TabletServer-5"

  Client → TabletServer-5: "UserTable, RowKey='com.cnn.www' 在哪个TabletServer?"
  TabletServer-5查Root Tablet: "METADATA Tablet 42覆盖 'com.*'"
                           → "METADATA Tablet 42在TabletServer-17"

  Client → TabletServer-17: "UserTable, RowKey='com.cnn.www' 在哪个TabletServer?"
  TabletServer-17查METADATA Tablet: "UserTable ['com.aaa', 'com.zzz')在TabletServer-42"

  Client → TabletServer-42: "读UserTable RowKey='com.cnn.www'"
  TabletServer-42: 返回数据

优化: Client缓存METADATA → 大部分请求只需1次查询(直接到User Tablet Server)
      → 缓存失效时也只需2次(Client → METADATA Tablet → User Tablet)
```

### 4.3 Tablet迁移过程

```
Master决定迁移Tablet X从Server A到Server B:

Step 1: Master标记Tablet X为UNASSIGNED
  METADATA表更新: Tablet X状态从SERVING→UNASSIGNED

Step 2: Master发送卸Tablet请求给Server A
  Server A: 
    ① 将MemTable做Minor Compaction(Flush所有SSTable)
    ② 停止服务Tablet X的请求(新请求返回"请重试")
    ③ 完成所有正在处理的请求
    ④ 回复Master: "Tablet X已卸载"

Step 3: Master发送加载Tablet请求给Server B  
  Server B:
    ① 从GFS读取Tablet X的所有SSTable文件
    ② 重放Commit Log中Tablet X的写入(如果有未Flush的)
    ③ 重建MemTable
    ④ 开始服务Tablet X的请求
    ⑤ 回复Master: "Tablet X已加载"

Step 4: Master更新METADATA
  Tablet X: TabletServer从A→B, 状态从UNASSIGNED→SERVING

Step 5: Client重试
  之前收到"请重试"的Client:
    重新查METADATA → 发现Tablet X已迁移到Server B
    → 向Server B发起请求(成功)
```

---

## 五、列族（Column Family）概念与设计

### 5.1 Column Family的设计意图

```
为什么要有Column Family?

传统关系型数据库: 
  CREATE TABLE users (
    id INT,
    name VARCHAR(100),
    email VARCHAR(200),
    avatar BLOB,          ← 大头像(可能1MB)
    preferences TEXT       ← 长JSON
  );
  SELECT name, email FROM users WHERE id=123;
  → 必须读取整行(包括1MB的avatar和长preferences!)

Bigtable的Column Family:
  Column Family: "basic"    → name, email (小字段, 一起压缩)
  Column Family: "media"    → avatar (大BLOB, 单独压缩)
  Column Family: "settings" → preferences (JSON, 单独压缩)
  
  SELECT basic:name, basic:email FROM users WHERE row='user123';
  → 只读"basic" Column Family的数据(跳过media和settings!)
```

### 5.2 Column Family的物理隔离

```
同一个Row的不同Column Family存储在不同的SSTable中:

Tablet X SSTable集合:
  ┌──────────────────────────────────────────┐
  │ SSTable_CF_basic_001  (CF=basic)         │
  │ SSTable_CF_basic_002  (CF=basic)         │
  │ SSTable_CF_media_001  (CF=media)         │
  │ SSTable_CF_settings_001 (CF=settings)    │
  └──────────────────────────────────────────┘

Compaction也是按Column Family独立进行的:
  - basic Column Family: 高频Compaction(数据小, 写入频繁)
  - media Column Family: 低频Compaction(数据大, 写入少)
  - settings Column Family: 中频Compaction

好处:
  1. IO隔离: 读取basic字段不会触发media的磁盘IO
  2. 压缩策略独立: basic用Snappy(快速), media用ZSTD(高压缩比)
  3. Compaction独立: media的大量Compaction不影响basic的延迟
  4. 缓存独立: basic的热数据可以独立缓存
```

### 5.3 Column Family配置示例（HBase映射）

```java
// HBase中创建Column Family（直接映射Bigtable概念）
Configuration conf = HBaseConfiguration.create();
Connection conn = ConnectionFactory.createConnection(conf);
Admin admin = conn.getAdmin();

// 创建表描述符
HTableDescriptor tableDesc = new HTableDescriptor(TableName.valueOf("webpages"));

// Column Family: "contents" - 页面内容(大BLOB, 1个版本, TTL=30天)
HColumnDescriptor cfContents = new HColumnDescriptor("contents");
cfContents.setMaxVersions(1);                    // 只要最新版本
cfContents.setTimeToLive(30 * 24 * 3600);        // 30天TTL
cfContents.setCompressionType(Compression.Algorithm.GZ); // GZip压缩
cfContents.setBlocksize(128 * 1024);             // 128KB Data Block

// Column Family: "links" - 链接关系(小数据, 3个版本)
HColumnDescriptor cfLinks = new HColumnDescriptor("links");
cfLinks.setMaxVersions(3);                       // 保留3个版本
cfLinks.setCompressionType(Compression.Algorithm.SNAPPY); // Snappy快速压缩
cfLinks.setInMemory(true);                       // 优先缓存内存

// Column Family: "metadata" - 页面元数据(小字段, 1个版本)
HColumnDescriptor cfMeta = new HColumnDescriptor("metadata");
cfMeta.setMaxVersions(1);
cfMeta.setBloomFilterType(BloomType.ROWCOL);     // Row+Col级Bloom Filter

tableDesc.addFamily(cfContents);
tableDesc.addFamily(cfLinks);
tableDesc.addFamily(cfMeta);

admin.createTable(tableDesc);
```

---

## 六、Bigtable与HBase/Cassandra的映射

### 6.1 Bigtable → HBase 概念映射

| Bigtable | HBase | 说明 |
|----------|-------|------|
| Bigtable | HBase | HBase是Bigtable最忠实的开源实现 |
| Tablet Server | RegionServer | 服务数据读写请求的工作节点 |
| Tablet | Region | 数据分片单元，按Row Key范围划分 |
| Master | HMaster | 负责Region分配、负载均衡、Schema变更 |
| Chubby | ZooKeeper | 分布式锁服务，存储集群元数据 |
| SSTable | HFile | 不可变的持久化数据文件 |
| MemTable | MemStore | 内存中的写入缓冲区 |
| Commit Log | WAL (Write Ahead Log) | 持久化写入日志 |
| Column Family | Column Family | 列的物理分组 |
| Minor Compaction | Minor Compaction | HFile的小合并 |
| Major Compaction | Major Compaction | HFile的大合并 |
| METADATA Table | hbase:meta | 存储Region位置的系统表 |
| GFS | HDFS | 底层分布式文件系统 |

### 6.2 HBase与Bigtable的关键差异

```
1. Coprocessor (HBase独有)
   Bigtable依赖MapReduce处理复杂计算(如构建索引)
   HBase引入了Coprocessor(类似RDBMS的存储过程和触发器)
     - Observer: 拦截Region操作(类似触发器)
     - Endpoint: 在Region端执行计算(类似存储过程)
   优势: 计算靠近数据，减少网络传输

2. 二级索引
   Bigtable不直接支持二级索引(应用层自己维护索引表)
   HBase通过Phoenix等项目提供了SQL-like的二级索引支持
   也可以通过Coprocessor实现自定义索引

3. Region分裂策略
   Bigtable: 按大小分裂(默认128-256MB)
   HBase: 支持多种分裂策略
     - ConstantSizeRegionSplitPolicy: 按固定大小
     - IncreasingToUpperBoundRegionSplitPolicy: 动态大小(默认)
     - KeyPrefixRegionSplitPolicy: 按Row Key前缀
     - DelimitedKeyPrefixRegionSplitPolicy: 按分隔符

4. 安全性
   Bigtable依赖Google内部认证系统
   HBase支持Kerberos认证、ACL行列级权限控制
```

### 6.3 Bigtable → Cassandra 概念映射

| Bigtable | Cassandra | 差异 |
|----------|-----------|------|
| 数据模型 | (row, column, timestamp) → value | Similar, but with CQL table abstraction |
| Row Key排序 | 字典序 | 支持自定义排序(通过Partitioner和Clustering Key) |
| 一致性 | 强一致性(单行) | 可调一致性(Tuneable Consistency) |
| 架构 | Master-Slave | Peer-to-Peer(Dynamo风格) |
| 共识 | Chubby(Paxos) | Gossip协议 |
| 写入路径 | MemTable → SSTable | Memtable → SSTable(相似) |
| Compaction | Minor + Major | SizeTiered / Leveled / TimeWindow |

**为什么Cassandra没有选择Bigtable的Master架构？**

Cassandra的Dynamo血统决定了：
- 多数据中心部署需要Peer-to-Peer架构（没有跨数据中心Master）
- 永远可写的需求（Dynamo的"购物车永远可用"）不适合Master-Slave
- Cassandra放弃了HBase/Bigtable的强一致性，换取了更高的可用性

---

## 七、关键应用场景 —— Google内部的"Table as Database"

### 7.1 Google的实际用例

```
场景1: Web Crawl索引 (最大的Bigtable集群)
  表名: webtable
  Row Key: 反转URL (com.cnn.www → 方便按域名分组)
  Column Family "contents": 页面原始HTML
  Column Family "anchor": 锚文本(从其他页面指向此页面的链接文字)
  Column Family "metadata": 抓取时间、最后修改时间、HTTP状态码
  规模: 数百TB, 数千台Tablet Server

场景2: Google Earth/Maps
  表名: earth_index
  Row Key: 地理区域编码
  Column Family "imagery": 卫星图像块(大BLOB)
  Column Family "vector": 矢量地图数据
  特点: 大量大BLOB数据的范围查询(缩放地图时)

场景3: Google Analytics
  表名: analytics_events
  Row Key: site_id + reverse_timestamp(方便按时间范围扫描)
  Column Family "metrics": 访问量、跳出率、转化率
  特点: 时间序列数据的聚合查询
  利用Timestamp多版本功能天然记录历史数据
```

### 7.2 Row Key设计原则（从Bigtable学到的）

```
原则1: 避免热点写入
  ✗ Row Key = 时间戳(递增)
    → 所有新写入集中在最后一个Tablet → 热点
  ✓ Row Key = 反转时间戳 + 随机后缀
    或 Row Key = hash(user_id) → 写入均匀分布

原则2: 利用字典序实现范围扫描
  设计: "域名 + 反转时间" 
    com.cnn.www#20240101
    com.cnn.www#20240102
    com.cnn.www#20240103
    → 扫描某个域名的所有历史记录只需要一次范围扫描!

原则3: Row Key不要太长
  每个Cell都包含完整的Row Key
  Row Key 100字节, 1亿行 → 10GB浪费在Row Key重复存储上
  
原则4: 平衡Region分裂和范围查询
  Row Key = hash(user_id) 
    → 写入均匀(好), 但无法做范围查询(坏)
  Row Key = user_id
    → 可以按user_id范围查询(好), 但可能热点(坏)
  折中: user_type(高基数) + user_id
    → 按user_type分散, user_id内有序
```

---

## 八、练习题

### 基础题

**1. 解释Bigtable中SSTable和MemTable的关系。为什么需要MemTable？**

<details>
<summary>参考答案</summary>

MemTable是内存中的有序数据结构（通常为SkipList），用于缓存最近的写入。写入先到MemTable（同时写WAL保证持久化），当MemTable达到大小阈值（如128MB），整个MemTable被冻结并Flush到GFS成为一个不可变的SSTable文件。

需要MemTable的原因：
1. 写入性能：内存随机写入远快于磁盘随机写入（LSM-Tree的核心优势）
2. 批量落盘：将多次随机写入合并为一次大块顺序写入SSTable
3. 读缓存：最新数据在MemTable中，读取时先查MemTable，不需要I/O

</details>

**2. Minor Compaction和Major Compaction有什么区别？**

参考上文第三节。

**3. Bigtable的METADATA三层结构是如何工作的？为什么不用两层？**

<details>
<summary>参考答案</summary>

考虑到两层结构（Root Tablet → User Tablets），如果User Tablet数量极大（百万级别），Root Tablet会变得非常大（超过内存限制且无法分裂）。

三层结构的设计巧妙之处：
- Root Tablet：只存METADATA Tablet位置（从不分裂，始终可以放在内存）
- METADATA Tablets：可以分裂（每个约128MB），存User Tablet位置
- User Tablets：真正的数据

三层结构可以线性扩展：每个METADATA Tablet可以定位约2^17个User Tablet，METADATA Tablet本身可以无限分裂。

</details>

### 进阶题

**4. 为什么Bigtable选择"单行事务"而不是"跨行事务"？这对上层应用有什么影响？**

<details>
<summary>参考答案</summary>

原因：
1. 分布式跨行事务（如Percolator）需要两阶段提交（2PC），性能代价大
2. Bigtable的设计目标是"PB级存储 + 毫秒级读写"，强事务会牺牲性能
3. Google的大部分应用场景（Web索引、地图数据、监控数据）不需要跨行事务
4. 需要跨行事务的场景通过上层抽象解决（Megastore → Spanner）

影响：
- 上层应用如果确实需要跨行原子操作，必须自行实现（如Google的Percolator使用Bigtable的CAS操作实现分布式事务）
- 应用设计需要考虑"数据是否应该放在同一行"来利用单行事务

</details>

**5. 如果让你给Bigtable加上二级索引，你会怎么设计？**

<details>
<summary>参考答案</summary>

方案1：应用层维护索引表
- 创建"索引表"：Row Key = (Column Value, Original Row Key)
- 写入主表时，同时写入索引表（利用单行事务保证主表和索引表的一致性是难点！）
- 这是Google内部最常用的方式

方案2：Coprocessor自动维护（HBase方式）
- 在RegionServer端安装Observer Coprocessor
- 写入主表后，自动触发索引更新
- 一致性由RegionServer保证（同Region内的操作是原子的）

方案3：异步索引（最终一致性）
- 写入主表成功后，异步更新索引表
- 读取时可能查到"过时"的索引（需要应用层容忍）
- 适合索引不一致不造成严重后果的场景（如"你可能也喜欢"推荐）

</details>

**6. SSTable的Bloom Filter为什么放在文件末尾（Footer中）？为什么不放在文件开头？**

<details>
<summary>参考答案</summary>

SSTable是顺序写入生成的：
1. 先写Data Blocks（此时还不知道所有Key）
2. 再写Index Block（汇总了所有Block的起始Key）
3. 最后写Footer（包含Bloom Filter offset）

如果Bloom Filter放在文件开头，必须在写完所有Data Blocks后"回头"写文件开头——这对于GFS来说意味着"随机写"，违反GFS的设计原则。

Footer放在末尾是顺序写的自然结果，读时只需要一次seek到文件末尾即可获取所有元信息。

</details>

### 设计题

**7. 设计一个基于Bigtable/HBase的微博Feed系统。要求：支持用户发布微博、关注/取消关注、获取首页Timeline（自己关注的人的最新微博）。**

<details>
<summary>参考答案</summary>

表设计：

1. 微博表 (weibo):
   - Row Key: user_id + reverse_timestamp (按用户+时间排序)
   - Column Family "content": 微博文本、图片URL等

2. Timeline表 (timeline):  
   - Row Key: user_id (当前用户的首页)
   - Column Family "feeds": 
     - Column Qualifier: reverse_timestamp + author_user_id
     - Value: weibo_id (指向微博表的引用)
   - 写入: 用户A发布微博 → 找到A的所有粉丝 → 在每个粉丝的Timeline中追加

3. 关注表 (follows):
   - Row Key: user_id (关注者)
   - Column Family "following":
     - Column Qualifier: followed_user_id
     - Value: 关注时间

读取首页Timeline:
  1. scan timeline表, Row Key=当前用户ID (1次range scan)
  2. 最多返回最近50条(按reverse_timestamp倒序即最近)
  3. 根据weibo_id批量读取微博内容(from weibo表)

写入推模式(Push) vs 拉模式(Pull)的权衡:
  - Push(写入时推送到粉丝Timeline): 读快，写放大(大V发布要推给千万粉丝)
  - Pull(读取时拉取关注者微博): 写快，读放大(读取时需要合并N个关注者)
  - 实践: 活跃用户用Push，非活跃用户用Pull(混合模式)

</details>

---

## 九、关键概念速查表

| 概念 | Bigtable术语 | HBase术语 | 说明 |
|------|-------------|----------|------|
| 数据分片 | Tablet | Region | 按Row Key范围分片 |
| 分片服务器 | Tablet Server | RegionServer | 服务数据读写 |
| 内存写入缓冲区 | MemTable | MemStore | 批量写入的内存结构 |
| 持久化数据文件 | SSTable | HFile | 不可变有序文件 |
| 写前日志 | Commit Log | WAL | 崩溃恢复 |
| 分布式锁服务 | Chubby | ZooKeeper | 集群元数据与协调 |
| 小合并 | Minor Compaction | Minor Compaction | MemTable生成SSTable的合并 |
| 大合并 | Major Compaction | Major Compaction | 全量SSTable合并 |
| 列分组 | Column Family | Column Family | 列的物理分组 |
| 分布式文件系统 | GFS | HDFS | 底层存储 |
| 行级事务 | Single-Row Transaction | Row-Level Atomicity | 单行内的原子操作保证 |

---

## 十、编程实践：用Python模拟LSM-Tree写入和读取过程

```python
import struct
import time
import hashlib
from collections import defaultdict
from typing import Optional, List, Tuple

class MemTable:
    def __init__(self, max_size: int = 256):
        self.data = {}
        self.max_size = max_size
        self.size = 0
        self.tombstones = set()

    def put(self, key: str, value: str, timestamp: int):
        self.data[key] = (value, timestamp)
        self.size += 1
        return self.size >= self.max_size

    def delete(self, key: str, timestamp: int):
        self.tombstones.add(key)
        self.data[key] = (None, timestamp)
        self.size += 1
        return self.size >= self.max_size

    def get(self, key: str) -> Optional[Tuple[str, int]]:
        if key in self.tombstones:
            return (None, self.data[key][1]) if key in self.data else None
        return self.data.get(key)

    def items_sorted(self):
        for key in sorted(self.data.keys()):
            yield key, self.data[key]

    def clear(self):
        self.data.clear()
        self.tombstones.clear()
        self.size = 0


class SSTable:
    def __init__(self, level: int, data: dict, tombstones: set):
        self.level = level
        self.data = dict(sorted(data.items()))
        self.tombstones = set(tombstones)
        self.min_key = min(self.data.keys()) if self.data else ""
        self.max_key = max(self.data.keys()) if self.data else ""
        self.bloom_filter = self._build_bloom_filter()

    def _build_bloom_filter(self) -> set:
        return {hashlib.md5(k.encode()).hexdigest()[:8] for k in self.data.keys()}

    def might_contain(self, key: str) -> bool:
        key_hash = hashlib.md5(key.encode()).hexdigest()[:8]
        return key_hash in self.bloom_filter

    def get(self, key: str) -> Optional[Tuple[str, int]]:
        if not self.might_contain(key):
            return None
        if key in self.tombstones:
            return (None, self.data[key][1]) if key in self.data else None
        return self.data.get(key)


class LSMTree:
    def __init__(self, memtable_size: int = 10):
        self.memtable = MemTable(max_size=memtable_size)
        self.immutable_memtable: Optional[MemTable] = None
        self.sstables: List[SSTable] = []
        self.timestamp_counter = 0
        self.wal: List[Tuple[str, str, str, int]] = []

    def _next_timestamp(self) -> int:
        self.timestamp_counter += 1
        return self.timestamp_counter

    def _flush_memtable(self):
        if self.immutable_memtable is None:
            return
        data = dict(self.immutable_memtable.data)
        tombstones = set(self.immutable_memtable.tombstones)
        sstable = SSTable(level=0, data=data, tombstones=tombstones)
        self.sstables.insert(0, sstable)
        print(f"  [Flush] MemTable → SSTable#{len(self.sstables)-1} "
              f"({len(data)} keys, range: [{sstable.min_key}, {sstable.max_key}])")
        self.immutable_memtable = None

    def put(self, key: str, value: str):
        ts = self._next_timestamp()
        self.wal.append(("PUT", key, value, ts))
        print(f"  [Write] PUT key='{key}', value='{value}', ts={ts}")

        if self.immutable_memtable is not None:
            self._flush_memtable()

        is_full = self.memtable.put(key, value, ts)
        if is_full:
            self.immutable_memtable = self.memtable
            self.memtable = MemTable(max_size=self.memtable.max_size)
            print(f"  [Switch] MemTable已满, 切换为Immutable, 等待Flush")

    def delete(self, key: str):
        ts = self._next_timestamp()
        self.wal.append(("DELETE", key, "", ts))
        print(f"  [Write] DELETE key='{key}', ts={ts}")

        if self.immutable_memtable is not None:
            self._flush_memtable()

        is_full = self.memtable.delete(key, ts)
        if is_full:
            self.immutable_memtable = self.memtable
            self.memtable = MemTable(max_size=self.memtable.max_size)

    def get(self, key: str):
        print(f"\n  [Read] GET key='{key}'")

        result = self.memtable.get(key)
        if result is not None:
            value, ts = result
            if value is None:
                print(f"    → MemTable: TOMBSTONE (ts={ts})")
                return None
            print(f"    → MemTable: value='{value}' (ts={ts})")
            return value

        if self.immutable_memtable is not None:
            result = self.immutable_memtable.get(key)
            if result is not None:
                value, ts = result
                if value is None:
                    print(f"    → Immutable MemTable: TOMBSTONE (ts={ts})")
                    return None
                print(f"    → Immutable MemTable: value='{value}' (ts={ts})")
                return value

        latest_ts = -1
        latest_value = None
        found_tombstone = False

        for i, sstable in enumerate(self.sstables):
            if not sstable.might_contain(key):
                print(f"    → SSTable#{i}: Bloom Filter跳过")
                continue

            result = sstable.get(key)
            if result is not None:
                value, ts = result
                if value is None:
                    if ts > latest_ts:
                        latest_ts = ts
                        found_tombstone = True
                    print(f"    → SSTable#{i}: TOMBSTONE (ts={ts})")
                else:
                    if ts > latest_ts:
                        latest_ts = ts
                        latest_value = value
                        found_tombstone = False
                    print(f"    → SSTable#{i}: value='{value}' (ts={ts})")

        if found_tombstone:
            print(f"    → 最终结果: 已删除 (最新ts={latest_ts})")
            return None
        if latest_value is not None:
            print(f"    → 最终结果: value='{latest_value}' (最新ts={latest_ts})")
            return latest_value

        print(f"    → 最终结果: Key不存在")
        return None

    def compact(self):
        print(f"\n  [Major Compaction] 合并所有SSTable...")
        merged_data = {}
        merged_tombstones = set()

        for sstable in reversed(self.sstables):
            for key, (value, ts) in sstable.data.items():
                if key in merged_data:
                    existing_ts = merged_data[key][1]
                    if ts > existing_ts:
                        merged_data[key] = (value, ts)
                else:
                    merged_data[key] = (value, ts)
            merged_tombstones.update(sstable.tombstones)

        final_data = {}
        for key, (value, ts) in merged_data.items():
            if key in merged_tombstones and value is None:
                continue
            if value is not None:
                final_data[key] = (value, ts)

        self.sstables = [SSTable(level=1, data=final_data, tombstones=set())]
        print(f"  [Compaction完成] {len(merged_data)} → {len(final_data)} keys")


if __name__ == "__main__":
    db = LSMTree(memtable_size=5)

    print("===== 写入阶段 =====")
    for i in range(12):
        db.put(f"key{i:02d}", f"value_{i}")

    print("\n===== 读取阶段 =====")
    db.get("key05")
    db.get("key00")
    db.get("key99")

    print("\n===== 删除阶段 =====")
    db.delete("key05")

    print("\n===== 删除后读取 =====")
    db.get("key05")

    print("\n===== 更新后读取 =====")
    db.put("key03", "value_3_updated")
    db.get("key03")

    print("\n===== Major Compaction =====")
    db.compact()

    print("\n===== Compaction后读取 =====")
    db.get("key03")
    db.get("key05")
```

---

## 十一、课后深度思考题

**思考题1：Bigtable的Compaction过程会产生写放大（Write Amplification）。假设一个Tablet有10个SSTable，每个100MB，做一次Major Compaction需要读写多少数据？如果每秒写入10MB，每小时产生多少写放大？如何降低？**

<details>
<summary>参考思路</summary>

Major Compaction读写量：
- 读取：10 × 100MB = 1GB
- 写入：合并后约1GB（假设无重复和墓碑）
- 总IO：2GB
- 写放大倍数：2GB / (10MB/s × 3600s × 实际写入比例)

每小时写入10MB × 3600 = 36GB原始数据。
如果每小时做一次Major Compaction，且SSTable总量约36GB：
- Compaction IO：36GB读 + 36GB写 = 72GB
- 写放大：72GB / 36GB = 2倍

降低方法：
1. 分层Compaction（LevelDB风格）：L0→L1→L2逐层合并，每层大小递增，减少大范围重写
2. 增大MemTable：减少Flush频率，减少SSTable数量
3. 调低Major Compaction频率：只在低峰期执行
4. RocksDB的Dynamic Level：自动调整每层大小比例，优化写放大

</details>

**思考题2：Bigtable的METADATA三层结构中，Root Tablet为什么"从不分裂"？如果Root Tablet也允许分裂，会有什么问题？**

<details>
<summary>参考思路</summary>

Root Tablet从不分裂的原因：
1. Root Tablet的位置存储在Chubby中（固定入口点）。如果Root Tablet分裂，Chubby中需要记录多个Root Tablet的位置，增加了Chubby的复杂度。
2. Root Tablet只存储METADATA Tablet的位置信息，数据量很小（每个METADATA Tablet约1KB元数据），即使管理数百万个User Tablet，Root Tablet也只有几MB，远不需要分裂。
3. 客户端的查找链是固定的：Chubby → Root Tablet → METADATA Tablet → User Tablet。如果Root Tablet分裂，查找链变得更复杂。

如果Root Tablet允许分裂：
- Chubby需要存储多个Root Tablet的位置（类似METADATA的三层变成四层）
- 客户端需要先查询"哪个Root Tablet包含我要找的METADATA Tablet"
- 增加了一次额外的网络往返
- 但实际上Root Tablet的数据量极小，分裂的需求几乎不存在

</details>

**思考题3：Bigtable只支持单行事务。如果要在Bigtable之上实现跨行事务（如转账：A扣100元，B加100元），你会如何设计？你的方案在什么条件下会失败？**

<details>
<summary>参考思路</summary>

方案1：Percolator风格（Google实际方案）
- 使用Bigtable的列级CAS（Compare-And-Swap）操作
- 每个Cell增加"锁"列和"写入"列
- 两阶段提交：先锁A和B，再提交
- 失败条件：客户端在两阶段之间崩溃 → 需要事务恢复机制（Percolator用"事务清理器"处理）

方案2：应用层2PC
- 选一个协调者，先预写A和B，再提交
- 失败条件：协调者崩溃 → 参与者永远等待（阻塞问题）

方案3：将相关数据放在同一行
- 设计Row Key = "transfer_A_B"，将A和B的余额放在同一行的不同列
- 利用单行事务保证原子性
- 失败条件：A或B的余额被其他事务同时修改 → 需要乐观锁

方案4：Spanner风格（Google最终方案）
- 使用TrueTime API提供全局时间戳
- 基于时间戳的并发控制
- 失败条件：时钟漂移超过TrueTime的误差范围

</details>

**思考题4：Bigtable的Bloom Filter可以按Row或Row+Column配置。在什么场景下应该用Row级Bloom Filter，什么场景下应该用Row+Column级？两者的内存开销差异有多大？**

<details>
<summary>参考思路</summary>

Row级Bloom Filter：
- 只按Row Key建立Bloom Filter
- 适用场景：主要按Row Key做点查（Get操作），不关心具体Column
- 内存开销：每个SSTable约1MB（100万行 × 10 bits/key / 8 ≈ 1.25MB）

Row+Column级Bloom Filter：
- 按(Row Key, Column Family:Qualifier)组合建立Bloom Filter
- 适用场景：同一Row有大量Column，但查询通常只访问少数Column
  - 例如：网页表有contents、anchor、metadata三个Column Family
  - 查询"某个URL的anchor"时，Row+Column级Bloom Filter可以跳过只含contents的SSTable
- 内存开销：可能是Row级的3-10倍（取决于Column数量）

选择建议：
- 如果Column Family少（1-2个）→ Row级足够
- 如果Column Family多且查询通常只涉及1-2个 → Row+Column级更优
- 如果内存紧张 → Row级
- HBase默认：Row级（可按Column Family配置）

</details>

**思考题5：Bigtable的Tablet分裂是自动的（按大小触发），但合并不是自动的。为什么Google选择"自动分裂+手动合并"而不是"自动分裂+自动合并"？自动合并会导致什么问题？**

<details>
<summary>参考思路</summary>

自动分裂的原因：
- Tablet太大 → 读写延迟增加、负载不均衡、故障恢复慢
- 分裂是"安全"操作：只修改元数据，不移动数据
- 分裂的收益立即可见

不自动合并的原因：
1. **合并是"昂贵"操作**：需要读取两个Tablet的所有SSTable，合并后写入新SSTable，消耗大量IO和CPU
2. **合并可能导致"分裂-合并"抖动**：如果Tablet在分裂阈值附近波动，自动合并后会立即再次分裂
3. **合并期间影响性能**：Major Compaction级别的IO开销可能影响在线读写
4. **小Tablet不一定有问题**：如果小Tablet的读写量也小，合并的收益不大
5. **人工判断更准确**：运维人员可以判断哪些Tablet应该合并（如大量删除后的碎片Tablet）

自动合并的风险：
- 分裂-合并循环：Tablet大小在阈值附近波动 → 反复分裂和合并
- IO风暴：大量Tablet同时触发合并 → 集群IO打满
- 干扰在线服务：合并的IO与正常读写竞争资源

</details>

---

> **核心Takeaway**：Bigtable = LSM-Tree + 分布式 + 多维有序Map。它告诉我们：系统设计的艺术在于**选择合适的简单结构，并将它们组合成强大的整体**——跳过表(SkipList) + 排序字符串表(SSTable) + 布隆过滤器(Bloom Filter) + 预写日志(WAL)，四个简单结构组合成了支撑Google数十亿页面的核心存储引擎。