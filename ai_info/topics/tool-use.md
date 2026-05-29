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

## 关键结论

- 工具描述就是 Agent-Computer Interface，应该像给新员工写操作手册。
- 工具数量变多后，需要动态发现、命名空间、示例和程序化编排。
- 工具输出要返回可行动上下文，而不是把无关日志倾倒给模型。
