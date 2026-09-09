# Jalapeño 首批实测结果（Jalapeño's first results show industry-leading speed and efficiency in AI inference）

- **原文链接**: [Jalapeño's first results show industry-leading speed and efficiency in AI inference](https://openai.com/index/jalapeno-first-results/)
- **作者**: OpenAI
- **发布日期**: 2026-08-25
- **检索日期**: 2026-09-09
- **标签**: #Jalapeño #自研推理芯片 #InferenceX #能效 #全栈协同设计

## 核心观点

OpenAI 首款自研推理芯片 Jalapeño 公布首批实测：单一架构同时做到更高吞吐与更低延迟，而现有硬件系统通常必须在两者间取舍。在 GPT‑OSS 120B、DeepSeek R1 670B、Kimi K2.5 1T 三个公开模型上，Jalapeño 在峰值吞吐下每瓦完成的 AI 工作量是对比系统的 1.5–1.9 倍，端到端延迟低 1.7–3.6 倍；高交互负载性能高 2.1–4.1 倍。收益跨模型家族成立，说明架构层面的有效性而非针对单一模型调优。

Jalapeño 同时是全栈优势的证据：OpenAI 把模型、产品、服务软件、芯片、内存、网络与整机系统一起设计，用真实工作负载的经验改进每一层。AI 也深度参与芯片自身开发——从初始设计到流片仅 9 个月。计划年底前开始在 OpenAI 算力基础设施中部署，与 NVIDIA 等伙伴的加速器并行；这是多代平台的起点：Gen 2 深入开发中，Gen 3 正在成形。

## 关键发现 / 关键技术

### 1. InferenceX 实测数据（SemiAnalysis 公共基准，按额定芯片功率归一化）
- GPT‑OSS 120B（对比 GB200 1200W）：峰值混合 TPS/kW ≈1.9×（85,448 vs 44,960）；端到端延迟 ≈1.7× 更低（1.03s vs 1.80s）；最低 TBT ≈2.7× 更低（0.69 vs 1.87ms，1,459 vs 535 tok/s/user）；在既有最优 TBT 下吞吐 ≈53.7×
- DeepSeek R1 670B MXFP4（对比 GB300 1400W）：TPS/kW ≈1.7×、延迟 ≈3.6×、最低 TBT ≈4.1×、同 TBT 吞吐 ≈104.3×
- Kimi K2.5 1T MXFP4：TPS/kW ≈1.5×、延迟 ≈3.4×、最低 TBT ≈3.8×、同 TBT 吞吐 ≈56.1×
- Jalapeño 额定 700W，实测持续功率保持 ≤550W；内部测试显示在前沿 OpenAI 模型上优势进一步扩大

### 2. 架构：在单芯片内同时为速度与效率设计
- 语言模型推理各阶段瓶颈不同：prefill 算力密集，decode 受内存带宽约束，跨核/跨片通信造成空闲等待
- 设计核心是最小化数据移动与通信延迟：KV cache 等模型状态可显式本地放置；大域网络让整个负载留在单一连通系统内，从请求到响应保持快速高效；兼顾 prefill 与 decode 且可随 agent 式负载的比例变化自适应

### 3. 用 AI 设计芯片，把芯片设计成 AI 可编程
- 早期模型协助设计与 bring-up，最新模型加速优化与编程；设计到流片 9 个月；AI 还优化了算术电路，在计划内塞入更多算力
- 清晰可预测的编程目标（局部张量、显式通信、可预期同步）让 AI 能处理映射、放置、调度与协同——传统上极难的并行编程问题
- 用 Codex + GPT‑Astra，团队两个月内让 3 个不在原生产计划内的开源权重模型达到高性能；对选定的 GPT‑OSS attention 与 MoE 块，AI 生成实现比人类专家实现快 1.5–1.8×

## 实践意义

Jalapeño 的实测数据把"自研推理芯片"从战略叙事变成了可复核的工程事实，直接对标 GB200/GB300 的每瓦吞吐与延迟。对推理服务与 agent 产品的运营者，芯片级能效提升最终会传导为更低的单次成功任务成本与更高的交互密度上限；对基础设施团队，其"按推理阶段放置状态、最小化数据移动"的思路对软件层的服务优化同样适用。多代路线图（Gen 2/Gen 3）与"AI 编程芯片"的开发循环，预示芯片迭代的节奏可能显著快于传统周期。

## 跨厂商对比

- 与 [OpenAI–Broadcom Jalapeño 推理芯片](openai-broadcom-jalapeno-inference-chip.md) 对比：官宣 vs 实测——前者确立合作、定位与多代计划，本文给出第三方公共基准（InferenceX）上的具体数字、功率归一化方法与架构细节，两篇构成 Jalapeño 的完整记录
- 与 [构建充裕的智能](building-abundant-intelligence.md) 互补：芯片实测是"全栈复利"故事在硬件层的最新落点，验证了"系统各层共同改进"的核心主张

## 资源

- 官方文章：https://openai.com/index/jalapeno-first-results/
- 相关：https://openai.com/index/the-full-stack-behind-abundant-intelligence/
