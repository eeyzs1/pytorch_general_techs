# 大模型机器学习产业级技术全景

本项目系统性地覆盖了大语言模型（LLM）从数据到部署的全生命周期技术栈，包含 20 个技术模块、125 个可运行的 Jupyter Notebook 代码示例。

📖 **文档导航**：
- [大模型机器学习技术全景.md](大模型机器学习技术全景.md) — 技术参考文档（适合有技术背景的读者）
- [趣味科普：AI训练技术给非技术人员的通关指南.md](趣味科普：AI训练技术给非技术人员的通关指南.md) — 趣味科普文档（适合零基础读者，用"养孩子"的比喻讲解所有技术）

## 项目结构

```
ml_train/
├── 00_foundations/             # 前置基础（深度学习训练核心/前沿优化器）
├── 01_data_engineering/        # 数据工程（…/合成验证/DoReMi配比深挖）
├── 02_learning_paradigms/      # 学习范式（14种范式）
├── 03_architecture_design/     # 架构设计（…/SSM/GNN-LLM/MoE规模化训练）
├── 04_pretraining/             # 预训练（…/代码专训/训练可观测性）
├── 05_distributed_training/    # 分布式训练（DP/TP/PP/3D/上下文并行Ulysses·Ring）
├── 06_fine_tuning/             # 微调（全参数/PEFT/指令微调）
├── 07_alignment_training/      # 对齐（…/过程监督/奖励黑客深挖）
├── 08_model_compression/       # 模型压缩（量化/剪枝/蒸馏/低秩）
├── 09_inference_optimization/  # 推理（…/硬件内核/Serving引擎内部）
├── 10_long_context/            # 长上下文处理（PI/NTK/YaRN/ALiBi）
├── 11_rag/                     # 检索增强生成（RAG/Embedding训练）
├── 12_agent/                   # 智能体（…/深度研究/工具调用RL）
├── 13_multimodal/              # 多模态（视觉/音频/视频/对齐/生成/实时语音双工）
├── 14_prompt_engineering/      # 提示工程（Zero-shot/Few-shot/CoT/DSPy）
├── 15_evaluation/              # 评估与基准（语言/推理/污染检测/Arena/不确定性校准）
├── 16_security_robustness/     # 安全与鲁棒性（攻击/防御/隐私/水印/护栏）
├── 17_continual_learning/      # 持续学习与适应
├── 18_mlops/                   # MLOps（Serving/监控/CI-CD/端侧/绿色AI/语义缓存/AI治理合规）
├── 19_interpretability/        # 可解释性（机理可解释性/表征引导）
├── 20_end_to_end/              # 端到端案例（MoE：配比→训练→EP→Serving→Go-Live）
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

1. **前置基础**：[00_foundations/00_deep_learning_basics.ipynb](00_foundations/00_deep_learning_basics.ipynb) — 深度学习训练核心基础（反向传播与自动微分、优化器对比、学习率调度、正则化与归一化）
2. **架构入门**：[03_architecture_design/01_overall_architecture.ipynb](03_architecture_design/01_overall_architecture.ipynb) — Transformer 架构设计
3. **学习范式**：[02_learning_paradigms/01_supervised_learning.ipynb](02_learning_paradigms/01_supervised_learning.ipynb) — 监督学习
4. **数据工程**：[01_data_engineering/01_data_collection.ipynb](01_data_engineering/01_data_collection.ipynb) — 数据采集与处理
5. **微调实战**：[06_fine_tuning/02_peft.ipynb](06_fine_tuning/02_peft.ipynb) — 参数高效微调
6. **对齐训练**：[07_alignment_training/01_rlhf.ipynb](07_alignment_training/01_rlhf.ipynb) — RLHF 对齐训练
7. **推理部署**：[09_inference_optimization/01_kv_cache.ipynb](09_inference_optimization/01_kv_cache.ipynb) → [18_mlops/01_model_serving.ipynb](18_mlops/01_model_serving.ipynb) — 推理优化与模型部署
8. **前沿技术**：[07_alignment_training/05_grpo.ipynb](07_alignment_training/05_grpo.ipynb) — GRPO · [09_inference_optimization/05_test_time_compute.ipynb](09_inference_optimization/05_test_time_compute.ipynb) — Test-Time Compute · [12_agent/05_mcp.ipynb](12_agent/05_mcp.ipynb) — MCP协议
9. **端到端串联**：[20_end_to_end/01_moe_from_mixture_to_serving.ipynb](20_end_to_end/01_moe_from_mixture_to_serving.ipynb) — MoE 配比→训练观测→EP→Serving→Go-Live

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
| 前置基础 | 反向传播、AdamW、Lion/Sophia/Muon、学习率调度、正则化、RMSNorm/LayerNorm、混合精度、梯度裁剪 |
| 数据工程 | 网页爬取、质量过滤、去重、PII、配比、DoReMi领域重加权、合成验证门禁、Tokenizer、数据增强 |
| 学习范式 | 监督/自监督/无监督/半监督/强化/迁移/元/多任务/联邦/对比/课程/主动/在线学习 |
| 架构设计 | Transformer族、MLA/GQA、MoE规模化（负载均衡/CF/EP）、Diffusion LLM、SSM混合、GNN+LLM、世界模型、神经符号 |
| 预训练 | CLM/MLM、MTP、学习率调度、混合精度、Loss Spike、缩放定律、数据退火、代码FIM/Pass@k、训练可观测性（激活/梯度/归因） |
| 分布式训练 | DDP/FSDP/ZeRO、TP/PP/SP、3D并行、Ulysses/Ring上下文并行、通信优化、容错弹性 |
| 微调 | LoRA/QLoRA/Adapter/Prefix/Prompt/P-Tuning v2/IA³/DoRA |
| 对齐训练 | RLHF/DPO族/GRPO、过程监督、奖励黑客与过度优化、Self-Rewarding/RLAIF/Constitutional AI |
| 模型压缩 | GPTQ/AWQ/SmoothQuant/QAT、结构化/非结构化/层剪枝、知识蒸馏 |
| 推理优化 | PagedAttention、Continuous Batching、投机解码、TTC、前缀缓存、多LoRA、PD分离、FA3/FP8、Serving调度/Radix内部 |
| 长上下文 | 位置插值PI、NTK-aware RoPE、YaRN、ALiBi、滑动窗口、Attention Sink/StreamingLLM、提示压缩 |
| RAG | 文档处理、稠密/稀疏/混合检索、重排、高级RAG、Embedding/Reranker训练 |
| Agent | 工具/规划/记忆、多智能体、MCP、Computer Use、深度研究、工具调用RL |
| 多模态 | 视觉-语言、音频-语言、视频-语言、跨模态对齐、文生图/统一生成、实时语音双工 |
| 评估 | 语言/推理/代码评估、LLM-as-Judge、数据污染检测、Arena竞技场/Elo评分、不确定性与校准 |
| 安全 | 提示注入/越狱/GCG、FGSM/PGD、后门攻击/数据投毒/成员推断、模型水印、模型供应链安全、生产级Guardrails |
| 可解释性 | Logit归因、Activation Patching、Sparse Autoencoder、线性探针、Activation Steering |
| MLOps | Serving、实验追踪、监控、CI/CD、端侧、绿色AI、语义缓存、EU AI Act治理与合规证据包 |
| 端到端案例 | MoE 产品切片：DoReMi配比→训练心跳/尖峰护栏→EP容量因子→checkpoint指纹→Continuous Batching→Go-Live门禁 |
| 工具库 | RMSNorm、DropPath、SwiGLU、RotaryPositionalEmbedding、梯度裁剪 |