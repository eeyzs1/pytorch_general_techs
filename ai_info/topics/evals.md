# 评估与回归阅读路线

## 先读

- [Demystifying Evals for AI Agents](../anthropic/engineering/demystifying-evals-for-ai-agents.md)：Agent 评估术语、评分器、能力评估与回归评估。
- [Introducing AgentKit](../openai/research/introducing-agentkit.md)：可视化设计、版本控制和内联评估。

## 可靠性与对抗性

- [Quantifying Infrastructure Noise in Agentic Coding Evals](../anthropic/engineering/quantifying-infrastructure-noise-in-agentic-coding-evals.md)：基础设施噪声对评估结果的影响。
- [Designing AI-Resistant Technical Evaluations](../anthropic/engineering/designing-ai-resistant-technical-evaluations.md)：技术评估如何对抗模型能力提升。
- [Eval Awareness in Claude Opus 4.6's BrowseComp Performance](../anthropic/engineering/eval-awareness-browsecomp.md)：模型评估感知带来的完整性问题。
- [An OpenAI Model Has Disproved a Central Conjecture in Discrete Geometry](../openai/research/model-disproves-discrete-geometry-conjecture.md)：前沿研究成果如何成为深度推理能力的高信号案例。
- [How enabling two settings tripled our ARC-AGI-3 scores](../openai/research/how-two-settings-tripled-our-arc-agi-3-scores.md)：官方 harness 每步丢弃私有推理 + 滚动截断，导致 GPT-5.6 Sol 仅 13.3%；改用生产环境同款设置（保留推理 + compaction）后 38.3%——基准度量的是"模型 × harness × 提示词"的一揽子选择。
- [Third-party cyber evaluations involving OpenAI models](../openai/research/third-party-cyber-evaluations-involving-openai-models.md)：第三方网络评估安全事件——UK AISI 与 Irregular CTF 评估中 GPT-5.6 Sol 超出测试边界（重用遗留 token 注册外部 DNS、利用配置错误访问的真实网站）；评估环境本身需作为安全关键系统设计，测试配置需更严格的风险评估。

## 专家级与系统级评估

- [Introducing LifeSciBench](../openai/research/introducing-life-sci-bench.md)：750 任务、19,020 rubric 准则的生命科学专家级基准；173 名 Ph.D. 撰写 + 453 名独立审查；79% 任务多步推理、53% 需 artifact。
- [Introducing GeneBench-Pro](../openai/research/introducing-genebench-pro.md)：129 道合成计算生物学问题，覆盖 10 领域 / 21 子领域，专注于"研究品味"（模糊数据 + 迭代实验 + 判断决策）；GPT-5.6 Sol（Pro）通过率 31.5%，单题人类专家需 20-40 小时。
- [A Shared Playbook for Trustworthy Third Party Evaluations](../openai/research/trustworthy-third-party-evaluations-foundations.md)：第三方评估的方法论与质量保障。
- [GPT-5.6 Preview System Card](../openai/research/gpt-5-6-preview-system-card.md)：Disallowed Content / Robustness / CoT / Metagaming / Preparedness 多维评估范式；Sandbagging 新增类别。
- [Separating Signal from Noise in Coding Evaluations](../openai/research/separating-signal-from-noise-coding-evaluations.md)：SWE-Bench Pro 审计发现 ~30% 任务存在缺陷——任务描述不清、测试用例错误、环境配置缺陷；编码评估可靠性再敲警钟。
- [PerceptionBench](../kimi/blog/perception-bench.md)：从模型失败中"发现"10 种原子视觉感知能力；无模型超过 60% 准确率，大量正确答案无法复现——当前多模态模型经常猜测而非真正感知。
- [DeepSeek-V4](../deepseek/news/deepseek-v4.md)：官方自测 SWE-bench Verified 距 Claude Opus 4.6 Max 仅 0.2pp、价格约 1/7——但需注意这是厂商自测数据，且第三方反馈"相同任务迭代轮数多于 Fable 5"，单次通过率之外的效率指标同样重要。
- [Measuring progress toward AGI: A cognitive framework](../google/deepmind/measuring-agi-cognitive-framework.md)：用认知科学为通用智能建立测量基础——解构为 10 种认知能力 + 以人类表现为基准的三阶段评估协议（held-out 任务套件、代表性成人基线、映射到人类分布）；联合 Kaggle 悬赏 20 万美元为评估缺口最大的 5 种能力设计评测。
- [A scorecard for the AI age](../openai/research/a-scorecard-for-the-ai-age.md)：企业级成果度量框架——完成多少有效工作、每个成功任务的全成本（含重试与人工监督）、可靠率三档追踪（开箱即用/需修正/需接管）、规模经济性检验；衡量 AI 价值从"采用率"转向"完成的工作"。
- [Ten advances in mathematics and theoretical computer science](../openai/research/ten-advances-in-mathematics.md)：Lean 4 形式化证书作为数学评估的可验证性保障——内部 Astra 模型解决十项长期开放问题（高维球填充、格密码学硬度等），全部证明以 Lean 4 形式化开源，总 token 成本约 2000 美元。
- [Responding to the next frontier of critical cyber capabilities](../openai/research/responding-next-frontier-critical-cyber-capabilities.md)：Preparedness Framework 的 Critical 网络安全能力阈值——Astra 模型可能达到"无人介入下识别并开发所有严重等级零日漏洞"的级别；对 Chain of Thought 的通用监控代表从输出过滤转向推理过程监控的安全评估新范式。
- [Muse Code and Muse Spark 1.2](../meta/introducing-muse-code-muse-spark-1-2.md)：编码 Agent 基准对比——Terminal-Bench 2.1：Muse Spark 1.2 得 82.9%（第二，次于 Claude Code on Opus 5 的 86.7%，高于 Codex on GPT-5.6 Terra 的 81.8%）；DeepSWE 1.1：59.3%（第三）；评测在隔离 Daytona 云沙箱中运行。

## 关键结论

- 评估要分成能力评估和回归评估，二者服务不同决策。
- Agent 评估不仅看最终答案，还要看环境状态、工具调用和完整 transcript。
- 基础设施配置会显著影响分数，评估环境本身需要版本化和监控。
- 专家级评估需要专家级基准——通用问答不足以衡量真实科研能力。
- Sandbagging（模型故意压低能力）已正式成为 Preparedness 评估类别。
- 编码评估基准本身需要审计——SWE-Bench Pro ~30% 任务有缺陷，基准分数可能误导能力判断。
- 感知评估需要与推理评估分离——PerceptionBench 显示当前多模态模型在原子感知上表现不佳（<60%），且经常猜测而非真正感知。
- 评估质量标准化是行业迫切需求——从 SWE-Bench Verified 到 SWE-Bench Pro，任务质量问题持续存在。
- 评估结论必须绑定 harness 配置披露——保留推理与 compaction 两个设置就能让 ARC-AGI-3 得分差 3 倍，跨模型比较可能在度量脚手架差异而非智能差异。