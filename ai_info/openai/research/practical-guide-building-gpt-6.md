# GPT-6 家族模型选择与实战指南（A model guide for the GPT-6 family）

- **原文链接**: [A model guide for the GPT-6 family](https://openai.com/index/practical-guide-building-gpt-6)
- **作者**: OpenAI
- **发布日期**: 2026-10-02
- **检索日期**: 2026-10-16
- **标签**: #模型选型 #GPT-6 #提示工程 #推理档位 #生产化

## 核心观点

OpenAI 发布 GPT-6 家族的官方实践指南：教创业公司如何选模型、调推理档位（reasoning effort）、改进提示词与技能（skills）、协调工具调用，以及把工作流推向生产。这是继 GPT-4.1 提示指南之后又一篇"官方最佳实践"长文——GPT-6 家族（Astra / Sol / Luna 三档 + effort 滑块）的复杂度已到"不读指南就选错档"的程度，官方下场做选型教育。

## 关键发现 / 关键技术

### 1. 指南覆盖的五个维度（官方摘要口径）
1. 模型选择：按任务类型（编码/专业工作 vs 轻量日常）在 Astra 与 Sol/Luna 间分档。
2. 推理档位：调 reasoning effort 匹配问题难度，避免"用 ultra 解简单题"。
3. 提示与技能：用 skills 沉淀可复用能力，而非在 prompt 里反复贴上下文。
4. 工具协调：多工具调用的组织方式。
5. 生产化准备：工作流从原型到生产的迁移清单。

### 2. 语境：DevDay 后的配套文档
- 与 GPT-6.1 Sol（9/29）、dots/Codex 更新同周期发布——新品越密，选型教育越关键。

## 实践意义

1. **官方选型决策树的权威版本**：模型分档 × effort 档位 × 成本的三维选择有了官方坐标系，可直接嵌入团队的技术选型规范。
2. **Skills 优先于 Prompt**：指南把 skills 提到与提示并列的一等公民，预示"能力沉淀"从提示词工程走向资产化管理。

## 跨厂商对比

- 与 [GPT-4.1 Prompting Guide](gpt-4-1-prompting-guide.md) 谱系对照：4.1 时代讲"怎么提示"，GPT-6 时代讲"怎么选档 + 怎么沉淀技能"——提示工程正在升维为模型编排工程。
- 与 [A Practical Guide to Building Agents](a-practical-guide-to-building-agents.md) 互补：Agent 指南讲架构（模型+工具+指令），本文讲模型层的精细选择，两份文档构成完整的构建手册。

## 资源

- 官方指南：[A model guide for the GPT-6 family](https://openai.com/index/practical-guide-building-gpt-6)
- 相关条目：[introducing-gpt-6-sol-and-luna](introducing-gpt-6-sol-and-luna.md)

> 注:openai.com 原文 403，本文基于官方 RSS 摘要整理，仅官方单源，具体建议条目待官方页面可达后补充。
