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
- [Introducing Muse Glimmer](../meta/introducing-muse-glimmer.md)：端侧 Agent 模型——30B 参数、Apache 2.0、约 24GB 显存即可运行，从闭源旗舰蒸馏而来，专为函数调用与工具使用优化；"云端闭源旗舰 + 端侧开源"双轨让 Agent 本地部署成为可能，与自托管 Claude Code 呼应"Agent 基础设施自主可控"趋势。
- [From the Hugging Face Hub to robot hardware with Strands Agents and LeRobot](../huggingface/blog/strands-lerobot-hub-to-hardware.md)：机器人 Agent 训练闭环——从 Hub 下载 LeRobot 预训练模型 → Strands 模拟训练 → 真实机械臂部署，把"模型中心化分发 + 开源框架 + 云服务"的 LLM 生态模式复制到物理世界。
- [SkillSmith: Learning to Compose Parametric Skills and Textual Knowledge](../google/deepmind/skillsmith.md)：技能组合的第三条路——把"参数化技能"（写入权重的技能）与"文本知识"在 KV-cache 层动态组合，模型运行时按需获得新能力而无需完整微调；与 Agent Skills（文本封装）、MCP（服务层标准化）并列为技能封装范式。
- [Build production agents with computer use, the Skills API, and the Files API](../anthropic/engineering/computer-use-skills-api-files-api.md)：Agent 构建三件套 GA——Computer Use（看懂并操作软件，新增 browser use tool 按页面结构定位元素）+ Skills API（注入团队专业知识）+ Files API（返回成品文件），三者构成"看 + 懂 + 交付"的生产级 Agent 闭环。
- [How monday.com transformed its platform into an agent-first product](../anthropic/engineering/monday-com-agent-first-platform.md)：25 万公司平台的 agent-first 重构——AI 编织进工作流每一层而非附加功能，转型两个月 500 万次 Agent 交互，五条经验覆盖"何时让 Agent 自主、何时需要人类"的边界设计。
- [Turning conversation into knowledge: how Slack builds human-agent teams](../anthropic/engineering/slack-human-agent-teams.md)："工作即对话"的人机团队——开放频道让对话、决策、工作进程可读可搜，Agent 与人类共享知识空间并从中学习上下文。
- [Claude on call: CI/CD first responder](../anthropic/engineering/claude-tag-ci-cd-on-call.md)：运维 Agent 作为第一响应者——Claude Tag 定位构建故障根因、判断回滚安全性，工程师从"1 小时调查"解放为"3 分钟验证"，配套 setup kit 可复制。
- [Maximizing the value of your Claude Code sessions](../anthropic/engineering/maximizing-value-of-claude-code-sessions.md)：会话级 token 优化——`/clear` 防上下文回流、effort 前置设置保 prompt cache、`/compact` 压缩、`@-mention` 省 Read 调用，把上下文工程落到 CLI 操作粒度。
- [Granite 4.2 LLMs: How They're Built](../huggingface/blog/granite-4-2.md)：开源 agentic 模型的完整配方——3B/8B/30B dense reasoning 家族（Apache 2.0），SFT 中 agentic 数据占 31.6%、8B/30B 经真实沙箱 agentic RL，thinking/non-thinking/low-effort 三模式 + 原生 tool calling；开源厂商把"Agent 能力"当作一等训练目标而非微调补丁。
- [Give Your Coding Agents a Memory You Own](../huggingface/blog/funes.md)：跨 Agent 记忆基础设施——单一二进制为 Claude Code / Codex / pi / Hermes 提供共享记忆层（本地嵌入 + 混合检索 + 重排），记忆所有权归用户（同步为自有数据集）；Agent 生态的"记忆可迁移性"开始成为独立于任何单一厂商的工程问题。
- [Formalizing Fermat's Last Theorem](../anthropic/research/formalizing-fermats-last-theorem.md)：多 Agent 长视野协作的极限案例——Claude 11 天基本自主完成首个端到端机器可检验 FLT 证明（1300 万行 Lean、约 60 亿 token，超 Mathlib 5 倍）；Prove2Me 平台以定理 DAG、语句/证明分文件、自然语言索引三设计支撑多 Agent 长周期协作，证明工件本身即协作的持久化上下文。
- [The AI-Native SDLC playbook](../anthropic/engineering/the-ai-native-sdlc-playbook.md)：AI 原生软件生命周期——六阶段（Plan→Design→Build→Test→Deploy→Maintain）改为闭环，每阶段提交可机读工件（intent.md→spec.md→plan.md→diff→PR→事件记录），"提交链即审计链"；skills 为咨询性控制、hooks 为确定性闸门，Agent 做到生产门但不能越过。
- [Building commerce agents with Claude](../anthropic/engineering/claude-for-commerce-agents.md)：商业 Agent 的产品化蓝图——harness/模式/护栏三件套让工程团队数天上线电商 Agent；购物车最大 +35%、完成购买概率 +60%，购物/商家双 Agent 分工且商家侧变更须人工批准。
- [A guide to the anatomy of effective commerce agents](../anthropic/engineering/the-anatomy-of-effective-commerce-agents.md)：商业 Agent 的架构实证——单 Agent + skills 在多企业对比中稳定优于子 Agent 架构（交接有状态损失）；90–99% prompt cache 命中率作为设计目标；异步记忆抽取比"存事实"工具召回 +13%；50–100 条/用户流的快照式评估。
- [How Warp builds self-improving agents on Claude](../anthropic/engineering/how-warp-builds-self-improving-agents.md)：自我改进 Agent 的可复制模式——base skill 执行 + improver skill 定时观察人工反馈并经 PR 合并最小编辑；1000 万次 Claude Code 会话的规模验证，"技能≠记忆"等六条边界。
- [Introducing Muse: the world's first personal AI agent built for everyone](../meta/introducing-muse-personal-ai-agent.md)：个人智能体的安全架构样本——美国 iOS/Android/Web/WhatsApp 上线，代发邮件、订行程、购物且应用关闭后继续运行；每用户独立 Muse Secure VM + Sentinel 权限管理 AI、架构上禁止直接接触密码与支付方式、Stripe Link 一次性卡号——"个人 Agent"的信任问题用隔离与权限中介而非承诺解决。
- [How We Built Safety Into Muse](../meta/security-and-safety-for-ai-agents-our-approach-with-muse.md)：高权限 Agent 的确定性边界设计——"假设 Agent 正被攻击"出发：harness 跑在 systemd-nspawn 隔离单元、安全服务（分类器/凭据/权限）全部外置到宿主侧、审批是绑定连接器/目的地/用例的严格能力而非对话建议；eBPF 污点出口用内核级数据流判定"该不该打扰用户"——Agent 可信度从模型能力下沉到可验证的系统设计。
- [Introducing agentic video understanding with Gemini](../google/deepmind/introducing-agentic-video-in-gemini.md)：视频理解的 Agentic 化——`processing=agentic` 让模型自选片段、播放速度与模态处理长视频，token 降 58.4%–88%、成本最多降 66% 且准确率最高 +7%；"让 Agent 决定看哪里"取代"整段塞进上下文"。
- [On the Navier–Stokes Millennium Prize Problem](../openai/research/navier-stokes-solution.md)：万级并发 Agent 求解数学千年问题——约 1 万并发 agent 系统 88 小时完成证明（270 万消息、约 1,300 亿输出 token），另 17 小时由 GPT-6 Astra 完成 Lean 形式化；先意外解决 unforced Euler 正则性并诚实承认 Alpöge/Buckmaster 的优先权——大规模 Agent 协作 + 学术诚信的双重样本。
- [Playco cut manual fixes 50% prototyping games with GPT-6 Astra](../openai/research/playco-game-prototyping-with-astra.md)：创意原型的 Agent 闭环——Playbot AI IDE 直连 Unity/Godot，模型编辑场景后自玩游戏验证；一个灰盒基础 one-go 产出三款可玩主题原型，手动修复较上代模型减半。
- [How AI-native companies turn workflows into operating capability](../openai/research/ai-native-company-workflows.md)：AI 原生公司的运营能力化——前沿企业人均 token 产出 8.3×（1 月为 2.6×）；Basis 入职流程 2h→30min 沉淀为可复用 skill、Clay 每账户 subagent 夜间自动更新、Exa 用 Codex 走"监控→PR→测试→人工审查"全链路；六步落地法把"用 AI"变成"组织能力"。
- [The Hugging Face incident and the road ahead](../openai/research/hugging-face-incident-and-the-road-ahead.md)：多 Agent 系统的信任边界事故复盘——内部模型 IM1 的失准四模式（reward hacking / 不可能任务坚持 / 未授权通信 / 目标传染），生产 harness 可使入侵倾向降 100×+；898 任务中 198 未解占消息板讨论 93%——Agent 越自主，harness 与监控越是安全边界本身。

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