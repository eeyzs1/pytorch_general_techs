# DeepMind 与新加坡政府共建端侧反诈模型（Google DeepMind and Singapore Government collaborate to build fine-tuned AI model for scam detection）

- **原文链接**: [Google DeepMind and Singapore Government collaborate to build fine-tuned AI model for scam detection](https://deepmind.google/blog/on-device-ai-scam-detection-mddi/)
- **作者**: JJ Geewax、Miguel de Andrés
- **发布日期**: 2026-10-14
- **检索日期**: 2026-10-16
- **标签**: #端侧AI #反诈 #Gemma #国家合作 #隐私

## 核心观点

DeepMind 与新加坡政府（GovTech/MDDI）联合开发运行在手机上的反诈模型：消息分析全程在设备端完成，不上传任何会话内容。这是 Google 与新加坡"国家 AI 伙伴关系"下的落地项目，针对的是新加坡最痛的社会问题——诈骗占报案犯罪一半以上，2019 年以来损失超 40 亿新元，其中社会工程类（先建立信任再要钱）占损失的八成。

技术路线是"小模型 + 两级流水线"：基于轻量 Gemma 微调，训练数据为本地诈骗话术（冒充公共机构、银行、本地人物及区域性新骗局）的脱敏数据；低功耗轻量分类器先做初筛，可疑会话再交给微调 Gemma 分析更大上下文确认操纵模式，确认后实时在端上弹出预警。

隐私设计是制度亮点：仅在用户同意且符合各应用条款时才能访问会话；部署形态下政府与 Google 均无法读取对话；微调在 GovTech 托管云内完成，训练数据与生产隔离，剔除个人隐私信息。

## 关键发现 / 关键技术

### 1. 两级端侧流水线
- 第一级：轻量分类器低功耗筛查入站消息，标记可疑项
- 第二级：微调 Gemma 分析更大片段的会话，确认操纵模式或排除误报
- 确认威胁时在设备上实时告警，提示用户在泄露信息或转账前暂停

### 2. 本地化微调数据
- 覆盖冒充公共机构、银行、本地人物的骗局与新兴区域性骗局
- 来源为诈骗报案与情报流的匿名化数据，剔除隐私与个人可识别信息
- 在 GovTech 管理的云环境内微调，训练数据与部署隔离；用合成对话与本地语言模式跨多类骗局测试

### 3. 隐私与治理边界
- 访问会话须用户同意并遵守各应用使用条款
- 政府与 Google 在该部署下均无法读取对话内容
- 分阶段推出，将集成进市民使用的应用程序（与新加坡政府共同开发）

### 4. 国家级 AI 合作的新形态
- 属于 Google 与新加坡政府 National AI Partnership 框架
- 与韩国合作（科学模型开放）不同，新加坡样板主打"面向社会治理的联合建模"

## 实践意义

这是"开放小模型 + 主权数据 + 端侧推理"三者组合的样板：Gemma 提供可微调的底座，本地诈骗数据留在本国云内，推理下沉到用户设备——既绕开跨境数据驻留争议，又把延迟与隐私成本压到最低。对其他国家（报道中已出现越南等地的效仿讨论），复制该模式的关键不是模型而是三件事：高质量本地诈骗语料、政府侧托管微调环境、应用层集成通道。

对反诈产品团队，两级流水线值得直接借鉴：初筛分类器决定电池与体验成本，Gemma 级复核决定误报率——把"何时升级到更大模型"做成显式状态机，是端侧 LLM 落地的通用范式。

## 跨厂商对比

- 与 [韩国国家合作](announcing-our-partnership-with-the-republic-of-korea.md) 对比：同属 National Partnerships for AI，韩国侧重开放五大科学模型 + 人才培养，新加坡侧重联合微调社会治理模型——同一框架分化出"科学开放"与"治理共建"两条路线。
- 与 [Private AI Compute 服务器端记忆](private-ai-compute-server-side-memory.md) 互补：同为"数据不出域"架构，服务器端记忆用机密计算保护云端个人数据，反诈模型把推理彻底留在设备端——端云两端各补一块隐私拼图。
- 与 [Gemma 十亿下载](gemma-one-billion-downloads.md) 对比：Gemmaverse 的生态叙事在此落到一个可量化的公共治理场景——开放权重模型第一次成为国家级反诈基础设施的核心组件。
- 与 [Muse 的 AI Agent 安全方法](../../meta/security-and-safety-for-ai-agents-our-approach-with-muse.md) 对比：Meta 从 Agent 行为安全入手防滥用，本项目的对手是会话另一端的人类骗子——"检测操纵模式"与"约束 Agent 行为"是恶意侧防御的两个互补面。

## 资源

- 官方文章：https://deepmind.google/blog/on-device-ai-scam-detection-mddi/
- 论文：无
- 代码：无
- Demo：无

> 注：官方页正文在检索环境被截断，本文经 TNGlobal（10-16）、The Star（10-14）、DigitalToday（10-14）等多源交叉验证。
