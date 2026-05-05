# OpenAI Research & Engineering — 核心观点总结

> 汇总自 [OpenAI Research](https://openai.com/research/) 和 [OpenAI Blog](https://openai.com/index/) 的 21 篇文章，涵盖 2025 年 1 月至 2026 年 5 月。

## 一、总体脉络

OpenAI 的技术文章呈现了两条并行的演进路径：

```
路径1（工程实践）: Agent 指南 → Codex/Operator → Harness Engineering → AgentKit → Codex 全面升级
路径2（安全研究）: Model Spec → 指令层级 → CoT 监控 → CoT-Control → RL奖励信号分析
路径3（平台生态）: Responses API → Apps SDK → ChatGPT 超级App → 计算机环境 → MCP 互操作
```

工程路径从 Agent 构建基础方法论出发，逐步构建产品（Codex、Operator、Deep Research），最终形成 Harness Engineering 方法论和 AgentKit 工具集，并在 2026 年 4 月发布 Codex 桌面版和全面升级（Computer Use、多 Agent、图像生成、90+ 插件）。安全路径从模型行为规范出发，逐步建立指令层级、CoT 监控和可监控性研究，并于 2026 年 4 月发布了 RL 奖励信号导致"Goblins"行为偏差的详细事后分析，形成纵深防御体系。平台路径从 API 工具出发，为 Responses API 配备完整计算机环境（Shell 工具 + 容器工作区 + Skills + Compaction），构建 ChatGPT 超级应用生态，并采纳 MCP 开放协议实现跨平台互操作。

## 二、五大核心主题

### 1. Agent 构建方法论与工具链

[A Practical Guide to Building Agents](a-practical-guide-to-building-agents.md) 奠定了理论基础——Agent 由模型、工具和指令三要素组成，护栏是必需品。[New Tools for Building Agents](new-tools-for-building-agents.md) 和 [New Tools and Features in the Responses API](new-tools-and-features-in-the-responses-api.md) 提供了底层 API（Web 搜索、文件搜索、Computer Use）和 Agents SDK。[The Next Evolution of the Agents SDK](the-next-evolution-of-the-agents-sdk.md) 新增 MCP 工具调用支持。[Introducing AgentKit](introducing-agentkit.md) 将工具链推向工业化——可视化设计、版本控制、内联评估。[Introducing the Codex App](introducing-the-codex-app.md) 发布了 macOS 桌面版，支持多 Agent 并行编排、Skills 系统和 Automations 自动调度，将 Codex 升级为 Agent 命令中心。[Codex for (almost) everything](codex-for-almost-everything.md) 发布了全面升级——Computer Use 操控桌面应用、应用内浏览器、gpt-image-1.5 图像生成、90+ 插件生态，每周服务超过 300 万开发者。

**核心洞察**: 从单 Agent 到多 Agent，从手写代码到 Harness Engineering，OpenAI 的 Agent 工具链在快速工业化。

### 2. Harness Engineering 与 Agent-First 开发

[Harness Engineering](harness-engineering.md) 是 OpenAI 最重要的工程贡献——3 名工程师用 Codex 零手写代码交付 100 万行产品。核心转变：人类从"编码者"变为"环境设计者"。[Building an AI-Native Engineering Team](building-an-ai-native-engineering-team.md) 描述了这种转变对团队的影响。[GPT-4.1 Prompting Guide](gpt-4-1-prompting-guide.md) 提供了 Agent 提示的具体技术。

**核心洞察**: 当 Agent 能处理全生命周期任务时，人类角色完全转向系统架构的"牧羊人"。构建时间、隐性知识显式化和可观测性是关键约束。

### 3. Agent 产品矩阵

| 产品 | 能力 | 对标 Anthropic |
|------|------|---------------|
| [Introducing Codex](introducing-codex.md) | 云端编码 Agent | Claude Code |
| [Codex Now Generally Available](codex-now-generally-available.md) | 编码 Agent GA + SDK | Claude Code GA |
| [Introducing Operator](introducing-operator.md) | GUI 操作 Agent (CUA) | Computer Use |
| [Introducing Deep Research](introducing-deep-research.md) | 多步研究 Agent | Research Feature |

**核心洞察**: OpenAI 的 Agent 产品更偏消费者和企业级，Anthropic 的更偏开发者工具。Codex GA 的 10 倍使用量增长验证了市场需求。Codex App 标志着从终端工具到桌面命令中心的形态演进，300 万周活跃开发者是重要里程碑。

### 5. 平台生态与超级应用

[New Tools for Building Agents](new-tools-for-building-agents.md) 发布了首批 Agent 构建块（Responses API + Agents SDK）。[Equipping the Responses API with a Computer Environment](equipping-the-responses-api-with-a-computer-environment.md) 为 Responses API 配备了完整计算机环境（Shell 工具 + 托管容器 + 服务端 Compaction + Agent Skills），标志着从"模型调用"到"系统级 Agent 执行"的转变。[Introducing Apps in ChatGPT](introducing-apps-in-chatgpt.md) 将 ChatGPT 转变为超级应用平台——8 亿用户可在对话中直接使用第三方应用。[Codex Now Generally Available](codex-now-generally-available.md) 标志着编码 Agent 进入生产。[The Next Evolution of the Agents SDK](the-next-evolution-of-the-agents-sdk.md) 采纳 MCP 开放协议实现跨平台互操作。

**核心洞察**: ChatGPT 正从"聊天机器人"演变为"超级应用平台"。MCP 的采纳意味着 OpenAI 从封闭生态走向开放互操作。

### 4. 安全与对齐研究

[Inside Our Approach to the Model Spec](inside-our-approach-to-the-model-spec.md) 定义了模型行为的公开框架。[Improving Instruction Hierarchy in Frontier LLMs](improving-instruction-hierarchy-in-frontier-llms.md) 解决提示注入防御。[How We Monitor Internal Coding Agents for Misalignment](how-we-monitor-internal-coding-agents-for-misalignment.md) 实践 CoT 监控。[Reasoning Models Struggle to Control Their Chains of Thought](reasoning-models-struggle-to-control-their-chains-of-thought.md) 证明了 CoT 监控的有效性。[Where the Goblins Came From](where-the-goblins-came-from.md) 是最有趣的模型行为调查——追踪 RL 奖励信号偏差如何通过 SFT 数据飞轮在多个模型代际间传播"Nerdy 风格"的口头禅（goblins/gremlins），揭示了奖励信号→训练数据→模型行为的完整因果链。

**核心洞察**: OpenAI 的安全策略是纵深防御——Model Spec（规范层）+ 指令层级（模型层）+ CoT 监控（运行时层）。推理模型 CoT 的不可控性反而是安全监控的优势。

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
| GPT-5.1 后 goblin 使用量增长 | +175% | [Where the Goblins Came From](where-the-goblins-came-from.md) |
| Nerdy 人格占 ChatGPT 回复 | 2.5%（却占 goblin 提及的 66.7%） | 同上 |
| Nerdy 奖励信号 creature 偏好 | 76.2% 数据集正偏向 | 同上 |

## 四、与 Anthropic 的对比

| 维度 | OpenAI | Anthropic |
|------|--------|-----------|
| 博客结构 | 分散在 /index/ 和 /research/ | 集中在 /engineering/ |
| 工程方法论 | Harness Engineering | Context Engineering → Harness Engineering |
| 上下文管理 | AGENTS.md | CLAUDE.md + Skills |
| 安全策略 | 指令层级 + CoT 监控 + RL 奖励审计 | 沙箱隔离 + 双重隔离 + 事后分析 |
| 工具生态 | Shell 工具 + 内置工具 + MCP 采纳 | 开放（MCP 协议） |
| 评估 | Evals 平台 + AgentKit 内联 | 8 步路线图 + LLM-as-judge |
| 产品定位 | 消费者 + 企业 + 开发者 | 开发者为主 |

## 五、贯穿始终的原则

1. **从最强模型开始**: 先用最强模型建立基线，再优化成本和延迟
2. **护栏不是可选的**: 从输入过滤到人机协作，安全是每层都需要的
3. **环境设计 > 代码编写**: Harness Engineering 的核心——设计让 Agent 可靠运行的环境
4. **隐性知识显式化**: 高级工程师的"隐性知识"必须写入文档和测试
5. **CoT 可监控性是安全基础**: 推理模型的思维链是安全监控的窗口
6. **工业化 Agent 开发**: 从手工作坊到可视化设计、版本控制、内联评估
7. **平台化是终局**: ChatGPT 从聊天机器人到超级应用平台，8 亿用户是生态基础
8. **奖励信号审计至关重要**: RL 训练中的微小奖励偏差可通过 SFT 数据飞轮在多个模型代际间放大，需建立系统化的行为审计工具

## 六、文章索引

| # | 日期 | 文章 | 主题 |
|---|------|------|------|
| 1 | 2025-01 | [Introducing Operator](introducing-operator.md) | GUI 操作 Agent |
| 2 | 2025-02 | [Introducing Deep Research](introducing-deep-research.md) | 多步研究 Agent |
| 3 | 2025-03 | [New Tools for Building Agents](new-tools-for-building-agents.md) | Agent 构建工具首批发布 |
| 4 | 2025-03 | [New Tools and Features in the Responses API](new-tools-and-features-in-the-responses-api.md) | Agent 开发 API |
| 5 | 2025 | [A Practical Guide to Building Agents](a-practical-guide-to-building-agents.md) | Agent 构建指南 |
| 6 | 2025 | [Building an AI-Native Engineering Team](building-an-ai-native-engineering-team.md) | AI 原生团队 |
| 7 | 2025-04 | [GPT-4.1 Prompting Guide](gpt-4-1-prompting-guide.md) | 提示工程指南 |
| 8 | 2025-05 | [Introducing Codex](introducing-codex.md) | 编码 Agent |
| 9 | 2025-10 | [Introducing Apps in ChatGPT](introducing-apps-in-chatgpt.md) | ChatGPT 超级应用平台 |
| 10 | 2025-10 | [Codex Now Generally Available](codex-now-generally-available.md) | Codex GA + SDK |
| 11 | 2026-02 | [Harness Engineering](harness-engineering.md) | Harness 工程方法论 |
| 12 | 2026-03-05 | [Reasoning Models Struggle to Control Their Chains of Thought](reasoning-models-struggle-to-control-their-chains-of-thought.md) | CoT 可监控性 |
| 13 | 2026-03-10 | [Improving Instruction Hierarchy in Frontier LLMs](improving-instruction-hierarchy-in-frontier-llms.md) | 指令层级安全 |
| 14 | 2026-03-19 | [How We Monitor Internal Coding Agents for Misalignment](how-we-monitor-internal-coding-agents-for-misalignment.md) | Agent 失准监控 |
| 15 | 2026-03-25 | [Inside Our Approach to the Model Spec](inside-our-approach-to-the-model-spec.md) | 模型行为规范 |
| 16 | 2026-04 | [Introducing AgentKit](introducing-agentkit.md) | Agent 构建工具集 |
| 17 | 2026-04-15 | [The Next Evolution of the Agents SDK](the-next-evolution-of-the-agents-sdk.md) | Agents SDK MCP 更新 |
| 18 | 2026-02-02 | [Introducing the Codex App](introducing-the-codex-app.md) | Codex 桌面 App |
| 19 | 2026-03 | [Equipping the Responses API with a Computer Environment](equipping-the-responses-api-with-a-computer-environment.md) | Agent 计算机环境 |
| 20 | 2026-04-17 | [Codex for (almost) everything](codex-for-almost-everything.md) | Codex 全面升级 |
| 21 | 2026-04-29 | [Where the Goblins Came From](where-the-goblins-came-from.md) | RL 奖励信号事后分析 |
