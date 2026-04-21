# Introducing Codex

- **原文链接**: [Introducing Codex](https://openai.com/index/introducing-codex/)
- **发布日期**: 2025-05
- **标签**: #Codex #编码Agent #codex-1 #云沙箱 #并行任务

## 核心观点

Codex 是 OpenAI 的云端 AI 软件工程 Agent，可将编码任务委派给它。基于 codex-1（o3 的软件工程优化版本），Codex 能在定制的云环境中并行编写功能、修复 Bug、提出 PR 和回答代码库问题。

## 关键概念

### codex-1 模型
- 基于 o3 推理模型，专门针对软件工程优化
- 在真实编码挑战上训练

### 云端沙箱执行
- 每个任务在隔离的云环境中运行
- 预加载用户仓库
- Codex 可读取、编辑和执行命令，不影响宿主系统

### 并行任务
- 可同时执行多个任务
- 编写功能、修复 Bug、提出 PR 可并行进行
- 使用 AGENTS.md 文件遵循项目特定标准

### Codex CLI
- 通过 npm 安装: `npm install -g @openai/codex`
- 命令行界面直接与 Agent 交互
- 支持本地文件系统操作

### DevDay 2025 扩展
- **Slack 集成**: 在 Slack 线程中 @Codex，自动获取上下文并完成任务
- **Codex SDK**: 将 CLI 的 Agent 能力嵌入自定义工作流
- **管理工具**: 工作区管理员可监控使用、强制环境控制、跟踪代码审查质量

## 实践启示

- Codex 代表了从"代码补全"到"自主编码 Agent"的演进
- 云端沙箱是安全并行执行的关键
- AGENTS.md 是项目级上下文的核心机制
- 与 Anthropic 的 Claude Code 有相似的架构理念

## 相关文章

- [Harness Engineering](harness-engineering.md) — Codex 的极限使用实验
- [A Practical Guide to Building Agents](a-practical-guide-to-building-agents.md) — Agent 构建方法论
- [Building an AI-Native Engineering Team](building-an-ai-native-engineering-team.md) — AI 原生工程团队
- [Introducing AgentKit](introducing-agentkit.md) — Agent 构建工具集
