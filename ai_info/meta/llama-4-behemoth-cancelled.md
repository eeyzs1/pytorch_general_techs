# Llama 4 Behemoth: The 2T-Parameter Model That Never Shipped

- **原文链接**: 综合报道（Meta 官方 + 社区跟踪）
- **作者**: Meta AI / 社区报道
- **发布日期**: 2025-04-05（公布）→ 2026-05（搁置确认）
- **检索日期**: 2026-06-07
- **标签**: #Meta #Llama4 #Behemoth #MoE #Cancelled

## 核心事件

Llama 4 Behemoth 是 Meta 在 2025 年 4 月公布的 ~2T 参数 MoE 旗舰模型（288B 活跃参数，16 个专家），定位为"教师模型"用于知识蒸馏。经过一年多的延迟，2026 年 5 月被确认搁置，从未公开发布。

## 关键数据

- **总参数**：~2 万亿
- **活跃参数**：2880 亿
- **架构**：Mixture of Experts，16 个专家
- **定位**：不是面向用户的产品，而是通过知识蒸馏训练 Scout 和 Maverick 的"教师模型"

## 搁置原因

1. **内部能力问题**：独立报道显示存在"内部能力担忧"
2. **MoE 路由挑战**：在如此大的活跃参数规模下，MoE 路由效率低下
3. **Llama 4 刷榜丑闻**：品牌信誉受损，继续发布旗舰模型无意义
4. **组织重组**：MSL 成立后，Llama 路线被放弃
5. **Muse Spark 取而代之**：2026 年 4 月 Muse Spark 发布时，基准测试中已不再提及 Behemoth

## 关键洞察

1. Behemoth 成为"纯规模路线的失败案例研究"——光是堆参数不够
2. Llama 品牌从发布到搁置仅 14 个月，反映了 AI 领域的迭代速度之快
3. Meta 从"开源旗手"到"闭源转向"，Behemoth 的失败是转折点
4. 对比 OpenAI、Anthropic、Google 的快速迭代，Meta 失去了一年多的时间