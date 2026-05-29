# 评估与回归阅读路线

## 先读

- [Demystifying Evals for AI Agents](../anthropic/engineering/demystifying-evals-for-ai-agents.md)：Agent 评估术语、评分器、能力评估与回归评估。
- [Introducing AgentKit](../openai/research/introducing-agentkit.md)：可视化设计、版本控制和内联评估。

## 可靠性与对抗性

- [Quantifying Infrastructure Noise in Agentic Coding Evals](../anthropic/engineering/quantifying-infrastructure-noise-in-agentic-coding-evals.md)：基础设施噪声对评估结果的影响。
- [Designing AI-Resistant Technical Evaluations](../anthropic/engineering/designing-ai-resistant-technical-evaluations.md)：技术评估如何对抗模型能力提升。
- [Eval Awareness in Claude Opus 4.6's BrowseComp Performance](../anthropic/engineering/eval-awareness-browsecomp.md)：模型评估感知带来的完整性问题。
- [An OpenAI Model Has Disproved a Central Conjecture in Discrete Geometry](../openai/research/model-disproves-discrete-geometry-conjecture.md)：前沿研究成果如何成为深度推理能力的高信号案例。

## 关键结论

- 评估要分成能力评估和回归评估，二者服务不同决策。
- Agent 评估不仅看最终答案，还要看环境状态、工具调用和完整 transcript。
- 基础设施配置会显著影响分数，评估环境本身需要版本化和监控。
