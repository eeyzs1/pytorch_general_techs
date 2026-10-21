# 重新设计 Anthropic 的源码管理：五个月自研 Scion（Redesigning source control at Anthropic）

- **原文链接**: [Redesigning source control at Anthropic](https://www.anthropic.com/engineering/redesigning-source-control)
- **作者**: Nick G. 及源码管理团队（S.G.、R.K.、Dan C.、Garrett H.、Ben L.、Colin M.、Joe P.）
- **发布日期**: 2026-10-13
- **检索日期**: 2026-10-16
- **标签**: #Scion #版本控制 #monorepo #agent规模 #基础设施 #antique

## 核心观点

当 Claude 写码使日均合并从 5 月约 2,500 次涨到 9 月 30,000+ 次（12 倍），为人类尺度构建的开发基建（源码管理/构建/CI）成为新瓶颈。Anthropic 的回应是 7 人团队五个月完成三件事：自研版本控制系统 Scion 并把 monorepo 从 git 整体迁出、配套代码评审工具 Antique 与代码搜索、富源码管理 IAM——核心洞察是"客户端永远在线"：git 为离线分布式设计的能力（本地全量历史/blame）在 agent 场景反而是负担。

效果量化：基础设施足迹比 git 镜像方案小 200 倍（CPU/内存），CI checkout 快两个数量级（分钟→秒），CI 一项就释放 25% CPU 容量。方法论闭环：Claude 既是瓶颈成因，也是五个月建成的原因（Mythos Preview 把手写的导入管线重写为 1/20 内存、4× 速度）。

## 关键发现 / 关键技术

### 1. 为什么 git 撑不住
- 主分支历史近 100 GB、压缩工作副本 25 GB+；CI 每天约 2,500 万次 checkout，天真拉取等于 600 PB/日流量
- 曾跑数百个内部 git 镜像续命：镜像越来越大、seed 与 main 脱节、partial clone 上 diff/blame 越来越难维护

### 2. Scion 的六条设计原则
- 客户端永远在线：围绕常驻服务器设计协议，按需取数
- 客户端-服务器不对称：服务器管 diff/blame/commit/merge，客户端只留有界缓存与工作副本
- 源码管理服务化：客户端用的全部查询同时以 API 暴露，多数 CI/工具不再需要本地仓库（自动 bisect/revert 流水线因此可行）
- 全面水平扩展：内容寻址 + 无全量物化副本 + 无 packfile 维护
- commit 廉价/增量/无锁：服务器端建 changeset，成本只随变更规模走；弱化 refs（全局状态是扩展天敌）
- 工作副本可选且默认稀疏：稀疏/虚拟化 checkout，写操作也可纯 API

### 3. 架构与数据结构
- changeset = write-ahead log 条目，只存相对第一父节点的变更文件 + 内容寻址 blob 指针；blame/路径历史/commit 图跳表等"派生数据"用统一递归机制按需计算
- scn client → 每节点 scion-daemon → 区域 scion-cache → 权威 scion-server（Spanner/云存储）三层缓存，全层命中率 >99%
- 对标 Google Piper / Meta Sapling（Mononoke 的 Bonsai 数据模型为先驱），明确不适配 git 一般场景

### 4. agent 时代的工程学
- 7 人 × 5 个月建成整套系统并完成迁移，同期合并量涨 10 倍——"小团队快速迁移"将成为常态
- 工程师价值转向：所有人承认 Claude 更会"写"，但系统边界、取舍判断、"对 Claude 说不"（阻止暴力扫 commit log、拒绝过度防御性设计）仍靠人；review 转为审"变更意图"而非逐行
- Claude Tag "superfans"：每组件一个 Slack 频道养一个只盯该组件健康度的 Claude，比传统告警多捕捉细微异常
- 传统 merge queue 在 agent 尺度失效：转向 post-merge/pre-deploy 测试，并发冲突让 Claude 修——比人发现冲突还快

## 实践意义

这是"agent 规模软件工程"的第一份系统级案例：当写码无限快，瓶颈全部转移到集成与验证，源码管理、CI、评审都需要按"客户端永远在线、变更无限多"重设计。对大团队的近期启示：不必自研，但应开始审计自己的 git 服务端架构——服务器端 RPC 化、协商协议简化、稀疏特性组合可用性，都是可以反过来给 git 平台提的方向。组织启示同样重要：merge queue/全局锁等"人类尺度"惯例在 agent 尺度下是可以、也应该抛弃的。

## 跨厂商对比

- 与 [Building a C Compiler with a Team of Parallel Claudes](building-a-c-compiler-with-a-team-of-parallel-claudes.md) 对比：编译器篇证明 agent 团队能产出大型代码，本文回答"产出到哪去"——上游产能爆炸倒逼下游基建重构
- 与 [How We Made claude.ai 3x Faster](how-we-made-claude-ai-faster.md) 互补：一个优化面向用户的前端路径，一个重建面向 agent 的源码底座——"AI 主导研发"在应用层与基建层的两翼
- 与 [An Update on Recent Claude Code Quality Reports](an-update-on-recent-claude-code-quality-reports.md) 对照：4 月的事故是基建 bug 伪装成模型退化，本文是把基建本身按 agent 尺度重造——从事后修复到主动架构演进

## 资源

- 论文：无
- 代码：无
- Demo：无
