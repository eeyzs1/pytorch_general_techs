# GLM-5-Turbo:龙虾增强基座(GLM-5-Turbo: The Lobster-Enhanced Foundation Model)

- **原文链接**: [GLM-5-Turbo: The Lobster-Enhanced Foundation Model](https://www.zhipuai.cn/zh/research/155)
- **作者**: 智谱 GLM 团队
- **发布日期**: 2026-03-15
- **检索日期**: 2026-09-29
- **标签**: #GLM-5-Turbo #智谱 #OpenClaw #Agent #ToolCalling #ZClawBench

## 核心观点

GLM-5-Turbo 是智谱面向 OpenClaw"龙虾"(lobster)场景的增强基座模型,核心理念是"Harness 再多不如模型自身变强"——与其在 Agent 外围堆叠编排框架,不如让模型内生地掌握工具调用与长任务执行。这是对"重 harness、轻模型"路线的正面回应。

模型围绕四大能力建设:Tool Calling、复杂指令拆解、定时持续任务、高吞吐长链路。配套发布 ZClawBench 端到端基准(国产第一),实测 Skills 使用比例从 26% 提升到 45%,Pony-Alpha-2 盲测中 90% 用户认为优于其他国产模型。商业化上,龙虾套餐限购 5 个,高峰 3 倍/非高峰 2 倍计费系数,API 提价 20%。

## 关键发现 / 关键技术

### 1. 设计理念:模型内生能力优先

把 Agent 能力从编排层回收到权重里,是本型号一切技术选择的出发点。

- "Harness 再多不如模型自身变强"
- 减少外部编排层的补丁式修补,把 Agent 能力回收到权重里
- 对用户而言:更薄的 Agent 框架、更低的维护成本

### 2. 四大核心能力

- Tool Calling:工具调用准确率与稳定性
- 复杂指令拆解:多步任务自动分解
- 定时持续任务:长时间驻留执行
- 高吞吐长链路:海量调用下的链路稳定性

### 3. 基准与实测数据

- 发布 ZClawBench 端到端基准,排名国产第一
- Skills 使用比例:26% → 45%,模型更主动地调用技能库
- Pony-Alpha-2 盲测:90% 用户认为优于其他国产模型

### 4. 定价与供给策略

供需紧张第一次被显性化为价格结构,而非排队降级。

- 龙虾套餐限购 5 个,控制算力供给缺口
- 高峰时段 3 倍系数、非高峰 2 倍系数的差异化计费
- API 提价 20%,引导负载向非高峰迁移

### 5. 生态位

- 与 OpenClaw 龙虾场景深度绑定,同批发布的 GLM-5V-Turbo 补齐视觉侧
- ZClawBench 为国产 Agent 模型提供了新的端到端评价标尺
- 模型、基准、套餐三位一体发布

### 6. 能力验证路径

- ZClawBench:端到端场景评测,排名国产第一
- Skills 使用比例 26% → 45%:从"偶尔调用"到"默认调用"的行为迁移
- Pony-Alpha-2 盲测 90% 优于其他国产:体感维度而非跑分维度

### 7. 对 Agent 架构的影响

- 定时持续任务能力让"常驻型 Agent"成为可能
- 高吞吐长链路适配龙虾场景的多步高并发调用
- 工具调用稳定性提升直接减少重试与补偿逻辑

## 实践意义

GLM-5-Turbo 代表了一种"降 harness 复杂度"的工程主张:当模型自身能稳定拆解指令、持续执行定时任务,Agent 框架可以更薄,维护成本随之下降。高峰/非高峰 3 倍/2 倍系数 + 套餐限购的组合,是国产厂商首次把"推理算力稀缺"显性化为定价结构,对重度 Agent 用户的成本模型影响直接——批处理任务应尽量调度到非高峰窗口;Skills 使用比例翻倍(26%→45%)也提示团队:技能库建设的 ROI 正在随模型换代快速上升。

## 跨厂商对比

- 与 [Claude Code 最佳实践](../../anthropic/engineering/claude-code-best-practices.md) 对比:Anthropic 的最佳实践围绕"精心设计 harness 与工作流",GLM-5-Turbo 主张"模型自身变强以简化 harness",两种路线在实践上可折中——薄 harness + 强模型
- 与 [GLM-5V-Turbo:多模态 Coding 基座](glm-5v-turbo.md) 对照:同批发布的姊妹型号,一个强化文本侧 Agent 执行,一个补齐视觉输入
- 与 [GLM-5.1 开源:独立工作 8 小时的模型](glm-5-1.md) 互补:5.1 提供长程任务的开源基座,5-Turbo 面向龙虾场景做了吞吐与工具调用的专项强化
- 与 [GLM Coding Plan 定价修订](glm-coding-plan-pricing-revision.md) 关联:API 提价 20% 与 Coding Plan 的定价调整同属智谱 2026 年商业化节奏的一部分

## 资源

- 官方发布:https://www.zhipuai.cn/zh/research/155
- API 文档:https://docs.bigmodel.cn/
- 多模态姊妹型号:https://www.zhipuai.cn/zh/research/156
- 智谱开放平台:https://www.bigmodel.cn/
