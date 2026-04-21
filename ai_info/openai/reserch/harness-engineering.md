# Harness Engineering: Building the Codex App Server for an Agent-First World

- **原文链接**: [Harness engineering](https://openai.com/index/harness-engineering/)
- **作者**: Ryan Lopopolo 等
- **发布日期**: 2026-02
- **标签**: #Harness工程 #Codex #零手写代码 #Agent-First #AGENTS-md

## 核心观点

OpenAI 进行了一项极限实验：**完全零手写代码**构建并交付一个内部 Beta 版软件产品。5 个月内，3 名工程师使用 Codex 生成了约 **100 万行代码**，开启了约 1,500 个 PR。人类不再写代码，而是设计系统环境、明确意图、建立反馈循环——这就是"Harness Engineering"。

## 关键概念

### 核心理念：完全不用手写代码
- 人类从不直接撰写任何代码
- 工程师工作重心转向系统设计、搭建框架和提升杠杆效率
- 代码产出效率提升后，瓶颈变成人类 QA 的处理能力

### AGENTS.md 模式
- 类似 Anthropic 的 CLAUDE.md，但由 Codex 自己生成
- 最初用于指引 Agent 如何在代码库执行任务的 AGENTS.md 文件本身也是由 Codex 生成的
- 从一开始，代码库的构建就是由 Agent 主导的

### 依赖流控制
依赖按受控序列流动：**Types → Config → Repo → Service → Runtime → UI**，Agent 被限制在这些层内操作。

### 关键战术

#### 构建时间控制在一分钟内
- 内循环：团队持续重建构建系统（从 Makefile 到 Bazel 再到 Nx），确保构建时间严格在 1 分钟内
- 逻辑分解：如果构建变慢，Agent 自动将构建图分解为更细粒度的部分

#### PR 审查范式转变
- 代码可轻松并行化时，真正的稀缺资源是"人类注意力"
- 后合并审查：不再在合并前进行冗长手动审查，而是自动化
- 大多数手动审查在代码合并后进行，用于质量检查和经验积累

#### 可观测性赋能
- 工程师工作不再是修 Bug，而是为 Agent 提供 Traces 和可观测性工具
- 使 Agent 具有"自愈"能力
- 让应用 UI、日志和应用指标直接对 Codex 可读

#### 经验"蒸馏"
- 高级工程师心中的"隐性知识"被写入 Skill 文档和测试
- 固化为系统上下文的一部分

### "幽灵库"与依赖内化
- 随着 Token 成本趋近于零，软件依赖可能逐渐消失
- **幽灵库 (Ghost Libraries)**: 开发者只需定义高保真 Spec，让 Agent 重新组装和实现
- **依赖内化**: 对中低复杂度的第三方库，Agent 可将其内联重写到仓库中

## 实践启示

- 从"Co-pilot"到"独立队友"——未来软件开发将围绕 Agent 可读性重构整个代码库
- 人成为系统架构的"牧羊人"
- 构建时间是 Agent 效率的关键约束
- 隐性知识显式化是规模化 Agent 的前提

## 相关文章

- [A Practical Guide to Building Agents](a-practical-guide-to-building-agents.md) — Agent 构建的基础方法论
- [Introducing Codex](introducing-codex.md) — Codex Agent 产品
- [Building an AI-Native Engineering Team](building-an-ai-native-engineering-team.md) — AI 原生工程团队
- [Introducing AgentKit](introducing-agentkit.md) — Agent 构建工具集
