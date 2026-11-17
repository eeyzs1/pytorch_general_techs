# 前沿模型失准监控：从探针到调查闭环（Frontier Model Misalignment）

- **原文链接**: [How we detect frontier model misalignment](https://openai.com/index/how-we-detect-frontier-model-misalignment/)
- **作者**: OpenAI
- **发布日期**: 2026-10-29
- **检索日期**: 2026-11-17
- **标签**: #失准监控 #Agent安全 #评估

## 核心观点

OpenAI 介绍覆盖训练、评估与内部使用的分层失准监控，将模型行为、动作及环境影响放在同一条检测链路中。

文章强调监控是纵深防御的一层，需要与对齐训练、访问控制和人工响应配合。

## 关键发现 / 关键技术

### 1. 机制与适用范围

用激活探针、模型审查、调查智能体及自动调查分层分配检测成本，最终接入人工处置。

### 2. 证据与边界

对历史事件重放、当前流量审计和红队测试分别验证监控能力；历史重放中的提前发现不等于事件当时已被阻止。

## 实践意义

工程解读：评估运行也应纳入监控覆盖，告警质量与响应链路要分别测量。

## 跨厂商对比

- 与 [安全评估方法](../../anthropic/engineering/building-strong-safety-evaluations.md) 对照：评测设计与运行监控互补，均不能只看最终分数。

## 资源

- 官方原文：[官方原文](https://openai.com/index/how-we-detect-frontier-model-misalignment/)
