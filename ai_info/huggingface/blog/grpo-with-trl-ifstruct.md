# 100 步 GRPO 微调 350M 模型，获得更可靠的结构化输出（Fine-tuning a 350M Model for Better Structured Outputs in 100 GRPO Steps）

- **原文链接**: [Fine-tuning a 350M Model for Better Structured Outputs in 100 GRPO Steps](https://huggingface.co/blog/grpo-with-trl-ifstruct)
- **作者**: Leonie Monigatti、ben burtenshaw、Sergio Paniego（Liquid AI 合作）
- **发布日期**: 2026-09-03
- **检索日期**: 2026-09-09
- **标签**: #GRPO #结构化输出 #TRL #小模型微调 #LLM评测

## 核心观点

这是一份完全公开、近零成本的操作指南：用 TRL 的 GRPO 对 LFM2.5-350M 做任务特定微调，仅约 500 条样本、100 个训练步、一块免费 16GB GPU（Colab/Kaggle 即可），就让 IFStruct 结构化输出基准的通过率从 22.6% 提升到 29.7%。

文章主张：schema 合规（输出有效、可解析、符合请求的格式与形状）往往决定一个小模型能否被接入下游系统，而这恰恰被多数基准折叠进更粗的推理分数。轻量任务特定 RL 可让 350M 模型逼近大模型——微调后的 29.7% 已接近 Qwen3.5-2B 的 33.15%。

## 关键发现 / 关键技术

### 1. 训练配方
- 数据：约 500 条 nvidia Nemotron-RL 结构化输出样本；40% 追加"fenced code block"指令、20% 转为顶层数组任务，弥合与 IFStruct 评测分布的两个缺口。
- LoRA r=16，约 600 万可训练参数（占模型 1.66%）；三个 [0,1] 奖励（json_format、field_count、schema_validation）按 [1.0, 0.5, 2.0] 加权；每 prompt 组 8 个生成，100 步，max_completion_length 1024。
- 评测栈：合并 LoRA 后转 BF16 GGUF，在 MacBook Pro（M5 Max，36GB 统一内存）上用 llama.cpp 起 OpenAI 兼容服务跑满 2000 样本。

### 2. 结果与基准复现
- 同一服务栈下前后对比：总体 22.6% → 29.7%（+7.1）；JSON 18.0% → 31.9%（+13.9）；bare list 16.6% → 29.7%（+13.1）；YAML 仅 27.2% → 27.5%（+0.3）——增益精准落在训练目标（JSON/裸列表）上。
- 本地复现基座得分 22.6%，与 IFStruct 官方博客的 21.1% 接近；平均延迟从 1453ms 到 1518ms，几乎无代价。
- 基座最高频错误是"必填字段缺失"（7228 次），微调后仍是最主要错误但通过率整体上移。

## 实践意义

端侧与边缘部署中"能否稳定吐出合法 JSON/YAML"比通用能力更关键。该配方证明 RL 微调不需要大规模算力：免费 GPU + 数百样本即可显著改善特定输出契约，且 notebook 全公开、可换成任意基座模型，适合需要在本地 GGUF 栈上交付结构化输出的团队直接照搬。

## 跨厂商对比

- 与 [Fast Gemma Challenge 验证 SOTA 配方：单流 A10G 上 510 TPS](fast-gemma-challenge-recipe.md) 对比：两者都是"开源可复现的 TRL/GRPO 配方"，前者瞄准推理吞吐的验证 SOTA，本文瞄准结构化输出契约这一工程刚需，指标与优化对象完全不同。
- 与 [LiquidAI LFM2.5-Encoders：CPU 上的快速长上下文编码器](lfm2-5-encoders.md) 互补：同属 Liquid AI LFM2.5 家族的效率路线，一个做 CPU 友好的理解侧编码器，一个做 GRPO 结构化输出微调，共同面向低成本端侧场景。

## 资源

- 论文：N/A（IFStruct 基准介绍见 [Liquid AI 官方博客](https://www.liquid.ai/blog/ifstruct-v1.0)）
- 代码：[grpo_with_trl_ifstruct.ipynb](https://github.com/Liquid4All/cookbook/blob/main/finetuning/notebooks/grpo_with_trl_ifstruct.ipynb)、[Liquid4All/ifstruct 评测框架](https://github.com/Liquid4All/ifstruct)
- Demo：N/A
