# Gemini 3.8 Flash TTS 与 Flash-Lite TTS 发布(Introducing Gemini 3.8 text-to-speech)

- **原文链接**: [Introducing Gemini 3.8 text-to-speech](https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-8-text-to-speech/)
- **作者**: Gemini 模型团队
- **发布日期**: 2026-09-24
- **检索日期**: 2026-09-29
- **标签**: #TTS #语音合成 #Gemini #多语言 #声音克隆

## 核心观点

Google 发布 Gemini 3.8 Flash TTS 与 Flash-Lite TTS,把 TTS 从"朗读"推进到"可导演、可选角":单行文本即可施加舞台指示精细控制语气;单一脚本能生成双说话人对话;Flash TTS 仅凭文字描述就能合成符合描述的新声音,或用 30 秒样本完成声音克隆。

两款模型覆盖 100+ 语言,Flash-Lite 面向高吞吐量产并提供音调语速控制。与 3.8 Live(实时输入侧)、Live Avatar(形象层)拼合后,Google 凑齐实时语音全栈——本篇补上的是输出侧,竞争定位直接对标 ElevenLabs。

## 关键发现 / 关键技术

### 1. 舞台指示与双说话人
- 单行文本施加舞台指示,精细控制语气与情绪走向
- 单一脚本生成双说话人对话:播客、访谈式内容一次成型

### 2. 声音的"描述生成"与克隆
- Flash TTS 仅凭文字描述即可合成符合描述的新声音——不提供样本也能"选角"
- 30 秒音频样本即可克隆既有声音
- 描述生成与样本克隆两种入口,覆盖"无样本选角"与"复刻既有声线"两类需求
- 声音资产从"预置列表"变为"可参数化生成"的对象

### 3. Flash-Lite:高吞吐量产
- 定位规模化内容生产的高吞吐场景
- 提供音调、语速控制,适配品牌一致性要求
- 与 Flash TTS 形成"质量档 / 量产档"双梯队

### 4. 在全栈中的位置
- 3.8 Live(2026-09-15)负责实时语音对话,Live Avatar(2026-09-24)负责可视化形象
- 3.8 TTS 补齐输出侧:非实时、高质量、可批量,与 Live 同月拼出语音全栈
- 竞争定位直接对标 ElevenLabs 等专业语音厂商

## 实践意义

"凭描述生成声音"改变语音产品的资产模式:过去声音是稀缺的授权资源,现在成为提示词可生成的对象;双说话人单脚本则把播客、有声剧的制作成本压缩到一次 API 调用。内容平台与客服系统应重新评估自建 TTS 管线的必要性。

架构上,Google 的语音版图已经分层:实时对话(Live)、形象(Avatar)、离线输出(TTS)、转写输入(transcribe)。开发者可按延迟与吞吐需求在各层单独选型,也可全栈采用换取一致性;与 ElevenLabs 的取舍点在于多模态协同 vs 单点音质。

语音全栈拼齐后,观察点转向整合体验:Live 的实时通道、Avatar 的形象层与 TTS 的离线产能能否共享声音资产与控制语法,将决定全栈采用的实际收益。

## 跨厂商对比

- 与 [Gemini 3.1 Flash TTS](gemini-3-1-flash-tts.md) 对比:前代以"音频标签"实现导演级控制(70+ 语言、Artificial Analysis TTS Elo 1,211),3.8 代把控制面升级为舞台指示 + 双说话人,新增描述生成声音与 30 秒克隆,语言扩至 100+——从"可导演"进化到"可选角"。
- 与 [Gemini 3.5 Transcribe](gemini-3-5-transcribe.md) 互补:transcribe 解决语音→文本的输入侧,3.8 TTS 解决文本→语音的输出侧,与 Live 系实时通道合看即是完整语音管线。
- 与 [OpenAI API 语音智能新模型](../../openai/research/advancing-voice-intelligence-with-new-models-in-the-api.md) 对比:OpenAI 将语音智能并入 API 模型家族统一供给,Google 以独立 TTS 产品线 + 描述驱动的声音生成直面 ElevenLabs——一体式 vs 专业化的两条路线。
- 与 [Gemini 3.8 Live 与 Live Extended Thinking](gemini-3-8-live-extended-thinking.md) 互补:Live 系管实时双向语音通道,3.8 TTS 管离线高质量产出,同月发布构成语音全栈的两翼。

## 资源

- 官方文章:https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-8-text-to-speech/
- 试用:https://aistudio.google.com/
- 前代模型卡:https://deepmind.google/models/model-cards/gemini-3-1-flash-audio/
- 形象层发布:https://deepmind.google/blog/introducing-gemini-38-live-with-live-avatar/
