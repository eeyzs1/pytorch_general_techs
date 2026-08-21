# 从 Hugging Face Hub 到机器人硬件：Strands Agents 与 LeRobot 打通闭环（From the Hugging Face Hub to robot hardware with Strands Agents and LeRobot）

- **原文链接**: [From the Hugging Face Hub to robot hardware with Strands Agents and LeRobot](https://huggingface.co/blog/amazon/strands-lerobot-hub-to-hardware)
- **作者**: AWS（Amazon）与 Hugging Face
- **发布日期**: 2026-08-14
- **检索日期**: 2026-08-21
- **标签**: #HuggingFace #AWS #LeRobot #Strands #机器人 #训练闭环 #开源

## 核心观点

AWS 与 Hugging Face 联合推出 Strands Agents + LeRobot 集成方案，打通"在 Hugging Face Hub 上记录/训练/部署机器人策略"的完整闭环。开发者可从 Hub 下载预训练机器人模型，用 Strands 机器人 SDK 在模拟器中训练，再部署到真实机械臂上——实现从数据集到实体硬件的端到端流程。

这一合作将 Hugging Face 的模型生态（LeRobot 机器人框架 + Hub 数据集）与 AWS 的云端训练能力、Strands 的硬件控制层连接起来，标志着开源机器人开发从"散件拼装"走向"统一平台"。LeRobot 作为 Meta 主导的开源机器人学习框架，在 AWS 集成下获得更完整的基础设施支持。

## 关键发现 / 关键技术

### 1. 训练闭环打通
- Hub 下载模型/数据集 → 模拟训练 → 真实硬件部署
- Strands Agents 提供机器人任务编排
- LeRobot 提供模仿学习与策略训练框架

### 2. 云端与硬件结合
- AWS 提供云端训练资源与推理服务
- Strands SDK 负责硬件抽象与控制
- 支持先模拟后实机（sim-to-real）工作流

### 3. 生态协同
- Hugging Face 负责模型与数据集分发
- 降低机器人开发入门门槛
- 与 NVIDIA 同期推出的 GR00T/Isaac 集成（LeRobot 生态）形成竞争与互补

### 4. 开放生态意义
- 延续"开源机器人"浪潮
- 开发者可复用社区模型而非从零训练
- 为物理 AI 进入系统化阶段提供基础设施

## 实践意义

机器人开发正在复制 LLM 生态的成功模式：模型中心化分发 + 开源框架 + 云服务。对机器人创业公司而言，这意味着不再需要自建完整 ML 基础设施。跨厂商看，Hugging Face 正从"模型托管平台"扩展为"物理 AI 平台"，与 NVIDIA 的 Isaac/GR00T 生态、Google 的 Gemini Robotics 形成三足鼎立。

## 跨厂商对比

- 与 [NVIDIA Cosmos-H-Dreams 手术机器人实时仿真](../../huggingface/blog/cosmos-h-dreams.md) 对比：Cosmos 侧重生成式仿真训练，LeRobot+Strands 侧重开源闭环与硬件部署
- 与 [Gemini Robotics 2 全身智能](../../google/deepmind/gemini-robotics-2-brings-whole-body-intelligence-to-robots.md) 对比：Google 走闭源 VLA 大模型路线，HF+AWS 走开源社区路线
- 与 [Meta Muse Code 终端编码 Agent](../../meta/introducing-muse-code-muse-spark-1-2.md) 对比：同为"开源工具链 + 云服务"模式，一个在数字世界（编码），一个在物理世界（机器人）

## 资源

- 论文：N/A
- 官方博客：https://huggingface.co/blog/amazon/strands-lerobot-hub-to-hardware
- LeRobot：https://github.com/huggingface/lerobot
