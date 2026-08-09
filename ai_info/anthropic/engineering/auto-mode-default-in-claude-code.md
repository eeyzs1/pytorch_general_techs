# Auto Mode 成为 Claude Code 默认权限设置

- **原文链接**: [Auto mode is now the default in Claude Code for Pro, Max, and Team plans](https://claude.com/blog/auto-mode-default-in-claude-code)
- **作者**: Anthropic
- **发布日期**: 2026-08-07
- **检索日期**: 2026-08-08
- **标签**: #安全 #权限 #ClaudeCode #自动审批 #PromptInjection #分类器

## 核心观点

Anthropic 宣布从 2026 年 8 月 14 日起，Claude Code 的 auto mode 将成为 Pro、Max、Team 计划的默认权限设置。这意味着新会话将自动启用基于分类器的自动权限决策，而非传统的逐条审批。分类器开销即日起不再向这些计划的用户收费。

Auto mode 的设计目标是在"不被打断"和"避免有害操作"之间取得平衡：每个工具调用都经过分类器评估，针对不可逆、破坏性或越界操作进行拦截。一项涉及 1,053 名付费测试者的对照实验显示，人工审核仅能拦截 13.6% 的危险命令，而 auto mode 可拦截 89%。在真实生产会话分析中，手动批准会话出现严重意外伤害的频率是 auto mode 会话的两倍以上。Auto mode 还让 Claude 自主运行时间延长，Teams & Enterprise 采纳者的 PR 产出增加约 25%。

## 关键发现 / 关键技术

### 1. 手动审批的失效：97% 批准率与审批疲劳

数据表明手动审批已变成习惯性动作：用户批准了 97% 的权限提示。截至 2026 年 6 月，49.5% 的活跃 CLI 用户手动创建了 Bash 允许规则，其中 5% 直接允许任意 shell 命令，另有 43% 设置了 `Bash(python:*)` 等解释器规则（实际等效于任意执行）。62% 的用户使用过 `bypassPermissions` 或点击"不再询问"，25% 的交互式会话以 bypass 模式启动。

### 2. 1,053 名测试者对照实验

通过研究供应商雇佣 1,053 名付费专业测试者进行编码研究。每个会话中途将一个权限提示替换为明显危险的命令。测试者仅拦截了 13.6%（143/1053），而 auto mode 拦截了 89%（937/1053）。随着会话变长，人工表现下降：早期拦截约 17%，50+ 提示后降至约 5%；auto mode 的拦截率则不随会话长度变化。

### 3. 第三方红队与 Prompt Injection 防御

Apollo Research 进行了两周 pilot，注入合成攻击。加固后分类器在 held-out 攻击集上捕获了约一半此前漏掉的攻击，miss rate 从 12% 降至 7%。Trajectory Labs 的独立评估中，72 个间接 prompt injection 场景各测试 10 次（共 720 次），**Claude Fable 5、Opus 5、Sonnet 5 运行 auto mode 时零攻击成功**；而 GPT-5.6 Sol 运行 Codex Auto-review 模式的攻击成功率为 5.83%，Full Access 模式为 19.03%。

### 4. 数据访问与共享规则强化

新增 hard denies 机制（数据外泄类操作永不批准）、secrets 与敏感信息区分规则、git push 目标可见性检查（public/private/trusted）、以及破坏性 git 操作前的 git status 检查。

## 实践意义

auto mode 成为默认标志着 Agent 权限管理从"人工逐条审批"正式转向"分类器自动决策"范式。对工程团队而言，这意味着长时运行 Agent（如 Claude Opus 5 处理大型任务数小时）变得更实用，同时安全性由数据支撑而非依赖易疲劳的人工判断。Enterprise 与 API 用户仍保留 opt-in 时间窗口，管理员可通过 managed settings 提前启用。

## 跨厂商对比

- 与 [Claude Code Auto Mode: A Safer Way to Skip Permissions](claude-code-auto-mode.md) 对比：本文是 auto mode 从 opt-in 功能升级为默认设置的产品公告，补充了 1,053 人对照实验、第三方红队、prompt injection 评估等新安全数据，以及"分类器开销不再收费"的商业策略转变
- 与 [Beyond Permission Prompts](beyond-permission-prompts.md) 互补：后者提出沙箱隔离架构作为安全 YOLO 模式的底层保障，auto mode 则在权限决策层用分类器替代人工审批，两者构成"隔离 + 分类器"的双重防御

## 资源

- 论文：N/A
- 代码：N/A
- Demo：https://code.claude.com/docs/en/auto-mode-config
