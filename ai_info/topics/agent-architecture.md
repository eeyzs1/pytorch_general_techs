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

## 长视野任务与 Agent-first 团队

- [Codex-Maxxing for Long-Running Work](../openai/research/codex-maxxing-long-running-work.md)：持久化工作区、可验证步骤、人类监督判断。
- [How Agents Are Transforming Work](../openai/research/how-agents-are-transforming-work.md)：97.9% 内部用户、99.8% 输出 token、80.6% 提交 30 分钟+ 任务——Codex 在 OpenAI 内部的"全员 Agent"现状。
- [Previewing GPT-5.6 Sol](../openai/research/previewing-gpt-5-6-sol.md)：引入 `max` 与 `ultra` 推理 effort，让 Sol 通过子 Agent 协同处理复杂任务。
- [Building Self-Improving Tax Agents with Codex](../openai/research/building-self-improving-tax-agents-with-codex.md)：生产反馈驱动的 Agent 自改进循环。
- [Agentic Coding and Persistent Returns to Expertise](../anthropic/research/claude-code-expertise.md)：400K 会话分析——70% 规划决策由人、80% 执行决策由 Claude。
- [Project Fetch: Phase Two](../anthropic/research/project-fetch-phase-two.md)：通用 Agent 在物理机器人上比人类快 18-37 倍。
- [Brain2Qwerty v2](../meta/brain2qwerty-v2.md)：Agent 用于科研 pipeline 优化——Meta 用 AI Agent 自动探索脑信号解码 pipeline 的优化配置，最终训练配置由工程师手动选择。这是 Agent 在科学研究流程中的具体应用案例，体现"Agent 探索 + 人类决策"协作模式。
- [ChatGPT Work](../openai/research/chatgpt-work-partner.md)：ChatGPT 从"聊天助手"升级为跨应用、长时间陪伴的"工作伙伴"——能在用户应用和文件中采取行动，陪伴项目数小时，将目标转化为完成的工作。
- [Claude Plays Robotics](../anthropic/research/claude-plays-robotics.md)：系统评估 LLM 控制多种机器人的能力边界——控制抽象层级决定成败，预训练策略 + 高层规划是当前最优路径。
- [Kimi K2.6](../kimi/blog/kimi-k2-6.md)：开源编码 Agent 的长视野执行能力——12+ 小时连续执行、4000+ 工具调用、跨语言泛化（Rust/Go/Python），展示开源模型在真实工程任务中的成熟度。
- [DeepSeek-V4](../deepseek/news/deepseek-v4.md)：官方定位"Agent 能力大幅提高"——支持 Tool Calls、Chat Prefix Completion、FIM Completion，且官方文档明确 Claude Code / GitHub Copilot / OpenCode 可直接以 DeepSeek 为后端；1M 上下文 + 27% 计算量让长视野 Agent 工作负载成本重构。

## Agent 内部可观测性与审计

- [A Global Workspace in Language Models](../anthropic/research/global-workspace.md)：J-lens 可读出 Agent 内部"特权思维空间"（J-space）的内容——不仅能审计 Agent 的最终决策，还能审计它"在想什么"。可编辑 J-space 因果性地改变 Agent 行为，为 Agent 内部状态审计提供新工具。
- [Natural Language Autoencoders](../anthropic/research/natural-language-autoencoders.md)：NLA 把 Agent 内部激活翻译成自然语言——可用于审计 Agent 是否私下注意到自己被测试、是否捏造数据、是否追求隐藏目标。

## 关键结论

- 简单、可组合的架构优先于复杂框架。
- 任务越长，越需要把规划、执行、评估和状态管理拆开。
- 真正的瓶颈会从代码生成转移到上下文质量、环境设计、可观测性和人类审核能力。
- 领域专长而非编码能力是 Agent 时代的稀缺资源——编码能力被 Agent 吸收后，理解问题的人最有价值。
- 持久化工作区、可验证步骤、跨 session 状态延续是长视野任务的工程基础设施。
- Agent 内部可观测性是下一个工程前沿——J-lens / NLA 让"Agent 在想什么"变得可审计，与 Agent 行为的外部可观测性（日志、trace）形成互补。
- 物理 Agent 的控制抽象设计至关重要——直接驱动关节大多失败，预训练策略 + LLM 高层规划是可行路径。
- 跨应用、长时间陪伴是通用工作 Agent 的核心能力——ChatGPT Work 展示从"对话"到"工作伙伴"的演进。
- 开源编码 Agent 已具备生产级长视野执行能力——Kimi K2.6 的 12 小时连续执行和 4000+ 工具调用证明开源模型可处理真实复杂工程任务。