# PyTorch 与大模型技术学习库

面向从模型训练到推理部署的中文学习资料，包含技术地图、工程笔记、Jupyter Notebook 和大数据课程。

| 方向 | 入口 | 内容 |
|---|---|---|
| LLM 工程技术 | [llm_techs](llm_techs/README.md) | 技术地图、缓存、服务调度、PyTorch 工具链 |
| 大模型训练 | [ml_train](ml_train/README.md) | 数据、架构、训练、对齐、评估与部署，126 个 Notebook |
| 端侧部署 | [on_device_deployment](on_device_deployment/README.md) | 模型压缩、硬件适配、端云协同与端侧运营 |
| 官方技术文章摘要 | [ai_info](ai_info/README.md) | 按厂商和主题组织的中文摘要及原文索引 |
| 大数据工程 | [big_data](big_data/README.md) | 从编程基础到架构设计与技术管理的课程和实验 |

## 本次内容更新 · 2026-11-17

- [推理服务与调度](llm_techs/03-推理服务与调度.md)：连续批处理、分块 Prefill、PD 分离、投机解码与满足延迟目标的吞吐量。
- [PyTorch 2.15 与大模型工程](llm_techs/04-PyTorch2.15与大模型工程.md)：官方发布要点、编译与导出、SDPA、torchao 及版本适用范围。
- [现代 PyTorch 推理实验](ml_train/09_inference_optimization/13_modern_pytorch_inference.ipynb)：无需下载模型，验证注意力掩码、编译数值一致性、计时方法及动态形状导出。
- [官方文章增量](ai_info/sync-report-2026-11-17.md)：新增 18 篇 Agent 记忆、评估、安全控制、后训练与高效推理摘要。
- [端侧运行时与交付](on_device_deployment/runtime_update_2026-11.md)：近期框架更新、硬件路线修订及 [ONNX 运行时一致性实验](on_device_deployment/05_hardware_deployment/5.5_export_runtime_parity.ipynb)。
- [湖仓与流处理工程更新](big_data/2026-11_湖仓与流处理工程更新.md)：版本兼容、CDC 恢复边界及 [可运行重放实验](big_data/labs/l3-cdc-replay/README.md)。

新资料附官方来源和检索日期。API 示例与硬件专属功能的验证范围见对应文档。

## 运行与校验

各子目录独立维护环境，安装方法见各自 README。仓库根目录可运行：

```bash
python ml_train/scripts/validate_notebooks.py
python ml_train/scripts/validate_notebooks.py 09_inference_optimization/13_modern_pytorch_inference.ipynb --execute
python ai_info/scripts/validate.py
python -m unittest discover -s big_data/labs/l3-cdc-replay -p "test_*.py"
```

第二条命令通过 Jupyter 内核运行新增实验，需要安装 `ml_train/requirements.txt` 中的依赖。
