# DeepSeek-V4-Pro GA 与 API 调价：最高涨幅 1100%，峰谷分时定价落地（DeepSeek-V4-Pro GA Release & API Pricing Update）

- **原文链接**: [DeepSeek-V4-Pro GA Release](https://api-docs.deepseek.com/news/news260813)
- **作者**: DeepSeek（深度求索）
- **发布日期**: 2026-08-13
- **检索日期**: 2026-08-21
- **标签**: #DeepSeek #API定价 #峰谷计费 #成本工程 #V4 #价格调整

## 核心观点

DeepSeek 于 2026 年 8 月 13 日宣布 V4-Pro 正式 GA，并同步发布 API 调价公告：新价格自 8 月 16 日 16:00 UTC 起生效（北京时间 8 月 17 日凌晨），部分模型涨幅最高达 1100%，峰谷分时计费全面落地——低峰时段价格为高峰的 50%。这是自 6 月预告调价以来的正式生效节点，标志着 DeepSeek 从"价格屠夫"转向"商业化平衡"。

调价背景包括：V4/V4-Pro/V4-Flash 系列训练与推理成本上升、算力需求随 Agent 场景增长、以及"以低价换规模"阶段向"合理定价换可持续"阶段的过渡。V4-Pro GA 本身带来重大 Agent 升级：推理 effort 三档可调（low/high/max）、原生 Responses API 支持与 Codex 一键配置。

## 关键发现 / 关键技术

### 1. V4-Pro GA 与 Agent 升级
- 重大 Agent 能力提升，生产环境收益显著
- 推理 effort 三档可调：low（简单任务）、high（日常 Agent 工作流）、max（复杂任务）
- 原生 OpenAI Responses API 支持，为 Codex 优化、一键配置
- App/Web "Expert Mode" 可用，模型名称不变

### 2. 涨幅与结构
- 部分模型最高涨幅达 1100%（约 12 倍）
- 峰谷分时计费：低峰时段价格 = 高峰时段的 50%
- 覆盖 V4 全系列（V4、V4-Flash、V4-Pro 等）

### 2. 峰谷定价机制
- 高峰期（如白天业务时段）按高价计费
- 低峰期（如夜间）价格为高峰一半
- 鼓励开发者错峰调用，优化算力利用率

### 3. 战略转向
- 从"极致低价"转向"成本 + 价值"定价
- 反映训练与推理成本的真实结构
- 行业普遍认为国产大模型"集体变贵"趋势开始

### 4. 市场影响
- 引发"国产大模型涨价潮"讨论
- 与 GLM Coding Plan 改版（积分制涨价）、Kimi 商业化并行
- 开发者成本模型需要重新评估

## 实践意义

DeepSeek 调价是国产大模型商业化分水岭：低价红利期结束，开发者与企业在模型选型时必须把"价格结构"（含峰谷时段）纳入架构设计。峰谷计费对批处理任务尤其重要——把非实时任务调度到低峰时段可显著降本。这也验证了算力成本终究要传导到 API 价格，纯烧钱换市场不可持续。

## 跨厂商对比

- 与 [DeepSeek-V4 API 定价与峰谷计费](../../deepseek/news/deepseek-v4-api-pricing.md) 互补：该文是定价规则介绍，本文是调价正式生效与涨幅落地
- 与 [GLM Coding Plan 套餐改版](../../glm/blog/glm-coding-plan-pricing-revision.md) 对比：GLM 从 prompt 计数改 token 积分制并涨价，DeepSeek 采用峰谷分时，国内厂商计费模型集体重构
- 与 [OpenAI GPT-5.6 价格性能前沿](../../openai/research/advancing-the-price-performance-frontier-with-gpt-5-6.md) 对比：OpenAI 通过效率提升降低单位成本，DeepSeek 通过价格结构优化回收成本，两种成本工程路线
- 与 [Claude 成本可见性与控制](../../anthropic/engineering/cost-visibility-and-control-in-claude.md) 对比：Anthropic 提供企业成本管控工具，DeepSeek 提供峰谷价格杠杆，成本治理思路互补

## 资源

- 论文：N/A
- 官方公告（V4-Pro GA 与调价）：https://api-docs.deepseek.com/news/news260813
- 定价页：https://api-docs.deepseek.com/quick_start/pricing
- 更新日志：https://api-docs.deepseek.com/updates/
