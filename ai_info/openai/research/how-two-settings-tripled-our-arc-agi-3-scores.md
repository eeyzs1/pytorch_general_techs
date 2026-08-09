# 两个设置如何让 ARC-AGI-3 成绩翻三倍（How enabling two settings tripled our scores on the ARC-AGI-3 benchmark）

- **原文链接**: [How enabling two settings tripled our scores on the ARC-AGI-3 benchmark](https://openai.com/index/how-two-settings-tripled-our-arc-agi-3-scores/)
- **作者**: Ilan Bigio, Ted Sanders
- **发布日期**: 2026-07-29
- **检索日期**: 2026-08-01
- **标签**: #ARC-AGI-3 #评估方法论 #保留推理 #Compaction #ResponsesAPI #Harness设计

## 核心观点

OpenAI 研究团队在 ARC-AGI-3 基准上发现：GPT-5.6 Sol 官方 harness 得分仅 13.3%（GPT-5.5 更只有 0.4%），并非模型不行，而是 harness 的两个设置问题——每次动作后丢弃私有推理、滚动截断窗口丢失历史。改用 ChatGPT/Codex 生产环境同款设置（Responses API 的"保留推理"与"compaction"）后，公开任务集得分升至 38.3%（约 3 倍），输出 token 反而减少 6 倍。

文章的核心提醒：基准测试很少孤立地度量模型，它同时度量 API 设置、harness 设计与提示词的一揽子选择——这已不是第一次"公开基准低分、排查后发现通用 harness 丢了推理消息"。

## 关键发现 / 关键技术

### 1. 问题诊断：两种"失忆"
- 官方 harness 每个动作后丢弃全部私有推理：模型每步都要从零重新理解游戏，看不到产生之前动作的计划与洞察
- 滚动截断（超 17.5 万字符丢弃最老消息）：不仅丢思考，连过去的动作与观察也丢失，且长时运行在高负载窗口还会轻微损害性能

### 2. 修复：保留推理 + Compaction
- Responses API 传 previous response ID 即可跨工具调用与轮次保留推理；模型不再每步重新解释游戏，单步思考时间下降、长期策略更连贯
- 用 compaction（对话过长时摘要续接）替代滚动截断：保住对每款游戏的长期学习成果，得分更高且 token 更省
- 在某款游戏的排行榜上，前沿模型均无法通过第一关之后的关卡；用 OpenAI harness 的 GPT-5.6 Sol 全通六关

### 3. 基准背景
- ARC-AGI-3 用刻意通用的 harness（无工具无特性）以凸显模型短板、公平比较；商用开发者则会针对模型特性优化 harness
- 人类测试者平均分约 48%（RHAE 指标），模型在评测中看不到得分

## 实践意义

对 API 开发者，官方建议非常明确：用 Responses API（而非旧 Chat Completions）、保留推理、启用 compaction——这也是对比模型时应要求的评测条件。对评估研究者，本文是继"harness 影响编码评测"之后又一力证：评估结论必须绑定 harness 配置披露，否则跨模型比较可能度量的是脚手架差异而非智能差异。对 agent 系统设计，"记忆连续性"（推理 + 动作历史）是长时任务性能的第一变量。

## 跨厂商对比

- 与 [从噪声中分离信号：编码评估](separating-signal-from-noise-coding-evaluations.md) 互补：编码域与游戏域共同证明"评估 = 模型 × harness"
- 与 [Codex-Maxxing 长时工作](codex-maxxing-long-running-work.md) 互补：compaction 在长时编码工作中的价值同样在 ARC 游戏中得到验证
- 与 [Anthropic 基础设施噪声量化](../../anthropic/engineering/quantifying-infrastructure-noise-in-agentic-coding-evals.md) 对比：Anthropic 量化基础设施噪声，OpenAI 揭示 harness 设置的系统性偏差，两者都在呼吁评估方法论的严谨化

## 资源

- 原文：[How enabling two settings tripled our scores on ARC-AGI-3](https://openai.com/index/how-two-settings-tripled-our-arc-agi-3-scores/)
- 基准：[ARC-AGI-3](https://arcprize.org/arc-agi/3)
- 文档：[Responses API Compaction](https://developers.openai.com/api/docs/guides/compaction)
