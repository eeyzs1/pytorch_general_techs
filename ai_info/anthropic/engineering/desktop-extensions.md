# Desktop Extensions: One-click MCP Server Installation for Claude Desktop

- **原文链接**: [Desktop Extensions: One-click MCP server installation for Claude Desktop](https://www.anthropic.com/engineering/desktop-extensions)
- **发布日期**: 2025-06
- **标签**: #MCP #桌面扩展 #DXT #安装 #用户体验

## 核心观点

Desktop Extensions（.dxt 文件，后更名为 .mcpb）解决了 MCP 服务器安装的摩擦问题，将整个 MCP 服务器及其所有依赖打包为单一可安装包，实现一键安装——就像浏览器扩展一样简单。

## 关键概念

### 之前的痛点
安装 MCP 服务器需要：
- 手动编辑 JSON 配置文件
- 管理依赖（Node.js、Python 运行时等）
- 理解命令行配置
- 这些摩擦意味着 MCP 服务器对非技术用户基本不可用

### Desktop Extension 架构
- 本质是一个 ZIP 归档，包含本地 MCP 服务器和 `manifest.json`
- 通过 stdio 传输在用户机器上运行
- 打包所有依赖，可离线工作
- 不需要 OAuth

### 安装流程
1. 下载 .dxt 文件
2. 双击或拖放到 Claude Desktop 设置窗口
3. Claude 自动配置一切并提示输入所需凭据

### 开发流程
1. 创建 MCP 服务器
2. 编写 manifest.json（描述服务器能力）
3. 使用 `npx @anthropic-ai/dxt pack` 打包
4. 本地测试
5. 分发 .dxt 文件

### MCP 服务器三大组件
- **Resources**: 暴露数据源（文件、数据库、API 端点）
- **Tools**: 定义 Claude 可调用的可执行函数。工具的设计原则参见 [Writing Effective Tools for AI Agents](writing-effective-tools-for-ai-agents.md)
- **Prompts**: 预配置的提示模板

## 实践启示

- Desktop Extensions 大幅降低了 MCP 服务器的使用门槛
- 对非技术用户友好，类似浏览器扩展的体验
- 开发者可以轻松分发自己构建的 MCP 服务器
- 内置 Node.js 运行时，无需用户额外安装
- 安装后的 MCP 服务器可结合 [Code Execution with MCP](code-execution-with-mcp.md) 的代码执行范式，实现 98.7% 的 Token 减少
- [Equipping Agents for the Real World with Agent Skills](equipping-agents-for-the-real-world-with-agent-skills.md) 的 Skills 可通过 MCP 服务器分发，Desktop Extensions 降低了这一路径的门槛
- [Beyond Permission Prompts](beyond-permission-prompts.md) 的沙箱架构同样适用于通过 Desktop Extensions 安装的 MCP 服务器——安全是 Agent 自主性的前提
