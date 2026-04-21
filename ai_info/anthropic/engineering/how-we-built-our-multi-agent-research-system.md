# How We Built Our Multi-Agent Research System

- **原文链接**: [How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system)
- **作者**: Jeremy Hadfield, Barry Zhang, Kenneth Lien, Florian Scholz, Jeremy Fox, Daniel Ford
- **发布日期**: 2025-06-13
- **标签**: #多Agent #研究系统 #编排者-工作者 #并行工具调用 #评估

## 核心观点

Anthropic 为 Claude 的 Research 功能构建了生产级多 Agent 系统，可搜索网页、Google Workspace 和集成服务。Lead Agent 协调过程，生成专门的子 Agent 并行工作。该系统在研究任务上比单 Agent 方法提升了 **90.2%**。Token 使用量单独解释了 80% 的性能差异。

## 架构设计

采用 [Building Effective Agents](building-effective-agents.md) 中定义的编排者-工作者（Orchestrator-Worker）模式：

1. 用户提交查询 → LeadResearcher Agent (Claude Opus 4) 分析并制定策略
2. LeadResearcher 将计划保存到 Memory（上下文窗口外的持久化）。这种持久化策略是 [Effective Context Engineering for AI Agents](effective-context-engineering-for-ai-agents.md) 中"结构化笔记"技术的生产实现
3. LeadResearcher 生成子 Agent (Claude Sonnet 4)，分配具体研究任务
4. 每个子 Agent 独立执行：搜索 → 用交错思维评估结果 → 返回压缩发现。子 Agent 只返回 1,000-2,000 token 的浓缩摘要，是 [Effective Context Engineering for AI Agents](effective-context-engineering-for-ai-agents.md) 中"子 Agent 架构"的实践
5. LeadResearcher 综合结果，必要时生成额外子 Agent
6. 所有发现传递给 CitationAgent 进行来源验证
7. 返回带引用的最终研究

## 关键指标

- 比单 Agent 提升 **90.2%**（Opus 4 主导 + Sonnet 4 子 Agent vs 单个 Opus 4）
- **80%** 的 BrowseComp 性能差异可由 Token 使用量解释
- **95%** 可由三个因素解释：Token 使用量、工具调用次数、模型选择
- 从 Sonnet 3.7 升级到 Sonnet 4 的收益大于将 3.7 的 Token 预算翻倍
- 并行工具调用将复杂查询的研究时间减少 **90%**。并行工具调用的技术实现参见 [Advanced Tool Use](advanced-tool-use.md)

## 8 条提示工程原则

1. **像你的 Agent 一样思考**: 用 Console 模拟精确提示和工具，逐步观察 Agent 行为
2. **教编排者如何委派**: 每个子 Agent 需要：目标、输出格式、工具/来源指导、清晰任务边界
3. **按查询复杂度缩放工作量**: 简单查询 1 Agent 3-10 工具调用；直接比较 2-4 子 Agent；复杂研究 10+ 子 Agent
4. **工具设计和选择至关重要**: 先检查所有可用工具，匹配用户意图。[Writing Effective Tools for AI Agents](writing-effective-tools-for-ai-agents.md) 提供了系统化的工具设计方法论
5. **让 Agent 自我改进**: 工具测试 Agent 反复使用有缺陷的工具后重写描述，未来 Agent 任务完成时间降低 40%
6. **先宽后窄**: Agent 默认查询过于具体冗长，应从短宽查询开始，逐步缩小
7. **引导思考过程**: Extended Thinking 作为可控草稿本；子 Agent 用交错思维评估质量
8. **并行工具调用变革速度**: 主 Agent 同时启动 3-5 子 Agent；每个子 Agent 同时使用 3+ 工具

## 评估方法

- 从约 20 个代表真实使用的查询开始
- LLM-as-judge 评分 0.0-1.0：事实准确性、引用准确性、完整性、来源质量、工具效率。更完整的评估框架参见 [Demystifying Evals for AI Agents](demystifying-evals-for-ai-agents.md)
- 人类评估发现：早期 Agent 持续选择 SEO 优化的内容农场而非权威来源

## 生产挑战

- **有状态错误处理**: 失败时无法重启（太昂贵）；让模型适应工具失败，结合确定性保障
- **彩虹部署**: 渐进版本过渡
- **非确定性调试**: 需要完整生产追踪
