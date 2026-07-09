# OpenAI and Broadcom Unveil LLM-Optimized Inference Chip

- **原文链接**: [OpenAI and Broadcom unveil LLM-optimized inference chip](https://openai.com/index/openai-broadcom-jalapeno-inference-chip/)
- **作者**: OpenAI
- **发布日期**: 2026-06-24
- **检索日期**: 2026-06-29
- **标签**: #Infrastructure #Broadcom #Jalapeño #InferenceChip #FullStack #GigawattScale

## 核心观点

OpenAI 与 Broadcom 联合发布 **Jalapeño**——OpenAI 首款自研 AI 加速器（Intelligence Processor），专为 LLM 推理设计，**早期测试显示每瓦性能远超当前最先进水平**。从设计到制造 tape-out 仅 **9 个月**——是高性能 ASIC 开发史上最快周期。Jalapeño 是 OpenAI "多代计算平台"的第一步，将与 Microsoft 等数据中心合作伙伴在 **2026 年底开始以吉瓦规模部署**。

## 关键信息

### 1. Jalapeño 是什么
- **为 LLM 推理从零设计的空白设计**——不是改造自通用加速器
- 由 OpenAI 设计架构，**Broadcom + Celestica 实现工业化**
- 同时支持当前和未来 LLM 跨行业使用
- 工程样片已在实验室以目标频率和功率运行 ML 工作负载（包括 **GPT-5.3-Codex-Spark**）

### 2. 性能
- 每瓦性能"远超当前 state-of-the-art"（详细技术报告将在未来几个月发布）
- 架构减少数据移动，平衡计算、内存和网络
- Broadcom 的 Tomahawk 网络硅帮助实现大规模生产

### 3. 设计到生产：9 个月
- 用 **OpenAI 模型加速设计优化流程**——"服务用户的模型也在帮助改进运行未来模型的基础设施"
- 软件-硬件协同开发
- 据称是高性能先进半导体 ASIC 开发史上最快周期

### 4. 全栈战略
- 从模型到产品到芯片——OpenAI 越来越多地自研整个堆栈
- 飞轮：更好基础设施 → 更高效率 → 更好训练和服务 → 更好模型 → 更好产品 → 更多用户 → 重新投入基础设施

### 5. 与 Microsoft 的部署
- Broadcom Hock Tan：与 Microsoft 等合作伙伴**从 2026 年开始部署吉瓦规模数据中心**

### 6. 行业意义
- "推理是 AI 触达用户的地方"——每一点成本、速度、可靠性改进都会体现为更快的产品响应
- 让先进 AI 更便宜、更可靠，让更多学生、开发者、中小企业、研究人员、企业能用

## 关键洞察

1. **垂直整合进入芯片层**——OpenAI 全栈战略从模型到产品到芯片
2. **AI 加速 AI 设计**——OpenAI 模型用于优化自家芯片
3. **推理专用 ≠ 通用 GPU**——为 LLM 特性优化的架构（数据移动、内存、网络）
4. **9 个月 ASIC 是新基线**——过去需要数年
5. **吉瓦级部署时间表明确**——2026 年底开始
6. **降低单位 token 成本**——让更多人和企业用得起

## 关键数据点

| 指标 | 数值 |
|------|------|
| 芯片代号 | Jalapeño |
| 架构设计者 | OpenAI |
| 工业化合作伙伴 | Broadcom、Celestica |
| 设计到 tape-out 时间 | 9 个月 |
| 部署规模 | 吉瓦级（gigawatt scale） |
| 部署合作伙伴 | Microsoft 等 |
| 部署时间 | 2026 年底起 |

## 相关文章

- [Supercomputer Networking to Accelerate Large Scale AI Training](mrc-supercomputer-networking.md)
- [Codex for Every Role, Tool, and Workflow](codex-for-every-role-tool-workflow.md)
- [OpenAI Frontier Models and Codex Are Now Available on AWS](openai-frontier-models-and-codex-are-now-available-on-aws.md)