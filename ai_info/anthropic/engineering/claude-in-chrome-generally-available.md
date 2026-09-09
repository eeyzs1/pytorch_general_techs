# Claude in Chrome 正式发布（Claude in Chrome is generally available）

- **原文链接**: [Claude in Chrome is generally available](https://claude.com/blog/claude-in-chrome-generally-available)
- **作者**: Anthropic
- **发布日期**: 2026-08-26
- **检索日期**: 2026-09-09
- **标签**: #BrowserAgent #PromptInjection #Safety #GAMilestone

## 核心观点

Claude in Chrome 在所有付费 Claude 计划上正式 GA。最重要的变化是自主性：Claude 不再需要逐步人工确认，可以连续完成浏览器任务（读页、输入、点击、导航、填表，使用用户已有登录态）；每个动作执行前由一个安全分类器校验"是否安全且匹配你的原始请求"，不匹配即拦截——这与 Claude Code 的 auto mode 是同一机制，用户可在设置中关闭改回手动确认。

GA 的底气来自对抗 prompt injection 的进展：模型训练（持续增长的攻击库）、扫描工具结果的 probes、动作前分类器三层防御。文中罕见地披露了完整评估数据：在职业红队攻击的当前评估上，Opus 4.5 无附加防御时攻击成功率 17.6%、Opus 5 为 3.8%；而 Opus 4.8 之后的模型配合 probes + 安全分类器，Sonnet 5、Opus 5、Mythos 5 零成功，Fable 5 仅 0.3%（经人工核实均为低严重度场景）。

## 关键发现 / 关键技术

### 1. 三层 prompt injection 防御
- 训练：攻击库来自内部自动攻击器、外部红队与真实世界监控；新攻击得手即入库，反哺未来模型与已部署防线。自 2025 年 11 月首次披露浏览器防线以来，模型抵抗力显著提升。
- Probes：网页/邮件等内容经工具结果进入模型，probes 扫描其中的疑似注入并警告模型以怀疑态度对待、必要时先询问用户；自 Opus 4.5 起部署并持续扩大覆盖攻击类型。
- 动作分类器：自动批准仅限判定安全的动作；分类器核对将执行的动作（导航到某网站、在页面输入文本）与用户原始请求，不符即阻断。

### 2. 评估方法与数据
- 旧评估（Chrome 试点期构建）已饱和——Fable 5、Opus 5、Sonnet 5 在 Cowork harness 中即使无 probes/分类器也是 0% 攻击成功率——因此退役。
- 当前评估使用职业红队采购的更强攻击：攻击到达模型时，无附加防御下 Opus 4.5 成功率 17.6%、Opus 5 为 3.8%；2025 年 11 月最强防线下 Opus 4.5（含 probes）为 16.7%。
- 全防线（probes + 自动批准分类器）下：Sonnet 5、Opus 5、Mythos 5 无任何攻击成功；Fable 5 为 0.3%，成功案例均属低严重度、修复中。注：并非所有攻击都会"到达"模型。

### 3. 可用性与边界
- 从 Chrome Web Store 安装；Enterprise 管理员可在组织设置中管理并限制到批准域名。
- 尚不支持其他 Chromium 浏览器与移动端；本地文件与其他应用仍需 Claude 桌面端。

## 实践意义

本文为"Agent 安全披露"设立了新标杆：不只描述机制，还公布分层评估数字与新旧防线对比，并诚实标注残余风险（0.3%）与缓解进度。对工程团队，可借鉴的是其"训练 + 内容扫描 + 动作校验"纵深防御结构，以及用饱和即退役、持续升级的评估集来度量安全。对产品团队，"自动批准 + 逐动作分类器"正在成为跨端（CLI、浏览器）统一的自主性安全范式。

## 跨厂商对比

- 与 [Cowork Chrome side panel](cowork-chrome-side-panel.md) 对比：从扩展 + 侧栏、逐步确认的形态，到 GA 后免逐步确认的自主形态，勾勒出浏览器 Agent 产品线的演进路径。
- 与 [Auto mode default in Claude Code](auto-mode-default-in-claude-code.md) 互补：同一"安全动作自动批准 + 分类器校验"机制从 CLI 默认扩展到浏览器，说明该机制是 Anthropic 的通用自主性底座。

## 资源

- 官方文章：https://claude.com/blog/claude-in-chrome-generally-available
- 相关产品：https://www.anthropic.com/research/prompt-injection-defenses（浏览器防线详解）
