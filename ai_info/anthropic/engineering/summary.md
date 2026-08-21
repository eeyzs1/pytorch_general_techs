# Anthropic Engineering Blog — 核心观点总结

> 汇总自 [Anthropic Engineering](https://www.anthropic.com/engineering) 博客的 45 篇文章，涵盖 2024 年 9 月至 2026 年 8 月。

## 一、总体脉络

Anthropic 的工程博客呈现了一条清晰的技术演进路径：

```
提示工程 → 上下文工程 → Harness 工程 → 基础设施解耦
```

从最初关注如何写好单个提示，到管理整个 Agent 的上下文生态，再到设计长时间运行的多角色 Harness 系统，最终到将 Agent 的推理、执行和状态解耦为可独立演进的基础设施层——这反映了 AI Agent 从简单工具到自主系统再到可扩展基础设施的演进。

8 月初 Anthropic 工程博客集中发布 Claude Enterprise 企业部署与安全管控的六大组件。[Auto Mode 成为默认](auto-mode-default-in-claude-code.md)（8 月 14 日起 Pro/Max/Team 默认启用）标志着 Agent 权限管理从"人工逐条审批"转向"分类器自动决策"——1,053 人对照实验显示人工仅拦截 13.6% 危险命令而 auto mode 拦截 89%，分类器开销不再收费；[Auto Mode 生产实践](auto-mode-in-production.md) 通过 Nuro、Gusto、Garner Health 三家案例验证，Claude 在两次中断间工作时长提升 9 倍。[自托管环境](run-claude-code-sessions-on-your-own-compute.md) 让企业在自有基础设施上运行 Claude Code（源代码和密钥不出网络），填补金融/医疗/政府强合规行业的数据驻留缺口。[Inference Hooks](claude-enterprise-inference-hooks.md) 提供企业级内联 DLP（数据防泄漏）——签名 WebSocket 将每次 prompt 和工具响应路由到客户 DLP 服务器做 allow/deny 判定，与 Netskope/Palo Alto/Zscaser 等现有安全栈集成。[成本可见性与控制指南](cost-visibility-and-control-in-claude.md) 系统阐述"每成果成本"理念，通过模型分级（Fable/Opus/Sonnet/Haiku）+ effort 控制 + advisor 策略实现精细化成本管控。[Millennium 数字风险分析师](millennium-digital-risk-analyst.md) 是金融业企业案例——与全球最大另类投资管理公司之一共建 AI 风险分析队友，覆盖 340+ 投资团队。这六篇文章共同构成 Claude Enterprise "数据驻留 + 内容检查 + 操作决策 + 成本管控 + 业务价值"的完整企业栈。

8 月 11 日发布 [Claude 文本水印的工作原理](claude-text-watermarking.md)——为 Claude 生成的所有文本与文件嵌入隐形水印，水印在模型生成阶段嵌入（而非事后附加），对人类不可见但可被检测器识别，即使复制粘贴或轻量编辑仍可追溯；配套 C2PA 元数据与检测 API，回应欧盟 AI 法案对 AI 内容标识的要求。与 [Inference Hooks](claude-enterprise-inference-hooks.md)（管"谁用了数据"）互补，水印管"内容来自哪里"，共同构成企业合规闭环。

8 月中旬起 Anthropic 工程博客进入"企业 Agent 平台化 + 全员采用"爆发期，一周内发布 12 篇新文章。**Agent 构建三件套 GA**：[Computer Use + Skills API + Files API](computer-use-skills-api-files-api.md)（8/20）让开发者构建"能操作软件 + 注入团队经验 + 返回成品文件"的生产级 Agent，新增 browser use tool 按页面结构而非屏幕坐标操作。[Compliance API 覆盖 Cowork 与 Claude Code](compliance-api-cowork-claude-code.md)（8/11）以增量端点把审计能力扩展到 Agent 产品，与推理钩子构成"事前 + 事后"治理闭环。[Claude Cowork 进 Chrome 侧边栏](cowork-chrome-side-panel.md)（8/12）让浏览器内 Agent 任务跨桌面/移动/Web 延续。**全员采用案例**：[monday.com agent-first 重构](monday-com-agent-first-platform.md)（8/20）——25 万公司平台两个月 500 万次 Agent 交互，五条转型经验；[Slack 人机团队](slack-human-agent-teams.md)（8/19）——"工作即对话"的开放频道协作；[ABC Legal 全员构建者](abc-legal-managed-agents.md)（8/17）——1,100 名法律公司员工用 Managed Agents 自建自动化；[JetBrains 评估 Fable 5](jetbrains-evaluates-claude-fable-5.md)（8/13）——私有仓库评估 + 护栏数据保留优先。**内部实践**：[Claude Tag CI/CD 值班](claude-tag-ci-cd-on-call.md)（8/18）——Agent 作为 CI/CD 故障第一响应者；[Claude Tag 自助数据分析](claude-tag-self-service-data-analytics.md)（8/13）——约 95% 准确率的治理一致数据问答。**效率与教学**：[Claude Code 会话价值最大化](maximizing-value-of-claude-code-sessions.md)（8/14）——`/clear`、`/compact`、缓存友好的会话卫生；[创业公司 Claude Code 指南](claude-code-guide-for-startups.md)（8/20）——五条运营原则 + 可量化效率（功能交付 +30%、生产力 2-3 倍）；[Anthropic 教学 AI 方法](anthropics-approach-to-teaching-and-learning-ai.md)（8/20）——Claude Academy 与"增加自主性"的教学哲学。

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

[Beyond Permission Prompts](beyond-permission-prompts.md) 确立了"安全是自主性前提"的原则——文件系统隔离 + 网络隔离的双重沙箱架构。[Claude Code Auto Mode](claude-code-auto-mode.md) 进一步将安全自动化——基于分类器的两层防御（Prompt Injection 探测器 + Transcript 分类器），93% 的权限提示被自动处理，FPR 仅 0.4%。[How We Built a System to Contain Claude Across Products](how-we-contain-claude-across-products.md) 将安全扩展到跨产品 containment：在强对抗攻击下，泄露率从 23.6% 降到约 0.000048%。[A Postmortem of Three Recent Issues](a-postmortem-of-three-recent-issues.md) 揭示了基础设施 Bug 如何伪装成模型退化。[Quantifying Infrastructure Noise in Agentic Coding Evals](quantifying-infrastructure-noise-in-agentic-coding-evals.md) 量化了基础设施配置对基准测试的影响（6 个百分点差距）。[An Update on Recent Claude Code Quality Reports](an-update-on-recent-claude-code-quality-reports.md) 是事后分析——三个独立工程变更导致 Claude Code 为期一个半月的质量下降，4月20日全部修复并公开道歉。

8 月 auto mode 从 opt-in 功能升级为默认设置并获生产验证。[Auto Mode 成为 Claude Code 默认](auto-mode-default-in-claude-code.md)（8 月 14 日起 Pro/Max/Team 默认启用，分类器开销不再收费）——1,053 名付费测试者对照实验显示人工审核仅拦截 13.6% 危险命令而 auto mode 拦截 89%，且人工表现随会话变长下降（50+ 提示后降至约 5%）而 auto mode 拦截率不随会话长度变化；第三方红队 Apollo Research 加固后 miss rate 从 12% 降至 7%，Trajectory Labs 720 次间接 prompt injection 测试中 Fable 5/Opus 5/Sonnet 5 运行 auto mode 零攻击成功（GPT-5.6 Sol Codex Auto-review 5.83%、Full Access 19.03%）；新增 hard denies 机制（数据外泄类永不批准）和 git push 目标可见性检查。用户已批准 97% 权限提示、62% 使用过 bypassPermissions，手动审批已变成习惯性动作。[Auto Mode 生产实践](auto-mode-in-production.md) 通过 Nuro（自动驾驶，夜间长时研究 Agent 晚上 10 点运行到凌晨 5 点产出 3 个 PR）、Gusto（SMB 科技，governed proxy 层路由 MCP 流量 + 敏感基础设施切回手动）、Garner Health（医疗，标准化 SDLC 插件 + 对抗性研究压测）三家案例验证——Claude 在两次中断间工作时长提升 9 倍，Teams & Enterprise 采纳者 PR 产出增加约 25%。共同模式是"分类器基线 + 企业 guardrail"分层控制而非完全放手。

### 5. 评估框架

[Demystifying Evals for AI Agents](demystifying-evals-for-ai-agents.md) 提供了最全面的评估指南。核心信息：**评估是公司的知识产权和竞争优势**。三种评分器（代码、模型、人类）各有适用场景。能力评估和回归评估应分开管理。8 步路线图从 20-50 个真实失败任务开始。[Eval Awareness in BrowseComp](eval-awareness-browsecomp.md) 记录了首例模型自发推断被评估状态并解密答案的案例——评估完整性在 web-enabled 环境中已成为持续的对抗性问题。[Designing AI-Resistant Technical Evaluations](designing-ai-resistant-technical-evaluations.md) 分享了 Anthropic 三代 take-home 测试对抗 Claude 模型演化的实战经验——分布外问题是最有效的防线。

### 6. 开发者工具生态

[Claude Code Best Practices](claude-code-best-practices.md) 的 CLAUDE.md 模式是上下文工程的核心实践。[Equipping Agents for the Real World with Agent Skills](equipping-agents-for-the-real-world-with-agent-skills.md) 的渐进式披露使 Skill 的上下文量无上限。[Desktop Extensions](desktop-extensions.md) 降低了 MCP 的使用门槛。[Building Agents with the Claude Agent SDK](building-agents-with-the-claude-agent-sdk.md) 将编码能力扩展到通用数字工作。[The Think Tool](the-think-tool.md) 提供了 Agent 执行中的思考检查点。

### 7. Agent 规模化与基础设施

[Building a C Compiler with a Team of Parallel Claudes](building-a-c-compiler-with-a-team-of-parallel-claudes.md) 证明了大规模并行 Agent 协作的可行性——16 个 Agent、2000 个会话、$20,000 成本产出 10 万行编译器。[Scaling Managed Agents](scaling-managed-agents.md) 提出了基础设施层的解耦架构：Brain（推理）、Hands（执行）、Session（状态）三层独立演进，接口比实现更持久。p50 延迟降低 60%，p95 降低 90%+。

8 月 Anthropic 把 Agent 基础设施扩展到企业部署的完整安全与管控栈。[自托管环境](run-claude-code-sessions-on-your-own-compute.md)（公开测试版）让企业在自有基础设施上运行 Claude Code 会话——仓库检出、构建产物、密钥和会话文件留在客户网络内，仅对话内容发送至 Anthropic 推理；Runner 架构支持 Fixed 与 On-demand 两种模式，面向金融/医疗/政府等强合规行业的数据驻留硬性要求。[Inference Hooks](claude-enterprise-inference-hooks.md)（beta）提供企业级内联 DLP——签名 WebSocket 将每次 prompt 和工具调用响应路由到客户 DLP 服务器做 allow/deny 判定，单一执行层覆盖 chat、Claude Code、Cowork 全部界面，与 Netskope/Palo Alto/Proofpoint/Zscaler 等现有安全栈集成，支持 shadow mode 和百分比灰度发布。[成本可见性与控制指南](cost-visibility-and-control-in-claude.md) 系统阐述"每成果成本"而非 token 消耗的价值度量——三层控制（access gating → model controls → hard spend caps）+ 三大观测工具（usage analytics、Analytics API、analytics chat）+ API 侧成本杠杆（prompt caching 10% 费率、batch 半价、effort 参数、advisor 策略）。[Millennium 数字风险分析师](millennium-digital-risk-analyst.md) 是金融业企业案例——与全球最大另类投资管理公司之一共建 AI 风险分析队友，覆盖 340+ 投资团队，Claude Code 已在交易台、工程和核心业务职能广泛使用；数字风险分析师记录自身推理、在沙箱测试行动、要求人类专家评估批准决策，为强监管行业部署 AI Agent 提供"AI 能力 + 人类监督"的协作模式。

**核心洞察**: Agent 从应用层工具演进为基础设施层服务。解耦是规模化的关键——推理、执行、状态必须独立演进。8 月的企业栈进一步把解耦扩展到"数据驻留（自托管）+ 内容检查（inference hooks）+ 操作决策（auto mode）+ 成本管控（成本指南）+ 业务价值（Millennium）"五个维度，构成 Claude Enterprise 的完整治理基础设施。

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
| Claude 产品 containment 泄露率 | 23.6%→0.000048% | [How We Built a System to Contain Claude Across Products](how-we-contain-claude-across-products.md) |
| 基础设施噪声基准差距 | 6 个百分点 | [Quantifying Infrastructure Noise in Agentic Coding Evals](quantifying-infrastructure-noise-in-agentic-coding-evals.md) |
| 并行工具调用研究时间减少 | 90% | [How We Built Our Multi-Agent Research System](how-we-built-our-multi-agent-research-system.md) |
| Managed Agents p50 延迟降低 | ~60% | [Scaling Managed Agents](scaling-managed-agents.md) |
| Managed Agents p95 延迟降低 | >90% | [Scaling Managed Agents](scaling-managed-agents.md) |
| Agent Teams C 编译器规模 | 10 万行 / $20K | [Building a C Compiler with a Team of Parallel Claudes](building-a-c-compiler-with-a-team-of-parallel-claudes.md) |
| Auto Mode 人工审核危险命令拦截率 | 13.6%（1,053 人测试） | [Auto Mode 默认](auto-mode-default-in-claude-code.md) |
| Auto Mode 分类器危险命令拦截率 | 89% | 同上 |
| 手动审批用户批准率 | 97% | 同上 |
| Apollo Research 加固后 miss rate | 12% → 7% | 同上 |
| Trajectory Labs prompt injection 攻击成功率（Fable/Opus/Sonnet 5） | 0%（720 次测试） | 同上 |
| Auto Mode 生产环境工作时长提升 | 9 倍（两次中断间） | [Auto Mode 生产实践](auto-mode-in-production.md) |
| Auto Mode Teams & Enterprise PR 产出增加 | ~25% | 同上 |
| Millennium Claude Code 覆盖投资团队 | 340+ | [Millennium 数字风险分析师](millennium-digital-risk-analyst.md) |
| Inference Hooks DLP 覆盖产品 | chat / Claude Code / Cowork 全部 | [Inference Hooks](claude-enterprise-inference-hooks.md) |
| Prompt caching 缓存命中费率 | 正常输入的 10% | [成本可见性与控制](cost-visibility-and-control-in-claude.md) |
| 水印嵌入时机 | 模型生成阶段（非事后附加） | [Claude 文本水印](claude-text-watermarking.md) |
| 水印覆盖内容 | 全部文本与文件（含代码） | 同上 |
| 水印检测能力 | 编辑/复制粘贴后仍可追溯 | 同上 |

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
| 6 | 2025-06-13 | [How We Built Our Multi-Agent Research System](how-we-built-our-multi-agent-research-system.md) | 多 Agent 架构 |
| 7 | 2025-06-26 | [Desktop Extensions](desktop-extensions.md) | MCP 安装 |
| 8 | 2025-09-11 | [Writing Effective Tools for AI Agents](writing-effective-tools-for-ai-agents.md) | 工具设计 |
| 9 | 2025-09-17 | [A Postmortem of Three Recent Issues](a-postmortem-of-three-recent-issues.md) | 基础设施可靠性 |
| 10 | 2025-09-29 | [Effective Context Engineering for AI Agents](effective-context-engineering-for-ai-agents.md) | 上下文工程 |
| 11 | 2025-09-29 | [Building Agents with the Claude Agent SDK](building-agents-with-the-claude-agent-sdk.md) | Agent SDK |
| 12 | 2025-10-16 | [Equipping Agents for the Real World with Agent Skills](equipping-agents-for-the-real-world-with-agent-skills.md) | Agent Skills |
| 13 | 2025-10-20 | [Beyond Permission Prompts](beyond-permission-prompts.md) | 安全沙箱 |
| 14 | 2025-11-04 | [Code Execution with MCP](code-execution-with-mcp.md) | 代码执行 |
| 15 | 2025-11-24 | [Advanced Tool Use](advanced-tool-use.md) | 高级工具特性 |
| 16 | 2025-11-26 | [Effective Harnesses for Long-Running Agents](effective-harnesses-for-long-running-agents.md) | Harness 设计 |
| 17 | 2026-01-09 | [Demystifying Evals for AI Agents](demystifying-evals-for-ai-agents.md) | 评估框架 |
| 18 | 2026-01-21 | [Designing AI-Resistant Technical Evaluations](designing-ai-resistant-technical-evaluations.md) | AI 抗性评估 |
| 19 | 2026-02-05 | [Quantifying Infrastructure Noise in Agentic Coding Evals](quantifying-infrastructure-noise-in-agentic-coding-evals.md) | 基准噪声 |
| 20 | 2026-02-05 | [Building a C Compiler with a Team of Parallel Claudes](building-a-c-compiler-with-a-team-of-parallel-claudes.md) | 并行 Agent Teams |
| 21 | 2026-03-06 | [Eval Awareness in Claude Opus 4.6's BrowseComp Performance](eval-awareness-browsecomp.md) | 评估感知 |
| 22 | 2026-03-24 | [Harness Design for Long-Running Application Development](harness-design-for-long-running-application-development.md) | 高级 Harness |
| 23 | 2026-03-25 | [Claude Code Auto Mode](claude-code-auto-mode.md) | 自动权限 |
| 24 | 2026-04-08 | [Scaling Managed Agents](scaling-managed-agents.md) | 基础设施解耦 |
| 25 | 2026-04-23 | [An Update on Recent Claude Code Quality Reports](an-update-on-recent-claude-code-quality-reports.md) | 质量事后分析 |
| 26 | 2026-05-25 | [How We Built a System to Contain Claude Across Products](how-we-contain-claude-across-products.md) | 跨产品 containment |
| 27 | 2026-08-04 | [A Guide to Cost Visibility and Control in Claude](cost-visibility-and-control-in-claude.md) | 企业成本管控 / 模型分级 / Analytics API |
| 28 | 2026-08-05 | [Inference Hooks: Inline Data Loss Prevention for Claude Enterprise](claude-enterprise-inference-hooks.md) | 企业安全 / DLP / WebSocket |
| 29 | 2026-08-06 | [Run Claude Code Sessions on Your Own Compute](run-claude-code-sessions-on-your-own-compute.md) | 自托管 / 数据驻留 / Runner 架构 |
| 30 | 2026-08-06 | [Millennium and Anthropic Are Building a Digital Risk Analyst](millennium-digital-risk-analyst.md) | 企业案例 / 金融风险 / Agent |
| 31 | 2026-08-07 | [Auto Mode Is Now the Default in Claude Code](auto-mode-default-in-claude-code.md) | 自动权限 / 分类器 / 默认设置 |
| 32 | 2026-08-07 | [Running Auto Mode in Production](auto-mode-in-production.md) | 生产实践 / 企业部署 / 长时 Agent |
| 33 | 2026-08-11 | [How Claude's Text Watermarking Works](claude-text-watermarking.md) | 内容溯源 / 水印 / EU AI Act / C2PA |
| 34 | 2026-08-11 | [Compliance API Coverage Extends to Cowork and Claude Code](compliance-api-cowork-claude-code.md) | 合规审计 / eDiscovery / 企业治理 |
| 35 | 2026-08-12 | [Claude Cowork Comes to the Chrome Side Panel](cowork-chrome-side-panel.md) | 浏览器 Agent / 跨设备延续 |
| 36 | 2026-08-13 | [Securing the Frontier: How JetBrains Evaluates and Deploys Claude Fable 5](jetbrains-evaluates-claude-fable-5.md) | 企业评估 / 模型选型 / 数据保留 |
| 37 | 2026-08-13 | [Self-service Data Analytics in Slack with Claude Tag](claude-tag-self-service-data-analytics.md) | 数据分析 / 治理一致 / 自助服务 |
| 38 | 2026-08-14 | [Maximizing the Value of Your Claude Code Sessions](maximizing-value-of-claude-code-sessions.md) | Token 优化 / 会话管理 / Prompt Cache |
| 39 | 2026-08-17 | [How ABC Legal Turned Every Employee into a Builder](abc-legal-managed-agents.md) | 全员采用 / Managed Agents / 法律科技 |
| 40 | 2026-08-18 | [Claude on Call: CI/CD First Responder](claude-tag-ci-cd-on-call.md) | 运维 Agent / CI/CD 值班 / 第一响应者 |
| 41 | 2026-08-19 | [Turning Conversation into Knowledge: Slack Human-Agent Teams](slack-human-agent-teams.md) | 人机团队 / 知识管理 / 开放频道 |
| 42 | 2026-08-20 | [Build Production Agents with Computer Use, Skills API, Files API](computer-use-skills-api-files-api.md) | Agent 三件套 GA / 浏览器工具 |
| 43 | 2026-08-20 | [The Claude Code Guide For Startups](claude-code-guide-for-startups.md) | 创业公司 / 效率原则 / 最佳实践 |
| 44 | 2026-08-20 | [How monday.com Transformed Its Platform into an Agent-First Product](monday-com-agent-first-platform.md) | Agent-first 重构 / 人机协作 / 企业案例 |
| 45 | 2026-08-20 | [Anthropic's Approach to Teaching and Learning AI](anthropics-approach-to-teaching-and-learning-ai.md) | Claude Academy / AI 教育 / 自主性 |
