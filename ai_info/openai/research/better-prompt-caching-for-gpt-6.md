# GPT-6 提示词缓存改进:最高 90% 折扣与 30 分钟窗口(Better prompt caching for GPT-6)

- **原文链接**: [Better prompt caching for GPT-6](https://openai.com/index/better-prompt-caching-for-gpt-6/)
- **作者**: OpenAI(官方博客)
- **发布日期**: 2026-09-22
- **检索日期**: 2026-09-29
- **标签**: #PromptCaching #GPT-6 #成本优化 #智能体基础设施 #API设计

## 核心观点

OpenAI 工程与产品团队改进 GPT-6 系列的提示词缓存(prompt caching):更高的缓存命中率、新的诊断工具(diagnostics)、显式缓存断点(explicit breakpoints)以及更细的控制项,整体目标是降低延迟与成本。第三方媒体 mixed-news 的解读给出关键数字:缓存输入的折扣最高可达 90%,条件是同一前缀在 30 分钟窗口内复用。

对智能体类负载(系统提示 + 工具定义 + 会话历史构成的长公共前缀、反复请求),这是数量级的成本优化;显式断点则让开发者可指定缓存切分点,避免长前缀中微小变动导致整段缓存失效——这正是过去一年智能体账单失控的主要根因之一。

## 关键发现 / 关键技术

### 1. 关键数字

| 项 | 数值/口径 |
|----|-----------|
| 缓存输入折扣 | 最高可达 90% |
| 复用条件 | 同一前缀在 30 分钟窗口内复用 |
| 整体目标 | 降低延迟与成本 |

### 2. 四项改进
- 更高的缓存命中率。
- 新的诊断工具(diagnostics):缓存命中率从黑盒变成可观测指标。
- 显式缓存断点(explicit breakpoints):指定缓存切分点,隔离易变内容。
- 更细的控制项。

### 3. 智能体负载的收益结构
- 智能体请求的公共前缀(系统提示、工具定义、会话历史)长且稳定,缓存命中率天然高。
- 过去的痛点:前缀中任何微小变动(如时间戳、动态上下文)会让整段缓存失效。
- 诊断工具的意义:缓存命中率进入 SRE 指标体系,成本优化从『事后看账单』变为『事前可调参』。

## 实践意义

1. **立即可做的重构**:重构提示词结构——稳定内容前置、动态内容后置,通常能立刻省下大比例费用。
2. **账单可观测**:用诊断工具把缓存命中率纳入智能体运维看板。
3. **迁移成本模型**:Anthropic 与 Google 的缓存计费(分钟级 TTL、自动前缀匹配)各有取舍,跨厂商迁移时需重算成本模型。
4. **与定价攻势同日**:本改进与 09-22 Sol/Luna 发布同日,显示 OpenAI 正同时从定价与效率两侧攻企业 TCO。

## 跨厂商对比

- 与 [用 Claude Platform 降低成本并提升性能](../../anthropic/engineering/reducing-cost-and-improving-performance-with-claude-platform.md) 对比:Anthropic 的提示词缓存走分钟级 TTL + 自动前缀匹配,GPT-6 以 30 分钟窗口 + 显式断点换控制力;两家都把缓存做成智能体成本优化的第一杠杆。
- 与 [Introducing GPT-6 Sol and Luna](introducing-gpt-6-sol-and-luna.md) 互补:同日发布的『定价 + 效率』组合拳,共同攻企业总拥有成本。
- 与 [GPT-5.6 如何融合前沿智能与前沿效率](gpt-5-6-frontier-intelligence-efficiency.md) 构成叙事链:7 月的价格性能前沿叙事,到 9 月落到缓存级的工程细化。

## 资源

- 官方博客:[Better prompt caching for GPT-6](https://openai.com/index/better-prompt-caching-for-gpt-6/)
- 第三方解读:[mixed-news(英文版):30 分钟窗口、最高 90% 折扣](https://mixed-news.com/en/openai-gpt-6-prompt-caching-30-minute-window-90-percent/)、[mixed-news(德文版)交叉佐证](https://mixed-news.com/de/openai-rabattiert-zwischengespeicherte-gpt-6-eingaben-um-bis-zu-90-wenn-sie-sie-innerhalb-von-30-minuten-wiederverwenden/)
- 相关条目:[Introducing GPT-6 Sol and Luna](introducing-gpt-6-sol-and-luna.md)

> 注:openai.com 原文 403,本文基于官方 RSS 描述与 mixed-news 英/德双版交叉验证,官方 URL 已列于资源。
