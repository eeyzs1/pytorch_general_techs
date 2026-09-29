# GLM-5.3-FlashX 发布:推理速度最高 200 tokens/s,定价为 Flash 的 2.5 倍(GLM-5.3-FlashX Release)

- **原文链接**: [智谱发布GLM-5.3-FlashX:推理速度最高200 tokens/s](https://stcn.com/article/detail/4190490.html)
- **作者**: 证券时报
- **发布日期**: 2026-09-18
- **检索日期**: 2026-09-29
- **标签**: #GLM-5.3-FlashX #智谱 #推理加速 #API定价 #国产芯片 #MaaS

## 核心观点

9 月 18 日,智谱发布 GLM-5.3-FlashX(API 模型代码 glm-5.3-flashx):推理速度最高 200 tokens/s,较 GLM-5.3-Flash 提速 5 倍,是 GLM-5 系列迄今最快的推理版本;定价为 Flash 的 2.5 倍,延续年内"性能升、价格升"的阶梯策略。

FlashX 与 Flash 同底座:320B 总参 / A18B 激活、稀疏 + 线性注意力混合架构、原生多模态、1M 上下文 / 128K 输出——提速来自推理系统工程优化而非重训模型。背景是 Ox-Alpha 走红后 10 万张国产芯片集群上线即打满,FlashX 以更高定价承接时延敏感的溢出需求。

中报数据为"供不应求→提价"提供财务佐证:MaaS 调用量较年初 +40 倍、平台用户突破 740 万、API 定价同比 +101%、毛利率 24.6%。

## 关键发现 / 关键技术

### 1. 速度与定价:5 倍提速、2.5 倍定价
- 推理速度最高 200 tokens/s,较 GLM-5.3-Flash 提升 5 倍,面向高并发、低时延的 Agent 与实时编码场景
- 定价为 GLM-5.3-Flash 的 2.5 倍:以速度而非能力分档,形成"Flash(低价多模态)→ FlashX(极速)→ GLM-5.3(旗舰)"三层产品线
- 提速 5 倍的底层支撑是 Infra Agent 对 10 万卡国产集群自建推理系统的优化,详见 [RSI 首个工程化实践:Infra Agent](glm-rsi-infra-agent.md)

### 2. 同底座规格:换的是推理栈,不是模型
- 320B 总参数 / A18B 激活的 MoE 配置,与 GLM-5.3-Flash 完全一致
- 稀疏注意力 + 线性注意力混合架构;原生多模态,输入支持文本 / 图像 / 视频
- 100 万 token 上下文窗口、最大输出 128K;API 模型代码 glm-5.3-flashx
- 能力定位延续 Flash:代码生成 / 理解 / 修复为主战场,多模态与长文档场景同规格

### 3. 供需背景:Ox-Alpha 走红、集群上线即打满
- GLM-5.3-Flash 以 Ox-Alpha 匿名身份登顶 OpenRouter / OpenCode 后调用量激增(6 天 62 万亿 token)
- 10 万张国产芯片集群上线即打满,FlashX 定位承接溢出需求,用价格杠杆为最紧急的高速推理负载分流
- FlashX 与 Flash 并存销售而非替代:低价档保留获客与生态规模,高速档变现时延敏感负载
- 定价上调与年内 Coding Plan 因算力耗尽停售-恢复互为印证:供给约束是贯穿 2026 年的主线(见 [智谱 50 亿美元再融资](zhipu-5b-refinancing-arr-guidance.md))

### 4. 涨价序列与商业化数据
- 2026 年定价序列:2 月 GLM-5 上调 → 3 月 GLM-5-Turbo +20% → 4 月 GLM-5.1 +10%
- 9 月 FlashX 定为 Flash 的 2.5 倍,"性能升价格升"贯穿全年,且首次以"速度"而非"代际升级"作为提价理由
- 中报佐证:MaaS 调用量较年初 +40 倍、平台用户突破 740 万、API 定价同比 +101%、毛利率 24.6%

## 实践意义

FlashX 表明推理速度正在成为与模型能力并列的定价维度:同一底座靠推理系统工程(调度、内核、服务框架)拉开 5 倍差距,"模型相同、体验不同"将成为 MaaS 常态。

对开发者,高吞吐 Agent 与编码流水线有了明确的高速档,选型时需把 tokens/s 纳入与效果同级的成本公式;对行业,供不应求下的连续提价说明头部国产模型厂商已从"低价换规模"转入"性能定价"阶段,推理基建能力(而非仅模型能力)开始直接体现在价格表上。

## 跨厂商对比

- 与 [GLM-5.3-Flash](glm-5-3-flash.md) 对比:Flash 主打"低价多模态普惠"(限时折扣价曾为 GLM-5.3 的 1/20),FlashX 主打"极速",同底座 5 倍速度差与 2.5 倍价差构成清晰的性能-价格阶梯
- 与 [GLM-5.3](glm-5-3.md) 对比:旗舰 GLM-5.3(743B)以能力取胜,FlashX 以速度取胜,智谱产品线就此完成"能力-成本-速度"三维细分
- 与 [DeepSeek-V4-Pro GA 与 API 调价](../../deepseek/news/deepseek-api-price-adjustment-2026-08.md) 对比:DeepSeek 以峰谷分时计费(部分模型涨幅最高 1100%)平衡算力供需,智谱以"速度分层 + 2.5 倍定价"承接溢出需求,两家先后走出"价格战→商业化平衡"的同构转折
- 与 [GLM Coding Plan 定价修订](glm-coding-plan-pricing-revision.md) 对比:Coding Plan 的订阅定价调整与 FlashX 的按量 2.5 倍定价互为镜像——同一供给约束下,订阅制控量、按量制提价

## 资源

- 官方文档:[GLM-5.3-Flash / FlashX 模型文档](https://docs.bigmodel.cn/cn/guide/models/vlm/glm-5.3-flash)
- 媒体报道:https://stcn.com/article/detail/4190490.html
- 背景阅读:[RSI 首个工程化实践:Infra Agent](glm-rsi-infra-agent.md)(提速 5 倍的系统层来源)

> 注:智谱官方渠道(bigmodel.cn/公众号)无法直接抓取,本文基于证券时报/上海证券报/TechWeb/IT之家等报道交叉验证,官方文档链接见资源。
