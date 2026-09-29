# Kimi K3 开放日:权重、技术报告与三项 Infra 开源(Kimi K3 Open Day)

- **原文链接**: [Kimi K3 Open Day: Weights, Technical Report and Three Open-Source Infra Projects](https://www.kimi.com/news/kimi-k3-open-source)
- **作者**: Kimi Team
- **发布日期**: 2026-07-27
- **检索日期**: 2026-09-29
- **标签**: #KimiK3 #开放权重 #技术报告 #MoonEP #FlashKDA #AgentEnv #Infra开源

## 核心观点

开放日兑现了 07-16 K3 发布时的承诺:Hugging Face 上线 moonshotai/Kimi-K3 完整权重,同步放出技术报告,并额外开源 MoonEP、FlashKDA、AgentEnv 三项基础设施。K3 保持 2.8T 参数 MoE、原生视觉、1M 上下文,仍是全球首个开源 3T 级模型。

技术报告补齐架构细节:KDA 与 AttnRes 按 3:1 混合并引入 Gated MLA;Stable LatentMoE 采用 16/896 专家、SiTU-GLU 与 Quantile Balancing;MoonViT-V2 以 next-token prediction 目标从零训练;整体规模化效率约提升 2.5 倍。

三项 Infra 覆盖 MoE 训练通信、H20 推理内核与 Agent 沙箱,把"开源一个模型"扩展成"开源一条技术栈",复现与二次开发门槛显著降低。

## 关键发现 / 关键技术

### 1. 权重与技术报告正式发布

- 权重上传 Hugging Face:[moonshotai/Kimi-K3](https://huggingface.co/moonshotai/Kimi-K3)
- 完整技术报告随权重同步发布,兑现"07-27 见"的承诺
- 核心规格:2.8T 参数 MoE、原生视觉、1M 上下文;全球首个开源 3T 级模型

### 2. 架构:KDA + AttnRes 3:1 混合 Gated MLA

- KDA(线性注意力)与 AttnRes 按 3:1 比例交替,并在 MLA 路径引入门控(Gated MLA)
- 该组合兼顾长上下文的 KV cache 效率与全局信息聚合,支撑 1M 上下文

### 3. Stable LatentMoE:16/896 专家

- 16/896 专家配置(激活 16 / 总数 896),极端稀疏控制推理成本
- SiTU-GLU 激活:增强表达能力与训练稳定性
- Quantile Balancing:从 router-score 分位数直接推导专家分配,防专家崩塌

### 4. MoonViT-V2:视觉编码器从零训练

- 以 next-token prediction 为训练目标从零训练,而非对比学习式预训练
- 与语言主干统一训练目标,原生融入多模态 token 流

### 5. 规模化效率 2.5 倍

- 架构与数据的综合优化带来约 2.5 倍整体缩放效率提升(相对 K2 世代)

### 6. 三项 Infra 开源

#### MoonEP:MoE 专家并行通信库

- 面向 MoE 专家并行的训练通信库,降低超大稀疏模型的分布式训练门槛

#### FlashKDA:H20 prefill 加速内核

- 在 H20 上 prefill 阶段快 1.72-2.22 倍,直接服务受限算力生态

#### AgentEnv:快照/恢复/分叉沙箱

- 与 KVCache.ai 合作,为 Agent 提供快照、恢复、分叉的沙箱环境
- 支撑长程 Agent 的可复现实验与回滚调试

## 实践意义

- **开源从权重延伸到 Infra**:MoonEP/FlashKDA/AgentEnv 让外部团队首次能触及 K3 级训练与推理栈的关键环节,而不只是拿权重做推理
- **硬件适配示范**:FlashKDA 聚焦 H20,为受限算力环境部署前沿 MoE 提供官方参照实现
- **Agent 基建补齐**:AgentEnv 的快照/分叉能力是长程 Agent 评测与调试的刚需,可与现有 harness 生态直接结合

## 跨厂商对比

- 与 [GLM-5.3](../../glm/blog/glm-5-3.md) 对比:同为国内前沿开源模型,GLM 走性价比与生态路线,K3 以 3T 级规模 + Infra 全栈开源建立差异化
- 与 [DeepSeek V4 Flash 官方发布](../../deepseek/news/deepseek-v4-flash-official-release.md) 对比:DeepSeek V4 Flash 主打轻量高效,K3 开放日证明"极致规模 + 全栈开源"同样可行
- 与 [Kimi K3](kimi-k3.md) 互补:后者解析模型设计与基准表现,本文记录开放日的权重落地与三项 Infra 开源

## 资源

- 权重:[Hugging Face - moonshotai/Kimi-K3](https://huggingface.co/moonshotai/Kimi-K3)
- MoonEP:[GitHub - MoonshotAI/MoonEP](https://github.com/MoonshotAI/MoonEP)
- FlashKDA:[GitHub - MoonshotAI/FlashKDA](https://github.com/MoonshotAI/FlashKDA)
- AgentEnv:[GitHub - MoonshotAI/AgentEnv](https://github.com/MoonshotAI/AgentEnv)(与 [KVCache.ai](https://kvcache.ai) 合作)
- 发布解析:[Kimi K3](https://www.kimi.com/blog/kimi-k3)
- 体验:[Kimi.com](https://www.kimi.com/) / [Kimi API](https://platform.kimi.ai/)
