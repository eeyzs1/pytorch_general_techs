# 工具使用与 ACI 阅读路线

## 先读

- [Writing Effective Tools for AI Agents](../anthropic/engineering/writing-effective-tools-for-ai-agents.md)：Agent 工具设计五大原则。
- [Raising the Bar on SWE-bench Verified](../anthropic/engineering/raising-the-bar-on-swe-bench-verified.md)：通过 ACI 优化提升 SWE-bench 表现。
- [New Tools for Building Agents](../openai/research/new-tools-for-building-agents.md)：Responses API、Agents SDK 和内置工具。

## 规模化工具

- [Advanced Tool Use](../anthropic/engineering/advanced-tool-use.md)：工具搜索、程序化工具调用和工具示例。
- [Code Execution with MCP](../anthropic/engineering/code-execution-with-mcp.md)：用代码执行降低工具调用 token 成本。
- [The Next Evolution of the Agents SDK](../openai/research/the-next-evolution-of-the-agents-sdk.md)：Agents SDK 对 MCP 的支持。
- [Advancing Voice Intelligence with New Models in the API](../openai/research/advancing-voice-intelligence-with-new-models-in-the-api.md)：实时语音模型如何把工具调用和 Agent 行为带入 voice interface。
- [New Tools and Features in the Responses API](../openai/research/new-tools-and-features-in-the-responses-api.md)：Web 搜索、文件搜索、Computer Use 的工具层迭代。
- [Equipping the Responses API with a Computer Environment](../openai/research/equipping-the-responses-api-with-a-computer-environment.md)：把 Shell 工具 + 托管容器 + 服务端 Compaction + Agent Skills 组合为"系统级 Agent 执行"。

## 工具组合与垂直化

- [Codex for Every Role, Tool, Workflow](../openai/research/codex-for-every-role-tool-workflow.md)：90+ 插件、6 角色插件、62 应用、110 技能——OpenAI 把工具组合工业化。
- [Open-Source Codex Orchestration with Symphony](../openai/research/open-source-codex-orchestration-symphony.md)：把 Codex 接入企业自建协调器，多 Agent 调度的开源实现。
- [Codex-Maxxing for Long-Running Work](../openai/research/codex-maxxing-long-running-work.md)：把"工作树 + 测试 + Git"作为可验证工具组合，让 Agent 的执行可观测、可回滚。

## 网络安全与安全工具

- [Daybreak: Tools for Securing Every Organization in the World](../openai/research/daybreak-securing-the-world.md)：Codex Security 把"漏洞扫描 + 补丁生成 + PR 提交"做成端到端工具链；GPT-5.5-Cyber 在 CyberGym 85.6%。
- [Patch the Planet: A Daybreak Initiative](../openai/research/patch-the-planet.md)：把"AI + 专家研究员"直接做成开源维护者的工具，5 天冲刺发现数百问题、合入数十补丁。
- [Mapping AI-enabled Cyber Threats: Insights from the LLM ATT&CK Navigator](../anthropic/research/attack-navigator.md)：ARiES 风险评分工具 + MITRE ATT&CK 框架扩展到 AI Agent 编排。
- [Measuring LLMs' Impact on N-day Exploits](../anthropic/research/n-days.md)：Mythos Preview 自动构建完整 exploit 工具链——N-day 利用从手工走向工业化。

## 跨域工具

- [Project Fetch: Phase Two](../anthropic/research/project-fetch-phase-two.md)：把 Agent + 物理机器人作为统一工具组合，比人类快 18-37 倍。
- [Agents in Biology: Paving the Way for Autonomous Wet-Lab Discovery](../anthropic/research/agents-in-biology.md)：把湿实验、数据库查询、确定性工具组合为 VirBench 自动化工具链。
- [Making Claude a Chemist](../anthropic/research/making-claude-a-chemist.md)：把化学专用工具（ChemDraw / MestReNova）作为 Agent 的专业 ACI。
- [Brain2Qwerty v2](../meta/brain2qwerty-v2.md)：把"AI Agent 自动探索解码 pipeline 优化配置"作为科研工具——Meta 在脑机接口研究中用 Agent 探索超参空间，但最终训练配置由工程师手动选择，体现"Agent 探索 + 人类决策"的协作模式。

## 关键结论

- 工具描述就是 Agent-Computer Interface，应该像给新员工写操作手册。
- 工具数量变多后，需要动态发现、命名空间、示例和程序化编排。
- 工具输出要返回可行动上下文，而不是把无关日志倾倒给模型。
- 工具的"工业化组合"是 Codex 多角色插件、Symphony 协调器、Daybreak 安全工具链的共同方向——把单点能力变为可重复的端到端工作流。
- 垂直工具（化学/生物/安全）比通用工具更专业——把领域工具作为 ACI 一部分，模型才能在该领域达到专家级。
