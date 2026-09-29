# 像物理学家一样剪枝：Ising 优化（Pruning LLMs Like a Physicist: Block Removal as an Ising Problem）

- **原文链接**: [Pruning LLMs Like a Physicist: Block Removal as an Ising Problem](https://huggingface.co/blog/MultiverseComputingCAI/pruning-llms-like-a-physicist-block-removal-as-an)
- **作者**: Multiverse Computing
- **发布日期**: 2026-09-21
- **检索日期**: 2026-09-29
- **标签**: #模型压缩 #剪枝 #Ising优化 #Hessian #无重训压缩

## 核心观点

Multiverse Computing 把 LLM 整块删除重构为约束二元优化问题，并精确映射到 Ising 玻璃：每个候选删除块对应一个 0/1 自旋变量；损失函数二阶泰勒展开的 Hessian 提供耦合项——对角元是单块重要性，非对角元是"逐块独立打分然后丢弃"式方法完全忽略的块间耦合。

能量函数是基准分数的强廉价代理：一次前向+反向得到 Hessian 后，评估任一候选剪枝配置只需一次能量计算，无需重跑基准。求解可选单 GPU 暴力枚举（Llama-3.3-70B 的 8/80 块组合约 290 亿配置、约两天）或转 QUBO 交给 tabu/量子启发求解器（数秒达到低能态）。结果：Llama-3.3-70B 无重训 50% 深度压缩后 MMLU 76.9，对比 block influence 打分的 54.0（+23 分）。

## 关键发现 / 关键技术

### 1. Ising 玻璃映射

- 每块一个 0/1 变量（删/留），压缩率约束映射为总自旋约束，目标函数来自损失二阶泰勒展开。
- Hessian 对角元 = 单块重要性；非对角元 = 块间耦合——这正是逐块独立打分方法的系统性盲区：删掉 A 块后 B 块的价值会变。
- 删除整块（而非单个神经元/头）保持架构规整，输出模型可直接部署，无需稀疏内核支持。

### 2. 能量作为廉价代理

- Hessian 只需一次前向+反向即可获得；此后每个候选配置只需一次能量计算，比跑基准便宜多个数量级。
- 能量与基准分数呈强相关，因此可作为全局搜索的代理目标，把"评估预算"从搜索瓶颈中解除。
- 这使 70B 级模型的结构搜索在单 GPU 上成为可能。

### 3. 两种求解路线

- 单 GPU 暴力枚举：Llama-3.3-70B 的 8/80 块组合约 290 亿配置，约两天可枚举完——小规模组合空间无需近似算法。
- QUBO 路线：问题转 QUBO 后交给 tabu 或量子启发求解器，数秒达到低能态，适合更大组合空间。
- 两条路线结果一致性好，量子启发求解器在此是"快而够好"的工程选项而非噱头。

### 4. 结果与反直觉发现

- Llama-3.3-70B 无重训删 50% 块：MMLU 76.9 vs block influence 打分的 54.0，提升 +23 分。
- 反直觉：Llama-3.1-8B 的第 17 激发态（能量次优解）经轻度重训后反超基态——低能态未必是对后续训练最友好的配置。
- 方法直接迁移到 Mamba2 + 注意力 + MoE 混合架构，无需针对架构改动；代码开源。
- 物理学工具（Ising 玻璃、激发态）在此不是类比修辞，而是可直接计算的数学对象。

## 实践意义

对需要就地压缩大模型的团队，这把剪枝从启发式打分升级为带耦合项的全局优化，且评估成本被能量代理压到近乎为零：70B 级模型单 GPU 可做。"激发态反超"提示实践上应保留多个低能态候选分别轻训再择优，而非迷信最优解。与量化正交（砍深度 vs 砍位宽），可叠加使用。

## 跨厂商对比

- 与 [Quantization-Aware Healing](quantization-aware-healing.md) 互补：同属"无/轻重训的模型效率"工具箱，量化恢复砍位宽、Ising 剪枝砍深度，二者理论上可串联。
- 与 [State of Open Models: Summer 2026](state-of-open-models-summer-2026.md) 对比：开源权重模型不仅是能力发布，也是此类可复现压缩研究的开放实验素材。
- 与 [Fast Gemma Challenge Recipe](fast-gemma-challenge-recipe.md) 互补：端到端推理优化配方中"把模型变小"的一环，可由结构化剪枝供给。

## 资源

- 论文：N/A（发布文含方法细节）
- 代码：[发布文内开源仓库入口](https://huggingface.co/blog/MultiverseComputingCAI/pruning-llms-like-a-physicist-block-removal-as-an)
- Demo：N/A
