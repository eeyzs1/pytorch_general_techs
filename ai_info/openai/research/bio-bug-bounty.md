# OpenAI Bio Bug Bounty：生物安全通用越狱测试计划

- **原文链接**: [OpenAI Bio Bug Bounty](https://openai.com/index/bio-bug-bounty/)
- **作者**: OpenAI
- **发布日期**: 2026-07-09
- **检索日期**: 2026-07-20
- **标签**: #BioSafety #BugBounty #Jailbreak #RedTeam #安全 #Preparedness

## 核心观点

OpenAI 将 GPT-5.5 Bio Bug Bounty 升级为持续的 OpenAI Bio Bounty Program，专注于测试能击败预定义生物安全挑战的**通用越狱**。该计划覆盖从 GPT-5.6 开始的前沿模型，奖励金额从 $25,000 提升至 $50,000。这是 AI 安全领域首个针对生物风险通用越狱的持续悬赏计划，标志着"安全悬赏"从"特定漏洞"向"系统性防御测试"的演进。

## 关键发现 / 关键技术

### 1. 通用越狱定义
- 能击败 OpenAI 预定义生物安全挑战的通用方法
- 非特定提示词或单一漏洞，而是系统性绕过防御的策略
- 覆盖 GPT-5.6 及后续前沿模型

### 2. 奖励机制
- 通用越狱奖励：$50,000（GPT-5.6 和 GPT-5.5 均适用）
- 部分成功（partial wins）可能获得较小奖励
- GPT-5.5 测试期至 2026-07-27，之后仅 GPT-5.6 在范围内

### 3. 参与流程
- 通过滚动申请流程提交申请（姓名、机构、经验）
- 入选者需签署 NDA，拥有 ChatGPT 账户
- 过往 GPT-5.5 Bio Bounty 申请者无需重新申请

### 4. 与现有安全计划的关系
- 独立于 [Safety Bug Bounty](https://bugcrowd.com/engagements/openai-safety) 和 [Security Bug Bounty](https://bugcrowd.com/engagements/openai)
- 专注于生物安全，其他计划覆盖一般安全和网络安全

## 实践意义

Bio Bug Bounty 代表了 AI 安全测试的新范式：
- **主动防御**：通过悬赏激励外部研究者发现防御弱点，而非等待恶意利用
- **通用性测试**：超越特定漏洞，测试系统性防御 robustness
- **生物安全优先级**：将生物风险与网络安全并列为最高安全优先级
- **行业标杆**：为其他 AI 公司建立生物安全测试标准

## 跨厂商对比

- 与 [Project Glasswing](../../anthropic/research/glasswing-initial-update.md) 对比：Anthropic 专注用 AI 发现软件漏洞，OpenAI 专注测试 AI 自身的生物安全防御
- 与 [Strengthening Societal Resilience with Rosalind Biodefense](strengthening-societal-resilience-with-rosalind-biodefense.md) 对比：Rosalind 是防御性生物安全研究，Bio Bug Bounty 是攻击性测试
- 与 [GPT-5.6 Preview System Card](gpt-5-6-preview-system-card.md) 互补：System Card 描述安全栈，Bio Bug Bounty 是安全栈的实战检验

## 资源

- 申请入口：[OpenAI Bio Bounty Program Application](https://openai.smapply.org/prog/gpt-5-5-safety-bio-bounty-program)
- 安全悬赏：[Safety Bug Bounty](https://bugcrowd.com/engagements/openai-safety)
- 网络安全悬赏：[Security Bug Bounty](https://bugcrowd.com/engagements/openai)
