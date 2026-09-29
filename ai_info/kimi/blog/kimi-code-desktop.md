# Kimi Code Desktop 正式发布(Kimi Code Desktop)

- **原文链接**: [Kimi Code Desktop is Now Available](https://www.kimi.com/news/kimi-code-desktop)
- **作者**: Moonshot AI
- **发布日期**: 2026-09-21
- **检索日期**: 2026-09-29
- **标签**: #KimiCode #桌面端 #AgentIDE #多Agent #开发工具

## 核心观点

Kimi Code Desktop 正式发布(changelog GA 于 09-17),覆盖 macOS(Apple Silicon/Intel)与 Windows。它是一个对话驱动的编码 Agent:读写代码、运行命令,并提供 Plan/Goal/Swarm/Tower(实验性)四种模式,从"先计划后执行"到多 Agent 并行全覆盖。

产品打磨集中在审阅与安全:按文件的 diff 审阅面板、内置终端、可截图标注/划词评论/@文件/元素点选的内置浏览器、Git 状态区,以及三档权限控制。本地 CLI 发起的任务会直接出现在桌面端;CLI 同步升级 v2.0.0(/desktop 命令)与 v2.1.0(全屏 TUI)。

## 关键发现 / 关键技术

### 1. 跨平台与 GA 节奏

- macOS(Apple Silicon/Intel)+ Windows 双平台
- changelog GA 日期 2026-09-17,发布公告 2026-09-21

### 2. 对话驱动的 Agent

- 以对话驱动 Agent 读写代码、运行命令
- 编辑与执行循环收敛进同一界面,降低上下文切换

### 3. 四种模式

| 模式 | 说明 |
|------|------|
| Plan | 先出计划,确认后执行 |
| Goal | 多轮推进长任务,可暂停/恢复 |
| Swarm | 主 Agent 调度 Subagent 协作 |
| Tower(实验性) | 多 Agent 并行工作 |

### 4. 审阅与内置工具

- diff 面板:按文件逐一审阅改动
- 内置终端:命令执行不离开应用
- 内置浏览器:截图标注、划词评论、@文件、元素点选
- Git 状态区:工作区改动一目了然
- 审阅粒度到文件与页面元素,长任务的每一步都可人工把关

### 5. 权限三档

- 始终询问 / 必要时询问 / 完全自动,按风险偏好调节自主程度
- 从谨慎试点到放开吞吐,同一产品可服务个人开发者与企业团队

### 6. CLI 协同

- 本地 CLI 发起的任务直接出现在桌面端任务列表
- CLI v2.0.0(09-17):新增 /desktop 命令
- CLI v2.1.0(09-23):全屏 TUI

## 实践意义

- **桌面端成为 Agent 竞争新阵地**:Kimi、Codex、Claude 都在做 chat-first 桌面 Agent,差异化集中在审阅体验与多 Agent 编排
- **权限分级是落地关键**:三档权限让个人开发者与企业团队都能找到安全/效率平衡点
- **CLI 与桌面端互通**:任务在两端可见,适配终端重度用户与 GUI 用户混合的团队

## 跨厂商对比

- 与 [Codex for Every Role](../../openai/research/codex-for-every-role-tool-workflow.md) 对比:Codex 强调把 Agent 嵌入各职能的工作流与工具链,Kimi Code Desktop 先把开发者自己的工作台做厚
- 与 [The AI-Native SDLC Playbook](../../anthropic/engineering/the-ai-native-sdlc-playbook.md) 对比:Anthropic 给出 AI 原生研发生涯方法论,Kimi 用 Plan/Goal/Swarm/Tower 四模式将其产品化
- 与 [Kimi K2.8 Preview](kimi-k2-8-preview.md) 关联:Desktop 是 K2.8/K3 能力的主要承载端,同期发布节奏相互咬合
- 与 [Kimi K2.7 Code](kimi-k2-7-code.md) 关联:CLI 底座模型的演进史,Desktop 是其 GUI 延伸

## 资源

- 发布:[Kimi Code Desktop](https://www.kimi.com/news/kimi-code-desktop)
- 下载与文档:[Kimi Code](https://www.kimi.com/code)
- 更新日志:[Kimi Code: What's New](https://www.kimi.com/code/docs/kimi-code/whats-new.html)
