# Code Execution with MCP: Building More Efficient AI Agents

- **原文链接**: [Code execution with MCP: Building more efficient AI agents](https://www.anthropic.com/engineering/code-execution-with-mcp)
- **作者**: Adam Jones, Conor Kelly
- **发布日期**: 2025-11-04
- **标签**: #MCP #代码执行 #Token优化 #文件系统 #隐私保护

## 核心观点

随着 MCP 采用规模扩大到数千个连接的服务器，工具定义和中间结果压垮了上下文窗口。解决方案：**将 MCP 服务器作为文件系统上的代码 API 而非直接工具调用呈现，让 Agent 编写代码与工具交互**。这将 Token 使用从 150,000 减少到 2,000——**98.7% 的减少**。Cloudflare 独立确认了这些发现，称之为"Code Mode"。这是 [Effective Context Engineering for AI Agents](effective-context-engineering-for-ai-agents.md) 中 Token 优化策略的极致体现。

## 关键概念

### 文件系统方法
MCP 服务器以文件系统目录结构呈现：

```
servers/
├── google-drive/
│   ├── getDocument.ts
│   └── index.ts
├── salesforce/
│   ├── updateRecord.ts
│   └── index.ts
└── ...
```

Agent 通过探索文件系统（列出 `./servers/`）发现工具，只读取需要的定义。

### 关键对比
传统方式 vs 代码执行方式：

**传统方式**: Google Drive → Salesforce 工作流需要将完整会议记录两次通过模型上下文

**代码执行方式**: 会议记录在代码中流转，**从不进入模型上下文**：

```typescript
import * as gdrive from './servers/google-drive';
import * as salesforce from './servers/salesforce';

const transcript = (await gdrive.getDocument({ documentId: 'abc123' })).content;
await salesforce.updateRecord({
  objectType: 'SalesMeeting',
  recordId: '00Q5f000001abcXYZ',
  data: { Notes: transcript }
});
```

### 隐私保护操作
- 中间结果留在执行环境中
- MCP 客户端可以拦截并标记化 PII（email → `[EMAIL_1]`，phone → `[PHONE_1]`）
- 真实数据在工具间流动但**从不通过模型**

### 状态持久化和可重用 Skills
- Agent 可以将工作代码保存为 `./skills/` 目录中的可重用函数
- 添加 SKILL.md 文件创建结构化的 Skill 引用
- 与 [Equipping Agents for the Real World with Agent Skills](equipping-agents-for-the-real-world-with-agent-skills.md) 的 Skills 模式天然集成——Skills 的可执行代码可通过代码执行范式运行

## 实践启示

- 代码执行范式是 MCP 规模化的关键
- 对于数据密集型工作流，Token 节省可达 98.7%
- 隐私保护是额外收益——敏感数据可以不经过模型
- [Advanced Tool Use](advanced-tool-use.md) 中的 PTC（程序化工具调用）是代码执行的 API 级实现——两者都通过代码编排避免中间结果进入上下文
- [Writing Effective Tools for AI Agents](writing-effective-tools-for-ai-agents.md) 的传统工具设计优化是代码执行的前置步骤——先优化工具本身，再用代码执行进一步优化
- [Desktop Extensions](desktop-extensions.md) 是 MCP 服务器的安装方式，安装后的服务器可直接用于代码执行范式
