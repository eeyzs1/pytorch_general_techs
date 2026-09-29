# Claude 发现类 CRISPR 重复阵列的新型酶系统（Claude discovers a novel enzyme system）

- **原文链接**: [Claude discovers a novel enzyme system](https://www.anthropic.com/news/claude-discovers-novel-enzyme-system)
- **作者**: Anthropic 生命科学研究所与实验室
- **发布日期**: 2026-09-23
- **检索日期**: 2026-09-29
- **标签**: #生命科学 #AIforScience #自主发现 #逆转录酶 #CRISPR #生物安全

## 核心观点

Anthropic 宣布成立生命科学研究组与配套实验室（湾区，BSL-1/2 级，全部实验由人类执行），并发布首个科学成果：Claude agent 团队在逆转录酶（RT）序列空间的大规模普查中发现一类新酶系统，命名 ART（array-associated reverse transcriptases，阵列关联逆转录酶）。ART 主要存在于噬菌体，由 RT + 相邻伙伴基因 + 长串联重复阵列构成；实验证实阵列表达为独立小 RNA，可能像 CRISPR 一样可编程。

普查规模：约 950 个 agent 协同工作 21 小时、消耗 2.1 亿 token，普查 20 万+ 个逆转录酶、筛出 3,500 个候选系统、压缩为 20 份人类可读报告（人类同等筛选需数周至数月）。发现瞬间属于单个 agent：阅读 RT 旁侧 DNA 时识别出串联重复阵列（"这是类 CRISPR 重复阵列?!"），随后自主计数、测距、比对、检索文献并提交报告。注：华尔街见闻报道部分专家认为重要性被夸大，科学影响尚待同行评议检验。

## 关键发现 / 关键技术

### 1. 规模化普查流水线
- 约 950 个 agent、21 小时、2.1 亿 token
- 普查 20 万+ 个逆转录酶，筛出 3,500 个候选系统
- 最终压缩为 20 份人类可读报告
- 人类完成同等筛选需数周至数月

### 2. "发现瞬间"：agent 的自主验证链
- 一个 agent 阅读 RT 旁侧 DNA 时识别出串联重复阵列："这是类 CRISPR 重复阵列?!"
- 自主执行：计数重复单元 → 测量间距 → 序列比对 → 检索文献
- 最终自主提交报告，不依赖人工提示或子任务拆解

### 3. ART 系统的构成与实验验证
- 三要素：逆转录酶（RT）+ 相邻伙伴基因 + 长重复阵列
- 主要存在于噬菌体基因组
- 实验证实：阵列表达为独立的小 RNA
- 潜在意义：可能像 CRISPR 一样可编程，或成新基因组工具来源（待验证）

### 4. 工作流与制度设计
- 工作流：Claude Science + Claude Code + 自建并行 harness
- 实验室为 BSL-1/2 级，全部实验由人类执行——agent 只做计算发现
- 预印本已发布
- Feng Zhang 评价为"AI agent 助力生物学发现的激动人心例证"

### 5. 争议与限定
- 华尔街见闻报道：部分专家认为该发现的重要性被夸大
- 从"阵列表达小 RNA"到"可编程编辑工具"仍有很长的验证路径

## 实践意义

"AI 发现 + 人类验证"的分工模板首次在实验科学中完整跑通：

- 对生命科学研究：RT 序列空间此前从未被如此系统地普查，"20 份候选报告"是给人类研究者的可执行清单而非终点
- 对 AI for Science 方法论：继数学证明之后，自主科学发现范式首次接入湿实验验证闭环，agent 负责广度搜索与自主验证、人类负责实验确证
- 对机构设计：Anthropic 自建 BSL-1/2 实验室并坚持"人类执行全部实验"，为同类项目提供了可复制的治理模板

## 跨厂商对比

- 与 [Paving the Way for Agents in Biology](agents-in-biology.md) 互补：该文讨论生物学数据基础设施与工具设计，本文是该基础设施支撑下的首个标志性产出
- 与 [形式化费马大定理](formalizing-fermats-last-theorem.md) 对比：数学证明与生物发现同为自主科学发现范式，后者首次接入湿实验验证闭环
- 与 [Strengthening Societal Resilience with Rosalind Biodefense](../../openai/research/strengthening-societal-resilience-with-rosalind-biodefense.md) 对比：OpenAI 投向生物防御（守住滥用下限），Anthropic 投向发现型生命科学（拉高科学上限），两家形成互补布局
- 与同批 [Claude 如何提升生物分子建模](claude-uplifts-biomolecular-modeling.md) 互补：一个优化工具链，一个用工具链做出发现

## 资源

- 官方新闻：https://www.anthropic.com/news/claude-discovers-novel-enzyme-system
- 预印本：已发布（链接见官方页面）
- 争议报道（华尔街见闻）：见 2026-09 下旬相关报道
