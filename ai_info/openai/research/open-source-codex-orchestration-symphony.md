# An Open-Source Spec for Orchestration: Symphony

- **原文链接**: [An open-source spec for orchestration: Symphony](https://openai.com/index/open-source-codex-orchestration-symphony/)
- **作者**: Alex Kotliarskyi, Victor Zhu, Zach Brock
- **发布日期**: 2026-04-27
- **检索日期**: 2026-06-04
- **标签**: #Symphony #Codex #编排 #Agent #开源 #SPEC-md #Harness工程

## 核心观点

OpenAI 团队发布 Symphony——一个开源 Agent 编排规范，将 Linear 等项目管理工具变成编码 Agent 的控制平面。Symphony 仅是一个 SPEC.md 文件，定义问题描述和预期解决方案。该团队部分实现了 500% 的 PR 交付增长。

## 从交互式 Agent 到编排式 Agent

### 问题
- 工程师管理多个 Codex 会话时出现上下文切换瓶颈
- 大多数人只能舒适管理 3-5 个会话，超过后生产力下降
- 人类注意力成为系统瓶颈

### 解决方案
- 将任务追踪器（Linear）作为控制平面
- 每个开放 Issue 映射到一个专用的 Agent 工作空间
- Symphony 持续监控任务看板，确保每个活跃任务有 Agent 运行
- Agent 崩溃或停滞时自动重启；新工作出现时自动拾取

## 关键设计

### 状态机工作流
- 基于 Linear 状态的任务状态机
- 任务可以产生多个 PR、跨仓库工作
- Agent 可以创建子任务（DAG）和依赖关系

### SPEC.md 即规范
- Symphony 只是一个 SPEC.md 文件
- 定义了问题、预期解决方案、目标和边界
- 语言无关，可多种实现

### 架构分层
- Policy Layer（WORKFLOW.md）
- Configuration Layer（类型化配置）
- Coordination Layer（编排器）
- Execution Layer（工作空间 + Agent 子进程）
- Integration Layer（Linear 适配器）
- Observability Layer（日志 + 状态展示）

## 工作方式转变

- 工程师不再监督 Codex 会话，而是管理任务
- PM 和设计师可以直接在 Linear 中创建任务
- Agent 处理 CI、rebase、冲突解决、flake 重试
- 模糊探索类任务仍由工程师直接交互完成

## 关键洞察

1. 从"管理 Agent 会话"到"管理任务"的范式转变解放了工程师注意力
2. SPEC.md 作为 Agent 编排规范是一种轻量级、可移植的方法
3. Agent 编排降低了对代码变更的感知成本，鼓励探索和实验
4. 给 Agent 目标而非严格的状态转换，类似给下属分配目标而非微观管理

## 相关文章

- [Harness Engineering](harness-engineering.md)
- [Building Self-Improving Tax Agents with Codex](building-self-improving-tax-agents-with-codex.md)
- [Building Effective Agents](../../anthropic/engineering/building-effective-agents.md)