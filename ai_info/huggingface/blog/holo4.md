# Holo4：驱动通用 computer-use agent（Holo4: Powering the General-Purpose Computer-Use Agent）

- **原文链接**: [Holo4: Powering the General-Purpose Computer-Use Agent](https://huggingface.co/blog/Hcompany/holo4)
- **作者**: H Company 团队（39 人署名）
- **发布日期**: 2026-09-28
- **检索日期**: 2026-09-29
- **标签**: #ComputerUse #开源权重 #GUIAgent #MoE #Agent训练

## 核心观点

H Company 发布开源权重的 computer-use 模型家族 Holo4：27B 稠密与 35B-A3B MoE 两个尺寸，BF16/FP8/NVFP4/GGUF 全格式。核心主张是"单一模型统一行动通道"：GUI 点击、代码沙盒、MCP、REST API 四条通道由同一个模型驱动，穿越桌面、浏览器、Android 与终端四类环境，而非为每类环境单独训练专用模型。

训练侧的关键设施是 Agentic Task Factory：从软件文档与截图合成约 1 万个可自动验证的任务环境，部分任务同时暴露 GUI 与 MCP 双路径，训练模型"择路"。团队对差距毫不掩饰：OSWorld 2.0 上 27B 为 61.7%、MoE 仅 30.9%，并直接引用 Claude Opus 5.5 的 81.8% 作对照；全部基准轨迹开源可回放。

## 关键发现 / 关键技术

### 1. 模型家族与部署格式

- 27B 稠密模型是主力：OSWorld 2.0 达 61.7%，进入开源权重 computer-use 模型第一梯队。
- 35B-A3B MoE 版本面向低成本高并发，但 OSWorld 2.0 仅 30.9%——团队公开承认稀疏化在精细 GUI 操作上代价显著。
- BF16/FP8/NVFP4/GGUF 多格式覆盖服务器 GPU、Apple Silicon 与消费级显卡的本地部署。

### 2. 四通道统一行动空间

- 同一模型统一 GUI 点击、代码沙盒、MCP、REST API 四条行动通道，环境覆盖桌面、浏览器、Android、终端。
- 传统做法是为每类环境微调专用模型并在外围做路由；Holo4 把路由内化进模型自身的通道选择。
- 多通道也改变了能力分析口径：同一任务走 GUI 与走 MCP 的成功率差异本身成为研究对象。

### 3. Agentic Task Factory 任务合成

- 从软件文档与截图自动合成约 1 万个可自动验证的任务环境，直击 computer-use 训练数据稀缺问题。
- 部分任务同时暴露 GUI 与 MCP 双路径，奖励模型按环境选择更优通道，训练"择路"能力。
- 任务自带自动验证器，训练信号不依赖人工判分。
- 约 1 万个环境的合成成本远低于人工设计任务，且可随软件版本更新重新合成。

### 4. 效率优势与轨迹开源

- Godot Pac-Man 项目任务上，Holo4 27B 用 68 次调用、240 万 token 完成；Qwen3.8-27B 底座需 197 次调用、1140 万 token。
- 相当于节省 65% 的工具调用与 79% 的 token 消耗，长 horizon 任务的成本优势被系统性放大。
- 全部基准轨迹开源可回放，社区可独立核对失败模式与调用分布，而非只看总分。

## 实践意义

对构建 computer-use agent 的团队，Holo4 提供了闭源 API 之外的开源权重选项：可本地部署、可审计调用轨迹、可在自有环境上继续微调。"单模型多通道"设计提示外围工程可大幅简化——不必再维护 GUI 与 API 两套技能栈。其差距披露方式同样值得学习：引用竞品最高分、公开 MoE 短板与全部轨迹，把"还差多远"变成可验证的事实而非营销话术。

## 跨厂商对比

- 与 [Introducing Operator](../../openai/research/introducing-operator.md) 对比：Operator 是托管的 computer-use 服务（模型 + 虚拟机 + 安全护栏），Holo4 是开源权重模型，用户自持环境与数据，可控性与可迁移性更高。
- 与 [Claude Opus 5.5](../../anthropic/research/claude-opus-5-5.md) 对比：Holo4 发布稿直接引用 Opus 5.5 的 OSWorld 2.0 81.8% 作为差距参照（27B 为 61.7%），闭源前沿仍领先约 20 个百分点。
- 与 [State of Open Models: Summer 2026](state-of-open-models-summer-2026.md) 互补：为开源/闭源能力版图补上 computer-use 维度的最新数据点。

## 资源

- 论文：N/A
- 代码：[Hcompany（Hugging Face 组织页，含 Holo4 全格式权重）](https://huggingface.co/Hcompany)
- Demo：[Holo4 发布文与基准轨迹下载](https://huggingface.co/blog/Hcompany/holo4)
