# L1 初级工程师：大数据入门

> **阶段定位**：从编程基础过渡到大数据技术栈，掌握Hadoop生态核心组件和Spark计算引擎，具备构建离线数仓的工程能力。
>
> **教学理念**：不做PPT讲师，做项目教练。每个技术点按照"感性认识→动手搭建→原理深挖→实战项目"四步走。

---

## 阶段目标

学员结业时能够：

1. **搭建Hadoop/Spark/Hive分布式环境**：能独立使用Docker Compose部署3节点集群
2. **使用MapReduce和Spark完成数据处理**：能写出生产级的WordCount、PV/UV统计、TopN等程序
3. **使用Hive进行离线数据分析**：能设计分区表、编写复杂HiveQL查询
4. **理解HDFS和YARN的架构原理**：能手绘HDFS读写流程图，解释NameNode/DataNode交互
5. **构建完整的离线数仓**：能独立完成ODS→DWD→DWS→ADS四层数仓设计
6. **具备Spark性能调优基础能力**：能诊断数据倾斜并给出解决方案

---

## 时间线与课程安排

| 周次 | 模块 | 课时 | 学时 | 核心内容 |
|------|------|------|------|----------|
| 第7-8周 | Hadoop生态基础 | 课时11-13 | 48h | HDFS原理、MapReduce编程、Hive数据仓库 |
| 第9-10周 | Spark核心 | 课时14-16.5 | 48h | RDD核心原理、Spark SQL/DataFrame、性能调优、[课时16.5：现代OLAP引擎入门](./第9-10周_Spark核心/课时16.5_现代OLAP引擎入门.md) |
| 第11-14周 | 项目实战 | 项目4-6 | 96h | 离线数仓构建、用户画像系统、Airflow编排 |
| 第14周末 | 结业考核 | - | 8h | 笔试 + 机试 + 项目答辩 |

> **总课时**：约200小时（含课堂授课48h + 实验操作72h + 项目开发80h）

---

## 技术栈总览

```yaml
核心框架:
  - Hadoop 3.x: HDFS + YARN + MapReduce
  - Hive 3.x: 数据仓库（Hive on Tez）
  - Spark 3.x: 通用计算引擎（PySpark为主，辅以Spark SQL）
  - Airflow 2.x: 工作流调度

辅助工具:
  - Docker + Docker Compose: 环境部署
  - MySQL 8.0: 关系型数据源
  - Sqoop: 数据导入导出
  - Git + GitHub: 版本管理与代码提交
  - ClickHouse: OLAP列式数据库
  - DuckDB: 嵌入式分析引擎
  - StarRocks: MPP OLAP引擎

编程语言:
  - Python 3.10+: 主要开发语言（PySpark）
  - Java 8+: MapReduce开发
  - SQL/HiveQL: 数据分析核心语言
  - Shell/Bash: 运维脚本

存储格式:
  - Parquet: 列式存储（生产标准）
  - ORC: Hive优化格式
  - CSV/JSON: 数据交换格式
```

---

## 前置要求

进入L1阶段前，学员必须完成L0阶段并通过结业考核：

- Python编程：能独立完成数据处理脚本
- SQL能力：熟练掌握JOIN、子查询、窗口函数
- Linux基础：能在命令行环境下操作
- Git基础：掌握分支管理、PR流程

---

## 学习路径与成长地图

```
L0(编程基础) ──→ L1(大数据入门) ──→ L2(工程深化) ──→ L3(技术深度) ──→ L4(架构师) ──→ L5(CTO)

L1阶段内部路径:
  第7-8周             第9-10周             第11-14周
  ┌──────────┐       ┌──────────┐       ┌──────────────┐
  │ Hadoop   │  ──→  │  Spark   │  ──→  │   项目实战    │
  │ 生态基础 │       │  核心引擎 │       │  离线数仓    │
  │          │       │          │       │  用户画像    │
  │ HDFS     │       │ RDD      │       │  Airflow     │
  │ MapReduce│       │ DataFrame│       │              │
  │ Hive     │       │ 性能调优 │       │              │
  │          │       │ OLAP入门 │       │              │
  └──────────┘       └──────────┘       └──────────────┘
       ↓                  ↓                    ↓
  感性认识阶段        原理深挖阶段         实战项目阶段
```

---

## 关键交付物

| 序号 | 交付物 | 对应课时 | 描述 |
|------|--------|----------|------|
| 1 | HDFS部署文档 | 课时11 | Docker Compose部署步骤 + Shell操作记录 |
| 2 | MapReduce作业 | 课时12 | WordCount + TopN + Join的Java源码 |
| 3 | Hive练习题集 | 课时13 | 20道HQL练习（建表/分区/JOIN/窗口函数） |
| 4 | Spark RDD练习 | 课时14 | PV/UV统计 + TopN + Join的PySpark实现 |
| 5 | Spark SQL分析 | 课时15 | 数据分析全流程（DataFrame API + SQL） |
| 6 | 性能调优报告 | 课时16 | 倾斜处理3种方案对比 + 实验数据 |
| 7 | 离线数仓项目 | 项目4 | ODS→DWD→DWS→ADS完整代码 + 文档 |
| 8 | 用户画像系统 | 项目5 | 标签体系文档 + Spark标签脚本 |
| 9 | Airflow DAG | 项目6 | 完整ETL调度DAG + 运行截图 |
| 10 | 结业答辩PPT | 考核 | 20分钟项目答辩 + 5分钟问答 |
| 11 | OLAP引擎练习 | 课时16.5 | ClickHouse建表+聚合查询+DuckDB分析 |
| 12 | 技术写作与协作沟通 | 补充模块_软技能 | 技术文档规范+跨团队协作实践+沟通技巧 |

---

## 补充模块：软技能

- [技术写作与协作沟通](./补充模块_软技能/技术写作与协作沟通.md)

---

## 每日学习节奏

```
上午(3h) — 理论学习 + 教师演示
  09:00-10:30  核心概念讲解
  10:30-12:00  代码Demo + 互动问答

下午(5h) — 动手实验 + 项目开发
  13:30-15:30  实验任务（个人完成）
  15:30-17:00  项目开发（小组协作）
  17:00-18:30  代码Review + 答疑

晚上(2h) — 自学巩固
  20:00-22:00  课后作业 + 技术Blog + GitHub提交
```

---

## 纪律要求（严格执行）

- **GitHub每日提交**：缺1天警告，连续缺3天启动退出流程
- **技术Blog每周1篇**：记录本周最大的1个收获 + 1个踩坑
- **迟到惩罚**：第2次开始，每次罚讲1小时技术分享
- **代码抄袭**：发现1次警告，发现2次淘汰
- **项目答辩**：不通过需补答辩，补答辩不通过则留级

---

## 环境准备

```yaml
硬件要求:
  CPU: 8核以上
  内存: 32GB（Docker集群至少需要16GB可用）
  磁盘: 500GB SSD

软件环境:
  - Docker Desktop 24.0+
  - VS Code + Python/PySpark插件
  - MySQL 8.0 Workbench
  - Git 2.40+
  - JDK 8/11（MapReduce编译需要）

一键启动大数据集群:
  docker-compose -f docker-compose-bigdata.yml up -d

服务清单:
  hadoop-namenode:1   端口9870  (HDFS Web UI)
  hadoop-datanode:3   端口9864
  hive-metastore:1    端口9083
  hive-server2:1      端口10000
  spark-master:1      端口8080  (Spark Web UI)
  spark-worker:2      端口8081
  mysql:1             端口3306
  airflow:1           端口8080
```

---

## 升L2条件

1. **GitHub贡献度**：L1阶段累计代码提交 ≥ 80次
2. **技术Blog**：至少6篇（每2周1篇）
3. **结业考核通过**：笔试 ≥ 80分 + 机试通过 + 项目答辩合格
4. **项目交付**：项目4/5/6全部完成并过审