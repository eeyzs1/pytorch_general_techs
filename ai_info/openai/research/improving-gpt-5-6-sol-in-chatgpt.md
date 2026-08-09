# 改进 ChatGPT 中的 GPT-5.6 Sol

- **原文链接**: [Improving GPT-5.6 Sol in ChatGPT—and expanding access to GPT-5.6 Luna for free users](https://openai.com/index/improving-gpt-5-6-sol-in-chatgpt/)
- **作者**: OpenAI
- **发布日期**: 2026-08-06
- **检索日期**: 2026-08-08
- **标签**: #GPT-5.6Sol #GPT-5.6Luna #ChatGPT #推理控制 #免费用户

## 核心观点

OpenAI 更新了 ChatGPT 中的 GPT-5.6 Sol，使其提供更聚焦的答案、更可靠的事实，并通过新的"思考"滑块让用户控制推理深度。Plus 和 Pro 用户现在用同一模型驱动即时响应和深度推理，体验更一致。Free 和 Go 用户的默认模型升级为 GPT-5.6 Luna，并提供无限文本聊天和新的 Think 按钮以处理更难的问题。

内部评估显示，在需要事实细节的金融、医疗和法律提示中，GPT-5.6 Luna 的含错误响应比 GPT-5.5 Instant 少约 62%，GPT-5.6 Sol 少约 68%。系统卡还引入了针对 18 岁以下用户的安全训练措施。

## 关键发现 / 关键技术

### 1. 更聚焦的答案
- 直接回答问题，避免不必要的格式和额外细节
- 快速问题给直接答案，多步骤规划/研究/写作给更完整但保持主推荐清晰的响应
- 以骑行天气查询为例：GPT-5.6 Sol 先回答"是否会淋湿"，再指出风而非雨是主要因素

### 2. 更可靠的事实
- 在金融、医疗、法律事实性提示评估中，GPT-5.6 Luna 错误响应减少 62%，GPT-5.6 Sol 减少 68%（相比 GPT-5.5 Instant）
- 更好地利用搜索到的来源回答问题，尤其在日期、数字、来源、规则、假设方面

### 3. 推理滑块与一致性
- Plus/Pro 用户可在 Web、移动端和桌面端使用新滑块控制推理深度
- Instant 和 Thinking 体验由同一模型驱动，切换时不再感觉像换了一个模型
- Free 用户通过新的 Think 按钮访问更深推理

### 4. 安全与可用性
- 针对 18 岁以下用户训练模型避免浪漫角色扮演、年龄限制挑战、替代真实人际关系
- 年龄适当的性内容、饮食障碍与身体形象风险、危险活动、图形暴力边界
- 鼓励青少年在需要支持时联系信任的人
- GPT-5.6 Sol 的 Chat 版本仅限 Chat 体验，Work 和 Codex 版本不变

## 实践意义

推理滑块代表了用户体验设计的新方向——将"思考多少"的控制权交给用户，而非模型自行决定。同一模型驱动即时和深度推理消除了体验不一致问题。Free 用户获得无限文本聊天和 Think 按钮是"丰富智能"使命的具体落地，显著降低了高级推理的访问门槛。

## 跨厂商对比

- 与 [预览 GPT-5.6 Sol](previewing-gpt-5-6-sol.md) 互补：该文是 Sol 的初始预览，本文是其发布后的能力改进与扩展
- 与 [GPT-5.6 前沿智能与效率](gpt-5-6-frontier-intelligence-efficiency.md) 互补：前者聚焦模型效率与前沿能力设计，本文聚焦 ChatGPT 中的实际体验优化
- 与 [GPT-5.6 介绍](introducing-gpt-5-6.md) 对比：该文是 GPT-5.6 系列的整体发布，本文是针对 Chat 场景的特定调优

## 资源

- 系统卡：https://cdn.openai.com/pdf/GPT_5_6_August_Updates.pdf
- 代码：N/A
- Demo：N/A
