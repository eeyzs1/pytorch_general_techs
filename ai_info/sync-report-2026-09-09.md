# 官网同步记录：2026-09-09

## 同步范围

本次实际检查的信源（含抓取失败的）：

| 信源 | URL | 抓取情况 |
|------|-----|----------|
| OpenAI | https://openai.com/index/ + /research/ + /news/rss.xml | ⚠️ 列表页 403（Cloudflare）；经官方 news RSS（160 条，pubDate 与锚点对齐）+ research/alignment feed 镜像 + sitemap 四方交叉检索；文章正文经 curl(浏览器 UA) 逐篇抓取成功 |
| Anthropic Engineering | https://claude.com/blog/（原 anthropic.com/engineering 已迁移） | ✅ 列表页浏览器渲染核验；13 篇文章页 datePublished 逐篇确认（web_fetch 被 JS 截断，改用浏览器 DOM） |
| Anthropic Research | https://www.anthropic.com/research | ✅ 成功（列表 + 文章页 web_fetch 直达） |
| Google DeepMind | https://deepmind.google/discover/blog/ + blog.google | ⚠️ 列表页 web_fetch 截断，浏览器取完整列表；8 篇候选逐篇确认日期（deepmind 文章页日期行 / blog.google JSON-LD）；正文多经第三方转述交叉核验 |
| Meta AI | https://ai.meta.com/blog/ + research.meta.ai + about.fb.com | ⚠️ 首轮 web_fetch 全部 DNS 屏蔽；**VPN 启动后经浏览器复核 research.meta.ai 成功**：08/21–08/31 窗口确认无遗漏、3 篇官方 URL 验证有效，并补录漏网新文《How We Built Safety Into Muse》（09-08，全文抓取）|
| Hugging Face | https://huggingface.co/blog | ⚠️ 官方域名对 harness 抓取器不可达（fetch failed）；16 篇正文经 hf-mirror.com 镜像获取（内容同步，URL 还原官方域名）；**VPN 启动后经浏览器抽验官方文章页可达、标题一致** |
| DeepSeek | https://www.deepseek.com/ + https://api-docs.deepseek.com/ | ✅ 成功（新公告走 api-docs/updates 渠道，官网 news 列表仍停留在 04-24） |
| GLM (智谱) | https://www.bigmodel.cn/ + zhipuai.cn + docs.bigmodel.cn | ⚠️ bigmodel.cn 主站为 SPA（web_fetch 仅 loading 空壳）；**zhipuai.cn/zh/research 与 docs.bigmodel.cn 复核可达**（zhipuai.cn 为官方结构化研究列表，确认 08/26 GLM-5.3-Flash 条目；docs 有模型文档页）。平台运营类动态（ZCode 活动）与业绩披露仍以媒体为信源 |
| Kimi (Moonshot) | https://www.kimi.com/blog/ | ✅ 成功，最新仍为 2026-07-16，无新文章 |

锚点（各 provider 库内最新 `published_at`）：anthropic 2026-08-20、openai 2026-08-19、google 2026-08-21、meta 2026-08-20、huggingface 2026-08-18、deepseek 2026-08-13、glm 2026-08-19、kimi 2026-07-16。检索窗口 2026-08-20 至 2026-09-09。

## 新增文章（自 2026-08-21 上次同步以来，共 86 篇）

### OpenAI（38 篇）

**旗舰与安全（8 篇）**

1. **2026-09-03 | GPT-6 Astra 发布** — ARC-AGI-3 99.9%、ExploitBench 100%、OSWorld 72.6%，首个达 Preparedness 网络 Critical 级的模型
2. **2026-09-03 | GPT-6 Astra 安全概览** — 失配标记约为 Sol 一半、生产级失配监控，坦承 CoT 可监控性下降
3. **2026-09-01 | 通往 Astra 之路** — Critical 判据实证（2 个未知 zero-day、提权到 root）；Astra GPU 分配 -59.2%
4. **2026-09-06 | 异星心智** — 首席科学家 Pachocki：目标/价值对齐二分、CoT 监控三重衰减、呼吁国际协调
5. **2026-09-06 | 研究加速：OpenAI 内部视角** — 3.1 agent-工作日/人类工作日、中位研究者日耗 >$600
6. **2026-09-08 | 纳维-斯托克斯千年奖问题** — 约 1 万并发 agent 88 小时证明 + Lean 形式化，不申领奖金
7. **2026-09-08 | GPT-5.6 Sol 运行量子计算实验** — MIT 近自主校准 6 比特芯片
8. **2026-09-03 | Daybreak 一线防御者 10 亿美元** — 水务/电网/地方政府优先，35+ 伙伴产品网络

**基建与经济（9 篇）**

9. **2026-08-25 | 富足智能背后的全栈** — CFO 版芯片/算力/模型/产品复利；Jevons 悖论
10. **2026-08-25 | Jalapeño 首批实测** — 每瓦峰值吞吐 1.5–1.9×，设计到流片 9 个月
11. **2026-08-31 | ChatGPT Ads 10 亿美元 ARR** — 上线 <200 天，支撑 10 亿+ 周活免费层
12. **2026-09-08 | 触手可及的工作** — 更强更便宜 AI 扩张可及工作范围
13. **2026-08-20 | Intelligence Age 博客创刊** — 权力集中风险与六原则
14. **2026-09-01 | AI 原生公司方法论** — 前沿企业人均 token 产出 8.3×
15. **2026-08-25 | Admin 插件** — 一个对话完成用量/成员/权限/限额管理
16. **2026-08-24 | GPT-5.6 上线 Kiro** — Terminal-Bench 2.1 成本约 -82%
17. **2026-08-26 | HF 事件与前行之路** — 责任方复盘：失准四模式、生产 harness 降入侵倾向 100×+

**教育与政策（11 篇）**

18. **2026-09-08 | 青少年发展研究资助 $5M** — 13–17 岁 AI 影响独立研究
19. **2026-09-08 | 支持新闻业（课堂到编辑室）** — 400+ ChatGPT Edu 进新闻院校
20. **2026-09-07 | 支持乌克兰独立新闻业** — 10 家机构 + API 额度
21. **2026-08-31 | 支持加州 SB 1119** — 青少年 AI 安全七项要求
22. **2026-08-27 | 批判性思维训练 RCT** — 1000+ 学生：GPT-4o 提分、思维训练提原创性
23. **2026-08-26 | ChatGPT for Teachers 扩至 55 学区** — 10 万+ 教职工、16 州隐私协议
24. **2026-08-26 | 学习永不停止** — 周 7000 万次自测对话
25. **2026-08-25 | 封禁俄罗斯影响力行动** — 假智库"主权指数"、34/36 抄袭错署
26. **2026-08-27 | 巴西布局** — 商业化运营启动、日消息 2.15 亿
27. **2026-08-28 | 泰国初创加速器** — MHESI 合作、10 家健康/教育初创
28. **2026-08-28 | 终止向 Cursor 供应模型** — SpaceX 收购触发控制权变更条款

**客户案例与产品（10 篇）**

29. **2026-09-08 | ChatGPT Images 2.5** — 延迟 -50%、周产 30 亿图、C2PA+水印
30. **2026-09-01 | EHR 医疗数据接入 ChatGPT** — Epic 集成 + 9 官方源、99.1% 安全评级
31. **2026-09-08 | 1Password +21% 生产力** — ROI 553%、零知识架构
32. **2026-09-03 | Playco 游戏原型 -50% 修复** — Astra one-go 三原型
33. **2026-09-03 | Legora 41 文档数分钟审完** — 4/4 植入错误全中、BAR +40%
34. **2026-09-02 | ATV Big Air Tour 3 天→3 小时** — AEO 流量 +1223%
35. **2026-09-01 | Gilbert + Tobin 律所治理** — 87% 席位活跃、KYC 3-8h→5min
36. **2026-08-31 | Polimill 日本公共 AI** — 1,050 自治体/55 万公务员
37. **2026-08-26 | loveholidays 全员 builder** — AI 变更 7%→79%
38. **2026-08-20 | Stampli -68% 上线工时** — 243h→77h

### Anthropic（16 篇：13 工程 + 3 研究）

1. **2026-08-21 | AI 原生 SDLC 手册** — 六阶段闭环、可机读工件链、hooks 确定性闸门
2. **2026-08-21 | Mythos 5 网络能力开放** — Claude Security 公测 + 3500 万美元 0xDAF
3. **2026-08-24 | 市场人员用 Claude Code 发个性化简报** — 9 条反馈规则、注册翻倍
4. **2026-08-25 | 记忆全入口生效** — 跨产品统一记忆 + 三档敏感分级
5. **2026-08-25 | Bain 加入 Partner Network** — 19,000 人部署、30–50% 生产力提升
6. **2026-08-26 | Claude in Chrome GA** — 免逐步确认 + 红队注入数据（Fable 5 全防线 0.3%）
7. **2026-08-26 | Cowork 内置专属浏览器** — 隔离执行不碰用户登录态
8. **2026-08-26 | Warp 自我改进 Agent** — 双技能循环、1000 万次会话规模验证
9. **2026-08-28 | Claude for Teachers** — 免费 Enterprise 开放美国 K-12
10. **2026-08-28 | Anthropic 员工用 Claude Tag** — 法务审查 1 天+→30 分钟
11. **2026-09-02 | 商业 Agent 蓝图** — 四行业参考实现、购物车 +35%
12. **2026-09-02 | 商业 Agent 解剖指南** — 单 Agent 优于子 Agent、90–99% 缓存命中率
13. **2026-09-08 | Claude Platform 降本增效** — prompt-audit 成本 -14.6% 且准确率 +5.3%
14. **2026-08-26 | 开放真实使用数据（研究）** — 25 万条对话经 Insights 支持外部独立研究
15. **2026-08-28 | 自动化研究者缓解对齐失败（研究）** — 10 类失败、欺骗项关闭 85% 差距
16. **2026-09-04 | 形式化费马大定理（研究）** — 1300 万行 Lean、11 天、Prove2Me 多 Agent

### Google DeepMind（8 篇）

1. **2026-08-26 | Gemini 3.5 Transcribe** — 智能转写（WER 4%/2.6%）、85+ 语言
2. **2026-08-27 | Gemini Omni 1.1 Flash** — 参考视频 + 增量续拍、360p 草稿省 2/3 成本
3. **2026-08-27 | 全球首个双盲 AI 评估试点** — Confidential Space 机密计算、基准污染对策
4. **2026-09-01 | 智能体式视频理解** — token 降 58.4–88%、成本最多 -66%
5. **2026-09-02 | Gemini 3.8 Flash 与 Flash Cyber** — CWE-Bench 47.2% 近前沿、Chrome 补丁 2.6×
6. **2026-09-02 | Fairwind 主动网络防御计划** — 申请制准入、漏洞发现数月→2 小时
7. **2026-09-03 | WeatherNext 3** — 逐小时 + 5 公里分辨率、进 Search/Maps/Cloud
8. **2026-09-08 | AlphaGenome Atlas** — 1 PB、约 90 亿 DNA 变异效应预测

### Meta（4 篇，3 篇二手信源交叉验证 + 1 篇 VPN 补录官方全文）

1. **2026-09-01 | Muse Voice Transcribe** — 流式 ASR 榜首（WER 3.1%）、20+ 说话人、$0.18/小时
2. **2026-09-02 | Muse Spark 1.3** — 编码超 GPT-5.6 Sol/Opus 5、AA 62 追平 Fable 5、预告开放权重
3. **2026-09-08 | Muse 个人智能体** — Secure VM + Sentinel + Stripe 一次性卡号
4. **2026-09-08 | How We Built Safety Into Muse（VPN 补录）** — 个人 Agent 安全架构完整工程叙述：systemd-nspawn 双安全域、surrogate token、eBPF 污点出口、$300K 漏洞赏金、Confidential VM 预告

### Hugging Face（16 篇）

1. **2026-08-20 | LFM2.5-DSpark** — ~300M 投机解码、H100 3.18×
2. **2026-08-21 | PwC 搜索基础设施** — 11 万+论文混合检索、HNSW Recall 0.9955
3. **2026-08-21 | ASR 基准优化测量** — benchmaxxing 量化、WER 最低者最易复现错误
4. **2026-08-25 | Granite 4.2** — dense reasoning 家族、512K 上下文、agentic RL
5. **2026-08-25 | Quantization-Aware Healing** — 4-bit 在 7/9 基准反超全精度
6. **2026-08-25 | gr.Workflow** — 节点图 = 画布 = REST API
7. **2026-08-26 | 多向量嵌入训练指南** — RTX 3090 14.5h 医学检索登顶
8. **2026-08-28 | Open ASR 榜纳入全球南方语言** — 4,888 说话人 ×12 属性公平性设计
9. **2026-09-01 | BenchMIRT** — IRT 审计 16 基准实际度量什么
10. **2026-09-01 | @huggingface/kernels** — 207 个 WebGPU 内核、vs ORT 2.57×
11. **2026-09-02 | IBM 时序模型上 Confluent** — Flink 内原生推理
12. **2026-09-03 | NeoMME** — 260M 多模态编码器、索引压缩 255×
13. **2026-09-03 | 100 步 GRPO 结构化输出** — 350M 模型 IFStruct 22.6→29.7
14. **2026-09-03 | funes 跨 Agent 记忆** — "记忆是数据集不是服务"
15. **2026-09-03 | 水彩画 RL 训练** — 成对评审 + 人类品味池
16. **2026-09-08 | Safety for Whom?** — 过拒绝 32.94%→4.16% 的边界对方法

### DeepSeek（1 篇）

1. **2026-08-21 | V4-Flash-Vision-Exp** — 多模态 API、单图 ≤384 tokens、免费 Files API

### GLM（3 篇，媒体信源）

1. **2026-08-27 | GLM-5.3-Flash 上线并开源** — 320B-A18B 原生多模态、Ox Alpha 匿名登顶（62T tokens）、10 万张国产芯片
2. **2026-09-04 | Flash × ZCode 夜间畅用** — 夜间 ZCode 零额度 / 其他 Agent ×2
3. **2026-09-03 | 半年度业绩会** — 营收 9.54 亿（+399.7%）、GLM-6.0 瞄准"自进化"

### Kimi（0 篇）

blog 最新仍是 2026-07-16（Kimi K3、PerceptionBench），自 K3 发布后近两个月无更新。

## 更新内容

- `catalog.yaml` 从 248 篇更新为 334 篇（新增 86 篇）
- `openai/research/summary.md`：文章数 106→144，新增 9 月脉络段落 + 索引 +38
- `anthropic/engineering/summary.md`：文章数 45→58，新增 8/21–9/8 脉络 + 索引 +13
- `anthropic/research/summary.md`：文章数 21→24，索引 +3
- `google/deepmind/summary.md`：文章数 29→37，新增 8 月下旬–9 月脉络 + 索引 +8
- `meta/summary.md`：文章数 13→17，索引 +4（含 VPN 补录的 Muse 安全架构文）
- `huggingface/blog/summary.md`：文章数 16→32，新增 4 个主题章节（9–12）+ 索引 +16
- `deepseek/news/summary.md`：文章数 5→6，索引 +1
- `glm/blog/summary.md`：文章数 4→7，新增 3 个主题章节 + 索引 +3
- `topics/agent-architecture.md`：+13 篇引用（Fermat、Navier-Stokes、SDLC、商业 Agent 双篇、Warp、Granite 4.2、funes、Muse 个人智能体、agentic video、Playco、AI 原生公司、HF 事件复盘）
- `topics/context-engineering.md`：+8 篇引用（GLM-5.3-Flash、NeoMME、train-multi-vector、pwc-search、funes、商业 Agent 解剖、Claude 记忆、EHR 可信源）
- `topics/evals.md`：+8 篇引用（GLM-5.3-Flash、Muse Voice、BenchMIRT、ASR 基准优化、Global South、双盲评估、GPT-6 Astra、商业 Agent 评估配方）
- `topics/safety.md`：+12 篇引用（safety-for-whom、自动化对齐研究者、Mythos 5 开放、Chrome GA、Cowork 浏览器、3.8 Flash Cyber、Fairwind、GPT-6 Astra、Path to Astra、异星心智、Daybreak $1B、HF 事件复盘、Intelligence Age、Images 2.5、SB 1119、青少年资助、俄罗斯影响力行动）
- `topics/tool-use.md`：+7 篇引用（V4-Flash-Vision-Exp、gr.Workflow、GRPO 结构化输出、商业 Agent 蓝图、Transcribe、Admin 插件、量子实验）
- `topics/codex-vs-claude-code.md`：+9 篇引用（SDLC 手册、Muse Spark 1.3、GPT-6 Astra、研究加速、Kiro、1Password/loveholidays/G+T、Cursor 终止供应）
- `topics/enterprise-ai-economics.md`：+11 篇引用（GLM 三篇、QAH、DSpark、Claude 降本、Bain、Claude Tag 内部、全栈富足智能、Jalapeño、ChatGPT Ads、Work Within Reach）
- `topics/README.md`：**已更新**——经用户确认新增 3 个主题文件并加入索引

### 新增主题文件（用户已确认）

- `topics/education.md`：教育 AI——OpenAI 教育产品矩阵（Teachers/Teens/插件/Academy）+ 研究证据（Bocconi RCT、学习行为数据）+ 政策护栏（SB 1119、APA 合作）+ Anthropic Claude for Teachers/Academy，共 13 篇引用
- `topics/news-media.md`：新闻业与 AI——OpenAI 新闻业支持（课堂到编辑室、乌克兰项目）+ 影响力行动归因 + 公共叙事之争（Apple 诉讼回应），共 4 篇引用
- `topics/international.md`：国际拓展与采用——巴西直营、泰国加速器、Google 韩国国家合作、Polimill 日本公共 AI，共 5 篇引用

## 校验结果

```text
python scripts/build_catalog.py
Wrote catalog.yaml with 334 articles
python scripts/validate.py
Validation passed: 334 articles, 366 markdown files
```

> 注：首轮同步结束时为 333 篇/365 文件；VPN 补录《How We Built Safety Into Muse》后为 334 篇/366 文件（另含 3 个新增主题文件 education/news-media/international）。

## 说明

### 信源抓取限制

1. **OpenAI 反爬**：openai.com 列表页/文章页对无浏览器 UA 请求 403，浏览器触发 Cloudflare 人机验证；本次经官方 news RSS + curl(浏览器 UA) 完成检索与正文抓取，38 篇全部为官方原文信源。**sitemap lastmod 大刷新警告**：8 月底站点迁移导致 300+ 篇旧文 lastmod 变为 2026-08-20+，本次已用 RSS/feed/catalog 四方交叉排除约 80 个假候选，后续同步切勿以 lastmod 判新旧。
2. **Meta 官网不可达**：ai.meta.com（DNS 解析到非公网地址）与 research.meta.ai 在本环境屏蔽；3 篇经 GIGAZINE 等二手信源 + 官方推文日期交叉验证，各文件已加注"官方链接待后续补全"；**08/21–08/31 窗口可能存在遗漏，下次同步优先复核**。
3. **GLM 官方站点 SPA**：bigmodel.cn 为 SPA 空壳无法直读；3 篇经新浪财经/IT之家/每经网交叉验证，文件内已注明信源。GLM-5.3 基座参数存在 743B（库存档）与 745B（每经稿）口径差异，两文各保留原信源数字。
4. **Hugging Face 官方域名直连失败**：正文经 hf-mirror.com 镜像获取（内容同步、URL 还原官方域名），16 篇全部抓到正文。
5. **claude.com JS 渲染**：web_fetch 截断，全部经浏览器 DOM 抓取；13 篇 datePublished 均逐篇核验。
6. **Google 文章页**：列表完整核验，但 6 篇 blog.google 正文仅标题，关键数据经第三方转述（Speech Technology、PPC Land、FoneArena 等）交叉核验，文件内已加注。
7. **Kimi 无更新**：K3 发布后近两个月博客静默，持续跟踪。

### 跨厂商新观察

1. **GPT-6 Astra 开启代际跃迁**：首个达 Preparedness 网络 Critical 级的模型（ExploitBench 100%、评测中发现并披露 2 个未知 zero-day），同一周 Meta Muse Spark 1.3（AA 62 追平 Fable 5）、Gemini 3.8 Flash（以小搏大）三线齐发——9 月第一周成为 2026 年迄今最密集的旗舰竞争窗口。
2. **数学千年问题成为 Agent 能力的"珠穆朗玛"**：OpenAI 纳维-斯托克斯（1 万并发 agent 88 小时 + Lean 形式化）与 Anthropic 费马大定理（1300 万行 Lean、11 天）同周双发，且都强调"诚实性"（承认优先权/遵循已有人类路线）——大规模 Agent 协作 + 形式化验证成为前沿实验室的共同展示位。
3. **"AI 对齐 AI"落地**：Anthropic 自动化研究者（欺骗项关闭 85% 安全差距、生产流程 1/15000 成本）与 OpenAI 异星心智（承认"没有实验室已充分解决对齐"）同周出现——对齐研究本身正在被 Agent 化，同时首席科学家级别开始公开管理预期。
4. **网络防御的"民主化竞赛"**：OpenAI Daybreak $1B、Anthropic 0xDAF $35M、Google Fairwind 计划三周内接连落地——前沿网络能力的分发治理成为三家共同的公共关系主战场，准入控制（Fairwind 申请制 / Cyber Verification / 输出型访问）成为标配。
5. **语音转写三家混战**：Gemini 3.5 Transcribe（8/26）、Muse Voice Transcribe（9/1，WER 3.1% 榜首）、HF 开源 ASR 榜（Global South 公平性 + benchmaxxing 审计）——语音入口从"识别准确率"竞争转向"智能清理 + 公平性 + 基准完整性"多维竞争。
6. **评估完整性成为行业议题**：Google 双盲评估（机密计算防基准污染）、HF BenchMIRT（基准实际度量什么）、ASR benchmaxxing（WER 最低者最易复现错误）同月出现——与既有 SWE-Bench Pro 审计、ARC-AGI-3 harness 敏感性共同构成"评估的评估"谱系。
7. **国产模型商业化加速**：智谱营收 +399.7%、GLM-5.3-Flash 匿名公测登顶 OpenRouter（62T tokens）、DeepSeek 多模态 API——"匿名发布 + 低价多模态 + 国产芯片"成为国产厂商的差异化组合拳。

### 撰写代理建议的新主题（已经用户确认并创建）

本次同步中多批撰写代理建议设立新 topic：**education**（OpenAI 教育五连 + Claude for Teachers）、**news-media**（新闻业支持三篇）、**international**（巴西/泰国/乌克兰拓展）。用户已确认，三个主题文件与 README 索引更新已在本次同步内完成（见上文"更新内容"）。

### 下次同步待办

1. ~~**Meta 08/21–08/31 窗口复核**~~：✅ 已于 2026-09-09 VPN 启动后经 research.meta.ai 官方列表复核——该窗口无遗漏，并补录《How We Built Safety Into Muse》（09-08）
2. **GLM 历史条目补录**：zhipuai.cn/zh/research 官方列表显示约 10 条未入库历史条目（2026/05 ZCube 推理网络、04/29 Scaling Pain、04/07 GLM-5.1、04/01 GLM-5V-Turbo、03/15 GLM-5-Turbo、02/21 GLM-5 技术报告、02/11 GLM-5 开源、02/02 GLM-OCR、01/19 GLM-4.7-Flash、01/13 华为多模态联合开源、2025/12 GLM-TTS/ASR）——对应 AGENTS.md 已知问题 #5"GLM 文章粒度不足"，后续同步优先补齐
3. **GLM/Meta 官方链接补全**（GLM 官方渠道已确认：zhipuai.cn/zh/research + docs.bigmodel.cn，本次已为 glm-5-3-flash.md 补官方链接；Meta 官方站点恢复可达后替换媒体信源）
4. 跟踪 GPT-6 Astra 的 CoT 可监控性问题后续（异星心智提出的衰减是否得到修复）
5. 跟踪 Muse Spark 开放权重发布（Zuckerberg 预告）与 Watermelon 模型
6. OpenAI 历史缺漏可补：introducing-gpt-rosalind（2026-04-16 首发）、introducing-aardvark（2025-10）
7. Kimi 博客静默近两月，若 K3 后续版本发布需重点跟踪
