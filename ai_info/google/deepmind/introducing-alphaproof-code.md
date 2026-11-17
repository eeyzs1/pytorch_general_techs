# AlphaProof Code：将形式化验证推进到真实实现（AlphaProof Code）

- **原文链接**: [Introducing AlphaProof Code: a breakthrough in verifying complex software at depth](https://deepmind.google/blog/introducing-alphaproof-code/)
- **作者**: Pushmeet Kohli, Swarat Chaudhuri
- **发布日期**: 2026-11-10
- **检索日期**: 2026-11-17
- **标签**: #形式化验证 #多智能体 #软件可靠性

## 核心观点

AlphaProof Code 结合人类专家与多模型智能体，对 Signal 协议相关实际代码的关键性质开展形式化验证。

专家审查规格，智能体生成证明，证明检查器验证形式化结果。

## 关键发现 / 关键技术

### 1. 机制与适用范围

工作将验证对象从协议设计推进到实现相关代码，使用 Lean 证明产物和人工重点审查相结合。

### 2. 证据与边界

形式化证明只覆盖所表达的规格、代码范围与假设；不能把它改写为整个产品没有任何漏洞。

## 实践意义

工程解读：区分规格正确性、证明检查通过与系统整体可靠性，分别记录证据。

## 跨厂商对比

- 与 [数学成果披露与 Lean 验证](../../openai/research/sharing-ai-progress-in-mathematics.md) 对照：对照自然语言成果、形式化产物与专家接受的不同状态。

## 资源

- 官方原文：[官方原文](https://deepmind.google/blog/introducing-alphaproof-code/)
