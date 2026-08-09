# Gemini API Managed Agents 更新：3.6 Flash、hooks 与更多（Gemini API Managed Agents: 3.6 Flash, hooks, and more）

- **原文链接**: [Gemini API Managed Agents: 3.6 Flash, hooks, and more](https://blog.google/innovation-and-ai/technology/developers-tools/expanding-managed-agents-gemini-api-3-6-flash-hooks/)
- **作者**: Philipp Schmid, Mariano Cocirio
- **发布日期**: 2026-07-28
- **检索日期**: 2026-08-01
- **标签**: #Agent #GeminiAPI #ManagedAgents #工具调用 #Google

## 核心观点

Gemini API 的 Managed Agents 迎来发布后最重要的一次升级：默认模型切换为 Gemini 3.6 Flash，新增环境 hooks（在沙箱内对每次工具调用进行阻断、lint 或审计）、预算控制、定时触发器，并向免费层开放。这次更新延续 7 月 7 日的后台任务与远程 MCP 集成，把 Managed Agents 从"远程 agent 执行"推向"可编程的云上自动化层"。

Managed Agents 的形态是：单次 Interactions API 调用即可在隔离的云端 Linux 沙箱中协调推理、代码执行、包安装、文件管理与网络检索，开发者用 AGENTS.md / SKILL.md 定义自定义 agent 并注册为可版本化的托管 agent。

## 关键发现 / 关键技术

### 1. 默认模型升级与可选模型
- `antigravity-preview-05-2026` 默认运行 Gemini 3.6 Flash，无需改代码
- 可通过 `agent_config.model` 显式指定：3.6 Flash（默认，均衡）、3.5 Flash、3.5 Flash-Lite（最低延迟与成本）

### 2. 环境 hooks：沙箱内治理工具调用
- 在环境中加入 `.agents/hooks.json`，runtime 在 `pre_tool_execution` / `post_tool_execution` 事件执行自定义脚本
- `matcher` 支持正则（如 `code_execution|write_file` 或 `*`）；pre-hook 返回 deny 可跳过工具调用并把拒绝理由注入模型上下文
- 支持 command 与 http 两类处理器；AI 原生投行 OffDeal 已用 post_tool_execution 在远程沙箱内做自动化图像核验

### 3. 生产化控制面
- 预算控制（max_total_tokens）防止 runaway agent；定时触发器让 agent 周期性无人值守运行
- 免费层开放；配套 Environments API 管理沙箱会话
- 承接 7 月 7 日更新：后台执行（background: true 返回任务 ID）、直连远程 MCP server、自定义函数（requires_action 挂起由客户端执行）、会话中刷新凭证且保留沙箱状态

## 实践意义

Google 把 agent harness 的关键件（沙箱、hooks、预算、调度）做成托管服务，直接对标 OpenAI Agents SDK 与 Claude Agent SDK 的托管化方向。环境 hooks 是差异化亮点——把"权限提示"式治理升级为沙箱内可编程的 pre/post 拦截管道，为生产级 agent 合规与审计提供了可复用范式；代价是对 Google 环境（文件系统持久化、网络规则、凭证模型）的深度绑定。

## 跨厂商对比

- 与 [Anthropic Scaling Managed Agents](../../anthropic/engineering/scaling-managed-agents.md) 对比：Anthropic 分享自托管 agent 规模化后的基础设施经验，Google 则把整套 harness 托管化输出，前者教你自建、后者让你租用
- 与 [GPT-5.6](../../openai/research/introducing-gpt-5-6.md) 对比：OpenAI 以 Codex + max/ultra 推理档位深化单 agent 能力上限，Google 以 Managed Agents + hooks 拓宽多 agent 托管与治理平面

## 资源

- 文档：[Managed Agents in the Gemini API](https://ai.google.dev/gemini-api/docs/agents) / [Agent hooks](https://ai.google.dev/gemini-api/docs/agent-hooks)
- 前序更新：[Expanding Managed Agents（7 月 7 日）](https://blog.google/innovation-and-ai/technology/developers-tools/expanding-managed-agents-gemini-api/)
