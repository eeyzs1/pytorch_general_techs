# Basis 用 GPT-6 Astra 快 2 倍完成税务工作簿（Basis completes a tax workbook 2x faster with GPT-6 Astra）

- **原文链接**: [Basis completes a tax workbook 2x faster with GPT-6 Astra](https://openai.com/index/basis-tax-workbook-with-astra/)
- **作者**: OpenAI(官方博客)
- **发布日期**: 2026-09-28
- **检索日期**: 2026-09-29
- **标签**: #Basis #GPT-6-Astra #税务自动化 #表格智能体 #客户案例

## 核心观点

会计自动化公司 Basis 用 GPT-6 Astra 处理含 50 个工作表（tab）的复杂税务工作簿，完成速度较 GPT-5.6 Sol 快 2 倍；对用户意图更强的理解，让其在真实使用中更令团队放心。

案例的技术看点是 Astra 在电子表格这类"结构化 + 半结构化混合"介质上的长链条操作能力：50 个 tab 意味着跨表引用、口径一致性与中间校验，模型需要在数十步工具调用间保持全局状态——这正是"意图理解 × 计算机操作"的复合考验。注意对比对象是上代 GPT-5.6 Sol 而非第三方模型，属于自家代际对比，阅读时应留意口径。

## 关键发现 / 关键技术

### 1. 任务画像
- 介质：复杂税务工作簿，含 50 个工作表（tab）。
- 难点：跨表引用、口径一致性、中间校验——需在数十步工具调用间保持全局状态。

### 2. 结果与口径

| 指标 | 数值 | 口径说明 |
|------|------|----------|
| 完成速度 | 较 GPT-5.6 Sol 快 2 倍 | 自家代际对比，非第三方模型对照 |
| 可靠性 | 团队"更放心" | 来自更强的用户意图理解，主观信任口径 |

### 3. 能力解构
- **意图理解**：理解用户在表格场景的真实意图（算什么、对什么口径）。
- **计算机操作**：在数十步工具调用间维持全局状态，完成跨表长链条操作。
- 两者复合，构成"表格智能体"区别于聊天式分析的核心能力。

### 4. 行业语境
- 税务与会计是 OpenAI 垂直化战略（金融版 2026-09-10、法律版 2026-09-17）的相邻战场。
- Basis 这类垂直应用层公司借用模型能力，向 CPA 事务所交付"审查级"自动化。

## 实践意义

1. **可追溯性优先**：财税自动化的可靠性评估重点是可追溯性（每步计算可解释）与口径一致性校验——建议要求智能体输出计算链路而非只给结果。
2. **口径审读**：代际对比数字（快 2 倍）不能直接外推为跨厂商优势，采购对比需自行补第三方模型基准。
3. **表格智能体成品类**：与数据智能体、文档理解案例并读，"表格智能体"正在成为 2026 年企业 AI 的独立品类，值得单独建立评测集（跨表一致性、中间校验、口径漂移）。

## 跨厂商对比

- 与 [Building Self-Improving Tax Agents with Codex](building-self-improving-tax-agents-with-codex.md) 对照：同属税务场景，Codex 路线聚焦"自改进税务智能体"的构建方法，Basis 案例给出生产环境的代际提速数据——方法论与实证互补。
- 与 [Legora 用 GPT-6 Astra 数分钟审完 41 份文档](legora-financial-statement-review-with-astra.md) 互补：同为"大批结构化介质 + Astra"场景，Legora 处理文档群（41 份），Basis 处理表格群（50 个 tab），共同指向"长链条结构化操作"这一 Astra 的差异化能力。
- 与 [Kimi 金融行业 AI 解决方案](../../kimi/blog/kimi-financial-industry-ai-solution.md) 对比：Kimi 从行业解决方案层切入金融，OpenAI 生态从税务工作簿这类具体工作流切入财税——垂直化竞争正在从"行业版"下沉到"工作流级"。

## 资源

- 官方博客：[Basis completes a tax workbook 2x faster with GPT-6 Astra](https://openai.com/index/basis-tax-workbook-with-astra/)
- 相关条目：[Building Self-Improving Tax Agents with Codex](building-self-improving-tax-agents-with-codex.md)、[Legora 用 GPT-6 Astra 数分钟审完 41 份文档](legora-financial-statement-review-with-astra.md)
- 第三方报道：待补

> 注:openai.com 原文 403,本文基于官方 RSS 官方描述整理,仅官方单源,待第三方验证补充。
