# Open TTS Leaderboard：多语言语音合成与声音克隆的可扩展评估（Open TTS Leaderboard: Scalable Evaluation for Multilingual Text-to-Speech and Voice Cloning）

- **原文链接**: [Open TTS Leaderboard: Scalable Evaluation for Multilingual Text-to-Speech and Voice Cloning](https://huggingface.co/blog/open-tts-leaderboard)
- **作者**: Eric Bezzam、Steven（Steveeeeeeen）、Eustache Le Bihan、mrfakename（Hugging Face 音频团队）
- **发布日期**: 2026-09-30
- **检索日期**: 2026-10-16
- **标签**: #TTS #评估基准 #语音合成 #开源模型 #排行榜

## 核心观点

Hub 上 TTS 模型已超 8,000 个，但评估仍碎片化：以人类投票为核心的竞技场（TTS Arena v2、Artificial Analysis、Voice Arena）无法跟上发布节奏——攒票要数周，且开源模型严重缺席（Artificial Analysis 92 个模型中仅 16 个开放权重，因为 API 模型接个 key 就能参赛，开源模型要主办方自己托管）。HF 音频团队推出 Open TTS Leaderboard，用客观指标把单个模型评估从数周压缩到数小时。

三大指标轴：可懂度（用 Open ASR 榜第一的 Qwen3-ASR-1.7B 转写生成音频算 WER/CER）、速度（H200 上批量推理 RTFx 与流式 batch-1 的 TTFA，含 CPU）、说话人相似度（WavLM 嵌入余弦相似度 SIM）。明确声明不替代人类偏好——自然度与表现力仍需人耳，但客观指标可以为竞技场筛选入围模型。

## 关键发现 / 关键技术

### 1. 客观指标设计

- 可懂度：英文以 Seed TTS Eval + CV3 Eval（零样本）宏平均 WER 排名；中日韩字符语言报 CER，多语言平均为跨语言宏平均。
- 速度：批量离线 RTFx（H200）；流式 TTFA 取 50 条 CV3-Eval 英文提示、batch 1、丢弃前 3 次预热后的中位数，另设 CPU 榜。
- 声音克隆模式：额外报 SIM 列与 SIM×速度×参数量的 Pareto 图。

### 2. 首批格局

- 英文 WER 领先：Kokoro-82M、Supertonic-3、fishaudio/s2-pro；多语言领先：k2-fsa/OmniVoice、s2-pro、FunAudioLLM/Fun-CosyVoice3-0.5B。
- 有趣反差：higgs-tts-3-4b 与 openbmb/VoxCPM2 在提供参考音频（克隆模式）时 WER 反而更好。
- 流式场景 kyutai/pocket-tts 在 GPU 与 CPU 上都表现出色——对语音 Agent 的首包延迟关键。

### 3. Listen 页与社区化

- "Listen"页可直接对比收听各模型在同一提示上的输出并投票（HF 账号登录防机器人），填补现有 TTS 榜"无处试听"的空白。
- 评估脚本将像 Open ASR Leaderboard 一样开源，接受 GitHub Issue/PR。

## 实践意义

选型 TTS 不再只能在竞技场 Elo 与厂商营销之间摇摆：延迟敏感的语音 Agent 看 TTFA 榜，多语言产品看宏平均 WER，克隆场景看 SIM。对开源 TTS 作者，这是低成本进入公共评估的通道——托管成本由榜单承担，入围竞技场也有了数据依据。

## 跨厂商对比

- 与 [Open ASR 榜首纳全球南方语言](open-asr-leaderboard-global-south.md) 对比：同属 HF Open 系榜单方法论——固定清单、公开脚本、客观指标，从 ASR 复制到 TTS；但 TTS 版新增流式 TTFA 与克隆 SIM 两个产品化维度。
- 与 [Real World VoiceEQ](real-world-voiceeq.md) 互补：VoiceEQ 用百万级人工评分量"人类质量"（副语言、情绪），Open TTS Leaderboard 用客观指标量"工程可用性"，两者共同界定语音生成评估的两极。
- 与 [Gemini 3.1 Flash TTS](../../google/deepmind/gemini-3-1-flash-tts.md) 对比：Google 走"模型内建评估维度"路线，HF 走"第三方可复现榜单"路线，商业 TTS 的多语言覆盖与开源模型的可获得性正在被公开量化对比。

## 资源

- 论文：无
- 代码：[Open TTS Leaderboard Space（评估脚本将开源）](https://huggingface.co/spaces/hf-audio/open_tts_leaderboard)
- Demo：[Listen 页可直接试听与投票](https://huggingface.co/spaces/hf-audio/open_tts_leaderboard)
