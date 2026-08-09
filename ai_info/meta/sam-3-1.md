# SAM 3.1：Object Multiplex 多目标联合跟踪，视频分割提速 7 倍（SAM 3.1）

- **原文链接**: [SAM 3.1 Release Notes](https://github.com/facebookresearch/sam3/blob/main/RELEASE_SAM3p1.md)
- **作者**: Meta（AI at Meta）
- **发布日期**: 2026-03-27
- **检索日期**: 2026-08-01
- **标签**: #SAM3.1 #SegmentAnything #视频分割 #ObjectMultiplex #多目标跟踪 #开源模型 #计算机视觉

> 注：SAM 3.1 未发布独立博客文章，官方通过 X（@AIatMeta）、GitHub Release Notes 与 Hugging Face checkpoint 同步发布；原文链接采用官方 GitHub Release Notes。

## 核心观点

SAM 3.1 是 Meta 对 SAM 3（2025 年 11 月发布）的 drop-in 效率升级，核心是 Object Multiplex——一种基于共享内存的联合多目标跟踪方法。此前 SAM 3 每跟踪一个对象都要独立前向计算，成本随目标数线性增长；SAM 3.1 把对象分桶联合处理，在单块 H100 上处理 128 个对象时推理提速约 7 倍，且不牺牲精度。Meta 明确把这次更新定位为"让高性能分割应用跑在更小、更易得的硬件上"，标志着开源视觉基础模型的竞争从精度转向部署效率。

## 关键发现 / 关键技术

### 1. Object Multiplex：共享内存联合跟踪
- 对象按固定容量分桶，多目标在单次前向中联合处理，消除逐对象重复计算
- 单次前向最多联合处理 16 个跟踪对象
- 中等目标数视频吞吐从 16 FPS 翻倍至 32 FPS（单块 H100）

### 2. 性能与精度数据
- 128 目标场景下单 H100 推理提速约 7 倍（对比 2025 年 11 月 SAM 3 初版）
- 视频对象分割（VOS）7 项基准中 6 项提升，MOSEv2 +2.0
- YT-Temporal-1B 上 cgF1 +2.1
- 图像精度与 SAM 3 持平（LVIS AP 48.8、SA-Co cgF1 54.1）——纯效率升级，非精度改动

### 3. 工程优化与发布形态
- 减少 CPU-GPU 同步、改进 torch.compile 支持、后处理与视觉编码器更多批处理
- checkpoint 上架 Hugging Face（facebook/sam3.1），需配合最新官方仓库代码使用
- 未集成进 Hugging Face Transformers，须使用 Meta 官方 repo

## 实践意义

视频分割的瓶颈正从精度转向部署成本：机器人、视频分析、体育赛事、剪辑工具等场景关心的是每帧成本与并发跟踪数，而非单一基准的小数点。SAM 3.1 把密集多目标视频工作流拉进消费级硬件预算内，且 checkpoint 与代码同步开源、发布即可用。对开源视觉生态，这预示"基础模型竞争"进入"推理效率竞争"阶段——后续专用视觉模型的差异化将更多体现在单位算力吞吐上。

## 跨厂商对比

- 与 [Gemini 3.5](../google/deepmind/gemini-3.5.md) 对比：Google 走通用多模态大模型路线（视频理解只是子能力），SAM 3.1 走专用分割基础模型 + 极致推理效率路线，二者在视频理解场景形成互补而非替代
- 与 [GPT-5.6](../openai/research/introducing-gpt-5-6.md) 对比：OpenAI 闭源旗舰按 token 计费，Meta 把视觉基础模型开源并持续压低部署成本，商业化路线截然相反
- 与 [Muse Spark](muse-spark.md) 互补：MSL 闭源旗舰走 Agent 商业化，SAM 系列延续 FAIR 开源传统，Meta 保持双轨并行

## 资源

- Release Notes：[RELEASE_SAM3p1.md](https://github.com/facebookresearch/sam3/blob/main/RELEASE_SAM3p1.md)
- 代码：[GitHub - facebookresearch/sam3](https://github.com/facebookresearch/sam3)
- 模型：[Hugging Face - facebook/sam3.1](https://huggingface.co/facebook/sam3.1)
- 官方公告：[X - @AIatMeta](https://x.com/AIatMeta/status/2037582117375553924)
