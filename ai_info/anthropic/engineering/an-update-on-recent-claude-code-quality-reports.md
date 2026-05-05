# An Update on Recent Claude Code Quality Reports

- **原文链接**: [An update on recent Claude Code quality reports](https://www.anthropic.com/engineering/april-23-postmortem)
- **发布日期**: 2026-04-23
- **标签**: #事后分析 #ClaudeCode #质量退化 #推理负荷 #上下文管理 #系统提示词

## 核心观点

2026年3月至4月，Claude Code 用户广泛报告响应质量下降。Anthropic 经过调查，确认问题并非模型能力退化或 API/推理层问题，而是三个独立的工程变更组合效应。所有问题已于 4 月 20 日（v2.1.116）全部修复。Anthropic 公开道歉并为所有订阅用户重置用量限额。

## 三个问题详解

### 问题 1：默认推理负荷从 high 降为 medium
- **时间线**: 3月4日部署，4月7日回滚
- **原因**: Opus 4.6 在 high effort 模式下偶尔思考过久导致 UI 卡死，为降低延迟和 token 消耗，将默认推理负荷从 high 改为 medium
- **问题**: medium effort 虽然延迟更低但在多数任务上智力略低，用户感知 Claude Code"变笨了"
- **受影响模型**: Sonnet 4.6、Opus 4.6
- **修复**: 回滚后所有用户默认 xhigh effort（Opus 4.7）或 high effort（其他模型）

### 问题 2：缓存优化 Bug 持续清除思考历史
- **时间线**: 3月26日部署，4月10日修复（v2.1.101）
- **设计意图**: 空闲超过1小时的会话，清除旧的思考内容以降低恢复会话的成本
- **Bug**: 本应只清除一次的思考历史，实际在每次对话轮次都被清除，导致 Claude 遗忘上下文、行为重复、工具调用异常
- **连锁效应**: 持续丢弃思考块导致缓存全部 miss，用户用量消耗超预期
- **检测困难**: 两个不相关的实验（消息队列、思考显示方式变更）抑制了 Bug 的可见性，即使经过多层 code review 和自动化测试也未能发现
- **关键发现**: 使用 Opus 4.7 回溯审查相关 PR 时，Opus 4.7 成功找到了 Bug 而 Opus 4.6 未能找到
- **受影响模型**: Sonnet 4.6、Opus 4.6

### 问题 3：系统提示词限制输出长度
- **时间线**: 4月16日上线（伴随 Opus 4.7），4月20日回滚
- **内容**: 添加 `"工具调用间文本 ≤25 词，最终回复 ≤100 词"` 的限制
- **初衷**: 减少 Opus 4.7 的冗长输出行为
- **问题**: 更广泛的评估显示代码质量下降约 3%（Opus 4.6 和 4.7 均受影响）
- **受影响模型**: Sonnet 4.6、Opus 4.6、Opus 4.7

### 完美风暴
三个变更各自影响不同的流量切片和时间表，聚合效应看起来像是广泛的、不一致的退化。加之内部使用和评估最初都未能复现问题，导致了较长的排查周期。

## 改进措施

1. **更多内部员工使用公开构建版本**（而非内部测试版本）
2. **强化 Code Review 工具**：允许额外仓库作为代码审查上下文，并交付给客户
3. **系统提示词变更的严格管控**：每次变更运行广泛的逐模型评估，逐行消融测试影响
4. **变更隔离**：模型特定变更应限制目标模型范围
5. **智力权衡变更**：增加浸泡期、更广泛的评估套件、渐进式发布
6. **透明沟通**：通过 @ClaudeDevs 和 GitHub 集中线程解释产品决策

## 关键教训

- **默认值的影响力远超预期**：绝大多数用户不会修改默认推理负荷设置
- **上下文管理的复杂性**：Bug 发生在 Claude Code 上下文管理、Anthropic API 和扩展思考的交汇处，越过了多层 review
- **基础设施 Bug ≠ 模型退化**：与 [A Postmortem of Three Recent Issues](a-postmortem-of-three-recent-issues.md) 一致的教训——用户感知的"变笨"往往来自工程层面
- **用户反馈是最后防线**：通过 /feedback 命令和公开可复现示例的用户最终帮助定位了问题

## 相关文章

- [A Postmortem of Three Recent Issues](a-postmortem-of-three-recent-issues.md) — 2025年的事后分析姊妹篇
- [Quantifying Infrastructure Noise in Agentic Coding Evals](quantifying-infrastructure-noise-in-agentic-coding-evals.md) — 基础设施噪声量化
- [Effective Context Engineering for AI Agents](effective-context-engineering-for-ai-agents.md) — 上下文管理方法论
