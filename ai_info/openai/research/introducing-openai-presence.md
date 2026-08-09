# 推出 OpenAI Presence（Introducing OpenAI Presence）

- **原文链接**: [Introducing OpenAI Presence](https://openai.com/index/introducing-openai-presence/)
- **作者**: OpenAI
- **发布日期**: 2026-07-22
- **检索日期**: 2026-08-01
- **标签**: #OpenAI_Presence #企业Agent #客服 #语音Agent #Codex改进循环 #生产级部署

## 核心观点

OpenAI 推出企业级产品 Presence，帮助企业部署可信赖的 AI agent，覆盖客户与内部工作流——回答问题、解决工单、操作企业系统、执行获批动作，必要时升级给人工。核心主张是：企业的挑战已不再是"证明 agent 能工作"，而是让 agent 在生产环境中足够可靠地承担高价值工作；这需要的不只是模型，而是策略、护栏、评估与部署专业知识的完整体系。

Presence 已在 OpenAI 自有英语电话支持渠道（1-888-GPT-0090）实战验证：数周内达到一线人工客服质量基准，目前 75% 的来电问题无需人工即可解决，Codex 驱动的改进循环曾在 10 天内把人工转接率降低 15 个百分点。

## 关键发现 / 关键技术

### 1. 按"工作"部署的最小权限模式
- 每次部署从一个具体工作开始（账单争议、保险理赔、IT 服务请求），agent 只获得该工作所需的知识与系统访问权
- 企业设定策略：agent 能做什么、何时需要审批、何时人工接管

### 2. Codex 驱动的持续改进循环
- 上线后，生产会话与升级记录暴露缺口，Codex 提出更新建议，团队测试并批准后发布
- 组件栈：策略与 SOP、护栏、获批动作、仿真、评估工具、Codex 改进流程；跨部署可复用（策略/评估/升级规则）与按工作流定制分离

### 3. 语音 + 聊天的实时体验与研究协同
- 支持客服、外呼销售、高风险内部流程等实时场景
- 与 OpenAI 研究团队紧密协作，每次部署的通用洞察回流研究与产品改进，形成跨客户复利

## 实践意义

Presence 是 OpenAI 把"内部验证过的 agent 运营体系"产品化的关键一步，与部署公司（FDE 交付）形成"产品 + 服务"双轨。对工程团队的参考价值：(1) "单工作最小权限 + 策略即配置"是可控 agent 的落地范式；(2) 改进闭环（生产缺口 → Codex 提案 → 人审 → 发布）把 agent 运维变成了软件工程问题；(3) 75% 自动解决率与 10 天 15pp 转接率下降是当前公开的最强客服 agent 生产数据之一。与语音智能新模型结合后，电话客服正成为 agent 商业化最成熟的场景。

## 跨厂商对比

- 与 [API 中的新语音智能模型](advancing-voice-intelligence-with-new-models-in-the-api.md) 互补：语音模型是能力底座，Presence 是把能力包成企业可交付产品的体系
- 与 [OpenAI 部署公司](openai-launches-the-deployment-company.md) 互补：部署公司出"人"（FDE），Presence 出"产品"，共同覆盖企业 agent 落地
- 与 [Anthropic 构建高效智能体](../../anthropic/engineering/building-effective-agents.md) 对比：Anthropic 强调从简单可组合模式起步，Presence 则展示 OpenAI 的全托管式企业封装路线

## 资源

- 原文：[Introducing OpenAI Presence](https://openai.com/index/introducing-openai-presence/)
