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
- [Equipping the Responses API with a Computer Environment](../openai/research/equipping-the-responses-api-with-a-computer-environment.md)：服务端 Compaction + Agent Skills + Shell 工具——OpenAI 把"长上下文"重新设计为"持久化执行环境"。
- [Dreaming: Better Memory for a More Helpful ChatGPT](../openai/research/chatgpt-memory-dreaming.md)：Dreaming V3 主动推理记忆——事实回忆 41.5% → 82.8%，计算成本降低约 5 倍。
- [A Global Workspace in Language Models](../anthropic/research/global-workspace.md)：J-space 是模型内部"特权思维空间"——可被读出、编辑、用于推理；为可解释性与可控干预提供新工具。
- [Claude's Values Across Models and Languages](../anthropic/research/claude-values-models-languages.md)：价值轴方法将 3,000+ 价值观压缩为少量可解释维度，发现跨模型和跨语言的系统性价值观差异——模型"价值观上下文"存在语言偏见。
- [DeepSeek-V4](../deepseek/news/deepseek-v4.md)：百万上下文工程化——CSA 压缩稀疏注意力把 KV cache 压至前代 10%、单 token FLOPs 降至 27%；配套 Engram 条件记忆模块用 O(1) 哈希查找替代神经网络计算，1M 上下文从"技术奇点"变为可承担的工程现实。
- [GLM-5.2](../glm/blog/glm-5-2.md)：1M 无损上下文针对长任务的目标保持与上下文漂移专门优化——国产旗舰把"长上下文不丢目标"作为主战场，长程任务评测达开源 SOTA。
- [GLM-5.3-Flash](../glm/blog/glm-5-3-flash.md)：开源多模态 + 1M 上下文的"经济版"路线——320B-A18B 稀疏激活把长上下文与多模态输入的成本同时压到旗舰的 1/20 折扣价档位，Ox Alpha 匿名公测（62T tokens 调用）证明低价不等于低用量。
- [How GPT-5.6 fuses frontier intelligence with frontier efficiency](../openai/research/gpt-5-6-frontier-intelligence-efficiency.md)：harness 层的上下文工程——延迟发现（集成、MCP 工具、技能仅在需要时呈现，防止上下文膨胀）+ 精确前缀保留（append-only 历史、工具确定性排序，维持高 prompt 缓存命中率）。
- [mDenseOn with the mLateOn: Multilingual Retrieval Models](../huggingface/blog/mdenseon-mlateon-retrieval-models.md)：307M 参数开源多语言检索模型——mLateOn（late-interaction）在 BEIR 得分 57.56 达 SOTA；token 级匹配避免单向量池化过度压缩，泛化到训练中完全未见的语言与文字体系（俄语 +28、中文 +36），为多语言 RAG 管道提供小模型底座。
- [SkillSmith: Learning to Compose Parametric Skills and Textual Knowledge](../google/deepmind/skillsmith.md)：把"技能上下文"沉入权重层——参数化技能（KV-cache 激活）与文本知识在运行时组合，模型无需微调即可按需获得新能力；与文本型技能（SKILL.md 渐进式披露）形成对照：一个把技能放在上下文/文件里，一个把技能放进模型内部表示。
- [Maximizing the value of your Claude Code sessions](../anthropic/engineering/maximizing-value-of-claude-code-sessions.md)：会话级上下文管理——`/clear` 防止无关上下文回流、effort 与模型前置设置保持 prompt cache 命中、`/compact` 在缓存过期前压缩、`@-mention` 直接附加文件内容省 Read 调用；"最小高信号 token 集合"原则的 CLI 落地。
- [Training and Finetuning Multi-Vector Embedding Models with Sentence Transformers](../huggingface/blog/train-multi-vector-encoder.md)：多向量检索的训练方法论——六种起点对照证明二次训练应从原始基座而非成品 checkpoint 出发（unsupervised 起点 +0.0311 NDCG@10 最优）；单张 RTX 3090 训练 14.5 小时可在医学检索领域超越通用检索模型。
- [NeoMME: an efficient Multimodal-native and Multilingual Encoder](../huggingface/blog/neomme.md)：多模态检索的架构瘦身——单一双向 Transformer 从零训练（无 vision tower / LLM decoder），260M 参数在 ViDoRe v3 仅比 <800M 最优低 0.002；池化 + 不对称量化把晚交互索引压 255×（1.5MB→6kB/页），多模态 RAG 的存储成本不再是禁区。
- [How HF Inference Endpoints, Jobs, and Buckets Power Search on Papers with Code](../huggingface/blog/pwc-search.md)：检索基础设施的生产工程——PostgreSQL 全文 + pgvector + 加权 RRF 混合检索 11 万+ 论文，embedding 格式当版本化 API（钉 revision）、离线索引 Jobs 与在线检索 Endpoint 分离、1 秒熔断回退词法检索；RAG 系统的可靠性来自工程分层而非更大模型。
- [Give Your Coding Agents a Memory You Own](../huggingface/blog/funes.md)：跨 Agent 记忆层——为 Claude Code / Codex / pi / Hermes 建共享记忆（Lance 数据集 + 向量/BM25 融合 + cross-encoder 重排），"记忆是数据集不是服务"，同步为用户自有数据集；handoff-vs-recall 基准显示 recall 比 handoff 便宜 8×/4×，compaction 在部分任务上彻底失败。
- [A guide to the anatomy of effective commerce agents](../anthropic/engineering/the-anatomy-of-effective-commerce-agents.md)：商业 Agent 的上下文工程实证——90–99% prompt cache 命中率作为架构设计目标（缓存读 1/10 价格、~100k token 快 1.5–2×）；异步记忆抽取（对话后离线沉淀）比"存事实"工具召回 +13%，记忆写入时机本身是架构决策。
- [Claude's memory works everywhere, and you decide what's in it](../anthropic/engineering/claudes-memory-works-everywhere.md)：记忆跨入口统一与用户主权——聊天与 Cowork 共享同一份记忆并双向流动，Topics 文件可逐条读/改/删；敏感主题三档分级（默认排除 / 显式开启+逐次通知+不回溯 / 永不存储），记忆可见性成为产品一级功能。
- [Healthcare organizations can now connect EHR and additional industry data to ChatGPT](../openai/research/chatgpt-connects-health-records-and-healthcare-sources.md)：可信源接地的医疗上下文——Epic EHR 双向集成 + PubMed/DailyMed/CMS 等 9 个官方源插件，60 国 26 专科医生审查 70 万+ 回复（99.1% 安全评级）；把"模型知识"换成"可溯源数据源"是高风险领域 RAG 的准入条件。

## 长视野任务的上下文延续

- [Codex-Maxxing for Long-Running Work](../openai/research/codex-maxxing-long-running-work.md)：长视野任务的"工作区即上下文"——AGENTS.md / 工作树 / 测试 / 状态作为跨 session 上下文载体。
- [How Agents Are Transforming Work](../openai/research/how-agents-are-transforming-work.md)：99 百分位用户单日 Agent turn 60+ 小时——上下文管理的工程化挑战是真实需求。
- [Building Self-Improving Tax Agents with Codex](../openai/research/building-self-improving-tax-agents-with-codex.md)：生产反馈作为上下文信号源，让 Agent 持续迭代。
- [Agentic Coding and Persistent Returns to Expertise](../anthropic/research/claude-code-expertise.md)：40 万 Claude Code 会话显示，专业规划需要持续上下文（CLAUDE.md + 笔记 + 测试循环）。
- [How enabling two settings tripled our ARC-AGI-3 scores](../openai/research/how-two-settings-tripled-our-arc-agi-3-scores.md)：保留推理 + compaction 替代滚动截断——ARC-AGI-3 得分 13.3% → 38.3% 且输出 token 少 6 倍；"记忆连续性"（推理 + 动作历史）是长时任务性能的第一变量。
- [Muse Code and Muse Spark 1.2](../meta/introducing-muse-code-muse-spark-1-2.md)：持久化后台 Agent 的上下文积累——会话期间持续存活避免重复信息收集；子 Agent 在独立 git worktree 并行工作并自主决定何时反馈；模型与 harness 协同训练把上下文压缩配方直接训进权重。

## 关键结论

- 上下文不是越多越好，目标是最小高信号 token 集合。
- 可持久化的项目规则、任务笔记和评估结果，比一次性长提示更可维护。
- 检索、压缩、Skill、记忆应该分层使用，避免把所有信息一次性塞进上下文。
- 长视野任务需要"工作区即上下文"——文件系统、版本控制、测试结果、AGENTS.md/CLAUDE.md 都是上下文载体。
- 主动推理记忆（Dreaming）比被动存储更有效——模型不只是"读"记忆，还要"整理"记忆。
- 模型内部"价值观上下文"存在语言偏见——非英语语言中情感表达类价值观显著更少，需关注多语言对齐的上下文公平性。
- 长时任务上下文管理的关键是"不丢推理"——保留推理 + 摘要续接（compaction）显著优于滚动截断，已在游戏与编码两个域得到验证。
