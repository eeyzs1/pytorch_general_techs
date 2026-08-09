# 官网同步记录：2026-08-08

## 同步范围

本次实际检查的信源（含抓取失败的）：

| 信源 | URL | 抓取情况 |
|------|-----|----------|
| OpenAI | https://openai.com/index/ + https://openai.com/research/ | ✅ 成功，获得 8 月完整文章列表 |
| Anthropic Research | https://www.anthropic.com/research | ✅ 成功，最新仍为 2026-07-28 |
| Anthropic Engineering | https://www.anthropic.com/engineering | ⚠️ 页面加载失败（"This page couldn't load"），工程博客已迁移至 https://claude.com/blog/ |
| Anthropic (claude.com/blog) | https://claude.com/blog/ | ✅ 成功，发现 6 篇新文章 |
| Google DeepMind | https://deepmind.google/discover/blog/ | ⚠️ 列表页返回疑似缓存版本，8 月文章经 WebSearch + 逐篇确认 |
| Meta AI | https://ai.meta.com/blog/ | ❌ 失败（"Not Logged In" 登录墙），改用 WebSearch 多轮检索替代 |
| Hugging Face | https://huggingface.co/blog | ⚠️ 部分页面抓取失败，经 WebSearch 确认内容与日期 |
| DeepSeek | https://www.deepseek.com/ + https://api-docs.deepseek.com/updates/ | ✅ 成功 |
| GLM (智谱) | https://www.bigmodel.cn/ + https://docs.bigmodel.cn/cn/update/new-releases | ✅ 成功，最新模型仍为 GLM-5.2 (2026-06-16) |
| Kimi (Moonshot) | https://www.kimi.com/blog/ + https://platform.moonshot.cn/blog | ✅ 成功，最新仍是 2026-07-16，无新文章 |

锚点（各 provider 库内最新 `published_at`，来自 catalog.yaml）：anthropic 2026-07-28、openai 2026-07-31、google 2026-07-30、meta 2026-07-24、huggingface 2026-07-29、deepseek 2026-07-15、glm 2026-06-16、kimi 2026-07-16。

## 新增文章（自 2026-08-01 上次同步以来）

共 **23 篇**（catalog 193 → 216）。

### OpenAI（9 篇）

1. **2026-08-01 | 十项数学与理论计算机科学进展（Ten Advances in Mathematics and Theoretical Computer Science）** — 内部 Astra 模型在长期未解数学问题上取得十项新成果，所有证明以 Lean 4 形式化证书发布
2. **2026-08-03 | Apple 搞错了（Apple is Getting This Wrong）** — 公开回应 Apple 诉讼，公开邮件记录纠正事实
3. **2026-08-03 | GPT-Live 连续语音交互工程解析（Continuous Voice Interaction with GPT Live）** — 全双工架构、WARP 协议、异步委托机制的工程深度解析
4. **2026-08-04 | 涉及 OpenAI 模型的第三方网络安全评估（Third-Party Cyber Evaluations Involving OpenAI Models）** — UK AISI 与 Irregular 评估中两起事件及新增防护措施
5. **2026-08-04 | ChatGPT Work 与 Codex 的教学新方式（New Ways to Learn and Teach with ChatGPT Work and Codex）** — 面向 K-12 教师、高校教师和学生的三类教育插件
6. **2026-08-06 | 提升 ChatGPT 中的 GPT-5.6 Sol（Improving GPT-5.6 Sol in ChatGPT）** — Sol 准确性提升 68% 事实错误减少，新增"思考"滑块，Luna 成为免费用户默认模型
7. **2026-08-06 | OpenAI 与 APA 推进青少年负责任 AI（OpenAI and APA Advance Responsible AI for Youth）** — 与美国心理学会合作推进青少年心理健康与 AI 安全
8. **2026-08-06 | 世界如何将 ChatGPT 用于工作（How the World is Putting ChatGPT to Work）** — 首次发布国家级 ChatGPT 使用数据（OpenAI Signals）
9. **2026-08-07 | 应对关键网络能力的下一个前沿（Responding to the Next Frontier of Critical Cyber Capabilities）** — Astra 模型可能达到"Critical"网络能力阈值，启动加强安全管控

### Anthropic（7 篇：6 工程 + 1 研究）

1. **2026-08-04 | Claude 成本可见性与控制指南（A Guide to Cost Visibility and Control in Claude）** — 企业 IT 管理员成本控制指南：访问管控、模型配置、硬性支出上限、Analytics API
2. **2026-08-05 | 推理钩子：Claude Enterprise 内联数据防泄漏（Inference Hooks: Inline DLP for Claude Enterprise）** — 签名 WebSocket 将每个推理请求路由至客户 DLP 服务器，集成 Netskope/Palo Alto/Proofpoint/Zscaler
3. **2026-08-06 | 在自有算力上运行 Claude Code 会话（Run Claude Code Sessions on Your Own Compute）** — 公测版自托管环境，源代码与密钥留在客户基础设施
4. **2026-08-06 | Millennium 与 Anthropic 使用 Claude 构建数字风险分析师** — 企业 AI 案例：Millennium 与 Anthropic 合作构建数字风险分析师
5. **2026-08-07 | 生产环境中运行 Auto Mode（Running Auto Mode in Production）** — Nuro、Gusto、Garner Health 三个生产案例，Claude 工作时间延长 9 倍
6. **2026-08-07 | Auto Mode 成为 Claude Code 默认模式（Auto Mode is Now the Default in Claude Code）** — 8 月 14 日起 Pro/Max/Team 计划默认启用；1,053 人测试研究：人工仅拦截 13.6% 危险命令 vs 分类器 89%
7. **2026-08-07 | 提升 Fable 5 的生物学安全防护（Improving Fable 5's Biology Safeguards）** — 生物学分类器重训，生物学相关回退减少约 85%

### Google DeepMind（1 篇）

1. **2026-08-06 | WeatherNext：AI 模型在气旋预测中取得突破** — WeatherNext AI 模型在气旋路径、强度和风结构预测上达到 SOTA，结果发表于 Nature，模型已开源

### Meta AI（1 篇）

1. **2026-08-05 | Muse Code 与 Muse Spark 1.2（Introducing Muse Code and Muse Spark 1.2）** — Meta 首个终端编码 Agent，持久化异步后台 Agent + append-only 事件日志，Terminal-Bench 2.1 得分 82.9%

### Hugging Face（3 篇）

1. **2026-07-30 | mDenseOn 与 mLateOn：开源多语言长上下文代码检索模型** — LightOn 发布两个 307M 参数多语言检索模型，BEIR SOTA (57.56)，2.8B 对训练语料
2. **2026-08-04 | Fast Gemma Challenge 验证 SOTA 配方全公开** — FINAL-Bench 分享 Fast Gemma Challenge 验证 SOTA 配方，A10G 单流 510.58 TPS
3. **2026-08-06 | Baseten 加入 Hugging Face 推理提供商** — HF 新增 Baseten 为官方推理提供商，零加价访问 DeepSeek V4 Flash、GLM-5.2、Kimi K3 等开源模型

### DeepSeek（1 篇）

1. **2026-07-31 | DeepSeek-V4-Flash 正式版 API 上线公测** — V4-Flash-0731 正式版发布，Agent 基准远超 V4-Pro-Preview（Terminal Bench 2.1: 82.7, NL2Repo: 54.2），原生支持 Responses API 格式

### GLM（1 篇）

1. **2026-07-30 | GLM Coding Plan 套餐改版** — 从按次数计费改为 token 积分制，新用户价格大幅上调（Pro ¥149→¥538/月），老用户保留原价，高峰期消耗 3 倍积分

### Kimi（0 篇）

blog 最新仍是 2026-07-16（Kimi K3 + PerceptionBench），无新文章。

## 更新内容

- `catalog.yaml` 从 193 篇更新为 216 篇
- `openai/research/summary.md`：更新文章数（95→104）、新增 4 个主题章节引用、16 个数据点、9 条索引
- `anthropic/engineering/summary.md`：更新文章数（26→32）、新增企业基础设施章节、10 个数据点、6 条索引
- `anthropic/research/summary.md`：更新文章数（19→20）、新增 Fable 5 生物学安全防护、2 个数据点、1 条索引
- `google/deepmind/summary.md`：更新文章数（23→24）、扩展气候与天气章节、5 个数据点、1 条索引
- `meta/summary.md`：更新文章数（8→9）、新增第 9 章 Muse Code 终端编码 Agent、4 个数据点、1 条索引
- `huggingface/blog/summary.md`：更新文章数（8→11）、新增工具平台与高效推理章节引用、7 个数据点、3 条索引
- `deepseek/news/summary.md`：更新文章数（3→4）、扩展 V4 系列章节、3 个数据点、1 条索引
- `glm/blog/summary.md`：更新文章数（2→3）、新增第 5 章 Coding Plan 定价改版、3 个数据点、1 条索引
- `topics/agent-architecture.md`：新增 4 篇文章引用（Muse Code 持久化 Agent、GPT-Live 语音 Agent、Auto Mode 生产案例、自托管 Claude Code）
- `topics/context-engineering.md`：新增 2 篇文章引用（mDenseOn 检索模型、Muse Code 上下文压缩）
- `topics/evals.md`：新增 4 篇文章引用（Lean 4 形式化证明、第三方网络评估、Preparedness Framework 阈值、Terminal-Bench/DeepSWE 基准）
- `topics/safety.md`：新增 6 篇文章引用（Auto Mode 安全研究、推理钩子 DLP、Fable 5 生物学防护、APA 青少年安全、网络评估事件、Astra Critical 阈值）
- `topics/tool-use.md`：新增 3 篇文章引用（GPT-Live 语音工具接口、教育插件垂直工具、推理钩子安全工具）
- `topics/codex-vs-claude-code.md`：新增 6 篇文章引用（GPT-5.6 Sol 改进、Codex 教育插件、Auto Mode 默认化、Auto Mode 生产案例、自托管 Claude Code、Muse Code 新竞争者）
- `topics/README.md`：无需更新（未新增 topic 文件）

## 校验结果

```text
python scripts/build_catalog.py
Wrote catalog.yaml with 216 articles
python scripts/validate.py
Validation passed: 216 articles, 242 markdown files
```

## 说明

### 信源抓取限制

1. **Anthropic Engineering 博客迁移**：`https://www.anthropic.com/engineering` 页面加载失败（"This page couldn't load"），经确认工程博客内容已迁移至 `https://claude.com/blog/`。旧 URL `anthropic.com/engineering/{slug}` 现对应 `claude.com/blog/{slug}`。本次新增的 6 篇 Anthropic 工程文章均来自 claude.com/blog，但仍归入 `anthropic/engineering/` 目录。建议后续更新 AGENTS.md 信源 URL。
2. **Meta AI 博客登录墙**：`ai.meta.com/blog/` 持续返回"Not Logged In"，无法直接抓取列表页。Muse Code 文章经 WebSearch + 第三方来源（Reuters、VentureBeat 等）交叉确认，原文 URL 为 `research.meta.ai/blog/introducing-muse-code-and-muse-spark-1-2`。
3. **Hugging Face 博客**：部分 huggingface.co/blog/* 页面抓取失败，经 WebSearch 确认内容与发布日期。部分社区博客文章（IDEOGRAM-4 inpainting、Qwen3.6 加速、OpenCode 训练教程）因 URL 不确定或内容较为边缘，本次未入库。
4. **DeepSeek API 定价调整公告**（2026-08-06）：多家媒体报道 DeepSeek 宣布将大幅上调 API 定价，但官方 changelog（api-docs.deepseek.com/updates/）尚未发布 8 月条目，该公告可能通过平台通知发出，暂未入库。

### 跨厂商新观察

1. **编码 Agent 三强格局形成**：Meta Muse Code 加入赛道后，Terminal-Bench 2.1 排名为 Claude Opus 5 (86.7%) > Muse Spark 1.2 (82.9%) > GPT-5.6 Terra (81.8%)。三方各具特色：Claude Code 在长时程任务领先，Muse Code 以模型-harness 协同训练为差异点，Codex 以产品矩阵见长。
2. **Auto Mode 安全实证**：Anthropic 的 1,053 人测试研究首次用数据证明——人工审批在速度上不可持续（97% 批准率）且在安全性上劣于自动分类器（13.6% vs 89% 拦截率），为"自动审批优于人工审批"提供了实证支持。
3. **Astra 模型浮现**：OpenAI 内部 Astra 模型在数学证明（Lean 4 形式化）和网络安全（可能达到 Critical 阈值）两个维度展现前沿能力，预示下一代模型发布。
4. **企业 AI 基础设施成熟**：Anthropic 本周集中发布自托管环境、DLP 推理钩子、成本控制指南、Millennium 案例四项企业功能，标志企业级 AI 部署从"能用"进入"可控可治理"阶段。

### 下次同步待办

1. 更新 AGENTS.md 中 Anthropic 工程博客信源 URL 为 `https://claude.com/blog/`
2. 跟踪 GLM-5.3 发布（创始人唐杰确认"即将发布"，但截至 8 月 8 日官方 changelog 仍为 GLM-5.2）
3. 跟踪 DeepSeek API 定价调整官方公告（待官方 changelog 更新后补入）
4. 关注 Hugging Face 社区博客中被跳过的边缘文章（若有重要内容遗漏后续补入）
