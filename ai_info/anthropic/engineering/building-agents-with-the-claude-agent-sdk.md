# Building Agents with the Claude Agent SDK

- **原文链接**: [Building agents with the Claude Agent SDK](https://www.anthropic.com/engineering/building-agents-with-the-claude-agent-sdk)
- **作者**: Thariq Shihipar 等
- **发布日期**: 2025-09-29
- **标签**: #Agent-SDK #Claude-Code #编程接口 #子Agent #MCP

## 核心观点

Claude Code SDK 更名为 Claude Agent SDK，以反映它驱动的远不止编码——深度研究、视频创作、笔记记录和其他非编码应用。核心设计原则是：**Agent 需要程序员使用的相同工具——终端访问、文件编辑、文件创建和文件搜索。通过给 Claude 一台计算机，它可以读取 CSV、搜索网络、构建可视化、解释指标，执行各种数字工作。** 这一原则与 [Building Effective Agents](building-effective-agents.md) 中"增强型 LLM"的理念一脉相承——Agent 的能力取决于它可用的工具。

## 关键概念

### Agent 循环
收集上下文 → 采取行动 → 验证工作 → 重复。[Claude Code Best Practices](claude-code-best-practices.md) 详细描述了这一循环在编码场景中的工作流模式。

### 核心能力

#### Agent 搜索
- 使用 bash 脚本（grep、tail）搜索文件
- 文件夹/文件结构成为上下文工程

#### 语义搜索
- 更快但准确性较低
- 先从 Agent 搜索开始，仅在需要时添加语义搜索

#### 子 Agent
- 默认支持，启用并行化和上下文隔离
- 只返回相关摘录，而非完整数据
- 这是 [Effective Context Engineering for AI Agents](effective-context-engineering-for-ai-agents.md) 中"子 Agent 架构"的 SDK 级实现

#### 压缩
- 接近上下文限制时自动总结之前的消息。这是 [Effective Context Engineering for AI Agents](effective-context-engineering-for-ai-agents.md) 中"压缩"技术的内置实现

#### MCP 集成
- 与外部服务（Slack、GitHub、Google Drive、Asana）的标准化集成
- 自动认证

#### 验证
- 基于规则的反馈（代码检查）
- 视觉反馈（通过 Playwright MCP 的截图）
- LLM-as-judge

### 支持的 Agent 类型
- 金融 Agent
- 个人助手
- 客户支持
- 深度研究 Agent

## 实践启示

- Agent SDK 将 Claude Code 的能力从编码扩展到通用数字工作
- 给 Agent 提供与程序员相同的工具是最有效的方法
- 子 Agent 是处理复杂任务的关键模式
- MCP 生态提供了丰富的集成能力
- [Equipping Agents for the Real World with Agent Skills](equipping-agents-for-the-real-world-with-agent-skills.md) 的 Skills 可通过 SDK 集成，扩展 Agent 的领域专业知识
- [Beyond Permission Prompts](beyond-permission-prompts.md) 的沙箱架构为 SDK 中的 Agent 运行提供安全保障
