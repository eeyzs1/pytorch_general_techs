# Harness Design for Long-Running Application Development

- **原文链接**: [Harness design for long-running application development](https://www.anthropic.com/engineering/harness-design-long-running-apps)
- **作者**: Prithvi Rajasekaran
- **发布日期**: 2026-03-24
- **标签**: #Harness设计 #GAN架构 #Planner-Generator-Evaluator #长时间运行 #自主开发

## 核心观点

从单 Agent 尝试转向**受 GAN 启发的架构**，涉及专门的 **Planner（规划者）、Generator（生成者）和 Evaluator（评估者）** 角色，以克服"上下文焦虑"和糟糕自我评估等问题。通过实施客观评分标准和自动化测试（如 Playwright），系统可以自主迭代数小时以产生高保真、功能完整的应用程序。这是 [Building Effective Agents](building-effective-agents.md) 中 Evaluator-Optimizer 工作流模式的演进——从两角色循环发展为三角色系统。

## 关键概念

### 从单 Agent 到多角色 Harness

#### 单 Agent 的问题
- **上下文焦虑**: Agent 担心上下文窗口耗尽，导致过早停止或保守行为。[Effective Context Engineering for AI Agents](effective-context-engineering-for-ai-agents.md) 的压缩和结构化笔记技术可缓解但不能完全消除此问题
- **自我评估困难**: Agent 难以客观评价自己的输出质量
- **长时间运行退化**: 随着会话延长，输出质量下降

#### GAN 启发的三角色架构

1. **Planner（规划者）**
   - 分析需求，制定详细计划
   - 将大任务分解为可管理的"Sprint"
   - 每个 Sprint 有明确的契约和验收标准

2. **Generator（生成者）**
   - 根据 Sprint 契约执行实现
   - 在每个 Sprint 中取得增量进展
   - 上下文重置后从计划文件恢复

3. **Evaluator（评估者）**
   - 客观评分 Generator 的输出
   - 使用自动化测试（Playwright 等）验证功能
   - 提供具体反馈指导下一轮迭代
   - Evaluator 的设计原则参见 [Demystifying Evals for AI Agents](demystifying-evals-for-ai-agents.md)——评估产出而非路径，内置部分得分

### Sprint 契约
- 每个 Sprint 有明确定义的范围和验收标准
- 契约是 Planner 和 Generator 之间的协议
- 完成标准可被 Evaluator 客观验证

### 上下文重置策略
- 在上下文窗口接近限制时主动重置
- 将进度保存到文件系统
- 新会话从保存的状态恢复
- 这是 [Effective Context Engineering for AI Agents](effective-context-engineering-for-ai-agents.md) 中压缩技术的主动版本——不等上下文腐烂发生，而是在临界点前主动重置

### 迭代 Harness 复杂度
- 随着模型改进，Harness 可以简化
- 当前需要复杂 Harness 是因为模型能力的限制
- 设计 Harness 时考虑未来模型升级的适应性

## 实验发现

- 结构化 Harness 增加了 Token 成本和延迟
- 但交付了显著更高的输出质量和功能完整性
- Agent 可以自主运行数小时构建完整应用
- 客观评分标准比 Agent 自我评估更可靠

## 实践启示

- 将规划、执行和评估分离为独立角色
- 使用自动化测试而非 Agent 自我评价
- Sprint 契约确保每个会话有明确的交付目标
- 随模型能力提升，逐步简化 Harness
- [Effective Harnesses for Long-Running Agents](effective-harnesses-for-long-running-agents.md) 是本文的前一版本——从初始化/编码双角色发展到 Planner/Generator/Evaluator 三角色
- [How We Built Our Multi-Agent Research System](how-we-built-our-multi-agent-research-system.md) 展示了多 Agent 协调的另一种模式——编排者-工作者而非 Planner-Generator-Evaluator
