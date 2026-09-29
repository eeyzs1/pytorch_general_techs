# Claude Opus 5.5 发布：Opus 成本下探 Fable 水平（Introducing Claude Opus 5.5）

- **原文链接**: [Introducing Claude Opus 5.5](https://www.anthropic.com/claude-opus-5-5)
- **作者**: Anthropic
- **发布日期**: 2026-09-22
- **检索日期**: 2026-09-29
- **标签**: #ClaudeOpus55 #模型发布 #AgenticCoding #行为审计 #双刃剑能力 #定价

## 核心观点

Claude Opus 5.5 是 Anthropic 5.5 家族首款模型（2026-09-22 发布），核心主张是"以 Opus 的成本获得 Fable 级智能"：大多数工作达到 Fable 5.1 水平，总成本却比 Opus 5 低约 40%。

价格与速度：输入 $4 / 输出 $20 每百万 token（降 20%）、缓存读 $0.20（降 60%）、输出提速 30% 以上。订阅侧同步放宽：五小时限额上调，且用户可自选时机重置限额。

这是 Anthropic 表达"为前沿降速"呼吁之后的首个发布，发布前经过 Frontier Design 与 METR 的外部评估。自动行为审计成绩为迄今最佳：不可逆与越界行动更少、抗提示注入优于 Opus 5，且测试范围扩展到更长任务、不可能任务与真实事件情景。

生物与网络攻击能力已与 Mythos 5.1 相当，因此出厂即配备 Fable 5.1 级防护——生物学风险经 LSVP、网络风险经 Cyber Verification Program 管理，把"高能力"与"强防护"绑定交付。

## 关键发现 / 关键技术

### 1. 定价与效率:Opus 成本下探 Fable 水平
- 5.5 家族首款模型；大多数工作达 Fable 5.1 水平，总成本比 Opus 5 低约 40%
- API 定价：输入 $4 / 输出 $20 每百万 token，较 Opus 5（$5/$25）降 20%
- 缓存读降至 $0.20（Opus 5 为 $0.50），降 60%——长上下文工作流的账单主力项显著下降
- 输出速度提升 30% 以上
- 订阅：五小时使用限额上调，用户可自选时机触发限额重置

### 2. 基准成绩
- Terminal-Bench：66.4%（终端环境长时程 agentic 任务）
- FrontierCode：54.4%（前沿编码基准）
- GDPval-AA：1846（专家级知识工作基准）
- HLE（带工具）：67.7%
- 基准之外，官方同样以自动行为审计与实战案例作为能力证据

### 3. "为前沿降速"后的首个发布：评估先行
- 这是 Anthropic 公开呼吁"为前沿降速"之后的首个模型发布
- 发布前经过 Frontier Design 与 METR 的外部评估
- 自动行为审计成绩为迄今最佳：更少不可逆行动与越界行动，抗提示注入优于 Opus 5
- 审计测试范围扩展：更长任务、不可能任务（impossible tasks）、真实事件情景

### 4. 双刃剑能力与出厂防护
- 生物与网络攻击能力已与 Mythos 5.1 相当
- 出厂即配 Fable 5.1 级防护：生物学场景经 LSVP 受控开放（见 [生命科学访问计划 LSVP 公测](life-sciences-verification-program.md)），网络场景经 Cyber Verification Program
- 高风险能力由此全部收敛到受控授权通道，而非默认放开

### 5. 实战案例
- 一天内完成 68 万行代码迁移
- 20 万行代码审计 3 小时完成；Opus 5 完成同样审计需 20 小时、2.5 倍 token
- HAProxy C→Rust 迁移 9.5 小时完成，成本比 Fable 5.1 低 51%
- 网页优化任务 40 次尝试成功 39 次

### 6. 输出风格:把最重要的信息放前面
- 模型被引导"把最重要的信息放前面"，便于人工核查其输出
- 对长报告、迁移方案类任务，审核者可优先验证关键结论，而不必通读全文
- 可审计性由产品行为直接承载，而非依赖事后工具

## 实践意义

Opus 5.5 把旗舰竞争进一步压到"智能/成本"曲线上：两个月内从 Opus 5 的"半价逼近 Fable"推进到"约六成成本达 Fable 5.1 水平"，大型代码迁移与审计的经济性被重新定义（68 万行/天、20 万行审计 3 小时）。

安全设计同样关键：双刃剑能力与出厂防护绑定，高风险用途只能经 LSVP/CVP 等受控通道获取；"把最重要的信息放前面"的输出约定，则让 agentic 工作流中的人工审核成本可控。

## 跨厂商对比

- 与 [Claude Opus 5](claude-opus-5.md) 对比：前代主打"半数价格逼近 Fable 5"（输入 $5 / 输出 $25），本代进一步降至 $4/$20、缓存读降 60%，防护升级到 Fable 5.1 级——能力、价格、防护三线并进
- 与 [GPT-6 Astra](../../openai/research/gpt-6-astra.md) 对比：2026 年两家旗舰都在性能之外强调安全交付；Opus 5.5 以"出厂防护 + 受控通道"管理与 Mythos 5.1 相当的双刃剑能力，把风险治理前置到发布时点
- 与 [生命科学访问计划 LSVP 公测](life-sciences-verification-program.md) 互补：Opus 5.5 的生物学防护开放通道由 LSVP 承接，模型发布与访问计划同一周落地，形成"能力 + 通道"的配套发布
- 与 [Measuring the pace of AI development](measuring-pace-of-ai-development.md) 互补：后者提供能力-时间度量框架，Opus 5.5 是"为前沿降速"呼吁后的首个新数据点——降的是风险能力推进，智能/成本曲线仍在快速下探

## 资源

- 发布页：https://www.anthropic.com/claude-opus-5-5
- 外部评估机构：METR（https://metr.org）
- 代码 / Demo：N/A
