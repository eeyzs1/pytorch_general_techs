# L3 高级工程师：技术深度

> **阶段定位**：从"会用框架"到"深入源码"，从"写代码"到"做技术决策"
>
> **周期**：20周 | **课时**：400h | **项目数**：2个核心项目 + 开源贡献 + 结业考核

---

## 阶段目标

L3阶段的核心目标是让学员具备**高级工程师的技术深度**——不只是能用Spark/Flink/Kafka完成业务需求，而是能深入理解底层实现原理，在面对极端场景（数据倾斜、大状态、高吞吐）时能做出最优技术决策。

学员结业时能够：

1. **源码级理解**：深入Spark SQL Catalyst、Flink Checkpoint/StateBackend、Kafka Producer/Broker核心源码，至少阅读3000行核心代码
2. **论文精读能力**：精读12篇分布式系统经典论文，能用自己的话复述核心设计思想，能批判性地分析论文假设和局限
3. **调优攻坚能力**：面对生产级"烂任务"（100TB数据、严重倾斜、不合理配置），能系统性地从倾斜→Shuffle→GC→Cache一步步优化至生产标准
4. **开源社区参与**：完成至少1个Apache开源项目PR（Spark/Flink/Kafka等），理解开源协作规范
5. **技术写作能力**：每周产出一篇源码分析文章（不少于2000字），包含架构图、关键代码注释和设计模式分析
6. **构建MLOps平台**：能使用MLflow管理模型生命周期，使用Feast管理特征，使用Milvus+LangChain构建RAG应用
7. **掌握云原生大数据部署**：能在Kubernetes上部署Spark/Flink/Kafka，理解Operator模式，完成Docker Compose→K8s迁移

---

## 阶段时间线

| 周次 | 模块 | 核心任务 | 强制输出 |
|------|------|----------|----------|
| 第23周 | 论文精读(1) + Spark源码(1) | 完成GFS、MapReduce、BigTable三篇论文精读；阅读DataFrame API表层源码 | 3篇论文读书笔记 + 1篇DataFrame源码分析 |
| 第24周 | 论文精读(2) + Spark源码(2) | 完成Dremel、RDD、Kafka三篇论文精读；深入Catalyst逻辑优化层 | 3篇论文读书笔记 + 1篇Catalyst优化Rule分析 |
| 第25周 | 论文精读(3) + Flink/Kafka源码 | 完成Flink、Dynamo、Raft三篇论文精读；阅读Flink Checkpoint和Kafka Producer源码 | 3篇论文读书笔记 + Flink/Kafka源码分析各1篇 |
| 第26周 | 论文精读(4) + 源码收尾 | 完成DataLakehouse、Photon、Spanner三篇论文精读；源码阅读收尾总结 | 3篇论文读书笔记 + 源码阅读总结报告 |
| 第27-28周 | 项目10前半段 | 调优攻坚：倾斜解决 + Shuffle优化 + UDF优化 | 每步优化对比数据 + 分析报告 |
| 第29-30周 | 项目10后半段 | 调优攻坚：内存GC调优 + Cache策略对比 + 最终报告 | 调优Checklist + 完整调优报告 |
| 第31-32周 | 开源贡献任务 | 寻找Issue → 提交PR → Code Review → 合入 | PR链接 + 社区互动记录 |
| 第33-35周 | 综合冲刺 | 调优报告完善 + 源码分析文章精选集 + 论文答辩准备 | 所有L3交付物整理 |
| 第36周 | L3结业考核 | 源码问答 + 论文答辩 + 调优实战 + 交叉面试 | 考核成绩单 |
| 补充模块 | MLOps与AI工程 | ML流水线+特征工程+LLM+MLOps平台 | 80h | MLOps平台、RAG助手、特征存储 |
| 补充模块 | 云原生大数据 | K8s+Spark/Flink on K8s+迁移项目 | 60h | K8s部署、云原生迁移报告 |

---

## 核心交付物清单

### 论文精读（12篇 × 每篇2000+字读书笔记）
- 每篇论文按"三遍阅读法"完成
- 输出格式：论文核心观点 + 技术映射 + 批判性思考 + 工程启发

### 源码分析系列（至少6篇，每篇2000+字）
- Spark SQL Catalyst方向：至少3篇（DataFrame API → Catalyst逻辑优化 → Catalyst物理计划/WholeStageCodegen）
- Flink方向：至少1篇（Checkpoint/Savepoint/StateBackend）
- Kafka方向：至少1篇（Producer核心流程/Broker存储机制）
- 源码阅读总结报告：1篇（对比三个组件的设计模式异同）

### 项目10：调优攻坚
- 完整的调优报告（含5步调优前后对比数据）
- 调优Checklist（可直接用于生产环境评审）
- 数据对比模板（含实验配置、结果数据、结论与建议）

### 开源贡献
- 至少1个PR（合入或至少经历完整Code Review）
- 社区互动记录（JIRA Issue、邮件列表、Code Review讨论）
- 开源协作规范总结

### 结业考核
- 源码现场问答
- 论文PPT答辩（15分钟）
- 调优实战演示（运行时间缩短90%以上）
- 交叉面试答辩

### MLOps与AI工程（补充模块）
- MLflow实验追踪配置和Model Registry
- Feast特征定义和在线/离线特征服务
- RAG智能助手代码（Milvus+LangChain）
- 项目10.5：MLOps平台完整交付物

### 云原生大数据（补充模块）
- K8s集群配置和Helm Charts
- Spark/Flink/Kafka on K8s部署YAML
- 项目11：云原生迁移完整交付物
- Docker Compose vs K8s性能对比报告

---

## 前置条件

进入L3阶段前，学员必须满足：

- [x] L2阶段结业通过（实时数据管道 + DDIA读书笔记 + 故障排查SOP）
- [x] 已阅读DDIA全书至少1遍（重点章节2遍以上）
- [x] Spark/Flink/Kafka有至少2个实际项目经验
- [x] 能独立搭建Docker Compose大数据集群环境
- [x] Git操作熟练（merge/rebase/cherry-pick/conflict resolution）

---

## 学习纪律

| 纪律项 | 要求 | 违规后果 |
|--------|------|----------|
| GitHub每日提交 | 工作日必须提交（源码笔记/调优代码/论文笔记） | 缺1天警告，连续缺3天启动退出流程 |
| 技术Blog每周1篇 | 每周一提交上周的源码分析或论文笔记 | 不交不进入下一周的课程 |
| 源码阅读打卡 | 每日记录阅读行数和理解的模块 | 周末汇总检查 |
| 论文读书笔记 | 每篇论文必须有结构化笔记 | 无笔记视为未阅读 |
| 代码实践 | 源码阅读必须配合debug和修改实验 | 纯读不写视为无效 |

---

## 推荐参考资源

| 资源类型 | 名称 | 说明 |
|----------|------|------|
| 书籍 | 《Spark SQL内核剖析》 | Catalyst优化器原理参考 |
| 书籍 | 《Apache Flink源码解析》 | Flink核心模块源码导读 |
| 书籍 | 《Kafka权威指南》第5-6章 | Producer和Broker内部原理 |
| 在线资源 | Spark源码GitHub仓库 | https://github.com/apache/spark |
| 在线资源 | Flink源码GitHub仓库 | https://github.com/apache/flink |
| 在线资源 | Kafka源码GitHub仓库 | https://github.com/apache/kafka |
| 论文 | L3论文清单12篇 | 见论文精读清单文档 |

---

## 补充模块目录结构

```
补充模块_MLOps与AI工程/
├── 课时27_MLOps流水线实战.md
├── 课时28_特征工程与特征存储.md
├── 课时29_LLM与RAG应用开发.md
└── 项目10.5_MLOps平台构建.md

补充模块_云原生大数据/
├── 课时30_Kubernetes与大数据.md
├── 课时31_Spark与Flink_on_K8s.md
└── 项目11_云原生大数据平台迁移.md
```