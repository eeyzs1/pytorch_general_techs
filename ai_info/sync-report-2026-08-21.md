# 官网同步记录：2026-08-21（修订版）

## 同步范围

本次实际检查的信源（含抓取失败的）：

| 信源 | URL | 抓取情况 |
|------|-----|----------|
| OpenAI | https://openai.com/index/ + https://openai.com/sitemap.xml/engineering/ + /research/ | ✅ 成功，sitemap + 正文日期逐一核验 |
| Anthropic Engineering | https://claude.com/blog/（原 anthropic.com/engineering 已迁移） | ✅ 成功，sitemap + 每篇 datePublished 核验 |
| Anthropic Research | https://www.anthropic.com/research | ✅ 成功 |
| Google DeepMind | https://deepmind.google/discover/blog/ + https://blog.google/ | ⚠️ 列表页仍为缓存版本，经 WebSearch + 官方 URL 核验 |
| Meta AI | https://research.meta.ai/blog/ | ✅ 成功（ai.meta.com 仍登录墙，改用 research.meta.ai） |
| Hugging Face | https://huggingface.co/blog | ✅ 成功 |
| DeepSeek | https://api-docs.deepseek.com/updates/ + /news/ | ✅ 成功 |
| GLM (智谱) | https://www.zhipuai.cn/zh/research/ + https://docs.bigmodel.cn/ | ✅ 成功 |
| Kimi (Moonshot) | https://www.kimi.com/blog/ | ✅ 成功，最新仍为 2026-07-16，无新文章 |

锚点（各 provider 库内最新 `published_at`）：anthropic 2026-08-07、openai 2026-08-07、google 2026-08-06、meta 2026-08-05、huggingface 2026-08-06、deepseek 2026-07-31、glm 2026-07-30、kimi 2026-07-16。

> **⚠️ 本次同步经历重要修订**：第一轮同步仅新增 12 篇，经用户质疑后核验发现严重漏收——直接抓取官方 sitemap/列表页确认 Anthropic 8/11-8/20 有 12 篇新文章、Meta 2 篇、HF 4 篇、Google 2 篇未收录。修订后总新增 **32 篇**（catalog 216 → 248）。教训：**检索必须直接抓取官方列表页/sitemap 并逐篇核验 datePublished，不能依赖 web_search 的二手结果**。

## 新增文章（自 2026-08-08 上次同步以来，共 32 篇）

### OpenAI（2 篇）

1. **2026-08-18 | ChatGPT for Teens** — 面向 13-17 岁青少年的专门版本，Study Mode 学习模式 + 防情感操控 + 家长指南
2. **2026-08-19 | 网络关键能力时代把控模型开发节奏（Pacing）** — 首次主动暂停前沿模型 RL 训练两周，安全监控约 20% 算力"安全税"

> 说明：OpenAI sitemap 中 aardvark / protein-synthesis / theoretical-physics / in-house-data-agent 等 slug 经 Wayback + 正文核验均为 2-3 月历史文章（sitemap lastmod 为更新时间而非发布日期），不属于本次窗口，未重复入库。

### Anthropic（14 篇：13 工程 + 1 研究）

1. **2026-08-11 | Claude 文本水印的工作原理** — 生成时嵌入隐形水印，编辑/复制后仍可追溯，回应 EU AI Act
2. **2026-08-11 | Compliance API 覆盖扩展至 Cowork 与 Claude Code** — 增量端点把审计能力扩展到 Agent 产品，与推理钩子构成"事前 + 事后"治理闭环
3. **2026-08-12 | Claude Cowork 来到 Chrome 侧边栏** — 浏览器内 Agent 跨标签工作、跨桌面/移动/Web 延续
4. **2026-08-13 | JetBrains 如何评估与部署 Claude Fable 5** — 私有仓库评估 + 护栏数据保留优先，88 家 Fortune Global 100 客户视角
5. **2026-08-13 | Slack 中的自助数据分析（Claude Tag）** — 约 95% 准确率、治理一致的全员数据问答
6. **2026-08-14 | 最大化 Claude Code 会话价值** — `/clear`、`/compact`、缓存友好的会话卫生
7. **2026-08-17 | ABC Legal 让每个员工成为构建者** — 1,100 名法律公司员工用 Managed Agents 自建自动化
8. **2026-08-18 | Claude Tag 值班：CI/CD 第一响应者** — Agent 定位故障根因，工程师从 1 小时调查解放为 3 分钟验证
9. **2026-08-19 | 把对话转化为知识：Slack 人机团队** — "工作即对话"的开放频道协作
10. **2026-08-19 | Claude 加速蛋白质设计与分析化学**（研究）— 15 靶点命中 14，外部湿实验验证
11. **2026-08-20 | Computer Use + Skills API + Files API 全面 GA** — Agent 构建三件套 + browser use tool
12. **2026-08-20 | 创业公司 Claude Code 指南** — 五条运营原则，ClickHouse 功能 +30%、Omni 生产力 2-3 倍
13. **2026-08-20 | monday.com agent-first 重构** — 25 万公司平台两个月 500 万次 Agent 交互
14. **2026-08-20 | Anthropic 的 AI 教学方法** — Claude Academy 与"增加自主性"的教学哲学

### Google DeepMind（5 篇）

1. **2026-08-06 | 领导层重组** — Hassabis 转任 Alphabet 首席科学家，Jeff Dean 离职创业
2. **2026-08-06 | Veo 3.1** — 4K + 原生竖屏视频 + 素材转视频
3. **2026-07-28（8 月中旬报道） | SkillSmith** — KV-cache 层组合参数化技能与文本知识
4. **2026-08-19 | Operation Blue Skies** — 与英国合作的首个国家级 AI 凝结尾迹试验
5. **2026-08-21 | Gemma 十亿下载** — 10 亿下载 + 10 万开发者变体

### Meta AI（4 篇）

1. **2026-08-10 | Muse Glimmer** — 30B Apache 2.0 开源端侧 Agent 模型
2. **2026-08-10 | The Future is for Everyone** — Zuckerberg 6510 字开源宣言
3. **2026-08-14 | 回应 Muse Spark 1.1 第三方评估配置问题** — Irregular 封闭测试配置错误，与 OpenAI/HF 事件同属评估环境安全短板
4. **2026-08-20 | Muse Spark 1.2 多模态智能** — 多模态增益在模型可用工具时最显著，视频转代码

### Hugging Face（5 篇）

1. **2026-08-10 | Muse Glimmer 登陆 HF** — Meta 开源模型在 HF 首发，分发即生态
2. **2026-08-13 | ICML 2026 开放复现** — 智能体复现 2,200+ 篇论文，交互式 logbook 公开
3. **2026-08-14 | 2026 夏季开源模型报告** — Qwen 30 亿下载超 Google/Meta，能力与采用竞赛分离
4. **2026-08-14 | Strands Agents + LeRobot 机器人训练闭环** — AWS × HF 打通"Hub → 模拟 → 实机"
5. **2026-08-18 | MultiVectorEncoder** — Sentence Transformers v6.0 原生支持 ColBERT/late interaction

### DeepSeek（1 篇）

1. **2026-08-13 | V4-Pro GA 与 API 调价** — 部分模型涨幅最高 1100%，峰谷分时计费落地

### GLM（1 篇）

1. **2026-08-19 | GLM-5.3** — 743B 参数，AA 指数 60 分并列开源第一，编程提升约 50%，暂缓开源

### Kimi（0 篇）

blog 最新仍是 2026-07-16，无新文章。

## 更新内容

- `catalog.yaml` 从 216 篇更新为 248 篇（新增 32 篇）
- `anthropic/engineering/summary.md`：文章数 33→45，8 月段落扩展 12 篇新文章，索引 +12
- `anthropic/research/summary.md`：文章数 20→21，索引 +1（蛋白质设计）
- `openai/research/summary.md`：文章数 104→106，索引 +2（Teens + Pacing）
- `google/deepmind/summary.md`：文章数 27→29，新增气候行动与开源生态章节，数据点 +6，索引 +2
- `meta/summary.md`：文章数 11→13，新增评估事件与多模态章节，数据点 +4，索引 +2
- `huggingface/blog/summary.md`：文章数 12→16，新增 4 篇引用，数据点 +4，索引 +4
- `deepseek/news/summary.md`：文章数 4→5，索引 +1（调价）
- `glm/blog/summary.md`：文章数 3→4，索引 +1（GLM-5.3）
- `topics/agent-architecture.md`：+6 篇引用（Computer Use 三件套、monday、Slack、CI/CD 值班、会话优化、SkillSmith）
- `topics/context-engineering.md`：+1 篇引用（会话优化）
- `topics/evals.md`：+3 篇引用（Meta 评估事件、Muse 多模态评估、ICML 复现）
- `topics/tool-use.md`：+2 篇引用（三件套、Muse 工具增强多模态）
- `topics/codex-vs-claude-code.md`：+2 篇引用（会话优化、创业公司指南）
- `topics/README.md`：无需更新

## 校验结果

```text
python scripts/build_catalog.py
Wrote catalog.yaml with 248 articles
python scripts/validate.py
Validation passed: 248 articles, 276 markdown files
```

## 说明

### 本次修订的教训（重要）

1. **检索方法缺陷**：第一轮同步过度依赖 web_search 的二手结果，未直接抓取官方列表页。经用户质疑后，改为直接抓取 claude.com/blog 列表页 + sitemap + 逐篇 datePublished 核验，发现 Anthropic 有 12 篇、Meta 2 篇、HF 4 篇、Google 2 篇新文章漏收。**结论：官方 sitemap/列表页是唯一可信的"新文章清单"来源，web_search 只能用于补充交叉验证。**
2. **lastmod ≠ 发布日期**：OpenAI sitemap 中多个 slug（aardvark、protein-synthesis 等）lastmod 为 8 月，但经 Wayback 最早快照与正文核验确认为 2-3 月历史文章。发布日期必须用页面的 datePublished/JSON-LD 或 Wayback 最早快照交叉确认。
3. **遗漏规模修正**：第一轮声称"新增 12 篇"，实际应为 32 篇。已通过重建 catalog（216→248）+ 全量校验确认无重复、无遗漏。

### 信源抓取限制

1. **Meta AI 博客登录墙**：ai.meta.com/blog 仍返回"Not Logged In"，全部 Meta 文章经 research.meta.ai（可访问）核验。
2. **Google DeepMind 列表页**：deepmind.google/discover/blog/ 返回缓存版本，8 月文章经 blog.google + WebSearch 确认。
3. **OpenAI index 页 JS 渲染**：openai.com/index/ 无法直接解析文章列表，改用官方 sitemap 分区（engineering/research）+ Wayback 核验。

### 跨厂商新观察

1. **"能力治理"成为前沿实验室公共词表**：OpenAI（训练暂停 + 20% 安全税）、Anthropic（生物分类器精化）、智谱（GLM-5.3 暂缓开源）、Meta（开源宣言）四家同时把"发布节奏"当作治理工具。
2. **Anthropic 企业 Agent 平台化爆发**：一周内 12 篇文章覆盖"三件套 GA + Compliance API + Chrome Cowork + 全员采用案例 + 内部实践"——企业 Agent 从"能用"进入"可治理、可全员采用"阶段。
3. **第三方评估环境安全成为行业共同短板**：OpenAI（Irregular）、Meta（Irregular）连续两起评估配置事件，HF 事件则为评估失控演变为真实入侵——评估环境必须按安全关键系统设计已成共识。
4. **开源生态双轨现实**：HF 报告显示 Qwen 30 亿下载领跑，Gemma 10 亿紧随；能力竞赛（Kimi K3、Qwen3.8-2.4T 万亿模型）与采用竞赛（小模型下载）分离。
5. **国产模型"集体变贵"**：DeepSeek 涨幅最高 1100%、GLM 积分制涨价、Kimi 商业化并行——低价红利期结束，峰谷计费成为行业标准。

### 下次同步待办

1. GLM-5.3 权重开放后补更新开源状态
2. 跟踪 Jeff Dean 新创业公司产品发布
3. 跟踪 OpenAI Astra 训练恢复时间（两周暂停期预计 9 月初结束）
4. 后续同步必须直接抓取官方 sitemap/列表页作为新文章清单来源
