# 在 Claude 与 Claude Code 里用好 Opus 5.5（Getting the most out of Opus 5.5 in Claude and Claude Code）

- **原文链接**: [Getting the most out of Opus 5.5 in Claude and Claude Code](https://claude.dev/blog/getting-the-most-out-of-opus-5-5/)
- **作者**: Addy Osmani
- **发布日期**: 2026-09-22
- **检索日期**: 2026-10-16
- **标签**: #Opus55 #提示工程 #长任务 #模型回退 #使用指南

> 补录说明：本文发布于 2026-09-22（锚点 2026-09-28 之前），上次同步遗漏，本次补录入库。

## 核心观点

Opus 5.5 官方上手指南，围绕三个行为变化重组使用习惯：更长时间独立工作（要给整任务 + 明确终点线）、每轮回复前必思考（删掉"think carefully"类提示语）、结束时 plainly 汇报（先读"需要你什么"）。指南最有信息量的一节是"消息被标记怎么办"——Opus 5.5 是首个出厂带 Fable 级生物与网络防护的 Opus，被拦截的常规会话会静默切换到旧模型继续，用户需要知道如何识别与切回。

设计类提示的新范式：与其说"别太generic"（只是换一个默认风格），不如列出不要的具体样式（米白背景、斜体重点词、01/02/03 编号、胶囊按钮）。

## 关键发现 / 关键技术

### 1. 提问方式三则
- 整任务一次给全 + 说清"done"标准 + 何时才停下问我（例：迁移支付端点、删旧客户端、测试全过）
- 删除"think hard"行：内建思考已每轮触发，chat 产品实测删掉后响应更快且质量无明显下降
- 设计任务列出排除项清单；跑长任务时中途补充消息会入队不打断

### 2. 长任务操纵
- CLAUDE.md 写明停/不停规则：不需要输入就继续、状态注与下一步同条、仅破坏性操作前停
- 大审计/迁移拆 subagent：每服务一个子 agent，回报后查证据再收
- 任务清单放 TASKS.md 文件——比滚动回看更能抗 compaction

### 3. 检查结果
- 长跑结束先读"需要你做什么"；汇总格式可定制（Blocked on me / Changed / Found 三段）
- 让它先于人类评审 diff（早期测试者：最低 effort 的 Opus 5.5 比 high effort 的 Opus 5 抓更多 bug 且误报更少）
- 研究类任务要求标注"无法确认的部分及查过哪里"

### 4. 被标记时
- 触发面含整个对话（文件/搜索结果），不止最后一条消息
- Claude apps / Claude Code 均可关闭"被标记时自动切换模型"；/model 切回；/feedback 报误拦
- 要求复现内部推理会被拒（reasoning_extraction 类别）——改为"用三句话解释为何选这个方案"

## 实践意义

"终点线 + 停止条件"的整任务委托是 5.5 代模型的正确用法分水岭——仍按 Opus 5 习惯逐段指挥会浪费其长跑能力。防护默认化带来的静默降级是新问题：企业用户应默认关闭自动切换并培训识别"Switched to"提示，否则关键工作可能悄然落在旧模型上。subagent + 证据核查 + 文件化任务清单三件套可直接抄进团队 CLAUDE.md 模板。

## 跨厂商对比

- 与 [What a Task Costs on Opus 5.5](what-a-task-costs-on-opus-5-5.md) 姊妹篇：一篇讲怎么用得好，一篇讲花得明白——同日发布的用法与账单双指南
- 与 [Introducing Claude Opus 5.5](../research/claude-opus-5-5.md) 互补：发布页给基准与定价，本文给日常操作的完整 checklist
- 与 [Maximizing the Value of Your Claude Code Sessions](maximizing-value-of-claude-code-sessions.md) 对比：会话卫生篇聚焦 token 经济（/clear、/compact、缓存），本文聚焦任务委托模式——互补的两层用法指南

## 资源

- 论文：无
- 代码：无
- Demo：无
