# MCP 官方 Ruby SDK 达到 1.0（The Official Ruby SDK for MCP Reaches 1.0）

- **原文链接**: [The Official Ruby SDK for MCP Reaches 1.0](https://blog.modelcontextprotocol.io/posts/ruby-sdk-1-0/)
- **作者**: Koichi Ito（Ruby SDK 维护者，与 Topher Bullock、Ateş Göral、Jonathan Hefner 及 Ruby 社区共同维护，源自 Shopify）
- **发布日期**: 2026-07-27
- **检索日期**: 2026-09-29
- **标签**: #MCP #Ruby #SDK #协议实现 #Rails

## 核心观点

MCP 官方 Ruby SDK（`mcp` gem）发布 1.0.0：公共 API 进入稳定期，破坏性变更只随主版本发布（语义化版本）；服务端与客户端一致性测试场景 100% 通过，并满足 MCP SDK 分级体系的全部 Tier 2 要求，正朝 Tier 1 推进。这是 MCP 多语言 SDK 生态中"社区孵化 → 官方维护 → 分级达标"路径的一个样本——Ruby SDK 起源于 Shopify，由 Ruby 核心社区成员维护。

1.0 实现了 2025-06-18 与 2025-11-25 两版规范修订，覆盖 tools/prompts/resources/sampling/elicitation/roots 全原语，并已着手支持即将到来的 2026-07-28 规范。

## 关键发现 / 关键技术

### 1. 100% 一致性通过率
- 服务端一致性从 2026 年 3 月 Tier 3 评估时的 83.3% 提升到 100%，无基线内失败项；自研一致性客户端同样 100% 通过客户端场景。
- sampling、elicitation（form 与 URL 模式）、进度通知在服务端与客户端双侧实现——这些是 SDK 分级中最容易被简化的部分。

### 2. HTTP 传输即标准 Rack 应用
- stdio 与 Streamable HTTP 双传输；HTTP 传输是标准 Rack 应用，可直接挂载进 Rails 路由或任何 Rack 兼容框架——Ruby/Web 生态的 MCP 服务器接入成本降到"加一条路由"。

### 3. 完整 OAuth 客户端
- MCP 客户端内置完整 OAuth 流程：动态客户端注册、PKCE、scope 处理，配合 2026-07-28 规范的授权加固方向，客户端安全基线齐备。

## 实践意义

对 Ruby/Rails 团队而言，官方 gem 稳定 API + Rails 原生挂载意味着把既有业务封装为 MCP 工具服务器的成本显著降低；对 MCP 生态而言，SDK 分级体系（Tier 1-3）配合公开的一致性评估 issue，让"各语言 SDK 成熟度"变成可比较的工程指标而非宣传语——选型时可直接查分级评估记录。

## 跨厂商对比

- 与 [MCP 2026-07-28 规范](../specification/mcp-2026-07-28-specification.md) 互补：规范定义协议语义（无状态核心、OAuth 加固），本文展示语言生态如何用分级体系把规范落到可验证的实现质量；Ruby SDK 1.0 实现的是前两版规范，对 07-28 规范的支持开发中。
- 与 [Desktop Extensions](../../anthropic/engineering/desktop-extensions.md) 对照：DXT 把 MCP 服务器分发做到"一键安装"，Ruby SDK 则把 MCP 服务器开发做到"Rails 加一条路由"——协议、SDK、分发三层共同降低工具生态门槛。

## 资源

- SDK 仓库：https://github.com/modelcontextprotocol/ruby-sdk
- 1.0.0 Release：https://github.com/modelcontextprotocol/ruby-sdk/releases/tag/v1.0.0
- RubyGems：https://rubygems.org/gems/mcp
- SDK 文档：https://ruby.sdk.modelcontextprotocol.io
- SDK 分级体系：https://modelcontextprotocol.io/community/sdk-tiers
