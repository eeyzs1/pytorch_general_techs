# AlphaGenome Atlas：人类基因组每一个可能 DNA 字母变化的预测图谱（AlphaGenome Atlas: A predictive map of every possible DNA letter change in the human genome）

- **原文链接**: [AlphaGenome Atlas: A predictive map of every possible DNA letter change in the human genome](https://deepmind.google/blog/alphagenome-atlas-a-predictive-map-of-every-possible-dna-letter-change-in-the-human-genome/)
- **作者**: AlphaGenome Atlas 团队（Google DeepMind）
- **发布日期**: 2026-09-08
- **检索日期**: 2026-09-09
  注：官方页面抓取受限，本文基于检索核验的日期与公开报道整理（页首日期/作者/分类经 web_fetch 核验，细节经 Stowers Institute 新闻稿转述核验）
- **标签**: #AlphaGenome #基因组学 #AIforScience #变异解读

## 核心观点

人类基因组约 30 亿个 DNA 字母，可能的单字母变异超过 90 亿个——逐一做实验验证在实践中不可能。Google DeepMind 发布 AlphaGenome Atlas：一个 1 PB 量级的数据集，对全部 90 亿+个可能 DNA 碱基变异的分子效应给出 AI 预测，官方称之为同类中最全面的目录。

在此之前的资源要么能对变异排序、要么能提示受扰生物过程，二者难以兼得。Atlas 把两者合并：既能全基因组范围排序变异影响，又能揭示变异预计扰动的生物过程，用于加速基础发现、疾病研究与治疗靶点寻找。配套工作以预印本形式发布于 bioRxiv。

## 关键发现 / 关键技术

### 1. 规模与团队
1 PB 数据集，覆盖约 30 亿碱基的 90 亿+种可能单字母变异的分子效应预测；由 Google DeepMind 团队（副总裁兼首席科学家 Žiga Avsec 领导）历时数年开发。

### 2. 科学协作网络
Stowers 研究所（Julia Zeitlinger 提供基因调控生物学专长，其实验室 Melanie Weilert 任主要作者）、Broad 研究所、埃克塞特大学、纪念斯隆-凯特琳癌症中心与斯坦福大学参与科学输入与应用探索；Zeitlinger 评价其可"快速查询多种细胞类型，寻找基因激活与抑制的一般模式"——因为每种细胞类型的"语言"略有不同，找出一般规则正是难题所在。

### 3. 应用定位
面向"细胞如何知道该开哪些基因、关哪些基因"的调控语言问题；对变异解读的意义在于：罕见病变异优先级排序、疾病机制假设生成、治疗靶点发现。

## 实践意义

对计算生物学与遗传学团队，Atlas 把"变异效应预测"从逐条调用模型变为可整体检索的静态资源，适合批量注释与假设生成；但预测仍是预测——临床决策级结论仍需实验验证，且预测在罕见变异上的校准更难。对 AI for Science 谱系，它是"大模型产出可复用科学数据资产"路线的又一样本。

## 跨厂商对比

- 与 [AI 协同临床：开启医疗新模式](ai-co-clinician.md) 对比：co-clinician 面向临床决策层（个体患者的治疗证据），Atlas 面向机制层（变异→分子效应的知识底座），分别占据"临床床边"与"实验台"两端。
- 与 [Claude 如何加速蛋白质设计与分析化学](../../anthropic/research/claude-accelerates-protein-design.md) 互补：Anthropic 侧验证 LLM 作为科研假设生成器的设计空间，Google 侧交付预计算的基因组级穷举式图谱——生成式探索与全量图谱构成 AI for Science 的两条互补路径。

## 资源

- 官方文章：https://deepmind.google/blog/alphagenome-atlas-a-predictive-map-of-every-possible-dna-letter-change-in-the-human-genome/
- 产品/API：https://deepmind.google/science/alphagenome/
