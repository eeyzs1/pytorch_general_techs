# Speeding Up Agentic Workflows with WebSockets in the Responses API

- **原文链接**: [Speeding up agentic workflows with WebSockets in the Responses API](https://openai.com/index/speeding-up-agentic-workflows-with-websockets/)
- **作者**: Brian Yu, Ashwin Nathan
- **发布日期**: 2026-04-22
- **检索日期**: 2026-06-04
- **标签**: #ResponsesAPI #WebSocket #Agent #延迟优化 #GPT-5.3-Codex-Spark #API

## 核心观点

OpenAI 通过 Responses API 引入 WebSocket 模式，使 Agent 循环端到端延迟降低 40%。随着模型推理速度从 65 TPS 提升到近 1000 TPS，API 层面的开销成为瓶颈，WebSocket 持久连接通过缓存会话状态消除了重复的前置和后置处理开销。

## 问题分析

### Agent 循环延迟构成
- API 服务处理（验证、处理请求）
- 模型推理（GPU 生成 Token）
- 客户端时间（运行工具、构建上下文）

历史上推理是瓶颈，API 开销容易隐藏。但随着推理加速（GPT-5.3-Codex-Spark 达 1000+ TPS），API 开销变得显著。

### 结构性问题
- 每个 Codex 请求被当作独立请求处理
- 每次都要重新处理会话状态和可重用上下文
- 对话越长，重复处理越昂贵

## WebSocket 方案

### 技术设计
- 使用 WebSocket 保持持久连接和内存缓存
- 维护 `previous_response_id` 的缓存状态
- 缓存内容包括：上一个 Response 对象、输入输出项、工具定义和命名空间、预渲染的 Token

### 优化效果
- 安全分类器和请求验证器仅处理新输入
- 内存缓存渲染 Token，跳过不必要的 Tokenization
- 复用模型路由逻辑
- 重叠非阻塞的后推理工作（如 billing）

### 实际效果
- Codex 将大部分流量迁移到 WebSocket 模式
- Vercel AI SDK 集成后延迟降低 40%
- Cline 多文件工作流快 39%
- Cursor 中 OpenAI 模型快 30%

## 关键洞察

1. 随着推理加速，基础设施服务的速度也需要同步提升，否则用户无法感受到模型加速
2. WebSocket 持久连接是 Agent 工作负载的自然选择——Agent 本身是长连接任务
3. 保持 API 形状兼容降低开发者迁移成本
4. 这个模式为未来更快推理打开了空间

## 相关文章

- [Introducing GPT-5.3-Codex-Spark](introducing-gpt-5-3-codex-spark.md)
- [Equipping the Responses API with a Computer Environment](equipping-the-responses-api-with-a-computer-environment.md)