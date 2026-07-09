# Anthropic Economic Index Report: Cadences

- **原文链接**: [Anthropic Economic Index report: Cadences](https://www.anthropic.com/research/economic-index-june-2026-report)
- **作者**: Anthropic Economic Research
- **发布日期**: 2026-06-26
- **检索日期**: 2026-06-29
- **标签**: #EconomicResearch #ClaudeUsage #Workweek #Rhythms #Artifacts #Compute

## 核心观点

Anthropic Economic Index 第三期报告：从"会话级"扩展到"小时级"采样，研究 Claude 使用的**节奏**（Cadences）、**产出物**（Artifacts）和**用户感知**（Perceptions）。核心结论：**Claude 的使用节奏与外部世界节奏高度同步**——工作日/周末、日内高峰、税务截止日等。**任务越有价值，使用的算力越多**——token 消耗与映射职业工资正相关。

## 关键发现

### 1. 节奏（Cadences）

#### 工作周模式
- 个人会话占比：工作日 ~35%，**周末 ~50%**
- 高收入国家这个转移最明显
- Claude Code 和 1P API 个人使用占比低，但工作-周末模式相同
- 周末最下降的 Claude Code 任务：后端架构、API 调试、数据存储
- 周末最上升的：AI Agent 设计、量化交易、游戏
- 周末创建业务的对话最多

#### 日内节奏
- 7 am：新闻请求
- 10-11 am：商务邮件高峰
- 6 pm：菜谱请求 2.3× 平均
- 5 am：睡眠建议高峰
- 晚上：媒体推荐
- 夜晚/周末的工作偏向**高薪职业**（营销经理、程序员）
- 低端职业（电话销售、文员）在夜间/周末占比下降

#### 税务截止日
- 4 月 14 日（美国截止日前一天）：税务相关会话是 5 月平均的 **8 倍**
- 4 月 16 日：急剧下降

### 2. 产出物（Artifacts）

- 93% 的会话产生某种产出物
- 最常见：解释（17%）、文档报告（15%）、指导（11%）
- 闲聊类输出（解释、指导）和书面交付物（文档、PPT）各占 ~1/3
- 代码和技术工作（应用、脚本）约 1/6

#### 用途分类
- 创意写作、指导、菜谱：80%+ 个人
- 营销内容、博客文章、数据库查询：80%+ 工作
- 计划策略、翻译：工作和个人各半

#### 算力 = 价值
- 高薪职业（市场经理 vs 编辑 $80 vs $37/h）的 token 消耗约 2.5×
- 应用构建类对话用 3× 中位数 token
- 简单解释类约 1/5
- **44% 的工资梯度由产出物类型混合解释**——高薪职业更多用算力密集型产出

### 3. 感知（Perceptions）—— Anthropic Economic Index Survey

- 4 月推出的新调查，链接到隐私保护的 Claude 使用数据
- 自动化使用程度高的用户：
  - **预期 AI 在未来一年承担更多任务**
  - **更乐观**——预期对工资、工作保障、意义都有正面影响

## 关键洞察

1. **使用节奏与外部世界同步**——Claude 已成为工作和生活的"基础设施"
2. **算力分配与价值挂钩**——token 消耗可作为工作价值的代理指标
3. **自动化越深的用户越乐观**——与"AI 替代焦虑"叙事相反
4. **周末个人使用占主导**——AI 在工作之外的渗透率比预期高
5. **高薪工作夜间/周末占比上升**——可能预示"全天候知识工作"模式

## 关键数据点

| 指标 | 数值 |
|------|------|
| 采样粒度 | 小时级（首次） |
| 个人会话占比（工作日） | ~35% |
| 个人会话占比（周末） | ~50% |
| 菜谱请求高峰（6 pm） | 2.3× 平均 |
| 税务请求高峰（4/14） | 8× 平均 |
| 产出物分类占比 | 93% 有产出 |
| 算力-工资比（市场经理/编辑） | 2.5× |
| 算力-产出物关系解释的工资梯度 | 44% |

## 相关文章

- [Agentic Coding and Persistent Returns to Expertise](claude-code-expertise.md)
- [Coding Agents in the Social Sciences](coding-agents-social-sciences.md)
- [How We Built Our Multi-Agent Research System](../engineering/how-we-built-our-multi-agent-research-system.md)