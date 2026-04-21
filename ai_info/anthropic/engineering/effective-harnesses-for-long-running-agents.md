# Effective Harnesses for Long-Running Agents

- **原文链接**: [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)
- **作者**: Justin Young
- **发布日期**: 2025-11-26
- **标签**: #Harness #长时间运行 #初始化Agent #编码Agent #进度跟踪

## 核心观点

为使 Claude Agent SDK 在多个上下文窗口间有效工作，Anthropic 开发了双重解决方案：**初始化 Agent**（在首次运行时设置环境）和**编码 Agent**（在每个会话中推进增量进展，同时为下一个会话留下清晰的产物）。这是 [Effective Context Engineering for AI Agents](effective-context-engineering-for-ai-agents.md) 中"结构化笔记"和"压缩"技术在长时间运行场景下的实践——用文件系统作为外部记忆，在上下文重置后保持连续性。

## 关键概念

### 核心挑战
长时间运行的 Agent 面临上下文窗口限制——任务可能跨越多个会话，需要在会话间保持连续性。

### 初始化 Agent (Initializer Agent)
- 行为类似技术负责人
- 摄取广泛规格，检查仓库，枚举约束
- 输出结构化计划：具体任务、文件触碰列表、依赖说明和验收标准
- 该计划成为独立编码者的契约

### 编码 Agent (Coding Agent)
- 每个会话被提示运行一系列步骤来获取上下文：
  - 运行 `pwd` 查看当前目录
  - 检查项目结构
  - 读取进度文件了解已完成的工作
  - 继续推进增量进展
- 关键原则：**每个会话都必须取得增量进展**

### 进度跟踪机制
- `claude-progress.txt` 文件跟踪已完成的工作
- 测试状态维护在 JSON 文件中
- 功能检查清单跟踪实现进度
- Git 提交作为持久化的检查点

### 会话间连续性
- 进度文件、git 提交和功能检查清单确保 Agent 在上下文重置后可以恢复
- 每个 Agent 会话被视为同一项目上前一会话的延续

## 实践启示

- 将长时间运行任务分解为可增量的会话
- 使用文件系统作为 Agent 的外部记忆
- 初始化和执行分离是关键模式
- 进度跟踪文件是会话间连续性的基础
- [Harness Design for Long-Running Application Development](harness-design-for-long-running-application-development.md) 是本文的进阶版——从初始化/编码双角色发展到 Planner-Generator-Evaluator 三角色系统
- [Building Agents with the Claude Agent SDK](building-agents-with-the-claude-agent-sdk.md) 提供了 SDK 中的压缩和子 Agent 支持，是本文的技术基础
- [How We Built Our Multi-Agent Research System](how-we-built-our-multi-agent-research-system.md) 展示了多 Agent 协调的另一种模式——编排者-工作者而非初始化者-编码者
