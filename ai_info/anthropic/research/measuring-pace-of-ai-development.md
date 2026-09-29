# 理解前沿实验室内部 AI 发展速度的度量（Measuring the pace of AI development inside frontier labs）

- **原文链接**: [Measuring the pace of AI development](https://www.anthropic.com/institute/measuring-pace-of-ai-development)
- **作者**: Marina Favaro、Phillie Wright、Anthropic Institute
- **发布日期**: 2026-09-17
- **检索日期**: 2026-09-29
- **标签**: #AnthropicInstitute #治理 #AI研发自动化 #agent监督 #算力分配 #pacing

## 核心观点

呼应 CEO 的《We Must Pace the Frontier》主张，Anthropic Institute 指出：要求前沿实验室放慢速度的前提，是社会能"看见"实验室内部的发展速度。为此发布三项可公开的内部度量——AI 主导的 AI 研发占比、agent 监督、算力分配——把 pacing 从口号变成可审计的指标体系。

2026 年 8 月的数据勾勒出快速演进图景：Claude 在 Anthropic 的 AI 研发任务中 AL4 级（高层提示下端到端完成）占比从 2 月的不足 1% 升至 26%，AL3+ 合计超 90%；内部平台常驻约 3 万个研发 agent，在线监控覆盖 100% 动作，8 月超 10 亿次决策仅 0.002% 被拦截。算力侧，7 月快照显示 AI 研发算力约 6% 用于安全。团队承诺引入多家第三方评估者常驻核验。

## 关键发现 / 关键技术

### 1. 度量一：AI 主导的 AI 研发占比（R&D 自动化指数）
- 采用 Epoch AI 的 AL0-AL5 分级框架
- AL4 含义：高层提示下端到端完成任务
- 2026 年 8 月：Claude 在 Anthropic AI 研发任务中 AL4 占 26%，2 月不足 1%
- AL3+ 合计超过 90%；尚无 AL5 级任务

### 2. 度量二：agent 监督
- 内部平台常驻约 30,000 个研发 agent
- 在线监控覆盖 100% 的 agent 动作
- 2026 年 8 月：超 10 亿次决策中 0.002%（约 1/47000）被拦截
- 离线监控：每周标记约 10 万条转录
- 其中约 50 条升级人工审查

### 3. 度量三：算力分配
- 2026 年 7 月快照：AI 研发算力约 6% 用于安全
- AI 驱动的 AI 研发中约 12% 投向安全（口径偏保守）
- 该指标披露"AI 递归改进自身"与"安全投入"的算力比例关系

### 4. 方法论与可信度建设
- 自下而上构建 542 节点的任务树，约 15,000 条任务
- Claude 评审员与人类专家判定一致率 59%
- 对照：人类评审员之间一致率仅 35%
- 计划引入多家第三方评估者常驻，独立核验三组指标

### 5. 局限与后续
- 三项指标目前为单点快照，时间序列尚短
- 算力口径偏保守，实际安全占比可能更高
- 第三方常驻评估者落地后，指标可信度将脱离"自我报告"

## 实践意义

这是前沿实验室首次系统性公开"AI 做 AI 研发"的量化画面：

- 对治理研究：为监管提供了可要求、可核对的披露模板，pacing 讨论从此有了数字基础
- 对 AI 团队：AL 分级 + 任务树方法可直接迁移到任何组织的研发自动化程度自评；59% vs 35% 的一致率提示模型评审员的判定噪声未必高于人类互评
- 对行业：第三方常驻评估者若成为惯例，"自我报告"的信任问题将被结构性缓解

## 跨厂商对比

- 与 [研究加速：OpenAI 内部视角](../../openai/research/research-acceleration-view-inside-openai.md) 对比：OpenAI 披露内部研发 agent 达 3.1 agent-工作日/日、日耗约 600 美元的运营数据，本文提供 AL 分级 + 监督 + 算力三件套——两家首次从不同切面公开同一命题
- 与 [How We Monitor Internal Coding Agents for Misalignment](../../openai/research/how-we-monitor-internal-coding-agents-for-misalignment.md) 互补：同为内部 agent 监控度量，OpenAI 聚焦失准信号检测，Anthropic 公布拦截率与升级流程的绝对规模
- 与 [近期网络安全事件的对齐评估](alignment-assessment-cybersecurity-incidents.md) 互补：对齐评估解释"为什么要降速"（失准风险真实存在），本文回答"如何知道有没有降速"

## 资源

- 官方文章：https://www.anthropic.com/institute/measuring-pace-of-ai-development
- Pacing 倡议：https://www.pacingthefrontier.com/
- AL 分级框架（Epoch AI）：https://epoch.ai/
