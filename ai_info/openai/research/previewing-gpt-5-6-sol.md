# Previewing GPT-5.6 Sol: A Next-Generation Model

- **原文链接**: [Previewing GPT-5.6 Sol: a next-generation model](https://openai.com/index/previewing-gpt-5-6-sol/)
- **作者**: OpenAI
- **发布日期**: 2026-06-26
- **检索日期**: 2026-06-29
- **标签**: #GPT-5.6 #Sol #Terra #Luna #CyberSecurity #Preparedness #ModelRelease

## 核心观点

OpenAI 预览 **GPT-5.6 系列三款模型**：Sol（旗舰）、Terra（平衡款，比 GPT-5.5 便宜 2×）、Luna（快速且最低成本）。Sol 配套"至今最强大的安全栈"。在网络安全、生物安全和自我改进三个 Preparedness 维度上，Sol 与 Terra 均达 **High 阈值**，但未达 Critical（Cyber）。新引入 `max` 推理 effort 和 `ultra` 模式（调用子 Agent 协同处理复杂任务）。

## 关键能力

### 1. GPT-5.6 Sol 性能亮点
- **Terminal-Bench 2.1（命令行工作流）**：Sol **91.9%** > Sol Ultra 88.8% > Claude Mythos 5 84.3% > Sol 88.8% > Terra 82.5%
- **GeneBench v1（基因组与定量生物学）**：Sol 用更少 token 优于 GPT-5.5
- **ExploitBench**：Sol 在长视野漏洞研究/利用上与 Mythos Preview 相当，**只用约 1/3 输出 token**
- **ExploitGym**（UC Berkeley 与 OpenAI 等前沿实验室合作）：Sol、Terra、Luna 推理增加时均显著提升

### 2. `max` 与 `ultra` 推理 effort
- `max`：让 Sol 有最长时间深度推理
- `ultra`：**超出单 Agent 能力**——通过子 Agent 协同加速复杂工作

### 3. 网络安全能力
- Sol 在漏洞研究和利用上**接近 Mythos Preview 性能，用 1/3 输出 token**
- 但 Sol 在 Chromium 和 Firefox 测试中：
  - 能识别漏洞和利用原语（exploit 构件）
  - **未能在测试条件下自主产生完整的功能性全链 exploit**
- 因此 Sol **未越过 Preparedness Framework 的 Cyber Critical 阈值**

### 4. 安全栈层级（layered safeguard stack）
- **模型层**：训练拒绝禁止的网络协助（包括伪装意图、jailbreak）
- **实时检查**：网络和生物误用分类器，输出生成时评估；高风险情况下，调用更大推理模型审查
- **账户级信号**：跨会话风险信号，识别持续恶意行为
- **差异化访问**：最敏感能力仅对可信防御者开放
- **监控 + 强制 + 持续测试**

### 5. 与美国政府的协调
- 预览前向美国政府通报计划
- 应政府请求，**先向"小规模可信合作伙伴"开放有限预览**，其参与与政府共享
- 之后才更广泛发布
- OpenAI 明确表示："**不相信这种政府访问流程应成为长期默认**"——它把最佳工具挡在用户、开发者、企业、网络防御者和全球合作伙伴之外

### 6. 部署计划
- Sol、Terra、Luna 将在未来几周 GA
- 与美国政府合作开发"网络 Executive Order 框架"

## 关键洞察

1. **GPT-5.6 系列继续向"超低延迟 + 多型号分层"演进**——Terra 比 GPT-5.5 便宜 2×
2. **网络能力接近 Mythos，但 token 效率更高**——Sol 用 1/3 token 接近 Mythos Preview 性能
3. **`ultra` 模式 = Agent 协同**——单模型到多模型协同的正式产品化
4. **未达 Cyber Critical 阈值**——尽管能力接近，OpenAI 仍判定未达最高风险
5. **政府介入是新现象**——首次明确表示"政府请求"影响公开发布节奏
6. **纵深防御已成标准**——模型层 + 实时分类器 + 账户级 + 差异化访问 + 监控

## 关键数据点

| 指标 | 数值 |
|------|------|
| 模型数 | 3（Sol, Terra, Luna） |
| Terra 价格 vs GPT-5.5 | 1/2 |
| Terminal-Bench 2.1（Sol） | 91.9% |
| ExploitBench token 效率 | 1/3 |
| Preparedness Cyber 等级 | High（未达 Critical） |
| 自动 red-team GPU 时长 | 700,000+ A100e 小时 |

## 相关文章

- [GPT-5.5 Instant](gpt-5-5-instant.md)
- [GPT-5.5 System Card](gpt-5-5-system-card.md)
- [GPT-5.6 Preview System Card](gpt-5-6-preview-system-card.md)
- [Daybreak: Tools for Securing Every Organization](daybreak-securing-the-world.md)