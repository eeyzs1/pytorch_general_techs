# 在 ChatGPT 中推出健康功能（Launching Health in ChatGPT）

- **原文链接**: [Launching Health in ChatGPT](https://openai.com/index/health-in-chatgpt/)
- **作者**: OpenAI
- **发布日期**: 2026-07-23
- **检索日期**: 2026-08-01
- **标签**: #ChatGPT_Health #健康数据 #AppleHealth #医疗记录 #隐私保护 #HealthBench

## 核心观点

OpenAI 向美国用户正式推出 Health in ChatGPT：用户可安全连接 Apple Health 和支持的医疗记录（含美国医院系统、One Medical、Function Health），让 ChatGPT 基于真实健康背景回答问题——对比新旧化验结果、总结就诊变化、关联睡眠/运动与日常状态。核心数据：每周超 3 亿人向 ChatGPT 提出健康相关问题，但健康信息散落在患者门户、病历、应用和可穿戴设备中，难以形成完整图景。

产品设计上吸取了早期独立健康空间的教训——超 70% 的健康对话发生在专门空间之外，因此新版允许健康背景"随行"进入任意对话（经用户授权）。隐私被作为核心架构：连接的健康数据不用于训练基础模型或投放广告，默认逐次请求授权，断开连接后 30 天内删除同步数据。

## 关键发现 / 关键技术

### 1. 从独立空间到"背景随行"
- 早期测试发现健康提问常自然出现在饮食规划等日常对话中，独立空间增加了不必要步骤
- 新版 Health 留在侧边栏作为管理中枢（连接账户、查看趋势、浏览记录），对话中默认逐次请求授权，也可用 @Health 显式调用

### 2. 模型与评估：医师共建
- GPT-5.5 Instant 把前沿健康智能带给免费用户，在最难健康评估上达到当时 Thinking 模型水平；GPT-5.6 Sol 是付费用户的最强健康模型
- 与全球数百名医师共建真实健康场景与评分细则（准确性、安全性、沟通、背景意识、完整性、恰当升级）；全系 GPT-5.6 在 HealthBench Professional 上超过 GPT-5.5
- 发布前由医师对连接健康数据的真实使用进行广泛测试与红队演练

### 3. 分层隐私与安全
- 对话静态与传输加密，Health 连接信息有额外加密保护
- 健康数据不训练模型、不投广告（不受用户训练设置影响）；记忆不会直接从病历生成；跨插件分享健康信息前有额外确认护栏

## 实践意义

健康是 AI 助手"个人数据连接"战略中敏感度最高的场景，本文的隐私架构（不训练、逐次授权、30 天删除、跨插件护栏）可视为行业参考实现。与个人理财功能对照，OpenAI 已形成高敏场景的统一打法：只读连接、明确"不替代专业人士"、医师/专家共建评估。对产品而言，"背景随行而非独立空间"的教训值得所有垂直功能借鉴——用户不会为了某个上下文切换房间。

## 跨厂商对比

- 与 [提升 ChatGPT 的健康智能](improving-health-intelligence-in-chatgpt.md) 互补：前者讲模型健康能力训练，本文讲数据连接产品落地
- 与 [ChatGPT 个人理财体验](personal-finance-chatgpt.md) 对比：同一"敏感数据只读连接"范式在金融场景的平行应用，隐私承诺结构高度一致
- 与 [Anthropic 生物领域智能体](../../anthropic/research/agents-in-biology.md) 对比：Anthropic 面向科研机构的专业生物工作流，OpenAI 面向消费者的个人健康数据，受众与合规边界不同

## 资源

- 原文：[Launching Health in ChatGPT](https://openai.com/index/health-in-chatgpt/)
- 评估：[HealthBench Professional](https://arxiv.org/pdf/2604.27470)
