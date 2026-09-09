# NeoMME：高效的多模态原生多语言编码器（NeoMME: an efficient Multimodal-native and Multilingual Encoder）

- **原文链接**: [NeoMME: an efficient Multimodal-native and Multilingual Encoder](https://huggingface.co/blog/Hcompany/neomme)
- **作者**: H Company（Tony Wu、Aurélien Lac）
- **发布日期**: 2026-09-03
- **检索日期**: 2026-09-09
- **标签**: #多模态编码器 #视觉文档检索 #多语言 #晚交互 #RAG

## 核心观点

H Company 发布 NeoMME（260M/800M）多语言多模态编码器：不用预训练 vision tower，也不用因果 LLM decoder，而是用一个双向 Transformer 从头同时处理文本 token 与 32×32 图像 patch，以掩码离散扩散目标预训练。针对检索、分类等非自回归生成任务，它去掉了 VLM 架构的参数与算力冗余。

在 ColPali 页面图像方法论上微调出 NeoMME-Retriever，一次前向同时输出 dense 与 late-interaction 两种嵌入；两个尺寸都落在 ViDoRe v3 的"模型大小-nDCG@10"Pareto 前沿。配合层级 token 池化与不对称量化，晚交互索引可从约 1.5 MB/页压到 6 kB/页且保留 95% 以上质量，模型以 Apache 2.0 开源。

## 关键发现 / 关键技术

### 1. 单一 Transformer 的多模态原生骨干
- 文本用因式分解 token 嵌入，图像切为不重叠的 32×32 patch 经小 MLP 投影，进入同一编码器；动态分辨率保持宽高比，信息密集的页面自动获得更多 token。
- 16,384 token 上下文（约两张 4K 图）；多数层用对称滑动窗口注意力，每六层与末层用全局注意力；131k BPE 多语言词表；从零预训练约 524B packed tokens（其中 290B 纯文本）。
- 多模态样本用 0.3–1 的高掩码率迫使模型依赖可见图像证据重建文本，消除纯语言捷径。

### 2. 检索性能与吞吐
- ViDoRe v3 nDCG@10：260M-Retriever 达 0.523，为 800M 以下最高分，与 ColQwen2.5（3.75B）差距仅 0.002 而参数少约 14×；800M 达 0.556，与同量级 Vultron Flash（0.565）差 0.009；800M 还以 3.6× 更少参数超过 ColPali v1.3。
- NVIDIA L40S 上 2048×2048 输入，260M 每秒编码约 51 页，约为 ColModernVBERT 的 2 倍吞吐。

### 3. 晚交互索引的实用化压缩
- 一张 2048×2048 页面产生 4,200 个向量（float32 约 2.1 MB），ViDoRe v3 实测平均约 1.5 MB/页。
- 层级 token 池化因子 10 + int8：39 kB/页（39× 压缩），保留 >99% nDCG@10；更激进的池化 8 + int8 查询 + binary 文档：6 kB/页（255×），保留 >95%。

## 实践意义

视觉文档检索（对页面截图直接检索、绕过 OCR）正从"改造 VLM"转向"原生多模态编码器"。NeoMME 证明小模型 + 压缩索引可在单卡上支撑生产级 Visual RAG；dense 与 late-interaction 双头一次前向输出，让"ANN 粗排 + 晚交互精排"可共用同一模型，索引存储不再是大范围部署的瓶颈。

## 跨厂商对比

- 与 [Sentence Transformers v6.0 的 MultiVectorEncoder：多向量（Late Interaction）检索模型](multi-vector-encoder.md) 对比：两者都主打多向量/晚交互检索，但 NeoMME 完全去掉预训练视觉塔、从零训练单一多模态 Transformer，并给出索引压缩的完整工程方案。
- 与 [mDenseOn 与 mLateOn：开源多语言长上下文代码检索模型](mdenseon-mlateon-retrieval-models.md) 互补：后者聚焦多语言文本的稠密 + 晚交互检索，NeoMME 把同类能力扩展到页面图像等多模态输入。

## 资源

- 论文：[arXiv:2609.01657](https://arxiv.org/abs/2609.01657)
- 代码：[NeoMME 模型合集](https://hf.co/collections/Hcompany/neomme)（260M/800M 及 Retriever 版，Apache 2.0）
- Demo：[neomme-retriever-demo](https://huggingface.co/spaces/tonywu71/neomme-retriever-demo)
