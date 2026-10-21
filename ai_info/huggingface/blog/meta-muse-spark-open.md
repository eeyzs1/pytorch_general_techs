# 欢迎 Muse Spark Open：Meta 的开源权重前沿多模态 MoE 模型（Welcome Muse Spark Open: open-weight frontier multimodal mixture-of-experts model from Meta）

- **原文链接**: [Welcome Muse Spark Open: open-weight frontier multimodal mixture-of-experts model from Meta](https://huggingface.co/blog/meta-muse-spark-open)
- **作者**: Pedro Cuenca、merve、ben burtenshaw、Guarin Flück、Quentin Gallouédec、Alvaro Bartolome 等（Hugging Face 团队）
- **发布日期**: 2026-10-15
- **检索日期**: 2026-10-16
- **标签**: #开源权重 #MoE #多模态 #Agent编码 #Meta

## 核心观点

Meta 的 Muse Spark Open 登陆 HF：约 816B 总参数、每 token 激活约 42B 的 MoE，输入文本/图像/音频/视频、输出文本，上下文至 1M token，HF 团队称之为"迄今最强的美国开源权重模型"。定位 agentic 编码：在真实开发者工作流（多文件重构、长调试会话）上训练，能读代码库、写调代码、调工具，边干活边看截图、听语音备注、看屏幕录像。

架构细节全部公开：62 层、隐藏维 8192、128 查询头/16 KV 头（GQA）+ QK-norm + 可学习残差门；每层 MoE 块 256 专家选 8（专家承载约 97% 参数）；1.8B 感知编码器（14×14 patch，承 Meta Perception Encoder 工作）处理图像与视频帧；音频编码器为卷积金字塔（80ms 一 token，12.5 token/s）。BF16 权重约 1.5TB safetensors，另有面向 Blackwell 的 NVFP4 版（单 B200 节点可跑；BF16 需 4 节点 8×H200、TP=32）。

## 关键发现 / 关键技术

### 1. 推理生态 day-0 全支持

- transformers 提供 MuseSparkForConditionalGeneration 与 Processor；llama.cpp、vLLM、SGLang、MLX 同日适配；Inference Endpoints 一键部署；TRL 微调方案随文给出。

### 2. 长上下文的真实成本

- 1M token 上下文里图像、视频、音频 token 与文本共用同一窗口；GQA 把每 token KV 缓存压到约 250KB，但满 1M 上下文仍需约 266GB（BF16）——长上下文是显存游戏，规划部署时须按此算账。

### 3. 与 Muse 家族的连续性

- 与 8 月的 Muse Glimmer（30B dense，本地友好）同 tokenizer 同词表，聊天模板向下兼容并扩展新模态；输入嵌入与输出层分离（各约 1.66B）。

### 4. HF 侧演示

- 官方演示包括 3D 资产生成器、用 OpenEnv + HF Sandbox 做浏览器交互、以及"打电话给你的浏览器"——都建立在其 agentic 编码能力上。

## 实践意义

开源权重阵营第一次有了 800B 级、原生多模态、1M 上下文的美国模型，agentic 编码工作流可以直接微调而非从头蒸馏。NVFP4 单节点部署路径让"前沿开源"的硬件门槛从集群降到一台 B200 机器。对 Meta，这是把分发权交给 HF 生态换取采用规模的又一次复制（Muse Glimmer 同款打法）。

## 跨厂商对比

- 与 [Muse Glimmer 登陆 HF](muse-glimmer-hf.md) 对比：Glimmer 是 30B dense 本地模型，Spark Open 是 816B-A42B MoE 前沿模型——Meta 的开源策略明显是"dense 保本地、MoE 争前沿"的双梯队。
- 与 [Meta 官方 Muse Spark Open 发布](../../meta/muse-spark-open.md) 互补：Meta 侧讲模型与产品定位，HF 侧补齐架构、部署配方与生态适配细节，两篇对照阅读可得全貌。
- 与 [Thinking Machines Inkling](thinkingmachines-inkling.md) 对比：Inkling（975B-A41B）与 Spark Open（816B-A42B）几乎同规格同路线——开源前沿的"万亿 MoE 竞赛"已有多家下注，HF 成为共同分发主场。

## 资源

- 论文：[Perception Encoder（arXiv 2504.13181）](https://huggingface.co/papers/2504.13181)
- 代码：[Meta Muse Spark Open 模型合集（Hugging Face）](https://huggingface.co/collections/meta-models/muse-spark-open)
- Demo：[HF 官方发布文与演示合集](https://huggingface.co/blog/meta-muse-spark-open)
