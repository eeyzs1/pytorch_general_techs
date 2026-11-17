# Kimi K3.1 Pro：扩大后训练与长程任务能力（Kimi K3.1 Pro）

- **原文链接**: [Introducing Kimi K3.1 Pro](https://www.kimi.com/en/blog/kimi-k3-1-pro)
- **作者**: Moonshot AI
- **发布日期**: 2026-10-24
- **检索日期**: 2026-11-17
- **标签**: #Kimi #长程任务 #开放权重

## 核心观点

Kimi 介绍 K3.1 Pro 的后训练扩展、百万 token 上下文及编程、创作和专业工作能力。

技术博客强调训练框架、环境与 rollout 调度等配套工程，而不是仅增加推理时长。

## 关键发现 / 关键技术

### 1. 机制与适用范围

官方给出多种公开与内部基准，应保留任务、harness、采样与评分口径；幻觉压力测试不是日常请求错误率。

### 2. 证据与边界

原文给出权重发布计划，本次另核对到官方 Hugging Face 模型页；开放权重使用 kimi-k3.1-pro 许可证，不等同于 Apache / MIT。

## 实践意义

工程解读：同时核对模型许可、执行框架与目标任务质量；不能由上下文长度推断长任务必然成功。

## 跨厂商对比

- 与 [DeepSeek 1017](../../deepseek/news/news261017.md) 对照：对照两家后训练与工程环境协同改进。

## 资源

- 官方原文：[官方原文](https://www.kimi.com/en/blog/kimi-k3-1-pro)
- 模型与许可证：[模型与许可证](https://huggingface.co/moonshotai/Kimi-K3.1-Pro)
