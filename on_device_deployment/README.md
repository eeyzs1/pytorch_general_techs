# 大模型端侧部署（On-Device Deployment）课程

面向 **模型压缩 → 推理/硬件 → 系统运营 → Agent/语音/车载/MCU** 的端侧部署全栈教材：理论文档 + 可运行 Jupyter 笔记本（多数可在 CPU 上仿真跑通）。

## 先读哪两份总览？

仓库入口就两份「全景文档」（已与旧版合并定稿），职责不同：

| 文档 | 干什么用 | 适合谁 |
|------|----------|--------|
| **[odd_learning_panorama.md](odd_learning_panorama.md)** | **学习级技术全景 / 学习地图**：按 Ch.1–24 列出全部技术，说明学什么、为何学、去哪练；含选型速查与组合拳 | 有一定 ML/工程基础、准备系统学习者 |
| **[odd_popular_science.md](odd_popular_science.md)** | **零基础趣味科普**：用生活比喻讲清仓库里全部技术（合并原趣味指南）；无公式 | 完全没有技术背景的读者、对内科普 |

> 两者都覆盖本仓库**全部技术分类**，但深度不同：科普讲「是什么感觉」，学习全景讲「怎么学」，细节与代码仍看下面的主讲义与 notebook。

## 快速开始

```bash
cd on_device_deployment
pip install -r requirements.txt
jupyter notebook
```

建议阅读顺序：

1. 按背景选读上面两份总览之一  
2. [on_device_deployment_techniques.md](on_device_deployment_techniques.md) — **技术详解主讲义**（算法、决策树全文、课程文件索引）  
3. 按章节打开对应 `.ipynb` 动手  
4. [hardware_roadmap.md](hardware_roadmap.md) — 按硬件选学习路径  
5. [comprehensive_projects.md](comprehensive_projects.md) — 综合项目  
6. [exercises_solutions.md](exercises_solutions.md) — 练习参考答案  

（旧链接 [fun_guide_for_everyone.md](fun_guide_for_everyone.md) 已重定向到趣味科普定稿。）

## 课程结构

| 章 | 主题 | 目录 |
|----|------|------|
| 1 | 模型压缩（量化/剪枝/蒸馏/低秩/超低比特/torchao） | `01_model_compression/` |
| 2 | 高效推理（KV / Attention / 投机解码 / Prefill-Decode / 长上下文） | `02_efficient_inference/` |
| 3 | 高效架构（SLM / SSM / MoE / NAS） | `03_efficient_architecture/` |
| 4 | 编译与运行时 | `04_compilation_runtime/` |
| 5 | 硬件与部署框架 | `05_hardware_deployment/` |
| 6 | 模型格式与版本 | `06_model_format/` |
| 7 | 端云协同 / 多模态 / 推理服务 / 功耗 / WASM / 语音全链路 | `07_edge_cloud/` |
| 8 | 端侧训练与个性化 / 多适配器 | `08_on_device_training/` |
| 9 | 端到端实战与排障 | `09_end_to_end/` |
| 10 | 国产 NPU 与国产模型 | `10_china_hardware/` |
| 12 | 评估指标脚手架 | `12_evaluation/` |
| 13 | 模型选型决策器 | `13_model_selection/` |
| 14 | 端侧 Agent | `14_edge_agent/` |
| 15 | MCU / TinyML | `15_mcu_tinyml/` |
| 16 | 端侧扩散 / 文生图 | `16_on_device_diffusion/` |
| 17 | 模型交付安全 | `17_model_security/` |
| 18 | OS 系统 AI 运行时 / 共享基座 | `18_system_runtime/` |
| 19 | 模型分发与 OTA | `19_model_ota/` |
| 20 | 端侧检索与向量库 | `20_on_device_retrieval/` |
| 21 | 流式音视频交互管线 | `21_streaming_av/` |
| 22 | 自定义算子与 Kernel | `22_custom_ops/` |
| 23 | 车载与功能安全 | `23_automotive_safety/` |
| 24 | 端侧 MLOps 与质量门禁 | `24_edge_mlops/` |

另：第2.4/2.5、第3.4、第8.4 见主讲义专节。完整映射表见主讲义末尾 **课程文件索引**。

## 依赖说明

- 核心：`torch`、`transformers`、`onnx`、`peft` 等（见 `requirements.txt`）
- 可选：`torchao`、`autoawq`、`llama-cpp-python`、`mlx`、Qualcomm AI Hub（按需取消注释）

没有 NPU/手机真机时，笔记本会走 **仿真路径**，重点学原理与流水线，不要求专用 SDK。
