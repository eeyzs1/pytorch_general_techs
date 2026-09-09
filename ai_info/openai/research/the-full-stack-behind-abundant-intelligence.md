# 富足智能背后的全栈（The full stack behind abundant intelligence）

- **原文链接**: [The full stack behind abundant intelligence](https://openai.com/index/the-full-stack-behind-abundant-intelligence/)
- **作者**: Sarah Friar（OpenAI CFO）
- **发布日期**: 2026-08-25
- **检索日期**: 2026-09-09
- **标签**: #全栈战略 #算力经济学 #Jalapeño #基础设施组合 #Jevons悖论

## 核心观点

CFO Sarah Friar 系统阐述 OpenAI 的算力战略：一个横跨数据中心与芯片、前沿模型、开发者平台、消费与企业产品、AI 原生设备的集成系统，且各层互相增强——更好的软件让硬件更高产，为自家工作负载设计的硬件提升速度与能效，更强的模型解锁更好的产品并带来更多需求、使用与学习信号，信号再回流改进整个系统。AI 的进步在整套系统共同改进时复利式最快。

战略口号是"广度构建、杠杆自持"（build for breadth, own for leverage）：不同工作负载对芯片、软件、网络、电力、延迟的要求不同，目标是始终停留在 Pareto 前沿上，为每个工作负载寻找能力、速度、可靠性、能效与成本的最强组合。当日同步发布的自研推理芯片 Jalapeño 首批实测（InferenceX 基准）提供了全栈协同的直接证据。效率最终转化为经济价值：更便宜、更强的智能让更多工作"值得做"（Jevons 悖论），收入再资助下一代研究与基础设施，形成复利优势。

## 关键发现 / 关键技术

### 1. Jalapeño 首批实测：全栈协同的第一份证据
- 在 SemiAnalysis 的公共基准 InferenceX 上（GPT‑OSS 120B），Jalapeño 的峰值每千瓦吞吐与 token 延迟均优于对比中的商用系统；在 DeepSeek R1 与 Kimi K2 上同样强劲，说明收益跨模型家族成立
- 模型、服务软件、芯片、内存、网络协同开发，才能把吞吐、延迟、能效、成本作为一个系统整体优化；这是与合作伙伴加速器并行的可信第一方路线，下一代已在开发

### 2. 广度构建、杠杆自持：多元化的供应商组合
- 前沿训练、高吞吐推理、常驻 agent 对系统的要求各不相同；不同芯片与供应商在不同维度领先，前沿本身在不断移动
- 组合从 Microsoft 与 NVIDIA 的基础扩展到 AWS、AMD、Broadcom、Cerebras、CoreWeave、Oracle、SB Energy、SoftBank，分别覆盖云、加速计算、低延迟推理、数据中心开发与能源
- 数据中心的杠杆：佐治亚州 Project Camellia——按客户工作负载设计设施，闭环节水，承诺接受年度独立公共审计

### 3. 把效率变成经济价值
- GPT‑5.6 Sol（max reasoning）在 Artificial Analysis Coding Agent Index 创下新高，同时输出 token 比另一领先模型少 54%——对客户意味着更快结果、更少重试、更长工作流可完成
- Jevons 悖论：能效提升使更多用途变得划算，扩大消费并创造新经济活动；最佳经济学度量是"每美元的有效智能"

## 实践意义

本文是理解 OpenAI 基础设施叙事的关键一篇：它把"自研芯片"定位为组合中的一条第一方路径而非对 NVIDIA 的替代，把投资纪律表述为"Pareto 前沿上的动态选择"。对企业与技术决策者，可直接借鉴其分档逻辑——按工作负载在能力、延迟、能效、成本间做组合优化，而非追求单一"最好"的算力或模型；对投资者，"有用智能每美元"与"复利优势"是跟踪 OpenAI 经营杠杆的核心指标。

## 跨厂商对比

- 与 [构建充裕的智能](building-abundant-intelligence.md) 对比：同系列深化——7 月底的战略宣言（为什么全栈）在本文推进到执行层（怎么做：Jalapeño 实测、十家供应商组合、Camellia 数据中心），并首次以 CFO 视角串联芯片—算力—模型—产品的复利机制
- 与 [Agent 时代的 AI 投资管理](managing-ai-investments-in-agentic-era.md) 互补：本文是供给侧（OpenAI 自身）的全栈经济性论证，该文是需求侧（企业客户）如何度量与管理 AI 投入的框架，两侧合读可见"算力经济学"的完整链条

## 资源

- 官方文章：https://openai.com/index/the-full-stack-behind-abundant-intelligence/
- 相关：https://openai.com/index/jalapeno-first-results/
