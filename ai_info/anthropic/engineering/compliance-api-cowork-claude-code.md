# Compliance API 覆盖扩展至 Claude Cowork 与 Claude Code（Compliance API coverage extends to Claude Cowork and Claude Code）

- **原文链接**: [Compliance API coverage extends to Claude Cowork and Claude Code](https://claude.com/blog/compliance-api-cowork-and-claude-code)
- **作者**: Anthropic
- **发布日期**: 2026-08-11
- **检索日期**: 2026-08-21
- **标签**: #Anthropic #ComplianceAPI #企业合规 #审计 #ClaudeCowork #ClaudeCode #eDiscovery

## 核心观点

Claude 的 Compliance API 覆盖范围扩展到 Claude Cowork（桌面/Web/移动）与 Claude Code（CLI 与桌面），对 Claude Enterprise 客户以 beta 形式提供。合规与安全团队现在可以通过他们已用于 Claude 聊天的同一 Compliance API 界面，拉取两个产品的会话内容与元数据，用于审计与 eDiscovery。

新端点是增量的——不改变现有数据拉取方式。这填补了一个治理缺口：Cowork 与 Claude Code 会话此前不在 Compliance API 覆盖内，企业无法通过统一接口审计这些 Agent 的使用。

## 关键发现 / 关键技术

### 1. 统一合规接口
- 同一 Compliance API 覆盖 Claude 聊天 + Cowork + Claude Code
- 无需为每个界面部署独立日志基础设施
- 审计与 eDiscovery 的单一数据源

### 2. 覆盖范围
- Cowork：桌面应用、Web、移动
- Claude Code：CLI 与桌面应用
- Claude Enterprise 客户 beta 提供

### 3. 增量端点设计
- 新端点是 addititve：现有数据拉取不受影响
- 向后兼容的企业 API 演进
- 会话内容 + 元数据的完整获取

### 4. 企业 Agent 治理闭环
- 与 [推理钩子 DLP](claude-enterprise-inference-hooks.md)（事前检查）互补
- Compliance API（事后审计）补齐治理链路
- 企业 Agent 部署的"事前 + 事后"双保险

## 实践意义

Compliance API 覆盖 Agent 产品，说明企业 Agent 治理从"内容检查"延伸到"行为审计"：安全团队不仅要阻止敏感数据流出，还要能回答"谁在何时让 Agent 做了什么"。对强监管行业（金融、医疗、法律），统一合规接口是部署 Agent 的前提条件；增量端点设计也为其他厂商的合规 API 演进提供参考。

## 跨厂商对比

- 与 [Inference Hooks 内联 DLP](claude-enterprise-inference-hooks.md) 互补：DLP 管请求内容（事前），Compliance API 管会话记录（事后）
- 与 [Claude 成本可见性](cost-visibility-and-control-in-claude.md) 对比：成本指南管支出，Compliance API 管合规，构成企业管控双维度
- 与 [OpenAI ChatGPT Enterprise 用量分析](../../openai/research/chatgpt-enterprise-spend-controls.md) 对比：OpenAI 提供管理员用量视图，Anthropic 提供合规审计 API，治理重点不同

## 资源

- 论文：N/A
- 官方公告：https://claude.com/blog/compliance-api-cowork-and-claude-code
