# A Postmortem of Three Recent Issues

- **原文链接**: [A postmortem of three recent issues](https://www.anthropic.com/engineering/a-postmortem-of-three-recent-issues)
- **发布日期**: 2025-09
- **标签**: #事后分析 #基础设施 #TPU #路由 #精度 #可靠性

## 核心观点

2025 年中，用户报告了 Claude 性能下降的问题。Anthropic 调查后发现，这些问题并非模型退化，而是三个基础设施 Bug 的组合效应。文章详细分析了每个 Bug 的根因、检测困难和修复过程。

## 三个 Bug 详解

### Bug 1: 长上下文路由错误 (Long Context Routing)
- **问题**: 为支持 1M 上下文，Anthropic 使用不同的服务器（可能是不同中间训练的模型），但流量路由错误地将请求发送到了错误的服务器
- **影响**: 约 30% 的请求被路由到错误的服务器
- **检测困难**: 测试的基数太低，无法捕捉到路由错误

### Bug 2: 输出损坏 (Output Corruption)
- **问题**: TPU 服务器上的配置错误导致 token 生成错误
- **根因**: 运行时性能优化偶尔给错误 token 分配高概率
- **表现**: 英文输出中出现泰文/中文字符，代码中出现语法错误
- **特点**: 间歇性出现，难以复现

### Bug 3: XLA:TPU 编译错误 (XLA:TPU Miscompilation)
- **问题**: 代码变更触发了 XLA:TPU 编译器中的潜在 Bug
- **根因**: 与混合精度算术有关（bf16 vs fp32）
  - 模型分布在多个 GPU 上，logits 以 bf16 格式存储但以 fp32 聚合
  - 不同 GPU 返回不同精度，暴露了 JAX 中的混合精度 Bug
- **特点**: 三个 Bug 中最难以捉摸和不一致的

### 完美风暴
三个 Bug 同时发生，导致用户感知到显著的性能下降，但每个 Bug 单独的影响都较难检测。

## 关键教训

- **浮点数和分布式系统**: Bug 3 同时涉及浮点精度和分布式系统问题
- **测试基数不足**: 低基数测试无法捕捉路由等系统性问题
- **基础设施 Bug ≠ 模型退化**: 用户感知的性能下降可能源于基础设施而非模型本身。[Quantifying Infrastructure Noise in Agentic Coding Evals](quantifying-infrastructure-noise-in-agentic-coding-evals.md) 进一步量化了基础设施配置对基准测试的影响——仅配置差异就能造成 6 个百分点的波动
- **所有 Bug 在 2025 年 9 月中旬修复**
- 在评估中排除基础设施干扰的方法参见 [Demystifying Evals for AI Agents](demystifying-evals-for-ai-agents.md)
- [Effective Harnesses for Long-Running Agents](effective-harnesses-for-long-running-agents.md) 同样面临基础设施可靠性挑战——长时间运行的 Agent 需要确定性保障来应对工具失败
