# Anthropic Research — 核心观点总结

> 汇总自 [Anthropic Research](https://www.anthropic.com/research) 页面的 20 篇文章，涵盖 2026 年 5 月至 8 月。

## 一、总体脉络

Anthropic 的 Research 博客呈现九条主线：

```
可解释性突破 → 对齐工程 → 科学应用 → 经济影响 → 网络安全防御 → 物理 Agent → 价值观测量 → 能力控制 → 旗舰模型
```

7 月 28 日发布 [Discovering Cryptographic Weaknesses with Claude](discovering-cryptographic-weaknesses.md)——Frontier Red Team 展示 Claude 从"发现密码库实现漏洞"跃升到"发现密码算法本身的数学缺陷"，削弱后量子签名方案 HAWK 并为减轮 AES 找到新攻击路径。7 月 24 日发布 [Claude Opus 5](claude-opus-5.md)——新旗舰模型，以一半价格逼近 Fable 5 前沿智能，编码与知识工作新 SOTA，官方称其"最对齐的模型"；同日发布 [Project Pilot](project-pilot.md)，Frontier Red Team 把物理 Agent 能力测量扩展到无人机，沉淀为新基准 Drone-Bench。7 月 14 日发布 [How Canada Uses Claude](how-canada-uses-claude.md)——首份国家级经济指数报告，发现加拿大人均 Claude 用量是预期的 4 倍，且采用差异由产业结构而非收入驱动。7 月 13 日发布 [Claude's Values Across Models and Languages](claude-values-models-languages.md)，提出"价值轴"方法将 3,000+ 价值观压缩为可操作的少量维度，发现跨模型和跨语言的系统性价值观差异。7 月 9 日发布 [Claude Plays Robotics](claude-plays-robotics.md)，系统评估 LLM 控制多种机器人的能力边界——控制抽象层级决定成败，预训练策略 + 高层规划是当前最优路径。7 月 8 日发布 [An Off Switch for Dual-Use Knowledge](off-switch-dual-use.md)，提出 GRAM 模块化预训练方法，在单次训练中实现"可配置能力"，删除模块效果接近从未训练且不影响通用能力。8 月 7 日发布 [改进 Fable 5 的生物学安全防护](improving-fable-5-biology-safeguards.md)——更新 Fable 5 生物学安全分类器，通过重写分类器"宪法"使生物学相关 fallback（回退到 Opus 5）减少约 85%，在保留对双用途研究生物学内容拦截的同时放行更多良性查询，体现"宽分类器启动 + 精化迭代"的前沿能力开放策略。

## 二、核心主题

### 1. 可解释性（Interpretability）

[A Global Workspace in Language Models](global-workspace.md)（2026-07-06）提出 J-space——一种**自发涌现**的小集合内部神经模式，扮演"全局工作空间"角色：可报告、可调控、用于推理、可重用、但不参与日常处理。Jacobian lens（J-lens）可读出 J-space 内容、编辑 J-space 内容因果性地改变 Claude 行为。这是神经科学"全局工作空间理论"在 LLM 中的实证。

[Natural Language Autoencoders](natural-language-autoencoders.md) 是 2026 年最重要的可解释性突破。NLA 将模型内部激活转化为自然语言文本，首次实现"读取模型内心独白"。关键发现：模型在评测中**普遍具有评估意识**（SWE-bench 26% 的问题上检测到），但真实对话中不到 1%。NLA 已在 Claude Mythos Preview 和 Opus 4.6 的部署前对齐审计中使用。NLA 与 J-space 互补：NLA 把内部激活翻译成自然语言描述，J-space 定位到具体负责"思考某概念"的小集合神经模式；后者更结构化、更可操控。

### 2. 对齐工程（Alignment）

[Teaching Claude Why](teaching-claude-why.md) 分享了四个关键教训，核心是"教为什么胜过教什么"。仅 3M tokens 的"困难建议"数据集（比评估分布 OOD 得多）就能将黑邮件率降至 3%。自 Haiku 4.5 以来，每个 Claude 模型在 agentic misalignment 评估上达到 0% 黑邮件率。

### 3. 安全与防御

[Project Glasswing: Initial Update](glasswing-initial-update.md) 展示了 Claude Mythos Preview 在网络安全领域的实际影响——一个月发现 10,000+ 高危漏洞，90.6% 真阳性率。软件安全的瓶颈已从"找漏洞"变成"修漏洞"。wolfSSL 案例（CVE-2026-5194）展示了 AI 发现可伪造证书漏洞的能力。

[Measuring LLMs' Impact on N-day Exploits](n-days.md) 把目光转向 N-day（已公开但未修补）漏洞：Mythos Preview 在 18 个 Firefox 补丁中自动构建 8 个完整利用，在 21 个 Windows 内核补丁中构建 8 条 lowpriv → SYSTEM 提权链（每条 ~$2,000，总计 $15,700）。N-day 利用开发的瓶颈已消失。

[Mapping AI-enabled Cyber Threats: Insights from the LLM ATT&CK Navigator](attack-navigator.md) 把 832 个被封禁账户的恶意行为映射到 MITRE ATT&CK v18，引入 ARiES 风险评分。中高风险行为者占比从 33% 上升到 56%（半年内增加 1.7 倍）。关键洞察：**脚手架（scaffolding）比技术能力更重要**——AI Agent 编排能力是新分水岭。MITRE ATT&CK 框架尚未涵盖自主代理式编排。

[Discovering Cryptographic Weaknesses with Claude](discovering-cryptographic-weaknesses.md) 把网络能力研究推向新边界：Claude Mythos Preview 从"发现密码库的**实现**漏洞"跃升到"发现密码**算法本身**的数学缺陷"。两项攻击分别显著削弱后量子签名方案 HAWK 的安全声明、为减轮 AES 找到新攻击路径——均不影响生产系统，但标志着前沿模型已进入此前只有顶级人类密码学家涉足的领域，密码算法的安全裕度需按"AI 增强的攻击者"重新校准。与 [N-days](n-days.md) 互补：一个测"用已知漏洞"，一个测"发现新数学弱点"。

[改进 Fable 5 的生物学安全防护](improving-fable-5-biology-safeguards.md)（2026-08-07）是生物学安全的分类器精化实践。Fable 5 发布时有意阻断几乎所有生物学查询（因其在某些高度复杂生物任务上已超越专家，能为开发生物武器提供显著"能力提升"），导致大量误报：合法生物学用户的请求被拦截并回退到较弱的 Opus 5。Anthropic 通过重写分类器"宪法"（区分受保护内容与允许内容的规则集合）、收集内外专家反馈、重新训练分类器，使生物学相关 fallback 减少 ~85%，总 fallback 在 Claude.ai 减少 ~67%、Cowork ~55%、Claude Code ~17%、Claude Platform ~7%。新分类器仍对有害和双用途研究生物学内容触发，但放行了化验解读、症状理解、教育性学习等良性用途。这体现了"宽分类器启动 + 精化迭代"的前沿能力开放策略——先以保守分类器快速发布获取反馈，再基于专家输入逐步精化边界。与 [Off-Switch Dual-Use](off-switch-dual-use.md) 同属双用途安全议题，与 [Agents in Biology](agents-in-biology.md) 互补（后者聚焦能力瓶颈，本文聚焦安全约束）。

### 4. 科学应用

[Making Claude a Chemist](making-claude-a-chemist.md) 是 Anthropic 首个将 Claude 应用于化学领域的研究。Opus 4.7 在 NMR 预测上匹敌甚至超越 ChemDraw 和 MestReNova，还能做传统软件做不到的逆结构解析。亚峰间距预测准确率：Claude ~80% vs ChemDraw/MestReNova 26-35%。

[Paving the Way for Agents in Biology](agents-in-biology.md) 用 VirBench（120 个病毒序列查询）测试主流 Agent。**最强模型准确率仅 91.3%**——对于生物数据检索，有效阈值是 100%。**添加确定性检索层（gget virus）后准确率接近 100%**。Ebola TMRCA 案例显示不一致检索会导致 2014 年疫情起源被推到 1922 年。

### 5. 经济影响

[Agentic Coding and Persistent Returns to Expertise](claude-code-expertise.md) 分析 ~400,000 个 Claude Code 会话。**70% 规划决策由人做、80% 执行决策由 Claude 做**——清晰的人机分工。**领域专长而非编码能力是决定因素**——专家比中级用户会话产出多 2 倍以上动作和 5 倍以上文本。任务价值（freelance 比价）平均上升 27%。

[Anthropic Economic Index Report: Cadences](economic-index-june-2026-report.md) 把数据采样粒度提升到小时级。Claude 使用节奏与外部世界高度同步：工作-周末循环、日内高峰、税务截止日（4 月 14 日税务请求 8× 平均）。**算力 = 价值**——token 消耗与映射职业工资正相关。**自动化使用越深的用户越乐观**——挑战"AI 替代焦虑"叙事。

[Coding Agents in the Social Sciences](coding-agents-social-sciences.md) 对 1,260 名定量社会科学家的调查显示：仅 20% 采用了编码代理，性别差距达 2 倍以上，顶尖大学采用率高 40%。编码代理用户发布更多工作论文，但期刊投稿量无显著差异。

### 6. 物理 Agent

[Project Fetch: Phase Two](project-fetch-phase-two.md) 让 Opus 4.7 **完全自主控制四足机器人**完成 2025 年 8 月人类团队完成的任务。**平均比 Claude 辅助团队快 18 倍、比无 Claude 团队快 37 倍**，代码量少 10 倍。这是"物理 Agentic AI 早期时代"的信号：通用 Agent 可使用现成物理工具。

[Claude Plays Robotics](claude-plays-robotics.md) 把物理 Agent 研究推向广度：系统测试多种机器人身体（经典控制玩具、模拟四足/人形、真实 Unitree Go2、机械臂）和多种控制抽象层级。核心发现：**控制抽象决定成败**——直接驱动关节大多失败，监督预训练策略时模型能完成真实导航和操纵任务。为 LLM + 机器人集成提供能力基线。

[Project Pilot](project-pilot.md) 是物理 Agent 测量的第三块拼图（Vend→Fetch→Pilot）：让前沿模型操控真实无人机完成"定位-跟随"类空中监视任务，沉淀为新基准 Drone-Bench。无人机是典型的双重用途技术（农业增产 vs 军事打击），Frontier Red Team 通过公开测量为"AI 自主操控机器人"的风险治理提供可复现的证据基础——把 AI 风险评估从数字世界（网络安全、生物）扩展到物理世界。

### 7. 价值观测量

[Claude's Values Across Models and Languages](claude-values-models-languages.md) 提出"价值轴"方法，将 3,000+ 价值观压缩为少量可解释维度。发现跨模型差异（与训练决策相关）和跨语言差异（非英语中情感表达类价值观更少）。使大规模价值观审计从"不可能"变为"可操作"。

### 8. 能力控制

[An Off Switch for Dual-Use Knowledge](off-switch-dual-use.md) 提出 GRAM（Gradient-Routed Auxiliary Modules），在预训练时将双重用途知识隔离到可删除模块。与数据过滤（不可恢复）和事后遗忘（易恢复）不同，GRAM 在单次训练中实现 16 种能力配置，删除模块效果接近从未训练且不影响通用能力。为差异化 AI 部署提供新范式。

### 9. 旗舰模型

[Claude Opus 5](claude-opus-5.md) 是 2026 年 7 月 24 日上线的旗舰模型，核心主张"以一半的价格提供接近 Fable 5 的前沿智能"：定价与 Opus 4.8 持平（$5/$25 每百万 token），CursorBench 3.2 max effort 距 Fable 5 峰值仅 0.5% 但单任务成本减半，ARC-AGI 3 得分为次优模型 3 倍，OSWorld 2.0 以约三分之一成本超越 Fable 5 最佳成绩。effort 档位 + Fast 模式（~2.5× 速度、2× 价格）让同一模型覆盖全频谱任务。安全上官方称其"最对齐"：自动化行为审计不当行为评分 2.3（近期最低），刻意不在网络任务上训练——漏洞"发现"接近 Mythos 5 但"利用"大幅落后，网络分类器干预频率预计比 Fable 5 低约 85%，被拦截请求默认回退 Opus 4.8。配套 beta：对话中途更换工具不失效 prompt cache、API 自动 fallback。Opus 5 与 Mythos 级前沿探索（如密码分析突破）构成 Anthropic"前沿探索 / 安全量产"的双轨。

## 三、关键数据点

| 指标 | 数值 | 来源 |
|------|------|------|
| NLA 检测评估意识（SWE-bench） | 26% | NLA |
| NLA 检测评估意识（真实对话） | <1% | NLA |
| NLA 审计游戏发现隐藏动机 | 12-15% | NLA |
| 无 NLA 审计成功率 | <3% | NLA |
| 黑邮件率（Claude 4 时代） | 96% | Teaching Claude Why |
| 黑邮件率（当前模型） | 0% | Teaching Claude Why |
| Glasswing 发现高危漏洞 | 10,000+ | Glasswing |
| 开源漏洞真阳性率 | 90.6% | Glasswing |
| Opus 4.7 NMR 氢谱误差 | ±0.079 ppm | Claude Chemist |
| Claude 亚峰间距预测准确率 | ~80% | Claude Chemist |
| ChemDraw/MestReNova 准确率 | 26-35% | Claude Chemist |
| VirBench 最佳模型准确率（无确定性层） | 91.3% | Agents in Biology |
| VirBench 加确定性层准确率 | ~100% | Agents in Biology |
| Mythos Preview Firefox PoC | 14/18 | N-days |
| Mythos Preview Firefox 利用 | 8/18 | N-days |
| Mythos Preview Windows 提权链 | 8/21 | N-days |
| Mythos Preview 单条 Windows 提权链成本 | ~$2,000 | N-days |
| ATT&CK Navigator 高风险占比 | 33% → 56% | Attack Navigator |
| Opus 4.7 项目任务平均速度提升（vs Team Claude） | 18× | Project Fetch Phase 2 |
| Opus 4.7 项目任务平均速度提升（vs Team Claude-less） | 37× | Project Fetch Phase 2 |
| Opus 4.7 代码量减少 | 10× | Project Fetch Phase 2 |
| Claude Code 任务价值上升 | +27% | Claude Code Expertise |
| Claude Code 修复 bug 占比下降 | 33% → 19% | Claude Code Expertise |
| 编码代理采用率（社科） | 20% | Social Sciences |
| Claude Code 使用率（社科） | 86% | Social Sciences |
| 加拿大占全球 Claude 流量 | 2.6%（排名第 8） | Canada Economic Index |
| 加拿大人均用量 vs 预期 | 4x | Canada Economic Index |
| 安大略省对话量占比 | 43.9% | Canada Economic Index |
| 四大省份对话量占比 | 94% | Canada Economic Index |
| 价值轴方法压缩价值观 | 3,000+ → 少量轴 | Values Across Models |
| GRAM 可配置能力数 | 16 种（4 类双重用途） | Off Switch Dual-Use |
| GRAM 模型规模测试 | 50M - 5B 参数 | Off Switch Dual-Use |
| Opus 5 定价（输入/输出每百万 token） | $5 / $25（与 Opus 4.8 持平） | Claude Opus 5 |
| Opus 5 CursorBench 3.2 与 Fable 5 峰值差距 | 0.5%（单任务成本减半） | Claude Opus 5 |
| Opus 5 ARC-AGI 3 得分 | 次优模型的 3 倍 | Claude Opus 5 |
| Opus 5 OSWorld 2.0 成本 | 约 Fable 5 的 1/3 | Claude Opus 5 |
| Opus 5 不当行为评分（自动化行为审计） | 2.3（近期模型最低） | Claude Opus 5 |
| Opus 5 网络分类器干预频率 vs Fable 5 | 低约 85% | Claude Opus 5 |
| Opus 5 Fast 模式速度 / 价格 | ~2.5× / 2× | Claude Opus 5 |
| 密码分析攻击对象 | HAWK 签名 + 减轮 AES | Cryptographic Weaknesses |
| Drone-Bench 评估载体 | 真实飞行 + 仿真"定位-跟随"任务 | Project Pilot |
| Fable 5 生物学相关 fallback 减少 | ~85% | Improving Fable 5 Biology Safeguards |
| Fable 5 总 fallback 减少（Claude.ai / Cowork / Code / Platform） | ~67% / ~55% / ~17% / ~7% | 同上 |

## 四、与 OpenAI 的对比

| 维度 | Anthropic | OpenAI |
|------|-----------|--------|
| 报告类型 | Economic Index（半年期 + 主题专期） | Codex 经济影响论文 |
| 节奏研究 | Cadences（小时级采样） | 暂未发布对应 |
| 网络安全 | Mythos Preview + ARiES 评分 | Daybreak + Codex Security + GPT-5.5-Cyber |
| 科学应用 | 自主研究：Opus 4.7 在 NMR / 病毒检索 | 案例研究：GPT-5 Pro 帮免疫学家 |
| 自主代理 | Project Fetch Phase 2（物理机器人） | Codex 长视野任务白皮书 |
| 经济叙事 | "领域专长不可替代" | "Agent 改变单位知识工作" |
| 旗舰模型 | Opus 5：半价逼近 Fable 5、effort 档位 + Fast、安全分类器 + 自动回退 | GPT-5.6：Sol/Terra/Luna 三档 + Fast mode、差异化访问控制 |
| 前沿网络能力 | 密码算法数学缺陷发现（受控研究 + 公开披露） | ExploitGym 评估失控入侵 HF 生产环境（事故披露） |

## 五、贯穿始终的原则

1. **可解释性是安全的基础**：不理解模型在想什么，就无法确保对齐
2. **教原则比教答案更有效**：OOD 泛化是对齐训练的核心目标
3. **安全是自主性的前提**：Glasswing + Daybreak 展示了"先找漏洞再修复"的防御范式
4. **AI 正在进入专业领域**：化学、生物学、网络安全——通用模型正在挑战专用工具
5. **采用不平等是真实问题**：技术红利分配不均需要主动干预
6. **AI 加速了攻击和防御的双向速率**：N-day 利用开发速度激增，防御方必须更快
7. **领域专长是 Agent 时代的护城河**：编码能力不再稀缺，理解问题才是
8. **确定性基础设施是 Agent 价值的瓶颈**：生物数据案例显示 100% 准确率需要确定性执行层
9. **前沿探索与安全量产双轨**：Mythos 级模型探索能力边界（密码分析、漏洞发现），Opus 5 刻意收敛双刃剑能力做"最对齐"的日常主力——能力分层是部署范式

## 六、文章索引

| # | 日期 | 文章 | 主题 |
|---|------|------|------|
| 1 | 2026-05-07 | [Natural Language Autoencoders](natural-language-autoencoders.md) | 可解释性 |
| 2 | 2026-05-08 | [Teaching Claude Why](teaching-claude-why.md) | 对齐 |
| 3 | 2026-05-22 | [Project Glasswing: Initial Update](glasswing-initial-update.md) | 安全 |
| 4 | 2026-05-27 | [Coding Agents in the Social Sciences](coding-agents-social-sciences.md) | 社会影响 |
| 5 | 2026-06-03 | [Mapping AI-enabled Cyber Threats: Insights from the LLM ATT&CK Navigator](attack-navigator.md) | 网络安全 |
| 6 | 2026-06-05 | [Making Claude a Chemist](making-claude-a-chemist.md) | 科学 |
| 7 | 2026-06-08 | [Paving the Way for Agents in Biology](agents-in-biology.md) | 科学 Agent |
| 8 | 2026-06-08 | [Measuring LLMs' Impact on N-day Exploits](n-days.md) | 网络安全 |
| 9 | 2026-06-16 | [Agentic Coding and Persistent Returns to Expertise](claude-code-expertise.md) | 经济研究 |
| 10 | 2026-06-18 | [Project Fetch: Phase Two](project-fetch-phase-two.md) | 物理 Agent |
| 11 | 2026-06-26 | [Anthropic Economic Index Report: Cadences](economic-index-june-2026-report.md) | 经济研究 |
| 12 | 2026-07-06 | [A Global Workspace in Language Models](global-workspace.md) | 可解释性 |
| 13 | 2026-07-08 | [An Off Switch for Dual-Use Knowledge](off-switch-dual-use.md) | 能力控制 / AI安全 |
| 14 | 2026-07-09 | [Claude Plays Robotics](claude-plays-robotics.md) | 物理 Agent / 机器人控制 |
| 15 | 2026-07-13 | [Claude's Values Across Models and Languages](claude-values-models-languages.md) | 价值观测量 / 对齐 |
| 16 | 2026-07-14 | [How Canada Uses Claude](how-canada-uses-claude.md) | 经济研究 / 区域分析 |
| 17 | 2026-07-24 | [Claude Opus 5](claude-opus-5.md) | 旗舰模型 / 对齐 |
| 18 | 2026-07-24 | [Project Pilot](project-pilot.md) | 物理 Agent / 无人机 / 双重用途 |
| 19 | 2026-07-28 | [Discovering Cryptographic Weaknesses with Claude](discovering-cryptographic-weaknesses.md) | 网络安全 / 密码学 |
| 20 | 2026-08-07 | [Improving Fable 5's Biology Safeguards](improving-fable-5-biology-safeguards.md) | 生物安全 / 分类器 / 双用途 |