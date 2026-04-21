# Introducing Apps in ChatGPT and the New Apps SDK

- **原文链接**: [Introducing apps in ChatGPT and the new Apps SDK](https://openai.com/index/introducing-apps-in-chatgpt/)
- **发布日期**: 2025-10-06
- **标签**: #Apps-SDK #ChatGPT应用 #MCP #超级App #应用生态

## 核心观点

OpenAI 在 ChatGPT 中引入了全新一代应用——用户可以在对话中直接与第三方应用交互。开发者可以通过新的 Apps SDK（预览版）开始构建这些应用，该 SDK 基于 Model Context Protocol (MCP) 构建。

## 关键概念

### ChatGPT 中的 Apps
- 用户可在对话中直接启动应用（输入应用名或接受 ChatGPT 建议）
- 应用根据对话上下文自动推荐
- 首批合作伙伴：Spotify、Canva、Booking.com、Figma、Expedia、Zillow 等
- 支持应用内交易和支付

### Apps SDK
- 基于 MCP（Model Context Protocol）构建——开放标准
- 开发者可定义：
  - **逻辑**: 应用如何处理和响应用户查询
  - **界面**: ChatGPT 内的用户界面和交互元素
  - **认证**: 安全登录和数据访问系统
- 预览版可用，开发者模式支持测试
- 计划推出应用提交流程、应用目录和变现机制

### ChatGPT 作为"操作系统"
- 类比 iOS 生态：ChatGPT = 操作系统，Apps SDK = 开发工具，8 亿用户 = 生态基础
- Agentic Commerce Protocol：支持 ChatGPT 内即时结账与交易
- 应用可暴露上下文回 ChatGPT，使模型能回答后续问题

### 与 MCP 的关系
- Apps SDK 构建在 MCP 之上
- 用 MCP 标准构建的应用可在任何兼容平台上运行
- 标志着 OpenAI 对开放协议的采纳

## 实践启示

- ChatGPT 正从"聊天机器人"演变为"超级应用平台"
- MCP 的采纳意味着 OpenAI 在开放生态上的态度转变
- 开发者现在可以在 8 亿用户的平台上构建应用
- 应用内交易将创造新的商业模式

## 相关文章

- [New Tools for Building Agents](new-tools-for-building-agents.md) — Agent 开发的基础工具
- [Introducing AgentKit](introducing-agentkit.md) — Agent 构建工具集
- [Introducing Codex](introducing-codex.md) — Codex 的 GA 版本
- [New Tools and Features in the Responses API](new-tools-and-features-in-the-responses-api.md) — 底层 API
