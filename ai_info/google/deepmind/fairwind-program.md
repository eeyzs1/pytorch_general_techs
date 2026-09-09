# Fairwind：面向政府与企业的主动式网络防御（Proactive cyber defense for governments and enterprises）

- **原文链接**: [Proactive cyber defense for governments and enterprises](https://blog.google/innovation-and-ai/technology/safety-security/fairwind-program/)
- **作者**: Google（Safety & Security 团队，官方博客未署名）
- **发布日期**: 2026-09-02
- **检索日期**: 2026-09-09
  注：官方页面抓取受限，本文基于检索核验的日期与公开报道整理（机制细节经 Apidog/TechTarget 日本转述核验）
- **标签**: #网络安全 #Fairwind #主动防御 #漏洞管理

## 核心观点

Google 启动 Fairwind 有限访问计划，把自家网络防御工具（核心是 Gemini 3.8 Flash Cyber 安全模型与 CodeMender 自动修复集成）向受信任的政府机构、关键基础设施运营方、软件维护者与核心技术平台开放，实现"主动式网络防御"：把漏洞响应从人工检测推进到"发现—修复—验证"的自动化闭环。

Fairwind 取代了 3.5 Flash Cyber 时代的邀请制试点：有公开申请流程、背景审查（安全历史与"伦理运营"）与成体系的伙伴义务。Flash Cyber 无公开 API、无公开定价、权重不开源、仅服务端托管——能力越强，分发越收紧。

## 关键发现 / 关键技术

### 1. 准入与义务设计
四类主体可申请（可信政府当局、关键基础设施运营方、软件维护者、核心技术平台），从事防御性基准评测的学术实验室亦可申请；独立研究员、赏金猎人与无基础设施足迹的咨询公司不在公布类别中。伙伴义务包括：每个使用者需防钓鱼 MFA 级别的用户级认证、访问仅限内部网络安全/事件响应/渗透测试团队、跟踪员工访问与使用、禁止任何形式的共享转售——条款封死了"包一层转卖"与"借 key 给承包商"的口子。

### 2. 交付物：以修复为导向的模型能力
经 Fairwind 提供的 Gemini 3.8 Flash Cyber 捆绑 CodeMender 自动修复工具链，漏洞发现后可直接产出补丁提案而非止步于报告；Google 公布的伙伴结果包括 Chrome 安全补丁数 2.6 倍于最佳商业模型、Wiz 渗透测试召回率提升 7.5–9.7 个百分点且成本降低 2.3–5.2 倍、关键漏洞发现从数月缩短到 2 小时内（均为 Google 侧或其具名伙伴数据）。

### 3. 竞争叙事的转变
第三方报道（TechTarget 日本）把 Fairwind 解读为漏洞响应竞争从"检测速度"转向"修复速度"的标志：当发现到修复通常需数周时，生成式 AI 有望把该周期压缩到分钟级，而 Fairwind 决定了谁能用上这把加速器。

## 实践意义

对政府 CERT、关基运营方与大型开源维护者，Fairwind 提供了把前沿安全模型嵌入 SOC 工作流的合规通道，代价是接受审计与用途限制；对普通企业安全团队，可用的仍是通用版 Gemini 3.8 Flash（代码审查、CVE 解读、指定缺陷修复），攻击面探索类请求会被通用安全训练拒绝。跨厂商看，"受限安全模型 + 准入计划"正在成为行业共识的部署形态。

## 跨厂商对比

- 与 [发布 Gemini 3.5 Flash Cyber：轻量级网络安全模型](introducing-gemini-3-5-flash-cyber.md) 对比：3.5 时代是政府与受信伙伴的邀请制试点，Fairwind 将其制度化为有申请流程、背景审查与义务条款的常设计划，交付物也从单一模型升级为"模型 + 修复工具链"。
- 与 [Daybreak: Tools for Securing Every Organization in the World](../../openai/research/daybreak-securing-the-world.md) 互补：两家都在探索"防御优先的受限安全能力 + 定向分发"，对照可见安全能力治理正从模型问题转变为分发与准入问题。

## 资源

- 官方文章：https://blog.google/innovation-and-ai/technology/safety-security/fairwind-program/
- 产品/API：https://deepmind.google/fairwind-program/
