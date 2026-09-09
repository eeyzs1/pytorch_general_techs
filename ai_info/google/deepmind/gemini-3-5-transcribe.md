# 更智能的语音转文字：Gemini 3.5 Transcribe（Intelligent transcription with Gemini 3.5 Transcribe）

- **原文链接**: [Intelligent transcription with Gemini 3.5 Transcribe](https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-5-transcribe/)
- **作者**: Google DeepMind（官方博客未署名）
- **发布日期**: 2026-08-26
- **检索日期**: 2026-09-09
  注：官方页面抓取受限，本文基于检索核验的日期与公开报道整理（细节经 Speech Technology 杂志对官方发布的转述核验）
- **标签**: #Gemini #Transcribe #ASR #实时转写 #语音Agent

## 核心观点

Google 发布 Gemini 3.5 Transcribe，官方称之为"迄今最精确的语音转文字模型"。它不只是把音频变成文字，而是在转写中理解说话意图：自动处理自我纠正（如"周二见——不对，周三"）、去除"嗯/啊"等语气填充词并自动排版，把原始音频直接转换为可用的格式化文本。

模型同时覆盖两条路径：实时流式（Live API，双向流、亚秒级延迟）与预录制音频处理（Interactions API，支持说话人归属与词级时间戳）。除 API 外，它还被植入 Gboard、Antigravity、Gemini app 与 Chrome 等日常界面，把"智能转写"从开发者能力扩展为平台级输入方式。

## 关键发现 / 关键技术

### 1. 智能转写而非逐字记录
自动去除填充词、处理自我纠正、自动格式化；支持自定义词汇表（行话与特殊拼写），可准确捕获邮政编码、订单号等字母数字实体。嘈杂真实环境中平均词错率（WER）：流式 4%、非流式 2.6%。

### 2. 双 API 形态与多语言
Live API 使用 gemini-3.5-transcribe-live 提供连续双向流式转写（亚秒延迟），适合语音 Agent 与实时字幕；Interactions API 使用 gemini-3.5-transcribe 面向录音、会议、通话记录，提供说话人归属与词级时间戳，预录制音频最多区分 3 个说话人；自动检测并转写 85+ 种语言，兼容地区口音。

### 3. 函数调用与界面落地
可通过 function calling 把图像生成、文件分析等任务委派给其他 Gemini 模型；已进入 Google AI Studio（Build 模式语音编程）、Gboard（Android 新增 Rambler 功能：语音转文字并语音编辑）、Antigravity（结合屏幕上下文与聊天历史）、Gemini app（macOS，语音命令驱动复杂工作流），即将登陆 Chrome（任意网页输入框语音输入）。

## 实践意义

对构建语音 Agent、实时字幕与通话后分析的团队，3.5 Transcribe 把过去需要额外后处理（去填充词、分段、说话人分离）的流水线压缩进单一模型调用，降低延迟与工程复杂度；智能转写与函数调用的组合让"语音作为 Agent 入口"成为默认交互形态。评估时需注意：WER 数字来自 Google 自测，中文等具体语种表现需自行验证。

## 跨厂商对比

- 与 [Gemini 3.1 Flash TTS：下一代富有表现力的 AI 语音](gemini-3-1-flash-tts.md) 对比：TTS 负责"文字→语音"，Transcribe 负责"语音→文字"，两者共同构成 Gemini 的语音双向通道；Transcribe 强调理解与清理，TTS 强调生成表现力。
- 与 [度量语音识别中的基准优化](../../huggingface/blog/asr-benchmark-optimization.md) 互补：HF 侧关注 ASR 基准的构建与"针对基准优化"的检测方法学，本文提供闭源商用 ASR 的最新能力基线（WER 4%/2.6%），对照可校准自测与公开基准的差距。

## 资源

- 官方文章：https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-5-transcribe/
- 产品/API：https://aistudio.google.com/
