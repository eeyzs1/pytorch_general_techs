# 如何在智能体时代管理 AI 投资（How to manage AI investments in the agentic era）

- **原文链接**: [How to manage AI investments in the agentic era](https://openai.com/index/managing-ai-investments-in-agentic-era/)
- **作者**: OpenAI
- **发布日期**: 2026-07-14
- **检索日期**: 2026-08-01
- **标签**: #AI投资 #ROI #企业采用 #支出控制 #ChatGPT_Work #成本治理

## 核心观点

OpenAI 面向企业领导者提出智能体时代 AI 投资的五步框架：提升使用与支出透明度、以最终 ROI 评估模型效率、在高级工作流规模化前建立治理、投资具备复利效应的工作流、让算力匹配已验证需求。核心主张是：token 单价不等于价值，领导者应关注"每美元产出的有效工作"（useful work per dollar）——完成的任务、节省的时间、改善的决策和可扩展的工作流。

文章给出关键数据：从 GPT-4 到 GPT-5.4，每百万 token 价格下降 97%；GPT-5.6 在 Artificial Analysis Coding Agent Index 中以少 54% 的输出 token、少 57% 的单任务耗时取得更优表现。随着团队从对话转向长周期工作流，管理员需要更清晰地掌握需求、支出与风险。

## 关键发现 / 关键技术

### 1. 透明度是投资前提
- 管理员需看清"谁在用、用哪些产品/模型、消耗多少算力、支撑什么工作"，否则无法解读账单是浪费还是业务关键
- 管理控制台的使用情况分析与支出控制可按用户/产品/模型查看采用率、额度与支出趋势
- 三个层级的洞察：工作空间（采用与支出是否同步增长）、团队与用户（需求增长点）、产品与模型（高价智能用在何处）

### 2. 以成果 ROI 而非 token 单价评估模型
- 最低 token 价格不等于最低总成本：便宜模型可能失败重试、产出需人工修正
- 对优先级工作流跟踪"每个被接受成果的成本"（客服=已解决工单，工程=通过评审的变更），并与业务价值配对
- 用反映真实任务（含边缘案例）的评估先定义"足够好"，再测算达标全成本

### 3. 治理、复利工作流与容量匹配
- 高级工作流规模化前先建立治理：权限、审批、审计
- 优先投资能持续累积价值的复利型工作流（模板、技能、数据连接可复用）
- 按已验证需求配置算力，避免过度预购或瓶颈阻塞

## 实践意义

这是 OpenAI 首次系统给出企业 AI 支出的"治理框架"，实质是把云计算 FinOps 方法论迁移到 token 经济。对采购与平台团队的直接启示：建立"每成果成本"指标优于"每 token 成本"；模型选型应按工作流分层（Sol 定计划、Luna 跑执行）；支出分析工具已成为企业 AI 平台的标配组件。该框架与 GPT-5.6 三档模型家族（Sol/Terra/Luna）形成产品与方法论的自洽闭环。

## 跨厂商对比

- 与 [ChatGPT 企业支出控制](chatgpt-enterprise-spend-controls.md) 互补：前者是工具发布，本文是使用该工具进行管理决策的方法论
- 与 [如何构建 AI 原生工程团队](building-an-ai-native-engineering-team.md) 对比：一个管"钱"（投资回报），一个管"人"（组织形态），共同构成企业 AI 转型的两个侧面
- 与 [Anthropic 经济指数报告](../../anthropic/research/economic-index-june-2026-report.md) 互补：Anthropic 提供宏观使用分布数据，OpenAI 提供微观投资决策框架

## 资源

- 原文：[How to manage AI investments in the agentic era](https://openai.com/index/managing-ai-investments-in-agentic-era/)
- 工具：[Usage analytics and spend controls](https://openai.com/index/chatgpt-enterprise-spend-controls/)
