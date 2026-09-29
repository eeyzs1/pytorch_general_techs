# Gemini 3.8 Live 与 Live Extended Thinking 发布(Introducing Gemini 3.8 Live and 3.8 Live Extended Thinking)

- **原文链接**: [Introducing Gemini 3.8 Live and 3.8 Live Extended Thinking](https://deepmind.google/blog/introducing-gemini-3-8-live-and-3-8-live-extended-thinking/)
- **作者**: Gemini 团队
- **发布日期**: 2026-09-15
- **检索日期**: 2026-09-29
- **标签**: #Gemini #Live #语音智能 #实时交互 #多语言

## 核心观点

Google 发布两款语音原生模型:Gemini 3.8 Live 与 3.8 Live Extended Thinking。前者主打近实时语音对话,后者在 Live 底座上叠加扩展思考。两者均支持视觉输入、后台异步工具调用(对话不中断)与对话中途切换语言,覆盖 97 种语言。

Extended Thinking 在 Artificial Analysis Speech-to-Speech Quality Index 以 82.6 登顶,tau-Voice 68.6%、Big Bench Audio 97.7%;定价音频输入 $0.005/分钟、输出 $0.018/分钟(约 $1.38/小时),不足 GPT-Live-1 同档 $3+ 的一半。第三方评测认为其音质自然度仍逊于 OpenAI 全双工——价格优势与体验差距并存。

## 关键发现 / 关键技术

### 1. 语音原生设计:工具调用不打断对话
- 近实时语音对话,同时接收视觉输入(摄像头/屏幕画面)
- 后台异步工具调用:发起调用后对话继续,结果返回后自然衔接,消除静默等待
- 对话中途可切换语言,覆盖 97 种语言

### 2. Extended Thinking 基准成绩
- Artificial Analysis Speech-to-Speech Quality Index:82.6,排名第一
- tau-Voice:68.6%;Big Bench Audio:97.7%
- 基础版 3.8 Live 在 Speech Agent Arena 位列第二

### 3. 定价:小时单价不足对手一半
- 音频输入 $0.005/分钟、音频输出 $0.018/分钟,合计约 $1.38/小时
- 对比 OpenAI GPT-Live-1 同档 $3+/小时:不足一半
- 第三方评测:音质自然度仍逊于 OpenAI 全双工,价格与体验的取舍明确

### 4. 渠道与可用性
- 开发者:Gemini API、AI Studio
- 企业:Gemini Enterprise 私人预览
- 消费级入口:Search Live、Workspace

## 实践意义

对语音智能体团队,异步工具调用 + 对话不中断是本代最重要的工程原语:它把"调用工具"从对话的停顿点变成对话的背景任务,直接决定客服、助理类产品的体验下限。按分钟计费(而非按 token)也改变了成本建模方式——语音智能体的边际成本第一次可以用小时级单价直观预算。

选型上,价格与体验出现明确分层:预算敏感、可接受自然度"略逊一筹"时,3.8 Live 系的价格杠杆显著;追求顶级全双工自然度仍需评估 OpenAI 方案。企业落地建议先用 Gemini Enterprise 预览验证工具调用衔接的真实延迟,再决定迁移范围。

## 跨厂商对比

- 与 [GPT Live 的持续语音交互](../../openai/research/continuous-voice-interaction-with-gpt-live.md) 对比:GPT-Live 确立全双工自然对话标杆,3.8 Live 以不到一半的小时价($1.38 vs $3+)换市场——基准登顶但第三方音质评价仍落后,两家在"自然度 vs 价格"上各执一端。
- 与 [OpenAI API 语音智能新模型](../../openai/research/advancing-voice-intelligence-with-new-models-in-the-api.md) 对比:OpenAI 把语音能力并入 API 模型家族统一演进,Google 保持 Live 独立产品线高频迭代,九月内连发 3.8 Live、Live Avatar 与 3.8 TTS。
- 与 [Gemini 3.8 Live with Live Avatar](gemini-3-8-live-avatar.md) 互补:3.8 Live 是语音与工具调用底座,Live Avatar 在其上叠加可视化形象层,两篇合读可见 Google 实时语音栈的纵向分层。
- 与 [Gemini 3.8 Flash TTS 与 Flash-Lite TTS](gemini-3-8-tts.md) 互补:Live 系管实时双向通道,3.8 TTS 管离线高吞吐输出,同月发布拼出语音全栈。

## 资源

- 官方文章:https://deepmind.google/blog/introducing-gemini-3-8-live-and-3-8-live-extended-thinking/
- 试用:https://aistudio.google.com/
- 第三方基准:https://artificialanalysis.ai/

> 注:deepmind.google 在检索环境不可达,本文经 my2cents.ai 日报(引用官方原文)/the-decoder/spyingbee 等多源交叉验证。
