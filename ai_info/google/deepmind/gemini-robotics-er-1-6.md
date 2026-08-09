# Gemini Robotics-ER 1.6：以具身推理驱动真实世界机器人任务（Gemini Robotics-ER 1.6: Powering real-world robotics tasks through enhanced embodied reasoning）

- **原文链接**: [Gemini Robotics-ER 1.6: Powering real-world robotics tasks through enhanced embodied reasoning](https://deepmind.google/blog/gemini-robotics-er-1-6/)
- **作者**: Laura Graesser and Peng Xu
- **发布日期**: 2026-04-14
- **检索日期**: 2026-08-01
- **标签**: #机器人 #具身智能 #Gemini #空间推理 #Google

## 核心观点

Gemini Robotics-ER 1.6 是 Google DeepMind "推理优先"机器人模型的重大升级，专注视觉与空间理解、任务规划和成功检测，作为机器人的高层推理大脑，可原生调用 Google Search、VLA 模型或任意第三方函数来执行任务。相比 ER 1.5 和 Gemini 3.0 Flash，它在指向（pointing）、计数、成功检测上显著提升，并解锁新能力——仪表读数。

文章同时强调这是其"最安全的机器人模型"：在对抗性空间推理任务上的安全策略合规性优于历代模型，并展现出更强的物理安全约束遵守能力。模型当日即通过 Gemini API 与 AI Studio 向开发者开放。

## 关键发现 / 关键技术

### 1. 指向（Pointing）：空间推理的基础
- 指向可表达物体检测计数、关系逻辑（"找出最小的"）、运动推理（轨迹与抓取点）、约束遵循（"指出能放进蓝杯子的所有物体"）
- 对比测试：ER 1.6 正确识别锤子、剪刀、钳子数量且不幻觉不存在的物体；ER 1.5 漏识别并产生幻觉，Gemini 3.0 Flash 接近但精细度不足

### 2. 成功检测与多视角理解
- 成功检测是自主性的决策引擎：判断重试失败步骤还是进入下一阶段
- 多视角推理融合头顶与腕部相机流，在动态、遮挡环境中判断任务完成状态

### 3. 仪表读数：真实世界视觉推理
- 源自与 Boston Dynamics 的设施巡检合作：Spot 机器人读取压力表、垂直液位计、数字读数、 sight glass
- 通过 agentic vision（视觉推理 + 代码执行）实现：先放大图像读取细节，再用指向和代码估算比例与刻度间隔，最终以世界知识解释含义，达到亚刻度精度

### 4. 安全性
- 安全指令遵循（如不操作液体、不抓超过 20kg 物体）相比 ER 1.5 大幅提升
- 在基于真实伤害报告的文本/视频危险识别基准上，较 Gemini 3.0 Flash 提升 +6%（文本）/+10%（视频）

## 实践意义

ER 1.6 展示了"通用 VLM + agentic vision"切入工业场景的路径：仪表读数这类窄而高频的任务正是通用模型替代专用视觉系统的起点。其"邀请开发者提交 10-50 张失败模式标注图"的开放姿态，也说明具身推理仍处于数据驱动的快速迭代期。

## 跨厂商对比

- 与 [Claude Plays Robotics](../../anthropic/research/claude-plays-robotics.md) 对比：Anthropic 验证通用 Claude 直接驱动机器人的可行性，Google 则以专用 ER 模型深耕空间推理与安全约束，一路径轻量一路径重专用化
- 与 [Gemini Robotics ER 2](gemini-robotics-er-2.md) 对比：ER 2 在三个月后实现连续视频理解、进度追踪与多机协作，ER 1.6 的静态快照式成功检测和单视角仪表读数是其直接前身

## 资源

- 模型试用：[Google AI Studio](https://aistudio.google.com/prompts/new_chat?model=gemini-robotics-er-1.6-preview)
- 开发者 Colab：[robotics-samples](https://github.com/google-gemini/robotics-samples/blob/main/Getting%20Started/gemini_robotics_er.ipynb)
