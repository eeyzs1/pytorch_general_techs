# 形式化费马大定理（Formalizing Fermat's Last Theorem）

- **原文链接**: [Formalizing Fermat's Last Theorem](https://www.anthropic.com/research/formalizing-fermats-last-theorem)
- **作者**: Anthropic（科学团队，Tianyi Peng 主导）
- **发布日期**: 2026-09-04
- **检索日期**: 2026-09-09
- **标签**: #形式化验证 #Lean #费马大定理 #Autoformalization #多Agent协作

## 核心观点

Anthropic 发布了费马大定理（FLT）首个完整的端到端机器可检验证明：Claude 在 11 天内基本自主地用 Lean 完成形式化，产出约 1300 万行 Lean 代码、证明 30,300 个定理（最终证明使用 29,500 个中间定理），规模超过 Mathlib 的 5 倍，路线遵循 Wiles 证明的 Darmon–Diamond–Taylor 简化版本。

这项工作的新颖之处不在"发现新数学"而在"验证"：Lean 仅依赖三条标准公理即完成检查，Kevin Buzzard 审阅后认可该成果足够坚实、可被后续工作构建。多 Agent 协作平台 Prove2Me 以定理依赖 DAG、语句与证明分文件、自然语言索引三大设计，解决了长周期形式化中的记忆退化与并行协作问题。

作者认为自动形式化将减轻数学界的审稿与纠错负担，并成为人类信任 AI 生成数学的关键基础设施。

## 关键发现 / 关键技术

### 1. 11 天端到端形式化的规模数据
- 1300 万行 Lean、30,300 个已证明定理（最终使用 29,500 个），超过 Mathlib 的 5 倍；整个项目消耗约 60 亿输出 token，所用模型为与 Claude Fable 5.1 大致相当的通用内部研究模型，harness 基于 Claude Code 的多 Agent 架构。
- 人类输入仅限偶发的高层指令（如"尽快推进 Mazur 定理"）；早期失败的 Agent 尝试贡献了最终证明约 7% 的非样板代码行。

### 2. Prove2Me 平台的三项关键设计
- 定理语句有向无环图（DAG）：Agent 依据依赖图决定下一个待证目标，缓解记忆退化并支持多 Agent 并行。
- 定理语句与证明分文件维护、链接独立管理：加速 Lean 编译、最小化资源消耗。
- 每条定理语句配自然语言描述索引：支持搜索与复用，简化证明路径。

### 3. 验证结论与生态影响
- Lean 检查通过，仅使用三条标准公理；comparator 确认定理陈述与 Mathlib 中 FLT 的表述一致；完整证明与走查文档已在 GitHub 开源，Kevin Buzzard 审阅并公开认可。
- 三个个人 Claude Max 订阅通过 Prove2Me 协作，3 天完成 Vinogradov 三素数定理的形式化，说明消费级订阅配合正确的脚手架即可参与大定理协作形式化。

## 实践意义

对 AI for Math 而言，这标志着"大规模数学文献自动形式化"从多年期社区工程（Imperial College FLT 项目仅蓝图就有 86 页）压缩到周级 Agent 工程；自动形式化既能排查既有数学语料中的错误，也为审阅海量的 AI 生成证明提供了可行机制。对工程团队而言，Prove2Me 的 DAG 任务分解、语句/证明分离、自然语言索引是长周期多 Agent 协作的通用模式，可直接迁移到代码库级的大规模并行任务。

## 跨厂商对比

- 与 [数学与理论计算机科学的十项进展](../../openai/research/ten-advances-in-mathematics.md) 对比：OpenAI 汇报前沿模型在数学与理论计算机科学上的十项研究进展（含 Lean 形式化元素），侧重"模型能产出什么新结果"；本文交付单一经典定理的完整机器可检验证明，侧重"机器能否验证既有数学"。
- 与 [An OpenAI Model Has Disproved a Central Conjecture in Discrete Geometry](../../openai/research/model-disproves-discrete-geometry-conjecture.md) 互补：一个用模型证伪猜想（发现新数学），一个用模型形式化已有 350 年历史的定理（检验旧数学），构成 AI 数学的两条并行路径。

## 资源

- 论文：https://doi.org/10.48550/arXiv.2608.28433（Prove2Me 平台论文）
- 代码：https://github.com/anthropics/fermats-last-theorem
- 官方文章：https://www.anthropic.com/research/formalizing-fermats-last-theorem
