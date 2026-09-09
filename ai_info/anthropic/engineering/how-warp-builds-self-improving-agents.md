# Warp 如何在 Claude 上构建自我改进 Agent（How Warp builds self-improving agents on Claude）

- **原文链接**: [How Warp builds self-improving agents on Claude](https://claude.com/blog/how-warp-builds-self-improving-agents-on-claude)
- **作者**: Michael Segner（Anthropic）与 Warp 团队（创始人兼 CEO Zach Lloyd 出镜）
- **发布日期**: 2026-08-26
- **检索日期**: 2026-09-09
- **标签**: #SelfImprovingAgents #AgentSkills #FeedbackLoop #OpenSource

## 核心观点

Warp（AI 终端与 Agent 化开发环境）把"会话结束即消失的用户反馈"变成了 Agent 的自我改进循环，并公开了一套人人可复用的简单模式：内层/基础技能（base skill）承载领域知识执行任务；人工反馈就地沉淀（PR 评论、issue 回复）；外层/改进技能（improver skill）作为观察者 Agent 定时运行，汇总累积反馈、对比 Agent 建议与人类反应，对基础技能提出最小修改。因为技能就是普通文件，Agent 极擅长更新它们——改动经正常 PR 评审合并后，下次运行自动继承改进。

问题起点是 Warp 内部代码审查 Agent：工程师抱怨其评论无用、输出低质；手工改 prompt、完善 AGENTS.md 都是止疼不治病。真正的问题是反馈随会话消失、从未进入 Agent 循环。该模式现已跑在 Warp 整个开源仓库上：spec 编写、review、triage 三个 Agent 各自带独立改进循环。

## 关键发现 / 关键技术

### 1. 规模与背景数据
- Warp 成立于 2020（创始人 Zach Lloyd），融资 $73M；80 万月活开发者在其上构建；56% 的 Fortune 500 在用。
- Warp 内累计运行 1000 万次 Claude Code 会话（每周 40 万+）；Warp Agent 对话总数 4000 万次。技术栈：Rust、Golang、GitHub Actions、内部 Agent 编排平台 Oz、Claude Platform。

### 2. 双技能 + 人工反馈的循环结构
- base skill：功能性领域知识与指令（如代码审查 Agent 执行所依据的技能）。
- 人工反馈：越具体越好——"你建议重命名这个变量，但我们的代码库约定这类全局变量用这种命名"，这类反馈告诉 Agent 下次怎么做对；反馈要零摩擦，在人们已在工作的地方（PR/issue 评论）自动捕获。
- improver skill：定时运行而非逐任务；拉取累积反馈，提出对 base skill 的小而聚焦的编辑；改动可评审、可批准、可合并，走正常 code review。
- 写技能的诀窍：写原则不写规则（"像指导一个聪明人，不是给计算机编程"）；解释 why 以利泛化；技能保持小并用渐进披露引用资源文件/脚本；反馈质量 > 数量（资深工程师的少量详细反馈比大量泛泛点赞值钱）；improver 技能高度可复用——代码审查 Agent 的 improver 与其他 Agent 的差异不大。

### 3. Issue triage 实例与边界条件
- 实例：新 GitHub issue 触发 GitHub Action 调 Agent 分析复杂度/可行性、打标签、建议修复方向；某次漏打 ready to spec 标签，维护者在 issue 上就地反馈（说明期望与原因）；Oz 上定时运行的 improver 用技能自带 Python 脚本拉取带反馈的 issue 汇总成 JSON 读回上下文，提出最小编辑开 PR（描述哪些信号触发了什么改动），人审合后下次生效。
- 最佳实践边界：技能 ≠ 记忆（程序性、稳定、需刻意变更 vs 推理时自动写入、永不停歇）；用模板化基础循环 + 领域加权平衡"一个还是多个 improver"；假定反馈会错——给 Agent 上下文做 sanity check、过滤谁的意见算数、保留人的过滤或终审；领域可验证就先建验证 harness 再让 Agent 对标调优；不可验证则靠确定性 golden-output eval 并把人类反馈限制在领域专家；追踪团队已在看的全局指标（time to merge、贡献者数、成本）回喂 improver，按 crawl-walk-run 节奏部署。

## 实践意义

这是"反馈驱动的持续改进"目前最清晰的可复制配方：不微调模型、不建复杂基础设施，只用文件化技能 + 定时观察者 + PR 工作流，就让任何 Agent 随时间变好，且人始终掌控变更。对工程团队，issue triage / 代码审查 / spec 编写三个开源场景可直接照抄；对平台设计者，"skills 即版本化知识资产"的定位值得借鉴——它把 prompt 工程变成了带评审的软件工程。

## 跨厂商对比

- 与 [Building self-improving tax agents with Codex](../../openai/research/building-self-improving-tax-agents-with-codex.md) 对比：同为"反馈驱动自我改进"，税务场景垂直且依赖领域校验，Warp 把同一思想通用化为文件化技能 + PR 循环，可移植性更强。
- 与 [Building effective agents](building-effective-agents.md) 互补：通用 Agent 设计模式回答"怎么建"，本文回答"怎么让建好的 Agent 持续变好"。

## 资源

- 官方文章：https://claude.com/blog/how-warp-builds-self-improving-agents-on-claude
- 相关产品：https://github.com/warpdotdev/warp-agents-demo-github-issue-triage（triage 演示）；https://www.anthropic.com/webinars/how-warp-builds-self-improving-agents-on-claude（网络研讨会）
