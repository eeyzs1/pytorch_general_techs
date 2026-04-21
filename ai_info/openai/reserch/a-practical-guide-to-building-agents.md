# A Practical Guide to Building Agents

- **原文链接**: [A practical guide to building agents](https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/)
- **发布日期**: 2025
- **标签**: #Agent #实践指南 #编排 #护栏 #模型选择

## 核心观点

这是 OpenAI 面向产品和工程团队的 Agent 构建实战指南，提炼自大量客户部署经验。文章定义了 Agent 的核心特征，提供了识别适用场景的框架、Agent 逻辑和编排的设计模式，以及确保障碍物安全、可预测和有效运行的最佳实践。

## 关键概念

### Agent 的定义
Agent 是**独立代表用户完成任务的系统**。核心特征：
- 使用 LLM 管理工作流执行和做出决策
- 能识别工作流何时完成，并在需要时主动纠正行动
- 失败时可停止执行并将控制权交回用户
- 可访问各种工具与外部系统交互，在明确的护栏内动态选择工具

### Agent 的三大核心组件

1. **模型 (Model)**: 驱动 Agent 推理和决策的 LLM
2. **工具 (Tools)**: Agent 可使用的外部函数或 API
3. **指令 (Instructions)**: 定义 Agent 行为的明确指南和护栏

### 何时构建 Agent
优先考虑以下工作流：
- **复杂决策**: 涉及细微判断、例外或上下文敏感决策（如退款审批）
- **难以维护的规则**: 规则集过于庞大和复杂（如供应商安全审查）
- **重度依赖非结构化数据**: 需要解释自然语言或文档（如保险索赔处理）

### 模型选择策略
- 用最强模型建立性能基线
- 在满足准确率目标后，用更小模型优化成本和延迟
- 不同任务可使用不同模型（简单检索用小模型，复杂决策用大模型）

### 编排模式

#### 单 Agent
- 适合简单、明确的任务
- 从单 Agent 开始，仅在需要时演进到多 Agent

#### 多 Agent
- **管理者模式 (Manager)**: 中心 Agent 编排，委派给专门子 Agent
- **去中心化模式 (Decentralized)**: Agent 间平等交接

### 护栏 (Guardrails)
护栏在每个阶段都至关重要：
- **输入过滤**: 防止不安全输入
- **工具使用限制**: 约束 Agent 可执行的操作
- **人机协作 (Human-in-the-loop)**: 关键决策需人类确认

## 实践建议

- 从单 Agent 开始，验证后再扩展
- 先用最强模型建立基线，再优化成本
- 护栏不是可选的——是必需品
- 确定性解决方案可能就足够了，不要过度工程化

## 相关文章

- [Harness Engineering](harness-engineering.md) — Agent 规模化的工程方法论
- [Introducing Codex](introducing-codex.md) — OpenAI 的编码 Agent 产品
- [Introducing AgentKit](introducing-agentkit.md) — Agent 构建工具集
- [New Tools and Features in the Responses API](new-tools-and-features-in-the-responses-api.md) — Agent 开发 API
