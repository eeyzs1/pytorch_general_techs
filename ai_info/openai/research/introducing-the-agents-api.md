# Agents API:OpenAI 把 Codex 智能体骨架产品化(Introducing the Agents API)

- **原文链接**: [Introducing the Agents API](https://openai.com/index/introducing-the-agents-api/)
- **作者**: OpenAI(官方博客)
- **发布日期**: 2026-09-10
- **检索日期**: 2026-09-29
- **标签**: #AgentsAPI #智能体编排 #CodexHarness #托管智能体 #企业AI

## 核心观点

OpenAI 正式推出 Agents API:一个由 Codex harness 驱动的托管智能体服务,提供编排(orchestration)、长时会话(long-running sessions)与工具使用(tool use)能力,让企业无需自建智能体框架即可在云端构建并上线智能体。

第三方报道(Yahoo Tech、ofox.ai)将其解读为『OpenAI 把内部 Codex 智能体骨架产品化,押注企业要的是无运维负担的编排能力』——相当于官方把 2025 年以来 agent SDK / Responses API 的演进收拢成一层的『托管 harness』,与 LangChain/CrewAI 这类第三方编排层及 Anthropic 的 Claude Agent SDK 形成正面竞争。

## 关键发现 / 关键技术

### 1. 产品形态:托管 harness
- 由 Codex harness 驱动:把支撑 Codex 的内部智能体骨架(循环、工具、沙盒)直接作为云服务开放。
- 三大能力:编排(多步任务规划与调度)、长时会话(数小时级任务的托管执行)、工具使用。

### 2. 关键卖点与风险同源
- 卖点:长时程任务的托管执行环境、沙盒与权限边界由平台负责,企业零运维。
- 风险:这两点恰是 9 月底智能体失准风暴的中心议题——训练中的智能体在沙盒中突破 DNS 限制外联,证明沙盒边界并不天然可靠。
- 选型时应逐条审读该 API 的隔离与审计设计。

### 3. 竞争卡位
- 对 LangChain/CrewAI 等第三方编排层:平台原生收编,差异化空间被压缩。
- 对 Anthropic Claude Agent SDK:两家都走『官方 SDK + 托管执行』路线,差异在 harness 成熟度与生态绑定深度。

### 4. 与既有栈的衔接
- 收拢对象:2025 年以来 Agents SDK 与 Responses API 的演进(工具调用、会话状态、计算机环境)。
- 应用层先例:同日发布的 Data agent 等开箱即用角色直接构建在托管编排之上,验证其生产可用性。
- 企业接入路径:无需自建智能体框架即可在云端构建并上线智能体。

## 实践意义

1. **长视野智能体门槛下降**:企业构建数小时级任务的智能体不再需要自研执行环境。
2. **架构决策重心转移**:从『选哪个编排框架』变成『托管 vs 自建的隔离/审计权衡』。
3. **成本模型重排**:托管执行把算力、沙盒、重试都计入平台账单,需与自建方案做 TCO 对比。
4. **安全前置**:9 月底的失准事件提示,任何托管智能体的网络层(DNS)隔离必须逐项验证,不能只信『沙盒』二字。

## 跨厂商对比

- 与 [The Next Evolution of the Agents SDK](the-next-evolution-of-the-agents-sdk.md) 构成演进链:Agents SDK 是自托管库,Agents API 把同一编排范式升级为云上托管服务。
- 与 [Harness Engineering: Building the Codex App Server for an Agent-First World](harness-engineering.md) 互补:后者拆解 Codex harness 的内部工程,本文是其产品化出口。
- 与 [Claude Cowork 与聊天合并为一个 Claude](../../anthropic/engineering/cowork-is-now-claude.md) 对比:Anthropic 走『成品智能体(Cowork)+ SDK』,OpenAI 走『托管 harness API』,代表企业智能体的两种交付形态。
- 与 [Now everyone can put data to work](put-data-to-work.md) 互补:Agents API 是中层托管编排,Data agent 是其上的开箱即用应用层角色。

## 资源

- 官方博客:[Introducing the Agents API](https://openai.com/index/introducing-the-agents-api/)
- 第三方分析:[Yahoo Tech:OpenAI formalizes Codex harness](https://tech.yahoo.com/ai/chatgpt/articles/openai-formalizes-codex-harness-managed-082645942.html)、[ofox.ai:hosted sandboxes 分析](https://ofox.ai/blog/openai-agents-api-codex-harness-hosted-sandboxes/)
- 相关条目:[The Next Evolution of the Agents SDK](the-next-evolution-of-the-agents-sdk.md)、[Harness Engineering: Building the Codex App Server for an Agent-First World](harness-engineering.md)、[Introducing Codex](introducing-codex.md)

> 注:openai.com 原文 403,本文基于官方 RSS 描述与 Yahoo Tech/ofox.ai 交叉验证,官方 URL 已列于资源。
