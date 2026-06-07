# Muse Spark: Meta's First Proprietary Superintelligence Model

- **原文链接**: [Introducing Muse Spark](https://ai.meta.com/blog/introducing-muse-spark-msl/)
- **作者**: Meta Superintelligence Labs
- **发布日期**: 2026-04-08
- **检索日期**: 2026-06-07
- **标签**: #Meta #MuseSpark #ClosedSource #Multimodal #Superintelligence

## 核心观点

Meta 发布 Muse Spark，这是 Meta Superintelligence Labs (MSL) 的首个 AI 模型，标志着 Meta 从开源策略向闭源前沿模型的战略转向。Muse Spark 不是 Llama 5，而是完全重新构建的新架构，定位为"个人超级智能"。

## 关键数据

### 性能指标
- **Artificial Analysis v4.0**：52（对比 GPT-5.4: 57，Gemini 3.1 Pro: 57）
- **CharXiv**（图表理解）：86.4（#1）
- **HealthBench Hard**（医疗推理）：42.8（#1）
- **FrontierScience**：38.3（#1）
- **HLE（Contemplating 模式）**：50.2（#1）
- **MMMU-Pro**（视觉推理）：80.5（#2，仅次于 Gemini 3.1 Pro）
- 计算效率：比 Llama 4 Maverick 高 **10 倍**

### 技术架构
- **原生多模态**：支持文本、图像、语音输入
- **262K 上下文窗口**
- **三种模式**：Instant（低延迟）→ Thinking（深度推理）→ Contemplating（多代理并行）
- **Contemplating Mode**：多个 AI 代理同时并行推理，综合输出

### 部署范围
- 已接入 Meta AI app、meta.ai、WhatsApp、Instagram、Facebook、Messenger、Ray-Ban 智能眼镜
- 覆盖约 **30 亿日活用户**
- 闭源，API 仅限合作伙伴私有预览

## 亮点应用
- **视觉诊断**：拍照诊断咖啡机故障，分步标注部件，如同真人维修工
- **营养分析**：拍照识别餐盘营养成分，结合个人健康数据给出建议
- **AR 实时交互**：通过 Ray-Ban 眼镜叠加实时提示
- **视觉编程**：自然语言指令生成可交互 Web 应用和小游戏

## 关键洞察

1. **Meta 从开源转向闭源**——这是 Meta AI 战略的根本性转变，Llama 时代的开源策略被放弃
2. MSL 由前 Scale AI CEO Alexandr Wang 领导，9 个月从零重建整个 AI 栈
3. Llama 4 刷榜丑闻后，Meta 彻底推倒重来，Muse Spark 是"赎罪之作"
4. 30 亿用户分发是 Meta 最大的竞争壁垒——即使模型略逊于 GPT-5.4，分发优势无人能敌