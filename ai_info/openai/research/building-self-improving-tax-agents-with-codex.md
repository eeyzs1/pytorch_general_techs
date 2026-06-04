# Building Self-Improving Tax Agents with Codex

- **原文链接**: [Building self-improving tax agents with Codex](https://openai.com/index/building-self-improving-tax-agents-with-codex/)
- **作者**: Aravind Srinivasan, Samay Shamdasani (Thrive Holdings), Arthur Fernandes Araujo, John de Wasseige (OpenAI)
- **发布日期**: 2026-05-27
- **检索日期**: 2026-06-04
- **标签**: #Codex #Agent #自改进 #税务AI #生产反馈 #评估 #Harness工程

## 核心观点

OpenAI 与 Thrive Holdings 合作为 Crete 会计师事务所网络构建了 Tax AI 系统，通过"专家反馈 + 生产追踪 + Codex 驱动的迭代循环"三支柱架构，实现了 Agent 在生产环境中的持续自改进。系统处理了 7000 份税务申报表，节省约 1/3 准备时间，准确率达 97%，吞吐量提升约 50%。

## 三部分自改进循环

### 1. 贴近实践者
- 实践者（会计师）的直觉和理解引导系统学习方向
- 他们能辨别哪些错误重要、哪些工作流值得优化

### 2. 产品追踪产出证据
- 捕获完整路径：源材料 → 提取字段及出处 → 下游提交 → 专家修正
- 将实践者修正转化为结构化数据：记录 Tax AI 提出的内容、实践者修改的内容、最终提交的内容

### 3. Codex 驱动的改进循环
- 生产问题 → 结构化发现 → 定向评估 → 限定工程任务
- Codex 检查产品追踪、评估、仓库和 Skills，进行根因分析、实施修复、验证并提交 PR

## 租赁房产案例

以 Schedule E 租赁房产收入提取为例，展示了完整的自改进循环：
- 实践者发现"fair rental days"字段持续被遗漏
- 生产追踪将修正分组为可操作的评估目标
- Codex 调查管道（提取模式、映射器行为、评分器问题）、实施修复、运行回归评估

## Codex 任务环境结构

- 可写工作树：包含 Agent 代码、评估数据集、Skills、文档
- 只读生产上下文：生产追踪、源工件、税务引擎文档
- 明确的任务边界文件：task.yaml、EXEC_PLAN.md、RESULTS.md

## 关键洞察

1. 真实世界的 Agent 系统需要"自改进循环"而非"一次性部署"
2. 生产追踪是自改进的关键基础设施——捕获完整路径而非仅输入输出
3. Codex 不是模糊告警的接收者，而是有证据、可编辑产品界面和显式验证门限的限定工程任务执行者
4. 实践者通过日常工作自然驱动改进循环，无需额外标注工作
5. 工程师保留架构、产品决策和发布职责

## 相关文章

- [Harness Engineering](harness-engineering.md)
- [An open-source spec for orchestration: Symphony](open-source-codex-orchestration-symphony.md)
- [Running Codex Safely at OpenAI](running-codex-safely.md)