# Gemini Robotics ER 2：机器人的高层大脑（Introducing Gemini Robotics ER 2）

- **原文链接**: [Introducing Gemini Robotics ER 2](https://blog.google/innovation-and-ai/models-and-research/google-deepmind/gemini-robotics-er-2/)
- **作者**: Steven Hansen, Peng Xu
- **发布日期**: 2026-07-30
- **检索日期**: 2026-08-01
- **标签**: #机器人 #具身推理 #视频理解 #多机协作 #Google

## 核心观点

Gemini Robotics ER 2 是 Google 最强具身推理模型，定位为机器人的"高层大脑"：与人交流、理解物理世界、规划多步任务，再把运动执行交给底层 VLA 模型，并可原生调用 Google Search 或任意自定义函数。相比 ER 1.6 的阶跃变化在于时序智能——通过连续视频流追踪自身进度、出错时自我纠正、精确判断进入下一步的时机，并首次引入多机器人协作。

模型发布即通过 Gemini API、Google AI Studio 公开预览（含 Live API 双向流式端点），并在 Gemini Enterprise Agent Platform 私有预览。

## 关键发现 / 关键技术

### 1. 物理 agentic 与工具编排
- 开发者可将 VLA、导航 API 等低层控制接口声明为工具，向模型流式输入视频/音频/文本
- 在真实 VLA、仿真 VLA、人类遥操作三种控制模式下，工具编排能力均稳定超越 ER 1.6
- 接入 Gemini Live API 双向流式端点，消除"停下-思考-再行动"的顿挫；Boston Dynamics Spot 演示按自然语言指令取爆米花（代码已开源）

### 2. 时序智能：进度分类与关键时刻定位
- 进度分类：把视频帧归入 0-100% 五档进度，准确率 57.4%，可实时调整动作或重试失败步骤而不重启整个工作流
- 关键时刻定位（moment-finding）：定位关键事件精确帧（如何时停止倒咖啡），准确率 91.3%、平均绝对时间误差 0.96 秒，执行速度为大模型类别的 4 倍

### 3. 空间智能与安全
- 成功/失败检测升级为原始视频流（捕捉泼洒、滑脱等执行中失败）；仪表读数扩展到数字显示、线性刻度、温度计等 10 种类型
- 在 Safety Instruction Following 与 Human Proximity 基准上超越 ER 1.6 及其他前沿模型：有人在附近时使人形机器人停机，区域清空后自主恢复
- 同步发布"安全 VLA 编排者"基准与安全技术报告

## 实践意义

ER 2 把机器人高层推理从"离散决策"推进到"连续时序感知"，57.4% 的进度分类准确率也诚实标注了当前边界。对开发者而言，"VLA 声明为工具 + Live API 流式编排"的架构可直接复用到巡检、仓储等场景；多机协作语义层则指向 fleet 级机器人调度的未来形态。

## 跨厂商对比

- 与 [Gemini Robotics-ER 1.6](gemini-robotics-er-1-6.md) 对比：ER 2 把成功检测从静态快照升级为连续视频、仪表读数从圆形表盘扩展到 10 类仪器，并新增多机协作——三个月内完成时序化跃迁
- 与 [Gemini Robotics 2](gemini-robotics-2-brings-whole-body-intelligence-to-robots.md) 互补：ER 2 负责"接下来做什么"（规划与验证），Robotics 2 VLA 负责"怎么动"（全身运动控制），两者构成完整物理 agent 栈

## 资源

- 试用：[Google AI Studio](https://ai.dev/prompts/new_chat?model=gemini-robotics-er-2-preview)
- 安全技术报告：[Gemini Robotics 2 Safety (PDF)](https://storage.googleapis.com/deepmind-media/gemini-robotics/Gemini-Robotics-2-Safety.pdf)
- 示例代码：[robotics-samples (GitHub)](https://github.com/google-gemini/robotics-samples/tree/main/live-api)
