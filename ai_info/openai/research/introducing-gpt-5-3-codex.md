# Introducing GPT-5.3-Codex

- **原文链接**: [Introducing GPT-5.3-Codex](https://openai.com/index/introducing-gpt-5-3-codex/)
- **作者**: OpenAI
- **发布日期**: 2026-02-05
- **检索日期**: 2026-05-29
- **标签**: #Codex #GPT-5.3-Codex #AgenticCoding #ComputerUse #Cybersecurity #GDPval

## 核心观点

GPT-5.3-Codex 是 OpenAI 面向 Codex 的新一代 agentic coding 模型。文章把它定位为从“写代码和审查代码”扩展到“在电脑上完成专业工作”的模型：它能处理长任务、使用工具、进行研究、调试部署，并在工作过程中接受用户实时 steer。

这篇文章补上了 [Introducing the Codex App](introducing-the-codex-app.md) 与 [Codex for (almost) everything](codex-for-almost-everything.md) 之间的关键模型层更新。

## 关键更新

### Frontier agentic capabilities
- 在 SWE-Bench Pro、Terminal-Bench 2.0、OSWorld-Verified、GDPval 等指标上展示编码、终端、桌面操作和知识工作能力。
- 强调更少 token 完成 Codex 任务，说明能力提升和执行效率同时发生。
- 不只服务软件工程师，也覆盖设计、产品、数据分析、文档、表格和演示等知识工作。

### Interactive collaborator
- Codex 不再只是等待最终结果的后台执行器。
- 用户可以在运行中查看进度、询问思路、调整方向，并保持上下文连续。
- 这会改变人机协作节奏：从一次性委托变成持续 steering。

### Codex 参与训练和部署自身
- OpenAI 团队使用早期版本的 Codex 调试训练、分析评估结果、优化 harness、诊断上下文渲染和缓存问题。
- 这与 [Harness Engineering](harness-engineering.md) 的经验一致：Agent 不只是产出代码，也会成为构建 Agent 基础设施的工具。

### Cybersecurity safeguards
- GPT-5.3-Codex 被描述为 OpenAI 首个在 Preparedness Framework 下达到网络安全 High capability 的模型。
- OpenAI 同时部署更强的安全训练、自动监控、trusted access、威胁情报和降级路由机制。

## 关键洞察

1. **Codex 的边界从 coding 扩展到 computer work**：模型能力覆盖研究、文档、数据、部署和桌面操作。
2. **长任务需要实时 steering**：越强的 Agent 越需要用户能在中途介入，而不是只验收最终输出。
3. **Agent 会反过来加速 Agent 研发**：Codex 被用于训练、评估、部署和产品分析自身。
4. **能力提升会同步抬高安全门槛**：网络安全能力达到 High capability 后，访问控制和监控成为发布前提。

## 相关文章

- [Introducing the Codex App](introducing-the-codex-app.md)
- [Harness Engineering](harness-engineering.md)
- [Codex for (almost) everything](codex-for-almost-everything.md)
- [Running Codex Safely at OpenAI](running-codex-safely.md)
