# Muse Wonder：Meta 首个前沿模型，把跨会话记忆与长任务坚持机制化（Muse Wonder: A Frontier Model For Personal & Professional AI Agents）

- **原文链接**: [Muse Wonder: A Frontier Model For Personal & Professional AI Agents](https://research.meta.ai/blog/muse-wonder)
- **作者**: Meta Superintelligence Labs（MSL）
- **发布日期**: 2026-10-12
- **检索日期**: 2026-10-16
- **标签**: #MuseWonder #前沿模型 #ActiveMemory #ActiveFocus #Agent评测

## 核心观点

Meta 于 10 月 12 日发布 Muse Wonder 与 Muse Wonder Full，官方定位为"个人与专业 Agent 任务的当前最好水平"、"迈向个人超级智能的一大步"。距上代旗舰 Muse Spark 1.3 仅 6 周，Artificial Analysis Intelligence Index v4.3 达 52/56（max effort，Spark 1.3 为 48），Wonder Full 在十项评测中六项进前三。据 The Information 早前披露，该项目内部代号"Watermelon"，以约 10 倍于 Muse Spark 的算力在千兆瓦级 Prometheus 数据中心训练 14 个月。

卖点不是泛化智能而是两个机制化能力：Active Memory（跨对话按天/周/月保留并主动调取用户上下文）与 Active Focus（在困难目标上坚持——换方法、顶住阻塞、不确信时求助、有后果动作前先确认）。知识问答仍是弱项（AA-Omniscience 30，低于 Opus 5.5 的 46），但幻觉率从 33% 降至 23%。API 定价 $4/$20 每百万 token；Wonder Full 仅面向 Muse Code 订阅者。发布方式异常低调：官方博客主索引未挂出该文，经 Zuckerberg Threads 宣布、OpenRouter 直接上线。

## 关键发现 / 关键技术

### 1. Active Memory 与 Active Focus 两套机制
- Active Memory：跨对话保留关于用户的上下文，任务需要时主动调取——官方演示含从图片构建可玩的 3D 厨房小游戏、按照片下单周边、编排婚礼座位表。
- Active Focus：遇阻时尝试替代方法、根据新信息调整、不确定时请求澄清、执行有后果动作前先向人确认——把"要么放弃、要么硬闯"的默认路径改为"先换方法、再求助、最后才动手"。
- 官方评测覆盖法律、金融、健康领域：FocusBench、SWE-Marathon、LAB，法律领域使用 Harvey Legal Agent 基准；Meta 内部称两项能力超越 Claude Fable 与 GPT-6 Astra（自评，无独立验证）。

### 2. AA Intelligence Index v4.3 独立评测
- Wonder Full (max) 56 / Wonder (max) 52，较 Spark 1.3 (max, 48) 分别 +8/+4；Wonder Full 十项中六项前三：CritPt 33%（#1）、GDP.pdf 33%（#1）、GDPval-AA v2.1 1857 Elo（#2）、AA-Briefcase 1729 Elo（#3）、AutomationBench-AA 71%（#3）、SciCode 63%（#3）。
- 最大单项跃升：Terminal-Bench 4.0 从 33% 到 57%（+24pt，追平 Gemini 4 Argon）；GDPval-AA +176 Elo、AA-Briefcase +148 Elo。
- Coding Agents Index：Wonder Full 68，追平 Claude Code + Sonnet 5.5（68）、高于 Opus 5.5（66）；Wonder 63；Spark 1.3 时代为 54。
- token 效率：输出约 54k/任务（较 Spark 1.3 的 60k 再降 10%）；Full 输入 6.44M/任务，比 Wonder 的 7.69M 省 16%——更强且更省。
- 弱项与缓解：AA-Omniscience Full 30 / Wonder 25（知识面落后）；幻觉率降至 23%/27%，Full 在 45+ 分模型中第二低（仅次 Gemini 4 Argon 的 15%）。

### 3. 分层可用性与定价
- Muse Wonder：Meta Model API、OpenRouter、Vercel AI Gateway（同日上架）；$4 输入 / $0.20 缓存 / $20 输出每百万 token，较 Spark 1.3 的 $1.25/$0.15/$4.25 全面上调；1M 上下文，输入支持文本/图像/视频/音频，输出文本。OpenRouter 实测 71 tok/s、三日 99.99% 在线率。
- Muse Wonder Full：仅 Muse Code 订阅者可用（Power Usage $50/月、Maximum Usage $200/月档），不按 token 计费；两型号能力差异官方未展开。
- AA 测算：Wonder 单任务成本 $4.52（Spark 1.3 $1.60 的 2.8 倍），低于 Claude Fable 5.1（$7.63）、Opus 5.5（$5.98），高于 GPT-6.1 Sol（$0.72）、Gemini 4 Argon（$1.99）。

### 4. 安全口径与"研究面缺席"的发布方式
- Meta 称其为"迄今最对齐的模型"，强调对抗性指令鲁棒性与 CBRN、网络滥用防护，完整安全报告仅承诺"很快"发布。
- 官方博客主索引未展示该文，公告经 Zuckerberg 的 Threads 帖发出，产品面（OpenRouter 真实流量）先于研究面——Forkast 评述为"研究面为空，这个空缺本身就是故事"。

## 实践意义

对 Agent 团队：Wonder 把两个最常见的失败模式——跨天任务上下文归零、遇阻后策略退化成乱改文件——拆成有名有姓的机制，评估长任务 Agent 时应把"跨会话记忆保持"与"阻塞恢复行为"纳入测试维度。记忆内容存什么、何时失效、如何清理，官方均未说明，落地需自立规矩。订阅墙分层（API 版 vs Full 版）开创同一前沿模型双轨变现的先例，企业选型需注意两者能力差异缺乏官方披露。Active Focus 的"先确认"由模型自行触发，不能替代权限体系与 CI 审批门。

## 跨厂商对比

- 与 [Muse Spark 1.3](introducing-muse-spark-1-3.md) 对比：6 周迭代 Intelligence Index +8、Terminal-Bench +24pt，但 API 定价上调至 $4/$20、单任务成本 2.8 倍——前沿能力与使用成本同步上探，Spark 1.3 退居性价比档。
- 与 [Claude 的记忆能力全产品线落地](../anthropic/engineering/claudes-memory-works-everywhere.md) 对比：Anthropic 把记忆做在产品层（跨 Claude 全线可用），Meta 把 Active Memory 做进模型层并按"天/周/月"跨度量化——同一能力的两条实现路径。
- 与 [Meta Connect 2026](meta-connect-2026.md) 连续叙事：Connect 承诺"Agent 全天候干活"，Wonder 的 Active Focus 与 Active Memory 正是该承诺的模型层兑现——发布节奏（Connect 后 18 天）刻意衔接。

## 资源

- 论文：无（官方博客未附，完整安全报告承诺"很快"）
- 官方博客：https://research.meta.ai/blog/muse-wonder
- Demo：https://openrouter.ai/meta/muse-wonder
- AA 独立评测：https://artificialanalysis.ai/articles/muse-wonder

> 注：research.meta.ai 在本环境不可达，本文经 Artificial Analysis、Forkast、GIGAZINE、CNBC、Apifox 多源交叉验证，官方 URL 见资源；内部代号 Watermelon 说法源自 The Information 报道（经 Forkast 转述）。
