# Kimi (Moonshot AI) — 核心观点总结

> 汇总自 [Kimi Blog](https://www.kimi.com/blog/) 和 [Moonshot AI 开放平台](https://platform.moonshot.cn/blog) 的 3 篇文章，涵盖 2026 年 4 月至 7 月。

## 一、总体脉络

Moonshot AI 在 2026 年呈现清晰的"开源 frontier"战略：

```
开源模型规模突破 → 专用能力深化 → 评估体系创新
```

Kimi K3 以 2.8T 参数成为全球首个开源 3T 级模型，Kimi K2.6 在编码 Agent 领域达到开源 SOTA，PerceptionBench 则从评估侧推动多模态感知能力的诊断式进步。Moonshot 的差异化在于"开放 + 规模 + 专用能力"的三位一体。

## 二、核心主题

### 1. 开源 Frontier 模型

[Kimi K3](kimi-k3.md) 是 Moonshot 的旗舰模型，2.8T 参数、原生多模态、100 万 token 上下文。基于 **Kimi Delta Attention（KDA）** 和 **Attention Residuals（AttnRes）** 架构，专为长视野编程、知识工作和深度推理设计。K3 是开源社区首次进入 3T 参数级别，标志着开源模型与闭源模型的规模差距正在缩小。

**KDA（arXiv:2510.26692）**：线性注意力 + 通道级衰减门控，与 MLA 按 3:1 混合，KV cache 减 75%，1M 解码吞吐 6.3 倍。**AttnRes（arXiv:2603.15031）**：用 softmax 注意力替代固定残差累加，Block AttnRes 将内存从 O(L·d) 降至 O(N·d)，25% 训练效率提升。

**Stable LatentMoE**：16/896 专家激活（1.8% 稀疏度），四大关键技术——Quantile Balancing（分位数均衡消除启发式超参）、Per-Head Muon（注意力头级独立优化）、SiTU（Sigmoid Tanh Unit 激活控制）、Gated MLA（门控注意力选择性）。专家共享压缩潜在表示层，2.5× 缩放效率提升。

### 2. 开源编码 Agent

[Kimi K2.6](kimi-k2-6.md) 是编码专用模型，在长视野编码任务上达到开源 SOTA。典型案例：用 Zig 优化 Qwen3.5-0.8B 推理（12 小时、4000+ 工具调用、吞吐量提升 13 倍），自主重构 8 年历史的 exchange-core 金融引擎。K2.6 展示了开源编码 Agent 处理真实世界复杂工程任务的能力。

### 3. 多模态评估创新

[PerceptionBench](perception-bench.md) 是视觉感知评估基准，从模型失败中"发现"10 种原子感知能力。核心发现：无模型超过 60% 准确率，大量正确答案无法复现——当前多模态模型经常猜测而非真正感知。PerceptionBench 为改进视觉感知提供诊断工具。

## 三、关键数据点

| 指标 | 数值 | 来源 |
|------|------|------|
| Kimi K3 参数量 | 2.8T | Kimi K3 |
| Kimi K3 上下文长度 | 1M tokens | Kimi K3 |
| Kimi K3 开源地位 | 全球首个开源 3T 级模型 | Kimi K3 |
| Kimi K2.6 最长连续执行 | 13 小时 | Kimi K2.6 |
| Kimi K2.6 工具调用数（单任务） | 4,000+ | Kimi K2.6 |
| Kimi K2.6 吞吐量提升 | ~15 → ~193 tokens/秒 | Kimi K2.6 |
| PerceptionBench 问题数 | 3,000 | PerceptionBench |
| PerceptionBench 最高模型准确率 | <60% | PerceptionBench |
| PerceptionBench 原子感知类别 | 10 | PerceptionBench |

## 四、与 OpenAI / Anthropic 的对比

| 维度 | Kimi (Moonshot) | OpenAI | Anthropic |
|------|-----------------|--------|-----------|
| 模型策略 | 开源 frontier | 闭源旗舰 + 开源旧模型 | 闭源 frontier |
| 最大模型 | 2.8T (K3, 开源) | GPT-5.6 Sol (闭源) | Claude Fable 5 (闭源) |
| 编码 Agent | K2.6 (开源 SOTA) | Codex (闭源) | Claude Code (闭源) |
| 多模态 | 原生多模态 | 多模态 | 多模态 |
| 长上下文 | 1M tokens | 未公开 | 未公开 |
| 评估创新 | PerceptionBench (感知诊断) | LifeSciBench / GeneBench-Pro | BrowseComp / 内部评估 |
| 核心差异化 | 开放 + 规模 | Agent 工业化 + 企业生态 | 安全 + 可解释性 |

## 五、贯穿始终的原则

1. **开放是核心竞争力**：K3 和 K2.6 均为开源模型，降低 AI 使用门槛
2. **规模仍然重要**：2.8T 参数是能力的基础，Kimi 持续推动开源规模上限
3. **专用能力深化**：K2.6 专注编码，在特定领域达到 SOTA
4. **评估驱动进步**：PerceptionBench 从诊断角度推动感知能力改进
5. **架构创新**：KDA 和 AttnRes 解决长上下文信息衰减问题

## 六、文章索引

| # | 日期 | 文章 | 主题 |
|---|------|------|------|
| 1 | 2026-04-20 | [Kimi K2.6](kimi-k2-6.md) | 开源编码 Agent |
| 2 | 2026-07-16 | [Kimi K3](kimi-k3.md) | 开源旗舰模型 |
| 3 | 2026-07-16 | [PerceptionBench](perception-bench.md) | 多模态感知评估 |
