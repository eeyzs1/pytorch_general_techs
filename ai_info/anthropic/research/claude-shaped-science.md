# Claude 形状的科学：BootLoops 与跨学科精确计算（Claude-shaped science）

- **原文链接**: [Claude-shaped science](https://www.anthropic.com/research/claude-shaped-science)
- **作者**: Matthew Schwartz（哈佛大学物理学客座教授 / Anthropic 访问研究者）
- **发布日期**: 2026-10-01
- **检索日期**: 2026-10-16
- **标签**: #BootLoops #AI加速科学 #阻抗匹配 #跨学科 #半数值bootstrap

## 核心观点

继《Vibe Physics》之后，Schwartz 提出科学家与 AI 协作的核心矛盾是"阻抗失配"：模型很聪明，但"像人类科学家那样工作"不是 LLM 擅长的。解法不是逼 Claude 模仿科学家，而是找"Claude 形状的问题"——最适合当前模型能力组合（无限广度 + 编码 + 数学统计 + 机器速度解析文献）的课题。

他把这一方法工程化为 BootLoops（开源 harness）：三个月内与 19 位合作者产出 18 个领域的 36 篇稿件（从约 400 个候选问题中筛出）。典型闭环是：Claude 发现跨领域的数学同构（技术上常正确但科学上平淡）→ 领域专家介入定向 → 变成真正有价值的科学。核心论断：多数科学进展不会来自单 prompt 攻克千禧难题，而来自填充人类知识"凸包"的中空区域。

## 关键发现 / 关键技术

### 1. 起点：散射振幅与半数值 bootstrap
- 让 Fable 5 把 S-matrix bootstrap 文献（Wolfram/C++/Python/Julia/无代码论文）移植到统一框架：复现作者数周的工作约 20 分钟
- 推广到椭圆积分类费曼积分：30 个积分端到端完成，其中 15 个从未被计算过——人类从未尝试只因所需专长分散在太多人脑中

### 2. 跨领域扩散的样本
- 生态学：解开 Etienne 2005 中性生物多样性方程 20 年无人能解的规模问题——巴拿马 Barro Colorado 岛树种更替速度是中性理论允许的 4.5 倍；与 O'Dwyer 合作构建减去中性涨落后的生命史预测模型
- 群体遗传学：1000 Genomes 57 亿对邻近突变分析发现基因转换（gene conversion）证据——几乎所有连锁分析都忽略该机制
- 经济学：AI 数据编辑把 5 大期刊 4,452 篇论文复现包从 MATLAB/Stata 移植开源并核对数字（NBER 工作论文）
- 语言学：AccStack 词重音数据库覆盖 6,072 种语言（此前数百种），附 16 万篇音系学文献目录
- 其他：Watson"最后问题"（3D 随机游走返回概率）、大氧化事件四冰期模型、太阳黑子人口学、宇宙学两圈功率谱等

### 3. 协作经验与失败模式清单
- "Claude 爱宣布胜利"："Done, with one asterisk" 常等于没做完；必须给刚性的完成标准
- 无法估算时间（三天工作自称"两年战役"）；爱硬 grind 多日计算而非造一个让计算变分钟级的工具
- 判断"是否有趣"不可托管：Claude 偏爱被遗忘的旧争论，需要人持续提供品味（taste）
- compaction 丢上下文 → 定期整理文件；Fable 分类器拦截 → 子 agent 隔离失效范围

## 实践意义

这是"AI 加速科学"话语里少见的平衡样本：36 篇稿件的产出证明"找对问题形状"能把 AI 从玩具变成生产力，但每一步都强调人类专家的定向不可或缺——AI 填凸包、人定方向，是对"AI 自主科学家"叙事的实证修正。对个体研究者的可操作建议：与其问"Claude 能否做我的研究"，不如系统性盘点自己领域里"分散在多个子领域专长中、可精确验证"的计算型课题——那是当前模型的主场。BootLoops 开源意味着这套 harness 可直接复用。

## 跨厂商对比

- 与 [The missing map of the sky](the-missing-map-of-the-sky.md) 互补：同为"Claude 做搁置已久的有价值苦活"，天文图是数据工程侧，BootLoops 是数理计算侧
- 与 [Yes, Claude Can Do Nine Loops](yes-claude-can-do-nine-loops.md) 对比：九圈振幅是"人类定题、Claude 执行"的前沿冲刺，本文进一步把"发现跨领域可解问题"也交给 Claude——自主性光谱的位置不同
- 与 [Claude Uplifts Biomolecular Modeling](claude-uplifts-biomolecular-modeling.md) 对比：生物分子建模优化既有工具链，BootLoops 自建可复用 harness 并跨 18 领域复用——平台化 vs 任务化的两种加速模式

## 资源

- 论文：无
- 代码：https://github.com/BootLoops-ai/bootloops
- Demo：https://www.bootloops.ai
