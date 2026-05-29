# L2 中级工程师：工程深化

> **阶段周期**：8周主线（第15-22周）+ 补充模块按需 | **总课时**：320h主线 + 85h补充 | **项目数**：3个核心项目 + 5个补充项目 | **目标角色**：大数据中级工程师

---

## 阶段目标

学员结业时能够：

1. **独立设计分布式数据管道**：从数据采集（CDC/Kafka）到流处理（Flink）到存储（ClickHouse）到可视化（Grafana）的端到端方案设计
2. **理解Kafka核心原理并配置生产级集群**：掌握零拷贝、ISR、Exactly-Once语义、事务机制，能够进行系统化性能调优
3. **使用Flink进行有状态流处理**：掌握DataStream API、Watermark机制、Checkpoint容错、Flink SQL CDC
4. **理解DDIA核心章节并能应用到实际架构设计**：覆盖Ch3-Ch12共10个章节，建立分布式系统的理论框架
5. **具备生产环境故障排查能力**：能够快速定位和解决Kafka、Flink、Spark、Hive等组件的常见故障
6. **掌握数据湖仓架构并完成Hive→Iceberg迁移**：理解Iceberg/Delta/Hudi三大表格式，能将传统Hive数仓迁移到湖仓架构
7. **实施数据治理体系**：能使用Great Expectations保障数据质量，使用DataHub管理元数据，使用OpenLineage追踪数据血缘

---

## 时间线与课程安排

| 周次 | 模块 | 内容 | 课时 | 核心产出 |
|------|------|------|------|----------|
| 第15-16周 | Kafka深入 | 架构原理 + Exactly-Once + 事务 | 40h | Kafka压测报告、事务Producer代码 |
| 第17-18周 | Flink流处理 | 核心API + Checkpoint + SQL CDC | 40h | Flink作业代码、CDC管道搭建 |
| 第19-22周 | DDIA精读 + 项目实战 | 读书会 + 3个综合项目 | 240h | 实时交易监控大屏、Kafka调优报告、故障排查SOP |
| 补充模块 | 数据湖仓实战 | Iceberg/Delta/Hudi实战 + 迁移项目 | 45h | Iceberg湖仓项目、迁移报告 |
| 补充模块 | 数据治理实操 | 数据质量 + 元数据 + 血缘 + 治理项目 | 40h | 数据治理平台、质量Dashboard |

### 每周节奏

```
周一至周四：上午理论(2h) + 下午动手(6h)
周五：项目阶段评审 + 集中答疑
周六：DDIA读书会（第19-22周）/ 技术分享会
周日：休息
```

---

## 项目清单

| 序号 | 项目名称 | 预计时长 | 技术栈 | 难度 |
|------|----------|----------|--------|------|
| 项目7 | 实时交易监控大屏 | 40h | MySQL→Kafka→Flink→ClickHouse→Grafana | ★★★★☆ |
| 项目8 | Kafka深度调优 | 20h | Kafka Producer/Consumer/Broker参数矩阵 | ★★★☆☆ |
| 项目9 | 数据管道故障排查手册 | 15h | 全栈故障模拟 + SOP编写 | ★★★☆☆ |
| DDIA读书会 | DDIA核心章节精读 | 持续12次 | DDIA全书12章 | ★★★★★ |
| 项目8.5 | 从Hive数仓迁移到Iceberg湖仓 | 25h | Spark+Iceberg+MinIO+Trino+Flink | ★★★★☆ |
| 项目9.5 | 数据治理平台搭建 | 20h | Great Expectations+DataHub+OpenLineage | ★★★★☆ |
| 项目A | 金融实时风控系统 | 40h | Kafka+Flink+规则引擎+实时决策 | ★★★★★ |
| 项目B | IoT设备监控与预测性维护 | 35h | Kafka+Flink+时序数据库+异常检测 | ★★★★☆ |
| 项目C | 广告实时竞价与归因分析 | 40h | Kafka+Flink+ClickHouse+流式Join | ★★★★★ |

---

## 前置要求

进入L2阶段前，学员必须通过L1结业考核，具备以下能力：

- 熟练搭建Hadoop/Spark/Hive分布式环境
- 能使用MapReduce和Spark完成数据处理
- 能使用Hive进行离线数据分析
- 理解HDFS和YARN的架构原理
- 完成过离线数仓构建（项目4）、用户画像系统（项目5）、Airflow编排（项目6）

---

## 学习资源

### 必读书籍

| 书名 | 作者 | 阅读重点 |
|------|------|----------|
| 《Kafka权威指南》 | Neha Narkhede | 第5-8章（Producer/Broker/Consumer内部原理） |
| 《基于Apache Flink的流处理》 | Fabian Hueske | 第1-8章（DataStream/状态/Checkpoint） |
| 《数据密集型应用系统设计》(DDIA) | Martin Kleppmann | 全书至少2遍，重点Ch3-Ch12 |
| 《大数据之路：阿里巴巴大数据实践》 | 阿里巴巴 | 全书，理解工业级实践 |

### 必读论文

| 序号 | 论文 | 年份 | 核心关注点 |
|------|------|------|------------|
| 1 | Kafka: a Distributed Messaging System | 2011 | 日志存储模型、Consumer Group |
| 2 | Resilient Distributed Datasets (Spark) | 2012 | RDD Lineage、窄/宽依赖 |
| 3 | Dynamo (Amazon) | 2007 | 最终一致性、Gossip协议 |
| 4 | Dremel | 2010 | 列式存储嵌套数据 |

---

## 实验室环境要求

### 本地开发环境

```
硬件最低配置:
  CPU: 8核以上（推荐16核）
  内存: 32GB以上（推荐64GB）
  磁盘: 1TB SSD

Docker Compose栈（一键启动）:
  Zookeeper × 3       端口2181
  Kafka Broker × 3    端口9092
  Flink JobManager     端口8081
  Flink TaskManager × 2
  MySQL 8.0           端口3306
  ClickHouse           端口8123/9000
  Grafana             端口3000
  Prometheus           端口9090
```

### 启动命令

```bash
cd docker/l2-environment
docker-compose up -d
```

### 验证命令

```bash
# 验证Kafka
kafka-topics.sh --list --bootstrap-server localhost:9092

# 验证Flink
curl http://localhost:8081/overview

# 验证ClickHouse
clickhouse-client --query "SELECT 1"

# 验证Grafana
curl http://localhost:3000/api/health
```

---

## 纪律要求

- **GitHub每日提交**：缺1天警告，连续缺3天启动淘汰
- **技术Blog每周1篇**：不交不进入下一周
- **DDIA读书笔记**：每次读书会前必须提交
- **每周复盘笔记**：记录"本周最大的1个收获 + 1个踩坑"
- **项目代码审查**：每个项目结项前必须通过Code Review

---

## 补充模块：跨行业实战

- [项目A：金融实时风控系统](./补充模块_跨行业实战/项目A_金融实时风控系统.md)
- [项目B：IoT设备监控与预测性维护](./补充模块_跨行业实战/项目B_IoT设备监控与预测性维护.md)
- [项目C：广告实时竞价与归因分析](./补充模块_跨行业实战/项目C_广告实时竞价与归因分析.md)

---

## 结业标准

参见 [结业考核/L2结业考核标准.md](结业考核/L2结业考核标准.md)

| 考核项 | 方式 | 通过标准 |
|--------|------|----------|
| Kafka调优 | 现场实操 | 给定Topic达到基准吞吐量×1.5 |
| Flink开发 | 现场编码 | 1小时内完成带Window+Checkpoint的Flink任务 |
| 故障排查 | 模拟演练 | 30分钟内定位并解决讲师注入的故障 |
| 架构讲解 | 投影问答 | 完整讲解项目7的架构设计，回答5个Why |
| DDIA答辩 | PPT+问答 | DDIA读书笔记分享，回答"与实际工作的映射" |

---

## 目录结构

```
L2_中级工程师/
├── README.md                                  ← 当前文件
├── 第15-16周_Kafka深入/
│   ├── 课时17_Kafka架构与核心概念.md          ← 零拷贝原理、压测命令
│   └── 课时18_Kafka_Exactly-Once与事务.md     ← 两阶段提交详解
├── 第17-18周_Flink流处理/
│   ├── 课时19_Flink核心概念.md                ← Watermark原理、DataStream代码
│   ├── 课时20_Flink_Checkpoint与容错.md       ← Checkpoint流程图、灾备演练
│   └── 课时21_Flink_SQL与CDC.md              ← Flink SQL CDC完整代码
├── 第19-22周_DDIA精读与项目/
│   ├── DDIA核心章节读书会.md                  ← 12章阅读指南、读书笔记模板
│   ├── 项目7_实时交易监控大屏.md              ← MySQL→Kafka→Flink→ClickHouse→Grafana
│   ├── 项目8_Kafka深度调优.md                 ← 参数矩阵实验、故障演练4场景
│   └── 项目9_数据管道故障排查手册.md          ← 10个故障场景SOP
├── 补充模块_数据湖仓实战/
│   ├── 课时22_Iceberg与Delta_Lake实战.md      ← 湖仓表格式对比+实战
│   └── 项目8.5_从Hive数仓迁移到Iceberg湖仓.md ← Hive→Iceberg完整迁移
├── 补充模块_数据治理实操/
│   ├── 课时23_数据质量与元数据管理.md          ← GE+DataHub+OpenLineage
│   └── 项目9.5_数据治理平台搭建.md             ← 质量体系+元数据+血缘+安全
├── 补充模块_跨行业实战/
│   ├── 项目A_金融实时风控系统.md               ← Kafka+Flink+规则引擎+实时决策
│   ├── 项目B_IoT设备监控与预测性维护.md         ← Kafka+Flink+时序数据库+异常检测
│   └── 项目C_广告实时竞价与归因分析.md          ← Kafka+Flink+ClickHouse+流式Join
└── 结业考核/
    └── L2结业考核标准.md                      ← 考核标准与评分细则
```
