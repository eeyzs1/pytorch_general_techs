# 欢迎 FLUX.3 Image Klein 登陆 Diffusers（Welcome FLUX.3 Image Klein in Diffusers）

- **原文链接**: [Welcome FLUX.3 Image Klein in Diffusers: The latest open image generation model from Black Forest Labs](https://huggingface.co/blog/flux-3)
- **作者**: Aritra Roy Gosthipaty、Sayak Paul、Linoy Tsaban（Hugging Face Diffusers 团队）
- **发布日期**: 2026-10-15
- **检索日期**: 2026-10-16
- **标签**: #文生图 #图像编辑 #Diffusers #布局控制 #开源模型

## 核心观点

Black Forest Labs 的 FLUX.3 Image Klein 在 Diffusers day-0 可用：一个模型覆盖文生图、多参考图生图，并新增布局控制——在提示里写 JSON 边界框（0–1000 归一化、y 坐标在前），指定每个区域画什么、或把参考图里某块内容从 from 框搬到 to 框。两个开源 checkpoint：蒸馏版默认 16 步无 CFG（H100 上 1024×1024 约 2 秒），base 版 50 步带 CFG。

工程亮点是作为 Modular Diffusers 管线发布：节点图可拆可换，"编码一次多次生成"（参考图 latent 复用）、在去噪循环里插自定义步骤都是原生操作。NVFP4/FP8 权重经 from_single_file 加载，覆盖小显存；LoRA 训练脚本文生图与编辑双份齐备。

## 关键发现 / 关键技术

### 1. 布局控制的接口设计

- 区域格式：`[{"id", "bbox", "desc"}]`，坐标 [y_min, x_min, y_max, x_max]；编辑时每区域给 src_bbox（参考图来源）与 tgt_bbox（输出位置），同框即锁定不动。
- 归一化坐标系意味着同一布局在任意分辨率下复用；提示中用 `<ref_image_0>`、`<silhouette_1>` 之类的 ID 引用区域与参考图。

### 2. 架构与文本编码器

- 双阶段流匹配架构、每个 token 有自己的时间步、四维位置编码（详见原文 The architecture 一章）；文本编码器用 Qwen3-VL。

### 3. 模块化管线

- ModularPipeline.from_pretrained + load_components 的新 API；管线块可单独替换、可在循环中注入步骤——为研究与产品定制留出接口而非黑盒。

## 实践意义

"提示即布局"把可控生成从外挂 ControlNet 拉进模型原生能力，电商改图、海报排版、素材迁移的工作流可以砍掉一整层适配代码。蒸馏版 2 秒出图 + FP8 小显存路径，让本地/边缘部署文生图的实际门槛进一步下降。

## 跨厂商对比

- 与 [用 Gradio Workflow 重建 AUTOMATIC1111](gradio-workflow-1111.md) 对比：A1111 时代的图像工作流靠外挂节点拼接，FLUX.3 把布局控制与多参考编辑内化进单一模型——工具链从"管线编排"向"模型原生能力"迁移的缩影。
- 与 [Muse Image](../../meta/muse-image.md) 对比：Meta 图像生成走产品化集成路线，BFL 走开源权重 + 框架 day-0 支持路线；布局控制这类精细可控性目前是开源侧的差异化卖点。
- 与 [ML Intern 造模型](building-with-ml-intern.md) 互补：ML Intern 展示社区如何基于开放图像模型造 LoRA 长尾，FLUX.3 这类强底座的每次升级都会放大该生态的产出质量。

## 资源

- 论文：无
- 代码：[black-forest-labs/flux-3-image-klein（Hugging Face）](https://huggingface.co/black-forest-labs/flux-3-image-klein)
- Demo：[FLUX.3 Image Klein Space](https://huggingface.co/spaces/black-forest-labs/flux-3-image-klein)
