# 用 Codex 与 ChatGPT 搜索新型抗菌分子

- **原文链接**: [How a researcher uses Codex and ChatGPT to search for new antimicrobial molecules](https://openai.com/index/using-codex-chatgpt-to-search-for-new-antimicrobials)
- **作者**: OpenAI(官方博客)
- **发布日期**: 2026-09-10
- **检索日期**: 2026-09-29
- **标签**: #AIforScience #抗菌肽 #Codex #基因组挖掘 #生物医药

## 核心观点

宾夕法尼亚大学教授 César de la Fuente 实验室的『AI for science』案例:团队用 OpenAI 的 Codex 与 ChatGPT 系统性地搜索现存物种与已灭绝物种的基因组,从中挖掘候选抗菌肽/抗菌分子,以应对耐药菌感染这一全球健康威胁。文章属于 OpenAI 的 Applied AI 叙事线,重点展示智能体工具在真实科研管线中的用法。

方法论上的关键点是『通用智能体而非专用模型』:把基因组数据接入编码智能体,让其批量扫描、注释并合成候选分子序列,再进入湿实验验证。这印证了通用前沿模型 + 领域数据工程正在成为生物医药发现的标准打法——而非为每个任务定制生物模型。

## 关键发现 / 关键技术

### 1. 科研管线设计
- 数据面:现存物种与已灭绝物种的基因组,作为抗菌肽/抗菌分子的搜索空间。
- 工具面:Codex(通用编码智能体)+ ChatGPT,承担基因组序列的批量扫描、注释与候选分子序列合成。
- 验证面:候选分子进入湿实验验证,形成『搜索-筛选-排序-实验』闭环。

### 2. 通用编码智能体的可复用性
- 核心主张:Codex 这类通用编码智能体在生物序列『搜索-筛选-排序』任务上可复用,不需要专用生物模型。
- de la Fuente 团队此前已多次发表 AI 发现抗菌肽的工作,本次与 OpenAI 官方博客合作强调的是工具泛化性。

### 3. 问题背景:耐药菌威胁
- 耐药菌感染是全球健康威胁,新抗菌分子发现管线长期供给不足。
- 基因组规模(而非单点任务)的搜索为评估 AI 科研加速率提供了更真实的证据。

### 4. 在 OpenAI 科研叙事中的位置
- 与 Navier–Stokes 智能体集群(约 1 万个智能体、88 小时)同属『智能体做科学』主线:数学侧重推理链,本文侧重数据管线。
- 与 Aardvark 的安全研究智能体对照:同为『通用智能体 + 领域数据』范式在不同学科的复用。
- 与 GPT Rosalind 生物安全系列共用『生物序列 + 智能体』的技术底座,应用面从国防延伸到民用药物发现。
- 外部实验室(宾大)可复用 OpenAI 工具,说明该打法已溢出公司边界。
- 后续观察点:候选分子进入湿实验与临床前阶段的通过率,是检验 AI 筛选有效性的终极指标。
- 风险面:抗菌分子的可合成性使该管线天然邻近两用性(生物安全)审查,需配套筛选红线。

## 实践意义

1. **AI 科研加速的基因组级证据**:对评估 AI 科研加速率的团队,该案例提供了基因组规模(而非单点任务)的一手样本,比单一基准更能反映管线杠杆。
2. **『通用模型 + 数据工程』范式**:生物医药发现团队可复用的路径是领域数据工程(基因组接入、注释规范),而非自训专用模型。
3. **湿实验仍是守门人**:候选分子必须经湿实验验证,AI 负责的是把搜索空间从『海量基因组』压缩到『可实验的候选集』。

## 跨厂商对比

- 与 [Introducing GPT Rosalind](introducing-gpt-rosalind.md) 与 [Strengthening Societal Resilience with Rosalind Biodefense](strengthening-societal-resilience-with-rosalind-biodefense.md) 构成 OpenAI 生命科学叙事线:Rosalind 系列面向生物安全与国防场景,本文展示同一模型能力在民用药物发现上的应用。
- 与 [Research Acceleration: A View Inside OpenAI](research-acceleration-view-inside-openai.md) 互补:后者给出智能体集群加速内部科研的宏观图景,本文是外部实验室(宾大)复用该打法的具体案例。
- 与 [Measuring the Pace of AI Development](../../anthropic/research/measuring-pace-of-ai-development.md) 对照:度量 AI 发展节奏需要『真实任务上的加速证据』,基因组规模抗菌分子搜索正是这类可测任务。

## 资源

- 官方博客:[How a researcher uses Codex and ChatGPT to search for new antimicrobial molecules](https://openai.com/index/using-codex-chatgpt-to-search-for-new-antimicrobials)
- 相关条目:[Introducing GPT Rosalind](introducing-gpt-rosalind.md)、[Research Acceleration: A View Inside OpenAI](research-acceleration-view-inside-openai.md)
- 待补:第三方独立转载未在时限内检索到(官方 RSS 描述与文章链接已核对)

> 注:openai.com 原文 403,本文基于官方 RSS 描述整理(独立第三方转载待补),官方 URL 已列于资源。
