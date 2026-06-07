# GPT-5.5 System Card

- **原文链接**: [GPT-5.5 System Card](https://openai.com/index/gpt-5-5-system-card/)
- **作者**: OpenAI
- **发布日期**: 2026-04-23
- **检索日期**: 2026-06-07
- **标签**: #GPT-5.5 #SystemCard #安全 #PreparednessFramework #并行推理

## 核心观点

GPT-5.5 是 OpenAI 首个完全重新训练的基座模型（自 4.5 时代以来），专为复杂真实世界工作设计——编码、在线研究、信息分析、文档和电子表格创建、跨工具操作。System Card 详细披露了安全性评估、Preparedness Framework 结果和并行测试时计算（GPT-5.5 Pro）的架构创新。

## 关键更新

### 模型架构
- GPT-5.5 是首个完全重新训练的基座模型（内部代号 "Spud"）
- GPT-5.5 Pro 使用同一底层模型，但启用了并行测试时计算（parallel test-time compute）
- 并行推理允许模型生成多条推理路径并选择最佳输出，类似集成方法但在架构层面实现

### 安全评估
- 完整的预部署安全评估和 Preparedness Framework
- 近 200 个早期访问合作伙伴反馈
- 覆盖：违禁内容、视觉安全、Jailbreak、提示注入、健康、幻觉、对齐、偏见
- CoT 可监控性和可控性评估
- 生物/化学和网络安全能力评估（CTF、CVE-Bench、VulnLMP 等）
- AI 自改进评估（Monorepo-Bench、MLE-Bench）

### 产品分层
- GPT-5.5：标准版，面向成本敏感型任务
- GPT-5.5 Pro：并行测试时计算，面向高价值任务

## 关键洞察

1. 并行测试时计算是推理效率的突破——允许在不增大模型的情况下提供差异化质量
2. 产品分层策略（标准 vs Pro）为 OpenAI 创造了新的定价灵活性
3. System Card 与模型发布同步公开，将安全文档作为产品发布的一部分
4. Preparedness Framework 覆盖生物、网络、AI 自改进三大风险域

## 相关文章

- [Introducing GPT-5.5](introducing-gpt-5-5.md)
- [GPT-5.5 Instant System Card](gpt-5-5-instant-system-card.md)
- [Introducing GPT-5.3-Codex](introducing-gpt-5-3-codex.md)