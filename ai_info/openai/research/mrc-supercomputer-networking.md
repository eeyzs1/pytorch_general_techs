# Supercomputer Networking to Accelerate Large Scale AI Training

- **原文链接**: [Supercomputer networking to accelerate large scale AI training](https://openai.com/index/mrc-supercomputer-networking/)
- **作者**: OpenAI
- **发布日期**: 2026-05-05
- **检索日期**: 2026-06-04
- **标签**: #网络 #超级计算机 #MRC #AI训练 #Stargate #RoCE #SRv6

## 核心观点

OpenAI 联合 AMD、Broadcom、Intel、Microsoft、NVIDIA 在 OCP 发布 MRC（Multipath Reliable Connection）协议，通过多平面网络、自适应数据包喷洒和静态源路由三项技术，大幅提升 GPU 网络的性能和可靠性，已在 Stargate 超级计算机中部署。

## 三大技术支柱

### 1. 多平面网络（Multi-plane Networks）
- 将每个 800Gb/s 网络接口拆分为多个 100Gb/s 链路
- 每个接口可连接 8 个不同交换机
- 仅需两层交换机连接约 131,000 个 GPU（传统方案需 3-4 层）
- 降低功耗、组件数量和总成本

### 2. 自适应数据包喷洒（Adaptive Packet Spraying）
- 将单个传输的数据包喷洒到数百条路径
- 数据包可乱序到达，目标端按内存地址直接交付
- 检测到拥塞路径时动态替换
- 丢包时立即停用该路径并通过探测包验证恢复
- 数据包修剪（Packet Trimming）：拥塞时裁剪负载仅转发头部，避免误判路径故障

### 3. 静态源路由（SRv6-based Source Routing）
- 禁用动态路由协议（BGP）
- 使用 IPv6 Segment Routing（SRv6），发送方直接指定路径
- 交换机使用静态路由表，无需重算路由
- 消除整个路由故障类别

## 生产效果

- 在具有数百万链路的大型训练网络中，MRC 确保链路抖动对同步预训练任务无影响
- 训练前沿模型时重启 4 个 Tier-1 交换机无需协调训练团队
- 链路修复可在服务中进行，无需禁用
- 单端口故障时任务可继续运行，仅降低 1/8 性能

## 关键洞察

1. 同步预训练是"故障放大器"——集群越大，任何链路故障影响越大
2. MRC 将网络可靠性从"避免故障"转变为"故障透明化"
3. 通过 OCP 开放 MRC 协议体现了 OpenAI 的共享基础设施标准战略
4. 静态源路由 + 端到端路径管理是超大规模网络的新范式

## 相关文章

- [Introducing GPT-5.3-Codex](introducing-gpt-5-3-codex.md)