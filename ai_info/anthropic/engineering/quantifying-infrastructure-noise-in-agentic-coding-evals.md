# Quantifying Infrastructure Noise in Agentic Coding Evals

- **原文链接**: [Quantifying infrastructure noise in agentic coding evals](https://www.anthropic.com/engineering/infrastructure-noise)
- **作者**: Gian Segato 等
- **发布日期**: 2025-11-26
- **标签**: #基准测试 #基础设施噪声 #评估 #可靠性 #资源配置

## 核心观点

仅基础设施配置就能使 Agent 基准测试分数波动数个百分点——有时甚至超过顶级模型之间的排行榜差距。在 Terminal-Bench 2.0 上，资源最多和最少的配置之间发现了 **6 个百分点的差距（p < 0.01）**。低于 3 个百分点的基准差异值得怀疑。这一发现与 [A Postmortem of Three Recent Issues](a-postmortem-of-three-recent-issues.md) 的教训一致——基础设施问题可能伪装成模型性能问题。

## 关键发现

### 两种资源体制

1. **修复阶段**（最高约 3× 基准指定资源）
   - 额外余量修复基础设施可靠性
   - 错误率从 5.8% 降至 2.1%（p < 0.001）
   - 不使任务变容易

2. **增强阶段**（超过 3×）
   - 额外资源主动帮助 Agent 解决更难的问题
   - 成功率攀升约 4 个百分点
   - 在 SWE-bench 上复现（5× RAM 时 1.54 个百分点）

### 统计显著性
- 朴素二项式置信区间已经跨越 1-2 个百分点
- 基础设施混淆因素叠加其上
- 3 个百分点以下的差异可能是噪声而非真实差异

## 实践启示

- 评估模型性能时，确保资源配置被**文档化、一致且作为一等实验变量**
- 在比较不同模型的基准分数时，考虑基础设施配置差异
- 不要轻信小幅度的基准改进——可能是基础设施噪声
- 为评估建立干净、一致的环境
- [Demystifying Evals for AI Agents](demystifying-evals-for-ai-agents.md) 提供了更完整的评估框架，其中第 5 步"构建健壮的评估工具"要求每次试验从干净环境开始——正是为了排除基础设施噪声
- [Raising the Bar on SWE-bench Verified](raising-the-bar-on-swe-bench-verified.md) 的 SWE-bench 评估实战中，基础设施配置也是影响结果的关键变量
