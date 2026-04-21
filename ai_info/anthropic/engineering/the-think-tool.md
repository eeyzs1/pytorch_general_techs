# The "Think" Tool: Enabling Claude to Stop and Think in Complex Tool Use Situations

- **原文链接**: [The "think" tool: Enabling Claude to stop and think in complex tool use situations](https://www.anthropic.com/engineering/claude-think-tool)
- **发布日期**: 2025-03-20
- **标签**: #工具 #推理 #思维链 #CoT #复杂任务

## 核心观点

"Think" 工具允许 Claude 在生成响应的过程中暂停并记录显式思考，在复杂推理或多步骤工具使用场景中显著提升性能。与 Extended Thinking（在生成响应前深度思考）不同，"Think" 工具是在响应生成过程中添加的中间思考步骤。Think Tool 是 [Effective Context Engineering for AI Agents](effective-context-engineering-for-ai-agents.md) 中"即时上下文检索"策略的补充——前者管理信息流，后者管理推理过程。

## 关键概念

### Think Tool vs Extended Thinking

| 特性 | Extended Thinking | Think Tool |
|------|------------------|------------|
| 时机 | 响应生成前 | 响应生成过程中 |
| 用途 | 深度规划与迭代 | 验证信息、检查进度 |
| 触发方式 | 自动/关键词触发 | 作为工具调用 |

### 使用场景
- 执行长链工具调用时，在中间步骤验证是否有足够信息继续
- 长时间多步骤对话中，检查是否遗漏关键信息
- 需要回溯或遵守详细策略的复杂任务

### 性能提升
- 在复杂策略遵循任务上实现了 **54% 的相对改进**
- 在 τ-Bench 基准测试中表现显著提升

### 工作原理
Think Tool 不改变环境或数据库，仅将思考追加到日志中，帮助 Agent：
- 处理信息并做出决策
- 回溯之前的推理
- 遵守详细的策略规则
- 在关键决策点进行自我验证

Think Tool 的设计遵循 [Building Effective Agents](building-effective-agents.md) 中"优先透明性"原则——让 Agent 的推理过程可见。同时，它也是 [Writing Effective Tools for AI Agents](writing-effective-tools-for-ai-agents.md) 中"工具应自包含、对错误健壮"原则的体现。

## 实践建议

- 在需要多步推理的 Agent 系统中添加 Think Tool
- 将 Think Tool 作为"草稿本"使用，让 Agent 在关键节点记录推理过程
- 与 Extended Thinking 配合使用：Extended Thinking 用于初始规划，Think Tool 用于执行中的检查点
- 在 [Claude Code Best Practices](claude-code-best-practices.md) 中，"think"、"think hard"、"think harder"、"ultrathink" 关键词触发不同深度的 Extended Thinking，与 Think Tool 互补
