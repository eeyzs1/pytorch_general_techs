# 在自有基础设施上运行 Claude Code 会话

- **原文链接**: [Run Claude Code sessions on your own compute](https://claude.com/blog/run-claude-code-sessions-on-your-own-compute)
- **作者**: Anthropic
- **发布日期**: 2026-08-06
- **检索日期**: 2026-08-08
- **标签**: #企业部署 #自托管 #ClaudeCode #基础设施 #合规 #Runner

## 核心观点

Anthropic 推出公开测试版的 self-hosted environments（自托管环境），允许企业在自有基础设施上运行 Claude Code 会话。会话可从 web、mobile、desktop 或 routine 发起，运行在客户网络内部，紧邻内部服务、工具链和安全控制，而非 Anthropic 托管的基础设施上。仓库检出、构建产物、密钥和会话创建/修改的文件均留在客户自供基础设施上；仅对话内容（prompt、响应、工具结果）发送至 Anthropic 推理，会话记录存储以便跨终端续接。

该功能面向网络、工具或合规要求需要将 Agent 执行保留在自有基础设施上的团队。Anthropic 强调，对多数企业仍推荐托管方案以简化运维，自托管需配备工程团队负责设置和持续维护。

## 关键发现 / 关键技术

### 1. 自托管的三大驱动力

- **网络访问**：会话在客户网络内运行，可访问内部服务、数据库、注册表，无需暴露到公网
- **可定制性**：预装编译器、SDK、内部 CLI，每个会话即开即用
- **合规**：源代码和构建产物留在客户控制的基础设施上

### 2. Runner 架构：Fixed 与 On-demand 两种模式

客户部署一组 runner（长驻进程），用于拾取会话并为每个会话启动 Claude Code 进程。两种模式：
- **Fixed**：保持固定数量的 runner，会话分发到各 runner
- **On-demand**：orchestrator 监听排队会话，按需启动 runner，工作完成后停止，容量随需求伸缩

每个 runner 可服务多个会话，但每个会话运行在独立 checkout 中，开发者间和账户间工作隔离。所有支持终端的会话路由到同一环境，一次配置即可在所有发起处生效。

### 3. 与 Remote Control 的区别

self-hosted environments 不同于 Remote Control：后者让开发者从手机/浏览器继续在自己机器上运行的会话，会话随该机器停止而结束且绑定运行 `claude` 的用户；前者在平台团队运营的共享基础设施上运行会话，可供任意用户使用。

## 实践意义

自托管环境填补了 Claude Code 企业部署中"数据驻留"的关键缺口——对金融、医疗、政府等强合规行业，源代码和密钥不出基础设施是硬性要求。该功能与 inference hooks（DLP 检查）和 auto mode（权限决策）配合，构成了 Claude Enterprise 的完整安全栈：自托管管数据驻留，inference hooks 管内容检查，auto mode 管操作决策。当前不支持 ZDR 组织，Team 和 Enterprise 计划可用，默认关闭。

## 跨厂商对比

- 与 [Beyond Permission Prompts](beyond-permission-prompts.md) 互补：后者通过沙箱（文件系统隔离 + 网络隔离）在单机层面保障 Agent 安全，self-hosted environments 则在网络和基础设施层面提供企业级数据驻留控制，两者分别解决"Agent 在机器内能做什么"和"Agent 在哪里运行"的问题
- 与 [Claude Code Best Practices](claude-code-best-practices.md) 对比：最佳实践关注 prompt 工程和会话管理，自托管环境关注部署架构，是企业规模化采纳 Claude Code 的基础设施前提

## 资源

- 论文：N/A
- 代码：N/A
- Demo：https://code.claude.com/docs/en/self-hosted-environments
