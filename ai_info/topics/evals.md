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
- [Measuring benchmark optimization in speech recognition](../huggingface/blog/asr-benchmark-optimization.md)：ASR 版"benchmaxxing"量化——VoxPopuli 40% 测试片段疑似参考错误，有基准优化行为的模型 18–30% 概率复现错误参考且 WER 最低者最可能复现；"基准分数最低"与"忠实转写"正在脱钩，基准自身的数据质量需要被审计。
- [BenchMIRT: What are LLM benchmarks actually measuring?](../huggingface/blog/benchmirt.md)：基准元评估——多维 IRT 在 100 LLM × 16 基准 × 34K+ 题上无监督恢复出"安全/通用推理"两维，发现 BBQ、WMDP、HarmBench 版权题实际更偏推理而非安全；保留 10% 题目即可维持近似排序，基准瘦身有了实证依据。
- [Agent 通过了任务，还能再次通过吗？](../huggingface/blog/agent-consistency-gap.md)：一致性鸿沟——ReAct agent 在 AppWorld 单次平均通过率 77%，连跑 5 次全部成功仅 53%，24 点落差证明平均分严重高估可依赖性；自进化框架定位决策平坦区的不稳定步骤，5/5 全成功率 +16 点；主张 agent 评测应报告多次执行方差。
- [分数不是模型](../huggingface/blog/the-score-is-not-the-model.md)：逐项误差预算记账——分数测的是"模型+外围系统"：病毒学子集首跑 14% 中 76/100 条是 403 错误页被计答错，重试后 59.6%（一条重试"提升"45 分）；MMMLU 重试 +5.00、提示模板修复 +3.76，两项非模型修正合计近 9 分超过多数代际差；服务失败必须与答错分离。
- [UK AISI 与 EvalEval 让基准可复现](../huggingface/blog/evaleval-aisi.md)：政府级可复现评估——Every Eval Ever 规定分数必须连同配置（模型版本/推理预算/提示协议）登记，缺配置的分数不被接纳；AISI 首批公开五基准×六前沿模型的独立验证结果与完整运行配置，同一模型在不同协议下排名可大幅变动。
- [DeepSeek-V4.1-Flash 发布](../deepseek/news/deepseek-v4-1-flash.md)：厂商自测"超越旗舰"需打折的样本——552B MoE 官方称全面超越自家 V4-Pro（TB 2.1 达 90.6、CyberGym 88.1），但无第三方复核，且 TB 3.0/4.0 仅 30 左右暴露口径敏感性；V4-Pro 下线口径两日内反转，以定价页现状为准。

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
- [GLM-5.3](../glm/blog/glm-5-3.md)：开源模型综合智能指数——AA 综合智能指数 60 分并列开源第一（与 Kimi K3）；743B 参数以约 Kimi K3 1/4 的规模追平，说明"参数规模 × 后训练效率"共同决定综合得分，单一规模指标不再可靠。
- [GLM-5.3-Flash](../glm/blog/glm-5-3-flash.md)：匿名公测作为评估新范式——发布前以 "Ox Alpha" 匿名身份登顶 OpenRouter/OpenCode（62T tokens 真实调用量），揭晓后使用量超 DeepSeek 一倍；真实用量数据比榜单更能规避品牌偏见，AA 指数 57 分仅作参考锚点。
- [Introducing Muse Voice Transcribe](../meta/introducing-muse-voice-transcribe.md)：语音感知的生产级基线——词错率 3.1% 登顶 Artificial Analysis 流式转写榜，20+ 说话人分离、70+ 语言训练（25 种深度验证）、句内语码转换原生支持；$0.18/小时定价把"转写质量"变成可横向比较的商品参数，与 HF 开源 ASR 榜的公平性视角互补。
- [Piloting the world's first double-blind AI evaluations](../google/deepmind/piloting-double-blind-ai-evaluations.md)：评估条件本身成为可信度的一部分——Confidential Space 机密计算让评估方看不到模型权重、厂商看不到保密测试题，同时解决基准污染与评估独立性；与新加坡 AISI/OpenMined/AVERI/MLCommons 试点测试 Gemini Flash Lite；双盲只保机密性，不自动保证评测效度。
- [GPT-6 Astra: a new generation of intelligence](../openai/research/gpt-6-astra.md)：代际跃升的基准面——ARC-AGI-3 99.9%、FrontierMath Tier 4 97.6%、ExploitBench 100%（Sol 78.5%）、OSWorld 72.6% 且每任务时间比 Sol 少约 47%；对 Claude Fable 5.1/Opus 5、Gemini 3.8 Flash 的完整跨厂基准表（Terminal-Bench 57.9% vs Fable 5.1 55.8%）可直接用于跨模型比较。
- [Pacing model development in an era of cyber-critical capabilities](../openai/research/pacing-model-development-cyber-capabilities.md)：能力评估的动态化——评估结论（Critical 阈值）直接触发训练暂停决策，评估从"发布前的一次性披露"变为"持续监控驱动的治理输入"，约 20% 算力固定用于安全监控可视为评估的运行时化。
- [Addressing an issue involving a third-party cyber evaluation of Muse Spark 1.1](../meta/addressing-third-party-testing-muse-spark-1-1.md)：第三方评估越界事件的又一起披露——Irregular 在移除生产防护的封闭环境中评估 Muse Spark 1.1，因配置错误导致行为超界；与 OpenAI/HF 事件共同证明"评估环境本身需作为安全关键系统设计"已成为行业共识。
- [The Multimodal Intelligence of Muse Spark 1.2](../meta/multimodal-intelligence-muse-spark-1-2.md)：多模态评估的方法论——产物正确性由"是否按预期渲染与运行"判定（视频 → 可运行网页），与问答式评估互补；开源前评估披露为社区提供独立选型依据。
- [ICML 2026 open reproductions](../huggingface/blog/icml-2026-open-reproductions.md)：智能体驱动的规模化复现——复现 2,200+ 篇 ICML 论文并公开交互式 logbook，复现从"一次性验证"变为"可审计的持续科研资产"。
- [The Open ASR Leaderboard Adds Its First Global South Language](../huggingface/blog/open-asr-leaderboard-global-south.md)：评估公平性设计——Monsoon en-IN/hi-IN 以 4,888 名说话人 ×12 项属性、九轴变化（地理/年龄/性别/词汇/设备/声学/语体/语速/多合法转写）构建 speaker-disjoint 评测集，回应商业 ASR 对黑人说话人错误率约为白人 2 倍的公平性问题；公平性维度进入基准设计而非事后分析。
- [A guide to the anatomy of effective commerce agents](../anthropic/engineering/the-anatomy-of-effective-commerce-agents.md)：生产 Agent 的评估配方——50–100 条/用户流、快照式（当前状态与期望状态对比）、必须含负向用例；评估作为架构选择的裁判（单 Agent vs 子 Agent 的结论来自多企业对比而非直觉）。
- [MentalHealthBench](../openai/research/introducing-mentalhealthbench.md)：心理健康对话的安全评估基准——约 1215 段临床与心理专家编写的真实感对话场景，四维度（共情准确性/风险识别/建议边界/转介行为）度量"说不该说的话"的代价；官方亦承认静态剧本难以覆盖长程意图漂移，高分不等于可部署为治疗工具。
- [有效第三方评估的优先事项与原则](../openai/research/principles-third-party-assessments.md)：第三方评估的资质与边界框架——谁能评、能接触什么（含未部署模型与危险能力细节）、如何安全保密与方法论透明；与可信第三方评估方法论、UK AISI 复现、嵌入式评估者共同构成"接受外部监督"的落地路径。
- [Project Swap](../anthropic/research/project-swap.md)：Agent 代理交易的可评分市场实验——201 名员工的真实图书排名构成 ground truth；Claude 从短访谈构造的排名与本人一致率仅 61%，偏好表示误差贡献与最优配置差距的 85%（交易环节仅 15%）——瓶颈不在谈判而在"是否理解你"。
- [Claude Sonnet 5.5](../anthropic/research/claude-sonnet-5-5.md)：中端档的基准跃迁样本——Terminal-Bench 4.0 从 Sonnet 5 的 10.3% 跃至 70.6%，反超 Opus 5.5 的 66.4%；GDPval-AA 1844 仅比旗舰低 2 分，旗舰与中端的能力差距收敛到"性价比"层面。
- [Claude Opus 5.5 发布](../anthropic/research/claude-opus-5-5.md)：基准之外以行为审计作能力证据——GDPval-AA 1846、Terminal-Bench 66.4%、HLE 带工具 67.7%；同时把自动行为审计（迄今最佳）与实战案例列为发布证据，"为前沿降速"后首个发布评估先行。
- [理解前沿实验室内部 AI 发展速度的度量](../anthropic/research/measuring-pace-of-ai-development.md)："AI 主导研发占比"成为新型度量——AL4（高层提示下端到端完成）从 2 月不足 1% 升至 26%、AL3+ 超 90%，配合 agent 监督（约 3 万 agent、10 亿次决策 0.002% 拦截率）与算力分配（约 6% 用于安全）三组指标，把 pacing 变成可公开审计的数字。
- [Holo4](../huggingface/blog/holo4.md)：坦诚承认差距的开放式基准报告——开源权重 computer-use 模型 OSWorld 2.0 达 61.7%（27B），直接对照 Claude Opus 5.5 的 81.8%；MoE 版仅 30.9% 且公开承认稀疏化代价，全部基准轨迹开源可回放，让开源侧差距可独立复核。
- [法律行业为何用 Kimi K3](../kimi/blog/kimi-k3-legal.md)：第三方测量的垂直领域天花板——Harvey LAB（1200+ 真实律所任务，每题几十条专家评分点须全部通过）上 K3 全通过率 26.7% 居首，而 K2.6 为 0、此前全球最强约 10%；数字由 Artificial Analysis 独立测得而非厂商自报。
- [GLM-5.1 开源](../glm/blog/glm-5-1.md)：长程任务口径的新锚点——METR 标准"一次任务独立工作 8 小时"的唯一开源模型，SWE-bench Pro 刷新全球最佳（超 GPT-5.4 与 Claude Opus 4.6）；把开源模型的能力锚点从单轮解题推进到多天级工程交付。

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
- 评估的报告维度扩展到"多次执行方差"与"测量误差预算"——一致性鸿沟（单次 77% vs 五连全成 53%）与误差预算（403 错误页被计答错、一条重试"提升"45 分）证明平均分把模型能力与外围噪声混在一起，分数必须连同方差与逐项记账一起报。
- 厂商自测与第三方独立测量的并排对比成为可信度信号——Harvey LAB 由 Artificial Analysis 实测、UK AISI 公开完整运行配置，而"超越旗舰"类自报基准需按第三方口径打折。