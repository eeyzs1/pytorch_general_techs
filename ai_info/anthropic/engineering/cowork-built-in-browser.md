# Cowork 中 Claude 拥有了自己的浏览器（Claude gets its own browser in Cowork）

- **原文链接**: [Claude gets its own browser in Cowork](https://claude.com/blog/cowork-built-in-browser)
- **作者**: Anthropic
- **发布日期**: 2026-08-26
- **检索日期**: 2026-09-09
- **标签**: #Cowork #BrowserAgent #DesktopApp #Sandboxing

## 核心观点

Claude Cowork 桌面端内置了 Claude 专属浏览器：当任务需要用到网站时，侧栏自动打开浏览器，Claude 自己导航网页、阅读、点击、输入——填表单、从仪表盘抽数、处理没有 connector 的 portal，全程免扩展、免安装。用户把任务的"网页部分"交出去后可以继续手头工作。

与 Claude in Chrome 的关键区别在于隔离："这是 Claude 的浏览器，不是你的"。Claude 看不到用户的标签页、书签、密码；除非用户逐站点主动迁入登录态，否则不共享任何东西（银行、邮箱、SSO 站点默认排除）。两条产品线分工明确：内置浏览器用于交出完整网页任务，Claude in Chrome 用于操作你已打开的页面与已登录的账户。

## 关键发现 / 关键技术

### 1. 隔离与登录态迁移
- Claude 永远看不到用户自己的标签页、书签、密码。
- 需要保持登录时可按站点迁入登录态：macOS 支持 Chrome/Edge/Firefox，Windows 与 Linux 支持 Firefox；银行、邮件、单点登录站点默认排除，除非用户显式选择包含。

### 2. 两种浏览器形态的分工
- 内置浏览器：交接式任务——为报告做调研、从供应商 portal 收集本月发票等"只需要一个浏览器"的场景。
- Claude in Chrome：操作用户已打开的页面——更新 CRM、处理收件箱、编辑眼前的文档；已安装扩展的用户保持默认不变，其他用户默认用内置浏览器。Settings → Cowork → Preferred browser 随时切换。

### 3. 安全与可用性
- 与任何在浏览器中行动的 Agent 一样承载 prompt injection 风险；内置浏览器运行与 Claude in Chrome 相同的防线（含"动作与请求核对"），官方明确这些措施显著降低但不消除风险，建议先在信任的站点上使用。
- 本周起向 Pro、Max、Team 计划滚动（macOS/Windows/Linux beta），到位后默认开启——给 Claude 涉及网站的任务即自动弹出；Enterprise 计划今日起可由管理员在组织设置中开启。浏览器住在桌面端：网页端或手机也可驱动，前提是桌面端在线。

## 实践意义

"自带浏览器"补齐了 Agent 工作流的关键一环：此前给 Claude 网页能力意味着交出用户自己的浏览器（及其全部登录态），现在任务级浏览器与个人浏览器解耦，隔离边界从"用户自律"变成"产品结构"。这与 CLI 世界里沙箱化执行、浏览器世界里独立会话的思路一致。对企业采纳者，逐站点登录迁移 + 默认排除高敏站点 + 管理员开关，构成了一条可控的渐进授权路径。

## 跨厂商对比

- 与 [Cowork Chrome side panel](cowork-chrome-side-panel.md) 对比：从"借用用户浏览器 + 扩展"到"自带隔离浏览器"，反映了浏览器 Agent 从能力验证走向信任设计。
- 与 [Introducing Operator](../../openai/research/introducing-operator.md) 对比：Operator 是独立的 Agent 浏览器产品形态，Cowork 内置浏览器把同等能力嵌入既有桌面工作流，两种产品化路径（独立入口 vs 工作流内嵌）值得对照观察。

## 资源

- 官方文章：https://claude.com/blog/cowork-built-in-browser
- 相关产品：https://claude.com/product/cowork
