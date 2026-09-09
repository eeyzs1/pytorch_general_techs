# 高效商业 Agent 的解剖指南（A guide to the anatomy of effective commerce agents）

- **原文链接**: [A guide to the anatomy of effective commerce agents](https://claude.com/blog/the-anatomy-of-effective-commerce-agents)
- **作者**: Matthew Koen、Ali Shazal（Anthropic）
- **发布日期**: 2026-09-02
- **检索日期**: 2026-09-09
- **标签**: #AgentArchitecture #LatencyOptimization #PromptCaching #Evals

## 核心观点

基于一年间与零售、市场、旅行、娱乐、电信团队共建商业 Agent 的经验，Anthropic 系统总结了高效商业 Agent 的工程解剖：核心架构是"单模型跑标准 agent loop + skills + tools + 强 eval 套件"，前面没有意图路由器，后面没有领域子 Agent 森林。全文分三部分：架构（决定一次）、延迟与成本、生产化（记忆、安全、评估、组织扩展）。

最重要的反直觉结论：在多个企业部署对比中，"单 Agent + skills"在质量上稳定优于"一个 prompt 打天下"和"每域一个子 Agent"，且往往成本与延迟更低——因为子 Agent 交接是状态有损操作，每次交接耗费数倍 token 并增加数秒延迟。质量（任务是否真正完成）比边际延迟收益对留存、参与、购物车规模的影响更大。

## 关键发现 / 关键技术

### 1. Skills 而非子 Agent；系统提示 vs 技能按频率划分
- 经验法则：涉及约 1/3 以上流量的指令进系统提示，其余进技能；安全/法律规则、品牌约束、过敏等关键用户事实永远在系统提示。若技能可由信号预判（如用户来自哪个页面），由 harness 在首次模型调用前注入，省掉加载轮次。
- 参考实现的划分：购物 Agent 提示词承载 grounding、购物车/结账语义、展示规则与商品搜索；skills 承担 search-discovery、purchase-research、planning-goals、customer-care、memory-personalization。商家 Agent 按运营域分技能：performance-insights、catalog-listings、inventory-operations、pricing-promotions、marketing-campaigns。
- 子 Agent 的两个合理位置：自包含的深研究任务（如搜索/读文档/跑代码后只回传紧凑答案）；已有独立合规面的专用 Agent（药房、金融服务）做 hand-off 而非 delegation。

### 2. 延迟三板斧与感知延迟
- 任务完成延迟 = Σ（每轮 time-to-last-token + 工具处理）。三个杠杆：更少轮次（预载上下文、并行工具调用、更强模型）、更快工具（eager dispatch——工具参数流式输出时即执行，把多秒间隙压到几百毫秒，Agent SDK 默认开启；让模型先发最慢的调用）、更快 token。任务平均超过约 5 轮时，更聪明的模型常常整体更快。
- 感知延迟：典型商业回复 500–700 输出 token，不流式即 5 秒以上转圈；解法是展示工具参数边流边渲染 + "展示工作过程"的进度文案。
- UI 组件即工具（present_products 等带类型参数），避免自定义标签解析；eager_input_streaming 可换 token 级流式但牺牲服务端 schema 校验；Sonnet 级以上模型 schema 违规极少见，仍建议包一层重试。

### 3. Prompt caching 是最大成本杠杆
- 缓存读价格约为新鲜输入的 1/10，写有约 1.25x 溢价；最佳商业部署跑出 90–99% 缓存命中率，应从第一天按此设计。~100k token 下缓存读还快 1.5–2 倍。
- 请求按变更频率排三段：global（系统提示 + 工具定义，字节级稳定）/ session（用户上下文与历史）/ volatile（时间戳、当前页，放最后）。最常见错误是把时间戳放系统提示顶部，每请求静默破缓存。技能以 tool result 形式加载落入可缓存前缀；断点每轮向前滚动。

### 4. 生产化：记忆、安全、评估、组织
- 记忆：异步抽取器在独立线程写记忆（不加对话延迟），在内部商业记忆 eval 上比"存事实工具"方案高 13% 事实召回；记忆存数据库 typed record（key/value/category/session），按人而非按账户键控（商户登录常共享）；读取分三层（常驻上下文 / 按轮预取 / lookup 工具）；记忆按数据处理问题设计（写入校验、用户可查改删、保留期、按部署开关）。
- 安全：执行在 harness 不在 prompt——模型只能提议（staged change + 服务器生成 ID），人 or 策略在 apply 时复核当前限额；写与渲染只接受服务器签发 ID（幻觉/粘贴/评论植入的 ID 一律拒绝）；限额按结果状态校验并按会话串行化写入；第三方内容（listing、评论、卖家消息）统一消毒 + 围栏标注。
- 评估：评快照不评对话（API 无状态，任何状态可直接构造），评结果不评路径；模拟用户 eval 只用于发现覆盖缺口；多数团队缺"脏状态"用例与负向用例——每个"应该做"配一个"应该拒"；每用户流 50–100 条用例起步，与 SME 共建，真实事故是最好的用例源。
- 多团队协作：所有权跟系统走（每技能/工具有唯一 owner 团队）；变更随用例进 CI（核心流量 + 全部安全用例 + 触碰部分的边界用例），每晚全量；Agent 进发布日历，金丝雀灰度，可免部署关闭单个技能，高峰期前冻结。

## 实践意义

这是目前对"消费级交易型 Agent"最完整的一份工程手册：从架构选型（反子 Agent 化）、成本工程（90%+ 缓存命中率设计）到安全（提议-审批分离、ID 白名单）与评估组织学。其"架构与模型解耦"的论断——换更好的模型只是配置变更 + eval sweep——为团队提供了抗模型迭代的架构信心。文末展望（语音、主动行动、代购 Agent 流量）也提示：同一套来源/暂存/审批规则是未来向第三方购物 Agent 开放工具的安全基础。

## 跨厂商对比

- 与 [Computer use, Skills API, Files API](computer-use-skills-api-files-api.md) 互补：该文介绍 Skills API 的机制本身，本文给出 skills 在商业场景的编排经济学——何时进提示、何时进技能、何时才用子 Agent。
- 与 [Building effective agents](building-effective-agents.md) 对比：通用设计模式之上的商业垂直生产化细节（缓存分段、护栏执行点、eval 组织学），可视为其续篇。

## 资源

- 官方文章：https://claude.com/blog/the-anatomy-of-effective-commerce-agents
- 相关产品：https://github.com/anthropics/commerce-agents（参考实现）
