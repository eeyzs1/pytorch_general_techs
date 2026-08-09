# Thinking Machines 发布 Inkling：原生多模态万亿参数开源模型（Welcome Inkling by Thinking Machines）

- **原文链接**: [Welcome Inkling by Thinking Machines](https://huggingface.co/blog/thinkingmachines-inkling)
- **作者**: ben burtenshaw、merve、Pedro Cuenca、Aritra Roy Gosthipaty、Andres Marafioti（Hugging Face 与 Thinking Machines Lab）
- **发布日期**: 2026-07-15
- **检索日期**: 2026-08-01
- **标签**: #多模态模型 #开源权重 #MoE #长上下文 #模型发布

## 核心观点

Thinking Machines Lab 在 Hugging Face 发布 Inkling——首个约 1T 参数、原生接收图像/文本/音频输入、支持 1M 上下文的开源多模态大模型，在 45 万亿 token 的文本、图像、音频与视频上训练。它是 decoder-only 的多模态 MoE（975B 总参、41B 激活，256 个专家），具备 agentic 能力，提供 BF16 与校准良好的 NVFP4 量化版本，并带推测式 MTP 层加速推理，day-0 支持 transformers、SGLang、vLLM、llama.cpp。

同期发布的 Inkling-Small（276B 总参/12B 激活）把部署门槛降到 8×H200 甚至单卡 Blackwell，并可在 Inference Endpoints 上一键部署达到 140–160 TPS。HF 团队强调它适合构建新一代多模态推理应用，并鼓励通过微调做领域适配。

## 关键发现 / 关键技术

### 1. 区别于主流的架构选择
- **相对注意力**取代 RoPE：每层注意力额外学习一个 per-token/per-head 相对特征 R，与 key-query 距离信息一起注入注意力 logits。
- **混合注意力**：5:1 的 sliding window 与 global attention 交替，末层用 global attention 构建富表征。
- **短卷积 SConv**：在隐藏态上做 1D 卷积混合局部表征，把局部建模从 attention/MoS 中解放出来。
- **MoE + shared expert sink**：Top-6 路由专家 + 2 个常激活共享专家；视觉用层次化 MLP patchifier，音频用离散 mel 频谱图（每 100ms 一块）。

### 2. 部署矩阵与推理生态
- BF16 需 2 TB VRAM（8×B300 或 16×H200）；NVFP4 需 600 GB；Inkling-Small BF16 需 600 GB，NVFP4 仅 180 GB（单卡 B300 或 2×H200 W4A16）。
- 提供 transformers `any-to-any` pipeline、`AutoModelForMultimodalLM`，SGLang/vLLM 一条命令起 OpenAI 兼容服务，llama.cpp + Unsloth 可压到 1-bit（VRAM 降 95%，保留 ~74.2% top-1% 精度）。Inference Providers 释放首日 2 小时免费额度。

### 3. 基准表现与后训练
- 推理：HLE(text) 31.6% / HLE(tools) 47.8% / AIME 2026 95.5% / GPQA Diamond 89.5%；Agentic：SWEBench Verified 80.2%、Terminal Bench 2.1 64.69；视觉 MMMU-Pro 74.0%；音频 VoiceBench 91.4%。
- 后训练用 tinker + OpenEnv agentic RL，采用 ECHO 算法（无 verifier 训练隐式世界模型）；可用 GOLD 算法做知识蒸馏把文档理解能力蒸馏到更小的端侧模型。

## 实践意义

Inkling 把"原生全模态 + 1M 上下文 + agentic + 开源权重"首次推到万亿参数级，且量化与多引擎支持使其在 8×H200 即可落地。对工程实践而言，相对注意力 + 混合滑动窗口 + SConv 的组合是长上下文效率的一条新路径，MTP 推测解码则在不改输出的前提下给生成提速。多模态推理"先转录再推理"的链式行为（OCR→表征→评估→答）也值得在做多模态 vibe eval 时参考。

## 跨厂商对比

- 与 [OpenAI GPT-5.6](../../openai/research/introducing-gpt-5-6.md) 对比：GPT-5.6 是闭源前沿模型，Inkling 以开源权重 + 1M 上下文 + 原生音频输入补齐了开源侧的全模态空白，但 HLE/SimpleQA 等事实性基准仍落后于闭源前沿。
- 与 [Google Gemma 4](../../google/deepmind/gemma-4.md) 对比：同为开源权重，Gemma 走小而精路线，Inkling 走超大规模 MoE + 全模态路线，定位互补。
- 与 [Anthropic Global Workspace](../../anthropic/research/global-workspace.md) 互补：Global Workspace 关注多模态融合的认知架构理论，Inkling 是该方向的大规模工程实现样本。

## 资源

- 模型集合：[thinkingmachines/inkling collection](https://huggingface.co/collections/thinkingmachines/inkling)
- 实时语音图像 Demo：[hf-realtime-voice Space](https://huggingface.co/spaces/HuggingFaceM4/hf-realtime-voice)
- 后训练示例：[OpenEnv echo_world_model](https://github.com/huggingface/OpenEnv/blob/main/examples/echo_world_model/backends/tinker_echo_demo.py)
