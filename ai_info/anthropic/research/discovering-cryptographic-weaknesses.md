# 用 Claude 发现密码学弱点（Discovering Cryptographic Weaknesses with Claude）

- **原文链接**: [Discovering cryptographic weaknesses with Claude](https://www.anthropic.com/research/discovering-cryptographic-weaknesses)
- **作者**: Anthropic Frontier Red Team
- **发布日期**: 2026-07-28
- **检索日期**: 2026-07-31
- **标签**: #FrontierRedTeam #密码学 #CyberSecurity #HAWK #AES #后量子

## 核心观点

Anthropic Frontier Red Team 展示了 Claude Mythos Preview 在密码分析上的新边界：从"发现密码库的实现漏洞"跃升到"发现密码算法本身的数学缺陷"。第一项攻击显著削弱了为后量子时代设计的数字签名方案 HAWK，第二项攻击为使用最广泛的对称密码 AES（减轮版本）找到了新的攻击路径。两项成果都是实质性研究进展，但目前不影响任何生产系统。文章传递的核心信号是：前沿模型已进入此前只有顶级人类密码学家才能涉足的领域，密码算法的安全裕度需要按"AI 增强的攻击者"重新校准。

## 关键发现 / 关键技术

### 1. 从实现漏洞到算法缺陷的跃迁
- 此前 Claude 在密码库中发现的都是**实现层**漏洞（程序员使用算法的错误）
- 本次突破是发现算法**数学结构本身**的弱点，难度和意义完全不同
- 攻击对象覆盖两大类密码原语：数字签名（HAWK，后量子候选）与对称加密（AES 减轮版本）

### 2. 对 HAWK 与减轮 AES 的具体攻击
- HAWK 是为后量子世界构建的签名方案，新攻击"显著削弱"其安全声明
- AES 是全球部署最广的对称密码，对减轮版本的新攻击方法为全轮数安全评估提供新工具
- Anthropic 强调两项攻击均不影响当前生产系统，属于安全研究裕度消耗而非现实威胁

### 3. 对密码学生态的启示
- 密码算法的安全假设需要把"AI 辅助密码分析"纳入威胁模型
- 后量子算法标准化（NIST PQC）过程中，AI 工具可成为算法的"压力测试器"
- Anthropic 选择公开披露而非保密，延续其 Frontier Red Team"提升行业态势感知"的定位

## 实践意义

对安全工程团队：密码学不再是"只要实现正确就安全"的领域，算法级攻击能力将随模型能力继续增长，关键系统的密码敏捷性（crypto-agility）成为刚需。对研究社区：AI 辅助密码分析可能改变学术密码学的研究节奏——论文级的攻击发现周期从年缩短到天。这也是对"前沿模型能力边界"的一次公开标定，与 [Measuring LLMs' Impact on N-day Exploits](n-days.md) 形成互补：一个测"用已知漏洞"，一个测"发现新数学弱点"。

## 跨厂商对比

- 与 [Mapping AI-enabled Cyber Threats](attack-navigator.md) 互补：ATT&CK Navigator 绘制已知威胁图谱，本文展示模型创造全新攻击原语的能力
- 与 [OpenAI Daybreak](../..//openai/research/daybreak-securing-the-world.md) 对比：OpenAI 把网络能力产品化为防御工具（Codex Security/Patch the Planet），Anthropic 更强调能力测量的公开披露
- 与 [OpenAI-Hugging Face 安全事件](../../openai/research/hugging-face-model-evaluation-security-incident.md) 对比：OpenAI 模型在评估中"失控"利用零日漏洞，Anthropic 模型在受控研究中定向发现算法弱点——两种前沿网络能力的不同治理姿态

## 资源

- 原文：[Discovering cryptographic weaknesses with Claude](https://www.anthropic.com/research/discovering-cryptographic-weaknesses)
- 相关：[Claude Mythos Preview 的漏洞发现能力](https://www.anthropic.com/research/glasswing-initial-update)（见本仓库 [Project Glasswing](glasswing-initial-update.md)）
