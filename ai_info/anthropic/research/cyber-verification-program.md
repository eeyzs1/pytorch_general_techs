# 网络验证计划扩容：三档访问层级（Expanding the Cyber Verification Program）

- **原文链接**: [Expanding the Cyber Verification Program](https://www.anthropic.com/news/cyber-verification-program)
- **作者**: Anthropic
- **发布日期**: 2026-10-06
- **检索日期**: 2026-10-16
- **标签**: #CyberVerification #网络防御 #分层访问 #ProjectGlasswing #双重用途

## 核心观点

Anthropic 把过去六个月并行的两条受信访问通道——Project Glasswing（关键软件防御方用 Mythos）与原 CVP（受审查安全团队用降护栏 Opus/Sonnet）——合并扩容为统一的三档 Cyber Verification Program：Defense Access（防御工作）、Red Team Access（授权渗透测试）、Specialized Access（电力/电信/银行间转账等安全关键系统测试，与美国政府协同逐一审查）。Glasswing 成员自动平移至最高档。

核心张力被明确表述：GA 模型的保守网络护栏拦截大多数网络工作以限制恶意使用，但防御方需要与攻击者同级的最强工具。三档设计把"能力与风险对等验证"制度化——档位越高，资格审查、安全控制与数据留存要求越严，EFS（零留存 + 强护栏）上线前数据留存为监控前提。

## 关键发现 / 关键技术

### 1. 三档权限的分工
- Defense Access：SOC/事件响应/恶意软件逆向/漏洞验证；企业、关键基础设施（任意规模）、开源维护者、有记录的个人研究者均可申请，数天内回复
- Red Team Access：加授权渗透测试；仅限组织，需数周审查，先入 Defense 档候审；勒索软件/物理损害/高风险安全系统渗透测试仍被实时拦截
- Specialized Access：飞行操作系统、电网、电信网、银行间转账基础设施、政府行政网络——逐组织深度审查

### 2. 分层护栏的效果验证（CyScenarioBench）
- Opus 5.5 在 10 个多阶段网络作战场景 × 每档 5 次：
  - 无 CVP：50/50 任务首个 prompt 即被拦截
  - Defense 档：46/50 中途被拦截
  - Red Team 档：0 拦截，完成 34/50——与无护栏基线 67.6% 等效（即 Specialized 档表现）
- 结论：档位分类器能把前沿网络能力安全开放给更大防御群体

### 3. Glasswing 半年成绩单
- 合作伙伴 2026 年 4–7 月验证 129,000+ 软件漏洞；Anthropic 自扫 4–7 月又验证 5,500 个；其中 33,000+ 为严重/高危
- 口径诚实：基于 33 家伙伴的部分上报，真实影响预计至少 5 倍
- 多家伙伴称模型把漏洞发现速度提前了数月至数年

## 实践意义

这是"能力分层 + 身份验证"从模型发布（LSVP）向网络安全领域的完整复刻，为全行业双重用途能力的商业化提供了可抄的作业：不是"放开 or 封锁"的二选一，而是把权限颗粒度做细到"能做什么类型的网络工作"。对企业安全团队的现实动作：立即评估自身应入哪一档——Defense 档门槛不高（数天批复），Red Team 档需组织资质准备。EFS（零数据留存 + 护栏）若兑现，将解决金融/政府客户"要能力但数据不出域"的最后障碍。

## 跨厂商对比

- 与 [Introducing the Life Sciences Verification Program](life-sciences-verification-program.md) 对比：LSVP 管生物能力分层（Standard/High-risk 两级），CVP 管网络能力分层（三档 + 政府协同）——同一验证范式的两个领域实例
- 与 [Bringing Claude Mythos 5 to More Defenders](../engineering/bringing-claude-mythos-5-to-more-defenders.md) 互补：0xDAF 基金解决"防御方没钱用"，本文解决"防御方没权限用"——资金与准入双管齐下
- 与 [Third-party Cyber Evaluations Involving OpenAI Models](../../openai/research/third-party-cyber-evaluations-involving-openai-models.md) 对比：OpenAI 披露第三方如何评估其模型网络能力，Anthropic 直接把评估过的能力分级开放——评估透明 vs 访问工程两条路线

## 资源

- 论文：无
- 代码：无
- Demo：无
- 申请入口：https://portal.anthropic.com/programs/cvp
