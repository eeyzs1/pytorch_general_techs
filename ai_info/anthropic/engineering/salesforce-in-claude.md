# Salesforce in Claude：CRM 原生接入会话（Salesforce in Claude: CRM natively in the conversation）

- **原文链接**: [Salesforce in Claude](https://claude.com/blog/salesforce-in-claude)
- **作者**: Anthropic、Salesforce
- **发布日期**: 2026-09-15
- **检索日期**: 2026-09-29
- **标签**: #Salesforce #CRM #Claudeforce #Connector #企业集成 #AgenticCRM

## 核心观点

Anthropic 与Salesforce 落地了 8 月 26 日宣布的扩大合作（社区俗称 "Claudeforce"）的关键一环：Salesforce in Claude——把 CRM 数据与操作原生接入 Claude 会话。销售与服务场景中，用户直接在 Claude 里查询和处理 Salesforce 记录，无需在应用间切换或手动导出数据。

这是双向整合的 Claude 侧：与既有的 "Claude in Salesforce"（在 Salesforce 产品内嵌 Claude 能力）相对，"Salesforce in Claude" 让 Claude 侧拥有 CRM 的原生操作权。同一个合作框架的两端，共同构成 agent 时代企业系统的双向互操作范式。

## 关键发现 / 关键技术

### 1. 能力范围
- CRM 数据原生接入 Claude 会话：直接查询客户、商机、工单等 Salesforce 记录。
- 销售场景：会话中完成记录查询与更新；服务场景：直接处理 Salesforce 中的服务请求。
- 操作在企业权限体系内进行，数据边界由 Salesforce 侧治理。

### 2. 覆盖与管理
- 计划覆盖：Pro/Max 个人计划与 Team/Enterprise 组织计划。
- 管理员配置：Team/Enterprise 由管理员统一设置连接与权限，个人计划用户自行接入。

### 3. 双向整合结构
- "Claude in Salesforce"：Salesforce 产品内嵌 Claude（agent 在 CRM 界面里工作）。
- "Salesforce in Claude"：Claude 会话原生操作 CRM（agent 在助手界面里工作）。
- 两个方向共用同一合作底座，官方叙事强调"agentic 前台系统"。

### 4. 生态同步动向
- 同日（2026-09-15），Deloitte Digital 宣布扩展与 Anthropic、Salesforce 的三方合作，共建 agentic 前台（front-office）解决方案。
- 与 8-26 宣布的扩大合作（含 Cowork 内置浏览器同日的 Claudeforce 报道）形成连续落点。

## 实践意义

企业 SaaS 数据接入是 agent 从"对话"走向"办事"的分水岭：CRM 是销售/服务团队的核心系统，原生接入意味着 Claude 不再只是问答助手，而是能直接读改业务记录的操作主体。对企业的启示是连接器（connector）策略的成熟——权限归 SaaS 侧、操作归 agent 侧、入口双向对等，这与 MCP 生态的标准化方向一致。对 Anthropic，Salesforce 是其企业分发战略中权重极高的伙伴：模型能力经由 CRM 触达一线业务用户，分发即护城河。

## 跨厂商对比

- 与 [Bain Company joins Claude partner network](bain-company-joins-claude-partner-network.md) 互补：Bain 代表咨询系伙伴把 Claude 带进客户交付，Salesforce 代表 SaaS 系伙伴把 Claude 带进产品内部，两条企业分发路径并行。
- 与 [Introducing Muse personal AI agent](../../meta/introducing-muse-personal-ai-agent.md) 对比：Meta 的个人 agent 通过第三方接入获得服务能力，Salesforce in Claude 则是深度系统级整合（数据 + 操作 + 权限），反映"连接"从 API 调用到治理型集成的深度差异。

## 资源

- 官方文章：https://claude.com/blog/salesforce-in-claude
- 合作官宣背景：https://www.anthropic.com/news
- Salesforce 相关：https://www.salesforce.com/

> 注：claude.com/blog 正文客户端渲染不可直抓，本文经多源交叉验证（见资源）；正文细节（具体对象/字段级能力）待原文可抓取后补全。
