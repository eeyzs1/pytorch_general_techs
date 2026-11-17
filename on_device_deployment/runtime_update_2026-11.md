# 端侧运行时与交付更新 · 2026-11-17

> 官方资料检索：2026-11-17。先按目标设备与交付约束选路径，再做真机性能与质量验证。

## 1. 近期工具链的已核验变化

| 路线 | 当前核验结果 | 对课程实践的影响 |
|---|---|---|
| ExecuTorch | 1.6.0，2026-11-12 发布 | 增加不依赖 PyTorch 的 Python 运行时；NXP Neutron 标为 production-ready，TensorRT 后端仍为 beta；按版本确认后端和导出依赖 |
| llama.cpp / ggml | 库版本 1.0.0，2026-11-13 发布 | 明确公共 C API / ABI 的版本边界；应用升级要同时检查绑定、后端库与模型格式支持 |
| LiteRT-LM | 官方入口当前列出 v0.18.0 | 作为 LiteRT 上的 LLM 编排层，包含多模态 embedding、模型信息查询及 NPU / GPU 优化；语言与硬件能力逐条检查 |
| Apple Core AI | WWDC26 官方介绍的新端侧框架 | 包含 Python 工具和 Swift 推理接口；按部署系统版本核对可用性，不把单个演示的速度当作全部 Apple 设备的保证 |

来源：[ExecuTorch 1.6](https://github.com/pytorch/executorch/releases/tag/v1.6.0)、[llama.cpp 1.0 公告](https://huggingface.co/blog/ggml-org/llama-cpp-v1)、[LiteRT-LM 官方入口](https://developers.google.com/edge/litert-lm)、[Apple Meet Core AI](https://developer.apple.com/videos/play/wwdc2026/324/)。LiteRT-LM 一行是文档检索快照，不推定其发布日期。

ExecuTorch 的 `stable` 文档入口在本次检索中仍显示 1.5，而 release 页已列 1.6。复现时选择对应 release 的代码、工具与文档，不能把浮动文档与任意安装版本混用。

## 2. 不同工具处在不同层

| 层次 | 例子 | 不能据此推断 |
|---|---|---|
| 张量 / 权重文件 | safetensors、量化权重 | 模型图、tokenizer 和生成策略已完整交付 |
| 图或部署程序 | ONNX、ExecuTorch `.pte` | 目标端所有算子均已支持或已走加速器 |
| 执行后端 | ONNX Runtime provider、ExecuTorch delegate | 初始化成功就代表全图委托成功 |
| 生成与应用层 | KV 管理、采样、流式输出、工具调用 | 单次矩阵前向耗时就是端到端生成延迟 |

现代 PyTorch ONNX 路线显式采用 `torch.onnx.export(..., dynamo=True)` 和 `dynamic_shapes`；这是基于 torch.export 的路径，适用于 PyTorch 2.6+。[PyTorch ONNX 文档](https://docs.pytorch.org/docs/2.15/onnx.html)

ONNX Runtime 用执行提供程序选择设备实现，支持与分区规则由具体 provider 决定。真机验收需查看算子分区、fallback 与执行记录，不能只看已安装 provider 名称。[Execution Providers](https://onnxruntime.ai/docs/execution-providers/)

## 3. 一个可运行的导出验收闭环

新增 [5.5_export_runtime_parity.ipynb](05_hardware_deployment/5.5_export_runtime_parity.ipynb)：

1. 固定随机种子、FP32 模型和输入范围。
2. 导出动态 batch / tokens 的 ONNX，运行图检查。
3. 显式用 ONNX Runtime CPU 执行，打印实际 provider。
4. 在最小、典型和最大形状下比较完整输出。
5. 在运行时入口拒绝越界、错误 dtype 与非有限数值。
6. 记录文件指纹、opset、版本、输入契约和回归误差。

符号维度名不能替代应用的完整输入契约。框架导出时记录的范围约束，也不能未经验证就假定由所有目标后端强制执行。

从 `on_device_deployment` 目录运行：

```bash
python -m pip install -r requirements.txt
jupyter notebook 05_hardware_deployment/5.5_export_runtime_parity.ipynb
```

自动执行可使用以下命令，输出保存到系统临时目录，源文件保持未执行状态：

```bash
python -m nbconvert --to notebook --execute 05_hardware_deployment/5.5_export_runtime_parity.ipynb --output edge-parity-executed --output-dir /tmp
```

Windows 可把 `/tmp` 替换为 PowerShell 的 `$env:TEMP`。若要交付模型，需另行保存完整产物目录。

## 4. 性能记录应包含什么？

| 条目 | 记录要求 |
|---|---|
| 环境 | 设备型号、系统 / 驱动、运行时与后端、构建选项 |
| 模型 | 权重与 tokenizer revision、量化配方、上下文与 KV 格式 |
| 时延 | 加载、首次执行、Prefill、Decode 分开记录；注明并发与预热 |
| 内存 | 权重、KV、临时工作区及进程峰值分别观察 |
| 功耗与热 | 固定供电、温度与持续运行时长，记录降频后的稳态 |
| 质量 | 真实任务集、结构化输出、长上下文与工具调用回归 |

TOPS、工艺节点或参数量都不能单独决定生成速度。不沿用没有设备、构建和负载来源的 tok/s 表格；空白项通过目标设备实测补齐。

## 5. 与课程其他章节衔接

- [硬件路线图](hardware_roadmap.md)：按已有设备选择实操顺序。
- [模型版本管理](06_model_format/6.1_model_versioning.ipynb)：把图、配置和 tokenizer 作为一致的交付单元。
- [模型安全](17_model_security/17.1_model_security.ipynb)：区分内容 hash、签名与来源验证。
- [模型 OTA](19_model_ota/19.1_model_ota.ipynb)：用兼容矩阵和验证 manifest 约束灰度与回退。
- [端侧质量门禁](24_edge_mlops/24.1_edge_mlops.ipynb)：输出“可运行、数值对齐、质量合格、设备指标达标”的分别证据。

本次 CPU 实验已在 Windows / Python 3.12.9 / PyTorch 2.10.0+cu128 / ONNX 1.21.0 / ONNX Script 0.6.2 / ONNX Runtime 1.24.4 上执行通过，四组输入最大绝对误差约 `1.79e-7`。这些结果验证导出与 CPU 运行一致性；ExecuTorch、Core AI、LiteRT-LM 与真机 NPU 性能仍需在各自环境中测试。
