# 从噪声中分离信号：编码评估的详细审计

- **原文链接**: [Separating signal from noise in coding evaluations](https://openai.com/index/separating-signal-from-noise-coding-evaluations/)
- **作者**: OpenAI
- **发布日期**: 2026-07-08
- **检索日期**: 2026-07-20
- **标签**: #评估 #SWE-Bench #基准测试 #任务质量 #可靠性 #编码评估

## 核心观点

OpenAI 对 SWE-Bench Pro 进行详细审计，发现**约 30% 的任务存在问题**——任务描述不清、测试用例错误、或环境配置缺陷。这是继 SWE-Bench Verified 被发现根本性问题后，对编码评估领域的又一次系统性质量审计。研究采用"人类监督的 Agent 审查"方法，结合人工标注活动，系统识别和分类任务缺陷。核心主张：当前编码基准的噪声水平已高到可能误导模型能力判断和部署决策。

## 关键发现 / 关键技术

### 1. SWE-Bench Pro 审计方法
- **人类监督的 Agent 审查**：用 Agent 初步筛查，人类专家复核
- **人工标注活动**：系统分类任务缺陷类型
- 与之前 SWE-Bench Verified 审计方法一致，确保可比性

### 2. 任务缺陷类型（~30% 任务有问题）
- 任务描述不清晰或存在歧义
- 测试用例错误或覆盖不全
- 环境配置缺陷导致无法正确评估
- 与真实软件工程实践脱节

### 3. 与 SWE-Bench Verified 的对比
- SWE-Bench Verified：根本性设计缺陷 + 污染问题
- SWE-Bench Pro：~30% 任务质量问题
- 两者都表明编码评估领域需要更严格的质量控制

### 4. 对模型评估的影响
- 有缺陷的任务可能导致对模型能力的错误判断
- 影响 Preparedness Framework 下的安全决策
- 需要更可靠的评估信号支持模型发布

## 实践意义

这项审计对 AI 评估领域有深远影响：
- **评估质量标准化**：推动建立编码任务的质量标准和审查流程
- **模型发布决策**：提醒行业不能盲目信任基准分数，需审计评估质量
- **Agent 评估方法**：人类监督的 Agent 审查方法可应用于其他评估领域
- **开源社区协作**：与 Scale AI 等基准维护方合作改进任务质量

## 跨厂商对比

- 与 [Quantifying Infrastructure Noise in Agentic Coding Evals](../../anthropic/engineering/quantifying-infrastructure-noise-in-agentic-coding-evals.md) 对比：Anthropic 关注基础设施噪声，OpenAI 关注任务质量；两者共同揭示编码评估的系统性可靠性问题
- 与 [Raising the Bar on SWE-bench Verified](../../anthropic/engineering/raising-the-bar-on-swe-bench-verified.md) 对比：Anthropic 展示如何在 SWE-bench 上取得好成绩，OpenAI 揭示基准本身的问题
- 与 [Demystifying Evals for AI Agents](../../anthropic/engineering/demystifying-evals-for-ai-agents.md) 互补：Anthropic 提供评估框架，OpenAI 提供具体审计案例

## 资源

- SWE-Bench Pro：[Scale AI SWE-Bench Pro](https://scale.com/blog/swe-bench-pro)
- 之前审计：[Why we no longer evaluate SWE-bench Verified](https://openai.com/index/why-we-no-longer-evaluate-swe-bench-verified/)
- Preparedness Framework：[OpenAI Preparedness Framework](https://cdn.openai.com/pdf/18a02b5d-6b67-4cec-ab64-68cdfbddebcd/preparedness-framework-v2.pdf)
