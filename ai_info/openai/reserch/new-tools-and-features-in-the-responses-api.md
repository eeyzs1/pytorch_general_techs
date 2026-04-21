# New Tools and Features in the Responses API

- **原文链接**: [New tools and features in the Responses API](https://openai.com/index/new-tools-and-features-in-the-responses-api/)
- **发布日期**: 2025-03（持续更新）
- **标签**: #Responses-API #Web搜索 #文件搜索 #Computer-Use #Agent开发

## 核心观点

Responses API 是 OpenAI 为构建 Agent 应用设计的核心 API，结合了 Chat Completions API 的简洁性和 Assistants API 的工具使用能力。自发布以来已有数十万开发者使用，处理了数万亿 token。API 内置了网页搜索、文件搜索和计算机使用等工具。

## 关键概念

### Responses API 定位
- 替代 Assistants API（计划退役）
- Chat Completions API 继续为不需要 Agent 功能的开发者服务
- Responses API 是构建 Agent 应用的基线

### 内置工具

1. **Web 搜索**: Agent 可搜索互联网获取实时信息
2. **文件搜索**: 在用户上传的文件中搜索和检索信息
3. **Computer Use**: Agent 可操作计算机界面（与 Operator 相同的 CUA 模型）

### Agents SDK
- 与 Responses API 同时发布
- 用于创建和管理多 Agent 工作流
- 支持管理者模式和去中心化模式

### 客户应用案例
- Zencoder 的编码 Agent
- Revi 的市场情报 Agent（面向私募和投资银行）
- MagicSchool AI 的教育助手

## 实践启示

- Responses API 是 OpenAI Agent 开发生态的核心
- 内置工具降低了 Agent 开发门槛
- 从 Chat Completions → Assistants → Responses API 的演进反映了 Agent 能力的增强
- 与 Anthropic 的 MCP 生态相比，OpenAI 的工具更内置但更封闭

## 相关文章

- [A Practical Guide to Building Agents](a-practical-guide-to-building-agents.md) — Agent 构建方法论
- [Introducing Operator](introducing-operator.md) — Computer Use 的消费者版本
- [Introducing AgentKit](introducing-agentkit.md) — 更高层的 Agent 构建工具
