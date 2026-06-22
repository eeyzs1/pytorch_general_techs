# L2 项目评分 Rubric

> 适用考核项：Kafka 调优 / Flink 开发 / 故障排查 / 架构讲解 / DDIA 答辩

| 维度 | 分值 | 优秀标准 |
|------|------|----------|
| Kafka 调优（现场实操） | 20 | 吞吐达到基准 ×1.5（≥300K rec/s），P99 延迟不恶化（< 基准 ×1.2），能解释 batch.size/linger.ms/acks/compression 原理，输出调优报告 |
| Flink 开发（现场编码） | 20 | 代码可编译运行，正确实现 EventTime+Watermark+Window+Checkpoint，含 SideOutput 处理迟到数据，RocksDB StateBackend 配置合理 |
| 故障排查（模拟演练） | 20 | 30 分钟内定位根因并解决，遵循五步法（观察→日志→定位→修复→验证），使用正确工具（Spark UI/Flink UI/EXPLAIN/fsck），提出预防措施 |
| 架构讲解（5 个 Why） | 20 | 白板画出项目 7 完整架构图，数据链路延迟说清楚，5 个 Why 回答有深度（Kafka vs Pulsar/Flink vs Spark Streaming/ClickHouse vs Doris/CDC vs SELECT 等） |
| DDIA 答辩（PPT+问答） | 20 | 用自己的话解释核心概念（非背诵），每个概念有实际技术映射，有批判性思考，能举出"因读 DDIA 改变的架构决策"真实案例 |

通过线：5 项全部通过（每项 ≥ 14 分），总分 ≥ 70。

等级：A（≥90，直通 L3+奖学金）/ B（≥80，升 L3）/ C（≥70，升 L3 需补强）/ D（≥60，补考）/ F（<60，重修）。
GitHub 贡献度要求：L2 阶段累计提交 ≥ 120 次（一票否决）。
