# Meta AI — 核心观点总结

> 汇总 Meta AI 近期重大动态，9 篇文章，涵盖 2025 年 4 月至 2026 年 8 月。

## 一、总体脉络

Meta AI 在 2025-2026 年经历了剧烈的战略转变：

```
Llama 4 发布 → 刷榜丑闻 → 组织重组 → 闭源转向 → Muse Spark → Brain2Qwerty v2 → SAM 3.1 → Muse Image / Spark 1.1 → Meta AI Agent 化 → Muse Code 编码 Agent
```

从开源旗手到闭源转向，从 Llama 品牌危机到 MSL 重建，Meta 用一年时间完成了 AI 战略的彻底重构。2026 年 6 月底，Meta 又发布 [Brain2Qwerty v2](brain2qwerty-v2.md)——非侵入式脑机接口的端到端 LLM 解码 pipeline，在 Nature Neuroscience 发表并开源全部训练代码与数据集，标志 Meta 在"AI + 神经科学"方向继续深入，与主流 LLM 产品形成"产品 + 科学"双轨。7 月 MSL 进入收获期：[Muse Image](muse-image.md) 图像生成进入 Instagram/WhatsApp 社交生态，[Muse Spark 1.1](muse-spark-1-1.md) 升级"主-子 Agent 编排"并开启 Meta Model API 公测（Meta 首次直接售卖旗舰模型调用），[Meta AI 获得 Agent 化能力](meta-ai-muse-spark-doesnt-just-think-it-acts.md)——定时任务、邮件日历连接、可引导深度研究，官方称"迈向个人超级智能的下一步"。开源侧 [SAM 3.1](sam-3-1.md) 用 Object Multiplex 把 128 目标视频分割推理提速约 7 倍，开源视觉基础模型竞争从精度转向部署效率。8 月 5 日 MSL 发布 [Muse Code](introducing-muse-code-muse-spark-1-2.md)——Meta 首个终端编码 Agent，由新模型 Muse Spark 1.2 驱动，正式加入由 Anthropic（Claude Code）与 OpenAI（Codex）主导的编码 Agent 赛道，差异化在于"模型与 harness 协同训练"和持久化后台 Agent + append-only 事件日志。

## 二、核心事件

### 1. Llama 4 刷榜丑闻

[Llama 4 Benchmark Scandal](llama-4-controversy.md) 是 2025-2026 年 AI 行业最大的信任危机。Meta 为不同基准测试使用了不同版本的模型，将每个测试的最佳分数拼凑成一张"统一"表格。2026 年 1 月，Yann LeCun 向 Financial Times 确认"结果被稍微篡改"。后果：LMSys Arena 排名从第 2 跌至第 32，Llama 品牌信誉永久受损，4 次组织重组。

### 2. Behemoth 搁置

[Llama 4 Behemoth](llama-4-behemoth-cancelled.md) 是 ~2T 参数 MoE 旗舰模型，定位为"教师模型"。2025 年 4 月公布后经历一年延迟，2026 年 5 月被确认搁置。成为"纯规模路线的失败案例研究"。

### 3. Muse Spark 闭源转向

[Muse Spark](muse-spark.md) 是 Meta Superintelligence Labs 的首个模型，2026 年 4 月发布。关键转变：
- **闭源**：不再开放权重，直接部署到 Meta 产品
- **新架构**：不是 Llama 5，而是从零重建
- **新领导**：前 Scale AI CEO Alexandr Wang 领导 MSL
- **高效**：比 Llama 4 Maverick 高 10 倍计算效率
- **分发**：覆盖 30 亿日活用户（Meta AI, WhatsApp, Instagram, Facebook, Messenger, Ray-Ban）

### 4. Brain2Qwerty v2 非侵入式脑机接口

[Brain2Qwerty v2](brain2qwerty-v2.md)（2026-06-29）是 Meta 在"AI + 神经科学"方向的旗舰研究：
- **端到端深度学习** 直接从 MEG 原始信号解码句子，跳过手工特征工程
- 用 **LLM 微调** 弥合噪声脑信号与连贯语言的语义鸿沟
- 9 名志愿者、22,000 句子训练，**词准确率 61%**（最佳 78%），相比其他非侵入方法 8% 提升 7.5 倍
- 在 **Nature Neuroscience** 发表，开源 v1+v2 训练代码 + v1 数据集
- 配套 [Tribev2](https://ai.meta.com/blog/tribe-v2-brain-predictive-foundation-model/)、NeuralSet、NeuralBench 形成"开放脑模型基础设施"
- **Meta 差异化**：与 Google DeepMind Co-Scientist/AlphaEvolve、Anthropic Claude Chemist、OpenAI GeneBench-Pro 等共同构成 2026 年的"AI for Science"竞争格局

### 5. SAM 3.1：开源视觉模型的效率转向

[SAM 3.1](sam-3-1.md)（2026-03-27）是 SAM 3 的 drop-in 效率升级，核心是 Object Multiplex——共享内存的联合多目标跟踪，把对象分桶联合处理消除逐对象重复计算。单块 H100 处理 128 个对象时推理提速约 7 倍且不牺牲精度（图像精度与 SAM 3 持平），中等目标数视频吞吐从 16 FPS 翻倍至 32 FPS。Meta 明确定位"让高性能分割跑在更小、更易得的硬件上"——开源视觉基础模型的竞争从精度转向部署效率。

### 6. Muse Image：图像生成进入社交生态

[Muse Image](muse-image.md)（2026-07-07）是 MSL 首个图像生成模型，首发即嵌入 Meta AI、Instagram、WhatsApp，并计划接入广告创意工具——图像生成直接对接 Meta 广告变现飞轮。最具平台特色也最争议的功能：可基于好友或创作者的公开 Instagram 帖子生成含其形象的图片（可 opt-out）；所有生成图片带隐形水印。这是 MSL 继 Muse Spark 后的第二个产品线，视频生成模型数月内待发。

### 7. Muse Spark 1.1 与 Meta Model API 公测

[Muse Spark 1.1](muse-spark-1-1.md)（2026-07-09）是面向 Agent 任务的多模态推理模型重大升级，被训练为"主 Agent"：收集上下文、制定计划、把子任务分派给并行子 Agent；务实的 Computer Use（写脚本更快就写脚本、点 GUI 更省事就点界面）；100 万 token 上下文 + 主动管理。同步开启 **Meta Model API 公测**——Meta 首次向开发者直接售卖旗舰模型调用（输入 $1.25 / 输出 $4.25 每百万 token），从"产品内置"走向"平台售卖"，目标对标 Claude 与 GPT 旗舰。

### 8. Meta AI Agent 化：个人超级智能的下一步

[Meta AI Doesn't Just Think, It Acts](meta-ai-muse-spark-doesnt-just-think-it-acts.md)（2026-07-24）宣布 Muse Spark 1.1 驱动的 Meta AI 获得代理化能力：制定计划、连接邮件与日历、可引导的深度研究（实时纠偏）、一键生成幻灯片，以及**定时任务**——每日简报、每周饮食计划、球鞋上新提醒"只需设置一次"即可自动运行，AI 开始拥有"时间"维度。功能 7 月 24 日起在部分市场上线，数周内扩展至更多国家和 WhatsApp。

### 9. Muse Code：Meta 首个终端编码 Agent

[Muse Code 与 Muse Spark 1.2](introducing-muse-code-muse-spark-1-2.md)（2026-08-05）是 MSL 正式进入编码 Agent 赛道的标志。Muse Code 是运行于终端的 AI 编码 Agent，由新模型 Muse Spark 1.2 驱动，面向大型代码仓库的复杂软件工程任务。两大核心设计：**持久化异步后台 Agent**（整个会话期间持续运行，大任务可拆分为多个子 Agent 在独立 git worktree 中并行工作）和**本地 append-only 事件日志**（记录每次模型调用、工具运行、审批与编辑，可精确重放且崩溃后可恢复，使 24 小时、1000+ 次工具调用的长时程任务能存活于故障）。Muse Spark 1.2 与 Muse Code 协同训练——引入拒绝采样的 Agent 轨迹、目标执行/上下文压缩/子 Agent 配方优化，并将 Muse Code 工具集纳入训练。内置三个默认技能：`/plan`（生成需审批的计划）、`/grill`（对计划反复压力测试）、`/goal`（围绕目标持续推进直至完成）。Terminal-Bench 2.1 得分 82.9%（第二，仅次于 Claude Code on Opus 5 的 86.7%，高于 Codex on GPT-5.6 Terra 的 81.8%），DeepSWE 1.1 得 59.3%（第三），Meta 内部 Coding Bench 70.6%（低于 Claude Opus 5 的 79.4%）。模型未开放权重，通过 Meta Model API 提供，定价与 Spark 1.1 一致（输入 $1.25/输出 $4.25 每百万 token）。Meta 自评在长时程与内部基准上仍落后于 Claude Opus 5，说明编码 Agent 的前沿仍在别处。

## 三、关键数据点

| 指标 | 数值 | 来源 |
|------|------|------|
| Llama 4 Maverick LMSys Arena 排名变化 | #2 → #32 | Llama 4 Controversy |
| Llama 4 Behemoth 参数 | ~2T | Behemoth |
| Muse Spark CharXiv | 86.4 (#1) | Muse Spark |
| Muse Spark HealthBench Hard | 42.8 (#1) | Muse Spark |
| Muse Spark 计算效率提升 | 10x vs Llama 4 | Muse Spark |
| Muse Spark 上下文窗口 | 262K | Muse Spark |
| Meta 组织重组（6 个月） | 4 次 | Llama 4 Controversy |
| Brain2Qwerty v2 词准确率 | 61%（最佳 78%） | Brain2Qwerty v2 |
| Brain2Qwerty v2 vs 其他非侵入方法 | 7.5×（61% vs 8%） | Brain2Qwerty v2 |
| Brain2Qwerty v2 训练句子数 | 22,000 | Brain2Qwerty v2 |
| Brain2Qwerty v2 志愿者数 | 9 | Brain2Qwerty v2 |
| SAM 3.1 128 目标推理提速（单 H100） | 约 7× | SAM 3.1 |
| SAM 3.1 中等目标视频吞吐 | 16 → 32 FPS | SAM 3.1 |
| SAM 3.1 单次前向联合跟踪对象上限 | 16 | SAM 3.1 |
| Muse Spark 1.1 API 定价（输入/输出） | $1.25 / $4.25 每百万 token | Muse Spark 1.1 |
| Muse Spark 1.1 上下文窗口 | 100 万 token | Muse Spark 1.1 |
| Muse Image 首发分发渠道 | Meta AI + Instagram + WhatsApp | Muse Image |
| Muse Spark 1.2 Terminal-Bench 2.1 | 82.9%（第二，仅次于 Opus 5 的 86.7%） | Muse Code |
| Muse Spark 1.2 DeepSWE 1.1 | 59.3%（第三） | Muse Code |
| Muse Spark 1.2 Meta Internal Coding Bench | 70.6%（Opus 5 为 79.4%） | Muse Code |
| Muse Code 定价（输入/输出） | $1.25 / $4.25 每百万 token（与 Spark 1.1 一致） | Muse Code |

## 四、关键洞察

1. **开源不等于可信**：Llama 4 丑闻暴露了开源模型基准测试的信任危机
2. **闭源转向是生存策略**：Meta 意识到开源无法在性能上追上 OpenAI/Google，转向闭源 + 分发优势
3. **30 亿用户是终极壁垒**：即使模型性能略逊，分发优势无人能敌
4. **纯规模路线失败**：Behemoth 的搁置证明"堆参数"不再是有效策略
5. **组织动荡是 AI 竞赛的常态**：4 次重组、LeCun 离职、Wang 入主——Meta 在动荡中寻找方向
6. **从产品内置到平台售卖**：Meta Model API 公测标志 Meta 加入开发者平台竞争，闭源模型成为直接收入来源
7. **Agent 化的杀手锏是"时间"维度**：定时任务 + 邮件日历连接让 Meta AI 从应答工具变为持续运行的个人代理
8. **开源侧转向部署效率**：SAM 3.1 不卷精度卷效率——开源基础模型的差异化正在从"最强"转向"最能跑"

## 五、文章索引

| # | 日期 | 文章 | 主题 |
|---|------|------|------|
| 1 | 2025-04 ~ 2026-01 | [Llama 4 Benchmark Scandal](llama-4-controversy.md) | 信任危机 |
| 2 | 2025-04 ~ 2026-05 | [Llama 4 Behemoth Cancelled](llama-4-behemoth-cancelled.md) | 旗舰搁置 |
| 3 | 2026-04-08 | [Muse Spark](muse-spark.md) | 闭源转向 |
| 4 | 2026-06-29 | [Brain2Qwerty v2](brain2qwerty-v2.md) | 脑机接口 / AI for Science |
| 5 | 2026-03-27 | [SAM 3.1](sam-3-1.md) | 视频分割 / 效率升级 / 开源 |
| 6 | 2026-07-07 | [Muse Image](muse-image.md) | 图像生成 / 社交生态 |
| 7 | 2026-07-09 | [Muse Spark 1.1 and the Meta Model API](muse-spark-1-1.md) | Agent 模型 / API 公测 |
| 8 | 2026-07-24 | [Meta AI Doesn't Just Think, It Acts](meta-ai-muse-spark-doesnt-just-think-it-acts.md) | Agent 化 / 定时任务 / 个人超级智能 |
| 9 | 2026-08-05 | [Introducing Muse Code and Muse Spark 1.2](introducing-muse-code-muse-spark-1-2.md) | 编码 Agent / 终端工具 / 协同训练 |