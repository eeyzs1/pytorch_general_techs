# Writing Effective Tools for AI Agents — Using AI Agents

- **原文链接**: [Writing effective tools for AI agents—using AI agents](https://www.anthropic.com/engineering/writing-tools-for-agents)
- **作者**: Ken Aizawa 及跨团队贡献者
- **发布日期**: 2025-10-20
- **标签**: #工具设计 #评估驱动 #命名空间 #Token效率 #Agent改进工具

## 核心观点

工具是一种"新型软件"——确定性系统与非确定性 Agent 之间的契约。文章描述了 Anthropic 的评估驱动方法论：**原型 → 评估 → 分析 → 优化 → 重复**。关键洞察是：即使对工具描述的微小优化也能带来显著的性能提升。Claude Sonnet 3.5 仅通过精确的工具描述优化就达到了 SWE-bench Verified 的最先进性能。这是 [Building Effective Agents](building-effective-agents.md) 中 ACI（Agent-Computer Interface）设计的系统化方法论。

## 五大工具设计原则

### 1. 选择正确的工具
- 构建少量、深思熟虑的工具，针对高影响工作流
- **合并相关操作**:
  - ❌ `list_users` + `list_events` + `create_event`
  - ✅ `schedule_event`（查找可用时间并安排）
  - ❌ `read_logs`
  - ✅ `search_logs`（只返回相关行及上下文）
  - ❌ `get_customer_by_id` + `list_transactions` + `list_notes`
  - ✅ `get_customer_context`（一次编译所有相关信息）

### 2. 命名空间工具
- 在公共前缀下分组相关工具（如 `asana_search`、`jira_search`、`asana_projects_search`）
- 前缀 vs 后缀命名空间对工具使用评估有非平凡影响——两种方法都应测试

### 3. 返回有意义的上下文
- 优先考虑上下文相关性而非灵活性
- 使用人类可读字段（`name`、`image_url`、`file_type`）而非加密标识符（`uuid`、`256px_image_url`、`mime_type`）
- 将 UUID 解析为语义上有意义的语言

### 4. 优化 Token 效率
- 实现分页、范围选择、过滤和截断，带合理默认值
- Claude Code 默认将工具响应限制在 25,000 token
- 暴露 `response_format` 枚举（concise/detailed）让 Agent 控制详细程度
- "detailed" 响应约 206 token vs "concise" 约 72 token（约 3 倍差异）。[Effective Context Engineering for AI Agents](effective-context-engineering-for-ai-agents.md) 强调每个 token 都在消耗注意力预算，Token 效率是上下文工程的核心

### 5. 提示工程化工具描述
- 像对新员工描述一样描述工具
- 将隐式知识显式化
- 避免歧义
- 参数命名无歧义（`user_id` 而非 `user`）

## 用 Agent 改进工具

- 将评估转录连接并粘贴到 Claude Code 中
- Claude 擅长同时分析转录和重构工具
- **工具测试 Agent**: 反复尝试使用有缺陷的工具，然后重写其描述，使未来 Agent 的任务完成时间降低 **40%**。[How We Built Our Multi-Agent Research System](how-we-built-our-multi-agent-research-system.md) 中的第 5 条原则"让 Agent 自我改进"正是这一实践的体现

## 评估设计

- 生成受真实世界使用启发的任务
- 每个任务配对可验证结果
- 使用简单 Agent 循环（while 循环包装交替的 LLM API 和工具调用）
- 指示评估 Agent 在工具调用前输出推理/反馈以触发 CoT
- 收集指标：准确性、总运行时间、工具调用次数、Token 消耗、工具错误

## 实践启示

- [Raising the Bar on SWE-bench Verified](raising-the-bar-on-swe-bench-verified.md) 是工具描述优化的实战案例——仅通过精确描述优化就达到 SOTA
- [Advanced Tool Use](advanced-tool-use.md) 在此基础上引入了 Tool Search Tool、PTC 和 Tool Use Examples，进一步优化工具使用的 Token 效率和准确率
