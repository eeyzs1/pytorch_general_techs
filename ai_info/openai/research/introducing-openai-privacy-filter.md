# Introducing OpenAI Privacy Filter

- **原文链接**: [Introducing OpenAI Privacy Filter](https://openai.com/index/introducing-openai-privacy-filter/)
- **作者**: OpenAI
- **发布日期**: 2026-04-22
- **检索日期**: 2026-05-29
- **标签**: #隐私 #PII #开源权重 #本地运行 #安全基础设施

## 核心观点

OpenAI Privacy Filter 是一个用于检测和遮蔽文本中个人身份信息（PII）的 open-weight 模型。它面向高吞吐隐私工作流，支持本地运行和长上下文输入，适合训练、索引、日志、审查等 AI 工程流水线中的隐私保护。

## 关键设计

### 小模型，高隐私能力
- 目标是上下文感知的 PII 检测，而不是只匹配邮箱、电话等规则格式。
- 可在本地运行，避免未脱敏数据必须发送到外部服务器。
- 支持长输入，适合批量数据处理。

### 架构方式
- 使用双向 token-classification 模型和 span decoding。
- 不是逐 token 生成文本，而是一次性标注输入序列，再解码出需要处理的 span。
- 开发者可以根据场景调整召回率与精确率。

## 关键洞察

1. **AI 安全需要基础设施模型**：隐私过滤不是应用层小功能，而是训练和数据管线的公共组件。
2. **上下文感知优于纯规则匹配**：PII 是否敏感经常依赖周围语境。
3. **本地运行降低数据暴露面**：对企业和合规场景尤其重要。
4. **隐私过滤可以服务 Agent 日志治理**：Agent transcript、工具输出和长期记忆都需要脱敏能力。

## 相关文章

- [Running Codex Safely at OpenAI](running-codex-safely.md)
- [How We Monitor Internal Coding Agents for Misalignment](how-we-monitor-internal-coding-agents-for-misalignment.md)
