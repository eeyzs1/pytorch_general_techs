# AI 协同临床：开启医疗新模式（Enabling a new model for healthcare with AI co-clinician）

- **原文链接**: [Enabling a new model for healthcare with AI co-clinician](https://deepmind.google/blog/ai-co-clinician/)
- **作者**: Alan Karthikesalingam, Vivek Natarajan and Pushmeet Kohli
- **发布日期**: 2026-04-30
- **检索日期**: 2026-08-01
- **标签**: #医疗AI #多模态 #Agent #Gemini #Google

## 核心观点

Google DeepMind 宣布 AI co-clinician 研究计划，提出"三元照护"（triadic care）范式：AI agent 在医生的临床权威下参与患者照护旅程，作为照护团队的协作成员放大医生专业能力，而非替代医生判断。WHO 预测 2030 年全球医疗工作者缺口超 1000 万，这是该计划的核心动因。

该计划同时覆盖医生端（循证证据综合、药物问答）和患者端（实时多模态远程医疗）两条研究线，并以严格的医生主导评估证明：AI 在多数循证任务上已可媲美甚至超过现有工具，但在识别"危险信号"和指导关键体格检查上仍逊于专家医生——当前定位应是支持工具而非临床判断的替代品。

## 关键发现 / 关键技术

### 1. 医生端证据综合：NOHARM 框架评估
- 改编 NOHARM 框架测试"作为错误"（错误信息）与"不作为错误"（遗漏关键信息）
- 98 个真实基层医疗查询的盲测中，97 例零严重错误，优于医生广泛使用的两类 AI 证据综合工具
- 在 OpenFDA RxQA 药物知识基准上，开放式问答场景超越其他前沿模型

### 2. 患者端实时多模态远程医疗
- 基于 Gemini 与 Project Astra，用实时音视频进行模拟远程问诊
- 与哈佛、斯坦福合作的随机模拟研究：20 个合成临床场景、10 名医生扮演患者
- 展示文本系统不具备的能力：实时纠正患者吸入器用法、引导肩部动作识别肩袖损伤

### 3. 与医生的量化差距
- 评估 140 项会诊技能维度：专家医生总体仍优于 AI，尤其在识别"red flags"上
- 但 AI co-clinician 在 140 项中的 68 项达到或超过基层医生（PCP）水平
- 研究含 120 例虚拟远程问诊，与 GPT-realtime 交叉对比

### 4. 临床级安全架构
- 双 agent 架构：Planner 模块持续监控对话，确保 Talker agent 不越出安全临床边界
- 检索侧执行验证与引用核查，优先临床级证据
- 已在美、印、澳、新西兰、新加坡、阿联酋推进分阶段真实世界评估合作

## 实践意义

AI co-clinician 是"AI 作为照护团队成员"这一定位最系统的官方阐述：不追求取代医生，而是在医生监督下扩展其触达范围。双 agent 安全架构（Planner 监控 Talker）为高风险垂直领域 agent 提供了可复用的工程范式。其"140 项维度逐项对人"的评估方法，也为医疗以外的专家级 agent 评估树立标杆。

## 跨厂商对比

- 与 [Anthropic Agents in Biology](../../anthropic/research/agents-in-biology.md) 对比：Anthropic 聚焦生物研究 workflow 中的 agent 能力边界，Google 则直接在临床照护场景中验证人机协同，两者都强调"专家监督下放大"而非替代
- 与 [AI co-scientist](co-scientist.md) 互补：co-scientist 面向科研假设生成，co-clinician 面向临床照护交付，共享"多 agent 协作 + 专家在环"的设计哲学

## 资源

- 技术报告：[Towards Conversational Medical AI with Eyes, Ears and a Voice](https://www.gstatic.com/vesper/ai_coclinician_technical_report.pdf)
- 相关论文：[NOHARM 框架](https://arxiv.org/abs/2512.01241) / [AMIE (Nature)](https://www.nature.com/articles/s41586-025-08866-7)
