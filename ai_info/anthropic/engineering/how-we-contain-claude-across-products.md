# How We Built a System to Contain Claude Across Products

- **原文链接**: [How we built a system to contain Claude across products](https://www.anthropic.com/engineering/how-we-contain-claude)
- **作者**: Hyung Won Chung, Jan Leike, Samuel Marks
- **发布日期**: 2026-05-25
- **检索日期**: 2026-05-29
- **标签**: #安全 #containment #Claude #PromptInjection #工具调用 #纵深防御

## 核心观点

Anthropic 把 Claude 的产品级安全问题定义为“containment”：当 Claude 能访问用户数据、连接外部工具并代表用户执行动作时，系统必须阻止模型被恶意内容诱导去泄露数据或执行越权动作。文章给出的核心指标是：在强对抗攻击下，防护前约 23.6% 的测试会发生数据泄露；多层防护后降到 0.000048%，也就是约 1 / 2,000,000 的攻击成功率。

这篇文章是 [Beyond Permission Prompts](beyond-permission-prompts.md) 和 [Claude Code Auto Mode](claude-code-auto-mode.md) 的产品级扩展：前两者强调沙箱和权限提示，这篇强调跨产品、跨连接器、跨工具执行场景中的系统性 containment。

## 防护架构

### 1. 运行前信任分级
- 对进入 Claude 上下文的信息做来源和可信度建模。
- 将用户明确指令、工具返回内容、网页/文档内容、第三方连接器结果分层处理。
- 关键思想：不是所有文本都能被当作同等优先级的指令。

### 2. 工具调用边界
- 对工具执行前后的数据流建立限制。
- 高风险动作需要额外校验，避免网页或文档中的恶意内容诱导模型调用敏感工具。
- 这种边界与 [Writing Effective Tools for AI Agents](writing-effective-tools-for-ai-agents.md) 中的 ACI 设计原则互补：工具不仅要易用，也要可控。

### 3. 检测器与策略组合
- 文章强调多层策略，而不是单个分类器。
- 防护包括提示注入检测、敏感数据流监控、工具调用审查和可疑转录分析。
- 与 [Claude Code Auto Mode](claude-code-auto-mode.md) 的两阶段分类器相似，但目标扩展到所有 Claude 产品。

### 4. 对抗性评估
- Anthropic 构建了专门的攻击评估集，用强对抗者模拟数据泄露和越权工具调用。
- 评估关注真实产品中可能出现的攻击路径：邮件、网页、文档、连接器、工具输出等。
- 这与 [Demystifying Evals for AI Agents](demystifying-evals-for-ai-agents.md) 的观点一致：安全评估必须覆盖 transcript、工具调用和最终状态。

## 关键洞察

1. **提示注入是系统问题，不只是模型问题**：模型能力提升不能替代产品层的权限、数据流和工具边界。
2. **防护必须组合使用**：单层检测器很难覆盖所有攻击路径，containment 依赖分层控制。
3. **攻击面来自连接器生态**：Claude 越能连接真实工作系统，越需要把不可信内容与用户意图分离。
4. **安全指标要贴近产品风险**：用“泄露概率”和“越权工具调用”这类结果指标，比只看分类准确率更接近真实风险。

## 与现有文章的关系

- [Beyond Permission Prompts](beyond-permission-prompts.md)：底层沙箱与权限隔离。
- [Claude Code Auto Mode](claude-code-auto-mode.md)：权限提示自动化与分类器防线。
- [Demystifying Evals for AI Agents](demystifying-evals-for-ai-agents.md)：Agent 安全评估方法。
- [Scaling Managed Agents](scaling-managed-agents.md)：Brain / Hands / Session 解耦后，containment 是 Hands 与工具边界的核心要求。
