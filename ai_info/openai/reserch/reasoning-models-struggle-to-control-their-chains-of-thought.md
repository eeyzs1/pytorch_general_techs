# Reasoning Models Struggle to Control Their Chains of Thought, and That's Good

- **原文链接**: [Reasoning models struggle to control their chains of thought, and that's good](https://openai.com/index/reasoning-models-struggle-to-control-their-chains-of-thought/)
- **发布日期**: 2026-03-05
- **标签**: #CoT-Control #思维链 #可监控性 #推理模型 #安全

## 核心观点

OpenAI 引入 CoT-Control 评估套件，发现推理模型难以控制其思维链 (CoT)。这一发现强化了 CoT 可监控性作为 AI 安全保障的价值——如果模型无法轻易隐藏其真实推理过程，那么监控思维链就是有效的安全策略。

## 关键概念

### CoT-Control 评估
- 测试推理模型是否能控制其思维链
- 评估模型是否能在思维链中"隐藏"真实意图
- 结论：推理模型难以有效控制其 CoT

### 为什么"难以控制"是好事
- 如果模型无法控制 CoT，就无法轻易欺骗监控者
- CoT 忠实反映了模型的真实推理过程
- 这使得 CoT 监控成为可行的安全策略

### 对安全的意义
- CoT 可监控性是推理模型的安全特性
- 与 [How We Monitor Internal Coding Agents for Misalignment](how-we-monitor-internal-coding-agents-for-misalignment.md) 直接相关
- 监控思维链比仅监控输出提供更深入的安全洞察

### 与对齐研究的联系
- 如果模型能完美控制 CoT，监控将失效
- 当前推理模型的 CoT 不可控性是一个安全优势
- 但随着模型能力提升，这一特性可能改变

## 实践启示

- CoT 监控是当前推理模型安全的有效工具
- 应趁 CoT 仍忠实于推理过程时建立监控基础设施
- 模型能力的提升可能改变 CoT 的可监控性
- 安全策略需要随模型能力演进

## 相关文章

- [How We Monitor Internal Coding Agents for Misalignment](how-we-monitor-internal-coding-agents-for-misalignment.md) — CoT 监控的实践应用
- [Improving Instruction Hierarchy in Frontier LLMs](improving-instruction-hierarchy-in-frontier-llms.md) — 另一种模型安全策略
- [Inside Our Approach to the Model Spec](inside-our-approach-to-the-model-spec.md) — 模型行为规范框架
