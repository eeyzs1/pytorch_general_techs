# Muse Spark Open：816B 开放权重、$20M 许可门槛与两台 Mac Studio（Introducing Muse Spark Open, The Most Capable US Open-Weight Model to Date）

- **原文链接**: [Introducing Muse Spark Open, The Most Capable US Open-Weight Model to Date](https://research.meta.ai/blog/muse-spark-open)
- **作者**: Meta Superintelligence Labs（MSL）
- **发布日期**: 2026-10-15
- **检索日期**: 2026-10-16
- **标签**: #MuseSparkOpen #开放权重 #MoE #许可证 #本地部署

## 核心观点

10 月 15 日 Meta 发布 Muse Spark Open：816B 总参 / 42B 激活的原生多模态 MoE、1M 上下文，官方称"迄今最强的美国开放权重模型"，主打编码、长时程任务与多步推理。这是 9 月 2 日 Muse Spark 1.3 发布时 Zuckerberg 开放权重预告的兑现——但落地形态是独立的 Open 版本而非开放 1.3 本身。与 Apple 合作优化 MLX：量化后约 493GB，两台 512GB M5 Ultra Mac Studio 即可本地运行完整模型。

"开放"附带明确商业门槛：Muse Model License 规定任何连续 12 个月 MaaS 收入达 $20M 即触发商业授权，且须署名"Built with Muse Spark Open"，下载还需填写法定姓名、出生日期与组织全称的门控表单。独立榜上 AA Intelligence Index 39（追平 DeepSeek V4.1），与三天前闭源旗舰 Muse Wonder（56）相差 17 分——Forkast 评述：这个差距不是缺陷，就是策略本身：前沿闭源，开放权重专注 Agent 与编码工作流。

## 关键发现 / 关键技术

### 1. 规格与基准：口径内的最强
- 816B 总参 / 42B 激活 MoE，1M token 上下文，原生多模态输入（文本/图像/视频/音频），面向编码、软件工程、长时程多步推理。
- AA Intelligence Index v4.3.2 得 39，追平 DeepSeek V4.1，落后 GLM 5.3（45）、Kimi K3（44）、Qwen3.8（40）——"美国最强开放权重"是限定国内市场的口径。
- Meta 自评：JobBench 61.8、MCP-Atlas 89.2（外部工具使用）、HLE-Diamond 26.1；并自称 agentic 任务与视觉推理超过 GLM 5.3 与 Kimi K3（厂商自评，无独立验证；部分类别如编程仍被反超）。

### 2. 许可证：$20M MaaS 收入门槛
- Muse Model License：任何连续 12 个月 MaaS 收入 ≥$20M 需取得商业授权；输出须含"Built with Muse Spark Open"署名；未设硬件 OEM 条款（较 StepFun 宽松）。
- 门控下载表单收集法定姓名、出生日期、组织全称——评估权重之前先交组织信息，与 DeepSeek V4（MIT）/GLM-5.3 Flash（Apache 2.0）的零门槛分发形成对照。
- 行业趋势：StepFun Model License 1.0 与 Mistral 收入门槛模型同样收敛于 $20M 量级——"权重可下载 + 商用有条件"正在成为开放权重新常态。

### 3. 两台 Mac Studio 跑 816B（Apple 合作）
- BF16 完整权重约需 1.6TB 内存；经 Apple MLX 量化降至约 493GB。
- 2 台 512GB M5 Ultra Mac Studio（pipeline / tensor 并行 + Thunderbolt 5 RDMA）可运行完整模型，等效约 1TB 统一内存；Engadget 称 4 台 256GB 配置约 $38,000；512GB 机型 Apple 称"十月下旬"发售。
- Apple 实测：4 机并行下生成速度提升 2.33–2.41×、8k 输入首 token 延迟 1.76×，最高约 36.7 tok/s（超人均阅读速度）；Apple 同日发布 MLX 分布式推理研究博客。
- 现场演示（Muse Code on-device）：修复开源 Mastodon iOS 客户端 bug 与新功能、在 DaVinci Resolve 中审片与裁剪视频。

### 4. 分发生态与安全
- 权重：Hugging Face（meta-models/Muse-Spark-Open-816B-A42B）、Amazon SageMaker AI、Google Cloud Model Garden、Microsoft Foundry。
- 托管 API：Baseten、Fireworks AI、Groq、Modal、Nebius、OpenRouter、Together AI；推理栈：SGLang、vLLM、TensorRT-LLM、Transformers、MLX、llama.cpp、Unsloth。
- 安全：因开放权重固有风险追加安全训练，达到内部安全框架发布阈值；完整评估报告承诺稍后发布，先见 HF 模型卡。

## 实践意义

对自托管团队：1M 上下文 + Agent/编码调优的大 MoE 首次进入工作站价位（约 $38k 起），本地化部署的合规与数据边界诉求有了新选项——但 $20M 收入门槛决定了它只适合"低于门槛或愿意谈判"的部署方，规模化前必须完成许可证审计。"开放"的定义正在坍缩为"可下载 + 有条件商用"，模型选型流程需把许可条款与基准分数同权重对待。与 Wonder 的 17 分差距表明：开放权重不再是前沿的延迟镜像，而是被刻意定位的次前沿产品线——部署方应按"特定工作流工具"而非"通用智能"评估它。

## 跨厂商对比

- 与 [Muse Spark 1.3](introducing-muse-spark-1-3.md) 对比：Zuckerberg 9 月 2 日预告的开放权重最终以独立 Open 版（816B/42B）落地，Spark 1.3 本体保持闭源——承诺兑现但对象换轨，且 Open 的 AA 39 低于 1.3 的 48，开放版始终次前沿一档。
- 与 [Muse Glimmer](introducing-muse-glimmer.md) 对比：同撑开放双轨，Glimmer 是 30B Apache 2.0 零门槛端侧模型，Spark Open 是 816B 门控许可大 MoE——Meta 形成"宽松小模型 + 严苛大模型"两层开放结构，与 8 月开放宣言的纯粹口径渐行渐远。
- 与 [Kimi K3](../kimi/blog/kimi-k3.md) 对比：AA 榜 K3（44）高于 Spark Open（39）且更早发布，中国开放旗舰在总分上占先；Meta 的差异化在于 Apple 生态联运与云市场全网分发，而非榜分。
- 与 [The Future is for Everyone](the-future-is-for-everyone.md) 呼应：8 月宣言主张"开放防止权力集中"，10 月落地却是 $20M 门槛 + 门控表单 + 强制署名——理念与执行的落差成为观察 Meta 开放战略的标尺。

## 资源

- 论文：无
- 官方博客：https://research.meta.ai/blog/muse-spark-open
- 权重：https://huggingface.co/collections/meta-models/muse-spark-open
- Demo：https://dev.meta.ai/models/muse-spark-open
- Apple MLX 分布式推理：https://machinelearning.apple.com/research/mlx-distributed-inference

> 注：research.meta.ai 在本环境不可达，本文经 Forkast、GIGAZINE、Artificial Analysis、Pakistan Post/Engadget 转述多源交叉验证，官方 URL 见资源。
