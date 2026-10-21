# AutoSynthData：为企业 Agent 生成训练数据（AutoSynthData: Generating Training Data for Enterprise Agents）

- **原文链接**: [AutoSynthData: Generating Training Data for Enterprise Agents](https://huggingface.co/blog/ServiceNow-AI/autosynthdata)
- **作者**: Esakkivel Esakkiraja、Shruthan Radhakrishna、Denis Akhiyarov、Sagar Davasam（ServiceNow CoreAI）
- **发布日期**: 2026-10-02
- **检索日期**: 2026-10-16
- **标签**: #合成数据 #Agent训练 #课程学习 #企业Agent #后训练

## 核心观点

企业需要的 Agent 必须在自己的环境里好用：特定工作流、特定工具组合、特定数据状态下的失败，通用能力分数看不出来。难点在于把"失败模式"变成"训练数据"——单个失败案例无法直接训练，需要大量可行、真实、可验证且恰好命中当前弱点的变体任务。ServiceNow 的 AutoSynthData 把这个缺口工程化：用目标模型在企业环境中的失败 + 更强教师在同环境的成功，蒸馏出"能力规格卡"，再据此生成、验证新任务用于后训练。

任务被抽象为三元组（系统规约、用户提示、验证器）：任务需满足可行性/真实性/难度（当前模型做不对），验证器需满足一致性/可靠性/完备性（不奖励错误行为、不惩罚有效解）。关键防泄漏设计：生成器拿到的规格卡经过消毒，不含原始评测题的提示、实体、轨迹或验证器细节。

## 关键发现 / 关键技术

### 1. 从失败到课程

- 诊断评测同时跑目标模型与教师模型，识别：被测能力、涉及工具与工作流结构、目标模型在哪失败而教师怎么成功、正确终态必须满足的性质、可保持能力的可变维度。
- 随目标模型进化，课程自动转向仍未解决的缺口——形成"评测→生成→训练→再评测"闭环。

### 2. Target + Multiply 两阶段扩展

- Target 阶段：并行 worker 从规格卡生成核心样本，每个候选经"验证→环境执行→求解器评估→修复"才被接受。
- Multiply 阶段：以已接受样本为锚派生新变体（新请求、新环境状态、新实体配置、新参考轨迹、新验证器）；倍增样本不能再派生倍增样本，从机制上限制跨代漂移。

### 3. 落地环境

- 以 EnterpriseOps Gym（arXiv 2603.13594）为演示环境，训练数据集已在 Hub 开源；配套 ITSM 与混合场景实验展示训练前沿的移动。

## 实践意义

这是"评测驱动训练"在企业侧的完整工程参考：多数团队的 Agent 微调卡在"没有贴着自己环境的数据"，AutoSynthData 给出的答案是把环境本身（工具、状态、验证器）当作任务生成器。验证器三性质与防泄漏规格卡的设计，对任何做 agent 合成数据的团队都可直接借鉴。

## 跨厂商对比

- 与 [Holo4](holo4.md) 对比：Holo4 的 Agentic Task Factory 从软件文档合成约 1 万个任务环境训练通用 computer-use 能力，AutoSynthData 从目标模型自身失败合成课程修补企业环境特定缺口——前者扩广度、后者补深度。
- 与 [100 步 GRPO 结构化输出](grpo-with-trl-ifstruct.md) 对比：都在证明"训练信号来自环境验证器而非人工标注"，但 GRPO 篇是 500 样本的小规模教学案例，本篇是企业级流水线化生产。
- 与 [用 Codex 构建自我改进的税务 Agent](../../openai/research/building-self-improving-tax-agents-with-codex.md) 对比：OpenAI 案例靠真实使用轨迹驱动迭代，ServiceNow 靠合成变体驱动——真实轨迹与合成课程的取舍是 Agent 团队的共同决策点。

## 资源

- 论文：[EnterpriseOps Gym（arXiv 2603.13594）](https://arxiv.org/abs/2603.13594)
- 代码：无
- Demo：[EnterpriseOps-Gym 数据集（Hugging Face）](https://huggingface.co/datasets/ServiceNow-AI/EnterpriseOps-Gym)
