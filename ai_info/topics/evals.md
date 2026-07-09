# 评估与回归阅读路线

## 先读

- [Demystifying Evals for AI Agents](../anthropic/engineering/demystifying-evals-for-ai-agents.md)：Agent 评估术语、评分器、能力评估与回归评估。
- [Introducing AgentKit](../openai/research/introducing-agentkit.md)：可视化设计、版本控制和内联评估。

## 可靠性与对抗性

- [Quantifying Infrastructure Noise in Agentic Coding Evals](../anthropic/engineering/quantifying-infrastructure-noise-in-agentic-coding-evals.md)：基础设施噪声对评估结果的影响。
- [Designing AI-Resistant Technical Evaluations](../anthropic/engineering/designing-ai-resistant-technical-evaluations.md)：技术评估如何对抗模型能力提升。
- [Eval Awareness in Claude Opus 4.6's BrowseComp Performance](../anthropic/engineering/eval-awareness-browsecomp.md)：模型评估感知带来的完整性问题。
- [An OpenAI Model Has Disproved a Central Conjecture in Discrete Geometry](../openai/research/model-disproves-discrete-geometry-conjecture.md)：前沿研究成果如何成为深度推理能力的高信号案例。

## 专家级与系统级评估

- [Introducing LifeSciBench](../openai/research/introducing-life-sci-bench.md)：750 任务、19,020 rubric 准则的生命科学专家级基准；173 名 Ph.D. 撰写 + 453 名独立审查；79% 任务多步推理、53% 需 artifact。
- [Introducing GeneBench-Pro](../openai/research/introducing-genebench-pro.md)：129 道合成计算生物学问题，覆盖 10 领域 / 21 子领域，专注于"研究品味"（模糊数据 + 迭代实验 + 判断决策）；GPT-5.6 Sol（Pro）通过率 31.5%，单题人类专家需 20-40 小时。
- [A Shared Playbook for Trustworthy Third Party Evaluations](../openai/research/trustworthy-third-party-evaluations-foundations.md)：第三方评估的方法论与质量保障。
- [GPT-5.6 Preview System Card](../openai/research/gpt-5-6-preview-system-card.md)：Disallowed Content / Robustness / CoT / Metagaming / Preparedness 多维评估范式；Sandbagging 新增类别。

## 关键结论

- 评估要分成能力评估和回归评估，二者服务不同决策。
- Agent 评估不仅看最终答案，还要看环境状态、工具调用和完整 transcript。
- 基础设施配置会显著影响分数，评估环境本身需要版本化和监控。
- 专家级评估需要专家级基准——通用问答不足以衡量真实科研能力。
- Sandbagging（模型故意压低能力）已正式成为 Preparedness 评估类别。