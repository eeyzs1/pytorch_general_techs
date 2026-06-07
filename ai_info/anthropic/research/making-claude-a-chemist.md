# Making Claude a Chemist

- **原文链接**: [Making Claude a chemist](https://www.anthropic.com/research/making-claude-a-chemist)
- **作者**: Anthropic (David Kamber)
- **发布日期**: 2026-06-05
- **检索日期**: 2026-06-07
- **标签**: #Claude #Chemistry #NMR #Science #Multimodal #AIforScience

## 核心观点

Anthropic 发布首个将 Claude 应用于化学领域的研究成果，展示 Claude 在 NMR（核磁共振）光谱预测和结构解析方面的能力，目标是将 AI 整合到化学家的日常工作流中。

## 关键内容

### Claude vs ChemDraw 的 NMR 预测对比

在 20 个化合物的测试中（来自训练截止日期后的 ChemRxiv 预印本）：

- **氢谱预测**：Opus 4.7 平均误差 ±0.079 ppm，远低于 ±0.20 ppm 的化学家接受窗口，优于 ChemDraw 和 MestReNova
- **碳谱预测**：Opus 4.7 与 MestReNova 基本持平（±1.37 vs ±1.48 ppm）
- **峰分裂模式**：Claude 三个模型 ~80% 正确率，而 ChemDraw/MestReNova 仅 26-35%

### 逆结构解析（从光谱推断结构）

这是传统软件做不到的任务。Opus 4.7 在 15 个问题上：
- 8 个简单分子：**100% 正确**（每次尝试都成功）
- 7 个复杂分子（给出起始物料提示）：4 个 100% 正确，3 个 3 次尝试中 2 次成功

### 未来方向

- 读取和渲染化学结构（从图片、专利、手绘转换）
- 反应与合成推理（路线规划、结果预测）
- 机理解释（电子箭头、中间体、过渡态）
- 化学文献理解（方法部分、支持信息、专利）

## 关键洞察

1. **通用模型无需化学专用微调**即可在 NMR 预测上匹敌甚至超越专业软件
2. Claude 能做传统软件做不到的**逆结构解析**（从光谱推断结构），这是化学家日常最耗时的任务
3. 扩展到 AI for Science 计划，支持化学研究
4. 化学领域 AI 工具长期未落地，主因是数据稀疏、格式不统一、付费墙。多模态 LLM 改变了这一局面