# Claude Sonnet 5.5:Terminal-Bench 4.0 跃至 70.6%（Introducing Claude Sonnet 5.5）

- **原文链接**: [Introducing Claude Sonnet 5.5](https://www.anthropic.com/claude-sonnet-5-5)
- **作者**: Anthropic
- **发布日期**: 2026-09-28
- **检索日期**: 2026-09-29
- **标签**: #ClaudeSonnet55 #模型发布 #TerminalBench #AgenticCoding #网络防护 #性价比

## 核心观点

Claude Sonnet 5.5（2026-09-28 发布）是 5.5 家族第二款模型，定位为边界清晰的日常主力：常规任务、修 bug、文档/幻灯/表格，以及带"设计眼光"的产出。

速度比 Sonnet 5 快 30% 以上。定价不变（输入 $2 / 输出 $10、缓存读 $0.20），但 token 消耗大幅减少，单任务成本最多降 30%；中/低 effort 档以约 1/10 的单任务成本超过 Sonnet 5 最高档。

Terminal-Bench 4.0 从 Sonnet 5 的 10.3% 跃至 70.6%，甚至高于 Opus 5.5 的 66.4%；GDPval-AA 1844 仅比 Opus 5.5 低 2 分。

安全上，其网络攻击能力已与 Opus 5 相当，因此成为首个出厂即配 cyber safeguards 与回退机制的 Sonnet；自动行为审计多数指标持平或改善。

## 关键发现 / 关键技术

### 1. 5.5 家族第二款:定位边界清晰
- 发布节奏：Opus 5.5（09-22）→ Sonnet 5.5（09-28，本文）
- Haiku 5.5 数周内发布，届时 5.5 家族三档全覆盖
- 定位：日常任务、修 bug、文档/幻灯/表格、带设计眼光的产出
- 与 Opus 5.5 分工：Opus 承接最难任务，Sonnet 以更低价格覆盖高频日常工作

### 2. 速度与成本:同价更快、更省
- 比 Sonnet 5 快 30% 以上
- 定价不变：输入 $2 / 输出 $10 每百万 token，缓存读 $0.20
- token 消耗大幅减少，每任务成本最多降低 30%
- 中/低 effort 档以约 1/10 的单任务成本超过 Sonnet 5 最高档
- 三重节省叠加：单价不变 + token 减少 + 输出更快

### 3. 基准:agentic 能力跃迁
- Terminal-Bench 4.0：从 Sonnet 5 的 10.3% 跃至 70.6%，高于 Opus 5.5 的 66.4%
- GDPval-AA：1844，仅比 Opus 5.5（1846）低 2 分
- OSWorld 2.1：80.1%（计算机图形界面操作基准）
- HLE（带工具）：64.5%
- mid-tier 在 Terminal-Bench 上反超自家旗舰，旗舰与中端的能力差距收敛到"性价比"层面

### 4. 长视野任务:首个仅凭截图通关《宝可梦 红》的 Sonnet
- 成为首个仅凭截图通关《宝可梦 红》的 Sonnet 模型
- 长视野游戏要求跨大量步骤的稳定规划与自我纠错
- 官方将其作为 agentic 稳定性的标志性演示

### 5. 安全:cyber safeguards 首次随 Sonnet 出厂
- 自动行为审计：多数指标与 Sonnet 5 持平或改善
- 网络攻击能力已与 Opus 5 相当
- 因此成为首个出厂即配 cyber safeguards 与回退机制的 Sonnet
- 回退机制随防护出厂：被拦截的高风险请求自动回退，而非直接失败

## 实践意义

日常 agentic 工作流的默认选型标准应从"最强模型"转向"单位成本吞吐"：Sonnet 5.5 以 $2/$10 的价格在 Terminal-Bench 4.0 上反超旗舰，批量任务没有理由默认用 Opus 档。

effort 档位成为成本控制主杠杆：中/低档以约 1/10 成本超过上代最高档，批量任务应默认低档、按需逐级上调。

安全工程上，"防护随能力出厂"从旗舰下沉到 mid-tier：当 Sonnet 级模型也具备 Opus 5 级网络攻击能力时，分类器与回退机制不再是旗舰专属——这为全行业 mid-tier 模型的出厂安全标准提供了参照。

## 跨厂商对比

- 与 [Claude Opus 5.5](claude-opus-5-5.md) 对比：同家族分工——Opus 5.5（$4/$20）面向最难任务，Sonnet 5.5（$2/$10）覆盖日常 agentic 工作，并在 Terminal-Bench 4.0（70.6% vs 66.4%）与单任务成本上占优
- 与 [Claude Opus 5](claude-opus-5.md) 互补：Opus 5 确立了 effort 档位 + Fast 模式的智能分层设计，Sonnet 5.5"中/低 effort 约 1/10 成本超上代最高档"是同一设计哲学在 mid-tier 上的延续与验证
- 与 [Measuring the pace of AI development](measuring-pace-of-ai-development.md) 互补：Terminal-Bench 4.0 单代从 10.3% 到 70.6% 的跃迁，是能力-时间度量下 mid-tier 提速的典型样本

## 资源

- 发布页：https://www.anthropic.com/claude-sonnet-5-5
- 代码：N/A
- Demo：N/A
