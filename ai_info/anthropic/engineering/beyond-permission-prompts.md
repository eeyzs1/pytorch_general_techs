# Beyond Permission Prompts: Making Claude Code More Secure and Autonomous

- **原文链接**: [Beyond permission prompts: making Claude Code more secure and autonomous](https://www.anthropic.com/engineering/beyond-permission-prompts)
- **发布日期**: 2025-10-31
- **标签**: #安全 #沙箱 #Claude-Code #文件系统隔离 #网络隔离

## 核心观点

传统的权限提示（Permission Prompts）模式在 Agent 自主性需求增长时变得不可持续。Anthropic 为 Claude Code 设计了基于沙箱的安全架构，通过文件系统隔离和网络隔离实现更安全、更自主的 Agent 运行。安全是 [Claude Code Best Practices](claude-code-best-practices.md) 中"安全 YOLO 模式"的底层保障。

## 关键概念

### 权限提示的局限
- 频繁的权限提示打断工作流，降低效率
- 用户可能养成盲目批准的习惯（"点击疲劳"）
- 无法有效应对提示注入攻击。[Writing Effective Tools for AI Agents](writing-effective-tools-for-ai-agents.md) 也指出工具安全设计需要考虑提示注入防御

### 沙箱架构：双重隔离

#### 文件系统隔离
- 控制哪些文件/目录可被读写
- 防止被提示注入的 Claude 修改敏感系统文件
- 默认拒绝写访问，需显式允许路径
- 读取默认允许，可拒绝特定路径（如 `~/.ssh`）

#### 网络隔离
- 确保 Claude 只能连接到批准的服务器
- 防止被提示注入的 Claude 泄露敏感信息或下载恶意软件
- 通过 Unix 域名套接字连接到沙箱外运行的代理服务器
- 代理服务器强制执行域限制，处理新请求域的用户确认
- 支持自定义代理以强制执行任意出站流量规则

### 双重隔离的必要性
- 没有网络隔离：被入侵的 Agent 可泄露 SSH 密钥等敏感文件
- 没有文件系统隔离：被入侵的 Agent 可轻松逃逸沙箱获取网络访问
- **有效的沙箱需要文件系统和网络双重隔离**

### Git 操作代理
- 部署命令通过代理处理 git 操作，防止直接凭据访问
- 凭据保留在沙箱外

## 实践启示

- 安全是 Agent 自主性的前提——没有安全保证的自主性是危险的
- 沙箱设计需要同时考虑文件系统和网络两个维度
- 代理模式是平衡安全与功能的有效策略
- 开源了 sandbox-runtime 工具供社区使用
- [Building Agents with the Claude Agent SDK](building-agents-with-the-claude-agent-sdk.md) 继承了 Claude Code 的安全机制，将沙箱能力扩展到通用 Agent 开发
- [Desktop Extensions](desktop-extensions.md) 安装的 MCP 服务器同样需要沙箱保护——文件系统隔离确保 MCP 工具不越权访问
