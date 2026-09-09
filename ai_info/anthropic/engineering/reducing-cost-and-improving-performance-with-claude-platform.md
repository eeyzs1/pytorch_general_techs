# 用 Claude Platform 降低成本并提升性能（Reducing cost and improving performance with Claude Platform）

- **原文链接**: [Reducing cost and improving performance with Claude Platform](https://claude.com/blog/reducing-cost-and-improving-performance-with-claude-platform)
- **作者**: Anthropic（Claude Platform 团队）
- **发布日期**: 2026-09-08
- **检索日期**: 2026-09-09
- **标签**: #成本优化 #PromptCaching #Effort参数 #ClaudeAPI #性能调优

## 核心观点

Anthropic 指出性能与成本并非天然此消彼长：Claude Platform 应用通常可以通过三个修正——最大化 prompt cache 命中率、升级前沿模型时清除提示词反模式、按任务校准 effort——在不牺牲性能的前提下显著降低成本。相关指导已打包进开源的 claude-api skill，可由 Claude Code 自动执行。

三个自动化命令是本文的骨架：/claude-api prompt-audit 清除反模式（Opus 4.8→Opus 5 迁移实测平均降本 14.6%、准确率提升 5.3%）；/claude-api cost-optimize 做整体成本审计（四个公开基准降低约 52%–73% 成本）；/claude-api hillclimb 在成本-性能空间迭代搜索（客服基准上以约五分之一成本把留出集准确率从 78.6% 提到 90.5%）。

## 关键发现 / 关键技术

### 1. Prompt cache 实践要点
- 缓存 pinned 到具体模型、读取要求全前缀字节级一致、TTL 有限；破坏命中的常见原因：中途改 effort/thinking、系统提示里的动态时间戳、工具定义重排、fork 前缀不一致、同步工具调用或子 Agent 超过 TTL（缓存过期后重写按 1.25× 计价，1 小时档 2×）。
- 保命技巧：冷门工具标 defer_loading 移出缓存前缀；系统指令以 mid-conversation 消息注入而非改 system prompt；静态内容（工具定义+系统提示）在前、增长的对话在后；在 compaction 等缓存必然失效的时刻切换模型/effort；用 max_tokens:0 请求预热缓存；Console 的 cache diagnostics API 能定位两次请求前缀从哪一字节开始分叉。

### 2. 前沿模型迁移的提示词反模式
- 六类反模式：验证仪式（"verify twice"）、强调助推词（"CRITICAL: YOU MUST"）、强制草稿板/固定流程、针对旧模型失败模式调优的过时少样本、矛盾规则、过时配置（如手动 thinking 预算会被 API 拒绝）。
- 实测：在客服基准上从干净提示词逐个植入反模式构成六个遗留提示词，Opus 4.8→Opus 5 迁移后跑一次 prompt-audit，平均成本 -14.6%、准确率 +5.3%（矛盾规则曾让 Opus 5 拒发四笔应退退款、手动草稿板与原生 thinking 冲突导致三次工具调用写进推理却未执行）。

### 3. effort 校准与成本审计结果
- effort 两头都会失准：过高导致过度思考（成本延迟上升甚至质量下降），过低导致证据不足就作答。Fable 5 在 FrontierCode Diamond 最难 50 题上从低 effort 11.5%/$5.35 到 max 30.9%/$19.00；CursorBench 3.2 上 Fable 5.1 低 effort 以三分之一成本匹配 Fable 5 高 effort（缓存读价 $0.25/M vs $1.00/M tokens）。
- cost-optimize 四基准：LegalBench 约 -58%（thinking token 从 102,779 降到 8,284）、tau2-bench retail 约 -73%、OfficeQA Pro 约 -52%（$136.20→$64.87）、SWE-bench Verified 约 -55%（中位步数 29→17，prompt token 75.2M→33.7M）。hillclimb 客服基准：Sonnet 5 低 effort + 路由规则修复，1 美分/票据回到 98.9% 训练准确率，14 张留出票据上 90.5% vs 原配置 78.6%，成本约五分之一。

## 实践意义

这套方法论把"降本"从拍脑袋换小模型变成了可度量的工程流程：先用量化数据定位 token 去向，再按 prompt cache → 反模式清理 → 输出限长 → 批处理 → effort/模型选择的顺序逐级优化，每一步都用评估集验证性能不掉。"强模型低 effort 可能比弱模型高 effort 更便宜"以及"在缓存必然失效的时刻才切换模型/effort"这两个反直觉结论，值得直接进团队的 API 使用清单。三个 /claude-api 命令也示范了"用 Claude 优化 Claude 应用"的自举模式。

## 跨厂商对比

- 与 [最大化 Claude Code 会话价值](maximizing-value-of-claude-code-sessions.md) 对比：那篇优化的是 Claude Code 会话内的 token 花费（会话管理、/compact 时机等）；本文面向直接调用 Claude API 的应用层，给出缓存、指令、effort 三大杠杆加自动化审计命令——同属成本工程但作用层不同。
- 与 [DeepSeek-V4 API 定价与峰谷计费](../../deepseek/news/deepseek-v4-api-pricing.md) 互补：DeepSeek 通过峰谷计费与定价结构调整从供给侧降本；Anthropic 这篇展示在单价不变的情况下靠使用侧优化（缓存命中率、effort 校准）拿到 50% 以上的降幅——两条路径可以叠加参考。

## 资源

- 论文：N/A
- 代码：https://github.com/anthropics/skills/tree/main/skills/claude-api（claude-api skill）
- 官方文章：https://claude.com/blog/reducing-cost-and-improving-performance-with-claude-platform
