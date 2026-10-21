# 用 Claude Sonnet 5.5 构建（Building with Claude Sonnet 5.5）

- **原文链接**: [Building with Claude Sonnet 5.5](https://claude.dev/blog/building-with-claude-sonnet-5-5/)
- **作者**: Addy Osmani
- **发布日期**: 2026-09-28
- **检索日期**: 2026-10-16
- **标签**: #Sonnet55 #开发者指南 #迁移 #between_tools #模型选择

> 补录说明：本文发布于 2026-09-28（锚点当日，上次同步 09-29 检查时漏收），本次补录入库。

## 核心观点

Sonnet 5.5 的开发者集成指南：何时选 Sonnet（规格清晰 + 有验收方式的日常任务、文档/幻灯/表格、重复跑的 agent 任务）vs 何时上 Opus 5.5（需谨慎判断的复杂工作、最难问题）。价格与 Sonnet 5 完全持平（$2/$10），省钱来自更少的 token 用量；1M 上下文原生、思考默认开启。Epic Games 早期测试：数万行游戏玩法架构代码、多小时任务、更少的手把手提示。

最有迁移价值的部分是五项破坏性变更的逐一拆解——thinking 关不掉只能换 between_tools（仅 low/medium/high 可用）、tool_choice 强制改 auto+strict、thinking 块绑定会话、computer use 走 toolset、advisor 搭配限制——以及"读取 content[0].text 会碎"的响应形状变化。

## 关键发现 / 关键技术

### 1. 选型表
- Sonnet 5.5：范围明确的日常编码、高量开发、带设计眼光的文档、重复 agent 任务（调查/评审/起草）
- Opus 5.5：谨慎判断的长视野 agentic 编码与知识工作、最难问题
- 官方口径："最难的长视野工作，Opus 是更好选择"；Haiku 5.5 数周内补位（后于 10-07 发布）

### 2. 迁移五坑 + 响应形状
- thinking: disabled 返回 400 → between_tools（只在工具间思考；xhigh/max 不可用、不能带其他字段、会话中不可变档）
- tool_choice any/tool 返回 400 → auto + strict: true（schema 需 additionalProperties: false）
- thinking 块模型绑定：Sonnet 5.5 读 Sonnet 5 的块（平滑迁移），但其他模型不读 5.5 的
- computer use 仅 computer_toolset_20260801；advisor 拒绝 Opus 4.8/4.7/Sonnet 5，接受者（Opus 5.5/5、Sonnet 5.5）建议加密回传
- 工具间短进度以 thinking 块返回（默认 display 为空）——按 type 遍历 content，勿再 content[0].text

### 3. 调参与护栏
- effort 重校准：Claude API 默认 high，Claude Code 默认 medium；latency 敏感场景 medium/low 起步
- low 档可能跳过真实验证 → 给"跑真检查才算完"的系统提示段落（文中有全文）
- 最小可缓存 prompt 降到 512 token；顶层 effort 变更会清缓存 → 用 beta 的 per-message effort
- 拒绝分类五类（cyber/bio/frontier_llm/reasoning_extraction/general_harms）；server-side fallback 仅重试 cyber 与 frontier_llm 到 Sonnet 5

## 实践意义

这是把 Sonnet 5.5 从"发布公告"变成"可集成组件"的关键文档：迁移清单 + effort 重校准 + between_tools 语义共同决定了存量代码库的升级成本。两条最实用的工程结论：按 type 读 content 应立即成为标准写法（思考默认开的 5.5 代全员适用）；low 档跳验证的系统提示补丁值得进所有生产 prompt 库。选型上"有验收方式就用 Sonnet"的口诀与 effort 指南（边界用例多用高档）组合成完整决策树。

## 跨厂商对比

- 与 [Introducing Claude Sonnet 5.5](../research/claude-sonnet-5-5.md) 互补：发布页给基准叙事（TB 4.0 70.6%），本文给 API 集成的全部细节——评测故事与工程落地的两半
- 与 [Spending Your Effort](spending-your-effort.md) 衔接：档位哲学篇讲怎么选档，本文确认 Sonnet 侧档位已重校准且给出各 surface 默认值
- 与 [Better Prompt Caching for GPT-6](../../openai/research/better-prompt-caching-for-gpt-6.md) 对比：OpenAI 以 90% 折扣/30 分钟窗口打缓存价格战，Anthropic 在 Sonnet 5.5 保持 $0.20 读价但用 512 token 门槛 + per-message effort 保缓存——降价与保值两种缓存策略

## 资源

- 论文：无
- 代码：无
- Demo：无
- 迁移指南：https://platform.claude.com/docs/en/models/sonnet-5-5/migration-guide
