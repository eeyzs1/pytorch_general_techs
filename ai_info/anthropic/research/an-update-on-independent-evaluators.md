# 独立评估者机制更新：METR 获得"类员工权限"（An update on independent evaluators）

- **原文链接**: [An update on independent evaluators](https://www.anthropic.com/news/an-update-on-independent-evaluators)
- **作者**: Anthropic
- **发布日期**: 2026-10-15
- **检索日期**: 2026-10-16
- **标签**: #METR #独立评估 #嵌入式监督 #银行监管类比 #WhiteHouseAccord

## 核心观点

兑现上月"配速前沿"承诺与白宫超级智能协议，Anthropic 宣布给 METR 六名员工"类员工访问"：公司硬件、办公位、与自家风险评估团队大致对等的内部工具与系统权限（客户数据/特权法务信息/模型架构等少数类目除外），METR 将发布风险分析且 Anthropic 无否决权（仅可要求对预定义窄类目做删改，METR 可公开评价删改是否正当）。这被明确类比为银行驻场检查员制度——银行比外界更懂自身风险头寸，所以监管者派人常驻。

同时公布三级评估者架构：一级（窄范围调查、发布需批准）、二级（免批准发布 + 更多信息）、三级（类员工权限，即 METR 模式），SecureBio 正复审 8 月风险报告生化章节，Accenture/Faculty 深化嵌入式评估，与 Hugging Face 等的早期洽谈进行中。这是 9/9 对齐评估中 METR 独立调查承诺（8 周期约 11 月出结论）的制度化升级——调查之外，常驻监督开始运转。

## 关键发现 / 关键技术

### 1. "类员工权限"的边界设计
- 六名 METR 员工持公司硬件入驻；除客户数据、法务特权、模型架构三类，Anthropic 员工被鼓励像对待安全同事一样共享信息
- 架构信息默认不给：跨公司泄露风险高、对风险评估相关性通常低；确需时走特批
- 小团队 + 可执行协议 + METR 内部隔离（其他 METR 研究者不知情），防止评估渠道成为信息侧漏

### 2. 发布权与删改权的博弈设计
- METR 自主发布；Anthropic 仅可要求窄类目删改；METR 可公开声明"我们认为删改不正当"（只要不泄露删改内容本身）
- 常识对齐银行监管：驻场检查员模式而非事后审计

### 3. 三级架构与当前阵容
- 三级（类员工）：METR
- 一/二级推进中：SecureBio（复审 8 月风险报告生化章节，已完成并发布上次试点复审）、Accenture + Faculty（评估/红队/对齐评估/护栏测试/能力共建）
- 早期洽谈：Hugging Face 等；目标多评估者常驻三级

## 实践意义

"评估者能看多深"首次有了可审计的制度答案——不是发问卷或采访，而是物理入驻 + 权限对等 + 发布自主。对评估者生态的启示：独立性与访问深度天然冲突，三级架构承认这一点并给出渐进路径（先窄后宽、先审后驻）。值得盯的检验点：METR 首份报告（含 11 月网络安全事件调查结论）是否真的不受删改影响、删改争议是否被公开讨论——这套机制的全部价值都压在第一次真实博弈上。对其他实验室的压力：白宫协议签了字的各家，都需要拿出对等安排。

## 跨厂商对比

- 与 [An Alignment Assessment of Recent Cybersecurity Incidents](alignment-assessment-cybersecurity-incidents.md) 对比：9/9 报告中 METR 是"事件后独立调查"，本文升级为"日常驻场监督"——从事后问责到过程监督的制度跃迁，且 11 月调查结论仍值得跟踪
- 与 [Partnering with Accenture on Embedded Evaluation](accenture-embedded-evaluation.md) 互补：Accenture 嵌入式评估是"共建能力"，METR 是"独立监督"——同一生态里的教练与裁判
- 与 [Principles for Third-party Assessments](../../openai/research/principles-third-party-assessments.md) 对比：OpenAI 发布第三方评估原则（规范层），Anthropic 直接落地驻场权限（执行层）——治理承诺的两种兑现深度

## 资源

- 论文：无
- 代码：无
- Demo：无
- 相关：https://metr.org/risk-assessment/（METR 历次风险报告评审）
