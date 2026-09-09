# 把 Claude Mythos 5 的网络安全能力带给更多防御者（Bringing the cybersecurity capabilities of Claude Mythos 5 to more defenders）

- **原文链接**: [Bringing the cybersecurity capabilities of Claude Mythos 5 to more defenders](https://claude.com/blog/bringing-claude-mythos-5-to-more-defenders)
- **作者**: Anthropic（安全团队）
- **发布日期**: 2026-08-21
- **检索日期**: 2026-09-09
- **标签**: #网络安全 #Mythos5 #ProjectGlasswing #开源安全 #CyberVerification

## 核心观点

Anthropic 把最强网络安全模型 Claude Mythos 5 从 4 月启动的 Project Glasswing 小范围试点扩展到更多防御者：Claude Security 扫描即日起可运行 Mythos 5，合作伙伴的网络安全产品将集成该模型，同时新设 3500 万美元的 Defender Advantage Fund（0xDAF）资助开源软件安全，并扩大 Cyber Verification Program。

核心风险逻辑是分发设计：用户直接与模型对话的风险最高，而只接收特定输出（一个补丁、一条告警）的风险则低得多。因此 Anthropic 以"输出型访问"扩大防御能力覆盖面——用户拿到 Mythos 级的防御结果，但无法把模型引向攻击用途——同时对模型的直接访问保留护栏。

目标是让医院、电网、金融系统与软件供应链的防御者在恶意行为者获得同级能力之前，先用上前沿防御能力。

## 关键发现 / 关键技术

### 1. Claude Security × Mythos 5
- Claude Enterprise 客户公测：扫描代码库并给出带 CWE 分类、置信度与严重度评级的发现及建议补丁；补丁在 Claude Code on the web 中实施，且必须经人工评审批准才能上线；按现有计划的标准 token 用量计费，无单独附加费。
- 扫描只返回详细发现而非模型原始输出，Mythos 访问不外溢到其他界面——防御者获得能力而不获得模型本体。

### 2. 合作伙伴集成与 3500 万美元 0xDAF 基金
- 与网络安全产品与服务伙伴合作把 Mythos 5 内建进防御者既有的安全运营、事件响应、威胁情报工具：终端用户通过专用界面获得特定产物（如建议补丁列表），无法提示模型开发利用，双方另有防滥用措施验证模型停留在预期范围内。
- Defender Advantage Fund（0xDAF）提供 3500 万美元 Claude credits，资助修补广泛使用开源项目的在档漏洞、可复制的自动化扫描与修补、抵御整类攻击的更激进安全方案；延续 Glasswing 已做的 400 万美元直接捐赠及对 Akrites、Gold Eagle 等协调修复计划的支持。

### 3. Cyber Verification Program 扩展
- 该计划已为审核通过的防御团队在 Opus/Sonnet 上降低安全拦截，减少合法授权安全工作的中断；数周内将扩展到更广的双用途能力，Mythos 级访问随后跟进。
- 与美国政府合作的 Project Glasswing 通道继续面向满足严格安全控制要求的关键基础设施保护者扩展。

## 实践意义

这是"前沿能力部署节奏"问题的一个具体答卷：Glasswing 给防御者留出的时间窗口，如今通过三类输出型通道（托管扫描、伙伴产品、验证计划）系统化扩展。对企业安全团队而言，Claude Security 的 Mythos 5 扫描 + 人工批准补丁流是一个可直接试用的入口；对安全厂商而言，"集成模型交付产物而非开放模型"的产品形态给出了把前沿模型商业化的合规模板。开源维护者则可关注 0xDAF 的申请通道——基金明确面向志愿者维护的项目。

## 跨厂商对比

- 与 [用 Claude 发现密码学弱点](../research/discovering-cryptographic-weaknesses.md) 对比：那篇展示 Mythos 级模型发现真实密码学弱点的攻防能力（能力本身的证明）；本文讲如何把这种能力安全地分发给更多防御者（能力的社会化与治理），两者是同一网络安全叙事的"研究"与"部署"两章。
- 与 [Daybreak: Tools for Securing Every Organization in the World](../../openai/research/daybreak-securing-the-world.md) 互补：OpenAI 的 Daybreak/Patch the Planet 同样聚焦"为全世界的组织修补漏洞"，Anthropic 以 Claude Security 托管扫描 + 3500 万美元 credits + Cyber Verification 计划落地——两家都把"防御者优先接触前沿模型"作为公开承诺。

## 资源

- 论文：N/A
- 代码：N/A
- 官方文章：https://claude.com/blog/bringing-claude-mythos-5-to-more-defenders
