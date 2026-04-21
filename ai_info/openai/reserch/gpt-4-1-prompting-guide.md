# GPT-4.1 Prompting Guide

- **原文链接**: [GPT-4.1 Prompting Guide](https://github.com/openai/openai-cookbook/blob/main/examples/gpt4-1_prompting_guide.ipynb)
- **发布日期**: 2025-04
- **标签**: #提示工程 #GPT-4.1 #Agent提示 #持久性 #思维链

## 核心观点

GPT-4.1 不会自动执行思维链推理——需要在提示中显式请求。为充分利用 GPT-4.1 的 Agent 能力，OpenAI 推荐在所有 Agent 提示中包含三种关键提醒。这些指令将模型从"聊天机器人"转变为"主动 Agent"。

## 关键概念

### 推荐提示结构
```
# Role and Objective
# Instructions
  ## Sub-categories for more detailed instructions
# Reasoning Steps
# Output Format
# Examples
  ## Example 1
# Context
# Final instructions and prompt
```

### Agent 提示的三种关键提醒

1. **持久性 (Persistence)**
   - 确保模型理解它处于多轮对话中
   - 防止过早将控制权交回用户
   - 示例: "You are an agent - please keep going until the user's query is completely resolved"

2. **工具使用规划 (Tool Use Planning)**
   - 指导模型在调用工具前先规划
   - 防止盲目工具调用
   - 示例: "Before calling a tool, think about which tool to use and why"

3. **思维链 (Chain of Thought)**
   - GPT-4.1 不自动执行 CoT，需显式请求
   - 添加"Think step by step"或类似指令
   - 对复杂任务显著提升质量

### 提示工程最佳实践
- 使用 Markdown 标题组织提示结构
- 从通用 `# Instructions` 开始，添加具体子节
- 提供明确的工作流步骤列表
- 调试时检查冲突或不够具体的指令
- 示例是"值千言的图片"——多样化、规范的示例比长篇规则更有效

### SWE-bench 提升数据
添加三种 Agent 提醒后，SWE-bench Verified 分数显著提升。

## 实践启示

- GPT-4.1 的 Agent 能力需要通过提示"激活"
- 结构化提示比自由格式更有效
- 持久性提醒是 Agent 与聊天机器人的关键区别
- 思维链不是自动的——必须显式请求

## 相关文章

- [A Practical Guide to Building Agents](a-practical-guide-to-building-agents.md) — Agent 构建的基础方法论
- [Harness Engineering](harness-engineering.md) — AGENTS.md 模式
- [Introducing Codex](introducing-codex.md) — Codex 中的提示优化
