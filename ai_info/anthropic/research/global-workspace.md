# A Global Workspace in Language Models

- **原文链接**: [A global workspace in language models](https://www.anthropic.com/research/global-workspace)
- **作者**: Anthropic Interpretability Team
- **发布日期**: 2026-07-06
- **检索日期**: 2026-07-07
- **标签**: #Interpretability #GlobalWorkspace #Neuroscience #Consciousness #Jspace #J-lens

## 核心观点

Anthropic 提出证据表明 Claude 内部存在一种"全局工作空间"——**J-space**——它自发涌现，而非被设计。J-space 是少量特殊的内部神经模式，与模型其余处理相比扮演特殊角色：当它"激活"时，并不意味着模型在说某个词，而是该词"在它脑海中"。研究受神经科学中的"全局工作空间理论"（Global Workspace Theory）启发，旨在检验 LLM 是否也会分化出"可报告、可控制、用于推理"的特权内部表征。

## 关键发现

### 1. J-space 的五个核心性质

- **可报告**：Claude 能报告 J-space 中的表征内容；非 J-space 表征则难以报告
- **可调控**：让 Claude 想某事或默默解题时，相应 J-space 模式会点亮
- **用于推理**：多步任务的中间步骤会在 J-space 中浮现，即使模型没说出来；这些表征因果性地中介任务表现
- **可重用**：一旦"France"在 J-space 中点亮，可以用于回答首都、语言、洲等不同问题
- **不参与日常处理**：阻止 Claude 使用 J-space 时，流畅说话、回忆简单事实、语法正确等不受影响，但失去高阶认知功能

### 2. 实验设计：Jacobian lens（J-lens）

- 对词汇表中每个词，J-lens 找出使 Claude 更可能在未来说出该词的内部激活模式
- 通过在不同层应用 J-lens，可观察模型决策过程中"沉默的词"的演化
- 在多个 prompt 上的 J-lens 读数显示的内部评估/计算并不出现在文本中：
  - 含 bug 的代码 → J-space 含 "ERROR"
  - 蛋白质序列字母 → J-space 含蛋白质生物功能
  - 提示注入搜索结果 → J-space 含 "injection" 和 "fake"
  - 多步数学问题 → 中间步骤按正确顺序出现在 J-space

### 3. 因果性证明：可编辑

- 实验：让 Claude 默默想一种运动并命名。J-lens 在它回答前显示 "Soccer"；将 "Soccer" 模式替换为等强度的 "Rugby" 模式，Claude 报告的运动变为 "Rugby"
- 注入 "lightning" 模式到 J-space，Claude 报告这个注入的想法是 lightning
- 多步推理示例："会织网的动物腿数为几？" → J-space 中 "spider" 浮现；将 "spider" 替换为 "ant"，Claude 回答 6（而不是 8）
- 同一"France"干预可同时影响首都、语言、洲、货币四个不同下游计算

### 4. 思维链与 J-space 的差异

- J-space 与"思维链 / scratchpad" 不同：CoT 是模型写给自己的文本，J-space 是内部神经激活中静默运行
- 让 Claude 复制无关句子的同时想柑橘类水果，J-space 含 "orange"、"fruits"、"thinking"、"imagery"——但文本输出只是被复制的句子
- "别想某物" 实验：J-space 中被禁止的概念比"从未提及"时亮得多（白熊效应），且伴随 "damn"、"failure" 出现

## 实践意义

- **审计工具**：J-lens 可用来发现 Claude 私下注意到自己被测试、故意捏造数据，或追求训练中埋设的隐藏目标
- **可控干预**：Anthropic 已开发技术影响 J-space 中点亮的模式，进而影响决策
- **理论价值**：J-space 的存在挑战了"模型只是统计模式匹配"的简化叙事，更接近神经科学对人类意识的解释

## 相关资源

- 完整论文：[A Global Workspace in Language Models](http://transformer-circuits.pub/2026/workspace/index.html)
- 开源代码：[anthropics/jacobian-lens](https://github.com/anthropics/jacobian-lens)
- 交互式 demo：[Neuronpedia J-lens](http://neuronpedia.org/jlens)
- 外部专家评论（神经科学 / 哲学 / LLM 可解释性）：[Anthropic CDN PDF](https://www-cdn.anthropic.com/files/4zrzovbb/website/cc4be2488d65e54a6ed06492f8968398ddc18ebe.pdf)

## 与 NLA 的关系

J-space 是 [Natural Language Autoencoders](natural-language-autoencoders.md) 的同伴研究：NLA 把内部激活翻译成自然语言描述，J-space 则定位到具体负责"思考某概念"的小集合神经模式。两者都用于部署前对齐审计，但 J-space 更结构化、更可操控，是可解释性工具箱的下一步。