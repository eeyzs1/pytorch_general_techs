# L1 项目评分 Rubric

> 适用考核项：机试（Hive SQL / Spark 编程 / 实战调优）+ 项目答辩（离线数仓 / 用户画像 / Airflow）

| 维度 | 分值 | 优秀标准 |
|------|------|----------|
| 理论基础（HDFS/MR/Hive/Spark） | 25 | 能准确解释 Block/副本/Shuffle/RDD 五大特性/外部表/数据倾斜，笔试 ≥ 80 分 |
| Hive SQL 与数据建模 | 20 | 建表语句规范（分区+Parquet+SNAPPY），JOIN/窗口函数/行转列正确，EXPLAIN 能分析分区裁剪与 Join 策略 |
| Spark 编程（RDD+DataFrame+SQL） | 20 | RDD/DataFrame/SQL 三套 API 均能正确使用，含 Cache/Broadcast 等优化意识，代码可运行且结果正确 |
| 实战调优 | 15 | 能从 Spark UI 诊断数据倾斜（Shuffle Read/GC 指标），给出加盐/Broadcast/AQE 至少 3 种方案及适用场景 |
| 项目答辩（技术深度+表达） | 20 | 架构图清晰、技术选型有理由、能回答"为什么"追问、有量化成果与反思 |

通过线：总分不低于 70，且理论基础不低于 20、三项机试全部通过、项目答辩不低于 14。

补考规则：笔试不通过 1 周后补考（最多 2 次）；机试不通过 1 周后补考（最多 2 次）；项目答辩不通过 2 周后补答辩（最多 1 次）。
