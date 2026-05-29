# 安全与可靠性阅读路线

## 运行时安全

- [Beyond Permission Prompts](../anthropic/engineering/beyond-permission-prompts.md)：文件系统隔离与网络隔离。
- [Claude Code Auto Mode](../anthropic/engineering/claude-code-auto-mode.md)：权限提示自动化与分类器防线。
- [Running Codex Safely at OpenAI](../openai/research/running-codex-safely.md)：企业内部 Codex 安全部署与 Agent 原生遥测。
- [Building a Safe, Effective Sandbox to Enable Codex on Windows](../openai/research/building-codex-windows-sandbox.md)：Windows 沙箱工程。
- [How We Built a System to Contain Claude Across Products](../anthropic/engineering/how-we-contain-claude-across-products.md)：跨产品 containment、防提示注入与工具边界。
- [Introducing OpenAI Privacy Filter](../openai/research/introducing-openai-privacy-filter.md)：PII 检测与本地隐私过滤模型。

## 模型行为与审计

- [Inside Our Approach to the Model Spec](../openai/research/inside-our-approach-to-the-model-spec.md)：模型行为规范。
- [Improving Instruction Hierarchy in Frontier LLMs](../openai/research/improving-instruction-hierarchy-in-frontier-llms.md)：指令层级与提示注入防御。
- [How We Monitor Internal Coding Agents for Misalignment](../openai/research/how-we-monitor-internal-coding-agents-for-misalignment.md)：编码 Agent 失准监控。
- [Where the Goblins Came From](../openai/research/where-the-goblins-came-from.md)：奖励信号偏差如何放大为可见行为。
- [Strengthening Societal Resilience with Rosalind Biodefense](../openai/research/strengthening-societal-resilience-with-rosalind-biodefense.md)：生物安全 trusted access 和防御加速。

## 关键结论

- Agent 自主性越高，越需要默认隔离、最小权限和可审计执行。
- 传统日志只能说明发生了什么，Agent 原生遥测还要解释为什么做。
- 安全不是单点机制，而是模型规范、指令层级、沙箱、审批、遥测、隐私过滤、trusted access 和评估的组合。
