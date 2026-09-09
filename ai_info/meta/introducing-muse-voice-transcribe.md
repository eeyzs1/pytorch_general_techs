# Muse Voice Transcribe：MSL 首个实时语音感知模型（Introducing Muse Voice Transcribe）

- **原文链接**: [Introducing Muse Voice Transcribe](https://research.meta.ai/blog/introducing-muse-voice-transcribe)
- **作者**: Meta Superintelligence Labs / Meta
- **发布日期**: 2026-09-01
- **检索日期**: 2026-09-09
- 注：初稿基于二手交叉验证信源（官方站点检索时不可达）；2026-09-09 经 VPN 复核，research.meta.ai 官方列表已确认本文条目（2026-09-01，标题一致），官方 URL 有效
- **标签**: #ASR #流式转写 #说话人分离 #语码转换 #MuseSpark

## 核心观点

Muse Voice Transcribe 是 Meta Superintelligence Labs（MSL）发布的首个实时音频感知模型，属 Muse Spark 多模态推理家族的自回归多模态成员。它把流式 ASR、20+ 说话人分离（diarization）与端点检测（endpointing）整合进单一模型，在 Artificial Analysis 流式转写评测中以 3.1% 词错率位居第一，说话人识别错误率同样低于对比模型。

模型以 70+ 语言训练，其中 25 种语言深度验证，原生支持句间与句内语码转换（code-switching），并借助上下文偏置（contextual bias）提升准确率；可处理 1 小时以上录音与 20+ 人对话，无需事后说话人标注。2026-09-02 起经 Meta Model API、Meta AI for Mac 与 Muse Code 提供，定价 $0.18/小时。

## 关键发现 / 关键技术

### 1. 单一模型完成"转写 + 分离 + 端点检测"
- 流式 ASR 实时输出文字；说话人分离覆盖 20+ 人对话；端点检测（utterance end detection）判定发言结束并触发"最终转写"
- Artificial Analysis 流式转写评测第一：最终转写词错率 3.1%；说话人识别错误率也低于对比模型（据 GIGAZINE 转述官方图表）

### 2. 多语言与语码转换
- 训练覆盖 70+ 语言，其中 25 种经过深度验证：英语、日语、韩语、中文（普通话）、印地语、孟加拉语、泰米尔语、泰卢固语、阿拉伯语、越南语、泰语、印尼语、马来语、他加禄语等——覆盖面明显偏向多语种与全球南方市场
- 原生支持句间与句内 code-switching（双语者常见的话语切换），并以 contextual bias 利用上下文提升识别准确率

### 3. 长音频、定价与可用性
- 支持 1 小时以上录音与 20+ 人对话，免除录音后处理（说话人标注、电平调整）
- 定价 $0.18/小时（约合 $3/1000 分钟），Artificial Analysis 称其为对比模型中最便宜的选项
- 2026-09-02 起经 Meta Model API、Meta AI for Mac、Muse Code 提供

## 实践意义

对语音 Agent 而言，低延迟流式转写加端点检测是"可打断、可追问"语音交互的前提；Voice Transcribe 把这一能力与说话人分离打包为 API，配合 $0.18/小时的定价，进一步压低会议纪要、客服质检、字幕生产等转写密集型工作流的边际成本。多语言与句内语码转换对中文-英文夹杂等真实双语场景尤具工程价值，值得在自有语音管线中与现有 ASR 方案做同槽位对比测试。

## 跨厂商对比

- 与 [Meta AI 不止会思考，更会行动](meta-ai-muse-spark-doesnt-just-think-it-acts.md) 对比：同属 MSL 的产品节奏——前者让 Muse Spark 在 Meta AI 中"行动"（定时任务、邮件日历连接、深度研究），本文补上"倾听"一侧，共同拼出个人 Agent"听→想→做"链路的输入端
- 与 [Gemini 3.1 Flash TTS](../google/deepmind/gemini-3-1-flash-tts.md) 互补：Google 该篇主攻语音合成（输出侧）的表现力，Voice Transcribe 主攻语音识别（输入侧）的准确与时延，二者构成全双工语音交互的两半
- 与 [度量语音识别中的基准优化](../huggingface/blog/asr-benchmark-optimization.md) 互补：HF/Hume 揭示 ASR 领域的 benchmaxxing（基准过拟合）风险与更可靠的评估方法，为解读 Voice Transcribe 的榜首成绩提供方法论校准

## 资源

- 官方公告：https://research.meta.ai/blog/introducing-muse-voice-transcribe
- 媒体报道：https://gigazine.net/gsc_news/en/20260902-meta-muse-voice-transcribe
