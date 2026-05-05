# Equipping the Responses API with a Computer Environment

- **原文链接**: [Equipping the Responses API with a Computer Environment](https://openai.com/index/equip-responses-api-computer-environment/)
- **发布日期**: 2026-03
- **标签**: #ResponsesAPI #Shell工具 #容器工作区 #AgentSkills #上下文压缩 #Agent基础设施

## 核心观点

OpenAI 为 Responses API 配备了完整的计算机环境，让模型能从"文本生成"升级为能在真实环境中执行任务的 Agent。核心组件包括 Shell 工具、托管容器工作区、服务端上下文压缩和 Agent Skills 标准，构建了从模型到 Agent 的完整基础设施层。

## 关键架构

### Shell 工具：模型的"手"
- 模型通过命令行与计算机交互，可使用 grep、curl、awk 等标准 Unix 工具
- 相比仅支持 Python 的 Code Interpreter，Shell 工具支持 Go、Java、NodeJS 等任意语言
- 模型只"提议" Shell 命令，不直接执行——由 Responses API 服务在容器中执行
- 支持一个步骤中提议多个命令并行执行，搜索结果、数据获取、中间验证可并发
- 输出长度可控：模型指定每个命令的输出上限，保留开头和结尾，省略中间冗余

### 执行循环
```
用户请求 → Responses API 组装上下文 → 模型决定下一步动作
  → 若选择 Shell 执行 → 返回命令给 API → 转发到容器运行时
  → 流式回传 Shell 输出 → 作为下一轮上下文 → 循环至任务完成
```
- Responses API 维护与容器的流式连接，实时中继输出让模型决定等待/继续/完成
- 多命令并发执行通过独立容器会话实现，API 多路复用输出流

### 服务端上下文压缩（Compaction）
- 长时间 Agent 运行中自动压缩上下文窗口
- 模型被训练为分析历史对话状态，生成加密的 token 高效压缩表示
- 压缩后上下文窗口 = 压缩项 + 高价值早期内容
- 支持服务端自动压缩（配置阈值）或独立 `/compact` 端点
- Codex 帮助构建了压缩系统，同时作为早期使用者——实现了自举改进

### 容器工作区
- **文件系统**: 提供容器和文件 API，让模型通过 Shell 有选择地打开、解析、转换文件，而非将所有输入塞入 prompt
- **数据库**: 建议将结构化数据存入 SQLite 并让模型描述表结构后按需查询，而非粘贴整表到 prompt——更快、更便宜、可扩展
- **网络访问**: 通过边车出口代理实施网络策略，域名范围密钥注入（模型只看到占位符），降低凭证泄露风险

### Agent Skills
- Skill = SKILL.md（元数据+指令）+ 配套资源（API spec、UI assets）的文件夹
- 容器提供持久文件和执行上下文，Shell 提供执行接口
- 模型用 `ls`/`cat` 发现 Skill 文件，解释指令，运行脚本——同一 Agent 循环
- 平台提供 API 管理 Skills：上传、存储为版本化包、按 ID 检索

## 完整工作流示例

```
一条 prompt → 发现合适 Skill → 获取数据 → 转换为本地结构化状态
  → 高效查询 → 生成持久化产物（如从实时数据创建电子表格）
```

## 对比 Anthropic

| 维度 | OpenAI | Anthropic |
|------|--------|-----------|
| Agent 执行环境 | Responses API + 托管容器 | Claude Managed Agents |
| 工具执行 | Shell 工具（完整命令行） | MCP + 内置工具 |
| 上下文管理 | 服务端 Compaction | Claude Code 上下文管理 |
| Skills | Agent Skills 开放标准 | Claude Skills / CLAUDE.md |
| 编排方式 | Responses API 内置循环 | Claude Agent SDK / Harness |

## 相关文章

- [New Tools and Features in the Responses API](new-tools-and-features-in-the-responses-api.md) — Responses API 早期版本
- [The Next Evolution of the Agents SDK](the-next-evolution-of-the-agents-sdk.md) — Agents SDK 更新
- [Introducing the Codex App](introducing-the-codex-app.md) — Codex App 发布
- [Harness Engineering](harness-engineering.md) — Harness 方法论
