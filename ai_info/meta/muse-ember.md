# Muse Ember：面向重复 Agent 子任务的经济模型（Muse Ember）

- **原文链接**: [Introducing Our Smallest, Most Efficient Model: Muse Ember](https://research.meta.ai/blog/muse-ember)
- **作者**: Meta AI
- **发布日期**: 2026-11-09
- **检索日期**: 2026-11-17
- **标签**: #高效模型 #Agent子任务 #评估口径

## 核心观点

Meta 发布 Muse Ember，定位大量重复的工具调用、编码子任务、路由和文档处理。

它与更强模型分工，以每项任务的质量和成本衡量执行层效率。

## 关键发现 / 关键技术

### 1. 机制与适用范围

公开与内部测试混合展示，Terminal-Bench 对比使用各自 harness，不能视为完全相同执行条件。

### 2. 证据与边界

模型通过 Meta Model API 等渠道提供；“更小、更高效”并不代表权重已开放或可以在手机本地部署。

## 实践意义

工程解读：路由方案需要比较任务成功、时延和成本，而不是仅比较每百万 token 标价。

## 跨厂商对比

- 与 [Gemini 4 Hydrogen](../google/deepmind/introducing-gemini-4-hydrogen.md) 对照：对照快速执行模型与强模型协作的定位。

## 资源

- 官方原文：[官方原文](https://research.meta.ai/blog/muse-ember)
