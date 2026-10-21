# 备战 2026 美国中期选举（Preparing for the 2026 US midterms）

- **原文链接**: [Preparing for the 2026 US midterms](https://www.anthropic.com/news/2026-us-midterms)
- **作者**: Anthropic Policy 团队
- **发布日期**: 2026-10-14
- **检索日期**: 2026-10-16
- **标签**: #选举安全 #政治偏见 #AnthropicInsights #滥用防护 #中期选举

## 核心观点

中期选举前的选举防护升级汇报，配以 25 万条对话的隐私保护分析：美国 Claude.ai 对话中政治/政策/社会议题占约 5.75%，选举/投票专属约 0.51%，"问 Claude 该投谁"约 0.01%，违反选举诚信政策的约 0.002%——用户主要把 Claude 当信息工具而非投票顾问。5.5 家族三款模型在政治公正性评估上均达 99%，为历来最均衡。

方法上的两个亮点：三家独立机构从不同角度压测言论自由表现（且公开指出 Claude 的缺陷：Sonnet 4.5 对右倾立场的软化不对等）；ISD/McCain Institute 红队发现"单个恶意请求会拒、拆成多个无害子步骤的整场行动会漏"——直接催生多步骤滥用的新分类器。产品侧与 Democracy Works 合作把官方投票信息接入对话内应答与开票夜实时结果。

## 关键发现 / 关键技术

### 1. 使用画像（2026-09-21 至 27，25 万条随机样本）
- 政治/政策/社会：5.75%；选举/投票：0.51%；请求投票建议：约 0.01%（95% CI 上界展示）；违规：约 0.002%
- 典型用途：跟进新闻、政策研究、了解候选人、办理政府服务

### 2. 公正性测量与三方独立压测
- Opus 5.5 / Sonnet 5.5 / Haiku 5.5 政治公正性评估 99%，拒绝政治讨论的频率更低
- Vanderbilt Future of Free Speech：数百条争议话题测试，多数回应"有实质参与"但发现 Claude 爱加未请求的 caveat/反驳
- Foundation for American Innovation：左右配对 prompt，发现 Sonnet 4.5 hedge 不对等（右倾更易被软化）
- Collective Intelligence Project：美英印 2,000+ 人三阶段共创评估原则

### 3. 滥用演化与新防御
- ISD + McCain Institute 在美/以/巴西压测：单一有害请求可靠拒绝；拆解为受众研究→建新闻站→写内容→分发规划的多步行动可漏过
- 新增分类器：假社交账号/新闻站、财务动机选举骗局、外国国家行为者、选务基础设施网络防护
- 实战案例：境外运营的假新闻站用 Claude 生产利于俄/朝/伊叙事的中期选举报道——已封号

## 实践意义

"多步拆解绕过单点拦截"是本次最可迁移的发现：任何内容审核/滥用防护团队都应把检测单元从"单请求"升级到"跨会话行动模式"。对 AI 政治传播的观察者：0.01% 的投票建议请求说明主流用户并未把 Claude 当拉票工具，真正的风险面在供给侧（假站/假号工业化），需求侧焦虑可能被高估。99% 公正性 + 更少拒绝的组合表明"公正"与"乐于讨论"不再互斥——这是对 2024 年"过度拒绝"批评的针对性回应。

## 跨厂商对比

- 与 [Detecting and Countering Misuse of AI: September 2026](threat-intelligence-report-september-2026.md) 互补：威胁情报报告披露滥用趋势，本文展示选举场景的专项防御落地
- 与 [2026 Usage Policy update](2026-usage-policy-update.md) 对比：政策更新重新划定选举规则边界（取消个性化定向一刀切），本文是边界内的工程执行——规则与分类器的分工
- 与 [Anthropic's Approach to Teaching and Learning AI](../engineering/anthropics-approach-to-teaching-and-learning-ai.md) 对比：教育场景强调自主性递进，选举场景强调干预克制——同一"何时介入"哲学的两个高风险应用域

## 资源

- 论文：无
- 代码：无
- Demo：无
- 相关：竞选使用指南 https://cdn.sanity.io/files/4zrzovbb/website/027b10ca405e9bb66b98c88d911b4b21a0b70123.pdf
