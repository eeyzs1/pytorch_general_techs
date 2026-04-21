# Effective Context Engineering for AI Agents

- **原文链接**: [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- **作者**: Prithvi Rajasekaran, Ethan Dixon, Carly Ryan, Jeremy Hadfield
- **发布日期**: 2025-09-29
- **标签**: #上下文工程 #提示工程 #上下文腐烂 #压缩 #子Agent

## 核心观点

随着 AI Agent 在更长任务中使用更多工具，编写一个好提示的老方法已不再足够。**上下文工程**是关于策划最小、最高信号的 token 集合，以最大化良好结果的可能性——跨越多轮 Agent 循环的每一轮。指导原则是：**找到最小可能的高信号 token 集合，最大化期望结果的可能性。每个 token 都在消耗模型有限的"注意力预算"。** 上下文工程是 [Building Effective Agents](building-effective-agents.md) 中 Agent 设计的核心——没有好的上下文管理，再好的架构也无法发挥作用。

## 关键概念

### 从提示工程到上下文工程
- **提示工程**: 关注单个指令的文本
- **上下文工程**: 管理流入模型有限注意力窗口的整个 token 宇宙——系统提示、工具、示例、消息历史、检索数据、MCP 状态

### 上下文腐烂 (Context Rot)
- 模型准确性随 token 数量增长而退化
- 根源于 Transformer 架构：每个 token 关注每个其他 token（n² 成对关系）
- 模型从训练数据中发展注意力模式，短序列更常见
- 位置编码插值允许处理更长序列但会退化——创造性能梯度而非硬性悬崖

### 系统提示的"金发姑娘区"
- **过于规定性**: 硬编码的 if-else 逻辑造成脆弱性
- **过于模糊**: 没有具体信号的高级指导
- **最优区**: 提供强启发式——足够具体以指导行为，足够灵活以泛化

### 三种长视野技术

1. **压缩 (Compaction)**
   - 接近上下文限制时总结对话，然后用摘要重新开始
   - Claude Code 保留架构决策、未解决的 Bug 和实现细节，丢弃冗余工具输出
   - Agent 用压缩上下文加最近访问的 5 个文件继续
   - 最佳实践：先最大化摘要中的召回率，然后迭代提高精确度

2. **结构化笔记 (Structured Note-taking)**
   - Agent 定期将笔记持久化到外部记忆
   - 示例：Claude 玩 Pokémon 时，Agent 在数千步中维护精确计数
   - 文件记忆工具已作为 Sonnet 4.5 发布的一部分公开测试

3. **子 Agent 架构 (Sub-agent Architectures)**
   - 将专门子 Agent 分配给具有干净上下文窗口的聚焦任务
   - 每个子 Agent 内部可能使用数万 token，但只返回 1,000-2,000 token 的浓缩摘要给编排者
   - [How We Built Our Multi-Agent Research System](how-we-built-our-multi-agent-research-system.md) 是这一架构的生产级实现——子 Agent 返回压缩发现，LeadResearcher 综合结果

### 即时上下文检索 (Just-in-time Context Retrieval)
- 推荐默认方式，而非预加载
- Agent 维护轻量级标识符（文件路径、存储查询、Web 链接），运行时动态加载数据
- Claude Code 使用 CLAUDE.md 文件预先加载 + glob/grep 即时导航——混合策略。[Claude Code Best Practices](claude-code-best-practices.md) 详细描述了 CLAUDE.md 的配置方式
- [Equipping Agents for the Real World with Agent Skills](equipping-agents-for-the-real-world-with-agent-skills.md) 的渐进式披露是即时检索的另一种实现——Skill 元数据始终加载，完整 SKILL.md 按需加载
- [Introducing Contextual Retrieval](introducing-contextual-retrieval.md) 提供了检索优化的具体技术——Contextual Embeddings + BM25 + 重排序可将检索失败率降低 67%

## 实践建议

- 使用 XML 标签或 Markdown 标题将提示组织为不同部分
- 策划多样化、规范的少量示例而非边缘案例清单——"示例是值千言的'图片'"
- 工具应自包含、对错误健壮、对预期用途极其清晰
- 从最佳模型的最小提示开始测试，然后根据失败模式添加指令
- **"做最简单有效的事"仍然是最好的建议**
