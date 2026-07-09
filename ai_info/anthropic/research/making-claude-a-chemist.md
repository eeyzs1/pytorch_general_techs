# Making Claude a Chemist

- **原文链接**: [Making Claude a chemist](https://www.anthropic.com/research/making-claude-a-chemist)
- **作者**: David Kamber（Anthropic 化学家）
- **发布日期**: 2026-06-05
- **检索日期**: 2026-06-29
- **标签**: #Science #Chemistry #NMR #Benchmark #GeneralPurposeModels

## 核心观点

Anthropic 启动"AI for Science"化学扩展计划。**Opus 4.7 在 NMR 谱预测上匹敌甚至超越 ChemDraw 和 MestReNova**——通用模型没有化学微调也能达到专用软件水平。**还能从 NMR 谱反向推导分子结构**——这是专用软件做不到的任务。

## 关键发现

### 1. 前向预测（结构 → NMR 谱）
- 在 20 个 ChemRxiv 预印本化合物（4 个骨架类，涵盖慢交换 NH、α-vinyl-imide 羰基、螺环酮、α-硅烷基甲磺酰胺等 NMR 挑战）上测试
- **Opus 4.7 氢谱误差 ±0.079 ppm**（远低于 ±0.20 ppm 的容差窗口）
- 碳谱：Opus 4.7 和 MestReNova 并列第一（±1.37 vs ±1.48 ppm）
- 峰形预测：Opus 4.7 匹配实验分裂模式最频繁；亚峰间距预测在 ±0.5 Hz 内的比例：**Opus 模型 ~80%，ChemDraw/MestReNova 26-35%**

### 2. 反向推导（谱 → 结构）
- Opus 4.7 在 8 个"简单"目标（单环或双片段）上**3 次运行 3 次正确**
- 在 7 个"困难"目标（融合环、螺环等）上，配合起始物料提示，4/7 在 3 次运行中都正确，剩余 3 个 2/3 正确
- **专用结构解析软件需要 2D NMR、专业训练和授权工具**——Claude 从 1D 谱和高分辨率质谱就能做到

### 3. 关键 NMR 难题
- 慢交换 NH 质子（在 6.8–7.9 ppm 窄带内）
  - Opus 4.7：始终略偏低，但稳定
  - Opus 4.6：猜测散落几个 ppm
  - Sonnet 4.6：放到 10–13 范围（错误）

### 4. 局限性
- 评估规模较小（20 个正向 + 15 个反向化合物）
- 困难目标需起始物料提示
- 未测试的化学骨架：慢交换 NH 杂芳烃（除氯吡嗪外）、2D 实验（HMBC、COSY、HSQC）、立体化学
- 未覆盖溶剂：methanol-d₄、benzene-d₆、acetone-d₆

## 关键洞察

1. **通用模型在专业领域已具竞争力**——Opus 4.7 在 NMR 任务上达到甚至超越 ChemDraw 和 MestReNova
2. **从"模拟"到"反向推导"的能力跳跃**——专用软件长期做不到的事，通用模型做到了
3. **可解释推理**——LLM 可以逐步展示推理过程，化学家可以审计
4. **CAS 增长太快**——290M+ 已披露物质，每天新增 15,000——AI 是唯一可持续扩展的工具

## 关键数据点

| 指标 | 数值 |
|------|------|
| 测试化合物数（正向） | 20（4 个骨架类 × 5） |
| 测试化合物数（反向） | 15（8 简单 + 7 困难） |
| Opus 4.7 氢谱 MAE | ±0.079 ppm |
| 容差窗口 | ±0.20 ppm（¹H）/ ±1.0 ppm（¹³C） |
| 亚峰间距预测准确率（Claude） | ~80% |
| 亚峰间距预测准确率（专用软件） | 26–35% |
| CAS 已披露物质 | 290M+ |
| 每天新增物质 | ~15,000 |

## 相关文章

- [Paving the Way for Agents in Biology](agents-in-biology.md)
- [Coding Agents in the Social Sciences](coding-agents-social-sciences.md)
- [How GPT-5 Helped Immunologist Derya Unutmaz Solve a 3-Year-Old Mystery](../../openai/research/gpt-5-immunology-mystery.md)