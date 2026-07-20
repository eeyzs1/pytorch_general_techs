# Claude 的价值观跨模型与语言：基于价值轴的压缩分析方法

- **原文链接**: [Claude's values across models and languages](https://www.anthropic.com/research/claude-values-models-languages)
- **作者**: Anthropic
- **发布日期**: 2026-07-13
- **检索日期**: 2026-07-20
- **标签**: #价值观 #对齐 #模型行为 #跨语言 #价值轴 #ConstitutionalAI

## 核心观点

Anthropic 提出一种将 Claude 表达的 3,000+ 种价值观压缩为少量**价值轴**（value axes）的方法，每个轴是两个价值观群体之间的数轴（如"情感温暖"vs"严谨"）。通过这种方法，研究系统比较了不同 Claude 模型和不同语言下价值观表达的差异。核心发现：价值观表达存在**系统性跨模型差异**（与训练决策相关）和**跨语言差异**（非英语语言中某些价值观表达更少）。这种方法使大规模价值观审计从"不可能"变为"可操作"。

## 关键发现 / 关键技术

### 1. 价值轴方法
- 将 3,000+ 价值观压缩为少量可解释的轴
- 每个轴是两个价值观群体之间的连续谱（如温暖 vs 严谨）
- Claude 在轴上的位置反映其价值观倾向

### 2. 跨模型差异
- 不同 Claude 模型表达不同价值观 profile
- 与角色训练（character training）和微调决策相关
- 价值轴方法能量化这些差异，连接训练决策与价值观表达

### 3. 跨语言差异
- 非英语语言中某些价值观表达显著更少
- 特别是与"情感表达"相关的价值观
- 英语中心训练数据可能导致价值观表达的"英语偏见"

### 4. 与之前工作的关系
- 基于 [Values in the Wild](https://www.anthropic.com/research/values-wild) 的 700,000 对话分析
- 从"列出价值观"到"理解价值观结构"
- 使价值观审计从描述性变为诊断性

## 实践意义

价值轴方法对 AI 对齐和审计有重要价值：
- **模型比较**：量化比较不同模型的价值观 profile
- **训练审计**：追踪训练决策如何影响价值观表达
- **多语言公平**：识别和纠正跨语言价值观表达差异
- **部署监控**：在生产环境中持续监控价值观漂移

## 跨厂商对比

- 与 [Teaching Claude Why](teaching-claude-why.md) 互补：Teaching Claude Why 关注如何训练价值观，本研究关注如何测量价值观
- 与 [Natural Language Autoencoders](natural-language-autoencoders.md) 对比：NLA 读取模型"内心独白"，价值轴方法分析模型"外在表达"
- 与 [OpenAI Model Spec](../../openai/research/inside-our-approach-to-the-model-spec.md) 对比：OpenAI 公开模型行为规范，Anthropic 开发价值观测量工具

## 资源

- 之前研究：[Values in the Wild](https://www.anthropic.com/research/values-wild)
- Claude 宪法：[Claude's Constitution](https://www.anthropic.com/constitution)
