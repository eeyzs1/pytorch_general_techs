# mDenseOn 与 mLateOn：开源多语言长上下文代码检索模型（mDenseOn with the mLateOn: Open Multilingual, Long-Context, and Code Retrieval Models）

- **原文链接**: [mDenseOn with the mLateOn: Open Multilingual, Long-Context, and Code Retrieval Models](https://huggingface.co/blog/lightonai/mdenseon-mlateon)
- **作者**: LightOn 团队
- **发布日期**: 2026-07-30
- **检索日期**: 2026-08-08
- **标签**: #检索模型 #多语言 #ColBERT #RAG #开源

## 核心观点

LightOn 发布 mDenseOn 与 mLateOn——两款 307M 参数的开源多语言检索模型，在英文通用检索（BEIR）、长文档检索（MLDR）、多语言检索（MIRACL）与代码检索（MTEB Code）四条基准上达到 SOTA。模型基于此前验证过的英文 DenseOn/LateOn 配方，通过 translate-train 扩展到 9 种自然语言加代码，构建了 28 亿对的多语言语料（迄今最大的开源多语言/跨语言检索训练集之一）。最引人注目的发现是：late-interaction 模型（mLateOn）能泛化到检索训练中完全未见的语言与文字体系，有效消除了 translate-train 配合 dense 模型的主要局限。模型、数据集与训练代码全部开源。

## 关键发现 / 关键技术

### 1. 双模型设计：dense 与 late-interaction
- mDenseOn（dense，单向量池化）与 mLateOn（late-interaction，token 级匹配）共享主干、训练数据与目标，唯一差异是文档表示方式
- mLateOn 在 BEIR 得分 57.56，超越所有对比基线（含两倍体量的模型）；MLDR 训练语言 87.69、全基准 77.92，为任意体量模型中最优
- MIRACL 上目标语言得分最佳；代码检索与最优模型差距在 3 分以内

### 2. 28 亿对多语言语料与训练方法
- 基于英文 DenseOn/LateOn 配方，通过 translate-train 扩展到 9 语言（英、法、德、西、意、葡、瑞典、挪威、阿拉伯）
- 融合 MIRACL（多语言有机数据）、MLDR（长文档）、LateOn-Code 微调数据（代码）
- 微调数据集 1630 万样本，覆盖 9 种自然语言与代码

### 3. 跨语言泛化的关键证据
- 在 MLDR 上，dense 模型在未见语言上崩溃，mLateOn 仍能工作：俄语 +28、中文 +36、印地语 +35、泰语 +29（nDCG@10 提升幅度）
- 在完整 MIRACL（含 13 种未见语言）上，mLateOn 平均分反而高于仅在训练语言上的得分
- 结论：token 级匹配避免了单向量池化的过度压缩，使模型泛化到训练分布之外的语言与文字

## 实践意义

late-interaction 模型此前已在 out-of-domain、长上下文与推理密集型检索上展现优势，本工作把该优势扩展到多语言与代码检索。对 RAG 与 Agent 检索管道：mLateOn 提供了一个 307M 参数的小模型即可在多语言、长文档、代码三类高频场景同时达 SOTA 的选项，降低了部署成本。对研究社区：开源的 28 亿对语料与训练代码为多语言检索研究提供了大规模基础。跨语言泛化到未见语言的发现尤其重要——它意味着 translate-train 配合 late-interaction 可覆盖长尾语言，缓解了多语言检索的数据稀缺问题。

## 跨厂商对比

- 与 [LFM2.5-Encoders](lfm2-5-encoders.md) 对比：两者都是小体量（<350M）开源编码/检索模型且强调 CPU 友好，但 LFM2.5 定位通用理解（分类/路由/检索多任务），mDenseOn/mLateOn 专攻检索并以 late-interaction 的跨语言泛化为差异化亮点
- 与 [Anthropic Contextual Retrieval](../../anthropic/engineering/introducing-contextual-retrieval.md) 互补：Contextual Retrieval 用 LLM 给检索块加上下文以提升 RAG 召回，本工作从检索器侧提供多语言长文档的精准匹配底座，两者在检索管道的不同环节增效

## 资源
- 模型：[lightonai/mDenseOn](https://huggingface.co/lightonai/mDenseOn)、[lightonai/mLateOn](https://huggingface.co/lightonai/mLateOn)
- 原文：[lighton.ai/lighton-blogs/mdenseon-and-mlateon](https://lighton.ai/lighton-blogs/mdenseon-and-mlateon-more-signal-less-noise-for-multilingual-agentic-search)
- 前作：[DenseOn 与 LateOn](https://huggingface.co/blog/lightonai/denseon-lateon)
