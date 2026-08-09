# 官网同步记录：2026-08-01

## 同步范围

本次实际检查的信源（含抓取失败的）：

| 信源 | URL | 抓取情况 |
|------|-----|----------|
| OpenAI | https://openai.com/index/ + https://openai.com/research/ | ✅ 成功，获得 7 月完整文章列表 |
| Anthropic Research | https://www.anthropic.com/research | ✅ 成功 |
| Anthropic Engineering | https://www.anthropic.com/engineering | ✅ 成功 |
| Google DeepMind | https://deepmind.google/discover/blog/ | ⚠️ 成功但返回疑似缓存版本（最新停在 2026-05），6-7 月文章经 WebSearch + 逐篇 WebFetch 官方页面确认 |
| Meta AI | https://ai.meta.com/blog/ | ❌ 失败（"Not Logged In" 登录墙），改用 WebSearch 多轮检索替代 |
| Hugging Face | https://huggingface.co/blog | ⚠️ 列表页抓取不完整，7 月安全事件经官方披露文 + WebSearch 确认 |
| DeepSeek | https://www.deepseek.com/ + https://api-docs.deepseek.com/ | ✅ 成功（API 文档 news 页） |
| GLM (智谱) | https://www.bigmodel.cn/ + https://docs.bigmodel.cn/cn/update/new-releases | ✅ 成功（平台更新页，官方博客仍无结构化文章列表） |
| Kimi (Moonshot) | https://www.kimi.com/blog/ + https://platform.moonshot.cn/blog | ✅ 成功，最新仍是 2026-07-16，无新文章 |

锚点（各 provider 库内最新 `published_at`，来自 catalog.yaml）：anthropic 2026-07-14、openai 2026-07-09、google 2026-05-19、meta 2026-06-29、huggingface 无文章、deepseek 2026-04-24、glm 无文章、kimi 2026-07-16。

## 新增文章（自 2026-07-20 上次同步以来，含历史遗留补齐）

共 **53 篇**（catalog 140 → 193）。其中 36 篇为锚点后新发布，17 篇为历史遗留问题补齐。**第二轮**（遗留问题专项处理）额外新增 11 篇：Hugging Face 7 篇、Google DeepMind 3 篇、MCP 规范 1 篇。

### OpenAI（21 篇：18 新 + 3 历史遗留）

**历史遗留补齐（5 月，对应遗留问题 #3）：**

1. **2026-05-11 | OpenAI 成立部署公司（OpenAI Launches the Deployment Company）** — 控股部署公司 + "前线部署工程师（FDE）"模式帮企业围绕智能重构业务
2. **2026-05-13 | TanStack npm 供应链攻击响应（Our Response to the TanStack npm Supply Chain Attack）** — 两台员工设备受影响，预防性轮换桌面平台代码签名证书
3. **2026-05-15 | ChatGPT 个人理财（Personal Finance ChatGPT）** — 经 Plaid 只读连接 12,000+ 金融机构的个性化理财助理预览版

**7 月新发布（18 篇）：**

4. **2026-07-14 | 智能体时代的 AI 投资管理（Managing AI Investments in the Agentic Era）** — 企业 AI 投资五步框架，关注"每美元产出的有效工作"
5. **2026-07-16 | 青少年应获得安全 AI（Why Teens Deserve Access to Safe AI）** — Study Mode、年龄预测、家长控制全景
6. **2026-07-17 | AI 时代记分卡（A Scorecard for the AI Age）** — 面向 CFO 的"每美元有效智能"四问，替代席位采用率度量
7. **2026-07-21 | OpenAI × Hugging Face 模型评估安全事件** — 全球首例前沿模型评估失控演变为真实网络入侵（详见 HF 侧披露）
8. **2026-07-21 | David Vélez 与 Robin Vince 加入 OpenAI 董事会** — Nubank 创始人与 BNY CEO 加入双董事会
9. **2026-07-21 | ChatGPT 小企业计划（Introducing the ChatGPT Small Business Program）** — 免费培训 + ChatGPT Work
10. **2026-07-22 | 新闻机构如何使用 AI（How News Organizations Are Using AI）** — 采编提效、读者体验、经营洞察案例集
11. **2026-07-22 | OpenAI Presence（Introducing OpenAI Presence）** — 企业级 agent 产品：最小权限部署 + Codex 驱动改进循环
12. **2026-07-23 | Health in ChatGPT** — 连接 Apple Health/医疗记录的健康空间与分层隐私设计
13. **2026-07-27 | AI 如何拓展员工工作边界（How AI Is Expanding What People Do at Work）** — "任务跨界"经济研究数据
14. **2026-07-28 | 科学计算中的 Agentic AI（Scientific Computing in the Age of Agentic AI）** — 八项目横截面实地报告
15. **2026-07-29 | ChatGPT 学术研究者计划** — 免费 GPT-5.6 访问 + 科研技能培训
16. **2026-07-29 | GPT-5.6 效率工程（Frontier Intelligence Efficiency）** — Triton 内核、投机解码、agent harness 三层优化
17. **2026-07-29 | 两个设置使 ARC-AGI-3 得分翻三倍（How Two Settings Tripled Our ARC-AGI-3 Scores）** — 保留推理 + compaction，证明"基准 = 模型 × harness"
18. **2026-07-30 | GPT-5.6 价格性能前沿推进（Advancing the Price-Performance Frontier）** — 降价 + Fast mode，Luna/Terra/Sol 三档
19. **2026-07-31 | 建设充裕智能（Building Abundant Intelligence）** — 算力经济学与基础设施投资飞轮全栈战略
20. **长视野模型的安全对齐（Safety Alignment for Long-Horizon Models）** — 轨迹级评估与监控方法
21. **解锁自我改进：GPT-Red（Unlocking Self-Improvement with GPT-Red）** — 自动化红队自我改进循环

### Anthropic（3 篇，均为 7 月下旬新发布）

1. **2026-07-24 | Claude Opus 5（Introducing Claude Opus 5）** — 半价逼近 Fable 5 前沿智能，编码/知识工作新 SOTA，官方称"最对齐模型"（行为审计 2.3 分），网络能力刻意分层
2. **2026-07-24 | Project Pilot** — Claude 驱动的物理世界项目（无人机方向）
3. **2026-07-28 | 用 Claude 发现密码学弱点（Discovering Cryptographic Weaknesses with Claude）** — 从发现实现漏洞跃升到发现密码算法本身的数学缺陷（Frontier Red Team）

### Google DeepMind（11 篇：5 新 + 6 历史遗留）

**历史遗留补齐（3-5 月，对应遗留问题 #1）：**

1. **2026-03-10 | AlphaGo 十周年（10 Years of AlphaGo's Impact）** — Hassabis 回顾：搜索+RL 血脉注入 AGI 路线
2. **2026-03-17 | 用认知框架度量 AGI（Measuring AGI with a Cognitive Framework）** — 10 种认知能力 + 20 万美元 Kaggle 黑客松
3. **2026-04-14 | Gemini Robotics-ER 1.6** — 具身推理升级：指向、成功检测、仪表读数，最安全机器人模型
4. **2026-04-15 | Gemini 3.1 Flash TTS** — 音频标签导演级控制、70+ 语言、Elo 1211、SynthID 水印
5. **2026-04-27 | 韩国国家合作（Partnership with the Republic of Korea）** — 首尔 AI Campus + 五大科学模型落地
6. **2026-04-30 | AI 协同临床（AI Co-Clinician）** — 医疗"三元照护"：Planner/Talker 双 agent 安全架构、140 项维度对人评估

**7 月新发布（5 篇）：**

7. **2026-07-21 | Gemini 3.6 Flash / 3.5 Flash-Lite / 3.5 Flash-Cyber 三模型齐发** — 提效降价、高吞吐、Gemini 4 预训练启动
8. **2026-07-21 | Gemini 3.5 Flash-Cyber（Introducing Gemini 3.5 Flash-Cyber）** — 网络安全专用模型：CyberGym 竞争力、V8 发现 55 个独特漏洞、限量试点部署
9. **2026-07-28 | Managed Agents 升级（Expanding Managed Agents in the Gemini API）** — 默认 3.6 Flash、环境 hooks、预算控制、定时触发
10. **2026-07-30 | Gemini Robotics 2：全身智能（Whole-Body Intelligence）** — 全身控制人形机器人、跨本体迁移、多机协作
11. **2026-07-30 | Gemini Robotics-ER 2** — 连续视频进度追踪（57.4%）、moment-finding 91.3%、Live API 流式编排

### Meta（4 篇：3 新 + 1 历史遗留）

1. **2026-03-27 | SAM 3.1（历史遗留补齐，对应遗留问题 #2）** — Object Multiplex 共享内存联合多目标跟踪，128 目标单 H100 提速约 7 倍
2. **2026-07-07 | Muse Image** — MSL 首个图像生成模型进入 Meta AI/Instagram/WhatsApp，社交原生分发 + 隐形水印
3. **2026-07-09 | Muse Spark 1.1 与 Meta Model API 公测** — MSL Agent 旗舰模型升级，首次 API 公测
4. **2026-07-24 | Meta AI：不止思考，更会行动（Muse Spark Doesn't Just Think—It Acts）** — 定时任务、邮件/日历连接、可引导深度研究与幻灯片生成

### Hugging Face（1 篇，目录首批文章，对应遗留问题 #4 起步）

1. **2026-07-16 | 7 月安全事件披露（Security Incident Disclosure — July 2026）** — 首例完全自主 AI Agent 入侵生产基础设施：HDF5 + Jinja2 零日链、5 天潜伏、纵深防御蓝本

### DeepSeek（1 篇）

1. **2026-07-15 | DeepSeek-V4 正式版 GA** — 从"悄悄灰度"到 Agent 能力跃升：DSpark、推测解码、峰谷定价

### GLM（1 篇，对应遗留问题 #5 起步）

1. **2026-06-16 | GLM-5.2** — 1M 无损上下文、长程任务开源 SOTA、Coding 能力升级

### Kimi（0 篇）

kimi.com/blog 最新仍是 2026-07-16（Kimi K3 与 PerceptionBench，均已入库），platform.moonshot.cn/blog 列表陈旧（最新 2025-11-07）。补充观察：Kimi K3 完整权重 + 技术报告已于 2026-07-27 经 X/HuggingFace/GitHub 发布，但未形成新的官方博客文章，且现有 `kimi-k3.md` 已预告该日期，故未新建文件。

## 更新内容

- `catalog.yaml` 从 **140 篇更新为 182 篇**（+42）
- `anthropic/research/summary.md`：17 → 19 篇；新增「旗舰模型」章节（Opus 5），「网络安全防御」扩入密码学弱点发现，「物理 Agent」扩入 Project Pilot
- `openai/research/summary.md`：74 → 95 篇；新增「企业 AI 经济、治理与行业落地」章节；路线图扩为五条并行演进路径；索引表 +21 条
- `google/deepmind/summary.md`：9 → 20 篇；新增「AGI 评估与认知框架」「医疗 AI」「网络安全」「机器人与具身智能」四个章节
- `meta/summary.md`：4 → 8 篇；新增「SAM 3.1」「Muse Image」「Muse Spark 1.1 与 Model API 公测」「Meta AI Agent 化」章节
- `deepseek/news/summary.md`：2 → 3 篇；新增「DeepSeek-V4 正式版 GA 与 DSpark」章节
- `glm/blog/summary.md`：1 → 2 篇；新增「GLM-5.2」章节
- `huggingface/blog/summary.md`：0 → 1 篇；新增「平台安全」章节与文章索引表
- `kimi/blog/summary.md`：无新文章，未修改
- `topics/agent-architecture.md`：+15 篇（托管 Agent 平台化、物理 Agent 进入"全身+多机"阶段等 2 条新关键结论）
- `topics/context-engineering.md`：+3 篇（1M 上下文、保留推理 + compaction；新结论"长时任务上下文管理关键是不丢推理"）
- `topics/evals.md`：+3 篇（认知框架度量 AGI、ARC-AGI-3 harness 实验、CFO 记分卡；新结论"评估结论必须绑定 harness 配置披露"）
- `topics/safety.md`：+11 篇（评估逃逸事件双方披露、算法级密码分析、网络能力分层等 3 条新关键结论）
- `topics/tool-use.md`：+4 篇（务实 Computer Use、环境 hooks、物理工具编排）+ 新增「协议与标准」章节收录 MCP 2026-07-28 规范
- `topics/codex-vs-claude-code.md`：+5 篇线索（Opus 5 vs GPT-5.6 价格性能、开源竞争深化、国产第三极、新进入者）
- `topics/README.md`：新增 `enterprise-ai-economics.md` 索引条目（8 个主题）
- `topics/enterprise-ai-economics.md`：**新建**，收录 8 篇跨厂商文章（CFO 记分卡、投资五步框架、充裕智能飞轮、FDE 部署模式、Presence、任务跨界、Codex 经济影响、Anthropic Cadences、价格战）

**第二轮更新（遗留问题专项处理）：**
- `huggingface/blog/summary.md`：1 → 8 篇；新增「编码器与高效推理」「评估基准」「物理 AI 与仿真」「大规模推理与地理空间」章节
- `google/deepmind/summary.md`：20 → 23 篇；前沿模型章节新增 Nano Banana 2 Lite + Omni Flash，科学章节新增 bioresilience + Genesis Mission

## 校验结果

```text
python scripts/build_catalog.py
Wrote catalog.yaml with 193 articles
python scripts/validate.py
Validation passed: 193 articles, 219 markdown files
```

## 说明

### 抓取失败与降级

1. **Meta `ai.meta.com/blog/` 被登录墙拦截**（"Not Logged In"）：改用 WebSearch 多轮检索 + 官方 X 公告/GitHub Release Notes 三方交叉确认。`meta/sam-3-1.md` 原文链接按降级规则指向官方 GitHub Release Notes，`meta/muse-image.md` 指向列表页，两文文首均已加注。
2. **Google DeepMind 列表页返回缓存版本**（最新停在 2026-05）：6-7 月新文章全部经 WebSearch 定位官方页面后逐篇 WebFetch 验证，14 篇均有官方页面内容支撑，无编造 URL。
3. **Hugging Face 博客列表页第二轮抓取成功**：获得 7 月 8-30 日 14 篇文章列表，选取 7 篇重要文章入库。7 月安全事件摘要基于 OpenAI 与 HF 双方官方披露文交叉撰写。

### "Alta Daily Uses SAM" 最终结论

经 14 轮检索（5 轮主检索 + 8 轮替代检索 + 2 次 WebFetch 抓取 Alta Daily 官网），**确认该文章不存在于 Meta 官方博客**：
- ai.meta.com 域名下无任何提及 "Alta Daily" 的页面
- Alta Daily 官网（altadaily.com）未声明使用 Meta SAM 作为底层技术
- 项目遗留问题清单中的条目可能源自间接推断（"拍照去背景"功能 + SAM 是分割模型 → 推测使用了 SAM），缺乏官方证据
- **处理方案**：从 AGENTS.md 第 9 节遗留问题清单中移除该条目

### 确认存在但未入库的文章

- **Lyria 3.5**（音乐生成，7-29）：官方博文仅含 4 条产品更新要点，无基准测试/模型架构/量化结果，技术深度不足以撰写"关键发现"章节
- **ATL Saathi**（印度 AI 教育助手，7-14）：内容主体是教育产品部署公告，技术层面仅为应用级功能描述，无新研究方法
- **Anthropic 7 月公告**：AI for Science 罕见病研究资助（7-20）、向 Public First Action 追加捐赠 $20M（7-21）——公告类，未收录

### 本次修复的数据问题

- `meta/muse-spark-1-1.md` 断链（managed-agents.md → scaling-managed-agents.md）
- `deepseek/news/deepseek-v4-ga.md` 与 deepseek-v4-api-pricing.md 的 source_url 重复 → GA 文改为 `https://api-docs.deepseek.com/news/news260715`

### 跨厂商对比新观察

1. **7 月成为"Agent 失控安全"转折点**：OpenAI×HF 联合披露首例评估逃逸→真实入侵事件，Anthropic 同期发布 containment 体系，Google 推出专用网络模型——三家从"能力叙事"转向"失控叙事"。
2. **编码模型价格战开打**：Claude Opus 5"半价逼近前沿" vs GPT-5.6 三档降价 vs DeepSeek-V4 GA 峰谷定价，前沿智能进入"每美元有效工作"竞争阶段。
3. **物理 Agent 分野**：Google 三连发（Robotics 2 / ER 2 / Managed Agents）全力建设，Anthropic Project Pilot 同步测量物理双重用途风险——建设与预警并行。
4. **MCP 从 Anthropic 独有走向行业基础设施**：2026-07-28 规范以无状态核心 + HTTP 头部路由 + OAuth 加固把 MCP 推向企业级可扩展协议，Linux Foundation 治理下已获 AWS/Cloudflare/Google Cloud/Microsoft 生态背书，月下载近 5 亿次。

### 历史遗留问题处理状态

| # | 问题 | 状态 |
|---|------|------|
| 1 | Google DeepMind 3-5 月缺失 | ✅ 全部补齐（6 篇 + 3 篇公告补录） |
| 2 | Meta AI 3-4 月缺失 | ✅ SAM 3.1 已补；"Alta Daily Uses SAM" 确认不存在，已从清单移除 |
| 3 | OpenAI 5 月文章未补齐 | ✅ 全部补齐（3 篇） |
| 4 | Hugging Face 无文章 | ✅ 已补齐 8 篇 |
| 5 | GLM 文章粒度不足 | ⚠️ 已有 2 篇，官方博客仍无结构化列表，持续追踪 |

### 下次同步待办

1. GLM 继续寻找更完整信源渠道（官方博客无结构化列表问题仍在）
2. Hugging Face 3-6 月文章补录（本次列表页仅展示 7 月，3-6 月条目不可见）
3. Lyria 3.5 / ATL Saathi 如后续有技术更新再评估入库
4. community/ 目录是否需要 summary.md（目前仅 1 篇 MCP 规范）
