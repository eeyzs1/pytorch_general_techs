# GPT-Live：新一代语音模型，实现自然人机交互

- **原文链接**: [Introducing GPT-Live](https://openai.com/index/introducing-gpt-live/)
- **作者**: OpenAI
- **发布日期**: 2026-07-08
- **检索日期**: 2026-07-20
- **标签**: #GPT-Live #VoiceAI #FullDuplex #ChatGPTVoice #RealtimeAPI #多模态

## 核心观点

GPT-Live 是 OpenAI 新一代语音模型，基于全双工架构实现"边听边说"的自然对话能力。与之前的语音模型相比，GPT-Live 能展现倾听反馈（如"嗯嗯"、"好的"）、快速来回对话、或在用户思考时保持安静。最核心突破是**智能委托机制**——当问题需要网络搜索、深度推理或复杂工作时，GPT-Live 会在后台调用最新前沿模型（当前为 GPT-5.5），完成后将结果带回对话，全程保持语音流畅。

## 关键发现 / 关键技术

### 1. 全双工架构
- 真正同时听和说，消除传统语音助手的"对讲机"感
- 支持自然对话节奏：打断、重叠、停顿、反馈词
- 在对话中展现"在场感"——知道何时说话、何时倾听

### 2. 智能委托机制
- 简单问题：GPT-Live 直接回答，保持低延迟
- 复杂问题：后台委托给 GPT-5.5（或未来更新模型），期间保持对话流畅
- 结果整合：将前沿模型的答案自然融入语音回复

### 3. 模型版本
- **GPT-Live-1**：完整能力版本
- **GPT-Live-1 mini**：轻量版本，平衡性能与成本
- 已向 ChatGPT 全球用户推出，API 即将开放

### 4. 与 ChatGPT Voice 集成
- 新 ChatGPT Voice 体验更智能、更自然
- 为复杂、长时间、agentic 语音工作奠定基础

## 实践意义

GPT-Live 代表了语音交互从"命令-响应"到"自然协作"的范式转变：
- **客户服务**：更自然的语音客服，能处理复杂查询
- **无障碍**：为视障或行动不便用户提供更平等的交互方式
- **移动场景**：驾驶、烹饪等场景下的安全语音交互
- **Agent 语音化**：为语音 Agent 处理复杂任务提供技术基础

## 跨厂商对比

- 与 [GPT-5.5 Instant](gpt-5-5-instant.md) 对比：GPT-Live 是语音专用模型，GPT-5.5 Instant 是通用文本模型；GPT-Live 在后台可调用 GPT-5.5 处理复杂任务
- 与 [Gemini Live](../../google/deepmind/gemini-3.5.md) 对比：Google 的 Gemini Live 也强调自然对话，但 OpenAI 的委托机制是独特差异化
- 与 [Claude Voice](../../anthropic/research/global-workspace.md) 对比：Anthropic 尚未发布专用语音模型，Claude 的语音能力通过 API 第三方集成

## 资源

- 系统卡：[GPT-Live System Card](https://deploymentsafety.openai.com/gpt-live)
- API 通知表单：[GPT-Live in the API](https://openai.com/form/gpt-live-1-in-the-api/)
