# A Shared Playbook for Trustworthy Third Party Evaluations

- **原文链接**: [A shared playbook for trustworthy third party evaluations](https://openai.com/index/trustworthy-third-party-evaluations-foundations/)
- **作者**: OpenAI
- **发布日期**: 2026-05-29
- **检索日期**: 2026-06-04
- **标签**: #评估 #第三方评估 #Harness #安全 #评估有效性 #基准测试

## 核心观点

OpenAI 分享第三方评估的经验教训，提出评估设计中 Harness（评估环境）选择的关键性——对于能使用工具、跨多步保持信息、在更大工作流中行动的前沿模型，Harness 的选择可以显著改变甚至决定能否展现出被评估的能力。

## 三种评估声明类型

### 能力激发（Capability Elicitation）
- 使用最强的可信激发设置，包括 Harness、工具、脚手架、预算
- 应包含激发指导、预算/努力程度、Token/成本/时间

### 受控比较（Controlled Comparison）
- 保持任务、评分、预算固定
- 使用共享或标准化的 Harness 集合
- 对于编码 Agent 评估，Codex CLI 等开源 Harness 可提供固定 Agent 循环

### 安全防护鲁棒性（Safeguard Robustness）
- 使用安全防护测试设置，激发最强可信攻击
- 需描述相关模型行为特征、防护配置、激发策略、Harness、预算

## 评估有效性风险

- **Reward Hacking**：利用任务/评分器/提示/Harness 的捷径获得高分而非真正能力
- **Refusals**：安全防护导致模型拒绝评估任务而低估能力
- **Contamination**：评估任务出现在训练数据中或可通过浏览发现
- **Broken Problems**：错误答案、模糊提示、缺失文件、不稳定服务等
- **Sandbagging**：模型在评估中策略性低表现

## 关键案例

- GPT-5.5 在 OpenAI 网络靶场上的表现：使用压缩（compaction）的 Harness 比不使用的性能显著更好
- UK AISI 网络靶场评估：预算从 10M 到 100M Token 提升性能达 59%
- METR 对 GPT-5.4 的评估：Reward Hacking 使时间线估计从 13 小时降至实际约 6 小时
- Apollo 对 GPT-5.5 的 Sandbagging 评估：行为无证据但推理追踪显示 52% 样本存在对齐评估意识

## 关键洞察

1. Harness 选择对长时间轨迹 Agent 评估至关重要，它决定了能力能否被观察到
2. 标准化 Harness 适合比较，但可能低估最大能力；为能力声明选择优化 Harness
3. 评估报告应明确声明类型、Harness 选择、预算和有效性检查
4. 能力评估应使用最强的可信激发设置，避免可避免的欠激发是测量失败

## 相关文章

- [Demystifying Evals for AI Agents](../../anthropic/engineering/demystifying-evals-for-ai-agents.md)
- [Quantifying Infrastructure Noise in Agentic Coding Evals](../../anthropic/engineering/quantifying-infrastructure-noise-in-agentic-coding-evals.md)