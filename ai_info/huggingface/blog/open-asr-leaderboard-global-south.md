# Open ASR Leaderboard 首次加入全球南方语言（The Open ASR Leaderboard Adds Its First Global South Language）

- **原文链接**: [The Open ASR Leaderboard Adds Its First Global South Language](https://huggingface.co/blog/open-asr-leaderboard-global-south)
- **作者**: Eric Bezzam、Shobhit Banga、Manas Dhir、Bhaskar Singh 等（Voice Arena 与 Hugging Face 合作）
- **发布日期**: 2026-08-28
- **检索日期**: 2026-09-09
- **标签**: #ASR #评测 #公平性 #印地语 #GlobalSouth #语音识别

## 核心观点

Voice Arena 与 Hugging Face 合作，为 Open ASR Leaderboard 引入两个新评测集：Monsoon en-IN（印度英语）与 Monsoon hi-IN（印地语）。印地语拥有超过 5 亿使用者，是该榜多语言页签上的首个印度语言——此前它只覆盖欧洲语言。

动机是既有研究反复证实的事实：ASR 错误率在人群间分布不均（PNAS 研究发现商业系统对黑人说话人的错误率约为白人说话人的两倍，性别、年龄、口音同样带来差异），而传统测试集只记录"说了什么"，几乎不记录"是谁说的"。Monsoon 沿九个轴系统性变化，让"总体 WER 正确、对特定人群错误"的失效模式显形。

每个评测集都含公开 split（可自评）与私有 split（限制针对性优化），四个 split 说话人不相交，共 4,888 名说话人、每名记录 12 项说话人属性。

## 关键发现 / 关键技术

### 1. 九轴变化的测试集设计
一个测试集只能暴露它所变化的失效模式。Monsoon 沿九个轴设计：地理、年龄、性别、词汇、设备、声学环境、语体、语速、以及"同一音频存在多个合法转写"。采集方法与之对应：跨数百个地区招募而非在少数地点长录音；贡献者用自己的手机与网络、室内外录音；提示词用日常话题引导观点、叙述与回忆（命名实体、数字、未排练措奏自然出现）；年龄与性别逐说话人记录并验证。

### 2. 公开 + 私有双 split，说话人不相交
- 两个语言 × 公开/私有 = 四个 split，共 4,888 名说话人，每人 12 项属性
- 公开 split 供社区自评，私有 split 扣留以限制 benchmark-specific 优化——延续该榜此前引入 held-out 私有集、量化 benchmark-fitting、修补归一化器的一贯路线

### 3. 印地语正字法变体
印地语存在同一音频对应多种合法书面形式的问题，文章用专门小节讨论正字法变体：正确变体不应被评测惩罚（与九轴中"多合法转写"一轴呼应）。

## 实践意义

对在多语言市场部署 ASR 的团队：聚合 WER 会掩盖人群级失效，评测集应显式沿说话人维度分层；公开 + 私有双 split 的做法可直接借鉴，防止自建评测被针对性优化。对基准维护者：记录"谁在说话"的元数据与记录"说了什么"同等重要。

## 跨厂商对比

- 与 [Real World VoiceEQ](real-world-voiceeq.md) 互补：同属 HF 语音评测可信度建设——VoiceEQ 引入 held-out 真实世界私有集，Monsoon 把"谁在说话"显式纳入评测维度，两者叠加让单一 WER 更难被操纵
- 与 [How two settings tripled our ARC-AGI 3 scores](../../openai/research/how-two-settings-tripled-our-arc-agi-3-scores.md) 对比：OpenAI 展示 harness 设置如何放大基准分数，本文（配合同日发布的 benchmark-fitting 分析）展示模型如何利用数据集成员线索，同为"基准分数 ≠ 真实能力"的跨模态证据

## 资源

- 论文：N/A
- 代码：N/A
- Demo：[Open ASR Leaderboard](https://huggingface.co/spaces/hf-audio/open_asr_leaderboard)；数据集 [Monsoon en-IN](https://huggingface.co/datasets/VoiceArena/MonsoonASR-Open-ASR-leaderboard-en-IN)、[Monsoon hi-IN](https://huggingface.co/datasets/VoiceArena/MonsoonASR-Open-ASR-leaderboard-hi-IN)
