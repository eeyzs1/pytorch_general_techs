# Helping ChatGPT Better Recognize Context in Sensitive Conversations

- **原文链接**: [Helping ChatGPT better recognize context in sensitive conversations](https://openai.com/index/chatgpt-recognize-context-in-sensitive-conversations/)
- **作者**: OpenAI
- **发布日期**: 2026-05-14
- **检索日期**: 2026-06-07
- **标签**: #ChatGPT #安全 #心理健康 #自残预防 #上下文感知 #SafetySummaries

## 核心观点

OpenAI 发布 ChatGPT 安全更新——通过"安全摘要"（Safety Summaries）机制，让 ChatGPT 能跨对话识别逐渐出现的风险信号。当风险在多个对话中逐渐显现时，模型能更好地识别模式并做出更安全的响应。

## 关键更新

### 安全摘要（Safety Summaries）
- 由专门训练的安全推理模型生成的简短事实性笔记
- 记录早期对话中与安全相关的上下文
- 范围狭窄、保存时间有限、仅在严重安全风险时使用
- 设计目标是捕获安全上下文，而非通用个性化或长期记忆

### 性能提升
- **单对话场景**：自杀/自残安全响应提升 50%，伤害他人场景提升 16%
- **跨对话场景（GPT-5.5 Instant）**：伤害他人安全响应提升 52%，自杀/自残提升 39%
- 安全摘要质量：安全相关性 4.93/5，事实性 4.34/5（4000+ 评估）
- 日常对话中无明显质量下降

### 专家参与
- 与全球医生网络中的精神科医生和心理学家合作
- 涵盖法医心理学、自杀预防和自残领域专家

### 当前限制
- 聚焦于自残和伤害他人场景
- 未来可能扩展到生物安全、网络安全等其他高风险领域

## 关键洞察

1. "跨对话风险识别"是 AI 安全的前沿难题——单条消息看似无害，但跨对话上下文可能揭示风险
2. Safety Summaries 是"专用安全记忆"——与 Dreaming V3 的通用个性化记忆互补但目标不同
3. 在安全性和日常体验之间取得了良好的平衡——日常对话无明显质量下降
4. 该技术可扩展到网络和生物安全等更广泛的风险领域

## 相关文章

- [Introducing Trusted Contact in ChatGPT](introducing-trusted-contact-in-chatgpt.md)
- [Dreaming: Better Memory for a More Helpful ChatGPT](chatgpt-memory-dreaming.md)
- [How We Monitor Internal Coding Agents for Misalignment](how-we-monitor-internal-coding-agents-for-misalignment.md)