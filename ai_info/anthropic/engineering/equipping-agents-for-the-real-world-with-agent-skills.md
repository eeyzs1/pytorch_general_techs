# Equipping Agents for the Real World with Agent Skills

- **原文链接**: [Equipping agents for the real world with Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)
- **作者**: Barry Zhang, Keith Lazuka, Mahesh Murag
- **发布日期**: 2025-10-16（2025-12-18 更新：作为开放标准发布于 agentskills.io）
- **标签**: #Agent-Skills #SKILL-md #渐进式披露 #可组合性 #开放标准

## 核心观点

Agent Skills 是组织化的指令、脚本和资源文件夹，Agent 可以动态发现和加载。核心设计原则是**渐进式披露（Progressive Disclosure）**：Skills 分层暴露信息，使上下文窗口保持精简。渐进式披露是 [Effective Context Engineering for AI Agents](effective-context-engineering-for-ai-agents.md) 中即时上下文检索策略的具体实现——只加载当前需要的上下文。

## 关键概念

### 渐进式披露（三个层级）

| 层级 | 加载内容 | 时机 |
|------|---------|------|
| 1 | 名称 + 描述元数据 | Agent 启动时（始终在系统提示中） |
| 2 | 完整 SKILL.md 正文 | Claude 判断相关性时按需加载 |
| 3+ | 额外引用文件 | 仅在特定子任务需要时 |

这使得 Skill 绑定的上下文量实际上是**无上限的**。

### SKILL.md 结构
- 必须以包含 `name` 和 `description` 的 YAML frontmatter 开头
- 正文包含指令、对额外文件的引用，以及可选的可执行脚本
- SKILL.md 是 [Claude Code Best Practices](claude-code-best-practices.md) 中 CLAUDE.md 的演进——从固定预加载到分层按需加载

### 上下文窗口序列
1. 系统提示 + Skill 元数据 + 用户消息
2. Claude 通过 Bash 工具读取 SKILL.md 触发 Skill
3. Claude 按需读取引用文件
4. Claude 使用加载的 Skill 指令继续任务

### 可执行代码
- Skills 可以包含用于确定性操作的可执行代码
- 预编写的 Python 或 Bash 脚本无需将脚本或数据加载到上下文即可运行
- 对排序、PDF 解析、数据转换等操作特别有价值——代码比 token 生成更可靠
- [Code Execution with MCP](code-execution-with-mcp.md) 展示了类似的思路——通过代码执行避免将中间结果加载到上下文

## 构建 Skills 的指南

1. **从评估开始**: 在代表性任务上运行 Agent，观察差距，增量构建 Skills。[Demystifying Evals for AI Agents](demystifying-evals-for-ai-agents.md) 提供了完整的评估框架
2. **为规模构建结构**: 将庞大的 SKILL.md 拆分为单独的引用文件；将互斥的上下文分开
3. **从 Claude 的视角思考**: 监控实际使用；观察意外轨迹；特别注意名称和描述。[Writing Effective Tools for AI Agents](writing-effective-tools-for-ai-agents.md) 同样强调名称和描述对 Agent 行为的关键影响
4. **与 Claude 迭代**: 让 Claude 将成功方法和常见错误捕获为可重用上下文
5. **安全**: 仅从可信来源安装 Skills；审计代码依赖和捆绑资源；注意连接到不可信外部网络源的指令

## 实践启示

- Skills 使通用 Agent 可以通过组合获得领域专业知识
- 渐进式披露确保上下文窗口不被不相关信息淹没
- [Building Agents with the Claude Agent SDK](building-agents-with-the-claude-agent-sdk.md) 集成了 Skills 机制，SDK 中可直接使用
