# AI 原生公司如何把工作流变成运营能力（How AI-native companies turn workflows into operating capability）

- **原文链接**: [How AI-native companies turn workflows into operating capability](https://openai.com/index/ai-native-company-workflows/)
- **作者**: OpenAI
- **发布日期**: 2026-09-01
- **检索日期**: 2026-09-09
- **标签**: #AI原生企业 #Agent工作流 #EnterpriseSignals #Codex #可复用技能

## 核心观点

OpenAI 最新的 Enterprise Signals 显示，企业 AI 正从"辅助"走向"执行"，但速度截然分化：前沿企业（AI 用量前 10%）每活跃用户产出的 token 是普通企业的 8.3 倍（1 月仅 2.6 倍）。差距扩大指向更深的运营转变——领先企业把 agent 接入公司上下文与工具、委派更实质性的工作、并让成功的工作流更容易复现。对领导者的挑战是把这种深度转化为人们可以信任、度量、改进的工作。

Basis、Clay、Exa Labs 三家创业公司分别把 agent 建进了员工入职、客户（账户）管理与开发者生态增长，工作流各不相同，但进阶路径一致且有可复用性：先教 agent 一个稳定流程（可复用技能），再在变化的工作中给它持续上下文（持久工作区），最后让它把机会带到"受测的执行"（工具 + 测试 + 人工审查）。三者都把改进本身做成工作流的一部分。

## 关键发现 / 关键技术

### 1. Basis：让入职流程可教（会计行业 agent 公司）
- 首日入职从 2 小时缩至 30 分钟：新员工当天获得 Codex 访问与公司专属 onboarding skill（面向特定工作流的可复用指令与资源集），Codex 迎新、讲解公司概念、后台完成集成设置
- 演示一次即固化为技能：明确的触发器、已知步骤、工具访问与"完成"定义；HR 可在下一批入职前更新技能处理例外

### 2. Clay：给分散工作一个持久大本营（GTM 自学习收入引擎）
- 每个账户一个持久工作区 + 专用 subagent，夜间审查一手来源（CRM、邮件、Slack、通话等）更新 deal folder；每天早晨协调 agent 汇总为优先行动清单
- 每晚节省约 1 小时收件箱分诊；推荐附带证据链，销售行动前可核查一手来源；可按权限扩展到 AE、BDR、方案工程师与销售负责人

### 3. Exa Labs：把机会带到受测行动（"Exa everywhere"）
- Codex 监控高优先级集成机会、汇集上下文、创建 PR、跑测试，并基于 Slack/Notion 出周报；可起草公告等下一步，交付前必须人工审查
- 人决定哪些机会重要、承诺什么、对外关系如何管理；测试与审查点让 agent 工作在发布前可见

### 4. 六步实验与扩展法
- 选择一个重要的端到端价值面；定义结果与度量（负责人、KPI、基线、护栏；用任务完成度/上下文与工具连接度/例外与审查负担度量深度，用周期时间/质量/成本/收入/风险度量价值）
- 写 agent 的"职位描述"（触发、产出、上下文、工具、权限、坚持程度、证据与停止点）；围绕 agent 建人的系统（决策权显式化）
- 让实验可见可复用：OpenAI 研究发现采用 6 个月后早期员工比高管每周多发 13 条消息——给员工试验空间，把有效过程打包为 skills、Plugins 或共享工作区（Chat 提问协作 / Work 多步知识工作 / Codex 技术执行）；把成功的运营模式带到下一个价值面

## 实践意义

本文是"Agent 落地方法论"的高浓度样本：不追求通用智能助手，而是选一个重复足够多、重要性足够高的工作流，把流程教给 agent、给它持续上下文、用测试与审查点框住执行边界，再把改进循环内置。8.3× 的 token 产出差距说明 AI 红利不会自动平均分配——组织设计（技能库、subagent 分工、证据与决策权）才是分化的根源。六步法可直接作为企业 agent 试点的工作清单。

## 跨厂商对比

- 与 [推出 OpenAI Presence](introducing-openai-presence.md) 互补：Presence 面向个人的持续陪伴与场景渗透，本文面向企业运营能力的沉淀，共同点是"持续上下文 + 可复用流程"的产品哲学
- 与 [monday.com 的 agent-first 平台](../../anthropic/engineering/monday-com-agent-first-platform.md) 对比：同为把 agent 嵌入既有工作平台的案例，Anthropic 生态侧重 Claude 与工作管理画布的结合，本文强调 skill/subagent/测试审查的工程化路径——两种"工作流即运营能力"的实现路线

## 资源

- 官方文章：https://openai.com/index/ai-native-company-workflows/
- 相关：https://openai.com/index/introducing-admin-plugin/
