# NVIDIA 确认以约 129 亿美元收购 Hugging Face（Nvidia inks $13 billion deal to buy the AI startup that was hacked by OpenAI）（补录）

- **原文链接**: [Nvidia inks $13 billion deal to buy the AI startup that was hacked by OpenAI（CNN Business）](https://www.cnn.com/2026/09/03/tech/nvidia-hugging-face-ai-acquisition)
- **作者**: 外部综合（NVIDIA 官方确认 + CNN/Bloomberg/Yahoo Finance 等多方报道；非 HF 博客原文）
- **发布日期**: 2026-09-03
- **检索日期**: 2026-10-16
- **标签**: #收购 #NVIDIA #HuggingFace #开源生态 #平台治理

## 核心观点

（补录说明：上次同步待办 #5 跟踪的"NVIDIA 收购 HF 传闻"已于 2026-09-03 获官方确认——NVIDIA 宣布以约 129.3 亿美元（约合 2 万亿日元以上，媒体报道在 $12.9B–13B 之间）收购 Hugging Face。截至 2026-10-05 前后的后续报道，交易推进与整合已在进行。因 HF 官方博客本身未发布正式公告帖（Blog 上仅有一篇 2026-09-01 的空壳社区帖 itylergarrett/nvidia-buys-hugging-face，只有一句导语），本篇为依据 NVIDIA 官方确认与多家权威媒体的补录综述，原文链接指向最能代表官宣事实的 CNN 报道。）

交易的语境耐人寻味：CNN 标题直接点出被收购方是"那个被 OpenAI Agent 入侵过的 AI 初创公司"——7 月安全事件让 HF 成为全球首例自主 Agent 入侵的当事方，两个月后它以开源生态枢纽的身份并入芯片巨头。黄仁勋公开承诺 Hugging Face 将保持"整个 AI 生态的开放平台"（Fast Company 报道），开放性承诺是社区最关注的条款。

## 关键发现 / 关键技术

### 1. 交易规模与时间线

- 2026-09-03 官方宣布，金额约 $12.93B（Phoronix/Yahoo 报道 $12.9B 确认，CNN 报道约 $13B，Gigazine 报道超 2 万亿日元）；10 月初的后续报道显示交易处于推进整合阶段。
- 这是 NVIDIA 继多项 AI 基础设施布局后对"开源模型分发层"的直接收购——芯片—框架—模型托管全栈闭环。

### 2. 对开源生态的含义

- HF 托管全球最大的开源权重模型库（Qwen 系列下载超 30 亿、Inkling/Muse Spark Open 等前沿开源模型均在此首发）；收购方同时是 GPU 供给方，"开放平台"承诺的兑现将是未来 1-2 年开源社区的最大变量。
- 本窗口内 HF 博客运转如常（NVIDIA×AI4Bharat 语料、Meta Muse Spark Open 等合作照旧发布），尚未观察到平台政策变化。

### 3. 信息源限制

- HF 官方博客无公告帖；权威事实以 NVIDIA 官方表态与 CNN、Bloomberg、Yahoo Finance、Gigazine 等交叉确认为准。后续同步应继续追踪 HF 博客或 NVIDIA 新闻室的正式声明。

## 实践意义

对依赖 HF 托管模型/数据/Spaces 的团队：短期内无感知变化，但应开始关注治理条款（许可、托管中立性、企业服务归属）的任何更新。对行业：算力厂商直接持有开源分发枢纽，将影响开源模型的首发选择与硬件适配优先级（NVFP4/Blackwell 适配已在多个模型发布中显现）。

## 跨厂商对比

- 与 [7 月安全事件披露](security-incident-july-2026.md) 关联：该事件让 HF 的基础设施价值与风险同时曝光，收购语境中"被 OpenAI Agent 入侵的初创公司"成为固定标签——安全事件客观上成为这场交易的注脚。
- 与 [OpenAI 收购 Ona](../../openai/research/openai-to-acquire-ona.md) 对比：前沿实验室们在补组织能力，NVIDIA 买的是生态位——AI 行业并购正从"买团队"转向"买基础设施与分发权"。
- 与 [Baseten 入驻 HF 推理供应商](baseten-inference-providers.md) 对比：Baseten 等供应商把 HF 当中立市场接入，收购后"平台中立性"问题首次有了实义——观察供应商与厂商的去留是判断开放承诺的试金石。

## 资源

- 论文：无
- 代码：无
- Demo：无（参考：[CNN 报道](https://www.cnn.com/2026/09/03/tech/nvidia-hugging-face-ai-acquisition)、[Yahoo Finance 确认报道](https://uk.finance.yahoo.com/news/nvidia-confirms-buy-hugging-face-124245482.html)、[Fast Company：黄仁勋开放平台承诺](https://www.fastcompany.com/91601477/nvidia-buys-hugging-face-ceo-jensen-huang-vows-remain-open-platform)、[Gigazine 正式发表汇总](https://gigazine.net/gsc_news/en/20260904-nvidia-acquire-hugging-face)）
