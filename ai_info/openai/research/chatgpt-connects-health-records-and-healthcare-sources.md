# 医疗机构现可将 EHR 与行业数据接入 ChatGPT（Healthcare organizations can now connect EHR and additional industry data to ChatGPT）

- **原文链接**: [Healthcare organizations can now connect EHR and additional industry data to ChatGPT](https://openai.com/index/chatgpt-connects-health-records-and-healthcare-sources/)
- **作者**: OpenAI
- **发布日期**: 2026-09-01
- **检索日期**: 2026-09-09
- **标签**: #医疗AI #EHR集成 #数据治理

## 核心观点

OpenAI 为 ChatGPT for Healthcare 引入两项数据连接能力：新的 Epic 电子病历（EHR）集成把授权患者上下文带入 ChatGPT，Healthcare Public Data 插件则提供对 PubMed、DailyMed、CMS Coverage 等九个官方医疗数据源的结构化直连。临床医生可以在一个受治理的工作区中安全地获取患者上下文与医学研究，而不必在预约记录、化验结果、用药与专科文档之间来回检索。

产品形态上支持两种互补体验：把授权患者信息从 EHR 带入 ChatGPT 做诊前准备，以及在受支持部署中把 ChatGPT 直接嵌入 EHR 界面，让 AI 辅助工作流不离开病历。UCSF Health 作为试点合作伙伴参与验证， AdventHealth 也在业务侧采用了同一治理工作区。

这套能力建立在配套的企业控制之上：角色访问、单点登录、审计日志，以及在适用商业伙伴协议（BAA）下的 HIPAA 合规工作流，覆盖 ChatGPT Work、Codex、应用与插件。

## 关键发现 / 关键技术

### 1. EHR 双向体验与九大官方数据源插件
- EHR 集成让临床医生用自然语言提问（"这位患者上次就诊后有什么变化？""今天门诊前应关注哪些化验结果？"），系统汇总授权病历中的相关信息并回溯到病历出处。
- Healthcare Public Data 插件聚合 ClinicalTrials.gov、CMS Coverage、RxNorm、DailyMed、PubMed 等九个官方源的结构化连接，支持精确比较试验入组标准、药品标识符、覆盖政策版本与医生记录，避免逐站检索。
- 分层可用性：Healthcare 客户由管理员启用；Enterprise 客户经账户团队确认 Regulated Workspace 配置；美国个人临床医生仅可安装公共数据插件，EHR 集成不对个人账户开放。

### 2. 基于真实医疗工作的评估
- OpenAI 与 60 个国家、49 种语言、26 个医学专科的数百名医生合作，累计审查超过 70 万条模型回复。
- 针对连接 EHR 上下文的表现：27 个临床用例（诊前回顾、临床时间线、用药审查、交班摘要等）、4,363 条评级中 99.1% 被医生评为安全。
- 另一轮两阶段评估中，基于美国大型医疗数据集的细微临床问答，五个被测连接数据源均有超过 93% 的回复被评为"良好"或更好的准确性。

## 实践意义

这是通用 AI 助手向"可信数据生态"演进的关键一步：模型能力之外，谁能把 EHR、官方药典与医保政策这类权威结构化源以受治理方式接入，谁就能进入临床工作流的核心。对医疗机构的启示是分阶段路径——先在受控工作区中连接公共数据源，再评估 EHR 集成与 BAA 配置，同时保留人类医生对每项输出的审阅责任。

对行业观察者而言，评估方法论同样值得关注：用真实临床用例与医生评级（而非纯基准分数）来验证连接上下文下的安全性与准确性，为医疗 AI 的落地验收提供了可复制的范式。

## 跨厂商对比

- 与 [ChatGPT 中的健康能力](health-in-chatgpt.md) 对比：health-in-chatgpt 面向个人用户的健康对话与信息支持，本文则是企业级的受治理数据连接（EHR 集成 + 官方数据源插件），标志 OpenAI 医疗线从消费级走向机构级。
- 与 [AI co-clinician](../../google/deepmind/ai-co-clinician.md) 互补：DeepMind 的协作临床医生聚焦临床科研假设生成与验证工具，本文聚焦把可信医疗数据源接入通用助手工作区，两者共同构成医疗数据生态的不同切面。

## 资源

- 官方文章：https://openai.com/index/chatgpt-connects-health-records-and-healthcare-sources/
- 相关：N/A
