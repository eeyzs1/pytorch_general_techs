# DeepSeek API 上线 Search 与 Fetch：联网检索成为模型 API 原语（Search & Fetch API）

- **原文链接**: [Search & Fetch | DeepSeek API Docs](https://api-docs.deepseek.com/guides/search)
- **作者**: DeepSeek（深度求索，API 文档团队）
- **发布日期**: 2026-10-16
- **检索日期**: 2026-10-16
- **标签**: #DeepSeek #SearchAPI #FetchAPI #Agent基础设施 #RAG #按次计费

## 核心观点

DeepSeek 在 API 文档站上线两个独立原语 API：**Search**（`POST /v1/tools/search`，结构化网页搜索）与 **Fetch**（`POST /v1/tools/fetch`，抓取单页并转 Markdown），官方定位是"给 Agent 与 RAG 应用提供实时网页内容"。二者与模型 API 同一 Bearer 认证、同一 base URL，均为原生 JSON API——开发者不再需要外接 Tavily/Serper 等第三方搜索服务即可在 DeepSeek 应用内闭环完成"检索—抓取—推理"。

计费采用**按成功请求**而非按 token：Search 与 Fetch 各 $0.75/千次成功请求，失败请求、空结果、超时一律不计费，`count` 只控制返回条数不影响单价；限流为账户级各 5 QPS、互不占用配额。Claude Code 内置 Web Search 工具与 Codex `web_search` 特性经 DeepSeek 发起的搜索请求，上线首两周免费（计费起始日另行公告）——延续"零改造接入 Claude Code/Codex 生态"策略。

> **日期说明**：官方未为此发布独立新闻稿，Change Log 与 news 列表均无条目，属"文档先行"式静默上线；本文发布日期取第三方首报日期（2026-10-16，80aj/Linux.do），确切上线日期以官方后续公告为准。

## 关键发现 / 关键技术

### 1. Search API：结构化检索 + 查询操作符透传
- 请求字段：`query`（1-128 Unicode 字符）、`count`（1-50，默认 10）、`need_content`（是否返回全文）、`ori_question`（用户原始问题，改善查询理解）、`localization`（IP 本地化结果）。
- 查询操作符原样透传：`site:`/`-site:`（站点限定/排除，多站点用 OR 连接）、`-`/`-"..."`（排除词/短语）、`"..."`（精确短语）、`lang:zh,en`（语言）、`after:`/`before:`（时间窗）。
- 返回结构面向"UI 与模型双读者"：`snippet`（100-200 字符，给界面）、`summary`（600-800 字符，给模型读）、`rerank_score`（0-3，≥1.5 视为高质量）、`authority`（0-4 权威分层，≥3 高权威）、`date`（RFC 3339）。

### 2. Fetch API：网页 → Markdown
- 输入单个 `url`（≤8192 字符，HTTP/HTTPS、须有 host、禁内嵌用户名密码），返回 `title` + Markdown 正文，可直接入上下文，与 1M 上下文及低价 KV Cache 命中互补。
- 错误语义明确：404=无法提取可用内容（站点拒绝、非支持内容类型等）、403=安全策略拒绝；受目标站点可用性与访问策略约束。

### 3. 计费与限流
- 仅 HTTP 200 且有结果才计费：Search 须返回非空 `results`，Fetch 须返回页面内容；各 $0.75/千次成功请求。
- 账户级 QPS 各 5，与模型并发限制相互独立；Fetch 另受每域名 QPS 限制；408/429/5xx 建议等待重试，402 需先充值，其余 4xx 修改请求后再试；错误格式 OpenAI 兼容。

### 4. 生态绑定与时间线
- Claude Code Web Search / Codex `web_search` 首两周免 Search API 费用——与 8-21 Files API（免费）同为"优先服务 Claude Code/Codex 存量工具生态"的落子。
- DeepSeek 的 Agent 输入侧基础设施至此齐了三块：文件（Files API，免费）、视觉（V4.1-Flash 原生多模态）、联网（Search/Fetch，按次计费）。

## 实践意义

对 Agent 开发者：检索从"第三方插件"变为模型 API 标配原语，链路缩短、稳定性责任收敛到模型厂；对成本工程：搜索成为独立成本项（按次计），Agent 预算需把"搜索次数 × $0.00075"单独建模，与 token 成本、峰谷调度叠加核算；对 RAG：Fetch 直出 Markdown 省去自建抓取解析管线，`authority`/`rerank_score` 字段可作检索质量过滤的现成信号。行业层面，OpenAI、Anthropic、Google 均已内置搜索工具，DeepSeek 跟进标志着"搜索能力"从加分项变为模型 API 标配。

## 跨厂商对比

- 与 [DeepSeek-V4-Flash-Vision-Exp 上线](deepseek-v4-flash-vision-exp.md) 对照：Files API 免费补齐文件输入、Search/Fetch 按次补齐联网输入——DeepSeek 按"单块能力 + 单独定价"逐件补齐 Agent 基础设施，而非打包成一体化平台。
- 与 [用 Computer Use、Skills API 与 Files API 构建生产级 Agent](../../anthropic/engineering/computer-use-skills-api-files-api.md) 对比：Anthropic 用 Computer Use 让 Agent 直接操作浏览器（通用但按 token 计费、成本高），DeepSeek 选择更窄的"搜索 + 抓取"两原语（按次计费、成本可控）——网页交互的"通用操作"与"专用原语"两条路线。
- 与 [Introducing Deep Research](../../openai/research/introducing-deep-research.md) 对比：OpenAI 把深度检索做成端到端产品（Deep Research），DeepSeek 先交出可组合的底层原语让开发者自建检索 Agent——产品化封装与原语开放的产品哲学差异。

## 资源

- 论文：无
- 代码：无
- Demo：无
- 官方指南：https://api-docs.deepseek.com/guides/search
- Search API 参考：https://api-docs.deepseek.com/api/search
- Fetch API 参考：https://api-docs.deepseek.com/api/fetch
- 定价页：https://api-docs.deepseek.com/quick_start/pricing
