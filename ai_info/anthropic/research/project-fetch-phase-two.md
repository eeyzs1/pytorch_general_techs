# Project Fetch: Phase Two

- **原文链接**: [Project Fetch: Phase two](https://www.anthropic.com/research/project-fetch-phase-two)
- **作者**: Michael Ilie, C. Daniel Freeman, Kevin K. Troy
- **发布日期**: 2026-06-18
- **检索日期**: 2026-06-29
- **标签**: #Robotics #Agents #PhysicalAI #Autonomy #ProjectFetch

## 核心观点

Project Fetch 第二阶段：用 Claude Opus 4.7 **完全自主**（无人类协助）控制四足机器人完成 2025 年 8 月第一阶段由人类团队完成的任务。结果：**Opus 4.7 在每个任务上至少比人类快 10 倍，平均比有 Claude 辅助的团队快 18 倍，比无 Claude 的团队快 37 倍**。在没有专门为机器人训练的情况下，通用 Agent 的物理操作能力已逼近人类专家——这是"物理 Agentic AI 早期时代"的信号。

## 关键发现

### 1. 实验设置
- 复用 2025 年 8 月的 Project Fetch 任务：操作四足机器人、连接视频/激光雷达、编写控制程序、监测路径、检测沙滩球、自动取球
- 用 Claude Opus 4.7（带 adaptive thinking，effort=maximum，Claude Code 环境）
- 研究人员只做：插上笔记本、输入初始 prompt、批准命令、批准进入下一步

### 2. 速度对比
| 任务 | Team Claude | Team Claude-less | Opus 4.7 |
|------|-------------|------------------|----------|
| 完成任一团队 2025 年完成的任务 | 平均数 | 平均数 | **至少快 10 倍** |
| 两个团队都完成的 4 个任务 | 基线 | — | **比 Claude-less 快 37 倍** |
| 两个团队都完成的 4 个任务 | 基线 | — | **比 Team Claude 快 18 倍** |
| 代码量 | 多 | 多 | **少约 10 倍** |

### 3. Opus 4.7 仍不能完成的
- **精确移动沙滩球**：需要闭环控制——感知偏差、调整下一个命令、逐步收敛
- 模型能移动机器人到球后并准备击球，但控制粗糙、不成功
- 与人类在该阶段的表现相似（人类也需要写程序）

### 4. 仍未触及
- 更困难的物理操作（写控制策略、设计机器人系统）
- 任务仍在模型的"能力范围"内

### 5. 关键模式
- 模型演进模式：**人类借助模型 → 模型借助人类 → 模型独立完成**
- 在网络安全中已观察到类似模式，现在在物理世界也开始显现

## 关键洞察

1. **物理 Agentic AI 早期时代到来**——通用 Agent 可使用"现成物理工具"，无需专门训练
2. **速度是核心优势**——不是能力，是完成时间
3. **代码效率显著**——比人类团队少 10 倍代码实现同等或更好结果
4. **闭环控制仍是难题**——精确感知-调整-执行循环是下一个突破点
5. **不应低估演进速度**——一年内从"协助人类"到"独立完成"，下一次跳跃可能在硬件/控制策略上

## 关键数据点

| 指标 | 数值 |
|------|------|
| 速度提升（vs Claude-less） | 37 倍 |
| 速度提升（vs Team Claude） | 18 倍 |
| 速度提升（最低） | 10 倍 |
| 代码量减少 | 10 倍 |
| 第一阶段时间 | 2025-08 |
| 第二阶段模型 | Claude Opus 4.7 |

## 相关文章

- [Effective Harnesses for Long-Running Agents](../engineering/effective-harnesses-for-long-running-agents.md)
- [Building a C Compiler with a Team of Parallel Claudes](../engineering/building-a-c-compiler-with-a-team-of-parallel-claudes.md)
- [Agentic Coding and Persistent Returns to Expertise](claude-code-expertise.md)