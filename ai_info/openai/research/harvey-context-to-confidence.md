# Harvey 用 GPT-6 Astra 把法律上下文变成更可靠的草稿（Harvey turns legal context into stronger drafts with GPT-6 Astra）

- **原文链接**: [Harvey turns legal context into stronger drafts with GPT-6 Astra](https://openai.com/index/harvey-from-context-to-confidence-with-astra/)
- **作者**: OpenAI(官方博客)
- **发布日期**: 2026-09-23
- **检索日期**: 2026-09-29
- **标签**: #Harvey #GPT-6-Astra #法律科技 #文书起草 #客户案例

## 核心观点

法律 AI 公司 Harvey 用 GPT-6 Astra 产出更结构化、更贴合上下文的法律文书草稿，让律师把时间集中在策略判断上。技术叙事的核心是"context into confidence"：法律草稿的质量瓶颈不在文采，而在事实与判例上下文的忠实度——Astra 的改进被表述为更强的上下文保持与结构化输出（条款层级、定义引用一致性），直接减少律师逐条核对的时间。

该案例与 2026-09-17 的 Astra for Law 构成微妙三角：Harvey 是构建在 OpenAI 模型上的独立法律应用层领军者（服务大量大所），而 OpenAI 自己又发布了面向律所的平台级产品——平台与生态客户既合作又潜在竞争的关系在此暴露无遗，Harvey 亦同时使用多家模型以对冲。

## 关键发现 / 关键技术

### 1. "Context into Confidence"
- 法律草稿的质量瓶颈：不在文采，而在事实与判例上下文的忠实度。
- Astra 的两项改进：
  - 更强的上下文保持——长材料中的事实与判例不漂移。
  - 结构化输出——条款层级、定义引用一致性，减少逐条核对时间。

### 2. 人机分工
- 智能体产出结构化草稿，律师把时间集中在策略判断上。
- 律师的价值从"起草"转向"判断与签字"。

### 3. 平台 × 生态的竞合结构

| 角色 | 动作 |
|------|------|
| Harvey | 基于 OpenAI 模型的独立法律应用层，服务大量大所；同时使用多家模型对冲 |
| OpenAI | 2026-09-17 自营发布 Astra for Law 平台级产品 |
| 关系 | 既合作（模型供给）又潜在竞争（争同一批律所预算） |

## 实践意义

1. **区分两种能力**：律所评估法律 AI 时应区分"模型能力"与"工作流产品力"——Harvey 的价值在后者：与 DMS、判例库、模板体系的集成。
2. **应用层护城河**：在模型厂商垂直化（OpenAI 自营法律版）压力下，应用层公司的护城河必须建立在数据、工作流与合规审计，而非裸模型调用。
3. **多模型对冲**：Harvey 同时使用多家模型的做法，值得所有应用层公司借鉴——避免单一供应商既是供给方又是竞争方时的议价劣势。

## 跨厂商对比

- 与 [Legora 用 GPT-6 Astra 数分钟审完 41 份文档](legora-financial-statement-review-with-astra.md) 对照：同为法律行业 Astra 案例，Legora 聚焦核对（tie-out）类穷举工作流并给出任务级基准数据，Harvey 聚焦起草类生成工作流——两者拼出法律 AI"审"与"写"两大场景。
- 与 [Kimi 金融行业 AI 解决方案](../../kimi/blog/kimi-financial-industry-ai-solution.md) 对比：同为"垂直行业 + 前沿模型"打法，Kimi 从金融行业切入，OpenAI 生态从法律（Harvey/Astra for Law）切入——垂直化已是中外厂商的共同路线。

## 资源

- 官方博客：[Harvey turns legal context into stronger drafts with GPT-6 Astra](https://openai.com/index/harvey-from-context-to-confidence-with-astra/)
- 第三方报道：[The Hindu：OpenAI 法律平台加剧律所用户争夺](https://www.thehindu.com/sci-tech/technology/openai-launches-legal-focused-ai-platform-escalating-race-for-law-firm-users/article71479273.ece)（佐证 Harvey 与 Astra for Law 并存格局）
- 相关条目：[Legora 用 GPT-6 Astra 数分钟审完 41 份文档](legora-financial-statement-review-with-astra.md)

> 注:openai.com 原文 403,本文基于官方 RSS 描述 + The Hindu 报道交叉验证,官方 URL 已列于资源。
