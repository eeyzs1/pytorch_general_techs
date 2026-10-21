# ProvenanceGuard：把来源搞对，而不只是把事实搞对（Getting the Source Right, Not Just the Fact: Source-Aware Verification for MCP Agents）

- **原文链接**: [Getting the Source Right, Not Just the Fact: Source-Aware Verification for MCP Agents](https://huggingface.co/blog/MultiverseComputingCAI/getting-the-source-right-not-just-the-fact-source)
- **作者**: Antonio Tiene、Ander Alvarez Sanz、Oliver Wirjadi、Alessandro Genuardi（Multiverse Computing）
- **发布日期**: 2026-09-29
- **检索日期**: 2026-10-16
- **标签**: #MCP #事实验证 #溯源 #Agent安全 #NLI

## 核心观点

MCP Agent 的答案往往混合多个工具输出（搜索结果、结构化记录、数据库查询），传统事实性检查器（RAGAS、MiniCheck、AlignScore、SummaC）把证据池化后判断"是否有支撑"，却回答不了"是不是被归到了正确的来源"。Multiverse Computing 把这种失败模式命名为 cross-source conflation（跨源混淆）：退款政策确实写明 30 天，但答案说"根据账户记录"——事实为真、归因错误，在医疗与金融场景中同样危险。

ProvenanceGuard 是叠加在黑盒 MCP Agent 之上的后置验证层：读取带来源 ID 的 MCP trace，分解声明→路由到最相关来源→NLI 检查支撑→核对归因→输出逐声明来源判定与放行/拦截决策，被拦截答案可走 RARR 式修复。全程不重训 Agent，纯本地模型（MiniLM 路由 + DeBERTa NLI）即可运行。

## 关键发现 / 关键技术

### 1. 医学 Agent 实测：138/139 拦截率

- 281 条真实医疗 Agent trace，40 个答案 361 条声明由人类专家复核。
- 专家认定不应通过的 139 条声明中拦截 138 条（漏 1）；代价是扣下 67 条实际有支撑的声明送审——保守策略偏向"宁可误拦不可放过"。
- 可识别来源的声明中约 86% 路由到正确来源。

### 2. 对比基线：唯一输出"声明→来源"映射

| 验证器 | 拦截 F1 | 输出声明-来源映射 |
|---|---|---|
| ProvenanceGuard | 0.802 | 是 |
| MiniCheck | 0.783 | 否 |
| RAGAS Faithfulness | 0.758 | 否 |
| AlignScore | 0.662 | 否 |
| SummaC-ZS | 0.436 | 否 |

### 3. 边界与开销

- 相似来源压力测试：拦截决策 F1 0.846，但精确来源识别仅 50.3%——"多个 plausible 来源中选对一个"仍是开放问题。
- 篡改归因的对照实验：50 例换源全部被抓出。
- 修复回路：173 条被拦截答案全部得到处置（144 条落安全回退而非硬改写）；整体开销约 0.5 秒/答案，NLI 与路由调用仅数十毫秒。
- 已被 NVIDIA NVFlow 金融 Agent 合并为可选的落地验证阶段（对照 SEC 摘要核验答案）。

## 实践意义

对构建 MCP Agent 的团队，这是"池化 RAG 评测"到"溯源评测"的范式补丁：审计人员可以逐声明查看"查的是哪个工具输出、判的是放行还是拦截"。医疗、金融等对归因敏感的场景可将其作为离线闸门，成本几乎可忽略；但需接受其保守姿态带来的额外人工复核量。

## 跨厂商对比

- 与 [Safety for Whom?](safety-for-whom.md) 对比：同出 Multiverse Computing，一个研究拒绝行为的粒度（拒绝对的主题内子集），一个研究归因的粒度（证据来自哪个来源）——都在把"粗粒度安全判定"拆成可审计的细粒度判定。
- 与 [funes：给编码 Agent 一个你拥有的记忆](funes.md) 互补：funes 解决 Agent 记忆的可拥有与可脱敏，ProvenanceGuard 解决 Agent 答案的可追溯与可归因，共同构成"Agent 输出可信链"的两端。
- 与 [OpenAI 内容溯源](../../openai/research/advancing-content-provenance.md) 对比：OpenAI 从生成内容溯源（媒体出处）角度切入，ProvenanceGuard 从 Agent 工具调用溯源（哪个 MCP 来源支撑哪句话）角度切入，"provenance"正在成为跨厂商的共同关键词。

## 资源

- 论文：[ProvenanceGuard: Source-Aware Factuality Verification for MCP-Based LLM Agents（arXiv 2606.18037）](https://arxiv.org/abs/2606.18037)
- 代码：[github.com/aalvsz/provenanceguard](https://github.com/aalvsz/provenanceguard)
- Demo：[Agentic AI Summit 2026 Berkeley 海报](https://github.com/aalvsz/provenanceguard/blob/main/poster/ProvenanceGuard_Agentic_AI_Summit_2026_Berkeley.pdf)
