# Gemini 3.1 Flash TTS：下一代富有表现力的 AI 语音（Gemini 3.1 Flash TTS: the next generation of expressive AI speech）

- **原文链接**: [Gemini 3.1 Flash TTS: the next generation of expressive AI speech](https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-1-flash-tts/)
- **作者**: Vilobh Meshram, Max Gubin（代表 Gemini 团队）
- **发布日期**: 2026-04-15
- **检索日期**: 2026-08-01
- **标签**: #TTS #语音合成 #Gemini #多语言 #Google

## 核心观点

Gemini 3.1 Flash TTS 是 Google 迄今最自然、最具表现力的文本转语音模型，核心创新是"音频标签"（audio tags）——把自然语言指令直接嵌入文本，细粒度控制语音的风格、节奏与演绎方式，让 TTS 从"朗读工具"变为"可导演的表演"。模型支持 70+ 语言与原生多说话人对话，全部音频内置 SynthID 水印。

发布当日即向开发者（Gemini API + AI Studio 预览）、企业（Vertex AI 预览）和 Workspace 用户（Google Vids）三路开放。

## 关键发现 / 关键技术

### 1. 基准表现
- Artificial Analysis TTS 排行榜 Elo 达 1,211，基于数千次盲测人类偏好的谷歌最自然语音模型
- 进入该机构"质量-价格最优象限"，主打高质量与低成本兼得

### 2. 音频标签与"导演椅"开发体验
- 音频标签：在文本中嵌入自然语言命令控制风格、语速、重音与情绪
- AI Studio 提供可配置控制：场景导演（定义环境与对话指令保持角色一致）、说话人级 Audio Profiles + Director's Notes（切换语速/语气/口音）、行内标签支持句中变换表达
- 调好的参数可一键导出为 Gemini API 代码，保证跨项目声音一致

### 3. 全球化与安全
- 70+ 语言的高保真语音与口音控制，覆盖主要市场
- 原生多说话人生成：单段文本直接产出播客、访谈、戏剧场景等多角色对话
- SynthID 不可感知水印内嵌音频，可可靠识别 AI 生成内容

## 实践意义

音频标签把 TTS 的控制接口从 SSML 式的技术标记升级为自然语言导演指令，显著降低语音应用的调优门槛；"导出即 API 代码"则打通了从原型到生产的路径。配合早期测试者（StyleUAI、Artlist、Sierra、HeyGen 等）的反馈，可预见语音 agent 与内容创作工具的语音质量竞争将快速升温。

## 跨厂商对比

- 与 [Gemini Omni](gemini-omni.md) 互补：Omni 主打"从任意模态生成任意模态"的视频起点，3.1 Flash TTS 则把音频生成的可控性推向导演级粒度，共同构成 Google 多模态生成矩阵
- 与 [GPT-5.6](../../openai/research/introducing-gpt-5-6.md) 对比：OpenAI 将语音实时能力内置于旗舰模型的 agentic 体验，Google 则以独立、低成本、可控的 TTS 模型服务开发者规模化语音应用

## 资源

- 试用：[Google AI Studio 语音生成](http://aistudio.google.com/generate-speech)
- 模型卡：[Gemini 3.1 Flash Audio model card](https://deepmind.google/models/model-cards/gemini-3-1-flash-audio/)
