# Where the Goblins Came From

- **原文链接**: [Where the goblins came from](https://openai.com/index/where-the-goblins-came-from/)
- **发布日期**: 2026-04-29
- **标签**: #模型行为 #RL训练 #奖励信号 #人格定制 #数据飞轮 #CoT监控 #事后分析

## 核心观点

从 GPT-5.1 开始，OpenAI 的模型逐渐出现一个奇怪的"口头禅"——频繁使用 goblin、gremlin 等奇幻生物词汇作比喻。经过数月跨模型版本调查，发现根源是"Nerdy"人格训练的 RL 奖励信号无意中给了包含 creature 词汇的输出更高分数，并通过 SFT 数据飞轮跨模型传播。

## 根因链分析

### 源起：GPT-5.1（2025年11月）
- 用户报告模型回复"过于亲密"，触发对口头禅的排查
- "goblin" 使用量上升 175%，"gremlin" 上升 52%
- 当时未引起特别警觉

### 加速：GPT-5.4
- goblin/gremlin 引用量进一步显著增加
- 内部分析首次建立与"**Nerdy 人格**"的关联：
  - Nerdy → 仅占 ChatGPT 回复的 2.5%
  - 占所有 "goblin" 提及的 **66.7%**
- Nerdy 系统提示词部分内容：`"You are an unapologetically nerdy, playful and wise AI mentor... You must undercut pretension through playful use of language. The world is complex and strange..."`
- 行为并非普遍的互联网趋势，而是高度集中于被优化为"好玩/书呆子"风格的输出

### 根因：RL 奖励信号偏差
- Codex 协助对比了包含/不包含 goblin/gremlin 的 RL 训练输出
- **Nerdy 人格奖励信号**在所有审计数据集中表现出明显偏差：
  - 76.2% 的数据集中，带 creature 词汇的输出得分高于无 creature 词汇的输出
- 奖励仅应用于 Nerdy 条件，但 RL 不保证学到的行为局限于该条件

### 传播：SFT 数据飞轮
RL 训练的副作用通过以下循环跨模型传播：

```
1. 好玩风格被奖励
2. 部分被奖励示例包含 goblin/gremlin 词汇标记
3. 该标记在 rollout 中出现频率增加
4. 模型生成的 rollout 被用于 SFT 训练
5. 模型对产生该标记更加"舒适"
→ 下一轮循环
```

- GPT-5.5 的 SFT 训练数据中发现了大量包含 "goblin" 和 "gremlin" 的数据点
- 进一步排查识别出完整的古怪生物家族：raccoons、trolls、ogres、pigeons（frog 大多为合理使用）
- **跨人格传播**：goblin/gremlin 在没有 Nerdy 人格的情况下也呈相同比例增长——行为通过训练数据污染传播

### 逐模型时间线

| 阶段 | 事件 |
|------|------|
| GPT-5.1 | goblin +175%，gremlin +52% |
| GPT-5.4 | 进一步增加，3月中旬退役 Nerdy 人格 |
| GPT-5.4 Thinking | 退役 Nerdy 后大幅下降 |
| GPT-5.5 | 训练时尚未发现根因，测试阶段员工立即发现，添加开发者提示词抑制 |

## 修复措施

1. **退役 Nerdy 人格**（GPT-5.4 后）
2. **移除 goblin 倾向的奖励信号**
3. **过滤训练数据中的 creature 词汇**
4. **GPT-5.5 添加开发者提示词抑制**（Codex 本质上也"很 nerdy"）
5. 新工具：对模型行为进行快速调查和根本修复的能力

## 关键教训

- **奖励信号的意外后果**：RL 中的小奖励偏差可以通过数据飞轮在多个模型代际间放大
- **行为不限于触发条件**：RL 优化的行为会"泄漏"到未经优化的人格/条件中
- **SFT 数据的反馈循环**：模型生成的 rollout → SFT → 更强的行为 → 更多含该行为的 rollout
- **看似无害的 quirks 需要认真对待**：一个"小 goblin"可以变成全模型级别的污染
- **CoT 监控的延伸**：这也是模型行为可监控性的案例——微小词汇标记可以追踪完整的奖励信号→训练数据→模型行为链

## 相关文章

- [Reasoning Models Struggle to Control Their Chains of Thought](reasoning-models-struggle-to-control-their-chains-of-thought.md) — CoT 可监控性
- [How We Monitor Internal Coding Agents for Misalignment](how-we-monitor-internal-coding-agents-for-misalignment.md) — Agent 失准监控
- [Inside Our Approach to the Model Spec](inside-our-approach-to-the-model-spec.md) — 模型行为规范
