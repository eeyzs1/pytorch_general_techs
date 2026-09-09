# 全球首个"双盲"AI 评估试点（Piloting the world's first double-blind AI evaluations）

- **原文链接**: [Piloting the world's first double-blind AI evaluations](https://deepmind.google/blog/piloting-the-worlds-first-double-blind-ai-evaluations/)
- **作者**: William Isaac、Sol Messing、Kristian Lum
- **发布日期**: 2026-08-27
- **检索日期**: 2026-09-09
  注：官方页面抓取受限，本文基于检索核验的日期与公开报道整理（页首日期/作者/分类经 web_fetch 核验，正文细节经 EvalCommunity 案例研究转述核验）
- **标签**: #评估 #安全 #双盲评估 #基准污染

## 核心观点

Google DeepMind 启动其称为"全球首个双盲 AI 评估"的试点：评估者与被评估的前沿模型互不知情——评估方看不到 Gemini 模型权重，Google 也看不到评估方的保密测试题，以密码学保护的环境同时保全双方的机密资产。

要解决的两个问题是基准污染与评估独立性：模型若已见过评测题，高分不再能证明真实能力（如同考前看过试卷）；而外部评估历来要么交出测试题、要么交出模型权重，两者都有不可接受的风险。双盲方案在此前零日志协议与合同条款之上叠加技术保障，让"独立评估的条件本身"成为评估可信度的一部分。

## 关键发现 / 关键技术

### 1. 双盲机制与技术栈
在 Google Cloud 机密计算产品 Confidential Space 构建的受保护环境中运行评估：保密评测提示与专有模型同处加密隔离域，评估方无法读取权重，Google 无法预览测试集，评测流程仅在受保护环境内完成后输出结果。

### 2. 试点伙伴与被评模型
与新加坡 AI 安全研究所（Singapore AI Safety Institute）、OpenMined、AVERI、MLCommons 合作，在隐私保护环境中用保密基准测试 Gemini Flash Lite 模型；DeepMind 将外部评估定位为内部测试的补充，用于发现盲区与压力测试。

### 3. 方法论边界
双盲只解决"评测材料与模型的机密性"，不自动保证评测有效性——基准是否测量目标构念、测试题是否合适、样例是否有代表性、分析是否恰当，仍取决于评估设计本身。

## 实践意义

对评测机构与监管方，这提供了"技术保障补充合同保障"的模板：当被评厂商可能见到测试集时，机密计算让预注册的保密评测成为可执行流程；对厂商，则是一种可对外证明"没有针对评测优化"的可信度建设。局限同样明显：目前仅是试点，且机制描述与伙伴名单均来自 Google 一侧的叙述。

## 跨厂商对比

- 与 [度量 AGI 进展：一个认知科学框架](measuring-agi-cognitive-framework.md) 对比：认知框架解决"测什么、如何定义能力维度"，双盲评估解决"在什么条件下测才可信"，二者构成评测方法学的正交两轴。
- 与 [两个设置如何让 ARC-AGI-3 成绩翻三倍](../../openai/research/how-two-settings-tripled-our-arc-agi-3-scores.md) 互补：OpenAI 侧展示同一模型因推理设置不同分数可差三倍——评分对条件极度敏感；双盲试点正是把"条件可控且不可提前优化"制度化。
- 与 [BenchMIRT：LLM 基准到底在测什么？](../../huggingface/blog/benchmirt.md) 互补：BenchMIRT 从基准构建角度处理评测效度，本文从环境安全角度处理评测完整性，合读可得"题目可信 + 过程可信"的完整链条。

## 资源

- 官方文章：https://deepmind.google/blog/piloting-the-worlds-first-double-blind-ai-evaluations/
- 产品/API：https://cloud.google.com/security/confidential-space（Confidential Space）
