# Gemini Omni 1.1 Flash：为开发者带来更强创意控制（Gemini Omni 1.1 Flash lets you build with more control）

- **原文链接**: [Gemini Omni 1.1 Flash lets you build with more control](https://blog.google/innovation-and-ai/technology/developers-tools/build-with-gemini-omni-1-1-flash/)
- **作者**: Google（开发者工具团队，官方博客未署名）
- **发布日期**: 2026-08-27
- **检索日期**: 2026-09-09
  注：官方页面抓取受限，本文基于检索核验的日期与公开报道整理（细节经 AI Primer 对 Google 开发者指南的转述核验）
- **标签**: #GeminiOmni #视频生成 #创意控制 #开发者工具

## 核心观点

Google 面向开发者推出 Gemini Omni 1.1 Flash，把生成式视频的"创意控制"作为核心卖点：视频片段可作为参考素材输入（最多 3 段），首帧/末帧关键帧插值可指定运镜起止，10 秒增量续拍并以最多 10 秒前文为上下文，可串成最长 40 秒的连续叙事。官方开发指南演示了在单个不间断镜头内，把三段舞蹈的编排分别移植到狗、章鱼、熊三个角色上。

分辨率路径被拆成"草稿—成品"两级：360p 草稿比 720p 快最多 60%、成本约三分之一，定稿可输出 1080p 或 4K。视频生成由此从"抽卡"转向可控的迭代式生产流程。

## 关键发现 / 关键技术

### 1. 视频作为参考输入 + 关键帧控制
除图像与文本外，Omni 1.1 接受最多 3 段参考视频（Google 功能说明为最多 3 秒参考素材），可在单个不间断镜头内做角色与编排迁移；首末帧插值用于运镜环绕、变焦过渡与无缝循环。

### 2. 场景延续（Scene Extension）
以 10 秒为增量续拍，每次续拍读取最多 10 秒此前画面作为上下文（替代此前仅取最后一秒的参考窗口），累计上限 40 秒；API 层通过 previous_interaction_id 加新文本指令实现延续，官方示例包括推拉变焦、急推变焦与围绕定格角色的 360° 环绕。

### 3. 分级分辨率与多渠道开放
360p 草稿（快最多 60%、约 1/3 成本）→ 720p 标准 → 1080p/4K 成品；接入面：Google AI Studio（Gemini API）、Gemini Enterprise Agent Platform、Flow（面向 Google AI Plus/Pro/Ultra 订阅者，含低积分草稿循环与 720p 下载）、Gemini app（场景延续），第三方 Pika API Club 同步上架。

## 实践意义

对内容工具开发者，参考视频+关键帧+续拍的组合把"可复现的镜头语言"写进 API，显著降低视频 Agent 与批量创意管线的编排成本；草稿/成品分离的计费结构也使迭代试错成本可预算。需注意各数值（60% 更快、1/3 成本、40 秒上限）来自 Google 官方文档与社区转述，实际吞吐因平台而异。

## 跨厂商对比

- 与 [Nano Banana 2 Lite 与 Gemini Omni Flash 开发者发布](start-building-with-nano-banana-2-lite-and-gemini-omni-flash.md) 对比：前作确立 Omni Flash"多模态生成 + API 优先"的定位，1.1 版把控制粒度从提示词细化到参考视频、关键帧与续拍的交互结构。
- 与 [发布 Veo 3.1 与 Flow 的高级能力](veo-3-1.md) 互补：Veo 系列面向影院级生成质量与 Flow 创作界面，Omni 1.1 Flash 面向开发者 API 的可控组合与成本分层，分别覆盖"质量优先"与"迭代优先"两类视频生产场景。

## 资源

- 官方文章：https://blog.google/innovation-and-ai/technology/developers-tools/build-with-gemini-omni-1-1-flash/
- 产品/API：https://aistudio.google.com/
