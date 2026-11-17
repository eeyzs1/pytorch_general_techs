# 构建可信安全评估：设计、运行与报告（Safety Evaluations）

- **原文链接**: [Building strong safety evaluations](https://www.anthropic.com/research/building-strong-safety-evaluations)
- **作者**: Anthropic Engineering
- **发布日期**: 2026-11-13
- **检索日期**: 2026-11-17
- **标签**: #安全评估 #方法论 #多轮评估

## 核心观点

Anthropic 从设计、运行和报告三个阶段说明安全评估的可靠性。

评估应测量实际关心的行为与伤害风险，而不是把拒绝率简单当作安全性的替代指标。

## 关键发现 / 关键技术

### 1. 机制与适用范围

区分观察性与因果问题；使用领域专家定义标准，覆盖多轮互动以及有害响应和过度拒绝。

### 2. 证据与边界

运行安全、预注册、完整统计报告与复现材料共同决定结果能否支持安全主张。

## 实践意义

工程解读：测试集、评分标准和环境应一起版本化，避免只发布一个通过率。

## 跨厂商对比

- 与 [OpenAI 嵌入式评估](../../openai/research/our-first-phase-of-embedded-assessments.md) 对照：内部评测质量与外部证据访问构成互补。

## 资源

- 官方原文：[官方原文](https://www.anthropic.com/research/building-strong-safety-evaluations)
