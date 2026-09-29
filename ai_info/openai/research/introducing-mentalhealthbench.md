# MentalHealthBench:AI 心理健康对话评估基准

- **原文链接**: [Introducing MentalHealthBench](https://openai.com/index/introducing-mentalhealthbench)
- **作者**: OpenAI(官方博客)
- **发布日期**: 2026-09-23
- **检索日期**: 2026-09-29
- **标签**: #评估基准 #心理健康 #安全性评估 #专家参与 #LLM评估

## 核心观点

OpenAI 发布 MentalHealthBench:一个由临床与心理专家参与构建的基准,用于评估 AI 在真实心理健康对话场景中回复的『有用性与安全性』。基准包含约 1215 段(官方口径为千余段)专家编写的真实感对话场景,覆盖抑郁、焦虑、自杀风险、成瘾等敏感议题。

它填补的空白很明显:通用聊天基准无法度量『说不该说的话』的代价,而心理健康恰是 LLM 被大量实际使用但安全证据最薄弱的场景之一。评估维度包括共情准确性、风险识别、建议边界(不替代专业治疗)与转介行为;OpenAI 强调 expert-informed 构建流程,意在让分数对临床可用性有解释力。

## 关键发现 / 关键技术

### 1. 基准构成
- 约 1215 段(官方口径千余段)由临床与心理专家编写的真实感对话场景。
- 议题覆盖:抑郁、焦虑、自杀风险、成瘾等敏感场景。
- 构建:expert-informed 流程,保证场景的临床真实性与评分维度的可解释性。

### 2. 评估维度:有用性与安全性并重
- 共情准确性:回应是否准确承接求助者情绪。
- 风险识别:自杀风险等危机信号能否被识别。
- 建议边界:不替代专业治疗的边界意识。
- 转介行为:该转介时是否转介(如自杀风险必转介的安全红线)。

### 3. 方法论边界
- 静态对话剧本难以覆盖真实求助者的长程意图漂移。
- 基准分数高 ≠ 可部署为治疗工具:它度量的是单轮/多轮对话质量,而非长期陪伴关系的安全性。

### 4. 与既有评测生态的关系
- 通用聊天基准度量『能做什么』,本基准度量『不该做什么』——安全维度的权重设计是关键差异。
- expert-informed 流程与各厂专家级高难评估思路同源:让分数对领域可用性有解释力。
- 基准若被广泛采用,可能成为健康类 AI 产品的事实准入标准,值得监管者提前关注。

## 实践意义

1. **健康/陪伴类产品的直接检验集**:建议在上线前跑通该基准并公开结果,这是目前最直接的心理健康场景安全证据。
2. **审批准入的参考条款**:基准中的安全红线设计(如自杀风险必转介)可成为产品审查与准入的参考条款。
3. **『专家参与式基准构建』的方法样本**:与通用基准不同,专家编写 + 敏感议题 + 安全维度的组合提供了可复制的构建范式。

## 跨厂商对比

- 与 [Safety Overview of GPT-6 Astra](safety-overview-gpt-6-astra.md) 互补:安全报告展示部署前的整体安全评估,本基准为心理健康这一垂直场景提供了标准化度量工具。
- 与 [Teen Development Research Grants](teen-development-research-grants.md) 及 [The Australian Youth Safety Blueprint](australian-youth-safety-blueprint.md) 构成 OpenAI 按人群分层的心理健康/安全证据链:青少年研究资助、国别安全蓝图与临床专家基准分别覆盖研究、政策与评测三层。
- 与 [Measuring the Pace of AI Development](../../anthropic/research/measuring-pace-of-ai-development.md) 对照:发展节奏度量依赖能力基准,而 MentalHealthBench 代表另一类基准——度量『不该做什么』的安全性基准,两类基准的构建方法论差异值得评估研究者总结。

## 资源

- 官方博客:[Introducing MentalHealthBench](https://openai.com/index/introducing-mentalhealthbench)
- 中文报道:[IT之家:1215 段对话评估](https://m.ithome.com/html/1006805.htm)、[凤凰科技:全新 AI 心理健康基准测试](https://tech.ifeng.com/c/8wgLgIOQLj8)
- 相关条目:[Safety Overview of GPT-6 Astra](safety-overview-gpt-6-astra.md)

> 注:openai.com 原文 403,本文基于多源转载交叉验证(IT之家/凤凰科技),官方 URL 已列于资源。
