# DeepSeek-V4 发布：双模型架构、百万上下文与推理成本革命（DeepSeek-V4 Released）

- **原文链接**: [DeepSeek-V4 预览版本发布（官方公众号公告）](https://mp.weixin.qq.com/s/8bxXqS2R8Fx5-1TLDBiEDg)
- **作者**: DeepSeek（深度求索）
- **发布日期**: 2026-04-24
- **检索日期**: 2026-07-20
- **标签**: #DeepSeek #V4 #开源模型 #MoE #1M上下文 #mHC #国产算力

## 核心观点

DeepSeek-V4 是深度求索继 V3（2024-12-26）之后 484 天推出的新一代旗舰系列，包含 V4-Pro（1.6T 总参数 / 49B 激活）和 V4-Flash（284B 总参数 / 13B 激活）双模型，均支持 100 万 token 上下文。核心技术主张：通过 mHC（流形约束超连接）、CSA/HCA 混合注意力等架构创新，把百万上下文的推理计算量压到 V3.2 的 27%、KV cache 压缩至 10%，让超长上下文从"技术奇点"变成"可承担的工程现实"。官方定位"世界顶级推理性能，Agent 能力大幅提高"，已在网页端、APP 和 API 全面上线，以 MIT 协议开源。

## 关键发现 / 关键技术

### 1. 双模型规格（官方 API 文档确认）

| 参数 | V4-Pro | V4-Flash |
|------|--------|----------|
| 总参数量 | 1.6T | 284B |
| 激活参数量 | 49B | 13B |
| 上下文长度 | 1M tokens | 1M tokens |
| 最大输出 | 384K | 384K |
| API 模型名 | `deepseek-v4-pro` | `deepseek-v4-flash` |
| 并发上限 | 500 | 2500 |

推理模式均支持非思考 / Think High / Think Max 三档；支持 JSON Output、Tool Calls、Chat Prefix Completion（Beta）、FIM Completion（Beta，仅非思考模式）。

### 2. 三大架构创新（基于论文原文）

#### mHC（流形约束超连接）— arXiv:2512.24880

**问题**：HC（Hyper-Connections）将残差流扩展为 n 条并行通道，但无约束的残差混合矩阵 H_res 导致**信号发散**——27B MoE 模型中 Amax Gain Magnitude 峰值达 **3000**，深层网络训练崩溃。

**核心公式**（单层 mHC）：
```
x_{l+1} = H_res^l · x_l + H_post^{lT} · F(H_pre^l · x_l, W_l)
```
- `x_l ∈ R^{n×C}`：n 条通道 × C 维特征
- `H_res^l ∈ R^{n×n}`：残差混合矩阵（**被约束为双随机矩阵**）
- `H_pre^l, H_post^l`：输入/输出投影（参数化为非负系数）

**双随机矩阵约束**（Birkhoff 多胞体）：
```
M ∈ R^{n×n},  M·1 = 1,  1^T·M = 1^T,  M ≥ 0
```
每行和、每列和均为 1，所有元素非负。这保证：
- 信号是残差流的**凸组合**（convex combination），总特征质量守恒
- 谱范数 ≤ 1，从数学上截断梯度爆炸
- 矩阵乘法封闭：多层堆叠后仍保持双随机性

**训练时的约束维护**：Sinkhorn-Knopp 算法（1967）——交替行归一化/列归一化，每层训练用 **20 次迭代**。不是梯度下降后直接更新，而是每次前向传播时将 H_res 投影到双随机流形上。

**效果**：Amax Gain Magnitude 从 3000 降至 **~1.6**，提升 3 个数量级；wall-time 开销仅 **6.7%**（通过 kernel fusion + selective recomputation + DualPipe overlap 实现）。

#### CSA + HCA 混合注意力 — arXiv:2606.19348（DeepSeek-V4 完整技术报告）

**CSA（Compressed Sparse Attention）**：
- **压缩**：每 4 个连续 token 的 KV 信息压缩为 1 个 entry（压缩比 4:1）
- **稀疏选择**：用 DeepSeek Sparse Attention（DSA）的 Lightning Indexer 为每个 query 选择 Top-K 最相关的压缩 entry
- 效果：局部细节保留 + 计算量大幅降低

**HCA（Heavily Compressed Attention）**：
- **激进压缩**：KV cache 压缩比 **128:1**（每 128 个 token 压缩为 1 个 entry）
- **密集注意力**：不稀疏选择，每个 query 关注全部压缩后的 entry
- 效果：全局结构可见 + KV cache 极小

**交替堆叠**：模型在层间交替使用 CSA 和 HCA——CSA 提供"详细但选择性"的视图，HCA 提供"完整但低分辨率"的视图，两者互补捕获局部细节和全局结构。

**效率结果**（1M token 上下文， vs V3.2）：
- 单 token 推理 FLOPs：**27%**
- KV cache：**10%**（标准注意力基线的 ~2%）
- V3.2（61 层）1M KV cache 约 83.9 GiB → V4 降至 ~8.4 GiB

#### Engram 条件记忆 — arXiv:2601.07372

**问题**：Transformer 缺乏原生知识检索原语，被迫用昂贵的计算"模拟"查表——早期层浪费在重建静态 N-gram 模式上。

**核心机制**：Engram 是**现代化的 N-gram 嵌入表**，实现 O(1) 条件查找：
- **Key**：N-gram 的哈希值（multi-head hashing）
- **Value**：可学习的嵌入向量（embedding）
- **上下文感知门控**：根据当前 token 上下文决定是否启用 Engram 查找
- **多分支集成**：Engram 嵌入与主干网络输出融合

**与 MoE 的互补**：MoE 是**条件计算**（动态路由到专家），Engram 是**条件记忆**（静态查找表）。论文发现两者存在 **U 形缩放定律**——最优分配比例约 20-25% 参数给 Engram，其余给 MoE。

**效果**（27B 参数规模，iso-parameter / iso-FLOPs 对比纯 MoE）：
- 知识检索：MMLU +3.4，CMMLU +4.0
- **推理**：BBH +5.0，ARC-Challenge +3.7（更大提升）
- **代码/数学**：HumanEval +3.0，MATH +2.4
- **长上下文**：MultiQuery NIAH 84.2 → 97.0

**机制解释**：Engram 把早期层从"静态重建"中解放出来，等效于**加深了网络**用于复杂推理；同时把局部依赖委托给查找，释放注意力容量给全局上下文。

**基础设施效率**：确定性寻址支持运行时从主机内存预取，开销可忽略。

### 3. 训练与优化（来自完整技术报告 arXiv:2606.19348）

- **Muon 优化器**：替代 AdamW 用于大部分参数，用 Newton-Schulz 迭代正交化梯度更新，加速收敛并提升稳定性
- **FP4 量化感知训练**：从 SFT 阶段开始，权重 MXFP4、激活 MXFP8，兼容广泛硬件
- **训练数据**：V4-Pro 33T tokens，V4-Flash 32T tokens
- **共享 KV 注意力**：进一步减半 per-entry cache 大小
- **基础设施**：TileLang 编译器、batch-invariant 确定性 kernel、fused MoE megakernel、Z3 形式化验证

### 4. 效率数据（官方技术报告确认）

- 单 token FLOPs 仅为 V3.2 的 **27%**，KV cache 压缩至前代 **10%**
- SWE-bench Verified 官方自测：V4-Pro-Max 距 Claude Opus 4.6 Max 仅差 0.2 个百分点，价格约为对方 1/7
- 训练数据量：V4-Pro 33T tokens，V4-Flash 32T tokens

### 5. 国产算力优先策略

V4 优先适配华为昇腾等国产 AI 芯片，未向美国芯片供应商开放测试；训练阶段曾与华为、寒武纪深度合作重写底层程序。这一策略与 R2 延期暴露的昇腾训练稳定性问题（训练仍部分依赖英伟达）形成对照。

## 实践意义

- **开源 frontier 规模再上台阶**：1.6T 开源模型 + MIT 协议，自部署 V4-Flash 在消费级显卡成为可能
- **Agent 工作负载成本重构**：多轮长对话 token 消耗大幅压缩，直接利好长视野 Agent
- **灰度验证方法**：社区通过"思维链第一人称（I'm / I'll vs Let me）"判断是否已接入 V4 GA——模型行为指纹成为版本识别手段
- **生态位判断**：第三方评测认为 V4 整体接近 Opus 4.8 级别、编码直追 GPT-5.6 Sol，但相同任务所需迭代轮数多于 Fable 5；性价比仍是核心武器

## 跨厂商对比

- 与 [Kimi K3](../../kimi/blog/kimi-k3.md) 对比：K3 以 2.8T 参数走"开源最大规模"路线，V4 以 1.6T + 27% 计算量走"效率优先"路线——开源阵营内部出现"规模 vs 效率"两条路径分化
- 与 [GPT-5.6](../../openai/research/introducing-gpt-5-6.md) 对比：GPT-5.6 用 `max`/`ultra` 推理 effort 按需扩展，V4 用非思考 / Think High / Think Max 三档对应；V4 编码能力被评价为"直追 GPT-5.6 Sol"但价格显著更低
- 与 [Claude Values](../../anthropic/research/claude-values-models-languages.md) 互补：Anthropic 研究跨语言价值观一致性，DeepSeek 作为中文母语模型在小语种场景的表现值得关注

## 资源

- 完整技术报告：[arXiv:2606.19348](https://arxiv.org/abs/2606.19348)（DeepSeek-V4: Towards Highly Efficient Million-Token Context Intelligence）
- mHC 论文：[arXiv:2512.24880](https://arxiv.org/abs/2512.24880)
- Engram 论文：[arXiv:2601.07372](https://arxiv.org/abs/2601.07372)
- Engram 代码：[GitHub - deepseek-ai/Engram](https://github.com/deepseek-ai/Engram)
- 模型权重：[Hugging Face - deepseek-ai/DeepSeek-V4-Pro](https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro)
- 官网公告：[DeepSeek-V4 预览版本发布](https://mp.weixin.qq.com/s/8bxXqS2R8Fx5-1TLDBiEDg)
- API 文档：[Models & Pricing](https://api-docs.deepseek.com/quick_start/pricing)
- 模型体验：[chat.deepseek.com](https://chat.deepseek.com/)

> 注：mHC、Engram、CSA/HCA、Muon 优化器、训练基础设施部分均基于 arXiv 论文原文（2026-07-20 检索）。完整技术报告共 55+ 页，涵盖架构、训练、后训练、评估和基础设施全链路。
