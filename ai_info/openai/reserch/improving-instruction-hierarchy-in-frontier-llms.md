# Improving Instruction Hierarchy in Frontier LLMs

- **原文链接**: [Improving instruction hierarchy in frontier LLMs](https://openai.com/index/improving-instruction-hierarchy/)
- **发布日期**: 2026-03-10
- **标签**: #指令层级 #IH-Challenge #提示注入防御 #安全 #可信指令

## 核心观点

OpenAI 引入 IH-Challenge 训练模型优先处理可信指令，改善指令层级、安全可引导性和抵抗提示注入攻击的能力。这是解决 Agent 安全核心问题——如何确保模型区分系统指令和用户输入——的重要技术进展。

## 关键概念

### 指令层级问题
- LLM 需要区分不同来源的指令
- 系统指令 > 开发者指令 > 用户输入
- 提示注入攻击利用模型无法区分指令来源的弱点

### IH-Challenge
- 训练模型优先处理可信指令
- 提高安全可引导性
- 增强抵抗提示注入攻击的能力

### 与 Agent 安全的关系
- Agent 系统中，模型有工具访问权限
- 提示注入可能导致 Agent 执行恶意操作
- 指令层级是 Agent 安全的基础防线

## 实践启示

- 指令层级是 Agent 安全的必要条件
- 提示注入是 Agent 部署的主要威胁
- 模型级别的防御比应用级别的补丁更可靠
- 与 Anthropic 的沙箱隔离是互补的安全策略

## 相关文章

- [How We Monitor Internal Coding Agents for Misalignment](how-we-monitor-internal-coding-agents-for-misalignment.md) — Agent 失准监控
- [Inside Our Approach to the Model Spec](inside-our-approach-to-the-model-spec.md) — 模型行为规范
- [Reasoning Models Struggle to Control Their Chains of Thought](reasoning-models-struggle-to-control-their-chains-of-thought.md) — 推理模型的可控性
