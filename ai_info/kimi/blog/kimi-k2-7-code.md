# Kimi K2.7 Code:开源长程编程模型(Kimi K2.7 Code)

- **原文链接**: [Kimi K2.7 Code: Open-Weights Long-Horizon Coding Model](https://www.kimi.com/resources/kimi-k2-7-code)
- **作者**: Kimi Team
- **发布日期**: 2026-06-12
- **检索日期**: 2026-09-29
- **标签**: #KimiK2.7Code #开源权重 #MoE #长程编程 #MCP #Agent

## 核心观点

Kimi K2.7 Code 是 Moonshot 面向长程编程任务的开源模型:1T 总参 MoE、激活 32B、256K 上下文,注意力采用 MLA,视觉侧内置 400M 参数 MoonViT,支持文/图/视频输入。模型仅提供思考模式,关闭 thinking 的场景由 K2.6 兜底。

相对 K2.6,Kimi Code Bench v2 从 50.9 提升到 62.0(+21.8%),MLS Bench Lite 从 26.7 到 35.1;MCP Mark Verified 达 81.1、超过 Opus 4.8 的 76.4,但整体编程基准仍落后 GPT-5.5(Codex)与 Opus 4.8。思考 token 平均节省 30%,叠加激进的缓存定价,显著拉低长程 Agent 的单位成本。

## 关键发现 / 关键技术

### 1. 规格与架构

- 1T 总参数 MoE,每 token 激活 32B
- 256K 上下文;注意力为 MLA
- 视觉:400M 参数 MoonViT,支持文本/图片/视频输入
- 61 层(其中 1 层稠密);384 个专家,每 token 选 8 个 + 1 个共享专家
- 词表 160K

### 2. 仅思考模式

- 模型只提供思考模式;用户关闭 thinking 时由 K2.6 兜底
- 思考 token 平均节省 30%(相对 K2.6)

### 3. 基准表现

| 基准 | K2.7 Code | 对比 |
|------|-----------|------|
| Kimi Code Bench v2 | 62.0 | K2.6 为 50.9(+21.8%) |
| MLS Bench Lite | 35.1 | K2.6 为 26.7 |
| MCP Mark Verified | 81.1 | 超 Opus 4.8 的 76.4 |

- MCP 工具调用可靠性首次反超最强闭源模型之一
- 整体编程基准仍落后 GPT-5.5(Codex)与 Opus 4.8

### 4. API 定价与高速版

- 输入:缓存命中 ¥1.30 / 未命中 ¥6.50 每百万 token;输出 ¥27.00 每百万 token
- 高速版:5-6 倍输出速度,消耗为 3 倍

### 5. 权重开源

- 权重开放:[Hugging Face - moonshotai/Kimi-K2.7-Code](https://huggingface.co/moonshotai/Kimi-K2.7-Code)

## 实践意义

- **长程 Agent 的成本模型**:思考 token 省 30% + 缓存命中 ¥1.30 的组合,直接降低 256K 上下文多轮工具调用场景的成本
- **MCP 可靠性标杆**:MCP Mark Verified 81.1 说明开源模型在工具调用上可胜任生产级 Agent
- **开源可自部署**:权重开放使其可进入私有化编码 Agent 栈,是 K2.8 闭源主力之外的开源主线

## 跨厂商对比

- 与 [Claude Code 最佳实践](../../anthropic/engineering/claude-code-best-practices.md) 对比:Claude Code 讲闭源 Agent 产品的工程用法,K2.7 Code 提供开源模型底座,两者可组合使用
- 与 [Kimi K2.6](kimi-k2-6.md) 对比:K2.6 主打长视野执行案例,K2.7 Code 在基准与思考效率上全面接棒
- 与 [Kimi K2.8 Preview](kimi-k2-8-preview.md) 对比:K2.8 为闭源 API 主力,K2.7 Code 仍是开源与高速版底座
- 与 [Kimi K3](kimi-k3.md) 对比:K3 是 2.8T 通用旗舰,K2.7 Code 是 1T 编程专用

## 资源

- 权重:[Hugging Face - moonshotai/Kimi-K2.7-Code](https://huggingface.co/moonshotai/Kimi-K2.7-Code)
- 资源页:[Kimi K2.7 Code](https://www.kimi.com/resources/kimi-k2-7-code)
- API:[Kimi OpenPlatform](https://platform.moonshot.cn/)
- 体验:[Kimi Code](https://www.kimi.com/code)

> 注:本文为补录(原文发布于 2026-06-12),检索日期按本次同步统一记为 2026-09-29。
