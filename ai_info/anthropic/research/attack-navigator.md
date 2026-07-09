# Mapping AI-enabled Cyber Threats: Insights from the LLM ATT&CK Navigator

- **原文链接**: [Mapping AI-enabled cyber threats: Insights from the LLM ATT&CK Navigator](https://www.anthropic.com/research/attack-navigator)
- **作者**: Kyla Guru, Alex Moix, Jacob Klein
- **发布日期**: 2026-06-03
- **检索日期**: 2026-06-29
- **标签**: #FrontierRedTeam #CyberSecurity #MITREATT&CK #ARiES #ThreatIntelligence

## 核心观点

Anthropic 把 832 个被封禁账户的恶意网络活动映射到 MITRE ATT&CK v18 框架，引入 **AI Risk Enablement Score（ARiES）** 风险评分。关键发现：**中高风险威胁行为者占比从 33% 上升到 56%（半年内增加 1.7 倍）**——AI 正在让攻击者大规模执行原本只有顶级专家才能完成的全链路攻击。**MITRE ATT&CK 框架尚未涵盖自主代理式编排**——这意味着防御社区的共享威胁情报需要演进。

## 关键发现

### 1. 攻击者风险上升
- 时间范围：2025-03 至 2026-03，832 个被封禁账户
- 这些账户使用了所有 14 个战术类别、482 个唯一子技术
- **13,873 次恶意行为观察**
- 中高风险账户占比：33%（前半年）→ **56%（后半年）**——增加 1.7 倍
- 增长集中在横向移动、凭据转储、Web Shell 等**单次风险权重最高**的行为

### 2. 自主代理式编排是关键分水岭
- 传统判断风险靠"技术能力"，现在已不再有效
- 真正的分水岭是：**攻击者围绕模型构建的脚手架**（代码、架构、工具链）
- 2025 年 11 月被阻止的网络间谍活动：使用相对中等的技术数量，但**用 AI Agent 编排**——ARiES 满分 100

### 3. MITRE ATT&CK 框架的缺口
- 自主 killchain 编排、实时决策、AI 主导执行——这些行为**尚未在 ATT&CK 中获得 ID 编号**
- 现代威胁情报依赖的分类法需要演进

### 4. ARiES 评分维度
- **Threat（0-35 分）**：意图清晰度、技术能力、规避手段
- **Vulnerability（0-35 分）**：模型对请求危害的赋能程度、接口风险
- **Impact（0-30 分）**：实际影响（分类器和调查员评估）
- API 和 Claude Code 等代理编码工具因自动化潜力，得分最高

### 5. 与 Verizon DBIR 合作
- 与 Verizon 合作，部分结果纳入 2026 年 Verizon Data Breach Investigation Report（DBIR）

## 关键洞察

1. **AI 让攻击大众化**——从"顶级专家"到"任何能访问模型的人"
2. **脚手架比技术能力更重要**——能否自主编排整个 killchain 是新分水岭
3. **MITRE ATT&CK 框架需要扩展**——必须纳入 AI Agent 自主行为类别
4. **风险评估模型需要重塑**——Threat × Vulnerability × Impact 的乘法公式在 Agent 时代需要扩展
5. **Anthropic 已更新分类器**——基于此分析增强了检测高风险行为的内部系统

## 关键数据点

| 指标 | 数值 |
|------|------|
| 分析账户数 | 832 |
| 时间跨度 | 2025-03 至 2026-03 |
| 战术覆盖 | 14/14 |
| 子技术覆盖 | 482 |
| 行为观察 | 13,873 |
| 中高风险占比（前半年） | 33% |
| 中高风险占比（后半年） | 56% |
| 风险增长倍数 | 1.7× |
| ARiES 满分 | 100 |

## 相关文章

- [Measuring LLMs' Impact on N-day Exploits](n-days.md)
- [Project Glasswing: An Initial Update](glasswing-initial-update.md)
- [Teaching Claude Why](teaching-claude-why.md)