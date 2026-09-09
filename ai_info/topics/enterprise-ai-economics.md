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
- [GLM Coding Plan "Flash × ZCode" 夜间畅用](../glm/blog/glm-flash-zcode-night-free.md)：峰谷计费的强化版——夜间时段经官方工具 ZCode 额度归零、经第三方 Agent 额度翻倍，"错峰填谷 + 自有渠道导流"双目标叠加；与 DeepSeek 低峰半价共同标志需求侧调度成为国产厂商的常规运营工具。
- [智谱 2026 半年度业绩会](../glm/blog/zhipu-h1-2026-earnings-glm-6.md)：国产大模型罕见的经营透明度——上半年营收 9.54 亿（+399.7%）、API 占 86.5%、亏损收窄；单位 token 推理成本较年初降 80%（10 万级国产芯片规模化推理），"降本曲线 + 后训练迭代"支撑起 1/20 折扣价的低价多模态模型。
- [The Future is for Everyone](../meta/the-future-is-for-everyone.md)：开源 AI 的经济学主张——Zuckerberg 以 6510 字论述"多超智能 + 开源防集中"，宣布 10 亿美元开放模型基金；"蒸馏开源"（旗舰闭源、衍生开源）成为 Meta 的算力投资与生态扩张双重叙事，与 OpenAI"充裕智能"的集中式算力投资形成路线对立。
- [Quantization-Aware Healing](../huggingface/blog/quantization-aware-healing.md)：压缩即增值的成本工程——用压缩前原始全精度模型做蒸馏 teacher，4-bit GPT-OSS 60B 在 9 基准中 7 个反超自家 bf16，比 QAT 快 7 倍达峰且不漂移、权重内存省约 4 倍；量化从"性能折损的省钱手段"变为"可能涨点的优化手段"，直接改写推理成本模型。
- [Up to 3.2x Faster Inference with LFM2.5-DSpark](../huggingface/blog/lfm25-dspark.md)：端侧与云端的双重降本——~300M 投机解码 draft 模型让 8B MoE 在 H100 提速 3.18×、2.6B 在 M4 Max 端侧达 ~140 tok/s 且 function-calling 延迟降 57%；贪心输出构造性恒等保证"加速不换答案"，成本工程与质量工程解耦。
- [Reducing cost and improving performance with Claude Platform](../anthropic/engineering/reducing-cost-and-improving-performance-with-claude-platform.md)：官方成本优化三杠杆——prompt cache 命中率（字节级前缀 / 1 小时 TTL / 预热）、前沿迁移清反模式、effort 校准（低 effort 以 1/3 成本匹配高 effort）；prompt-audit 实测迁移成本 -14.6% 且准确率 +5.3%，cost-optimize 四基准降 52%–73%——"每成果成本"从理念变成平台自带工具。
- [Bain & Company joins the Claude Partner Network](../anthropic/engineering/bain-company-joins-claude-partner-network.md)：咨询巨头进入 AI 分发链——19,000 员工全员部署 Claude，试点数周 7,000+ 活跃、客户复杂遗留代码库项目 30–50% 生产力提升；与 OpenAI Partner Network（30 万认证顾问目标）形成"认证渠道 vs Premier 咨询伙伴"两种规模化路径。
- [How Anthropic employees use Claude Tag](../anthropic/engineering/how-anthropic-employees-use-claude-tag.md)：内部效率量化的样本——15+ 条 Slack 讨论串 45 分钟变评审级文档、~120 条原始发现压成周报（人工估计需一周）、营销法务审查从 1 天+ 降至 30 分钟/件；"Anthropic 自己怎么用"成为企业买家最可信的效率证据。
- [The full stack behind abundant intelligence](../openai/research/the-full-stack-behind-abundant-intelligence.md)：CFO 视角的全栈复利——芯片/算力/模型/产品四层进步互相放大，GPT-5.6 Sol 创 Artificial Analysis 新高且输出 token 少 54%；Jevons 悖论（效率提升扩大总需求）成为"降价不降收入"的经济学解释。
- [Jalapeño's first results](../openai/research/jalapeno-first-results.md)：自研芯片的实测兑现——三公开模型每瓦峰值吞吐 1.5–1.9×、端到端延迟低 1.7–3.6×（700W vs GB200/GB300），设计到流片仅 9 个月且 AI 生成的 attention/MoE 块比人写快 1.5–1.8×；自研推理芯片从战略叙事进入量产倒计时。
- [A milestone in expanding access to AI](../openai/research/expanding-access-to-ai-with-chatgpt-ads.md)：广告作为免费 AI 的经济引擎——上线不到 200 天年化 run rate 达 10 亿美元、40+ 国家、数万广告主，支撑 10 亿+ 周活免费层；电商案例 28 天 3× ROAS 且 >80% 流量为新客户。
- [The Work Now Within Reach](../openai/research/the-work-now-within-reach.md)：更强更便宜 AI 的扩张论——10 亿周活 + 250 万企业的双通道复利，GPT-5.6 Sol 使服务成本 -20%、token 效率 +15%；客户证据 Boston Children's 40+ 诊断、Circles 65% 自主解决。"能力增强 × 成本下降"同时发生时，可及工作范围本身在扩大。

## 关键结论

- 衡量 AI 价值的基本经济问题：AI 完成工作的价值增长是否快于其生产成本——token 只是中间产物，"成功成果的成本"才是正确度量。
- 最强模型一次做对，往往比便宜模型反复重试加人工修正更经济——按"成果需要多少智能"在同一工作流内分档混用模型成为标准采购逻辑。
- 企业 AI 竞争的下半场从模型能力转向部署能力——FDE 模式（OpenAI Deployment Company）与产品化护栏（Presence）是两种互补的商业化路径。
- 任务跨界数据（43.5%）表明 AI 对劳动力市场的重构先于职位变化发生——使用数据是比就业统计更早的领先指标。
- 前沿智能进入价格竞争阶段：OpenAI 三档降价、DeepSeek 峰谷计费、Claude Opus 5"半价逼近前沿"——"每美元有效工作"取代 benchmark 分数成为厂商叙事核心。
- 价格竞争出现分化：OpenAI 靠效率提升降价，DeepSeek/GLM 靠峰谷结构与积分制提价回收成本——"低价换规模"与"合理定价换可持续"两种成本工程路线并存。
