# OlmoEarth 平台：行星级地理空间推理（The OlmoEarth Platform: Geospatial inference at planetary scale）

- **原文链接**: [The OlmoEarth Platform: Geospatial inference at planetary scale](https://huggingface.co/blog/allenai/olmoearth-infrastructure)
- **作者**: Ai2（Allen Institute for AI）OlmoEarth 团队（Kyle Wiggers 执笔）
- **发布日期**: 2026-07-29
- **检索日期**: 2026-08-01
- **标签**: #地理空间推理 #大规模推理 #卫星数据 #Earth观测 #分布式系统

## 核心观点

Ai2 的 OlmoEarth 模型族在约 10 TB 多模态卫星数据上预训练，已被政府、NGO 用于森林砍伐监测、粮食安全与野火风险。但最该用这些模型的环境类组织往往缺乏管理"标注—微调—大规模推理"全生命周期的工程团队。为此 Ai2 构建 OlmoEarth 平台——把地理空间模型从微调评估带到大规模推理的基础设施，可在约一天内对洲级区域跑推理，处理数十 TB 影像，成本低于每平方公里一美分的零头。

文章拆解了行星级卫星推理的工程挑战：跨提供商发现与对齐影像、把作业分发到成百上千 worker、按需窗口化读取像素、以及在分布式计算常规失败中自动恢复。

## 关键发现 / 关键技术

### 1. 三阶段异构硬件流水线
- **数据获取与预处理（CPU，重 I/O）**：拉取、重投影、对齐、归一化影像并写成利于快速加载的格式；下载与准备常比模型推理更耗时，故交给 CPU 而非昂贵 GPU。
- **推理（GPU）**：跑前向并把最小处理后输出直写存储。
- **后处理（CPU）**：拼接各窗口输出、施加掩码/缩放、导出 Zarr/GeoTIFF/GeoJSON。多进程数据加载器持续喂 GPU，输出流式直写 blob 存储。

### 2. 两级分区与极端扇出
- OlmoEarth Run 把作业覆盖区域切成实例级 partition，再细分为模型级 window，每个 window 独立前向；相邻 partition 略重叠并在拼合时消缝。
- 北美野火风险图峰值用约 19600 CPU + 994 GPU 并行，网络吞吐超 168 GB/s，把估计 4737 小时串行算力压缩到约 30.5 小时墙钟——155× 加速；扇出受云配额约束，作为每次作业可调旋钮（输出分辨率、模型大小、原始影像缓存可换算权衡）。

### 3. 影像索引、窗口读取与失败恢复
- 自建元数据索引（对 AWS Open Data 走 SNS 通知，无变更流则每几分钟轮询上游），使外部请求跟随新影像发布节奏而非作业突发，避免压垮 ESA/Planetary Computer 的 STAC API。
- 运行时按 COG/Zarr 云优化格式做窗口化读取，只取所需字节；每个任务在动态创建的 VM 上跑可重入、幂等的 runner 容器，失败自动重试、回退备用提供商，监控进程重启停滞 runner。

## 实践意义

这是"开源基础模型 + 运营化平台"把先进模型交付给非工程团队的范本：模型开源只解决一半问题，把数据获取、大规模并行推理、失败恢复与可操作输出打通才能闭环。其工程经验（异构硬件分阶段、自建索引缓冲外部 API、可重入幂等任务、窗口化云读取）对任何大规模地理/科学推理系统都适用。路线图中的全局预计算 embedding 替代原始影像前向、以及 agent 化工具降低使用门槛，指明了下一步方向。

## 跨厂商对比

- 与 [Google WeatherNext 飓风](../../google/deepmind/weathernext-hurricane.md) 互补：两者都把 AI 用于地球尺度问题，WeatherNext 聚焦气象预报模型，OlmoEarth 聚焦把地球观测模型运营化到洲级推理基础设施。
- 与 [OpenAI 用 Codex 模拟黑洞](../../openai/research/using-codex-to-simulate-black-holes.md) 对比：同为"AI + 科学计算"，但本工作是面向多组织的生产级推理平台，而非单点科学发现。
- 与 [Google AI Co-Scientist](../../google/deepmind/co-scientist.md) 对比：Co-Scientist 是科学推理 Agent，OlmoEarth 是科学推理的工程底座，定位互补。

## 资源

- 平台主页：[allenai.org/olmoearth](https://allenai.org/olmoearth)
- 模型介绍：[OlmoEarth v1.1](https://allenai.org/blog/olmoearth-v1-1)
- 相关平台：[Skylight](https://allenai.org/skylight)、[EarthRanger](https://allenai.org/earthranger)
