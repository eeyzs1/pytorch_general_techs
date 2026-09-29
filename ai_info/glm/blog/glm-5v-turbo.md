# GLM-5V-Turbo:多模态 Coding 基座(GLM-5V-Turbo: A Multimodal Coding Foundation Model)

- **原文链接**: [GLM-5V-Turbo: A Multimodal Coding Foundation Model](https://www.zhipuai.cn/zh/research/156)
- **作者**: 智谱 GLM 团队
- **发布日期**: 2026-04-01
- **检索日期**: 2026-09-29
- **标签**: #GLM-5V-Turbo #多模态 #智谱 #Coding #视觉编码 #Agent

## 核心观点

GLM-5V-Turbo 是智谱面向 Coding 场景的多模态基座:在预训练阶段就完成视觉-文本融合,而非后挂视觉适配器,因此能直接"看懂"设计稿、截图与网页并生成可运行代码,同时支持 200k 上下文。它把多模态从"图片问答"重新定位为"工程输入界面"。

模型在 30+ 任务上做了协同强化学习(覆盖 AndroidWorld、WebVoyager、CC-Bench-V2 与"龙虾基准"等 Agent 基准),技术上采用自研 CogViT 视觉编码器与 MTP(多 token 预测),并深度适配 Claude Code 与 OpenClaw/AutoClaw 等 Agent 框架。字节 TRAE、美团、快手已在生产中给出好评;'股票分析师' Skill 展示了看 K 线 60 秒产出图文研报的垂直能力。

## 关键发现 / 关键技术

### 1. 预训练级视觉-文本融合

融合发生在预训练阶段而非后训练外挂,这是与"视觉适配器"路线的根本区别。

- 视觉能力在预训练阶段与语言联合建模,而非事后对齐
- 直接从设计稿/截图/网页生成可运行代码
- 200k 上下文,容纳完整工程图纸 + 代码库片段
- 融合层级前移带来更稳的版面/图表结构理解

### 2. 自研组件

- CogViT 视觉编码器:面向文档/UI/图表的结构化视觉表征
- MTP(多 Token 预测):提升生成吞吐与规划能力
- 两个组件均在基座内原生训练,非外挂模块

### 3. 30+ 任务协同 RL

用 Agent 环境而非静态图片做强化学习,训练目标与落地形态一致。

- Agent 基准覆盖:AndroidWorld、WebVoyager、CC-Bench-V2、龙虾基准
- 多任务协同强化学习,避免单任务过拟合
- 覆盖移动端、浏览器、编码、龙虾四类 Agent 环境

### 4. 工具链适配

- 深度适配 Claude Code 与 OpenClaw/AutoClaw
- 存量 Agent 工作流可低成本切换到多模态输入
- 与智谱自家 Coding 生态形成"模型-框架"双向耦合

### 5. 生产落地与垂直 Skill

- 字节 TRAE、美团、快手生产环境好评
- '股票分析师' Skill:读取 K 线图 60 秒输出图文研报
- 展示"视觉理解 + 结构化输出"的组合变现路径
- 60 秒级响应说明视觉理解未被置于低优先级流水线

### 6. 生态位

- 与 GLM-5-Turbo 同批发布,文本/视觉双基座并进
- 多模态输入 + Agent 执行在同一个基座内闭环

### 7. 输入形态的工程价值

把"截图→代码"的转换从人工流程变成模型原生能力。

- 设计稿/截图/网页三类输入直接映射到前端与脚本产出
- 200k 上下文支持"整页设计 + 现有代码库"联合理解
- 减少中间的文本描述环节,也就减少了信息损耗

## 实践意义

GLM-5V-Turbo 的价值在于把多模态变成 Coding Agent 的"眼睛":前端工程师可以直接投喂 Figma 截图,运维可以直接投喂监控面板截图,让模型输出代码而非描述。200k 上下文 + Claude Code 适配意味着迁移成本极低——在既有 Agent 工作流里把文本模型换成多模态基座即可。对国内团队,字节/美团/快手的落地背书降低了尝鲜风险;'股票分析师' Skill 则示范了把多模态能力封装为垂直产品的最短路径。

## 跨厂商对比

- 与 [Muse & Glimmer(Hugging Face)](../../huggingface/blog/muse-glimmer-hf.md) 对比:HF 侧开源视觉模型聚焦通用感知能力,GLM-5V-Turbo 把视觉直接焊进 Coding 基座,路径是"垂直场景优先"
- 与 [Kimi Perception Bench](../../kimi/blog/perception-bench.md) 对比:Moonshot 以感知评测体系量化多模态短板,智谱以 30+ 任务协同 RL 直接优化 Agent 场景表现,评测与训练两种推进视角互补
- 与 [GLM-5-Turbo:龙虾增强基座](glm-5-turbo.md) 对照:同批发布的姊妹型号,5-Turbo 强化文本侧工具调用,5V-Turbo 补齐视觉输入,组合覆盖完整 Coding Agent 形态
- 与 [GLM-OCR:SOTA 复杂文档解析](glm-ocr.md) 对照:OCR 用 0.9B 专用模型解决文档输入,5V-Turbo 用预训练级融合解决通用视觉输入,专用与通用两条路线并行

## 资源

- 官方发布:https://www.zhipuai.cn/zh/research/156
- API 文档:https://docs.bigmodel.cn/
- 相关基座:https://www.zhipuai.cn/zh/research/155
- 智谱开放平台:https://www.bigmodel.cn/
