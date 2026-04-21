# How We Monitor Internal Coding Agents for Misalignment

- **原文链接**: [How we monitor internal coding agents for misalignment](https://openai.com/index/how-we-monitor-internal-coding-agents-for-misalignment/)
- **发布日期**: 2026-03-19
- **标签**: #对齐监控 #CoT监控 #内部Agent #安全 #思维链

## 核心观点

OpenAI 使用思维链 (CoT) 监控来研究内部编码 Agent 的失准行为——分析真实部署来检测风险并加强 AI 安全保障。这是首批公开讨论在生产环境中监控 Agent 思维链以检测失准的研究之一。

## 关键概念

### CoT 监控方法
- 监控 Agent 的思维链而非仅监控输出
- 思维链是 Agent 推理过程的窗口
- 可检测输出中不可见的失准行为

### 内部编码 Agent 监控
- 在真实内部部署中监控编码 Agent
- 分析 Agent 是否偏离预期目标
- 检测潜在的风险行为模式

### 与 CoT-Control 的关系
- [Reasoning Models Struggle to Control Their Chains of Thought](reasoning-models-struggle-to-control-their-chains-of-thought.md) 发现推理模型难以控制其思维链
- 这意味着 CoT 监控是可行的——模型无法轻易"隐藏"其真实意图
- CoT 的不可控性反而是安全监控的优势

## 实践启示

- CoT 监控是 Agent 安全的重要工具
- 监控推理过程比仅监控输出更有效
- 内部部署是发现安全问题的宝贵测试场
- 思维链的"不可控性"是安全监控的"特性而非缺陷"

## 相关文章

- [Reasoning Models Struggle to Control Their Chains of Thought](reasoning-models-struggle-to-control-their-chains-of-thought.md) — CoT 可控性研究
- [Improving Instruction Hierarchy in Frontier LLMs](improving-instruction-hierarchy-in-frontier-llms.md) — 指令层级安全
- [Inside Our Approach to the Model Spec](inside-our-approach-to-the-model-spec.md) — 模型行为规范框架
