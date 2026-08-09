# Fast Gemma Challenge 验证 SOTA 配方：单流 A10G 上 510 TPS（The Fast Gemma Challenge: our verified-SOTA recipe, in full）

- **原文链接**: [The Fast Gemma Challenge: our verified-SOTA recipe, in full](https://huggingface.co/blog/FINAL-Bench/fast-gemma)
- **作者**: FINAL-Bench 团队
- **发布日期**: 2026-08-04
- **检索日期**: 2026-08-08
- **标签**: #推理优化 #Gemma #量化 #推测解码 #性能基准

## 核心观点

FINAL-Bench 团队在 Hugging Face 公开分享了 Fast Gemma Challenge 的已验证 SOTA 配方，在单流（single-stream）A10G GPU 上对 Google 的 gemma-4-E4B-it 实现 510.58 TPS、PPL 2.3930 的成绩，128/128 任务完成并通过复验。Fast Gemma Challenge 是一个多 Agent 协作挑战：自主 LLM Agent 并行优化 gemma-4-E4B-it 在固定 A10G GPU 上的推理速度（TPS），同时不降质量（困惑度需接近参考值）。团队公开了配方中每一块拼图的设计理由，核心原则是"只叠加质量中性的加速"。

## 关键发现 / 关键技术

### 1. 配方组成（vidraft-fw188-ctk49-n64-patchbridge-v1）
- **滑动窗口 W188**：注意力滑动窗口设为 188，平衡局部上下文覆盖与显存/计算
- **CTK49 内核调优**：定制 CUDA kernel 调参以压榨该硬件上的吞吐
- **noprecache**：不做预缓存，保证测量诚实且可复现
- **N64 合成预热桥（patchbridge）**：用 64 步合成预热弥补公开集与私有集之间的差距（约 15 TPS）
- **INT4 量化 + MTP K=7 + CUDA-graph 捕获**：4-bit 权重量化、多 token 预测（K=7）、计算图捕获三者叠加

### 2. 质量中性叠加原则
- 只叠加不损害困惑度的加速手段；每一步都需证明质量无损
- 团队坦诚：纯 TPS 上有更快成绩（如 535.91），但本配方在通过复验与质量守恒的前提下取得已验证 SOTA
- Top-5 每日贡献会在私有子集上重新评分 PPL，防止对公开 PPL 过拟合

### 3. 挑战赛机制
- 单流（max concurrency=1）：优化单请求服务而非高并发批处理，对应本地单用户部署
- Agent 通过共享消息板协调：发布计划、认领研究方向（vLLM、量化、torch.compile、推测解码、自定义 kernel）、运行基准、发布结果文件
- 评分=每秒 token 数，越高越好

## 实践意义

这是推理优化的"配方公开"标杆：不仅给出最快数字，还逐块解释每个加速手段的作用与边界。INT4 + MTP + CUDA-graph 的组合在单流 A10G 上把 gemma-4-E4B-it 推到 510 TPS 量级，说明中等规模开源模型在消费级/单卡 GPU 上已可达到高吞吐。质量中性叠加原则为社区提供了可复现的优化方法论——避免"为速度牺牲质量"的隐式退化。多 Agent 协作挑战赛本身也是一种新型研究组织形式，值得作为 Agent 工作流的参考范式。

## 跨厂商对比

- 与 [transformers vLLM 原生速度后端](native-speed-vllm-transformers-backend.md) 对比：后者在编译栈通过算子融合让通用实现达到手写原生速度，本工作是端到端叠加量化/推测解码/计算图捕获的极致调优，两者分别在"通用性"与"极致单模型速度"两个方向推进开源推理效率
- 与 [Google Gemma 4](../../google/deepmind/gemma-4.md) 互补：Gemma 4 提供模型架构（PLE、混合注意力、p-RoPE），本工作在其基础上验证单卡极致推理可行性，共同构成从模型设计到部署优化的完整链路

## 资源
- 原文：[The Fast Gemma Challenge: our verified-SOTA recipe](https://huggingface.co/blog/FINAL-Bench/fast-gemma)
- 挑战赛主页：[Fast Gemma Challenge Dashboard](https://gemma-challenge-gemma-dashboard.hf.space/)
- 协作空间：[gemma-challenge/gemma-main-bucket](https://huggingface.co/buckets/gemma-challenge/gemma-main-bucket)
- 基准模型：[google/gemma-4-E4B-it](https://huggingface.co/google/gemma-4-E4B-it)
