# LFM2.5-VL-DSPark：视觉语言模型加速（LFM2.5-VL-DSPark: Faster Vision-Language Models via Speculative Decoding）

- **原文链接**: [LFM2.5-VL-DSPark](https://huggingface.co/blog/LiquidAI/lfm2-5-vl-dspark)
- **作者**: Liquid AI
- **发布日期**: 2026-09-24
- **检索日期**: 2026-09-29
- **标签**: #投机解码 #视觉语言模型 #本地推理 #MLX #llama.cpp

## 核心观点

Liquid AI 为 LFM2.5-VL-3B 发布约 280M 参数的投机解码 drafter，仅增加 8.9% 参数量：4 层 attention-only 栈（193M）+ 隐藏态投影（21M）+ Markov 头（65.5M）。drafter 捕获目标模型 tapped 层隐藏态后一次起草 k 个候选；图像 patch 与文本 token 在此之前已进入共享表示，因此起草算法与文本版 DSpark 完全一致——视觉模型无需重新发明投机解码。

实测 M5 Max（MLX）解码加速 2.30-3.13×、端到端 1.56-2.62×，M3 Ultra（llama.cpp）1.57-2.14×，H100 解码 2.66×。团队同时点出 Amdahl 限制：投机解码只加速 decode，视觉编码与 prefill 不受益。day-1 支持 llama.cpp/MLX-VLM/SGLang，贪心输出与目标模型逐字节一致。

## 关键发现 / 关键技术

### 1. Drafter 架构：280M 的三段式预算

- 总参数约 280M，仅占 3B 目标模型的 8.9%：4 层 attention-only 栈 193M 负责上下文建模，隐藏态投影 21M 对齐目标表示，Markov 头 65.5M 负责一次起草 k 个候选。
- attention-only 设计避开完整 transformer 的 FFN 开销，起草延迟远低于验证成本，保证"接受率换来得不失速"。
- drafter 与目标模型权重独立发布，可按需加载、按需卸载：不需要加速时移除 drafter 即回到原模型。

### 2. 视觉扩展为何能复用文本算法

- 关键洞察：drafter 从目标模型 tapped 层读取隐藏态时，图像 patch 与文本 token 已融合在共享表示中，跨模态信息不需要 drafter 自己重新编码。
- 因此视觉版的起草-验证循环与文本版 DSpark（对应其块 8-9 的算法描述）完全相同，工程实现直接复用。
- 贪心解码下输出与目标模型逐字节一致，不引入新的分布偏移，评测与部署口径不变。

### 3. 跨后端实测

- M5 Max + MLX：解码 2.30-3.13×，端到端 1.56-2.62×。
- M3 Ultra + llama.cpp：1.57-2.14×；H100：解码 2.66×——加速不依赖单一硬件生态。
- 端到端倍数低于解码倍数，原因见下节的 Amdahl 限制，文中如实分列而非只报最好数字。

### 4. Amdahl 限制与 day-1 生态

- 投机解码只加速 decode 阶段；视觉编码与 prefill 完全不受益，端到端收益存在硬上限——团队选择写明而非回避。
- day-1 支持 llama.cpp、MLX-VLM、SGLang 三条推理栈，覆盖本地与云端两类部署。
- 对本地视觉 agent（截图理解、GUI 解析、文档 VQA）是近乎免费的加速：3B 模型 + 8.9% 参数换 1.5-3× 端到端提速。

## 实践意义

对在 Apple Silicon 或单卡 GPU 上跑 VLM 的团队，DSpark drafter 把交互延迟压缩到可感知范围以下，而显存与磁盘代价可控。"从目标模型隐藏态起草"的思路可迁移到其他 VLM：模态融合在目标模型内完成后，投机解码无需感知多模态。其 Amdahl 声明提醒所有加速工作的报告规范——必须分阶段（prefill/decode/视觉编码）报告收益，避免用 decode 加速比冒充整体提速。

## 跨厂商对比

- 与 [LFM2.5-DSPark](lfm25-dspark.md) 对比：文本版 DSpark 的视觉延伸，起草算法与隐藏态接口完全复用，验证了该 drafter 设计的跨模态通用性。
- 与 [WebGPU Kernels](webgpu-kernels.md) 互补：一个从算法侧（草稿-验证）减少解码串行依赖，一个从内核侧提升算子效率，两者可叠加。
- 与 [Native Speed: vLLM 与 transformers 后端](native-speed-vllm-transformers-backend.md) 对比：服务端吞吐优化与单机解码延迟优化是推理效率的两条战线，DSpark 聚焦后者。

## 资源

- 论文：N/A
- 代码：[LiquidAI（Hugging Face 组织页，含 LFM2.5-VL-3B 与 DSpark drafter）](https://huggingface.co/LiquidAI)
- Demo：[发布文内基准表与各后端启动命令](https://huggingface.co/blog/LiquidAI/lfm2-5-vl-dspark)
