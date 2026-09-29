# 两周把 claude.ai 提速 3 倍（How we made claude.ai 3x faster）

- **原文链接**: [How we made claude.ai 3x faster](https://claude.dev/blog/how-we-made-claude-ai-faster/)
- **作者**: Raymond Wang、Sam Attard、Issac G.（Anthropic 应用工程）
- **发布日期**: 2026-09-23
- **检索日期**: 2026-09-29
- **标签**: #性能优化 #ClaudeTag #CI棘轮 #前端工程 #Agent驱动开发 #claude.ai

## 核心观点

Anthropic 应用工程团队回顾 8 月的一次两周性能冲刺：一个 Slack 频道 + 处于 beta 的 Claude Tag，驱动一个能力约等于 Opus 5.5 的内部研究模型，对 claude.ai 前端做端到端优化。分工是——Claude 找瓶颈、建基准、提交改进、盯部署；人类定目标、做取舍、给批准。结果：两周合并 3,000+ 变更，零客户事故、零回滚，核心路径提速 3-5 倍。

方法论的核心一句话："一旦 Claude 能度量某件事，它就能优化它。"团队用确定性计数器（Valgrind 指令数、V8 覆盖率、React commit 数、DOM 变更数）构建只降不升的 CI 棘轮，把"变快"从主观感受变成机器可执行的不变量，让 agent 在无人监督下也不会退化性能。

## 关键发现 / 关键技术

### 1. 四条关键路径的量化结果
- 四条路径覆盖用户活动的 95%：
  - p75 可输入时间：3.1s → 0.55s（约 5.6 倍）
  - Claude Code 新会话启动：0.8s → 0.3s
  - Cowork 云会话启动：2.6s → 0.73s
  - 合计每天节省数万用户小时。

### 2. 确定性计数器与 CI 棘轮
- 度量手段：Valgrind 指令数、V8 覆盖率、React commit 数、DOM 变更数——全部确定性、可复现、无噪声。
- 棘轮机制：指标只允许下降（或持平），上升即 CI 失败，性能改进被永久锁定。
- 效果：某路径指令数下降 48% 与 31%，墙上时间下降 78% 与 44%。

### 3. 趣味发现（长尾即金矿）
- 输入路径挂载 6,900 个 React hooks——一次击键的隐性成本。
- 一个 `:root:has()` CSS 选择器给每次 DOM 变更增加 24ms。
- em dash（—）触发 UTF-16 双字节代码路径，导致高亮卡死 1 秒；20 行修复。
- 残留的 `location.reload()` 每天制造 50 万次隐形页面重载。

### 4. 协作规模与人类角色
- 峰值日合并 200+ 变更，150+ 并行线程同时推进。
- 近 200 个 feature flag 中过半已在冲刺中清理。
- 人类角色转向三层引导——雄心（ambition）、品味（taste）、方向（direction）；"please be braver"（请更大胆些）成为给人留的提示词。

## 实践意义

这篇文章把 "AI 主导研发" 从口号变成带数字的工程报告：3,000+ 合并、零回滚说明质量门禁（基准 + 棘轮 + 部署监控）才是 agent 大规模写代码的前提，而不是人肉 review。确定性度量是全文最可迁移的经验——LLM 无法可靠优化"感觉更快"，但可以 relentless 地优化一个单调递减的计数器；任何团队都可以为自己的关键路径建立这种棘轮。同时它划出了人的新位置：不再逐行审代码，而是调雄心、定品味、给方向。

## 跨厂商对比

- 与 [Claude Tag 值班](claude-tag-ci-cd-on-call.md) 互补：值班场景是 Claude 盯生产故障并响应，本文是 Claude 主动发起改进并守住性能底线——同一 Claude Tag 基建在"救火"与"提速"两个方向的复用。
- 与 [The AI-native SDLC playbook](the-ai-native-sdlc-playbook.md) 对比：playbook 给出 AI 原生研发生命周期的框架，本文是该框架在性能工程上的一次实战落地，提供了可复制的度量与棘轮细节。
- 与 [Measuring the pace of AI development](../../anthropic/research/measuring-pace-of-ai-development.md) 互补：一个度量 AI 能力进步的宏观节奏，一个度量 AI 亲手优化的工程指标——"度量驱动"同时作用于研究与研发两端。

## 资源

- 官方文章：https://claude.dev/blog/how-we-made-claude-ai-faster/
- 开发者博客：https://claude.dev/blog/
- 相关（CI/CD 值班）：https://claude.com/blog/ai-ci-cd-on-call
