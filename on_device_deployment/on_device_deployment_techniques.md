# 大模型端侧部署（On-Device Deployment）技术全景

## 目录

- [总览](#总览)
- [1 模型压缩（Model Compression）](#1-模型压缩model-compression)
  - [1.1 量化（Quantization）](#11-量化quantization)
  - [1.2 剪枝（Pruning）](#12-剪枝pruning)
  - [1.3 知识蒸馏（Knowledge Distillation）](#13-知识蒸馏knowledge-distillation)
  - [1.4 低秩分解（Low-Rank Factorization）](#14-低秩分解low-rank-factorization)
- [2 高效推理架构（Efficient Inference Architecture）](#2-高效推理架构efficient-inference-architecture)
  - [2.1 KV Cache 优化](#21-kv-cache-优化)
  - [2.2 注意力机制优化](#22-注意力机制优化)
  - [2.3 推理加速策略](#23-推理加速策略)
- [3 高效模型架构设计（Efficient Model Architecture）](#3-高效模型架构设计efficient-model-architecture)
  - [3.1 轻量化架构设计](#31-轻量化架构设计)
  - [3.2 线性注意力与亚二次复杂度架构](#32-线性注意力与亚二次复杂度架构)
  - [3.3 混合专家架构（Mixture of Experts, MoE）](#33-混合专家架构mixture-of-experts-moe)
- [4 编译与运行时优化（Compilation & Runtime Optimization）](#4-编译与运行时优化compilation--runtime-optimization)
  - [4.1 计算图优化](#41-计算图优化)
  - [4.2 针对硬件的代码生成](#42-针对硬件的代码生成)
  - [4.3 内存优化](#43-内存优化)
- [5 硬件适配与部署框架（Hardware Adaptation & Deployment Framework）](#5-硬件适配与部署框架hardware-adaptation--deployment-framework)
  - [5.1 端侧NPU适配](#51-端侧npu适配)
  - [5.2 端侧部署框架](#52-端侧部署框架)
  - [5.3 硬件感知优化](#53-硬件感知优化)
- [6 模型格式与序列化（Model Format & Serialization）](#6-模型格式与序列化model-format--serialization)
- [7 端云协同与系统集成（Edge-Cloud Collaboration & System Integration）](#7-端云协同与系统集成edge-cloud-collaboration--system-integration)
  - [7.1 端云协同推理](#71-端云协同推理)
  - [7.2 多模态端侧部署](#72-多模态端侧部署)
  - [7.3 隐私与安全](#73-隐私与安全)
  - [7.4 端侧推理服务](#74-端侧推理服务)
- [8 端侧训练与个性化（On-Device Training & Personalization）](#8-端侧训练与个性化on-device-training--personalization)
  - [8.1 参数高效微调（PEFT）](#81-参数高效微调peft)
  - [8.2 端侧训练优化](#82-端侧训练优化)
  - [8.3 个性化与持续适应](#83-个性化与持续适应)
- [9 评估指标体系（Evaluation Metrics）](#9-评估指标体系evaluation-metrics)
- [技术选型决策树](#技术选型决策树)
- [总结](#总结)

---

## 总览

大模型端侧部署旨在将大规模语言模型（LLM）及多模态模型高效运行在资源受限的终端设备上（手机、平板、嵌入式设备、车载平台等）。其核心挑战在于：**模型体积大、计算需求高、内存带宽受限、功耗预算严格**。以下从产业级视角，对端侧部署所涉及的全部技术进行系统性分类。

---

## 1 模型压缩（Model Compression）

> **目的**：在可接受的精度损失范围内，显著降低模型的存储体积、计算量和内存占用，使其能够在端侧设备上加载和运行。

### 1.1 量化（Quantization）

> **目的**：将模型权重和/或激活值从高精度浮点表示（FP32/FP16）映射到低精度整数表示（INT8/INT4/INT2等）或低比特浮点表示（FP8等），以减少存储空间和计算量，同时利用低精度运算单元获得更高吞吐。

📖 代码实践：[1.1_quantization.ipynb](model_compression/1.1_quantization.ipynb)

#### 1.1.1 训练后量化（Post-Training Quantization, PTQ）

> **基本原理**：在模型训练完成后，无需重新训练，通过校准数据集统计权重/激活的分布，将浮点值映射到低精度整数空间。核心是寻找最优的量化参数（scale和zero-point），使得量化误差最小。

- **对称量化（Symmetric Quantization）**
  - 原理：量化范围关于零点对称，zero-point固定为0，仅使用scale参数。计算简单，适合权重分布近似对称的场景。
- **非对称量化（Asymmetric Quantization）**
  - 原理：量化范围不对称，使用独立的scale和zero-point，能更好地拟合偏斜分布（如ReLU后的激活值），精度更高但计算略复杂。
- **逐通道量化（Per-Channel Quantization）**
  - 原理：为权重张量的每个输出通道独立计算量化参数，比逐张量量化能更精确地捕捉各通道的数值分布差异，显著提升低比特量化精度。
- **逐组量化（Per-Group Quantization）**
  - 原理：将权重按组（如128列一组）分别计算量化参数，在逐通道和逐张量之间取得精度与开销的平衡。AWQ、GPTQ等方法均采用此策略。

#### 1.1.2 量化感知训练（Quantization-Aware Training, QAT）

> **基本原理**：在训练过程中插入伪量化（fake quantization）节点，模拟量化带来的误差，让模型在训练阶段就适应低精度表示，从而在量化后保持更高精度。

- **全量化感知训练（Full QAT）**
  - 原理：对权重和激活均插入伪量化操作，通过反向传播更新全精度权重，前向传播时模拟量化效果。需要完整训练流程，精度最优但成本最高。
- **部分量化感知训练（Partial QAT）**
  - 原理：仅对敏感层进行QAT微调，其余层使用PTQ。在训练成本和精度之间取得平衡。
- **量化感知低秩微调（QA-LoFT/QLoRA）**
  - 原理：将基座模型保持量化状态，仅对低秩适配器（LoRA）进行训练，大幅降低QAT的显存需求和训练成本。

#### 1.1.3 混合精度量化（Mixed-Precision Quantization）

> **基本原理**：不同层/模块对量化的敏感度不同，对敏感层保持较高精度（FP16/INT8），对不敏感层使用较低精度（INT4/INT2），在整体压缩率和精度之间取得最优平衡。

- **自动混合精度搜索（Auto Mixed-Precision Search）**
  - 原理：通过HAWQ、HAWQ-V2等方法计算各层的Hessian谱/迹来评估量化敏感度，自动确定每层的最优比特数，满足整体精度约束下最大化压缩率。
- **硬件感知混合精度（Hardware-Aware Mixed-Precision）**
  - 原理：在搜索空间中加入硬件约束（如某些NPU不支持INT2运算），确保所选精度组合在目标硬件上可高效执行。
- **FP8浮点量化（FP8 Quantization）**
  - 原理：使用8位浮点格式（E4M3和E5M2两种编码）替代FP16/FP32。E4M3（4位指数+3位尾数）用于前向传播，动态范围较小但精度更高；E5M2（5位指数+2位尾数）用于反向传播，动态范围更大。NVIDIA H100/RTX 4090+、Intel数据中心GPU等硬件原生支持FP8 Tensor Core运算，相比FP16可获得约2倍吞吐提升和50%内存节省。FP8量化通常只需简单的缩放因子（delayed scaling），无需复杂的校准流程。

#### 1.1.4 主流量化算法

| 算法 | 核心原理 | 特点 |
|------|---------|------|
| **LLM.int8()** | 混合精度分解：对离群值特征维度使用FP16，其余使用INT8 | 首次实现LLM INT8推理几乎无损 |
| **GPTQ** | 基于OBQ（Optimal Brain Quantization）的逐层逐列量化：逐列量化权重，每量化一列后立即更新尚未量化列的Hessian逆，以补偿该列量化带来的误差。支持3/4/8bit | 逐组量化+懒惰batch更新，速度快，GPU友好 |
| **AWQ** | 基于激活感知的权重量化：识别对激活分布影响最大的权重通道（salient weights），对这些通道乘以缩放因子后再量化 | 保护重要权重通道，INT4量化几乎无损 |
| **SmoothQuant** | 将激活中的量化难度迁移到权重：对离群值通道，将激活除以smooth因子 $s_j = \max(|X_j|)^\alpha / \max(|W_j|)^{1-\alpha}$，权重乘以对应因子，使激活和权重均易于量化。$\alpha$ 通常取0.5 | 解决激活量化难题，实现W8A8量化 |
| **SpQR** | 将离群值权重以高精度孤立存储，其余权重以3-4bit量化 | 压缩率与精度的精细平衡 |
| **QuIP/QuIP#** | 利用随机正交矩阵对权重进行不相交性变换后再量化，降低量化误差 | 理论保证的2bit量化方法 |
| **AQLM** | 基于多码本向量量化的方法，将权重分组后用多个码本的线性组合表示 | 极低比特（2bit）下精度领先 |
| **HQQ** | 无需校准数据的量化方法，通过半二次分裂优化直接从权重分布推断量化参数 | 零数据量化，适合无法获取校准数据的场景 |
| **FP8量化** | 使用E4M3/E5M2浮点格式，通过delayed scaling策略将FP16权重缩放至FP8范围 | 硬件原生加速，校准简单，适合H100/RTX 4090+等新硬件 |

---

### 1.2 剪枝（Pruning）

> **目的**：移除模型中对输出贡献较小的参数（权重/神经元/注意力头等），直接减少模型参数量和计算量。

📖 代码实践：[1.2_pruning.ipynb](model_compression/1.2_pruning.ipynb)

#### 1.2.1 非结构化剪枝（Unstructured Pruning）

> **基本原理**：将单个权重置零，产生稀疏权重矩阵。剪枝粒度最细，理论上精度损失最小，但需要稀疏计算硬件/软件支持才能获得实际加速。

- **幅度剪枝（Magnitude Pruning）**
  - 原理：按权重绝对值大小排序，移除绝对值最小的权重。简单直接，但未考虑权重对损失函数的影响。
- **梯度剪枝（Gradient-based Pruning）**
  - 原理：基于梯度信息（如Taylor展开一阶项）评估权重重要性，移除对损失函数影响最小的权重。
- **稀疏度渐进增长（Sparse Growth / Gradual Magnitude Pruning, GMP）**
  - 原理：训练过程中从0%稀疏度逐步增长到目标稀疏度，让模型逐步适应稀疏结构，比一次性剪枝精度更高。

#### 1.2.2 结构化剪枝（Structured Pruning）

> **基本原理**：按结构化单元（注意力头、FFN中间维度、整层等）进行剪枝，剪枝后模型仍是稠密矩阵，无需稀疏计算支持即可获得实际加速。

- **注意力头剪枝（Attention Head Pruning）**
  - 原理：评估各注意力头的重要性（如对输出方差的贡献），移除贡献最小的头。多头注意力本身具有冗余性。
- **FFN中间维度剪枝（FFN Intermediate Dimension Pruning）**
  - 原理：FFN层中间维度通常远大于隐藏维度，存在大量冗余。按列/行移除不重要的中间神经元。
- **层剪枝/层丢弃（Layer Dropping）**
  - 原理：移除整层Transformer层。研究表明LLM中间层存在较大冗余，可安全移除部分层。
- **短上下文层剪枝（Short-Context Layer Pruning）**
  - 原理：针对短上下文场景，某些层对短序列推理贡献极小，可针对性移除。
- **LLM-Pruner / SliceGPT / ShortGPT / LaCo 等方法**
  - 原理：各方法通过不同的重要性度量（如Hessian、激活范数、层间相似度等）来指导结构化剪枝决策。

#### 1.2.3 半结构化剪枝 / N:M稀疏（Semi-Structured / N:M Sparsity）

> **基本原理**：在每M个连续权重中保留N个非零值（如2:4稀疏），形成固定稀疏模式。NVIDIA Ampere及后续架构的稀疏Tensor Cores可直接加速2:4稀疏矩阵运算，获得约2倍加速。

- **2:4稀疏训练**
  - 原理：每4个权重中保留2个，稀疏度50%。通过稀疏感知训练恢复精度，硬件可获得接近2倍吞吐提升。
- **N:M稀疏变体**
  - 原理：探索不同的N:M比例（如1:4, 4:8等），在稀疏度和硬件支持之间取得平衡。

---

### 1.3 知识蒸馏（Knowledge Distillation）

> **目的**：将大模型（教师模型）的知识迁移到小模型（学生模型），使小模型在参数量大幅减少的情况下仍能逼近大模型的性能。

📖 代码实践：[1.3_knowledge_distillation.ipynb](model_compression/1.3_knowledge_distillation.ipynb)

#### 1.3.1 白盒蒸馏（White-Box Distillation）

> **基本原理**：可访问教师模型的内部状态（logits、中间层特征、注意力图等），利用这些丰富信息指导学生模型训练。

- **Logits级蒸馏（Logits-Level / Response-Based）**
  - 原理：学生模型的输出logits与教师模型的soft logits之间计算KL散度损失。教师输出的概率分布包含"暗知识"（类别间的相似性信息），比硬标签信息更丰富。
- **特征级蒸馏（Feature-Level / Intermediate-Layer）**
  - 原理：对齐教师和学生中间层的隐藏状态或特征表示，通常需要线性变换层将学生的特征映射到教师的特征空间。
- **注意力蒸馏（Attention Transfer）**
  - 原理：让学生模型的注意力图模仿教师模型的注意力分布，学习教师模型的注意力模式。
- **MiniLLM**
  - 原理：将KL散度替换为反向KL散度，避免学生模型过度拟合教师分布的"长尾"部分，更适合生成式LLM蒸馏。

#### 1.3.2 黑盒蒸馏（Black-Box Distillation）

> **基本原理**：仅能通过API访问教师模型的输出（生成的文本），无法获取内部状态。通过教师模型生成的高质量数据来训练学生模型。

- **指令蒸馏（Instruction Distillation）**
  - 原理：使用教师模型对大量指令生成回答，构建指令微调数据集训练学生模型。如Alpaca、Vicuna等方法。
- **数据增强蒸馏**
  - 原理：利用教师模型对原始数据进行改写、扩展、多样化生成，丰富学生模型的训练语料。
- **自蒸馏（Self-Distillation）**
  - 原理：模型自身作为教师，通过不同训练阶段或不同数据增强下的输出一致性来提升性能。

---

### 1.4 低秩分解（Low-Rank Factorization）

> **目的**：将大型权重矩阵分解为两个或多个低秩矩阵的乘积，减少参数量和计算量。

📖 代码实践：[1.4_low_rank_factorization.ipynb](model_compression/1.4_low_rank_factorization.ipynb)

- **SVD分解（Singular Value Decomposition）**
  - 原理：对权重矩阵进行奇异值分解 W = UΣV^T，保留前r个最大奇异值，得到 W ≈ U_r Σ_r V_r^T，参数量从mn降至r(m+n)。
- **Tucker分解**
  - 原理：对高维张量进行多模式分解，保留各模式的主成分，适合多维权重张量（如注意力权重）的压缩。
- **低秩重参数化（LoRA-style Factorization）**
  - 原理：冻结原始权重W，添加低秩增量 ΔW = AB，其中A∈R^{m×r}, B∈R^{r×n}。推理时可将AB合并回W，无额外推理开销。虽主要用于微调，但其低秩思想可用于压缩。

---

## 2 高效推理架构（Efficient Inference Architecture）

> **目的**：在不改变模型参数的前提下，通过优化推理过程中的计算策略和内存管理，显著提升推理速度和降低内存占用。

### 2.1 KV Cache 优化

> **基本原理**：自回归生成中，每步需访问之前所有token的Key/Value向量。KV Cache缓存已计算的KV以避免重复计算，但其内存占用随序列长度线性增长，成为长序列推理的核心瓶颈。

📖 代码实践：[2.1_kv_cache.ipynb](efficient_inference/2.1_kv_cache.ipynb)

#### 2.1.1 KV Cache 量化

- **KV Cache INT8/INT4 量化**
  - 原理：将缓存的Key/Value张量从FP16量化为INT8或INT4，直接将KV Cache内存占用减半或降至1/4。由于Key和Value的分布不同，通常对Key使用逐通道量化，对Value使用逐张量量化。
- **KV Cache 分组量化（Grouped Quantization）**
  - 原理：将KV向量按组量化，每组独立计算量化参数，精度更高。

#### 2.1.2 KV Cache 内存管理

- **PagedAttention（vLLM）**
  - 原理：借鉴操作系统虚拟内存的分页管理思想，将KV Cache划分为固定大小的block，按需分配，非连续存储。消除内存碎片，支持更大batch和更长序列。
- **Prefix Caching / RadixAttention**
  - 原理：对共享前缀（如system prompt）的KV Cache进行缓存复用，避免重复计算。RadixAttention使用基数树结构管理前缀，支持高效的前缀匹配和复用。

#### 2.1.3 KV Cache 压缩与淘汰

- **滑动窗口注意力（Sliding Window Attention, SWA）**
  - 原理：每个token只关注最近W个token的KV，超出窗口的KV被丢弃。KV Cache大小固定为O(W)，不随序列增长。Mistral/Gemma等模型采用此设计。
- **KV Cache 淘汰策略（Eviction Policy）**
  - 原理：当KV Cache超出预算时，根据注意力分数（attention sink）、token重要性等指标选择性淘汰不重要的KV。如H2O（Heavy-Hitter Oracle）保留注意力分数最高的KV。
- **KV Cache 合并（Merging）**
  - 原理：将相似的KV向量合并为代表性向量（如取加权平均），减少KV数量同时保留关键信息。如CaM、D2O等方法。
- **跨层KV共享（Cross-Layer KV Sharing）**
  - 原理：相邻层的KV表示高度相似，可共享同一份KV Cache。如CLA（Cross-Layer Attention）、YOCO等架构，将KV Cache占用减半。

---

### 2.2 注意力机制优化

> **目的**：标准自注意力的计算复杂度为O(n²)，是长序列推理的核心瓶颈。优化注意力计算可显著降低延迟和内存。

📖 代码实践：[2.2_attention_optimization.ipynb](efficient_inference/2.2_attention_optimization.ipynb)

#### 2.2.1 高效注意力计算

- **Flash Attention / Flash Attention 2/3**
  - 原理：通过分块计算（tiling）和重计算（recomputation）策略，减少对HBM的读写次数，将注意力计算变为IO-bound而非compute-bound。不改变数学结果，是精确注意力的硬件高效实现。
- **Flash Decoding**
  - 原理：针对decode阶段（每步仅1个query token）的优化，将KV按split并行计算后reduce，提升GPU利用率。

#### 2.2.2 注意力架构优化

- **多查询注意力（Multi-Query Attention, MQA）**
  - 原理：所有注意力头共享同一组Key/Value投影，仅Query保持多头。KV Cache减少为1/num_heads，推理速度显著提升。
- **分组查询注意力（Grouped-Query Attention, GQA）**
  - 原理：在MHA和MQA之间取折中，将Query头分组，每组共享一组KV。如Llama-2 70B使用8组KV（70个Query头），在精度和效率间取得平衡。
- **多令牌预测（Multi-Token Prediction, MTP）**
  - 原理：一次前向传播预测多个token，减少自回归步数，提升推理吞吐。

#### 2.2.3 稀疏注意力

- **局部注意力（Local Attention）**
  - 原理：每个token仅关注局部窗口内的token，复杂度O(n·w)。
- **全局+局部混合注意力（Global+Local Hybrid）**
  - 原理：少量token具有全局注意力（如CLS token），其余使用局部注意力。如Longformer。
- **稀疏注意力模式（Sparse Attention Patterns）**
  - 原理：按固定模式（如strided、fixed pattern）选择性地计算部分注意力对，跳过大部分注意力计算。

---

### 2.3 推理加速策略

📖 代码实践：[2.3_inference_acceleration.ipynb](efficient_inference/2.3_inference_acceleration.ipynb)

#### 2.3.1 投机解码（Speculative Decoding）

> **基本原理**：使用小模型（draft model）快速生成多个候选token，再用大模型（target model）并行验证这些token，接受正确的token、拒绝错误的token。在保持与大模型完全相同输出分布的前提下，显著提升推理速度。

- **自投机解码（Self-Speculative Decoding）**
  - 原理：不使用额外的draft模型，而是利用同一模型的浅层（early exit）或低精度版本来生成候选token，节省draft模型的内存开销。
- **基于n-gram的投机解码**
  - 原理：从缓存中检索匹配的n-gram序列作为候选，无需draft模型。
- **树状投机解码（Tree-based Speculative Decoding）**
  - 原理：draft模型生成树状候选结构（多分支），target model一次验证整棵树，提高接受率。如Medusa、Eagle。
- **Medusa**
  - 原理：在模型头部添加多个额外的预测头（medusa heads），每个头独立预测未来不同位置的token，一次前向传播生成多个候选。

#### 2.3.2 批量推理优化

- **连续批处理（Continuous Batching / Iteration-Level Scheduling）**
  - 原理：不等待整个batch完成后再处理新请求，而是在每个迭代步动态插入新请求、移除已完成请求，显著提升GPU利用率。
- **动态批处理（Dynamic Batching）**
  - 原理：将不同时间到达的请求动态组成batch，减少等待时间。

#### 2.3.3 早期退出（Early Exit）

> **基本原理**：并非所有token都需要经过全部Transformer层。简单token在浅层即可获得足够置信的输出，可提前退出计算，节省计算量。

- **置信度驱动的早期退出**
  - 原理：在每层输出附加分类头，当输出置信度超过阈值时提前退出。
- **自适应深度推理（Adaptive Depth Inference）**
  - 原理：根据输入难度动态决定推理深度，简单输入浅层退出，复杂输入深层推理。

---

## 3 高效模型架构设计（Efficient Model Architecture）

> **目的**：从架构层面设计更适合端侧部署的模型，使其在参数量更少的情况下达到与大模型可比的性能。

### 3.1 轻量化架构设计

📖 代码实践：[3.1_lightweight_architecture.ipynb](efficient_architecture/3.1_lightweight_architecture.ipynb)

- **小参数量模型（Small Language Models, SLM）**
  - 原理：通过精心设计训练数据（高质量、高多样性）和训练策略，使小参数量模型（1B-3B）达到甚至超越更大模型的性能。代表：Phi系列、Gemma-2B、MiniCPM。
- **深度与宽度的最优权衡**
  - 原理：研究表明，在相同参数预算下，更深更窄的网络比浅更宽的网络更适合语言建模任务。如MobileLLM采用深而窄的设计。
- **权重共享（Weight Sharing）**
  - **嵌入共享（Embedding Sharing / Tied Embeddings）**：输入嵌入层和输出lm_head共享权重矩阵，减少参数量。如GPT-2、Llama-3等采用此设计。
  - **跨层参数共享（Cross-Layer Parameter Sharing）**：多层Transformer共享相同的权重参数（如ALBERT风格的共享注意力权重和FFN权重），参数量大幅减少但层数不变，保留深层推理能力。端侧部署时共享权重只需加载一份，内存占用显著降低。
  - **量化码本共享（Codebook Sharing）**：在向量量化中，多个权重块共享同一组量化码本，减少码本存储开销。

### 3.2 线性注意力与亚二次复杂度架构

> **基本原理**：标准注意力的O(n²)复杂度限制了长序列推理。线性注意力通过kernel化或分解将复杂度降至O(n)，状态空间模型通过隐状态递推实现O(n)推理。

📖 代码实践：[3.2_linear_attention_ssm.ipynb](efficient_architecture/3.2_linear_attention_ssm.ipynb)

- **线性注意力（Linear Attention）**
  - 原理：将softmax(QK^T)V分解为 φ(Q)(φ(K)^T V)，先计算 φ(K)^T V（与序列长度无关），再与 φ(Q) 相乘，复杂度从O(n²)降至O(nd²)。如Linear Transformer、RetNet。
- **状态空间模型（State Space Models, SSM）**
  - 原理：通过隐状态的线性递推建模序列依赖，推理时每步仅需O(d)计算和O(d)内存，不受序列长度影响。代表：Mamba（选择性状态空间）、S4。
- **线性RNN架构（Linear RNN）**
  - 原理：使用线性递推替代传统RNN的非线性激活，结合门控机制实现高效并行训练和O(1)推理。代表：RWKV（时间混合+通道混合交替）、Griffin（门控线性注意力+局部注意力混合）。
- **混合架构（Hybrid Architecture）**
  - 原理：将注意力层和SSM/线性注意力层交替堆叠，在关键位置保留精确注意力，其余位置使用高效线性层。如Jamba（Mamba+Attention+MoE）、Zamba。

### 3.3 混合专家架构（Mixture of Experts, MoE）

> **基本原理**：将FFN层替换为多个专家网络（experts），通过路由器（router）为每个token选择Top-K个专家。总参数量大但每次推理仅激活部分专家，实现"大模型能力、小模型成本"。

📖 代码实践：[3.3_moe.ipynb](efficient_architecture/3.3_moe.ipynb)

- **稀疏MoE（Sparse MoE）**
  - 原理：每个token仅激活Top-1或Top-2专家，如Mixtral 8x7B每次仅激活2个专家（约13B参数），但拥有46B总参数的知识容量。
- **MoE量化与压缩**
  - 原理：MoE模型的专家权重存在大量冗余，可对不活跃专家进行更激进的量化或剪枝，进一步降低端侧部署成本。
- **MoE路由优化**
  - 原理：优化路由策略使专家负载均衡，避免少数专家过载。端侧部署时还需考虑专家权重的按需加载。
- **MoE端侧部署特殊挑战**
  - **专家权重按需加载**：MoE总参数量大（如Mixtral 8x7B有46B参数），端侧内存无法全部驻留。需根据路由预测结果，在计算前将目标专家权重从慢存储（Flash/SSD）加载到快内存（SRAM/DRAM），计算后释放。关键在于路由预测的提前量和加载延迟的隐藏。
  - **专家合并与蒸馏**：多个专家的权重可能高度相似，可将相似专家合并为单个专家（expert merging），或将多个专家的知识蒸馏到更少的专家中（expert distillation），降低端侧内存需求。
  - **Expert Choice Routing**：与传统Token Choice（每个token选Top-K专家）不同，Expert Choice由每个专家选择Top-K token，天然实现负载均衡，避免路由崩塌问题。

---

## 4 编译与运行时优化（Compilation & Runtime Optimization）

> **目的**：通过编译器优化和运行时调度，将模型计算图映射到目标硬件上，最大化硬件利用率和推理吞吐。

### 4.1 计算图优化

📖 代码实践：[4.1_graph_optimization.ipynb](compilation_runtime/4.1_graph_optimization.ipynb)

- **算子融合（Operator Fusion）**
  - 原理：将多个连续算子合并为单个算子执行，减少中间结果的内存读写。如将QKV投影+RoPE+Attention融合为单个kernel，将Linear+LayerNorm融合等。
- **死代码消除（Dead Code Elimination）**
  - 原理：移除计算图中对最终输出无贡献的算子和分支，减少无效计算。
- **常量折叠（Constant Folding）**
  - 原理：在编译期将可确定的常量表达式预计算，将结果内联到图中，减少运行时计算。
- **内存布局优化（Memory Layout Optimization）**
  - 原理：调整张量的内存排布（如NCHW→NHWC）以匹配硬件的内存访问模式，减少cache miss。

### 4.2 针对硬件的代码生成

📖 代码实践：[4.2_code_generation.ipynb](compilation_runtime/4.2_code_generation.ipynb)

- **TVM / Apache TVM**
  - 原理：统一的深度学习编译器框架，通过搜索最优算子实现（AutoTVM/Ansor）为目标硬件生成高效代码。支持CPU、GPU、NPU等多种后端。
- **MLIR / XLA**
  - 原理：多级中间表示编译框架，通过逐级lowering将高层计算图逐步转换为目标硬件指令。XLA用于TensorFlow/JAX的图编译优化。
- **TensorRT**
  - 原理：NVIDIA推出的推理优化器，针对GPU进行层融合、精度校准、kernel自动调优，生成优化后的推理引擎。
- **Core ML Tools**
  - 原理：Apple的模型转换与优化工具，将训练好的模型转换为Core ML格式，针对Apple Silicon的CPU/GPU/Neural Engine进行优化。

### 4.3 内存优化

📖 代码实践：[4.3_memory_optimization.ipynb](compilation_runtime/4.3_memory_optimization.ipynb)

- **激活重计算 / 梯度检查点（Activation Recomputation / Gradient Checkpointing）**
  - 原理：前向传播时不保存中间激活值，反向传播时重新计算所需激活，以计算换内存。端侧推理中可用于降低峰值内存占用。
- **内存复用（Memory Planning / In-Place Operation）**
  - 原理：分析计算图的生命周期，将不再使用的张量内存分配给新张量，减少总内存占用。如静态内存规划（Static Memory Planning）。
- **权重按需加载（Weight Streaming / Offloading）**
  - 原理：不将全部权重常驻内存，而是按层或按需从存储加载到内存，用完即释放。牺牲速度换取更低的内存峰值。

---

## 5 硬件适配与部署框架（Hardware Adaptation & Deployment Framework）

> **目的**：将优化后的模型部署到具体的端侧硬件平台上，需要解决硬件异构性、驱动适配、算子支持度等问题。

### 5.1 端侧NPU适配

📖 代码实践：[5.1_npu_adaptation.ipynb](hardware_deployment/5.1_npu_adaptation.ipynb)

- **高通 Hexagon NPU / QNN**
  - 原理：高通骁龙平台的Hexagon DSP/NPU，通过QNN（Qualcomm Neural Network）SDK进行模型部署。支持INT8/INT4量化推理，最新骁龙8 Gen 3/4的NPU算力达45+ TOPS。
- **苹果 Neural Engine (ANE) / Core ML**
  - 原理：Apple A系列/M系列芯片内置的Neural Engine，通过Core ML框架部署。ANE针对16位浮点和8位整数量化优化，M4芯片ANE算力达38 TOPS。
- **联发科 APU / NeuroPilot**
  - 原理：联发科天玑平台的AI处理单元，通过NeuroPilot SDK部署。支持INT8/INT16推理。
- **华为 NPU / CANN**
  - 原理：华为麒麟/昇腾芯片的NPU，通过CANN（Compute Architecture for Neural Networks）进行部署优化。
- **三星 NPU / Samsung Neural SDK**
  - 原理：Exynos芯片内置NPU，通过Samsung Neural SDK部署。

### 5.2 端侧部署框架

📖 代码实践：[5.2_deployment_frameworks.ipynb](hardware_deployment/5.2_deployment_frameworks.ipynb)

| 框架 | 核心原理 | 特点 |
|------|---------|------|
| **llama.cpp / ggml** | 纯C/C++实现，基于ggml张量库，支持多种量化格式（Q4_0, Q4_K_M, Q8_0等），CPU优先设计 | 跨平台、零依赖、社区活跃、GGUF格式 |
| **MLC-LLM** | 基于Apache TVM的通用LLM部署框架，将模型编译为目标硬件的原生代码 | 支持iOS/Android/Windows/Linux，编译期优化 |
| **ExecuTorch (PyTorch)** | PyTorch官方端侧推理框架，提供模型导出（export）、编译（compile）、运行（runtime）全流程 | 与PyTorch生态无缝集成，支持iOS/Android |
| **ONNX Runtime** | 微软开源的跨平台推理引擎，通过ONNX格式模型在各种硬件上高效执行 | 支持CPU/GPU/NPU，成熟稳定 |
| **TensorFlow Lite** | Google的移动端推理框架，支持Android/iOS，提供模型转换和硬件委托（delegate）机制 | Android生态集成度高 |
| **Core ML** | Apple的端侧ML框架，深度集成iOS/macOS生态，自动利用ANE/GPU/CPU | Apple平台最优选择 |
| **NCNN** | 腾讯开源的高性能神经网络前向计算框架，针对ARM CPU优化 | 无依赖，ARM优化极致 |
| **MNN** | 阿里开源的轻量级推理引擎，支持CPU/GPU/NPU，针对移动端深度优化 | 端侧推理性能优异 |
| **TFLite Micro** | TensorFlow Lite的微控制器版本，针对MCU等极低资源设备 | 支持Cortex-M等MCU |
| **TinyEngine** | MIT提出的MCU端推理引擎，支持内存感知的模型编译和推理 | 面向极低功耗MCU |

### 5.3 硬件感知优化

📖 代码实践：[5.3_hardware_aware.ipynb](hardware_deployment/5.3_hardware_aware.ipynb)

- **内存带宽优化**
  - 原理：LLM推理的decode阶段是内存带宽受限（memory-bound）的——每次生成一个token需要读取全部模型权重，但仅执行少量计算。优化方向：量化（减少数据搬运量）、算子融合（减少访存次数）、权重预取（overlap计算与访存）。
- **计算单元利用率优化**
  - 原理：prefill阶段是计算受限（compute-bound），需要充分利用并行计算单元。优化方向：批量矩阵乘（GEMM）、张量并行、Flash Attention。
- **功耗预算优化**
  - 原理：端侧设备有严格的TDP（热设计功耗）限制。通过动态电压频率调整（DVFS）、计算精度自适应、推理调度等手段在性能和功耗间取得平衡。

---

## 6 模型格式与序列化（Model Format & Serialization）

> **目的**：高效的模型存储格式直接影响加载速度、内存占用和跨平台兼容性。

📖 代码实践：[6.0_model_format.ipynb](model_format/6.0_model_format.ipynb)

| 格式 | 核心原理 | 特点 |
|------|---------|------|
| **GGUF** | GGML的统一格式，支持元数据嵌入、多种量化类型、mmap加载 | llama.cpp生态标准格式，端侧部署最流行 |
| **SafeTensors** | HuggingFace推出的安全张量格式，使用内存映射（mmap）零拷贝加载 | 加载速度快、无pickle安全风险、HuggingFace默认格式 |
| **ONNX** | 开放神经网络交换格式，标准化的算子定义，跨框架互操作 | 推理引擎通用输入格式 |
| **MLIR** | 多级中间表示，支持从高层计算图到硬件指令的逐级变换 | 编译器基础设施，非直接部署格式 |
| **Core ML (.mlpackage/.mlmodelc)** | Apple Core ML的模型包格式，包含计算图和权重 | Apple生态专用 |
| **QNN Context Binary** | 高通QNN的预编译二进制格式，包含针对Hexagon NPU的优化指令 | 高通平台专用，加载即推理 |

---

## 7 端云协同与系统集成（Edge-Cloud Collaboration & System Integration）

> **目的**：在端侧设备计算能力不足时，通过端云协同策略实现大模型能力的按需获取，同时保护用户隐私。

### 7.1 端云协同推理

📖 代码实践：[7.1_edge_cloud_inference.ipynb](edge_cloud/7.1_edge_cloud_inference.ipynb)

- **模型拆分推理（Split Computing / Model Splitting）**
  - 原理：将模型按层拆分，浅层在端侧执行，深层在云端执行。中间特征上传至云端而非原始数据，兼顾隐私和计算效率。
- **自适应推理路由（Adaptive Inference Routing）**
  - 原理：根据输入复杂度和端侧负载动态决定推理在端侧还是云端执行。简单请求端侧处理，复杂请求路由到云端。
- **推测验证协同（Edge-Cloud Speculative Decoding）**
  - 原理：端侧小模型作为draft model生成候选token，云端大模型并行验证，减少云端计算量和通信轮次。

### 7.2 多模态端侧部署

📖 代码实践：[7.2_multimodal_deployment.ipynb](edge_cloud/7.2_multimodal_deployment.ipynb)

- **视觉语言模型压缩（VLM Compression）**
  - 原理：对视觉编码器（如ViT）和语言模型分别进行量化和压缩，视觉编码器通常可更激进量化。如LLaVA的端侧部署。
- **多模态融合优化**
  - 原理：优化视觉特征和语言特征的融合方式，减少跨模态交互的计算开销。如使用更轻量的投影层、压缩视觉token数量。
- **音频/语音模型端侧部署**
  - 原理：Whisper等语音模型的端侧量化与部署，流式处理优化，低延迟语音交互。

### 7.3 隐私与安全

📖 代码实践：[7.3_privacy_security.ipynb](edge_cloud/7.3_privacy_security.ipynb)

- **联邦学习（Federated Learning）**
  - 原理：在端侧本地训练模型更新，仅上传梯度/参数差值到服务器聚合，原始数据不出端。适合端侧模型的个性化微调。
- **差分隐私（Differential Privacy）**
  - 原理：在模型输出或梯度中添加校准噪声，使得无法从输出推断出单个训练样本的信息，提供数学可证明的隐私保护。
- **模型加密与安全推理**
  - 原理：对端侧模型权重进行加密存储，推理时在可信执行环境（TEE）中解密执行，防止模型窃取。如ARM TrustZone、Apple Secure Enclave。
- **水印与模型溯源**
  - 原理：在模型权重或输出中嵌入不可见水印，用于追踪模型来源和防止未授权使用。

### 7.4 端侧推理服务

> **目的**：产业级端侧部署不仅需要单次推理优化，还需要完整的推理服务系统来管理多模型共存、请求调度和生命周期。

- **请求排队与优先级调度**
  - 原理：端侧设备可能同时服务多个应用（如语音助手、实时翻译、文本补全），需要根据请求优先级和延迟要求进行调度。高优先级交互式请求优先处理，低优先级后台任务延后执行。
- **多模型共存内存管理**
  - 原理：端侧可能同时部署多个模型（如基础对话模型+专用任务模型），需要在有限内存中管理多模型权重的加载/卸载。通过权重共享、时分复用、按需加载等策略最大化内存利用率。
- **推理超时与降级策略**
  - 原理：当端侧推理延迟超过阈值时，自动降级到更小的模型或路由到云端，保证用户体验。降级策略包括：切换低精度模型、减少推理层数（early exit）、回退到云端推理。
- **模型热更新与A/B测试**
  - 原理：端侧模型需要在不中断服务的情况下更新。通过双缓冲加载（新模型在后台加载，加载完成后原子切换）实现热更新；通过流量分配实现A/B测试，逐步验证新模型效果。

---

## 8 端侧训练与个性化（On-Device Training & Personalization）

> **目的**：在端侧设备上对模型进行微调和个性化适配，使模型更好地服务本地用户，同时保护用户数据隐私。

### 8.1 参数高效微调（PEFT）

📖 代码实践：[8.1_peft.ipynb](on_device_training/8.1_peft.ipynb)

- **LoRA / QLoRA**
  - 原理：冻结预训练权重，仅训练低秩适配器矩阵。QLoRA进一步将基座模型量化为4bit（NF4格式），仅适配器保持高精度（BF16），端侧训练显存需求极低。QLoRA的核心是双重量化（double quantization）和分页优化器（paged optimizer），使7B模型在24GB显存上可训练。
- **Adapter**
  - 原理：在Transformer层中插入小型适配器模块（下投影-非线性-上投影），仅训练适配器参数。
- **Prefix Tuning / Prompt Tuning**
  - 原理：在输入前添加可训练的虚拟token/prefix，仅训练这些少量参数。
- **IA³（Infused Adapter by Inhibiting and Amplifying）**
  - 原理：通过可学习的向量对注意力层的Key/Value和FFN的输出进行逐元素缩放（amplify或inhibit），参数量比LoRA更少（仅训练3个向量），适合极低资源的端侧微调。

### 8.2 端侧训练优化

📖 代码实践：[8.2_training_optimization.ipynb](on_device_training/8.2_training_optimization.ipynb)

- **选择性反向传播（Selective Backpropagation）**
  - 原理：仅对部分层进行反向传播，冻结其余层，减少训练的计算量和内存占用。
- **梯度累积与混合精度**
  - 原理：端侧内存有限，通过小batch+梯度累积模拟大batch效果；使用FP16/BF16混合精度减少训练内存占用。
- **内存高效优化器**
  - 原理：使用8bit优化器（如8-bit AdamW）、节省内存的优化器（如Sophia、Lion），降低优化器状态的内存占用。
- **梯度检查点（Gradient Checkpointing）**
  - 原理：前向传播时不保存中间激活值，仅保存关键检查点的输出，反向传播时从检查点重新计算所需激活。以约30%的额外计算换取60%+的内存节省，是端侧训练最关键的内存优化技术之一。

### 8.3 个性化与持续适应

> **目的**：端侧模型需要持续适应用户的个性化需求，同时避免灾难性遗忘和隐私泄漏。

- **灾难性遗忘防御**
  - 原理：端侧微调时，新数据上的训练可能导致模型遗忘预训练知识。防御方法包括：EWC（Elastic Weight Consolidation，对重要参数施加L2正则约束）、MAS（Memory Aware Synapses，基于输出敏感度评估参数重要性）、经验回放（保留少量旧数据混合训练）。
- **端侧数据高效利用**
  - 原理：端侧数据通常稀缺且分布偏斜。通过数据增强（同义词替换、回译等）、合成数据生成（用模型自身生成训练样本）、主动学习（选择最有信息量的样本标注）来提升数据效率。
- **个性化与隐私的权衡**
  - 原理：更强的个性化通常需要更多用户数据，增加隐私风险。通过差分隐私微调（在梯度中添加噪声）、联邦学习（数据不出端）、最小化适配器参数量（仅LoRA的少量参数包含用户信息）来在个性化和隐私间取得平衡。
- **用户画像与条件生成**
  - 原理：通过轻量级用户画像模块（如可学习的user embedding或soft prompt），在推理时根据用户特征条件化模型输出，无需修改模型权重即可实现个性化。

---

## 9 评估指标体系（Evaluation Metrics）

> **目的**：系统化的评估指标是端侧部署技术选型和优化的基础。不同应用场景对精度、延迟、内存、功耗的优先级不同，需要综合评估。

### 9.1 延迟指标

| 指标 | 定义 | 典型目标 |
|------|------|---------|
| **首Token延迟（TTFT, Time To First Token）** | 从输入发送到第一个输出token生成的延迟，反映prefill阶段效率 | 交互式场景 < 200ms |
| **Token间延迟（ITL, Inter-Token Latency）** | 生成连续两个token之间的延迟，反映decode阶段效率 | 实时对话 < 50ms/token |
| **端到端延迟（E2E Latency）** | 从输入发送到完整输出生成的总延迟 | 取决于输出长度和场景 |

### 9.2 吞吐指标

| 指标 | 定义 | 典型参考 |
|------|------|---------|
| **吞吐量（Throughput）** | 单位时间生成的token数（tokens/s），受batch size和序列长度影响 | 骁龙8 Gen3 INT4 7B模型约 10-20 tokens/s |
| **并发请求数** | 同时处理的推理请求数量，反映服务能力 | 端侧通常1-4个并发 |

### 9.3 资源指标

| 指标 | 定义 | 典型参考 |
|------|------|---------|
| **内存峰值（Peak Memory）** | 推理过程中的最大内存占用（模型权重+KV Cache+激活值） | 7B INT4模型约 4-5GB |
| **模型体积（Model Size）** | 量化后模型文件的存储大小 | 7B INT4约 3.5-4GB, 7B INT8约 7GB |
| **功耗（Power）** | 推理过程中的芯片功耗 | 移动端NPU推理约 2-5W |
| **能效比（Energy Efficiency）** | 每焦耳生成的token数（tokens/J），衡量能量利用效率 | NPU推理能效比远高于CPU/GPU |

### 9.4 精度指标

| 指标 | 定义 | 用途 |
|------|------|------|
| **Perplexity** | 模型对测试集的困惑度，越低越好 | 量化/剪枝前后精度损失的核心度量 |
| **下游任务准确率** | 在具体任务（MMLU、HumanEval等）上的表现 | 评估实际应用能力 |
| **量化前后差异** | 量化模型与原始模型输出的KL散度或余弦相似度 | 量化算法选择的参考 |

### 9.5 典型场景参考数据

| 模型 | 量化 | 硬件平台 | 推理速度 | 内存占用 | Perplexity变化 |
|------|------|---------|---------|---------|---------------|
| Llama-2-7B | W4A16 (AWQ) | RTX 4090 | ~80 tokens/s | ~4GB | +0.1~0.3 |
| Llama-2-7B | W4A16 (GPTQ) | RTX 4090 | ~75 tokens/s | ~4GB | +0.1~0.5 |
| Llama-2-7B | W8A8 (SmoothQuant) | 骁龙8 Gen3 CPU | ~5-8 tokens/s | ~7GB | +0.05~0.2 |
| Llama-2-7B | Q4_K_M (llama.cpp) | M2 MacBook Air | ~15-20 tokens/s | ~4.5GB | +0.2~0.5 |
| Phi-3-mini-3.8B | Q4_K_M | 骁龙8 Gen3 NPU | ~20-30 tokens/s | ~2.5GB | +0.1~0.3 |

> 注：以上数据为典型值，实际性能因实现、驱动版本和测试条件而异，仅供参考。

---

## 技术选型决策树

```
端侧部署大模型
│
├── 模型太大放不下？ → 模型压缩
│   ├── 量化（首选，效果最好）
│   │   ├── W4A16：AWQ/GPTQ（GPU端侧）
│   │   ├── W8A8：SmoothQuant（CPU/NPU端侧）
│   │   ├── FP8：E4M3/E5M2（H100/RTX 4090+等新硬件）
│   │   └── W4A4：QuIP#/AQLM（极致压缩）
│   ├── 剪枝（结构化剪枝优先）
│   └── 蒸馏（需要训练资源）
│
├── 推理太慢？ → 推理优化
│   ├── Prefill慢 → Flash Attention / 批量优化
│   ├── Decode慢 → 投机解码 / 量化 / KV Cache优化
│   └── 长序列慢 → 稀疏注意力 / SSM / 滑动窗口
│
├── 内存不够？ → 内存优化
│   ├── KV Cache太大 → KV量化 / PagedAttention / 滑动窗口
│   ├── 权重太大 → 量化 + 权重按需加载
│   └── 峰值内存高 → 激活重计算 / 内存复用
│
├── 需要个性化？ → 端侧训练
│   ├── QLoRA（推荐）
│   ├── IA³（极低资源）
│   └── Adapter / Prefix Tuning
│
└── 硬件适配？ → 部署框架选择
    ├── iOS → Core ML / MLC-LLM
    ├── Android (高通) → QNN / ExecuTorch / MNN
    ├── Android (联发科) → NeuroPilot / MNN
    ├── 通用CPU → llama.cpp
    └── NVIDIA GPU → TensorRT-LLM
```

---

## 总结

大模型端侧部署是一个系统工程，涉及从模型算法层到硬件系统层的全栈优化。各技术之间并非独立，而是相互配合、联合使用：

1. **量化 + KV Cache优化**：同时压缩权重和KV，最大化内存节省
2. **量化 + 投机解码**：小模型量化后更快生成候选，大模型量化后更快验证
3. **剪枝 + 蒸馏**：先剪枝再蒸馏恢复精度，或蒸馏到更小架构
4. **编译优化 + 硬件适配**：编译器针对特定NPU生成最优代码
5. **端云协同 + 隐私保护**：在享受云端算力的同时保护用户数据
6. **MoE + 按需加载**：利用MoE的稀疏激活特性，结合权重流式加载降低端侧内存压力

产业级端侧部署的关键在于：**在精度、速度、内存、功耗之间找到最优平衡点**，这需要根据具体硬件平台、应用场景和性能指标进行系统性调优。
