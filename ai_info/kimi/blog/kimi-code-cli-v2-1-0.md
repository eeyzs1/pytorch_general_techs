# Kimi Code CLI v2.1.0:全屏 TUI 与工作区安全加固(Kimi Code CLI v2.1.0)

- **原文链接**: [Kimi Code CLI Changelog — v2.1.0](https://www.kimi.com/code/docs/kimi-code-cli/changelog.html)
- **作者**: Moonshot AI
- **发布日期**: 2026-09-23
- **检索日期**: 2026-10-16
- **标签**: #KimiCode #CLI #全屏TUI #工作区安全 #符号链接 #默认安全

## 核心观点

CLI v2.1.0(09-23)是 Desktop GA 后 CLI 侧的第一个功能版本:实验性全屏 TUI、启动提速与内存下降、文件监听默认关闭。安全加固是重头戏——文件工具无法再经符号链接访问工作目录外的文件、项目本地配置仅在工作区受信任后生效、后台 git 操作不再执行仓库 git 配置中的命令。

但故事有反复:次日 v2.1.1"回退 2.1.0 中部分过于严格的防御性改动"并把文件监听恢复为默认开启,Desktop 1.0.4 同日同样恢复监听。同周 Desktop 1.0.3(09-23)还修复了"恶意网页可通过本地内嵌服务器执行任意命令"的安全漏洞。收紧—回摆的 24 小时,是编码 Agent 在默认安全与可用性之间真实工程张力的缩影。

## 关键发现 / 关键技术

### 1. 实验性全屏 TUI

- `/settings` 的 TUI mode 或 `tui.toml` 中 `tui_mode = "fullscreen"` 开启,重启生效
- transcript 独立滚动、支持鼠标选择;点击折叠块即可展开或收起
- 新增可点击的 "Jump to bottom" 指示器

### 2. 性能与默认行为变化

- 缩短 CLI 启动时间并降低内存占用,大项目首屏等待明显变短
- v2.1.0 将配置文件与工作区文件监听默认关闭(`[watch] enabled = true` 或 `KIMI_CODE_WATCH=1` 可再开启);v2.1.1(09-24)又恢复为默认开启
- AGENTS.md、skills、MCP 配置的热更新依赖该监听,默认值的反复直接影响工作流

### 3. 工作区安全加固(v2.1.0 → v2.1.1 部分回退)

- 文件工具无法再通过符号链接访问工作目录外的文件
- 项目本地配置仅在工作区受信任后生效
- 后台 git 操作不再执行仓库 git 配置(如 hooks)中的命令;拒绝解析结果为 home 目录或文件系统根目录的附加目录
- v2.1.1 明确"回退 2.1.0 中部分过于严格的防御性改动"——加固力度一日内回调

### 4. Desktop 同周三连更

| 版本 | 日期 | 要点 |
|------|------|------|
| 1.0.2 | 09-19 | 内置浏览器全面升级:Agent 浏览活动实时展示、按活动分组汇总来源 |
| 1.0.3 | 09-23 | 修复恶意网页可经本地内嵌服务器执行任意命令的漏洞;本地 HTML 可在内置浏览器直接打开验证 |
| 1.0.4 | 09-24 | 恢复默认监听工作区文件变化;修复信任工作区后仓库 Git hooks 不生效 |

### 5. 上下文行为细节

- v2.0.2(09-19):系统提示词不再假设当前工作目录就是项目根目录
- v2.0.1(09-18):移除系统提示词中"禁止访问工作目录以外所有文件"的一刀切规则,改用更精细的边界

## 实践意义

- **默认值即安全策略**:符号链接逃逸、仓库 git hooks、未信任配置三个攻击面收紧,与文件监听的回摆说明"默认安全"需要与可用性反复校准,而非一次到位
- **给编码 Agent 团队的清单**:symlink 逃逸与"仓库内配置在信任前生效"是通用攻击面,Kimi 的实现可直接作为威胁模型参照
- **本地服务边界**:Desktop 1.0.3 的内嵌服务器 RCE 修复提醒——桌面 Agent 的本地 HTTP 服务是常被忽视的攻击面

## 跨厂商对比

- 与 [ZCode 代码上传争议](../../glm/blog/glm-zcode-data-upload-incident.md) 对比:ZCode 因默认开启的云端索引付出 16% 股价回撤的代价后才移除功能;Kimi 同期主动收紧本地边界(symlink/信任/监听),一个事后补救、一个事前加固,共同坐实"默认开启=隐性数据外发"的行业教训
- 与 [Beyond Permission Prompts](../../anthropic/engineering/beyond-permission-prompts.md) 互补:Anthropic 主张用文件系统/网络沙箱在架构层收窄边界,Kimi v2.1.0 把同一原则落到符号链接、工作区信任、git hooks 三个具体攻击面,粒度更细但覆盖面更窄
- 与 [Kimi Code Desktop 正式发布](kimi-code-desktop.md) 关联:Desktop GA 后 CLI 与桌面端进入双轨周更,v2.1.x 与 Desktop 1.0.2-1.0.4 同周交错发布,CLI 独有迭代(全屏 TUI)保留终端重度用户

## 资源

- 发布:[Kimi Code CLI 变更记录](https://www.kimi.com/code/docs/kimi-code-cli/changelog.html)
- 汇总:[Kimi Code: What's New](https://www.kimi.com/code/docs/kimi-code/whats-new.html)
- 代码:[github.com/MoonshotAI/kimi-code](https://github.com/MoonshotAI/kimi-code)
