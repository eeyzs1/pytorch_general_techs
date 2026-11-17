# Meta 将专门模型与主动记忆带入 Muse 和 Meta AI（Specialized Models）

- **原文链接**: [Bringing Specialized Models to Muse and Meta AI](https://research.meta.ai/blog/specialized-models-for-muse-and-metaai)
- **作者**: Meta AI
- **发布日期**: 2026-11-06
- **检索日期**: 2026-11-17
- **标签**: #模型专门化 #Agent记忆 #任务恢复

## 核心观点

Meta 介绍用 Muse Wonder 改善现有模型，并将 Active Memory 与 Active Focus 带到 Muse / Meta AI。

目标是跨会话保留有用信息，并在任务受阻或用户中途纠偏时继续推进目标。

## 关键发现 / 关键技术

### 1. 机制与适用范围

临时与长期信息、过期与仍相关的信息需要区分；记忆不是简单堆积全部历史。

### 2. 证据与边界

页面采用内部指标展示改进，不能把内部综合分或任务增幅直接换算成任意业务的效果。

## 实践意义

工程解读：为记忆更新、目标恢复与用户纠偏分别设置回归任务。

## 跨厂商对比

- 与 [Anthropic 记忆组件](../anthropic/engineering/components-of-agent-memory.md) 对照：比较模型能力侧与显式记忆组织侧的实现视角。

## 资源

- 官方原文：[官方原文](https://research.meta.ai/blog/specialized-models-for-muse-and-metaai)
