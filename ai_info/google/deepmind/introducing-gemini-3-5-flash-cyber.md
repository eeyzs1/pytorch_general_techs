# 发布 Gemini 3.5 Flash Cyber：轻量级网络安全模型（Introducing Gemini 3.5 Flash Cyber）

- **原文链接**: [Introducing Gemini 3.5 Flash Cyber](https://deepmind.google/blog/introducing-gemini-3-5-flash-cyber/)
- **作者**: Raluca Ada Popa, Four Flynn
- **发布日期**: 2026-07-21
- **检索日期**: 2026-08-01
- **标签**: #网络安全 #CodeMender #Gemini #垂直模型 #Google

## 核心观点

Gemini 3.5 Flash Cyber 是基于 3.5 Flash 微调的轻量级网络安全模型，专用于快速、低成本地发现、验证并修补漏洞。核心论点：AI 找漏洞的速度已超过防御者修复的速度，应对这一不对称威胁需要"高能力 + 可负担 + 可规模化"的模型——轻量模型可在同一代码库上被多次调用、扫描更多代码路径，比单次调用巨型模型更适合漏洞挖掘的搜索空间问题。

鉴于双重用途属性，3.5 Flash Cyber 采取审慎部署策略：短期内仅通过 CodeMender 以限量试点形式向政府与可信伙伴开放，后续逐步扩大；CodeMender 的基础能力也将通过 Gemini Enterprise Agent Platform 以 GA 模型直接提供给客户。

## 关键发现 / 关键技术

### 1. 基准表现
- **CyberGym**（数百个真实软件漏洞）：CodeMender 对单份报告最多调用 5 次 3.5 Flash Cyber，即取得与大得多的模型相竞争的成绩
- **Big Sleep 独立评估**（Chrome、Safari 级复杂代码库的关键漏洞挖掘，无安全护栏压测）：显著超越主线 3.5 Flash 与 3.6 Flash
- **Chrome 生产 commit 扫描流水线**（漏洞未公开、无污染）：相比 3.5 Flash 显著提升；Opus 4.6 之后的竞对新版本因内置安全护栏拒绝执行任务，未列入对比

### 2. 独特漏洞发现能力
- 在 V8 JavaScript 引擎上等调用次数对比：3.5 Flash Cyber 发现 55 个独特确认问题，主线 3.5 Flash 47 个，Claude Opus 4.6 36 个
- 其中 10 个问题是另外两个模型均未发现的；随调用次数增加仍持续发现新代码路径与漏洞

### 3. 真实世界战果
- 已在 Google 内部 Chrome、Android、Cloud、Ads、YouTube 代码库投入使用
- Google Cloud 漏洞研究团队实测：2 小时内发现公开 API 的远程代码执行漏洞和敏感生产服务的内存损坏漏洞，并生成可绕过 ASLR 与 W^X 缓解措施的 100% 可靠 RCE exploit
- Wiz 与 Cloud CISO 安全工程测试者确认其相对主线 3.5 Flash 的显著能力提升

### 4. 数据与工具壁垒
- OSV.dev 漏洞库（70 万+ 开源漏洞）与 10 余年 OSS-Fuzz 结果提供高质量训练素材
- 模型学会操作行业标准工具、阅读 Chromium 级数百万行代码项目、独立进行数小时连续深度分析

## 实践意义

这是前沿实验室首次将"网络安全专用小模型 + 多 agent 编排"完整产品化：轻量模型多次调用换搜索广度的架构，为代码审计、commit 扫描流水线提供了可负担的部署形态。"发现速度 > 修复速度"的判断也预示防御侧自动化的军备竞赛将加速；而"仅限政府与可信伙伴"的限量部署，与 OpenAI 对高能力模型的差异化访问控制形成行业呼应。

## 跨厂商对比

- 与 [Anthropic Discovering Cryptographic Weaknesses](../../anthropic/research/discovering-cryptographic-weaknesses.md) 对比：Anthropic 展示通用模型在密码学弱点发现上的前沿能力，Google 则以专用微调模型 + CodeMender 编排走工程化落地路线，一研究一产品
- 与 [GPT-5.6](../../openai/research/introducing-gpt-5-6.md) 对比：GPT-5.6 把网络安全作为旗舰模型的通用能力并对高风险能力做差异化访问，Google 直接发布垂直专用模型并限定防御方使用，治理路径殊途同归

## 资源

- CodeMender：[Introducing CodeMender](https://deepmind.google/blog/introducing-codemender-an-ai-agent-for-code-security/)
- 同日发布总览：[Gemini 3.6 Flash, 3.5 Flash-Lite, and 3.5 Flash Cyber](gemini-3-6-flash-3-5-flash-lite-3-5-flash-cyber.md)
