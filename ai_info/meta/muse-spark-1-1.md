# Muse Spark 1.1：Meta 的 Agent 旗舰模型与首次 API 公测（Muse Spark 1.1 and the Meta Model API）

- **原文链接**: [Introducing Muse Spark 1.1 and the Meta Model API](https://ai.meta.com/blog/introducing-muse-spark-meta-model-api/)
- **作者**: Meta Superintelligence Labs
- **发布日期**: 2026-07-09
- **检索日期**: 2026-07-31
- **标签**: #MuseSpark #Meta #Agent #ModelAPI #ComputerUse #多Agent编排

## 核心观点

Muse Spark 1.1 是 Meta 超级智能实验室（MSL）面向 Agent 任务的多模态推理模型重大升级，同步开启 Meta Model API 公测——Meta 首次向开发者直接售卖旗舰模型调用（输入 $1.25 / 输出 $4.25 每百万 token，新账户 $20 免费额度）。模型被训练为"主 Agent"：收集上下文、制定计划、把子任务分派给并行子 Agent 执行以缩短端到端时延；作为子 Agent 时也懂得配合与上报能力边界。Alexandr Wang 称其为 Meta 在 Agent 与编码任务上最强的模型，目标对标 Claude 与 GPT 旗舰。

## 关键发现 / 关键技术

### 1. 主-子 Agent 编排架构
- 复杂任务下自主规划、调度、委派多个并行子 Agent
- 子 Agent 模式下识别可用工具、到达能力边界时主动上报
- 100 万 token 上下文 + 主动管理：记住历史操作、找回早期信息、压缩时保留后续步骤所需关键内容

### 2. 务实的 Computer Use
- 按场景自选执行方式：写脚本更快就写脚本、点 GUI 更省事就点界面、批量场景一次生成多步操作统一执行
- 解决传统计算机操作 Agent"每一步重新看屏-推理-点击"的低效问题
- 案例：订餐过程中用户临时改条件，模型自主发现新情况并调整方案

### 3. 真实代码库编码与生态适配
- 面向诊断复杂 bug、企业级系统新功能、大规模代码迁移训练
- 适配不同编码工具链与 harness：规划模式、目标条件、子 Agent 委派、上下文压缩
- OpenCode 调试演示：搭建网页应用→自动截图找问题→定位代码→修改→再验证

### 4. 商业化转向
- API 定价低于 OpenAI/Anthropic 同级产品，但仅限 Meta 自家生态（未上 OpenRouter 等第三方平台）
- 开源版 MuseSpark 在开发中但未定档；下一代代号 "Watermelon" 训练中，算力高一个数量级

## 实践意义

Meta 正式从"开源生态换影响力"转向"闭源 API 换收入"，Agent 能力是其切入企业市场的楔子。对开发者：主流编码 harness 即插即用的设计降低了试用门槛，定价激进；对行业：主-子 Agent 编排从框架层（LangGraph 等）下沉到模型层，模型原生编排能力可能成为下一代 Agent 模型的标配。

## 跨厂商对比

- 与 [Muse Spark 初代](muse-spark.md) 对比：从"首个闭源超级智能模型"到"Agent 任务专精 + API 商业化"
- 与 [GPT-5.6](../openai/research/introducing-gpt-5-6.md) 对比：OpenAI 强调可扩展智能档位与企业集成，Meta 强调主-子 Agent 编排与激进定价
- 与 [Claude 的 Managed Agents](../anthropic/engineering/scaling-managed-agents.md) 对比：Anthropic 在平台层解耦 brain/hands，Meta 把编排能力直接训进模型
- 与 [Kimi K3](../kimi/blog/kimi-k3.md) 对比：K3 走 2.8T 开源长程编码路线，Muse Spark 1.1 走闭源 API + Agent 编排路线

## 资源

- 原文：[Introducing Muse Spark 1.1 and the Meta Model API](https://ai.meta.com/blog/introducing-muse-spark-meta-model-api/)
- 相关：[Muse Spark 初代](muse-spark.md)
