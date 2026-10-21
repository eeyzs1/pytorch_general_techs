# OpenAI DevDay 2026 回顾：二十余项更新宣告 Agent 时代（DevDay 2026 Recap）

- **原文链接**: [DevDay 2026 Recap](https://openai.com/index/devday-2026-recap)
- **作者**: OpenAI
- **发布日期**: 2026-09-29
- **检索日期**: 2026-10-16
- **标签**: #DevDay2026 #Agent #dots #GPT-6.1Sol #ChatGPTSpace #Codex #Ultrafast

## 核心观点

DevDay 2026 一场发布会抛出 20+ 项更新，主线只有一个：把 ChatGPT 从"响应需求"的产品改造成一套可以长期承担工作的 Agent 系统。旗舰新品是常驻个人 Agent [dots](introducing-dots.md) 与人机共享工作区 ChatGPT Space（取代原 Library）；模型侧发布 [GPT-6.1 Sol](introducing-gpt-6-1-sol.md)——以 Astra 五分之一的价格逼近其编程与计算机操作能力；基础设施侧 Ultrafast 高速模式进入 ChatGPT Work 与 Codex，并新增 500 美元档 Pro 500 订阅。

模型本身已不是这场发布会的中心：dots 的身份体系、Space 的共享上下文、Codex 的可复用云环境、插件目录与 MCP 事件触发共同构成"harness + infra + context"三层支撑。订阅的含义随之改变——从"多少次模型调用"变成一整套 Agent 服务，批评者称之为 AaaS（Agent as a Service）重走 SaaS 老路。

## 关键发现 / 关键技术

### 1. dots：常驻个人 Agent（本次最重要新品）
- 24 小时在线、无需重复交代背景；每个 dot 有独立身份与权限体系、一台独立云端电脑和浏览器，可连接 4000+ 应用，同时推进多个项目。
- 可自定义名字/形象/角色；用户可随时查看其云电脑工作状态，也可授权连接本人笔记本带入真实工作环境。
- 跨渠道保持上下文：网页/桌面/移动端可发消息或打电话，dot 也会主动汇报、提问；已支持 Slack 与 Teams，短信在路线图上。开放 Pro、Business Premium、Enterprise；首个 dot 含在订阅内。企业"专职 dot"（组织内独立身份与职责）在小范围测试，多 dot 组队是既定方向。

### 2. ChatGPT Space 与 Pages
- 文件、页面、演示文稿、表格、项目资料放入同一 Space，随时 @ChatGPT/Codex/dot 基于共享内容工作。
- 核心组件 Page 为多人实时编辑文档，可放交互工具，Agent 可直接修改内容、补图表、继续研究，并可从已连接工具持续获取信息、自动更新（依赖插件新增的 MCP 事件触发）。移动端首发只读。

### 3. GPT-6.1 Sol 与 Ultrafast、Pro 500
- GPT-6.1 Sol 定位"接近 Astra 的专业工作能力 + Sol 档价格"，详见[专文摘要](introducing-gpt-6-1-sol.md)。
- Ultrafast 模式从 GPT-5.6 Sol 预览扩展到 GPT-6 Astra 并正式进入 ChatGPT Work 与 Codex：Codex 内 token 生成最高 8×（约 300 tokens/s）、API 内最高 6×；首发仅 Pro 500 及符合条件的 Enterprise/Edu 工作区。
- Pro 500：月费 500 美元，额度约为 Plus 的 25 倍 + Astra Ultrafast；Pro 200 重新开放但用量口径改变（第三方测算按 API 标价折算约为旧版一半），引发"要么加钱、要么降智"争议。

### 4. Codex 全家桶更新
- Codex Cloud：云端开发环境可复用（不必每次重建沙箱）、手机远程接管、团队共享环境与权限；CLI 支持语音对话、新增 /agents 多 Agent 视图、Prompt 直接编辑、会话恢复、内置 git worktree 隔离。
- 代码审查：摘要 + diff + 追问，支持离线云端初审，覆盖 GitHub PR 与 GitLab MR。
- Codex Security Cloud 默认接入 Daybreak Blue 网络安全模型：可整仓扫描、持续检查新提交、调查去重并整理修复方案。
- Agents API 补齐 computer use：OpenAI 托管底层 Codex 执行框架，多 Agent、工具、上下文压缩与 computer use 一体化。

### 5. 平台与企业
- 插件：重做创建/提交/发现流程与统一目录；新增 MCP 事件触发；企业可把插件嵌入自建网站并按成员身份权限调用。
- 新增 Sign in with ChatGPT（类谷歌登录，默认只共享姓名/邮箱/头像）、可分享个人资料页、Decisions API（Luna 在预设选项中做实时分类/路由判断，限量预览）、Amazon Bedrock 托管 Agent（Agents API 形态）、隐私智能（零数据保留 + 离线自动安全审查 + 隐私推理）、可刷 OpenAI 额度的软件市场（Adobe/Figma/Salesforce/ServiceNow/CrowdStrike 等）。

## 实践意义

1. **产品重心从模型转向系统**：Agent 好不好用越来越取决于模型之外的 harness（组织行为）、infra（稳定执行）与 context（认识用户）三层——与 OpenAI 自己的 Harness Engineering 叙事完全一致。
2. **订阅经济学切换**：dots 装进订阅、Ultrafast/最高额度向 Pro 500 收拢，"按调用付费"向"按 Agent 服务付费"迁移；采购方需重新核算单位工作成本。
3. **自主性边界仍踩刹车**：dot 不碰钱、不做交易、关键步骤需用户确认——三个月内两次暂停训练的背景下，OpenAI 明显比 Meta Muse 等竞品保守，这既是差异化卖点也是能力上限。

## 跨厂商对比

- 与 [GPT-6 Sol 与 Luna 发布](introducing-gpt-6-sol-and-luna.md) 对比：9/22 的降价是"价格战"单点动作，DevDay 则把价格优势（6.1 Sol）组装进完整 Agent 产品矩阵，策略从卖模型转向卖系统。
- 与 [ChatGPT Work](chatgpt-work-partner.md) 互补：Work 把 ChatGPT 升级为"跨应用工作伙伴"，dots 进一步给了它常驻身份、云电脑与主动联络能力，是同一产品线的两步演进。
- 与 [Introducing the Agents API](introducing-the-agents-api.md) 衔接：DevDay 为 Agents API 补上 computer use 与托管执行框架，智能体骨架从 API 原语走向开箱即用。

## 资源

- 官方回顾：[DevDay 2026 Recap](https://openai.com/index/devday-2026-recap)
- 第三方综述：[DoNews/字母榜：一文速览 OpenAI DevDay](https://www.donews.com/article/detail/6885/107984.html)、[UISDC：这届 DevDay 最值得关注的 6 件事](https://www.uisdc.com/openai-devday-recap)
- 相关条目：[introducing-dots](introducing-dots.md)、[introducing-gpt-6-1-sol](introducing-gpt-6-1-sol.md)

> 注:openai.com 原文 403，本文基于官方 RSS 标题/摘要 + DoNews（字母榜）、UISDC 第三方综述交叉验证；具体数字（8×、300 tokens/s、25 倍额度等）引自第三方现场记录，待官方页面可达后复核。
