# Granite Switch 4.1：一个端点同时会聊天、做决策、听语音（Granite Switch 4.1: Chat, Decisions, and Speech from One Endpoint）

- **原文链接**: [Granite Switch 4.1: Chat, Decisions, and Speech from One Endpoint](https://huggingface.co/blog/ibm-granite/granite-switch-4-1)
- **作者**: Kate Soule、Subhajit Chaudhury、Hendrik Strobelt、Luis A Lastras（IBM Granite 团队）
- **发布日期**: 2026-10-15
- **检索日期**: 2026-10-16
- **标签**: #IBM #Granite #ActivatedLoRA #决策模型 #多模态端点

## 核心观点

IBM 把 Granite Switch 项目的"模块化模型"思路推进到 4.1：Granite-Switch-4.1-8B 与 -30B 把三个能力组合进一个托管端点——通用 Decision aLoRA、安全专长 Guardian aLoRA（平均超过 Jev 1.13、Microsoft-Decision-1、GPT-Luna-Decisions、Clef-Flash 等决策模型）、以及嵌入的 Granite-Speech-5.0-Turbo-CTC（OpenASR 榜上最快的 ASR 模型）。同卡显存占用与裸底座相当：更多能力不更多 GPU。

关键是 Activated LoRA 的缓存复用：底座生成时建的 KV cache 可被后续任何 adapter 决策复用，配合团队给 vLLM 贡献的低秩 adapter 推理加速与同置 ASR 编码器，聊天请求、决策请求、语音请求可以在一个端点内高速"切换"。演示 Space 里 8B 模型实时完成"转写音频→生成摘要→安全筛查→15 个自定义标记检查"全链路。

## 关键发现 / 关键技术

### 1. 专家胜过通才

- Granite Libraries 的专长 adapter 在专门分类任务上普遍超过通用决策模型；adapter 共享底座 KV cache，"通才 + 若干专家"的边际成本几乎为零。
- 实测竞速：Granite-Switch-4.1-30B（冻结底座 + 4 个专家 aLoRA）跑完真实五步 RAG 工作流显著快于 Jev-27B（冻结 Qwen 底座 + 1 个通用 LoRA）。

### 2. 决策吞吐量级差

- 自定义 3B Granite Switch 玩 Doom：60–100 决策/秒，对照 Jev 报告的 10 决策/秒；且边玩边解说答疑——高吞吐决策场景（游戏、实时风控）是 aLoRA 架构的主场。

### 3. 可组合与可扩展

- 官方模型"电池齐全"但只是参考实现：任何人可从 Granite Libraries 目录混搭 adapter 编译自己的 Switch 模型；Mellea 的 Adapter SDK 与训练教程即将发布。

## 实践意义

"一个端点 = 聊天 + 决策 + 语音"直接命中企业集成的运维痛点：不用再维护三个服务的路由、扩缩容与版本对齐。aLoRA 的 KV cache 复用证明 adapter 路线在推理成本上可以打平单体模型——为"通用底座 + 可插拔专长"的企业模型架构提供了性能依据。

## 跨厂商对比

- 与 [Granite 4.2](granite-4-2.md) 对比：4.2 用真实沙箱 agentic RL 训"会思考的 dense 模型"，Switch 4.1 用 aLoRA 组合学"会切换的服务化模型"——IBM 开源双线并进：模型能力与部署架构各走一路。
- 与 [异步 GRPO+LoRA 跨 HF Jobs](async-grpo-lora-hfjobs.md) 互补：后者证明 LoRA 可以跨作业异步训练同步，前者证明 LoRA 可以零成本在线切换——rank-1 adapter 正在成为训练与推理两侧的共同接口。
- 与 [Claude Opus 5.5](../../anthropic/research/claude-opus-5-5.md) 对比：闭源前沿把能力全部收进单体模型，IBM 把专长外置为可组合 adapter——"能力内聚"与"能力组合"是当前模型工程的两大阵营。

## 资源

- 论文：[Activated LoRA（IBM Research）](https://research.ibm.com/blog/inference-friendly-aloras-lora)
- 代码：[generative-computing/granite-switch](https://github.com/generative-computing/granite-switch)
- Demo：[Speech-to-Decisions Space](https://huggingface.co/spaces/ibm-granite/speech-to-decisions)
