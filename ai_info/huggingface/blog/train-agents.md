# Agent 后训练课程：从轨迹模仿到完整运行反馈（Post-training Agents）

- **原文链接**: [A curriculum for post-training agents](https://huggingface.co/blog/huggingface/train-agents)
- **作者**: Ben Burtenshaw, Sergio Paniego, merve
- **发布日期**: 2026-10-20
- **检索日期**: 2026-11-17
- **标签**: #Agent后训练 #TRL #强化学习

## 核心观点

Hugging Face 将 Agent 后训练整理为 SFT、蒸馏、RL、环境交互和 harness 扩展五步。

学习对象从单次答案扩展为多轮工具调用与环境反馈的完整轨迹。

## 关键发现 / 关键技术

### 1. 机制与适用范围

每一步对应数据、教师、奖励函数、环境或 harness 等不同前置资产，不是依次打开几个训练开关。

### 2. 证据与边界

课程指出只模仿正确轨迹不足以学习自身失败后的恢复，on-policy 方法和环境反馈因此具有不同作用。

## 实践意义

工程解读：先定义任务、环境、奖励和验证器，再决定训练方法及规模。

## 跨厂商对比

- 与 [DeepSeek 1017 更新](../../deepseek/news/news261017.md) 对照：课程训练机制与产品侧后训练改进互为学习参照。

## 资源

- 官方原文：[官方原文](https://huggingface.co/blog/huggingface/train-agents)
