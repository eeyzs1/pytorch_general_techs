# 开源软件可选漏洞扫描服务上线（Launching an opt-in vulnerability-finding service for open-source software）

- **原文链接**: [Launching an opt-in vulnerability-finding service for open-source software](https://www.anthropic.com/research/launching-opt-in-vuln-finding-service-for-open-source)
- **作者**: Anthropic Frontier Red Team
- **发布日期**: 2026-10-08
- **检索日期**: 2026-10-16
- **标签**: #OSSScanner #漏洞披露 #开源安全 #CVD #模型生成报告

## 核心观点

Frontier Red Team 推出 OSS Scanner：受 Google OSS-Fuzz 启发的可选式漏洞扫描服务，用最强模型（含 Mythos）为开源项目免费做周期性深度扫描。关键设计决断是"零人工审查"——报告完全由模型生成、不经人工 triage 直达维护者，以此换取扫描速度与频率；代价是可能出错。背景数据：过去六个月发现 29,000+ 候选漏洞但人工只能消化约 6,000 个，而维护者越来越多地主动要求"把未验证的都发给我"（已直发近 5,000 份）。

信任基础来自第三方验证：专家渗透测试员复核 97 个严重/高危发现，85 个（88%）达到 CVD 披露标准，12 个中 11 个是重复已知问题、仅 1 个真正的误报——"无人工审查"的模型报告质量已接近人工门槛。

## 关键发现 / 关键技术

### 1. 漏洞发现产能与人工瓶颈
- 六个月 29,000+ 候选漏洞，人工仅 triage 约 6,000
- 近 5,000 份报告在维护者主动要求下未验证直发
- CyberGym 基准上 LLM 漏洞发现率从去年初 <20% 升至今年 >85%——维护者从收到"AI 垃圾"变为收到高质量报告

### 2. OSS Scanner 机制
- 报告含：自包含复现器、漏洞解释（尽量含引入时间的 bisect）、候选补丁
- 早期验证中数十个项目收到数百份报告，其中多个漏洞可链成未认证远程代码执行
- 维护者口碑：PostgreSQL（"异常高的发现率、修复近乎即用"）、OpenSSL（"与人写的一样好甚至更好"）、wolfSSL（74 份报告仅 2 份无效、5 个成 CVE）、curl（"近年最严重漏洞之一"）、HotCRP

### 3. 参与门槛
- 核心 maintainers 通过向 GitHub 仓库提 PR 报名，采用 OSS-Fuzz 类似标准："对基础设施与用户安全有关键影响"
- 有 triage 能力的项目走快车道；没有的仍走人工验证 CVD
- 配套：Claude for OSS 免费 Max 20x 订阅用于修复

## 实践意义

这是安全披露经济学的一次范式实验：当模型发现能力（29,000）远超人工验证产能（6,000）时，"验证后披露"必然积压，"opt-in 直发 + 让维护者自选"成为务实的分流阀。88% 的专家复核通过率说明模型报告的信号噪声比已可承受。对开源社区的动作项：符合"关键影响"标准的项目应尽快报名——在 GLM-5.3 级攻击能力开放下载的当下，防御方的时间窗口以天计。对其他 AI 公司的参照：OpenAI 的 Patch the Planet 走类似路线，"AI 找漏洞 + 免费给防御方"正在成为前沿实验室的标配公共品。

## 跨厂商对比

- 与 [Project Glasswing: Initial Update](glasswing-initial-update.md) 对比：Glasswing 是"人工验证 + 定向披露"的精耕模式，OSS Scanner 是"模型直发 + opt-in"的规模模式——同一产能瓶颈催生的两条披露流水线
- 与 [Introducing the Anthropic Cyber Mission](anthropic-cyber-mission.md) 互补：Cyber Mission 是总纲（关键基础设施 + 开源两大支柱），本文是开源支柱的首个落地产品
- 与 [Patch the Planet](../../openai/research/patch-the-planet.md) 对比：OpenAI 聚焦"发现后帮修"，Anthropic 把"未经人工验证的原始发现"也开放给有能力的维护者——披露粒度的两种取舍

## 资源

- 论文：无
- 代码：https://github.com/anthropics/oss-scanner（报名入口）
- Demo：https://red.anthropic.com/oss-scanner
