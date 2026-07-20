# DeepSeek-V4 API 定价与峰谷计费：旧模型名 7 月 24 日废弃（DeepSeek-V4 API Pricing & Peak-Valley Billing）

- **原文链接**: [Models & Pricing — DeepSeek API Docs](https://api-docs.deepseek.com/quick_start/pricing)
- **作者**: DeepSeek（深度求索）
- **发布日期**: 2026-06-29
- **检索日期**: 2026-07-20
- **标签**: #DeepSeek #API定价 #峰谷计费 #模型迁移 #成本工程

## 核心观点

DeepSeek 于 2026 年 6 月 29 日向 API 用户发送邮件，官宣 V4 正式版 7 月中旬上线并同步调整定价：首次在大模型 API 中引入电力行业式的"峰谷计费"——高峰时段（每日 9:00-12:00、14:00-18:00）API 价格为平时 2 倍。同时旧模型名 `deepseek-chat` / `deepseek-reasoner` 将于 2026-07-24 15:59 UTC 废弃，分别映射到 `deepseek-v4-flash` 的非思考 / 思考模式。这是"价格屠夫"第一次给算力装上计价器。

## 关键发现 / 关键技术

### 1. 官方定价（美元，每百万 token，API 文档确认）

| 模型 | 输入（缓存命中） | 输入（缓存未命中） | 输出 |
|------|------------------|--------------------|------|
| deepseek-v4-flash | $0.0028 | $0.14 | $0.28 |
| deepseek-v4-pro | $0.003625 | $0.435 | $0.87 |

对应人民币定价（官方邮件）：V4-Flash 平时输入 ¥1 / 输出 ¥2，高峰翻倍；V4-Pro 平时输入 ¥3 / 输出 ¥6，高峰翻倍。

### 2. 峰谷计费机制

- **高峰时段**：每日 9:00-12:00、14:00-18:00，全部价格 ×2
- **设计意图**：引导批量任务、离线评测、数据生成移至低谷时段；实时 Agent 为延迟付费
- **缓存命中价格不动量级**：V4-Flash 缓存命中输入 $0.0028/百万 token，依然是全场最低档位之一

### 3. 旧模型废弃迁移

- `deepseek-chat` → `deepseek-v4-flash`（非思考模式）
- `deepseek-reasoner` → `deepseek-v4-flash`（思考模式，默认开启）
- 废弃时间：2026-07-24 15:59 UTC
- API 同时兼容 OpenAI 与 Anthropic 双格式，Anthropic 格式 base_url 为 `https://api.deepseek.com/anthropic`

### 4. 与竞品价格对比

- V4-Pro 输出 $0.87/百万 token vs Anthropic Fable 5 输出 $50/百万 token——约 1/57
- 36kr 报道：V4-Pro-Max 在 SWE-bench Verified 距 Claude Opus 4.6 Max 仅 0.2 个百分点，价格约 1/7

## 实践意义

- **成本工程成为显学**：Agent 团队需要把任务按"实时 / 离线"分类调度，峰谷价差 2 倍足以改变批处理架构
- **缓存策略价值放大**：缓存命中与未命中价差 50 倍（flash），prompt 前缀稳定化、会话复用的 ROI 极高
- **迁移窗口紧迫**：7 月 24 日后旧模型名失效，所有硬编码 `deepseek-chat` / `deepseek-reasoner` 的系统必须在此之前完成迁移
- **Agent 工具链利好**：官方文档明确 Claude Code、GitHub Copilot、OpenCode 等 Agent 工具可直接以 DeepSeek 为后端模型

## 跨厂商对比

- 与 [Kimi K2.6](../../kimi/blog/kimi-k2-6.md) 对比：Kimi 以开源编码 Agent 的"能力"竞争，DeepSeek 以"Opus 级能力 + 1/7 价格"竞争——开源阵营对闭源形成钳形攻势
- 与 [Beyond Rate Limits](../../openai/research/beyond-rate-limits.md) 对比：OpenAI 用 rate limit 分层管理算力供需，DeepSeek 直接用价格信号（峰谷计费）调节——两种算力治理思路
- 与 [Kimi K3](../../kimi/blog/kimi-k3.md) 互补：K3 开源权重供自部署，V4 低价 API 供直接调用——"自部署 vs 低价 API"构成开源模型的两种商业化路径

## 资源

- 定价页：[Models & Pricing](https://api-docs.deepseek.com/quick_start/pricing)
- 思考模式：[Thinking Mode](https://api-docs.deepseek.com/guides/thinking_mode)
- Agent 接入：[Agent Integrations Guide](https://api-docs.deepseek.com/quick_start/agent_integrations/claude_code)
