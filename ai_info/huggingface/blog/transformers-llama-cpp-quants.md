# transformers 原生运行 llama.cpp 量化（Run llama.cpp Quantizations Natively in transformers）

- **原文链接**: [Run llama.cpp Quantizations Natively in transformers](https://huggingface.co/blog/transformers-llama-cpp-quants)
- **作者**: Hugging Face transformers 团队
- **发布日期**: 2026-09-22
- **检索日期**: 2026-09-29
- **标签**: #GGUF #量化 #本地推理 #AppleSilicon #transformers

## 核心观点

transformers 现在支持指定 gguf_file 后直接 from_pretrained 加载 GGUF 检查点，加载后的一切都是标准 transformers API，也可用 transformers serve 暴露 OpenAI 兼容端点。性能不靠模拟：经 kernels 库复用 ggml 的 Metal 内核——ggml-quantization 直接读取打包态量化权重、ggml-norm 融合归一化计算，权重以打包态驻留 Metal；M2 Max 上三个检查点实测吞吐接近 llama.cpp。

首阶段范围是 Apple Silicon + Qwen3.5，从 Q4_K_M 起步（4B 检查点 2.74GB，对比 BF16 的 8.42GB）。定位清晰：在 Python/PyTorch 生态内对 GGUF 做实验、评估、转换与反量化微调；追求极致推理性能仍应选 llama.cpp。长期愿景是把 ggml 内核带给更多新架构。

## 关键发现 / 关键技术

### 1. gguf_file 加载路径

- from_pretrained 指定 gguf_file 即可加载 GGUF，之后 generate、pipeline、chat template 全部按标准 transformers API 工作。
- transformers serve 直接把该模型暴露为 OpenAI 兼容端点，无需额外服务框架。
- GGUF 与 safetensors 检查点可在同一套代码里互换，便于对照评估与格式转换。

### 2. kernels 库复用 ggml 内核

- 性能路径是把 ggml 的 Metal 内核包装进 kernels 库：ggml-quantization 在打包态直接执行矩阵运算，无需反量化展开。
- ggml-norm 把归一化算子融合，减少 kernel launch 次数与内存往返。
- 权重始终保持打包态驻留 Metal，避免 unpack 带来的内存峰值与带宽损失。

### 3. 实测与内存收益

- M2 Max 上三个 Qwen3.5 检查点吞吐接近原生 llama.cpp，差距已小到不影响实验结论。
- 内存收益直接：4B Q4_K_M 为 2.74GB，BF16 为 8.42GB，约降至三分之一。
- 首阶段从 Q4_K_M 起步，覆盖最常用的社区量化档位。
- 后续量化档位与架构支持按同一 kernels 复用模式扩展，不依赖 llama.cpp 的 Python 绑定。

### 4. 定位边界与愿景

- 明确边界：这是 GGUF 进入 PyTorch 生态的通道，不是 llama.cpp 的替代品；极致推理仍推 llama.cpp。
- 目标用户：想在 Python/PyTorch 生态内对 GGUF 做实验、评估、转换、反量化微调（再量化发布）的团队。
- 愿景：把 ggml 内核带给更多新架构，让 transformers 用户在官方支持滞后期也能跑量化检查点。

## 实践意义

对已有 transformers 评测/训练管线的团队，GGUF 不再是二等公民：可直接把社区量化检查点拉进评估套件，或反量化后 LoRA 微调再重新量化发布，工作流不离开 Python。对量化方法研究者，这打通了"量化检查点→标准基准评估"的最短路径。与 oMLX 同日公告合看，HF 正把本地 AI 的两大格式（GGUF/MLX）都纳入一线支持。

## 跨厂商对比

- 与 [oMLX 创建者加入 Hugging Face](omlx-joins-hf.md) 互补：同周两则公告共构 GGUF（transformers 原生）与 MLX（oMLX 全职维护）双线本地 AI 战略。
- 与 [Native Speed: vLLM 与 transformers 后端](native-speed-vllm-transformers-backend.md) 对比：一个解决服务端大规模吞吐，一个解决本地单机量化推理，覆盖推理谱系两端。
- 与 [WebGPU Kernels](webgpu-kernels.md) 互补：同为"复用成熟内核生态进 PyTorch 系"的路径。

## 资源

- 论文：N/A
- 代码：[huggingface/transformers](https://github.com/huggingface/transformers)、[huggingface/kernels](https://github.com/huggingface/kernels)
- Demo：[发布文内 M2 Max 实测与加载示例](https://huggingface.co/blog/transformers-llama-cpp-quants)
