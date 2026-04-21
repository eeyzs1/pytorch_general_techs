# Introducing Operator

- **原文链接**: [Introducing Operator](https://openai.com/index/introducing-operator/)
- **发布日期**: 2025-01（2025-07 更新：集成到 ChatGPT 作为 ChatGPT Agent）
- **标签**: #Computer-Use #CUA #浏览器Agent #GUI交互 #Operator

## 核心观点

Operator 是 OpenAI 的首个 Computer-Using Agent (CUA)，能够像人类一样操作浏览器——点击、滚动、输入文字和填写表单。它通过解读屏幕截图与图形用户界面交互，解锁了协助完成各种日常任务的潜力。

## 关键概念

### Computer-Using Agent (CUA)
- 基于 CUA 模型构建
- 解读屏幕截图并操作 GUI——按钮、菜单和文本字段
- 与人类使用相同的工具和界面

### 能力范围
- 在浏览器中执行各种日常任务
- 订购杂货、预订餐厅、购买活动门票
- 填写表单、导航网站

### 安全设计
- 在远程浏览器中运行，而非用户本地环境
- 用户可随时接管控制
- 敏感操作（如支付）需用户确认
- 系统卡详细说明了安全评估

### 从 Operator 到 ChatGPT Agent
- 2025 年 7 月，Operator 完全集成到 ChatGPT 中
- 作为 ChatGPT Agent 提供更新后的能力

## 实践启示

- CUA 代表了 AI 与计算交互的新范式——从 API 调用到 GUI 操作
- 安全性是 CUA 的首要考虑——远程浏览器 + 用户确认
- Operator 的能力受限于网站的反自动化措施
- CUA 是 Agent 从"工具使用者"到"计算机使用者"的跨越

## 相关文章

- [A Practical Guide to Building Agents](a-practical-guide-to-building-agents.md) — Agent 构建方法论
- [New Tools and Features in the Responses API](new-tools-and-features-in-the-responses-api.md) — API 中的 Computer Use 工具
- [Introducing Deep Research](introducing-deep-research.md) — 另一种 Agent 能力
