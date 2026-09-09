# 瓦解一项来自俄罗斯的新隐蔽影响力行动（Disrupting a new covert influence campaign from Russia）

- **原文链接**: [Disrupting a new covert influence campaign from Russia](https://openai.com/index/disrupting-malicious-uses-of-ai-influence-campaign-russia/)
- **作者**: OpenAI
- **发布日期**: 2026-08-25
- **检索日期**: 2026-09-09
- **标签**: #OpenAI #影响力行动 #滥用治理 #安全

## 核心观点

OpenAI 封禁了一批极可能源自俄罗斯的 ChatGPT 账号。这些账号用于推广自称为以色列"专家社区"的 International Burke Institute（IBI）：一个 2025 年 2 月注册的网站，通过抄袭与错误署名学术文章、发布吹俄贬西方的"Burke 主权指数"，伪装成可信智库。运营者用俄语提示生成英文社媒评论，并明确要求 ChatGPT 隐藏俄语痕迹，借助 VPN 规避 OpenAI 对俄罗斯的访问限制。

尽管行动触达的受众有限（Brookings Breakout Scale 第三类下沿），其精心程度前所未有：这是 OpenAI 首次瓦解如此 elaborate 的俄罗斯关联影响力行动。文章指出其真正意义在于"制造权威"的基础设施——虚构专家、回炉学术内容、编造专有指数；而对 AI 的辅助性使用，恰恰成为整个行动暴露与被瓦解的入口。

## 关键发现 / 关键技术

### 1. 行动结构：伪装智库 + AI 宣传
- ChatGPT 仅用于生成推广 IBI 网站的社媒帖与评论，分布在 X、LinkedIn、Facebook、Substack、Telegram；帖子既有 IBI 名义账号，也有伪装成普通用户的账号
- IBI 网站文章并非模型生成：抽样 36 篇（2025-09 至 2026-05 发表）中 34 篇系从网上抄袭，部分错误署名——如把剑桥大学出版社原发自 Bradford 大学教授的文章错署给诺丁汉大学教授，把 Migration Policy Institute 的文章错署给一位澳大利亚食品科学教授

### 2. 归因线索：机器翻译泄露母语
- 德语报道把德国"红绿灯联盟"（Ampelkoalition）直译为"Svetofor coalition"——svetofor 是包括俄语在内多个斯拉夫语中的"交通灯"，英语或德语母语者几乎不可能这样表达
- 伪装美国媒体的 Telegram 账号"American Observer"简介出现非惯用英语（如 "a totally unhackneyed perspective on hazzy"）
- 另一运营者生成德语频道"Lahme Ente"（批判乌克兰、欧盟与德国政府、主张对俄友好）的内容，并为聚焦德美法波与土耳其的十余个 Telegram 频道生成 logo

### 3. 影响评估与意义
- 典型帖子浏览量低、官方账号订阅少；Telegram 频道各约 1–2 万订阅者；按 Brookings Breakout Scale 评估为第三类下沿（多平台、有少量破圈迹象）
- OpenAI 的核心判断：行动的价值不在受众而在基础设施——可随时间放大的"权威制造"资产；且其对 AI 的辅助性使用（提示语言、翻译破绽）成为识别与瓦解行动的关键证据

## 实践意义

对平台信任与安全团队而言，本案例展示了"AI 生成内容作为归因指纹"的检测思路：语言破绽、非惯用表达与提示模式可串联出幕后运营者。对研究错误信息与宣传的团队而言，"假智库 + 伪指数 + 回炉学术内容"的权威制造模式值得纳入监测清单——引用任何"指数""智库"前应核查内容来源与专家署名的真实性。

## 跨厂商对比

- 与 [我们对待 Model Spec 的方法](inside-our-approach-to-the-model-spec.md) 互补：Model Spec 定义模型应有的行为边界（含滥用防护），本篇展示边界被恶意利用后的检测、瓦解与披露闭环，是滥用治理"事前规则 + 事后执法"的两端。
- 与 [推进内容溯源](advancing-content-provenance.md) 互补：溯源技术从供给侧标记 AI 生成内容，本篇的调查方法从需求侧识别伪装机构，两者共同对抗"制造权威"式操纵。

## 资源

- 官方文章：https://openai.com/index/disrupting-malicious-uses-of-ai-influence-campaign-russia/
- 相关：N/A
