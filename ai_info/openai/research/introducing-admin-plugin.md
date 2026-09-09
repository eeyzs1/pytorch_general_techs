# 推出 ChatGPT Work 与 Codex 的 Admin 插件（Introducing the Admin plugin for ChatGPT Work and Codex）

- **原文链接**: [Introducing the Admin plugin for ChatGPT Work and Codex](https://openai.com/index/introducing-admin-plugin/)
- **作者**: OpenAI
- **发布日期**: 2026-08-25
- **检索日期**: 2026-09-09
- **标签**: #Admin插件 #企业管理 #ChatGPTWork #Codex #对话式运维

## 核心观点

OpenAI 为 ChatGPT Work 与 Codex 推出 Admin 插件：管理员在一个对话里提问、下钻细节、执行授权变更并确认结果，无需复杂提示词或在分析、设置、报表之间来回切换。管理一个增长中的工作区通常要在多系统间移动才能定位问题并行动，Admin 插件把管理分析与受支持的动作聚合到一起，帮助团队保持工作区的安全、高效与预算内。

能力覆盖四类日常任务：理解采用与用量（ChatGPT Work 与 Codex 的活动与 credit 消耗、接近限额预警）、管理成员与群组（入/离职与团队调整）、管理访问与权限（有效权限、访问问题诊断、按角色/群组控制功能或模型访问）、管理用量限额与支出请求（调整限额、结合上下文审批）。插件在管理员既有角色与权限内工作，不授予更宽的访问：每条指令被映射为受支持的读/写动作并返回结构化结果，影响面更大的操作在执行前可先审阅。

## 关键发现 / 关键技术

### 1. 自动化例行管理工作流（无需自研工程）
- 把待审批的用量请求路由到 Slack 或 Microsoft Teams，授权审查者在既有工具内批准/拒绝
- 监控功能访问请求：满足预定义标准即自动批准，例外转人工审查；每个工作流确认变更已应用，管理员全程可控

### 2. 权限感知与可审计
- 将 Admin Console 的能力以"权限感知工具"的形式暴露给 ChatGPT Work 与 Codex，遵循工作区策略与审批要求
- 每次变更可见三件事：请求了什么、是否完成、改变了什么

### 3. OpenAI IT 团队自用数据
- 全球 IT 负责人 Kunal Malik：价值远超"更快出报表"——插件把问题连接到下一个受支持动作
- Slack 中的 ChatGPT Work agent 处理员工 IT 请求、分诊与执行工单、检索上下文、核对政策、完成任务并上报例外：部署的工作流解决约 45% 工单量
- ChatGPT Work 把工单数据与历史变成运营健康看板，在支持量近乎翻倍的情况下清零积压，团队从被动响应转向按实时数据定优先级

### 4. 安装路径
- 在 ChatGPT 工作区设置中启用插件，再从 ChatGPT Work（Web/桌面）的 Plugins 目录安装

## 实践意义

Admin 插件是"把管理控制台 agent 化"的典型样本：对 IT 与平台管理团队，它示范了如何用对话界面压缩"分析 → 决策 → 执行 → 确认"的闭环，同时用权限映射与结构化结果保住审计性；对企业采购者，它降低了 ChatGPT Work / Codex 的治理运营成本，使大规模席位管理变得可行。OpenAI IT 自身的 45% 工单自动解决率与看板化运营，是评估"agent 进后台职能"ROI 的直接参考。

## 跨厂商对比

- 与 [ChatGPT 企业支出控制](chatgpt-enterprise-spend-controls.md) 互补：支出控制建立限额、审批与额度体系的政策底座，Admin 插件把对这些策略的日常操作（查用量、调限额、批请求）变成对话式动作——前者定规则，后者降操作成本
- 与 [Compliance API 与 Cowork/Claude Code](../../anthropic/engineering/compliance-api-cowork-claude-code.md) 对比：Anthropic 用策略 API 在代码与工具调用层强制合规边界，OpenAI 用权限感知的对话式 admin agent 让治理操作自然化，两种"治理即产品"的路线互为参照

## 资源

- 官方文章：https://openai.com/index/introducing-admin-plugin/
- 相关：https://openai.com/index/ai-native-company-workflows/
