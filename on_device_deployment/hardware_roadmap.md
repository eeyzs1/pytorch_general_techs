# 硬件实操路线图

> 本文档提供从零到真实硬件部署的渐进式实操路径。所有路径都从纯软件模拟起步，逐步过渡到真实设备，适合自学和教学场景。

---

## 先读这个：你的硬件选择决策树

```
你的设备情况？
│
├── 你有一台 MacBook (Apple Silicon, M1/M2/M3/M4)
│   └── → 路径 M：最省钱的起步方案（零额外开销）
│       核心优势：ANE 推理（Core ML）、GPU 推理（MLC-LLM）、CPU 推理（llama.cpp）全支持
│
├── 你有一台 Windows/Linux 笔记本 + NVIDIA GPU (RTX 2060 或更好)
│   └── → 路径 G：GPU 推理的最佳实践
│       核心优势：TensorRT-LLM、vLLM、AWQ/GPTQ 全工具链
│
├── 你有一台 Android 手机（骁龙 8 系列，近 2 年内的旗舰）
│   └── → 路径 A：最贴近真实端侧部署场景
│       核心优势：直接在目标设备上开发测试，NPU 实战
│
├── 你只有一台普通笔记本（无 GPU / 集成显卡）
│   └── → 路径 C：零门槛起步
│       核心优势：llama.cpp CPU 推理即可跑通大部分课程内容
│       实际部署体验依赖路径 A 或 M
│
└── 你有预算（¥2000-5000）可以购买开发板
    └── → 路径 D：开发板方案（见后文推荐）
        核心优势：完整的嵌入式部署体验，IoT/车载/机器人场景
```

---

## 路径 M：MacBook (Apple Silicon) 方案

### 可用技术栈
| 推理后端 | 框架 | 量化支持 | 适用模型大小 |
|---------|------|---------|------------|
| CPU (Apple Silicon) | llama.cpp | Q2-Q8 K-Quant | 最高 7B (16GB RAM) |
| GPU (Metal) | MLC-LLM / llama.cpp Metal | q4f16_1 | 最高 7B |
| ANE (Neural Engine) | Core ML | FP16/INT8 | 最高 3-4B |

### 阶段一：CPU 推理入门（0 成本，跟随课程即可）
```bash
# 安装 llama.cpp Python 绑定
pip install llama-cpp-python

# 下载一个小模型（Qwen2.5-0.5B GGUF）
# 从 HuggingFace 搜索 "Qwen2.5-0.5B-Instruct-GGUF"

# 在 Python 中加载并推理
python -c "
from llama_cpp import Llama
llm = Llama(model_path='qwen2.5-0.5b-q4_k_m.gguf', n_ctx=2048)
output = llm('你好，请介绍一下自己', max_tokens=100)
print(output['choices'][0]['text'])
"
```

学习目标：
- [ ] 理解 GGUF 格式和 K-Quant 量化
- [ ] 会用 llama-cpp-python 加载和推理
- [ ] 会测试不同量化格式（Q4_K_M vs Q5_K_M vs Q8_0）的精度和速度差异

### 阶段二：GPU (Metal) 推理加速
```bash
# 安装 MLC-LLM
pip install mlc-llm

# 使用 MLC 的预编译模型
mlc_llm chat HF://mlc-ai/Qwen2.5-1.5B-Instruct-q4f16_1-MLC \
    --device metal
```

学习目标：
- [ ] 理解 AOT 编译 vs JIT 解释执行的区别
- [ ] 对比 Metal GPU 和 CPU 的推理速度差异（应该有 3-5x）
- [ ] 用课程 5.3 的 Roofline 工具分析 M4 芯片的内存层次

### 阶段三：ANE (Neural Engine) 部署
```bash
# 安装 coremltools
pip install coremltools

# Python 中转换 PyTorch 模型到 Core ML
python -c "
import coremltools as ct
import torch

# 加载模型（需要先转换为 TorchScript 或 traced 模型）
# 参考：https://apple.github.io/coremltools/docs-guides/
"
```

学习目标：
- [ ] 了解 Core ML 的模型转换流程
- [ ] 理解 ANE 对 FP16 比 INT8 效率更高（与 GPU/NPU 不同！）
- [ ] 对比 ANE vs GPU vs CPU 的推理功耗（使用 macOS 的 powermetrics 工具）
- [ ] 用 Instruments (Xcode) 做 ANE 利用率分析

### 硬件观察工具
```bash
# CPU/GPU 功耗和频率监控
sudo powermetrics --samplers cpu_power,gpu_power -i 1000 -n 60

# 内存监控
vm_stat 1

# 模型加载时的内存变化
sudo memory_pressure
```

---

## 路径 G：Windows/Linux + NVIDIA GPU 方案

### 可用技术栈
| 推理后端 | 框架 | 量化支持 | 适用场景 |
|---------|------|---------|---------|
| CUDA GPU | vLLM / TensorRT-LLM | AWQ/GPTQ/FP8 | 高性能推理，服务化部署 |
| CUDA GPU | llama.cpp CUDA | Q2-Q8 K-Quant | 快速原型，单用户推理 |
| CUDA GPU | PyTorch + bitsandbytes | NF4/INT8 | 研究实验，量化探索 |

### 阶段一：GPU 推理基础（有 GPU 的最快起步）
```bash
# 安装 vLLM
pip install vllm

# 启动一个 1.5B 模型的推理服务
python -m vllm.entrypoints.openai.api_server \
    --model Qwen/Qwen2.5-1.5B-Instruct \
    --quantization awq \
    --max-model-len 4096
```

学习目标：
- [ ] 理解 vLLM 的 PagedAttention 和连续批处理
- [ ] 对比 batch_size=1 和 batch_size=8 的吞吐差异
- [ ] 用 nvidia-smi 监控 GPU 利用率和显存

### 阶段二：AWQ/GPTQ 量化实战
```bash
# 安装 autoawq
pip install autoawq

# 量化一个模型（1.5B 约需 3-5 分钟，8GB 显存）
python -c "
from awq import AutoAWQForCausalLM
from transformers import AutoTokenizer

model_path = 'Qwen/Qwen2.5-1.5B-Instruct'
quant_path = 'qwen2.5-1.5b-awq'

model = AutoAWQForCausalLM.from_pretrained(model_path)
tokenizer = AutoTokenizer.from_pretrained(model_path)

model.quantize(tokenizer, quant_config={
    'zero_point': True,
    'q_group_size': 128,
    'w_bit': 4,
    'version': 'GEMM'
})
model.save_quantized(quant_path)
"
```

学习目标：
- [ ] 独立完成一次 AWQ 量化
- [ ] 对比量化前后模型的 PPL 和推理速度
- [ ] 理解 group_size 和 zero_point 对精度-速度的影响

### 阶段三：TensorRT-LLM 部署（加分项）
```bash
# TensorRT-LLM 是 NVIDIA 官方推理引擎
# 流程：HF Model → TensorRT-LLM checkpoint → build engine → run
# 注意：安装和配置相对复杂，建议在有经验后尝试
```

### GPU 监控工具
```bash
# GPU 利用率、显存、温度
nvidia-smi -l 1

# PyTorch 模型的内存分析
python -c "
import torch
print(f'Allocated: {torch.cuda.memory_allocated()/1024**3:.2f} GB')
print(f'Cached:    {torch.cuda.memory_reserved()/1024**3:.2f} GB')
"
```

---

## 路径 A：Android 手机方案

### 前置条件
- 一台 2023 年后发布的旗舰 Android 手机（推荐骁龙 8 Gen2/Gen3/Elite）
- 开发者模式已开启 + USB 调试
- ADB 已安装

### 阶段一：在 Android 上运行 llama.cpp
```bash
# 方法1：通过 Termux（Android 终端模拟器）
# 在手机上安装 Termux，然后：
pkg install cmake
git clone https://github.com/ggerganov/llama.cpp
cd llama.cpp
cmake -B build
cmake --build build --config Release -j4

# 将 GGUF 模型推送到手机
adb push model-q4_k_m.gguf /sdcard/models/

# 运行推理
./build/bin/llama-cli \
    -m /sdcard/models/model-q4_k_m.gguf \
    -p "你好" \
    -n 50
```

学习目标：
- [ ] 在手机上成功运行 llama.cpp 推理
- [ ] 测量手机 CPU 推理的 tok/s
- [ ] 对比手机和 PC/Mac 的 CPU 推理性能差距

### 阶段二：高通 QNN SDK 入门（如果手机是高通芯片）
```bash
# 下载 Qualcomm AI Engine Direct SDK
# https://developer.qualcomm.com/software/qualcomm-ai-engine-direct-sdk

# 流程：
# 1. PyTorch 模型 → ONNX
# 2. ONNX → QNN 量化工具 → QNN 模型
# 3. QNN 模型 → QNN 编译器 → Context Binary
# 4. 在手机上用 QNN Runtime 加载运行
```

> **注意**：QNN SDK 的安装和配置有一定门槛（需要注册高通开发者账号，SDK 体积大），但这正是真实的 NPU 部署体验。

### 阶段三：MNN / NCNN 轻量级推理
```bash
# MNN 是阿里的移动端推理框架，对 CPU/NPU 都支持
# 比直接使用 QNN 更容易上手

# 安装 MNN Python 工具
pip install MNN

# 转换模型
python -c "
import MNN
# PyTorch → MNN 格式转换
# 参考：https://github.com/alibaba/MNN
"
```

### Android 调试工具
```bash
# ADB 基础命令
adb devices                         # 查看连接的设备
adb shell                           # 进入手机 shell
adb push local_file /sdcard/       # 推送文件
adb pull /sdcard/remote_file .     # 拉取文件

# 手机性能监控
adb shell top -n 1                  # 进程 CPU/内存
adb shell dumpsys battery           # 电池状态
adb shell dumpsys cpuinfo           # CPU 信息

# 实时监控内存
adb shell dumpsys meminfo | grep -E "Native|Graphics|TOTAL"
```

---

## 路径 C：纯 CPU 方案（零额外成本）

对于没有 GPU、没有高端手机的学习者，这条路径让你依然可以学到 80% 的内容。

### 核心工具链
```bash
# 1. llama.cpp（CPU 推理的事实标准）
pip install llama-cpp-python

# 2. ONNX Runtime CPU
pip install onnxruntime

# 3. PyTorch CPU（课程所有 notebook 都在 CPU 可跑）
pip install torch --index-url https://download.pytorch.org/whl/cpu
```

### 学习路线
1. **跟随课程 notebook**：所有代码都在 CPU 上可运行，完整覆盖第 1-4 章和 6-9 章
2. **量化实验**：课程 1.1 和 9.1 的量化代码在 CPU 上完整可跑
3. **llama.cpp 体验**：下载 GGUF 量化模型，在 CPU 上体验不同量化格式
4. **性能分析**：用课程 5.3 的 Roofline 工具分析 CPU 上的瓶颈

### 局限和弥补方案
| 课程内容 | CPU 上能做吗 | 如何弥补 |
|---------|:----------:|---------|
| NPU 适配（5.1） | ❌ | 阅读 QNN/ANE 文档 + 看公开 benchmark |
| GPU 推理加速 | ❌ | 使用课程模拟代码理解原理 |
| Roofline 实战 | ⚠️ 可模拟 | 用课程代码做模拟分析 |
| 量化推理加速 | ⚠️ 无加速 | CPU 上量化后用 FP32 反量化计算，不加速但可以验证精度 |
| 硬件基准测试 | ⚠️ 可模拟 | 用课程 5.4 的框架做模拟分析 |
| 端侧训练 | ⚠️ 慢 | 用极小模型（<100M 参数）体验流程 |

---

## 路径 D：开发板方案（¥2000-5000 预算）

### 推荐开发板

| 开发板 | 核心芯片 | NPU 算力 | 价格（约） | 适用场景 |
|--------|---------|---------|:-----:|---------|
| **Jetson Orin Nano (8GB)** | NVIDIA Orin | 40 TOPS | ¥3500 | GPU 推理 + CUDA 生态，最适合学习 LLM 端侧部署 |
| **树莓派 5** | BCM2712 | 无 NPU | ¥500 | 极低成本体验 CPU 推理，0.5B 模型可跑 |
| **瑞芯微 RK3588 开发板** | RK3588 | 6 TOPS | ¥800-1500 | NPU 部署实战（IoT 场景） |
| **高通 RB5 开发套件** | QRB5165 | 15 TOPS | ¥4000+ | 高通 QNN 实战，最贴近手机场景 |
| **地平线 RDK X5** | Sunrise 5 | 10 TOPS | ¥2000 | 国产 NPU 实战 |

### 推荐：Jetson Orin Nano 起步

这是最佳的学习型开发板，理由：
- NVIDIA 生态（CUDA/TensorRT/Triton），与云端 GPU 同源
- 40 TOPS 算力可跑 3B-7B 量化模型
- 社区成熟，教程丰富
- 支持 vLLM、llama.cpp、TensorRT-LLM

```bash
# Jetson Orin Nano 设置 (Ubuntu + JetPack 6.0+)
# 1. 刷写 JetPack 系统（NVIDIA SDK Manager）
# 2. 安装依赖
sudo apt update
sudo apt install python3-pip cmake

# 3. 编译 llama.cpp（启用 CUDA）
git clone https://github.com/ggerganov/llama.cpp
cd llama.cpp
cmake -B build -DGGML_CUDA=ON
cmake --build build --config Release -j4

# 4. 运行 7B 模型
./build/bin/llama-cli -m qwen2.5-3b-q4_k_m.gguf -p "Hello" -n 50 -ngl 99
```

### Jetson 监控工具
```bash
# 类似 nvidia-smi 的工具
sudo tegrastats                    # GPU/CPU/内存/温度全维度监控
sudo jtop                          # 更好的可视化工具（需安装 pip install jetson-stats）
```

---

## 推荐的渐进式实操顺序

不管你从哪条路径开始，推荐按以下顺序逐步接触真实硬件：

```
第 1 个月：纯 CPU 模拟（跟随课程）
  └── 完成所有 notebook，初步建立知识体系
  └── 输出：能在 CPU 上独立量化模型、验证精度、做 Roofline 分析

第 2 个月：第一个真实推理框架
  └── 在 Mac 的 Metal / Windows 的 GPU / Android 的 llama.cpp 中选择一个
  └── 实现：量化 → GGUF/ONNX → 框架推理 → 基准测试
  └── 输出：一份真实的部署方案文档

第 3 个月：接触 NPU 或进阶 Topic
  └── 选项1：如果有 Jetson Orin — 跑 TensorRT-LLM 或 vLLM
  └── 选项2：如果预算有限 — 用瑞芯微 RK3588 体验 NPU 部署
  └── 选项3：如果是 Mac 用户 — 用 Core ML + ANE 做真实 NPU 部署
  └── 输出：对比 CPU/GPU/NPU 三者的性能差异

第 4 个月：综合实战
  └── 选择项目二或项目五（综合实战项目），独立完成
  └── 输出：完整项目代码 + 部署报告
```

---

## 常见硬件问题的预期表现

以下数据来自课程第 5 章和社区 benchmark，帮助你建立合理的预期：

| 硬件 | 模型 | 预期 tok/s | 模型加载方式 |
|------|------|:----------:|------------|
| MacBook M1 (16GB) | Qwen2.5-1.5B Q4_K_M | 40-50 | llama.cpp Metal |
| MacBook M1 (16GB) | Qwen2.5-7B Q4_K_M | 12-18 | llama.cpp Metal |
| RTX 4060 Laptop (8GB) | Qwen2.5-7B AWQ | 50-70 | vLLM |
| 骁龙 8 Gen3 手机 | Qwen2.5-1.5B Q4_K_M | 20-30 | llama.cpp CPU |
| Jetson Orin Nano (8GB) | Qwen2.5-3B Q4_K_M | 25-35 | llama.cpp CUDA |
| 树莓派 5 | Qwen2.5-0.5B Q4_K_M | 3-5 | llama.cpp CPU |

---

## 常见踩坑和解决

### 坑 1：GGUF 模型下载慢
```bash
# 使用 HuggingFace 镜像站
export HF_ENDPOINT=https://hf-mirror.com
huggingface-cli download model-name --local-dir ./models
```

### 坑 2：Mac M1 上 llama-cpp-python 安装 Metal 后端失败
```bash
# 确保设置正确的编译参数
CMAKE_ARGS="-DGGML_METAL=on" pip install llama-cpp-python --force-reinstall --no-cache-dir
```

### 坑 3：QNN SDK 安装庞大（15GB+）
```bash
# 如果只是学习，用 QNN 的文档 + 课程代码理解就够了
# 真正需要 QNN SDK 的场景：你要发布使用了高通 NPU 的商业 App
```

### 坑 4：Jetson 上 CUDA 版本混乱
```bash
# JetPack 系统自带 CUDA，不要额外安装
# 用 nvcc --version 确认版本
# 编译代码时指定正确的 CUDA 架构
cmake -DCMAKE_CUDA_ARCHITECTURES=87 ..  # Orin 是 sm_87
```

---

> **核心建议**：不要等有了"完美硬件"才开始。第一天就能在 CPU 上跑课程代码。硬件是放大器，不是前提条件。