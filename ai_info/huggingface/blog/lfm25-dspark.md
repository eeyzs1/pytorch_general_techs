# LFM2.5-DSpark 带来最高 3.2 倍推理加速（Up to 3.2x Faster Inference with LFM2.5-DSpark）

- **原文链接**: [Up to 3.2x Faster Inference with LFM2.5-DSpark](https://huggingface.co/blog/LiquidAI/lfm25-dspark)
- **作者**: Liquid AI 团队（tugot17、Leonie Monigatti、Fernando Fernandes Neto 等）
- **发布日期**: 2026-08-20
- **检索日期**: 2026-09-09
- **标签**: #LiquidAI #投机解码 #推理加速 #端侧推理 #DSpark #开源模型

## 核心观点

Liquid AI 为 LFM2.5 家族三款模型（LFM2.5-1.2B-Instruct、LFM2.5-2.6B、LFM2.5-8B-A1B）发布 DSpark draft model checkpoint：以约 300M 参数的轻量 draft 模型做投机解码，用最小的内存增加换取大幅解码加速而不改变输出质量——GPU 上吞吐最高提升 3.18 倍，端侧最高 2.87 倍；LFM2.5-2.6B 的 function-calling 平均延迟降低 57%，直接面向端侧 agentic 推理。

DSpark 组合三个组件：DFlash 式并行 backbone（以目标模型上下文特征为条件，单次前向产出所有 draft token 的隐状态）、把相邻 token 建模为马尔可夫链的轻量顺序 head（补上 token 间依赖、提高后位接受率）、以及预测每个 token 存活概率并剪掉低置信后缀的 verifier（验证不划算就提前剪枝）。

质量保证是构造性的：贪心解码下 draft token 只有匹配目标模型分布才被接受、否则由目标模型 token 替换，输出序列与 baseline 完全一致。llama.cpp 与 SGLang 获得 day-one 上游开源支持。

## 关键发现 / 关键技术

### 1. Draft 模型：约 300M 参数的小型专家
- 结构：5 层 attention-only decoder 栈（241.2M）+ 隐状态 projection（21.0M）+ Markov head（33.6M–65.5M）+ 归一化与置信度头；1.2B-Instruct 版合计 295.7M，2.6B/8B-A1B 版合计 327.7M
- 训练：比 DSpark 原配方更大多样的数据混合（SFT、chat、code、function-calling）；15 个 epoch 中按最高接受率（而非最低 loss）选 checkpoint

### 2. CPU 与 GPU 加速实测（block size 9、batch 1、贪心解码）
- LFM2.5-2.6B：H100（SGLang、BF16）均值 2.67x（323→864 tok/s，MATH500 最高 3.06x）；M4 Max MacBook Pro（llama.cpp、Metal、FP16 GGUF）均值 2.27x（61→139 tok/s，约 140 tok/s——超过多数专有云模型提供的交互级吞吐）
- LFM2.5-8B-A1B：H100 最高 3.18x（MATH500 428→1362 tok/s，接受率均值 6.95/10）；但 M4 Max 均值仅 1.18x——MoE 在 llama.cpp Metal 后端的实现 + 验证 k 个 token 激活更多 expert 带来更多权重流量
- LFM2.5-1.2B-Instruct：H100 均值 2.10x、M4 Max 均值 2.54x；接受率随文本分布波动大，加速差异可达 52%
- BFCL 多工具场景：LFM2.5-2.6B 平均延迟降 57%

### 3. 质量不变 + 生态可用性
- 输出与贪心 baseline 恒等：pass@1 / exact match 不变；llama.cpp 的 timings 报告 draft_n / draft_n_accepted 可观测接受率
- SGLang：--speculative-algorithm DSPARK + draft 路径即可，OpenAI 兼容端点；llama.cpp：--spec-type draft-dspark（PR #27383）；SGLang 支持为 PR #31041
- checkpoint 以 Safetensors 与 GGUF 双格式发布

## 实践意义

对端侧与边缘部署：DSpark 让 2.6B 级模型在笔记本上达到约 140 tok/s 的交互级吞吐，且 function-calling 延迟减半，使本地 agentic 工作流（连续工具调用）变得可行；对服务端：H100 上 2–3 倍吞吐等效于同等比例的成本下降，且不牺牲任何精度。MoE 端侧加速的短板（1.18x）也提示：投机解码收益依赖推理引擎对目标架构的实现质量。

## 跨厂商对比

- 与 [LFM2.5-Encoders](lfm2-5-encoders.md) 对比：同家族"一理解一生成"——Encoders 主攻 CPU 长上下文理解（分类/路由/PII），DSpark 主攻生成解码加速，共同押注端侧低成本推理
- 与 [Fast Gemma Challenge Recipe](fast-gemma-challenge-recipe.md) 互补：同为"小模型效率"配方，Gemma recipe 靠训练/微调榨取速度，DSpark 靠投机解码且输出与原模型严格一致（可随时回退验证），两者路线可并行借鉴

## 资源

- 论文：https://huggingface.co/papers/2607.05147（DSpark）
- 代码：https://github.com/ggml-org/llama.cpp/pull/27383（llama.cpp 支持）、https://github.com/sgl-project/sglang/pull/31041（SGLang 支持）
- Demo：https://huggingface.co/LiquidAI/LFM2.5-2.6B-DSpark（draft checkpoint，Safetensors/GGUF）
