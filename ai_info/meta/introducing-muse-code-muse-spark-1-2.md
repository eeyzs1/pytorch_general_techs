# Muse Code 与 Muse Spark 1.2：Meta 首个终端编码 Agent（Introducing Muse Code and Muse Spark 1.2）

- **原文链接**: [Introducing Muse Code and Muse Spark 1.2](https://research.meta.ai/blog/introducing-muse-code-and-muse-spark-1-2)
- **作者**: Meta Superintelligence Labs（MSL）
- **发布日期**: 2026-08-05
- **检索日期**: 2026-08-08
- **标签**: #MuseCode #MuseSpark #编码Agent #终端工具 #Meta

## 核心观点

Meta 超级智能实验室（MSL）发布 Muse Code 测试版——一款运行于终端的 AI 编码 Agent，由新模型 Muse Spark 1.2 驱动。它面向大型代码仓库的复杂软件工程任务：规划变更、编写代码、运行工具并验证结果。Muse Code 的两大核心设计是持久化异步后台 Agent（整个会话期间持续运行，而非按任务临时创建）与本地 append-only 事件日志（记录每次模型调用、工具运行、审批与编辑，可精确重放且崩溃后可恢复）。Muse Spark 1.2 与 Muse Code 协同训练，在 Terminal-Bench 2.1 上得分 82.9%。模型未开放权重，通过 Meta Model API 与 Muse Code 提供。

## 关键发现 / 关键技术

### 1. 持久化后台 Agent 与并行子 Agent
- 异步后台 Agent 在整个会话期间持续存活，积累上下文，避免重复信息收集，降低延迟与人工引导
- 大任务可拆分为多个子 Agent，各自在独立 git worktree 中并行工作，互不覆盖
- 后台 Agent 自主决定何时向主 Agent 反馈结果

### 2. 可重放、可恢复的运行时
- 本地事件日志作为唯一可信数据源：每次模型调用、工具运行、审批、编辑均被追加记录
- 运行过程可精确重放（replay-exact）且重启安全（restart-safe）：崩溃后从中断处继续
- 使长时程任务（如 24 小时、1000+ 次工具调用的内核优化案例）能存活于故障

### 3. 内置技能与协同训练
- 三个默认技能：`/plan`（生成需审批的计划）、`/grill`（对计划反复压力测试）、`/goal`（围绕目标持续推进直至完成）
- Muse Spark 1.2 与 Muse Code 协同训练：引入拒绝采样的 Agent 轨迹、目标执行/上下文压缩/子 Agent 的配方优化，并将 Muse Code 工具集纳入训练
- 长时程训练覆盖整库生成、大型端到端项目与自动化研究；利用 Spark 1.1 生成高难度编程环境作为 1.2 的自我改进数据

### 4. 评测表现
- Terminal-Bench 2.1：82.9%（第二，仅次于 Claude Code on Opus 5 的 86.7%，高于 Codex on GPT-5.6 Terra 的 81.8%）
- DeepSWE 1.1：59.3%（第三，Claude Code 65.0% 与 Codex 64.8% 领先）
- Meta Internal Coding Bench（440 项内部真实 PR 任务）：70.6%（低于 Claude Opus 5 的 79.4%）
- 评测在隔离的 Daytona 云沙箱中运行，对比含 Grok 4.5、Gemini 3.6 Flash、Kimi K3

## 实践意义

Meta 正式加入由 Anthropic（Claude Code）与 OpenAI（Codex）主导的编码 Agent 赛道。Muse Code 的差异化在于"模型与 harness 协同训练"——把工具集、上下文压缩、子 Agent 编排直接训进权重，而非事后包装。持久化后台 Agent 与 append-only 事件日志直击长时程任务的两大痛点：上下文丢失与故障不可恢复。但 Meta 自评在长时程（DeepSWE）与自家内部基准上仍落后于 Claude Opus 5，说明编码 Agent 的前沿仍在别处。定价与 Spark 1.1 一致（输入 $1.25/输出 $4.25 每百万 token），约为同级模型价格的 1/4。

## 跨厂商对比

- 与 [Muse Spark 1.1](muse-spark-1-1.md) 衔接：1.1 引入主-子 Agent 编排与 Meta Model API 商业化，1.2 在此基础上专攻编码能力并与 Muse Code harness 协同训练，从"通用 Agent 模型"演进为"编码 Agent 模型 + 工具"一体化产品
- 与 [Muse Spark 初代](muse-spark.md) 对比：初代是 Meta 闭源转向的首个旗舰，1.2 把能力收敛到编码场景并首次配套终端 Agent
- 与 [Codex 全面可用](../openai/research/codex-now-generally-available.md) 对比：Codex 走产品矩阵（CLI/桌面/IDE 插件），Muse Code 目前仅终端且无桌面端，但协同训练与持久化后台 Agent 是其架构差异点

## 资源
- 原文：[Introducing Muse Code and Muse Spark 1.2](https://research.meta.ai/blog/introducing-muse-code-and-muse-spark-1-2)
- 安装：`curl -fsSL https://dev.meta.ai/install.sh | bash`（macOS / Linux）
- 模型 API：[developer.meta.com/ai](https://developer.meta.com/ai/)
- 评测方法报告：[Muse Spark 1.2 methodology](https://research.meta.ai/static/muse-spark-1-2-methodology)
