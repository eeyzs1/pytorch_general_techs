# GPT-5.6：前沿智能，随雄心扩展

- **原文链接**: [GPT-5.6: Frontier intelligence that scales with your ambition](https://openai.com/index/gpt-5-6/)
- **作者**: OpenAI
- **发布日期**: 2026-07-09
- **检索日期**: 2026-07-20
- **标签**: #GPT-5.6 #AgenticAI #Codex #KnowledgeWork #FrontierModel #安全

## 核心观点

GPT-5.6 是 OpenAI 最新旗舰模型系列，核心主张是"从每个 token 获得更多有用工作"——更强性能/美元比、按需最大能力。与 [GPT-5.5](introducing-gpt-5-5.md) 相比，GPT-5.6 在保持高效默认模式的同时，提供 `max`/`ultra` 推理 effort 档位，让用户按任务复杂度灵活选择智能水平。模型在 agentic coding、computer use、知识工作、网络安全和科学研究等长链路任务上实现全面跃升。

## 关键发现 / 关键技术

### 1. 高效默认 + 按需最大性能
- GPT-5.6 默认模式在保持接近 GPT-5.5 延迟的同时，智能水平显著提升
- `max` 和 `ultra` 推理 effort 档位允许用户为复杂任务支付更多 token 换取更高准确率
- 在 SWE-Bench Pro、Terminal-Bench 等编码基准上达到新 SOTA

### 2. 端到端知识工作
- 在 Word、Excel、PowerPoint、Chat 和 Cowork 等 Microsoft 365 场景中成为首选模型
- 能处理更混乱、多步骤、跨工具的任务，规划、调用工具、检查自身结果
- 支持从早期想法到 polished 演示文稿的完整工作流

### 3. 网络安全与科学前沿
- 在网络安全评估中展现更强漏洞发现和修复能力
- 在科学计算和推理任务上持续突破
- OpenAI 内部使用 GPT-5.6 加速自身研发

### 4. 安全与 Preparedness
- 发布前经过完整安全框架评估、外部 red team、网络安全和生物能力测试
- 引入差异化访问控制，高风险能力仅对受信任用户开放
- 配套发布 [GPT-5.6 System Card](https://deploymentsafety.openai.com/gpt-5-6)

## 实践意义

GPT-5.6 标志着前沿模型从"单一智能水平"向"可扩展智能"转变。对企业而言，这意味着：
- **成本优化**：简单任务用默认模式，复杂任务用 max/ultra 模式，避免过度支付
- **Agent 工业化**：更强 agentic 能力使 Codex 等 Agent 工具能处理更长时间、更复杂的任务
- **安全分层**：差异化访问模式为高能力 AI 的负责任部署提供范本

## 跨厂商对比

- 与 [GPT-5.5](introducing-gpt-5-5.md) 对比：GPT-5.6 在保持效率的同时大幅提升智能上限，特别是 max/ultra 档位的引入
- 与 [Claude Opus 4.6](../../anthropic/research/global-workspace.md) 对比：OpenAI 强调"可扩展智能"，Anthropic 强调"可解释性 + 对齐"
- 与 [Gemini 3.5](../../google/deepmind/gemini-3.5.md) 对比：Google 强调多模态原生，OpenAI 强调 agentic 能力和企业集成

## 资源

- 系统卡：[GPT-5.6 System Card](https://deploymentsafety.openai.com/gpt-5-6)
- Microsoft 365 集成：[GPT-5.6 in Microsoft 365 Copilot](https://openai.com/index/gpt-5-6-preferred-model-microsoft-365-copilot/)
