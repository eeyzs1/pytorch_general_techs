# Asana 用 GPT-6.1 Sol 把浏览器智能体成本降 76 倍（Asana cuts model costs 76x in browser tests with GPT-6.1 Sol）

- **原文链接**: [Asana cuts model costs 76x in browser tests with GPT-6.1 Sol](https://openai.com/index/asana-browser-agent)
- **作者**: OpenAI（客户案例：Asana）
- **发布日期**: 2026-10-09
- **检索日期**: 2026-10-16
- **标签**: #浏览器智能体 #成本优化 #GPT-6.1Sol #Codex #Asana

## 核心观点

Asana 在 Codex 中用 GPT-6 Astra 重构其浏览器智能体（browser agent）的测试方案，使浏览器测试的模型成本下降 76 倍、速度提升 5 倍——从而能把更强的模型装进面向客户的产品。这是 GPT-6.1 Sol 发布十天后首个公开的"76× 降本"工程案例：n­ear-Astra 模型 + Codex 执行环境组合拳，把此前不可行的重度 UI 自动化测试变成日常可跑的基础设施。

## 关键发现 / 关键技术

### 1. 量化成效
| 指标 | 变化 |
|------|------|
| 浏览器智能体测试模型成本 | ↓ 76× |
| 测试速度 | ↑ 5× |
| 手段 | Codex 中用 GPT-6 Astra 重构测试方案，日常运行迁移至 GPT-6.1 Sol 档 |

### 2. 方法含义
- 测试是 Agent 产品最烧 token 的环节之一（反复渲染、重试、长轨迹）；在 Codex 托管环境里用前沿模型重构测试本体、用低价模型日常执行，是"重构一次、便宜一万次"的成本范式。

## 实践意义

1. **Agent 产品的成本结构可再设计**：76× 说明"跑不起"的往往是测试与评估层，而非产品层——把重活搬到 1/5 价格模型上是通用打法。
2. **"向客户提供更强模型"的经济学**：内部成本每降一个数量级，面向客户的免费/含订阅能力就能升一档。

## 跨厂商对比

- 与 [Introducing GPT-6.1 Sol](introducing-gpt-6-1-sol.md) 直接衔接：发布时的"1/5 价格 near-Astra"承诺，十天内被客户转化为 76× 成本案例——价格信号到工程收益的传导速度快于以往任何一代。
- 与 Asana 8 月"两周完成多年测试系统迁移、约 $12K 成本"案例前后呼应：同一客户从"用 Codex 做迁移"到"用 GPT-6 Astra/Sol 降浏览器测试成本"，Asana 已成为 OpenAI 展示工程经济学的常驻样本（8 月案例未单独入库）。

## 资源

- 官方案例：[Asana cuts model costs 76x in browser tests](https://openai.com/index/asana-browser-agent)
- 相关条目：[advancing-computer-use-with-ironclad](advancing-computer-use-with-ironclad.md)

> 注:openai.com 原文 403，本文基于官方 RSS 摘要整理，仅官方单源，待第三方验证补充。
