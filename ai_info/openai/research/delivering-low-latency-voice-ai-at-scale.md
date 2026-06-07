# How OpenAI Delivers Low-Latency Voice AI at Scale

- **原文链接**: [How OpenAI delivers low-latency voice AI at scale](https://openai.com/index/delivering-low-latency-voice-ai-at-scale/)
- **作者**: OpenAI
- **发布日期**: 2026-05-04
- **检索日期**: 2026-06-07
- **标签**: #VoiceAI #WebRTC #基础设施 #RealtimeAPI #低延迟 #工程

## 核心观点

OpenAI 工程团队详细披露了 Realtime API 和 ChatGPT 语音能力的底层基础设施——重新架构的 WebRTC 堆栈，为 9 亿+ 周活跃用户提供自然对话速度的语音 AI。核心创新是将 WebRTC 流量拆分为无状态 Global Relay 和有状态 Transceiver 的分层架构。

## 关键更新

### 架构创新：Relay + Transceiver 分离
- **Edge Transceiver**：瘦边缘服务，终止客户端 WebRTC 连接（ICE、DTLS、SRTP 密钥、会话生命周期），将媒体转换为更简单的内部协议
- **Global Relay**：无状态 UDP 转发器，将内部协议通过少量稳定 UDP 地址传输到推理、转录、TTS 和编排服务
- 关键技巧：将路由元数据编码到 ICE ufrag 中，实现零热路径查找

### 解决的三大约束
- 单端口单会话的媒体终止
- 有状态 ICE 和 DTLS 会话
- 全球路由延迟

### 性能指标
- 美国客户端首字节时间约 500ms
- 语音到语音延迟目标 800ms
- 全球分布式 Relay 实现地理就近接入
- Relay 用 Go 实现，无需内核旁路

### 设计原则
- 拆分有状态和无状态组件
- 编码路由元数据避免查找
- 全球分布式 Relay 就近接入
- 保持简单实现

## 关键洞察

1. "模型 + WebRTC SDK 单机部署"已成为慢架构——生产级语音 AI 需要 Relay-Transceiver 分离模式
2. 将 WebRTC 复杂性限制在边缘层，使模型服务器可以部署在最便宜的 GPU 池中
3. 该架构为 ChatGPT 语音模式、Realtime API 和第三方语音 Agent 构建者提供了统一基础设施
4. 与 [MRC 超级计算机网络](mrc-supercomputer-networking.md) 和 [Symphony 编排](open-source-codex-orchestration-symphony.md) 一起，构成了 OpenAI 基础设施的全貌

## 相关文章

- [Advancing Voice Intelligence with New Models in the API](advancing-voice-intelligence-with-new-models-in-the-api.md)
- [Supercomputer Networking to Accelerate Large Scale AI Training](mrc-supercomputer-networking.md)