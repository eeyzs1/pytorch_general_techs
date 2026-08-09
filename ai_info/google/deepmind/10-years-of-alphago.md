# 从围棋到生物学乃至更远：AlphaGo 影响十年（From games to biology and beyond: 10 years of AlphaGo's impact）

- **原文链接**: [From games to biology and beyond: 10 years of AlphaGo’s impact](https://deepmind.google/blog/10-years-of-alphago/)
- **作者**: Demis Hassabis
- **发布日期**: 2026-03-10
- **检索日期**: 2026-08-01
- **标签**: #AlphaGo #AGI #AIforScience #强化学习 #Google

## 核心观点

Hassabis 在 AlphaGo 战胜李世石十周年之际撰文回顾：2016 年超 2 亿观众见证的第 2 局"第 37 手"不仅证明了 AI 能超越模仿人类专家、发现全新策略，更宣告现代 AI 时代提前十年到来。围棋盘面 10^170 种可能位置（远超可观测宇宙原子数）的搜索难题，催生了深度神经网络 + 搜索 + 强化学习这一此后被反复泛化的技术范式。

文章核心主张：AlphaGo 的技术血脉（搜索、规划、与自我对弈强化学习）经由 AlphaZero、AlphaFold、AlphaProof、AlphaEvolve 一路注入今天的 Gemini 与 AGI 路线——"Gemini 的世界模型 + AlphaGo 的搜索规划 + 专用 AI 工具调用"的组合将是通向 AGI 的关键。

## 关键发现 / 关键技术

### 1. 技术谱系
- AlphaGo Zero 从随机对弈自学成为史上最强；AlphaZero 泛化到任意双人完全信息博弈，数小时掌握国际象棋并击败 Stockfish
- 李世石感言：AlphaGo 是"来自未来的路线图"，预告 AI 时代不是遥远模糊的未来

### 2. 科学突破的催化
- **AlphaFold 2**（2020）解决 50 年蛋白质折叠难题：2 亿蛋白质结构免费开放，全球超 300 万研究者使用，2024 年诺贝尔化学奖
- **数学推理**：AlphaProof + AlphaGeometry 2 首个达 IMO 银牌标准；Gemini Deep Think 2025 年达 IMO 金牌水平
- **算法发现**：AlphaEvolve 找到矩阵乘法新解法，迎来自己的"Move 37 时刻"
- **AI co-scientist**：在帝国理工验证中独立复现了研究者耗时多年的抗生素耐药假设
- 另有 AlphaGenome、聚变能源、WeatherNext 等应用

### 3. 通向 AGI 的配方
- Gemini 从第一天起多模态，构建世界模型；最新 Gemini 的推理沿用 AlphaGo/AlphaZero 开创的技术
- 下一代系统需能调用专用工具（如用 AlphaFold 查蛋白质结构）
- 真正的创造力标准：不只是想出围棋新策略，而是发明一个如围棋般深邃优雅的新游戏

## 实践意义

这篇十周年回顾本质是 DeepMind 的 AGI 技术宣言：把"搜索 + 学习 + 世界模型 + 工具"的组合拳正式列为 AGI 路线，与纯 scaling 叙事形成对照。对读者而言，AlphaGo → AlphaFold → AlphaEvolve 的谱系也是理解 Google 当前模型矩阵（Gemini + 专用科学模型）组织方式的最佳框架。

## 跨厂商对比

- 与 [AlphaEvolve](alphaevolve.md) 互补：本文把 AlphaEvolve 定位为"AlphaGo 搜索思想在代码空间的直系后裔"，两篇合读可见 DeepMind 统一的技术世界观
- 与 [AI co-scientist](co-scientist.md) 互补：co-scientist 的"agent 辩论假设"机制正是 AlphaGo 搜索与推理原则向科研协作的迁移

## 资源

- AlphaGo 专题：[deepmind.google/research/alphago](https://deepmind.google/research/alphago/)
- 纪录片：[AlphaGo Movie (YouTube)](https://www.youtube.com/watch?v=WXuK6gekU1Y)
