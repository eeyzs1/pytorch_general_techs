# Gemini 3.8 Flash 与 3.8 Flash Cyber 发布（Introducing Gemini 3.8 Flash and 3.8 Flash Cyber）

- **原文链接**: [Introducing Gemini 3.8 Flash and 3.8 Flash Cyber](https://blog.google/innovation-and-ai/models-and-research/gemini-models/3-8-flash-and-3-8-flash-cyber/)
- **作者**: Google DeepMind（官方博客未署名）
- **发布日期**: 2026-09-02
- **检索日期**: 2026-09-09
  注：官方页面抓取受限，本文基于检索核验的日期与公开报道整理（基准与定价数据经 FoneArena/Apidog 转述核验）
- **标签**: #Gemini #Flash #网络安全 #智能体 #代码

## 核心观点

Google 发布下一代 Flash 双模型：Gemini 3.8 Flash 面向软件工程、智能体任务与专业领域多步推理；Gemini 3.8 Flash Cyber 聚焦防御性网络安全（自主漏洞发现与自动补丁），仅通过 Fairwind 计划向受信方开放。两者共享同一基础智能与长时程智能体循环设计，是六周内 Google 的第三次 Flash 发布。

Flash 路线的竞争逻辑依旧是"以小搏大"：3.8 Flash 在长视野软件工程基准 DeepSWE v1.1 上以远低于大型前沿模型的成本胜出多数对手；Flash Cyber 在 CyberGym 漏洞发现上超越 3.5 Flash Cyber 与显著更大的前沿模型，补丁基准 CWE-Bench 上以显著更低成本逼近最强前沿模型（47.2% vs 47.8% pass@1）。

## 关键发现 / 关键技术

### 1. Gemini 3.8 Flash：推理与领域基准
- HLE-Verified（跨 STEM/人文/专业领域的多步推理）54.9%
- Vals Finance Agent V2 与 Harvey 法律 Agent 基准均超 Gemini 3.7 Flash 与其他前沿模型
- 复杂任务会执行更多推理步与迭代工具调用、推高 token 用量；可用更低 effort 档位控制开销，3.7 Flash 继续服务效率优先负载

### 2. Gemini 3.8 Flash Cyber：漏洞发现与自动补丁
- CyberGym（行业标准的漏洞发现基准）：前沿级表现，超 3.5 Flash Cyber 与更大模型
- Google 内部真实世界基准（覆盖 20 种编程语言）：成功率 >70%
- CWE-Bench（Collinear 运行的外部补丁基准）：47.2% pass@1，对比领先前沿模型的 47.8%，成本显著更低
- 实战结果：Chrome 安全团队正确补丁数达最佳商业模型（体积大得多）的 2.6 倍；Wiz 内部渗透测试基准召回率高 7.5–9.7 个百分点、成本低 2.3–5.2 倍；Google Cloud 漏洞研究在 2 小时内发现一个关键基础漏洞（常规流程需数月）

### 3. 安全、定价与可用性
- 安全：包含 CBRN（化学/生物/放射/核）与网络攻击滥用防护；Cyber 版采用更宽松的网络安全缓解策略以覆盖防御场景；经 Gray Swan 度量的提示注入鲁棒性提升
- 定价：2026-12-31 前 $0.75/$3.75 每百万输入/输出 token，2027-01-01 起为 $1.50/$7.50
- 可用性：Google Antigravity、Gemini API（AI Studio/Android Studio）、Stitch、Gemini Enterprise；消费者侧经 Gemini app（AI Pro/Ultra）、Search AI Mode 与 Sheets；Flash Cyber 经 Fairwind 计划提供

## 实践意义

对 Agent 工程团队，3.8 Flash 延续"更努力工作"路线：更高 effort 换更高任务完成率，token 预算需按档位建模；年底前的半价窗口适合做迁移评估。对安全团队，Flash Cyber 的"优先修复而非利用"取向与 Fairwind 准入绑定，意味着外部无法独立复现其数字——采用决策需信任 Google 及其具名伙伴的实测报告。

## 跨厂商对比

- 与 [发布 Gemini 3.6 Flash、3.5 Flash-Lite 与 3.5 Flash Cyber](gemini-3-6-flash-3-5-flash-lite-3-5-flash-cyber.md) 对比：3.6 代的卖点是降价与省输出 token（消费侧优化），3.8 代转向长循环硬指标与金融/法律/安全等垂直基准，两代合看可见 Flash 从成本线走向能力线。
- 与 [发布 Gemini 3.5 Flash Cyber：轻量级网络安全模型](introducing-gemini-3-5-flash-cyber.md) 互补：3.5 Flash Cyber 确立"防御优先的受限安全模型"形态，3.8 Flash Cyber 把准入制度化为 Fairwind 计划并公布伙伴实测，是同一策略的成熟化。

## 资源

- 官方文章：https://blog.google/innovation-and-ai/models-and-research/gemini-models/3-8-flash-and-3-8-flash-cyber/
- 产品/API：https://deepmind.google/models/model-cards/gemini-3-8-flash/
