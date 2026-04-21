# Raising the Bar on SWE-bench Verified with Claude 3.5 Sonnet

- **原文链接**: [Raising the bar on SWE-bench Verified with Claude 3.5 Sonnet](https://www.anthropic.com/engineering/raising-the-bar-on-swe-bench-verified)
- **发布日期**: 2025-01-06
- **标签**: #SWE-bench #Agent #工具设计 #ACI #基准测试

## 核心观点

升级版 Claude 3.5 Sonnet 在 SWE-bench Verified 上达到 49% 的成绩，超越了之前最先进模型的 45%。文章详细解释了围绕模型构建的"Agent"，旨在帮助开发者从 Claude 3.5 Sonnet 获得最佳性能。ACI 的核心理念来源于 [Building Effective Agents](building-effective-agents.md)。

## 关键概念

### SWE-bench 的特殊性
- 使用来自真实项目的实际工程任务，而非竞赛或面试风格的问题
- 尚未饱和——有大量改进空间（当时没有模型超过 50%）
- 测量的是整个"Agent"而非孤立的模型

### Agent 架构设计
文章重点展示了 Agent 的脚手架（scaffolding）设计如何显著影响性能，即使使用相同的底层模型。

### ACI 优化实战
最关键的发现：**花在优化工具上的时间比优化整体提示还多**。这一发现的系统化方法论参见 [Writing Effective Tools for AI Agents](writing-effective-tools-for-ai-agents.md)。

具体优化案例：
- 模型在使用相对文件路径时频繁出错，切换到绝对文件路径后错误消除
- 工具描述的精确性对 Agent 性能有巨大影响
- 将工具描述视为给初级开发者的文档字符串来编写

## 实践启示

- Agent 的性能不仅取决于底层模型，还高度依赖于脚手架设计
- 工具接口的设计（ACI）是 Agent 性能的关键杠杆
- 简单的工具描述优化可以带来显著的性能提升
- 在评估模型性能时，应将脚手架配置作为一等公民变量。但需注意 [Quantifying Infrastructure Noise in Agentic Coding Evals](quantifying-infrastructure-noise-in-agentic-coding-evals.md) 指出基础设施配置本身就能使基准分数波动数个百分点
- 更完整的评估框架参见 [Demystifying Evals for AI Agents](demystifying-evals-for-ai-agents.md)
