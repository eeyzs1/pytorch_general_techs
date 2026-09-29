# GPT-Rosalind 发布：面向生命科学的前沿推理模型（Introducing GPT-Rosalind）

- **原文链接**: [Introducing GPT-Rosalind](https://openai.com/index/introducing-gpt-rosalind/)
- **作者**: OpenAI(官方博客,署名未核实——原文经第三方转载交叉验证)
- **发布日期**: 2026-04-16
- **检索日期**: 2026-09-29
- **标签**: #GPT-Rosalind #生命科学 #药物发现 #TrustedAccess #Codex #前沿推理模型

## 核心观点

OpenAI 发布 GPT-Rosalind：首个面向生命科学的前沿推理模型，继 GPT-5.4-Cyber（网络安全）之后的第二款领域专用前沿模型，以 Rosalind Franklin 命名。定位药物发现早期环节——文献综合、假设生成、实验设计与数据分析；背景是美国新药研发平均 10-15 年、临床淘汰率约 90%。

能力证据主要来自外部：与 Dyno Therapeutics 用未发表 RNA 序列做无污染评测，best-of-10 序列→功能预测超 57 位专家的第 95 百分位、序列生成超 84% 的专家；BixBench Pass@1 达 0.751，领先 GPT-5.4（0.740）、Grok 4.2（0.728）、Gemini 3.1 Pro（0.550）。模型以研究预览上线 ChatGPT/Codex/API，仅限可信访问计划的美国企业客户。

## 关键发现 / 关键技术

### 1. 领域定位与命名
- 首个生命科学前沿推理模型；继 GPT-5.4-Cyber 之后，OpenAI 领域专用前沿模型系列的第二款。
- 以 Rosalind Franklin 命名——其 DNA 晶体学成像正是双螺旋结构发现的关键证据。
- 聚焦药物发现早期：文献综合、假设生成、实验设计、数据分析。
- 行业痛点：美国新药研发平均 10-15 年、临床阶段淘汰率约 90%。

### 2. Dyno Therapeutics 无污染评测
- 评测使用从未发表的 RNA 序列，排除训练数据污染嫌疑。
- best-of-10 序列→功能预测：超过 57 位人类专家的第 95 百分位。
- 序列生成任务：超过 84% 的专家。

### 3. 公开与内部基准

| 基准 | GPT-Rosalind | 对照 |
|------|------|------|
| BixBench Pass@1 | 0.751 | GPT-5.4 0.740 / Grok 4.2 0.728 / Gemini 3.1 Pro 0.550 |
| LABBench2 | 11 项子任务中 6 项胜出 | vs GPT-5.4 |
| 内部化学基准 | ~0.66 | GPT-5.4 ~0.55 |
| 内部实验设计基准 | ~0.65 | GPT-5.4 ~0.32 |
| 内部科学工具基准 | ~0.58 | GPT-5.4 ~0.41 |

### 4. 可信访问与发布形态
- 研究预览上线 ChatGPT、Codex 与 API 三个入口。
- 仅限可信访问计划（Trusted Access）的美国企业客户，预览期不消耗 API 额度。
- Trusted Access 三大支柱：有益使用、治理与安全监督、受控访问。

### 5. 生态与市场反应
- 免费 Codex Life Sciences 插件：GitHub 开源，接入 50+ 科学数据库。
- 首批合作伙伴：Amgen、Moderna、Thermo Fisher、Allen Institute。
- 发布当日 IQVIA 股价下跌 2%——市场将 AI 药物研发视为对 CRO/医药信息服务的替代信号。

## 实践意义

1. **领域专用前沿模型成为新发布范式**：继 GPT-5.4-Cyber 后第二例，"通用旗舰 + 领域专用"双轨路线对全行业有参考价值。
2. **无污染评测方法论可复用**：与 Dyno 以未发表数据评测，为生物 AI 能力声明提供了防污染的评测模板。
3. **Trusted Access 是高风险能力部署模板**：有益使用 + 治理监督 + 受控访问，而非简单的开放或封闭。
4. **插件化降低落地门槛**：50+ 数据库的开源插件把模型接入真实科研工作流，而非停留在问答层面。
5. **市场外溢效应显现**：IQVIA 单日 -2% 说明 AI for Science 已开始重定价医药产业链。

## 跨厂商对比

- 与 [Strengthening Societal Resilience with Rosalind Biodefense](strengthening-societal-resilience-with-rosalind-biodefense.md) 构成三部曲：本文（2026-04 发布）→ 该文（2026-05 生物防御与政府扩展）→ 能力更新（2026-06），展示"发布—扩展—深化"的领域模型运营节奏。
- 与 [Introducing New Capabilities to GPT-Rosalind](introducing-new-capabilities-to-gpt-rosalind.md) 对比：发布时的 BixBench/LABBench2 评测在 2026-06 更新中被 LifeSciBench/MedChemBench/GeneBench 等端到端工作流评测接续，评测体系从单点准确率走向工作流。
- 与 [Paving the Way for Agents in Biology](../../anthropic/research/agents-in-biology.md) 对比：Anthropic 认为生物 Agent 的瓶颈在确定性数据基础设施而非模型推理（VirBench 加确定性检索层后从 ~91.3% 升至接近 100%）；OpenAI 则以领域专用模型 + 50+ 数据库插件双管齐下，两条路线互补。
- 与 [Making Claude a Chemist](../../anthropic/research/making-claude-a-chemist.md) 对比：Anthropic 用通用模型验证"通用够用"（Opus 4.7 无化学微调即匹敌专用软件），OpenAI 选择"领域更强"的专用前沿模型——同一问题的两种回答。
- 与 [Co-Scientist](../../google/deepmind/co-scientist.md) 对比：DeepMind 走多代理"想法锦标赛"架构并经 Nature 论文验证；GPT-Rosalind 走单模型 + 工具插件 + Trusted Access 商业化路线，三家对"AI 加速科学发现"给出不同答案。

## 资源

- 官方博客：[Introducing GPT-Rosalind](https://openai.com/index/introducing-gpt-rosalind/)
- 代码：Codex Life Sciences 插件（GitHub 开源，接入 50+ 数据库，仓库地址见官方博客）
- 相关条目：[Introducing New Capabilities to GPT-Rosalind](introducing-new-capabilities-to-gpt-rosalind.md)、[Strengthening Societal Resilience with Rosalind Biodefense](strengthening-societal-resilience-with-rosalind-biodefense.md)

> 注:openai.com 原文 403,本文基于多源转载交叉验证(Axios/habr/Gigazine/Lifeboat 等),官方 URL 已列于资源。
