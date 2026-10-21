# Claude Haiku 5.5：小模型价格再砍 75%，5.5 家族集齐（Introducing Claude Haiku 5.5）

- **原文链接**: [Introducing Claude Haiku 5.5](https://www.anthropic.com/claude-haiku-5-5)
- **作者**: Anthropic
- **发布日期**: 2026-10-07
- **检索日期**: 2026-10-16
- **标签**: #ClaudeHaiku55 #模型发布 #小模型 #成本优化 #effort档位 #缓存降价

## 核心观点

Claude Haiku 5.5（2026-10-07 发布）补齐 5.5 家族最后一块：史上最便宜、最快、最强的小模型，平均运行成本比 Haiku 4.5 低约 75%，面向高吞吐、成本敏感型工作（摘要、压缩、数据库查询、分类），也是编码工作中理想的 subagent 档，以及实时客服、浏览器操作等延迟敏感场景的最快选择。

基准呈现"小模型质变"：GDPval-AA 1620 对 Haiku 4.5 的 735——翻倍以上，且超过 GPT-6 Luna 的 1437；OSWorld 2.1 从 15.7% 跃至 72.4%；Terminal-Bench 4.0 从 0% 到 39.2%。首个带 effort 档位的 Haiku，把"按成本或按智力优化"的选择权下沉到入门档。同步宣布：Sonnet 5.5 缓存读减半至 $0.10（agentic 工作约再省 20%），Max/Team 新增每月 API 额度。

## 关键发现 / 关键技术

### 1. 基准：对上一代翻倍、跨厂商领先
- GDPval-AA v2.1：1620（Haiku 4.5 为 735，GPT-6 Luna 1437，Sonnet 5.5 1840）
- AA-Briefcase v1.1：1578（上代 614，Luna 1336）
- OSWorld 2.1（离线子集）：72.4%（上代 15.7%，Luna 48.9%）
- HLE 无工具 45.9% / 带工具 57.4%；Terminal-Bench 4.0 39.2%（上代 0%，Luna 16.4%）；FrontierCode 1.1 46.4%（超 Luna 的 42.4%）
- 客户证言：Asana AI Teammates 延迟降 30%+、单轮推理最快 2.5×

### 2. 定价：100k token 分界线
- 输入 $0.10（≤100k）/ $0.50（>100k）；输出 $0.50 / $2.50；缓存读 $0.01 / $0.05；缓存写 $0.125 / $0.625
- 对比 Haiku 4.5（$1/$5/$0.10）：全线约 90% 降幅；约 90% 的 Haiku 请求 prompt 不到 100k
- 大分屏定价把长上下文滥用的成本内部化，短 prompt 高吞吐场景拿到极致低价

### 3. 家族与生态联动
- 首个带可调 effort 的 Haiku（low/medium/high/xhigh/max）
- 网络护栏比 Haiku 4.5 严、比近期大模型略宽：放行防御性任务、拦截渗透测试类；生物学护栏与 Sonnet 5/5.5、Opus 5 相同
- 对齐评估多数指标较上代改善；系统卡公开
- Sonnet 5.5 缓存读 $0.20→$0.10，多数 agentic 工作成本再降约 20%；Max/Team 每月 API credit

## 实践意义

5.5 家族三档齐备（$0.1/$2/$4 输入价），"subagent 经济"被重新定价：批量分类/检索/摘要类 subagent 应立即迁移 Haiku 5.5，其 GDPval 超过上代 Luna 级竞品意味着"小模型 = 低能力"的假设失效，多 agent 架构中主控 Opus + 执行 Haiku 的成本结构比上代优化一个数量级。Sonnet 缓存读减半对重度 agentic 用户是被动收益——无需改动即可省 20%，但值得重跑成本基准以重新分配 effort 档位预算。

## 跨厂商对比

- 与 [Introducing Claude Sonnet 5.5](claude-sonnet-5-5.md) 对比：Sonnet 5.5 以 $2/$10 在 TB 4.0 反超旗舰，Haiku 5.5 以 $0.1/$0.5 把"GPT-6 Luna 级能力"打到十分之一价格——5.5 家族的"每档都是上代旗舰能力"策略完整落地
- 与 [Claude Opus 5.5](claude-opus-5-5.md) 互补：Opus 承接最难任务并首次配 Fable 级防护，Haiku 承接高频 subagent 与延迟敏感场景——同一发布周期的两端
- 与 [Introducing GPT-6 Sol and Luna](../../openai/research/introducing-gpt-6-sol-and-luna.md) 对比：OpenAI 以 Sol/Luna 拉开 API 半价攻势，Anthropic 用 Haiku 5.5 的 75% 降幅 + 分屏定价回应——小模型价格战进入"按 prompt 长度分层"的精细阶段

## 资源

- 发布页：https://www.anthropic.com/claude-haiku-5-5
- 系统卡：https://www.anthropic.com/claude-haiku-5-5-system-card
- 代码：无
- Demo：无
