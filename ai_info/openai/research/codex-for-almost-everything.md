# Codex for (almost) Everything

- **原文链接**: [Codex for (almost) everything](https://openai.com/index/codex-for-almost-everything/)
- **发布日期**: 2026-04-17
- **标签**: #Codex #重大升级 #ComputerUse #多Agent #图像生成 #插件生态 #记忆 #后台自动化

## 核心观点

Codex 发布里程碑式重大更新，面向每周超过 300 万开发者。Codex 从单一的代码编写助手升级为能操作电脑、使用任意桌面应用、生成图像、记忆偏好并从过往行为中学习的全能 Agent 平台。App 新增了深度开发者工作流支持，包括 PR 审查、多文件/终端查看、SSH 远程连接和应用内浏览器。

## 关键更新

### Computer Use：操控你的电脑
- Codex 能"看见"屏幕内容，使用独立光标模拟点击和键盘输入
- 可操作 Mac 上任意桌面应用（后台运行，不影响用户自己的工作）
- 多个 Agent 可在 Mac 上并行工作
- 适用场景：前端变更迭代、应用测试、操作不带 API 的应用
- 初始仅支持 macOS，后续扩展

### 应用内浏览器
- App 内置浏览器，开发者可在页面上直接评论提供精确指令
- 适用于前端和游戏开发
- 计划扩展至完整浏览器操控（超越 localhost）

### gpt-image-1.5 集成
- Codex 可调用图像模型生成和迭代图像
- 结合截图和代码，在同一工作流中创建产品概念图、前端设计、mockup 和游戏素材

### 90+ 新增插件
- 整合 Skills、应用集成和 MCP 服务器
- 重点插件：Atlassian Rovo（JIRA）、CircleCI、CodeRabbit、GitLab Issues、Microsoft Suite、Neon、Remotion、Render、Superpowers

### 开发者工作流增强
- **GitHub PR 审查**：直接在 App 中处理 Review 评论
- **多终端标签页**：同时运行多个终端
- **SSH 远程连接**（alpha）：连接到远程 devbox
- **富媒体预览**：PDF、电子表格、幻灯片、文档在侧边栏直接查看
- **摘要面板**：追踪 Agent 计划、来源和产出物

### 增强的 Automations
- 支持复用已有对话线程，保留此前建立的上下文
- Codex 可为未来安排任务并在时间到达时自动唤醒继续工作（可跨天数或周）
- 团队用例：自动合入 PR、Slack/Gmail/Notion 消息跟进

### 记忆（Memory）- 预览
- Codex 可记住有用上下文：个人偏好、修正意见、耗时收集的信息
- 未来任务完成更快、质量更高——不再依赖大量自定义指令
- 结合项目上下文、已连接插件和记忆，Codex 可主动建议开始新一天的工作或接续之前的项目

### 个性化功能
- 上下文感知建议：Codex 可识别 Google Docs 中的待处理评论、从 Slack/Notion/代码库获取相关上下文、提供优先级排序的行动清单
- 记忆和个性化功能后续向 Enterprise/Edu 和 EU/UK 用户推出

## 产品演进

Codex 一年的演进路径：
```
编写代码 → 理解系统 → 收集上下文 → 审查工作
  → 调试问题 → 协调整合 → 维持长期工作
```

## 与 Anthropic 对比

| 能力 | OpenAI Codex | Anthropic Claude Code |
|------|-------------|----------------------|
| 桌面应用操控 | Computer Use (Mac) | Computer Use |
| 多 Agent 并行 | 多 Agent Worktree | Agent Teams |
| 图像生成 | gpt-image-1.5 | 无 |
| 插件生态 | 90+ 插件 | MCP 服务器生态 |
| 背景自动化 | Automations（定时+云触发） | Managed Agents |
| 记忆/个性化 | Memory（预览） | Memory |
| 应用形态 | App + CLI + IDE + Web + Slack | App + CLI + IDE |

## 相关文章

- [Introducing Codex](introducing-codex.md) — Codex 初始发布
- [Introducing the Codex App](introducing-the-codex-app.md) — Codex App 发布
- [Codex Now Generally Available](codex-now-generally-available.md) — Codex GA
- [Harness Engineering](harness-engineering.md) — 极限使用实验
- [Equipping the Responses API with a Computer Environment](equipping-the-responses-api-with-a-computer-environment.md) — Agent 基础设施
