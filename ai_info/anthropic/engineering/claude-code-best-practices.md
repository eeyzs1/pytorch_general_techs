# Claude Code: Best Practices for Agentic Coding

- **原文链接**: [Claude Code: Best practices for agentic coding](https://www.anthropic.com/engineering/claude-code-best-practices)
- **作者**: Boris Cherny 等
- **发布日期**: 2025-04-18
- **标签**: #Claude-Code #最佳实践 #CLAUDE-md #编码工作流 #自动化

## 核心观点

Claude Code 是一个命令行式的 Agent 编码工具——有意设计为低层且不带偏见，提供接近原始模型访问的能力。文章概述了六个领域的最佳实践：自定义设置、工具配置、常见工作流、优化策略、无头自动化和多 Claude 协作。

## 关键概念

### CLAUDE.md 模式
最重要的配置机制——一个在每次对话开始时自动拉入上下文的 Markdown 文件。CLAUDE.md 是 [Effective Context Engineering for AI Agents](effective-context-engineering-for-ai-agents.md) 中上下文工程理念的核心实践——通过预加载关键信息减少即时检索的需求。

推荐内容：
- Bash 命令（构建、测试、类型检查）
- 核心文件/工具
- 代码风格
- 测试指令
- 仓库规范
- 开发环境设置

放置选项：
- 仓库根目录（最常见，提交到 git）
- 父目录（monorepo）
- 子目录（按需加载）
- 主文件夹（`~/.claude/CLAUDE.md`，所有会话生效）

使用 "IMPORTANT" 或 "YOU MUST" 等强调词提高遵守率。CLAUDE.md 的渐进式扩展参见 [Equipping Agents for the Real World with Agent Skills](equipping-agents-for-the-real-world-with-agent-skills.md)，后者将类似理念发展为分层加载的 SKILL.md 模式。

### 自定义斜杠命令
存储为 `.claude/commands/` 中的 Markdown 文件，支持 `$ARGUMENTS` 占位符。

### 工作流模式

1. **探索 → 计划 → 编码 → 提交**: 先阅读文件（告诉 Claude 不要写代码），用 Extended Thinking 规划，实现，提交
2. **TDD**: 写测试 → 确认失败 → 提交测试 → 写实现 → 提交代码
3. **视觉迭代**: 给 Claude 截图能力（Puppeteer MCP），提供模型，迭代直到匹配
4. **安全 YOLO 模式**: 在无互联网容器中使用 `--dangerously-skip-permissions`。安全架构的详细设计参见 [Beyond Permission Prompts](beyond-permission-prompts.md)

### 无头自动化

```bash
# 非交互式提示执行
claude -p "<prompt>" --output-format stream-json

# 扇出模式：批量操作
for file in $(cat files.txt); do
  claude -p "Migrate $file from React to Vue." --allowedTools Edit Bash(git commit:*)
done

# 管道模式
claude -p "<your prompt>" --json | your_command
```

### 多 Claude 工作流
- **编写者 + 审阅者模式**: 分离终端和上下文
- 多个 git checkout 用于并行任务
- git worktrees 用于轻量级并行分支

## 实践建议

- 告诉 Claude "think"、"think hard"、"think harder"、"ultrathink" 触发不同深度的 Extended Thinking，与 [The Think Tool](the-think-tool.md) 的执行中思考互补
- 优先运行单个测试而非整个测试套件以提高性能
- 完成一系列代码更改后务必运行类型检查
- 使用 MCP 集成外部服务（Slack、GitHub、Google Drive 等）
- [Building Agents with the Claude Agent SDK](building-agents-with-the-claude-agent-sdk.md) 提供了 Claude Code 的编程接口，将编码能力扩展到通用数字工作
