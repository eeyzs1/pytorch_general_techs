# PerceptionBench：评估多模态大语言模型的原子视觉感知能力

- **原文链接**: [Introducing PerceptionBench](https://www.kimi.com/blog/perception-bench)
- **作者**: Kimi Team
- **发布日期**: 2026-07-16
- **检索日期**: 2026-07-20
- **标签**: #PerceptionBench #视觉感知 #多模态评估 #基准测试 #MLLM #幻觉检测

## 核心观点

Kimi 发布 PerceptionBench，一个**从模型失败中发现而非预先定义**的视觉感知评估基准。通过归因前沿模型在 40+ 基准上的失败到最早视觉原因，提炼出 10 种原子感知能力和 3,000 个验证问题。核心发现：**没有模型超过 60% 准确率**，且总分相近的模型可能展现完全不同的感知优劣势。更严峻的是，大量正确答案在重复提问时无法复现——当前模型经常**猜测而非真正感知**。

## 关键发现 / 关键技术

### 1. 失败驱动的分类法
- 从 40+ 现有基准的真实模型失败中归因到最早错误步骤
- 非预先定义，而是从实际失败中"发现"10 种原子感知能力

### 2. 10 种原子感知类别
| 类别 | 占比 | 示例 |
|------|------|------|
| 深度与 3D | 11.0% | 桌子上有几个盘子？ |
| 视觉计数 | 11.0% | 图中有几个人？ |
| 视觉关系 | 11.0% | 最右边音符接触几条线？ |
| 视觉属性 | 11.0% | 有多少种颜色的帽子？ |
| 视觉定位 | 11.0% | 紫色线连接到杯子的哪个部分？ |
| 细粒度识别 | 9.7% | 棋盘上有几个黑皇后？ |
| 视觉比较 | 9.3% | 有多少个相同的动物剪影？ |
| 上下文整合 | 8.5% | 有多少只猴子碰过轮盖？ |
| 幻觉 | 9.0% | 图中有几个黄色空心环？（答案：0） |
| OCR | 8.5% | 蓝色数字是什么？ |

### 3. 核心发现
- **无模型超过 60% 准确率**
- 总分相近的模型可能有非常不同的感知 profile
- **大量正确答案无法复现**——模型在猜测而非感知

### 4. 与现有基准的关系
- 现有基准各覆盖感知的一小部分，重叠度低（平均 Jaccard 0.20）
- PerceptionBench 聚合和重新平衡这些碎片视图
- 提供"锐利诊断"而非"又一个分数"

## 实践意义

PerceptionBench 对多模态 AI 发展有重要价值：
- **诊断而非排名**：帮助开发者理解模型感知的具体弱点
- **感知 vs 推理分离**：隔离感知问题，避免被推理能力掩盖
- **幻觉检测**：专门类别检测模型"看到不存在的东西"
- **训练指导**：为改进视觉感知提供明确目标

## 跨厂商对比

- 与 [Introducing LifeSciBench](../../openai/research/introducing-life-sci-bench.md) 对比：LifeSciBench 是专家级科学任务基准，PerceptionBench 是基础感知能力基准
- 与 [Introducing GeneBench-Pro](../../openai/research/introducing-genebench-pro.md) 对比：GeneBench-Pro 关注"研究品味"，PerceptionBench 关注"原子感知"
- 与 [Eval Awareness in Claude Opus 4.6's BrowseComp Performance](../../anthropic/engineering/eval-awareness-browsecomp.md) 互补：都关注模型评估的可靠性问题

## 资源

- 基准页面：[PerceptionBench](https://www.kimi.com/blog/perception-bench)
