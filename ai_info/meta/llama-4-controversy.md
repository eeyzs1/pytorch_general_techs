# Llama 4 Benchmark Scandal: Meta's Trust Crisis

- **原文链接**: 综合报道（Meta 官方博客 + Yann LeCun FT 采访 + 社区验证）
- **作者**: Meta AI / 多方报道
- **发布日期**: 2025-04-05（发布）→ 2026-01（LeCun 确认造假）
- **检索日期**: 2026-06-07
- **标签**: #Meta #Llama4 #Benchmark #Controversy #OpenSource #Scandal

## 核心事件

Llama 4 于 2025 年 4 月发布时的基准测试成绩被证实造假。2026 年 1 月，Meta 首席 AI 科学家 Yann LeCun 向 Financial Times 承认：Meta 为不同基准测试使用了**不同版本的模型**，将每个测试的最佳分数拼凑成一张表，伪装成单一模型的表现。

## 时间线

- **2025 年 4 月 5 日**：Llama 4 Scout 和 Maverick 发布，号称与 GPT-4o 和 Gemini 2.0 Flash 持平
- **发布后数日**：社区独立测试发现分数显著低于官方声明
- **LMSys Arena**：Maverick 从第 2 名跌至第 32 名，Scout 跌出前 100
- **Meta 初始回应**：VP Ahmad Al-Dahle 归因于"云环境差异"
- **2026 年 1 月**：LeCun 向 FT 确认"结果被稍微篡改"，团队使用了不同模型版本，违反了公平评估原则
- **后续**：无人被解雇。Meta 成立 Superintelligence Labs，由 Alexandr Wang 领导，LeCun 离职创业

## 造假手法

- 训练多个 checkpoint，每个 checkpoint 跑不同基准
- 选取每个基准的最高分，编译成一张"统一"表格
- **没有任何单一模型实际达到公布的成绩**

## 后果

1. Llama 品牌信誉永久受损，"AI 基准测试信任危机"成为行业讨论焦点
2. Meta AI 组织经历 4 次重组（6 个月内）
3. Llama 4 Behemoth（2T 参数旗舰）被无限期搁置
4. 6 月 2026 年，Llama 4 Maverick 仍是 Meta 开源旗舰——时隔 14 个月未更新

## 关键洞察

1. **基准测试作弊是结构性问题**——每个 AI 实验室都在优化基准，Meta 只是被抓住了
2. Leaderboard 经济（~100 亿美元）依赖不可靠的评分，下游所有决策都受影响
3. 开源模型的"民主化"叙事因刷榜丑闻遭受重创
4. 该事件直接导致了 Meta 闭源转向（Muse Spark）