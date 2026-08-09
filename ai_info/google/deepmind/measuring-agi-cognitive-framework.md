# 度量 AGI 进展：一个认知科学框架（Measuring progress toward AGI: A cognitive framework）

- **原文链接**: [Measuring progress toward AGI: A cognitive framework](https://blog.google/innovation-and-ai/models-and-research/google-deepmind/measuring-agi-cognitive-framework)
- **作者**: Ryan Burnell, Oran Kelly
- **发布日期**: 2026-03-17
- **检索日期**: 2026-08-01
- **标签**: #AGI #评估 #认知科学 #Kaggle #Google

## 核心观点

"我们离 AGI 还有多远"缺乏实证度量工具。Google DeepMind 发布论文《Measuring Progress Toward AGI: A Cognitive Taxonomy》，主张用认知科学为 AI 系统的通用智能建立科学测量基础：将通用智能解构为 10 种关键认知能力，并提出以人类表现为基准的三阶段评估协议。

为把框架落地，DeepMind 联合 Kaggle 发起黑客松，悬赏 20 万美元邀请社区为评估缺口最大的 5 种认知能力设计评测，借助 Kaggle 新上线的 Community Benchmarks 平台对前沿模型进行测试。

## 关键发现 / 关键技术

### 1. 十大认知能力分类法
- 感知、生成、注意、学习、记忆、推理、元认知、执行功能、问题解决、社会认知
- 框架综合心理学、神经科学与认知科学数十年研究构建

### 2. 三阶段评估协议
- 用覆盖各能力的广泛认知任务套件评估 AI（held-out 测试集防数据污染）
- 从人口统计代表性成人样本收集人类基线
- 将 AI 表现映射到人类表现分布中进行定位

### 3. Kaggle 黑客松
- 聚焦评估缺口最大的 5 种能力：学习、元认知、注意、执行功能、社会认知
- 奖金池 20 万美元：每条赛道前两名各 1 万美元，4 个全场最佳各 2.5 万美元
- 提交窗口 3 月 17 日至 4 月 16 日，6 月 1 日公布结果

## 实践意义

这是继各类"AGI 分级框架"之后，前沿实验室首次把 AGI 度量落到可操作的心理测量学协议上，并以众包方式补评估缺口。对评估研究者而言，"人类基线 + 分布映射"的协议设计比单一基准分数更有诊断价值；对厂商而言，认知能力雷达图可能成为下一代系统卡的标准组件。

## 跨厂商对比

- 与 [Anthropic Global Workspace](../../anthropic/research/global-workspace.md) 互补：Anthropic 从认知架构（全局工作空间理论）内部解释模型机制，Google 从认知能力分类外部度量通用智能，两者同为认知科学反哺 AI 的路径
- 与 [Demystifying evals for AI agents](../../anthropic/engineering/demystifying-evals-for-ai-agents.md) 对比：Anthropic 聚焦 agent 任务级评估的工程实践，Google 则试图为"通用智能"本身建立度量学，粒度一微观一宏观

## 资源

- 论文：[Measuring Progress Toward AGI: A Cognitive Taxonomy](https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/measuring-progress-toward-agi/measuring-progress-toward-agi-a-cognitive-framework.pdf)
- 黑客松：[Kaggle 竞赛页](http://kaggle.com/competitions/kaggle-measuring-agi)
