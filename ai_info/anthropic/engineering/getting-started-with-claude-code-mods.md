# Claude Code mods 入门：用 JS/TS 改写 IDE 行为（Getting started with Claude Code mods）

- **原文链接**: [Getting started with Claude Code mods](https://claude.dev/blog/getting-started-with-claude-code-mods/)
- **作者**: Addy Osmani
- **发布日期**: 2026-10-01
- **检索日期**: 2026-10-16
- **标签**: #ClaudeCode #mods #插件系统 #hooks #自定义UI

## 核心观点

mods 是运行在 Claude Code 会话内的小型 JS/TS 模块：能观察会话中的一切事件、改写 Claude Code 的行为、或在终端/桌面端绘制自定义 UI。本质是"打包成插件的 hooks"——每个 mod 通过 register(on) 注册事件钩子，形成类似中间件的链：观察（next 后返回）、改写（改参数后 next）、应答（不经 next 直接拒绝或代答）三种动作。Claude Code 自身的一些功能（AGENTS.md 支持、/diff 面板）就是以 mod 形式实现的，源码在公开仓库 mods/ 下。

零门槛入口被刻意做低：不需要学 API，直接对 Claude 描述想要的 mod，允许热重载后当场生成。教程用 80 行的 Token Weather（上下文窗口天气条）走完全流程，再用 Blast Radius（危险命令预览面板）和 Replay Theater（回放本回合编辑）两个进阶示例展示 API 边界。

## 关键发现 / 关键技术

### 1. 事件与 API 面
- 事件覆盖：tool.call、prompt.submit、turn 起止、session 起止、slash 命令、ui.render（界面每块绘制）
- `$` API：ui/session/state/store/fs/process/clock/http/tool/command/model——mod 跑在无 DOM 无 Node 的沙箱，一切经 `$`
- 状态放 `$.state`（宿主持有，热重载后存活）而非模块变量——每次保存都是重新 register

### 2. 三个示例 mod
- Token Weather：AbovePrompt 组件上画上下文占比天气条（<25% ☀ / 90%+ ↯ Compact soon），12 回合 sparkline + 增量；读 `$.session.usage()` 免费且 state 变更自动重绘
- Blast Radius：拦 rm -rf / git reset --hard / 迁移类命令，先 dry-run（git status --porcelain、du 等）算波及面，开 Pane 让人按 1/2 决定；窄终端自动降级画到提示条上方
- Replay Theater：记录本回合每次 Edit/Write 的前后文本，回合结束后 /replay 逐步走 diff

### 3. 工程配套
- Claude Code 2.1.287+ 默认启用；每次加载把当前构建的类型声明写进 mod 的 .claude-plugin/types/
- claude plugin validate 静态校验钩子与调用；claude plugin test 在真实运行时上跑 *.test.ts（测试钩子可 stub $.session.usage 等宿主应答）
- 分发即插件：marketplace.json + 三条命令安装；mod 运行在用户机器上权限同 Claude Code，"只装信任来源"被反复强调

## 实践意义

mods 把 Claude Code 从"可配置的工具"变成"可编程的平台"——与 VS Code 扩展生态的差别在于：模板里内置了"让 Claude 帮你写 mod"的第一方路径，扩展开发本身也被 agent 化。最实用的两类 mod 是"可视化状态"（Token Weather 类）与"高风险动作的人工确认面板"（Blast Radius 类）——后者本质是把 permission prompt 升级为富交互。团队采用建议：从"每个工程师自己观察什么"的问题出发提需求，让 Claude 生成，再决定是否值得沉淀为团队插件。

## 跨厂商对比

- 与 [Beyond Permission Prompts](beyond-permission-prompts.md) 对比：沙箱机制做的是"限制能碰什么"，mods 做的是"在碰之前让人看清会碰什么"——硬边界与知情确认的互补
- 与 [Claude Code Best Practices](claude-code-best-practices.md) 互补：CLAUDE.md 管上下文与约定，mods 管行为与 UI——配置面与编程面的分层
- 与 [Claude Code in the cloud](claude-code-in-the-cloud.md) 同期发布：云会话把执行环境外移，mods 把客户端体验深挖——Claude Code 平台化的两翼

## 资源

- 论文：无
- 代码：https://github.com/anthropics/claude-code-playground/tree/main/claude-code/mods
- Demo：无
