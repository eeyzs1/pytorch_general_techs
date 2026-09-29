# Cooley 如何用 ChatGPT 加速 IPO 工作(How Cooley is accelerating IPO work with ChatGPT)

- **原文链接**: [How Cooley is accelerating IPO work with ChatGPT](https://openai.com/index/cooley-gopublic)
- **作者**: OpenAI(官方博客)
- **发布日期**: 2026-09-17
- **检索日期**: 2026-09-29
- **标签**: #Cooley #法律AI #ChatGPT-Work #IPO #GO-Public #专业服务

## 核心观点

OpenAI 与顶级律所 Cooley 的案例:Cooley 基于 ChatGPT Work 构建 IPO 专用工具 GO Public,把 IPO 流程中的尽职调查问题清单、招股书草稿核对与监管问询响应智能化,帮助律师更早发现披露问题,把精力集中在真正需要专业判断的环节。

该案例与同日发布的 Astra for Law 形成配合:Cooley 是平台级产品(Astra for Law + 定制工作流)的样板客户,展示"律所自建工作流 on OpenAI 平台"的路径——律所保有流程与客户关系,OpenAI 提供模型、数据连接与合规控制。法律行业竞争维度因此更清晰:Harvey 代表独立法律 AI 公司路线,Cooley+OpenAI 代表平台赋能路线,而 Anthropic 亦在争夺同一批大所。

## 关键发现 / 关键技术

### 场景:IPO 的高价值模板化管线
- 覆盖环节:尽职调查问题清单、招股书草稿核对、监管问询响应。
- 目标:更早发现披露问题,律师精力集中于真正需要专业判断的环节。
- 路线对照:Harvey(OpenAI 09-23 案例)代表独立法律 AI 公司路线,Cooley+OpenAI 代表平台赋能路线——两条路线在同一官方博客序列中并列。

### 工作流:律所自建 on OpenAI 平台
1. 律所保有流程与客户关系——GO Public 是 Cooley 在 ChatGPT Work 上自建的专用工具。
2. OpenAI 提供模型、数据连接与合规控制;与同日发布的 Astra for Law 的"法律级"控制配合。
3. 分工结果:平台方不碰律所业务,律所不自研模型——专业化边界清晰。

### 合规要点
- 客户保密特权(attorney-client privilege)与模型数据隔离是部署前必须审计的条款。
- 这正是 Astra for Law 主打的"legal-grade controls"卖点在真实客户的落地。

## 实践意义

1. **管线拆解模板**:把高价值、模板化程度高的业务(IPO)拆解为可智能体化的管线,是专业服务机构可复制的路径。
2. **双轨生态**:OpenAI 在专业服务行业同时走"平台自建 + 生态伙伴"(如 Harvey)两条路线,买方需评估两种绑定形态的锁定风险。
3. **合规前置**:特权数据隔离与审计条款应在采购前逐条审计,而非部署后补丁。

## 跨厂商对比

- 与 [Introducing Astra for Law](astra-for-law.md) 构成同日双发:平台产品与样板客户的配合叙事,展现"模型 + 数据 + 合规"打包的落地形态。
- 与 [Gilbert + Tobin](gilbert-tobin.md) 对照:两家律所案例并读,可见大所以"自建工作流 on 前沿模型平台"的共同采用模式——G+T 重治理与采用率,Cooley 重单一业务管线的深度智能化。
- 与 [Kimi K3 法律行业方案](../../kimi/blog/kimi-k3-legal.md) 对比:国内厂商以行业模型 + 本土数据源切入法律服务,OpenAI 以平台 + 生态切入——法律 AI 的两种垂直化路径。

## 资源

- 官方博客:[How Cooley is accelerating IPO work with ChatGPT](https://openai.com/index/cooley-gopublic)
- 第三方佐证:The Hindu 对 OpenAI 法律平台整体的报道(佐证时间线)
- 相关条目:[Introducing Astra for Law](astra-for-law.md)、[Legora Financial Statement Review with Astra](legora-financial-statement-review-with-astra.md)

> 注:openai.com 原文 403,本文基于官方 RSS 描述 + The Hindu 报道佐证时间线整理;案例细节仍以官方源为主,待更多第三方验证补充。
