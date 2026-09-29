# GPT-6 Sol 与 Luna:价格减半、9% 成本胜 Opus 5(Introducing GPT-6 Sol and Luna)

- **原文链接**: [Introducing GPT-6 Sol and Luna](https://openai.com/index/introducing-gpt-6-sol-and-luna/)
- **作者**: OpenAI(官方博客)
- **发布日期**: 2026-09-22
- **检索日期**: 2026-09-29
- **标签**: #GPT-6 #Sol #Luna #价格战 #模型分级

## 核心观点

OpenAI 发布 GPT-6 家族的两款新模型 Sol 与 Luna,把『前沿智能』带向日常工作负载,两者在能力与成本上提供不同平衡:Sol 偏强推理、Luna 主打轻量高效。第三方报道(mixed-news)披露激进定价:GPT-6 Sol/Luna API 价格减半,且 OpenAI 宣称 Sol 以约 9% 于 Anthropic Opus 5 的成本即可胜过后者——这是对 Anthropic 企业旗舰的直接价格战;百度百家号等中文媒体以『OpenAI 与 Anthropic 同日上新』记录了 9 月 22 日两家对垒的场面。

产品逻辑上,Sol/Luna 补齐了 Astra(旗舰)与 GPT-5.6(上代性价比)之间的档位,配合同日发布的提示词缓存改进,构成完整的『每美元智能』攻势,承接 7 月 GPT-5.6『前沿智能 × 前沿效率』的叙事。

## 关键发现 / 关键技术

### 1. 双模型分工
- Sol:偏强推理,面向复杂推理任务。
- Luna:主打轻量高效,面向高频解析类负载。
- 两者把『前沿智能』带向日常工作负载,与 Astra(最高能力)形成三档格局。

### 2. 定价与对标

| 项 | 数值/口径 |
|----|-----------|
| Sol/Luna API 价格 | 减半 |
| Sol vs Anthropic Opus 5 | 约 9% 的成本即可胜过(OpenAI 宣称) |
| 档位 | 补齐 Astra(旗舰)与 GPT-5.6(上代)之间 |

### 3. 同日对垒的行业场面
- 9 月 22 日 OpenAI 与 Anthropic 同日发布新模型,被中文媒体记录为两家正面对垒。
- 同日还有 GPT-6 提示词缓存改进发布,定价与效率两侧同步发力。

## 实践意义

1. **选型矩阵重排**:重推理任务用 Astra/Sol、高频解析任务用 Luna,并结合缓存策略优化总账;先做任务分层审计,再分配模型档位。
2. **自托管经济性受压**:对开源阵营,价格持续下探将挤压自托管的经济理由。
3. **竞争连锁反应**:Opus 5 面临『更贵却未必更强』的公关压力,预期 Anthropic 将在下月发布回应性定价或新旗舰。
4. **V7 类案例的范式确认**:用 Luna 处理海量低难度环节、把旗舰留给强推理聚合环节,正是本分层定价鼓励的工程模式。
5. **采购谈判窗口**:价格战期是把降价与缓存折扣条款写入企业协议的好时机。

## 跨厂商对比

- 与 [Claude Opus 5.5 发布](../../anthropic/research/claude-opus-5-5.md) 直接对标:OpenAI 以『约 9% 成本胜 Opus 5』的口径发起价格战,Anthropic 企业旗舰(Opus 成本已下探 Fable 水平)的溢价空间被直接挑战。
- 与 [GPT-5.6:前沿智能,随雄心扩展](introducing-gpt-5-6.md)、[GPT-5.6 推进价格性能前沿](advancing-the-price-performance-frontier-with-gpt-5-6.md) 构成叙事链:7 月确立『前沿智能 × 前沿效率』,9 月 Sol/Luna 是其档位化延续。
- 与 [Better prompt caching for GPT-6](better-prompt-caching-for-gpt-6.md) 互补:同日发布,定价与效率两侧同时攻企业 TCO。
- 与 [DeepSeek-V4.1-Flash 发布](../../deepseek/news/deepseek-v4-1-flash.md) 对比:低成本高性能档位是全行业共同战场,开源阵营的低价优势正被前沿厂商降价压缩。

## 资源

- 官方博客:[Introducing GPT-6 Sol and Luna](https://openai.com/index/introducing-gpt-6-sol-and-luna/)
- 第三方报道:[mixed-news:价格减半、9% 成本胜 Opus 5](https://mixed-news.com/en/openai-halves-gpt-6-api-prices-sol-luna-opus-5-cost/)、[百度百家号:OpenAI 与 Anthropic 同日上新](https://baijiahao.baidu.com/s?id=1877124042939649616)
- 相关条目:[GPT-6 Astra:面向工作的下一代智能](gpt-6-astra-next-generation-of-work.md)、[Better prompt caching for GPT-6](better-prompt-caching-for-gpt-6.md)

> 注:openai.com 原文 403,本文基于官方 RSS 描述与 mixed-news/百度百家号交叉验证,官方 URL 已列于资源。
