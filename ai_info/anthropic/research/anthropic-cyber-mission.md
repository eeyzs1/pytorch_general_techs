# Anthropic 网络使命：关键基础设施防御计划 + OSS Scanner（Introducing the Anthropic Cyber Mission）

- **原文链接**: [Introducing the Anthropic Cyber Mission](https://www.anthropic.com/news/anthropic-cyber-mission)
- **作者**: Anthropic
- **发布日期**: 2026-10-08
- **检索日期**: 2026-10-16
- **标签**: #CyberMission #关键基础设施 #OT安全 #开源安全 #防御优先

## 核心观点

Anthropic 把散落的网络安全投入整编为长期承诺"Anthropic Cyber Mission"，首批两大支柱：关键基础设施防御计划（CIDP）——把前沿模型、驻场工程师与威胁研究带给保护 operational technology（电网/水务/交通）的可信服务商，创始伙伴 11 家（Accenture、Booz Allen、CrowdStrike、Deloitte、Dragos、Hitachi、Insane Cyber、Nozomi、Palo Alto、PwC、Rockwell）；开源软件——OSS Scanner 免费扫描 + 自动化 triage/补丁研究方向。

战略判断明确：Glasswing 证明了找漏洞的速度，但"验证、排序、修复"仍是瓶颈，OT 环境的修复窗口甚至以年/十年计。官方给出时间表预测——两年内攻守易势（AI 利好防御），但近期仍是攻强守弱。

## 关键发现 / 关键技术

### 1. CIDP 的切入方式
- 不直接服务运营商，而是服务"运营商依赖的可信服务商"：安全咨询、工业网络安防、设备制造商三类
- 已开工：多家伙伴正用 Claude 修复漏洞并帮助客户同步修复
- OT 现实约束：设备不能停机打补丁、变更风险高、专有设备——先小队列试点再扩

### 2. 从州政府到全国基础设施的递进
- 6 月起已为美国超半数州及最大公共关键基础设施运营商提供前沿模型与技术支持
- 伙伴证言聚焦"机器速度防御"：Palo Alto Unit 42、CrowdStrike、Rockwell 等均以"AI 攻击速度 vs AI 防御速度"立论

### 3. 开源支柱的路线图
- OSS Scanner（同日上线）→ 自动 triage 与补丁 → 新安全架构与编码实践研究
- 资助 Python Software Foundation、Alpha-Omma/OpenSSF、Apache、Akrites、Gold Eagle；0xDAF 基金支撑
- Claude for OSS 免费 Max 订阅 + CVP 扩展访问

### 4. 为什么是现在
- 高网络能力模型已对攻击者广泛可得（呼应 GLM-5.3 评估）
- 利用成本暴跌而修复仍靠人；Glasswing 中漏洞从发现到修复常隔数月

## 实践意义

这是"防御优先"从口号到组织化的分水岭：Anthropic 把安全产品（Claude Security）、访问计划（CVP）、基础设施伙伴（CIDP）、开源公共品（OSS Scanner/0xDAF）与资金整合为单一使命，11 家创始伙伴覆盖 OT 安全全价值链——其他实验室的安全投入多以单点产品/基金形式存在。对 OT/ICS 从业者：CIDP 是首个把前沿模型 + 驻场工程打包进工业安全服务商的方案，值得关注其"小队列学习"进展。对预测的检验标准：两年内"AI 利好防御"能否兑现，取决于修复自动化速度。

## 跨厂商对比

- 与 [Expanding the Cyber Verification Program](cyber-verification-program.md) 互补：CVP 解决"谁能用强模型"，Cyber Mission 解决"用来保护什么"——准入与使命同日发布，构成完整安全战略
- 与 [Project Glasswing: Initial Update](glasswing-initial-update.md) 对比：Glasswing 证明"找得快"，Cyber Mission 承认"修得慢"才是真瓶颈——从发现能力竞赛转向修复体系建设的战略转进
- 与 [Daybreak Securing the World](../../openai/research/daybreak-securing-the-world.md) 对比：OpenAI 的 Daybreak 走"产品化防御工具"路线，Anthropic 走"生态联盟 + 免费公共品"路线——防御优先的两种组织形态

## 资源

- 论文：无
- 代码：https://github.com/anthropics/oss-scanner
- Demo：无
- 报名：CIDP https://claude.com/form/critical-infrastructure-defense-program-interest
