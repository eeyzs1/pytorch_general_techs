# Agent 架构阅读路线

## 先读

- [Building Effective Agents](../anthropic/engineering/building-effective-agents.md)：Workflow 与 Agent 的基础区分，以及提示链、路由、并行化、编排者-工作者、评估者-优化者五种模式。
- [A Practical Guide to Building Agents](../openai/research/a-practical-guide-to-building-agents.md)：从模型、工具、指令、护栏四个维度理解 Agent 产品化。

## 进阶

- [How We Built Our Multi-Agent Research System](../anthropic/engineering/how-we-built-our-multi-agent-research-system.md)：生产级多 Agent 研究系统。
- [Harness Design for Long-Running Application Development](../anthropic/engineering/harness-design-for-long-running-application-development.md)：Planner / Generator / Evaluator 的长任务 Harness。
- [Harness Engineering](../openai/research/harness-engineering.md)：Agent-first 软件工程的极端案例。
- [Introducing GPT-5.5](../openai/research/introducing-gpt-5-5.md)：通用旗舰模型向长任务、computer use 和知识工作 Agent 收敛。
- [Work with Codex from Anywhere](../openai/research/work-with-codex-from-anywhere.md)：长任务 Agent 的跨设备监督与远程环境协作。

## 关键结论

- 简单、可组合的架构优先于复杂框架。
- 任务越长，越需要把规划、执行、评估和状态管理拆开。
- 真正的瓶颈会从代码生成转移到上下文质量、环境设计、可观测性和人类审核能力。
