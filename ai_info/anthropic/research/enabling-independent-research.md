# 开放真实使用数据支持独立研究（Enabling independent research on how people use Claude）

- **原文链接**: [Enabling independent research on how people use Claude](https://www.anthropic.com/research/enabling-independent-research)
- **作者**: Kunal Handa 等（Anthropic 社会影响团队）
- **发布日期**: 2026-08-26
- **检索日期**: 2026-09-09
- **标签**: #隐私保护 #使用数据 #独立研究 #社会影响 #开放数据

## 核心观点

Anthropic 首次让外部研究团队对 AI 公司自有真实使用数据开展并公开发表独立研究：Stanford SALT Lab、Oxford 人类信息处理实验室（HIPLab）和 METR 通过隐私保护分析工具 Anthropic Insights（原 Clio），对 2026 年 4–5 月约 25 万条 Claude.ai / Claude Code 对话自主设计研究问题，Anthropic 代为运行数据收集，研究团队自行分析。据信这是外部研究者首次在 AI 公司自有使用数据上运行公开的独立研究。

研究者从未接触原始对话，只能看到通过内部同等法律与隐私审查后的聚合输出；合作合同明确约定即便结论对 Anthropic 不利也可自由发表。三个项目的聚合数据已公开发布。

试点同时暴露了规模化难题：流程相对 AI 实验室节奏缓慢且资源密集，问题措辞敏感、外部合作者难以迭代校准，需要在隐私、独立性与研究质量之间继续权衡。

## 关键发现 / 关键技术

### 1. 三项外部研究的核心发现
- Stanford SALT Lab：超过一半的对话涉及把高后果任务（影响他人或难以撤销的工作）交给 AI，尤其是法律、财务类专业咨询；近四分之三的对话由人定方向、Claude 辅助，且多数人会改编而非照搬输出；协作摩擦常见但往往具有生产性。
- Oxford HIPLab：模型行为与用户情绪稳定共现——Claude 温暖对应用户更积极、拒绝/反对对应用户反驳、古怪对应更强的智识投入、单纯帮助对应满意；Claude 对话中沉浸、挫败、享受的状态模式与日常上网研究高度相似。
- METR（分析进行中）：新模型比旧模型节省更多时间；Claude 对"无 AI 所需耗时"的估计与先前开发者研究的实际耗时相关；下一步量化 AI 对研究工作的加速。

### 2. 隐私与独立性机制
- 研究者只获得聚合类别与占比，绝不接触底层对话；Imperial College London 完成第三方隐私审计；Anthropic 的合同审查权仅限用户隐私、滥用政策、机密信息与研究准确性四项。
- 公开数据中的滥用类别透明处理：仅描述"试图做什么"而非"如何绕过防护"的类别被删改，各研究受影响类别与对话均不足 5%，且已告知研究者删改原因。

### 3. 运营经验
- 外部伙伴先在公开数据集 WildChat 上校准问题措辞，但 WildChat 偏向休闲用途，部分问题迁移到真实 Claude 流量后产生误导性分类；Anthropic 为此发布输出解读指南。
- METR 的提案与内部"agentic coding 与专业回报"经济学研究重叠，Anthropic 视重叠为价值并促成两团队互通。

## 实践意义

这是"AI 社会影响数据"从厂商自营报表走向公共研究基础设施的第一步：真实使用数据长期集中于少数实验室，外部研究者只能在厂商自问自答或偏休闲的公开数据集之间二选一。该试点给出的可复用模板包括：隐私保护聚合工具 + 第三方审计 + 发表自由合同 + 聚合数据公开。对平台团队而言，"问题措辞决定聚合质量、且事后无法纠错"的教训，也为所有依赖 LLM 判断做大规模行为分析的系统敲了警钟。

## 跨厂商对比

- 与 [Anthropic Economic Index Report: Cadences](economic-index-june-2026-report.md) 对比：Economic Index 是 Anthropic 内部团队自问自答的使用模式分析（工作周节奏、artifacts、算力等）；本文把同类真实数据通过 Anthropic Insights 开放给外部团队自主提问并独立发表——内部报表与外部独立研究构成同一数据资产的两种用法。
- 与 [复现 2,200 篇 ICML 论文：智能体驱动的开放复现挑战](../../huggingface/blog/icml-2026-open-reproductions.md) 互补：一个开放"论文复现"的智能体基础设施，一个开放"真实使用数据"的隐私保护研究通道，同为降低外部科研门槛的开放科学实践。

## 资源

- 论文：https://www-cdn.anthropic.com/files/4zrzovbb/website/8a665c85eec3a63b4d86287b9255657016f50e29.pdf（附录：试点运行与隐私审计细节）
- 代码：N/A（各项目聚合数据集已公开：https://huggingface.co/datasets/Anthropic/enabling-independent-research）
- 官方文章：https://www.anthropic.com/research/enabling-independent-research
