# Gemini Robotics 2 为机器人带来全身智能（Gemini Robotics 2 brings whole body intelligence to robots）

- **原文链接**: [Gemini Robotics 2 brings whole body intelligence to robots](https://deepmind.google/blog/gemini-robotics-2-brings-whole-body-intelligence-to-robots/)
- **作者**: Carolina Parada
- **发布日期**: 2026-07-30
- **检索日期**: 2026-08-01
- **标签**: #机器人 #具身智能 #VLA #人形机器人 #Google

## 核心观点

Google DeepMind 发布 Gemini Robotics 2 系列——驱动下一代自适应机器人的"智能层"，实现三大突破：智能全身控制、高级灵巧操作、多机器人协作。此前模型只能控制人形机器人上半身完成桌面任务，Gemini Robotics 2 首次把物理 AI 扩展到全身运动：行走、下蹲、伸展与操作一体化，且可本地运行、数小时内适配全新机器人本体。

系列包含三个模型：Gemini Robotics 2（VLA，端到端运动控制）、Gemini Robotics ER 2（VLM 推理大脑，规划分钟级多步任务并协调机器人团队）、Gemini Robotics On-Device 2（端侧高效 VLA）。

## 关键发现 / 关键技术

### 1. 全身控制人形机器人
- 演示：Apptronik Apollo 2 接收"把浇水壶放进底层架子绿色收纳箱"指令后，自主走向桌子、拿起水壶、移动至货架并精确放置
- 同一模型检查点跨三种本体：Apollo 2 + SharpaWave 灵巧手、Apollo 2 + Inspire 手、Franka Duo + Robotiq 夹爪

### 2. 灵巧操作与成功率
- 拧下灯泡成功率 92%（控制手指力度避免捏碎）
- 多指灵巧任务仍是难点：装灯泡 36%，扎垃圾袋、封 Ziplock 袋等任务成功率 32%-44%，地面拾取约 46%
- 官方定位：全身与夹爪类任务达中高水平成功率，多指操作具挑战性

### 3. 多机器人协作与开放策略
- ER 2 作为共享语义理解层，让不同形态机器人分工完成单机无法完成的复杂工作流
- ER 2 当日上线 Google AI Studio 公开预览，Gemini Enterprise Agent Platform 私有预览
- VLA 与 On-Device 模型先向早期合作伙伴开放；On-Device 2 用数小时数据即可适配新本体

## 实践意义

"全身控制 + 跨本体迁移 + 端侧适配"三件套直击机器人学习两大痛点——技能难以跨硬件迁移、泛化依赖大量本体特定数据。但官方坦诚的成功率数据（精细多指操作 32%-46%）也说明：通用人形机器人离可靠商用仍有明显距离，当前更适合半结构化场景。

## 跨厂商对比

- 与 [Claude Plays Robotics](../../anthropic/research/claude-plays-robotics.md) 对比：Anthropic 走"通用大模型直接玩机器人"的轻量验证路线，Google 则以 VLA + ER + On-Device 三模型分层架构重投入全身控制，工程深度与目标场景差异明显
- 与 [Gemini Robotics-ER 1.6](gemini-robotics-er-1-6.md) 对比：1.6 解决"看清与判断"（指向、成功检测、仪表读数），Robotics 2 解决"全身动起来"（运动控制 + 多机协作），三个月完成从感知大脑到运动智能的闭环

## 资源

- 开发者博客：[Introducing Gemini Robotics ER 2](https://blog.google/innovation-and-ai/models-and-research/google-deepmind/gemini-robotics-er-2/)
- 模型页：[Gemini Robotics](https://deepmind.google/models/gemini-robotics/vla/)
