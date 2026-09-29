# Private AI Compute 新增安全服务器端记忆层(Advancing Private AI Compute with secure server-side memory)

- **原文链接**: [Advancing Private AI Compute with secure server-side memory](https://deepmind.google/blog/advancing-private-ai-compute-with-secure-server-side-memory/)
- **作者**: Google DeepMind 与 Platforms & Devices / Core / Cloud 团队
- **发布日期**: 2026-09-23
- **检索日期**: 2026-09-29
- **标签**: #隐私 #安全计算 #记忆 #个人助理 #云计算

## 核心观点

个人助理必须跨设备延续上下文,但前沿模型的算力放不进终端。Private AI Compute 的云端硬件隔离安全区此前是"无状态"的——任务结束即清除上下文,无法积累记忆。本次更新为其加上服务器端持久记忆层:一个云端安全数字保险库。

机制上,用户信息封存于按用户分割的专用加密存储;解锁密钥只保存在用户设备,包括 Google 在内任何第三方都无法读取明文。调用时设备与云端受保护隔离环境建立认证端到端加密通道,安全区在隔离内存中短暂解密、处理、再加密——官方表述为"信息如同从未离开设备"。

## 关键发现 / 关键技术

### 1. 问题:无状态安全区留不住记忆
- 云端硬件隔离安全区承载超出终端能力的算力,个人数据在受保护环境处理
- 此前设计无状态:任务结束清除上下文,助手"每事从零开始"
- 跨设备个人助理需要长期记忆,与无状态设计直接冲突
- 算力、隐私、记忆构成三角难题:终端算力不足、云端信任不足、记忆又必需——服务器端记忆层是三者的折中解

### 2. 服务器端记忆层:云端数字保险库
- 用户信息封存于按用户分割的专用加密存储,用户之间互相隔离
- 解锁密钥只在用户设备;包括 Google 在内任何第三方无法读取明文
- 记忆持久化:任务结束后上下文不再清除,跨会话、跨设备延续
- 调用链路:设备与云端受保护隔离环境建立认证端到端加密通道 → 安全区在隔离内存短暂解密 → 处理 → 再加密

### 3. 可验证的信任机制
- 技术白皮书更新,公开架构细节
- 服务器软件防篡改的公开记录:设备在送出数据前可验证云端运行的软件版本
- 领先安全公司独立审计,形成外部制衡
- 三重机制各司其职:白皮书管透明度、防篡改记录管可验证性、审计管公信力

### 4. 定位:架构与路线更新,非全量上线
- 官方明确这是架构与路线图更新,并非即刻全量交付的产品能力
- 从无状态到有状态的过渡,依赖白皮书、防篡改记录与审计逐项落地

## 实践意义

这是"云上个人记忆"目前最完整的隐私架构参照:设备持钥、按用户分割加密、可验证的服务器软件透明度、独立审计——四件套几乎构成个人数据云端处理的信任清单。做跨设备助手、健康档案、家庭记忆类产品的团队可直接拿它当设计评审模板。

短期内它不可直接调用:定位是路线图而非产品接口。工程团队应跟踪白皮书与审计报告的更新节奏,把"数据是否离开设备、以什么形态离开"纳入与 Google 生态集成的尽职调查项;对手厂商则会面对"云端记忆可验证性"的新竞争维度。

对 Google 自家生态,这一层也是个人助理路线的前置件:没有可验证的记忆隐私架构,跨设备助手积累的长期上下文就会成为监管与信任的最大风险点。

## 跨厂商对比

- 与 [Claude 的记忆无处不在](../../anthropic/engineering/claudes-memory-works-everywhere.md) 对比:Anthropic 把记忆做成跨环境的产品能力(便利优先、服务端托管),Google 用硬件隔离 + 设备持钥把记忆做成密码学架构(隐私优先)——记忆产品化 vs 记忆架构化两条路线。
- 与 [浏览器内构建的 Cowork](../../anthropic/engineering/cowork-built-in-browser.md) 对比:Cowork 把执行边界收回浏览器本地,Private AI Compute 把边界延伸到云端安全区——对"数据去哪儿"给出相反方向的答案,分别适合轻负载与重负载场景。
- 与 [Gemini 3.8 Live 与 Live Extended Thinking](gemini-3-8-live-extended-thinking.md) 互补:Live 系提供实时多模态交互能力,Private AI Compute 决定这些能力能否带着长期记忆进入个人场景——能力层与信任层的分工。

## 资源

- 官方文章:https://deepmind.google/blog/advancing-private-ai-compute-with-secure-server-side-memory/
- 相关能力层:https://deepmind.google/blog/introducing-gemini-3-8-live-and-3-8-live-extended-thinking/

> 注:deepmind.google 在检索环境不可达,本文经 my2cents.ai 日报(引用官方原文)/the-decoder/spyingbee 等多源交叉验证。
