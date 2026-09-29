# UK AISI 与 EvalEval 让基准可复现（UK AISI and EvalEval Make Benchmarks Reproducible）

- **原文链接**: [EvalEval × UK AISI: Reproducible Benchmark Results on an Open Infrastructure](https://huggingface.co/blog/evaleval-aisi)
- **作者**: EvalEval 联盟、英国 AI 安全研究所（UK AISI）
- **发布日期**: 2026-09-22
- **检索日期**: 2026-09-29
- **标签**: #评测 #可复现性 #基准测试 #AI治理 #开放科学

## 核心观点

EvalEval 联盟与英国 AI 安全研究所（AISI）合作，用开放基础设施发布评估结果：Every Eval Ever 提供共享的结果上报模式，Evaluation Cards 是开放发布平台。AISI 首批公开五个基准（HealthBench、FrontierMath、HLE、SWE-Bench Pro、TB 2.0）在六个前沿模型（Claude Opus 4/4.5/4.6、GPT-5/5.2/5.4）上的独立验证结果与完整运行配置。

配套论文（arXiv:2606.17930）量化了推理算力与协议选择如何改变榜单：HLE 成绩随 oracle 反馈与 token 预算持续上升——同一模型在不同协议下排名可大幅变动。这是评估报告标准化的首批政府级落地：监管侧机构开始公开"怎么测的"，而不只是"测了多少分"。

## 关键发现 / 关键技术

### 1. 开放评估基础设施

- Every Eval Ever 定义共享上报模式：分数必须连同配置（模型版本、推理预算、提示协议）一起登记，缺配置的分数不被接纳。
- Evaluation Cards 作为开放平台承载发布，结果可被第三方程序化拉取与复核。
- 目标是把"跑分"从新闻稿变成可审计记录：任何人都能核对分数是在什么条件下产生的。

### 2. 五基准 × 六模型的公开验证

- 五个基准覆盖健康问答（HealthBench）、数学（FrontierMath）、综合性高难（HLE）、软件工程（SWE-Bench Pro）与终端任务（TB 2.0）。
- 六个前沿模型横跨 Anthropic 与 OpenAI 两代旗舰（Opus 4/4.5/4.6、GPT-5/5.2/5.4），完整配置随结果一起公开。
- 验证由 AISI 独立执行，属于第三方复核而非厂商自报。
- 六模型横跨两代旗舰，使同一基准内的代际进步与厂商间差距可以直接对比。

### 3. Cyber CTFs 与 The Last Ones

- 在五基准之外，AISI 另加 Cyber CTFs（网络安全攻防）与 The Last Ones 两项安全相关评估。
- 安全能力评估的结果与配置同样开放发布，延续"可复现优先"的上报模式。
- 这把标准化上报从能力榜扩展到安全审计场景，是政府机构公开安全评估配置的先例。

### 4. 论文：协议与算力改变榜单

- 论文量化显示：HLE 成绩随 oracle 反馈与 token 预算持续上升，推理算力是榜单上的隐含变量。
- 不报告推理预算的榜单实质上不可比较——不同团队的"同一基准"可能测的是不同协议。
- 这为"榜单噪声"提供系统性证据，也解释了为何完整配置必须随分数一起发布。

## 实践意义

对企业选型与安全审计，这套基础设施把"信不信榜单"变成"核对配置后自行复跑"。评估团队可直接复用上报模式，把分数、预算、协议一次性登记；模型厂商发布会引用第三方可复现结果也会更可信。政府机构以身作则公开验证配置，是评估标准化从社区倡议走向监管实践的第一步。

## 跨厂商对比

- 与 [Piloting Double-Blind AI Evaluations](../../google/deepmind/piloting-double-blind-ai-evaluations.md) 互补：双盲评估解决人评偏好偏差，EvalEval/AISI 解决机评可复现性，共同指向"评估方法学与分数本身同等重要"。
- 与 [分数不是模型](the-score-is-not-the-model.md) 互补：AISI 从协议与预算侧、Nacar 从服务与外围系统侧论证同一件事——分数测的是系统而非模型本体。
- 与 [BenchMIRT](benchmirt.md) 对比：同为基准质量与可比性研究，前者聚焦检索类基准的多维审查，本文聚焦上报协议的标准化落地。

## 资源

- 论文：[arXiv:2606.17930](https://arxiv.org/abs/2606.17930)
- 代码：[UK AI Security Institute（公开结果与配置入口）](https://www.aisi.gov.uk)
- Demo：[EvalEval × AISI 发布文](https://huggingface.co/blog/evaleval-aisi)
