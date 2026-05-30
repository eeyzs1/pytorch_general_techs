# 大模型机器学习产业级技术全景

本项目系统性地覆盖了大语言模型（LLM）从数据到部署的全生命周期技术栈，包含 18 个技术模块、70+ 个可运行的 Jupyter Notebook 代码示例。

## 项目结构

```
ml_train/
├── 00_foundations/             # 前置基础（深度学习训练核心）
├── 01_data_engineering/        # 数据工程（采集/清洗/配比/标注/管道工程）
├── 02_learning_paradigms/      # 学习范式（14种范式）
├── 03_architecture_design/     # 架构设计（Transformer/MoE/注意力/扩散LLM）
├── 04_pretraining/             # 预训练（目标/策略/稳定性）
├── 05_distributed_training/    # 分布式训练（DP/TP/PP/3D并行）
├── 06_fine_tuning/             # 微调（全参数/PEFT/指令微调）
├── 07_alignment_training/      # 对齐训练（RLHF/DPO/GRPO/安全对齐）
├── 08_model_compression/       # 模型压缩（量化/剪枝/蒸馏/低秩）
├── 09_inference_optimization/  # 推理优化（KV Cache/解码/编译/Test-Time Compute）
├── 10_long_context/            # 长上下文处理
├── 11_rag/                     # 检索增强生成（RAG）
├── 12_agent/                   # 智能体（工具/规划/记忆/多智能体/MCP）
├── 13_multimodal/              # 多模态（视觉/音频/视频/对齐）
├── 14_prompt_engineering/      # 提示工程（Zero-shot/Few-shot/CoT）
├── 15_evaluation/              # 评估与基准
├── 16_security_robustness/     # 安全与鲁棒性
├── 17_continual_learning/      # 持续学习与适应
├── 18_mlops/                   # MLOps与模型部署
└── utils/                      # 共享工具模块
```

## 快速开始

### 环境配置

```bash
python3 -m venv .venv
source .venv/bin/activate

# 基础依赖
pip install -r requirements.txt

# 完整开发环境（含测试、格式化工具）
pip install -r requirements-dev.txt
```

### 质量检查

提交或继续扩展 Notebook 前，先运行项目自带的静态门禁：

```bash
make validate
# 或直接运行：
python3 scripts/validate_notebooks.py
```

该检查会覆盖：

- 所有 `.ipynb` 是否为合法 JSON / nbformat 4
- Notebook 是否包含 Python kernel 元数据
- 每个代码 cell 是否能通过 Python AST 语法解析
- Notebook `source` 行尾格式是否正确，避免多行代码被拼成一行
- 代码中使用的第三方 import 是否已写入 `requirements.txt`
- 是否误提交了执行计数或输出结果

### 推荐学习路径

1. **前置基础**：[00_foundations/00_deep_learning_basics.ipynb](00_foundations/00_deep_learning_basics.ipynb) — 深度学习训练核心基础（反向传播、优化器、学习率调度、正则化、归一化、梯度管理、混合精度）
2. **架构入门**：[03_architecture_design/01_overall_architecture.ipynb](03_architecture_design/01_overall_architecture.ipynb) — Transformer 架构设计
3. **学习范式**：[02_learning_paradigms/01_supervised_learning.ipynb](02_learning_paradigms/01_supervised_learning.ipynb) — 监督学习
4. **数据工程**：[01_data_engineering/01_data_collection.ipynb](01_data_engineering/01_data_collection.ipynb) — 数据采集与处理
5. **微调实战**：[06_fine_tuning/02_peft.ipynb](06_fine_tuning/02_peft.ipynb) — 参数高效微调
6. **对齐训练**：[07_alignment_training/01_rlhf.ipynb](07_alignment_training/01_rlhf.ipynb) — RLHF 对齐训练
7. **推理部署**：[09_inference_optimization/01_kv_cache.ipynb](09_inference_optimization/01_kv_cache.ipynb) → [18_mlops/01_model_serving.ipynb](18_mlops/01_model_serving.ipynb) — 推理优化与模型部署
8. **前沿技术**：[07_alignment_training/05_grpo.ipynb](07_alignment_training/05_grpo.ipynb) — GRPO · [09_inference_optimization/05_test_time_compute.ipynb](09_inference_optimization/05_test_time_compute.ipynb) — Test-Time Compute · [12_agent/05_mcp.ipynb](12_agent/05_mcp.ipynb) — MCP协议

完整技术全景请参阅 [大模型机器学习技术全景.md](大模型机器学习技术全景.md)。

## 每个 Notebook 的特点

- 每个 Notebook 遵循"**理论说明 → 代码实现 → 结果打印**"的教学模式
- 代码中包含丰富的 `print` 输出和 `Key:` 关键结论总结
- 建议按 Notebook 内顺序运行；部分后续 cell 会复用前面定义的模型或辅助函数
- 默认示例尽量保持 CPU 可运行；涉及 Hugging Face 模型下载的 cell 需要联网环境
- 每个 Notebook 开头标注 **预估学习时间**
- 每个 Notebook 末尾附带 **课后思考题**
- 各 cell 设计为可独立运行

## 技术全景

| 模块 | 技术覆盖 |
|------|---------|
| 前置基础 | 反向传播、AdamW、学习率调度、正则化、RMSNorm/LayerNorm、混合精度、梯度裁剪 |
| 数据工程 | 网页爬取、质量过滤、去重、PII去除、数据配比、合成数据、管道工程化 |
| 学习范式 | 监督/自监督/无监督/半监督/强化/迁移/元/多任务/联邦/对比/课程/主动/在线学习 |
| 架构设计 | Decoder-Only/Encoder-Only/Encoder-Decoder、MHA/MQA/GQA/MLA、RoPE、SwiGLU、MoE、Diffusion LLM |
| 预训练 | CLM/MLM、学习率调度、混合精度、梯度裁剪/Loss Spike处理 |
| 分布式训练 | DDP/FSDP/ZeRO、张量/流水线/序列并行、3D并行、通信优化 |
| 微调 | LoRA/QLoRA/Adapter/Prefix/Prompt/P-Tuning v2/IA³/DoRA |
| 对齐训练 | RLHF(P+R+PPO)、DPO/IPO/KTO/ORPO/SimPO、GRPO、RLAIF/Constitutional AI |
| 模型压缩 | GPTQ/AWQ/SmoothQuant/QAT、结构化/非结构化/层剪枝、知识蒸馏 |
| 推理优化 | PagedAttention、MQA/GQA/MLA、Continuous Batching、投机解码/Medusa/Eagle、Test-Time Compute |
| Agent | 函数调用/代码执行、ReAct/ToT/Plan-and-Solve、多智能体协作、MCP协议 |
| MLOps | 模型Serving(vLLM/TGI/Triton)、负载均衡、模型注册、成本优化 |
| 安全 | 提示注入/越狱/GCG、FGSM/PGD、后门攻击/数据投毒/成员推断 |
| 工具库 | RMSNorm、DropPath、SwiGLU、RotaryPositionalEmbedding、梯度裁剪 |