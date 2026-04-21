# The Next Evolution of the Agents SDK

- **原文链接**: [The next evolution of the Agents SDK](https://openai.com/index/the-next-evolution-of-the-agents-sdk/)
- **发布日期**: 2026-04-15
- **标签**: #Agents-SDK #MCP #工具调用 #多Agent #护栏

## 核心观点

Agents SDK 迎来重大更新，新增 MCP 工具调用支持、增强的多 Agent 编排能力和更强大的护栏系统。这次更新使 Agents SDK 与更广泛的 AI 工具生态实现了互操作。

## 关键概念

### MCP 工具调用支持
- Agents SDK 现在支持 Model Context Protocol (MCP) 工具
- 可与任何 MCP 兼容的服务器交互
- 标志着 OpenAI 对开放协议的进一步采纳

### 增强的多 Agent 编排
- 改进的 Agent 交接机制
- 更灵活的工作流编排
- 支持更复杂的多 Agent 协作模式

### 增强的护栏系统
- 更精细的输入/输出验证
- 可配置的安全策略
- 支持自定义护栏规则

### 与 AgentKit 的关系
- Agents SDK 是 AgentKit 的底层编程接口
- Agent Builder 可视化设计器生成 Agents SDK 代码
- 两者互补：SDK 用于编程式开发，AgentKit 用于可视化开发

## 实践启示

- MCP 支持意味着 OpenAI Agent 可与 Anthropic MCP 生态互操作
- Agents SDK 正在成为 OpenAI Agent 开发的标准编程接口
- 护栏系统的增强反映了生产部署的安全需求
- 与 AgentKit 的双轨开发模式满足不同开发者偏好

## 相关文章

- [New Tools for Building Agents](new-tools-for-building-agents.md) — Agents SDK 的初始发布
- [Introducing AgentKit](introducing-agentkit.md) — 可视化 Agent 构建工具
- [New Tools and Features in the Responses API](new-tools-and-features-in-the-responses-api.md) — 底层 API
- [A Practical Guide to Building Agents](a-practical-guide-to-building-agents.md) — Agent 构建方法论
