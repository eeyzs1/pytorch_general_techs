# 发布 Gemini 3.6 Flash、3.5 Flash-Lite 与 3.5 Flash Cyber（Introducing Gemini 3.6 Flash, 3.5 Flash-Lite, and 3.5 Flash Cyber）

- **原文链接**: [Introducing Gemini 3.6 Flash, 3.5 Flash-Lite, and 3.5 Flash Cyber](https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-6-flash-3-5-flash-lite-3-5-flash-cyber/)
- **作者**: Tulsee Doshi（代表 Gemini 团队）
- **发布日期**: 2026-07-21
- **检索日期**: 2026-08-01
- **标签**: #Gemini #Flash #Agent #模型发布 #Google

## 核心观点

Google 一次发布三款 Gemini 模型，全部围绕"规模化构建 AI agent"的效率命题：3.6 Flash 作为主力模型在编码、知识工作与多模态上全面超越 3.5 Flash 且更便宜；3.5 Flash-Lite 以 350 tokens/s 成为 3.5 系最快、最具成本效益的高吞吐选项；3.5 Flash Cyber 则与 CodeMender 组合切入网络安全垂直场景。

文章同时披露两个重要信号：Gemini 3.5 Pro 正在合作伙伴中测试；Gemini 4 已启动"迄今最雄心勃勃的预训练"。

## 关键发现 / 关键技术

### 1. 3.6 Flash：更高效且更便宜的主力
- Artificial Analysis 显示输出 token 用量比 3.5 Flash 减少 17%，DeepSWE 上最高减少 65%
- 价格 $1.50/1M 输入、$7.50/1M 输出，低于 3.5 Flash
- 基准对比 3.5 Flash：DeepSWE 49% vs 37%、MLE Bench 63.9% vs 49.7%、OSWorld-Verified 83.0% vs 78.4%、GDPval-AA v2 1421 vs 1349
- computer use 成为 Gemini API 与 Gemini Enterprise 的内置客户端工具

### 2. 3.5 Flash-Lite：为高吞吐 agentic 工作流而生
- 350 输出 tokens/s（Artificial Analysis）；$0.3/1M 输入、$2.5/1M 输出
- 对比 3.1 Flash-Lite：Terminal-Bench 2.1 54% vs 31%、GDM-MRCR v2 长上下文 72.2% vs 60.1%、GDPval-AA v2 1140 vs 642
- 多项 agentic/编码评测反超 3 Flash：SWE-Bench Pro 54.2% vs 49.6%、OSWorld-Verified 74.0% vs 65.1%
- 支持 thinking level 配置：低档位跑高量任务，高档位处理多步子 agent 工作负载

### 3. 3.5 Flash Cyber in CodeMender 与安全
- 多个 3.5 Flash Cyber agent 协作产出单一报告，在 CyberGym 基准上以更低成本达到前沿竞争力
- 双重用途考量：仅通过 CodeMender 向政府与可信伙伴限量试点开放
- 3.6 Flash 配备增强 Frontier Safety 防护（CBRN 与网络攻击滥用），更抗越狱同时减少误拒

### 4. 可用性
- 当日上线 Gemini API（AI Studio、Android Studio）、Google Antigravity、Gemini Enterprise Agent Platform 与 Gemini app；3.5 Flash-Lite 同步接入 Google 搜索

## 实践意义

"token 效率"取代"跑分"成为本轮发布的主叙事：3.6 Flash 少 17% 输出 token + 更低单价，直接降低 agentic 任务的单位经济学成本；3.5 Flash-Lite 则瞄准主 agent + 子 agent 架构中的高量执行层。这是 Flash 系列对 GPT-5.6 "可扩展智能" 叙事的对位回应——两者都在把"为不同复杂度任务付不同价格"产品化。

## 跨厂商对比

- 与 [Gemini 3.5](gemini-3.5.md) 对比：3.5 确立 Flash 的前沿级智能，3.6 Flash 在同档位上把 token 效率与价格再压一档，并原生内置 computer use
- 与 [GPT-5.6](../../openai/research/introducing-gpt-5-6.md) 对比：OpenAI 用 max/ultra 推理档位纵向扩展单模型智能，Google 用 3.6/3.5-Lite/Cyber 横向切分工作负载，成本控制策略一纵一横

## 资源

- 模型卡：[Gemini 3.6 Flash](https://deepmind.google/models/model-cards/gemini-3-6-flash/) / [3.5 Flash-Lite](https://deepmind.google/models/model-cards/gemini-3-5-flash-lite/)
- 开发者指南：[Latest Gemini model](https://ai.google.dev/gemini-api/docs/latest-model)
