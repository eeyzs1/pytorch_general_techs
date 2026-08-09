# MCP 2026-07-28 规范：无状态核心与企业级扩展（The 2026-07-28 Specification）

- **原文链接**: [The 2026-07-28 Specification](https://blog.modelcontextprotocol.io/posts/2026-07-28/)
- **作者**: Model Context Protocol 工作组（Linux Foundation）
- **发布日期**: 2026-07-28
- **检索日期**: 2026-08-01
- **标签**: #MCP #规范更新 #无状态核心 #OAuth #企业级 #LinuxFoundation

## 核心观点

这是 MCP 自问世以来最大的一次规范修订，核心动作是把协议从"双向有状态"改造成"请求/响应无状态"。官方将其定位为继一年多前远程 MCP 推出后最重要的一次发布——MCP 正在从实验性协议成长为生产级基础设施。Tier 1 SDK（TypeScript、Python、Go、C#）月下载量已接近 5 亿次，TS 与 Python 累计突破 10 亿次，规模化压力催生了这次改造。

这次更新主张：协议层不应隐藏会话状态，而应让每个请求自描述（携带协议版本、客户端身份与能力），从而任何请求都能落到任意实例上、由普通轮询负载均衡器分发。配合正式的扩展框架（Tasks、MCP Apps、EMA）、OAuth 加固与十二个月最小弃用窗口，MCP 给出了企业级 Agent 基础设施的成熟底座。

## 关键发现 / 关键技术

### 1. 无状态协议核心：取消握手与会话

正式移除 `initialize`/`initialized` 握手与 `Mcp-Session-Id` 头（SEP-2575、SEP-2567）。每个请求自行携带协议版本、客户端身份与能力（放在 `_meta` 中）。新增可选的 `server/discover` RPC 供客户端提前探测能力，但非必需。请求示例：

```
POST /mcp HTTP/1.1
MCP-Protocol-Version: 2026-07-28
Mcp-Method: tools/call
Mcp-Name: search

{"jsonrpc":"2.0","id":1,"method":"tools/call",
 "params":{"name":"search","arguments":{"q":"otters"},
 "_meta":{"io.modelcontextprotocol/clientInfo":{"name":"my-app","version":"1.0"}}}}
```

协议层无会话不强制应用无状态——若服务器需要跨调用保持状态，应由工具显式生成 handle 并让模型作为参数回传，这种"模型可见的 handle"比隐藏在传输层中的会话状态更可控。

### 2. Multi Round-Trip Requests（MRTR）

MRTR（SEP-2322）替代原先需要保持长连接的服务器发起请求（`elicitation/create`、`sampling/createMessage`、`roots/list`）。机制：服务器返回 `resultType: "input_required"` 并附上待回答请求，客户端带上 `inputResponses` 重试原调用。这让"工具执行中途向用户确认/补参数"这类交互在无状态协议上成为可能。

### 3. 头部路由与网关友好

Streamable HTTP 请求必须携带 `Mcp-Method` 和 `Mcp-Name` 头（SEP-2243），网关、限流器、WAF 可直接基于头部路由与鉴权，无需解析 JSON body。这是 MCP 成为"一等 HTTP 工作负载"的关键。

### 4. 可缓存的列表响应

`tools/list`、`prompts/list`、`resources/list`、`resources/read` 响应携带 `ttlMs` 与 `cacheScope`（SEP-2549），客户端可缓存工具目录并保持上游 prompt cache 在重连后稳定——这与 [Code Execution with MCP](../../anthropic/engineering/code-execution-with-mcp.md) 中"工具定义压垮上下文窗口"的痛点直接相关。

### 5. 授权加固

- 授权服务器须按 RFC 9207 返回 `iss` 参数，客户端兑换 code 前必须校验（SEP-2468），关闭授权服务器混用漏洞。
- 客户端在 DCR 时设置 `application_type`，让授权服务器不再拒绝桌面/CLI 应用的 `localhost` 重定向（SEP-837）。
- 客户端凭据绑定到签发方，禁止跨授权服务器复用（SEP-2352）。
- 动态客户端注册（DCR）正式弃用，转向 Client ID Metadata Documents（CIMD）作为标准。

### 6. 扩展框架与 Tasks

正式锁定扩展框架。Tasks 从实验性核心移入 `io.modelcontextprotocol/tasks` 扩展（SEP-2663），采用轮询式 `tasks/get` 与新增的 `tasks/update`；变更通知从旧的 HTTP GET 端点迁到单一 `subscriptions/listen` 流，客户端按通知类型按需订阅。Tasks、MCP Apps、Enterprise Managed Authorization（EMA）共同构成企业级扩展矩阵。

### 7. 弃用策略与弃用项

引入正式弃用策略，最小窗口十二个月。Roots、Sampling、Logging 被弃用（SEP-2577），仍可工作至少一年；旧版 HTTP+SSE 传输同样进入一年退场期。新实现不应再采用被弃用项。

### 8. SDK 与生态支持

四套 Tier 1 SDK（TypeScript、Python、Go、C#）同步支持 `2026-07-28`，Rust SDK 处于 beta。AWS（Bedrock AgentCore）、Cloudflare（Agents SDK + Workers）、Google Cloud、Microsoft Foundry、Figma、Honeycomb、Supabase、Netlify 等均在发布日表态支持。Honeycomb 报告约 20% 月度交互查询由 Agent 发起。

## 实践意义

- **基础设施侧**：MCP 服务器可直接跑在标准可扩展基础设施上，无需管理会话或持久连接；round-robin 负载均衡即够用，部署成本显著下降。
- **网关与安全侧**：头部路由让企业可以在 WAF/网关层统一鉴权与计量，而不必侵入 JSON body；EMA 让企业以托管方式管理授权。
- **Agent 工程侧**：列表响应可缓存意味着工具目录不再反复占用上下文，与代码执行范式叠加可进一步压缩 Token；MRTR 让"执行中确认"在无状态下可行，扩展了工具交互边界。
- **协议演进侧**：十二个月最小弃用窗口让团队可计划升级而非被动应对，这对把 MCP 作为默认底座的企业团队尤为关键。

## 跨厂商对比

- 与 [Code Execution with MCP](../../anthropic/engineering/code-execution-with-mcp.md) 互补：后者解决"工具定义压垮上下文"的应用层 Token 优化（98.7% 削减），本次规范则在协议层给出"列表响应可缓存 + 无状态核心"的根因解法——两者叠加是 MCP 规模化的完整路径。
- 与 [Building Agents with the Claude Agent SDK](../../anthropic/engineering/building-agents-with-the-claude-agent-sdk.md) 对比：Claude Agent SDK 是厂商 Agent 框架，MCP 则是其下的开放协议层；无状态核心让这类 SDK 在远程工具调用时无需维护会话，简化了 harness 实现。
- 与 [Writing Effective Tools for AI Agents](../../anthropic/engineering/writing-effective-tools-for-ai-agents.md) 对比：该文聚焦单个工具的设计原则，MCP 2026-07-28 则定义工具如何在协议层被路由、缓存与鉴权——前者是"工具怎么写好"，后者是"工具怎么规模化管理"。
- 与 [Introducing AgentKit](../../openai/research/introducing-agentkit.md) 对比：AgentKit 是 OpenAI 的 Agent 构建套件，依赖厂商私有接口；MCP 作为开放标准让跨厂商工具生态成为可能，本次企业级扩展（EMA/Tasks）进一步缩小了与厂商专属方案的能力差距。
- 与 [New Tools for Building Agents](../../openai/research/new-tools-for-building-agents.md) 对比：OpenAI 持续扩展其工具能力集，而 MCP 的扩展框架（Tasks、MCP Apps）走的是"协议层标准化扩展"路线，方向不同但目标一致。
- 与 [Expanding Managed Agents: Gemini API 3.6 Flash Hooks](../../google/deepmind/expanding-managed-agents-gemini-api-3-6-flash-hooks.md) 对比：Google 的托管 Agent 与 Hooks 是厂商托管路径，MCP 无状态核心让托管 Agent 平台（如 Bedrock AgentCore、Cloudflare Workers）能以更低运维成本承载第三方 MCP 服务器。

## 资源

- 规范文档：https://modelcontextprotocol.io/specification/2026-07-28
- 完整变更日志：https://modelcontextprotocol.io/specification/2026-07-28/changelog
- 文档与指南：https://modelcontextprotocol.io/docs/2026-07-28/getting-started/intro
- TypeScript SDK：https://github.com/modelcontextprotocol/typescript-sdk
- Python SDK：https://github.com/modelcontextprotocol/python-sdk
- Go SDK：https://github.com/modelcontextprotocol/go-sdk
- C# SDK：https://github.com/modelcontextprotocol/csharp-sdk
- Rust SDK（beta）：https://github.com/modelcontextprotocol/rust-sdk
