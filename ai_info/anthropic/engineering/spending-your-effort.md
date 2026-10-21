# 使用 Claude Code：把 effort 花在刀刃上（Using Claude Code: Spending your effort）

- **原文链接**: [Using Claude Code: Spending your effort](https://claude.dev/blog/spending-your-effort/)
- **作者**: Thariq Shihipar
- **发布日期**: 2026-09-25
- **检索日期**: 2026-10-16
- **标签**: #effort档位 #TerminalBench #评测分析 #验证深度 #ClaudeCode

> 补录说明：本文发布于 2026-09-25（锚点 2026-09-28 之前），上次同步遗漏，本次补录入库。

## 核心观点

回答"effort 到底是什么、什么时候用哪档"：effort 是"希望模型花多少算力"的近似表达，改变的主要是验证与边界测试的深度和自主判断的量。作者用三档构建实验 + Terminal-Bench 3.0 全量失败分析得出核心结论——高 effort 最适合"隐藏边界用例多"的任务（硬件、代码评审、安全）；常规软件工程的最优循环是：先让模型访谈我 → low effort 实现 → 人工复审 → high effort 验证。

Terminal-Bench 3.0 的失败归因给出机制解释：升 effort 减少的是"漏边界用例"型失败（紫），救不了"方法错了"型失败（蓝）——所以先确认方向对再加大投入。

## 关键发现 / 关键技术

### 1. 三类任务的 effort 响应
- 未明确规格的构建（健身 App）：low = 日志+简单图（1.5 分钟），max = 带热力图的完整应用（67 分钟）——要迭代基底用 low，要一次最佳用 max
- 轻规格设计（重设计 /config 菜单）：low 出"传达想法但不像 Claude Code"的草图（1 分钟），max 出高保真+多流程走查（28 分钟）——探索愿景反而 low 更好
- 高规格构建（访谈后给 spec）：各档产出趋同（16→79 分钟），规格质量抹平 effort 差异

### 2. Terminal-Bench 3.0 的边界用例证据
- Fable 5.1 在 html-js-filter（HTML 净化器）从 low 的 1/5 升到 xhigh 的 5/5
- low 尝试约 2 分钟一遍写完、只对一个手写页测试；high 约 33 分钟：对抗性自审初稿 → 读解析器源码查 bug → 大量干净用例回归 → 标准 XSS 测试套件 → 自写随机文档 fuzzer
- 全基准失败谱系：升档系统性地把"漏边界"（Fable 5.1 low 40 次 → max 14 次）转为"读错需求/选错解读"类——思考更深不等于理解更对

### 3. 推荐循环
- 规格访谈 → low 实现 → 人工 gist 复审（必要时 low 迭代）→ high 验证测试
- 域判断：硬件/代码评审/安全等"验证密集"域直接高起步；机械改动（改名/套模式）low 即可

## 实践意义

effort 的心智模型从"聪明程度旋钮"校正为"验证深度旋钮"：它买的是对抗性自查、读源码、写 fuzzer 这类自我质疑行为，而不是更聪明的方向选择。与成本指南联动后形成完整决策树：先问"边界用例多不多"（多 → 高 effort 值得），再问"方向确定吗"（不确定 → 人工介入比加 token 划算）。"访谈我 → low 干活 → high 验证"的循环可直接作为团队默认工作流模板。

## 跨厂商对比

- 与 [What a Task Costs on Opus 5.5](what-a-task-costs-on-opus-5-5.md) 同日姊妹篇：成本篇讲 effort 对账单的影响，本文讲 effort 对产出质量的影响——价格与价值两侧合看才是完整决策
- 与 [Introducing Claude Opus 5](../research/claude-opus-5.md) 对比：Opus 5 发布确立 effort 档位设计，本文提供第一份基于失败归因的档位使用实证——设计意图与使用证据的呼应
- 与 [Quantifying Infrastructure Noise in Agentic Coding Evals](quantifying-infrastructure-noise-in-agentic-coding-evals.md) 互补：基建噪声篇讲评测环境的坑，本文讲评测结果怎么指导生产档位选择——评测可信 → 档位可信的依赖链

## 资源

- 论文：无
- 代码：https://github.com/harbor-framework/terminal-bench/releases/tag/v3.0.0（基准任务集）
- Demo：无
