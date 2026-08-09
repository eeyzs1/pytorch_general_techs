# 原生速度：transformers vLLM 建模后端（Native-speed vLLM transformers modeling backend）

- **原文链接**: [Native-speed vLLM transformers modeling backend](https://huggingface.co/blog/native-speed-vllm-transformers-backend)
- **作者**: Harry Mellor、Lysandre（Hugging Face）
- **发布日期**: 2026-07-08
- **检索日期**: 2026-08-01
- **标签**: #推理优化 #vLLM #transformers #torch.fx #模型服务

## 核心观点

transformers 作为 ML 参考建模库支持 450+ 架构，但其代码此前在 vLLM 中只能拿到"接近"原生的推理速度，极致性能仍需手写 vLLM 专用实现。本文宣布 transformers vLLM 建模后端的最新迭代：通过对模型图做静态分析并在运行时动态施加推理专用算子融合，使 transformers 实现在 vLLM 中达到或超过手写原生实现的速度，模型作者一次集成到 transformers 即可自动获得 vLLM 极致推理性能，无需再写一行优化代码。

在三组差异很大的 Qwen3 模型（4B dense、32B tensor-parallel、235B FP8 MoE data+expert parallel）上，transformers 后端的吞吐"meet or beat"原生实现。一条 `--model-impl transformers` 标志即可启用，并与常用并行选项组合。

## 关键发现 / 关键技术

### 1. torch.fx 图分析与 AST 改写
- 用 `torch.fx` 对模型图做静态分析，搜索已知可优化模式；再用 AST（抽象语法树）原地改写源码部分操作。
- 产出多对一映射到 vLLM 超优化 kernel 的融合算子，如 MoE 专家并行（EP）所需的融合，以及 `MergedColumnParallelLinear` 与 `QKVParallelLinear`——后者使 TP/PP 并行计划可被推断。

### 2. 仍可编译、可训练
- 改写后的模型仍能通过 `torch.compile` 与 CUDA Graphs，与专用 vLLM 实现一致。
- 关键区别：transformers 实现可同时用于训练/评估/RL rollout，而 vLLM 专用实现只能用于推理——同一份模型代码可贯穿训练与推理。

### 3. 基准方法与限制
- 三条件对比：native（`--model-impl vllm` 手写实现）、after（带 PR 的 transformers）、before（不带 PR 的 transformers），提供可复现 benchmark.sh gist。
- 当前限制：使用线性注意力的模型暂不支持（即将支持）；代码存在于 Hub repo 的自定义模型因合规性问题大概率不可用。

## 实践意义

这把"为 transformers 写一次实现"真正变成了"训练/推理统一入口"：新模型集成到 transformers 后无需再为 vLLM 单独移植即可获得原生级吞吐，显著降低模型作者的维护成本与首日部署延迟。对部署侧，这意味着升级 vLLM 即可继承优化，而不必等待社区补齐每个新架构的手写端口。它也巩固了 transformers 作为生态"模型定义库"的中心地位。

## 跨厂商对比

- 与 [OpenAI 推进价格性能前沿](../../openai/research/advancing-the-price-performance-frontier-with-gpt-5-6.md) 对比：OpenAI 在闭源栈内压榨前沿模型性价比，本工作在开源栈内通过编译期融合把通用实现拉到手写实现的水平，是开源侧推理效率的基础设施进展。
- 与 [OpenAI Jalapeno 推理芯片](../../openai/research/openai-broadcom-jalapeno-inference-chip.md) 互补：Jalapeno 是硬件层加速，transformers-vLLM 后端是软件层算子融合，两者分别从硬件与编译栈缩小通用实现与专用实现的性能差距。

## 资源

- 基准脚本：[benchmark.sh gist](https://huggingface.co/datasets/ariG23498/useful-scripts/blob/main/transformers-backend-vllm-benchmark.sh)
- transformers 模型定义：[Transformers model definition](https://huggingface.co/blog/transformers-model-definition#a-model-definition-library)
- vLLM transformers 后端：[vLLM 2025-04-11 blog](https://vllm.ai/blog/2025-04-11-transformers-backend)
- Torch FX 文档：[https://docs.pytorch.org/docs/2.12/fx.html](https://docs.pytorch.org/docs/2.12/fx.html)
