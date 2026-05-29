# 上下文工程阅读路线

## 先读

- [Effective Context Engineering for AI Agents](../anthropic/engineering/effective-context-engineering-for-ai-agents.md)：从提示工程转向上下文工程的核心文章。
- [Claude Code Best Practices](../anthropic/engineering/claude-code-best-practices.md)：CLAUDE.md、计划模式、测试循环等编码 Agent 实践。
- [GPT-4.1 Prompting Guide](../openai/research/gpt-4-1-prompting-guide.md)：OpenAI 侧的提示与指令组织经验。

## 检索与记忆

- [Introducing Contextual Retrieval](../anthropic/engineering/introducing-contextual-retrieval.md)：Contextual Embeddings + BM25 + rerank 的 RAG 优化。
- [Equipping Agents for the Real World with Agent Skills](../anthropic/engineering/equipping-agents-for-the-real-world-with-agent-skills.md)：Skill 的渐进式披露。
- [Codex for (almost) Everything](../openai/research/codex-for-almost-everything.md)：Codex Memory、插件和桌面工作流演进。
- [Work with Codex from Anywhere](../openai/research/work-with-codex-from-anywhere.md)：跨设备 session 同步、远程环境和长任务上下文延续。

## 关键结论

- 上下文不是越多越好，目标是最小高信号 token 集合。
- 可持久化的项目规则、任务笔记和评估结果，比一次性长提示更可维护。
- 检索、压缩、Skill、记忆应该分层使用，避免把所有信息一次性塞进上下文。
