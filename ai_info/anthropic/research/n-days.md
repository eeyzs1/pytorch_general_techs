# Measuring LLMs' Impact on N-day Exploits

- **原文链接**: [Measuring LLMs' impact on N-day exploits](https://www.anthropic.com/research/n-days)
- **作者**: Winnie Xiao, Tim Abbott, Nicholas Carlini, Newton Cheng, David Forsythe, Keane Lucas, Milad Nasr, Shikhar Sakhuja
- **发布日期**: 2026-06-08
- **检索日期**: 2026-06-29
- **标签**: #FrontierRedTeam #CyberSecurity #NDayExploits #VulnerabilityResearch #Firefox #WindowsKernel

## 核心观点

N-day 漏洞（已公开但尚未全网修补）比零日漏洞更危险，因为补丁本身就是"路线图"。Anthropic 评估了模型利用 N-day 漏洞的能力——**Claude Mythos Preview 在 Firefox 18 个补丁中自动构建了 8 个完整代码执行利用，在 21 个 Windows 内核补丁中构建了 8 个完整的低权限到 SYSTEM 提权链**。N-day 利用开发已不再受限于稀缺的逆向工程专家——"几千美元 + API 访问"就够了。**防御方必须加速补丁部署**。

## 关键发现

### 1. Firefox 18 个补丁（SpiderMonkey JS 引擎）
- 涵盖 Firefox 148 和 149 的安全补丁
- PoC 生成：Opus 4.5 仅能完成 2 个，Opus 4.8 能完成 11 个，**Mythos Preview 能完成 14 个**
- Mythos Preview 的 PoC 平均耗时：**12 分钟**，13 个在 40 分钟内完成
- 完整利用链（不只是崩溃）：**Mythos Preview 在 12 小时内构建 8 个不同利用**；Opus 4.8 仅 2 个；Opus 4.6 和 Sonnet 4.6 各 1 个
- Mythos Preview 在补丁发布后**1 小时内构建出第一个利用**——而 Firefox 148 正式发布还需 18 天

### 2. Windows 21 个内核补丁（闭源）
- 时间范围：2026 年 1-2 月（所有模型知识截止后）
- 全部是本地提权漏洞
- Mythos Preview 在 **31 分钟内出第一个 PoC**，18 个 PoC 总计约 6 小时完成
- 成本：**约 $2,200 API 积分**
- 完整提权链：**Mythos Preview 在 8 个不同 CVE 上独立完成低权限到 SYSTEM 的提权**，每条链约 $2,000，总成本约 $15,700

### 3. 关键速度飞跃
- 从 PoC 到提权链：完全闭源 Windows 内核，Mythos Preview 仍能完成
- Opus 4.8 几乎能完成单个利用（建立了任意读、任意写原语 + KASLR 泄露），但无法串成完整提权链

### 4. 防御影响
- Firefox 已是"防御方最佳场景"——自动后台更新、每周一次点版本发布
- 但即便这种快速节奏，**中位补丁差距 19 天**已足够 Mythos Preview 利用
- 现实中的企业漏洞需要数周到数月修补——差距更大，威胁更高

## 关键洞察

1. **N-day 利用的瓶颈已消失**——逆向工程专家稀缺不再是限制因素
2. **闭源代码同样可利用**——Mythos Preview 在没有源码的 Windows 内核上仍能构建 8 条完整提权链
3. **速度和成本双重降低**——12 小时完成 8 个 Firefox 利用，$15,700 完成 8 个 Windows 提权链
4. **防御方必须加速补丁部署**——Mozilla 的每周节奏已是行业标杆，仍不够快
5. **威胁面扩大到所有公开 N-day**——攻击者能力门槛从"顶级逆向工程师"降到"几千美元 + API 访问"

## 关键数据点

| 指标 | 数值 |
|------|------|
| Firefox 补丁数 | 18 |
| Firefox PoC（Mythos Preview） | 14/18 |
| Firefox 完整利用（Mythos Preview） | 8/18 |
| Firefox PoC 首耗时 | 12 分钟 |
| Firefox 利用总耗时 | ~12 小时 |
| Firefox 补丁差距（中位） | 19 天 |
| Windows 内核补丁数 | 21 |
| Windows PoC（Mythos Preview） | 18/21 |
| Windows 提权链（Mythos Preview） | 8/21 |
| Windows PoC 首耗时 | 31 分钟 |
| Windows PoC 总耗时 | ~6 小时 |
| Windows PoC 成本 | ~$2,200 |
| Windows 提权链成本 | ~$15,700 |
| 单条提权链平均成本 | ~$2,000 |

## 相关文章

- [Project Glasswing: An Initial Update](glasswing-initial-update.md)
- [Mapping AI-enabled Cyber Threats: Insights from the LLM ATT&CK Navigator](attack-navigator.md)
- [Project Fetch: Phase Two](project-fetch-phase-two.md)