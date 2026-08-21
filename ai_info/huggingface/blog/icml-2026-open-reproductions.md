# 复现 2,200 篇 ICML 论文：智能体驱动的开放复现挑战（Reproducing 2,200 ICML papers: the ICML 2026 open reproductions）

- **原文链接**: [ICML 2026 open reproductions](https://huggingface.co/blog/icml-2026-open-reproductions)
- **作者**: Hugging Face
- **发布日期**: 2026-08-13
- **检索日期**: 2026-08-21
- **标签**: #HuggingFace #ICML #复现 #智能体 #开放科学 #科研基础设施 #Agent

## 核心观点

Hugging Face 发起 ICML 2026 开放复现挑战，用 AI 智能体复现 ICML 论文的实验。挑战覆盖 2,200+ 篇论文，通过交互式 logbook 公开项目日志、代码与追踪，让社区可以查看每个复现的进展。这是"AI Agent 驱动的科研复现"的大规模实验——把复现从"人工重跑"转向"智能体自动执行 + 社区监督"。

挑战主页展示了首个完整复现案例："Towards Optimal Robustness in Learning-Augmented Paging"——智能体从论文理解到代码运行的全过程记录在可交互 logbook 中，任何人可查看。这代表了开放科学的新形态：可审计、可交互、可复现的科研流程。

## 关键发现 / 关键技术

### 1. 大规模复现挑战
- 覆盖 2,200+ 篇 ICML 论文
- 智能体驱动复现执行
- 交互式 logbook 公开全过程

### 2. 智能体复现工作流
- 论文理解 → 代码实现 → 实验运行
- 每一步记录在可审计的 logbook
- 失败与重试过程透明可见

### 3. 开放科学基础设施
- 项目日志、代码、trace 全部公开
- 社区可监督与参与
- 复现成为可交互的科研对象

### 4. 案例：Learning-Augmented Paging
- 首个完整复现案例
- 展示智能体复现的完整路径
- 验证"智能体复现"方法的可行性

## 实践意义

这是"AI 智能体 + 开放科学"的结合实验：复现作为科研诚信的核心环节，传统上耗时且不可见。HF 用智能体规模化复现 2,200 篇论文，并把过程做成可交互 logbook，让"复现"从一次性的验证变成持续的、可审计的科研资产。对科研社区而言，这预示复现工作的自动化与透明化趋势。

## 跨厂商对比

- 与 [OpenAI 科学计算 Agent 实地报告](../../openai/research/scientific-computing-agentic-ai.md) 对比：OpenAI 观察 Agent 做科学计算的角色转变，HF 用 Agent 规模化复现论文，都是"Agent 进入科研流程"的证据
- 与 [Ai2 OlmoEarth 大规模推理](olmoearth-infrastructure.md) 对比：OlmoEarth 是推理基础设施，ICML 复现是科研验证基础设施
- 与 [HF 安全事件披露](../../huggingface/blog/security-incident-july-2026.md) 对比：同为 HF 对社区的透明公开，一个管安全，一个管科研诚信

## 资源

- 论文：N/A
- 官方挑战：https://huggingface.co/blog/icml-2026-open-reproductions
- 挑战空间：https://huggingface.co/spaces/ICML-2026-agent-repro/challenge
