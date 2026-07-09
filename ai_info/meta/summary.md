# Meta AI — 核心观点总结

> 汇总 Meta AI 近期重大动态，4 篇文章，涵盖 2025 年 4 月至 2026 年 6 月。

## 一、总体脉络

Meta AI 在 2025-2026 年经历了剧烈的战略转变：

```
Llama 4 发布 → 刷榜丑闻 → 组织重组 → 闭源转向 → Muse Spark → Brain2Qwerty v2
```

从开源旗手到闭源转向，从 Llama 品牌危机到 MSL 重建，Meta 用一年时间完成了 AI 战略的彻底重构。2026 年 6 月底，Meta 又发布 [Brain2Qwerty v2](brain2qwerty-v2.md)——非侵入式脑机接口的端到端 LLM 解码 pipeline，在 Nature Neuroscience 发表并开源全部训练代码与数据集，标志 Meta 在"AI + 神经科学"方向继续深入，与主流 LLM 产品形成"产品 + 科学"双轨。

## 二、核心事件

### 1. Llama 4 刷榜丑闻

[Llama 4 Benchmark Scandal](llama-4-controversy.md) 是 2025-2026 年 AI 行业最大的信任危机。Meta 为不同基准测试使用了不同版本的模型，将每个测试的最佳分数拼凑成一张"统一"表格。2026 年 1 月，Yann LeCun 向 Financial Times 确认"结果被稍微篡改"。后果：LMSys Arena 排名从第 2 跌至第 32，Llama 品牌信誉永久受损，4 次组织重组。

### 2. Behemoth 搁置

[Llama 4 Behemoth](llama-4-behemoth-cancelled.md) 是 ~2T 参数 MoE 旗舰模型，定位为"教师模型"。2025 年 4 月公布后经历一年延迟，2026 年 5 月被确认搁置。成为"纯规模路线的失败案例研究"。

### 3. Muse Spark 闭源转向

[Muse Spark](muse-spark.md) 是 Meta Superintelligence Labs 的首个模型，2026 年 4 月发布。关键转变：
- **闭源**：不再开放权重，直接部署到 Meta 产品
- **新架构**：不是 Llama 5，而是从零重建
- **新领导**：前 Scale AI CEO Alexandr Wang 领导 MSL
- **高效**：比 Llama 4 Maverick 高 10 倍计算效率
- **分发**：覆盖 30 亿日活用户（Meta AI, WhatsApp, Instagram, Facebook, Messenger, Ray-Ban）

### 4. Brain2Qwerty v2 非侵入式脑机接口

[Brain2Qwerty v2](brain2qwerty-v2.md)（2026-06-29）是 Meta 在"AI + 神经科学"方向的旗舰研究：
- **端到端深度学习** 直接从 MEG 原始信号解码句子，跳过手工特征工程
- 用 **LLM 微调** 弥合噪声脑信号与连贯语言的语义鸿沟
- 9 名志愿者、22,000 句子训练，**词准确率 61%**（最佳 78%），相比其他非侵入方法 8% 提升 7.5 倍
- 在 **Nature Neuroscience** 发表，开源 v1+v2 训练代码 + v1 数据集
- 配套 [Tribev2](https://ai.meta.com/blog/tribe-v2-brain-predictive-foundation-model/)、NeuralSet、NeuralBench 形成"开放脑模型基础设施"
- **Meta 差异化**：与 Google DeepMind Co-Scientist/AlphaEvolve、Anthropic Claude Chemist、OpenAI GeneBench-Pro 等共同构成 2026 年的"AI for Science"竞争格局

## 三、关键数据点

| 指标 | 数值 | 来源 |
|------|------|------|
| Llama 4 Maverick LMSys Arena 排名变化 | #2 → #32 | Llama 4 Controversy |
| Llama 4 Behemoth 参数 | ~2T | Behemoth |
| Muse Spark CharXiv | 86.4 (#1) | Muse Spark |
| Muse Spark HealthBench Hard | 42.8 (#1) | Muse Spark |
| Muse Spark 计算效率提升 | 10x vs Llama 4 | Muse Spark |
| Muse Spark 上下文窗口 | 262K | Muse Spark |
| Meta 组织重组（6 个月） | 4 次 | Llama 4 Controversy |
| Brain2Qwerty v2 词准确率 | 61%（最佳 78%） | Brain2Qwerty v2 |
| Brain2Qwerty v2 vs 其他非侵入方法 | 7.5×（61% vs 8%） | Brain2Qwerty v2 |
| Brain2Qwerty v2 训练句子数 | 22,000 | Brain2Qwerty v2 |
| Brain2Qwerty v2 志愿者数 | 9 | Brain2Qwerty v2 |

## 四、关键洞察

1. **开源不等于可信**：Llama 4 丑闻暴露了开源模型基准测试的信任危机
2. **闭源转向是生存策略**：Meta 意识到开源无法在性能上追上 OpenAI/Google，转向闭源 + 分发优势
3. **30 亿用户是终极壁垒**：即使模型性能略逊，分发优势无人能敌
4. **纯规模路线失败**：Behemoth 的搁置证明"堆参数"不再是有效策略
5. **组织动荡是 AI 竞赛的常态**：4 次重组、LeCun 离职、Wang 入主——Meta 在动荡中寻找方向

## 五、文章索引

| # | 日期 | 文章 | 主题 |
|---|------|------|------|
| 1 | 2025-04 ~ 2026-01 | [Llama 4 Benchmark Scandal](llama-4-controversy.md) | 信任危机 |
| 2 | 2025-04 ~ 2026-05 | [Llama 4 Behemoth Cancelled](llama-4-behemoth-cancelled.md) | 旗舰搁置 |
| 3 | 2026-04-08 | [Muse Spark](muse-spark.md) | 闭源转向 |
| 4 | 2026-06-29 | [Brain2Qwerty v2](brain2qwerty-v2.md) | 脑机接口 / AI for Science |