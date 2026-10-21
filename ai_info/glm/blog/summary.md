# GLM (智谱 AI) — 核心观点总结

> 汇总自 [智谱大模型开放平台](https://www.bigmodel.cn/)、[zhipuai.cn/zh/research 官方研究列表](https://www.zhipuai.cn/zh/research/) 及权威媒体报道，当前覆盖 2025 年 12 月至 2026 年 10 月，共 28 篇。

## 一、总体脉络

智谱 AI（Zhipu AI）是中国领先的大模型公司，GLM（General Language Model）系列是其核心产品。与 OpenAI、Anthropic 等美国厂商不同，智谱采用"开源 + 商业化"双轨策略，同时提供 API 服务和开源模型。GLM 系列基于自回归填空预训练，支持复杂自然语言指令和困难推理问题。

## 二、核心主题

### 1. GLM 模型系列

GLM 是智谱的核心大模型系列，包括：
- **ChatGLM**：对话模型，支持多轮对话、内容创作、信息归纳
- **GLM-4**：第四代模型，开源多语言多模态对话模型
- **GLM-4V**：视觉理解版本
- **GLM-4.1V**：最新视觉模型更新（2025-07-04）
- **GLM-5.2**：2026 年 6 月 16 日上线的新一代旗舰（详见下文专题）

### 2. GLM-5.2：1M 无损上下文与长程任务开源 SOTA

[GLM-5.2](glm-5-2.md)（2026-06-16）是智谱新一代旗舰模型，核心卖点是 **1M 无损上下文与长程任务能力**——显著减少复杂任务中的上下文漂移与目标遗忘，Coding 与长程任务评测达开源 SOTA。关键事实：

- **参数效率优先**：约 7400 亿参数，仅为 Kimi K3（2.8T）的约 1/4，依靠后训练能力以小参数对标国际顶级闭源模型的编程性能，是首个在 AI 编程能力上追上 Claude Opus 级别的国产模型
- **长程任务定位**：总裁王绍兰明确"让模型自主且长时间地运行一个任务，实现端到端交付"（如新药研发中几十个智能体联合行动找靶点）
- **开源 + 商业化双轮**：宣布开放部分模型权重，上线 BigModel 平台与 GLM Coding Plan（订阅制），兼容 Claude Code、VS Code 等主流编码工具
- **迭代节奏**：保持约两个月一版（GLM-5.1 于 4 月发布，8 小时连续工作、对齐 Claude Opus 4.6）；2026 年一季度全球调用量增长 400%，平台注册企业及用户突破 600 万

### 3. 平台能力

智谱大模型开放平台提供：
- **模型调用**：文本、视觉、图像、视频、音频模型 API
- **模型部署**：专属资源上的模型实例部署
- **模型微调**：自有数据创建微调任务
- **模型评测**：基于数据集和指标评估模型效果
- **联网搜索**：网页检索、问答增强、搜索智能体
- **知识库检索**：文档、网页、结构化数据的问答和检索增强

### 4. 开源策略

GLM-4 系列在 GitHub 开源（Apache-2.0 许可证），包括：
- 多语言多模态对话模型
- 6.7k stars，568 forks
- 最新更新：GLM-4.1V（2025-07-04）

### 5. GLM Coding Plan 套餐改版

[GLM Coding Plan 套餐改版](glm-coding-plan-pricing-revision.md)（2026-07-30）是 GLM 编码订阅体系的首次重大计费改版，核心变化是从 prompt 计数转向以 token 消耗为基础的积分制，以提升额度计算的透明度与可预期性。引入峰谷定价机制：GLM-5.2/GLM-5-Turbo 作为高阶模型在高峰时段（每周一至周五 14:00-18:00 UTC+8）消耗 3 倍积分，非高峰期 1 倍；GLM-4.7 全天按 1 倍消耗；周末全天按非高峰时段抵扣。老用户权益完全不受影响——V1 老用户到期前可按 V2 版价格订阅，V2 个人套餐与团队套餐用户价格/权益/额度/计算方式均不变，团队套餐各席位额度同步上调 30%。新用户与到期用户需订阅新版积分套餐，价格显著上调。这标志着国产编码订阅服务从"次数计费"向"token 计费"对齐行业惯例，峰谷定价与 DeepSeek 的做法趋同，说明国内厂商在算力调度策略上正在收敛。

### 6. GLM-5.3：前沿编程与涌现的网络安全能力

[GLM-5.3](glm-5-3.md)（2026-08-19）是智谱新一代基座模型，743B 参数（约为 Kimi K3 的 1/4），AA 综合智能指数 60 分并列开源第一，编程能力较前代提升约 50%，并涌现出防御性网络安全能力。官方以"新版本能力过强，暂缓开源"为由不立即开放权重（预告下周五开源），API 即日上线且价格不变。GLM-5.3 标志智谱从"模型发布"转向"能力 + 安全 + 商业化"并重，其"暂缓开源"的发布节奏控制与 Anthropic 的"宽分类器启动 + 精化迭代"形成有趣对照——两家都在处理"前沿能力与安全"的平衡。

### 7. GLM-5.3-Flash：开源多模态经济版与"匿名公测"发布范式

[GLM-5.3-Flash](glm-5-3-flash.md)（2026-08-26 上线并开源，媒体稿 08-27）是 GLM-5 系列首个原生多模态模型：320B 总参 / A18B 激活、文本/图像/视频输入、100 万 token 上下文。发布前以匿名 "Ox Alpha" 身份在 OpenRouter 与 OpenCode 登顶并刷新双平台历史纪录（Token 调用量 62T），揭晓后使用量超 DeepSeek 一倍以上；AA 综合智能指数 57 分进入前沿区间，限时折扣价为 GLM-5.3 的 1/20。全部线上流量由 10 万张国产芯片承载——国产算力栈首次在超大规模真实流量下得到验证。"匿名公测 → 揭晓"成为规避品牌偏见、以真实用量验证能力的新发布范式。

### 8. "Flash × ZCode" 夜间畅用：峰谷计费的强化版

[GLM Coding Plan "Flash × ZCode" 夜间畅用](glm-flash-zcode-night-free.md)（活动 2026-09-03 至 09-20）在每晚 23:00–次日 9:00（UTC+8 含周末）对 GLM-5.3-Flash 实行"经官方工具 ZCode 额度消耗为 0、经其他 Agent 额度 ×2"的双轨梯度——把 7 月改版引入的峰谷积分制进一步强化为"错峰填谷 + 自有渠道导流"的运营工具，与 DeepSeek 的峰谷计费（低峰半价）形成国产厂商共同的需求侧调度策略。

### 9. 半年度业绩与 GLM-6.0 方向

[智谱 2026 半年度业绩会](zhipu-h1-2026-earnings-glm-6.md)（2026-09-03，媒体披露）给出国产大模型罕见的经营透明度：上半年营收 9.54 亿元（+399.7%）、API 业务占 86.5%（8.25 亿，+2735.7%）、亏损 20.72 亿收窄。技术上确认 GLM-5.x 全系共用 1 月完成的约 745B 基座、靠后训练迭代（5.3 与 5.2 同架构同参数，后训练差异带来端到端完成率 +50%）——与 DeepSeek V4-Flash-0731"架构不变仅重新后训练"互为印证；GLM-6.0 方向为更大有效规模、更长原生上下文、原生多模态统一建模与"自进化"。10 万级国产芯片规模化推理下单位 token 成本较年初降 80%。

### 10. GLM-5 时代：从开源旗舰到 8 小时长程模型（2026 年 2-4 月，历史补录）

[GLM-5 开源](glm-5-open-source.md)（02-11）确立"Agentic Engineering"叙事：744B 总参/40B 激活、28.5T tokens，SWE-bench Verified 77.8 与 Terminal-Bench 2.0 56.2 开源 SOTA，适配昇腾等七大国产算力，发布前以 Pony Alpha 匿名盲测（25% 用户误猜 Claude Sonnet 5）。[GLM-5 技术报告](glm-5-technical-report.md)（02-21，arXiv:2602.15763）首次集成 DeepSeek Sparse Attention（继续预训练 20B token 适配，长序列注意力计算降 1.5-2 倍）、Slime 异步 RL 框架、跨阶段在线蒸馏与 INT4 QAT。[GLM-5-Turbo](glm-5-turbo.md)（03-15）面向 OpenClaw"龙虾"场景，发布 ZClawBench 端到端基准，Skills 使用比例 26%→45%。[GLM-5V-Turbo](glm-5v-turbo.md)（04-01）是多模态 Coding 基座：设计稿/截图/网页直接生成可运行代码，自研 CogViT 编码器 + 30+ 任务协同 RL。[GLM-5.1](glm-5-1.md)（04-07）开源并刷新 SWE-bench Pro 全球最佳（超 GPT-5.4 与 Opus 4.6），METR 口径下唯一 8 小时级持续工作的开源模型；8 小时 1200+ 步从零构建 Linux 桌面、655 轮迭代把向量库查询推到 6.9 倍 QPS。

### 11. 专业小模型矩阵：OCR / 语音 / 图像（2025-12 至 2026-02，历史补录）

[GLM-OCR](glm-ocr.md)（02-02）：0.9B 参数登顶 OmniDocBench V1.5（94.6 分），复杂表格直接输出 HTML，0.2 元/百万 tokens 约为传统方案 1/10。[GLM-TTS](glm-tts.md)（2025-12-10）：10 万小时数据训练即具备 3 秒音色复刻，GRPO 四奖励（CER/相似度/情感/笑声）分层正则化，seed-tts-eval 中文 CER 0.89% 开源 SOTA。[GLM-ASR-Nano](glm-asr-nano.md)（2025-12-09）：1.5B 高鲁棒 ASR，开源模型最低平均错误率 4.10（Whisper V3 为 6.93），方言/耳语音量/嘈杂环境专攻；"智谱 AI 输入法"为其首个生产部署。[GLM-Image](glm-image-huawei.md)（2026-01-13）与华为联合开源：昇腾 + 昇思全流程训练的 SOTA 文字渲染图像模型（LongText-Bench 中文 0.979），"自回归 9B + 7B DiT 扩散 + Glyph Encoder"混合架构，API 0.1 元/图。[GLM-4.7-Flash](glm-4-7-flash.md)（01-19）：30B/3B 激活免费开源，同尺寸开源 SOTA，替代 4.5-Flash。

### 12. 推理基础设施：ZCube 组网与 Scaling Pain（历史补录）

[ZCube](glm-zcube.md)（05-20，SIGCOMM 2025 论文落地）：针对 PD 分离下 KV Cache 传输的源-目的不对称，取消 Spine 层、Leaf 奇偶两组完全二部图互联（直径 2 跳）；千卡生产集群实测交换机与光模块 capex -33%（万卡省 2.1-6.4 亿元）、GPU 平均推理吞吐 +15%、TTFT P99 -40.6%。[Scaling Pain](glm-scaling-pain.md)（04-29）：日均数亿次 Coding Agent 调用下的异常治理——用投机采样指标（spec_accept_length/accept_rate）做在线异常检测，修复 PD 分离异步 Abort 的 KV Cache 复用竞态（异常率万分之十几→万分之三以下）与 HiCache read-before-ready（SGLang PR #22811），LayerSplit 分层存储命中 90% 时长文本吞吐 +10%-132%。

### 13. 9 月中下旬：FlashX、RSI 工程化、再融资与 ZCode 事件

[GLM-5.3-FlashX](glm-5-3-flashx.md)（09-18）：推理最高 200 tokens/s（较 Flash 提速 5 倍），定价为 Flash 的 2.5 倍——Ox-Alpha 走红后 10 万张国产芯片上线即打满，FlashX 承接溢出需求，"性能升、价格升"策略延续（年内第四次调价）。[RSI Infra Agent](glm-rsi-infra-agent.md)（09-17）：GLM-5.3 驱动的 Infra Agent 在 10 万+ 张国产芯片集群从零搭建调试推理服务，不到两周整体处理速度提升至 3 倍、单 token 成本接近英伟达生态水平——国内首次公开"AI 自我改进"用于生产，是 FlashX 提速与 GLM-6"自进化"路线的工程前奏。[50 亿美元再融资](zhipu-5b-refinancing-arr-guidance.md)（09-16）："小股大债"全部投算力扩容，全业务 ARR 达 18 亿美元、年末指引由 24 亿上调至 30 亿美元，海外云托管 API 分成收入 10 月起确认。[ZCode 代码上传争议](glm-zcode-data-upload-incident.md)（09-18 起，09-28 收尾）：开发者发现 ZCode 默认"代码库索引"中 Repo Wiki 功能触发 313MB 工作区与 Git 历史上传（海外报道 564 次尝试）；智谱经历"致歉→v3.14.0 移除上传链路→Apache-2.0 开源 ZCode→信通院与绿盟双审计确认云端零数据→'你不发起，不上云'承诺+10 万份 1 亿 token 补偿"的完整应对链，股价三日累跌逾 16%——AI 编程工具"功能便利 vs 数据主权"的标志性案例。

### 14. 10 月上中旬：网安第三方背书、海外分发开局与 ZCode 深度复盘

[Anthropic 报告评估 GLM-5.3 网络安全能力](glm-5-3-anthropic-cyber-report.md)（09-30，报告 09-29）：ExploitBench 端到端漏洞利用 50/410，与 Claude Mythos Preview（56 次）接近；同时批评简单技术可在 64%-100% 情况下绕过 GLM-5.3 防护——竞对官方报告首次系统评估中国开源前沿模型，能力背书与防护批评同框，并印证 GLM-5.3 权重已按预告于发布两周后开放。[ZCode 争议后续：媒体深度复盘](zcode-followup.md)（10-02，澎湃豹变）：补偿方案（付费用户 4 张周额度重置卡 + 4 张 5 小时卡、9-28 至 10-7 全员每日限量 Token）之后承认"信任不能一键重置"；补齐服务端持钥加密、全量 Git 历史打包、用户协议自相矛盾等工程细节，并以 xAI Grok Build / Claude Code / DeepSeek GDPR / OpenAI 2023 泄露横向对照 + 新《网络安全法》与"清朗"专项背景，将个案定性为行业级信任问题。[Cursor 上线 GLM-5.3](glm-5-3-cursor-cursorbench.md)（10-05）：CursorBench 4.0 开放权重模型最高分 42.6%（Max 推理设置），德国主权 AI Aleph Alpha 新模型 Kolibri 披露使用 GLM——完成"匿名验证→第三方基准→主流工具分发"三级跳。[GLM-5.3 接入 Amazon Bedrock](glm-5-3-amazon-bedrock.md)（10-06）：AWS 按模型调用量与智谱收入分成，9 月预告的"海外分成收入 10 月起确认"如期兑现；阿里云百炼已签类似协议、华为云已上架 GLM-5.3——云分发成为 ARR 第二曲线且不占用自有算力。[古河加盟智谱](zhipu-guhe-cyber-talent.md)（10-15）：MSRC 榜首、两获 Pwnie Awards 的顶级白帽古河（Yuki Chen）进入 GLM 基础模型组专攻 cyber 能力，其团队已用 GLM 挖出 23 个 Windows 漏洞并全部获 MSRC 确认；与字节跳动 Seed Alignment & Preparedness 招募构成 24 小时内的安全人才竞赛——网安从"能力涌现"走到"人才建制 + 收入支柱"（约 100 家安全企业接入、Co-work 网安订单 1 个月超 10 亿元）。

## 三、关键数据点

| 指标 | 数值 | 来源 |
|------|------|------|
| GLM-4 GitHub stars | 6.7k | GitHub |
| GLM-4 GitHub forks | 568 | GitHub |
| 开源许可证 | Apache-2.0 | GitHub |
| 最新模型更新 | GLM-4.1V (2025-07-04) | GitHub |
| 平台模型覆盖 | 文本/视觉/图像/视频/音频 | bigmodel.cn |
| Token 换算比例 | 约 1:1.6（token:字） | bigmodel.cn |
| GLM-5.2 参数量 | 约 7,400 亿 | GLM-5.2 |
| GLM-5.2 上下文窗口 | 1M tokens（无损） | GLM-5.2 |
| GLM-5.2 定位 | 长程任务 / Coding 开源 SOTA | GLM-5.2 |
| 2026 Q1 全球调用量增长 | 400% | GLM-5.2 |
| 平台注册企业及用户 | 600 万+ | GLM-5.2 |
| Coding Plan 高阶模型高峰积分系数 | 3 倍（GLM-5.2/GLM-5-Turbo） | GLM Coding Plan 改版 |
| Coding Plan 高峰时段 | 周一至周五 14:00-18:00（UTC+8） | 同上 |
| Coding Plan 团队套餐席位额度上调 | 30% | 同上 |
| GLM-5.3 参数量 | 743B | GLM-5.3 |
| GLM-5.3 AA 综合智能指数 | 60 分（并列开源第一，与 Kimi K3） | GLM-5.3 |
| GLM-5.3 编程能力提升 | ~50%（vs 前代） | GLM-5.3 |
| GLM-5.3 开源状态 | 暂缓开源（下周五预告） | GLM-5.3 |
| GLM-5.3-Flash 参数规模 | 320B 总参 / A18B 激活 | GLM-5.3-Flash |
| GLM-5.3-Flash 上下文 / 输入模态 | 1M tokens / 文本+图像+视频 | GLM-5.3-Flash |
| Ox Alpha 匿名公测 Token 调用量 | 62T（OpenRouter + OpenCode 双平台登顶） | GLM-5.3-Flash |
| GLM-5.3-Flash 承载芯片 | 10 万张国产芯片（全部线上流量） | GLM-5.3-Flash |
| GLM-5.3-Flash AA 指数 / 折扣价 | 57 分 / GLM-5.3 的 1/20 | GLM-5.3-Flash |
| ZCode 夜间畅用时段 | 每晚 23:00–次日 9:00（UTC+8，2026-09-03 至 09-20） | Flash × ZCode 活动 |
| ZCode 夜间额度梯度 | ZCode 0 消耗 / 其他 Agent ×2 | 同上 |
| 2026 H1 营收 | 9.54 亿元（+399.7%），API 占 86.5% | 半年度业绩会 |
| 2026 H1 亏损 | 20.72 亿元（收窄） | 同上 |
| GLM-5.x 基座策略 | 共用 745B 基座（2026-01 完成）+ 后训练迭代 | 同上 |
| 单位 token 推理成本 | 较年初降 80% | 同上 |
| GLM-5 参数 / 训练量 | 744B 总参 / 40B 激活 / 28.5T tokens | GLM-5 开源 |
| GLM-5 SWE-bench Verified / Terminal-Bench 2.0 | 77.8 / 56.2（开源 SOTA） | 同上 |
| GLM-5 国产算力适配 | 7 家（昇腾/摩尔线程/寒武纪/昆仑芯/沐曦/燧原/海光） | 同上 |
| DSA 长序列注意力计算降幅 | 约 1.5-2 倍（200K 上下文近半 GPU 成本） | GLM-5 技术报告 |
| GLM-5.1 SWE-bench Pro | 全球最佳（超 GPT-5.4 与 Opus 4.6） | GLM-5.1 |
| GLM-5.1 持续工作时长 | 8 小时+（METR 口径唯一开源模型） | 同上 |
| GLM-5V-Turbo 上下文 | 200k（多模态 Coding 基座） | GLM-5V-Turbo |
| GLM-OCR 参数 / OmniDocBench V1.5 | 0.9B / 94.6 分登顶 | GLM-OCR |
| GLM-TTS 中文 CER | 0.89%（seed-tts-eval 开源 SOTA） | GLM-TTS |
| GLM-ASR-Nano 平均错误率 | 4.10（Whisper V3 6.93） | GLM-ASR-Nano |
| GLM-Image 长文本渲染（中文） | LongText-Bench 0.979（开源第一） | GLM-Image |
| GLM-Image API 定价 | 0.1 元/图 | 同上 |
| GLM-4.7-Flash 参数 | 30B 总参 / 3B 激活（免费调用） | GLM-4.7-Flash |
| ZCube capex 节省 / 吞吐 / TTFT P99 | -33% / +15% / -40.6% | ZCube |
| Scaling Pain 异常率修复 | 万分之十几 → 万分之三以下 | Scaling Pain |
| GLM-5.3-FlashX 速度 / 定价 | 200 tokens/s（5 倍）/ Flash 的 2.5 倍 | FlashX |
| RSI Infra Agent 提速 | 两周内整体处理速度 3 倍 | RSI Infra Agent |
| 再融资规模 / ARR | 50 亿美元（年内累计 90 亿）/ 18 亿、年末指引 30 亿 | 再融资 |
| ZCode 上传包体积 / 文件数 | 313MB（解压 345MB）/ 42,411 个 | ZCode 事件 |
| ZCode 补偿 | 10 万份 × 1 亿 token + 付费用户额度重置卡 | ZCode 事件 |
| ExploitBench 端到端漏洞利用 | GLM-5.3 50/410 vs Mythos Preview 56 | Anthropic 报告 |
| GLM-5.3 防护绕过率 | 64%-100%（简单技术，Anthropic 模拟测试） | Anthropic 报告 |
| CursorBench 4.0 开放权重最高分 | 42.6%（GLM-5.3，Max 推理设置） | Cursor 上线 |
| 海外云分成 | Amazon Bedrock 按调用量分成（10 月起确认收入） | Amazon Bedrock |
| 国内云分发 | 阿里云百炼已签分成协议 / 华为云已上架 GLM-5.3 | 同上 |
| 古河团队 Windows 漏洞 | 23 个全部获微软 MSRC 确认与致谢 | 古河加盟 |
| Co-work 网安行业订单 | GLM-5.3 发布后 1 个月内超 10 亿元人民币 | 古河加盟 |
| 接入 GLM 的安全企业 | 约 100 家（安全厂商/大厂/研究机构/金融机构） | 同上 |

## 四、与 OpenAI / Anthropic / Kimi 的对比

| 维度 | GLM (智谱) | OpenAI | Anthropic | Kimi (Moonshot) |
|------|-----------|--------|-----------|-----------------|
| 公司地点 | 中国 | 美国 | 美国 | 中国 |
| 模型策略 | 开源 + 商业化 | 闭源为主 | 闭源 | 开源 frontier |
| 最大模型 | GLM-5.2（约 740B） | GPT-5.6 Sol | Claude Fable 5 | Kimi K3 (2.8T) |
| 开源程度 | GLM-4 开源 | 部分旧模型开源 | 闭源 | K3/K2.6 开源 |
| 平台能力 | 全模态 API | 全模态 API | 文本为主 | 全模态 API |
| 核心差异化 | 中文优化 + 本土化 | Agent 工业化 | 安全 + 对齐 | 开放 + 规模 |

## 五、贯穿始终的原则

1. **开源与商业化并行**：GLM-4 开源吸引开发者，API 服务实现商业化
2. **中文场景优化**：针对中文语言和本土应用场景深度优化
3. **全栈平台能力**：从模型调用到部署、微调、评测的完整工具链
4. **多模态覆盖**：文本、视觉、图像、视频、音频全场景覆盖
5. **参数效率对标旗舰**：GLM-5.2 以 K3 约 1/4 的参数量追上 Claude Opus 级编程能力——后训练能力成为国产模型的差异化杠杆
6. **长程任务是下一代战场**：1M 无损上下文 + 端到端交付定位，与 DeepSeek V4、Kimi K3 在"长任务 Agent"方向正面竞争

## 六、文章索引

| # | 日期 | 文章 | 主题 |
|---|------|------|------|
| 1 | 2025-07-04 | [GLM-4.1V Update](https://github.com/THUDM/GLM-4) | 视觉模型更新 |
| 2 | 2025-12-09 | [GLM-ASR-Nano](glm-asr-nano.md) | 高鲁棒 ASR / 方言噪声 / 开源（补录） |
| 3 | 2025-12-10 | [GLM-TTS](glm-tts.md) | 多奖励 RL 语音合成 / CER 0.89%（补录） |
| 4 | 2026-01-13 | [GLM-Image × 华为](glm-image-huawei.md) | 昇腾全程训练 / 文字渲染 SOTA（补录） |
| 5 | 2026-01-19 | [GLM-4.7-Flash](glm-4-7-flash.md) | 30B/3B 免费开源（补录） |
| 6 | 2026-02-02 | [GLM-OCR](glm-ocr.md) | 0.9B 文档解析 SOTA（补录） |
| 7 | 2026-02-11 | [GLM-5 开源](glm-5-open-source.md) | Agentic Engineering / 开源 SOTA（补录） |
| 8 | 2026-02-21 | [GLM-5 技术报告](glm-5-technical-report.md) | 744B / DSA / 异步 RL（补录） |
| 9 | 2026-03-15 | [GLM-5-Turbo](glm-5-turbo.md) | 龙虾增强 / ZClawBench（补录） |
| 10 | 2026-04-01 | [GLM-5V-Turbo](glm-5v-turbo.md) | 多模态 Coding 基座（补录） |
| 11 | 2026-04-07 | [GLM-5.1](glm-5-1.md) | 8 小时长程 / SWE-bench Pro 全球最佳（补录） |
| 12 | 2026-04-29 | [Scaling Pain](glm-scaling-pain.md) | 推理异常治理 / 竞态修复（补录） |
| 13 | 2026-05-20 | [ZCube](glm-zcube.md) | 推理网络架构 / capex -33%（补录） |
| 14 | 2026-06-16 | [GLM-5.2](glm-5-2.md) | 旗舰模型 / 1M 无损上下文 / 长程任务 |
| 15 | 2026-07-30 | [GLM Coding Plan 套餐改版](glm-coding-plan-pricing-revision.md) | 计费改版 / 积分制 / 峰谷定价 |
| 16 | 2026-08-19 | [GLM-5.3](glm-5-3.md) | 基座模型 / 编程 50% / 网络安全 / 暂缓开源 |
| 17 | 2026-08-27 | [GLM-5.3-Flash](glm-5-3-flash.md) | 开源多模态 / Ox Alpha 匿名登顶 / 国产芯片 |
| 18 | 2026-09-03 | [智谱 2026 半年度业绩会](zhipu-h1-2026-earnings-glm-6.md) | 业绩披露 / GLM-6.0 方向 / 后训练迭代 |
| 19 | 2026-09-04 | [GLM Coding Plan "Flash × ZCode" 夜间畅用](glm-flash-zcode-night-free.md) | 夜间免费 / 峰谷调度 / 自有渠道导流 |
| 20 | 2026-09-16 | [50 亿美元再融资与 ARR 指引](zhipu-5b-refinancing-arr-guidance.md) | 小股大债 / ARR 18 亿→指引 30 亿 |
| 21 | 2026-09-17 | [RSI Infra Agent](glm-rsi-infra-agent.md) | AI 自我改进上生产 / 两周提速 3 倍 |
| 22 | 2026-09-18 | [GLM-5.3-FlashX](glm-5-3-flashx.md) | 200 tokens/s / 定价 2.5 倍 |
| 23 | 2026-09-28 | [ZCode 代码上传争议](glm-zcode-data-upload-incident.md) | 数据主权事件 / 开源+双审计+补偿 |
| 24 | 2026-09-30 | [Anthropic 报告评估 GLM-5.3 网络安全能力](glm-5-3-anthropic-cyber-report.md) | ExploitBench 50/410 / 防护绕过 64-100% |
| 25 | 2026-10-02 | [ZCode 争议后续：媒体深度复盘](zcode-followup.md) | 信任重建 / 行业横向对照 / 监管背景 |
| 26 | 2026-10-05 | [Cursor 上线 GLM-5.3](glm-5-3-cursor-cursorbench.md) | CursorBench 4.0 开放权重最高分 / 主权 AI 采用 |
| 27 | 2026-10-06 | [GLM-5.3 接入 Amazon Bedrock](glm-5-3-amazon-bedrock.md) | 海外收入分成 / 云分发第二曲线 |
| 28 | 2026-10-15 | [古河加盟智谱](zhipu-guhe-cyber-talent.md) | 顶级白帽入基座组 / 网安订单超 10 亿 |

> **说明**：GLM 官方信源渠道已确认可用：[zhipuai.cn/zh/research](https://www.zhipuai.cn/zh/research/)（官方结构化研究列表）与 [docs.bigmodel.cn](https://docs.bigmodel.cn/)（开放平台文档）。bigmodel.cn 主站为 SPA 需浏览器渲染；平台运营类动态（FlashX/再融资/ZCode 事件等）与业绩披露以证券时报/上海证券报/TechWeb/IT之家等权威媒体交叉验证入库。上次同步遗留的 12 条历史条目（ZCube、Scaling Pain、GLM-5.1、GLM-5V-Turbo、GLM-5-Turbo、GLM-5 技术报告与开源、GLM-OCR、GLM-4.7-Flash、华为 GLM-Image、GLM-TTS、GLM-ASR-Nano）已于 2026-09-29 全部补录完成（AGENTS.md 已知问题 #5 关闭）。**2026-10-16 同步备注**：docs.bigmodel.cn 更新日志已迁移至 [/cn/update/new-releases](https://docs.bigmodel.cn/cn/update/new-releases)（旧路径 /cn/guide/start/explore-updates 返回 404），最新条目仍为 2026-08-26（GLM-5.3-Flash），zhipuai.cn/zh/research 官方研究列表最新亦为 2026-08-26——检索窗口（09-29 至 10-16）内无官方模型/研究发布，新增 5 篇均基于权威媒体交叉验证。原 "Z Managed Agents (Beta)" 栏目已更名为 "Managed Agents (Beta)" 并升为文档站一级导航，概述页声明"API 与控制台均已全量开放"（9 月底同步时为 API 内测），文档树扩至 25+ 页（Agent/Environment/Session/Events、MCP、Skills、Multi-Agent、沙箱环境、记忆、定时任务、聊天渠道接入等）；但更新日志仍无对应条目、无发布日期可考，继续列为待核查项。GLM-6 截至 2026-10-16 未发布（官方渠道无条目，网传 6.0 Leak 仍为第三方推测）。10 月未入库：10-10 智谱联合杭州国资成立 10 亿元创投合伙企业（仅工商信息、单源、无技术/产品内容）、南向资金与港股行情类纯市场报道。
