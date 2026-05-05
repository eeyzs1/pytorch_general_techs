# Introducing the Codex App

- **原文链接**: [Introducing the Codex App](https://openai.com/index/introducing-the-codex-app/)
- **发布日期**: 2026-02-02（3月4日更新：Windows 版上线）
- **标签**: #Codex #桌面应用 #多Agent编排 #Skills #Automations #macOS #Windows

## 核心观点

Codex App 是 OpenAI 推出的 macOS 桌面应用（后扩展 Windows），专为多 Agent 并行编排而设计。它将 Codex 从一个"代码编写者"升级为可以同时管理多个 Agent 的命令中心，支持长时间运行的任务与后台自动化。同时推出了 Skills 系统和 Automations 自动调度。

## 关键概念

### 多 Agent 编排
- 多个 Agent 在独立线程中运行，按项目组织
- 支持 worktree，多个 Agent 可同时操作同一仓库而不产生冲突
- 每个 Agent 在隔离的代码副本上工作
- 可在 App 中审查 Agent 变更、评论 diff，或在本地编辑器中手动修改

### Skills 技能系统
- Skills 是可复用的指令+资源+脚本包，扩展 Codex 超越代码生成
- App 内置专门的 Skills 创建和管理界面
- 可显式指定使用某 Skill，或让 Codex 根据任务自动选择
- 支持团队跨仓库共享 Skills
- 内置 Skill 库涵盖：Figma 设计转代码、Linear 项目管理、Cloudflare/Netlify/Render/Vercel 云部署、GPT Image 图像生成、OpenAI API 文档、PDF/Excel/Docx 文档操作

### Automations 自动调度
- 按预定时间表在后台自动运行 Agent 任务
- 完成后结果进入审查队列
- 可设置定期执行日历
- OpenAI 内部用例：每日 issue 分诊、CI 失败查找和总结、每日发布简报生成

### 安全保障
- 使用原生开源且可配置的系统级沙箱
- 默认限制 Agent 只能编辑工作目录内的文件
- 网络访问等高风险操作需用户授权
- 支持项目和团队级别的权限规则配置

### 双人格模式
- 开发者可选两种 Agent 交互风格：简洁执行型 vs 对话共情型
- 能力完全相同，仅交互风格不同
- 通过 `/personality` 命令切换

## 实践启示

- Codex App 代表了从"终端/IDE 内工具"到"独立 Agent 工作台"的形态演进
- Skills + Automations 的组合使得 Codex 具备了"自主工作流"能力，不再需要实时人类监督
- Worktree 隔离是多 Agent 并行编程的关键基础设施
- 截至 2026 年 2 月，Codex 周活跃开发者超过 100 万，整体用量自 GPT-5.2-Codex 以来翻倍

## 相关文章

- [Introducing Codex](introducing-codex.md) — Codex 的初始发布
- [Codex Now Generally Available](codex-now-generally-available.md) — Codex GA 版本
- [Codex for (almost) everything](codex-for-almost-everything.md) — 2026年4月重大升级
- [Harness Engineering](harness-engineering.md) — Codex 的极限使用实验
- [Introducing AgentKit](introducing-agentkit.md) — Agent 构建工具集
