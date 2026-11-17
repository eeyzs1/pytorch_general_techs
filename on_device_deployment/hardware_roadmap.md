# 硬件实操路线图

> 更新与官方资料检索：2026-11-17。目标是用已有设备建立正确性与测量闭环，再进入专用硬件部署。
> 近期版本、官方来源及验证范围见 [端侧运行时与交付更新](runtime_update_2026-11.md)。

## 先选路径，再选模型

| 已有环境 | 起步路径 | 应先验证 |
|---|---|---|
| 普通 PC / 无独显 | C：CPU | 导出、数值、输入契约与内存预算 |
| Apple Silicon Mac | M：Apple | CPU / GPU / Apple 专用框架的适用版本与算子支持 |
| NVIDIA GPU PC | G：CUDA | 驱动、模型格式、后端与显存预算；服务框架的操作系统支持 |
| Android 手机 | A：Android | 目标 SoC、系统版本、后端、算子分区及持续功耗 |
| 浏览器 | B：WebGPU / WASM | 浏览器支持、模型下载、Tab 内存与计算后端 |
| MCU / 传感器板 | E：TinyML | SRAM、静态内存规划、唤醒或传感任务 |
| 已有嵌入式开发板 | D：开发板 | SDK / 板卡版本、交叉编译、供电散热与实际运行记录 |

优先使用手边设备。芯片 TOPS、工艺节点与参数量不能直接换算成 tok/s，也不能证明支持某个模型的全部算子。

## 路径 C：纯 CPU 先跑通交付

1. 完成 [5.5 导出与运行时一致性](05_hardware_deployment/5.5_export_runtime_parity.ipynb)。
2. 完成 [6.0 模型格式](06_model_format/6.0_model_format.ipynb) 与 [6.1 版本管理](06_model_format/6.1_model_versioning.ipynb)。
3. 选择实际模型后，估算权重、KV、运行时工作区与进程峰值；不要只算量化权重大小。
4. 再使用 llama.cpp 或 ONNX Runtime 的 CPU 路径测量实际输入分布。

从课程目录运行新增实验：

```bash
jupyter notebook 05_hardware_deployment/5.5_export_runtime_parity.ipynb
```

完成标准：多个有效形状与 Eager 参考对齐，非法输入被拒绝，能说明模型文件、图格式与运行时的区别。CPU 实验验证机制；不以它推算 NPU 加速比。

## 路径 M：Apple Silicon

| 目标 | 可评估路线 | 兼容性重点 |
|---|---|---|
| 本地研究与模型试验 | MLX / MLX-LM、llama.cpp Metal | 芯片、内存、模型架构与量化实现 |
| App 中部署自有模型 | Core AI、Core ML、ExecuTorch 相应后端 | OS / SDK 可用性、转换工具、精度与算子支持 |
| 使用系统提供的模型 | Apple 系统模型接口 | 设备与地区可用性、任务边界，不等同于加载任意自有模型 |

Core AI 是 WWDC26 官方介绍的端侧模型部署框架，包含 Python 工具与 Swift API；Core ML 的既有模型与兼容路线仍需按项目维护。不要把“支持 Apple Silicon”自动理解为模型在 ANE 上完整运行。[Apple Core AI](https://developer.apple.com/videos/play/wwdc2026/324/)、[Core ML](https://developer.apple.com/documentation/coreml)

先做 CPU / GPU 正确性对照，再用目标平台工具观察后端分区、加载时间、内存与持续功耗。对于统一内存设备，还要给系统与其他应用预留空间，不使用“某内存容量必定能跑某参数量”的固定表格。

## 路径 G：Windows / Linux 与 NVIDIA GPU

本地单用户可评估 llama.cpp CUDA；研究试验可使用 PyTorch；服务压测可按框架官方支持环境使用 vLLM 或 TensorRT-LLM。Windows、WSL2、Linux 的安装与后端支持分别核对。

先运行 PyTorch 的 SDPA / compile / export [基础实验](../ml_train/09_inference_optimization/13_modern_pytorch_inference.ipynb)，再按 [推理服务与调度](../llm_techs/03-推理服务与调度.md) 建立服务基线。

```text
权重与模型配置 → 确认格式 / 量化配方 → 兼容运行时 → 质量回归 → 服务负载测试
```

AWQ 模型需要相应量化权重与配置；不能对普通 BF16 checkpoint 只加一个 `--quantization awq` 就当作完成量化。选择量化工具时检查当前维护情况和框架版本，不混装不兼容的包。

测量时固定输入 / 输出长度、并发、dtype 与预热。报告 TTFT、TPOT / ITL 和峰值显存，不能用无来源的速度区间作为验收标准。

## 路径 A：Android 手机

两类路线需要区分：

- **应用模型部署**：LiteRT / LiteRT-LM、ExecuTorch、QNN 或其他目标运行时，携带自有模型与应用配置。
- **系统 AI 能力**：使用系统提供的模型和服务，受设备、系统与接口权限约束，不等于任意模型直接访问 NPU。

当前 [LiteRT-LM](https://developers.google.com/edge/litert-lm) 覆盖多平台和多种语言入口；具体设备能否走 GPU / NPU，仍需按所用版本、模型和后端检查。ExecuTorch 的 Qualcomm 等 delegate 也要对齐 SDK 与目标设备。

建议步骤：

1. 记录设备 SoC、Android 版本、内存与目标应用 SDK。
2. 从对应框架的官方示例开始，确认模型转换和加载。
3. 检查实际委托的算子、CPU fallback 与输入限制。
4. 比较短输入、长输入和持续运行后的生成质量、内存与温升。
5. 再接入 [模型 OTA](19_model_ota/19.1_model_ota.ipynb) 与 [端侧 MLOps](24_edge_mlops/24.1_edge_mlops.ipynb)。

Qualcomm AI Hub 的编译 / profile 作业与“把应用安装到自己的手机”是不同步骤；云端设备结果需连同设备与 SDK 信息保留，不能写成已经在用户真机运行。

## 路径 B：浏览器端（WebGPU / WASM）

从 [7.6 浏览器实验](07_edge_cloud/7.6_browser_wasm.ipynb) 和 `07_edge_cloud/browser_demo/index.html` 开始。

确认浏览器 API、实际计算后端、模型下载体积、缓存与 Tab 内存预算。WebGPU 的存在不代表任意模型都支持，也不等于原生 NPU delegate。

完成标准：能说明不支持 WebGPU 时的行为，区分冷下载、冷加载与预热后前向，在刷新页面和资源不足时有明确处理。

## 路径 E：MCU / TinyML

目标是始终在线的唤醒、分类与传感，不以完整大语言模型为起点。

先运行 [15.1 MCU / TinyML](15_mcu_tinyml/15.1_mcu_tinyml.ipynb)，再根据板卡选择对应的 MCU 后端与官方示例。记录权重、激活 arena、栈与外设缓冲的总 SRAM 占用；把需要大模型的任务交给上级设备或端云路径。

## 路径 D：嵌入式开发板

板卡按已有环境与目标任务选择；Jetson、Arm MCU、Android / Linux NPU 板卡使用不同工具链，不能只按 TOPS 横向排序。

逐项确认：

1. 硬件型号、内存、供电、散热、系统镜像和 SDK。
2. 编译器、目标架构与运行时后端是否匹配。
3. 实际模型是否有可用转换路径与参考实现。
4. 是否能取得质量、内存、延迟与持续功耗的可重复记录。

同一模型在不同板卡上比较时，保留量化方法、上下文、batch、生成长度及温度条件。源码按选定 release / commit 固定，不能把某张 JetPack 或 SDK 配置表直接用于另一代硬件。

## 通用验收清单

| 关卡 | 必须能提供的证据 |
|---|---|
| 可加载 | 运行时、版本与目标设备初始化记录 |
| 可运行 | 所需算子与动态输入范围的成功 / 失败样例 |
| 数值一致 | 与参考实现的多输入比较及容差 |
| 质量合格 | 真实任务回归；量化、长上下文、结构化输出分别检查 |
| 指标达标 | 预热、并发、内存、功耗与热稳态的测量配置 |
| 可交付 | 权重、图、tokenizer、配置、输入契约、指纹与回退版本 |

“导出成功”“CPU 运行一致”“NPU 全图委托”“业务质量合格”应分别验收。

## 近期官方入口

- [ExecuTorch 1.6.0 发布记录](https://github.com/pytorch/executorch/releases/tag/v1.6.0)
- [llama.cpp / ggml 1.0.0 版本边界](https://huggingface.co/blog/ggml-org/llama-cpp-v1)
- [Google LiteRT-LM](https://developers.google.com/edge/litert-lm)
- [Apple Core AI](https://developer.apple.com/videos/play/wwdc2026/324/)
- [ONNX Runtime 执行提供程序](https://onnxruntime.ai/docs/execution-providers/)
