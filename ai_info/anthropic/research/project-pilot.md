# Project Pilot：AI 能控制无人机吗？（Project Pilot: Can AI control a drone?）

- **原文链接**: [Project Pilot: Can AI control a drone?](https://www.anthropic.com/research/project-pilot)
- **作者**: Anthropic 与 Andon Labs
- **发布日期**: 2026-07-24
- **检索日期**: 2026-07-31
- **标签**: #FrontierRedTeam #Robotics #DroneBench #PhysicalAI #双重用途 #Agent

## 核心观点

Project Pilot 是 Anthropic 与 Andon Labs 继 Project Vend（AI 经营小卖部）、Project Fetch（AI 控制机器狗）之后的又一物理世界能力评估：让前沿模型操控真实无人机，自主完成"定位-跟随"类空中监视任务，并沉淀为新基准 Drone-Bench。核心结论是模型使用现成机器人的能力正沿着"编码 Agent 使用软件工具"的轨迹快速逼近实用水平。无人机是典型的双重用途技术（农业增产 vs 军事打击），Frontier Red Team 通过公开测量为"AI 自主操控机器人"的风险治理提供证据基础。

## 关键发现 / 关键技术

### 1. Drone-Bench 基准
- 结合真实飞行与仿真环境，评估模型完成"定位并跟随目标"任务的能力
- 任务类型参照专业/业余无人机的真实使用场景（航拍监视式任务）
- 与 Project Fetch 的机器狗场景互补：飞行机器人对实时性、空间推理要求更高

### 2. 模型物理操控能力的演进轨迹
- Project Fetch Phase Two 已显示模型用现成机器人的能力在快速提升
- 无人机控制比机械臂/机器狗更复杂：三维空间、动态平衡、实时决策
- 模型已能在简单任务上自主完成飞行控制，但离复杂场景仍有距离

### 3. 双重用途风险测量框架
- Frontier Red Team 的定位是"态势感知"：量化 AI 距离自主驾驶机器人还有多远
- 无人机在农业、物流、战争中的广泛使用使其成为物理 AI 风险的最佳测量载体
- 公开基准让外部研究者和政策制定者共享同一份能力证据

## 实践意义

这是"物理 Agent"能力测量的第三块拼图（Vend→Fetch→Pilot），把 AI 风险评估从数字世界（网络安全、生物）扩展到物理世界。对机器人和无人机行业：模型即操控者的时代比预期更近，飞控系统的权限设计与人工接管机制需要提前规划。对政策制定：Drone-Bench 这类公开基准为出口管制、使用限制等讨论提供了可复现的技术证据。

## 跨厂商对比

- 与 [Project Fetch: Phase Two](project-fetch-phase-two.md) 衔接：同一研究线的空中延伸，从四足地面机器人到飞行平台
- 与 [Claude 玩机器人](claude-plays-robotics.md) 对比：Claude Plays Robotics 探索控制抽象边界，Project Pilot 聚焦具体高危载体（无人机）的能力标定
- 与 [Google Gemini Robotics-ER 1.6](../../google/deepmind/gemini-robotics-er-1-6.md) 对比：Google 把具身推理做成可商用模型能力，Anthropic 把同族能力作为风险对象公开测量——"能力建设"与"能力预警"的两种路线

## 资源

- 原文：[Project Pilot: Can AI control a drone?](https://www.anthropic.com/research/project-pilot)
- 前序项目：[Project Fetch: Phase Two](https://www.anthropic.com/research/project-fetch-phase-two)
- 合作方：[Andon Labs](https://andonlabs.com/)
