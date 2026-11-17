# Decision Models：直接评估候选动作的结构化接口（Decision Models）

- **原文链接**: [Decision Models in Hugging Face](https://huggingface.co/blog/decision)
- **作者**: Aritra Roy Gosthipaty, Lysandre, Pedro Cuenca, Tom Aarsen
- **发布日期**: 2026-11-10
- **检索日期**: 2026-11-17
- **标签**: #决策模型 #结构化输出 #推理效率

## 核心观点

Decision Model 从状态与预定义问题出发，直接返回结构化决策及概率，适合路由、抽取和候选项判断等任务。

它与逐 token 生成 JSON 的计算方式不同，也不等同于所有任务都可换成固定分类。

## 关键发现 / 关键技术

### 1. 机制与适用范围

接口把输入状态、问题与候选原语分开，让应用明确可接受的输出空间。

### 2. 证据与边界

Hugging Face 说明 Transformers、llama.cpp、模型发现和训练工具的接入方向，实际运行需对应版本与支持模型。

## 实践意义

工程解读：可比较生成式方案与决策接口的质量、延迟和概率校准，不能仅凭输出格式选型。

## 跨厂商对比

- 与 [Muse Ember](../../meta/muse-ember.md) 对照：一个改变决策接口，一个优化生成式执行模型，解决效率问题的层次不同。

## 资源

- 官方原文：[官方原文](https://huggingface.co/blog/decision)
