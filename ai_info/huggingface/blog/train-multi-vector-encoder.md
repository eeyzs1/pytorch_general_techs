# 用 Sentence Transformers 训练与微调多向量 Embedding 模型（Training and Finetuning Multi-Vector Embedding Models with Sentence Transformers）

- **原文链接**: [Training and Finetuning Multi-Vector Embedding Models with Sentence Transformers](https://huggingface.co/blog/train-multi-vector-encoder)
- **作者**: Tom Aarsen（Hugging Face，Sentence Transformers 维护者）
- **发布日期**: 2026-08-26
- **检索日期**: 2026-09-09
- **标签**: #SentenceTransformers #多向量检索 #ColBERT #微调 #LateInteraction #RAG

## 核心观点

Sentence Transformers v6.0 引入第四种模型类型 MultiVectorEncoder（ColBERT 风格 late interaction）及配套完整训练方案。本文是"使用篇"multi-vector-encoder 的官方续作，讲训练侧：模型、数据集、损失函数、训练参数、评估器与 Trainer 六大组件，`pip install -U "sentence-transformers[train]"` 即可复现。

核心实证：作者微调出的 multi-vector-encoder/mLateOn-medical，在单张 RTX 3090 上训练 14.5 小时，在 MIRIAD 医学检索评测上轻松超过其能找到的所有通用检索模型——dense、sparse、lexical、multi-vector 皆然，且体积只有最强通用模型的一小部分。

两个反直觉发现：通用检索 checkpoint 普遍按短文档配置（经典 ColBERT 截断 180/300 token、dense 常见 256/512），在平均 941 token 的医学段落上截断损失最高达 0.24 NDCG@10，超过任何架构差异；做领域适配时，未经监督微调的 -unsupervised checkpoint 远优于"成品"checkpoint。

## 关键发现 / 关键技术

### 1. 起点选择：-unsupervised checkpoint 最优
六个起点、同一配方、25k 医学问句-段落对、1,000 留出问题、50k 段落语料的对照实验（NDCG@10 零样本 → 微调后）：
- lightonai/mLateOn-unsupervised：0.9087 → 0.9398（+0.0311，最佳）
- lightonai/mLateOn：0.9277 → 0.9319（+0.0042）
- lightonai/LateOn-unsupervised：0.9026 → 0.9206（+0.0180）
- lightonai/LateOn：0.9185 → 0.9105（−0.0080）
- lightonai/GTE-ModernColBERT-v1：0.9198 → 0.9007（−0.0191）
- gte-modernbert-base + 全新随机 projection head：— → 0.9177

结论在两个模型家族复现：成品 checkpoint 在所有尝试的学习率下几乎不动甚至退化；处于"大规模对比预训练后、通用监督微调前"的 pre-supervised checkpoint 才是领域适配最佳起点。没有此类 checkpoint 时，强检索预训练 backbone + 全新 projection 是紧随其后的选择（与现有 checkpoint 差距 0.03 以内，仅需 25k 训练对）。

### 2. 长文档与索引技巧
- 解除 query/document 长度上限，让截断回落到 tokenizer 的 model_max_length（mLateOn 家族已服务主干完整 8192 token 上下文）
- 标点 skiplist：在"无/标点/停用词/两者"四组消融中质量微胜，并免费把文档索引缩小 9.6%
- 经典 ColBERT 技巧默认关闭且可配置；[MASK] 查询扩展在四种配置下均无可测差异，无需照搬

### 3. 单卡 14.5 小时登顶
- mLateOn-medical：RTX 3090 × 14.5 小时，以远小于最强通用模型的活跃参数量在 MIRIAD 上取得最高 NDCG@10
- LightOn 用同样路径为代码检索训练了 LateOn-Code——医疗、法律、金融、企业内部文档都等不来官方模型，数小时单卡即可自建

## 实践意义

对 RAG 与检索团队：领域多向量模型进入"消费级 GPU 数小时"时代，选择正确的起点（pre-supervised checkpoint）比选架构更重要；长文档场景务必先检查 checkpoint 的截断配置。配套的 Dataset/Loss/Evaluator/Trainer 组件与多数据集训练让整条微调管线留在 sentence-transformers 一个生态内。

## 跨厂商对比

- 与 [MultiVectorEncoder 使用篇](multi-vector-encoder.md) 互补：官方前后篇——前者讲加载、编码与向量数据库索引，本文讲训练与微调，合起来构成 v6.0 多向量能力的完整文档
- 与 [LightOn mDenseOn/mLateOn](mdenseon-mlateon-retrieval-models.md) 对比：mLateOn 家族既是本文实验的最佳起点（-unsupervised checkpoint + 8192 长文档），也是本文方法训练出的 mLateOn-medical 的底座，模型发布与训练框架互为印证

## 资源

- 论文：N/A
- 代码：https://github.com/huggingface/sentence-transformers
- Demo：https://huggingface.co/multi-vector-encoder/mLateOn-medical（微调出的医学检索模型）
