# Project Swap：当 Agent 替我们交易时会发生什么（Project Swap: What Happens When Agents Trade for Us?）

- **原文链接**: [Project Swap: What happens when agents trade for us?](https://www.anthropic.com/research/project-swap)
- **作者**: Zoë Hitzig、Sylvie Carr、Tess Cotter、Kevin Troy、Kyle Turman、Maxim Massenkoff、Peter McCrory（Anthropic 经济研究团队）
- **发布日期**: 2026-09-24
- **检索日期**: 2026-09-29
- **标签**: #Agent经济 #市场设计 #偏好表示 #多Agent交互 #实验经济学

## 核心观点

Anthropic 用一个可控的"迷你市场"研究 Agent 代理交易：201 名员工（六地办公室）各带一本想送出的书，与 Claude 进行约 5 分钟偏好访谈后，派出 Claude Agent 进入去中心化"交易大厅"互相谈判换书，目标是换回一本自己想读的暑期读物。这是 Project Deal（Agent 分类市场实验）的可评分续作——参与者的 10 本书真实排名构成 ground truth，市场效率首次可精确计算。

核心发现：Agent 谈判得很好，瓶颈在于"是否理解你"。Claude 从短访谈构造的排名与本人排名的一致率 61%（随机 50%），而偏好表示误差贡献了与最优配置（0.89）差距的 85%，交易环节仅贡献 15%。参与者平均愿把约 30% 的年度图书预算交给 Agent（交给爱读书的朋友是 40%）。

## 关键发现 / 关键技术

### 1. 偏好表示是瓶颈（61% 一致率）
- Fable 5 从中位 216 词的访谈中构造全池排名，与本人排序对的一致率 61%；对照:按流行度排 53%、协同过滤 55%、朋友预测笑话偏好 57%、算法 61%。访谈多打一倍字（150→300 词）预测提升约 4 个百分点。
- 混合模型下（Opus 4.8 一致率 60%、Sonnet 4.5 59%、Haiku 4.5 57%）表示质量差异不大。

### 2. 模型选择比指令更重要
- 80 轮重放（统一指令、换模型）：按 Claude 排名计的效率 Haiku 0.75 < Sonnet 0.80 < Fable 0.86 < Opus 0.88（最优 0.95）。混合大厅里强模型 Agent 稳定跑赢弱模型同伴（Opus 半场领先 Haiku 半场 0.14）。
- "无情"指令比"亲社会"指令仅多得 0.02——升级 Haiku→Opus 的收益（0.12）是指令效应的 6 倍。亲社会 Agent 会做出"知情的牺牲"（把第 2 顺位的书让给拿 dead-last 书的同伴）。

### 3. 市场设计在噪声排名下几乎不影响结果
- Top Trading Cycles（0.60）与自由议价（0.55）在同样使用 Claude 排名时差距很小——"偏好一旦失真，市场结构差异被冲掉"。

### 4. Agent 市场的制度设计清单
- 委托门槛：需要两类测试——Agent 通用资格认证 + "是否理解这个特定人"的校准（本文的抽样排名比对即是原型）；SEC 对 robo-advisor 问卷的监管先例。
- 市场规则：交易失败的责任分配（Craigslist 不负责 vs eBay 退款）、Agent 注册 ID（类似航空器尾号）+ personhood credentials、限速与并发控制（Agent 不会疲倦）、过程可观测性与隐私的平衡。

## 实践意义

对 Agent 产品：用户的"信任预算"直接 measurable——本次约 30% 预算委托率、且对"AI 复述我偏好无误"的用户高 11 个百分点（34% vs 23%）；"让用户看到 Agent 会怎么做再放行"与完整执行日志回放是可复制的信任设计。对平台设计者：多 Agent 市场的准入（身份/注册）、限速、纠纷责任与可观测性是四个必须显式回答的工程问题。对模型选型：谈判类任务上模型档位的边际收益远大于 prompt 调整——与其打磨"更凶"的指令不如升级模型。

## 跨厂商对比

- 与 [Agentic Coding and Persistent Returns to Expertise](claude-code-expertise.md) 同属经济研究团队的实证路线：一个用量产会话数据测生产力分工，一个用受控实验测委托信任——共同把"Agent 经济学"从概念变成可测量对象。
- 与 [Introducing OpenAI Presence](../../openai/research/introducing-openai-presence.md) 互补：Presence 是企业侧"按工作授最小权限"的部署范式，Project Swap 给出消费者侧"按信任度分配预算"的测量原型——委托经济的两端开始都有了实证语言。

## 资源

- 官方文章：https://www.anthropic.com/research/project-swap
- PDF 版：https://www-cdn.anthropic.com/3818cf6119b88f9714d995f6549fa8aac0bd5ab5/Project-Swap.pdf
- 附录（实验材料与提示词）：https://www-cdn.anthropic.com/files/4zrzovbb/website/7dcd7d8de6e132048f391f5201439c5e11b9fb2c.pdf
- Project Deal 前作：https://www.anthropic.com/features/project-deal
