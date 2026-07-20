# Claude 玩机器人：语言模型控制物理机器人的能力边界

- **原文链接**: [Claude plays robotics](https://www.anthropic.com/research/claude-plays-robotics)
- **作者**: Shmuel Berman, Michael Ilie, Jia Deng, Daniel Freeman
- **发布日期**: 2026-07-09
- **检索日期**: 2026-07-20
- **标签**: #Robotics #EmbodiedAI #PhysicalAI #Agent #控制抽象 #ProjectFetch

## 核心观点

Anthropic 系统测试了语言模型控制多种机器人身体的能力——从经典控制玩具到真实 Unitree Go2 四足机器人。核心发现：**模型能力高度依赖控制抽象层级**。直接驱动关节大多失败，但监督预训练控制器或使用简单定向工具时，模型能完成真实导航和操纵任务。这是首次大规模评估 LLM 在多种机器人任务上的控制能力，为"物理 Agentic AI"时代提供能力基线。

## 关键发现 / 关键技术

### 1. 控制抽象层级决定成败
- **直接扭矩控制**：模型大多失败——无法处理高频、连续、精确的物理控制
- **编写控制器代码**：部分成功，但调试困难
- **强化学习训练控制器**：模型能设计训练流程，但效率不高
- **监督预训练策略**：最成功——模型提供高层指令，预训练策略执行

### 2. 测试任务覆盖
- **经典控制**：摆平衡等
- **运动与导航**：四足机器人平衡、行走、空间移动
- **操纵**：机械臂抓取和移动物体

### 3. 机器人平台
- 经典控制玩具
- 模拟四足和人形机器人
- 真实 Unitree Go2（Project Fetch 同款）
- 机械臂

### 4. 模型表现趋势
- 模型在机器人任务上快速进步
- 新模型显著更强于调整策略和跨域转换感官理解
- 某些 embodiment 形式仍然难以控制

## 实践意义

这项研究对物理 AI 发展有重要指导意义：
- **控制抽象设计**：为 LLM 设计机器人接口时，应选择合适抽象层级
- **预训练策略价值**：通用策略 + LLM 高层规划是近期可行路径
- **仿真到现实**：模型在模拟中的表现可部分迁移到真实机器人
- **安全考虑**：LLM 控制物理系统带来新的安全风险

## 跨厂商对比

- 与 [Project Fetch: Phase Two](project-fetch-phase-two.md) 互补：Project Fetch 是单一机器人深度任务，本研究是多机器人广度评估
- 与 [Gemini 3.5](../../google/deepmind/gemini-3.5.md) 对比：Google 的 Gemini 系列包含机器人控制能力，Anthropic 测试通用 LLM 的机器人控制边界
- 与 [OpenAI Operator](../../openai/research/introducing-operator.md) 对比：Operator 控制数字界面（GUI），Claude 控制物理机器人

## 资源

- 相关研究：[Project Fetch: Phase Two](project-fetch-phase-two.md)
