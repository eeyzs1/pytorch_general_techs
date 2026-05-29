# Introducing GPT-5.3-Codex-Spark

- **原文链接**: [Introducing GPT-5.3-Codex-Spark](https://openai.com/index/introducing-gpt-5-3-codex-spark/)
- **作者**: OpenAI
- **发布日期**: 2026-02-12
- **检索日期**: 2026-05-29
- **标签**: #Codex #GPT-5.3-Codex-Spark #低延迟 #实时编码 #Cerebras

## 核心观点

GPT-5.3-Codex-Spark 是 GPT-5.3-Codex 的小型实时编码版本，也是 OpenAI 与 Cerebras 合作的首个里程碑。它的目标不是替代长时间自主运行的 Codex，而是补齐“实时修改、即时反馈、快速协作”的工作模式。

## 关键更新

### 实时编码体验
- 面向快速修改逻辑、重塑界面、目标性编辑等低延迟场景。
- 文章强调在超低延迟硬件上提供超过 1000 tokens/s 的体验。
- 与 GPT-5.3-Codex 的长任务能力互补：一个适合“跑很久”，一个适合“马上改”。

### Speed and intelligence
- Codex-Spark 是更小的模型，但仍保留足够真实编码能力。
- 适合用户在 IDE、App 或 CLI 中边看边改。
- 对交互式 Agent 产品来说，延迟本身就是能力的一部分。

### Powered by Cerebras
- OpenAI 将其作为与 Cerebras 合作的研究预览。
- 重点是验证超低延迟 serving 对开发者工作流的影响。

## 关键洞察

1. **Agent 产品需要多速度层**：长任务模型和实时模型应服务不同交互节奏。
2. **延迟影响信任和可控性**：实时反馈让用户更容易监督、纠偏和迭代。
3. **模型大小不是唯一变量**：serving 硬件、吞吐和端到端产品体验共同决定可用性。

## 相关文章

- [Introducing GPT-5.3-Codex](introducing-gpt-5-3-codex.md)
- [Introducing the Codex App](introducing-the-codex-app.md)
- [Codex for (almost) everything](codex-for-almost-everything.md)
