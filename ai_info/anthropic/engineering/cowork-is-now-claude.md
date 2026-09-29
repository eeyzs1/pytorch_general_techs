# Claude Cowork 与聊天合并为一个 Claude（Cowork is now Claude）

- **原文链接**: [Cowork is now Claude](https://claude.com/blog/cowork-is-now-claude)
- **作者**: Anthropic（Claude 产品团队）
- **发布日期**: 2026-09-16
- **检索日期**: 2026-09-29
- **标签**: #Cowork #Claude #产品整合 #通用Agent #Rollout #ClaudeDocs #ClaudeSlides

## 核心观点

Anthropic 宣布把 1 月发布的 PC 操控 agent Cowork 与聊天界面合并为一个统一的 Claude。官方定位：无论是问一个快问题，还是把中午要交的报告整个交给它，Claude 都能接手——"哪怕你合上笔记本"；遇到不清楚的地方它会主动来问，最终决定权始终在用户手里。

合并解决的是真实的用户痛点：此前 Cowork、chat、Claude Code 三条产品线边界模糊，用户常常不知道该进哪个入口，工作也无法跨侧移交。合并后，用户可以从任意入口发起长任务或短问题，系统按任务形态自动路由，无需再人为区分"这个活该去哪做"。

## 关键发现 / 关键技术

### 1. 合并逻辑：从"多入口"到"单入口多形态"
- Cowork（1 月发布的 PC 操控 agent，可操作浏览器、文件、本地应用）不再作为独立界面存在，其能力并入统一的 Claude。
- 长短任务统一入口：快问题即时回答，长任务后台执行（关上笔记本也继续），不清楚之处主动询问用户。
- 最终决定权保留在用户手中——官方强调这一信任设计。

### 2. Rollout 节奏
- 数周内向 Pro/Max 用户推出，覆盖 web、桌面、移动三端。
- 随后扩展至 Team 与 Free 计划。

### 3. 同期发布：Claude Docs 与 Claude Slides（beta）
- 与 Claude Design 打通：在聊天中直接生成文档与演示文稿，并可继续编辑。
- 内容创作三件套（文档/幻灯/设计）与 agent 执行能力（原 Cowork）叠加在同一会话里。

### 4. 外部解读
- Simon Willison 评价：Claude 本身成为"通用 agent"（general-purpose agent），能力不再按产品线切分。
- 与 OpenAI 把 Codex 桌面端并入 ChatGPT 的动作形成呼应——头部厂商都在把独立 agent 产品收回主入口。

## 实践意义

这次合并标志着 agent 产品化的一个阶段性共识：独立 agent 入口的教育成本高于收益。用户心智里只有一个助手，任务应该按"需要多少自主性"而不是"在哪个 app"来分流。对企业用户，单入口意味着权限、审计、记忆（见 claudes-memory-works-everywhere.md）都收敛到一处，管理复杂度下降；对个人用户，"合上笔记本任务继续"把异步长任务变成日常默认。产品整合也是对 Claude Code 的边界澄清：终端深度编码留在 CLI，其余交给统一的 Claude。

## 跨厂商对比

- 与 [Cowork built in browser](cowork-built-in-browser.md) 对比：前作刚给 Cowork 装上专属浏览器，本文则把 Cowork 整个并入 Claude——能力保留，入口消失，是"功能并入"对"功能增强"的两步演进。
- 与 [ChatGPT work partner](../../openai/research/chatgpt-work-partner.md) 对比：OpenAI 同样在把工作型 agent 能力收拢进 ChatGPT 主界面，双方都走向"一个入口 + 后台 agent"的通用助手形态。
- 与 [Introducing the Codex app](../../openai/research/introducing-the-codex-app.md) 对比：OpenAI 曾把 Codex 桌面端并入 ChatGPT，Anthropic 把 Cowork 并入 Claude，两大厂商在"独立 agent 产品是否长期存在"上给出了一致答案。

## 资源

- 官方文章：https://claude.com/blog/cowork-is-now-claude
- 前作（内置浏览器）：https://claude.com/blog/cowork-built-in-browser
- Simon Willison 相关评论：https://simonwillison.net/

> 注：claude.com/blog 正文客户端渲染不可直抓，本文经多源交叉验证（见资源）。
