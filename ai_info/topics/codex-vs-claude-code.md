# Codex 与 Claude Code 对比阅读路线

## OpenAI 线索

- [Introducing Codex](../openai/research/introducing-codex.md)：Codex 初始发布。
- [Codex Now Generally Available](../openai/research/codex-now-generally-available.md)：Codex GA、SDK 与企业功能。
- [Introducing the Codex App](../openai/research/introducing-the-codex-app.md)：Codex 桌面 App。
- [Introducing GPT-5.3-Codex](../openai/research/introducing-gpt-5-3-codex.md)：Codex 专用长任务模型。
- [Introducing GPT-5.3-Codex-Spark](../openai/research/introducing-gpt-5-3-codex-spark.md)：低延迟实时编码模型。
- [Codex for (almost) Everything](../openai/research/codex-for-almost-everything.md)：Computer Use、插件、记忆、自动化。
- [Work with Codex from Anywhere](../openai/research/work-with-codex-from-anywhere.md)：移动端、Remote SSH、Hooks 和企业工作流。
- [OpenAI and Dell Technologies Partner to Bring Codex to Hybrid and On-Premises Enterprise Environments](../openai/research/dell-codex-enterprise-partnership.md)：混合云与本地企业部署。

## Anthropic 线索

- [Claude Code Best Practices](../anthropic/engineering/claude-code-best-practices.md)：Claude Code 工作流最佳实践。
- [Claude Code Auto Mode](../anthropic/engineering/claude-code-auto-mode.md)：更少权限提示的安全模式。
- [An Update on Recent Claude Code Quality Reports](../anthropic/engineering/an-update-on-recent-claude-code-quality-reports.md)：Claude Code 质量问题事后分析。

## 对比维度

- 产品形态：Codex 覆盖 Web、CLI、IDE、App、移动端、插件、Remote SSH 和自动化；Claude Code 更强调开发者终端工作流与 MCP 生态。
- 安全策略：Codex 侧强调企业部署、沙箱、遥测和审计；Claude Code 侧强调权限、沙箱和自动化分类器。
- 上下文载体：Codex 常见载体是 AGENTS.md、Skills、Memory；Claude Code 常见载体是 CLAUDE.md、Skills、项目笔记。
- 工程方法：OpenAI 强调 Harness Engineering 和 Agent-first 环境设计；Anthropic 强调 Context Engineering、ACI 和长任务 Harness。
