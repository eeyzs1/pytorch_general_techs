# MCP 新路线图：Agent 消息原语与统一传输（The New MCP Roadmap）

- **原文链接**: [The New MCP Roadmap](https://blog.modelcontextprotocol.io/posts/mcp-roadmap/)
- **作者**: David Soria Parra、Den Delimarsky（MCP 首席维护者）
- **发布日期**: 2026-08-22
- **检索日期**: 2026-09-29
- **标签**: #MCP #路线图 #Agent通信 #传输协议 #企业安全

## 核心观点

MCP 两位首席维护者发布新版路线图，先复盘 3 月旧路线图四大方向在 2026-07-28 规范中的落地：协议级会话与初始化握手被移除（SEP-2575/2567）使服务器可无状态水平扩展，Tasks 转为官方扩展（SEP-2663）并以 MRTR 模式（SEP-2322）取代服务器主动请求，治理上正式采纳 Contributor Ladder 与功能生命周期/弃用政策，企业侧 issuer 校验、issuer 绑定客户端凭证与 EMA 扩展已稳定并被 Anthropic、Microsoft、Okta 采纳。

新路线图把下一阶段聚焦五大优先领域：Agent 消息原语（服务器发起事件免轮询）、HTTP 原生传输统一与加固、Agent 身份与企业级安全（DPoP、Workload Identity Federation、ID-JAG）、改进原语（统一 tools/call 结果契约、渐进式发现）、SDK 开发者体验。落入优先领域的 SEP 将获加速评审。

## 关键发现 / 关键技术

### 1. Agent 消息原语：从"客户端轮询"走向"服务器推送"
- 服务器发起事件（webhook/频道）让 Agent 免轮询获取长任务进展；跨 Agents / Transports / Triggers & Events 三个工作组组合审查事件语义。
- Tasks 扩展（SEP-2663）成熟化后并入规范主体，成为长时任务的标准化表达。

### 2. HTTP 原生传输统一
- 本地服务器也将走 Streamable HTTP over stdio，协议收敛到单一传输，消除 stdio 与 HTTP 两套行为差异带来的实现分叉。

### 3. Agent 身份与企业级安全
- DPoP 定稿推广、Workload Identity Federation、ID-JAG 授权与标准 token exchange；与 IETF OAuth/WIMSE 标准组织深化合作，企业身份栈与 MCP 的集成路径标准化。

### 4. 渐进式发现对抗上下文膨胀
- 百级工具的列表会让模型选择退化——统一 tools/call 结果契约与渐进式发现（progressive discovery）被列为改进原语优先项，直接回应工具生态爆发后的上下文工程问题。

## 实践意义

对 Agent 工具生态而言，这份路线图意味着三件事：MCP 服务器实现将进一步"无状态化 + HTTP 原生化"，普通负载均衡即可水平扩展的架构红利会扩大到本地场景；企业身份（DPoP/WIMSE/ID-JAG）进入协议主线，MCP 在金融、政务等强身份治理环境的可用性提升；渐进式发现把"工具太多导致模型选错工具"从应用层补丁上升为协议层特性，与上下文工程的最小高信号 token 原则同向。

## 跨厂商对比

- 与 [MCP 2026-07-28 规范](mcp-2026-07-28-specification.md) 对比：07-28 规范解决了"无状态核心 + 企业级扩展"的当下问题，本文则定义"Agent 消息原语 + 统一传输 + 身份"的下一程，两者构成协议演进的连续两步。
- 与 [Advanced Tool Use](../../anthropic/engineering/advanced-tool-use.md) 互补：Anthropic 在模型/平台侧用工具搜索、程序化工具调用应对大规模工具列表，MCP 则在协议侧用渐进式发现解决同一问题——应用层与协议层双管齐下。

## 资源

- 官方路线图：https://modelcontextprotocol.io/development/roadmap
- 本博文：https://blog.modelcontextprotocol.io/posts/mcp-roadmap/
- 2026-07-28 规范发布博文：https://blog.modelcontextprotocol.io/posts/2026-07-28/
- 规范 changelog：https://modelcontextprotocol.io/specification/2026-07-28/changelog
- 工作组列表：https://modelcontextprotocol.io/community/working-interest-groups
