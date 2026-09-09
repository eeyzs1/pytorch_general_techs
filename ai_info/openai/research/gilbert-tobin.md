# 律所 Gilbert + Tobin 如何治理并规模化 AI（How law firm Gilbert + Tobin governs and scales AI with OpenAI）

- **原文链接**: [How law firm Gilbert + Tobin governs and scales AI with OpenAI](https://openai.com/index/gilbert-tobin/)
- **作者**: Gilbert + Tobin × OpenAI
- **发布日期**: 2026-09-01
- **检索日期**: 2026-09-09
- **标签**: #企业治理 #ChatGPT-Enterprise #法律行业

## 核心观点

Gilbert + Tobin 是澳大利亚领先的公司制律所，业务覆盖资本市场、并购、争议解决与科技。其 AI 战略不是改变法律服务本身的交付方式，而是提高支撑法律服务运营工作的标准——同时保住客户期望的治理与专业问责。

采用路径呈三段式：ChatGPT Enterprise 先在运营团队受控试点，再扩展到市场、业务开发、招聘、财务、技术、业务转型及部分法律业务；CEO Sam Nickless 以自身用例向员工示范，并明确"AI 不是作弊"——它是员工运用专业判断的另一种工具；迁移到具备澳大利亚数据驻留的 OpenAI 环境后，访问进一步扩大。Codex 则把 firm 从"AI 辅助个人完成离散任务"推进到"AI 在更大工作流中完成定义明确的步骤"，人类始终负责审查与批准结果。

截至 2026 年 6 月，已启用席位的 87% 处于活跃使用状态，是该所其他工具通常采用率的两倍以上——且未设置任何强制使用指标。

## 关键发现 / 关键技术

### 1. 治理框架与数据驻留
- 明确的指引覆盖批准的任务类型、可输入内容与输出审查方式；同时评估了合同保护、基于角色的访问、数据处理要求与管理控制。
- 澳大利亚数据驻留满足了内部要求与客户期望，是扩大访问的前提（CIO Mitch Owens：OpenAI 从企业视角构建了我们这类组织需要的控制）。
- 边界意识：法律专用工作流仍由 Harvey 等批准平台承担，ChatGPT 服务于运营侧；使用者负责约束任务、核查输出、行使专业判断并批准最终成果。

### 2. 效率收益与 Codex 的"执行者"角色
- 招聘研究与数据提取工作流从约 4 小时降至约 20 分钟；每名候选人节省约 25 分钟。
- 选定的冲突、KYC、AML 与相关检查从 3-8 小时降至 5 分钟——Codex 完成研究与处理步骤并产出报告，供人工审查签批。
- Codex 还完成了覆盖 300 个实体的审计报告（省下整整一天人工）、检查并重命名 1,100 个文件、把需求转化为可运行的 Python 应用，以及为 AWS 环境构建监控"watchtower"。
- 特色用例：基于 CEO Nickless 的写作、优先级与业务背景构建的 custom GPT"数字孪生"，供高管在占用 CEO 时间前先压测想法（市场总监 Daniel Quinn 案例）。

## 实践意义

对专业服务与受监管行业，这个案例的可复制点在于"采用率是治理的函数"：不设强制指标、领导示范、角色化培训（业务转型团队逐团队演示定制工作流），配合数据驻留与清晰的使用边界，反而换来 87% 的活跃率。"AI 是工具、人对结果负责"的问责框架，为法律、金融等信任密集型行业提供了规模化 AI 的叙事模板。

Codex 部分则展示了从"助手"到"执行者"的分界：让 AI 承担不规则、难以用传统自动化 justify 的多步运营工作（审计报告、文件重命名、合规检查），人退到审查与签批环节。

## 跨厂商对比

- 与 [JetBrains 评估 Claude Fable 5](../../anthropic/engineering/jetbrains-evaluates-claude-fable-5.md) 对比：JetBrains 以工程团队内部评测数据驱动模型采用决策，Gilbert + Tobin 以领导层示范 + 治理框架驱动全所采用，两种企业采用机制互为镜像。
- 与 [ABC Legal 的托管 Agent](../../anthropic/engineering/abc-legal-managed-agents.md) 互补：同为法律行业，ABC 通过托管 agent 服务交付能力，Gilbert + Tobin 展示律所内部自建治理与人机分工的路径。

## 资源

- 官方文章：https://openai.com/index/gilbert-tobin/
- 相关：N/A
