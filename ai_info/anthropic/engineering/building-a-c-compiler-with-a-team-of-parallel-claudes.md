# Building a C Compiler with a Team of Parallel Claudes

- **原文链接**: [Building a C compiler with a team of parallel Claudes](https://www.anthropic.com/engineering/building-c-compiler)
- **发布日期**: 2026-02-05
- **标签**: #Agent-Teams #并行Agent #编译器 #任务声明 #大规模协作

## 核心观点

"Agent Teams" 是一种新的 LLM 监督方法——多个 Claude 实例在共享代码库上并行工作，无需主动人类干预。为压力测试此方法，作者让 16 个 Agent 从零开始编写一个基于 Rust 的 C 编译器，目标是能编译 Linux 内核。经过近 2,000 个 Claude Code 会话和 $20,000 的 API 成本，Agent 团队产出了一个 100,000 行的编译器，可在 x86、ARM 和 RISC-V 上构建 Linux 6.9。与 [How We Built Our Multi-Agent Research System](how-we-built-our-multi-agent-research-system.md) 的编排者-工作者模式不同，Agent Teams 采用去中心化协调——没有中心编排者，而是通过文件系统协调。

## 关键概念

### Agent Teams 架构
- 多个 Claude 实例并行工作在共享代码库上
- 无需主动人类干预
- 通过基于文件的任务声明机制协调。这种文件系统协调是 [Effective Context Engineering for AI Agents](effective-context-engineering-for-ai-agents.md) 中"结构化笔记"策略的变体——用文件系统替代上下文窗口进行通信

### Git-based 任务声明
- Agent 通过向 `current_tasks/` 目录写入文本文件来"锁定"任务
- 例如：一个 Agent 锁定 `current_tasks/parse_if_statement.txt`，另一个锁定 `current_tasks/fix_type_checking.txt`
- Git 同步防止重复工作

### Agent 专业化
不同 Agent 可承担不同角色：
- **核心开发 Agent**: 修复 Bug 和实现功能
- **文档 Agent**: 维护 README 和进度文件
- **代码质量 Agent**: 识别和合并重复代码

### 并行化的优势
- 16 个 Agent 并行运行，可同时调试多个 Bug 和实现功能
- 大幅扩展 LLM Agent 可实现的范围
- 不同 Agent 可同时处理不同模块

### 局限性
- 编译器已接近 Opus 4.6 的能力极限
- 新功能和 Bug 修复经常破坏现有功能
- 成本高昂（$20,000 API 费用）
- Token 消耗显著高于单会话

## 实践启示

- 从较小的团队（2-4 个 Agent）开始测试
- 在理解 Token 消耗模式后再扩展
- 使用基于文件的任务声明避免冲突
- Agent Teams 适合大型、可分解的项目
- 预算规划至关重要——大规模并行 Agent 消耗大量 Token
- [Effective Harnesses for Long-Running Agents](effective-harnesses-for-long-running-agents.md) 的进度跟踪机制（`claude-progress.txt`）与 Agent Teams 的任务声明机制异曲同工
- [Harness Design for Long-Running Application Development](harness-design-for-long-running-application-development.md) 的 Evaluator 角色可解决"新功能破坏现有功能"的问题——客观评分比 Agent 自我评估更可靠
- [Claude Code Best Practices](claude-code-best-practices.md) 的多 Claude 工作流（编写者+审阅者）是 Agent Teams 的轻量版
- [Scaling Managed Agents](scaling-managed-agents.md) 的 Brain/Hands/Session 解耦为 Agent Teams 提供了基础设施层的支撑
