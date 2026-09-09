# Granite 4.2 LLM 的构建之道（Granite 4.2 LLMs: How They're Built）

- **原文链接**: [Granite 4.2 LLMs: How They're Built](https://huggingface.co/blog/ibm-granite/granite-4-2)
- **作者**: Yousaf Shah、Swanand Kadhe、Riddhiman Moulick 等（IBM Granite 团队）
- **发布日期**: 2026-08-25
- **检索日期**: 2026-09-09
- **标签**: #IBM #Granite #开源模型 #推理模型 #AgenticRL #长上下文

## 核心观点

IBM 发布 Granite 4.2：Granite 家族首批 dense decoder-only reasoning LLM，共 3B / 8B / 30B 三个尺寸，全部 Apache 2.0 开源。每个模型从零预训练于约 15T token，五阶段策略把上下文扩展到 512K token；SFT 使用思维链、推理与 agentic 轨迹数据；随后是多阶段强化学习管线，其中 8B 与 30B 额外经过 agentic RL——在真实沙箱环境中学习调用工具、编辑运行代码、驱动终端与搜索网页。

每个模型都有 thinking / non-thinking 开关与 low-effort 思考模式（对简单问题只花很短的推理预算），并支持原生 tool calling：经 OpenAI 兼容端点（如 vLLM）以 OpenAI function-calling 格式发出工具调用，无需额外胶水即可接入 agentic harness。

全文是一份"构建实录"：架构、预训练、SFT 数据与质控、多阶段 RL 管线、可扩展 agentic RL 基础设施、结果、量化（FP8/FP4/GGUF）与软硬件栈。

## 关键发现 / 关键技术

### 1. 架构与预训练
- GQA（40 注意力头 / 8 KV 头）、RoPE（θ = 10,000,000）、SwiGLU MLP、RMSNorm（ε=1e-5）、输入/输出 embedding 不共享、bfloat16
- 3B：40 层、embedding 2560、MLP 8192；8B：40 层、4096、12800；30B：64 层、4096、32768；序列长度均 131072
- 约 15T token 五阶段：1–2 阶段基础预训练，3–4 阶段中训练高质量数据退火，5 阶段长上下文训练扩展到 512K token

### 2. SFT 与多阶段 RL 管线
- SFT 约 720 万样本（约 100B token）：agentic 31.6% + 非 agentic 68.4%；30B 模型另有 Phase 2 SFT；配套数据质控流程
- RL 按阶段课程推进：Foundational RL 打技能基础 → Agentic RL（仅 8B/30B）在真实沙箱环境中学习行动 → RLHF 完成对齐；文章专门讨论支撑规模化 agentic RL 的基础设施
- 三尺寸差异主要在后训练：8B/30B 多出 agentic RL 块

### 3. 推理模式、量化与生态
- thinking / non-thinking / low-effort 三档；多轮对话含历史思考截断、思考与最终答案解析
- 量化提供 FP8、FP4 与 GGUF
- 支持 vLLM 与 SGLang（官方 cookbook）；可接入 OpenCode、Pi、OpenHands 等 agentic coding harness

## 实践意义

对企业团队：Apache 2.0 + 512K 上下文 + 原生工具调用 + 三档推理预算，构成可自托管的 reasoning/agentic 底座，且按算力分级选型（3B 起步、8B/30B 带 agentic RL）。对自建后训练管线的团队：多阶段 RL（尤其真实环境中的 agentic RL）的完整开源实录少见，阶段课程、奖励信号与基础设施章节可直接参考。

## 跨厂商对比

- 与 [Thinking Machines Inkling](thinkingmachines-inkling.md) 对比：同属"开源模型构建实录"，Inkling 代表独立实验室的数据与训练管线实践，Granite 4.2 展示企业级（IBM）多尺寸家族 + agentic RL 路线，后训练深度是主要差异
- 与 [Meta Muse Glimmer](../../meta/introducing-muse-glimmer.md) 对比：同为开源权重发布，Meta 主打前沿能力与生态影响力，Granite 4.2 主打企业可部署性（Apache 2.0、vLLM/SGLang、agentic harness 即插即用）与推理/工具链完备

## 资源

- 论文：N/A
- 代码：https://github.com/ibm-granite/granite-4.2-language-models
- Demo：https://huggingface.co/collections/ibm-granite/granite-42-language-models（HF 模型集合）
