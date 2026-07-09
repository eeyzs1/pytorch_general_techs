# Codex 与 Claude Code 对比阅读路线

## OpenAI 线索

- [Introducing Codex](../openai/research/introducing-codex.md)：Codex 初始发布。
- [Codex Now Generally Available](../openai/research/codex-now-generally-available.md)：Codex GA、SDK 与企业功能。
- [Introducing the Codex App](../openai/research/introducing-the-codex-app.md)：Codex 桌面 App。
- [Introducing GPT-5.3-Codex](../openai/research/introducing-gpt-5-3-codex.md)：Codex 专用长任务模型。
- [Introducing GPT-5.3-Codex-Spark](../openai/research/introducing-gpt-5-3-codex-spark.md)：低延迟实时编码模型。
- [Codex for (almost) Everything](../openai/research/codex-for-almost-everything.md)：Computer Use、插件、记忆、自动化。
- [Codex for Every Role, Tool, Workflow](../openai/research/codex-for-every-role-tool-workflow.md)：多角色插件 + Sites + Annotations，覆盖 62 应用 / 110 技能。
- [Work with Codex from Anywhere](../openai/research/work-with-codex-from-anywhere.md)：移动端、Remote SSH、Hooks 和企业工作流。
- [OpenAI and Dell Technologies Partner to Bring Codex to Hybrid and On-Premises Enterprise Environments](../openai/research/dell-codex-enterprise-partnership.md)：混合云与本地企业部署。
- [OpenAI Frontier Models and Codex Are Now Available on AWS](../openai/research/openai-frontier-models-and-codex-are-now-available-on-aws.md)：AWS Bedrock 企业分发。
- [Access OpenAI Models and Codex Through Your Oracle Cloud Commitment](../openai/research/openai-on-oracle-cloud.md)：Oracle OCI 多云分发。
- [OpenAI to Acquire Ona](../openai/research/openai-to-acquire-ona.md)：收购 Git 持久化 Agent 厂商。
- [Building Self-Improving Tax Agents with Codex](../openai/research/building-self-improving-tax-agents-with-codex.md)：生产反馈驱动的 Agent 自改进循环。
- [Codex-Maxxing for Long-Running Work](../openai/research/codex-maxxing-long-running-work.md)：长视野任务的工程基础设施——持久化工作区、可验证步骤、人类监督判断。
- [How Agents Are Transforming Work](../openai/research/how-agents-are-transforming-work.md)：OpenAI 内部 97.9% 用户、99.8% 输出 token、80.6% 个人提交 30 分钟+ 任务——Codex 在工业级 Agent 部署中的真实地位。
- [HP Inc. Launches Frontier Strategic Partnership with OpenAI](../openai/research/hp-frontier-partnership.md)：HP Frontier 全企业级 Codex 部署，几周内 122 PR / 43 项目 / 释放 82 小时/周安全产能。
- [Introducing the OpenAI Partner Network](../openai/research/introducing-openai-partner-network.md)：$150M 投资，目标 2026 年底 30 万认证顾问。
- [OpenAI and Broadcom Unveil LLM-Optimized Inference Chip](../openai/research/openai-broadcom-jalapeno-inference-chip.md)：Jalapeño 自研推理芯片——9 个月 ASIC 周期，2026 年底吉瓦级部署。
- [Previewing GPT-5.6 Sol](../openai/research/previewing-gpt-5-6-sol.md)：Sol/Terra/Luna 三档模型 + `max`/`ultra` 推理 effort——Codex 任务的上限模型。

## Anthropic 线索

- [Claude Code Best Practices](../anthropic/engineering/claude-code-best-practices.md)：Claude Code 工作流最佳实践。
- [Claude Code Auto Mode](../anthropic/engineering/claude-code-auto-mode.md)：更少权限提示的安全模式。
- [An Update on Recent Claude Code Quality Reports](../anthropic/engineering/an-update-on-recent-claude-code-quality-reports.md)：Claude Code 质量问题事后分析。
- [Agentic Coding and Persistent Returns to Expertise](../anthropic/research/claude-code-expertise.md)：40 万 Claude Code 会话分析——70% 规划由人做、80% 执行由 Claude 做，编码能力不再是稀缺资源。

## 物理 Agent 与跨域延伸

- [Project Fetch: Phase Two](../anthropic/research/project-fetch-phase-two.md)：通用 Agent 在物理机器人上比人类快 18-37 倍——Codex / Claude Code 的方法论从数字域延伸至物理域。
- [Agents in Biology: Paving the Way for Autonomous Wet-Lab Discovery](../anthropic/research/agents-in-biology.md)：跨域 Agent 的工程化基础设施（VirBench 120 查询、91.3% → 接近 100%）。
- [Making Claude a Chemist](../anthropic/research/making-claude-a-chemist.md)：科学发现 Agent 的领域工程。

## 模型内部可解释性（双向延伸）

- [A Global Workspace in Language Models](../anthropic/research/global-workspace.md)：J-space / J-lens 让"读取模型内心独白"变为"可读出 + 可编辑 + 可干预"——为 Codex / Claude Code 的内部调试与对齐审计提供新工具。

## 对比维度

- 产品形态：Codex 覆盖 Web、CLI、IDE、App、移动端、插件、Remote SSH 和自动化；Claude Code 更强调开发者终端工作流与 MCP 生态。
- 安全策略：Codex 侧强调企业部署、沙箱、遥测和审计；Claude Code 侧强调权限、沙箱和自动化分类器。
- 上下文载体：Codex 常见载体是 AGENTS.md、Skills、Memory；Claude Code 常见载体是 CLAUDE.md、Skills、项目笔记。
- 工程方法：OpenAI 强调 Harness Engineering 和 Agent-first 环境设计；Anthropic 强调 Context Engineering、ACI 和长任务 Harness。
- 经济部署：Codex 已进入 OpenAI 内部 97.9% 用户、AWS/Oracle/Dell/HP 多云全栈、Partner Network 30 万顾问；Claude Code 在 40 万会话中验证"专业规划 + Agent 执行"的新分工。
