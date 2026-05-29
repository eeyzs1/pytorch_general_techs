# 大数据技术全景图（产业级）

> 本文档系统性地梳理了大数据领域所有产业级技术，按照 **大分类 → 子分类 → 分支** 的层级结构组织，并详细阐述每个分类/分支的目的与基本原理。

---

## 目录

1. [数据采集与摄入](#1)
2. [消息队列与事件流](#2)
3. [数据存储](#3)
4. [数据湖与数据湖仓](#4)
5. [数据计算与处理](#5)
6. [数据仓库与OLAP](#6-olap)
7. [数据集成与ETL](#7-etl)
8. [数据编排与调度](#8)
9. [数据分析与BI](#9-bi)
10. [机器学习与AI](#10-ai)
11. [数据治理与安全](#11)
12. [数据监控与可观测性](#12)
13. [数据虚拟化与联邦](#13)
14. [实时分析与决策](#14)
15. [数据开发平台与工具](#15)

---

## 1. 数据采集与摄入

**目的**：将分散在各种数据源中的原始数据，以可靠、高效、低延迟的方式传输到大数据平台中，是整个数据生命周期的起点。

### 1.1 日志采集

**目的**：从服务器、容器、应用程序等运行环境中自动收集日志数据，用于运维监控、安全审计和业务分析。

| 分支 | 代表技术 | 基本原理 |
|------|----------|----------|
| 轻量级日志采集器 | Filebeat、Fluent Bit | 基于文件的尾部读取（tail），通过inotify/eventloop监听文件变更，轻量进程占用极少资源，将日志行封装后发送到下游 |
| 日志聚合与路由 | Apache Flume | 基于Source-Channel-Sink架构，Source接收数据，Channel缓冲，Sink输出，支持多级串联实现日志聚合与路由 |
| 日志处理与转发 | Logstash、Fluentd | 基于插件架构的日志处理管道：Input → Filter（解析/过滤/丰富）→ Output，支持正则解析（Grok）、字段映射等 |

### 1.2 数据库变更捕获（CDC）

**目的**：实时捕获数据库的增删改操作（INSERT/UPDATE/DELETE），将变更数据以事件流的形式同步到下游系统，实现准实时数据同步，避免全量轮询。

| 分支 | 代表技术 | 基本原理 |
|------|----------|----------|
| 基于日志的CDC | Debezium、Canal、Maxwell、Oracle GoldenGate | 读取数据库的事务日志（MySQL Binlog、PostgreSQL WAL、Oracle Redo Log），解析日志中的行级变更事件，将其转化为结构化的变更事件流发布到消息队列；Maxwell输出原生JSON格式，与Kafka集成最为便捷；OGG是企业级CDC标杆，支持异构数据库间实时同步 |
| 基于框架集成的CDC | Flink CDC | 将CDC能力内嵌到Flink计算框架中，直接从Binlog/WAL读取变更并转化为Flink DataStream，实现采集与计算一体化 |

### 1.3 批量数据传输

**目的**：在关系型数据库（RDBMS）与大数据存储（HDFS/Hive等）之间进行大规模数据的批量导入导出，适用于离线数仓构建和定期数据同步场景。

| 分支 | 代表技术 | 基本原理 |
|------|----------|----------|
| JDBC并行传输 | Sqoop | 利用MapReduce框架，将数据库表按主键范围切分为多个分片，每个Map Task通过JDBC并行读取/写入，实现大规模数据迁移 |
| 多源异构传输 | DataX、SeaTunnel | 基于Reader-Writer-Framework插件架构，Reader从源端拉取数据，Writer写入目标端，Framework负责调度、缓冲和容错，支持数十种数据源互连 |
| 云原生批量传输 | AWS DMS、GCP Data Transfer Service | 云托管的数据迁移服务，自动处理连接管理、增量同步和Schema映射 |

### 1.4 实时数据摄入

**目的**：以低延迟（秒级甚至毫秒级）将实时产生的数据摄入到大数据平台，支撑实时数仓、实时监控等场景。

| 分支 | 代表技术 | 基本原理 |
|------|----------|----------|
| 流式摄入管道 | Apache NiFi、StreamSets | 基于有向无环图（DAG）的可视化数据流设计，每个处理器（Processor）完成一步数据操作（读取/转换/路由/写入），支持背压（Backpressure）和优先级调度 |
| 连接器生态 | Kafka Connect | 基于Source Connector和Sink Connector插件体系，Source Connector从外部系统拉取数据写入Kafka，Sink Connector从Kafka读取数据写入外部系统，支持Exactly-Once语义 |
| 边缘摄入 | MQTT Broker（EMQX、Mosquitto） | 基于发布-订阅模式的轻量级消息协议，适用于带宽有限和网络不稳定的边缘场景，QoS分级保障消息可靠性 |

### 1.5 网络数据采集

**目的**：从互联网公开数据源（网页、API等）获取结构化或半结构化数据，用于竞品分析、舆情监控、市场研究等。

| 分支 | 代表技术 | 基本原理 |
|------|----------|----------|
| 分布式爬虫 | Scrapy、Apache Nutch | Scrapy基于Twisted异步框架，通过Scheduler-Downloader-Parser-Pipeline管道处理请求；Nutch基于MapReduce实现分布式爬取，集成Hadoop生态 |
| 无头浏览器采集 | Puppeteer、Playwright、Selenium | 通过DevTools Protocol或WebDriver协议控制无头浏览器，执行JavaScript渲染，获取动态加载的页面内容 |
| API数据采集 | 各类REST/GraphQL客户端 | 通过HTTP请求调用公开API，使用OAuth/API Key认证，按速率限制（Rate Limit）拉取结构化数据 |

---

## 2. 消息队列与事件流

**目的**：在分布式系统中实现异步解耦、流量削峰、数据缓冲和可靠传输，是实时数据架构的核心基础设施。

### 2.1 事件流平台

**目的**：提供高吞吐、持久化、可回放的事件流存储与分发能力，是构建事件驱动架构和实时数据管道的基石。

| 分支 | 代表技术 | 基本原理 |
|------|----------|----------|
| 分区日志模型 | Apache Kafka | 基于分布式提交日志（Commit Log），消息按Topic分区存储，每个分区是有序的追加写入日志，通过Consumer Group实现并行消费，支持消息回放和Exactly-Once语义 |
| 分层架构流平台 | Apache Pulsar | 采用计算-存储分离架构，Broker层处理消息收发，BookKeeper层持久化存储，支持多租户、跨地域复制和分层存储（热/温/冷） |
| 云托管流服务 | AWS Kinesis、Azure Event Hubs、GCP Pub/Sub | 云原生托管服务，自动管理分片和容量，按需扩展，与云生态深度集成；Pub/Sub为GCP核心异步消息服务，与BigQuery/Dataflow原生集成 |

### 2.2 消息队列

**目的**：在服务之间提供异步通信能力，支持请求-响应、发布-订阅、点对点等消息模式，实现系统解耦和流量控制。

| 分支 | 代表技术 | 基本原理 |
|------|----------|----------|
| AMQP协议队列 | RabbitMQ | 基于AMQP协议，通过Exchange-Queue-Binding路由模型，支持Direct/Fanout/Topic/Headers四种交换器类型，消息确认机制保证可靠投递 |
| 高可靠消息队列 | Apache RocketMQ | 基于NameServer-Broker-Producer-Consumer架构，支持顺序消息、事务消息、延迟消息和消息回溯，金融级可靠性 |
| 轻量级消息系统 | NATS、Apache ActiveMQ | NATS基于发布-订阅核心模式，极致轻量和低延迟；ActiveMQ支持JMS规范，多协议兼容 |

### 2.3 消息协议与标准

**目的**：定义消息的格式、传输和语义规范，确保异构系统之间能够互操作。

| 分支 | 代表技术 | 基本原理 |
|------|----------|----------|
| AMQP | RabbitMQ原生协议 | 定义了连接、通道、交换器、队列等抽象层，规范消息路由、确认和事务语义 |
| MQTT | EMQX、Mosquitto | 面向IoT场景的轻量级协议，基于Topic层级路由，三级QoS保障，报文头最小2字节 |
| CloudEvents | CNCF标准 | 定义事件数据的统一描述格式（属性+数据），使事件可在不同云平台和系统间互操作 |

---

## 3. 数据存储

**目的**：为不同类型的数据（结构化、半结构化、非结构化）和不同的访问模式（随机读写、范围查询、全文检索、时序聚合等）提供最优的存储引擎。

### 3.1 分布式文件系统

**目的**：提供可水平扩展的大规模文件存储，支持PB级甚至EB级数据存储，是大数据生态的存储底座。

| 分支 | 代表技术 | 基本原理 |
|------|----------|----------|
| 主从架构文件系统 | HDFS（Hadoop） | NameNode管理元数据和目录结构，DataNode存储实际数据块（默认128MB），数据块多副本（默认3副本）保证可靠性，适合大文件顺序读写 |
| 统一存储系统 | Ceph | 基于CRUSH算法实现数据分布，RADOS提供统一对象存储层，上层通过RGW（对象）、CephFS（文件）、RBD（块）提供多种接口，无单点故障 |
| 对象存储网关 | MinIO | 兼容S3 API的轻量级对象存储，基于纠删码（Erasure Coding）实现数据冗余，适合云原生部署和边缘场景 |
| 分布式缓存/加速层 | Alluxio、JuiceFS | Alluxio在计算框架和底层存储之间构建分布式内存缓存层，通过数据本地性加速I/O，减少远端存储访问；JuiceFS基于对象存储+元数据引擎构建POSIX兼容文件系统，兼顾高性能和低成本 |

### 3.2 键值（KV）存储

**目的**：提供O(1)时间复杂度的随机读写能力，用于缓存、会话管理、实时计数等需要极低延迟的场景。

| 分支 | 代表技术 | 基本原理 |
|------|----------|----------|
| 内存KV缓存 | Redis | 基于内存的单线程（6.0后I/O多线程）KV存储，使用I/O多路复用实现高并发，支持String/Hash/List/Set/ZSet/Stream等数据结构，RDB+AOF持久化 |
| 嵌入式KV引擎 | RocksDB、LevelDB | 基于LSM-Tree（Log-Structured Merge-Tree）的嵌入式存储引擎，写入先入MemTable，满后刷入SSTable，后台Compaction合并排序，写性能极高 |
| 分布式内存网格 | Apache Ignite | 基于分布式内存的KV存储和计算网格，数据按分区分布在集群节点，支持SQL查询和ACID事务 |

### 3.3 文档数据库

**目的**：存储和查询半结构化数据（JSON/BSON文档），无需预定义Schema，适合快速迭代和异构数据存储。

| 分支 | 代表技术 | 基本原理 |
|------|----------|----------|
| JSON文档存储 | MongoDB | 文档以BSON格式存储，支持动态Schema、二级索引、聚合管道，通过分片（Shard）实现水平扩展，副本集保证高可用 |
| 全文检索引擎 | Elasticsearch | 基于Apache Lucene，文档写入时通过分词器建立倒排索引，支持全文检索、聚合分析、地理位置查询，通过分片和副本实现分布式 |
| 分布式文档库 | CouchDB | 基于MVCC（多版本并发控制）的文档数据库，使用MapReduce视图进行查询，支持多主复制和离线同步 |

### 3.4 列式数据库

**目的**：以列为单位存储数据，大幅提升分析查询的I/O效率（只读取需要的列），是OLAP场景的核心存储选择。

| 分支 | 代表技术 | 基本原理 |
|------|----------|----------|
| 宽列存储 | Apache HBase | 基于BigTable模型，数据按RowKey排序存储在Region中，列族在存储层分离，支持数十亿行×百万列的稀疏表，LSM-Tree写入，适合随机读写 |
| 分布式列式库 | Apache Cassandra | 基于Dynamo+BigTable的混合架构，无中心节点（Gossip协议），一致性哈希分布数据，可调一致性级别（ONE/QUORUM/ALL），跨数据中心复制 |
| 高性能列式库 | ScyllaDB | 用C++重写的Cassandra兼容引擎，基于Seastar框架实现无共享（Share-Nothing）架构，每核独立运行，避免锁竞争，性能数倍于Cassandra |

### 3.5 图数据库

**目的**：以节点和边的方式存储实体及其关系，原生支持图遍历查询，适合社交网络、知识图谱、风控等关系密集型场景。

| 分支 | 代表技术 | 基本原理 |
|------|----------|----------|
| 原生图数据库 | Neo4j | 采用属性图模型（节点-关系-属性），原生图存储（免索引邻接），节点直接存储指向邻居的指针，图遍历无需全局索引，支持Cypher查询语言 |
| 分布式图数据库 | JanusGraph、NebulaGraph | JanusGraph基于HBase/Cassandra存储图数据，使用Elasticsearch做二级索引；NebulaGraph采用存储-计算分离架构，Raft协议保证一致性，支持nGQL查询 |
| 实时图分析 | TigerGraph | 基于MPP架构的分布式图数据库，原生并行图计算引擎，支持3步以内深度遍历的实时查询，内置GSQL图查询语言 |

### 3.6 时序数据库

**目的**：专门针对时间序列数据（带时间戳的指标数据）进行优化存储和查询，支持高效的时间范围查询、降采样和数据过期。

| 分支 | 代表技术 | 基本原理 |
|------|----------|----------|
| 专用时序引擎 | InfluxDB | 基于TSM（Time Structured Merge Tree）引擎，数据按时间分区，列式存储，自动压缩和降采样，支持Flux/InfluxQL查询语言 |
| 时序扩展引擎 | TimescaleDB | 基于PostgreSQL扩展，自动将时序表按时间切分为Chunk（Hypertable），保留PostgreSQL完整SQL能力，支持连续聚合（Continuous Aggregate） |
| 国产时序引擎 | TDengine | 专为IoT场景设计，一个数据采集点一张表，超级表（Super Table）管理同类型采集点，列式存储+双层分片，查询性能远超通用数据库 |

### 3.7 向量数据库

**目的**：存储和检索高维向量数据，支持近似最近邻（ANN）搜索，是AI/LLM应用（RAG、语义搜索、推荐）的核心基础设施。

| 分支 | 代表技术 | 基本原理 |
|------|----------|----------|
| 专用向量引擎 | Milvus | 基于ANN索引（IVF/HNSW/DiskANN等），将向量数据构建为索引结构，支持L2/内积/余弦相似度，存储-计算分离架构，支持十亿级向量检索 |
| 轻量向量引擎 | Qdrant、Chroma | Qdrant基于HNSW索引，Rust实现，支持过滤+向量混合查询；Chroma面向AI应用，内置Embedding函数，开箱即用 |
| 全托管向量服务 | Pinecone、Weaviate | Pinecone为全托管服务，自动管理索引和扩缩容；Weaviate支持向量+结构化混合搜索，内置多种向量化模块 |

### 3.8 关系型数据库（MPP）

**目的**：通过大规模并行处理（MPP）架构，将SQL查询分布到多个计算节点并行执行，实现TB-PB级结构化数据的高性能分析查询。

| 分支 | 代表技术 | 基本原理 |
|------|----------|----------|
| 无共享MPP | Greenplum | 基于PostgreSQL的MPP数据库，Master节点接收查询并生成执行计划，Segment节点并行执行，通过Interconnect进行数据重分布（Motion），支持行列混合存储 |
| 实时分析MPP | ClickHouse | 列式存储+向量化执行引擎，数据按Part组织，后台Merge合并，支持主键索引、跳数索引，单表查询性能极高，支持分布式表（Distributed Engine） |
| 嵌入式OLAP | DuckDB | 进程内嵌入式OLAP引擎，向量化执行+列式存储，零依赖、无需服务器，可直接查询CSV/Parquet/JSON等文件，适合本地数据分析、CI/CD测试和边缘场景 |
| 云原生MPP | Snowflake、Amazon Redshift | Snowflake基于云原生存储-计算分离架构，虚拟仓库（Virtual Warehouse）按需启停，独立扩缩容；Redshift基于列式存储的MPP，通过并发扩缩和Result Caching优化性能 |

---

## 4. 数据湖与数据湖仓

**目的**：以开放格式（Parquet/ORC/Avro）存储企业全部原始数据，支持多引擎读写，实现"写一次、读多次"的数据共享，是现代数据架构的核心存储层。

### 4.1 数据湖表格式

**目的**：在对象存储（S3/HDFS）上的文件集合之上增加表结构管理（Schema）、事务保证（ACID）和时间旅行（Time Travel）能力，使数据湖具备数据仓库的特性。

| 分支 | 代表技术 | 基本原理 |
|------|----------|----------|
| Iceberg | Apache Iceberg | 基于快照隔离的表格式，元数据分层（Metadata File → Manifest List → Manifest File → Data File），每次写入生成新快照，支持Schema演化、分区演化、行级删除，不绑定计算引擎 |
| Delta Lake | Databricks Delta Lake | 基于事务日志（_delta_log）的ACID表格式，每次写入生成JSON日志文件记录操作，支持OPTIMIZE压缩和Z-ORDER聚类，与Spark深度集成 |
| Hudi | Apache Hudi | 面对Upsert场景设计的表格式，支持Copy-On-Write（COW）和Merge-On-Read（MOR）两种表类型，MOR在读取时合并增量日志，写入性能更高，内置Compaction和Cleaning策略 |

### 4.2 数据湖平台

**目的**：提供数据湖的创建、管理、安全和治理的一体化平台，降低数据湖的使用门槛。

| 分支 | 代表技术 | 基本原理 |
|------|----------|----------|
| 全托管湖平台 | AWS Lake Formation、Databricks | Lake Formation提供数据湖的集中权限管理、数据目录和ETL编排；Databricks提供Notebook开发环境、Delta Lake表格式和Photon加速引擎的一体化平台 |
| 湖仓一体平台 | Apache Gravitino | 统一元数据目录，跨多个数据源（Hive/Iceberg/Kafka等）提供统一的元数据管理和访问控制（亦用于联邦元数据，见 13.2 节） |

### 4.3 元数据目录

**目的**：管理数据湖中所有数据集的Schema、分区、位置等元信息，使计算引擎能够发现和理解数据。

| 分支 | 代表技术 | 基本原理 |
|------|----------|----------|
| 集中式元数据服务 | Hive Metastore、AWS Glue Catalog | Hive Metastore作为元数据集中存储服务，使用关系型数据库存储表/分区/列定义，计算引擎通过Thrift API访问；Glue Catalog为云托管版本，无服务器架构 |
| 开放元数据标准 | Apache XTable（原OneTable） | 提供Iceberg/Delta/Hudi之间的元数据互转能力，同一份数据可被不同引擎以不同表格式读取 |

---

## 5. 数据计算与处理

**目的**：对采集和存储的数据进行清洗、转换、聚合、计算等操作，将其转化为有业务价值的信息，是大数据平台的核心计算能力。

### 5.1 批处理

**目的**：对大规模历史数据进行离线计算，适合对延迟不敏感但对吞吐量要求极高的场景（如T+1报表、模型训练数据准备）。

| 分支 | 代表技术 | 基本原理 |
|------|----------|----------|
| 内存计算引擎 | Apache Spark | 基于RDD/DataFrame/Dataset抽象，将数据尽可能缓存在内存中，DAG调度器将作业拆分为Stage，每个Stage内并行执行Task，支持SQL/Streaming/ML/Graph多库统一 |
| SQL批处理引擎 | Apache Hive、Apache Tez | Hive将HQL编译为MapReduce/Tez DAG执行计划，Tez通过DAG优化减少中间结果落盘，适合超大规模离线ETL |
| 云原生批处理 | AWS EMR、Google Dataproc、Azure Synapse | 云托管的大数据集群和批处理服务，按需创建和释放计算资源，自动扩缩容，与云存储深度集成；Synapse支持Spark和SQL双引擎的一体化分析 |

### 5.2 流处理

**目的**：对持续产生的实时数据流进行低延迟计算，支持实时监控、实时推荐、实时风控等毫秒-秒级响应场景。

| 分支 | 代表技术 | 基本原理 |
|------|----------|----------|
| 有状态流处理 | Apache Flink | 基于事件时间（Event Time）处理模型，通过Checkpoint机制（Chandy-Lamport算法变体）实现Exactly-Once语义，State Backend管理状态（RocksDB/Heap），支持窗口、CEP和侧输出 |
| 微批流处理 | Spark Structured Streaming | 将流数据切分为微批次（Micro-Batch），复用Spark SQL引擎处理，延迟约100ms级别，实现简单但延迟较高 |
| 嵌入式流处理 | Kafka Streams | 轻量级流处理库，无需独立集群，直接嵌入应用，基于Kafka Consumer/Producer实现，本地RocksDB存储状态，支持Exactly-Once |
| 统一批流编程模型 | Apache Beam | 提供统一的批流编程API（Pipeline→PCollection→PTransform），编写一次代码即可在多种Runner（Flink/Spark/Dataflow）上运行，CNCF毕业项目，支持Event Time和Watermark语义 |
| 原生流处理 | Apache Storm | 经典的流处理引擎，Tuple在Spout-Bolt拓扑中流动，保证At-Least-Once语义，Trident支持Exactly-Once |

### 5.3 交互式计算

**目的**：支持用户以SQL方式对大规模数据进行秒级交互式查询，适合数据探索、即席分析和自助BI场景。

| 分支 | 代表技术 | 基本原理 |
|------|----------|----------|
| MPP SQL引擎 | Trino（原Presto）、Apache Impala | Trino采用Coordinator-Worker架构，将SQL解析为逻辑计划→物理计划→Stage-Task，Worker并行执行，支持联邦查询跨多数据源；Impala原生运行在HDFS/Kudu上，通过LLVM编译查询为本地代码 |
| 预计算OLAP引擎 | Apache Kylin | 基于Cube预计算，将维度组合的所有聚合结果预先计算并存储为HBase中的KV对，查询时直接读取预计算结果，实现亚秒级响应 |
| 实时OLAP引擎 | Apache Druid | 列式分布式存储，数据按时间分片为Segment，实时节点（MiddleManager）摄入数据，历史节点（Historical）服务查询，支持时间序列和GroupBy聚合 |

### 5.4 图计算

**目的**：对大规模图结构数据（社交网络、知识图谱、路网等）进行迭代式计算（PageRank、最短路径、社区发现等）。

| 分支 | 代表技术 | 基本原理 |
|------|----------|----------|
| 批量图计算 | Apache Giraph、GraphX | Giraph基于Pregel模型，以Vertex为中心的BSP（Bulk Synchronous Parallel）迭代计算，每轮Superstep中各顶点处理消息并更新状态；GraphX基于Spark RDD的图计算库，使用VertexRDD和EdgeRDD表示图 |
| 图神经网络 | DGL、PyG（PyTorch Geometric） | DGL基于消息传递框架实现图神经网络，将GNN层编译为稀疏矩阵运算；PyG利用稀疏张量操作加速图卷积，支持数百种GNN模型 |

### 5.5 科学计算与数据处理

**目的**：提供数据清洗、特征工程、统计分析等能力，是数据科学家日常工作的基础工具。

| 分支 | 代表技术 | 基本原理 |
|------|----------|----------|
| 单机科学计算 | NumPy、Pandas | NumPy基于C/Fortran的N维数组，向量化运算避免Python循环；Pandas基于NumPy提供DataFrame抽象，支持索引、分组、透视等操作 |
| 分布式科学计算 | Dask、Vaex、Ray | Dask将Pandas/NumPy任务图切分为子任务并行执行；Vaex使用内存映射和零拷贝技术处理超大数据集；Ray提供分布式任务调度框架 |

---

## 6. 数据仓库与OLAP

**目的**：为企业提供统一的数据分析基础设施，支持结构化数据的高性能查询和多维分析，驱动业务决策。

### 6.1 企业级数据仓库

**目的**：按照主题域组织企业数据，支持复杂SQL查询、报表生成和数据挖掘，是BI分析的核心数据源。

| 分支 | 代表技术 | 基本原理 |
|------|----------|----------|
| 传统MPP数仓 | Teradata、Greenplum | 基于Shared-Nothing架构，数据按Hash/Range分布到各节点，通过并行扫描和Hash Join实现高性能查询，支持行列混合存储和分区 |
| 云原生数仓 | Snowflake、BigQuery、Redshift | Snowflake存储-计算分离，Virtual Warehouse独立扩缩容；BigQuery基于Dremel技术，无服务器架构，按查询量计费；Redshift基于列式MPP，RA3节点实现存储计算分离 |
| 开源数仓 | Apache Hive | 基于HDFS的数据仓库，将SQL编译为分布式执行计划，支持分区/分桶/存储格式优化，适合超大规模离线分析 |

### 6.2 OLAP引擎

**目的**：支持多维数据分析（上卷、下钻、切片、切块），提供亚秒级查询响应，是BI报表和自助分析的核心引擎。

| 分支 | 代表技术 | 基本原理 |
|------|----------|----------|
| 预计算OLAP | Apache Kylin | Kylin通过Cube预计算将维度组合的聚合结果物化，查询直接命中预计算结果（HBase/KV存储），实现亚秒级响应；适合维度固定的场景 |
| MPP实时OLAP | Apache Doris、StarRocks | 基于MPP分布式架构，向量化执行引擎+列式存储，支持实时数据导入和标准SQL查询，兼顾高性能与易用性，StarRocks兼容MySQL协议，支持多表物化视图 |
| 列式实时OLAP | ClickHouse、Apache Pinot | ClickHouse向量化执行+主键索引+跳数索引，单表查询极致性能；Pinot基于Segment的分布式存储，实时节点+离线节点混合架构，支持Upsert和星型Schema |
| 时序OLAP | Apache Druid | 面向时序数据的OLAP引擎，数据按时间分区为Segment，列式存储+位图索引，支持实时摄入和亚秒级聚合查询 |

### 6.3 湖仓一体（Lakehouse）

**目的**：融合数据湖的灵活性和数据仓库的性能，在同一平台上同时支持BI报表和机器学习工作负载。

| 分支 | 代表技术 | 基本原理 |
|------|----------|----------|
| 开源湖仓 | Apache Doris、StarRocks | 上述MPP引擎亦具备湖仓能力：通过External Catalog直接查询Iceberg/Hudi/Delta Lake等开放格式数据，统一管理内部表和外部表，实现湖仓联邦查询 |
| 商业湖仓 | Databricks Lakehouse | 基于Delta Lake表格式+Photon加速引擎，支持BI直连、流批一体和ML工作负载，Unity Catalog统一治理 |
| 轻量湖仓 | DuckDB | 嵌入式OLAP引擎，原生支持直接查询Parquet/Iceberg/Delta Lake文件，无需服务端部署，适合本地湖仓探索和CI/CD数据测试 |

---

## 7. 数据集成与ETL

**目的**：将数据从源系统提取（Extract）、转换（Transform）、加载（Load）到目标系统，是数据流转和加工的核心环节。

### 7.1 ETL/ELT工具

**目的**：提供可视化的数据集成开发环境，支持数据抽取、清洗、转换和加载的全流程管理。

| 分支 | 代表技术 | 基本原理 |
|------|----------|----------|
| 可视化ETL | Apache NiFi、Talend | NiFi基于DAG的拖拽式数据流设计，每个Processor完成一步操作，支持数据血缘追踪和背压控制；Talend基于Eclipse的图形化ETL开发，自动生成Java代码 |
| 现代ELT | dbt（data build tool） | 转换层工具，不移动数据，直接在数仓中编写SQL转换逻辑（Model），支持增量模型、测试、文档生成和血缘追踪，Git版本管理 |
| 开源数据集成 | Airbyte、SeaTunnel | Airbyte基于Connector目录，提供数百种连接器，支持增量同步和CDC；SeaTunnel（原Waterdrop）基于Spark/Flink引擎，高吞吐数据集成 |

### 7.2 数据管道

**目的**：构建可靠、可观测的数据流转管道，确保数据从源端到目标端的端到端质量。

| 分支 | 代表技术 | 基本原理 |
|------|----------|----------|
| 流式管道 | Kafka Connect + Debezium | Debezium捕获源端CDC事件，写入Kafka，Kafka Connect Sink将数据写入目标端，实现端到端低延迟数据管道 |
| 批量管道 | AWS Glue、Azure Data Factory、Apache Spark | AWS Glue提供托管ETL服务，自动生成PySpark代码；Data Factory为Azure云原生数据集成服务，支持拖拽式数据管道和多种连接器；Spark通过DataFrame API编写批量ETL逻辑 |

### 7.3 API集成

**目的**：通过API方式连接不同系统，实现数据交换和服务调用，是企业集成的关键模式。

| 分支 | 代表技术 | 基本原理 |
|------|----------|----------|
| API网关 | Kong、Apache APISIX | 基于Nginx/OpenResty的反向代理，统一管理API路由、认证、限流、日志，Kong通过插件机制扩展功能 |
| 集成平台 | MuleSoft、Apache Camel | MuleSoft提供API设计-实现-管理的全生命周期平台；Camel基于Enterprise Integration Patterns，通过DSL定义路由和转换规则 |

---

## 8. 数据编排与调度

**目的**：管理数据管道和工作流的执行顺序、依赖关系和资源分配，确保数据处理任务按时、按序、可靠地完成。

### 8.1 工作流调度

**目的**：定义和管理数据处理任务的DAG依赖关系，按照时间或事件触发执行，支持重试、告警和监控。

| 分支 | 代表技术 | 基本原理 |
|------|----------|----------|
| DAG调度器 | Apache Airflow | 基于DAG定义工作流，Python代码描述任务依赖，Scheduler解析DAG并调度Task到Executor执行，支持多种Executor（Local/Celery/Kubernetes），丰富的Operator生态 |
| 可视化调度器 | Apache DolphinScheduler | 基于DAG的可视化拖拽式工作流设计，去中心化架构，支持多租户，内置数十种任务插件，适合非开发人员使用 |
| 现代调度器 | Prefect、Dagster | Prefect基于Python函数+装饰器定义任务，动态DAG，支持混合执行；Dagster以Asset（数据资产）为中心，Software-Defined Asset定义数据血缘和依赖 |
| 传统调度器 | Azkaban、Oozie | Azkaban基于Web UI管理Hadoop作业流；Oozie基于XML定义Hadoop工作流，与Hadoop生态紧密集成 |

### 8.2 资源管理

**目的**：管理集群计算资源（CPU、内存、GPU）的分配和调度，确保多租户和多任务的资源隔离和公平共享。

| 分支 | 代表技术 | 基本原理 |
|------|----------|----------|
| 通用资源管理 | Kubernetes | 基于Pod的容器编排，通过Scheduler将Pod调度到Node，ResourceQuota限制命名空间资源，LimitRange约束Pod资源，支持GPU调度 |
| 大数据资源管理 | Apache YARN | ResourceManager全局资源管理，NodeManager管理单节点资源，ApplicationMaster管理单个应用，支持Capacity/Fair调度器 |
| 混合资源管理 | Apache Mesos | 双层调度框架，Mesos提供底层资源 offers，上层Framework（Spark/Chronos等）决定接受哪些资源并调度任务 |

---

## 9. 数据分析与BI

**目的**：将数据转化为可理解的信息和洞察，通过可视化、报表和交互式分析驱动业务决策。

### 9.1 BI工具

**目的**：提供数据查询、报表制作、仪表盘搭建的自助化工具，使业务人员能够独立进行数据分析。

| 分支 | 代表技术 | 基本原理 |
|------|----------|----------|
| 企业级BI | Tableau、Power BI、FineBI | Tableau基于VizQL将拖拽操作转化为SQL查询，支持实时连接和Extract模式；Power BI基于DAX表达式和VertiPaq引擎，与Microsoft生态深度集成；FineBI国产BI，支持中国式复杂报表 |
| 开源BI | Apache Superset、Metabase | Superset基于Flask+React，支持SQL Lab和可视化仪表盘，丰富的图表类型；Metabase面向非技术用户，自然语言查询（Question）自动生成SQL |
| 嵌入式BI | Looker、Redash | Looker基于LookML定义数据模型，生成SQL查询，支持嵌入式分析；Redash以SQL查询为核心，支持多种数据源和告警 |

### 9.2 数据可视化

**目的**：通过图表、地图、网络图等视觉元素直观呈现数据特征和规律，辅助人类理解复杂数据。

| 分支 | 代表技术 | 基本原理 |
|------|----------|----------|
| 编程式可视化 | D3.js、ECharts、Plotly | D3.js基于SVG的数据驱动文档，通过数据绑定操作DOM实现任意可视化；ECharts基于Canvas/SVG，丰富的图表类型和交互能力；Plotly基于WebGL支持大规模数据渲染 |
| 监控可视化 | Grafana | 基于Panel和Dashboard的可视化平台，支持数十种数据源（Prometheus/InfluxDB/MySQL等），内置告警系统，支持变量模板实现动态仪表盘 |
| 地理可视化 | Mapbox、Kepler.gl | Mapbox基于矢量瓦片和WebGL渲染地图；Kepler.gl基于Deck.gl的大规模地理数据可视化 |

### 9.3 统计分析

**目的**：运用统计学方法对数据进行描述性统计、推断统计和建模分析，发现数据中的规律和因果关系。

| 分支 | 代表技术 | 基本原理 |
|------|----------|----------|
| 统计计算语言 | R、SAS、SPSS | R语言拥有丰富的统计包（tidyverse/ggplot2/lme4），面向统计学家；SAS/SPSS为企业级统计软件，提供GUI和编程双模式 |
| Python统计库 | SciPy、Statsmodels、Pingouin | SciPy提供假设检验、分布函数等基础统计；Statsmodels提供回归分析、时间序列、方差分析等高级统计建模；Pingouin专注于常用统计检验的简洁API |

---

## 10. 机器学习与AI

**目的**：从数据中自动学习模式和规律，构建预测模型和智能应用，实现数据驱动的自动化决策。

### 10.1 机器学习框架

**目的**：提供模型训练、评估和推理的基础设施，支持从传统ML到深度学习的全流程开发。

| 分支 | 代表技术 | 基本原理 |
|------|----------|----------|
| 传统ML框架 | scikit-learn、XGBoost、LightGBM | scikit-learn基于NumPy/SciPy，提供统一的fit/predict API，涵盖分类/回归/聚类/降维等算法；XGBoost基于梯度提升决策树，列式直方图加速+正则化防过拟合；LightGBM基于直方图+Leaf-wise生长策略，训练速度更快 |
| 深度学习框架 | PyTorch、TensorFlow、JAX | PyTorch动态计算图+Eager执行，Python原生调试体验；TensorFlow静态图+XLA编译优化，部署生态完善；JAX基于函数式编程，自动微分+JIT编译+vmap向量化 |
| 分布式训练 | Horovod、DeepSpeed、Megatron-LM | Horovod基于Ring-AllReduce的分布式SGD，跨框架兼容；DeepSpeed提供ZeRO优化器（分片Optimizer State/Gradient/Parameter），支持千亿参数模型训练；Megatron-LM基于Tensor/Pipeline/Sequence并行训练超大Transformer |

### 10.2 MLOps

**目的**：将DevOps理念应用于机器学习，实现模型的全生命周期管理（开发→训练→部署→监控→迭代），提高模型交付效率和质量。

| 分支 | 代表技术 | 基本原理 |
|------|----------|----------|
| 实验追踪 | MLflow、Weights & Biases | MLflow Tracking记录每次实验的超参数、指标和产物（Artifact），支持模型注册和部署；W&B提供可视化实验对比和团队协作 |
| 编排平台 | Kubeflow、Vertex AI、SageMaker | Kubeflow基于Kubernetes的ML平台，Pipeline定义训练工作流；Vertex AI/SageMaker为云托管ML平台，提供AutoML、模型部署和监控 |
| 模型服务 | TensorFlow Serving、Triton Inference Server、vLLM | TF Serving支持模型版本管理和A/B测试；Triton支持多框架模型并发推理和动态批处理；vLLM专为LLM推理优化，PagedAttention管理KV Cache |

### 10.3 特征工程

**目的**：管理、存储和提供机器学习特征，确保训练和推理时特征的一致性，避免训练-服务偏差（Training-Serving Skew）。

| 分支 | 代表技术 | 基本原理 |
|------|----------|----------|
| 特征存储 | Feast、Tecton、Hopsworks | Feast定义特征视图（Feature View），将特征物化到在线存储（Redis/DynamoDB）供推理使用，离线存储（S3/BigQuery）供训练使用，保证线上线下特征一致性 |
| 特征计算 | Apache Beam、Flink SQL | Beam统一批流编程模型，计算批量/实时特征；Flink SQL以SQL定义实时特征计算逻辑 |

### 10.4 AutoML

**目的**：自动化机器学习流程中的特征工程、模型选择、超参数调优等环节，降低ML应用门槛。

| 分支 | 代表技术 | 基本原理 |
|------|----------|----------|
| 开源AutoML | Auto-sklearn、FLAML、Optuna | Auto-sklearn基于贝叶斯优化+元学习自动选择模型和超参数；FLAML基于经济型超参数优化，自动调整搜索预算；Optuna基于定义-by-run的API，支持剪枝和多目标优化 |
| 商业AutoML | H2O.ai、DataRobot | H2O.ai提供分布式AutoML，自动训练和堆叠多个模型；DataRobot自动化从数据准备到模型部署的全流程 |

### 10.5 大模型与LLM

**目的**：基于大规模预训练语言模型，实现文本生成、对话、摘要、翻译等通用AI能力，是当前AI产业的核心方向。

| 分支 | 代表技术 | 基本原理 |
|------|----------|----------|
| 基座模型 | GPT系列、LLaMA、Qwen、DeepSeek | 基于Transformer Decoder的自回归语言模型，通过Next-Token Prediction在大规模语料上预训练，学习语言的统计规律和世界知识 |
| LLM应用框架 | LangChain、LlamaIndex | LangChain提供Chain/Agent/Tool抽象，编排LLM调用和外部工具；LlamaIndex专注于RAG场景，提供文档解析、索引构建和检索生成管道 |
| RAG（检索增强生成） | 向量数据库 + LLM | 将用户查询先在向量数据库中检索相关文档片段，再将检索结果作为上下文注入LLM Prompt，减少幻觉并引入私有知识 |
| LLM微调 | LoRA、QLoRA、PEFT | LoRA在Transformer层注入低秩分解矩阵，仅训练少量参数实现高效微调；QLoRA在LoRA基础上使用4-bit量化进一步降低显存需求 |

---

## 11. 数据治理与安全

**目的**：确保数据的质量、一致性、可追溯性和安全性，是企业数据资产化和合规运营的基础保障。

### 11.1 数据质量

**目的**：持续监控和保障数据的准确性、完整性、一致性和时效性，防止脏数据影响下游分析和决策。

| 分支 | 代表技术 | 基本原理 |
|------|----------|----------|
| 数据验证框架 | Great Expectations、Pandera | Great Expectations基于Expectation定义数据质量规则（非空/唯一/范围/分布等），自动生成数据质量报告和文档；Pandera基于Schema定义DataFrame的列类型和约束 |
| 数据质量监控 | Apache Griffin、Deequ、Soda | Griffin基于Spark计算数据质量指标，支持批量和流式模式；Deequ（Amazon开源）基于Spark实现数据约束验证和指标计算；Soda使用YAML声明数据检查规则 |
| 异常检测 | Monte Carlo、Anomalo | 基于统计方法（Z-Score/IQR）和ML模型自动检测数据异常（体积异常/Schema变更/值分布偏移），主动告警 |

### 11.2 元数据管理

**目的**：管理数据的"数据"——表结构、字段含义、数据来源、负责人等，使数据可发现、可理解、可信任。

| 分支 | 代表技术 | 基本原理 |
|------|----------|----------|
| 数据目录 | DataHub、Apache Atlas、OpenMetadata | DataHub基于推送+拉取模式采集元数据，图数据库存储实体关系，支持搜索和血缘追踪；Atlas为Hadoop生态设计，支持分类和策略；OpenMetadata提供Schema/Lineage/Quality统一管理 |
| 数据发现 | Amundsen、Metacat | Amundsen基于Neo4j图数据库存储元数据关系，支持搜索和数据使用统计排名；Metacat提供统一的元数据API层，支持跨数据源Schema查询 |

### 11.3 数据血缘

**目的**：追踪数据从源头到终点的完整流转路径，支持影响分析（上游变更影响哪些下游）和根因分析（下游异常由哪个上游导致）。

| 分支 | 代表技术 | 基本原理 |
|------|----------|----------|
| 血缘追踪 | Apache Atlas、OpenLineage、Marquez | Atlas通过Hive Hook/Spark Listener自动捕获SQL执行产生的血缘关系；OpenLineage定义开放血缘标准，各工具（Airflow/Spark/dbt）推送血缘事件；Marquez收集和可视化血缘事件 |
| 代码级血缘 | SQL解析器（SqlGlot、Apache Calcite） | 解析SQL语句的AST（抽象语法树），提取表级和列级依赖关系，构建血缘图谱 |

### 11.4 数据安全与隐私

**目的**：保护数据免受未授权访问、泄露和滥用，满足GDPR、数据安全法等合规要求。

| 分支 | 代表技术 | 基本原理 |
|------|----------|----------|
| 访问控制 | Apache Ranger、Apache Sentry | Ranger基于策略的细粒度访问控制（行级/列级/脱敏），支持Hive/HBase/Kafka等组件；Sentry基于角色的访问控制（RBAC），与Hadoop生态集成 |
| 数据脱敏 | Protegrity、Informatica Masking | 静态脱敏：对存储数据中的敏感字段进行替换/遮盖/加密；动态脱敏：查询时实时对返回结果脱敏，原始数据不变 |
| 隐私计算 | 联邦学习、差分隐私、同态加密、安全多方计算 | 联邦学习：各方数据不出域，只交换模型梯度；差分隐私：在查询结果中添加校准噪声保护个体隐私；同态加密：在密文上直接计算；安全多方计算：多方协同计算不泄露各自输入 |
| 数据加密 | Vault、AWS KMS | Vault管理加密密钥的生命周期，提供动态密钥和加密即服务；KMS为云托管密钥管理服务，集成云存储和数据库加密 |

---

## 12. 数据监控与可观测性

**目的**：实时监控大数据平台的运行状态、性能指标和数据质量，快速发现和定位问题，保障平台稳定运行。

### 12.1 系统监控

**目的**：监控服务器、容器、数据库、消息队列等基础设施和服务的健康状态和性能指标。

| 分支 | 代表技术 | 基本原理 |
|------|----------|----------|
| 指标监控 | Prometheus、Datadog、Zabbix | Prometheus基于Pull模式采集指标（Exporter暴露/metrics端点），时序数据库存储，PromQL查询，AlertManager告警；Datadog为SaaS全栈监控；Zabbix基于Agent/SNMP采集，支持自动发现 |
| 可视化告警 | Grafana | 连接多种数据源，Dashboard+Panel展示指标，Alert Rule定义告警阈值，支持通知渠道（Email/Slack/PagerDuty） |

### 12.2 日志管理

**目的**：集中收集、索引和检索分布式系统的日志，支持故障排查和审计分析。

| 分支 | 代表技术 | 基本原理 |
|------|----------|----------|
| ELK Stack | Elasticsearch + Logstash + Kibana | Logstash采集和解析日志，Elasticsearch建立倒排索引存储，Kibana可视化查询和分析 |
| 云原生日志 | Fluentd/Fluent Bit + Loki | Fluent Bit轻量采集，Loki基于标签的日志索引（只索引元数据不索引全文），LogQL查询，存储成本远低于ES |
| 日志分析 | Splunk | 企业级日志分析平台，支持实时搜索、机器学习异常检测和IT运维分析 |

### 12.3 分布式追踪

**目的**：追踪分布式系统中请求的完整调用链路，定位性能瓶颈和故障节点。

| 分支 | 代表技术 | 基本原理 |
|------|----------|----------|
| 链路追踪 | Jaeger、Zipkin | 基于OpenTracing/OpenTelemetry标准，请求经过每个服务时生成Span，通过TraceID串联，可视化调用链和耗时分布 |
| 统一可观测 | OpenTelemetry | CNCF项目，统一Traces/Metrics/Logs三大信号的采集和导出标准，SDK自动埋点，Collector接收和转发 |

---

## 13. 数据虚拟化与联邦

**目的**：在不移动数据的前提下，提供统一的数据访问接口，实现跨数据源的联邦查询和逻辑数据集成。

### 13.1 数据虚拟化

**目的**：创建逻辑数据层，将多个异构数据源映射为统一的虚拟表，用户无需关心数据的物理位置和格式。

| 分支 | 代表技术 | 基本原理 |
|------|----------|----------|
| 企业数据虚拟化 | Denodo、Red Hat JBoss DV | Denodo基于查询下推（Pushdown）优化，将SQL操作尽量推送到源数据库执行，减少数据传输，支持缓存和物化视图加速查询 |
| 开源联邦查询 | Trino、Apache Drill | Trino通过Connector连接各数据源，Coordinator生成查询计划并下推到各数据源执行，Worker间Exchange传输中间结果 |

### 13.2 数据联邦

**目的**：实现跨数据源的联合查询，用户通过一条SQL同时查询多个数据源的数据。

| 分支 | 代表技术 | 基本原理 |
|------|----------|----------|
| SQL联邦引擎 | Trino、Spark SQL、Dremio | Trino支持跨Hive/MySQL/Kafka/Iceberg等多源联邦查询；Spark SQL通过DataSource V2 API支持联邦查询；Dremio在Trino基础上增加数据反射（Data Reflection）加速查询 |
| 联邦元数据 | Apache Gravitino | 统一管理跨Hive/Iceberg/Kafka等数据源的元数据，提供统一的目录和访问控制 |

---

## 14. 实时分析与决策

**目的**：在数据产生的瞬间完成分析并做出决策，支撑实时风控、实时推荐、实时定价等业务场景。

### 14.1 复杂事件处理（CEP）

**目的**：从事件流中检测符合特定模式的事件序列（如"3分钟内连续3次登录失败"），触发实时告警或业务动作。

| 分支 | 代表技术 | 基本原理 |
|------|----------|----------|
| 流式CEP | Apache Flink CEP | 基于NFA（非确定性有限自动机）模式匹配，定义Pattern序列（begin→next→followedBy→within），事件按时间顺序驱动状态转移，匹配成功触发回调 |
| 规则引擎 | Drools、Easy Rules | Drools基于Rete算法构建规则网络，将业务规则编译为推理网络，增量更新规则时只影响局部网络，适合复杂业务规则管理 |

### 14.2 实时推荐

**目的**：根据用户实时行为和上下文，毫秒级生成个性化推荐结果。

| 分支 | 代表技术 | 基本原理 |
|------|----------|----------|
| 实时特征+模型 | Redis + ML Model + Feature Store | 用户行为实时写入Redis，Feature Store提供预计算特征，ML模型在线推理，结果缓存返回，端到端延迟<100ms |
| 向量检索推荐 | Milvus/HNSW + Embedding | 将用户和物品编码为向量，通过ANN检索找到最相似的Top-K物品，支持实时向量更新和查询 |

### 14.3 实时风控

**目的**：在交易或操作发生的瞬间评估风险等级，决定放行/拦截/人工审核。

| 分支 | 代表技术 | 基本原理 |
|------|----------|----------|
| 流式风控 | Flink + 规则引擎 + ML模型 | Flink实时计算交易特征（频率/金额/设备指纹），规则引擎执行专家规则，ML模型评估风险概率，综合决策 |
| 图风控 | Neo4j/NebulaGraph + 图算法 | 构建交易/用户/设备关联图，通过图算法（社区发现/中心度/PageRank）识别团伙欺诈和异常关联 |

---

## 15. 数据开发平台与工具

**目的**：提供数据开发、测试、部署和协作的一体化环境，提高数据团队的工作效率和代码质量。

### 15.1 数据开发IDE

**目的**：为数据工程师和分析师提供专业的SQL/Python开发环境，支持代码补全、调试和执行。

| 分支 | 代表技术 | 基本原理 |
|------|----------|----------|
| 通用数据库IDE | DBeaver、DataGrip | DBeaver基于JDBC连接任意数据库，SQL编辑器+结果集查看+ER图；DataGrip（JetBrains）智能代码补全、重构和版本控制集成 |
| Notebook开发 | Jupyter、Apache Zeppelin | Jupyter基于Cell的交互式Notebook，支持Markdown+代码混合，Kernel架构支持多语言；Zeppelin支持多语言解释器和可视化图表 |

### 15.2 数据版本控制

**目的**：对数据集和模型进行版本管理，支持实验可复现和回滚。

| 分支 | 代表技术 | 基本原理 |
|------|----------|----------|
| 数据版本管理 | DVC（Data Version Control）、LakeFS | DVC基于Git管理数据版本，数据存储在远程（S3/GCS），Git只记录元数据和哈希，支持Pipeline定义和实验管理；LakeFS在对象存储上提供Git-like分支/合并/回滚操作 |
| 模型版本管理 | MLflow Model Registry、DVC | MLflow Model Registry管理模型版本和阶段（Staging/Production），支持模型审批和回滚 |

### 15.3 数据测试

**目的**：对数据管道的输出进行自动化验证，确保数据转换逻辑的正确性。

| 分支 | 代表技术 | 基本原理 |
|------|----------|----------|
| SQL测试 | dbt test、Great Expectations | dbt test定义Schema Test（unique/not_null/accepted_values）和Custom Test（SQL断言），在模型构建后自动运行；Great Expectations定义数据质量Expectation并生成验证报告 |
| 管道集成测试 | pytest + Spark/Dask | 编写Python测试用例，构造小数据集验证ETL逻辑，CI/CD流水线自动执行 |

---

## 附录：大数据技术全景架构图（文字版）

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           大数据技术全景架构                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐     │
│  │ 日志采集  │  │ CDC采集   │  │ 批量传输  │  │ 实时摄入  │  │ 网络采集  │     │
│  │Filebeat  │  │ Debezium │  │ Sqoop    │  │ NiFi     │  │ Scrapy   │     │
│  │Fluentd   │  │ Canal/OGG│  │ DataX    │  │Kafka C.  │  │Puppeteer │     │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘     │
│       │             │             │             │             │            │
│       └─────────────┴─────────────┼─────────────┴─────────────┘            │
│                                   ▼                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                    消息队列与事件流                                    │   │
│  │  Kafka │ Pulsar │ RocketMQ │ RabbitMQ │ NATS                        │   │
│  └────────────────────────────┬────────────────────────────────────────┘   │
│                               │                                            │
│       ┌───────────────────────┼───────────────────────┐                    │
│       ▼                       ▼                       ▼                    │
│  ┌─────────┐           ┌──────────┐           ┌──────────┐               │
│  │数据存储  │           │数据计算   │           │数据湖/仓  │               │
│  │HDFS     │           │Spark     │           │Iceberg   │               │
│  │Redis    │           │Flink     │           │Delta Lake│               │
│  │MongoDB  │           │Trino     │           │Hudi      │               │
│  │HBase    │           │Hive      │           │Hive MS   │               │
│  │Neo4j    │           │Kylin     │           │          │               │
│  │InfluxDB │           │Druid     │           │          │               │
│  │Milvus   │           │ClickHouse│           │          │               │
│  │Alluxio  │           │Beam     │           │          │               │
│  │DuckDB   │           │Doris    │           │          │               │
│  └────┬────┘           └────┬─────┘           └────┬─────┘               │
│       │                     │                      │                      │
│       └─────────────────────┼──────────────────────┘                      │
│                             ▼                                             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │数据集成   │  │数据编排   │  │数据分析BI │  │机器学习AI │  │实时决策   │   │
│  │NiFi      │  │Airflow   │  │Superset  │  │PyTorch   │  │Flink CEP │   │
│  │dbt       │  │DolphinSch│  │Tableau   │  │MLflow    │  │Drools    │   │
│  │Airbyte   │  │K8s/YARN  │  │Grafana   │  │Feast     │  │向量检索   │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
│                             │                                             │
│       ┌─────────────────────┼───────────────────────┐                     │
│       ▼                     ▼                       ▼                     │
│  ┌──────────┐  ┌──────────────────┐  ┌──────────────────┐               │
│  │数据治理   │  │数据监控与可观测性  │  │数据虚拟化与联邦   │               │
│  │Atlas     │  │Prometheus        │  │Trino             │               │
│  │Ranger    │  │Grafana           │  │Dremio            │               │
│  │Great Exp.│  │OpenTelemetry     │  │Denodo            │               │
│  │隐私计算   │  │ELK/Loki          │  │Gravitino         │               │
│  └──────────┘  └──────────────────┘  └──────────────────┘               │
│                                                                           │
│  ┌──────────────────────────────────────────────────────────────────┐     │
│  │                    数据开发平台与工具                               │     │
│  │ Jupyter │ DBeaver │ DVC │ dbt │ LakeFS │ DuckDB │ MLflow   │     │
│  └──────────────────────────────────────────────────────────────────┘     │
│                                                                           │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 技术选型决策参考

| 场景 | 推荐技术组合 | 核心理由 |
|------|-------------|----------|
| 离线数仓 | Hive + Spark + Airflow + Superset | 成熟稳定，生态完善，社区活跃 |
| 实时数仓 | Flink + Kafka + Doris/StarRocks + ClickHouse | 端到端低延迟，流批一体 |
| 数据湖仓 | Iceberg/Delta + Trino + Spark + dbt | 开放格式，多引擎互操作 |
| 实时风控 | Flink CEP + Kafka + Redis + Neo4j | 毫秒级决策，图关联分析 |
| AI/LLM应用 | PyTorch + Milvus + LangChain + vLLM | 全栈AI能力，向量检索+LLM推理 |
| 数据治理 | DataHub + Great Expectations + Ranger + OpenLineage | 元数据+质量+安全+血缘全覆盖 |
| 云原生大数据 | K8s + Spark on K8s + Flink on K8s + MinIO + Iceberg | 容器化部署，弹性伸缩 |
| 本地分析/边缘 | DuckDB + Parquet + Iceberg | 零依赖嵌入式分析，单机处理TB级数据 |
