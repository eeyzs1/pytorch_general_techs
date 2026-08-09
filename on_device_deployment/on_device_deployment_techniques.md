# 大模型端侧部署（On-Device Deployment）技术全景

## 目录

- [总览](#总览)
- [1 模型压缩（Model Compression）](#1-模型压缩model-compression)
  - [1.1 量化（Quantization）](#11-量化quantization)
  - [1.2 剪枝（Pruning）](#12-剪枝pruning)
  - [1.3 知识蒸馏（Knowledge Distillation）](#13-知识蒸馏knowledge-distillation)
  - [1.4 低秩分解（Low-Rank Factorization）](#14-低秩分解low-rank-factorization)
  - [1.5 超低比特量化（Sub-2-bit Quantization）](#15-超低比特量化sub-2-bit-quantization)
  - [1.6 torchao 与官方量化工具链](#16-torchao-与官方量化工具链)
- [2 高效推理架构（Efficient Inference Architecture）](#2-高效推理架构efficient-inference-architecture)
  - [2.1 KV Cache 优化](#21-kv-cache-优化)
  - [2.2 注意力机制优化](#22-注意力机制优化)
  - [2.3 推理加速策略](#23-推理加速策略)
  - [2.4 Prefill / Decode 分治](#24-prefill--decode-分治)
  - [2.5 长上下文技术](#25-长上下文技术beyond-kv-cache)
- [3 高效模型架构设计（Efficient Model Architecture）](#3-高效模型架构设计efficient-model-architecture)
  - [3.1 轻量化架构设计](#31-轻量化架构设计)
  - [3.2 线性注意力与亚二次复杂度架构](#32-线性注意力与亚二次复杂度架构)
  - [3.3 混合专家架构（Mixture of Experts, MoE）](#33-混合专家架构mixture-of-experts-moe)
  - [3.4 硬件感知 NAS](#34-硬件感知-nas-与一次训练多部署once-for-all--mcunet)
- [4 编译与运行时优化（Compilation & Runtime Optimization）](#4-编译与运行时优化compilation--runtime-optimization)
  - [4.1 计算图优化](#41-计算图优化)
  - [4.2 针对硬件的代码生成](#42-针对硬件的代码生成)
  - [4.3 内存优化](#43-内存优化)
- [5 硬件适配与部署框架（Hardware Adaptation & Deployment Framework）](#5-硬件适配与部署框架hardware-adaptation--deployment-framework)
  - [5.1 端侧NPU适配](#51-端侧npu适配)
  - [5.2 端侧部署框架](#52-端侧部署框架)
  - [5.3 硬件感知优化](#53-硬件感知优化)
  - [5.4 硬件基准测试与选型](#54-硬件基准测试与选型)
- [6 模型格式与序列化（Model Format & Serialization）](#6-模型格式与序列化model-format--serialization)
- [7 端云协同与系统集成（Edge-Cloud Collaboration & System Integration）](#7-端云协同与系统集成edge-cloud-collaboration--system-integration)
  - [7.1 端云协同推理](#71-端云协同推理)
  - [7.2 多模态端侧部署](#72-多模态端侧部署)
  - [7.3 隐私与安全](#73-隐私与安全)
  - [7.4 端侧推理服务](#74-端侧推理服务)
  - [7.5 功耗管理与电池感知调度](#75-功耗管理与电池感知调度)
  - [7.6 WebAssembly与浏览器端推理](#76-webassembly与浏览器端推理)
  - [7.7 端侧语音全链路（ASR-LLM-TTS）](#77-端侧语音全链路asr-llm-tts)
- [8 端侧训练与个性化（On-Device Training & Personalization）](#8-端侧训练与个性化on-device-training--personalization)
  - [8.1 参数高效微调（PEFT）](#81-参数高效微调peft)
  - [8.2 端侧训练优化](#82-端侧训练优化)
  - [8.3 端侧评估与个性化](#83-端侧评估与个性化)
  - [8.4 多适配器路由](#84-多适配器路由一基座多-lora)
- [9 端到端实战与故障排查（E2E Deployment & Troubleshooting）](#9-端到端实战与故障排查e2e-deployment--troubleshooting)
  - [9.1 端到端部署流水线](#91-端到端部署流水线)
  - [9.2 故障排查与调试方法](#92-故障排查与调试方法)
- [10 中国国产硬件生态专题（China Domestic Hardware Ecosystem）](#10-中国国产硬件生态专题china-domestic-hardware-ecosystem)
  - [10.1 国产NPU部署实践](#101-国产npu部署实践)
  - [10.2 国产开源模型端侧部署](#102-国产开源模型端侧部署)
- [11 课后练习与思考题（Exercises）](#11-课后练习与思考题exercises)
- [12 评估指标体系（Evaluation Metrics）](#12-评估指标体系evaluation-metrics)
- [13 端侧模型选型（2026 主流小模型）](#13-端侧模型选型2026-主流小模型)
- [14 端侧 Agent 与新范式（2026 前沿）](#14-端侧-agent-与新范式2026-前沿)
- [15 MCU / TinyML 极低功耗部署](#15-mcu--tinyml-极低功耗部署)
- [16 端侧扩散模型与图像生成](#16-端侧扩散模型与图像生成)
- [17 模型交付安全与 IP 保护](#17-模型交付安全与-ip-保护)
- [18 OS 系统 AI 运行时与共享基座](#18-os-系统-ai-运行时与共享基座)
- [19 模型分发与 OTA](#19-模型分发与-ota)
- [20 端侧检索与向量库](#20-端侧检索与向量库)
- [21 流式音视频交互管线](#21-流式音视频交互管线)
- [22 自定义算子与 Kernel 工程](#22-自定义算子与-kernel-工程)
- [23 车载与功能安全部署](#23-车载与功能安全部署)
- [24 端侧 MLOps 与质量门禁](#24-端侧-mlops-与质量门禁)
- [技术选型决策树](#技术选型决策树)
- [总结](#总结)

---

## 总览

大模型端侧部署旨在将大规模语言模型（LLM）及多模态模型高效运行在资源受限的终端设备上（手机、平板、嵌入式设备、车载平台等）。其核心挑战在于：**模型体积大、计算需求高、内存带宽受限、功耗预算严格**。以下从产业级视角，对端侧部署所涉及的全部技术进行系统性分类。

> **两份全景导读（覆盖本仓库全部技术 · 已合并定稿）**  
> - **学习地图**：[odd_learning_panorama.md](odd_learning_panorama.md) — 学什么、去哪练  
> - **零基础科普**：[odd_popular_science.md](odd_popular_science.md) — 生活比喻讲全部分类  
> （本文是技术详解主讲义，不替代上述两份导读。）

---

## 1 模型压缩（Model Compression）

> **目的**：在可接受的精度损失范围内，显著降低模型的存储体积、计算量和内存占用，使其能够在端侧设备上加载和运行。

### 1.1 量化（Quantization）

> **目的**：将模型权重和/或激活值从高精度浮点表示（FP32/FP16）映射到低精度整数表示（INT8/INT4/INT2等）或低比特浮点表示（FP8等），以减少存储空间和计算量，同时利用低精度运算单元获得更高吞吐。

📖 代码实践：[1.1_quantization.ipynb](01_model_compression/1.1_quantization.ipynb)

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

📖 代码实践：[1.2_pruning.ipynb](01_model_compression/1.2_pruning.ipynb)

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

📖 代码实践：[1.3_knowledge_distillation.ipynb](01_model_compression/1.3_knowledge_distillation.ipynb)

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

📖 代码实践：[1.4_low_rank_factorization.ipynb](01_model_compression/1.4_low_rank_factorization.ipynb)

- **SVD分解（Singular Value Decomposition）**
  - 原理：对权重矩阵进行奇异值分解 W = UΣV^T，保留前r个最大奇异值，得到 W ≈ U_r Σ_r V_r^T，参数量从mn降至r(m+n)。
- **Tucker分解**
  - 原理：对高维张量进行多模式分解，保留各模式的主成分，适合多维权重张量（如注意力权重）的压缩。
- **低秩重参数化（LoRA-style Factorization）**
  - 原理：冻结原始权重W，添加低秩增量 ΔW = AB，其中A∈R^{m×r}, B∈R^{r×n}。推理时可将AB合并回W，无额外推理开销。虽主要用于微调，但其低秩思想可用于压缩。

### 1.5 超低比特量化（Sub-2-bit Quantization）

> **前沿趋势（2025-2026）**：传统量化（INT8/INT4）已接近成熟，2025 年起，**1.58-bit 和 2-bit 量化**成为端侧部署的新前沿，目标是将 7B 模型压缩至 1-2GB，使手机能流畅运行。

📖 代码实践：[1.5_sub2bit_quantization.ipynb](01_model_compression/1.5_sub2bit_quantization.ipynb)

#### 1.5.1 BitNet 1.58-bit（三值量化）

- **核心思想**：权重仅取 {-1, 0, +1} 三个值，即 1.58 bit（log₂3 ≈ 1.585）。矩阵乘法退化为加减法，完全消除乘法运算。
- **训练方法**：从预训练 FP16 模型出发，通过量化感知训练（QAT）逐步将权重收敛到三值。关键技巧包括 LayerNorm 后量化、权重中心化预处理。
- **硬件收益**：MatMul 计算量降低 10x+，内存带宽降低 4-6x。联发科天玑 9500 已原生支持 1.58-bit 推理加速。
- **精度表现**：BitNet-b1.58-3B 在 MMLU 上与 FP16 Llama-2-3B 持平，部分任务超越。

#### 1.5.2 2-bit 产业级量化（HY-1.8B-2Bit）

- **腾讯混元 HY-1.8B-2Bit**（2026.02）：首个产业级 2-bit 端侧大模型，1.8B 参数仅占 ~600MB 内存，可在主流手机上流畅运行。
- **技术要点**：分组量化（group size=64）+ 非均匀量化码本 + 残差补偿。通过 2-bit QAT 保持精度，在 CMMLU/CEval 上接近 4-bit 基线。
- **1.25-bit Sherry**：结合 3:4 结构化稀疏（每 4 个权重保留 3 个非零），等效 1.25-bit，进一步压缩。

#### 1.5.3 QAT 成为标准实践

- **趋势转变**：2025 年前，量化以训练后量化（PTQ）为主流（AWQ/GPTQ）。2026 年起，Google Gemma 4、BitNet 等模型**原生采用 QAT 训练**，量化不再是"后处理"而是"训练的一部分"。
- **Gemma 4 的 INT4 QAT**：训练阶段即模拟 INT4 量化噪声，最终模型在 INT4 推理时精度损失 <1%，远优于 PTQ 方案。
- **端侧部署启示**：未来应优先选择原生量化训练的模型（如 Gemma 4 INT4 版本），而非对 FP16 模型做 PTQ。

### 1.6 torchao 与官方量化工具链

> **目的**：梳理 PyTorch 官方量化栈（`torchao`）与 ExecuTorch 的衔接方式，避免只掌握第三方 AWQ/GPTQ、却不会走官方端侧导出路径。

📖 代码实践：[1.6_torchao_toolchain.ipynb](01_model_compression/1.6_torchao_toolchain.ipynb)

- **Weight-only INT4/INT8**：对 Linear 权重做分组量化，激活保持 FP16/BF16，适合 decode 带宽受限场景。
- **静态/动态激活量化**：配合 XNNPACK / QNN Delegate，满足 NPU 对激活 INT8 的要求。
- **与生态分工**：
  - HuggingFace 研究流：AWQ / GPTQ / bitsandbytes
  - PyTorch 官方端侧流：`torchao` → `torch.export` → ExecuTorch
  - CPU GGUF 流：llama.cpp 自带量化工具
- **选型建议**：新项目若目标是 Android/iOS + ExecuTorch，优先 `torchao`；已有 GGUF 资产则继续 llama.cpp。

---

## 2 高效推理架构（Efficient Inference Architecture）

> **目的**：在不改变模型参数的前提下，通过优化推理过程中的计算策略和内存管理，显著提升推理速度和降低内存占用。

### 2.1 KV Cache 优化

> **基本原理**：自回归生成中，每步需访问之前所有token的Key/Value向量。KV Cache缓存已计算的KV以避免重复计算，但其内存占用随序列长度线性增长，成为长序列推理的核心瓶颈。

📖 代码实践：[2.1_kv_cache.ipynb](02_efficient_inference/2.1_kv_cache.ipynb)

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

#### 2.1.4 KV Cache 向量量化（TurboQuant, 2026）

- **TurboQuant（Google, 2026.03）**
  - 原理：结合 PolarQuant（极坐标量化）和 QJL（Quantized Johnson-Lindenstrauss 投影），对 KV Cache 做向量级量化压缩。不同于标量量化（逐元素量化），向量量化以组为单位映射到码本，信息保留率更高。
  - 效果：KV Cache 压缩 **6 倍**，精度损失近乎为零（<0.5% PPL 增加），在 H100 上实现 8 倍推理加速。
  - 端侧意义：长上下文场景（如端侧 RAG、长文档摘要）的 KV Cache 内存瓶颈被大幅缓解，使手机能处理 32K+ 上下文。

---

### 2.2 注意力机制优化

> **目的**：标准自注意力的计算复杂度为O(n²)，是长序列推理的核心瓶颈。优化注意力计算可显著降低延迟和内存。

📖 代码实践：[2.2_attention_optimization.ipynb](02_efficient_inference/2.2_attention_optimization.ipynb)

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

#### 2.2.4 多头潜在注意力（MLA, Multi-head Latent Attention）

- **MLA（DeepSeek 首创，DeepSeek-V2/V3 采用）**
  - 原理：将 Key/Value 投影到低维**潜在空间**（latent space），缓存压缩后的潜在向量而非原始 KV。推理时从潜在向量解压恢复 KV。KV Cache 压缩 **4-8 倍**。
  - 与 GQA/MQA 的区别：GQA/MQA 通过减少 KV 头数压缩（有精度损失），MLA 通过低秩投影压缩（近乎无损）。
  - 端侧价值：长上下文场景下 KV Cache 内存占用大幅降低，且推理质量不受影响。DeepSeek-V3 的 128K 上下文在端侧部署成为可能。

---

### 2.3 推理加速策略

📖 代码实践：[2.3_inference_acceleration.ipynb](02_efficient_inference/2.3_inference_acceleration.ipynb)

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

#### 2.3.4 结构化输出与语法约束（Structured Output & Grammar Constrained Decoding）

> **基本原理**：在端侧场景中，LLM 常用于 function calling、信息抽取、JSON 生成等结构化任务。语法约束解码（Grammar Constrained Decoding）在解码阶段强制输出符合预定义语法（JSON Schema、正则表达式、BNF 文法）的 token 序列，避免无效输出和重试，显著降低端侧推理成本。

- **GBNF 文法约束（llama.cpp）**
  - 原理：llama.cpp 支持 GBNF（GGML BNF）文法定义，在每步解码时将不符合文法的 token 概率置零，保证输出 100% 合规。常用于 JSON 生成、function calling 参数填充
  - 优势：无需微调模型，零精度损失，端侧开销极小（<5% 延迟增加）
  - 示例：定义 JSON Schema 文法 → llama.cpp 自动生成合规 JSON，无需 retry
- **Outlines / Guidance 库**
  - 原理：通过在 logits 层面施加约束（掩码非法 token），引导模型生成符合特定格式的输出。Outlines 将正则/JSON Schema 编译为 FSM（有限状态机），在每步解码时用 FSM 确定合法 token 集合
  - 端侧适用性：Outlines 支持 llama.cpp 后端，可与端侧量化模型配合使用
- **Function Calling 端侧实现**
  - 原理：通过 grammar 约束模型输出 function name + arguments 的 JSON 结构，端侧解析后调用本地 API（如日历、通讯录、传感器）
  - 挑战：端侧小模型的 function calling 能力弱于大模型，需结合 prompt engineering + grammar 约束 + few-shot 示例
- **token 节省效果**：结构化输出避免了"生成→解析失败→重试"的循环，在 function calling 场景可节省 30-60% 的 token 消耗，对端侧推理延迟和功耗有直接改善

---


### 2.4 Prefill / Decode 分治

> **目的**：端侧 LLM 的算力画像在两阶段截然不同，必须作为独立优化分类，而不是混在“推理加速”里顺带提一句。

- **Prefill（提示吞入）**：compute-bound 或中等高算强度；可批处理、可用 FlashAttention、可 NPU 大核。
- **Decode（逐 token）**：memory-bound；吃带宽与 KV；适合权重量化、KV 量化、投机解码。
- **工程实践**：
  - 导出两张图 / 两个 method（prefill graph & decode graph），ExecuTorch 等 Runtime 已常见
  - 动态 shape：prefill 按 bucket（128/256/512）编译；decode 固定 batch=1
  - 调度：预填充可短时提频，decode 阶段优先保带宽与温度（接第7.5章）

### 2.5 长上下文技术（Beyond KV Cache）

> **目的**：长上下文不只是“把 KV 压小”，还包括位置编码外推、注意力模式与上下文压缩策略。

- **位置编码外推**：YaRN / NTK-aware RoPE scaling / 位置插值；导出时需与训练配置一致
- **局部-全局混合注意力**：如滑动窗口 + 少量全局 token（Gemma 等）；实现要避免每步物理 shift KV
- **上下文压缩 / 摘要进缓存**：超限时将旧轮次摘要为短 system 片段再继续（Agent 刚需）
- **检索替代无限上下文**：超长文档优先第20章端侧检索，而不是硬扩到 128K 全进 KV

---

## 3 高效模型架构设计（Efficient Model Architecture）

> **目的**：从架构层面设计更适合端侧部署的模型，使其在参数量更少的情况下达到与大模型可比的性能。

### 3.1 轻量化架构设计

📖 代码实践：[3.1_lightweight_architecture.ipynb](03_efficient_architecture/3.1_lightweight_architecture.ipynb)

- **小参数量模型（Small Language Models, SLM）**
  - 原理：通过精心设计训练数据（高质量、高多样性）和训练策略，使小参数量模型（1B-3B）达到甚至超越更大模型的性能。代表：Phi系列、Gemma-2B、MiniCPM。
- **深度与宽度的最优权衡**
  - 原理：研究表明，在相同参数预算下，更深更窄的网络比浅更宽的网络更适合语言建模任务。如MobileLLM采用深而窄的设计。
  - **MobileLLM 深度洞察（Meta, 2024-2025）**：在 sub-1B（<10亿参数）规模下，**架构比参数量更重要**。125M/350M 参数模型采用 30-42 层深而窄的设计（hidden_size=576-1024），在零样本下游任务上超越同参数量的浅而宽模型 5-15%。关键发现：小模型需要"深度"来构建层次化表征，大模型则受益于"宽度"。
  - **共享注意力层（DeepSeek 风格）**：相邻若干层共享同一组注意力权重（仅 FFN 独立），在保持深层推理能力的同时减少参数量。DeepSeek-V2 采用此设计，端侧部署时只需加载一份注意力权重。
- **权重共享（Weight Sharing）**
  - **嵌入共享（Embedding Sharing / Tied Embeddings）**：输入嵌入层和输出lm_head共享权重矩阵，减少参数量。如GPT-2、Llama-3等采用此设计。
  - **跨层参数共享（Cross-Layer Parameter Sharing）**：多层Transformer共享相同的权重参数（如ALBERT风格的共享注意力权重和FFN权重），参数量大幅减少但层数不变，保留深层推理能力。端侧部署时共享权重只需加载一份，内存占用显著降低。
  - **量化码本共享（Codebook Sharing）**：在向量量化中，多个权重块共享同一组量化码本，减少码本存储开销。

### 3.2 线性注意力与亚二次复杂度架构

> **基本原理**：标准注意力的O(n²)复杂度限制了长序列推理。线性注意力通过kernel化或分解将复杂度降至O(n)，状态空间模型通过隐状态递推实现O(n)推理。

📖 代码实践：[3.2_linear_attention_ssm.ipynb](03_efficient_architecture/3.2_linear_attention_ssm.ipynb)

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

📖 代码实践：[3.3_moe.ipynb](03_efficient_architecture/3.3_moe.ipynb)

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


### 3.4 硬件感知 NAS 与一次训练多部署（Once-for-All / MCUNet）

> **目的**：在 MCU/手机档位差异大时，用搜索得到满足延迟/内存约束的子网，而不是只手工改宽度深度。

- **Once-for-All**：超网训练后按设备约束采样子网，免逐设备重训
- **MCUNet / TinyNAS**：联合搜索骨干与推理库调度，面向 KB–MB 级
- **延迟预测器**：用查表或小型回归模型估计端侧延迟，避免搜索时每次真机跑满
- **与本课程关系**：手机 LLM 更多是选现成 SLM（第13章）；NAS 在 TinyML（第15章）与 CV 骨干上更关键

---

## 4 编译与运行时优化（Compilation & Runtime Optimization）

> **目的**：通过编译器优化和运行时调度，将模型计算图映射到目标硬件上，最大化硬件利用率和推理吞吐。

### 4.1 计算图优化

📖 代码实践：[4.1_graph_optimization.ipynb](04_compilation_runtime/4.1_graph_optimization.ipynb)

- **算子融合（Operator Fusion）**
  - 原理：将多个连续算子合并为单个算子执行，减少中间结果的内存读写。如将QKV投影+RoPE+Attention融合为单个kernel，将Linear+LayerNorm融合等。
- **死代码消除（Dead Code Elimination）**
  - 原理：移除计算图中对最终输出无贡献的算子和分支，减少无效计算。
- **常量折叠（Constant Folding）**
  - 原理：在编译期将可确定的常量表达式预计算，将结果内联到图中，减少运行时计算。
- **内存布局优化（Memory Layout Optimization）**
  - 原理：调整张量的内存排布（如NCHW→NHWC）以匹配硬件的内存访问模式，减少cache miss。

### 4.2 针对硬件的代码生成

📖 代码实践：[4.2_code_generation.ipynb](04_compilation_runtime/4.2_code_generation.ipynb)

- **TVM / Apache TVM**
  - 原理：统一的深度学习编译器框架，通过搜索最优算子实现（AutoTVM/Ansor）为目标硬件生成高效代码。支持CPU、GPU、NPU等多种后端。
- **MLIR / XLA**
  - 原理：多级中间表示编译框架，通过逐级lowering将高层计算图逐步转换为目标硬件指令。XLA用于TensorFlow/JAX的图编译优化。
- **TensorRT**
  - 原理：NVIDIA推出的推理优化器，针对GPU进行层融合、精度校准、kernel自动调优，生成优化后的推理引擎。
- **Core ML Tools**
  - 原理：Apple的模型转换与优化工具，将训练好的模型转换为Core ML格式，针对Apple Silicon的CPU/GPU/Neural Engine进行优化。

### 4.3 内存优化

📖 代码实践：[4.3_memory_optimization.ipynb](04_compilation_runtime/4.3_memory_optimization.ipynb)

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

📖 代码实践：[5.1_npu_adaptation.ipynb](05_hardware_deployment/5.1_npu_adaptation.ipynb)

#### 5.1.1 NPU架构深潜

- **NPU核心组件**
  - MAC阵列：矩阵乘加速单元，NPU的核心计算引擎（256-4096个MAC单元，支持INT8/INT4）
  - 片上SRAM：高速片上缓存，存储激活值和部分权重（256KB-8MB，带宽>1TB/s）
  - DMA引擎：在DRAM和SRAM之间搬运数据（多通道并行，支持2D/3D传输）
  - 标量/向量处理器：执行softmax、LayerNorm、激活函数等（FP16/INT32）
- **主流NPU架构对比**
  - 高通Hexagon：V68 ISA，4x128 INT8 MAC，4MB SRAM，75 TOPS (8 Elite)，原生INT4支持
  - 苹果Neural Engine：数据流架构，16x128 INT8 MAC，~8MB SRAM (M4)，38 TOPS，FP16优化最佳
  - 华为昇腾：达芬奇架构3D Cube，16x16x16 Cube，2-8MB SRAM，128 TOPS (310P)
  - 联发科APU：Cadence DSP+自研加速，可配置MAC阵列，2-4MB SRAM，45 TOPS (9400)，天玑9500原生支持1.58-bit
- **2026年2nm芯片世代更新**
  - 骁龙8 Elite Gen 5（2025Q4）：3nm→2nm工艺，Hexagon V69，~60 TOPS (INT8)，原生INT4/1.58-bit加速
  - Apple A20（2025Q4）：2nm工艺，ANE 35+ TOPS，统一内存带宽提升至120 GB/s
  - 联发科天玑9500（2026Q1）：2nm工艺，~50 TOPS，首款原生支持BitNet 1.58-bit推理的移动芯片
  - 华为昇腾910C（2025）：5nm工艺，256 TOPS (INT8)，面向端云协同场景
- **NPU内存层次与数据流**
  - DRAM（4-16GB，30-120 GB/s）→ DMA异步传输 → SRAM（256KB-8MB，>1 TB/s）→ MAC寄存器（4-32KB，>10 TB/s）
  - 关键洞察：NPU性能瓶颈通常不在MAC阵列计算能力，而在DRAM→SRAM的数据搬运

#### 5.1.2 NPU算子兼容性与分解策略

- **LLM关键算子的NPU分解**
  - Multi-Head Attention → 拆分为QKV投影+注意力计算+输出投影（MatMul+Softmax+MatMul+Concat）
  - RoPE → 预计算cos/sin表，分解为逐元素乘加（Elementwise Mul+Add）
  - SwiGLU → 拆分为两个线性层+SiLU+逐元素乘（MatMul+SiLU+Elementwise Mul）
  - RMSNorm → 分解为平方+求和+开方+归一化（Pow+Reduce+Div+Mul）
  - Top-K Sampling → 回退CPU（NPU不支持动态排序）
- **CPU回退代价模型**：$T_{\text{fallback}} = T_{\text{NPU}\to\text{CPU}} + T_{\text{CPU}} + T_{\text{CPU}\to\text{NPU}}$，即使1-2个算子回退也可能成为整体推理瓶颈

#### 5.1.3 NPU量化适配

- **各NPU精度支持**
  - 高通Hexagon：权重INT8/INT4，激活INT8/FP16，MAC吞吐75 TOPS (INT8)
  - 苹果ANE：权重FP16/INT8，激活FP16，FP16推理效率最高
  - 华为昇腾：权重INT8/INT4，激活INT8/INT16，128 TOPS (INT8)
  - 联发科APU：权重INT8/INT16，激活INT8/FP16，无INT4支持
- **混合精度量化配置优化**：$\min_{(W_b, A_b)} \text{Size}(W_b) \quad \text{s.t.} \quad \text{Accuracy}(W_b, A_b) \geq \text{threshold} \quad \text{and} \quad (W_b, A_b) \in \text{NPU\_Supported}$

#### 5.1.4 NPU部署管线

- **通用部署管线**：模型导出 → 算子兼容性检查 → 计算图优化 → 量化 → NPU编译 → 精度验证 → 性能Profile → 部署打包
- **各厂商SDK对比**
  - 高通QNN：ONNX→QNN IR→QNN量化→QNN编译→Context Binary→QNN Runtime
  - 苹果Core ML：coremltools转换→ANE优化→Xcode编译→Core ML Framework
  - 华为CANN：ONNX→AMCT量化→ATC编译→OM模型→ACL推理引擎

#### 5.1.5 动态Shape处理与内存管理

- **动态Shape解决方案**
  - Padding+Mask：编译一次运行时零开销，短序列浪费算力
  - 多shape编译：为常用shape分别编译，运行时选择最接近的
  - Dynamic Batch Dispatch：prefill和decode分别编译，decode固定batch=1+seq_len=1
- **KV Cache内存管理**：NPU不支持动态内存分配，需编译期预分配最大KV Cache空间；PagedAttention在NPU上难以直接映射（不支持非连续内存访问）

#### 5.1.6 NPU性能Profile与调试

- **Profile方法论**：算子级耗时（QNN Profiler/msprof）、内存占用（SRAM使用率、DRAM访问量）、功耗（硬件功耗计）、精度验证（逐层余弦相似度>0.999）
- **常见瓶颈与优化**：CPU回退（算子分解）、SRAM溢出（Tiling优化）、MAC利用率低（增大batch/算子融合）、DMA瓶颈（双缓冲/权重预取）、量化精度损失（混合精度）

#### 5.1.7 异构调度与CPU+NPU协同

- **典型分工**：Token Embedding(CPU) + QKV/Attention/FFN(NPU) + TopK/Sampling(CPU) + KV Cache管理(CPU)
- **异构调度策略**：子图级调度（共享内存传递数据）、流水线并行（NPU计算第i层时CPU准备第i+1层）、双缓冲（NPU处理当前batch时DMA预取下一batch权重）
- **CPU↔NPU数据搬运优化**：共享内存零拷贝、异步DMA计算与搬运重叠、算子融合减少子图数量

#### 5.1.8 实际部署性能基准（2025年数据）

| 模型 | 量化 | 平台 | Prefill | Decode (tok/s) | 内存占用 |
|------|------|------|---------|---------------|----------|
| Qwen2.5-1.5B | W4A16 | 骁龙8 Elite NPU | ~15ms/512tok | 25-35 | ~1.2GB |
| Qwen2.5-3B | W4A16 | 骁龙8 Elite NPU | ~30ms/512tok | 15-20 | ~2.2GB |
| Llama-3.1-8B | W4A16 | 骁龙8 Elite NPU | ~80ms/512tok | 8-12 | ~5GB |
| Phi-3-mini-3.8B | W4A16 | M4 MacBook ANE | ~25ms/512tok | 20-30 | ~2.8GB |
| Qwen2.5-7B | W8A8 | 昇腾310P | ~40ms/512tok | 12-18 | ~8GB |

### 5.2 端侧部署框架

📖 代码实践：[5.2_deployment_frameworks.ipynb](05_hardware_deployment/5.2_deployment_frameworks.ipynb)

#### 5.2.1 llama.cpp / GGUF生态

- **GGUF格式核心设计**
  - mmap零拷贝加载：操作系统将文件直接映射到进程地址空间，加载时间O(1)
  - K-Quant混合量化：两级量化设计（super-block 256权重 + sub-block 32权重），在相同比特数下比均匀量化精度更高
  - 元数据嵌入：词表、超参数等元数据嵌入文件，无需额外配置文件
- **K-Quant原理**：super-block存储全局scale（FP16精度），sub-block存储局部scale和offset（FP16精度），权重数据为4/5/6-bit整数。Q4_K_M是7B模型部署的最常用格式
- **llama.cpp关键优化**：mmap加载、量化GEMV kernel（手写AVX2/NEON汇编）、KV Cache环形缓冲区、连续批处理、多后端支持（CPU/CUDA/Metal/Vulkan/SYCL）

#### 5.2.2 ExecuTorch (PyTorch端侧部署)

- **架构**：torch.export → ExportedProgram → to_edge + partition → Partitioned Graph (Per-Backend) → compile + bundle → .pte File → On-Device Inference
- **Delegate机制**：XNNPACK Delegate（CPU）、QNN HTA Delegate（高通Hexagon NPU）、Core ML Delegate（苹果ANE）、Vulkan Delegate（GPU）
- **异构分区原理**：将计算图G划分为子图，每个子图分配到最优后端：$b_i = \arg\min_{b \in B} \text{Latency}(G_i, b)$
- **轻量运行时**：端侧运行时仅约100KB，适合资源受限设备

#### 5.2.3 MLC-LLM (编译期优化部署)

- **核心思想**：基于Apache TVM，将模型编译为目标硬件的原生代码（AOT编译），而非解释执行
- **编译流程**：HuggingFace Model → TVM Relay IR → 算子融合+常量折叠+内存规划 → Target Codegen (Metal/CUDA/Vulkan) → .so/.dylib
- **量化格式**：q4f16_1（权重INT4+激活FP16）是最常用配置
- **vs llama.cpp vs ExecuTorch**：MLC-LLM AOT编译性能更优但NPU支持有限；llama.cpp JIT解释执行更灵活且CPU推理最成熟；ExecuTorch Delegate机制NPU支持最好

#### 5.2.4 ONNX导出与推理

- **ONNX在LLM部署中的角色**：模型转换的通用中间站，PyTorch→ONNX→QNN/CANN/TensorRT/ONNX Runtime/OpenVINO
- **关键问题**：自定义算子（RoPE/SwiGLU需分解或注册）、动态shape（dynamic_axes参数）、精度损失（验证$\|f(x) - f_{ONNX}(x)\|_\infty < 10^{-5}$）、KV Cache（作为输入/输出传递）

#### 5.2.5 Core ML (Apple端侧部署)

- **Core ML LLM部署流程**：PyTorch → coremltools转换 → .mlpackage → Core ML优化（权重量化/ANE调度）→ .mlmodelc → Core ML Runtime（ANE优先→GPU→CPU）
- **特殊考量**：ANE对FP16效率最高（INT8反而可能更慢）、State API支持KV Cache跨步传递、iOS App模型文件建议<4GB、iPhone总内存限制约4-6GB

#### 5.2.6 其他重要框架

| 框架 | 目标 | LLM支持 | NPU支持 | 量化 | 最佳场景 |
|------|------|---------|---------|------|----------|
| **llama.cpp/GGUF** | CPU通用 | ★★★★★ | ★ | Q2-Q8 K-Quant | CPU推理, 快速原型 |
| **MLC-LLM** | CPU/GPU | ★★★★ | ★★ | q4f16_1 | GPU推理优化 |
| **ExecuTorch** | CPU/NPU/GPU | ★★★ | ★★★★ | INT8/INT4 | PyTorch生态, 移动端多后端 |
| **ONNX Runtime** | CPU/GPU/NPU | ★★★ | ★★★ | INT8 (QDQ) | 通用推理, NPU delegate |
| **Core ML** | ANE/GPU/CPU | ★★★ | ★★★★★ | FP16/INT8 | iOS/macOS, ANE加速 |
| **NCNN** | ARM CPU | ★★ | ★ | INT8 | CV模型, ARM极致优化 |
| **MNN** | CPU/GPU/NPU | ★★★ | ★★★ | INT8/INT4 | 移动端多模态 |

#### 5.2.7 产业级部署工程实践

- **精度保障**：逐层对比余弦相似度>0.999、端到端PPL增加<0.5、回归测试
- **常见陷阱**：动态shape（NPU编译失败）、算子不兼容（分解/替换/自定义算子）、量化格式不兼容（使用目标框架自带量化工具）、内存泄漏（KV Cache释放）、热节流（功耗管理）、并发安全（运行时线程安全）
- **CI/CD集成**：自动导出→自动量化→精度验证→性能基准→打包发布
- **版本管理**：模型版本、框架版本、配置版本、A/B测试

#### 5.2.15 MLX (Apple Silicon 原生框架)

- **核心定位**：Apple 官方开源的机器学习框架，专为 Apple Silicon（M1-M4/M7-A18 Pro）统一内存架构设计，是 macOS/iOS 端侧 LLM 部署的事实标准
- **统一内存优势**：MLX 直接利用 Apple Silicon 的统一内存架构（CPU/GPU/ANE 共享同一物理内存），无需 CPU↔GPU 数据拷贝。M2 Max 96GB 统一内存可加载 70B INT4 模型，这是同价位 GPU 无法实现的
- **关键设计**：
  - **惰性计算（Lazy Evaluation）**：MLX 采用类似 PyTorch 的 eager 接口，但内部构建计算图并惰性执行，支持自动算子融合
  - **动态图 + 即时编译**：运行时通过 Metal Performance Shaders 生成优化的 GPU kernel，无需预编译
  - **量化支持**：支持 INT4/INT8/FP16 混合精度量化，`mlx-lm` 库提供一键量化工具
  - **模型格式**：使用 safetensors 存储权重，配置使用 JSON，无需专用二进制格式
- **mlx-lm 工具链**：
  - `mlx_lm.load()` → 加载 HuggingFace 模型并自动转换
  - `mlx_lm.quantize()` → AWQ/RTN 量化
  - `mlx_lm.generate()` → 流式生成，支持 KV Cache
  - `mlx_lm.server` → OpenAI 兼容 API 服务
- **vs Core ML**：Core ML 面向移动端 ANE 优化但 LLM 支持有限（State API 复杂）；MLX 面向 Apple Silicon GPU，LLM 生态更成熟（支持 Llama/Qwen/Mistral 等）。iOS 18.2+ 的 Apple Intelligence 部分功能基于 MLX 技术栈
- **性能参考**：M4 Max 运行 Llama-3-8B INT4 约 40-50 tokens/s；M2 Ultra 运行 Llama-3-70B INT4 约 8-12 tokens/s

#### 5.2.16 Qualcomm AI Hub

- **核心定位**：高通官方的端侧 AI 模型分发与部署平台，简化 QNN（Qualcomm Neural Network）SDK 的使用复杂度
- **核心功能**：
  - **模型仓库**：提供预优化的模型库（LLM/CV/Audio），已针对骁龙平台预编译
  - **一键部署**：`qai-hub` CLI 工具支持从 HuggingFace 模型到骁龙 NPU 部署的完整流程
  - **云端编译**：在 Qualcomm 云端将模型编译为 QNN 图，避免本地安装 QNN SDK
  - **设备管理**：支持 USB/WiFi 连接的真机调试和性能分析
- **LLM 部署流程**：
  1. `qai-hub get-model` → 从模型仓库获取预优化 LLM
  2. `qai-hub submit-job` → 在云端编译为 QNN 图（指定目标芯片如 Snapdragon 8 Gen 3）
  3. `qai-hub download-job` → 下载编译后的模型到设备
  4. 通过 QNN Runtime 或 llama.cpp QNN 后端执行推理
- **与 ExecuTorch 的关系**：ExecuTorch 的 QNN Delegate 底层调用 QNN SDK；AI Hub 提供更上层的封装（模型管理、云端编译、性能分析），但灵活性不如 ExecuTorch 直接编程
- **适用场景**：快速原型验证（用预编译模型）、生产部署（用云端编译优化）、性能基准（用 AI Hub 的 profiling 工具）

#### 5.2.17 框架对比总结（更新）

| 框架 | 目标 | LLM支持 | NPU支持 | 量化 | 最佳场景 |
|------|------|---------|---------|------|----------|
| **llama.cpp/GGUF** | CPU通用 | ★★★★★ | ★ | Q2-Q8 K-Quant | CPU推理, 快速原型 |
| **MLC-LLM** | CPU/GPU | ★★★★ | ★★ | q4f16_1 | GPU推理优化 |
| **ExecuTorch** | CPU/NPU/GPU | ★★★ | ★★★★ | INT8/INT4 | PyTorch生态, 移动端多后端 |
| **ONNX Runtime** | CPU/GPU/NPU | ★★★ | ★★★ | INT8 (QDQ) | 通用推理, NPU delegate |
| **Core ML** | ANE/GPU/CPU | ★★★ | ★★★★★ | FP16/INT8 | iOS/macOS, ANE加速 |
| **MLX** | Apple GPU | ★★★★★ | ★★ | INT4/INT8/FP16 | macOS Apple Silicon, 大模型 |
| **Qualcomm AI Hub** | 骁龙NPU | ★★★ | ★★★★★ | INT4/INT8 | 骁龙平台快速部署 |
| **NCNN** | ARM CPU | ★★ | ★ | INT8 | CV模型, ARM极致优化 |
| **MNN** | CPU/GPU/NPU | ★★★ | ★★★ | INT8/INT4 | 移动端多模态 |
| **CoreAI** (2026) | Apple全栈 | ★★★★★ | ★★★★★ | INT4/INT8/FP16 | iOS/macOS, 替代Core ML, 比MLX快2.47x |
| **LiteRT-LM** (2026) | Android CPU/NPU | ★★★★ | ★★★★ | INT4/INT8 | TFLite演进版, 内存降30%+ |
| **Ollama** | CPU/GPU | ★★★★★ | ★ | Q4_K_M等 | 极简部署, 一行命令运行模型 |


#### 5.2.18 厂商系统栈补全（联发科 / Google AI Edge / 三星）

| 栈 | 定位 | 备注 |
|----|------|------|
| **MediaTek NeuroPilot** | 天玑 APU 工具链 | 与 BitNet 1.58-bit 叙事需核对芯片世代 |
| **Google AI Edge / LiteRT** | Android 官方演进路径 | AICore 负责系统模型；App 侧 LiteRT 委托 GPU/NPU |
| **Samsung Gauss / Galaxy AI** | 垂直整合 | 常走“系统预置 + 端云混合”，App 可调用的是能力 API 而非裸权重 |

选型提醒：能走系统 API 就不要重复内嵌同尺寸基座（接第18章共享基座）。

---

### 5.3 硬件感知优化

📖 代码实践：[5.3_hardware_aware.ipynb](05_hardware_deployment/5.3_hardware_aware.ipynb)

#### 5.3.1 Roofline模型深度分析

- **数学基础**：性能上界 $P_{\max} = \min(I \cdot \text{BW}, \text{Peak FLOPS})$，拐点 $I_{\text{threshold}} = \frac{\text{Peak FLOPS}}{\text{BW}}$
- **不同硬件的Roofline特征**
  - 高通Hexagon NPU：75 TOPS, 60 GB/s, 拐点=1250 FLOP/B → 大多数LLM算子memory-bound
  - Apple M4 ANE：38 TOPS, 120 GB/s, 拐点=317 FLOP/B → ANE带宽优势
  - ARM Cortex-A715：0.5 TFLOPS, 40 GB/s, 拐点=12.5 FLOP/B → 几乎全部memory-bound
  - NVIDIA RTX 4090：165 TFLOPS, 1008 GB/s, 拐点=164 FLOP/B → 大多数LLM算子compute-bound
- **关键洞察**：端侧NPU/CPU的拐点远高于云端GPU，量化（减少数据搬运）在端侧效果更显著

#### 5.3.2 内存层次优化

- **Tiling策略**：将大算子按SRAM容量切分为小tile，最大化数据在SRAM中的复用次数，最小化DRAM访问次数
- **Flash Attention Tiling**：通过分块计算+running max/sum统计，避免O(L²)的SRAM需求，将SRAM需求从O(L²)降至O(Bq×Bk)
- **GEMM Tiling**：将矩阵乘C=AB按tile大小切分，每个tile的A块在SRAM中被复用N/Tn次，DRAM访问量从O(MNK)降至O(MNK/T)

#### 5.3.3 双缓冲与流水线优化

- **双缓冲原理**：将SRAM分为两个buffer，NPU计算Buffer A时DMA预取下一层到Buffer B，交换指针后立即开始下一层计算
- **延迟隐藏条件**：$T_{\text{DMA}} \leq T_{\text{compute}}$，compute-bound场景效果最好，memory-bound场景效果有限
- **优化叠加效果**：INT4量化(4x) + 双缓冲(1.5-2x) + 算子融合(1.2x) ≈ 8-10x decode加速

#### 5.3.4 量化对硬件性能的影响

- **量化改变算术强度**：INT4量化将权重搬运量减少4x，算术强度提升约4x，使算子向compute-bound区域移动
- **量化加速效果**：Decode(batch=1)带宽受限→INT4加速~3-4x；Prefill(batch=4)计算受限→INT4加速~1.0-1.5x；KV Cache带宽受限→KV量化加速~2-4x
- **混合精度MAC利用率**：W4A8是NPU最优配置（INT4权重+INT8激活，MAC利用率400%，带宽需求25%）

#### 5.3.5 功耗预算优化

- **功耗模型**：$P = \alpha C V^2 f + V I_{\text{leak}}$，端侧需在TDP内最大化性能
- **热节流机制**：手机NPU TDP 3-5W，降频阈值~45°C，降频后性能降至50-70%
- **功耗优化策略**
  - DVFS：降低f和V，功耗按V²f降低，20-40%功耗降低
  - 精度自适应：温度低→W4A16，温度高→W4A8，30-50%功耗降低
  - 推理调度：交互式请求NPU立即执行，后台请求CPU低频延迟执行
  - 模型切换：温度低→7B模型，温度高→1.5B模型，40-60%功耗降低

#### 5.3.6 硬件感知模型设计

- **量化友好架构**：GQA/MQA（减少KV头数）、ReLU/GELU（替代SiGLU/SwiGLU）、共享嵌入（量化一次）
- **NPU友好架构**：hidden_dim对齐2的幂（MAC阵列效率更高）、GQA（减少KV数量）、固定长度/padding（NPU编译期需固定shape）
- **硬件感知NAS**：$\min_{\theta} \mathcal{L}(\theta) \quad \text{s.t.} \quad \text{Latency}(\theta, H) \leq T_{\text{budget}} \quad \text{and} \quad \text{Memory}(\theta) \leq M_{\text{budget}}$

#### 5.3.7 优化策略选择矩阵

| 瓶颈类型 | Prefill (compute-bound) | Decode (memory-bound) |
|---------|----------------------|---------------------|
| **首选优化** | 算子融合 / Flash Attention | 量化 (W4A16) |
| **次选优化** | 增大batch / 张量并行 | KV量化 / 权重预取 |
| **进阶优化** | 硬件感知NAS | 双缓冲 / 算子融合 |
| **量化效果** | 有限 (~1.2x) | 显著 (~3-4x) |

### 5.4 硬件基准测试与选型

> **目的**：系统化的硬件基准测试是端侧部署选型的基础。通过四层测试体系（微基准→核函数→模型→压力），在多维度（性能、内存、功耗、生态、成本）上对候选硬件进行数据驱动的评估。

📖 代码实践：[5.4_hardware_benchmarking.ipynb](05_hardware_deployment/5.4_hardware_benchmarking.ipynb)

#### 5.4.1 四层基准测试体系

| 层级 | 测试内容 | 测量对象 | 典型耗时 |
|------|---------|---------|---------|
| **微基准 (Micro)** | 单算子（GEMM/Attention）峰值性能 | Roofline参数 | 5-10分钟 |
| **核函数基准 (Kernel)** | 完整推理步骤(prefill/decode) | 算子融合+内存优化效果 | 30-60分钟 |
| **模型基准 (Model)** | 完整模型端到端性能 | TTFT、吞吐、内存峰值、功耗 | 2-4小时 |
| **压力基准 (Stress)** | 长时间运行(1-24h)稳定性 | 热节流、内存泄漏、性能退化 | 1-24小时 |

#### 5.4.2 五维评估框架

| 维度 | 权重(推理) | 关键指标 |
|------|-----------|---------|
| **性能** | 35% | TTFT <500ms, ITL <50ms, 吞吐 >15 tok/s |
| **内存** | 25% | 可用内存、带宽、SRAM容量、KV Cache预算 |
| **功耗** | 20% | TDP、能效比(tok/J)、热节流比例 |
| **生态** | 10% | SDK成熟度、算子覆盖率、社区活跃度 |
| **成本** | 10% | 芯片成本、开发成本、维护成本 |

#### 5.4.3 关键性能指标

- **TTFT (Time To First Token)**：首token延迟，prefill阶段效率指标，端侧目标<500ms
- **ITL (Inter-Token Latency)**：token间延迟，decode阶段效率指标，端侧目标<50ms
- **P99长尾延迟**：99%请求的最大延迟，比平均值更能反映用户体验
- **持续性能vs峰值性能**：30分钟压力测试后的稳态性能，由于热节流通常只有峰值的50-70%

#### 5.4.4 GEMM微基准与Roofline分析

通过测量不同M/N/K尺寸的GEMM性能，确定硬件的实际Roofline参数：

- **Decode阶段 (M=1)**：算术强度极低（~1-10 FLOP/B），几乎全部memory-bound → 量化收益最大
- **Prefill阶段 (M=512+)**：算术强度高（~50-200 FLOP/B），compute-bound → 量化收益有限
- **Ridge Point**：端侧NPU（1000+ FLOP/B）远高于云端GPU（~150 FLOP/B），端侧量化加速效果更显著

#### 5.4.5 硬件选型速查

| 场景 | 首选硬件 | 量化 | 预期性能 |
|------|---------|------|----------|
| 旗舰手机AI助手 | 骁龙8 Elite / A18 Pro | W4A16 | 1.5B@30tok/s, 3B@18tok/s |
| 中端手机 | 骁龙7 Gen3 / 天玑8300 | W4A16 | 1.5B@20tok/s |
| 平板/笔记本 | M4 / 骁龙X Elite | W4A16 | 3B@30tok/s, 7B@12tok/s |
| 边缘服务器 | Jetson Orin / 昇腾310P | W4A8 | 7B@15tok/s |
| IoT/低成本 | RK3588 | W8A8 | 0.5B@5tok/s |

#### 5.4.6 CI/CD集成与性能回归检测

产业级部署必须将基准测试自动化到CI/CD流水线中，关键阈值：

| 指标 | 回归阈值 | 动作 |
|------|---------|------|
| TTFT | 增加>20% | 阻止合并 |
| 吞吐 | 下降>15% | 阻止合并 |
| 内存峰值 | 增加>10% | 警告 |
| 功耗 | 增加>20% | 警告 |

---

## 6 模型格式与序列化（Model Format & Serialization）

> **目的**：高效的模型存储格式直接影响加载速度、内存占用和跨平台兼容性。

📖 代码实践：[6.0_model_format.ipynb](06_model_format/6.0_model_format.ipynb) · [6.1_model_versioning.ipynb](06_model_format/6.1_model_versioning.ipynb)

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

📖 代码实践：[7.1_edge_cloud_inference.ipynb](07_edge_cloud/7.1_edge_cloud_inference.ipynb)

- **模型拆分推理（Split Computing / Model Splitting）**
  - 原理：将模型按层拆分，浅层在端侧执行，深层在云端执行。中间特征上传至云端而非原始数据，兼顾隐私和计算效率。
- **自适应推理路由（Adaptive Inference Routing）**
  - 原理：根据输入复杂度和端侧负载动态决定推理在端侧还是云端执行。简单请求端侧处理，复杂请求路由到云端。
- **推测验证协同（Edge-Cloud Speculative Decoding）**
  - 原理：端侧小模型作为draft model生成候选token，云端大模型并行验证，减少云端计算量和通信轮次。
- **端侧 RAG（On-Device Retrieval-Augmented Generation）**
  - 原理：在端侧设备上构建轻量级检索增强生成管线，从本地知识库（文档、笔记、邮件等）检索相关片段，注入 LLM prompt 生成回答。全程数据不出端，兼顾隐私和个性化
  - **端侧向量数据库**：使用 SQLite + sqlite-vss 或 ChromaDB 嵌入式模式存储文档向量，支持万级文档的毫秒级检索。向量维度通常压缩到 384-768（如 all-MiniLM-L6-v2 嵌入模型）
  - **嵌入模型部署**：端侧部署轻量嵌入模型（如 MiniLM 23M 参数、BGE-small 33M 参数），FP16 约 50-70MB，INT8 约 25-35MB
  - **分块策略**：端侧文档通常较短（笔记/邮件），采用 256-512 token 固定分块 + 50 token 重叠，避免跨块语义断裂
  - **上下文管理**：端侧 LLM 上下文窗口有限（通常 2K-4K），需严格控制检索片段数量（top-2 到 top-5）和长度（每片段 200-300 token）
  - **增量索引**：用户数据持续产生，需支持增量插入和索引更新。sqlite-vss 支持 INSERT 触发器自动更新向量索引
  - **隐私优势**：所有检索和生成在端侧完成，用户数据不上传云端，满足 GDPR/CCPA 合规要求

### 7.2 多模态端侧部署

📖 代码实践：[7.2_multimodal_deployment.ipynb](07_edge_cloud/7.2_multimodal_deployment.ipynb)

- **视觉语言模型压缩（VLM Compression）**
  - 原理：对视觉编码器（如ViT）和语言模型分别进行量化和压缩，视觉编码器通常可更激进量化。如LLaVA的端侧部署。
- **多模态融合优化**
  - 原理：优化视觉特征和语言特征的融合方式，减少跨模态交互的计算开销。如使用更轻量的投影层、压缩视觉token数量。
- **音频/语音模型端侧部署**
  - 原理：Whisper等语音模型的端侧量化与部署，流式处理优化，低延迟语音交互。
- **多模态 Token 剪枝（Token Pruning, 2025-2026）**
  - **视觉 Token 剪枝（IDPruner）**：视觉语言模型中，ViT 产生的视觉 token 数量庞大（如 576 个），但很多 token 对当前任务贡献低。IDPruner 借鉴最大边际相关性（MMR）算法，动态选择与文本 query 最相关的视觉 token 子集，将视觉 token 减少 50-70%，推理速度提升 1.5-2x，精度损失 <1%。
  - **音频 Token 合并（Samp）**：将相邻的音频 token 合并为代表性 token，减少音频序列长度，适用于端侧 Whisper/音频 LLM 部署。
  - **端侧意义**：多模态模型的核心瓶颈是视觉/音频 encoder 产生的 token 过多，token 剪枝使手机能流畅运行多模态推理。

### 7.3 隐私与安全

📖 代码实践：[7.3_privacy_security.ipynb](07_edge_cloud/7.3_privacy_security.ipynb)

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

📖 代码实践：[7.4_inference_service.ipynb](07_edge_cloud/7.4_inference_service.ipynb) · 配套监控：[7.4_edge_monitoring.ipynb](07_edge_cloud/7.4_edge_monitoring.ipynb)

- **请求排队与优先级调度**
  - 原理：端侧设备可能同时服务多个应用（如语音助手、实时翻译、文本补全），需要根据请求优先级和延迟要求进行调度。高优先级交互式请求优先处理，低优先级后台任务延后执行。
- **多模型共存内存管理**
  - 原理：端侧可能同时部署多个模型（如基础对话模型+专用任务模型），需要在有限内存中管理多模型权重的加载/卸载。通过权重共享、时分复用、按需加载等策略最大化内存利用率。
- **推理超时与降级策略**
  - 原理：当端侧推理延迟超过阈值时，自动降级到更小的模型或路由到云端，保证用户体验。降级策略包括：切换低精度模型、减少推理层数（early exit）、回退到云端推理。
- **模型热更新与A/B测试**
  - 原理：端侧模型需要在不中断服务的情况下更新。通过双缓冲加载（新模型在后台加载，加载完成后原子切换）实现热更新；通过流量分配实现A/B测试，逐步验证新模型效果。

### 7.5 功耗管理与电池感知调度

> **目的**：端侧设备的电池约束是硬性限制，需要系统化的功耗管理策略来最大化推理时长和用户体验。

📖 代码实践：[7.5_power_battery.ipynb](07_edge_cloud/7.5_power_battery.ipynb)（配套热节流实测见 [5.4_hardware_benchmarking.ipynb](05_hardware_deployment/5.4_hardware_benchmarking.ipynb)）

#### 7.5.1 功耗建模

芯片功耗由动态功耗和静态功耗两部分组成：

$$P = \alpha C V^2 f + V I_{\text{leak}}$$

其中：
- $\alpha$：活动因子（active factor），取决于执行的操作类型
- $C$：等效电容
- $V$：供电电压
- $f$：工作频率
- $I_{\text{leak}}$：漏电流

**LLM推理的功耗特征**：
- Prefill阶段：计算密集型，功耗较高（接近TDP）
- Decode阶段：内存带宽密集型，功耗较低（通常为TDP的50-70%）
- NPU推理功耗远低于CPU/GPU（能效比高3-10倍）

#### 7.5.2 DVFS（动态电压频率调节）

- 原理：动态调整NPU/CPU的频率$f$和电压$V$，功耗按$V^2f$降低，在满足延迟要求的前提下最小化功耗
- 实现：根据推理负载的紧迫程度选择不同的频率档位，如交互式请求使用高频、后台请求使用低频
- 收益：典型配置可降低20-40%功耗

#### 7.5.3 电池感知调度策略

| 电池电量 | 调度策略 | 预期效果 |
|---------|---------|---------|
| >50% | 全速推理，最大模型 | 最佳精度 |
| 20-50% | 切换中等模型，降低分辨率 | 平衡精度与续航 |
| 10-20% | 仅核心功能，最小模型 | 延长续航 |
| <10% | 仅云端推理或禁用AI | 保护可用性 |

#### 7.5.4 精度自适应与功耗的权衡

| 温度/电量条件 | 量化配置 | 功耗降低 | 精度影响 |
|-------------|---------|---------|---------|
| 正常 | W4A16 (INT4权重+FP16激活) | 基线 | 几乎无损 |
| 高温/低电 | W4A8 (INT4权重+INT8激活) | 30-50% | 轻微损失 |
| 极端 | 回退到1.5B模型 | 40-60% | 可接受 |

### 7.6 WebAssembly与浏览器端推理

> **目的**：WebAssembly (WASM) 和 WebGPU 技术的发展使得在浏览器中运行 AI 模型成为现实，这是端侧部署的新兴重要场景。

📖 代码实践：[7.6_browser_wasm.ipynb](07_edge_cloud/7.6_browser_wasm.ipynb) · 浏览器骨架：[browser_demo/index.html](07_edge_cloud/browser_demo/index.html)

#### 7.6.1 技术栈概览

| 技术 | 角色 | 特点 |
|------|------|------|
| **WASM** | CPU推理运行时 | 接近原生性能，跨浏览器兼容 |
| **WebGPU** | GPU加速推理 | 更低延迟，最新浏览器支持 |
| **WebNN** | NPU推理API | 标准化NPU访问，W3C草案阶段 |
| **ONNX Runtime Web** | 推理引擎 | 自动选择WASM/WebGPU后端 |

#### 7.6.2 主流浏览器端推理框架

| 框架 | 引擎 | 量化支持 | 特点 |
|------|------|---------|------|
| **WebLLM** | Apache TVM WebGPU | W4A16 | 端到端聊天界面，Mistral/Llama支持 |
| **Transformers.js** | ONNX Runtime Web | INT8 | HuggingFace生态兼容 |
| **MediaPipe LLM** | 自研 WebGPU | W4A16 | Google出品，Gemma/Phi优化 |
| **llama.cpp (WASM)** | 手写SIMD | Q4_K_M | 成熟稳定，社区活跃 |

#### 7.6.3 浏览器端推理的优势与局限

**优势**：
1. 零安装：用户打开网页即可使用，无需下载App
2. 隐私：数据完全留在浏览器，不上传服务器
3. 跨平台：适用于所有现代浏览器（Chrome、Edge、Safari、Firefox）
4. 分发简单：模型文件通过CDN分发

**局限**：
1. 内存限制：WASM默认可寻址4GB，浏览器Tab有更严格限制（通常1-2GB）
2. 模型加载慢：首次加载需从CDN下载（可配合Service Worker缓存）
3. 性能差距：WASM比原生慢1.5-2×，WebGPU受限于浏览器调度
4. 算子覆盖：部分算子无WASM/WebGPU实现

#### 7.6.4 Chrome内置AI（Gemini Nano）

Chrome 126+ 直接内置Gemini Nano模型（约3B参数），通过Prompt API提供本地AI能力：
- 零下载：模型预装在Chrome中
- 本地执行：完全离线可用
- API简洁：`const session = await ai.languageModel.create()`

### 7.7 端侧语音全链路（ASR-LLM-TTS）

> **目的**：真实语音助手不是“只跑一个 LLM”，而是 **唤醒/KWS → ASR → LLM/NLU → TTS** 的流水线；任一段延迟或内存失控都会毁掉体验。多模态笔记本覆盖了部件，本节把全链路系统约束补齐。

📖 代码实践（部件与调度）：[7.2_multimodal_deployment.ipynb](07_edge_cloud/7.2_multimodal_deployment.ipynb)

- **延迟预算分解（端到端 <500ms 交互）**
  - KWS：常驻、极小模型（MCU/DSP，见第15章）
  - 流式 ASR：边听边出 partial transcript，TTFT 与端点检测（VAD）解耦
  - LLM：流式 token；首 token 预算通常 <200ms
  - TTS：流式声码器，不必等 LLM 整句结束
- **内存共存策略**：三模型很少同时常驻；ASR 结束后可卸载 encoder，TTS 与 LLM 分时或共享 CPU/NPU
- **量化组合经验**：ASR INT8、LLM INT4、TTS FP16/INT8（声学对量化更敏感时保 FP16）
- **失败降级**：ASR 低置信 → 云端识别；LLM 超时 → 模板回复；TTS 失败 → 文本展示

---

## 8 端侧训练与个性化（On-Device Training & Personalization）

> **目的**：在端侧设备上对模型进行微调和个性化适配，使模型更好地服务本地用户，同时保护用户数据隐私。

### 8.1 参数高效微调（PEFT）

📖 代码实践：[8.1_peft.ipynb](08_on_device_training/8.1_peft.ipynb)

- **LoRA / QLoRA**
  - 原理：冻结预训练权重，仅训练低秩适配器矩阵。QLoRA进一步将基座模型量化为4bit（NF4格式），仅适配器保持高精度（BF16），端侧训练显存需求极低。QLoRA的核心是双重量化（double quantization）和分页优化器（paged optimizer），使7B模型在24GB显存上可训练。
- **Adapter**
  - 原理：在Transformer层中插入小型适配器模块（下投影-非线性-上投影），仅训练适配器参数。
- **Prefix Tuning / Prompt Tuning**
  - 原理：在输入前添加可训练的虚拟token/prefix，仅训练这些少量参数。
- **IA³（Infused Adapter by Inhibiting and Amplifying）**
  - 原理：通过可学习的向量对注意力层的Key/Value和FFN的输出进行逐元素缩放（amplify或inhibit），参数量比LoRA更少（仅训练3个向量），适合极低资源的端侧微调。

### 8.2 端侧训练优化

📖 代码实践：[8.2_training_optimization.ipynb](08_on_device_training/8.2_training_optimization.ipynb)

- **选择性反向传播（Selective Backpropagation）**
  - 原理：仅对部分层进行反向传播，冻结其余层，减少训练的计算量和内存占用。
- **梯度累积与混合精度**
  - 原理：端侧内存有限，通过小batch+梯度累积模拟大batch效果；使用FP16/BF16混合精度减少训练内存占用。
- **内存高效优化器**
  - 原理：使用8bit优化器（如8-bit AdamW）、节省内存的优化器（如Sophia、Lion），降低优化器状态的内存占用。
- **梯度检查点（Gradient Checkpointing）**
  - 原理：前向传播时不保存中间激活值，仅保存关键检查点的输出，反向传播时从检查点重新计算所需激活。以约30%的额外计算换取60%+的内存节省，是端侧训练最关键的内存优化技术之一。

### 8.3 端侧评估与个性化

> **目的**：端侧模型需要持续适应用户的个性化需求，同时避免灾难性遗忘和隐私泄漏。

📖 代码实践：[8.3_on_device_eval.ipynb](08_on_device_training/8.3_on_device_eval.ipynb)

- **灾难性遗忘防御**
  - 原理：端侧微调时，新数据上的训练可能导致模型遗忘预训练知识。防御方法包括：EWC（Elastic Weight Consolidation，对重要参数施加L2正则约束）、MAS（Memory Aware Synapses，基于输出敏感度评估参数重要性）、经验回放（保留少量旧数据混合训练）。
- **端侧数据高效利用**
  - 原理：端侧数据通常稀缺且分布偏斜。通过数据增强（同义词替换、回译等）、合成数据生成（用模型自身生成训练样本）、主动学习（选择最有信息量的样本标注）来提升数据效率。
- **个性化与隐私的权衡**
  - 原理：更强的个性化通常需要更多用户数据，增加隐私风险。通过差分隐私微调（在梯度中添加噪声）、联邦学习（数据不出端）、最小化适配器参数量（仅LoRA的少量参数包含用户信息）来在个性化和隐私间取得平衡。
- **用户画像与条件生成**
  - 原理：通过轻量级用户画像模块（如可学习的user embedding或soft prompt），在推理时根据用户特征条件化模型输出，无需修改模型权重即可实现个性化。

---


### 8.4 多适配器路由（一基座多 LoRA）

> **目的**：系统或超级 App 内同时服务翻译、写作、代码等技能时，用适配器路由替代多模型常驻。

- **路由策略**：意图分类（小模型/规则）→ `adapter_id`；未知意图走 base
- **内存**：同一时间只激活 1–2 个 LoRA；LRU 淘汰（接第7.4章）
- **冲突**：同一 base 上多 LoRA 可合并（加法）或切换；注意任务负迁移
- **与第18章**：系统级共享 base 时，adapter 成为 App 个性化的主载荷（也是 OTA 最小单元，第19章）

---

## 9 端到端实战与故障排查（E2E Deployment & Troubleshooting）

> **目的**：将前述所有技术串联成完整的端到端部署流水线，并提供系统化的故障排查方法论，使学习者具备独立完成端侧部署项目的能力。

### 9.1 端到端部署流水线

> **目的**：从原始PyTorch模型出发，经历量化→导出→编译→部署→验证的完整流程，涵盖GPU和NPU两条路径。

📖 代码实践：[9.1_end_to_end_deployment.ipynb](09_end_to_end/9.1_end_to_end_deployment.ipynb)

#### 9.1.1 标准端侧部署流程

```
原始PyTorch模型（FP16/FP32）
        │
        ├──→ 路径A：GPU端侧（手机GPU/笔记本GPU）
        │       │
        │       ├── Step 1: AWQ/GPTQ量化 → W4A16
        │       ├── Step 2: 导出GGUF格式
        │       ├── Step 3: llama.cpp加载推理
        │       └── Step 4: 精度验证+性能基准
        │
        ├──→ 路径B：NPU端侧（高通骁龙/苹果ANE/华为昇腾）
        │       │
        │       ├── Step 1: SmoothQuant量化 → W8A8
        │       ├── Step 2: 导出ONNX
        │       ├── Step 3: NPU编译器编译（QNN/Core ML/CANN）
        │       └── Step 4: 精度验证+性能基准
        │
        └──→ 路径C：浏览器端
                │
                ├── Step 1: 导出ONNX
                ├── Step 2: ONNX Runtime Web转换
                └── Step 3: WebGPU/WASM推理
```

#### 9.1.2 各阶段关键检查点

| 阶段 | 检查项 | 通过标准 |
|------|--------|---------|
| 量化后 | 权重余弦相似度 | >0.999（逐层） |
| 量化后 | Perplexity变化 | <+0.5（WikiText-2） |
| 导出后 | ONNX推理一致性 | $\|f_{torch} - f_{onnx}\|_\infty < 10^{-5}$ |
| 编译后 | NPU推理一致性 | >0.999（逐层余弦相似度） |
| 部署后 | 端到端TTFT | <500ms（目标场景） |
| 部署后 | 端到端ITL | <50ms（目标场景） |

#### 9.1.3 实战案例清单

| 案例 | 模型 | 量化 | 目标硬件 | 关键挑战 |
|------|------|------|---------|---------|
| 案例1 | Qwen2.5-1.5B | W4A16 GPTQ | 骁龙8 Elite | GGUF导出+CPU推理 |
| 案例2 | Llama-3.2-3B | W8A8 SmoothQuant | 高通Hexagon NPU | QNN算子兼容性 |
| 案例3 | Phi-3-mini | FP16 | 苹果ANE (Core ML) | ANE算子适配 |
| 案例4 | Qwen2.5-7B | Q4_K_M | Jetson Orin | 内存管理+KV Cache |

#### 9.1.4 各平台标准化检查清单

**GPU端侧（llama.cpp/GGUF）**：
- [ ] 量化完成，PPL变化<0.5
- [ ] GGUF文件大小符合预期
- [ ] mmap加载正常（查看加载时间<1s）
- [ ] 生成结果与原始模型一致（BLEU>0.95）
- [ ] 内存峰值在设备容量的70%以内

**NPU端侧（QNN/Core ML/CANN）**：
- [ ] ONNX导出成功，无动态shape报错
- [ ] 算子兼容性检查通过（支持率>95%）
- [ ] NPU编译器编译成功
- [ ] 逐层精度对比>0.999
- [ ] NPU推理不出现CPU回退（或回退<2个算子）

**浏览器端**：
- [ ] ONNX模型体积<500MB
- [ ] WASM/WebGPU推理正常
- [ ] Service Worker缓存命中率>90%（二次访问）
- [ ] 首Token延迟<2s（含模型加载）

### 9.2 故障排查与调试方法

> **目的**：端侧部署的调试难度远高于服务器端（无法直接print、日志受限、设备异构），需要系统化的排查方法论。

📖 代码实践：[9.2_troubleshooting_debug.ipynb](09_end_to_end/9.2_troubleshooting_debug.ipynb)

#### 9.2.1 常见问题分类与排查

##### 类型一：内存不足（OOM）

| 症状 | 可能原因 | 排查方法 | 解决方案 |
|------|---------|---------|---------|
| 模型加载即OOM | 量化后模型仍过大 | 计算模型理论大小，对比设备可用内存 | 降低量化比特（INT8→INT4）、切换更小模型 |
| 推理中间OOM | KV Cache增长 | 监控KV Cache增长曲线 | KV量化、滑动窗口、H2O淘汰 |
| 长时间运行后OOM | 内存泄漏 | 监控内存增长趋势 | 检查KV Cache释放、模型热更新逻辑 |

##### 类型二：精度异常

| 症状 | 可能原因 | 排查方法 | 解决方案 |
|------|---------|---------|---------|
| 输出乱码/重复 | 量化精度损失过大 | 逐层对比余弦相似度 | 混合精度量化（敏感层FP16） |
| 某些输入正常，某些异常 | 离群值通道未保护 | 检查激活分布 | SmoothQuant/W4A16→保护离群值通道 |
| NPU输出与CPU不一致 | 算子实现差异 | 逐算子对比，定位差异算子 | 使用CPU回退该算子，或换用等效算子 |

##### 类型三：性能不达标

| 症状 | 可能原因 | 排查方法 | 解决方案 |
|------|---------|---------|---------|
| TTFT过长 | Prefill计算慢 | Profile各层耗时 | Flash Attention、增大batch |
| ITL过长 | Decode带宽受限 | 检查MAC利用率 | 量化（核心方法）、KV量化 |
| 持续运行后性能下降 | 热节流 | 监控温度曲线 | DVFS降频、间歇推理、小模型切换 |

##### 类型四：框架/编译错误

| 症状 | 可能原因 | 排查方法 | 解决方案 |
|------|---------|---------|---------|
| ONNX导出失败 | 动态shape/自定义算子 | 检查trace vs scripting | torch.export / 算子分解 |
| NPU编译失败 | 不支持的算子 | 检查算子兼容性列表 | 算子分解、CPU回退 |
| 运行时crash | SDK版本不匹配 | 检查驱动/SDK版本矩阵 | 对齐版本、使用Docker |

#### 9.2.2 逐层精度对比方法

```python
# 精度排查的核心方法：逐层对比输出
for layer_name, (fp_output, q_output) in zip(layer_names, layer_outputs):
    cos_sim = F.cosine_similarity(fp_output, q_output)
    if cos_sim < 0.999:  # 阈值
        print(f"⚠ {layer_name}: cos_sim={cos_sim:.6f} — 量化损失过大!")
```

#### 9.2.3 NPU算子回退的代价估算

$$T_{\text{fallback}} = T_{\text{NPU}\to\text{CPU}} + T_{\text{CPU}} + T_{\text{CPU}\to\text{NPU}}$$

单个算子的CPU回退可能引入10-50ms额外延迟，若1-2个算子回退将成为整体推理瓶颈。因此优先使用算子分解/等效替换，仅在无替代时回退CPU。

#### 9.2.4 调试工具速查

| 工具 | 用途 | 平台 |
|------|------|------|
| PyTorch Profiler | 算子级耗时分析 | GPU/CPU |
| QNN Profiler | 高通NPU算子耗时 | 骁龙 |
| msprof | 华为昇腾NPU算子耗时 | 昇腾 |
| Instruments (Xcode) | ANE利用率、内存 | Apple |
| ONNX Runtime Profiling | ONNX推理瓶颈 | 通用 |

---

## 10 中国国产硬件生态专题（China Domestic Hardware Ecosystem）

> **目的**：在中国市场部署端侧AI模型，需要了解国产NPU芯片和国产开源模型的特性，制定针对性的适配方案。

📖 代码实践：[10.1_china_npu.ipynb](10_china_hardware/10.1_china_npu.ipynb)

### 10.1 国产NPU部署实践

#### 10.1.1 华为昇腾（Ascend）全栈部署

| 组件 | 说明 |
|------|------|
| **硬件** | 昇腾310P（边缘）、昇腾910B（云端推理） |
| **推理引擎** | ACL (Ascend Computing Language) |
| **量化工具** | AMCT (Ascend Model Compression Toolkit)：支持量化感知训练和训练后量化 |
| **编译工具** | ATC (Ascend Tensor Compiler)：将ONNX/Caffe模型编译为OM离线模型 |
| **部署流程** | PyTorch → ONNX → AMCT量化 → ATC编译 → OM模型 → ACL推理 |

**昇腾端侧部署关键注意事项**：
- 动态shape支持有限，推荐使用固定shape + padding方案
- OM模型是预编译格式，设备加载即可推理，无需在线编译
- 支持INT8和INT4量化，推荐W8A8配置
- 关注算子支持度：部分LLM自定义算子（如GELU变体）需要分解

#### 10.1.2 寒武纪（Cambricon）MLU

| 组件 | 说明 |
|------|------|
| **硬件** | MLU370（边缘推理卡） |
| **SDK** | Cambricon Neuware |
| **推理框架** | MagicMind（算子融合+编译优化） |
| **量化支持** | INT8/INT16，支持逐通道量化 |
| **部署流程** | PyTorch → ONNX → MagicMind编译 → 离线模型 → CNRT推理 |

#### 10.1.3 地平线（Horizon Robotics）

| 组件 | 说明 |
|------|------|
| **硬件** | Journey系列（车载AI芯片）、Sunrise系列（AIoT） |
| **SDK** | Horizon Open Explorer (OE) 开发包 |
| **推理框架** | HBDK (Horizon BPU Development Kit) |
| **量化特点** | 强制INT8量化，专有量化校准方法 |
| **适用场景** | 车载座舱AI、机器人视觉+语言 |

#### 10.1.4 瑞芯微（Rockchip）RK系列

| 组件 | 说明 |
|------|------|
| **硬件** | RK3588（6 TOPS NPU）、RK3576 |
| **SDK** | RKNN-Toolkit2 |
| **推理框架** | RKNN Runtime |
| **量化** | 支持FP16/INT8，仅权重INT8 |
| **适用模型** | 极小语言模型（0.5B-1.5B），以视觉模型为强项 |

#### 10.1.5 国产NPU选型速查

| NPU | 算力 (TOPS) | 内存 | 功耗 | 量化 | 适用模型 | 最佳场景 |
|-----|-----------|------|------|------|---------|---------|
| 昇腾310P | 128 | 8-32GB | 12W | INT8/INT4 | 1.5B-7B | 边缘服务器 |
| 寒武纪MLU370 | 48 | 8-24GB | 75W | INT8/INT16 | 1.5B-7B | 云端+边缘 |
| 地平线J6 | 34 | 4-8GB | 15W | INT8 | 0.5B-1.5B | 车载AI |
| RK3588 | 6 | 2-8GB | 5W | INT8/FP16 | 0.5B-1.5B | IoT低成本 |

### 10.2 国产开源模型端侧部署

#### 10.2.1 主流国产模型端侧部署特性

| 模型 | 参数量 | 架构特点 | 推荐量化 | 推荐硬件 | 关键注意 |
|------|--------|---------|---------|---------|---------|
| **Qwen2.5** | 0.5B-7B | GQA、SwiGLU、RoPE | W4A16 AWQ | 骁龙8 Elite / 昇腾310P | GQA天然友好，无特殊注意事项 |
| **DeepSeek** | 1.5B-7B | MLA (Multi-head Latent Attention) | W4A16 | 骁龙/昇腾/M4 | MLA需自定义attention kernel |
| **MiniCPM** | 1B-3B | 深而窄+WSD调度 | W4A16 | 骁龙7+ | 为端侧设计，开箱即用 |
| **ChatGLM** | 1.5B-4B | 双向位置编码 | W8A8 SmoothQuant | 骁龙8系列 | 位置编码需NPU适配 |
| **Yi** | 1.5B-6B | 标准LLaMA架构 | Q4_K_M (llama.cpp) | CPU推理 | 架构标准，GGUF导出顺利 |

#### 10.2.2 模型格式生态

| 平台 | 分发格式 | 量化 | 社区 |
|------|---------|------|------|
| ModelScope | SafeTensors+config | 多种 | 中国最大模型社区 |
| HuggingFace | SafeTensors+config | 多种 | 国际主流 |
| Gitee AI | 多种格式 | 有限 | 国产替代方案 |
| 各厂商自有 | 自研格式 | 厂商量化 | 仅供厂商SDK使用 |

---

## 11 课后练习与思考题（Exercises）

> **目的**：通过动手实践和深度思考，巩固各章节学到的方法论，培养独立解决端侧部署问题的能力。

### 第1章 模型压缩

**动手题**：
1. 实现对同一个LLaMA-3.2-1B模型分别使用逐张量INT4、逐组INT4和GPTQ量化，比较三者的PPL和输出余弦相似度
2. 使用Hessian迹方法对6层Transformer进行混合精度分配，验证不同比特组合的精度-存储效率

**思考题**：
1. 为什么SmoothQuant将激活的量化难度"迁移"到权重？这种迁移的代价是什么？
2. AWQ和GPTQ都利用校准数据，它们的根本区别是什么？为什么AWQ不需要Hessian逆而GPTQ需要？

### 第2章 高效推理架构

**动手题**：
1. 实现PagedAttention的连续批处理调度器，展示内存利用率从60%提升到95%
2. 对比滑动窗口(4096)和无限制KV Cache在不同序列长度下的内存占用，绘制增长曲线

**思考题**：
1. H2O淘汰策略保留"最近窗口"和"历史高注意力token"，为什么单独任何一种策略都不够？
2. 在计算资源极度受限的端侧，Flash Attention是否仍然有效？为什么？

### 第3章 高效模型架构

**动手题**：
1. 实现一个GQA版本的注意力（从MHA 32头改为GQA 4组），测量KV Cache的内存节省
2. 用MoE架构（4个expert，Top-2路由）替换标准FFN，对比相同参数量下的推理速度

**思考题**：
1. SSM（如Mamba）声称O(n)复杂度，为什么在实际端侧部署中可能不比优化的Transformer快？
2. MoE模型的总参数量可以达到大模型水平，但端侧推理时只有部分专家活跃，为什么依然难以在手机上部署Mixtral 8x7B？

### 第4章 编译与运行时优化

**动手题**：
1. 使用torch.compile对一个小型Transformer进行编译优化，对比编译前后的推理速度
2. 手动实现算子融合（QKV投影+注意力），测量融合前后的内存和延迟变化

**思考题**：
1. 为什么NPU上PagedAttention难以直接映射？有什么可能的解决方案？
2. 激活重计算用计算换内存，端侧设备上计算和内存哪个更稀缺？如何据此决定重计算策略？

### 第5章 硬件部署

**动手题**：
1. 用5.4提供的Roofline分析工具，为骁龙8 Elite和M4分别绘制Roofline图，标注典型LLM算子的位置
2. 使用硬件选型决策框架，为"车载语音助手（7B模型，要求<30ms ITL）"选出最佳硬件方案

**思考题**：
1. 端侧NPU的Ridge Point（1000+ FLOP/B）远高于GPU（~150 FLOP/B），这对部署策略有何影响？
2. 芯片的标称TOPS（峰值算力）和实际LLM推理性能之间为什么存在巨大差距？

### 第6章 模型格式与序列化

**动手题**：
1. 将同一个PyTorch模型分别导出为ONNX、SafeTensors和TorchScript格式，对比文件大小、加载速度和跨平台兼容性
2. 实现一个简单的模型版本管理器，支持版本号校验、哈希验证和A/B测试流量分配

**思考题**：
1. GGUF格式为什么能在端侧部署中成为事实标准？其mmap零拷贝加载的设计相比SafeTensors有何优劣？
2. 在模型迭代频繁的生产环境中，如何设计模型版本管理策略来平衡存储成本和回滚效率？

### 第7章 端云协同

**动手题**：
1. 用 7.4 推理服务笔记本实现：交互请求优先于后台总结，并在 2.4GB 内存预算下完成 LLM↔文生图切换
2. 用 7.5 笔记本为 SoC=15%、T=48°C 推导调度策略，并估算单轮对话耗电
3. 打开 `browser_demo/index.html`，对照 7.6 说明 WebGPU 与 WASM 的选型边界

**思考题**：
1. 端云协同推理中，中间特征传输替代原始数据上传，是否真正保护了用户隐私？攻击者能从中间特征重建原始输入吗？
2. 浏览器端推理（WebGPU vs WASM）与原生App推理相比，在哪些场景下是更优选择？

### 第8章 端侧训练

**动手题**：
1. 使用QLoRA对一个1B模型进行个性化微调（模拟用户数据），测量训练内存和速度

**思考题**：
1. 端侧微调带来个性化能力的同时，为什么可能导致灾难性遗忘？如何检测和防止？
2. 联邦学习中"梯度"传输替代"数据"传输，差分隐私如何防止梯度泄漏用户信息？

### 第9章 端到端实战与故障排查

**动手题**：
1. 按照第9.1节的标准流程，将一个1.5B模型从PyTorch导出到GGUF并在llama.cpp上运行，记录每一步的检查点验证结果
2. 人为制造一个量化精度异常（如对敏感层使用过大group_size），使用逐层余弦相似度方法定位并修复问题

**思考题**：
1. 在端到端部署流水线中，量化、导出、编译三个阶段各有哪些常见的失败模式？如何建立自动化检测机制？
2. NPU部署时CPU回退代价高昂，如何在编译期就预测和最小化回退算子数量？

### 第10章 中国国产硬件生态

**思考题**：
1. 华为昇腾的OM模型是预编译格式（编译期固定shape），这与端侧LLM推理的动态序列长度需求如何协调？有哪些工程解决方案？
2. 国产NPU（昇腾/寒武纪/地平线）在LLM算子支持度上与高通Hexagon存在差距，这对国产模型（如Qwen、DeepSeek）的端侧部署有何影响？如何弥补？

### 第12章 评估指标体系

**动手题**：
1. 设计一个端侧部署的综合评估打分系统，为性能（TTFT/ITL/吞吐）、内存、功耗、精度四个维度分配权重，并对两个候选方案打分比较
2. 实现一个自动化基准测试脚本，测量模型在不同输入长度（128/256/512/1024）下的TTFT和ITL，并绘制延迟-序列长度曲线

**思考题**：
1. 在交互式对话场景和后台批处理场景中，TTFT和吞吐量哪个更重要？如何根据场景调整评估指标的权重？
2. 能效比（tokens/J）在电池供电设备上是关键指标，但测量它需要硬件功耗计。在没有专用硬件的情况下，如何通过软件手段估算能效比？

### 第13章 端侧模型选型

**动手题**：
1. 用 13.1 选型器为「车载中文语音助手，可用内存 2.5GB，需要工具调用」给出 Top-3，并说明否决项
2. 将同一场景的 bits 从 4 改为 2，观察候选集合如何变化

### 第14章 端侧 Agent

**动手题**：
1. 扩展 14.1 Agent：新增 `get_location` 工具，并用 JSON 约束保证参数合法
2. 为 Agent 对话设计 KV 预算：超过 N token 时触发摘要压缩（可用伪代码）

**思考题**：
1. 端侧 Agent 为何比单轮聊天更容易 OOM？列出至少三条缓解路径。

### 第15章 MCU / TinyML

**动手题**：
1. 估算 TinyKWS INT8 模型能否放入 256KB SRAM（含激活 arena），并给出裁剪建议
2. 设计“MCU 唤醒 → AP 拉起 ASR+LLM”的状态机

### 第16章 端侧扩散

**动手题**：
1. 比较 50/8/4 步采样的延迟，给出手机相册场景的步数建议
2. 设计 LLM 与 SD-Turbo 的分时内存策略（参考 7.4）

### 第17章 模型交付安全

**动手题**：
1. 用 17.1 流水线演示：篡改权重被拒、换设备 license 失败
2. 讨论水印能否单独充当 DRM，为什么？

### 第18章 OS 系统 AI 运行时

**动手题**：
1. 用 18.1 演示多 App 适配器并存，并在预算内触发 LRU 驱逐
2. 说明为何系统预置基座优于每个 App 各嵌一份同尺寸模型

### 第19章 模型分发与 OTA

**动手题**：
1. 模拟分片下载中断后从 ledger 续传
2. 比较“全量基座 OTA”与“仅 LoRA OTA”的流量与风险

### 第20章 端侧检索

**动手题**：
1. 为私有文档建简易索引，并强制上下文 token 预算裁剪
2. 讨论何时用暴力检索 vs HNSW/sqlite-vec

### 第21章 流式音视频管线

**动手题**：
1. 走通 barge-in 状态迁移，并核算首包语音是否 <800ms
2. 列出车载免提场景缺少 AEC 时的失败模式

### 第22章 自定义算子

**动手题**：
1. 把 RMSNorm 拆成可下沉的标准算子序列，并做数值对齐
2. 估算 5% CPU 回退对端到端延迟的影响

### 第23章 车载功能安全

**动手题**：
1. 用看门狗仿真超时进入安全态
2. 设计“LLM 建议”与“安全执行器”的隔离边界图

### 第24章 端侧 MLOps

**动手题**：
1. 跑通导出/量化/设备三道 gate，故意让一道失败并阻止 release
2. 定义 10 条金样本（含工具调用）与通过率阈值

### 综合实战

1. 独立完成一个完整的端侧部署项目：选择3B模型 → AWQ量化 → 导出GGUF → llama.cpp部署 → 基准测试 → 撰写部署报告

---

## 12 评估指标体系（Evaluation Metrics）

> **目的**：系统化的评估指标是端侧部署技术选型和优化的基础。不同应用场景对精度、延迟、内存、功耗的优先级不同，需要综合评估。

📖 代码实践：[12.1_evaluation_metrics.ipynb](12_evaluation/12.1_evaluation_metrics.ipynb)

### 12.1 延迟指标

| 指标 | 定义 | 典型目标 |
|------|------|---------|
| **首Token延迟（TTFT, Time To First Token）** | 从输入发送到第一个输出token生成的延迟，反映prefill阶段效率 | 交互式场景 < 200ms |
| **Token间延迟（ITL, Inter-Token Latency）** | 生成连续两个token之间的延迟，反映decode阶段效率 | 实时对话 < 50ms/token |
| **端到端延迟（E2E Latency）** | 从输入发送到完整输出生成的总延迟 | 取决于输出长度和场景 |

### 12.2 吞吐指标

| 指标 | 定义 | 典型参考 |
|------|------|---------|
| **吞吐量（Throughput）** | 单位时间生成的token数（tokens/s），受batch size和序列长度影响 | 骁龙8 Gen3 INT4 7B模型约 10-20 tokens/s |
| **并发请求数** | 同时处理的推理请求数量，反映服务能力 | 端侧通常1-4个并发 |

### 12.3 资源指标

| 指标 | 定义 | 典型参考 |
|------|------|---------|
| **内存峰值（Peak Memory）** | 推理过程中的最大内存占用（模型权重+KV Cache+激活值） | 7B INT4模型约 4-5GB |
| **模型体积（Model Size）** | 量化后模型文件的存储大小 | 7B INT4约 3.5-4GB, 7B INT8约 7GB |
| **功耗（Power）** | 推理过程中的芯片功耗 | 移动端NPU推理约 2-5W |
| **能效比（Energy Efficiency）** | 每焦耳生成的token数（tokens/J），衡量能量利用效率 | NPU推理能效比远高于CPU/GPU |

### 12.4 精度指标

| 指标 | 定义 | 用途 |
|------|------|------|
| **Perplexity** | 模型对测试集的困惑度，越低越好 | 量化/剪枝前后精度损失的核心度量 |
| **下游任务准确率** | 在具体任务（MMLU、HumanEval等）上的表现 | 评估实际应用能力 |
| **量化前后差异** | 量化模型与原始模型输出的KL散度或余弦相似度 | 量化算法选择的参考 |

### 12.5 典型场景参考数据

| 模型 | 量化 | 硬件平台 | 推理速度 | 内存占用 | Perplexity变化 |
|------|------|---------|---------|---------|---------------|
| Llama-2-7B | W4A16 (AWQ) | RTX 4090 | ~80 tokens/s | ~4GB | +0.1~0.3 |
| Llama-2-7B | W4A16 (GPTQ) | RTX 4090 | ~75 tokens/s | ~4GB | +0.1~0.5 |
| Llama-2-7B | W8A8 (SmoothQuant) | 骁龙8 Gen3 CPU | ~5-8 tokens/s | ~7GB | +0.05~0.2 |
| Llama-2-7B | Q4_K_M (llama.cpp) | M2 MacBook Air | ~15-20 tokens/s | ~4.5GB | +0.2~0.5 |
| Phi-3-mini-3.8B | Q4_K_M | 骁龙8 Gen3 NPU | ~20-30 tokens/s | ~2.5GB | +0.1~0.3 |

> 注：以上数据为典型值，实际性能因实现、驱动版本和测试条件而异，仅供参考。

---

## 13 端侧模型选型（2026 主流小模型）

> **目的**：2025-2026 年涌现了大量高质量小模型（SLM），选对模型是端侧部署成功的第一步。本章对比当前主流的端侧可用模型，提供选型参考。

📖 代码实践：[13.1_model_selection.ipynb](13_model_selection/13.1_model_selection.ipynb)

### 13.1 纯文本模型

| 模型 | 参数量 | 量化后体积 | 上下文 | 特点 | 端侧推荐场景 |
|------|--------|-----------|--------|------|-------------|
| **Gemma 4 E2B** | 2B | ~1.2GB (INT4) | 8K | Google原生QAT训练，INT4精度极佳 | Android通用对话 |
| **Gemma 4 E4B** | 4B | ~2.2GB (INT4) | 8K | "Agent原生"设计，工具调用强 | 端侧Agent/工具调用 |
| **Phi-4** | 14B | ~7GB (INT4) | 16K | GPQA超越GPT-4o，推理能力强 | 高端设备复杂推理 |
| **Qwen3-4B** | 4B | ~2.3GB (INT4) | 32K | 中文最强4B，支持长上下文 | 中文场景首选 |
| **Qwen3-8B** | 8B | ~4.5GB (INT4) | 128K | 支持超长上下文+MLA | 长文档处理 |
| **MiniCPM 3.0** | 4B | ~2.2GB (INT4) | 32K | 多模态支持，中文优秀 | 多模态端侧 |
| **Llama 3.2 1B** | 1B | ~0.7GB (INT4) | 128K | 极轻量，低端设备可用 | 低端手机/手表 |
| **Llama 3.2 3B** | 3B | ~1.7GB (INT4) | 128K | 生态最成熟，社区支持广 | 通用部署 |
| **DeepSeek-Coder-V2-Lite** | 16B MoE(2.4B激活) | ~3GB (INT4) | 128K | 代码补全专精 | 端侧代码助手 |
| **HY-1.8B-2Bit** | 1.8B | ~0.6GB (2-bit) | 4K | 2-bit量化，极致压缩 | 低端设备 |

### 13.2 多模态模型

| 模型 | 参数量 | 模态 | 特点 |
|------|--------|------|------|
| **Gemma 4 多模态版** | 4B | 文+图 | 首款手机可跑的多模态大模型 |
| **MiniCPM-V 3.0** | 4B+ViT | 文+图 | 中文多模态优秀，OCR能力强 |
| **Phi-3-Vision** | 4B+ViT | 文+图 | 文档理解强，适合办公场景 |

### 13.3 选型决策建议

- **中文场景**：Qwen3-4B（通用）/ MiniCPM 3.0（多模态）
- **英文场景**：Gemma 4 E2B（轻量）/ Phi-4（高性能设备）
- **代码补全**：DeepSeek-Coder-V2-Lite
- **Agent/工具调用**：Gemma 4 E4B
- **低端设备（<4GB可用内存）**：Llama 3.2 1B / HY-1.8B-2Bit
- **长上下文（>32K）**：Qwen3-8B（128K + MLA）

---

## 14 端侧 Agent 与新范式（2026 前沿）

> **趋势**：2026 年端侧 AI 从"单轮问答"进化为"多轮 Agent"——模型能自主调用工具、规划步骤、执行任务，全程在设备上完成，无需云端。

📖 代码实践：[14.1_edge_agent.ipynb](14_edge_agent/14.1_edge_agent.ipynb)

### 14.1 端侧 Agent 架构

- **核心能力**：Function Calling（工具调用）+ 多轮规划 + 状态管理
- **端侧挑战**：
  - **上下文管理**：Agent 多轮对话的 KV Cache 持续增长 → 需 TurboQuant/MLA 压缩
  - **工具调用延迟**：每步需生成结构化 JSON → 需 GBNF 语法约束解码（见 2.3.4）
  - **内存预算**：Agent 框架本身占用内存 → 需极小模型（<4B）
- **代表模型**：Gemma 4 E4B（Agent 原生设计）、Qwen3（强 Function Calling）

### 14.2 端侧 RAG 与 Agent 结合

- **架构**：用户 Query → 端侧 RAG 检索知识 → Agent 规划 → 工具调用 → 生成回答
- **全链路端侧**：向量检索（SQLite-VSS/ChromaDB）+ LLM 推理 + 工具执行，全程离线
- **应用场景**：离线智能助手、隐私敏感的文档问答、车载语音 Agent

### 14.3 联邦学习与端侧持续进化

- **联邦学习（Federated Learning）**：多设备协同训练，梯度聚合在云端，原始数据不出端
- **2026 进展**：Google 联邦学习框架支持 LLM 的 LoRA 参数联邦聚合，实现端侧模型持续个性化
- **端侧 Agent 自进化**：Agent 在使用中积累经验（成功/失败的轨迹），通过端侧 LoRA 微调持续优化

### 14.4 部署工具生态（2026 更新）

- **Ollama**：一行命令运行模型（`ollama run gemma4`），支持模型融合、GPU 内存共享，端侧原型开发首选
- **LM Studio**：图形界面管理模型，支持 GGUF/MLX 多格式，适合非技术用户
- **Apple CoreAI**（WWDC 2026）：替代 Core ML 的统一 AI 推理框架，比 MLX 快 2.47x，iOS/macOS 开发者首选
- **Google LiteRT-LM**：TFLite 演进版，2026.03 更新降内存 30%+，Android 端 LLM 部署官方方案

---

## 15 MCU / TinyML 极低功耗部署

> **目的**：补齐“手机 SoC LLM”之下的另一半端侧世界——Cortex-M、Ethos-U、传感器 MCU 上的 KB–MB 级模型。关键词检测、异常检测、简单分类往往先于 LLM 常驻设备。

📖 代码实践：[15.1_mcu_tinyml.ipynb](15_mcu_tinyml/15.1_mcu_tinyml.ipynb)

### 15.1 与手机端侧的资源鸿沟

| 维度 | 旗舰手机 NPU | MCU + Ethos-U | 纯 MCU |
|------|-------------|---------------|--------|
| 内存 | 4–16GB | 256KB–2MB SRAM | 64–512KB |
| 算力 | 10–60 TOPS | 0.05–0.5 TOPS | 无 NPU |
| 典型模型 | 1B–7B SLM | 10K–1M 参数 | 1K–100K |
| 运行时 | llama.cpp / ExecuTorch / QNN | ExecuTorch / TFLM | CMSIS-NN / TFLM |

### 15.2 关键技术点

- **深度可分离卷积 / DS-CNN**：KWS 的事实标准结构，参数与 MAC 远低于常规 CNN。
- **INT8 全静态图**：禁止动态 shape 与运行时 malloc；AOT 内存规划一次算清 arena。
- **ExecuTorch → Ethos-U**：与手机共享 `torch.export` 流程，是连接两档设备的桥梁。
- **始终在线与事件触发**：KWS 在 DSP/MCU 常驻，唤醒后再拉起大模型，节省主 SoC 功耗。

### 15.3 部署建议

1. 先定延迟与内存硬预算（例如 20ms / 200KB），再选模型。
2. 用代表性噪声数据做 PTQ，避免实验室干净音频过拟合。
3. 与第 7.7 节语音全链路衔接：MCU 负责唤醒，AP/NPU 负责 ASR+LLM。

---

## 16 端侧扩散模型与图像生成

> **目的**：端侧不只是文本；相册美化、壁纸生成、AR 贴图依赖 **少步数扩散模型**。其内存峰值与优化手段与 LLM 不同，需单独成章。

📖 代码实践：[16.1_on_device_diffusion.ipynb](16_on_device_diffusion/16.1_on_device_diffusion.ipynb)

### 16.1 核心约束

- **步数就是延迟**：经典 50 步在手机上不可用；LCM / SD-Turbo / Lightning 等到 4–8 步。
- **分辨率决定激活峰值**：512→384/256 或 VAE tiling，往往比再砍一点权重更有效。
- **与 LLM 分时复用**：文生图时卸载/流式 LLM 权重，避免双模型 OOM。

### 16.2 优化组合

1. 步数蒸馏（首选）
2. UNet/DiT 权重量化 INT8/INT4，VAE 谨慎量化
3. 小分辨率 + 后超分（可选）
4. ControlNet / LoRA 插件化，按需加载
5. NPU 上优先委托卷积密集子图，Attention 可能回退 GPU/CPU

### 16.3 选型提示

| 场景 | 推荐方向 |
|------|---------|
| 1s 内出图 | SD-Turbo / LCM 系，4 步 |
| 人像美化 | 小分辨率 img2img + 专用 LoRA |
| 与助手共存 | 插件化加载，推理完立即释放 |

---

## 17 模型交付安全与 IP 保护

> **目的**：端侧模型以文件形式落在用户设备上，面临盗用、篡改、逆向。第 7.3 节侧重隐私与联邦；本节补 **交付与 IP** 视角。

📖 代码实践：[17.1_model_security.ipynb](17_model_security/17.1_model_security.ipynb)

### 17.1 威胁模型

- 直接拷贝 GGUF/mlpackage/pte 二次分发
- 篡改权重植入后门或广告触发器
- 提取用户 LoRA / 个性化适配器中的隐私方向

### 17.2 防护技术

- **完整性**：签名 + 哈希（与 6.1 版本管理联动）；启动时校验
- **机密性**：权重加密静态存储，运行时在 TEE/安全内存解密；或厂商 secure model container
- **水印与指纹**：第 7.3 节水印用于溯源；模型指纹用于授权校验
- **授权与轮换**：设备绑定 license、短时会话密钥、OTA 吊销
- **最小化暴露**：只下发任务所需 LoRA/适配器，基座可由系统预装（Apple/Google 内置模型路径）

### 17.3 工程清单

1. 发布流水线：量化产物 → 签名 → 加密包装 → CDN
2. 客户端：安全加载 → 完整性检查 → 推理 → 密钥清零
3. 运营：异常设备吊销、版本强制升级、审计日志

---


## 18 OS 系统 AI 运行时与共享基座

> **目的**：产业级端侧不只是 App 内嵌一个 Runtime，而是 **操作系统级 AI 服务**：多 App 共享基座模型、按需挂载适配器、统一调度内存与权限。缺了这一层，课程会停在“单应用部署”。

📖 代码实践：[18.1_system_ai_runtime.ipynb](18_system_runtime/18.1_system_ai_runtime.ipynb)

### 18.1 系统 AI 服务形态

| 平台 | 系统能力 | 典型入口 |
|------|---------|---------|
| **Android** | AICore / Gemini Nano 系统服务；按功能模块下载 | ML Kit GenAI / Prompt API 风格接口 |
| **iOS / macOS** | Foundation Models / CoreAI；系统预装小模型 | App Intent / 系统 Writing Tools |
| **Windows** | Copilot+ NPU 运行时；ISQ/厂商 EP | ONNX Runtime + QNN/OpenVINO |
| **厂商 ROM** | 三星 Galaxy AI、小米 HyperAI、荣耀 YOYO 等 | 系统助手进程常驻 |

### 18.2 共享基座 + 每应用适配器

- **一基座多租户**：系统只常驻 1 份 INT4 基座（如 1–3B），各 App 下发/挂载私有 LoRA/IA³。
- **路由**：`app_id → adapter_id`；无适配器则走通用基座；冲突时按前台 App 优先。
- **隔离**：适配器权重可加密；对话 KV 按会话隔离，禁止跨 App 读取。
- **生命周期**：后台 App 的 adapter 可卸载；基座受系统内存压力（LMKD / jetsam）保护等级约束。

### 18.3 进程、权限与后台

- **绑定服务 / XPC**：App 不直连 NPU，经系统 daemon 排队（见 7.4）。
- **权限**：麦克风、相册、通讯录按系统隐私授权；模型推断的敏感意图需二次确认。
- **后台限制**：长任务需前台服务/BGProcessing；被杀后要能从 session checkpoint 恢复。

### 18.4 与本课程其它章的衔接

- 调度/降级 → 第7.4/7.5 章；安全加载 → 第17章；个性化 LoRA → 第8章；选型 → 第13章。

---

## 19 模型分发与 OTA

> **目的**：端侧模型动辄数百 MB–数 GB，**如何可靠送到设备并热更新**是独立工程分类，不等于“版本号管理”（第6.1节）或“防篡改”（第17章）。

📖 代码实践：[19.1_model_ota.ipynb](19_model_ota/19.1_model_ota.ipynb)

### 19.1 分发管线

1. 构建产物：量化包 + 元数据（arch、量化、最低 OS、哈希）
2. CDN 分片：按 4–16MB chunk；支持 Range 断点续传
3. 客户端组装：边下边校验 chunk 哈希；全部通过后原子切换（双缓冲，见 7.4）
4. 失败：保留旧版本；指数退避重试；弱网降级只下 LoRA 不定制基座

### 19.2 增量更新（Delta OTA）

- **bsdiff / courgette 类二进制差分**：v1→v2 只传差量，适合小改动。
- **适配器优先**：基座不动，只 OTA LoRA（KB–MB 级）是端侧最经济路径。
- **分模块更新**：tokenizer / projector / LLM 可独立版本。

### 19.3 渐进式可用

- 先下 tokenizer + 配置 → 可显示“准备中”
- 再下关键层或草稿小模型 → 可先跑弱能力
- 最后补全权重 → 全功能；用户无感升级

### 19.4 发布策略

- 灰度：按设备档位 / 地区 / 电量条件推送（与 7.5 联动）
- 强制升级：安全漏洞或坏量化版本；吊销旧签名（第17章）
- 度量：下载成功率、平均耗时、切换失败率、回滚率

---

## 20 端侧检索与向量库

> **目的**：端侧 RAG 不是“调用一下 Chroma”一笔带过，需要 **Embedding 模型部署 + 向量索引 + 内存/精度权衡** 的完整技术分类。

📖 代码实践：[20.1_on_device_retrieval.ipynb](20_on_device_retrieval/20.1_on_device_retrieval.ipynb)

### 20.1 端侧 Embedding

- 模型：E5-small / BGE-small / 厂商微模型（通常 20–100M）
- 量化：INT8 几乎无损；维度 384/768；可 PCA/Matryoshka 截断到 128–256 维省内存
- 部署：常与 LLM 分时；或固定在 CPU/ANE 小网

### 20.2 索引结构

| 结构 | 内存 | 延迟 | 端侧适用 |
|------|------|------|---------|
| 暴力余弦 | 低实现成本 | 大数据慢 | <5k 条 |
| HNSW | 较高 | 低 | 中等语料首选 |
| IVF-PQ | 可压缩 | 中 | 较大私有语料 |
| SQLite-VSS / sqlite-vec | 随 DB | 中 | 移动 App 易集成 |

### 20.3 系统约束

- 索引构建放首次空闲；增量插入要可控（避免主线程卡顿）
- 检索 Top-K 结果必须 **截断进 LLM 上下文**（见第14章 Agent 的 OOM 风险）
- 隐私：向量库默认不出端；云端检索需明文脱敏

---

## 21 流式音视频交互管线

> **目的**：第7.7节给出 ASR-LLM-TTS 部件组合；本章上升为 **实时交互系统分类**：打断、双工、回声消除与帧级延迟预算。

📖 代码实践：[21.1_streaming_av_pipeline.ipynb](21_streaming_av/21.1_streaming_av_pipeline.ipynb)

### 21.1 典型状态机

`Idle → Listening(VAD) → ASR Streaming → LLM Streaming → TTS Streaming → Speaking`，任意时刻可被 **Barge-in（用户打断）** 拉回 Listening。

### 21.2 关键技术

- **VAD / 端点检测**：决定何时切 ASR；过于敏感会截断，过于迟钝增尾延迟
- **AEC（回声消除）**：TTS 外放时麦克风回路；车载/免提刚需
- **全双工 vs 半双工**：全双工要并行 ASR+TTS 通路与打断策略；端侧算力常迫使半双工
- **流式 ASR partial** → 预填 LLM prompt；**LLM token 流** → 句子级送 TTS，降低首包语音延迟

### 21.3 延迟预算示例（对话助手）

| 段 | 预算 |
|----|------|
| VAD 尾点 | 50–150ms |
| ASR 终值 | 100–300ms |
| LLM TTFT | <200ms |
| TTS 首帧 | <150ms |
| E2E 首声 | 常目标 <800ms |

### 21.4 与多模态/视频

- 实时视觉问答：相机帧选关键帧 → 视觉 encoder → 与语音通路仲裁（避免双模态同时打满 NPU）
- 视频理解：时序采样 + token 预算，见第7.2节 token 剪枝

---

## 22 自定义算子与 Kernel 工程

> **目的**：NPU/GPU 上“官方算子覆盖不够”是端侧落地头号工程风险之一；需要独立方法论，而不是只在排障里提“CPU 回退”。

📖 代码实践：[22.1_custom_ops_kernel.ipynb](22_custom_ops/22.1_custom_ops_kernel.ipynb)

### 22.1 决策树

1. 能否用等价标准算子图分解？（RoPE、SwiGLU、RMSNorm）
2. 能否改模型结构避开？（换激活、换注意力实现）
3. 必须自定义：在目标 Runtime 注册 op（ExecuTorch / ONNX / QNN / Core ML）
4. 最后才 CPU 回退（测量代价，见第9.2.3节）

### 22.2 工程内容

- **图模式匹配**：融合 QKV、识别 attention 模板再下沉
- **Kernel 后端**：NEON / AVX、Vulkan、Metal、Hexagon HVX、CUDA
- **数值对齐**：与 FP32 参考比余弦/MaxErr；纳入第24章门禁
- **版本契约**：自定义 op 的 ABI 与模型版本绑定，OTA 时同步

### 22.3 高频端侧自定义点

RoPE、RMSNorm、SiLU/SwiGLU、INT4 GEMM 解包、KV cache update、采样（top-k/p）、MLA 吸收投影。

---

## 23 车载与功能安全部署

> **目的**：车载不是“更大的手机”。功能安全（ISO 26262 等）对 **不确定性输出、延迟上界、失效时安全态** 提出独立分类要求。

📖 代码实践：以清单与场景仿真为主（见 [23.1_automotive_safety.ipynb](23_automotive_safety/23.1_automotive_safety.ipynb)）；完整认证需主机厂流程。

### 23.1 与消费电子差异

| 维度 | 手机 | 车载 |
|------|------|------|
| 延迟 | 体验指标 | 常有硬截止（DDL） |
| 失败 | 重试/云端 | 必须安全态（降级/禁用） |
| 温度 | 可降频 | 舱内宽温、长时满载 |
| 变更 | 频繁 OTA | 变更受安全论证约束 |
| 数据 | 隐私为主 | 另含法规与事件记录 |

### 23.2 技术控制措施

- **看门狗**：推理超时 → 切断执行器建议，回落到规则语音/仪表提示
- **双通道**：关键决策 ASR+规则 NLU 与 LLM 建议分离；LLM 不直连安全相关执行器
- **确定性**：固定 shape、禁止动态内存抖动；长稳压测（热/振动/电压）
- **溯源**：模型版本进入事件记录仪相关日志（与第17/19章联动）

### 23.3 推荐架构

感知/规控安全链 **不经过 LLM**；LLM 仅用于信息娱乐、导航对话、手册问答，并明确 HMI 披露“建议性内容”。

---

## 24 端侧 MLOps 与质量门禁

> **目的**：把第9章排障与第12章指标提升为 **持续交付体系**：每次量化/编译/OTA 都有可重复门禁。

📖 代码实践：[24.1_edge_mlops.ipynb](24_edge_mlops/24.1_edge_mlops.ipynb)

### 24.1 流水线阶段门禁

| 阶段 | 门禁 |
|------|------|
| 导出 | 算子覆盖率、动态 shape 合法性 |
| 量化 | PPL/任务指标跌幅、逐层余弦 |
| 编译 | NPU 回退算子数、二进制大小 |
| 设备 | TTFT/ITL/峰值内存/热节流 10 分钟长稳 |
| 发布 | 签名、license、灰度比例 |

### 24.2 设备农场与金样本

- 金样本 prompt 集：中英、工具调用、长上下文、敏感拒答
- 多档位设备（高通/联发科/苹果/RK）并行回归
- 失败自动归因：精度 / 性能 / 崩溃（ANR、EXC_RESOURCE）

### 24.3 线上可观测

- 客户端埋点：TTFT、取消率、降级率、OOM 杀进程
- 与第7.4监控衔接；隐私最小化（不上报原文，只上报哈希与直方图）
- 触发回滚：关键指标超阈或安全漏洞（第19章强制 OTA）

---

## 技术选型决策树

```
端侧部署大模型
│
├── 模型太大放不下？ → 模型压缩 (第1章)
│   ├── 量化（首选，效果最好）
│   │   ├── W4A16：AWQ/GPTQ（GPU端侧）
│   │   ├── W8A8：SmoothQuant（CPU/NPU端侧）
│   │   ├── FP8：E4M3/E5M2（H100/RTX 4090+等新硬件）
│   │   ├── W4A4：QuIP#/AQLM（极致压缩）
│   │   └── 1.58-bit/2-bit：BitNet/HY-2Bit（2026前沿, 极致压缩）
│   ├── 剪枝（结构化剪枝优先）
│   └── 蒸馏（需要训练资源）
│
├── 推理太慢？ → 推理优化 (第2章)
│   ├── Prefill慢 → Flash Attention / 批量优化
│   ├── Decode慢 → 投机解码 / 量化 / KV Cache优化
│   └── 长序列慢 → 稀疏注意力 / SSM / 滑动窗口 / MLA / TurboQuant
│
├── 内存不够？ → 内存优化 (第4章)
│   ├── KV Cache太大 → KV量化 / PagedAttention / 滑动窗口 / TurboQuant(6x压缩)
│   ├── 权重太大 → 量化 + 权重按需加载
│   └── 峰值内存高 → 激活重计算 / 内存复用
│
├── 需要个性化？ → 端侧训练 (第8章)
│   ├── QLoRA（推荐）
│   ├── IA³（极低资源）
│   └── Adapter / Prefix Tuning
│
├── 硬件适配？ → 部署框架选择 (第5章)
│   ├── iOS/macOS → CoreAI(2026, 推荐) / MLX / Core ML
│   ├── Android (高通) → QNN / ExecuTorch / MNN / LiteRT-LM
│   ├── Android (联发科) → NeuroPilot / MNN / LiteRT-LM
│   ├── 国产NPU (第10章)
│   │   ├── 华为昇腾 → CANN / AMCT
│   │   ├── 寒武纪 → MagicMind
│   │   ├── 地平线 → HBDK
│   │   └── 瑞芯微 → RKNN
│   ├── 通用CPU → llama.cpp / Ollama(极简部署)
│   ├── 浏览器端 → WebLLM / Transformers.js (第7.6节)
│   ├── MCU/传感器 → ExecuTorch Ethos-U / TFLM (第15章)
│   └── NVIDIA GPU → TensorRT-LLM
│
├── 选什么模型？ → 模型选型 (第13章)
│   ├── 中文场景 → Qwen3-4B / MiniCPM 3.0
│   ├── 英文场景 → Gemma 4 E2B / Phi-4
│   ├── 代码补全 → DeepSeek-Coder-V2-Lite
│   ├── Agent/工具调用 → Gemma 4 E4B
│   └── 低端设备 → Llama 3.2 1B / HY-1.8B-2Bit
│
├── 需要 Agent 能力？ → 端侧 Agent (第14章)
│   ├── 工具调用 → GBNF语法约束 + Function Calling
│   ├── 知识增强 → 端侧 RAG (第7.1节)
│   └── 持续进化 → 联邦学习 + LoRA
│
├── 语音助手全链路？ → ASR-LLM-TTS (第7.7节) + KWS/MCU (第15章)
├── 端侧文生图？ → 少步数扩散 (第16章)
├── 模型防盗版/防篡改？ → 交付安全 (第17章)
│
├── 系统预置模型 / 多 App 共享？ → OS AI 运行时 (第18章)
├── 模型怎么下发与热更新？ → OTA 分发 (第19章)
├── 私有知识库问答？ → 端侧检索 (第20章)
├── 实时语音打断/双工？ → 流式音视频管线 (第21章)
├── NPU 缺算子？ → 自定义 Kernel (第22章)
├── 车载量产约束？ → 功能安全 (第23章)
├── 持续回归与发布门禁？ → 端侧 MLOps (第24章)
│
├── 部署出问题？ → 故障排查 (第9.2节)
│   ├── OOM → 量化/小模型/KV管理
│   ├── 精度异常 → 逐层对比/混合精度
│   ├── 性能不达标 → Profile/量化
│   └── 编译失败 → 算子分解/CPU回退
│
└── 需要系统评估？ → 评估指标 (第12章)
    ├── 性能：TTFT、ITL、吞吐
    ├── 内存：峰值、带宽利用率
    ├── 精度：PPL、下游任务
    └── 功耗：TDP、能效比
```

---

## 总结

大模型端侧部署是一个系统工程，涉及从模型算法层到硬件系统层的全栈优化。本课程从以下维度系统覆盖：

| 维度 | 核心技术 | 关键收益 |
|------|---------|---------|
| **模型压缩** (第1章) | 量化、剪枝、蒸馏、低秩、超低比特、torchao | 模型体积 60-90%，精度损失可控 |
| **推理优化** (第2章) | KV Cache、Flash Attention、投机解码、MLA | 吞吐 2-5×，延迟降低 50% |
| **架构设计** (第3章) | GQA、SSM、MoE、自定义算子 | KV Cache 4-8×减少 |
| **编译运行时** (第4章) | 图优化、代码生成、内存优化 | 延迟 20-30%，内存 15-25% |
| **硬件部署** (第5章) | NPU适配、框架选择、基准测试 | 硬件利用率 70%+ |
| **模型格式** (第6章) | ONNX、GGUF、TorchScript、版本管理 | 多平台互操作 |
| **端云协同** (第7章) | 协同推理、多模态、语音全链路、功耗、WASM | 云端算力+端侧隐私 |
| **端侧训练** (第8章) | PEFT、QLoRA、训练优化、个性化 | 适配内存 <2GB |
| **实战与排查** (第9章) | 端到端流水线、故障诊断 | 独立完成部署 |
| **国产生态** (第10章) | 昇腾/寒武纪/地平线、Qwen/DeepSeek/MiniCPM | 中国市场适配 |
| **评估指标** (第12章) | TTFT/ITL/内存/精度/功耗 | 可复现验收 |
| **模型选型** (第13章) | 2026 主流 SLM/VLM | 选对模型事半功倍 |
| **端侧 Agent** (第14章) | Function Calling、RAG、联邦 | 离线多步任务 |
| **MCU/TinyML** (第15章) | KWS、Ethos-U、INT8 静态图 | 始终在线极低功耗 |
| **端侧扩散** (第16章) | 少步数蒸馏、分辨率/内存策略 | 手机文生图 |
| **交付安全** (第17章) | 签名、加密、水印、授权 | 防盗用与防篡改 |
| **系统 AI 运行时** (第18章) | AICore/Foundation Models、共享基座 | 多 App 复用、省内存 |
| **模型 OTA** (第19章) | 分片、差分、灰度、渐进可用 | 可运营的端侧模型 |
| **端侧检索** (第20章) | Embedding、HNSW/IVF、sqlite-vec | 私有知识不出端 |
| **流式 AV 管线** (第21章) | VAD、AEC、打断、双工 | 可用的语音助手体验 |
| **自定义算子** (第22章) | 分解/注册/Kernel/对齐 | 降低 NPU 回退 |
| **车载功能安全** (第23章) | 看门狗、安全态、隔离 | 可量产车载 AI |
| **端侧 MLOps** (第24章) | 门禁、设备农场、可观测 | 可持续发布 |

各技术之间并非独立，而是相互配合、联合使用：

1. **量化 + KV Cache优化**：同时压缩权重和KV，最大化内存节省
2. **量化 + 投机解码**：小模型量化后更快生成候选，大模型量化后更快验证
3. **剪枝 + 蒸馏**：先剪枝再蒸馏恢复精度，或蒸馏到更小架构
4. **编译优化 + 硬件适配**：编译器针对特定NPU生成最优代码
5. **端云协同 + 隐私保护**：在享受云端算力的同时保护用户数据
6. **MoE + 按需加载**：利用MoE的稀疏激活特性，结合权重流式加载降低端侧内存压力

**产业级端侧部署的核心**：在精度、速度、内存、功耗、成本五大维度之间找到最优平衡点，这需要根据具体硬件平台、应用场景和性能指标进行系统性调优。

---

## 课程文件索引

| 章节 | 内容 | Notebook |
|------|------|----------|
| 1.1 | 量化技术 | [01_model_compression/1.1_quantization.ipynb](01_model_compression/1.1_quantization.ipynb) |
| 1.2 | 模型剪枝 | [01_model_compression/1.2_pruning.ipynb](01_model_compression/1.2_pruning.ipynb) |
| 1.3 | 知识蒸馏 | [01_model_compression/1.3_knowledge_distillation.ipynb](01_model_compression/1.3_knowledge_distillation.ipynb) |
| 1.4 | 低秩分解 | [01_model_compression/1.4_low_rank_factorization.ipynb](01_model_compression/1.4_low_rank_factorization.ipynb) |
| 1.5 | 超低比特量化 | [01_model_compression/1.5_sub2bit_quantization.ipynb](01_model_compression/1.5_sub2bit_quantization.ipynb) |
| 1.6 | torchao 工具链 | [01_model_compression/1.6_torchao_toolchain.ipynb](01_model_compression/1.6_torchao_toolchain.ipynb) |
| 2.1 | KV Cache | [02_efficient_inference/2.1_kv_cache.ipynb](02_efficient_inference/2.1_kv_cache.ipynb) |
| 2.2 | 注意力优化 | [02_efficient_inference/2.2_attention_optimization.ipynb](02_efficient_inference/2.2_attention_optimization.ipynb) |
| 2.3 | 推理加速 | [02_efficient_inference/2.3_inference_acceleration.ipynb](02_efficient_inference/2.3_inference_acceleration.ipynb) |
| 3.1 | 轻量级架构 | [03_efficient_architecture/3.1_lightweight_architecture.ipynb](03_efficient_architecture/3.1_lightweight_architecture.ipynb) |
| 3.2 | 线性注意力/SSM | [03_efficient_architecture/3.2_linear_attention_ssm.ipynb](03_efficient_architecture/3.2_linear_attention_ssm.ipynb) |
| 3.3 | MoE架构 | [03_efficient_architecture/3.3_moe.ipynb](03_efficient_architecture/3.3_moe.ipynb) |
| 4.1 | 图优化 | [04_compilation_runtime/4.1_graph_optimization.ipynb](04_compilation_runtime/4.1_graph_optimization.ipynb) |
| 4.2 | 代码生成 | [04_compilation_runtime/4.2_code_generation.ipynb](04_compilation_runtime/4.2_code_generation.ipynb) |
| 4.3 | 内存优化 | [04_compilation_runtime/4.3_memory_optimization.ipynb](04_compilation_runtime/4.3_memory_optimization.ipynb) |
| 5.1 | NPU适配 | [05_hardware_deployment/5.1_npu_adaptation.ipynb](05_hardware_deployment/5.1_npu_adaptation.ipynb) |
| 5.2 | 部署框架 | [05_hardware_deployment/5.2_deployment_frameworks.ipynb](05_hardware_deployment/5.2_deployment_frameworks.ipynb) |
| 5.3 | 硬件感知优化 | [05_hardware_deployment/5.3_hardware_aware.ipynb](05_hardware_deployment/5.3_hardware_aware.ipynb) |
| 5.4 | 硬件基准测试 | [05_hardware_deployment/5.4_hardware_benchmarking.ipynb](05_hardware_deployment/5.4_hardware_benchmarking.ipynb) |
| 6.0 | 模型格式 | [06_model_format/6.0_model_format.ipynb](06_model_format/6.0_model_format.ipynb) |
| 6.1 | 模型版本管理 | [06_model_format/6.1_model_versioning.ipynb](06_model_format/6.1_model_versioning.ipynb) |
| 7.1 | 端云协同推理 | [07_edge_cloud/7.1_edge_cloud_inference.ipynb](07_edge_cloud/7.1_edge_cloud_inference.ipynb) |
| 7.2 | 多模态部署 | [07_edge_cloud/7.2_multimodal_deployment.ipynb](07_edge_cloud/7.2_multimodal_deployment.ipynb) |
| 7.3 | 隐私安全 | [07_edge_cloud/7.3_privacy_security.ipynb](07_edge_cloud/7.3_privacy_security.ipynb) |
| 7.4 | 端侧推理服务 | [07_edge_cloud/7.4_inference_service.ipynb](07_edge_cloud/7.4_inference_service.ipynb) |
| 7.4b | 端侧监控运维 | [07_edge_cloud/7.4_edge_monitoring.ipynb](07_edge_cloud/7.4_edge_monitoring.ipynb) |
| 7.5 | 功耗与电池调度 | [07_edge_cloud/7.5_power_battery.ipynb](07_edge_cloud/7.5_power_battery.ipynb) |
| 7.6 | 浏览器 / WASM | [07_edge_cloud/7.6_browser_wasm.ipynb](07_edge_cloud/7.6_browser_wasm.ipynb) · [browser_demo](07_edge_cloud/browser_demo/index.html) |
| 7.7 | 语音全链路 | 见第7.7节 + [7.2_multimodal_deployment.ipynb](07_edge_cloud/7.2_multimodal_deployment.ipynb) |
| 8.1 | PEFT | [08_on_device_training/8.1_peft.ipynb](08_on_device_training/8.1_peft.ipynb) |
| 8.2 | 训练优化 | [08_on_device_training/8.2_training_optimization.ipynb](08_on_device_training/8.2_training_optimization.ipynb) |
| 8.3 | 端侧评估与个性化 | [08_on_device_training/8.3_on_device_eval.ipynb](08_on_device_training/8.3_on_device_eval.ipynb) |
| 9.1 | 端到端流水线 | [09_end_to_end/9.1_end_to_end_deployment.ipynb](09_end_to_end/9.1_end_to_end_deployment.ipynb) |
| 9.2 | 故障排查 | [09_end_to_end/9.2_troubleshooting_debug.ipynb](09_end_to_end/9.2_troubleshooting_debug.ipynb) |
| 10.1 | 国产NPU部署实践 | [10_china_hardware/10.1_china_npu.ipynb](10_china_hardware/10.1_china_npu.ipynb) |
| 10.2 | 国产开源模型端侧部署 | 见本文档第10.2节 |
| 11 | 课后练习与思考题 | [exercises_solutions.md](exercises_solutions.md) |
| 12.1-12.5 | 评估指标体系 | [12_evaluation/12.1_evaluation_metrics.ipynb](12_evaluation/12.1_evaluation_metrics.ipynb) |
| 13 | 端侧模型选型（2026） | [13_model_selection/13.1_model_selection.ipynb](13_model_selection/13.1_model_selection.ipynb) |
| 14 | 端侧 Agent 与新范式 | [14_edge_agent/14.1_edge_agent.ipynb](14_edge_agent/14.1_edge_agent.ipynb) |
| 15 | MCU / TinyML | [15_mcu_tinyml/15.1_mcu_tinyml.ipynb](15_mcu_tinyml/15.1_mcu_tinyml.ipynb) |
| 16 | 端侧扩散 / 文生图 | [16_on_device_diffusion/16.1_on_device_diffusion.ipynb](16_on_device_diffusion/16.1_on_device_diffusion.ipynb) |
| 17 | 模型交付安全 | [17_model_security/17.1_model_security.ipynb](17_model_security/17.1_model_security.ipynb) |
| 18 | OS 系统 AI 运行时 | [18_system_runtime/18.1_system_ai_runtime.ipynb](18_system_runtime/18.1_system_ai_runtime.ipynb) |
| 19 | 模型分发与 OTA | [19_model_ota/19.1_model_ota.ipynb](19_model_ota/19.1_model_ota.ipynb) |
| 20 | 端侧检索与向量库 | [20_on_device_retrieval/20.1_on_device_retrieval.ipynb](20_on_device_retrieval/20.1_on_device_retrieval.ipynb) |
| 21 | 流式音视频管线 | [21_streaming_av/21.1_streaming_av_pipeline.ipynb](21_streaming_av/21.1_streaming_av_pipeline.ipynb) |
| 22 | 自定义算子与 Kernel | [22_custom_ops/22.1_custom_ops_kernel.ipynb](22_custom_ops/22.1_custom_ops_kernel.ipynb) |
| 23 | 车载与功能安全 | [23_automotive_safety/23.1_automotive_safety.ipynb](23_automotive_safety/23.1_automotive_safety.ipynb) |
| 24 | 端侧 MLOps 与门禁 | [24_edge_mlops/24.1_edge_mlops.ipynb](24_edge_mlops/24.1_edge_mlops.ipynb) |
| 2.4-2.5 | Prefill/Decode、长上下文 | 见本文档第2.4/2.5节 |
| 3.4 | 硬件感知 NAS | 见本文档第3.4节 |
| 8.4 | 多适配器路由 | 见本文档第8.4节 |
| - | 学习级技术全景 | [odd_learning_panorama.md](odd_learning_panorama.md) |
| - | 零基础趣味科普（合并定稿） | [odd_popular_science.md](odd_popular_science.md) |
| - | 综合实战项目 | [comprehensive_projects.md](comprehensive_projects.md) |
| - | 硬件实操路线图 | [hardware_roadmap.md](hardware_roadmap.md) |
