# dots 正式登场：OpenAI 的常驻个人 Agent（Introducing dots）

- **原文链接**: [Introducing dots](https://openai.com/index/introducing-dots)
- **作者**: OpenAI
- **发布日期**: 2026-09-29
- **检索日期**: 2026-10-16
- **标签**: #dots #个人Agent #常驻智能体 #ChatGPT #AgentOS

## 核心观点

dots 是 OpenAI 的主动式常驻助理（proactive assistants）：不等你开口、不重置记忆，在复杂项目与日常任务上持续推进工作，"让工作前进的同时你始终保持掌控"。它是 DevDay 2026 的旗舰新品，也被普遍视为对 Meta Muse 的正面应战——第三方评论将其定位为"Muse 与 Cue 的中间形态"：像 Muse 一样 24 小时在线，但比个人助理更"实体化"——每个 dot 有独立身份与权限体系、独立云端电脑与浏览器，可连接 4000+ 应用并同时处理多个项目。

dots 的发布标志着 OpenAI 把 ChatGPT 从"对话入口"升级为"常驻工作者"：同一个 dot 在网页、桌面、移动端、Slack、Teams 间保持上下文，既能被你召唤，也会主动汇报进度、提问、等你拍板。多 dot 组队与组织内"专职 dot"已在路线图与小规模测试中。

## 关键发现 / 关键技术

### 1. 形态：身份 + 云电脑 + 应用连接
- 每个 dot 可自定义名字、形象、角色；拥有一台独立云端电脑和浏览器。
- 可接入约 4000 个应用；用户可随时查看 dot 的云电脑在做什么，也可授权 dot 连接自己的笔记本进入真实工作环境。
- 一个 dot 同时接手多个项目自主推进——用户随时丢新任务，无需开新对话或逐步教学。

### 2. 交互：双向主动 + 跨渠道连续性
- 网页/桌面/手机可发消息或直接打电话给 dot；dot 也会主动联系用户（汇报、提问、等决策）。
- ChatGPT 之外已支持 Slack 与 Teams，短信接入在计划中；跨渠道共享同一上下文。

### 3. 开放与商业化
- 面向符合条件的市场逐步开放 Pro、Business Premium、Enterprise。
- 第一个 dot 包含在订阅内、聊天不占 ChatGPT 用量；但 dot 代跑 Codex 或 Work 任务时正常扣额度——"Agent 服务"的计费边界开始显形。
- 少量企业测试"专职 dot"：组织内独立身份与明确职责，即 Agent 作为"数字员工"的雏形；未来多 dot 组队协作。

### 4. 自主性边界（第三方批评焦点）
- dot 可用电脑、浏览器、4000+ 应用，但不碰支付与交易，关键步骤需用户确认——评论认为这与其说保守不如说受制于近期安全事件后的信任重建。

## 实践意义

1. **个人 Agent 从功能到形态**：dots 把"身份 + 持久上下文 + 独立执行环境 + 主动联络"打包为默认形态，为后续所有个人 Agent 产品设立了结构清单。
2. **企业"数字员工"试点开始**：专职 dot 的组织身份与职责设计，预示 HR/权限/审计将进入 Agent 管理范畴。
3. **隐私与自主性张力**：授权 dot 进入个人笔记本 + 长期在线，对权限最小化与行为审计提出比聊天助手高一个量级的要求。

## 跨厂商对比

- 与 [ChatGPT Work](chatgpt-work-partner.md) 互补：Work 让 ChatGPT 成为跨应用的"工作伙伴"，dots 给这份工作加上常驻身份与执行实体——同一战略的两级台阶。
- 与 [Fyxer：AI 行政助理](fyxer-email-agents.md) 对比：Fyxer 聚焦邮件单一场景的人机信任构建，dots 是全场景常驻形态；前者证明垂直信任需渐进积累，后者把信任问题一次性摆上台面。
- 与 [Meta 引入 Muse 个人 AI Agent](../../meta/introducing-muse-personal-ai-agent.md) 对照：Muse 以社交分发 + 硬件入口见长、行事大胆；dots 以企业渠道 + 权限保守为差异，9 月个人 Agent 井喷期的两条路线分野。

## 资源

- 官方发布：[Introducing dots](https://openai.com/index/introducing-dots)
- 第三方报道：[DoNews/字母榜 DevDay 综述](https://www.donews.com/article/detail/6885/107984.html)、[WIRED: OpenAI Wants Its New Agent to Run Your Life](https://www.wired.com/story/openai-wants-its-new-agent-to-run-your-life-mine-said-it-loved-me/)、[至顶网：Muse 还是 dots](https://www.zhiding.cn/ai-applications/2026/1014/3202072.shtml)
- 相关条目：[devday-2026-recap](devday-2026-recap.md)

> 注:openai.com 原文 403；本文基于官方 RSS 摘要 + DoNews、WIRED、qazinform、至顶网等多源交叉验证整理。
