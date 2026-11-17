# Control Room：在推理层集中停止研究工作负载（Control Room）

- **原文链接**: [Control Room: A central system to track and stop model workloads across our research infrastructure](https://openai.com/index/control-room/)
- **作者**: OpenAI
- **发布日期**: 2026-11-09
- **检索日期**: 2026-11-17
- **标签**: #运行时控制 #Agent安全 #基础设施

## 核心观点

Control Room 为研究推理工作负载分配身份，在推理引擎检查其执行授权，把停止控制从分散的任务代码移到较集中的推理入口。

它与失准监控配合，将告警转化为可执行的停止动作。

## 关键发现 / 关键技术

### 1. 机制与适用范围

引擎根据 job_id 检查授权，停止后的任务不能继续获得模型输出；任务进程本身可能仍存活。

### 2. 证据与边界

官方说明授权缓存造成最多 35 秒停止滞后，控制服务故障时拒绝请求；不应将其写成即时杀死全部进程。

## 实践意义

工程解读：分别验证身份覆盖、控制通路、缓存时效与故障时行为。

## 跨厂商对比

- 与 [安全评估运行规范](../../anthropic/engineering/building-strong-safety-evaluations.md) 对照：都将可观测、可中止的执行环境视为评估系统的一部分。

## 资源

- 官方原文：[官方原文](https://openai.com/index/control-room/)
