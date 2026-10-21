# 用 Google Antigravity 加速抗菌肽搜索（Accelerating the search for antimicrobial peptides with Google Antigravity）

- **原文链接**: [Accelerating the search for antimicrobial peptides with Google Antigravity](https://deepmind.google/blog/accelerating-antimicrobial-discovery/)
- **作者**: Pengfei Tian、Maxwell L. Bileschi、Zoi Tsangalidou、Sukhdeep Singh、Lucy J. Colwell
- **发布日期**: 2026-10-15
- **检索日期**: 2026-10-16
- **标签**: #Antigravity #抗菌肽 #AIforScience #ProtNLM #智能体科学

## 核心观点

这是一篇罕见的"诚实展示科学智能体边界"的技术复盘：研究者驾驶 Google Antigravity 中的智能科学工作台，在一次会话内串联数据库筛选、序列搜索、结构比对、基因组上下文检查与文献综合，为肺炎链球菌近缘种 Streptococcus pseudopneumoniae 优先级化了一株抗菌肽候选——目前正处于湿实验室验证中，尚无任何活性数据。

候选分子 UniProt A0A0U0D591（97 氨基酸，Lactococcin 972 家族）：Swiss-Prot 人工审核库无显著同源序列；AlphaFold DB 预测折叠与一个已实验测定的细菌素接近；基因组邻域（上游 6bp 处 ABC 转运 permease、邻近 ATP 结合伴侣、另一个细菌素与 XRE 转录调节子）支持其属于细菌素系统假说。

文中最有价值的细节是方法学克制：所有"细胞分裂机制""抗耐药呼吸道病原体"活性均为预测而非实验结论；官方未公开检索输出、显著性阈值与完整排序标准。同时发布 Biomolecular Structure Viewer——3D 结构里 Agent 高亮区域、研究者回传标注的双向工具。

## 关键发现 / 关键技术

### 1. 研究者主导的智能体工作流
- 人设定目标（在 S. pseudopneumoniae 中发现并计算验证新型抗菌肽）、选择追问问题与取证证据；Agent 负责跨库查询、结构分析与文献综合
- 单会话串联：蛋白库过滤 → 序列搜索 → 预测结构比对 → 基因组上下文 → 文献综合，ProtNLM 提供序列到功能预测

### 2. 候选分子证据链
- A0A0U0D591：97 aa，Lactococcin 972 家族；Swiss-Prot 无显著同源（TrEMBL 为自动注释）
- AlphaFold DB 模型折叠与已实验测定细菌素接近（官方未给出比对指标，AlphaFold 结构置信度不等同实验证据）
- 基因组邻域：6bp 上游 ABC 转运 permease 操纵子 + ATP 结合伴侣 + 另一注释细菌素 + XRE 转录调节子
- 文献综合产生"细胞分裂机制""抗耐药病原体"假说——均为预测

### 3. 输出物与当前状态
- 产出成套湿实验方案：蛋白表达、抗菌药敏试验、靶标结合、体外毒性
- 候选与其他管线分子已进入湿实验室验证；未公布检测结果、活性/毒性数据、实验室与时间表

### 4. Biomolecular Structure Viewer
- 集成 3D 结构查看：Agent 可高亮结构区域，研究者把标注回传给 Agent——结构生物学场景的"人机共驾"界面
- 官方演示覆盖从蛋白筛选、结构/基因组分析到湿实验计划的全流程

## 实践意义

对抗药性危机下的药物发现团队，这篇文章的价值不在候选分子本身，而在可复用的工作流骨架："计算优先级化 + 明确标注证据等级 + 直通湿实验方案"。它同时示范了科学智能体报道的正确姿势——区分数据库注释与实验证据、公开局限（未公开阈值与完整排序）。

对 Antigravity 平台，这是"科学工作台"叙事的首个公开深度案例：与 Co-Scientist 的多智能体假设锦标赛、AlphaEvolve 的算法进化不同，Antigravity 路线是"研究者驾驶 + Agent 执行跨库操作"。评估时应把三者视为互补管线而非竞争。

## 跨厂商对比

- 与 [Co-Scientist](co-scientist.md) 对比：Co-Scientist 用多智能体锦标赛生成与排名假设，Antigravity 工作流由研究者逐步驾驶、Agent 执行检索分析——"自驱假设生成"与"人驾取证流水线"两种科学智能体范式。
- 与 [AlphaEvolve](alphaevolve.md) 互补：AlphaEvolve 进化算法与优化目标，本工作流优先级化生物分子候选——同为 Agentic Science，一个收敛数值目标，一个产出实验假说。
- 与 [Agents in Biology](../../anthropic/research/agents-in-biology.md) 对比：Anthropic 用 Claude 系智能体做生物学长程任务，DeepMind 用平台化工作台 + 自家蛋白模型栈（ProtNLM/AlphaFold）——垂直模型深度 vs 通用 Agent 广度。
- 与 [Introducing SynthID Bio](introducing-synthid-bio.md) 同期互补：同一窗口内，一个负责"设计并验证抗菌肽"，一个负责"给 AI 设计的生物分子加水印"——AI 制药的生产侧与溯源侧同步成型。

## 资源

- 官方文章：https://deepmind.google/blog/accelerating-antimicrobial-discovery/
- 论文：无
- 代码：无
- Demo：https://antigravity.google/use-cases/science（Antigravity 科学工作流）

> 注：官方页正文在检索环境被截断，本文经 Data Phoenix（10-15）、NeoTeo/Unite.AI（10-16）、gigazine 相关报道等多源交叉验证；候选编号与基因组邻域细节以 Data Phoenix/Unite.AI 转述为准。
