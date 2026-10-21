# ThinkingBox：Agent 说做完了，数据库不同意（The Agent Said It Was Done. The Database Disagreed.）

- **原文链接**: [The Agent Said It Was Done. The Database Disagreed.](https://huggingface.co/blog/microsoft/thinkingbox)
- **作者**: Tuhin Kundu（Microsoft，与 Hugging Face 联合博客；Sergio Paniego（HF）等协作）
- **发布日期**: 2026-10-03
- **检索日期**: 2026-10-16
- **标签**: #Agent评测 #状态验证 #一致性 #基准测试 #MCP

## 核心观点

微软 ThinkingBox 基准只看 Agent 留下的记录，不看它说的话：507 个有状态企业工作流（零售、车险、旅行、虚拟银行、咨询），每个在干净后端上独立跑 20 次，对终态后端字段与副作用做可执行检查。开篇案例一针见血——客服 Agent 九次工具调用全部规范、正确读懂政策，却把本应置为 hold 的工单标成 solved 关闭："轨迹是主张，数据库状态是证据，重复是信任测试。"

规模数据证实直觉：12 个模型 121,680 次有效试验中 79,853 次未通过可执行检查，其中 67.24% 表面上"干净终止、调用过状态变更工具、无报错"——但 77.61% 存在错误字段值、43.30% 产生多余副作用、25.36% 缺失必需效果。工具调用规范性与最终状态正确性是两件事。

## 关键发现 / 关键技术

### 1. pass@1 格局与领域悬崖

- 总榜：Claude Opus 5.5 以 67.16% 居首（Opus 5 为 66.50%），GPT-5.4 65.36%；开源最强 Kimi-K3 57.37%，与 GPT-6 Astra（58.31%）相差不足 1 分；GLM-5.1 33.19。
- 领域差异巨大：Claude Opus 4.6 零售 68.62% 但车险仅 8.30%——跨领域能力不可外推，选型必须测自己的域。

### 2. 20 次重复后的幸存率

- 三指标：pass@1（通常水平）、pass@20（至少一次能做对，广度）、observed 20/20（20 次全对，可靠性）。
- 单次分数的幸存率：仅三家保住七成以上——GPT-6 Astra 保留 78%，Claude Opus 5.5 与 Opus 5 各 71%；GLM-5.1、Kimi-K2.6、DeepSeek-V4-Pro 仅保留约 8%。
- "能做对一次"与"每次都做对"的差距即部署风险的量化。

### 3. 开放可复现

- 通过 OpenEnv（thinkingbox_env）隔离 MCP 工具会话运行；数据与失败案例在 microsoft/thinkingbox-data 开源，开篇案例的失败检查就是单字段比对（工单 status=solved vs 要求 hold）。

## 实践意义

对 Agent 验收方：把评测从"看轨迹/看回复"迁移到"查库表/查副作用/重复 20 次"，ThinkingBox 提供了现成的方法论与开源实现。对模型方：开源模型在单次广度上已逼近闭源第二梯队，但重复可靠性普遍塌方——这是下一个训练主战场。

## 跨厂商对比

- 与 [Agent 一致性鸿沟](agent-consistency-gap.md) 对比：IBM 用五连任务量化 Agent 一致性（单次 77% vs 五连 53%），ThinkingBox 把一致性测试搬到有状态企业后端并加严到 20 连——两者共同宣告"pass@1 已不足以作为 Agent 质量指标"。
- 与 [分数不是模型](the-score-is-not-the-model.md) 互补：一个修基准测量的误差，一个修基准测量的对象（轨迹→终态），评估方法学正在系统性补课。
- 与 [可信第三方评估的基础](../../openai/research/trustworthy-third-party-evaluations-foundations.md) 对比：OpenAI 讨论第三方评估的制度基础，ThinkingBox 给出评估内容本身的技术标准——状态验证 + 重复测试可直接并入任何企业的验收流程。

## 资源

- 论文：[ThinkingBox（arXiv 2608.19741）](https://arxiv.org/abs/2608.19741)
- 代码：[microsoft/thinkingbox-data](https://github.com/microsoft/thinkingbox-data)、[OpenEnv thinkingbox_env](https://github.com/huggingface/OpenEnv/tree/main/envs/thinkingbox_env)
- Demo：无
