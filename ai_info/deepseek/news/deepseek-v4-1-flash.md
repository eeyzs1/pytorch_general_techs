# DeepSeek-V4.1-Flash 发布：Flash 级成本超越旗舰（DeepSeek-V4.1-Flash: Smarter, Faster, More Efficient）

- **原文链接**: [DeepSeek-V4.1-Flash Release](https://api-docs.deepseek.com/zh-cn/news/news260910)
- **作者**: DeepSeek（深度求索，官方新闻无个人署名）
- **发布日期**: 2026-09-10
- **检索日期**: 2026-09-29
- **标签**: #DeepSeek #V4.1-Flash #原生多模态 #KVCache压缩 #峰谷计费

## 核心观点

DeepSeek 发布 V4.1-Flash：全新模型架构家族中尺寸最小的成员，具备原生多模态视觉理解。552B 参数 MoE 采用全新 Causal Encoder–Decoder 非对称架构（输入侧激活 8B、输出侧 16B），配合新预训练方法与更大规模 RL 后训练，官方基准显示其智能水平超越包括 V4-Pro 在内的旗舰模型——以 Flash 级定价获得超旗舰级 Agent + 多模态能力。

同时这是一次激进的代际切换：模型名改为 `deepseek-flash`，旧 `deepseek-v4-flash` 与 `deepseek-v4-flash-vision-exp` 名称仍被接受但对应模型已退役（视觉能力并入原生多模态，Vision-Exp 实验线终结），请求自动路由至 V4.1-Flash 并按 Flash 价计费。权重与技术报告已在 Hugging Face 开源。

## 关键发现 / 关键技术

### 1. 基准：小尺寸反超自家旗舰
- GPQA Diamond 90.9、Codeforces Rating 3471、Terminal-Bench 2.1 达 90.6（TB 3.0 为 30.0、TB 4.0 为 31.2）、DeepSWE v1.1 74.2、HLE 带工具 63.9、CyberGym 88.1、Agents' Last Exam 31.8、MathArena Apex 65.6——官方称多方测试表明性能、费用、速度、总用时全面超越 V4-Pro。

### 2. KV Cache 压缩：Agent 成本的隐形杠杆
- KV Cache 相对上一代压缩到 HBM 需求 1/4、SSD 需求 1/8（相对初代模型累计缩小 437 倍）；缓存命中费用在 Agent 场景占比很高，长时 Agent 任务成本直接大幅下降。

### 3. API 与定价
- 上下文 1M、最大输出 384K、并发 2500。定价 2026-09-10 12:00（北京时间）生效,延续峰谷计费（闲时为峰时一半,峰时段为工作日 01:00-04:00 与 06:00-10:00 UTC）:输入缓存命中 $0.003-0.006、未命中 $0.15-0.30、输出 $0.60-1.20 每百万 token（对比 v4-pro 输入 $0.66-1.32 / 输出 $1.98-3.96）。
- V4-Pro 下线口径演变:新闻页原称 9 月 14 日起 `deepseek-v4-pro` 路由至 V4.1-Flash,同日 Change Log 改口"应用户需求继续提供 V4 Pro 服务、计费不变";截至 09-29 定价页仍列 deepseek-v4-pro（V4-Pro-0813）,当前事实以"V4 Pro 继续服务"为准。

### 4. 生态与开源
- 权重与《DeepSeek_V41_Tech_Report》在 Hugging Face 开源;欢迎具备 2000 卡 GPU 与存储集群的团队洽谈大规模部署;腾讯 WorkBuddy/CodeBuddy 与 OpenCode 已作为官方合作伙伴全量接入。

## 实践意义

对存量 V4-Flash/Vision-Exp 用户:模型名不变、零改造迁移即获能力升级 + 降价,Vision-Exp 的"实验性多模态"正式转正为原生能力。对重负载 Agent 任务:KV Cache 压缩 + 闲时调度 + 缓存命中低价三者叠加,长时 Agent 的成本模型被重写。对行业:Flash 级模型反超旗舰意味着"旗舰 = 最强"的定价叙事失效,DeepSeek 用同架构家族（可扩展出更大参数模型）预告了 V4.1-Pro 的到来。

## 跨厂商对比

- 与 [DeepSeek-V4-Flash-Vision-Exp 上线](deepseek-v4-flash-vision-exp.md) 对比:Vision-Exp 以"实验版本外挂模态"渐进补齐视觉（单图 384 tokens）,V4.1-Flash 把视觉收编为原生多模态并直接退役实验线——渐进路线三个月走完闭环。
- 与 [V4-Pro GA 与 API 调价](deepseek-api-price-adjustment-2026-08.md) 对照:8 月调价"收刀"（涨幅最高 1100%）,9 月 V4.1-Flash 降价——涨的是旧旗舰 Pro、降的是新 Flash,"以价换量"重心迁移到新架构家族。
- 与 [GLM-5.3-Flash](../../glm/blog/glm-5-3-flash.md) 互为镜像:两家都以"Flash 级尺寸 + 1M 上下文 + 原生多模态 + 低价"打 Agent 市场,智谱靠 10 万张国产芯片压成本,DeepSeek 靠架构（非对称激活 + KV Cache 压缩 437×）压成本。

## 资源

- 官方公告（中文）：https://api-docs.deepseek.com/zh-cn/news/news260910
- 官方公告（英文）：https://api-docs.deepseek.com/news/news260910
- 更新日志：https://api-docs.deepseek.com/updates
- 定价页：https://api-docs.deepseek.com/quick_start/pricing
- 模型权重：https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash
- 技术报告：https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/main/DeepSeek_V41_Tech_Report.pdf
