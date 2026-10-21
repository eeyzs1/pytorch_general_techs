# LASER：面向更安全对话的递归采样（Meet LASER: Recursive sampling for safer conversations）

- **原文链接**: [Meet LASER: Recursive sampling for safer conversations](https://alignment.openai.com/laser/)
- **作者**: Isak Czeresnia Etinger（OpenAI Alignment 团队）
- **发布日期**: 2026-10-06
- **检索日期**: 2026-10-16
- **标签**: #安全评估 #主动学习 #向量数据库 #效率工程 #Codex

## 核心观点

LASER（Logistic Augmented Sampling over Embeddings，Recursively）是 OpenAI 为安全评估自动挖掘"稀有、模糊、处在政策决策边界"对话的流水线：廉价逻辑回归分类器负责筛选，昂贵推理模型负责标注，循环往复自我强化。效果是三重的：把原本需要多轮人工专门工作的评估集构建压缩到几小时；用贪心多样性采样保证每个样本的信息量；找到同等数量违规样本所需的评分算力约为随机采样的 1/10,000。隐私上，流水线只处理合成与去标识对话，不接触原始用户数据。

## 关键发现 / 关键技术

### 1. 评分-拟合-采样循环
- 初始样本：按安全政策文档生成合成对话 + 相似的去标识对话 + 随机对话。
- 循环：推理评分器（带 CoT 的 LLM）判定对话是否被政策允许 → 用全部已标数据在嵌入向量上拟合逻辑回归 → 在分类器决策边界（预测违规概率约 40%-60%/30%-70% 区间，主动学习中的不确定性采样）采样新对话 → 重复。
- 结果：边界采样使约 1/2 被评分对话最终判为违规，而随机采样下违规基率约 1/20,000——这是 10,000× 算力节省的来源。

### 2. 向量数据库里跑逻辑回归（工程亮点）
- 嵌入（256 维、归一化）存入 Rockset；利用其近似点积检索，把逻辑回归概率区间约束改写为对常数 w 的点积区间约束（P∈[MIN,MAX] ⟺ log 常数界 < w·x < 常数界），于是一条 SQL（`WHERE DOT_PRODUCT(:w, embedding) BETWEEN :C1 AND :C2`）即可在数十亿点上秒级完成"逻辑回归采样"。

### 3. 贪心多样性采样
- 从随机一条违规对话开始，迭代选离已选集合最远的对话，生成有序列表——取前 N 条即为最大多样性的 N 条违规样本，直接提升单位样本评估信号。

### 4. 其他可复用技巧
- 推理评分器利用 prompt caching（政策固定前缀）大幅降本，单次运行数十万次评分。
- 整个 DAG 流水线由 Codex 加速实现并审查大部分 PR——安全基础设施本身的 Agent 化开发样本。
- 已用于 GPT-6 Astra 敏感领域评估（暴力违法行为、自残、性内容），确保长尾细分类别进入评测集。

## 实践意义

1. **安全评估从手工到流水线**：新安全关切出现时，"数小时内出评估集"取代多轮专家迭代——安全团队的反应速度量级提升。
2. **分类器+推理模型分工范式**：廉价模型选点、昂贵模型标注、互相蒸馏的循环，可平移到评测集构建、数据标注、红队样本挖掘等任何"找稀有正例"的场景。
3. **数据库侧 ML 的新解法**：把回归约束改写为点积区间的"查询技巧"，让已有向量库直接承担大规模统计筛选，无需导出数据。

## 跨厂商对比

- 与 [Introducing MentalHealthBench](introducing-mentalhealthbench.md) 对比：MentalHealthBench 靠 1,215 段专家对话定义质量，LASER 用递归采样自动找边界样本——专家撰写与自动挖掘是安全评测集构建的两条路线，前者深度后者覆盖。
- 与 [Separating Signal from Noise in Coding Evaluations](separating-signal-from-noise-coding-evaluations.md) 互补：编码评估审计发现 ~30% 任务有缺陷（去噪），LASER 从源头提升信号密度（增效），共同指向"评测集质量是评测的瓶颈"。
- 与 [GPT-5.6 效率工程](gpt-5-6-frontier-intelligence-efficiency.md) 并观：同是把昂贵模型用在刀刃上的分层设计——推理栈的复利逻辑被搬到安全评估基础设施。

## 资源

- 官方博客（含图示与 BibTeX）：[Meet LASER](https://alignment.openai.com/laser/)
- 相关工具：[Rockset](https://openai.com/index/openai-acquires-rockset/)、[prompt caching 文档](https://platform.openai.com/docs/guides/prompt-caching)
- 相关条目：[safety-overview-gpt-6-astra](safety-overview-gpt-6-astra.md)

> 注:alignment.openai.com 官方页面直抓成功，全文核实，无需第三方交叉验证。
