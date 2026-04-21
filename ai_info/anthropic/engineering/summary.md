# Anthropic Engineering Blog — 核心观点总结

> 汇总自 [Anthropic Engineering](https://www.anthropic.com/engineering) 博客的 21 篇文章，涵盖 2024 年 9 月至 2026 年 4 月。

## 一、总体脉络

Anthropic 的工程博客呈现了一条清晰的技术演进路径：

```
提示工程 → 上下文工程 → Harness 工程 → 基础设施解耦
```

从最初关注如何写好单个提示，到管理整个 Agent 的上下文生态，再到设计长时间运行的多角色 Harness 系统，最终到将 Agent 的推理、执行和状态解耦为可独立演进的基础设施层——这反映了 AI Agent 从简单工具到自主系统再到可扩展基础设施的演进。

## 二、七大核心主题

### 1. Agent 架构模式

[Building Effective Agents](building-effective-agents.md) 奠定了理论基础，定义了 Workflow（预定义路径）和 Agent（动态指导）的区别，提出了五种工作流模式。[How We Built Our Multi-Agent Research System](how-we-built-our-multi-agent-research-system.md) 展示了编排者-工作者模式在生产中的成功应用（90.2% 提升）。[Harness Design for Long-Running Application Development](harness-design-for-long-running-application-development.md) 将架构推向了 GAN 启发的 Planner-Generator-Evaluator 三角色系统。[Building a C Compiler with a Team of Parallel Claudes](building-a-c-compiler-with-a-team-of-parallel-claudes.md) 展示了 16 个 Agent 并行协作的极限——从零构建 10 万行编译器。[Scaling Managed Agents](scaling-managed-agents.md) 将架构推向了基础设施层——Brain/Hands/Session 三层解耦。

**核心洞察**: 最成功的 Agent 实现使用简单、可组合的模式，而非复杂框架。保持简洁是第一原则。但随着规模扩大，解耦和专业化成为必需。

### 2. 上下文工程

[Effective Context Engineering for AI Agents](effective-context-engineering-for-ai-agents.md) 是最重要的概念性贡献——从"提示工程"到"上下文工程"的范式转变。核心原则：**找到最小可能的高信号 token 集合**。每个 token 都在消耗模型有限的注意力预算。

关键技术：
- **压缩 (Compaction)**: 接近限制时总结对话
- **结构化笔记**: Agent 定期持久化笔记到外部记忆
- **子 Agent 架构**: 专门子 Agent 返回浓缩摘要
- **即时检索**: 维护轻量标识符，运行时动态加载

[Introducing Contextual Retrieval](introducing-contextual-retrieval.md) 提供了检索优化的具体技术（Contextual Embeddings + BM25 + 重排序，失败率降低 67%）。

### 3. 工具设计

[Writing Effective Tools for AI Agents](writing-effective-tools-for-ai-agents.md) 提出了五大原则：选择正确工具、命名空间、返回有意义上下文、优化 Token 效率、提示工程化描述。关键发现：**花在优化工具上的时间比优化提示还多**。

[Advanced Tool Use](advanced-tool-use.md) 引入了三大 Beta 特性（Tool Search Tool、Programmatic Tool Calling、Tool Use Examples），解决了工具规模化的 Token 问题。[Code Execution with MCP](code-execution-with-mcp.md) 将 Token 优化推到极致——98.7% 的减少。

### 4. 安全与可靠性

[Beyond Permission Prompts](beyond-permission-prompts.md) 确立了"安全是自主性前提"的原则——文件系统隔离 + 网络隔离的双重沙箱架构。[A Postmortem of Three Recent Issues](a-postmortem-of-three-recent-issues.md) 揭示了基础设施 Bug 如何伪装成模型退化。[Quantifying Infrastructure Noise in Agentic Coding Evals](quantifying-infrastructure-noise-in-agentic-coding-evals.md) 量化了基础设施配置对基准测试的影响（6 个百分点差距）。

### 5. 评估框架

[Demystifying Evals for AI Agents](demystifying-evals-for-ai-agents.md) 提供了最全面的评估指南。核心信息：**评估是公司的知识产权和竞争优势**。三种评分器（代码、模型、人类）各有适用场景。能力评估和回归评估应分开管理。8 步路线图从 20-50 个真实失败任务开始。

### 6. 开发者工具生态

[Claude Code Best Practices](claude-code-best-practices.md) 的 CLAUDE.md 模式是上下文工程的核心实践。[Equipping Agents for the Real World with Agent Skills](equipping-agents-for-the-real-world-with-agent-skills.md) 的渐进式披露使 Skill 的上下文量无上限。[Desktop Extensions](desktop-extensions.md) 降低了 MCP 的使用门槛。[Building Agents with the Claude Agent SDK](building-agents-with-the-claude-agent-sdk.md) 将编码能力扩展到通用数字工作。[The Think Tool](the-think-tool.md) 提供了 Agent 执行中的思考检查点。

### 7. Agent 规模化与基础设施

[Building a C Compiler with a Team of Parallel Claudes](building-a-c-compiler-with-a-team-of-parallel-claudes.md) 证明了大规模并行 Agent 协作的可行性——16 个 Agent、2000 个会话、$20,000 成本产出 10 万行编译器。[Scaling Managed Agents](scaling-managed-agents.md) 提出了基础设施层的解耦架构：Brain（推理）、Hands（执行）、Session（状态）三层独立演进，接口比实现更持久。p50 延迟降低 60%，p95 降低 90%+。

**核心洞察**: Agent 从应用层工具演进为基础设施层服务。解耦是规模化的关键——推理、执行、状态必须独立演进。

## 三、关键数据点

| 指标 | 数值 | 来源 |
|------|------|------|
| 多 Agent vs 单 Agent 提升 | 90.2% | [How We Built Our Multi-Agent Research System](how-we-built-our-multi-agent-research-system.md) |
| Token 使用解释性能差异 | 80% | 同上 |
| 工具描述优化降低任务完成时间 | 40% | [Writing Effective Tools for AI Agents](writing-effective-tools-for-ai-agents.md) |
| Tool Search Tool Token 减少 | 85% (77K→8.7K) | [Advanced Tool Use](advanced-tool-use.md) |
| 代码执行 MCP Token 减少 | 98.7% (150K→2K) | [Code Execution with MCP](code-execution-with-mcp.md) |
| Contextual Retrieval 失败率降低 | 67% | [Introducing Contextual Retrieval](introducing-contextual-retrieval.md) |
| Think Tool 策略遵循改进 | 54% | [The Think Tool](the-think-tool.md) |
| 基础设施噪声基准差距 | 6 个百分点 | [Quantifying Infrastructure Noise in Agentic Coding Evals](quantifying-infrastructure-noise-in-agentic-coding-evals.md) |
| 并行工具调用研究时间减少 | 90% | [How We Built Our Multi-Agent Research System](how-we-built-our-multi-agent-research-system.md) |
| Managed Agents p50 延迟降低 | ~60% | [Scaling Managed Agents](scaling-managed-agents.md) |
| Managed Agents p95 延迟降低 | >90% | [Scaling Managed Agents](scaling-managed-agents.md) |
| Agent Teams C 编译器规模 | 10 万行 / $20K | [Building a C Compiler with a Team of Parallel Claudes](building-a-c-compiler-with-a-team-of-parallel-claudes.md) |

## 四、贯穿始终的原则

1. **简洁优先**: 做最简单有效的事。简单、可组合的模式胜过复杂框架。
2. **上下文是稀缺资源**: 每个 token 都有成本。上下文工程是 Agent 性能的关键杠杆。
3. **工具即接口**: ACI（Agent-Computer Interface）与 API 设计同等重要。工具描述应像给新员工的文档。
4. **评估驱动**: 从评估开始，评估是知识产权。评估驱动的迭代优于直觉驱动。
5. **安全是自主性的前提**: 没有安全保证的自主性是危险的。双重隔离是最低要求。
6. **渐进式披露**: 信息分层加载，上下文窗口保持精简。
7. **分离关注点**: 规划、执行、评估应分离。初始化和编码应分离。
8. **基础设施是一等公民**: 基础设施配置和 Bug 可以主导性能表现。

## 五、文章索引

| # | 日期 | 文章 | 主题 |
|---|------|------|------|
| 1 | 2024-09-19 | [Introducing Contextual Retrieval](introducing-contextual-retrieval.md) | RAG 检索优化 |
| 2 | 2024-12-19 | [Building Effective Agents](building-effective-agents.md) | Agent 架构模式 |
| 3 | 2025-01-06 | [Raising the Bar on SWE-bench Verified](raising-the-bar-on-swe-bench-verified.md) | ACI 优化实战 |
| 4 | 2025-03-20 | [The Think Tool](the-think-tool.md) | Agent 思考工具 |
| 5 | 2025-04-18 | [Claude Code Best Practices](claude-code-best-practices.md) | 编码工作流 |
| 6 | 2025-06 | [Desktop Extensions](desktop-extensions.md) | MCP 安装 |
| 7 | 2025-06-13 | [How We Built Our Multi-Agent Research System](how-we-built-our-multi-agent-research-system.md) | 多 Agent 架构 |
| 8 | 2025-09 | [A Postmortem of Three Recent Issues](a-postmortem-of-three-recent-issues.md) | 基础设施可靠性 |
| 9 | 2025-09-29 | [Effective Context Engineering for AI Agents](effective-context-engineering-for-ai-agents.md) | 上下文工程 |
| 10 | 2025-09-29 | [Building Agents with the Claude Agent SDK](building-agents-with-the-claude-agent-sdk.md) | Agent SDK |
| 11 | 2025-10-16 | [Equipping Agents for the Real World with Agent Skills](equipping-agents-for-the-real-world-with-agent-skills.md) | Agent Skills |
| 12 | 2025-10-20 | [Writing Effective Tools for AI Agents](writing-effective-tools-for-ai-agents.md) | 工具设计 |
| 13 | 2025-10-31 | [Beyond Permission Prompts](beyond-permission-prompts.md) | 安全沙箱 |
| 14 | 2025-11-04 | [Code Execution with MCP](code-execution-with-mcp.md) | 代码执行 |
| 15 | 2025-11-24 | [Advanced Tool Use](advanced-tool-use.md) | 高级工具特性 |
| 16 | 2025-11-26 | [Quantifying Infrastructure Noise in Agentic Coding Evals](quantifying-infrastructure-noise-in-agentic-coding-evals.md) | 基准噪声 |
| 17 | 2025-11-26 | [Effective Harnesses for Long-Running Agents](effective-harnesses-for-long-running-agents.md) | Harness 设计 |
| 18 | 2026-01-09 | [Demystifying Evals for AI Agents](demystifying-evals-for-ai-agents.md) | 评估框架 |
| 19 | 2026-02-05 | [Building a C Compiler with a Team of Parallel Claudes](building-a-c-compiler-with-a-team-of-parallel-claudes.md) | 并行 Agent Teams |
| 20 | 2026-03-24 | [Harness Design for Long-Running Application Development](harness-design-for-long-running-application-development.md) | 高级 Harness |
| 21 | 2026-04-10 | [Scaling Managed Agents](scaling-managed-agents.md) | 基础设施解耦 |
