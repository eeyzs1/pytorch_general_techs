# 论纳维–斯托克斯千年奖问题（On the Navier–Stokes Millennium Prize Problem）

- **原文链接**: [On the Navier–Stokes Millennium Prize Problem](https://openai.com/index/navier-stokes-solution/)
- **作者**: OpenAI
- **发布日期**: 2026-09-08
- **检索日期**: 2026-09-09
- **标签**: #数学 #NavierStokes #Lean形式化 #多Agent系统 #千年奖问题

## 核心观点

OpenAI 公布纳维–斯托克斯存在性与光滑性问题的解：由内部系统生成的分析证明表明，三维不可压缩流体从光滑初始状态（静止、受光滑外力、能量全程有限）出发，可在有限时间内发展出奇性——速度无界增长而外部作用力保持光滑。这解决了官方千年奖表述中的命题 C（及 D），该问题悬置约 90 年。

证明同时提供了 writeup 与 Lean 形式化。求解使用了一个能力显著超过 GPT-6 Astra、8 月 28 日才开始训练的内部模型（训练仍在进行），由约 1 万个并发 agent 组成的协调系统完成。OpenAI 明确表示不为此申领千年奖，公布目的是如实告知 AI 进展速度。

## 关键发现 / 关键技术

### 1. 结果的数学内容
- 解是向内螺旋并被轴向拉伸的涡旋——"像意面"：中心区域收缩且加速，但能量始终有限
- 技术难点在于让方程各项（加速度、压力梯度、动量输运、黏性）在流体自身运动中"变大而精确相消"，而非靠人为无穷大外力
- 历史脉络：Navier/Stokes 十九世纪奠基，Leray 1934 年广义解，2000 年入选七大千年奖问题

### 2. 求解过程：多 agent 协调系统
- 9 月 1 日受"两个千年奖问题已被解决"的传闻启发，启动对全部开放千年奖问题的评估；agent 分组并行尝试同一问题的不同变体（A/B 求证型、C/D 反证型）
- 意外先解决了无外力 Euler 方程正则性问题（约 100 个 agent 协作约 50 小时），随后集中资源转向 Navier–Stokes，并用 Codex 跨组汇总最有用洞察
- 9 月 5 日得到解——距启动约 88 小时；GPT-6 Astra 另用 17 小时完成 Lean 形式化验证
- 全部尝试合计 490 万条消息、约 3,000 亿输出 token；Navier–Stokes 部分占 270 万条消息、约 1,300 亿 token
- agent 具备读取缓存互联网与运行代码的工具，全程维持与前沿模型评估相同的监控与隔离保障

### 3. 并发工作与归属
- 传闻后确认与 Anthropic 员工 Levent Alpöge 和 NYU 教授 Tristan Buckmaster 的工作相关：他们解决的是 forced Euler 问题；OpenAI 主动联系提议联合公告并承认其优先权
- OpenAI 声明（研究者与 agent）在对方公开发布前未曾接触其工作，但不排除其脱敏产品使用数据帮助过模型改进；两组证明在 Euler 情形的具体结果亦不同（forced vs unforced）

## 实践意义

这是首个由 AI 系统主导完成的千年奖级成果，且与 Anthropic 侧的 Euler 工作同周出现——"AI 解决顶级数学开放问题"正从个例变为可复现的工作流。其方法论值得直接借鉴：问题变体分组并行、跨组洞察由 Codex 汇总再注入、Lean 形式化作为独立验证环节（且由另一模型执行），构成一条可审计的自动化研究流水线。对科学界，"不申领奖金、公开全部提示词与证明"的姿态为 AI 生成结果的学术归属立了先例；对安全社区，一个训练中模型即达此能力，进一步坐实了 an-alien-mind 所述"进展快于保障"的担忧。

## 跨厂商对比

- 与 [数学与理论计算机科学的十项进展](ten-advances-in-mathematics.md) 对比：十项进展是内部 Astra 版本在十个领域并行取证的广度展示（总成本约 $2,000 级），本文是集中约 1 万并发 agent、1.3 亿亿级 token 攻单一千年奖问题的深度案例，且模型已迭代到"显著超过 Astra"的下一代
- 与 [形式化费马大定理](../../anthropic/research/formalizing-fermats-last-theorem.md) 互补：同周双发——Anthropic 侧用 Lean 形式化已有经典定理（费马大定理），OpenAI 侧用 Lean 验证 AI 新产生的证明；两者共同确立"Lean 形式化 = AI 数学结果可信度基座"的行业规范

## 资源

- 官方文章：https://openai.com/index/navier-stokes-solution/
- 论文/系统卡：https://cdn.openai.com/pdf/32d9f210-8b73-45e0-91bc-82a30aef8a9a/navier-stokes.pdf（Euler 论文：https://cdn.openai.com/pdf/315b36cd-ec98-4023-8342-93345194ece1/euler.pdf）
- Lean 形式化证明：https://github.com/openai/NavierStokesAndEuler
