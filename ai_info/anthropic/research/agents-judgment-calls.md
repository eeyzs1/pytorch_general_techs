# AI 如何影响专家判断：执行辅助之外的决策偏向（Experts' Judgment Calls）

- **原文链接**: [How AI agents shape experts’ judgment calls](https://www.anthropic.com/research/agents-judgment-calls)
- **作者**: Anthropic
- **发布日期**: 2026-10-27
- **检索日期**: 2026-11-17
- **标签**: #人机协作 #实验设计 #专家判断

## 核心观点

研究让 50 名使用 Claude Code 的专业分析师完成统计分析，随机设置智能体在若干合理选项间的倾向，检验专家是否受其影响。

它关注判断权如何在协作中转移，而不只是执行速度。

## 关键发现 / 关键技术

### 1. 机制与适用范围

分析师在四个分析选择上有 86% 跟随智能体倾向；只有少数人在事后把论据归因于智能体。

### 2. 证据与边界

11 名未使用智能体者是自选组，不能将其与使用组的差异直接解释为随机分配 AI 使用的因果效果。

## 实践意义

工程解读：关键判断可记录候选方案、证据和人工理由，以评估人类监督是否真正发挥作用。

## 跨厂商对比

- 与 [Agent 对工作方式的影响](../../openai/research/how-agents-are-transforming-work.md) 对照：使用行为分析与受控判断实验回答不同问题。

## 资源

- 官方原文：[官方原文](https://www.anthropic.com/research/agents-judgment-calls)
