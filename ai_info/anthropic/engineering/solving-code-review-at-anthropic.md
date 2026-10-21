# Claude Code 团队的代码评审之道（How the Claude Code team does code review）

- **原文链接**: [How the Claude Code team does code review](https://claude.dev/blog/solving-code-review-at-anthropic/)
- **作者**: Addy Osmani、Morgan Westlee Lunt、Qing Wang
- **发布日期**: 2026-10-15
- **检索日期**: 2026-10-16
- **标签**: #代码评审 #AI写码 #分层防御 #风险分级 #ClaudeCode

## 核心观点

Claude 写了 Claude Code 约 90% 的代码，那"还有人读代码吗？"本文给出答案：评审没有消失，而是从"终点的闸门"变成"全程的拼写检查"。6–9 月间合并 PR 翻倍、回退率降 40%+ 的同时，团队把优化目标明确为"在不增加回退与事故的前提下，最小化人类评审时间"——人类时间同时计入"评审耗时"与"修坏代码耗时"两面，revert/事故率是守门指标。

六层防线：PR 前自证（给 Claude 可运行的验收方式）→ 每个 PR 必过 AI 评审（发现先经多 agent 投票过滤）→ 可阻断的安全评审 → 阻断式 CI → 按风险分级的人类审批（低风险可零人）→ merge queue + 灰度 + 快速回滚。核心哲学：风险由变更本身决定而非作者决定，agent 的批准永远不能充当人类的名额。

## 关键发现 / 关键技术

### 1. PR 之前：让工作可自证
- 给 Claude 能跑的验收（测试/构建/截图对比），要输出而非"我完成了"；子 agent 以新上下文审 diff
- Boris Cherny（Claude Code 作者）：给 Claude 验证方式"可能是最重要的事"，最终结果好 2–3 倍
- CLAUDE.md 保持短小 + REVIEW.md 由 code owners 维护（说清该仓库"失败长什么样"、要求文件行号证据）
- 反复被 flag 的问题修在源头：skill/lint 规则/说明文件

### 2. AI 评审与收敛治理
- Code Review for Claude Code GA（Team/Enterprise），研究预览上线后获实质性评审意见的内部 PR 从 16% 升至 54%
- 多 agent 找 bug → 另一组投票，够了票才贴出；纯风格/清理类发现被丢弃；按 Important/Nit/Pre-existing 标注
- 收敛问题被量化治理：一个 CLI PR 隔夜 50+ 轮评审；59% 的 flag 其实是"首轮就存在的旧代码"——对策为三轮上限、只审增量 diff、标记 bug 类别、不重复已贴发现；rounds-to-pass 与召回率并列追踪
- 事故即 eval：历史事故 PR + 修复/回退构成每日回归集

### 3. 人类审批的风险分级
- 分类器读变更定风险档：低（文档/内部功能/flag 后 additive）自动化全绿即并、零人；中（普通产品变更/缓存/自动更新/系统提示词）一人；高（最高危路径 + 白名单）两人
- 变更而非作者定档；受信作者名单才有轻量路径；触发变更者计入评审（"谁指使谁负责"）；approval 绑定具体 commit，agent push 后需重批

### 4. 人留在哪里
- 五类决策留给人：要不要做（方向/品味/范围）、高危代码（计费/自动更新/CI 工作流）、架构定式、读证据（测试输出/截图/发现）、对结果负责
- 知识传递换轨：无人再靠读 diff 学代码——要懂哪块就让 Claude 写那块的 explainer（几分钟、反映当下代码）
- "You land it, you own it"：变更小、一切可逆（flag/回退/灰度）、事故复盘看系统不追责

## 实践意义

这是目前最完整的"AI 写码时代的评审 SOP"，可直接裁剪采用（文末附分阶段落地清单：先 CI + PR 模板加 Testing/Risk/How to revert，再 AI 评审 + REVIEW.md，再风险分级 + CODEOWNERS）。三个最反直觉的数据：噪声对 agent 作者更贵（人会摆手，agent 会真去修又触发新一轮评审）；AI 评审的"轮次收敛"必须作为一等指标否则评审死循环；零人合并已在低风险档发生且边界持续移动。与 Scion 一文对照读：源码管理解决"合得进"，本文解决"敢不敢合"。

## 跨厂商对比

- 与 [Redesigning source control](redesigning-source-control.md) 姊妹篇：Scion 让 30,000 次/日合并可行，本文让这些合并不失控——agent 尺度研发的吞吐与质量双闸
- 与 [The AI-Native SDLC Playbook](the-ai-native-sdlc-playbook.md) 对比：SDLC 手册给六阶段框架，本文给评审阶段的全部操作细节——框架与实现的互补
- 与 [Demystifying Evals for AI Agents](demystifying-evals-for-ai-agents.md) 互补："事故变成每日 eval 集"把产品工程与模型评估的方法论打通——eval 即知识产权的工程体现

## 资源

- 论文：无
- 代码：https://code.claude.com/docs/en/code-review（Code Review for Claude Code）
- Demo：无
