# LFM2.5-24B-A2B：在设备上跑快速、私密的 Agent（Run fast, private agents on-device with LFM2.5-24B-A2B）

- **原文链接**: [Run fast, private agents on-device with LFM2.5-24B-A2B](https://huggingface.co/blog/LiquidAI/lfm25-24b-a2b)
- **作者**: Raahul Vignesh、Song Duong、Akhilesh Deepak Gotmare、Fernando Fernandes Neto 等（Liquid AI 团队）
- **发布日期**: 2026-10-13
- **检索日期**: 2026-10-16
- **标签**: #端侧推理 #MoE #Agent模型 #开源权重 #LiquidAI

## 核心观点

Liquid AI 发布 LFM2.5-24B-A2B：24B 总参数、仅 2B 激活的推理模型，为"快、私密、本地"的设备端 Agent 打造，也是 LFM2.5 家族的收官之作——家族至此横跨两个数量级（230M 到 24B）。开放权重（Base 与后训练版均上架 Hub）。

卖点是把 MoE 的"大容量小激活"做到端侧可用：与总参和激活都多约 50% 的 Qwen3.6-35B-A3B 相比，八个 agentic 与工具使用基准中五个有竞争力，LiveClaw 48.09 vs 38.19、AutomationBench 27.69 vs 8.72；速度上比同类 MoE 快至 1.7 倍——Apple M5 Max 184 token/s，单张 B300 最高 21K 输出 token/s。

## 关键发现 / 关键技术

### 1. 端侧 Agent 定位

- 2B 激活让内存带宽成为瓶颈的消费设备也能跑 24B 容量的模型；184 token/s 在笔记本上足以支撑实时工具调用循环。
- LiveClaw / AutomationBench 等 agentic 基准的大幅领先，说明稀疏化没有牺牲其目标场景（工具编排）的能力。

### 2. 家族与生态

- LFM2.5 家族从 230M 到 24B-A2B 全尺寸开放，配套 Playground 与本地运行/微调文档；延续 LiquidAI"混合架构 + 全格式分发"路线（此前 DSpark 投机解码、CPU 编码器均同策略）。

### 3. 隐私主张

- "私密"是第一级卖点：敏感数据不出设备，Agent 场景（邮件、文件、浏览记录）本地闭环。

## 实践意义

端侧 Agent 的"能力/速度"权衡点被再次推高：24B 容量 + 2B 激活 + 184 tok/s 意着本地 Agent 不再只是玩具。对隐私合规行业（医疗、法务、金融），开源权重 + 设备内闭环是比 API 更容易过审的架构。云侧 21K tok/s 的 B300 数字则暗示同一模型可无缝从端侧放大到服务端。

## 跨厂商对比

- 与 [LFM2.5-DSpark](lfm25-dspark.md) 对比：DSpark 用 300M drafter 换 3.18× 推测解码加速，24B-A2B 用 MoE 稀疏激活直接省计算——LiquidAI 在同一"端侧提速"目标下并行押注两条技术路线。
- 与 [transformers 原生运行 llama.cpp 量化](transformers-llama-cpp-quants.md) 互补：后者解决本地部署的格式与内核问题，前者提供为本地而生的模型设计，端侧栈的模型侧与运行时侧同时成熟。
- 与 [oMLX 维护者加入 HF](omlx-joins-hf.md) 对比：HF 吸纳 MLX 维护者巩固 Apple Silicon 本地生态，LiquidAI 持续供给本地模型——"本地 AI"正从社区运动变成平台战略。

## 资源

- 论文：无
- 代码：[LiquidAI/LFM2.5-24B-A2B（Hugging Face）](https://huggingface.co/LiquidAI/LFM2.5-24B-A2B)
- Demo：[Liquid AI Playground](https://playground.liquid.ai/chat?model=LFM2.5-24B-A2B)
