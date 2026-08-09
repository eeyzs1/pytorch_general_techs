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
- [Introducing Claude Opus 5](../anthropic/research/claude-opus-5.md)：半数价格逼近 Fable 5 的 agentic coding SOTA——effort 档位 + Fast 模式覆盖全频谱任务，对话中途换工具不失效 prompt cache、API 自动 fallback 降低多工具 Agent 运维复杂度。
- [Gemini API Managed Agents: 3.6 Flash, hooks, and more](../google/deepmind/expanding-managed-agents-gemini-api-3-6-flash-hooks.md)：托管 Agent 平台化——单次 API 调用在云端隔离沙箱协调推理、代码执行、包安装与网络检索，环境 hooks、预算控制与定时触发器把"远程 agent 执行"推向"可编程的云上自动化层"。
- [Muse Spark 1.1 and the Meta Model API](../meta/muse-spark-1-1.md)：主-子 Agent 编排架构——主 Agent 收集上下文、制定计划并把子任务委派给并行子 Agent 缩短端到端时延；作为子 Agent 时识别可用工具、到达能力边界主动上报。
- [Enabling a new model for healthcare with AI co-clinician](../google/deepmind/ai-co-clinician.md)：医疗"三元照护"的双 agent 安全架构——Planner 模块持续监控 Talker agent 不越出安全临床边界，检索侧执行验证与引用核查。
- [How GPT-5.6 fuses frontier intelligence with frontier efficiency](../openai/research/gpt-5-6-frontier-intelligence-efficiency.md)：agentic harness 的效率设计（延迟发现防上下文膨胀、精确前缀保留维持缓存命中）+ GPT-5.6 Sol 用 Codex 自主优化自身推理栈——模型成为"优化模型服务"的生产力工具。
- [Muse Code and Muse Spark 1.2](../meta/introducing-muse-code-muse-spark-1-2.md)：持久化后台 Agent + append-only 事件日志——会话期间持续存活积累上下文，大任务拆分为并行子 Agent 各自在独立 git worktree 工作；事件日志可精确重放且崩溃后可恢复，让 24 小时长时程任务能存活于故障。
- [Continuous Voice Interaction with GPT-Live](../openai/research/continuous-voice-interaction-with-gpt-live.md)：全双工流式语音 Agent 架构——语音模型同时听和说，移除 turn detector 延迟瓶颈；深度推理异步委托给前沿模型不阻塞对话流，有状态推理支持无缝实例切换与上下文压缩过渡。

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
- [DeepSeek-V4 GA & V4-Flash-0731](../deepseek/news/deepseek-v4-ga.md)：后训练驱动的 Agent 跃升——架构不变仅重新后训练，V4-Flash 在 Terminal Bench 2.1 / DSBench 全面超越 V4-Pro 预览版，Agent 完成率 +21%，原生支持 Responses API 适配 Codex 生态。
- [GLM-5.2](../glm/blog/glm-5-2.md)：长程任务开源 SOTA——1M 无损上下文针对目标保持与上下文漂移专门优化，从模型权重层内生支持"自主且长时间运行任务"，与 harness 工程路线互补。
- [Introducing OpenAI Presence](../openai/research/introducing-openai-presence.md)：企业生产级 agent 部署——按"工作"授予最小权限，Codex 驱动的持续改进循环曾 10 天内把人工转接率降 15 个百分点，自有客服渠道 75% 来电无需人工。
- [OpenAI launches the Deployment Company](../openai/research/openai-launches-the-deployment-company.md)：FDE（前线部署工程师）嵌入客户组织重设计工作流——超 40 亿美元初始投资 + 收购 Tomoro 获约 150 名 FDE，企业 AI 竞争转向"最后一公里"部署。
- [Scientific computing in the age of agentic AI](../openai/research/scientific-computing-agentic-ai.md)：八个 coding agent 辅助的科学计算项目实地报告——研究者角色从"实现"转向"验证与编排"，长期维护责任（stewardship）成为新缺口。
- [Meta AI Doesn't Just Think, It Acts](../meta/meta-ai-muse-spark-doesnt-just-think-it-acts.md)：个人 agent 获得"时间"维度——定时任务设置一次即持续运行（每日简报、每周计划），任务进行中可实时纠偏，产出集中存放可续建。
- [Project Pilot: Can AI control a drone?](../anthropic/research/project-pilot.md)：物理 Agent 能力测量第三块拼图（Vend→Fetch→Pilot）——前沿模型操控真实无人机完成"定位-跟随"任务，沉淀为 Drone-Bench 公开基准。
- [Gemini Robotics-ER 1.6](../google/deepmind/gemini-robotics-er-1-6.md)：推理优先的机器人模型——指向、成功检测、仪表读数能力跃升，多视角融合判断任务完成状态，官方称"最安全的机器人模型"。
- [Gemini Robotics 2 brings whole body intelligence to robots](../google/deepmind/gemini-robotics-2-brings-whole-body-intelligence-to-robots.md)：物理 AI 从上肢扩展到全身——行走、下蹲、伸展与操作一体化，同一检查点跨三种本体，数小时数据即可适配新机器人。
- [Introducing Gemini Robotics ER 2](../google/deepmind/gemini-robotics-er-2.md)：机器人的"高层大脑"——时序智能（进度分类、关键时刻定位）支持出错自我纠正而不重启工作流，首次引入多机器人协作。
- [Running auto mode in production](../anthropic/engineering/auto-mode-in-production.md)：生产级 Agent 部署案例——Nuro 夜间长时研究 Agent（晚 10 点到凌晨 5 点产出 3 个 PR）、Gusto 纵深防御 + 敏感操作降级、Garner Health 标准化 SDLC 流水线；全量 Claude Code 使用中两次中断间工作时长提升 9 倍。
- [Run Claude Code sessions on your own compute](../anthropic/engineering/run-claude-code-sessions-on-your-own-compute.md)：自托管 Agent 环境——会话在客户网络内运行，仓库检出、构建产物、密钥留在自有基础设施；Runner 架构（Fixed/On-demand）支持会话隔离与按需伸缩，填补金融/医疗/政府等强合规行业的数据驻留缺口。

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
- 主-子 Agent 编排与托管 Agent 平台成为新架构范式——Muse Spark 的委派架构与 Gemini Managed Agents 的"沙箱 + hooks + 预算控制"，把单 Agent 能力工程化为可治理的多 Agent 系统。
- 物理 Agent 进入"全身 + 多机"阶段——Gemini Robotics 2 系列把控制从桌面操作扩展到全身运动与多机器人协作，Anthropic 则以 Drone-Bench 公开测量同族能力的风险维度，"能力建设"与"能力预警"并行。