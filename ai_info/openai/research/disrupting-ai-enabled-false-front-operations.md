# 阻断借助 AI 的"虚假掩护"影响力行动（Disrupting AI-enabled "false front" operations）

- **原文链接**: [Disrupting AI-enabled "false front" operations](https://openai.com/index/disrupting-ai-enabled-false-front-operations)
- **作者**: OpenAI
- **发布日期**: 2026-10-08
- **检索日期**: 2026-10-16
- **标签**: #影响力行动 #滥用治理 #虚假身份 #地缘宣传 #平台安全

## 核心观点

OpenAI 封禁了源自俄罗斯与伊朗的两批 ChatGPT 账号：它们为地缘政治与冲突叙事运营"虚假掩护"（false front）实体——伊朗侧伪造七个"西方记者"人设向全球媒体供稿，俄罗斯侧把不知情的拉美雇员组织成一家"智库"，暗中破坏乌克兰的地区声誉并影响当地政治。OpenAI 称这是两年半来阻断过的最复杂的假面身份运营：掩护组织的大多数原创内容由被蒙在鼓里的真人员工生产，AI 在其中承担研究、写作与内容放大。

## 关键发现 / 关键技术

### 1. 伊朗行动：七个假记者、约百篇文章
- 七个伪装成美国等西方国家记者/自由撰稿人的人设（如自称"美国自由撰稿人"的 Ervin B. Hoskins），在 X、Instagram 等平台养号。
- 以这些署名在全球约 12 家中小型线上媒体（聚焦国际事务/地缘政治/中东）发表或转供稿件，OpenAI 识别出近 100 篇；最早一篇 2025 年 7 月，最新至 2026 年 10 月，今年美伊冲突爆发后发文频率明显上升。
- 同批账号还生成与美伊战争相关的社交媒体评论。归因线索来自平台透明度数据：X 显示该账号经"West Asia android app"连接、Instagram 显示位于伊朗——两账号随后被停用。

### 2. 俄罗斯行动："社会研究中心"智库伪装
- 运营名为 Social Research Center（SRC）的"智库"，在拉美招募不知情本地员工实际为俄方工作。
- 员工本人不知情，且 SRC 的多数原创内容由这些被蒙蔽员工产出——AI 用于辅助内容生产与放大，形成"真人劳动 + AI 提效"的混合掩护。
- 目标：损害乌克兰在拉美的声誉、影响当地政治。OpenAI 评价其为"两年半来阻断过的最复杂假面身份尝试"。

### 3. 模式演进
- 从以往"AI 批量生成水军内容"进化为"投资真人机构作为掩护、AI 做研究与放大"——检测难度从内容层（AI 文风）转移到组织层（机构真实性），平台需要跨平台透明度数据与媒体溯源配合。

## 实践意义

1. **假新闻的"供稿链"攻击面**：中小国际事务媒体的外部供稿审核是薄弱环节——编辑部应核查新撰稿人的可验证履历与本地 presence。
2. **"不知情员工"是新型攻击载体**：组织側的招聘与合作方尽职调查（谁在给这家"智库"发工资）比内容检测更能暴露此类行动。
3. **平台透明度元数据的价值**：本次归因关键证据是 X/Instagram 的连接方式与地理位置标记——跨平台数据共享是影响力行动治理的基础设施。

## 跨厂商对比

- 与 [Disrupting a covert influence campaign from Russia](disrupting-malicious-uses-of-ai-influence-campaign-russia.md)（8 月）对照：上月行动还是内容生成型（俄语矩阵账号），本次升级为机构掩护型——俄方行动在一个月内完成了形态跃迁。
- 与 [阻断有组织的模型蒸馏行动](disrupting-a-coordinated-model-distillation-campaign.md) 同观：同一周 OpenAI 安全博客披露的两类"协调滥用"分别针对模型资产与公共舆论，滥用治理正在与安全工程并列为常设职能。

## 资源

- 官方披露：[Disrupting AI-enabled "false front" operations](https://openai.com/index/disrupting-ai-enabled-false-front-operations)
- 第三方验证：[AFP: OpenAI says Iran, Russia influence ops busted](https://www.afp.com/en/openai-says-iran-russia-influence-ops-busted)
- 相关条目：[disrupting-malicious-uses-of-ai-influence-campaign-russia](disrupting-malicious-uses-of-ai-influence-campaign-russia.md)

> 注:openai.com 原文 403；行动细节（七个记者人设、~100 篇文章、SRC 智库结构、引语）经 AFP 对官方报告的详细转述核实，AFP 为独立通讯社。
