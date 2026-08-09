# GLM-5.2：1M 无损上下文与长程任务开源 SOTA（GLM-5.2 Flagship Model）

- **原文链接**: [智谱开放平台新品发布](https://docs.bigmodel.cn/cn/update/new-releases)
- **作者**: 智谱 AI（Zhipu AI）
- **发布日期**: 2026-06-16
- **检索日期**: 2026-07-31
- **标签**: #GLM-5.2 #智谱 #长程任务 #1M上下文 #开源模型 #Coding

## 核心观点

GLM-5.2 是智谱 2026 年 6 月 16 日上线的新一代旗舰模型，核心卖点是 1M 无损上下文与长程任务能力：显著减少复杂任务中的上下文漂移与目标遗忘，Coding 与长程任务评测达到开源 SOTA，在复杂系统工程、深度调试中表现更稳。模型约 7400 亿参数，是首个在 AI 编程能力上追上 Claude Opus 级别的国产模型，并宣布开放部分模型权重。智谱保持约两个月一版的迭代节奏，2026 年一季度全球调用量增长 400%，平台注册企业及用户突破 600 万。

## 关键发现 / 关键技术

### 1. 长程任务能力体系化
- 1M 无损上下文，针对长任务中的目标保持、上下文漂移做专门优化
- 通过算法架构创新与工程优化降低训练和推理算力消耗
- 总裁王绍兰明确定位："让模型自主且长时间地运行一个任务，实现端到端交付"（如新药研发中几十个智能体联合行动找靶点）

### 2. 参数效率优先
- 约 7400 亿参数，仅为 Kimi K3（2.8T）的约 1/4
- 依靠后训练能力以小参数对标国际顶级闭源模型的编程性能
- 对比 GLM-5.1（4 月发布，8 小时连续工作、对齐 Claude Opus 4.6）稳步迭代

### 3. 开源与商业化双轮
- 部分权重开源，上线 BigModel 平台与 GLM Coding Plan（个人版/团队版）
- 兼容 Claude Code、VS Code 等主流编码工具，订阅制而非纯按量计费
- 政务、金融、制造、医疗等行业落地加速

## 实践意义

GLM-5.2 印证了"长程任务"已成为国产旗舰模型的主战场——光有大上下文窗口不够，还要在数小时级任务中不丢目标。对企业选型：GLM Coding Plan 的订阅制+主流 IDE 兼容提供了 Claude Code 之外的合规可选项。参数效率路线（7400 亿对标 2.8T 级能力）也降低了私有化部署门槛。

## 跨厂商对比

- 与 [Kimi K3](../../kimi/blog/kimi-k3.md) 对比：K3 以 2.8T 参数换能力上限，GLM-5.2 以 1/4 参数换部署效率——同登全球榜单的"北京双子星"两种路线
- 与 [DeepSeek-V4 正式版](../../deepseek/news/deepseek-v4-ga.md) 对比：DeepSeek 靠后训练+DSpark 提速，GLM 靠长程任务专项优化+订阅制商业化
- 与 [Anthropic 长时 Agent Harness](../../anthropic/engineering/effective-harnesses-for-long-running-agents.md) 互补：Anthropic 从 harness 工程解长时任务，GLM 从模型权重层内生支持

## 资源

- 发布公告：[docs.bigmodel.cn/cn/update/new-releases](https://docs.bigmodel.cn/cn/update/new-releases)
- 模型文档：[GLM-5.2 模型指南](https://docs.bigmodel.cn/cn/guide/models/text/glm-5.2)
- 平台：[bigmodel.cn](https://www.bigmodel.cn/)
