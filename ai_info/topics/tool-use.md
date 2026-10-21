# 工具使用与 ACI 阅读路线

## 先读

- [Writing Effective Tools for AI Agents](../anthropic/engineering/writing-effective-tools-for-ai-agents.md)：Agent 工具设计五大原则。
- [Raising the Bar on SWE-bench Verified](../anthropic/engineering/raising-the-bar-on-swe-bench-verified.md)：通过 ACI 优化提升 SWE-bench 表现。
- [New Tools for Building Agents](../openai/research/new-tools-for-building-agents.md)：Responses API、Agents SDK 和内置工具。

## 规模化工具

- [Advanced Tool Use](../anthropic/engineering/advanced-tool-use.md)：工具搜索、程序化工具调用和工具示例。
- [DeepSeek V4-Flash-Vision-Exp](../deepseek/news/deepseek-v4-flash-vision-exp.md)：多模态工具接口的兼容性设计——单图 384 tokens 封顶按 token 计费、Files API 以 file_id 跨请求复用图片、Chat Completions / Messages / Responses 三种 API 格式并存，OpenAI 与 Anthropic 生态的存量 Agent 工具近零改造即可获得视觉能力。
- [Code Execution with MCP](../anthropic/engineering/code-execution-with-mcp.md)：用代码执行降低工具调用 token 成本。
- [The Next Evolution of the Agents SDK](../openai/research/the-next-evolution-of-the-agents-sdk.md)：Agents SDK 对 MCP 的支持。
- [Advancing Voice Intelligence with New Models in the API](../openai/research/advancing-voice-intelligence-with-new-models-in-the-api.md)：实时语音模型如何把工具调用和 Agent 行为带入 voice interface。
- [New Tools and Features in the Responses API](../openai/research/new-tools-and-features-in-the-responses-api.md)：Web 搜索、文件搜索、Computer Use 的工具层迭代。
- [Equipping the Responses API with a Computer Environment](../openai/research/equipping-the-responses-api-with-a-computer-environment.md)：把 Shell 工具 + 托管容器 + 服务端 Compaction + Agent Skills 组合为"系统级 Agent 执行"。
- [Muse Spark 1.1 and the Meta Model API](../meta/muse-spark-1-1.md)：务实的 Computer Use——按场景自选执行方式（写脚本更快就写脚本、点 GUI 更省事就点界面），批量场景一次生成多步操作统一执行，解决"每步重新看屏-推理-点击"的低效。
- [Gemini API Managed Agents: 3.6 Flash, hooks, and more](../google/deepmind/expanding-managed-agents-gemini-api-3-6-flash-hooks.md)：环境 hooks 治理工具调用——`.agents/hooks.json` 在 pre/post_tool_execution 事件执行自定义脚本，可按正则匹配工具进行阻断、lint 或审计，拒绝理由直接注入模型上下文。
- [Continuous Voice Interaction with GPT-Live](../openai/research/continuous-voice-interaction-with-gpt-live.md)：语音作为工具接口——全双工语音模型同时听和说，深度推理和工具调用走异步路径不阻塞对话流；会话开始即创建前沿模型推理会话并预填充初始上下文，用稳定会话亲和性和 prompt caching 降低延迟。
- [Agents API：OpenAI 把 Codex 智能体骨架产品化](../openai/research/introducing-the-agents-api.md)：托管 harness 的工具层——编排、长时会话与工具使用由 Codex harness 以云服务开放，沙盒与权限边界由平台负责；Data agent 等开箱即用角色直接构建其上，验证托管编排的生产可用性。
- [GPT-Live-1 进入 API](../openai/research/introducing-gpt-live-1-in-the-api.md)：语音即工具接口——全双工可打断对话 + 自定义音色 + telephony 电话网直连；工程重心从"拼装 ASR+LLM+TTS"转移到打断策略、延迟预算、音色合规与电话网对接，瞄准呼叫中心替换市场。
- [Holo4：驱动通用 computer-use agent](../huggingface/blog/holo4.md)：四通道统一——GUI 点击、代码沙盒、MCP、REST API 由同一开源权重模型驱动，环境覆盖桌面、浏览器、Android 与终端；Agentic Task Factory 从软件文档与截图合成约 1 万个可自动验证任务，部分任务暴露 GUI/MCP 双路径训练模型"择路"。
- [Kimi Code Desktop 正式发布](../kimi/blog/kimi-code-desktop.md)：内置浏览器与终端工具——浏览器支持截图标注、划词评论、@文件与元素点选，内置终端让命令执行不离开应用；审阅粒度到文件与页面元素，三档权限控制调节自主程度。
- [Muse Realtime Avatar](../meta/muse-realtime-avatar.md)：共享 token 流驱动双输出——一条语音 token 流同时驱动音频解码器与视频生成器，口型、韵律与表情天然对齐、无需后处理对齐管线；guidance-aware 蒸馏 + self-forcing 把交互式化身压进 870ms 首响预算。
- [OpenAI DevDay 2026 回顾](../openai/research/devday-2026-recap.md)：工具生态的平台化整编——插件重做创建/提交/发现流程并统一目录、新增 MCP 事件触发（外部事件驱动 Agent 自动更新 Page）、Agents API 补齐 computer use，Sign in with ChatGPT 与 Decisions API（Luna 实时分类/路由判断）把"登录与决策"也变成可调用能力。
- [DeepSeek Search & Fetch API](../deepseek/news/deepseek-search-fetch-api.md)：联网检索成为模型 API 原语——Search 返回 snippet/summary/rerank_score/authority 分层结构（面向 UI 与模型双读者），Fetch 网页转 Markdown 直接入上下文；按成功请求计费（各 $0.75/千次、失败不计费），Claude Code/Codex 发起的搜索首两周免费，Agent 的"检索—抓取—推理"闭环不再依赖第三方搜索服务。

## 协议与标准

- [The 2026-07-28 MCP Specification](../community/specification/mcp-2026-07-28-specification.md)：MCP 问世以来最大修订——无状态协议核心（移除 initialize 握手，每请求自描述，普通负载均衡即可水平扩展）、MRTR 多轮往返替代长连接 elicitation、HTTP 头部路由（网关/WAF 无需解析 JSON body 即可鉴权）、可缓存列表响应（ttlMs + cacheScope 保持 prompt cache 跨重连稳定）、OAuth 授权加固（RFC 9207 iss 校验 + localhost 重定向 + 凭据绑定签发方）；Tasks 移入扩展框架，Roots/Sampling/Logging 进入弃用期。
- [MCP 新路线图：Agent 消息原语与统一传输](../community/specification/mcp-roadmap.md)：下一程五大优先领域——Agent 消息原语（服务器发起事件免轮询）、HTTP 原生传输统一（本地服务器也走 Streamable HTTP）、Agent 身份与企业安全（DPoP、Workload Identity Federation、ID-JAG）、改进原语（统一 tools/call 结果契约 + 渐进式发现）、SDK 开发者体验。
- [MCP 官方 Ruby SDK 达到 1.0](../community/blog/ruby-sdk-1-0.md)：SDK 分级体系与 100% 一致性——服务端与客户端一致性测试场景全部通过，满足 Tier 2 全部要求并朝 Tier 1 推进；HTTP 传输即标准 Rack 应用，Rails 加一条路由即可挂载 MCP 服务器，SDK 成熟度成为可比较的工程指标。
- [ProvenanceGuard](../huggingface/blog/getting-the-source-right.md)：MCP Agent 的来源感知验证——针对"跨源混淆"（事实为真但归因到错误来源）的后置验证层：分解声明 → 路由来源 → NLI 核对归因，医学 Agent 实测对不该通过的 139 条声明拦截 138 条；唯一输出"声明 → 来源"映射的验证器（拦截 F1 0.802），纯本地小模型即可叠加在黑盒 Agent 之上。

## 工具组合与垂直化

- [Codex for Every Role, Tool, Workflow](../openai/research/codex-for-every-role-tool-workflow.md)：90+ 插件、6 角色插件、62 应用、110 技能——OpenAI 把工具组合工业化。
- [Open-Source Codex Orchestration with Symphony](../openai/research/open-source-codex-orchestration-symphony.md)：把 Codex 接入企业自建协调器，多 Agent 调度的开源实现。
- [Codex-Maxxing for Long-Running Work](../openai/research/codex-maxxing-long-running-work.md)：把"工作树 + 测试 + Git"作为可验证工具组合，让 Agent 的执行可观测、可回滚。
- [New ways to learn and teach with ChatGPT Work and Codex](../openai/research/learn-teach-chatgpt-work-codex.md)：教育插件作为垂直化工具——K-12 教师、大学教师、大学生三款插件把应用、角色技能、指令和工作流打包，让用户无需构建复杂提示即可上手；插件化策略将"如何提示"的负担从用户转移到预配置工作流。
- [Fine-tuning a 350M Model for Better Structured Outputs in 100 GRPO Steps](../huggingface/blog/grpo-with-trl-ifstruct.md)：结构化输出作为工具调用契约——350M 小模型用 500 样本 / 100 步 GRPO 把 IFStruct 从 22.6% 提到 29.7%，JSON 子项 +13.9；结构化输出是把 LLM 接入工具与系统的"接口层"，小模型 + 定向 RL 即可逼近 6 倍大模型的水平。
- [Wire It, Run It, Deploy It: AI Workflows in Gradio](../huggingface/blog/gradio-workflow-guide.md)：gr.Workflow 把工具链变成可视化资产——typed 节点图同时渲染为拖拽画布与 REST API（每输出一端点），三类节点 × 四种 operator（函数 / 模型 / Space / 数据集行）一键部署 Spaces；工具编排的产物从代码变为可分享、可直接调用的工作流对象。
- [Building commerce agents with Claude](../anthropic/engineering/claude-for-commerce-agents.md)：垂直行业工具链打包——商业 Agent 蓝图含四行业参考实现 + Claude Code 插件，购物 Agent 调商家工具、商家 Agent 管目录与订单且变更须人工批准；工具权限按角色分层的生产范式。
- [Intelligent transcription with Gemini 3.5 Transcribe](../google/deepmind/gemini-3-5-transcribe.md)：语音作为 Agent 入口的生产化——智能转写（去填充词/自我纠正/自动格式化）+ function calling 委派图像生成、文件分析等任务给其他 Gemini 模型；Live API 亚秒级双向流 + Interactions API 说话人归属与词级时间戳，落地 Gboard/Antigravity/Gemini app/Chrome。
- [Introducing the Admin plugin for ChatGPT Work and Codex](../openai/research/introducing-admin-plugin.md)：管理操作的工具化——一个对话完成用量/成员/权限/限额四类操作且权限感知不越权，审批自动路由 Slack/Teams 并按条件自动批准；OpenAI IT 自用 45% 工单自动解决、支持量翻倍下积压清零。
- [How GPT-5.6 Sol helps run quantum computing experiments](../openai/research/codex-quantum-computing-experiments.md)：实验室工具的 Agent 封装——MIT EQuS 把 GPT-5.6 Sol 接入 Codex 连接实验室软件，对未校准 6 比特芯片近自主完成标准校准链；measurement-specific skills 把实验操作封装为可通宵运行、手机异步抽查的技能，弱信号场景仍需资深研究者指导。
- [GLM-5V-Turbo：多模态 Coding 基座](../glm/blog/glm-5v-turbo.md)：多模态 Coding 工具链（历史补录）——预训练级视觉-文本融合直接"看懂"设计稿、截图与网页生成可运行代码，200k 上下文；深度适配 Claude Code 与 OpenClaw/AutoClaw，"股票分析师"Skill 读 K 线 60 秒产出图文研报。
- [GLM-OCR：SOTA 复杂文档解析](../glm/blog/glm-ocr.md)：垂直专业工具（历史补录）——0.9B 参数在 OmniDocBench V1.5 以 94.6 分登顶、整体接近 Gemini-3-Pro，复杂表格直接输出 HTML；1.86 页/秒、约 1 元处理 2000 张 A4，兼容 vLLM/SGLang/Ollama 可端侧部署。
- [GLM-TTS：工业级语音合成](../glm/blog/glm-tts.md)：语音输出侧专用工具（历史补录）——10 万小时数据即具备 3 秒音色复刻，GRPO 同时优化字错率、说话人相似度、情感、笑声四个奖励；seed-tts-eval 中文 CER 0.89% 为开源 SOTA，LoRA 定制仅需 15% 参数 + 约 1 小时音频。
- [GLM-ASR-Nano：高鲁棒性语音识别](../glm/blog/glm-asr-nano.md)：语音输入侧专用工具（历史补录）——1.5B 参数取得开源最低平均错误率 4.10（Whisper V3 为 6.93），方言、中英同句混说、耳语音量、嘈杂环境与自定义热词直击真实"不完美语音"；智谱 AI 输入法为首个生产部署。
- [Gemini 3.8 Flash TTS 与 Flash-Lite TTS 发布](../google/deepmind/gemini-3-8-tts.md)：语音输出工具从"可导演"到"可选角"——单行舞台指示精细控制语气、单一脚本生成双说话人对话、凭文字描述合成新声音或 30 秒样本克隆，覆盖 100+ 语言；与 3.8 Live、Live Avatar 同月拼齐实时语音全栈。
- [刚果埃博拉响应中的 Claude](../anthropic/research/ebola-response.md)：Skill 汇总疫情数据——WHO AFRO 用 Claude Skill 自动汇总各区 PowerPoint 疫情数据、与前一日对比并解释趋势，把一整天的 sitrep 压缩到 1 小时以内；领域工作流"技能化"交付的高风险场景样本。
- [LightOnOCR-3](../huggingface/blog/lightonocr-3.md)：文档解析垂直工具的多合一化——单模型同时输出转录、归一化边界框、图像描述与图表 HTML 表格，替代"OCR + 版面分析 + 图表抽取"三段管线且输出 token 平均少 9–14%；4B 综合 86.3 仅落后 35B 的 Infinity Parser Pro 1.3 分，按文档类型选 0.8B/1B/4B 是可行策略。

## 网络安全与安全工具

- [Daybreak: Tools for Securing Every Organization in the World](../openai/research/daybreak-securing-the-world.md)：Codex Security 把"漏洞扫描 + 补丁生成 + PR 提交"做成端到端工具链；GPT-5.5-Cyber 在 CyberGym 85.6%。
- [Patch the Planet: A Daybreak Initiative](../openai/research/patch-the-planet.md)：把"AI + 专家研究员"直接做成开源维护者的工具，5 天冲刺发现数百问题、合入数十补丁。
- [Mapping AI-enabled Cyber Threats: Insights from the LLM ATT&CK Navigator](../anthropic/research/attack-navigator.md)：ARiES 风险评分工具 + MITRE ATT&CK 框架扩展到 AI Agent 编排。
- [Measuring LLMs' Impact on N-day Exploits](../anthropic/research/n-days.md)：Mythos Preview 自动构建完整 exploit 工具链——N-day 利用从手工走向工业化。
- [Inference hooks: inline DLP for Claude Enterprise](../anthropic/engineering/claude-enterprise-inference-hooks.md)：DLP 集成作为安全工具——签名 WebSocket 把工具调用响应在返回模型前先经检查；支持 shadow mode、基于角色的排除、百分比灰度发布，可与 Netskope/Palo Alto/Zscaler 等现有 DLP 服务器集成。
- [Launching an opt-in vulnerability-finding service for open-source software](../anthropic/research/launching-opt-in-vuln-finding-service-for-open-source.md)：安全披露经济学的范式实验——六个月 29,000+ 候选漏洞人工只能消化约 6,000 个，OSS Scanner 以"零人工审查"换取扫描速度与频率，报告直发 opt-in 维护者；专家复核 97 个严重/高危发现 88% 达 CVD 披露标准，模型报告的信号噪声比已可承受。

## 跨域工具

- [Project Fetch: Phase Two](../anthropic/research/project-fetch-phase-two.md)：把 Agent + 物理机器人作为统一工具组合，比人类快 18-37 倍。
- [Agents in Biology: Paving the Way for Autonomous Wet-Lab Discovery](../anthropic/research/agents-in-biology.md)：把湿实验、数据库查询、确定性工具组合为 VirBench 自动化工具链。
- [Making Claude a Chemist](../anthropic/research/making-claude-a-chemist.md)：把化学专用工具（ChemDraw / MestReNova）作为 Agent 的专业 ACI。
- [Brain2Qwerty v2](../meta/brain2qwerty-v2.md)：把"AI Agent 自动探索解码 pipeline 优化配置"作为科研工具——Meta 在脑机接口研究中用 Agent 探索超参空间，但最终训练配置由工程师手动选择，体现"Agent 探索 + 人类决策"的协作模式。
- [Gemini Robotics-ER 1.6](../google/deepmind/gemini-robotics-er-1-6.md)：机器人的高层推理大脑——原生调用 Google Search、VLA 模型或任意第三方函数执行任务，成功检测决定重试失败步骤还是进入下一阶段。
- [Introducing Gemini Robotics ER 2](../google/deepmind/gemini-robotics-er-2.md)：物理工具编排——开发者把 VLA、导航 API 等低层控制接口声明为工具，模型流式接收视频/音频/文本并原生调用 Search 或自定义函数，在真实 VLA、仿真 VLA、人类遥操作三种模式下编排能力均超 ER 1.6。
- [From the Hugging Face Hub to robot hardware with Strands Agents and LeRobot](../huggingface/blog/strands-lerobot-hub-to-hardware.md)：机器人训练闭环工具链——Hub 下载 LeRobot 模型/数据集 → Strands 模拟训练 → 真实机械臂部署的端到端流程，把"模型中心化分发 + 开源框架 + 云服务"的 LLM 生态模式复制到物理世界，降低机器人开发者的 ML 基础设施门槛。
- [Introducing Muse Glimmer](../meta/introducing-muse-glimmer.md)：端侧 Agent 的工具调用——30B 参数、Apache 2.0、专为函数调用与工具使用优化的开源模型，约 24GB 显存本地运行；把"工具调用能力"从云端 API 下沉到消费级硬件，工具使用不再依赖云端连接。
- [Build production agents with computer use, the Skills API, and the Files API](../anthropic/engineering/computer-use-skills-api-files-api.md)：Agent 工具三件套 GA——Computer Use 新增 browser use tool（读页面结构操作具体元素而非屏幕坐标），Skills API 打包团队方法论按需注入，Files API 交付结构化成品；"操作 + 方法 + 产出"的完整工具闭环。
- [The Multimodal Intelligence of Muse Spark 1.2](../meta/multimodal-intelligence-muse-spark-1-2.md)：工具增强的多模态推理——多模态增益在模型可调用工具时最显著，视觉检查 → 工具调用 → 推理的闭环让视频可直接转化为可运行代码产物。
- [NVIDIA Warp 与 MjWarp 加速机器人仿真](../huggingface/blog/nvidia-mjwarp-robotics-sim.md)：GPU 批量仿真 + 确定性执行——SO-101 机械臂仿真从 MuJoCo CPU 单环境扩展到 2048 个并行环境，优化目标从"单个世界跑多快"变成"同时能跑多少个世界"；1.15 确定性执行模式让 GPU 原子操作可复现，用少量性能换可信的回归测试。

## 关键结论

- 工具描述就是 Agent-Computer Interface，应该像给新员工写操作手册。
- 工具数量变多后，需要动态发现、命名空间、示例和程序化编排。
- 工具输出要返回可行动上下文，而不是把无关日志倾倒给模型。
- 工具的"工业化组合"是 Codex 多角色插件、Symphony 协调器、Daybreak 安全工具链的共同方向——把单点能力变为可重复的端到端工作流。
- 垂直工具（化学/生物/安全）比通用工具更专业——把领域工具作为 ACI 一部分，模型才能在该领域达到专家级。
- MCP 把"百级工具列表导致选择退化"列为协议层优先项——渐进式发现与统一 tools/call 结果契约进入路线图，与模型侧工具搜索（Anthropic Advanced Tool Use）双轨并行，上下文工程问题上升为协议特性。
- 行动通道向"单模型多通道"与"语音即接口"收敛——Holo4 用单一模型统一 GUI/沙盒/MCP/REST 四通道，GPT-Live-1 与 Muse Realtime Avatar 把语音与化身纳入工具调用界面，外围两套技能栈的维护开始被内化进模型。
- 联网检索正从外挂服务收编为平台原生工具层——DeepSeek 把 Search/Fetch 做成按成功请求计费的 API 原语，OpenAI 插件目录新增 MCP 事件触发让工具反向主动驱动 Agent，工具生态的"平台化"与"协议化"两条线在同一个窗口交汇。
