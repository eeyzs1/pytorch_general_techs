# 用 Computer Use、Skills API 与 Files API 构建生产级 Agent（Build production agents with computer use, the Skills API, and the Files API）

- **原文链接**: [Build production agents with computer use, the Skills API, and the Files API](https://claude.com/blog/computer-use-skills-api-files-api)
- **作者**: Anthropic
- **发布日期**: 2026-08-20
- **检索日期**: 2026-08-21
- **标签**: #Anthropic #ComputerUse #SkillsAPI #FilesAPI #Agent #浏览器工具 #GA

## 核心观点

Anthropic 宣布 Computer Use、Skills API 与 Files API 三大能力在 Claude Platform 全面 GA（一般可用）。三者的组合让开发者可以构建"能操作软件、应用团队专业经验、返回成品文件"的生产级 Agent。Computer Use 新增浏览器工具（browser use tool），让 Agent 在网页应用中按页面结构定位元素而非屏幕坐标。

这标志着 Agent 开发从"单点能力"走向"完整生产栈"：Computer Use 解决"操作"，Skills API 解决"专业知识注入"，Files API 解决"产出交付"。三者合一后，Agent 可以端到端完成"看懂软件 → 用团队方法论操作 → 产出结构化文件"的完整工作流。

## 关键发现 / 关键技术

### 1. Computer Use GA + 浏览器工具
- Agent 通过截图"看见"软件，像人一样点击、输入、滚动
- 可操作从未为自动化设计的应用
- 新增 browser use tool：读取页面结构，作用于具体字段/按钮而非屏幕坐标

### 2. Skills API GA
- 把团队的专业知识（方法论、流程、偏好）打包为可复用技能
- Agent 按需加载技能，实现"团队经验的程序化注入"
- 与 Agent Skills 生态（SKILL.md）衔接

### 3. Files API GA
- 支持 Agent 返回结构化成品文件
- 与 Computer Use 的"操作"和 Skills 的"方法"构成产出闭环
- 面向生产工作流的文件级交付

### 4. 生产级定位
- 三大 API 全部 GA，标志技术成熟度达到生产标准
- 面向企业 Agent 构建者而非实验用户
- 与 [Claude Enterprise 推理钩子](claude-enterprise-inference-hooks.md) 的企业安全栈互补

## 实践意义

Agent 构建的"三件套"（看 + 懂 + 交付）在 Anthropic 平台全面可用，开发者无需拼接多个厂商能力。browser use tool 解决了一个长期痛点：Agent 在浏览器中只能按坐标盲点，现在能理解页面结构语义操作。对企业而言，这意味着"操作遗留系统 + 注入领域方法 + 产出成品"的完整 Agent 闭环可以全栈落地。

## 跨厂商对比

- 与 [Muse Spark 1.1 的务实 Computer Use](../../meta/muse-spark-1-1.md) 对比：Meta 强调"按场景自选执行方式"，Anthropic 强调"平台级三 API 组合"，两种路线分别代表策略选择与基础设施完备
- 与 [Equipping the Responses API with a Computer Environment](../../openai/research/equipping-the-responses-api-with-a-computer-environment.md) 对比：OpenAI 用 Shell 工具 + 容器提供计算机环境，Anthropic 用 Computer Use + Skills + Files 提供操作环境，工具哲学的差异：执行 vs 操作
- 与 [Inference Hooks 企业 DLP](claude-enterprise-inference-hooks.md) 互补：前者管 Agent 操作内容的安全，本文管 Agent 操作能力的构建

## 资源

- 论文：N/A
- 官方公告：https://claude.com/blog/computer-use-skills-api-files-api
- Claude Platform 文档：https://platform.claude.com/
