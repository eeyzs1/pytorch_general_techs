# 法律行业为何用 Kimi K3(Why the Legal Industry Runs on Kimi K3)

- **原文链接**: [Why the Legal Industry Runs on Kimi K3](https://www.kimi.com/news/kimi-k3-legal)
- **作者**: Moonshot AI
- **发布日期**: 2026-08-28
- **检索日期**: 2026-09-29
- **标签**: #法律科技 #HarveyLAB #Tenet #领域模型 #开源模型

## 核心观点

Artificial Analysis 在 Harvey LAB 上测得 K3 全通过率 26.7% 居首——这套基准由 1200+ 真实律所任务构成,每题设几十条专家评分点、须全部通过才算通过;K2.6 通过率为 0,此前全球最强模型也只有约 10%。K3 把法律实务可用性的天花板抬高了数倍。

Harvey(OpenAI 投资、估值 110 亿美元)基于 K3 发布首个法律行业模型 Tenet,多项法律基准超过最先进闭源模型;国内多家红圈律所采购 Kimi 企业版。"开源通用模型 + 领域后训练"正在成为垂直 SOTA 的新范式。

## 关键发现 / 关键技术

### 1. Harvey LAB:全通过率 26.7% 居首

- 基准构成:1200+ 真实律所任务;每题几十条专家评分点,须全部通过
- K3 全通过率 26.7%,排名第一
- 对照:K2.6 为 0;此前全球最强模型约 10%

### 2. Tenet:Harvey 基于 K3 的法律行业模型

- Harvey:OpenAI 投资,估值 110 亿美元
- Tenet 为首个基于 K3 的法律行业模型,多项法律基准超越最先进闭源模型
- 路径:开源通用底座 + 法律领域后训练
- 值得注意的是:Harvey 由 OpenAI 投资,却选择 K3 开源权重作为 Tenet 底座——后训练可控性胜过资本关系

### 3. 国内红圈律所采购

- 多家红圈律所采购 Kimi 企业版,法律成为 K3 企业化最快的行业之一

### 4. 法律工作流

- 合同拆解 + Word 批注 + 修订稿输出,覆盖合同审查全流程
- 华宇元典/天眼查可溯源检索,引用带文号/案号,可回溯核验
- 腾讯会议 CLI 插件:会议纪要与任务跟进进入律师工作流
- 邮箱插件:邮件场景直接调用,无需切换工具

### 5. 新范式:开源底座 + 领域后训练

- 闭源 API 模型无法被第三方后训练;开源权重让 Harvey 这类垂直公司能造出自己的 SOTA
- Tenet 证明:垂直最优解可以长在开源通用模型之上

## 实践意义

- **评测要贴近实务**:Harvey LAB 的"全评分点通过"口径比平均分更接近法律交付标准,可作为垂直领域评测设计参照
- **开源模型的第二增长曲线**:被 Harvey 选为底座说明开源权重的可控性与可后训练性是垂直厂商的刚需
- **工作流嵌入决定采用率**:批注、溯源检索、会议/邮箱插件决定律师是否真的用起来,模型分数只是入场券

## 跨厂商对比

- 与 [Harness Engineering](../../openai/research/harness-engineering.md) 对比:OpenAI 强调 harness 决定 Agent 上限;法律场景同理,成败在华宇元典检索、Word 批注等工作流编排而非裸模型
- 与 [GLM-5.3](../../glm/blog/glm-5-3.md) 对比:同为国内开源前沿模型争夺垂直底座地位,K3 已拿下 Harvey/Tenet 标杆案例
- 与 [Kimi K3](kimi-k3.md) 关联:本文是 K3 发布后最重要的行业验证之一,把基准分数翻译成律所采购决策

## 资源

- 发布:[Why the Legal Industry Runs on Kimi K3](https://www.kimi.com/news/kimi-k3-legal)
- K3 权重:[Hugging Face - moonshotai/Kimi-K3](https://huggingface.co/moonshotai/Kimi-K3)
- Harvey:[harvey.ai](https://www.harvey.ai/)
