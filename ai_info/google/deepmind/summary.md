# Google DeepMind — 核心观点总结

> 汇总自 [Google DeepMind Blog](https://deepmind.google/blog/) 的 29 篇文章，涵盖 2026 年 3 月至 8 月。

## 一、总体脉络

Google DeepMind 在 2026 年呈现五大战略方向：

```
模型突破 → Agent 平台 → 科学发现 → 具身智能 → AGI 评估与治理
```

Gemini 3.5 + Omni 构建前沿模型矩阵，Antigravity 2.0 打造 Agent 开发平台，Gemini for Science 将 AI 深度嵌入科学研究。Google 的差异化在于"模型 + 平台 + 科学"三位一体。7 月新动态把版图继续外扩：Gemini Robotics 2 系列实现全身控制人形机器人，3.6 Flash / 3.5 Flash-Lite / 3.5 Flash Cyber 三模型齐发主打 Agent 效率与网络安全垂直场景，Managed Agents 升级为"可编程的云上自动化层"；3-4 月补齐的 AlphaGo 十周年、AGI 认知框架、韩国国家合作与 AI co-clinician 则展示了"技术谱系叙事 + 国家级落地 + 医疗新模式"的治理与生态纵深。6-7 月的扩展进一步把科研模型推向"基础设施化"：DeepMind 与 Isomorphic Labs 联合发布"生物韧性"框架把 AlphaFold/AlphaGenome/AlphaEvolve 从科研突破转化为生物安全基础设施；Nano Banana 2 Lite 与 Gemini Omni Flash 两款开发者媒体模型把图像与视频生成管线打通；Genesis Mission 的 4000 万美元承诺则把五大科研模型投放到 DOE 国家实验室的实际科研流水线。8 月初 [WeatherNext 气旋预测突破](weathernext-cyclones-breakthrough.md) 在《Nature》发表——单一 AI 模型同时预测热带气旋路径、强度和风场结构，三天预报达到此前模型两天预报水平（约等于过去十年气象学进展），同步开源 WeatherNext 2 与 WeatherNext Cyclones 模型代码及权重。8 月 6 日 [Google 领导层重组](next-chapter-ai-momentum.md)——Demis Hassabis 卸任 DeepMind CEO 转任 Alphabet 首席科学家兼 DeepMind 主席，27 年老将 Jeff Dean 离职创业，Koray Kavukcuoglu 接任 CEO，研究（AGI/科学）与应用（Gemini 产品化）分线管理；同日发布 [Veo 3.1](veo-3-1.md)——4K 输出 + 原生竖屏视频 + 改进的素材转视频，直接回应 Sora 2 竞争。8 月中旬研究 [SkillSmith](skillsmith.md) 把模型权重当作"可读写模态"，通过 KV-cache 层组合参数化技能与文本知识，在 Gemma 3 4B 上小模块反超全量微调。

## 二、核心主题

### 1. 前沿模型

[Gemini 3.5](gemini-3.5.md) 是 Google 2026 年最重要的 Agentic 模型发布，Flash 版本首次达到前沿级别智能，输出速度是竞品的 4 倍。配套 [Gemini Spark](https://deepmind.google/blog/gemini-spark/) 是 7x24 个人 AI 代理。

[Gemini Omni](gemini-omni.md) 是原生多模态生成模型，实现"任意到任意"的内容生成，是 Google 区别于 OpenAI/Anthropic 的核心差异化。

[Gemini 3.6 Flash / 3.5 Flash-Lite / 3.5 Flash Cyber](gemini-3-6-flash-3-5-flash-lite-3-5-flash-cyber.md) 三模型齐发全部围绕"规模化构建 AI agent"的效率命题：3.6 Flash 全面超越 3.5 Flash 且更便宜（输出 token 用量 -17%，DeepSWE 上最高 -65%）；3.5 Flash-Lite 以 350 tokens/s 成为高吞吐选项，多项 agentic 评测反超 3 Flash；同时披露 Gemini 3.5 Pro 正在合作伙伴测试、Gemini 4 已启动"迄今最雄心勃勃的预训练"。

[Gemini 3.1 Flash TTS](gemini-3-1-flash-tts.md) 是 Google 最自然的 TTS 模型，核心创新"音频标签"把自然语言指令嵌入文本细粒度控制演绎，支持 70+ 语言与原生多说话人对话，Artificial Analysis TTS 榜 Elo 1,211，全部音频内置 SynthID 水印。

[Nano Banana 2 Lite 与 Gemini Omni Flash](start-building-with-nano-banana-2-lite-and-gemini-omni-flash.md)（2026-06-30）是两款面向开发者的生成式媒体模型：Nano Banana 2 Lite 是最快的 Gemini Image 模型（4 秒延迟、约 $0.034 每 1K 图），Gemini Omni Flash 是高质量视频生成与对话式编辑模型（约 $0.10/秒）。两者均已在 Google AI Studio、Gemini API 和 Gemini Enterprise Agent Platform 上线，核心是"创意迭代"——让开发者构建从图像到视频的完整创作管线并维持多轮编辑的上下文一致性，把快速图像生成与视频创作/编辑打通。两者可链式协作形成端到端多媒体体验。

### 2. Agent 平台

[Google Antigravity 2.0](antigravity-2.0.md) 定位为 Agent-first 开发平台，支持多代理协作。对标 OpenAI Codex 和 Anthropic Claude Code，但更强调科学场景和企业集成。

[Gemini API Managed Agents 更新](expanding-managed-agents-gemini-api-3-6-flash-hooks.md) 把托管 Agent 从"远程执行"推向"可编程的云上自动化层"：默认模型切到 3.6 Flash，新增环境 hooks（pre/post_tool_execution 阻断、lint、审计工具调用）、预算控制（max_total_tokens 防 runaway）、定时触发器，并向免费层开放；开发者用 AGENTS.md / SKILL.md 定义可版本化的托管 agent。

### 3. AI for Science

[Gemini for Science](gemini-for-science.md) 是 Google 的科学 AI 战略旗舰，包含三个核心工具：假设生成（Co-Scientist）、计算发现（AlphaEvolve + ERA）、文献洞察（NotebookLM）。Nature 发表两篇验证论文。

[Co-Scientist](co-scientist.md) 是多代理 AI 系统，模拟科学方法的"想法锦标赛"。已在 Daiichi Sankyo、Bayer Crop Science、美国国家实验室使用。

[AlphaEvolve](alphaevolve.md) 是 Gemini 驱动的编码代理，结合进化算法和 LLM 发现新算法。BASF 用于供应链优化，Klarna 用于 ML 训练加速。

[10 Years of AlphaGo's Impact](10-years-of-alphago.md) 是 Hassabis 在 AlphaGo 战胜李世石十周年之际的技术谱系回顾："第 37 手"宣告现代 AI 时代提前十年到来，搜索 + 规划 + 自我对弈强化学习的血脉经 AlphaZero、AlphaFold（2 亿蛋白质结构、300 万+ 研究者、2024 诺贝尔化学奖）、AlphaProof、AlphaEvolve 一路注入今天的 Gemini——"Gemini 的世界模型 + AlphaGo 的搜索规划 + 专用工具调用"被定位为通向 AGI 的关键组合。

[Announcing Our Partnership with the Republic of Korea](announcing-our-partnership-with-the-republic-of-korea.md) 是 "National Partnerships for AI" 的样板：在首尔设 AI Campus，向韩国科研界开放 AlphaEvolve / AlphaGenome / AlphaFold（韩国已有 85,000+ 使用者）等五大科学模型，联合培养人才并与韩国 AI 安全研究所合作——选中韩国因其 AI 创新密度全球第一（斯坦福 AI Index 2026）。

[Our approach to bioresilience](our-approach-to-bioresilience.md)（2026-07-16）是 DeepMind 与 Isomorphic Labs 联合发布的"生物韧性"框架，把前沿 AI 模型系统性应用于生物安全——从防范自然流行病到应对生物武器威胁。框架围绕"预防—检测—响应"三层面展开，过去 12 个月内推进超过 15 项与政府机构、生物安全组织和科研团队的合作，并复用 AlphaFold、AlphaGenome、AlphaEvolve、SynthID、IsoDDE 五大模型。文章主张 AI 不仅需防范被恶意行为者滥用，更应主动赋能政府与生物安全专家构建更有韧性的社会防御体系——这是把科研突破从"学术成果"转化为"生物安全基础设施"的战略宣言，也是其更广泛 CBRN 风险管理的一部分。

[Accelerating the frontiers of scientific discovery: Google's $40M commitment to the Genesis Mission](accelerating-the-frontiers-of-scientific-discovery-googles-40m-commitment-to-the-genesis-mission.md)（2026-07-22）在 DOE Genesis Mission Summit 2026 上宣布向 Genesis Mission 投入 4000 万美元的 AI token 和云额度，支持美国能源部国家实验室科研人员（白宫 2025 年 11 月发起、目标十年内将美国科学发现速度翻倍）。DeepMind 将 AlphaEvolve、AlphaFold 3、AlphaGenome、WeatherNext、AlphaEarth Foundations 五大科研模型及 Gemini for Government 平台提供给 DOE 研究人员，并在 PNNL 和 NLR 等国家实验室取得可量化的效率提升——展示前沿 AI 工具从"论文成果"走向"实验室基础设施"的具体路径。

### 4. 基础设施与开源

[Decoupled DiLoCo](decoupled-diloco.md) 是分布式训练新方法，减少对 GPU 间高速互联的依赖，降低 AI 训练基础设施门槛。

[Gemma 4](gemma-4.md) 定位为"字节对字节最强开源模型"，与 Meta Llama 在开源市场直接竞争。

### 5. 气候与天气

[WeatherNext](weathernext-hurricane.md) 帮助美国国家飓风中心更准确预测飓风 Melissa，AI 天气预测从实验室走向实际部署。

[WeatherNext 气旋预测突破](weathernext-cyclones-breakthrough.md)（2026-08-06，Nature 发表）是该能力的系统化论文总结与模型开源：单一 AI 模型（WeatherNext Cyclones）同时预测热带气旋路径、强度和风场结构，桥接了传统方法需两类模型（粗分辨率全球模型预测路径 + 高分辨率专用模型预测强度）的权衡。在 2023-2024 年历史气旋上评测，路径、强度、风场结构的提前量优势均超过 24 小时——平均而言三天预报达到此前模型两天预报水平，相当于为预报员多赢得一整天的提前量，约等于过去十年的气象学进展。训练使用近 20TB 全球大气数据 + IBTrACS 历史气旋数据库（近 5000 场历史风暴），用 Functional Generative Networks 生成集成预报集合（规模从 50 成员扩展到 1000 成员），单块 TPU 上不到一分钟生成一份 15 天预报。反直觉的是仅需 28×28km 分辨率数据（比传统模型粗 100 倍）。同步开源 WeatherNext Cyclones、WeatherNext 2、WeatherNext 2-mini（Colab 可免费运行）代码与权重。与 [WeatherNext 飓风预测](weathernext-hurricane.md) 构成从案例验证到科学发表的完整闭环。

### 6. AGI 评估与认知框架

[Measuring Progress Toward AGI: A Cognitive Framework](measuring-agi-cognitive-framework.md) 为"我们离 AGI 还有多远"建立实证度量工具：将通用智能解构为 10 种认知能力（感知、生成、注意、学习、记忆、推理、元认知、执行功能、问题解决、社会认知），提出以人类表现为基准的三阶段评估协议；联合 Kaggle 悬赏 20 万美元为评估缺口最大的 5 种能力设计评测。

### 7. 医疗 AI

[AI Co-Clinician](ai-co-clinician.md) 提出"三元照护"（triadic care）范式：AI agent 在医生临床权威下参与患者照护，放大医生能力而非替代判断（WHO 预测 2030 年全球医疗工作者缺口超 1000 万）。医生端 NOHARM 框架盲测 98 个真实基层医疗查询，97 例零严重错误；患者端基于 Gemini 与 Project Astra 的实时多模态远程医疗能实时纠正吸入器用法——但在识别"危险信号"上仍逊于专家医生，当前定位是支持工具。

### 8. 网络安全

[Introducing Gemini 3.5 Flash Cyber](introducing-gemini-3-5-flash-cyber.md) 是基于 3.5 Flash 微调的轻量级网络安全模型，核心论点：AI 找漏洞的速度已超过防御者修复速度，轻量模型可在同一代码库多次调用、扫描更多代码路径，比单次调用巨型模型更适合漏洞挖掘。V8 引擎等调用次数对比发现 55 个独特确认问题（主线 3.5 Flash 47、Claude Opus 4.6 36，其中 10 个为独有）；已在 Google 内部 Chrome/Android/Cloud 代码库投产，Cloud 团队实测 2 小时发现 RCE 漏洞并生成 100% 可靠 exploit。双重用途属性下仅通过 CodeMender 限量试点开放。

### 9. 机器人与具身智能

[Gemini Robotics-ER 1.6](gemini-robotics-er-1-6.md) 是"推理优先"机器人模型的重大升级：指向（pointing）、计数、成功检测显著提升，解锁仪表读数新能力，可原生调用 Google Search / VLA / 第三方函数，官方称"最安全的机器人模型"。

[Gemini Robotics 2](gemini-robotics-2-brings-whole-body-intelligence-to-robots.md) 首次把物理 AI 扩展到全身运动：行走、下蹲、伸展与操作一体化，同一检查点跨三种本体（Apollo 2 + 两种灵巧手、Franka Duo），拧灯泡成功率 92%，可本地运行、数小时适配新本体。系列含 VLA（端到端运动控制）、ER 2（推理大脑）、On-Device 2（端侧 VLA）三模型。

[Gemini Robotics ER 2](gemini-robotics-er-2.md) 定位机器人的"高层大脑"：相比 ER 1.6 的阶跃变化是时序智能——连续视频流追踪自身进度（进度分类 57.4%）、关键时刻定位（91.3% 准确率、0.96s 误差、4× 速度）、出错自我纠正，并首次引入多机器人协作；接入 Live API 双向流式消除"停下-思考-再行动"顿挫，Boston Dynamics Spot 演示代码已开源。

### 10. 组织与领导力

[The next chapter of our AI momentum](next-chapter-ai-momentum.md)（2026-08-06）是 Pichai 给团队的内部信公开版：Demis Hassabis 卸任 DeepMind CEO，转任 Alphabet 首席科学家并担任 DeepMind 主席，聚焦 AGI 级研究方向；Koray Kavukcuoglu 接任 DeepMind CEO 掌舵 Gemini 产品化；27 年老将 Jeff Dean 携三位顶尖科学家离职创业。研究（AGI、科学发现）与应用（Gemini 产品化）分线管理，消息公布后 Alphabet 股价一度下跌超 4%——市场对核心科学家流失的担忧直接反映在估值上。与 OpenAI 通过外部董事强化治理（David Vélez 等）形成对比，Google 选择让研究者回归研究的组织路线。

### 11. 视频生成

[Introducing Veo 3.1](veo-3-1.md)（2026-08-06）是视频生成模型的工业级升级：4K 输出 + 高保真超分、原生 9:16 竖屏视频适配短视频生态、改进的"Ingredients to Video"（素材转视频）提升角色一致性与音视频同步，Flow 创作工具同步获得新能力。Veo 3.1 同步在 Gemini API 提供，支持程序化调用。与 Gemini Omni 打通多模态生成形成组合，直接对标 OpenAI Sora 2，控制性（一致性、格式、素材）成为关键差异点。

### 12. 技能组合研究

[SkillSmith](skillsmith.md)（arXiv 2607.27497）把"参数化技能"（写入权重的技能）与"文本知识"（自然语言描述）在 KV-cache 层组合成新技能，把模型权重当作"可读写的输入模态"。在 Gemma 3 4B 上验证：组合的小模块在目标任务上超越全量微调且保持通用能力，计算成本远低于完整微调。与 Anthropic Agent Skills（SKILL.md 文本封装）、MCP（服务层标准化）形成"文本、文件、权重"三种技能封装路线。

### 13. 气候行动与开源生态

[Operation Blue Skies](operation-blue-skies.md)（2026-08-19）是 Google 与英国政府合作的首个国家级 AI 试验：AI 为飞行员选择产生更少凝结尾迹的飞行路线，在 Shanwick 北大西洋空域真实运行——凝结尾迹的变暖效应与航空碳排放相当，AI 以极小燃油代价换取显著气候收益，是"天气预测能力（WeatherNext）转化为气候干预"的标志。[Gemmaverse：Gemma 十亿下载](gemma-one-billion-downloads.md)（2026-08-21）庆祝 Gemma 累计下载突破 10 亿次、开发者构建 10 万+ 变体，覆盖太空任务到医疗健康——与 HF 报告显示的 Qwen 30 亿下载共同勾勒开源模型生态头部格局。

## 三、关键数据点

| 指标 | 数值 | 来源 |
|------|------|------|
| Gemini 3.5 Flash Terminal-Bench 2.1 | 76.2% | Gemini 3.5 |
| Gemini 3.5 Flash 速度优势 | 4x | Gemini 3.5 |
| Gemini 3.5 Flash 成本优势 | <50% | Gemini 3.5 |
| Muse Spark 计算效率 vs Llama 4 | 10x | Muse Spark |
| Antigravity 集成数据库 | 30+ | Gemini for Science |
| Co-Scientist 合作机构 | 100+ | Gemini for Science |
| AlphaEvolve 企业应用 | BASF, Klarna | AlphaEvolve |
| WeatherNext 实际部署 | 美国国家飓风中心 | WeatherNext |
| AGI 认知框架认知能力数 | 10 种 | Measuring AGI |
| AGI 评估 Kaggle 黑客松悬赏 | $200,000（5 种能力） | Measuring AGI |
| AlphaFold 免费开放蛋白质结构 | 2 亿（300 万+ 研究者） | 10 Years of AlphaGo |
| 韩国 AlphaFold 研究者用户 | 85,000+ | Korea Partnership |
| AI co-clinician NOHARM 盲测零严重错误 | 97/98 例 | AI Co-Clinician |
| 2030 年全球医疗工作者缺口预测 | 超 1,000 万 | AI Co-Clinician |
| Gemini 3.6 Flash 输出 token 用量 vs 3.5 Flash | -17%（DeepSWE 最高 -65%） | 三模型发布 |
| Gemini 3.6 Flash 定价（输入/输出） | $1.50 / $7.50 每 1M | 三模型发布 |
| Gemini 3.5 Flash-Lite 输出速度 | 350 tokens/s | 三模型发布 |
| Gemini 3.1 Flash TTS 语言数 / Elo | 70+ / 1,211 | Gemini 3.1 Flash TTS |
| 3.5 Flash Cyber V8 独特确认问题 | 55（3.5 Flash 47、Opus 4.6 36） | Gemini 3.5 Flash Cyber |
| Gemini Robotics 2 拧灯泡成功率 | 92% | Gemini Robotics 2 |
| Gemini Robotics 2 跨本体数 | 3（同一检查点） | Gemini Robotics 2 |
| ER 2 关键时刻定位准确率 / 时间误差 | 91.3% / 0.96s | Gemini Robotics ER 2 |
| ER 2 进度分类准确率 | 57.4% | Gemini Robotics ER 2 |
| Nano Banana 2 Lite 延迟 / 成本 | 4s / $0.034 每 1K 图 | Nano Banana 2 Lite |
| Gemini Omni Flash 定价 | $0.10/秒 | Nano Banana 2 Lite |
| Bioresilience 框架层级 | 预防—检测—响应（3 层） | Bioresilience |
| Bioresilience 12 个月合作项目 | 15+ | Bioresilience |
| Bioresilience 复用模型数 | 5（AlphaFold/AlphaGenome/AlphaEvolve/SynthID/IsoDDE） | Bioresilience |
| Genesis Mission 投入 | $40M（AI token + 云额度） | Genesis Mission |
| Genesis Mission 提供科研模型数 | 5（AlphaEvolve/AlphaFold 3/AlphaGenome/WeatherNext/AlphaEarth） | Genesis Mission |
| WeatherNext Cyclones 提前量优势 | >24 小时（路径/强度/风场结构） | WeatherNext Cyclones Breakthrough |
| WeatherNext 训练数据量 | ~20TB 全球大气 + 近 5000 场历史风暴 | 同上 |
| WeatherNext 集成规模 | 1000 成员（去年 50） | 同上 |
| WeatherNext 单块 TPU 15 天预报生成时间 | <1 分钟 | 同上 |
| WeatherNext Cyclones 数据分辨率 | 28×28km（比传统模型粗 100 倍） | 同上 |
| Veo 3.1 输出分辨率 | 4K + 原生 9:16 竖屏 | Veo 3.1 |
| Veo 3.1 关键升级 | 角色一致性 / 素材转视频 / 音视频同步 | Veo 3.1 |
| SkillSmith 验证模型 | Gemma 3 4B（小模块反超全量微调） | SkillSmith |
| SkillSmith 技能组合层 | KV-cache（无需修改基础权重） | SkillSmith |
| Operation Blue Skies 试验空域 | Shanwick 北大西洋（英国国家级） | Operation Blue Skies |
| 凝结尾迹变暖效应 | 与航空碳排放相当（部分估算） | Operation Blue Skies |
| Gemma 累计下载 | 10 亿+ | Gemma One Billion |
| Gemma 开发者变体 | 100,000+ | Gemma One Billion |

## 四、贯穿始终的原则

1. **多模态是第一性原理**：Google 从 Gemini 1.0 起就原生多模态，Omni 将这一优势推向极致
2. **Agent 是产品形态**：从 Antigravity 到 Gemini Spark，Agent 不是特性而是产品
3. **科学是战略高地**：AlphaFold 之后，Google 用 Co-Scientist + AlphaEvolve 构建科学 AI 生态
4. **开源 + 云端双轨**：Gemma 开源吸引开发者，Gemini 云端提供商业价值
5. **生态整合是壁垒**：Search、Android、Cloud、YouTube 的 30 亿用户分发无人能及
6. **具身智能进入全身时代**：从 ER 1.6 的空间推理到 Robotics 2 的全身控制 + 多机协作，"推理大脑 + VLA 小脑"分层架构成形
7. **效率是 Agent 规模化的前提**：3.6 Flash / Flash-Lite / Flash Cyber 全线围绕"更便宜地跑更多 agent"，轻量垂直模型可多次调用扫描更大搜索空间
8. **国家级合作是新的落地通道**：韩国样板把科学模型、人才培养、安全研究打包进 National Partnerships 框架

## 五、文章索引

| # | 日期 | 文章 | 主题 |
|---|------|------|------|
| 1 | 2026-04 | [Gemma 4](gemma-4.md) | 开源模型 |
| 2 | 2026-04 | [Decoupled DiLoCo](decoupled-diloco.md) | 基础设施 |
| 3 | 2026-05-19 | [Gemini 3.5](gemini-3.5.md) | 前沿模型 |
| 4 | 2026-05-19 | [Gemini Omni](gemini-omni.md) | 多模态生成 |
| 5 | 2026-05-19 | [Gemini for Science](gemini-for-science.md) | 科学 AI |
| 6 | 2026-05-19 | [Co-Scientist](co-scientist.md) | 多代理科学 |
| 7 | 2026-05-19 | [AlphaEvolve](alphaevolve.md) | 编码代理 |
| 8 | 2026-05-19 | [Antigravity 2.0](antigravity-2.0.md) | Agent 平台 |
| 9 | 2026-05 | [WeatherNext Hurricane](weathernext-hurricane.md) | 气候 AI |
| 10 | 2026-03-10 | [10 Years of AlphaGo's Impact](10-years-of-alphago.md) | AGI / AI for Science / 技术谱系 |
| 11 | 2026-03-17 | [Measuring Progress Toward AGI: A Cognitive Framework](measuring-agi-cognitive-framework.md) | AGI 评估 / 认知科学 |
| 12 | 2026-04-14 | [Gemini Robotics-ER 1.6](gemini-robotics-er-1-6.md) | 具身智能 / 空间推理 |
| 13 | 2026-04-15 | [Gemini 3.1 Flash TTS](gemini-3-1-flash-tts.md) | 语音合成 / 多语言 |
| 14 | 2026-04-27 | [Partnership with the Republic of Korea](announcing-our-partnership-with-the-republic-of-korea.md) | 国家合作 / AI for Science |
| 15 | 2026-04-30 | [AI Co-Clinician](ai-co-clinician.md) | 医疗 AI / 三元照护 |
| 16 | 2026-07-21 | [Gemini 3.6 Flash / 3.5 Flash-Lite / 3.5 Flash Cyber](gemini-3-6-flash-3-5-flash-lite-3-5-flash-cyber.md) | 模型发布 / Agent 效率 |
| 17 | 2026-07-21 | [Introducing Gemini 3.5 Flash Cyber](introducing-gemini-3-5-flash-cyber.md) | 网络安全 / CodeMender |
| 18 | 2026-07-28 | [Gemini API Managed Agents: 3.6 Flash, Hooks, and More](expanding-managed-agents-gemini-api-3-6-flash-hooks.md) | Agent 平台 / 沙箱治理 |
| 19 | 2026-07-30 | [Gemini Robotics 2: Whole Body Intelligence](gemini-robotics-2-brings-whole-body-intelligence-to-robots.md) | 人形机器人 / VLA |
| 20 | 2026-07-30 | [Introducing Gemini Robotics ER 2](gemini-robotics-er-2.md) | 具身推理 / 多机协作 |
| 21 | 2026-06-30 | [Nano Banana 2 Lite 与 Gemini Omni Flash](start-building-with-nano-banana-2-lite-and-gemini-omni-flash.md) | 生成式媒体 / 图像与视频 |
| 22 | 2026-07-16 | [Our approach to bioresilience](our-approach-to-bioresilience.md) | 生物安全 / CBRN / AlphaFold |
| 23 | 2026-07-22 | [Genesis Mission $40M commitment](accelerating-the-frontiers-of-scientific-discovery-googles-40m-commitment-to-the-genesis-mission.md) | AI for Science / DOE 国家实验室 |
| 24 | 2026-08-06 | [WeatherNext Cyclones Breakthrough](weathernext-cyclones-breakthrough.md) | 天气预报 / 气旋预测 / 开源模型 |
| 25 | 2026-08-06 | [The Next Chapter of Our AI Momentum](next-chapter-ai-momentum.md) | 领导层 / 组织变革 / Hassabis |
| 26 | 2026-08-06 | [Introducing Veo 3.1](veo-3-1.md) | 视频生成 / 4K / 竖屏 |
| 27 | 2026-07-28 | [SkillSmith: Composing Parametric Skills](skillsmith.md) | 技能组合 / KV-cache / 权重即模态 |
| 28 | 2026-08-19 | [Operation Blue Skies: Reducing Aviation Climate Impact with AI](operation-blue-skies.md) | 气候行动 / 凝结尾迹 / 航线优化 |
| 29 | 2026-08-21 | [Inside the Gemmaverse: One Billion Gemma Downloads](gemma-one-billion-downloads.md) | 开源生态 / 里程碑 / 开发者社区 |