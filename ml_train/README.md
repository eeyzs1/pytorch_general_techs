# 大模型机器学习产业级技术全景

本项目系统性地覆盖了大语言模型（LLM）从数据到部署的全生命周期技术栈，包含 17 个技术模块、60+ 个可运行的 Jupyter Notebook 代码示例。

## 项目结构

```
ml_train/
├── 01_data_engineering/       # 数据工程（采集/清洗/配比/标注）
├── 02_learning_paradigms/     # 学习范式（14种范式）
├── 03_architecture_design/    # 架构设计（Transformer/MoE/注意力）
├── 04_pretraining/            # 预训练（目标/策略/稳定性）
├── 05_distributed_training/   # 分布式训练（DP/TP/PP/3D并行）
├── 06_fine_tuning/            # 微调（全参数/PEFT/指令微调）
├── 07_alignment_training/     # 对齐训练（RLHF/DPO/安全对齐）
├── 08_model_compression/      # 模型压缩（量化/剪枝/蒸馏/低秩）
├── 09_inference_optimization/ # 推理优化（KV Cache/解码/编译）
├── 10_long_context/           # 长上下文处理
├── 11_rag/                    # 检索增强生成（RAG）
├── 12_agent/                  # 智能体（工具/规划/记忆/多智能体）
├── 13_multimodal/             # 多模态（视觉/音频/视频/对齐）
├── 14_prompt_engineering/     # 提示工程（Zero-shot/Few-shot/CoT）
├── 15_evaluation/             # 评估与基准
├── 16_security_robustness/    # 安全与鲁棒性
└── 17_continual_learning/     # 持续学习与适应
```

## 快速开始

### 环境配置

```bash
pip install -r requirements.txt
```

### 推荐学习路径

1. **入门**：[02_learning_paradigms/14_deep_learning_basics.ipynb](02_learning_paradigms/14_deep_learning_basics.ipynb) — 深度学习训练基础（反向传播、优化器、学习率调度、正则化、归一化、梯度管理、混合精度）
2. **架构**：[03_architecture_design/01_overall_architecture.ipynb](03_architecture_design/01_overall_architecture.ipynb) — Transformer 架构设计
3. **范式**：[02_learning_paradigms/01_supervised_learning.ipynb](02_learning_paradigms/01_supervised_learning.ipynb) — 监督学习
4. **微调**：[06_fine_tuning/02_peft.ipynb](06_fine_tuning/02_peft.ipynb) — 参数高效微调
5. **对齐**：[07_alignment_training/01_rlhf.ipynb](07_alignment_training/01_rlhf.ipynb) — RLHF 对齐训练
6. **压缩**：[08_model_compression/01_quantization.ipynb](08_model_compression/01_quantization.ipynb) — 模型量化
7. **推理**：[09_inference_optimization/01_kv_cache.ipynb](09_inference_optimization/01_kv_cache.ipynb) — KV Cache 推理优化

完整技术全景请参阅 [大模型机器学习技术全景.md](大模型机器学习技术全景.md)。

## 每个 Notebook 的特点

- 每个 Notebook 遵循"**理论说明 → 代码实现 → 结果打印**"的教学模式
- 代码中包含丰富的 `print` 输出和 `Key:` 关键结论总结
- 各 cell 设计为可独立运行

## 技术全景

| 模块 | 技术覆盖 |
|------|---------|
| 数据工程 | 网页爬取、质量过滤、去重、PII去除、数据配比、合成数据 |
| 学习范式 | 监督/自监督/无监督/半监督/强化/迁移/元/多任务/联邦/对比/课程/主动/在线学习 |
| 架构设计 | Decoder-Only/Encoder-Only/Encoder-Decoder、MHA/MQA/GQA/MLA、RoPE、SwiGLU、MoE |
| 预训练 | CLM/MLM、学习率调度、混合精度、梯度裁剪/Loss Spike处理 |
| 分布式训练 | DDP/FSDP/ZeRO、张量/流水线/序列并行、3D并行、通信优化 |
| 微调 | LoRA/QLoRA/Adapter/Prefix/Prompt/P-Tuning v2/IA³/DoRA |
| 对齐训练 | RLHF(P+R+PPO)、DPO/IPO/KTO/ORPO/SimPO、RLAIF/Constitutional AI |
| 模型压缩 | GPTQ/AWQ/SmoothQuant/QAT、结构化/非结构化/层剪枝、知识蒸馏 |
| 推理优化 | PagedAttention、MQA/GQA/MLA、Continuous Batching、投机解码/Medusa/Eagle |
| Agent | 函数调用/代码执行、ReAct/ToT/Plan-and-Solve、多智能体协作 |
| 安全 | 提示注入/越狱/GCG、FGSM/PGD、后门攻击/数据投毒/成员推断 |
