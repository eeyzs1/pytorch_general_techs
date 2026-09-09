# 用 TRL 和 OpenEnv 训练编码模型画水彩（Training a coding model to paint watercolours with TRL and OpenEnv）

- **原文链接**: [Training a coding model to paint watercolours with TRL and OpenEnv](https://huggingface.co/blog/train-to-paint-with-code)
- **作者**: Sergio Paniego（Hugging Face；原创想法来自 Surya Narreddi）
- **发布日期**: 2026-09-03
- **检索日期**: 2026-09-09
- **标签**: #强化学习 #GRPO #创意生成 #代码生成 #OpenEnv

## 核心观点

2026 年 8 月，Surya Narreddi 的"语言模型画水彩"视频走红（超 150 万播放），模型用 p5.brush 写 JavaScript 作画，但原始工作未开源。Sergio Paniego 从工程侧完整复现并开源整条管线：TRL + OpenEnv，基座为 Qwen3.5-35B-A3B。奖励来自"品味"而非可验证答案，直接回答"能否对审美偏好做 RL"。

奖励由四项构成（gate 0.05、length 0.05、成对评审 0.60、HPSv3 审美模型 0.30），两个模型评审都是某人品味的代理；而"品味"最终由人工筛选的 178 幅参考画池定义——池即奖励函数，换池即换风格，代码一行不用改。

## 关键发现 / 关键技术

### 1. RL 环境与参考池
- 环境封装 p5.brush 库、限制性系统提示（47 个方法只允许 10 个）、headless Chromium 渲染与防作弊 gate；模型只能画填充形状，水彩晕染由库自动叠加，模型输出约 150 行可读、可改、可重跑的代码。
- 178 幅参考画分 love/okay 两档，全部由模型生成：GLM-5.2（64 幅）、Kimi-K3（57）、Qwen3-Coder-Next（35）、Qwen3.5-122B-A10B（22），从 iNaturalist 开放授权木槿实拍出发经三轮视觉模型反馈精炼、逐幅人工评级入选。
- 成对评审为 Qwen3-VL-30B-A3B-Instruct（经 Inference Providers 调用），与池中 4 幅参考双向对比，得分为获胜占比；HPSv3 为 7B 开源偏好模型，代表"平均人的品味"。

### 2. 三组奖励配比与训练修复
- judge-led（评审 0.60/HPSv3 0.30）与 hps-led（0.30/0.60）各跑 110 步，组均奖励（首末三分之一）分别 +0.27 与 +0.24；验证组 hps-only（0/0.90）60 步 +0.13。一步约 15–18 分钟。
- 四项 GRPOTrainer 修复解锁学习：lr 2e-5→5e-5、scheduler linear→constant_with_warmup、scale_rewards group→none、target_modules 手写清单→all-linear（MoE 投影命名不同导致原本只训到 40 层中的 10 层）。
- 模型最先学会的是"不再产出烂画"：总分 <0.3 的 rollout 在 judge-led 从 99 降到 16（hps-led 从 37 到 4）；评审项还把颜料覆盖率翻倍（0.11→0.23、0.13→0.30），说明学到的正是池所编码的个人风格。

## 实践意义

这是一份"RL over taste"的完整开源参考：主观奖励可以通过参考池 + 双评审建模，且增益可量化。对工程团队更大的启发是三点：调试方法论（先缩小问题直到有东西能学，再逐个加回难点）、MoE 模型 LoRA target_modules 的命名陷阱、以及 HF Jobs + Spaces + Inference Providers 组成的全托管 RL 基础设施——环境与评分模型都是可复制的 Space。

## 跨厂商对比

- 与 [Fast Gemma Challenge 验证 SOTA 配方：单流 A10G 上 510 TPS](fast-gemma-challenge-recipe.md) 对比：同为 TRL/GRPO 开源配方，一个用可验证奖励冲推理吞吐，一个用主观审美奖励学风格，展示了 GRPO 在两类奖励下的不同调试模式。
- 与 [100 步 GRPO 微调 350M 模型，获得更可靠的结构化输出](grpo-with-trl-ifstruct.md) 互补：同日发布的两篇 TRL GRPO 实操文，一个 350M 稠密模型的轻量微调，一个 35B-A3B MoE + 浏览器环境交互，覆盖 GRPO 落地光谱的两端。

## 资源

- 论文：N/A（原作者 Surya Narreddi 的完整技术报告预告中）
- 代码：[HuggingEnvs/02-watercolour](https://github.com/adithya-s-k/HuggingEnvs/tree/main/02-watercolour)
- Demo：[paint-with-code 合集](https://huggingface.co/collections/HuggingEnvs/paint-with-code-6a955b79d63f67f1631d9be6)（环境、评分模型、rollouts 数据集与训练脚本）
