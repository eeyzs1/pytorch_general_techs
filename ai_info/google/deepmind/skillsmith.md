# SkillSmith：将参数化技能与文本知识组合为新技能（SkillSmith: Learning to Compose Parametric Skills and Textual Knowledge）

- **原文链接**: [SkillSmith: Learning to Compose Parametric Skills and Textual Knowledge](https://arxiv.org/abs/2607.27497)
- **作者**: Google DeepMind
- **发布日期**: 2026-07-28
- **检索日期**: 2026-08-21
- **标签**: #Google #SkillSmith #模型权重 #KV-Cache #技能组合 #Gemma #研究

## 核心观点

Google DeepMind 提出 SkillSmith，一种把"参数化技能"（写入模型权重的技能）与"文本知识"（自然语言描述）组合成新技能的方法。核心思路是把模型权重当作"可读写的输入模态"，通过 KV-cache 层面的技能组合，让模型在运行时动态获得新能力，而无需完整微调。

在 Gemma 3 4B 上验证：SkillSmith 合成的技能在多项任务上超越全量微调的小模块，且保持了模型的通用能力。这项研究与"把技能写进提示词（文本）"和"把技能烤进权重（微调）"两种路线并列，提供了第三条路——在 KV-cache 层组合两者。

## 关键发现 / 关键技术

### 1. 权重作为可读写模态
- 将模型内部表示（KV-cache 激活）视为可组合的"技能载体"
- 技能以参数化形式存储，可与文本指令动态组合
- 无需修改基础权重即可注入新能力

### 2. 小模块反超全量微调
- 实验中 SkillSmith 组合的小模块在目标任务上超过全量微调效果
- 保持通用能力的同时获得专用技能
- 计算成本远低于完整微调

### 3. 与现有技能路线的区别
- 文本技能（prompt/skills）易解释但依赖上下文窗口
- 权重技能（微调）强但成本高、易遗忘
- SkillSmith 组合两者：文本提供语义，权重提供参数化记忆

### 4. 应用场景
- 动态模型适配：运行时按需加载技能
- 多技能叠加：同一模型承载多个可切换技能
- 与 Agent Skills、MCP 等外部技能体系形成对比

## 实践意义

如果"权重即模态"成立，模型定制将从"重新训练"走向"运行时组合"——企业可用文本描述 + 小型参数模块为通用模型按需装配领域技能。这与 Anthropic Agent Skills（SKILL.md 渐进式披露）形成有趣对照：Anthropic 把技能放在上下文/文件中，Google 把技能沉入权重表示层。对 Agent 开发者而言，这预示技能封装方式将出现"文本、文件、权重"三种并存的生态。

## 跨厂商对比

- 与 [Anthropic 为真实世界装备 Agent Skills](../../anthropic/engineering/equipping-agents-for-the-real-world-with-agent-skills.md) 对比：Anthropic 用 SKILL.md 文本文件封装技能（外部知识），Google 用参数化权重封装技能（内部表示），代表技能组合的两种极端路线
- 与 [MCP 2026-07-28 规范](../../community/specification/mcp-2026-07-28-specification.md) 对比：MCP 是工具/服务层的标准化，SkillSmith 是模型内部层的组合
- 与 [Gemma 4 开放模型](gemma-4.md) 互补：Gemma 4 提供基础权重，SkillSmith 展示在 Gemma 上的技能组合方法

## 资源

- 论文：https://arxiv.org/abs/2607.27497
- 代码：N/A（研究论文）
