# GLM-5 技术报告(GLM-5 Technical Report)

- **原文链接**: [GLM-5 Technical Report](https://www.zhipuai.cn/zh/research/153)
- **作者**: Z.ai GLM Team
- **发布日期**: 2026-02-21
- **检索日期**: 2026-09-29
- **标签**: #GLM-5 #技术报告 #MoE #稀疏注意力 #异步RL #QAT #国产芯片

## 核心观点

GLM-5 技术报告披露了这一代旗舰的完整配方:744B 总参数 / 40B 激活的 MoE(256 个专家、80 层),在 28.5T tokens 上预训练,并首次集成 DeepSeek Sparse Attention——通过继续预训练 20B token 完成适配,长序列注意力计算量降低 1.5-2 倍。

后训练侧亮点密集:中期训练按 32K/128K/200K 三阶段扩展上下文;构造 1000 万 issue-PR 对(160B token)的编程数据;基础设施采用异步 RL + 异步 Agent RL + 跨阶段在线蒸馏 + INT4 QAT 量化的组合。GLM-5 在 AA 指数 v4.0 得 50 分创开源 SOTA,SWE-bench Verified 77.8、Terminal-Bench 2.0 56.2;同时适配昇腾等七大国产芯片,单台 Atlas 800T A3 以 W4A8 即可容纳 750B 级模型。

## 关键发现 / 关键技术

### 1. 架构与预训练

稀疏激活 MoE + 外来稀疏注意力的"双稀疏"组合是 GLM-5 的效率底座。

- 744B 总参数 / 40B 激活,MoE:256 专家、80 层
- 预训练数据 28.5T tokens
- 首次集成 DeepSeek Sparse Attention:继续预训练 20B token 适配
- 长序列注意力计算降低 1.5-2 倍

### 2. 中期训练:三阶段上下文扩展

- 32K → 128K → 200K 逐阶段扩展
- 分阶段课程避免一次性拉长上下文导致的训练不稳定
- 与稀疏注意力协同,控制长序列的注意力开销

### 3. 后训练数据

用真实软件工程工作流数据替代孤立的代码片段。

- 1000 万 issue-PR 对,合计 160B token
- 覆盖 issue 描述、代码变更、评审反馈的全过程
- 为 Agent 化编程行为提供过程级监督信号

### 4. 后训练基础设施

- 异步 RL 基础设施 + 异步 Agent RL
- 跨阶段在线蒸馏:训练各阶段之间持续互相传递能力
- INT4 QAT(量化感知训练):精度前移到训练期,部署期零额外成本

### 5. 基准成绩

- AA 指数 v4.0:50 分,开源 SOTA
- SWE-bench Verified:77.8
- Terminal-Bench 2.0:56.2
- 编程与终端两条 Agent 主战场均处第一梯队

### 6. 国产算力适配

- 适配昇腾等七大国产芯片
- 单台 Atlas 800T A3 以 W4A8 容纳 750B 级模型
- 旗舰能力单机可部署,私有化门槛大幅降低

### 7. 报告的复现价值

- 架构、数据配比、训练阶段、量化策略全链路披露
- DeepSeek Sparse Attention 的 20B token 适配经验可迁移
- 异步 RL + 在线蒸馏管线为后续开源模型训练提供参考实现

## 实践意义

这份报告是国产旗舰模型工程化程度的一次集中展示:稀疏注意力借鉴 DeepSeek 并以 20B token 继续预训练完成"移植",说明先进注意力方案已可跨架构复用;异步 RL + 在线蒸馏 + QAT 的组合为"训练-部署一体化"提供了模板。对国内企业最关键的是部署侧结论——单台 Atlas 800T A3(W4A8)容纳 750B 模型,意味着旗舰级能力可以在不组集群的前提下私有化,合规敏感行业从此有了可行解。

## 跨厂商对比

- 与 [DeepSeek-V4](../../deepseek/news/deepseek-v4.md) 对比:GLM-5 直接集成 DeepSeek Sparse Attention,体现国产厂商之间"架构成果互鉴"的独特生态;两者在 Agent/编程基准上同场竞技
- 与 [GLM-5 开源:Agentic Engineering 时代最好的开源模型](glm-5-open-source.md) 互补:开源公告面向开发者叙事,本报告补齐全部技术细节与数据
- 与 [Kimi K3 开放前沿智能](../../kimi/blog/kimi-k3.md) 对比:同为开源旗舰,K3 走大参数路线,GLM-5 以 40B 激活 + 稀疏注意力换推理效率
- 与 [智谱联合华为开源国产芯片训练的 GLM-Image](glm-image-huawei.md) 互补:GLM-5 验证国产芯片的推理与训练适配,GLM-Image 走得更远——全流程训练都在国产栈完成

## 资源

- 官方发布:https://www.zhipuai.cn/zh/research/153
- 论文:https://arxiv.org/abs/2602.15763
- 开源公告:https://www.zhipuai.cn/zh/research/154
- 智谱开放平台:https://www.bigmodel.cn/
