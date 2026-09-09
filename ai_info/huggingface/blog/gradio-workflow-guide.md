# 连线、运行、部署：Gradio 中的 AI 工作流（Wire It, Run It, Deploy It: AI Workflows in Gradio）

- **原文链接**: [Wire It, Run It, Deploy It: AI Workflows in Gradio](https://huggingface.co/blog/gradio-workflow-guide)
- **作者**: yuvraj sharma、Abubakar Abid（Gradio 团队）
- **发布日期**: 2026-08-25
- **检索日期**: 2026-09-09
- **标签**: #Gradio #工作流编排 #低代码 #部署 #REST API #HuggingFace

## 核心观点

多数有趣的 AI 应用是流水线：生成图像再抠图编辑、写脚本再配音。Gradio 内置的 gr.Workflow 把"流水线"本身变成界面：把步骤描述为带类型的节点图，Gradio 渲染出拖拽画布——每个节点可单独运行、每个中间结果就地可见，取代 print-debugging。同一张图自动成为 REST API，并支持一键部署到 HF Spaces。

工作流由三类节点组成：references（输入）、operators（执行步骤）、subjects（输出）。operator 可以是自己的 Python 函数、Inference Providers 上的模型、另一个 Gradio Space、或 Hub 数据集的一行；类型化端口之间拖拽连线即可。fn 节点就是 Python，用 @spaces.GPU 装饰后由 ZeroGPU 按调用抓取 GPU 跑自有模型。

文章给出五个可复制的 live demo：图片编辑、AI 媒体工作室、并行图像生成、数据集画像、ZeroGPU 动画。

## 关键发现 / 关键技术

### 1. 三类节点 × 四种 operator
- references / operators / subjects 的节点图模型；连线发生在类型化端口之间
- operator 四种来源：本地 Python fn、HF Inference Providers 模型、现有 Gradio Space、Hub 数据集行
- 最小起步：`gr.Workflow(bind=[your_function]).launch()`

### 2. 每个输出即一个 REST endpoint
- 媒体工作室示例中三个输出各有独立端点：/sticker、/voiceover、/episode_title，可不开 UI 直接从代码调用
- gradio_client 调用示例：`Client("ysharma/gr-workflow-multi-endpoint-API")` 的 /word_count、/fahrenheit；调用模型或 Space 的端点需传 HF token；也可用 curl 直接请求
- 同一画布 = 拖拽界面 + REST API + 一键部署到 Spaces，三合一

### 3. 五个官方 demo 与 GPU 节点
- 图片编辑：单节点调 Qwen-Image-Edit（Inference Providers）
- AI 媒体工作室：FLUX.1-schnell 生成 → 背景 removal Space 出贴纸；主题 → MeloTTS 配音；主题 → Qwen2.5-7B-Instruct 写标题——一张画布两次模型调用 + 两次 Space 调用
- 生成艺术实验室：fan-out 模式，一个提示并行喂多个 operator（水彩版、赛博朋克版 + LLM 写标题）
- 数据侦探：输入数据集 ID，四路并行经 Datasets Server API 出概览卡、行预览、列统计、分布图
- ZeroGPU 动画：fn 节点内经 Diffusers 跑 LTX-Video，@spaces.GPU 按调用分配 GPU；预告下篇用它复刻 AUTOMATIC1111 级别的应用

## 实践意义

对原型与内部工具开发者：原型（画布）、API（每输出一端点）、部署（一键 Spaces）三步合一，且中间结果可见让多步管线可调试。对 agent 开发者：工作流天然是可编排、可编程消费的服务单元，agent 可直接以 REST 调用其中任意一步。官方指南（gradio.app/guides/workflows）覆盖 operator 种类、JSON schema 与可复用模式。

## 跨厂商对比

- 与 [Baseten Inference Providers](baseten-inference-providers.md) 互补：Baseten/HF 讲模型 serving 与推理基础设施层，gr.Workflow 讲把多个模型/服务编排成应用的界面与 API 层，两者是栈的相邻两层
- 与 [AgentKit](../../openai/research/introducing-agentkit.md) 对比：OpenAI 的 AgentKit 是面向其生态的可视化 agent 构建套件，gr.Workflow 是开源、模型无关的节点图编排 + 自动 API 化，定位相近但开放度与生态绑定不同

## 资源

- 论文：N/A
- 代码：https://gradio.app/guides/workflows（官方 gr.Workflow 指南）
- Demo：https://huggingface.co/spaces/ysharma/gr-workflow-04-ai-media-studio（文内五个可复制 Space 之一）
