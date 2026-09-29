# Claude 算出九圈散射振幅（Yes, Claude Can Do Nine Loops）

- **原文链接**: [Yes, Claude can do Nine Loops](https://www.anthropic.com/research/yes-claude-can-do-nine-loops)
- **作者**: Matt von Hippel（客座，物理学家/科学作家）；附 Lance Dixon（SLAC）后记；Anthropic 侧由 Liam Fitzpatrick、Siddharth Mishra-Sharma 执行
- **发布日期**: 2026-09-25
- **检索日期**: 2026-09-29
- **标签**: #AIforScience #散射振幅 #N4超杨米尔斯 #ClaudeScience #低成本前沿计算

## 核心观点

物理科普作家 Matt von Hippel 于 8 月 7 日向 AI 公司发起挑战：用学术界的算力预算，解决散射振幅领域的悬而未决问题（N=4 超杨-米尔斯九圈振幅或 N=8 超引力七圈）。不到一个月后，Anthropic 的两位物理学家用 Fable 5.1 在 Claude Science harness 中应战成功——Claude 以一条简单提示（"计算平面 N=4 SYM 的六粒子六边形振幅至九圈"）加"持续推进"的指令，自主完成了九圈 MHV 振幅的完整计算，并给出 bootstrap 与 form-factor 两条独立路径的互相印证。SLAC 的 Lance Dixon（八圈纪录保持者）验证了结果。

最重要的结论不是"AI 超越了计算极限"，而是"专家对极限的判断过于保守"——Claude 用已知方法 + 稍多算力 + 更好的软件工程就完成了人类以为做不到的事，且全程几乎无人类干预（一次性通过脆弱的多步计算）。同期中科院 Song He 团队用 GPT-6 辅助也得到九圈 symbol，人类+AI 竞争几乎同周撞线。

## 关键发现 / 关键技术

### 1. 低成本完成前沿计算
- 端到端成本约 1,000–2,000 美元（Claude Science 平台按需付费）；其中 bootstrap 计算的 Python/SymPy 部分约 $100——相当于 96 CPU 跑一周，对学术界完全可负担。
- 两条计算路径（直接 bootstrap、经由 antipodal duality 的 form-factor 间接路径）都由 Claude 自主选择并执行；提示词仅包含问题描述与"我去睡觉了，每 4-6 小时汇报一次"级别的监督。

### 2. 一次性可靠执行脆弱计算链
- Dixon 后记指出该计算"像失败的舒芙蕾"——任一步出错全盘崩溃，且大量细节无法完全写进论文，Claude 需要从头开发全部代码。Claude 一次性完成，验证者 Dixon 断言"Claude 对我们 2019 和 2023 论文的理解超过除合著者外的任何人类"。

### 3. 人机几乎同周撞线
- Song He 组（中科院）几乎同时用 GPT-6 辅助约束计算完成九圈 symbol——但只是"AI 辅助人类框架"而非 Anthropic 的"近无人类"路径。两组成果都由人类团队撰写论文发表，Claude 的角色已结束。

### 4. 对 AI 能力争论的校准
- 作者原期待看到"计算极限被超越"的惊人新方法，实际得到的是"低垂果实比想象的多"：简单明确的目标在专家眼中可能远比实际更难。作者 3 月还观察到 AI 做物理像"需要大量手把手的学生"，本次已是顶级专家才会碰的前沿计算——技术确实在快速变好。

## 实践意义

对科研团队：在明确、可验证的目标上，前沿 LLM + 付费科学 harness（Claude Science）已经可以在 1-2 千美元量级完成此前被认为"算力不可及"的计算任务；各领域应立即盘点自己的"九圈问题"并准备验证方案。对 AI 治理讨论：这是"计算瓶颈被高估"的直接证据——预测超智能风险时的"算力不足"反驳需要重新校准。

## 跨厂商对比

- 与 [形式化费马大定理](formalizing-fermats-last-theorem.md) 对比：费马大定理是 11 天、60 亿 token 的多 Agent 马拉松（验证已知数学），本文是单 Agent、千美元级的一周冲刺（推进计算前沿）——同为"AI 数理能力"展示位，成本结构差 3-4 个数量级，说明前沿计算的门槛正在快速下降。
- 与 [On the Navier–Stokes Millennium Prize Problem](../../openai/research/navier-stokes-solution.md) 互补：OpenAI 用万级并发 Agent 攻千年难题，Anthropic 用单 Agent + 消费级预算攻细分领域前沿；Song He 组用 GPT-6 做"辅助"恰好横跨两家范式。

## 资源

- 完整九圈结果：https://smsharia.io/cosmic-nine-loops/
- Song He 组并发结果（Zenodo）：https://doi.org/10.5281/zenodo.22800071
- 挑战原文：https://4gravitons.com/2026/08/07/it-only-counts-when-ai-gets-to-my-field/
- Lance Dixon 八圈论文：https://arxiv.org/abs/2308.08199
