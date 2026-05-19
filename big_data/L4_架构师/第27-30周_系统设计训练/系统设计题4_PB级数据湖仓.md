# 系统设计题4：支持PB级数据的数据湖仓系统

## 一、需求分析

### 1.1 功能性需求

| 维度 | 需求详情 |
|------|----------|
| **数据规模** | 当前500TB，年增长200TB，3年内达到PB级 |
| **数据类型** | 结构化（数据库表）、半结构化（JSON/XML/Protobuf日志）、非结构化（图片/视频元数据、文档） |
| **写入模式** | 批量写入（T+1数据管道）、流式写入（CDC实时同步）、Upsert/Merge（数据修正） |
| **查询模式** | BI报表查询、Ad-hoc自助分析、数据科学（Python/SQL交互式）、ML训练数据导出 |
| **数据治理** | Schema演化管理、数据血缘、数据质量监控、数据发现（Catalog） |
| **多引擎支持** | Spark/Flink/Trino/Python等不同计算引擎共享同一份数据 |

### 1.2 非功能性需求

```
性能:
  - 批量写入吞吐: >10GB/s
  - Trino交互查询: P95 < 30秒 (100GB级别扫描)
  - Spark ETL任务: 日跑批窗口 < 4小时

可用性:
  - 元数据服务: 99.99%
  - 数据读写: 99.9%

一致性:
  - ACID事务保证（不会读到中间状态的写入）
  - 时间旅行（可回溯到任意时间点的表快照）
  - Schema演化保证向后兼容

成本:
  - 存储成本：通过冷热分层降低TCO
  - 计算成本：通过弹性资源减少闲置浪费
```

---

## 二、容量估算

### 2.1 数据增长

```
当前数据量: 500TB
年增长率: 40% (200TB/年)

3年投影:
  Year 1: 500TB + 200TB = 700TB
  Year 2: 700TB + 280TB = 980TB
  Year 3: 980TB + 392TB = ~1.4PB

存储分层 (3年后):
  热数据 (近7天, 10%): 140TB × $0.1/GB/月 = $14,000/月
  温数据 (7-90天, 30%): 420TB × $0.03/GB/月 = $12,600/月
  冷数据 (>90天, 60%): 840TB × $0.01/GB/月 = $8,400/月
  ─────────────────────────────────────────────
  月存储成本: ~$35,000
  年存储成本: ~$420,000
```

### 2.2 计算资源

```
日常计算负载:
  Spark ETL: 200个任务，平均20核40GB，并发20个
  → 400核 800GB常驻

  Trino交互查询: 50并发，平均每查询使用8核16GB
  → 400核 800GB (弹性)

  ML训练: 定期（每周），100核200GB
  → 弹性分配

总日常计算: ~800核 1.6TB内存
峰值（大促+月末）: ×2 = 1600核
```

---

## 三、候选方案对比

### 方案A：Apache Iceberg + Trino + Spark (纯开源方案)

```
┌─────────────────────────────────────────────────────────┐
│                   计算引擎层                             │
│      Spark (ETL)  │  Trino (查询)  │  Flink (流)       │
└────────────────────────┬────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────┐
│                Iceberg 表格式层                          │
│   ┌─────────────────────────────────────────────┐      │
│   │  元数据层 (Metadata)                         │      │
│   │  - 表Schema + 分区信息                       │      │
│   │  - 快照列表 (Snapshot)                       │      │
│   │  - 文件清单 (Manifest)                       │      │
│   ├─────────────────────────────────────────────┤      │
│   │  数据层 (Data)                               │      │
│   │  - Parquet/ORC/Avro 数据文件                │      │
│   └─────────────────────────────────────────────┘      │
└────────────────────────┬────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────┐
│              存储层 (S3 / HDFS / MinIO)                 │
│   热数据: SSD │ 温数据: HDD │ 冷数据: 归档存储          │
└─────────────────────────────────────────────────────────┘
```

**优点**:
- Iceberg是Apache顶级项目，社区活跃，贡献者多（Netflix/Apple/AWS等大厂参与）
- 真正的开放表格式，多引擎共享（Spark/Flink/Trino/Presto/Hive/Impala）
- ACID事务 + 时间旅行 + 分区演化 + Schema演化
- 隐藏式分区（Partition Evolution），无需重写历史数据即可变更分区策略
- 对象存储友好（S3/HDFS/MinIO均可）

**缺点**:
- Upsert/Merge性能不如Hudi（Copy-on-Write模式下需重写整个文件）
- 小文件问题需要后台Compaction
- Trino查询需要Metastore + Iceberg Catalog两层元数据
- 分区演化功能虽强但操作需谨慎，错误的演化可能影响查询性能

### 方案B：Apache Hudi + Spark + Flink (CDC优先方案)

```
┌─────────────────────────────────────────────────────────┐
│                   计算引擎层                             │
│      Spark (批量)  │  Flink (流写入)  │  Trino (查询)  │
└────────────────────────┬────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────┐
│                  Hudi 表格式层                           │
│   ┌─────────────────────────────────────────────┐      │
│   │  时间线 (Timeline)                           │      │
│   │  - Commit/Deltacommit/Clean/Rollback        │      │
│   ├─────────────────────────────────────────────┤      │
│   │  索引 (Index)                                │      │
│   │  - Bloom Filter / HBase / Bucket Index      │      │
│   ├─────────────────────────────────────────────┤      │
│   │  Copy-on-Write │ Merge-on-Read             │      │
│   └─────────────────────────────────────────────┘      │
└────────────────────────┬────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────┐
│                   存储层 (HDFS / S3)                     │
└─────────────────────────────────────────────────────────┘
```

**优点**:
- Upsert/Merge能力业界最强（MoR模式增量写入性能极佳）
- 针对CDC场景深度优化（增量Pipeline、Changelog模式）
- 内置索引（Bloom Filter/HBase/Bucket Index）加速Upsert
- 支持Incremental Query（只读取变更数据）
- 数据压缩和Clustering（自动优化文件大小和布局）

**缺点**:
- 强依赖HDFS语义（S3上的性能不如Iceberg，List操作开销大）
- 多引擎支持不如Iceberg（Flink支持完善，Trino通过Hive Sync间接支持）
- 表服务（Table Service）需要独立进程运行Compaction/Cleaning
- MoR模式查询性能（需Merge Base+Log文件）不如CoW

### 方案C：Delta Lake + Databricks (商业生态方案)

```
┌─────────────────────────────────────────────────────────┐
│              Databricks / Spark 生态                     │
│   Photon引擎 │ Delta Live Tables │ Unity Catalog        │
└────────────────────────┬────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────┐
│                Delta Lake 表格式                         │
│   ┌─────────────────────────────────────────────┐      │
│   │  事务日志 (_delta_log/)                      │      │
│   │  - JSON 事务记录                            │      │
│   │  - Checkpoint (Parquet)                     │      │
│   ├─────────────────────────────────────────────┤      │
│   │  数据文件 (Parquet)                          │      │
│   │  - 自动Optimize + Z-ordering               │      │
│   └─────────────────────────────────────────────┘      │
└────────────────────────┬────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────┐
│                   存储层 (S3 / ADLS / HDFS)              │
└─────────────────────────────────────────────────────────┘
```

**优点**:
- 与Databricks/Spark生态深度集成，开发体验最好
- Delta Live Tables简化Pipeline定义和运维
- Photon引擎（C++向量化）显著提升查询性能
- Unity Catalog提供统一的数据治理体验
- Auto Optimize + Z-ordering自动优化文件布局

**缺点**:
- 多引擎支持弱：非Spark引擎（Trino/Flink）支持不如Iceberg
- 依赖Databricks Runtime（开源版Delta Lake功能有限）
- 供应商锁定风险（与Databricks平台深度耦合）
- 商业版本成本高（DBU按使用量计费）

---

## 四、方案对比总结

| 维度 | 方案A (Iceberg) | 方案B (Hudi) | 方案C (Delta Lake) |
|------|----------------|-------------|-------------------|
| 多引擎支持 | ★★★★★ | ★★★☆☆ | ★★★☆☆ |
| Upsert/Merge性能 | ★★★☆☆ | ★★★★★ | ★★★★☆ |
| 对象存储兼容性 | ★★★★★ | ★★★☆☆ | ★★★★☆ |
| 查询性能 | ★★★★☆ | ★★★★☆ | ★★★★★ |
| 分区演化 | ★★★★★ | ★★☆☆☆ | ★★★☆☆ |
| 社区活跃度 | ★★★★★ | ★★★★☆ | ★★★★★ |
| 商业锁定风险 | ★★★★★ (无) | ★★★★★ (无) | ★★☆☆☆ |
| 运维复杂度 | ★★★★☆ | ★★★☆☆ | ★★★★☆ |

---

## 五、最终选择：方案A（Apache Iceberg）

### 选择理由

**1. 多引擎共享是核心需求**
PB级数据湖仓的核心理念是"一份数据，多引擎计算"。Iceberg作为真正的开放表格式，被Spark/Flink/Trino/Presto/Hive/Impala/Doris/StarRocks等几乎所有主流引擎原生支持。Hudi和Delta Lake在多引擎支持上存在明显的短板。

**2. 对象存储原生优化**
我们的存储层计划使用MinIO（自建对象存储）+ 冷数据归档到阿里云OSS。Iceberg从设计之初就针对对象存储做了大量优化（如规避S3的最终一致性、Manifest文件减少List操作等）。Hudi对HDFS语义有强依赖，在纯对象存储环境下的表现不如Iceberg。

**3. 分区演化能力**
PB级数据经过3年积累，分区策略必然需要调整（如从按月分区改为按天分区，或增加业务维度作为子分区）。Iceberg的隐藏式分区（Partition Evolution）可以在不重写历史数据的情况下变更分区策略，这是Hudi和Delta Lake不原生支持的。

**4. 社区活力**
Iceberg被Netflix/Apple/AWS/Tencent等大厂广泛采用，Apache顶级项目，社区治理成熟。2023年Google也宣布BigLake支持Iceberg格式。长期来看，Iceberg最有可能成为数据湖仓的事实标准。

**5. 组合方案覆盖Hudi的优势**
对于Upsert需求较重的实时链路，可以使用Flink + Hudi（方案B）作为写入层，定期Compaction后转为Iceberg格式供多引擎查询。两者不是互斥关系。

### ADR记录

```markdown
# ADR-005: 数据湖仓表格式选择 Apache Iceberg

## 状态
已采纳

## 决策
以Apache Iceberg为核心表格式构建数据湖仓。对于高Upsert需求的实时链路，可选Hudi作为写入中间层。

## 理由
1. 多引擎共享是核心需求，Iceberg被几乎所有主流引擎原生支持
2. 对象存储兼容性最优，适配MinIO + OSS的存储架构
3. 分区演化能力是PB级数据3年生命周期的刚需
4. Apache顶级项目，社区治理成熟，最可能成为行业标准
5. Hudi可在特定场景（CDC实时Upsert）作为补充方案

## 后果
- 正面：多引擎共享、对象存储友好、分区演化灵活
- 负面：Upsert性能不如Hudi，需后台Compaction管理
- 风险：分区演化操作需严格测试，避免影响查询性能

## 替代方案
- Hudi：Upsert强但多引擎支持和对象存储兼容性不足
- Delta Lake：开发体验好但有供应商锁定风险
```

---

## 六、核心架构设计

### 6.1 Iceberg表结构设计

```sql
-- 订单事实表 (Iceberg v2格式)
CREATE TABLE lakehouse.dwd.orders (
    order_id BIGINT NOT NULL,
    user_id BIGINT NOT NULL,
    product_id BIGINT NOT NULL,
    amount DECIMAL(20,2),
    status STRING,
    channel STRING,
    event_time TIMESTAMP,
    dt DATE
) USING iceberg
PARTITIONED BY (months(dt), bucket(16, user_id))
TBLPROPERTIES (
    'format-version' = '2',
    'write.format.default' = 'parquet',
    'write.parquet.compression-codec' = 'zstd',
    'write.metadata.delete-after-commit.enabled' = 'true',
    'write.metadata.previous-versions-max' = '10',
    'history.expire.max-snapshot-age-ms' = '604800000'
);

-- 时间旅行查询（回溯到3天前的数据）
SELECT * FROM lakehouse.dwd.orders
FOR SYSTEM_TIME AS OF TIMESTAMP '2024-01-15 00:00:00'
WHERE dt = '2024-01-14';
```

### 6.2 冷热数据分层

```
数据热度生命周期:
  
  Hot (近7天):
    存储: MinIO NVMe SSD集群
    格式: Parquet (zstd压缩)
    Iceberg分支: main
    查询: Trino + Spark直接查询

  Warm (7-90天):
    存储: MinIO HDD集群
    格式: Parquet (zstd压缩, 更高压缩级别)
    Iceberg分支: main

  Cold (>90天):
    存储: 阿里云OSS归档存储
    格式: Parquet (gzip高压缩)
    Iceberg分支: cold_archive
    查询: 需先解冻（OSS取回到MinIO），延迟增加

迁移策略:
  - 每日定时任务：dt < date_sub(CURRENT_DATE, 7) → 从Hot迁移到Warm
  - 每周定时任务：dt < date_sub(CURRENT_DATE, 90) → 从Warm迁移到Cold
  - Iceberg的expire_snapshots + orphan文件清理
```

### 6.3 Catalog架构

```
Catalog层次:
  
  Hive Metastore (元数据持久化)
    ├── lakehouse.ods    (原始数据层)
    ├── lakehouse.dwd    (明细数据层)
    ├── lakehouse.dws    (汇总数据层)
    ├── lakehouse.ads    (应用数据层)
    └── lakehouse.ml     (ML特征/训练数据)

  Trino Iceberg Catalog配置:
    connector.name=iceberg
    hive.metastore.uri=thrift://hive-metastore:9083
    iceberg.catalog.type=hive
    iceberg.catalog.warehouse=s3://lakehouse/

  Spark配置:
    spark.sql.catalog.lakehouse=org.apache.iceberg.spark.SparkCatalog
    spark.sql.catalog.lakehouse.type=hive
```

---

## 七、配套工具选型

### 7.1 数据治理

```
数据发现: Amundsen / DataHub
  - 表搜索 + 列搜索
  - 数据血缘可视化
  - 使用频率和热度统计

数据质量: Great Expectations / Deequ
  - 表行数校验
  - NULL值比例
  - 数值范围检查
  - Schema一致性检查

Schema管理: Apache Atlas / Schema Registry
  - Schema注册和版本管理
  - 向前/向后兼容性检查
  - Schema变更通知
```

### 7.2 小文件Compaction

```sql
-- Iceberg RewriteDataFiles (Spark任务, 每天凌晨执行)
CALL lakehouse.system.rewrite_data_files(
    table => 'dwd.orders',
    strategy => 'binpack',
    options => map(
        'target-file-size-bytes', '134217728',  -- 128MB目标
        'min-file-size-bytes', '67108864',       -- 最小64MB
        'max-file-size-bytes', '268435456'       -- 最大256MB
    )
);

-- 删除孤儿文件
CALL lakehouse.system.remove_orphan_files(
    table => 'dwd.orders',
    older_than => TIMESTAMP '2024-01-15 00:00:00'
);
```

---

## 八、监控与告警

```
数据管道:
  - 每日数据增量（告警：低于历史均值的50% 或高于200%）
  - Iceberg Snapshot创建延迟
  - Compaction任务执行时间

存储:
  - 各层存储使用量（Hot/Warm/Cold）
  - 小文件数量（告警：> 10000/表）
  - 孤儿文件大小（定期清理）

查询:
  - Trino查询P95延迟
  - 全表扫描查询告警（无分区过滤）
  - 慢查询Top 10

治理:
  - 表数量增长趋势
  - Schema变更频率
  - 未使用的表（30天无查询）
```