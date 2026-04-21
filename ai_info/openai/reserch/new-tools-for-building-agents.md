# New Tools for Building Agents

- **原文链接**: [New tools for building agents](https://openai.com/index/new-tools-for-building-agents/)
- **发布日期**: 2025-03-11
- **标签**: #Responses-API #Agents-SDK #Web搜索 #文件搜索 #Computer-Use #护栏

## 核心观点

OpenAI 发布了首批专门为构建 Agent 应用设计的构建块：Responses API、Agents SDK 和内置工具（Web 搜索、文件搜索、Computer Use）。这些工具旨在简化 Agent 开发，解决开发者反馈的"缺乏可见性和内置支持"的痛点。

## 关键概念

### Responses API
- 结合 Chat Completions API 的简洁性和 Assistants API 的工具使用能力
- 单次 API 调用可使用多个工具和模型轮次
- 统一的基于项目的设计、更简单的多样性、直观的流式事件
- `response.output_text` 等 SDK 辅助函数简化文本访问

### 内置工具

1. **Web 搜索**: GPT-4o 使用 Web 搜索在 SimpleQA 上达到 90% 准确率（GPT-4.5 无搜索仅 63%）
2. **文件搜索**: 在用户上传文件中搜索和检索信息
3. **Computer Use**: 与 Operator 相同的 CUA 模型，Agent 可操作计算机界面

### Agents SDK
- 开源，用于管理多 Agent 工作流
- 可配置的语言模型、Agent 交接、内置安全控制和分析工具
- Python 优先设计，利用 Python 原生特性编排和链式 Agent
- 五大核心能力：Agent 编排、交接、护栏、追踪、Python 优先

### 护栏 (Guardrails)
- 输入和输出验证确保安全性和可靠性
- 内置安全控制

### 追踪 (Tracing)
- 内置追踪工具用于可视化、调试和优化 Agent 工作流
- 统一监控功能

## 实践启示

- Responses API 是 Agent 开发的新基线——Assistants API 计划退役
- 内置工具大幅降低了 Agent 开发门槛
- Web 搜索 + 推理模型的组合显著提升事实准确性
- Agents SDK 的 Python 优先设计降低了学习曲线

## 相关文章

- [New Tools and Features in the Responses API](new-tools-and-features-in-the-responses-api.md) — API 的持续更新
- [Introducing AgentKit](introducing-agentkit.md) — 更高层的 Agent 构建工具
- [Introducing Operator](introducing-operator.md) — Computer Use 的消费者版本
- [A Practical Guide to Building Agents](a-practical-guide-to-building-agents.md) — Agent 构建方法论
