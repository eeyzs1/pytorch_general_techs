# AI 原生 SDLC 手册（The AI-Native SDLC playbook）

- **原文链接**: [The AI-Native SDLC playbook](https://claude.com/blog/the-ai-native-sdlc-playbook)
- **作者**: Anthropic Applied AI 团队（致谢 Jim Blackhurst、Will Steuk、Jamal Arif）
- **发布日期**: 2026-08-21
- **检索日期**: 2026-09-09
- **标签**: #SDLC #AgenticSDLC #ClaudeCode #工程治理 #意图工件

## 核心观点

传统 SDLC 为"写代码是最耗时最昂贵的阶段"而设计；当 Claude Code 这类 Agent 把构建压缩到小时级，瓶颈便转移到构建左右的规划、评审/测试与部署，逐行人审的控制方式与现实脱节，治理成本反而上升。产出最高价值的组织已围绕 Agent 能力重造流程，同时让人保持在环。

Anthropic Applied AI 团队发布 AI 原生 SDLC 分阶段手册：六个阶段（规划、设计、构建、测试、部署、维护）从线性流程变成闭环，每阶段以提交一个可机读工件收尾——intent.md、spec.md、plan.md、diff 及其测试、PR 与评审记录、事件记录——下一阶段从读取它开始，提交链即审计链。

手册为每个 play 给出起步条件、实施步骤、治理考量与领先/滞后指标，人类判断保留在各个门上。

## 关键发现 / 关键技术

### 1. 工件驱动的六阶段闭环
- Plan：发起者用 Claude 头脑风暴并直接写 intent.md 入版本控制，无需产品团队代笔；产品负责人审校后提交。Design：需求与设计压缩为一次会话，政策以 skills 形式编码进 git，前端可在 Claude Design 中从 intent.md 生成设计稿。
- Build：Plan mode 强制先批准计划再动文件，auto mode 让例行事免逐条确认；CLAUDE.md 与 skills 承载机构知识。Test：continuous evals（持续评估）作为合并门贯穿实现过程，生产事件应转化为永久 eval。

### 2. 部署与治理：hooks 作为确定性闸门
- Deploy 阶段 Claude 双向参与评审：既按组织政策审别人的 PR，也处理自己 PR 上的评审意见；人类注意力上移到"变更是否符合计划意图、风险是否可接受"。
- 治理原则是"Agent 可以一路做到生产门，但不能越过它"：分支保护让 Agent 产出只能走 PR；生产部署 hook 必须由具名发布经理授权；按环境分层授权；回滚是演练最充分的路径，部署工具经 MCP 暴露为受限工具。

### 3. 维护阶段：闭环自治运行
- 确定性脚本监控生产指标（如 Western Electric 规则的 bands.yaml 分层：1σ 记录、2σ 只读诊断、3σ 提案），越限时才调用 Claude，诊断结果写成新 intent.md 重启整个管线。
- Claude Security 提供托管定时扫描（运行于 Mythos 5），发现带 CWE 分类与置信度、经人工评审出补丁；Claude Tag（Slack 公测）让 Claude 以独立身份值守事件频道，事后复盘写入版本化 lessons 文件。

## 实践意义

这是目前最完整的"组织级 Claude 化流程再造"参考：它不是教个体工程师怎么用 Claude Code，而是回答"当代码产出速度提升一个量级后，审批、评审、安全、合规、值班怎么跟着改"。对受监管企业尤其有参考价值——每个 play 都附带治理考量和度量方式（DORA 指标、门等待时长、eval 通过率、重复事件率）。`intent.md → spec.md → plan.md → diff/测试 → PR → 事件记录` 的工件链也给多 Agent 流水线提供了可审计的最小接口设计。

## 跨厂商对比

- 与 [Claude Code: Best Practices for Agentic Coding](claude-code-best-practices.md) 对比：best practices 聚焦单个工程师的 Claude Code 使用技巧（CLAUDE.md、探索-实现-提交工作流等）；本文把视角抬到组织级，改造的是代码之外的整个生命周期流程与治理结构。
- 与 [Harness Engineering: Building the Codex App Server for an Agent-First World](../../openai/research/harness-engineering.md) 互补：OpenAI 讲 Agent-first 世界里服务端 harness 的架构工程（零手写代码、AGENTS.md 约定），Anthropic 这篇讲围绕 Claude 的六阶段流程与门禁治理——一个在基础设施层，一个在流程层，可对照采用。

## 资源

- 论文：N/A
- 代码：N/A（配套 Claude Code 管理文档见 code.claude.com/docs，文中附完整清单）
- 官方文章：https://claude.com/blog/the-ai-native-sdlc-playbook
