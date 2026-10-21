# Claude Code 上云实战：云会话田野指南（Claude Code in the cloud: a field guide to cloud sessions）

- **原文链接**: [Claude Code in the cloud: a field guide to cloud sessions](https://claude.dev/blog/claude-code-in-the-cloud/)
- **作者**: Addy Osmani
- **发布日期**: 2026-10-06
- **检索日期**: 2026-10-16
- **标签**: #ClaudeCode #云会话 #并行任务 #GitHub代理 #字段指南

## 核心观点

云会话让每个 Claude Code 任务跑在独立虚拟机上：新 VM + 仓库克隆到新分支 + 环境预配置，从 claude.ai/code、手机、桌面、终端（claude --cloud）或 Slack 发起，全程可在浏览器/手机跟踪，产出一条可直接转 PR 的分支。随 Pro/Max/Team/Enterprise 附带，云机器不另收费（消耗同一用量额度）。核心价值三件套：任务间物理隔离（不再抢工作树/端口）、不依赖本机在线（合盖/断网照跑）、以分支为交付物。

实测样本：三个会话 16 秒内启动，分别修 flaky 测试（连跑 40 次套件 0 失败）、重写 API 文档（逐端点 curl 验证）、改造结构化日志，87 秒全部完成。安全架构上 GitHub token 不进 VM（代理持有，VM 内只有只能推自己分支的短时凭证）、网络走可分级 allowlist 代理。

## 关键发现 / 关键技术

### 1. 本地 vs 云的决策表
- 留本地：本地数据库/VPN 服务/GPU/手机模拟器/桌面硬件、秒级视觉回路、零数据保留组织（云会话关闭）
- 上云：并行积压清理、需要重复证明的修复（套件跑 200 次）、计划-执行-收尾三段流、手机跟进、CI 失败与 review 评论自动修、定时例程、跑不完全信任的代码

### 2. 七类工作流
- 并行清积压：每个任务自包含"哪里坏了/做完什么样/怎么证明"，flaky 测试题要求连跑 30+ 次并被超额完成（40 次）
- 计划-执行：本地 plan mode 敲定方案提交后 `claude --cloud "执行 docs/migration-plan.md"`；`claude --teleport` 把云会话连同对话拉回终端收尾
- Auto-fix：GitHub App 监听 PR，自动修失败检查与 review 意见，歧义处会问人
- Routines（研究预览）：prompt+仓库+连接器+环境打包，按 cron/HTTP/GitHub 事件触发，免审批跑在 claude/ 分支
- 不可信代码：一次性 VM + 无 SSH 密钥 + 会话级 GitHub 凭证 + 网络可设 None

### 3. 环境与限制
- VM 规格 4 vCPU/16GB RAM/30GB 磁盘；setup script 以 root 预装并缓存快照（约 7 天重建）
- 前台命令默认 2 分钟超时（最多 10 分钟）后转后台最长 30 分钟——长测试在一条命令里很便宜
- 仓库级 .claude 配置随行走，个人 ~/.claude 不上传；空闲 VM 回收需及时 commit
- GitHub 接线的最大坑：登录授权 ≠ App 安装，私有库需后者装在所有者账号/组织上

## 实践意义

"每任务一机"把并行 agent 开发从 worktree 手工编排升级为平台原生能力，配额模型（多会话并行消耗倍速）是主要约束。最有价值的操作建议：给每个任务指定"证明完成的命令"（跑 N 次套件、逐端点 curl），让验证成本近乎为零地内嵌进执行；setup script + SessionStart hook 的分工（机器级 vs 项目级）值得标准化。对安全团队：跑第三方代码从"在我笔记本上"变为"在一次性沙箱里"，是最实际的攻击面收缩。

## 跨厂商对比

- 与 [Run Claude Code Sessions on Your Own Compute](run-claude-code-sessions-on-your-own-compute.md) 对比：自托管解决"数据不出网"，云会话解决"任务不互扰"——同为企业场景的隔离与便捷两端
- 与 [Getting Started with Claude Code Mods](getting-started-with-claude-code-mods.md) 同期：mods 深耕客户端体验，云会话把执行外移——Claude Code 平台化双翼
- 与 [Building Effective Agents](building-effective-agents.md) 互补：云会话是"单 agent 单任务多机并行"，与多 agent 编排正交——横向扩展与纵向复杂度两条路线

## 资源

- 论文：无
- 代码：无
- Demo：无
- 文档：https://code.claude.com/docs/en/claude-code-on-the-web
