# DeepSeek-V4-Flash 正式版发布：后训练驱动的 Agent 能力跃升（DeepSeek-V4-Flash Official Release / V4-Flash-0731 Public Beta）

- **原文链接**: [DeepSeek API Change Log — 2026-07-31 V4-Flash Update](https://api-docs.deepseek.com/updates/)
- **作者**: DeepSeek（深度求索）
- **发布日期**: 2026-07-31
- **检索日期**: 2026-08-08
- **标签**: #DeepSeek #V4-Flash #Agent基准 #ResponsesAPI #Codex

## 核心观点

DeepSeek 将 DeepSeek-V4-Flash API 正式版（V4-Flash-0731）推入公测。API 调用方式不变，只需将模型名设为 `deepseek-v4-flash` 即可使用最新版本。Agent 能力显著增强，基准成绩全面超越 V4-Pro-Preview：Terminal Bench 2.1 达 82.7。模型架构与参数量与 V4-Flash-Preview 完全一致，仅通过重新后训练实现能力跃升。正式版原生支持 Responses API 格式并专门适配 Codex 生态。本次仅升级 Flash API，V4-Pro API 与 App/Web 端模型暂未变更。

## 关键发现 / 关键技术

### 1. 后训练驱动的 Agent 基准跃升
- 架构不变（284B 总参/13B 激活），仅重新后训练
- Terminal Bench 2.1：82.7；NL2Repo：54.2；Cybergym：76.7；DeepSWE：54.4
- Toolathlon verified：70.3；Agent Last Exam：25.2；Automation Bench（Public）：25.1
- DSBench-FullStack（内部全栈开发测试集）：68.7；DSBench-Hard（内部 Coding Agent 难题集）：59.6

### 2. 评测配置说明
- 公开基准中的 Code Agent 任务使用 DeepSeek Harness minimal mode（即将发布）作为框架
- 配置：max effort level、topp=0.95、temperature=1.0
- DSBench-FullStack 与 DSBench-Hard 为内部测试集

### 3. Responses API 与 Codex 原生适配
- V4-Flash 正式版原生支持 Responses API 格式
- 专门适配 Codex：可在 Codex CLI、ChatGPT 桌面端、VS Code 插件中直接调用
- 配置文档见 api-docs.deepseek.com/quick_start/agent_integrations/codex

## 实践意义

这是"后训练杠杆大于架构迭代"的又一证据：同架构仅靠重新后训练就在 Agent 基准上实现代际提升，说明当前阶段数据与训练流程的回报高于改架构。对使用 Codex/Claude Code 等工具链的开发者，V4-Flash 以极低定价成为可直接替换的后端选项——尤其 Terminal Bench 82.7 已接近编码 Agent 第一梯队。原生 Responses API 支持意味着无需协议转换即可接入 OpenAI 工具生态，降低了迁移成本。

## 跨厂商对比

- 与 [DeepSeek-V4 正式版 GA](deepseek-v4-ga.md) 衔接：GA 公告已预告 V4-Flash-0731 即将发布，本文是该发布的完整基准与配置细节，两者共同记录从预览到正式版的完整演进
- 与 [DeepSeek-V4 预览版](deepseek-v4.md) 衔接：同架构从预览到正式版的 Agent 能力跨度，体现后训练的杠杆效应
- 与 [V4 API 定价与峰谷计费](deepseek-v4-api-pricing.md) 衔接：Flash API 保持极低定价（缓存命中输入 0.02 元/百万 token、输出 2 元/百万 token）并引入峰谷定价（高峰翻倍）

## 资源
- 更新日志：[api-docs.deepseek.com/updates](https://api-docs.deepseek.com/updates/)
- Codex 适配文档：[api-docs.deepseek.com/quick_start/agent_integrations/codex](https://api-docs.deepseek.com/quick_start/agent_integrations/codex)
- 定价：[api-docs.deepseek.com/quick_start/pricing](https://api-docs.deepseek.com/quick_start/pricing)
