# Building Effective Agents

- **原文链接**: [Building effective agents](https://www.anthropic.com/engineering/building-effective-agents)
- **作者**: Erik Schluntz, Barry Zhang
- **发布日期**: 2024-12-19
- **标签**: #agent #架构模式 #workflow #ACI

## 核心观点

在与数十个团队合作构建 AI Agent 后，Anthropic 发现最成功的实现使用的是**简单、可组合的模式**，而非复杂框架。文章定义了"工作流"（Workflow，预定义代码路径）和"Agent"（LLM 动态指导自身过程）的区别，并提出了五种工作流模式和自主 Agent 的指导原则。

## 关键概念

### 基础构建块：增强型 LLM
所有 Agent 系统的起点是一个增强了检索、工具和记忆能力的 LLM。如何管理这个 LLM 的上下文生态，参见 [Effective Context Engineering for AI Agents](effective-context-engineering-for-ai-agents.md)。

### 五种工作流模式

1. **提示链 (Prompt Chaining)**: 将任务分解为顺序步骤，每步 LLM 处理上一步输出，步骤间有程序化"门"进行验证。适用于可清晰分解为固定子任务的场景。
2. **路由 (Routing)**: 对输入分类并导向专门的后续任务。关注点分离使每条路径拥有优化的提示。适用于不同类别需要分别处理的场景。
3. **并行化 (Parallelization)**: LLM 有时可以同时处理同一任务，并通过程序化方式聚合输出。两种变体：任务分割（将任务拆分为独立子任务并行执行）和投票（同一任务多次执行以获得多样化输出）。
4. **编排者-工作者 (Orchestrator-Workers)**: 中心 LLM 动态分解任务、委派给工作者 LLM、综合结果。子任务非预定义。这一模式在生产中的成功应用参见 [How We Built Our Multi-Agent Research System](how-we-built-our-multi-agent-research-system.md)。
5. **评估者-优化者 (Evaluator-Optimizer)**: 一个 LLM 生成响应，另一个提供评估和反馈，循环直到满足质量阈值。这一模式在 [Harness Design for Long-Running Application Development](harness-design-for-long-running-application-development.md) 中被发展为 Planner-Generator-Evaluator 三角色系统。

### 自主 Agent
基于环境反馈在循环中使用工具。它们独立计划、操作，并在每一步从环境获取"真实信号"（工具调用结果、代码执行输出）。关键警告：更高的成本和复合错误的可能性。

## 三大核心原则

1. **保持设计简洁** — 不要过度工程化
2. **优先透明性** — 展示计划步骤
3. **精心设计 Agent-计算机接口 (ACI)** — 通过充分的工具文档和测试来优化。ACI 的系统化设计方法论参见 [Writing Effective Tools for AI Agents](writing-effective-tools-for-ai-agents.md)。

## 关键洞察

来自 SWE-bench 的重要 ACI 洞察："我们实际上花在优化工具上的时间比优化整体提示还多。"例如：模型在使用相对文件路径时出错；切换到绝对文件路径后消除了错误。应将工具描述视为给初级开发者的文档字符串。这一洞察的详细实战案例参见 [Raising the Bar on SWE-bench Verified](raising-the-bar-on-swe-bench-verified.md)。
