# Gemini 4 Argon 全面开放：人人可用（Gemini 4 Argon is now available for everyone）

- **原文链接**: [Gemini 4 Argon is now available for everyone](https://blog.google/innovation-and-ai/models-and-research/gemini-models/introducing-gemini-4-argon/)
- **作者**: Google Gemini 团队（官方博客未署名；Sundar Pichai 同日于 X 宣布）
- **发布日期**: 2026-10-13
- **检索日期**: 2026-10-16
- **标签**: #Gemini #全面开放 #订阅 #Antigravity #API

## 核心观点

发布仅两周后，Google 把 Gemini 4 Argon 从 Fairwind 受限通道推向所有 Google AI Pro 与 Ultra 订阅者：Gemini 应用与 Search 的 AI 模式均可使用，Pichai 同日在 X 公布一批 Googler 用例。付费 API 同步就位——模型 ID `gemini-4-argon` 以 Stable 状态进入 Gemini API 目录。

第三方画像比 Google 自家对比表克制：Artificial Analysis Intelligence Index v4.3.2 上 Argon 以高推理档得 53 分，与 GPT-6 Astra 并列，领先 GPT-6.1 Sol 与 Meta 新发的 Muse Wonder Max 一分，但落后 Claude Opus 5.5/Sonnet 5.5 约五分。"追平第一梯队、未登顶"是外部共识。

GA 同日带来产品化改造：Antigravity 的智能体编码界面进入 macOS 版 Gemini 应用（聊天与编码同窗切换）、主界面新增"任务模式"开关——Gemini 可在你离开电脑时跨 Google 应用持续干活。引入期 API 价格 $2/$10，11-30 后翻倍至 $4/$20。

## 关键发现 / 关键技术

### 1. 开放范围与入口
- Google AI Pro（$19.99/月）与 Ultra 订阅者：Gemini 应用 + Search AI 模式
- 付费 API：`gemini-4-argon` 为 Stable 模型 ID（API 文档 10-13 更新）；不在免费层，不随 AI Pro 计划附带
- 定价：引入期（至 2026-11-30）$2/$10 每 1M token、缓存输入 95% 折扣（$0.10）；12-01 起 $4/$20；Batch/Flex $1/$5，Priority $3.60/$18；支持隐式缓存、不支持显式缓存

### 2. 规格与能力边界（API 模型页）
- 统一上下文 1,048,576 token（输入输出共享）；同步调用默认最大输出 65,536，开启 long decode 可至 1,048,576
- 输入支持文本/图像/视频/音频/PDF，输出文本；代码执行、函数调用、文件搜索、URL context、Search grounding、结构化输出齐备；Computer Use 为 Preview
- 不支持：音频生成、图像生成、Live API——实时语音与文生图仍需专用模型

### 3. 第三方与真实工作负载
- Artificial Index v4.3.2：53 分，平 GPT-6 Astra，领先 GPT-6.1 Sol 与 Muse Wonder Max 各 1 分，落后 Opus 5.5/Sonnet 5.5 约 5 分
- Box 测试：数据分析/生命科学/医疗/法律/教育娱乐全面高于 Gemini 3.1 Pro
- Chrome 团队：约 600 万行网页处理代码重构（4000 万行代码库），数周完成（原需数月），消除整类稳定性问题
- 机器人：输入演示视频→自建仿真→部署实机（Apptronik Apollo 连续投中 7 球），数周级仿真压缩到数小时
- 科研：80,000+ NASA 火星气象日志与 Ingenuity 遥测蒸馏成汇报幻灯片；Pixel CAD 文件经 Antigravity + Blender MCP 生成爆炸视图动画

### 4. 产品整合
- Antigravity 智能体编码界面入驻 macOS 版 Gemini 应用
- 新增"任务模式"开关：跨 Google 应用与服务的后台持续执行
- 日常对话改进：更少对冲、更少重复、避开陈词滥调；长任务给出更频繁的进度更新

## 实践意义

两周内"受限发布→全面开放→Stable API"三连跳，说明 Fairwind 式分阶段发布正在成为可复用的发布节奏，而非一次性姿态。对工程团队，真正的新信息是 API 侧：Stable 模型 ID 意味着可以写进生产配置与回归测试；而"引入期半价"必须在预算表里单列——12 月起成本翻倍，Batch/Flex（$1/$5）是批量任务的正确出口。

产品侧"聊天/编码同窗 + 后台任务模式"把 Gemini 应用从对话工具推向个人 Agent 工作台，直接对标各家编码 Agent 的入口之争。评估建议照旧：长输出、知识工作、SWE 场景优先实测；终端密集与实时语音场景继续用专 用模型。

## 跨厂商对比

- 与 [Claude Opus 5.5](../../anthropic/research/claude-opus-5-5.md) 对比：AA 指数落后约 5 分但价格为一半（$2/$10 vs $4/$20，引入期），Argon 以性价比与 1M 长输出打差异化——两家在"顶尖质量"与"广度+长输出"间各自站位。
- 与 [Muse Wonder](../../meta/muse-wonder.md) 对比：Meta 前一天（10-12）发布 Muse Wonder，AA 指数 Wonder Max 落后 Argon 一分——Google 与 Meta 在"第二梯队头部"的贴身缠斗成为秋季主旋律。
- 与 [Gemini 4 Argon 发布](gemini-4-argon.md) 互补：公告篇定能力与安全框架，本文记录 GA、API Stable 化与产品整合——同一模型的两段生命周期。
- 与 [Antigravity 2.0](antigravity-2.0.md) 对比：Antigravity 5 月定位"Agent-first 开发平台"，本次反向把编码界面嵌入消费级 Gemini 应用——平台与个人工作台的边界开始互溶。

## 资源

- 官方文章：https://blog.google/innovation-and-ai/models-and-research/gemini-models/introducing-gemini-4-argon/
- 论文：无
- 代码：无
- Demo：无
- API 模型页：https://ai.google.dev/gemini-api/docs/models/gemini-4-argon

> 注：官方页正文在检索环境被截断，本文经 gigazine（10-14）、mashable（10-13）、七牛云技术复盘（10-14，API 规格）、Search Engine Journal（10-13）等多源交叉验证；AA 指数以 Artificial Analysis 10-13 榜单为准。
