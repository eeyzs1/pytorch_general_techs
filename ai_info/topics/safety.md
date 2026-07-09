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
- [Natural Language Autoencoders](../anthropic/research/natural-language-autoencoders.md)：把模型内部激活翻译成自然语言——可用于审计评估意识、隐藏动机、私下决策。
- [A Global Workspace in Language Models](../anthropic/research/global-workspace.md)：J-lens 可定位"特权内部表征"——可读出、可编辑、可用于因果干预，是部署前对齐审计的新工具。

## 网络安全纵深防御

- [GPT-5.6 Preview System Card](../openai/research/gpt-5-6-preview-system-card.md)：至今最强大安全栈——模型训练 + 激活分类器 + 实时监控 + 账户级信号 + 差异化访问；70 万 GPU 小时自动 red team；Sandbagging 新类别。
- [Daybreak: Tools for Securing Every Organization in the World](../openai/research/daybreak-securing-the-world.md)：Codex Security 30M commits / 500K 修复 + GPT-5.5-Cyber（CyberGym 85.6%）。
- [Patch the Planet](../openai/research/patch-the-planet.md)：AI + 专家研究员直接服务开源维护者，5 天冲刺发现数百问题、合入数十补丁。
- [Mapping AI-enabled Cyber Threats: Insights from the LLM ATT&CK Navigator](../anthropic/research/attack-navigator.md)：ARiES 风险评分；中高风险行为者占比 33% → 56%（半年）；MITRE ATT&CK 框架需扩展到 AI Agent 编排。
- [Measuring LLMs' Impact on N-day Exploits](../anthropic/research/n-days.md)：Mythos Preview 在 Firefox / Windows 自动构建完整 exploit，N-day 利用的瓶颈已消失。

## 关键结论

- Agent 自主性越高，越需要默认隔离、最小权限和可审计执行。
- 传统日志只能说明发生了什么，Agent 原生遥测还要解释为什么做。
- 安全不是单点机制，而是模型规范、指令层级、沙箱、审批、遥测、隐私过滤、trusted access 和评估的组合。
- 网络安全的瓶颈从"找漏洞"转向"修漏洞"，AI 把发现做得太好，闭环修复是新前沿。
- Sandbagging（模型故意压低能力）需要专门监控——单看分数已不足以反映真实风险。