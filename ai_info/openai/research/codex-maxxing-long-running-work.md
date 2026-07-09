# Codex-Maxxing for Long-Running Work

- **原文链接**: [Codex-maxxing for long-running work](https://openai.com/index/codex-maxxing-long-running-work/)
- **作者**: Jason Liu（白皮书）
- **发布日期**: 2026-06-22
- **检索日期**: 2026-06-29
- **标签**: #Codex #LongRunningWork #WhitePaper #Harness #PersistentWorkspace

## 核心观点

OpenAI 发布白皮书（Jason Liu 撰写），系统阐述 **Codex 用于长视野任务**的实践方法：把 Codex 当作**持久化工作区**——保留上下文、管理复杂工作流、维持长项目的进展。核心方法论：**将远大目标拆分为可验证步骤，维持跨工作流的连续性，判断何时委托给 Codex vs 何时人类监督最有效**。

## 关键策略

### 1. 持久化工作区
- Codex 不仅是一个 prompt-response 工具——它能维持长项目的"状态"
- 在多个 session 之间保留上下文、决策、进度

### 2. 拆解 + 验证
- 把远大目标分解为**可验证的小步骤**
- 每步有明确的成功标准
- 避免"端到端大任务"的黑盒

### 3. 跨工作流连续性
- Codex 在多个并行工作流之间保持一致性
- 复用之前的决策、约束、模式

### 4. 委托 vs 监督的判断
- 何时让 Codex 自主执行（明确、可验证、低风险）
- 何时人类必须深度参与（高风险、模糊、需要判断）

## 关键洞察

1. **持久化是长视野的关键**——单次 session 的 Agent 受限于上下文窗口
2. **验证 > 完成**——每步可验证比一次性完成更可靠
3. **人类判断不能完全外包**——关键决策点需要人类监督
4. **这与 Harness Engineering 一脉相承**——"环境设计 > 代码编写"

## 相关文章

- [Harness Engineering](harness-engineering.md)
- [Building Self-Improving Tax Agents with Codex](building-self-improving-tax-agents-with-codex.md)
- [Introducing the Codex App](introducing-the-codex-app.md)
- [Work with Codex from Anywhere](work-with-codex-from-anywhere.md)