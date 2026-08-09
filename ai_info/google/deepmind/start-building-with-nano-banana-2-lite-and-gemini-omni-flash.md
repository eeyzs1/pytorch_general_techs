# Nano Banana 2 Lite 与 Gemini Omni Flash 开发者发布（Start building with Nano Banana 2 Lite and Gemini Omni Flash）

- **原文链接**: [Start building with Nano Banana 2 Lite and Gemini Omni Flash](https://deepmind.google/blog/start-building-with-nano-banana-2-lite-and-gemini-omni-flash/)
- **作者**: Alisa Fortin, Anish Nangia (Product Managers, Google DeepMind)
- **发布日期**: 2026-06-30
- **检索日期**: 2026-08-01
- **标签**: #Gemini #ImageGeneration #VideoGeneration #Multimodal #Google

## 核心观点

Google DeepMind 同时发布两款面向开发者的生成式媒体模型：Nano Banana 2 Lite（最快的 Gemini Image 模型）和 Gemini Omni Flash（高质量视频生成与对话式编辑模型）。两者均已在 Google AI Studio、Gemini API 和 Gemini Enterprise Agent Platform 上线，旨在让开发者以更低成本、更高速度构建端到端多媒体体验，将快速图像生成与视频创作和编辑打通。

文章强调生成式媒体的核心是"创意迭代"，这两款模型让开发者可以构建从图像到视频的完整创作管线，并维持多轮编辑的上下文一致性。

## 关键发现 / 关键技术

### 1. Nano Banana 2 Lite 性能指标

- 模型标识：gemini-3.1-flash-lite-image
- 延迟：文本生成图像仅需 **4 秒**，适合交互式原型和快速视觉草拟
- 成本：**$0.034 / 1K 张图像**，面向高吞吐、预算敏感场景
- 定位：替代初代 Nano Banana（gemini-2.5-flash-image），在速度、质量、成本三维度全面改进
- 保留能力：提示词遵循、角色一致性、图内文字渲染

### 2. Nano Banana 家族矩阵

| 模型 | 标识 | 定位 |
|------|------|------|
| Nano Banana 2 Lite | gemini-3.1-flash-lite-image | 极速、高吞吐，速度优先 |
| Nano Banana 2 | gemini-3.1-flash-image | 通用主力，质量与成本平衡 |
| Nano Banana Pro | gemini-3-pro-image | 专业级，强调精度与控制 |
| Nano Banana（旧版） | gemini-2.5-flash-image | 遗留模型，建议升级至 2 Lite |

### 3. Gemini Omni Flash 能力

- 模型标识：gemini-omni-flash-preview
- 定价：**$0.10 / 秒视频输出**（与 Veo 3.1 Fast 同价）
- 核心能力：对话式视频编辑（自然语言修改视频）、多模态引用（图文视频组合输入维持场景一致性）、现实知识调用（历史 / 生物 / 叙事逻辑构建视频）、文字与动作同步
- 限制：当前仅支持 10 秒视频生成；不支持音频引用上传和场景扩展；视频引用不超过 3 秒但模型尚未正确处理；换景 / 平移时角色一致性有限

### 4. 模型链式协作

开发者可将 Nano Banana 2 Lite 生成的高速图像传递给 Gemini Omni Flash 动画化为视频，通过 Interactions API 维持会话历史，支持最多 3 次连续编辑。演示应用包括 Anywhere（自拍换地标并动画化）、Space Lift（室内设计图转电影级展示）、Omni Product Studio（静态商品图转电商视频）。

## 实践意义

这两款模型体现了生成式 AI 从"单次生成"向"迭代创作管线"的演进。Nano Banana 家族的分层定价（Lite / 2 / Pro）让开发者可按场景选择速度-质量-成本的最优解；Omni Flash 的对话式编辑能力将视频创作从"一次成型"转向"多轮精修"。两者均集成 SynthID 水印，延续 Google 在 AI 内容透明度上的策略，并在 Google 消费端（AI Mode in Search、Gemini app、NotebookLM、Google Photos、Google Flow、Google Ads）同步铺开。

## 跨厂商对比

- 与 [Gemini 3.5](gemini-3.5.md) 对比：Gemini 3.5 定义了前沿智能与行动能力的整体框架，本文的 Nano Banana 2 Lite 和 Omni Flash 是其在图像 / 视频生成维度的具体产品化，共享 Gemini 多模态底座但定位为成本敏感的开发者工具
- 与 [Gemini Omni](gemini-omni.md) 互补：Gemini Omni 是"从任意输入创造任意输出"的整体能力宣言，本文的 Omni Flash 是其面向开发者的轻量化、成本优化版本，定价与 Veo 3.1 Fast 持平
- 与 [Introducing Gemini 3.5 Flash Cyber](introducing-gemini-3-5-flash-cyber.md) 对比：Flash Cyber 聚焦网络安全场景的专用模型，Nano Banana 2 Lite / Omni Flash 聚焦创意生成场景，体现 Flash 系列的垂直化分工策略

## 资源

- 博文：https://deepmind.google/blog/start-building-with-nano-banana-2-lite-and-gemini-omni-flash/
- Nano Banana 2 Lite 模型页：https://deepmind.google/models/gemini-image/flash-lite/
- Gemini Omni 模型页：https://deepmind.google/models/gemini-omni/
- Google AI Studio：https://aistudio.google.com/
- Gemini API 文档（Omni）：https://ai.google.dev/gemini-api/docs/omni
- Gemini API 文档（Image）：https://ai.google.dev/gemini-api/docs/image-generation
