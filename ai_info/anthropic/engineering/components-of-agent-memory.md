# Agent 记忆组件：从记录到经过验证的经验（Agent Memory）

- **原文链接**: [The components of agent memory](https://www.anthropic.com/research/components-of-agent-memory)
- **作者**: Anthropic Engineering
- **发布日期**: 2026-11-06
- **检索日期**: 2026-11-17
- **标签**: #Agent记忆 #上下文工程 #评估

## 核心观点

Anthropic 将跨会话记忆拆成轨迹、记忆笔记、组织后的表示和预加载上下文；dreaming 在会话间整理这些材料。

文章把跨会话经验与权重学习、单会话上下文及 compaction 区分开。

## 关键发现 / 关键技术

### 1. 机制与适用范围

CL-Bench 实验观察模型能否把反馈整理为已验证规则，而不是积累未经检验的猜测。

### 2. 证据与边界

游戏案例说明记得更多不一定更有用；目标、计划和可复用规则，与每轮可直接读取的临时状态具有不同价值。

## 实践意义

工程解读：记忆需要来源、验证状态和更新机制，效果应由后续任务检验。

## 跨厂商对比

- 与 [ChatGPT Dreaming](../../openai/research/chatgpt-memory-dreaming.md) 对照：比较主动整理记忆的共同机制。
- 与 [Meta 专门模型的 Active Memory](../../meta/specialized-models-for-muse-and-metaai.md) 对照：对照显式记忆组织与模型训练的侧重。

## 资源

- 官方原文：[官方原文](https://www.anthropic.com/research/components-of-agent-memory)
