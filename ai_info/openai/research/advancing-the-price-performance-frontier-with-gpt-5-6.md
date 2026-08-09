# GPT-5.6 推进价格性能前沿（Advancing the price-performance frontier with GPT-5.6）

- **原文链接**: [Advancing the price-performance frontier with GPT‑5.6](https://openai.com/index/advancing-the-price-performance-frontier-with-gpt-5-6/)
- **作者**: OpenAI
- **发布日期**: 2026-07-30
- **检索日期**: 2026-08-01
- **标签**: #GPT-5.6 #定价 #Luna #Terra #FastMode #成本效率

## 核心观点

OpenAI 把 GPT-5.6 效率工程的收益直接让利给客户：最快最便宜的 Luna 降价 80%（输入 $0.20 / 输出 $1.20 每百万 token），均衡款 Terra 降价 20%（$2 / $12），Sol 价格不变但推出 Fast mode——2 倍价格换最高 2.5 倍速度，智能不变，取代 Priority Processing。ChatGPT Work 与 Codex 订阅价格不变，但 Luna/Terra 用量消耗的额度同步减少。

文章给出的定位逻辑：Luna 以约 6% 的单任务成本达到一年前前沿级模型的性能、近 9 倍速度；在 Agents' Last Exam 专业工作评测上，Luna 以估算低近 99% 的单任务成本超越 Fable 5。企业应按"成果需要多少智能"在同一工作流内分档混用模型（如 Sol 定计划、Luna 跑实现）。

## 关键发现 / 关键技术

### 1. 新定价与 Fast mode
- Luna $0.20/$1.20、Terra $2/$12（每百万输入/输出 token），7 月 30 日起生效，AWS 同日跟进
- Fast mode 兼容旧 priority 标记，与 Codex 中 /fast 对齐；智能水平与 Standard 完全一致

### 2. 效率的来源（与工程文呼应）
- 模型走更直接的任务路径、路由让硬件保持满载、生产软件 token 生成更高效、上下文管理避免重复劳动
- GPT-5.6 Sol 自主重写生产内核使端到端服务成本降 20%、投机解码实验提升 token 生成效率超 15%——效率收益形成"模型改进自身服务"的紧反馈环

### 3. 客户验证
- Replit 称 Luna 接近"便宜到无法计量的智能"；Notion 评估 Terra 质量与 GPT-5.5 相当而单任务成本减半、耗时少 60%
- Blitzy：Luna 支撑 2.2 倍上下文、8.5 倍更少输出 token，成本较 GPT-5.4 mini 低 87%；Dust：同任务 40% 更快 40% 更便宜；Cognition 把 Luna 集成进 Devin Fusion 做"大模型的配对程序员"

## 实践意义

Luna 的定价（$0.20/$1.20）把"前沿级一年前智能"拉进大宗高并发场景的经济区间，直接冲击 DeepSeek、GLM 等性价比模型的腹地——OpenAI 开始在价格曲线上主动进攻。对开发者：(1) 重新核算高并发场景（文档分析、交互分类、后台自动化）的模型选型，Luna 可能改变"自建小模型 vs API"的账本；(2) Sol+Luna 的分档编排（规划用贵模型、执行用便宜模型）应成为默认架构；(3) Fast mode 为延迟敏感场景提供了不换模型的提速选项。

## 跨厂商对比

- 与 [GPT-5.6 效率工程](gpt-5-6-frontier-intelligence-efficiency.md) 互补：效率如何产生 → 效率如何定价，两日连发构成完整叙事
- 与 [GPT-5.6：前沿智能，随雄心扩展](introducing-gpt-5-6.md) 互补：发布时讲能力分档，本文讲分档的价格落地
- 与 [Anthropic Claude Opus 5](../../anthropic/research/claude-opus-5.md) 对比：OpenAI 以三档定价正面竞争每美元智能，Anthropic 仍以单旗舰 + 可靠性叙事为主，定价策略分化明显

## 资源

- 原文：[Advancing the price-performance frontier with GPT‑5.6](https://openai.com/index/advancing-the-price-performance-frontier-with-gpt-5-6/)
- 定价：[API Pricing](https://openai.com/business/pricing/#api)
