# Core Dump Epidemiology: Fixing an 18-Year-Old Bug

- **原文链接**: [Core dump epidemiology: fixing an 18-year-old bug](https://openai.com/index/core-dump-epidemiology-data-infrastructure-bug/)
- **作者**: OpenAI Engineering
- **发布日期**: 2026-06-30
- **检索日期**: 2026-07-07
- **标签**: #Debugging #Infrastructure #C++ #CoreDump #Epidemiology #Reliability #Libunwind #Rockset

## 核心观点

OpenAI 工程师通过"流行病学家式"诊断方法（而非"医生式"个体诊断）发现并修复了 Rockset 服务中看似不可能的两个独立 bug：一个由**单台 Azure 物理主机的静默硬件损坏**引起，另一个来自 **GNU libunwind 中一个存在 18 年的竞态条件**。本文展示了如何从混乱的 core dump 群体数据中分离信号——这是 Agent 时代基础设施可靠性工程的关键范式。

## 问题现象

- Rockset（OpenAI ChatGPT 数据基础设施，被数据插件与对话搜索大量使用）的 C++ 执行层偶发段错误
- 看似不可能的失败模式：正常 C++ 函数"返回到非法地址"
- 部分案例：返回地址槽为 NULL；部分案例：`%rsp` 像在普通执行中被减了 8 字节
- 因 Rockset 查询处理 leaf 是复制的，单次崩溃对客户端影响小，但每个 segfault 都对应一个必须修复的 bug

## 诊断方法演进

### 1. 医生模式（失败）
- 仔细检查几个 core dump，逐个形成假设并排除
- 候选包括：C++ 代码 bug、编译器/链接问题、运行时库、Linux 内核 bug（信号/上下文切换）、罕见故障
- ASAN staging 未捕获 → 不像是简单越界写
- 手动检查更多 core dump 效率太低

### 2. 信号深度调查（部分进展）
- Rockset 编译用 `-fno-omit-frame-pointer`，`%rbp` 总是可达
- AMD64 ABI 保留 128 字节 red zone，信号处理时不被内核破坏
- 通过 red zone 看到了"函数 X 已弹出，但返回地址槽为 NULL"
- 高度怀疑是**异常处理**——因为 unwind 本质上接近 `longjmp` 或纤程切换，必须恢复 callee-save 寄存器、`%rbp` 和 `%rsp`

### 3. 流行病学家模式（突破）
- 让 ChatGPT 写脚本下载每个 core dump 的前缀，提取寄存器，用日志过滤已知误报，自动标记三类崩溃：
  - return-to-null
  - misaligned-stack
  - other
- 在过去一年所有 Rockset 生产 core dump 上并行运行
- 一旦有干净数据集，**相关性立刻浮现**：

| 崩溃类型 | 集群 / 区域 | 开始时间 | 节点寿命 |
|----------|-------------|----------|----------|
| return-to-null | 跨多集群、跨区域 | 频率近期上升但无明确起始日 | — |
| misaligned-stack | **单区域** | **明确开始日** | 永不在长寿节点上 |

## 两个独立 bug

### Bug #1：单台 Azure 物理主机硬件损坏
- 通过 Kubernetes 节点列表与时间戳，把 misaligned-stack 崩溃追溯到**单台物理主机**
- 该主机从服务中移除后，misaligned-stack 崩溃**完全消失**
- 在控制环境数周压力测试**未能复现**寄存器损坏
- 改进：fatal signal handler 现在包含寄存器状态以便仅凭日志检测复发；控制平面改为**重用而非回收** VM，使坏节点检测更简单

### Bug #2：GNU libunwind 18 年竞态条件
- 重新审视 return-to-null 崩溃：所有案例**都发生在异常 unwind 期间**
- 二进制链接了 libgcc 与 GNU libunwind 两个含异常 unwind 实现的库，动态链接器选了 libunwind（而非预期的 libgcc）
- unwind 本质上接近 `setcontext` 风格的寄存器恢复——如果目标 IP 在控制转移前已变成 NULL，就会表现为"返回到 NULL"
- libunwind 存在**单一指令的竞态窗口**，导致目标地址变成 NULL
- 为什么现在出现？频率近期上升，但与具体服务规模 / 流量 / 节点寿命**没有清晰相关性**

## 修复措施

1. **改进 fatal signal handler**：包含寄存器状态以仅凭日志检测复发
2. **VM 重用而非回收**：让坏节点检测在基础设施层更简单
3. **更新 runbook 与团队心智模型**：包含硬件损坏可能性
4. **修复 libunwind**：贡献 patch 给上游 GNU 项目

## 核心启示

### 1. 流行病学家 > 医生
- 当数据量大、模式相似但根因不同时，单病例深挖会陷入**误把多类问题当一类问题**
- 高质量**全人群级数据集**能立刻揭示单病例无法看到的模式
- 自动分析 pipeline 比人工检查更可扩展

### 2. ChatGPT 充当诊断助手
- 编写自动分析脚本（下载、提取、过滤、分类）
- 加速形成假设但**不应代替证据**
- 与工程师的交互式对话帮助打破错误假设

### 3. 异常处理不是普通函数调用
- unwind 涉及动态控制转移，恢复 `%rbp` / `%rsp` / callee-save 寄存器
- 任何 unwind 实现 bug 都可能在生产中表现为看似"返回到 NULL"或"栈指针错位"
- 慎用非标准 unwind 实现（libgcc vs libunwind 二选一时要明确）

## 与其他基础设施事后分析的对比

- 与 [A Postmortem of Three Recent Issues](../../anthropic/engineering/a-postmortem-of-three-recent-issues.md) 类似：都是关于"基础设施问题伪装成模型问题"
- 与 [An Update on Recent Claude Code Quality Reports](../../anthropic/engineering/an-update-on-recent-claude-code-quality-reports.md) 形成对比：Anthropic 的质量下降源自三个独立工程变更，OpenAI 的崩溃源自两个独立 bug（硬件 + 上游库）
- 与 [Quantifying Infrastructure Noise in Agentic Coding Evals](../../anthropic/engineering/quantifying-infrastructure-noise-in-agentic-coding-evals.md) 互补：都强调基础设施配置对性能的影响，但本文更偏**可靠性**而非**基准噪声**