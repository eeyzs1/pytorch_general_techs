# 给你的编码 Agent 一个你拥有的记忆（Give Your Coding Agents a Memory You Own）

- **原文链接**: [Give Your Coding Agents a Memory You Own](https://huggingface.co/blog/funes)
- **作者**: David Corvoysier（Hugging Face）
- **发布日期**: 2026-09-03
- **检索日期**: 2026-09-09
- **标签**: #Agent记忆 #编码Agent #上下文工程 #检索 #开源工具

## 核心观点

Hugging Face 开源 funes：给 Claude Code、Codex、pi、Hermes 等编码 Agent 加一层可持久、可迁移的记忆。它把机器上已有的会话 trace 变成可检索资产——解析、分块、本地嵌入后写入 Lance 数据集，向量 + BM25 融合、cross-encoder 重排、按新近度加权；agent 在对话中自行调用 recall 工具取回原文与出处。

其核心主张是"记忆是数据集，不是服务"：本地优先、无需账号；绑定后同步为你自有、默认私有的 HF 数据集，发布前做凭据脱敏与二次密钥扫描。由此实现跨 agent、跨机器、跨团队共享同一份可溯源的工作记忆，新 agent 不再"以陌生人身份"遇见项目。

## 关键发现 / 关键技术

### 1. 记忆管线与跨 Agent 复用
- 单二进制安装，`funes add claude`（或 codex/pi/hermes）一条命令接入：构建首个索引、给 agent 挂上 recall/get 工具、并自动索引每个完成的 turn（增量，不重嵌全史）。
- 一条确定性管线把各家 trace 解析成统一 turn-and-block 形状，因此 recall 可横跨不同 agent 的历史；每条结果标注来源 agent、时间戳、session 与 turn，recall 返回原文而非摘要，get 命令可展开完整 turn 及上下文。
- 嵌入与重排默认在本地完成，无 ML 运行时依赖的推理后端；远程记忆读取时缓存到本地，热查询回到本地速度。

### 2. recall vs compaction vs handoff 的成本实验
- 在 handoff-vs-recall 基准（两个必须依赖会话先验知识才能完成的任务）上，recall 是三者中最便宜的：一个任务上比写 handoff 便宜 8×，另一个便宜 4×。
- compaction（多数 agent 的默认做法）是唯一结果分裂的通道：其摘要抹平了关键发现，导致其中一个任务始终无法完成；recall 直接返回原文段落，不依赖摘要存活。

## 实践意义

长会话的上下文成本问题有了第三条路：不压缩、不交接，而是把历史外部化为可检索记忆。对多 agent、多机器、多成员团队，共享记忆让新成员的 agent 第一天就能检索数月决策与死胡同；开源项目也可发布"版本背后的会话"，成为可搜索的项目史（类比自动维护的 CLAUDE.md）。安全上需注意发布前的脱敏与扫描边界（SECURITY.md 有明确说明）。

## 跨厂商对比

- 与 [Dreaming: Better Memory for a More Helpful ChatGPT](../../openai/research/chatgpt-memory-dreaming.md) 对比：ChatGPT 记忆是封闭产品内的服务化功能，funes 是用户自有的开放数据集记忆——可跨厂商 agent 迁移、可审计、可导出，不被任何 API 租回。
- 与 [Claude Code: Best Practices for Agentic Coding](../../anthropic/engineering/claude-code-best-practices.md) 互补：CLAUDE.md 是手写的静态项目指引，funes 把完整会话轨迹变成自动索引的动态记忆并可直接被 agent 检索，两者可叠加使用。

## 资源

- 论文：N/A
- 代码：[huggingface/funes](https://github.com/huggingface/funes)
- Demo：[huggingface/funes-memory 数据集](https://huggingface.co/datasets/huggingface/funes-memory)（funes 开发记忆，可用 `funes ask` 直接查询）
