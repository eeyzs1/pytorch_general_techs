# 让数据为每个人工作:ChatGPT Work 的 Data agent(Now everyone can put data to work)

- **原文链接**: [Now everyone can put data to work](https://openai.com/index/put-data-to-work/)
- **作者**: OpenAI(官方博客)
- **发布日期**: 2026-09-10
- **检索日期**: 2026-09-29
- **标签**: #DataAgent #ChatGPTWork #数据分析 #自然语言BI #企业AI

## 核心观点

OpenAI 在 ChatGPT Work 中正式推出 Data agent(数据智能体):企业用户可用自然语言连接公司数据源,让智能体自主完成取数、清洗、洞察提炼,并生成交互式仪表盘(dashboard),把『人人可用数据分析』作为产品目标。这是 ChatGPT Work 自 7 月发布以来最重的能力补强之一。

它与同期发布的 Agents API、GPT-6 Astra 形成组合拳:底层是 Astra 的推理与工具调用,中层是托管智能体编排,应用层是 Data agent 这样的开箱即用角色。产品逻辑对标企业 BI + 分析师的日常工作流(Tableau/Power BI 生态),但以对话驱动、免 SQL 门槛为核心卖点。

## 关键发现 / 关键技术

### 1. Data agent 的能力闭环
- 自然语言连接公司数据源。
- 自主完成:取数 → 清洗 → 洞察提炼 → 生成交互式仪表盘。

### 2. 三层架构组合拳

| 层 | 组件 | 角色 |
|----|------|------|
| 底层 | GPT-6 Astra | 推理与工具调用 |
| 中层 | Agents API | 托管智能体编排 |
| 应用层 | Data agent | 开箱即用的数据角色 |

### 3. 生态配套
- 同期 09-16 发布『How to connect AI usage to business value』,帮管理者度量这类智能体带来的实际业务价值。

### 4. 部署必答题
- 数据权限与行级安全:哪些数据源、哪些粒度可被 Data agent 触达。
- 智能体数据外发管控:仪表盘分享、导出与跨系统流转的边界。

## 实践意义

1. **长尾分析分流**:数据团队应关注 Data agent 对企业内『长尾分析需求』的分流效应,把人力集中到高价值建模。
2. **权限成为必答题**:数据权限、行级安全与智能体数据外发管控是新的部署必答题。
3. **BI 生态冲击**:对话驱动 + 免 SQL 门槛直接切 Tableau/Power BI 的入口流量。
4. **度量配套**:用使用分析把『采用率』连接到真实业务成果,避免为用而用。

## 跨厂商对比

- 与 [ChatGPT Work:跨应用 Agent,将目标转化为完成的工作](chatgpt-work-partner.md) 构成前后篇:7 月发布 ChatGPT Work 平台,9 月的 Data agent 是其最重的能力补强。
- 与 [Claude Cowork 与聊天合并为一个 Claude](../../anthropic/engineering/cowork-is-now-claude.md) 对比:Anthropic 把数据分析纳入 Claude 的工作界面,OpenAI 以专职 Data agent 角色切入;两家都在把『对话式分析』做成企业入口。
- 与 [Introducing the Agents API](introducing-the-agents-api.md) 互补:Data agent 是托管编排层上的第一个官方开箱即用角色。

## 资源

- 官方博客:[Now everyone can put data to work](https://openai.com/index/put-data-to-work/)
- 相关条目:[ChatGPT Work:跨应用 Agent,将目标转化为完成的工作](chatgpt-work-partner.md)、[Introducing the Agents API](introducing-the-agents-api.md)
- 第三方信源:待补(独立第三方报道未在时限内检索到)

> 注:openai.com 原文 403,本文基于官方 RSS 描述整理(第三方独立信源待补),官方 URL 已列于资源。
