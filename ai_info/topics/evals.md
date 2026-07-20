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
- [Separating Signal from Noise in Coding Evaluations](../openai/research/separating-signal-from-noise-coding-evaluations.md)：SWE-Bench Pro 审计发现 ~30% 任务存在缺陷——任务描述不清、测试用例错误、环境配置缺陷；编码评估可靠性再敲警钟。
- [PerceptionBench](../kimi/blog/perception-bench.md)：从模型失败中"发现"10 种原子视觉感知能力；无模型超过 60% 准确率，大量正确答案无法复现——当前多模态模型经常猜测而非真正感知。
- [DeepSeek-V4](../deepseek/news/deepseek-v4.md)：官方自测 SWE-bench Verified 距 Claude Opus 4.6 Max 仅 0.2pp、价格约 1/7——但需注意这是厂商自测数据，且第三方反馈"相同任务迭代轮数多于 Fable 5"，单次通过率之外的效率指标同样重要。

## 关键结论

- 评估要分成能力评估和回归评估，二者服务不同决策。
- Agent 评估不仅看最终答案，还要看环境状态、工具调用和完整 transcript。
- 基础设施配置会显著影响分数，评估环境本身需要版本化和监控。
- 专家级评估需要专家级基准——通用问答不足以衡量真实科研能力。
- Sandbagging（模型故意压低能力）已正式成为 Preparedness 评估类别。
- 编码评估基准本身需要审计——SWE-Bench Pro ~30% 任务有缺陷，基准分数可能误导能力判断。
- 感知评估需要与推理评估分离——PerceptionBench 显示当前多模态模型在原子感知上表现不佳（<60%），且经常猜测而非真正感知。
- 评估质量标准化是行业迫切需求——从 SWE-Bench Verified 到 SWE-Bench Pro，任务质量问题持续存在。