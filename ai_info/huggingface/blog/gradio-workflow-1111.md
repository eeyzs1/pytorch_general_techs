# 用 Gradio Workflow 重建 AUTOMATIC1111（Rebuilding AUTOMATIC1111 with Gradio Workflow）

- **原文链接**: [Rebuilding AUTOMATIC1111 with Gradio Workflow](https://huggingface.co/blog/gradio-workflow-1111)
- **作者**: Gradio 团队（Hugging Face）
- **发布日期**: 2026-09-10
- **检索日期**: 2026-09-29
- **标签**: #Gradio #工作流 #图像生成 #可视化编程 #RESTAPI

## 核心观点

Gradio 团队用 gr.Workflow 把 AUTOMATIC1111（A1111）的大部分功能重建为单画布应用 Workflow1111：11 条媒体管线、73 个节点，覆盖文生图、hi-res fix、图生图、LLM 写提示、VLM 反推、DETR 自动掩码、prompt matrix、放大、背景移除、ControlNet 标注器、PNG Info、Wan2.2 图生视频等 A1111 标志性能力。

设计上以四种算子（fn/model/space/dataset）提供统一抽象——本地函数、Hub 模型、Spaces、数据集都是同一种节点，无需 ComfyUI 式自定义节点生态；同深度节点自动并行；36 个算子中 22 个纯本地运行；每个输出节点自动暴露为 REST 端点（共 9 个）。定位与 ComfyUI 互补：更低门槛、Python 原生、API 优先。

## 关键发现 / 关键技术

### 1. 覆盖面：73 节点重建 A1111

- 11 条媒体管线串联 73 个节点：文生图、图生图、hi-res fix、prompt matrix、放大、背景移除等 A1111 主力功能逐一对应。
- 11 条管线可独立运行也可互相拼接，对应 A1111 的 tab 式使用习惯。
- 现代扩展：LLM 写提示、VLM 反推、DETR 自动掩码、ControlNet 标注器、Wan2.2 图生视频。
- PNG Info 节点保留 A1111 的参数回读传统，工作流可从图片元数据反向恢复。
- 单画布承载全部管线，不再需要 A1111 式多页面切换。

### 2. 四算子统一抽象

- fn（本地 Python 函数）、model（Hub 模型推理）、space（托管 Spaces）、dataset（数据集读取）四种算子覆盖全部节点类型。
- 不需要 ComfyUI 式的自定义节点包生态：任何 Python 函数直接成为画布节点。
- 画布即代码：工作流保存为可版本化的 Python 结构，进 CI 与代码审查。

### 3. 执行模型：并行与本地化

- 同深度节点自动并行执行，无需手工编排并发。
- 36 个算子中 22 个纯本地运行，兼顾隐私与离线场景；远程算子按需调用 Hub 资源。
- 本地/远程混合意味着敏感图片可全程不出机，只有重载生成环节上云。

### 4. API 优先：输出节点即端点

- 每个输出节点自动成为 REST 端点，Workflow1111 共暴露 9 个。
- 画布应用同时是可编程服务：前端演示与后端 API 由同一工作流生成，原型到服务距离归零。
- 与 ComfyUI 的关系是互补而非替代：A1111 老用户获得熟悉的功能集，新用户获得更低门槛。

## 实践意义

对图像工作流用户，Workflow1111 是 A1111 与 ComfyUI 之外的第三选项：A1111 的易用 + 节点图的灵活 + Python 原生 + 自动 REST API。对应用开发者，"输出节点即端点"的模式让内部工具天然可编程。四算子抽象也示范了如何用统一接口收编本地函数、模型、Spaces 与数据集四类异构资源。

## 跨厂商对比

- 与 [Gradio Workflow 指南](gradio-workflow-guide.md) 互补：概念指南说明 gr.Workflow 是什么，本文用 73 节点的完整实战应用证明其表达力上限。
- 与 [LFM2.5-VL-DSPark](lfm2-5-vl-dspark.md) 互补：画布中的 VLM 反推、DETR 掩码等本地算子正受益于 MLX/llama.cpp 一类的本地推理加速。

## 资源

- 论文：N/A
- 代码：[gradio-app/gradio（gr.Workflow）](https://github.com/gradio-app/gradio)
- Demo：[发布文内 Workflow1111 Space 入口](https://huggingface.co/blog/gradio-workflow-1111)
