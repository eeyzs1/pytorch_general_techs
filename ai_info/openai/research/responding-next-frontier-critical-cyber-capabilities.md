# 应对关键网络安全能力的下一前沿

- **原文链接**: [Responding to the next frontier of critical cyber capabilities](https://openai.com/index/responding-next-frontier-critical-cyber-capabilities/)
- **作者**: OpenAI
- **发布日期**: 2026-08-07
- **检索日期**: 2026-08-08
- **标签**: #Astra #网络安全 #PreparednessFramework #关键能力 #安全管控

## 核心观点

OpenAI 最新内部评估显示，即将发布的 Astra 模型在 agentic 编码和网络安全方面取得显著进展，基于专家评估无法排除其达到 Preparedness Framework 下"Critical"网络安全能力阈值的可能性。Critical 阈值指模型能在无人介入下识别并开发所有严重等级的零日漏洞，或仅凭高层目标 devising 并执行端到端的新型网络攻击策略。

OpenAI 已采取多项措施：更严格的安全控制、暂停不满足强化要求的活动、对 Astra 所有 agentic 应用实施通用监控、与政府机构和安全组织合作测试、为第三方测试伙伴提供推荐安全控制。此前 GPT-5.6 Sol 评估为 High 而非 Critical 阈值。

## 关键发现 / 关键技术

### 1. Critical 网络安全能力阈值
- 模型能在无人介入下识别并开发所有严重等级的功能性零日漏洞，针对许多加固的真实世界关键系统
- 或能仅凭高层目标 devising 并执行端到端的新型网络攻击策略，针对加固目标
- 初步评估显示 Astra 性能足够强，目前无法排除 Critical 能力级别

### 2. 已采取的内部措施
- 实施更严格安全控制：隔离测试环境、限制网络和工具访问、增强模型权重保护和加密、额外监控和检测、沙箱执行
- 暂停不满足强化安全控制要求的 Astra 内部活动
- 对所有 Astra agentic 应用（包括训练和评估）实施通用监控，监控 Chain of Thought 并触发安全响应
- 与相关政府机构和选定 AI 安全组织合作测试能力
- 为第三方测试伙伴提供运行高风险评估和工作负载的推荐安全控制

### 3. Preparedness Framework 沿革
- 2023 年 12 月首次发布，远早于模型接近生物、化学、网络安全和 AI 自我改进能力达到当前水平
- 2025 年 6 月模型接近生物 High 能力阈值时采取了类似强化措施
- GPT-5.6 Sol 此前评估为 High 而非 Critical 阈值
- Astra 未参与 Hugging Face 事件

## 实践意义

这是 OpenAI 首次公开表示其模型可能达到 Critical 网络安全能力阈值，标志着前沿模型能力进入新阶段。Preparedness Framework 的提前部署和透明披露为行业提供了能力治理的参考框架。对 Chain of Thought 的通用监控代表了 agentic 安全管控的新范式——从输出过滤转向推理过程监控。

## 跨厂商对比

- 与 [Daybreak：守护世界安全](daybreak-securing-the-world.md) 互补：前者聚焦防御性网络安全应用，本文聚焦即将到来的 Critical 能力阈值及其治理
- 与 [Hugging Face 模型评估安全事件](hugging-face-model-evaluation-security-incident.md) 互补：前者是已发生的安全事件复盘，本文是对未来更高能力的前瞻性治理
- 与 [数学与理论计算机科学的十项进展](ten-advances-in-mathematics.md) 对比：两者均由 Astra 模型驱动，前者展示数学研究能力，本文揭示其网络安全能力的前瞻评估
- 与 [发现密码学弱点](../../anthropic/research/discovering-cryptographic-weaknesses.md) 对比：Anthropic 用 Claude 主动发现密码学弱点帮助防御，OpenAI 则聚焦模型自身可能达到的攻击能力阈值

## 资源

- Preparedness Framework：https://cdn.openai.com/pdf/18a02b5d-6b67-4cec-ab64-68cdfbddebcd/preparedness-framework-v2.pdf
- 代码：N/A
- Demo：N/A
