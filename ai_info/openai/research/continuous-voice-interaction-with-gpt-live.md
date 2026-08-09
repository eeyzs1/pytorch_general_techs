# GPT-Live 连续语音交互的工程实现

- **原文链接**: [How we built a realtime system for responsive voice AI in six months](https://openai.com/index/continuous-voice-interaction-with-gpt-live/)
- **作者**: Justin Uberti, Zahan Malkani (Members of Technical Staff)
- **发布日期**: 2026-08-03
- **检索日期**: 2026-08-08
- **标签**: #GPT-Live #语音AI #全双工 #低延迟 #WebRTC #工程架构

## 核心观点

这是 GPT-Live 发布后的工程深度文章，详述了 OpenAI 在六个月内构建实时语音 AI 系统的架构设计。核心突破是从传统的"轮次检测"架构转向全双工流式架构——语音模型同时听和说，消除了 turn detector 这一延迟瓶颈。当需要深度推理时，GPT-Live 异步委托给前沿模型（如 GPT-5.5），不阻塞对话流。

系统在每一层都针对低延迟优化：Go 语言重写媒体前端（p95 延迟降至原系统 p50 水平）、WebRTC 传输、有状态推理的无缝实例切换、以及自研 WARP 协议将启动握手从六次网络往返压缩到一次。

## 关键发现 / 关键技术

### 1. 从轮次到流式架构
- 传统语音 AI 依赖 turn detector 判断用户是否说完，猜早了打断用户，猜晚了响应迟钝
- GPT-Live 的全双工模型同时听和说，彻底移除 turn detector
- 音频流直接进出模型，深度推理和工具调用走异步路径

### 2. 有状态推理与无缝切换
- 长会话上下文持续增长，模型实例按需伸缩
- 切换机制：预热新实例 → 预填充当前上下文 → 双实例并行推理 → 就绪后切换
- 上下文压缩也作为托管过渡处理：原实例继续对话时在后台压缩并准备新实例，避免媒体中断

### 3. 异步委托路径优化
- 会话开始时即创建前沿模型推理会话并预填充初始上下文
- 使用稳定会话亲和性和 prompt caching 降低延迟
- 从连续语音中推导离散轮次：维护"投机视图"（供 UI）和"权威记录"（供日志）两套对话视图

### 4. WARP 协议与 Instant Connect
- 自研 WebRTC Abridged Roundtrip Protocol (WARP) 将媒体启动从六次网络往返降至一次
- 通过 SPED、DTLS 1.3、SNAP 等向后兼容改进实现
- Instant Connect 预先协商 SDP 参数，将信令交换移出关键路径
- 最终客户端只需一个 UDP 数据包即可启动会话

## 实践意义

该文为实时语音 AI 系统设计提供了完整的工程参考：媒体流与应用逻辑分离、有状态推理的实例管理、异步委托的延迟优化、以及传输层协议创新。WARP 作为开放规范已提交 IETF TSVWG，并已集成到 libwebrtc 和 Pion 中，惠及更广泛的 WebRTC 生态。

## 跨厂商对比

- 与 [GPT-Live 介绍](introducing-gpt-live.md) 互补：该文是产品发布介绍，本文是其工程实现深度解析，两者构成完整的 GPT-Live 技术图景
- 与 [大规模低延迟语音 AI 交付](delivering-low-latency-voice-ai-at-scale.md) 互补：前者奠定了流式媒体基础设施，GPT-Live 在此基础上进一步将流式推理推到模型层
- 与 [Gemini 3.5](../../google/deepmind/gemini-3.5.md) 对比：Google 的 Gemini Live 同样强调自然对话，但 OpenAI 的委托机制和 WARP 协议是独特的工程差异化

## 资源

- 论文：N/A
- WARP 协议规范：https://datatracker.ietf.org/doc/draft-uberti-tsvwg-warp/
- Demo：N/A
