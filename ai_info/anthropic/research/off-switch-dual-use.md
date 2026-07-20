# 双重用途知识的"开关"：GRAM 模块化预训练方法

- **原文链接**: [An off switch for dual-use knowledge in AI models](https://www.anthropic.com/research/off-switch-dual-use)
- **作者**: Anthropic（与 AE Studio 合作）
- **发布日期**: 2026-07-08
- **检索日期**: 2026-07-20
- **标签**: #AI安全 #双重用途 #GRAM #模块化预训练 #访问控制 #生物安全

## 核心观点

Anthropic 与 AE Studio 合作提出 GRAM（Gradient-Routed Auxiliary Modules），一种在预训练时将双重用途知识隔离到可删除模块的方法。与数据过滤（训练后无法恢复）和事后遗忘（容易恢复）不同，GRAM 在训练时为每类双重用途知识创建专用"隔间"，训练后可选择保留或删除。实验显示，删除模块的效果接近从未训练过该数据，且不影响通用能力。这是首次在单次训练中实现"可配置能力"的前沿模型方法。

## 关键发现 / 关键技术

### 1. GRAM 架构与梯度路由机制

**架构**：在标准 Transformer 的 **MLP 块** 中添加小型辅助模块（auxiliary modules），每个模块对应一类双重用途知识（如病毒学、网络安全）。不是 MoE 的动态路由，而是**训练时静态分配**。

**梯度路由（Gradient Routing）核心机制**：
- 训练数据预先标记领域标签（如"病毒学"、"网络安全"）
- 前向传播：所有模块正常计算（为了 batching 效率）
- **反向传播**：通过**梯度掩码（gradient masking）** 控制参数更新
  - 通用文本：梯度更新所有参数（基础模块 + 所有辅助模块）
  - 双重用途文本：梯度**只更新对应辅助模块**，基础模块和其他辅助模块的梯度被置零
- 关键：知识在**参数级别**被隔离——病毒学知识只存储在病毒学模块的神经元权重中

**为什么删除模块后效果接近"从未训练"**：
- 基础模块从未接收过双重用途数据的梯度
- 辅助模块独立存储该领域知识
- 删除辅助模块 → 相当于该知识从未进入模型

### 2. 与现有方法的对比
| 方法 | 训练成本 | 可配置性 | 通用能力影响 | 抗恢复性 |
|------|---------|---------|-------------|---------|
| 数据过滤 | 高（需训练多模型） | 无 | 无 | 强 |
| 事后遗忘 | 低 | 无 | 有 | 弱（易恢复） |
| **GRAM** | **低（单模型）** | **强（16 种配置）** | **无** | **强** |

### 3. 实验验证
- **合成数据集**：儿童故事按主题标记，GRAM 可"忘记"任意主题，性能接近单独训练
- **真实数据**：网络文本 + 代码 + 科学论文，4 个双重用途领域（病毒学、网络安全、核物理、niche 编程语言），每领域约占训练数据的 **0.25%**
- **规模测试**：50M 到 5B 参数，GRAM 在各规模均匹配数据过滤效果
- **训练成本**：比训练 5 个独立数据过滤模型便宜 **5 倍**（单模型 + 4 模块 vs 5 个独立模型）

### 4. 安全性测试
- 删除模块后，攻击者难以用少量恶意数据恢复知识
- 与数据过滤的抗恢复性相当，远强于事后遗忘方法
- **局限**：对 128M token 的定向 fine-tuning 恢复攻击的抵抗力弱于数据过滤（论文坦承的限制）

## 实践意义

GRAM 为 AI 安全部署提供新范式：
- **差异化访问**：同一模型可根据部署场景配置不同能力
- **合规灵活性**：快速响应监管要求，无需重新训练
- **成本效率**：避免为不同安全级别训练多个模型
- **研究价值**：为"能力控制"提供可扩展的技术路径

## 跨厂商对比

- 与 [Strengthening Societal Resilience with Rosalind Biodefense](../../openai/research/strengthening-societal-resilience-with-rosalind-biodefense.md) 对比：OpenAI 采用"受信任访问"策略（控制谁能用），GRAM 采用"能力开关"策略（控制模型能做什么）
- 与 [OpenAI Privacy Filter](../../openai/research/introducing-openai-privacy-filter.md) 对比：Privacy Filter 过滤输出中的 PII，GRAM 在预训练时隔离知识
- 与 [GPT-5.6 Preview System Card](../../openai/research/gpt-5-6-preview-system-card.md) 互补：OpenAI 的安全栈是运行时防御，GRAM 是训练时防御

## 资源

- 官方博客：[An off switch for dual-use knowledge](https://www.anthropic.com/research/off-switch-dual-use)
- 完整论文：[Modular Pretraining Enables Access Control](https://alignment.anthropic.com/2026/modular-pretraining/)
- 代码：[GitHub - agencyenterprise/modular-pretraining](https://github.com/agencyenterprise/modular-pretraining)
- 数据集：[Hugging Face - AE-data/dual-use-papers](https://huggingface.co/datasets/AE-data/dual-use-papers)
- 相关工作：[Pretraining Data Filtering](https://alignment.anthropic.com/2025/pretraining-data-filtering/) / [Selective Gradient Masking](https://alignment.anthropic.com/2025/selective-gradient-masking/)

> 注：梯度路由实现细节基于 Anthropic 官方博客和第三方技术报道（techzeitgeist、remio）交叉验证；论文原文未公开梯度掩码的具体代码实现，上述描述为基于"每层添加辅助模块 + 训练时按数据标签路由梯度"的合理推断。
