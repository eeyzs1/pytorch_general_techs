# Scaling Managed Agents: Decoupling the Brain from the Hands

- **原文链接**: [Scaling managed agents: Decoupling the brain from the hands](https://www.anthropic.com/engineering/managed-agents)
- **发布日期**: 2026-04-10
- **标签**: #Managed-Agents #架构解耦 #Brain-Hands #可扩展性 #容错

## 核心观点

Managed Agents 是 Anthropic 为长时间运行的 Agent 工作提供的托管服务，围绕一个关键架构原则构建：**接口必须比实现更持久**。文章明确将此定位为解决"尚未想象的程序"问题——与操作系统数十年前通过虚拟化解决的相同问题。核心架构决策是将"大脑"（Claude 及其 Harness）与"双手"（沙箱和工具）以及"会话"（会话事件日志）解耦。这是 [Harness Design for Long-Running Application Development](harness-design-for-long-running-application-development.md) 的基础设施层延伸——从应用层 Harness 设计到平台层解耦架构。

## 关键概念

### 三层解耦架构

1. **大脑 (Brain)**: Claude 及其 Harness
   - 负责推理和决策
   - 可独立升级和替换
   - Brain 层的 Harness 设计参见 [Harness Design for Long-Running Application Development](harness-design-for-long-running-application-development.md) 和 [Effective Harnesses for Long-Running Agents](effective-harnesses-for-long-running-agents.md)

2. **双手 (Hands)**: 沙箱和执行工具
   - 执行具体操作
   - 容器化，可随时销毁和重建
   - Hands 层的安全设计参见 [Beyond Permission Prompts](beyond-permission-prompts.md)——文件系统隔离和网络隔离的双重沙箱

3. **会话 (Session)**: 会话事件日志
   - 持久化记录所有操作
   - 支持故障恢复和审计

### 核心设计原则

- **接口比实现更持久**: 客户代码不应因模型升级而需要重写
- **容器可销毁**: 执行环境可随时重建
- **会话可恢复**: 故障后可从持久化日志恢复
- **凭据不可达**: 敏感信息与 Agent 隔离

### 性能提升
- p50 首个 Token 延迟降低约 **60%**
- p95 延迟降低超过 **90%**
- 实现了可扩展和容错的 Claude Agent 编排

### 操作系统类比
文章明确引用操作系统历史——"尚未想象的程序"——将此定位为基础设施层思维而非应用层优化。这表明 Anthropic 正在为模型能力不可预测扩展的未来构建基础设施。

## 实践启示

- 解耦是 Agent 规模化的关键架构决策
- 将推理、执行和状态分离使系统更健壮
- 为未来模型升级设计——接口应稳定，实现可演进
- 容错和可恢复性是生产 Agent 系统的必需品
- 凭据隔离是安全的基础
- [Building a C Compiler with a Team of Parallel Claudes](building-a-c-compiler-with-a-team-of-parallel-claudes.md) 的大规模并行 Agent 是 Managed Agents 的典型使用场景——16 个 Agent 的 Brain/Hands/Session 都需要独立管理
- [Building Agents with the Claude Agent SDK](building-agents-with-the-claude-agent-sdk.md) 提供了 Agent SDK 的编程接口，Managed Agents 是 SDK 的托管运行时
