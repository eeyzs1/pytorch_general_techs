# 最大化 Claude Code 会话价值（Maximizing the value of your Claude Code sessions）

- **原文链接**: [Maximizing the value of your Claude Code sessions](https://claude.com/blog/maximizing-the-value-of-your-claude-code-sessions)
- **作者**: Anthropic
- **发布日期**: 2026-08-14
- **检索日期**: 2026-08-21
- **标签**: #Anthropic #ClaudeCode #Token优化 #会话管理 #PromptCache #最佳实践

## 核心观点

Anthropic 发布 Claude Code 会话效率指南，教用户"如何运行高效会话，从每个 token 中获得最大价值"。核心洞察：会话管理（而非提示技巧）是 token 成本的主要杠杆——上下文积累、模型切换、缓存失效都会显著影响成本。文章给出了从 `/clear` 到 `/compact` 的具体操作建议。

关键建议包括：任务间运行 `/clear` 防止无关上下文回流；开始前设置模型与 effort 档位（中途更改会破坏 prompt cache 增加成本）；用 `@-mention` 引用文件替代命名（省一次 Read 调用）；为嘈杂命令添加静默标志或放子 Agent 执行；新会话先跑 `/context` 检查加载内容；离开键盘前先 `/compact`（prompt cache 会过期）。

## 关键发现 / 关键技术

### 1. 会话卫生（Session Hygiene）
- 任务间 `/clear`：防止无关上下文回流模型，减少 token
- 新会话 `/context`：检查已加载内容（CLAUDE.md、MCP 工具定义），裁掉不必要部分
- 离开前 `/compact`：prompt cache 过期前压缩

### 2. 缓存友好的会话设计
- 开始前设置模型与 effort 档位，中途更改破坏 prompt cache
- 保持精确前缀稳定以维持高缓存命中率
- 批量任务共享同一前缀获益最大

### 3. 上下文输入优化
- `@-mention` 文件直接附加内容，省 Read 调用或搜索
- 嘈杂命令加静默标志，或放子 Agent 隔离输出
- 工具输出一旦进入会话就保留到结束，需控制

### 4. 与成本可见性的衔接
- 会话级优化与 [企业成本指南](cost-visibility-and-control-in-claude.md) 形成互补
- 个人开发者可自行控制 token 消耗
- 与 prompt caching 计费机制（10% 费率）联动

## 实践意义

Claude Code 的成本大头不是单次调用而是会话积累：每次模型调用都会携带此前全部上下文。这份指南把"上下文工程"落到 CLI 操作的粒度——`/clear`、`/compact`、`@-mention`、effort 前置设置等具体动作。对重度用户和按量计费团队，这些操作可显著降低成本；这也印证了 Anthropic "上下文是稀缺资源"的一贯理念。

## 跨厂商对比

- 与 [Claude 成本可见性与控制](cost-visibility-and-control-in-claude.md) 互补：前者是企业级管控（模型分级 + 支出上限），本文是开发者级会话优化
- 与 [Contextual Retrieval 上下文优化](introducing-contextual-retrieval.md) 对比：检索层优化减少上下文体积，会话管理减少上下文积累
- 与 [Codex-Maxxing 长任务实践](../../openai/research/codex-maxxing-long-running-work.md) 对比：OpenAI 侧重长任务基础设施，Anthropic 侧重单会话 token 效率，两种效率路线

## 资源

- 论文：N/A
- 官方指南：https://claude.com/blog/maximizing-the-value-of-your-claude-code-sessions
