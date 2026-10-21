# GPT-6.1 Sol 发布：以 Astra 五分之一的价格逼近 Astra（Introducing GPT-6.1 Sol）

- **原文链接**: [Introducing GPT-6.1 Sol](https://openai.com/index/introducing-gpt-6-1-sol)
- **作者**: OpenAI
- **发布日期**: 2026-09-29
- **检索日期**: 2026-10-16
- **标签**: #GPT-6.1Sol #模型发布 #性价比 #编程智能体 #计算机操作

## 核心观点

GPT-6.1 Sol 在 DevDay 2026 当天发布，定位一句话说清：在复杂编程、计算机操作和专业工作上做到接近 GPT-6 Astra 的水平，但 API 价格维持在 Sol 档——标准输入/输出价格仅为 Astra 的五分之一。它是 9/22 [GPT-6 Sol/Luna 降价](introducing-gpt-6-sol-and-luna.md)之后的快速迭代（GPT-6 Sol 发布仅一周），延续 Sol 系列"高性价比专业档"的家族定位，并与 dots、ChatGPT Space 同日组成"Agent 时代"产品矩阵的模型底座。

版本关系上，Sol 谱系为：GPT-5.6 Sol（7 月，效率工程主角）→ GPT-6 Sol（9/22，价格减半、约 9% 成本胜 Opus 5）→ GPT-6.1 Sol（9/29，near-Astra 能力补齐）。官方同时预告 GPT-6.1 Sol 的 Ultrafast 高速模式"未来几天"上线。

## 关键发现 / 关键技术

### 1. Agent 基准：三项中两项逼近或超越 Astra

| 基准 | GPT-6.1 Sol | GPT-6 Astra |
|------|-------------|-------------|
| DeepSWE v1.1（编程） | 75.22% | 73.23% |
| OSWorld 2.0（计算机操作） | 71.42% | 73.49% |
| Terminal-Bench Science（科学任务） | 57.02% | 68.10% |

- 编程反超、GUI 操作接近，科学推理仍有明显差距——"near-Astra"是有分寸的表述。

### 2. 定价与开放范围
- API：输入 $2/M tokens、输出 $10/M tokens、缓存输入 $0.1/M——与 GPT-6 Sol 同档（Astra 的 1/5）。
- 开放 Plus、Pro、Business、Enterprise、Edu 用户，可在 ChatGPT Work 与 Codex 使用；首发暂不进入普通 ChatGPT 对话。

### 3. 产品化语境
- 与 Ultrafast、Pro 500 同场：OpenAI 把"最强速度"（Astra Ultrafast）留在高档订阅，把"接近最强的工作能力"（6.1 Sol）做成低价 API——分层售卖能力与速度两个维度。

## 实践意义

1. **旗舰=最强的叙事进一步失效**：编程与计算机操作这类"可验证工作"上，中档价格模型已可反超旗舰，工程选型应按任务类型分档（科学/深度推理仍需 Astra）。
2. **成本工程有了新锚点**：$2/$10 + 90% 缓存折扣的组合使长时 Agent 工作流（配合 dots/Codex）的单位任务成本大幅下降。
3. **版本节奏加快**：Sol 一周内两迭代（6 Sol → 6.1 Sol），采购与评测周期必须跟上"次旗舰季度多刷"的节奏。

## 跨厂商对比

- 与 [GPT-6 Sol 与 Luna：价格减半](introducing-gpt-6-sol-and-luna.md) 直接衔接：9/22 确立 Sol 档价格锚（约 9% 成本胜 Opus 5），9/29 的 6.1 Sol 在同价位补齐能力，是同一价格战略的第二步。
- 与 [GPT-6 Astra 发布](gpt-6-astra.md) 对比：Astra 以 ARC-AGI-3 99.9%、Critical 级网络能力立"能力上限"，6.1 Sol 以 1/5 价格覆盖 80-100% 的日常 Agent 工作负载，两者构成明确的能力-价格阶梯。
- 与 [Anthropic Claude Sonnet 5.5 发布](../../anthropic/research/claude-sonnet-5-5.md) 同观：Sonnet 5.5 以中档模型 Terminal-Bench 4.0 反超 Opus 5.5，GPT-6.1 Sol 以 1/5 价格编程反超 Astra——中档模型反超旗舰是 9 月跨厂商的共同现象。

## 资源

- 官方发布：[Introducing GPT-6.1 Sol](https://openai.com/index/introducing-gpt-6-1-sol)
- 第三方验证：[DoNews/字母榜 DevDay 综述（含基准数字）](https://www.donews.com/article/detail/6885/107984.html)、[The Next Web: Near-Astra intelligence for a fifth of the price](https://thenextweb.com/news/openai-gpt-6-1-sol-price-astra-devday)、[llm-stats 技术深析](https://llm-stats.com/blog/research/gpt-6-1-sol-launch)
- 相关条目：[devday-2026-recap](devday-2026-recap.md)、[better-prompt-caching-for-gpt-6](better-prompt-caching-for-gpt-6.md)

> 注:openai.com 原文 403；基准与定价数字经官方 RSS 摘要 + DoNews/TNW/llm-stats 三个独立第三方源交叉验证。
