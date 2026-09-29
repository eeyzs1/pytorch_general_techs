# ZCube:面向下一代大模型推理的网络架构(ZCube: A Network Fabric for Next-Generation LLM Inference)

- **原文链接**: [ZCube: A Network Fabric for Next-Generation LLM Inference](https://www.zhipuai.cn/zh/research/160)
- **作者**: 智谱 AI、驭驯网络、清华大学
- **发布日期**: 2026-05-20
- **检索日期**: 2026-09-29
- **标签**: #ZCube #推理网络 #PD分离 #智谱 #SIGCOMM2025 #集群架构

## 核心观点

PD(预填充-解码)分离架构把 KV Cache 传输变成了推理集群的"新内存墙",但传统数据中心网络(如 ROFT 静态拓扑)假设流量源-目对称,与 PD 分离下"少数 Prefill 节点向大量 Decode 节点搬运 KV Cache"的不对称模式错配,导致局部热点与链路利用率低下。

智谱联合驭驯网络与清华提出 ZCube 拓扑:取消传统 Spine 层,由 Leaf 交换机构成奇、偶两组完全二部图互联,任意两节点直径仅 2 跳,天然匹配 KV Cache 多对多散射的流量形态。该架构源自 SIGCOMM 2025 论文 From ATOP to ZCube,并已在千卡生产集群(承载 GLM-5.1 coding 业务)完成验证,同时降低网络 capex 与提升 GPU 有效吞吐。

## 关键发现 / 关键技术

### 1. 问题定义:KV Cache 传输的源-目的不对称

PD 分离改变了集群流量的方向性假设,这是 ZCube 全部设计的出发点。

- PD 分离后,Decode 请求需从 Prefill 实例拉取 KV Cache,流量呈"少量源、大量目的"的散射形态
- 传统云网络流量假设源-目对称,ROFT 等静态拓扑在 KV 搬运高峰下出现局部热点
- 光模块与交换机投入随集群规模线性膨胀,成为推理成本的重要组成
- Coding 长上下文业务放大了该矛盾:单请求 KV Cache 体积大、传输时延直接影响 TTFT

### 2. ZCube 拓扑设计

用拓扑结构与流量形态"同构"的方式消灭热点。

- 取消 Spine 层,仅保留 Leaf 交换机,层级更扁平
- Leaf 划分奇、偶两组,构成完全二部图互联
- 任意两节点通信直径 2 跳,无跨层 Oversubscription 瓶颈
- 拓扑与 KV Cache 散射流量天然同构,热点被二部图结构均匀稀释

### 3. 千卡生产集群实测

数据来自承载 GLM-5.1 coding 业务的千卡生产集群,而非实验室环境。

- 交换机与光模块 capex 降低 33%
- 按万卡集群折算,节省约 2.1 亿至 6.4 亿元人民币
- GPU 平均推理吞吐提升 15%
- 首 Token 时间 TTFT P99 降低 40.6%,长尾体验显著改善

### 4. 平滑演进能力

架构的生命力在于不推翻现有投资也能升级。

- 链路速率从 100G 升级到 200G 时,吞吐再提升 19%
- 拓扑对现有 GPU 节点透明,无需改造计算侧
- 已在生产环境承载真实业务,而非纸面推演

### 5. 学术渊源与产学研分工

- 源于 SIGCOMM 2025 论文 From ATOP to ZCube
- 智谱(业务场景)+ 驭驯网络(网络工程)+ 清华(体系结构研究)
- 学术成果到生产部署的完整闭环

### 6. 组网工程含义

对交换机选型与运维的具体影响。

- 取消 Spine 后交换机层级减少,组网规则更简单
- 完全二部图结构让流量分担可预测,便于容量规划
- 2 跳直径降低了跨集群时延不确定性,利于 TTFT 控制

## 实践意义

ZCube 把"推理基础设施降本"从模型侧(稀疏注意力、量化)延伸到了网络侧:当 KV Cache 搬运成为 PD 分离的主要带宽消费者,拓扑设计本身就是吞吐工程。对自建推理集群的团队而言,33% 的网络 capex 降幅与 15% 的 GPU 有效吞吐提升意味着同批算力可承载更多并发;TTFT P99 降低 40.6% 对 Coding Agent 这类交互式场景尤为关键。而对超大规模(万卡级)部署,2.1 亿至 6.4 亿元的节省直接改写推理的单位经济模型——网络拓扑第一次成为与模型架构同等级的成本杠杆。

## 跨厂商对比

- 与 [DeepSeek-V4 API 定价](../../deepseek/news/deepseek-v4-api-pricing.md) 对比:DeepSeek 靠模型侧架构创新压低 token 单价,ZCube 代表"网络侧降本"路线,两者共同指向推理单位经济模型的持续优化
- 与 [GLM-5.1 开源:独立工作 8 小时的模型](glm-5-1.md) 互补:GLM-5.1 的 coding 长任务推理正是 ZCube 千卡集群承载的真实业务负载,模型能力与基础设施同步演进
- 与 [Scaling Pain:超大规模 Coding Agent 推理实践](glm-scaling-pain.md) 互补:Scaling Pain 攻关 serving 软件栈的稳定性,ZCube 从物理网络层解决同一业务的高并发搬运问题
- 与 [GLM-5.3:前沿编程能力与涌现的网络安全能力](glm-5-3.md) 对照:GLM-5.3 证明模型能力迭代,ZCube 证明其底层推理网络的配套演进

## 资源

- 官方发布:https://www.zhipuai.cn/zh/research/160
- 论文:From ATOP to ZCube(SIGCOMM 2025)
- 相关模型:https://www.zhipuai.cn/zh/research/157
- 智谱开放平台:https://www.bigmodel.cn/
