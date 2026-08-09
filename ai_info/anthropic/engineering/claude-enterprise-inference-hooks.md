# Inference Hooks：Claude Enterprise 的内联数据防泄漏

- **原文链接**: [Inference hooks: inline data loss prevention for Claude Enterprise](https://claude.com/blog/claude-enterprise-inference-hooks)
- **作者**: Anthropic
- **发布日期**: 2026-08-05
- **检索日期**: 2026-08-08
- **标签**: #企业安全 #DLP #InferenceHooks #数据防泄漏 #WebSocket #合规

## 核心观点

Anthropic 推出 inference hooks（推理钩子）beta 功能，让企业合规团队在每次 prompt 和工具调用响应到达 Claude 之前进行检查和策略执行。覆盖 Claude Enterprise 全部界面——chat、Claude Code、Claude Cowork 等。企业的 DLP（数据防泄漏）服务器做出 allow/deny 判定，Claude 实时执行该判定，在未批准内容到达模型前拦截。

此前原生内联执行仅限于 Claude Code 的客户端 hooks。inference hooks 用单一执行层覆盖所有 Claude Enterprise 界面，无需为每个产品单独集成。该功能基于开放的 webhook 协议和已发布的 schema，可与 Netskope、Palo Alto Networks、Proofpoint、Zscaler 等现有 DLP 服务器集成。

## 关键发现 / 关键技术

### 1. 签名 WebSocket 路由机制

组织开启 inference hooks 后，每次推理请求通过签名 WebSocket 连接路由到安全服务器。模型生成前，Claude 将 prompt 及其上下文发送到客户服务器；服务器返回 allow/deny 判定，Claude 仅在收到判定后继续。工具调用同样检查：当 Claude 调用工具（包括 MCP、skills、plugins 连接的工具），工具响应在返回模型前先经检查。

### 2. 统一覆盖与简化部署

一次组织级配置即覆盖 chat、Claude Code、Cowork 及其他 Claude Enterprise 产品，包括通过 MCP connectors、skills、plugins 的工具调用。支持 shadow mode（always allow）、基于角色的排除、百分比灰度发布，可自定义失败策略容忍度、超时等设置以匹配组织风险偏好。

### 3. 与现有 DLP 生态集成

inference hooks 使用开放的 webhook 协议和已发布 schema，部署时只需指向现有工具已报告的同一服务器——包括 Netskope、Palo Alto Networks、Proofpoint、Zscaler 或自建 AI 安全服务器。安全厂商也可基于文档化 schema 构建集成。

## 实践意义

inference hooks 解决了企业 AI 部署中"统一内容检查"的核心痛点：此前每个 Claude 产品需单独集成 DLP，运维成本高且易遗漏。单一执行层覆盖全部界面后，安全团队可在一处策略管控所有 AI 交互。对于强合规行业（金融、医疗），这意味着可以将 Claude 纳入现有 DLP 管控范围而非建立平行体系。与自托管环境和 auto mode 配合，构成"数据驻留 + 内容检查 + 操作决策"的三层企业安全栈。

## 跨厂商对比

- 与 [How We Contain Claude Across Products](how-we-contain-claude-across-products.md) 对比：后者阐述 Anthropic 如何在不同产品间隔离和约束 Claude 行为（产品级隔离架构），inference hooks 则将检查点从产品内部延伸到客户侧 DLP 服务器，让企业自己定义内容策略边界
- 与 [Run Claude Code Sessions on Your Own Compute](run-claude-code-sessions-on-your-own-compute.md) 互补：自托管解决数据驻留（代码/密钥不出基础设施），inference hooks 解决内容检查（prompt/响应经过 DLP），两者分别覆盖"数据在哪"和"数据说了什么"

## 资源

- 论文：N/A
- 代码：N/A
- Demo：https://platform.claude.com/docs/en/manage-claude/inference-hooks
