# Introducing AgentKit

- **原文链接**: [Introducing AgentKit](https://openai.com/index/introducing-agentkit/)
- **发布日期**: 2026-04
- **标签**: #AgentKit #Agent-Builder #Connector-Registry #ChatKit #评估

## 核心观点

AgentKit 是 OpenAI 为开发者和企业打造的完整 Agent 构建工具集，解决了过去构建 Agent 需要协调零散工具的痛点。它包含可视化工作流设计器、连接器管理平台和聊天界面开发包，并扩展了评估能力。

## 关键概念

### 三大核心组件

1. **Agent Builder**
   - 可视化画布，拖拽节点组合逻辑
   - 连接工具并配置自定义防护机制
   - 支持预览运行、内联评估配置和完整版本控制
   - 可从空白画布起步或使用预制模板
   - 案例: Ramp 仅用数小时从零构建采购 Agent；LY Corporation 不到两小时构建工作助手 Agent

2. **Connector Registry**
   - 统一管理员面板，管理 ChatGPT 与 API 的数据源
   - 包含预置连接器（Dropbox、Google Drive、Sharepoint、Microsoft Teams）
   - 支持第三方 MCP

3. **ChatKit**
   - 嵌入基于聊天的 Agent 界面的开发工具包
   - 处理流式响应、对话线程管理、模型思考过程展示
   - 可根据主题或品牌自定义
   - 案例: Canva 开发者社区支持助手节省两周时间

### 评估能力扩展
- **数据集**: 快速构建 Agent 评估，通过自动评分器和人工注释扩展
- **追踪评分**: 对 Agent 工作流端到端评估，自动评分找出不足
- **自动提示优化**: 根据人工注释和评分器输出生成改进提示
- **第三方模型支持**: 在 OpenAI Evals 平台内评估其他供应商模型
- 案例: Carlyle 的多 Agent 尽职调查框架开发周期缩短 50%+，准确率提升 30%

### 强化微调 (RFT)
- 在 o4-mini 上正式发布
- GPT-5 上提供内测版本
- 赋予开发者自定义推理模型的能力

## 实践启示

- AgentKit 将 Agent 开发从"手工作坊"推向"工业化"
- 可视化 + 版本控制是 Agent 工作流管理的关键
- 评估不再是事后补充——内联到构建流程中
- MCP 支持表明 OpenAI 在开放生态上的态度

## 相关文章

- [A Practical Guide to Building Agents](a-practical-guide-to-building-agents.md) — Agent 构建方法论
- [New Tools and Features in the Responses API](new-tools-and-features-in-the-responses-api.md) — AgentKit 的底层 API
- [Harness Engineering](harness-engineering.md) — Agent 工作流的工程实践
