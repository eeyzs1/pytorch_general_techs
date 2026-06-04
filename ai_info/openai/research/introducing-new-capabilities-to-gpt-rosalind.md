# Introducing New Capabilities to GPT-Rosalind

- **原文链接**: [Introducing new capabilities to GPT-Rosalind](https://openai.com/index/introducing-new-capabilities-to-gpt-rosalind/)
- **作者**: OpenAI
- **发布日期**: 2026-06-03
- **检索日期**: 2026-06-04
- **标签**: #GPT-Rosalind #生命科学 #药物发现 #医疗化学 #基因组学 #Agent #Codex

## 核心观点

OpenAI 发布 GPT-Rosalind 更新，结合 GPT-5.5 的 Agent 编码和工具使用能力，在药物化学和基因组学等核心药物发现领域实现更强的模型智能。新模型在 LifeSciBench 基准上全面领先，同时推出了 Life Sciences Research 和 NGS Analysis 插件以及原生生物文件查看器。

## 关键更新

### LifeSciBench 基准
- 6 个工作流领域：证据处理、分析、设计与优化、科学推理、验证与操作、翻译与交流
- GPT-Rosalind 在所有领域领先 GPT-5.5

### 医疗化学（MedChemBench）
- 27.5% vs GPT-5.5 的 25.1%，Token 使用减少 7.2%
- 覆盖多模态化学结构理解、SAR、药物效力/毒性/ADME 预测、先导化合物优化、逆合成分析

### 基因组学与定量生物学（GeneBench）
- 准确率 21.6% vs GPT-5.5 的 20.4%，Token 使用减少 31%
- 涵盖功能基因组学、空间转录组学、蛋白质组学、表观基因组学、应用遗传学

### 湿实验室辅助（LabWorkBench）
- 63.2% vs GPT-5.5 的 55.8%，Token 减少 5.3%
- 基于真实实验室协议，测试扰动与实验结果的关联能力

### 插件与工具
- Life Sciences Research 插件：来源证据检索、生物学解释
- Life Sciences NGS Analysis 插件：生物信息学执行
- 原生生物文件查看器：序列、比对、结构查看器，支持上下文内交互

## 关键洞察

1. GPT-Rosalind 标志着从"通用模型"到"专业领域深度 Agent"的演进
2. LifeSciBench 采用端到端工作流评估而非单一维度，更贴近真实科研需求
3. 在专业领域同时提升准确率和降低 Token 消耗是模型优化的关键方向
4. 原生文件查看器 + Agent 推理 = 科研工作台而非问答工具

## 相关文章

- [Strengthening Societal Resilience with Rosalind Biodefense](strengthening-societal-resilience-with-rosalind-biodefense.md)
- [Introducing GPT-5.5](introducing-gpt-5-5.md)