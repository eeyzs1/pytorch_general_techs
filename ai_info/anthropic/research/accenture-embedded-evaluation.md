# 与 Accenture 合作嵌入式评估（Embedded evaluation with Accenture）

- **原文链接**: [Embedded evaluation with Accenture](https://www.anthropic.com/news/accenture-embedded-evaluation)
- **作者**: Anthropic
- **发布日期**: 2026-09-18
- **检索日期**: 2026-09-29
- **标签**: #评估 #红队 #对齐 #透明度 #安全治理 #独立评估

## 核心观点

Anthropic 于 2026-09-18 宣布与 Accenture 建立嵌入式评估合作，兑现 CEO"内部常驻评估者"的承诺。评估工作由 Accenture 旗下 Faculty 主导，覆盖模型评估与红队、对齐评估、安全防护测试，并把政企部署经验反哺到评估视角；双方未来五年各投入至少 10 亿美元。

嵌入式评估者与外部评估的关键差异在于位置与权限：在 AI 公司内部工作、接近员工权限，可观摩训练成形过程、追踪具体决策、与团队直接交谈。Anthropic 强调独立评估不减少自身责任，而是让问责"更可验证"。

资金模式上，当前由 Anthropic 直接资助，长期主张 pooled/政府资金；合作双向且非排他，目标是培育基于共享标准的评估者生态。

## 关键发现 / 关键技术

### 1. 合作内容:Faculty 主导的三类评估
- 模型评估与红队：能力边界与失败模式的系统性测试
- 对齐评估：核查模型行为与预期目标的一致性
- 安全防护测试：检验分类器、回退等防护机制的有效性
- 三类工作构成"能力—对齐—防护"的完整评估矩阵

### 2. 政企部署经验反哺
- Accenture 旗下 Faculty 主导执行，带来大规模政企部署的实战视角
- 弥合"实验室评估"与"真实部署场景"之间的落差
- 政企侧的高风险部署场景，恰是传统外部评估最难覆盖的部分

### 3. 投入规模
- 双方未来五年各投入至少 10 亿美元
- 嵌入式评估由此成为常设职能，而非项目制外聘
- 组织级投入对应常驻团队与红队基础设施的长期建设

### 4. 嵌入式评估者 vs 外部评估
- 在 AI 公司内部工作，接近员工权限
- 可观摩训练成形过程、追踪具体决策、与研究人员直接交谈
- 黑盒 API 评估难以观测训练数据与决策链，嵌入式访问弥补这一盲区
- 时间覆盖不同：嵌入式评估伴随研发全过程，外部评估集中在发布节点

### 5. 资金模式
- 当前：Anthropic 直接资助
- 长期：主张 pooled（联合资金池）与政府资金，缓解"被评估者付费"的利益冲突

### 6. 生态目标:共享标准的评估者生态
- 合作双向、非排他：Faculty 可服务其他 AI 公司，Anthropic 也可引入其他评估者
- 非排他性让同一评估者可横向积累跨厂商基线
- 共享标准之下，各家的安全声明才能横向比较

## 实践意义

第三方评估从"发布后外聘"走向"常驻嵌入式"，是"为前沿降速"诉求在组织架构上的落点：评估者能看到训练成形与决策过程，安全声明的事后可验证性显著提高。

对行业，若 pooled/政府资金与共享标准落地，评估者生态将形成类似审计行业的独立专业层级——届时"哪家模型更安全"可以从营销话术变成可比对的审计结论。

对 AI 公司自身，"独立评估不减少自身责任"的表态意味着嵌入式评估不是责任转移，而是把内部安全工作置于可验证的监督之下。

## 跨厂商对比

- 与 [Measuring the pace of AI development](measuring-pace-of-ai-development.md) 互补：同周的透明度动作一体两面——对外引入常驻第三方评估者，对内发布能力-时间度量，共同回应"前沿是否降速、如何验证"的诉求
- 与 [Alignment assessment of cybersecurity incidents](alignment-assessment-cybersecurity-incidents.md) 对比：METR 的对齐评估是事后、独立的外部调查，Accenture/Faculty 是事中、常驻的嵌入式监督，两者并行构成内外两层评估体系
- 与 [Automated researchers mitigate alignment failures](automated-researchers-mitigate-alignment-failures.md) 互补：自动化对齐研究在模型侧自我修复，嵌入式评估在组织侧外部监督——两条路线共同压缩"发现—修复"周期

## 资源

- 发布页：https://www.anthropic.com/news/accenture-embedded-evaluation
- 代码：N/A
- Demo：N/A
