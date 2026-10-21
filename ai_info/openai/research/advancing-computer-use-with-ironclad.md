# 携手 Ironclad 推进计算机操作：把合同工作流变成训练与评测任务（Advancing computer use with Ironclad）

- **原文链接**: [Advancing computer use with Ironclad](https://openai.com/index/advancing-computer-use-with-ironclad)
- **作者**: OpenAI × Ironclad
- **发布日期**: 2026-10-06
- **检索日期**: 2026-10-16
- **标签**: #ComputerUse #专业工作流 #合同智能体 #训练与评测 #企业落地

## 核心观点

OpenAI 与合同管理平台 Ironclad 公开研究合作：不是演示"AI 会点网页"，而是把复杂合同工作流（状态机式的合同生命周期 + 法务审批 + 字段级约束）转化为 AI 智能体的训练与评测任务，以此推进面向专业工作的 computer use。合作的核心命题是：当 Agent 进入财务、采购、法务后台，如何证明它理解业务规则、没有越权、留下了可复核的证据链。

## 关键发现 / 关键技术

### 1. 为什么合同是 computer use 的"硬考场"
- 合同有草稿/审核中/已批准/待签署/已签署等多状态，同一操作在不同状态下权限完全不同（草稿可编辑、已签署只能走补充协议）——Agent 若只看见"编辑按钮存在"，就可能做出技术上成功、业务上越界的动作。
- "改对显示字段"≠"改对业务"：付款周期可能同时存在于展示文本与参与审批的结构化字段，只改前者就是事故。

### 2. 从结果评测到行为评测
- 合作强调的评测转向：不只问"最后是不是改成了 45 天"（Outcome），还要问"改的是哪份合同、从哪读的旧值、按什么顺序调用工具、是否产生未授权副作用"（Behavioral）。
- Trace 作为证据链：合格轨迹须回答用户要什么、Agent 认的是哪份对象、读了哪些规则、依次做了什么、系统最终变了什么——事件序列式留痕而非思考文本堆砌。
- 评测集须覆盖"应该停下"的时刻：同名合同须询问、超策略上限须转人工、已签署须拒绝、审批服务不可用须保留草稿。

### 3. 对行业的溢出价值
- 中文测试社区随即以该合作为底本提出 Computer Use Agent 验收方法论（环境/身份/行为/证据四层验收表、越权率与人工确认率纳入回归指标）——专业工作流评测正在成为 QA 学科的新分支。

## 实践意义

1. **专业软件 Agent 的验收范式**：状态定义 → 行为路径断言 → 副作用与证据回归，可直接迁移到退款审批、优惠券配置、工单流转等任何后台流程。
2. **确定性规则优先、语义判断兜底**：合同 ID、角色权限、状态迁移用代码断言，只有开放性说明质量交给 LLM 裁判——企业 Agent 质量门禁的可行配方。
3. **厂商-垂直平台共建评测**：与 Ironclad 式的领域厂商合作生成训练/评测任务，可能成为 computer use 数据难题的标准解法。

## 跨厂商对比

- 与 [GPT-6 Astra：面向工作的下一代智能](gpt-6-astra-next-generation-of-work.md) 衔接：Astra 工作篇展示 computer use 能力上限，Ironclad 合作补上"专业工作流如何被系统性评测"的下半篇——能力与验收配对才敢进生产。
- 与 [Astra for Law](astra-for-law.md) 互补：Astra for Law 是法律行业的产品化打包，Ironclad 合作是合同工作流的研究级评测基建——一个卖能力，一个建考场。
- 与 [Cognition 用 Astra 让 Devin 测试自己的工作](cognition-devin-testing-with-astra.md) 同观：两家都在解决"Agent 干完 ≠ 干对"，Cognition 走自我验收，OpenAI×Ironclad 走领域专家共建行为断言。

## 资源

- 官方发布（Publication 类）：[Advancing computer use with Ironclad](https://openai.com/index/advancing-computer-use-with-ironclad)
- 第三方衍生：[阿里云开发者社区：测试会操作专业软件的 Agent](https://developer.aliyun.com/article/1769074)（霍格沃兹测试开发学社，基于该合作研究整理的验收方法论）
- 相关条目：[equipping-the-responses-api-with-a-computer-environment](equipping-the-responses-api-with-a-computer-environment.md)

> 注:openai.com 原文 403；本文基于官方 RSS 摘要 + 阿里云/腾讯云开发者社区对该合作的转述整理（两处为同一来源的转载，深度细节有限），官方页面可达后建议复核。
