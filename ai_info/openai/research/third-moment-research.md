# Third Moment Research：让 1 万个智能体持续运行 36 小时以上（How Third Moment Research runs 10,000 agents for 36+ hours）

- **原文链接**: [How Third Moment Research runs 10,000 agents for 36+ hours](https://openai.com/index/third-moment-research)
- **作者**: OpenAI（客户案例：Third Moment Research）
- **发布日期**: 2026-10-14
- **检索日期**: 2026-10-16
- **标签**: #长视野智能体 #大规模并发 #GPT-6 #Codex #Daybreak

## 核心观点

AI 研究机构 Third Moment Research 用 GPT-6 Astra 与 GPT-6.1 Sol（编码/Codex/智能体编排）加 Daybreak（网络安全）搭建"能连续专注数天、越用越好"的长视野智能体系统，单次运行可同时维持 1 万个智能体连续工作 36 小时以上。这是目前公开口径下规模最大的长时并发智能体运行之一，把"长视野任务"的边界从小时级推到天级。

## 关键发现 / 关键技术

### 1. 规模指标
- 并发智能体：10,000 个；连续运行时长：36+ 小时。
- 模型分工：GPT-6 Astra（前沿推理）+ GPT-6.1 Sol（高性价比编码/计算机操作）+ Codex（执行环境）+ Daybreak（安全侧）。

### 2. "越用越好"的闭环
- 官方摘要强调 agents "improve with use"——运行中积累的轨迹与反馈回流为改进素材，与 OpenAI 自身"研究加速"叙事（3.1 agent-工作日/人类工作日）同构。

## 实践意义

1. **长视野工程的参照点**：1 万并发 × 36 小时给"持久化工作区、可验证步骤、监督判断"这套 Codex 方法论提供了外部验证规模。
2. **模型分档在大规模运行中的必要性**：前沿模型与 1/5 价格模型混编，是控制天级运行成本的现实方案。

## 跨厂商对比

- 与 [Codex-Maxxing for Long-Running Work](codex-maxxing-long-running-work.md) 对照：Codex 白皮书给方法论（持久化、可验证、人类监督），本案例给出已验证的规模上限——方法论 + 实测的组合。
- 与 [Perplexity 把端到端系统托付给 GPT-6 Astra](perplexity-accuracy-with-astra.md) 同观：一周内两个"把生产系统整体交给长视野智能体"的案例，长时可靠性正从卖点变为采购标准。

## 资源

- 官方案例：[How Third Moment Research runs 10,000 agents for 36+ hours](https://openai.com/index/third-moment-research)
- 相关条目：[research-acceleration-view-inside-openai](research-acceleration-view-inside-openai.md)

> 注:openai.com 原文 403，本文基于官方 RSS 摘要整理，仅官方单源，待第三方验证补充。
