# 企业 AI 经济学阅读路线

## 先读

- [A scorecard for the AI age](../openai/research/a-scorecard-for-the-ai-age.md)：面向 CFO 的 AI 价值四问记分卡——完成多少有效工作、每个成功任务全成本（含重试与人工监督）、可靠率三档追踪、规模经济性；衡量 AI 从"采用率"转向"完成的工作"。
- [How to manage AI investments in the agentic era](../openai/research/managing-ai-investments-in-agentic-era.md)：企业 AI 投资五步框架——支出透明度、以成果 ROI 而非 token 单价评估模型、治理前置、投资复利工作流、算力匹配已验证需求；GPT-4 到 GPT-5.4 每百万 token 价格已降 97%。

## 充裕智能与全栈战略

- [Building abundant intelligence](../openai/research/building-abundant-intelligence.md)：OpenAI 经济引擎的系统阐述——"更强智能 → 更广采用 → 更多投资 → 更高智能与效率"飞轮；模型触达 10 亿用户与 200 万家企业；Codex agentic 工作已占内部周输出 token 的 99.8%。

## 落地模式与组织重构

- [OpenAI launches the Deployment Company](../openai/research/openai-launches-the-deployment-company.md)：控股部署公司 + "前线部署工程师（FDE）"模式，40 亿美元初始投资、收购 Tomoro 获 150 名 FDE；企业 AI 下一阶段的瓶颈不在模型能力，而在部署到真实场景。
- [Introducing OpenAI Presence](../openai/research/introducing-openai-presence.md)：企业级 agent 产品——最小权限部署 + 策略/护栏/评估体系；自有电话支持渠道实战验证，75% 来电无需人工，Codex 改进循环 10 天降低人工转接率 15pp。

## 劳动力市场信号

- [How AI is expanding what people do at work](../openai/research/how-ai-is-expanding-what-people-do-at-work.md)："任务跨界"（task crossover）概念——基于 80 万条工作消息，43.5% 职业专属消息落在用户本职之外；任务层面的变化先于职位描述变化出现，是传统劳动力统计未捕捉的前瞻指标。
- [How agents are transforming work](../openai/research/how-agents-are-transforming-work.md)：Codex 经济影响论文——80.6% 个人用户提交了估计超 30 分钟人类工作的请求；非开发者用户增速超过开发者（个体 137×、组织 189×）。
- [Anthropic Economic Index: Cadences](../anthropic/research/economic-index-june-2026-report.md)：Claude 使用节奏与外部世界高度同步（工作日/周末、税务截止日）；任务越有价值消耗算力越多——token 消耗与映射职业工资正相关。

## 价格与成本工程

- [Advancing the price-performance frontier with GPT-5.6](../openai/research/advancing-the-price-performance-frontier-with-gpt-5-6.md)：Luna 降价 80%、Terra 降价 20%、Sol 推 Fast mode（2 倍价格换 2.5 倍速度）；Luna 以约 6% 的单任务成本达到一年前前沿级性能。
- [DeepSeek-V4 API 定价与峰谷计费](../deepseek/news/deepseek-v4-api-pricing.md)：大模型 API 首次引入电力行业式"峰谷计费"——高峰时段价格 2 倍；"价格屠夫"给算力装上计价器。
- [DeepSeek-V4-Pro GA 与 API 调价](../deepseek/news/deepseek-api-price-adjustment-2026-08.md)：价格战转向的标志性节点——部分模型涨幅最高 1100%、低峰时段价格为高峰 50%，峰谷分时计费全面落地；"以低价换规模"阶段结束，"合理定价换可持续"开始，开发者成本模型需把峰谷调度纳入架构设计。
- [GLM Coding Plan 套餐改版](../glm/blog/glm-coding-plan-pricing-revision.md)：国产编码订阅从"次数计费"转向"token 积分制"并引入峰谷系数（高峰 3 倍积分）——国产厂商计费模型集体重构，"集体变贵"成为 2026 下半年行业趋势。
- [The Future is for Everyone](../meta/the-future-is-for-everyone.md)：开源 AI 的经济学主张——Zuckerberg 以 6510 字论述"多超智能 + 开源防集中"，宣布 10 亿美元开放模型基金；"蒸馏开源"（旗舰闭源、衍生开源）成为 Meta 的算力投资与生态扩张双重叙事，与 OpenAI"充裕智能"的集中式算力投资形成路线对立。

## 关键结论

- 衡量 AI 价值的基本经济问题：AI 完成工作的价值增长是否快于其生产成本——token 只是中间产物，"成功成果的成本"才是正确度量。
- 最强模型一次做对，往往比便宜模型反复重试加人工修正更经济——按"成果需要多少智能"在同一工作流内分档混用模型成为标准采购逻辑。
- 企业 AI 竞争的下半场从模型能力转向部署能力——FDE 模式（OpenAI Deployment Company）与产品化护栏（Presence）是两种互补的商业化路径。
- 任务跨界数据（43.5%）表明 AI 对劳动力市场的重构先于职位变化发生——使用数据是比就业统计更早的领先指标。
- 前沿智能进入价格竞争阶段：OpenAI 三档降价、DeepSeek 峰谷计费、Claude Opus 5"半价逼近前沿"——"每美元有效工作"取代 benchmark 分数成为厂商叙事核心。
- 价格竞争出现分化：OpenAI 靠效率提升降价，DeepSeek/GLM 靠峰谷结构与积分制提价回收成本——"低价换规模"与"合理定价换可持续"两种成本工程路线并存。
