# Demystifying Evals for AI Agents

- **原文链接**: [Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)
- **发布日期**: 2026-01-09
- **标签**: #评估 #评估框架 #Grader #能力评估 #回归评估

## 核心观点

这是 Anthropic 最全面的评估指南。文章提供了构建 AI Agent 评估的完整框架，涵盖术语、评分器类型、能力评估 vs 回归评估、特定 Agent 类型的评估设计，以及 8 步路线图。核心信息：**评估是公司的知识产权和关键竞争优势。**

## 核心术语

| 术语 | 定义 |
|------|------|
| 任务/测试用例 | 具有定义输入和成功标准的单个测试 |
| 试验 (Trial) | 每次尝试（因非确定性需要多次） |
| 评分器 (Grader) | 评分逻辑（任务可有多个评分器） |
| 转录/追踪 | 试验的完整记录 |
| 评估套件 | 相关任务的集合 |

## 三种评分器类型

| 类型 | 方法 | 最适合 |
|------|------|--------|
| **基于代码** | 字符串匹配、二进制测试、静态分析、结果验证、工具调用验证 | 快速、廉价、客观、可复现 |
| **基于模型** | 评分标准、自然语言断言、成对比较、多评判共识 | 灵活、捕捉细微差别、可扩展 |
| **人类** | 主题专家审查、抽查采样、A/B 测试 | 黄金标准质量、捕捉边缘情况 |

## 能力评估 vs 回归评估

- **能力评估**: "这个 Agent 能做好什么？"（从低通过率开始，给团队一个攀登的山峰）
- **回归评估**: "它是否仍能处理以前能处理的？"（应维持约 100% 通过率）
- 高分的能力评估"毕业"到回归套件

## 非确定性指标

- **pass@k**: k 次尝试中至少 1 次成功的概率（随 k 增加）
- **pass^k**: k 次试验全部成功的概率（递减——如 75% 单次 × 3 次试验 = 42%）

## 8 步路线图

1. **尽早开始** — 来自真实失败的 20-50 个任务就足够了
2. **从手动检查开始** — 将用户报告的失败转换为测试用例
3. **编写无歧义的任务**，附带参考解决方案
4. **构建平衡的问题集** — 测试行为应该和不应该发生的情况
5. **构建健壮的评估工具** — 每次试验从干净环境开始。[Quantifying Infrastructure Noise in Agentic Coding Evals](quantifying-infrastructure-noise-in-agentic-coding-evals.md) 量化了不干净环境对评估结果的影响——仅基础设施配置差异就能造成 6 个百分点波动
6. **深思熟虑地设计评分器** — 评估 Agent 产出了什么，而非路径；内置部分得分
7. **监控能力评估饱和** — 100% 通过率意味着评估只追踪回归
8. **保持套件健康** — 专门的评估团队拥有基础设施；领域专家贡献任务

## 实践启示

- [Raising the Bar on SWE-bench Verified](raising-the-bar-on-swe-bench-verified.md) 是 SWE-bench 评估的实战案例——展示了如何从评估失败中优化 Agent
- [Writing Effective Tools for AI Agents](writing-effective-tools-for-ai-agents.md) 的评估驱动方法论（原型→评估→分析→优化→重复）是本文第 5-6 步的具体实践
- [How We Built Our Multi-Agent Research System](how-we-built-our-multi-agent-research-system.md) 使用 LLM-as-judge 评估研究质量，是"基于模型"评分器的生产案例
- [A Postmortem of Three Recent Issues](a-postmortem-of-three-recent-issues.md) 揭示了基础设施 Bug 如何伪装成模型退化——强调了第 5 步"干净环境"的重要性
