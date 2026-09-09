# 用 Claude 构建商业 Agent（Building commerce agents with Claude）

- **原文链接**: [Building commerce agents with Claude](https://claude.com/blog/claude-for-commerce-agents)
- **作者**: Anthropic
- **发布日期**: 2026-09-02
- **检索日期**: 2026-09-09
- **标签**: #CommerceAgents #AgentBlueprint #ClaudePlatform #EnterpriseAI

## 核心观点

Anthropic 发布"商业 Agent 蓝图"（commerce agent blueprint），把 harness、模式与护栏打包成可复用的工程资产，目标是让工程团队在数天内（而非数月）上线电商买卖 Agent。蓝图包含购物 Agent 与商家 Agent 两套完整参考实现，覆盖零售、旅行、电信、票务四个垂直行业，并附带 Claude Code 插件与各行业可运行 demo。

背景数据：零售商在 Claude 上运行购物 Agent 后，购物车最大增大 35%，购物者完成购买的概率提高 60%；Shopify、Priceline 等企业客户已在生产环境运行此类 Agent。发布时间点瞄准假日季规划。

代码可部署在团队已有的 Claude 构建路径上：Claude API、Amazon Bedrock、Microsoft Foundry、Google Cloud Vertex AI；Accenture、Mastercard、Visa 等生态伙伴正在帮助客户与商户社区采用该蓝图。

## 关键发现 / 关键技术

### 1. 购物 Agent（shopping agent）
- 运行在商家自己的 App 或网站内，蓝图提供目录、购物车、结账、客户偏好、订单历史的集成点；支付环节留给商家（自有结账或 agentic payments 供应商）。
- 能力：多商品目录搜索与凑单、记住客户偏好并个性化推荐、在对话内直接渲染商品/对比/购物车（而非纯文本）、构建购物车并交给结账、在同一对话中回答订单/退货/退款政策等客服问题。
- 护栏：价格与商品被约束在实际目录数据内，避免操纵性追加销售（manipulative upsell）；以 skills + tools 形式提供 catalog search、multi-item planning、deep research、personalization、customer care、in-conversation UI。

### 2. 商家 Agent（merchant agent）
- 面向店铺运营者：回答销售表现问题、追踪库存并主动预警（如促销前即将售罄）、基于自有销售历史推荐定价与促销、起草营销活动。
- 关键设计：Agent 主动建议的任何变更都需人工批准后才生效——"用户拥有最终决定权，Agent 负责看店"。
- 技能形式：sales analytics、catalog and inventory management、marketing and promotions、in-portal UI（图表与仪表盘）。

### 3. 构建途径与生态
- 三条构建路径任选：Messages API、Agent SDK、Claude Managed Agents（beta）。
- GitHub 开源（anthropics/commerce-agents），配套各垂直行业 live demo 与一篇工程深度解析（见同日发布的 anatomy 指南）。

## 实践意义

商业 Agent 的交付方式正从"各家自研"转向"参考实现 + Claude Code 定制"：工程团队先在自导览 demo 中看效果，再用 Claude Code 把参考实现改造成自己的目录、政策与品牌。护栏内建（目录约束、反操纵销售、人工审批）意味着安全不是可选项而是蓝图的默认部分。对零售/旅行/电信/票务团队，这是一条从实验到生产的捷径，也是观察 Anthropic 垂直行业战略的样本。

## 跨厂商对比

- 与 [Building effective agents](building-effective-agents.md) 对比：该文给出通用 Agent 设计原则（简单组合模式优先、单 Agent + 工具），本文是同一哲学在商业垂直的落地，附参考实现、护栏与四行业 demo。
- 与 [Introducing AgentKit](../../openai/research/introducing-agentkit.md) 互补：AgentKit 代表 OpenAI 的"平台化套件"路线，商业蓝图代表 Anthropic 的"垂直行业参考实现"路线，两者都在降低 Agent 开发门槛。

## 资源

- 官方文章：https://claude.com/blog/claude-for-commerce-agents
- 相关产品：https://github.com/anthropics/commerce-agents（蓝图仓库）；https://claude.com/solutions/commerce（行业 demo）
