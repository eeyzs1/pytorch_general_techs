# 用 Claude 自动化评估设计与爬山优化（Automating eval design and hillclimbing with Claude）

- **原文链接**: [Automating eval design and hillclimbing with Claude](https://claude.dev/blog/automating-eval-design-and-hillclimbing/)
- **作者**: Lance Martin
- **发布日期**: 2026-09-28
- **检索日期**: 2026-10-16
- **标签**: #评估设计 #爬山优化 #过拟合 #claude-api技能 #LLM评审

> 补录说明：本文发布于 2026-09-28（锚点当日，上次同步 09-29 检查时漏收），本次补录入库。

## 核心观点

把"好评估长什么样"与"怎么对着评估优化而不自欺"两套方法论装进 claude-api skill：/claude-api build-eval 在你的代码库里访谈式建评估（生产转录优先 → 工单 → 手写 → 合成），/claude-api hillclimb 每轮只提一个可归因的改动，靠 train/test 分割与"只有 train 涨就回滚"的规则对抗过拟合。

好评估四要素：镜像生产分布、更强模型/更多思考应当更好、前沿有及格余量（最强模型不到 100%）、轮间方差低。反采样的警告尤为深刻：按"今天模型失败"挑案例是在采样该模型能力曲面的谷底——评估测到的是模型的失败指纹而非任务本身的难度。

## 关键发现 / 关键技术

### 1. build-eval 流水线
- 输入采样顺序：生产转录（问留存与敏感数据）→ bug 报告/工单 → 手写 5–10 例 → 代码库合成
- grader 选最便宜够用的：输出受限用程序化校验；开放输出用 LLM-as-judge（rubric 写成可核查断言而非 1–5 分；有基线时做随机顺序盲选）；judge 模型不得是被测模型
- 诊断三查：同输出两次评分是否一致（grader 稳定性）、超时/API 错误（管道噪声）、基线 ≥95% 即警告改爬山目标为成本/延迟

### 2. hillclimb 机制与防过拟合
- 可改面：系统提示、skills、工具描述、模型/effort 等 API 参数、harness 代码——优先选"便宜可迭代且分数可归因"的面（文本类）
- 三防：train/test 随机分割；失败转录内容绝不粘进提示词；答案结构性隔离（防 reward hack 直取答案）
- 噪声门槛：开局检查"评估噪声 < 你会据以行动的最小改进"，否则建议加重复/案例
- 停滞 2–3 轮触发根因分桶：把剩余失败按原因排序（区分歧义案例/harness 错误/方差），只把合法失败带入后续轮

### 3. 两组实测
- 成本向：44 工单客服基准，Opus 4.8 high 起步 74.4%/$4.6 每单 → 审计提示词 + 降 Opus 5.5 low（87.8%/$1.9）→ 降 Sonnet 5 low（88.9%/$1.0）→ 加路由规则（98.9%）——留出 14 单上 90.5% vs 78.6%，成本约 1/5
- 性能向：claude-api skill 自评 66% → 补 8 个特性文档 74% → 修 C#/Java 类型表 77% → 停滞分桶发现"内容在但模型写旧 API 形状"→ 加新旧映射表 80% → 修歧义任务与错误 grader → ~88%

## 实践意义

"评估即知识产权"从口号变成可执行命令。三个最可复用的机制：train 涨 test 不涨即回滚（过拟合的在线检测器）；失败根因分桶（区分"内容缺失"与"模型写旧形状"后者的修法是加映射表而非堆内容）；成本向爬山在饱和评估上依然有效（保持质量降成本的搜索空间永远存在）。对团队 adopting 的路径：先 build-eval 把存量工单变成评估集，再让 hillclimb 跑夜间任务，人只审最终报告。

## 跨厂商对比

- 与 [Demystifying Evals for AI Agents](demystifying-evals-for-ai-agents.md) 衔接：evals 圣经给出八步路线图与三种评分器，本文把其中"设计+迭代"两步自动化——方法论与工具化的接力
- 与 [Reducing Cost and Improving Performance with Claude Platform](reducing-cost-and-improving-performance-with-claude-platform.md) 对比：降本篇给出 prompt-audit 的单点结果（-14.6%/+5.3%），本文展示同一基准上的完整爬山轨迹（74.4%→98.9% 且成本降 4/5）——快修与系统优化两种深度
- 与 [Designing AI-Resistant Technical Evaluations](designing-ai-resistant-technical-evaluations.md) 互补：AI 抗性评估讲"评估不被模型攻破"，本文讲"评估不被自己人过拟合"——评估完整性的外防与内防

## 资源

- 论文：无
- 代码：https://github.com/anthropics/skills/tree/main/skills/claude-api
- Demo：无
