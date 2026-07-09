# OpenAI Research & Engineering — 核心观点总结

> 汇总自 [OpenAI Research](https://openai.com/research/) 和 [OpenAI Blog](https://openai.com/index/) 的 69 篇文章，涵盖 2025 年 1 月至 2026 年 7 月。

## 一、总体脉络

OpenAI 的技术文章呈现四条并行的演进路径：

```
路径1（工程实践）: Agent 指南 → Codex/Operator → Harness Engineering → AgentKit → Codex 全面升级 → Codex 企业安全 → Codex 多角色 → AWS/Oracle 分发 → Codex 长视野
路径2（安全研究）: Model Spec → 指令层级 → CoT 监控 → CoT-Control → RL奖励信号分析 → Codex 安全部署实践 → 青少年安全 → 前沿治理 → GPT-5.6 安全栈 → Daybreak
路径3（平台生态）: Responses API → Apps SDK → ChatGPT 超级App → 计算机环境 → MCP 互操作 → 多平台沙箱 → AWS 企业分发 → 记忆系统 → 推理健康
路径4（科学+全栈）: GPT-Rosalind → 数学猜想 → 黑洞模拟 → 免疫学突破 → LifeSciBench → Daybreak 自主研究 → Jalapeño 自研芯片
```

工程路径继续向 Codex 工业化迈进：6 月推出 Codex 长视野任务白皮书 + 多角色插件 + OpenAI Partner Network（$150M 投资、目标 30 万认证顾问），HP Frontier 全企业级部署；Codex 在 OpenAI 内部已达 97.9% 活跃用户、99.8% 输出 token。6 月底 [Core Dump Epidemiology](core-dump-epidemiology-data-infrastructure-bug.md) 分享了 OpenAI 基础设施可靠性工程的关键范式——流行病学家式诊断，把看似一类的不可能崩溃分离为两个独立 bug（Azure 单台主机硬件损坏 + GNU libunwind 18 年竞态）。安全路径在 6 月发布 GPT-5.6 系列（Sol/Terra/Luna）+ 最强安全栈，引入 `max`/`ultra` 推理 effort；同时推出 Daybreak + Codex Security + GPT-5.5-Cyber + Patch the Planet——把网络安全从"找漏洞"推进到"从发现到修复的闭环"。平台路径 6 月发布 ChatGPT Enterprise 统一分析 + 支出控制 + 健康性能提升（2.3 亿周用户、71% 事实性问题下降）。科学路径 6 月底发布 [GeneBench-Pro](introducing-genebench-pro.md)——面向研究级计算生物学的"判断决策"基准（129 题、10 领域、合成数据），并发布 LifeSciBench 专家级基准 + 免疫学家案例 + Daybreak 自主发现 Linux/FreeBSD/OpenBSD 等数十个 0-day。基础设施层 6 月推出 Jalapeño 自研推理芯片（9 个月 ASIC 周期，2026 年底吉瓦级部署）。

## 二、六大核心主题

### 1. Agent 构建方法论与工具链

[A Practical Guide to Building Agents](a-practical-guide-to-building-agents.md) 奠定了理论基础——Agent 由模型、工具和指令三要素组成，护栏是必需品。[New Tools for Building Agents](new-tools-for-building-agents.md) 和 [New Tools and Features in the Responses API](new-tools-and-features-in-the-responses-api.md) 提供了底层 API（Web 搜索、文件搜索、Computer Use）和 Agents SDK。[The Next Evolution of the Agents SDK](the-next-evolution-of-the-agents-sdk.md) 新增 MCP 工具调用支持。[Introducing AgentKit](introducing-agentkit.md) 将工具链推向工业化——可视化设计、版本控制、内联评估。[Introducing GPT-5.3-Codex](introducing-gpt-5-3-codex.md) 和 [Introducing GPT-5.3-Codex-Spark](introducing-gpt-5-3-codex-spark.md) 补齐 Codex 的长任务与实时编码模型层。[Codex for (almost) everything](codex-for-almost-everything.md) 和 [Work with Codex from Anywhere](work-with-codex-from-anywhere.md) 则把 Codex 扩展到 Computer Use、移动端、Remote SSH、Hooks 和企业环境。[Codex-Maxxing for Long-Running Work](codex-maxxing-long-running-work.md) 系统阐述 Codex 用于长视野任务的实践方法——持久化工作区、可验证步骤、人类监督判断。

**核心洞察**: 从单 Agent 到多 Agent，从手写代码到 Harness Engineering，OpenAI 的 Agent 工具链在快速工业化。

### 2. Harness Engineering 与 Agent-First 开发

[Harness Engineering](harness-engineering.md) 是 OpenAI 最重要的工程贡献——3 名工程师用 Codex 零手写代码交付 100 万行产品。核心转变：人类从"编码者"变为"环境设计者"。[Building an AI-Native Engineering Team](building-an-ai-native-engineering-team.md) 描述了这种转变对团队的影响。[GPT-4.1 Prompting Guide](gpt-4-1-prompting-guide.md) 提供了 Agent 提示的具体技术。[Introducing GPT-5.5](introducing-gpt-5-5.md) 显示通用旗舰模型也在向长任务、computer use、知识工作和 agentic execution 收敛。[How Agents Are Transforming Work](how-agents-are-transforming-work.md) 用数据量化 Codex 的经济影响——80.6% 个人用户提交过 30 分钟+ 任务，研究部门用量 11 个月增长 56 倍。

**核心洞察**: 当 Agent 能处理全生命周期任务时，人类角色完全转向系统架构的"牧羊人"。构建时间、隐性知识显式化和可观测性是关键约束。

### 3. Agent 产品矩阵

| 产品 | 能力 | 对标 Anthropic |
|------|------|---------------|
| [Introducing Codex](introducing-codex.md) | 云端编码 Agent | Claude Code |
| [Codex Now Generally Available](codex-now-generally-available.md) | 编码 Agent GA + SDK | Claude Code GA |
| [Introducing GPT-5.3-Codex](introducing-gpt-5-3-codex.md) | Codex 专用长任务模型 | Claude Code 模型层 |
| [Work with Codex from Anywhere](work-with-codex-from-anywhere.md) | 移动端与远程环境协作 | Claude Code 远程/托管工作流 |
| [Codex for Every Role, Tool, Workflow](codex-for-every-role-tool-workflow.md) | 多角色插件 + Sites + Annotations | — |
| [OpenAI Frontier Models on AWS](openai-frontier-models-and-codex-are-now-available-on-aws.md) | AWS Bedrock 企业分发 | — |
| [OpenAI on Oracle Cloud](openai-on-oracle-cloud.md) | Oracle OCI 多云分发 | — |
| [OpenAI to Acquire Ona](openai-to-acquire-ona.md) | 持久化 Agent 执行能力 | — |
| [Introducing Operator](introducing-operator.md) | GUI 操作 Agent (CUA) | Computer Use |
| [Introducing Deep Research](introducing-deep-research.md) | 多步研究 Agent | Research Feature |

**核心洞察**: OpenAI 的 Agent 产品更偏消费者和企业级，Anthropic 的更偏开发者工具。Codex GA 的 10 倍使用量增长验证了市场需求。Codex App 标志着从终端工具到桌面命令中心的形态演进，300 万周活跃开发者是重要里程碑。OpenAI 内部 97.9% 用户使用 Codex、99.8% 输出 token 来自 Codex——这是 Agent 工具链成熟的标志。

### 4. 平台生态与超级应用

[New Tools for Building Agents](new-tools-for-building-agents.md) 发布了首批 Agent 构建块（Responses API + Agents SDK）。[Equipping the Responses API with a Computer Environment](equipping-the-responses-api-with-a-computer-environment.md) 为 Responses API 配备了完整计算机环境（Shell 工具 + 托管容器 + 服务端 Compaction + Agent Skills），标志着从"模型调用"到"系统级 Agent 执行"的转变。[Introducing Apps in ChatGPT](introducing-apps-in-chatgpt.md) 将 ChatGPT 转变为超级应用平台——8 亿用户可在对话中直接使用第三方应用。[Codex Now Generally Available](codex-now-generally-available.md) 标志着编码 Agent 进入生产。[The Next Evolution of the Agents SDK](the-next-evolution-of-the-agents-sdk.md) 采纳 MCP 开放协议实现跨平台互操作。[New Usage Analytics and Updated Spend Controls](chatgpt-enterprise-spend-controls.md) 在 Global Admin Console 中统一 ChatGPT + Codex 信用额度视图，按用户/产品/模型分解，让企业精细化管理 AI 部署。

**核心洞察**: ChatGPT 正从"聊天机器人"演变为"超级应用平台"。MCP 的采纳意味着 OpenAI 从封闭生态走向开放互操作。Codex 登陆 AWS Bedrock + Oracle Cloud + Dell + HP Frontier 标志着 OpenAI 从"自建分发"到"多云企业分发 + 合作伙伴生态"的战略转变。Dreaming V3 记忆系统让 ChatGPT 从被动存储转向主动推理记忆，是平台智能化的关键一步。

### 5. 安全与对齐研究

[Inside Our Approach to the Model Spec](inside-our-approach-to-the-model-spec.md) 定义了模型行为的公开框架。[Improving Instruction Hierarchy in Frontier LLMs](improving-instruction-hierarchy-in-frontier-llms.md) 解决提示注入防御。[How We Monitor Internal Coding Agents for Misalignment](how-we-monitor-internal-coding-agents-for-misalignment.md) 实践 CoT 监控。[Reasoning Models Struggle to Control Their Chains of Thought](reasoning-models-struggle-to-control-their-chains-of-thought.md) 证明了 CoT 监控的有效性。[Where the Goblins Came From](where-the-goblins-came-from.md) 追踪 RL 奖励信号偏差如何通过 SFT 数据飞轮传播。[Introducing OpenAI Privacy Filter](introducing-openai-privacy-filter.md) 把隐私过滤做成可本地运行的基础设施模型。[Strengthening Societal Resilience with Rosalind Biodefense](strengthening-societal-resilience-with-rosalind-biodefense.md) 展示了高能力生物模型的 trusted access 防御路线。[Running Codex Safely at OpenAI](running-codex-safely.md) 展示了企业内部 Codex 部署的多层次安全控制。[Building a Safe, Effective Sandbox to Enable Codex on Windows](building-codex-windows-sandbox.md) 详述了从零构建 Windows 沙箱的两代方案。[Advancing Youth Safety and Opportunity Through Global Leadership](advancing-youth-safety-and-opportunity-through-global-leadership.md) 在 G7 峰会前发布 9 项青少年 AI 安全原则，呼吁建立国际青少年 AI 安全研究所。[GPT-5.6 Preview System Card](gpt-5-6-preview-system-card.md) 发布"至今最强大的安全栈"——模型训练 + 激活分类器 + 实时监控 + 账户级信号 + 差异化访问 + 700,000+ A100e 小时自动 red team。[Daybreak: Tools for Securing Every Organization](daybreak-securing-the-world.md) 扩展 Daybreak 到大规模漏洞发现 + 修复闭环：Codex Security 已扫描 3000 万 commits、500K+ 自动确认修复；GPT-5.5-Cyber 在 CyberGym 上达 85.6%。[Patch the Planet](patch-the-planet.md) 把"AI + 专家研究员"直接送到开源维护者前，5 天冲刺已发现数百问题、合入数十补丁。

**核心洞察**: OpenAI 的安全策略是纵深防御——Model Spec（规范层）+ 指令层级（模型层）+ CoT 监控（运行时层）+ 工程沙箱（执行层）+ Agent 原生审计（可见性层）+ Trusted Access（访问层）+ 自动 Red Team（测试层）。推理模型 CoT 的不可控性反而是安全监控的优势。Windows 沙箱的构建证明了 Agent 安全在多平台部署中的工程挑战。Trusted Contact 和 Safety Summaries 标志着 AI 安全从"内容审核"扩展到"人机协作安全网"，ChatGPT 从被动工具转变为主动安全参与者。Content Provenance 的多层策略（C2PA + SynthID + 公共验证）是应对 AI 生成内容泛滥的系统性方案。Daybreak 把"防御 = 找 + 修 + 验证 + 部署"完整闭环，是 AI 安全工具工业化的标志。

### 6. 科学应用与基础设施

[Introducing GPT-Rosalind](introducing-new-capabilities-to-gpt-rosalind.md) 把生命科学 AI 提升到 Agent 级别。[An OpenAI Model Has Disproved a Central Conjecture in Discrete Geometry](model-disproves-discrete-geometry-conjecture.md) 是 80 年悬案的 AI 解答。[Using Codex to Simulate Black Holes](using-codex-to-simulate-black-holes.md) 展示 Codex 在天体物理学的应用。[Introducing LifeSciBench](introducing-life-sci-bench.md) 发布 750 任务专家级生命科学基准，覆盖 7 个工作流 + 7 个生物域，173 名 Ph.D. 科学家撰写，453 名独立专家审查。[Introducing GeneBench-Pro](introducing-genebench-pro.md) 是 6 月底发布的另一研究级基准——129 道合成计算生物学问题、10 个领域、21 个子领域，专注于"研究品味"（模糊数据 + 迭代实验 + 判断决策），与 LifeSciBench 互补。GPT-5.6 Sol 最高推理水平 28.7%（Pro 模式 31.5%），远高于开发初期的 GPT-5 (<5%)。[How GPT-5 Helped Immunologist Derya Unutmaz Solve a 3-Year-Old Mystery](gpt-5-immunology-mystery.md) 展示 GPT-5 Pro 作为科学合作者——解决 3 年未解的免疫学谜题，成功预测未发表实验结果。[Improving Health Intelligence in ChatGPT](improving-health-intelligence-in-chatgpt.md) 公布 2.3 亿周用户在 ChatGPT 咨询健康，GPT-5.5 Instant 健康性能接近 Thinking 模型，2 个月事实性问题下降 71%。[OpenAI and Broadcom Unveil LLM-Optimized Inference Chip](openai-broadcom-jalapeno-inference-chip.md) 推出 Jalapeño——OpenAI 首款自研 AI 加速器，9 个月 ASIC 周期，2026 年底吉瓦级部署。这是 OpenAI 全栈战略从模型到产品到芯片的关键一跳。[Core Dump Epidemiology: Fixing an 18-Year-Old Bug](core-dump-epidemiology-data-infrastructure-bug.md) 是基础设施层的可靠性工程案例——流行病学家式诊断方法把看似一类的不可能崩溃分离为两个独立 bug，为 Agent 时代的 C++ 基础设施工程提供范式。

**核心洞察**: 通用模型在专业科学领域已具竞争力——GPT-5 Pro 在免疫学、Codex 在天体物理学、Jalapeño 在 LLM 推理。LifeSciBench + GeneBench-Pro 标志着 AI 评估从"问答"到"完整研究工作流 + 判断决策"的进化。OpenAI 全栈战略进入芯片层——当模型、产品、芯片三层协同优化时，单位 token 成本大幅下降，使先进 AI 更易普及。基础设施可靠性工程进入"全人群诊断"时代——流行病学家 > 医生。

## 三、关键数据点

| 指标 | 数值 | 来源 |
|------|------|------|
| Harness Engineering 代码量 | ~100 万行 | [Harness Engineering](harness-engineering.md) |
| Harness Engineering 团队规模 | 3 名工程师 | 同上 |
| Harness Engineering PR 数量 | ~1,500 个 | 同上 |
| Codex 使用量增长 | 10 倍（5-10 月） | [Codex Now Generally Available](codex-now-generally-available.md) |
| ChatGPT 周活跃用户 | 8 亿+ | 同上 |
| AgentKit 构建时间（Ramp） | 数小时 | [Introducing AgentKit](introducing-agentkit.md) |
| AgentKit 评估开发周期缩短 | 50%+ | 同上 |
| AgentKit 准确率提升 | 30% | 同上 |
| Web 搜索准确率（GPT-4o） | 90%（SimpleQA） | [New Tools for Building Agents](new-tools-for-building-agents.md) |
| Deep Research 完成时间 | 数十分钟（人类需数小时） | [Introducing Deep Research](introducing-deep-research.md) |
| Codex 周活跃开发者 | 300 万+ | [Codex for (almost) everything](codex-for-almost-everything.md) |
| Codex 新增插件数 | 90+ | 同上 |
| GPT-5.3-Codex Terminal-Bench 2.0 | 66.9% | [Introducing GPT-5.3-Codex](introducing-gpt-5-3-codex.md) |
| GPT-5.3-Codex Spark 生成速度 | 1000+ tokens/s | [Introducing GPT-5.3-Codex-Spark](introducing-gpt-5-3-codex-spark.md) |
| GPT-5.1 后 goblin 使用量增长 | +175% | [Where the Goblins Came From](where-the-goblins-came-from.md) |
| Nerdy 人格占 ChatGPT 回复 | 2.5%（却占 goblin 提及的 66.7%） | 同上 |
| Nerdy 奖励信号 creature 偏好 | 76.2% 数据集正偏向 | 同上 |
| Codex 每周用户数 | 500 万+ | [Codex for Every Role](codex-for-every-role-tool-workflow.md) |
| Codex 新增角色插件 | 6 个（覆盖 62 应用 / 110 技能） | 同上 |
| Dreaming V3 事实回忆成功率 | 82.8%（2024 年为 41.5%） | [ChatGPT Memory Dreaming](chatgpt-memory-dreaming.md) |
| Dreaming V3 计算成本降低 | 约 5 倍 | 同上 |
| 语音 AI 首字节时间（美国） | ~500ms | [Low-Latency Voice AI](delivering-low-latency-voice-ai-at-scale.md) |
| ChatGPT 周活跃用户 | 9 亿+ | 同上 |
| 跨对话安全响应提升（GPT-5.5 Instant） | +52%（伤害他人）/ +39%（自残） | [Sensitive Conversations](chatgpt-recognize-context-in-sensitive-conversations.md) |
| Safety Summaries 质量评分 | 相关性 4.93/5, 事实性 4.34/5 | 同上 |
| GPT-5.6 Sol Terminal-Bench 2.1 | 91.9% | [Previewing GPT-5.6 Sol](previewing-gpt-5-6-sol.md) |
| GPT-5.6 Sol ExploitBench token 效率 | Mythos Preview 1/3 | 同上 |
| GPT-5.6 自动 red-team GPU 时长 | 700,000+ A100e | [GPT-5.6 Preview System Card](gpt-5-6-preview-system-card.md) |
| Codex Security 扫描 commits | 3000 万+ | [Daybreak](daybreak-securing-the-world.md) |
| Codex Security 扫描代码库 | 30,000+ | 同上 |
| Codex Security 人工确认修复 | 70,000+ | 同上 |
| Codex Security 自动确认修复 | 500,000+ | 同上 |
| GPT-5.5-Cyber CyberGym | 85.6%（vs GPT-5.5 81.8%） | 同上 |
| GPT-5.5-Cyber ExploitGym | 39.5%（vs GPT-5.5 25.95%） | 同上 |
| GPT-5.5-Cyber SEC-bench Pro | 69.8%（vs GPT-5.5 63.1%） | 同上 |
| Patch the Planet 5 天冲刺发现问题 | 数百 | [Patch the Planet](patch-the-planet.md) |
| Patch the Planet 5 天冲刺合入补丁 | 数十 | 同上 |
| Linux Kernel 指针泄露 PoC | 8 | 同上 |
| Linux Kernel 本地提权 exploit | 24 | 同上 |
| HTTP/2 Bomb 影响网站 | 880,000+ | 同上 |
| OpenAI 内部 Codex 活跃用户占比 | 97.9% | [How Agents Are Transforming Work](how-agents-are-transforming-work.md) |
| OpenAI 内部 Codex 输出 token 占比 | 99.8% | 同上 |
| 个人用户提交 30 分钟+ 任务比例 | 80.6% | 同上 |
| 个人用户提交 8 小时+ 任务比例 | 25.6% | 同上 |
| 非开发者增长（个体/组织/内部） | 137× / 189× / 12× | 同上 |
| 99 百分位日 Agent turn | 60+ 小时 | 同上 |
| LifeSciBench 任务数 | 750 | [LifeSciBench](introducing-life-sci-bench.md) |
| LifeSciBench 任务撰写科学家 | 173 | 同上 |
| LifeSciBench Rubric 准则数 | 19,020 | 同上 |
| LifeSciBench 多步推理任务占比 | 79% | 同上 |
| ChatGPT 周健康用户 | 2.3 亿 | [Improving Health](improving-health-intelligence-in-chatgpt.md) |
| 健康事实性问题下降（2 个月） | 71% | 同上 |
| 医生审查回答数 | 70 万+ | 同上 |
| OpenAI Partner Network 投资 | $150M | [Partner Network](introducing-openai-partner-network.md) |
| 认证顾问目标（2026 年底） | 300,000 | 同上 |
| HP 工程师 PR 数（几周内） | 122（43 项目） | [HP Frontier](hp-frontier-partnership.md) |
| HP 安全团队产能解锁 | ~82 小时/周 | 同上 |
| Jalapeño 设计到 tape-out | 9 个月 | [Jalapeño](openai-broadcom-jalapeno-inference-chip.md) |
| Jalapeño 部署规模 | 吉瓦级（2026 年底起） | 同上 |
| Trusted Access for Cyber 国家 | 8+（澳/加/法/德/日/韩/ENISA/英国） | [Daybreak](daybreak-securing-the-world.md) |
| GeneBench-Pro 任务数 | 129 | [GeneBench-Pro](introducing-genebench-pro.md) |
| GeneBench-Pro 覆盖领域 / 子领域 | 10 / 21 | 同上 |
| GeneBench-Pro 专家评审估算单题时长 | 20-40 小时 | 同上 |
| GeneBench-Pro 人类专家单题成本 | 数千美元 | 同上 |
| GeneBench-Pro 单题 AI 推理成本 | 数美元 | 同上 |
| GeneBench-Pro GPT-5.6 Sol（Pro）通过率 | 31.5% | 同上 |
| GeneBench-Pro 早期 GPT-5 通过率 | <5% | 同上 |
| GeneBench-Pro 测试时计算扩展倍数 | 6× | 同上 |
| Rockset 崩溃数（一年） | 不限（生产环境持续） | [Core Dump Epidemiology](core-dump-epidemiology-data-infrastructure-bug.md) |
| GNU libunwind 竞态条件年龄 | 18 年 | 同上 |
| Libunwind 竞态窗口 | 单一指令 | 同上 |
| Misaligned-stack 崩溃物理主机数 | 1 台（Azure） | 同上 |
| 病毒学 VirBench 最高模型准确率（Anthropic） | 91.3% | [Paving the Way for Agents in Biology](../../anthropic/research/agents-in-biology.md) |
| J-space 涌现特性数 | 5（可报告/可调控/用于推理/可重用/不参与日常处理） | [Global Workspace](../../anthropic/research/global-workspace.md) |

## 四、与 Anthropic 的对比

| 维度 | OpenAI | Anthropic |
|------|--------|-----------|
| 博客结构 | 分散在 /index/ 和 /research/ | 集中在 /engineering/ 和 /research/ |
| 工程方法论 | Harness Engineering | Context Engineering → Harness Engineering |
| 上下文管理 | AGENTS.md | CLAUDE.md + Skills |
| 安全策略 | 指令层级 + CoT 监控 + RL 奖励审计 + 工程沙箱 + Agent 原生遥测 + Trusted Access | 沙箱隔离 + 双重隔离 + 事后分析 + Auto Mode 分类器 + Constitutional Classifiers |
| 工具生态 | Shell 工具 + 内置工具 + MCP 采纳 | 开放（MCP 协议） |
| 评估 | Evals 平台 + AgentKit 内联 + LifeSciBench | 8 步路线图 + LLM-as-judge + NLA |
| 产品定位 | 消费者 + 企业 + 开发者 | 开发者为主 |
| 网络安全 | Daybreak + Codex Security + GPT-5.5-Cyber + Patch the Planet | Project Glasswing + N-day exploits + ATT&CK Navigator + Mythos Preview |
| 科学应用 | 案例研究（免疫学、黑洞）+ LifeSciBench | 自主研究（NMR、病毒检索） |
| 自研芯片 | Jalapeño（与 Broadcom 合作） | 无 |
| 经济研究 | Codex 影响力论文（自家产品） | Economic Index（独立报告系列） |

## 五、贯穿始终的原则

1. **从最强模型开始**: 先用最强模型建立基线，再优化成本和延迟
2. **护栏不是可选的**: 从输入过滤到人机协作，安全是每层都需要的
3. **环境设计 > 代码编写**: Harness Engineering 的核心——设计让 Agent 可靠运行的环境
4. **隐性知识显式化**: 高级工程师的"隐性知识"必须写入文档和测试
5. **CoT 可监控性是安全基础**: 推理模型的思维链是安全监控的窗口
6. **工业化 Agent 开发**: 从手工作坊到可视化设计、版本控制、内联评估
7. **平台化是终局**: ChatGPT 从聊天机器人到超级应用平台，8 亿用户是生态基础
8. **奖励信号审计至关重要**: RL 训练中的微小奖励偏差可通过 SFT 数据飞轮在多个模型代际间放大，需建立系统化的行为审计工具
9. **Agent 原生审计是安全的最后防线**: 传统安全日志只能回答"发生了什么"，Agent 原生遥测才能解释"为什么"和"用户意图"
10. **多平台安全是 Agent 部署的基础工程挑战**: Windows 等平台缺乏原生沙箱工具，需从 OS 原语层构建安全执行环境
11. **从"找漏洞"到"修漏洞"**: 瓶颈已转移，AI 把发现做得太好，闭环修复是新前沿
12. **全栈战略进入芯片层**: 当模型、产品、芯片三层协同优化时，单位 token 成本大幅下降
13. **企业 AI 进入合作伙伴生态阶段**: 从"自建直销"到"全球合作伙伴 + Forward Deployed + 多专业认证"
14. **持久化是长视野任务的关键**: Agent 不只是单次 prompt-response，需要维持跨 session 的状态和决策

## 六、文章索引

| # | 日期 | 文章 | 主题 |
|---|------|------|------|
| 1 | 2025 | [A Practical Guide to Building Agents](a-practical-guide-to-building-agents.md) | Agent / 实践指南 |
| 2 | 2025 | [Building an AI-Native Engineering Team](building-an-ai-native-engineering-team.md) | AI原生团队 / 工程文化 |
| 3 | 2025-01（2025-07 更新：集成到 ChatGPT 作为 ChatGPT Agent） | [Introducing Operator](introducing-operator.md) | Computer-Use / CUA |
| 4 | 2025-02-02 | [Introducing Deep Research](introducing-deep-research.md) | 深度研究 / 研究Agent |
| 5 | 2025-03-11 | [New Tools for Building Agents](new-tools-for-building-agents.md) | Responses-API / Agents-SDK |
| 6 | 2025-03（持续更新） | [New Tools and Features in the Responses API](new-tools-and-features-in-the-responses-api.md) | Responses-API / Web搜索 |
| 7 | 2025-04 | [GPT-4.1 Prompting Guide](gpt-4-1-prompting-guide.md) | 提示工程 / GPT-4.1 |
| 8 | 2025-05 | [Introducing Codex](introducing-codex.md) | Codex / 编码Agent |
| 9 | 2025-10-06 | [Introducing Apps in ChatGPT and the New Apps SDK](introducing-apps-in-chatgpt.md) | Apps-SDK / ChatGPT应用 |
| 10 | 2025-10-06（与 DevDay 2025 同日） | [Codex Now Generally Available](codex-now-generally-available.md) | Codex-GA / Slack集成 |
| 11 | 2026-02 | [Harness Engineering: Building the Codex App Server for an Agent-First World](harness-engineering.md) | Harness工程 / Codex |
| 12 | 2026-02-02（3月4日更新：Windows 版上线） | [Introducing the Codex App](introducing-the-codex-app.md) | Codex / 桌面应用 |
| 13 | 2026-02-05 | [Introducing GPT-5.3-Codex](introducing-gpt-5-3-codex.md) | Codex / GPT-5.3-Codex |
| 14 | 2026-02-12 | [Introducing GPT-5.3-Codex-Spark](introducing-gpt-5-3-codex-spark.md) | Codex / GPT-5.3-Codex-Spark |
| 15 | 2026-03 | [Equipping the Responses API with a Computer Environment](equipping-the-responses-api-with-a-computer-environment.md) | ResponsesAPI / Shell工具 |
| 16 | 2026-03-05 | [Reasoning Models Struggle to Control Their Chains of Thought, and That's Good](reasoning-models-struggle-to-control-their-chains-of-thought.md) | CoT-Control / 思维链 |
| 17 | 2026-03-10 | [Improving Instruction Hierarchy in Frontier LLMs](improving-instruction-hierarchy-in-frontier-llms.md) | 指令层级 / IH-Challenge |
| 18 | 2026-03-19 | [How We Monitor Internal Coding Agents for Misalignment](how-we-monitor-internal-coding-agents-for-misalignment.md) | 对齐监控 / CoT监控 |
| 19 | 2026-03-25 | [Inside Our Approach to the Model Spec](inside-our-approach-to-the-model-spec.md) | Model-Spec / 模型行为 |
| 20 | 2026-04 | [Introducing AgentKit](introducing-agentkit.md) | AgentKit / Agent-Builder |
| 21 | 2026-04-15 | [The Next Evolution of the Agents SDK](the-next-evolution-of-the-agents-sdk.md) | Agents-SDK / MCP |
| 22 | 2026-04-17 | [Codex for (almost) Everything](codex-for-almost-everything.md) | Codex / 重大升级 |
| 23 | 2026-04-22 | [Introducing OpenAI Privacy Filter](introducing-openai-privacy-filter.md) | 隐私 / PII |
| 24 | 2026-04-23 | [Introducing GPT-5.5](introducing-gpt-5-5.md) | GPT-5.5 / AgenticAI |
| 25 | 2026-04-23 | [GPT-5.5 System Card](gpt-5-5-system-card.md) | GPT-5.5 / SystemCard / 安全 |
| 26 | 2026-04-29 | [Where the Goblins Came From](where-the-goblins-came-from.md) | 模型行为 / RL训练 |
| 27 | 2026-05-04 | [How OpenAI Delivers Low-Latency Voice AI at Scale](delivering-low-latency-voice-ai-at-scale.md) | VoiceAI / WebRTC / 基础设施 |
| 28 | 2026-05-05 | [GPT-5.5 Instant System Card](gpt-5-5-instant-system-card.md) | GPT-5.5-Instant / SystemCard |
| 29 | 2026-05-05 | [GPT-5.5 Instant: Smarter, Clearer, and More Personalized](gpt-5-5-instant.md) | GPT-5.5-Instant / ChatGPT |
| 30 | 2026-05-05 | [Advancing Youth Safety and Wellbeing in EMEA](advancing-youth-safety-in-emea.md) | 青少年安全 / EMEA / 资助 |
| 31 | 2026-05-05 | [Supercomputer Networking to Accelerate Large Scale AI Training](mrc-supercomputer-networking.md) | 网络 / 超级计算机 / MRC |
| 32 | 2026-05-07 | [Advancing Voice Intelligence with New Models in the API](advancing-voice-intelligence-with-new-models-in-the-api.md) | VoiceAI / RealtimeAPI |
| 33 | 2026-05-07 | [Introducing Trusted Contact in ChatGPT](introducing-trusted-contact-in-chatgpt.md) | ChatGPT / 安全 / 心理健康 |
| 34 | 2026-05-08 | [Running Codex Safely at OpenAI](running-codex-safely.md) | Codex / 安全 / 沙箱 |
| 35 | 2026-05-13 | [Building a Safe, Effective Sandbox to Enable Codex on Windows](building-codex-windows-sandbox.md) | Codex / Windows / 沙箱 |
| 36 | 2026-05-14 | [Work with Codex from Anywhere](work-with-codex-from-anywhere.md) | Codex / 移动端 / RemoteSSH |
| 37 | 2026-05-14 | [Helping ChatGPT Better Recognize Context in Sensitive Conversations](chatgpt-recognize-context-in-sensitive-conversations.md) | ChatGPT / 安全 / 上下文感知 |
| 38 | 2026-05-18 | [OpenAI and Dell Technologies Partner to Bring Codex to Hybrid and On-Premises Enterprise Environments](dell-codex-enterprise-partnership.md) | Codex / Enterprise / Dell |
| 39 | 2026-05-19 | [Advancing Content Provenance](advancing-content-provenance.md) | 内容溯源 / C2PA / SynthID |
| 40 | 2026-05-20 | [An OpenAI Model Has Disproved a Central Conjecture in Discrete Geometry](model-disproves-discrete-geometry-conjecture.md) | 数学 / ResearchMilestone |
| 41 | 2026-05-22 | [OpenAI Named a Leader in Enterprise Coding Agents by Gartner](gartner-2026-agentic-coding-leader.md) | Codex / Enterprise / Gartner |
| 42 | 2026-05-29 | [Strengthening Societal Resilience with Rosalind Biodefense](strengthening-societal-resilience-with-rosalind-biodefense.md) | 生物安全 / Rosalind |
| 43 | 2026-06-01 | [OpenAI Frontier Models and Codex Are Now Available on AWS](openai-frontier-models-and-codex-are-now-available-on-aws.md) | AWS / Bedrock / Codex / 企业 |
| 44 | 2026-06-02 | [Advancing Youth Safety and Opportunity Through Global Leadership](advancing-youth-safety-and-opportunity-through-global-leadership.md) | 青少年安全 / G7 / 治理 |
| 45 | 2026-06-03 | [Introducing New Capabilities to GPT-Rosalind](introducing-new-capabilities-to-gpt-rosalind.md) | GPT-Rosalind / 生命科学 |
| 46 | 2026-06-04 | [Dreaming: Better Memory for a More Helpful ChatGPT](chatgpt-memory-dreaming.md) | ChatGPT / Memory / DreamingV3 |
| 47 | 2026-06-08 | [Built to Benefit Everyone: Our Plan](built-to-benefit-everyone-our-plan.md) | 战略 / AGI / 三阶段 |
| 48 | 2026-06-08 | [Confidential Submission of Draft S-1 to the SEC](openai-submits-confidential-s-1.md) | IPO / SEC / 公司治理 |
| 49 | 2026-06-08 | [Introducing the OpenAI Economic Research Exchange](economic-research-exchange.md) | 经济研究 / AI经济影响 |
| 50 | 2026-06-10 | [Access OpenAI Models and Codex Through Your Oracle Cloud Commitment](openai-on-oracle-cloud.md) | Oracle / OCI / 多云分发 |
| 51 | 2026-06-11 | [OpenAI to Acquire Ona](openai-to-acquire-ona.md) | 收购 / Codex / 持久化Agent |
| 52 | 2026-06-11 | [How an Astrophysicist Uses Codex to Help Simulate Black Holes](using-codex-to-simulate-black-holes.md) | Codex / 天体物理 / 应用AI |
| 53 | 2026-06-12 | [New OpenAI Academy Courses for the Next Era of Work](academy-courses-applying-ai-at-work.md) | OpenAI-Academy / AI培训 / Agent工作流 |
| 54 | 2026-06-14 | [Introducing the OpenAI Partner Network](introducing-openai-partner-network.md) | PartnerNetwork / 企业 / 咨询 |
| 55 | 2026-06-17 | [Introducing LifeSciBench](introducing-life-sci-bench.md) | LifeSciBench / 生命科学 / 评估 |
| 56 | 2026-06-18 | [New Usage Analytics and Updated Spend Controls for Enterprises](chatgpt-enterprise-spend-controls.md) | ChatGPTEnterprise / AdminConsole |
| 57 | 2026-06-18 | [Improving Health Intelligence in ChatGPT](improving-health-intelligence-in-chatgpt.md) | ChatGPT / Health / HealthBench |
| 58 | 2026-06-22 | [Daybreak: Tools for Securing Every Organization in the World](daybreak-securing-the-world.md) | Daybreak / CodexSecurity / 网络安全 |
| 59 | 2026-06-22 | [Patch the Planet: A Daybreak Initiative](patch-the-planet.md) | Daybreak / OpenSource / 漏洞修复 |
| 60 | 2026-06-22 | [Codex-Maxxing for Long-Running Work](codex-maxxing-long-running-work.md) | Codex / LongRunningWork / WhitePaper |
| 61 | 2026-06-23 | [How GPT-5 Helped Immunologist Derya Unutmaz Solve a 3-Year-Old Mystery](gpt-5-immunology-mystery.md) | AppliedAI / GPT-5 / 免疫学 |
| 62 | 2026-06-24 | [OpenAI and Broadcom Unveil LLM-Optimized Inference Chip](openai-broadcom-jalapeno-inference-chip.md) | Infrastructure / Broadcom / Jalapeño |
| 63 | 2026-06-25 | [How Agents Are Transforming Work](how-agents-are-transforming-work.md) | EconomicResearch / Codex / 长视野任务 |
| 64 | 2026-06-26 | [Previewing GPT-5.6 Sol: A Next-Generation Model](previewing-gpt-5-6-sol.md) | GPT-5.6 / Sol / Terra / Luna |
| 65 | 2026-06-26 | [GPT-5.6 Preview System Card](gpt-5-6-preview-system-card.md) | GPT-5.6 / SystemCard / 安全栈 |
| 66 | 2026-06-28 | [HP Inc. Launches Frontier Strategic Partnership with OpenAI](hp-frontier-partnership.md) | HP / Frontier / 企业部署 |
| 67 | 2026-06-30 | [Introducing GeneBench-Pro](introducing-genebench-pro.md) | 计算生物学 / Benchmark / 专家级 |
| 68 | 2026-06-30 | [Core Dump Epidemiology: Fixing an 18-Year-Old Bug](core-dump-epidemiology-data-infrastructure-bug.md) | 基础设施可靠性 / 调试 / Libunwind |
| 69 | 2026-07-07 | （本同步记录） | 同步记录 |