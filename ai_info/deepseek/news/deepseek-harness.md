# DeepSeek Harness v0.1 开发者预览版开源：一切皆插件（DeepSeek Harness Developer Preview: Everything is a Plugin）

- **原文链接**: [DeepSeek Harness: Explore the limits of intelligence](https://www.deepseek.com/harness/)
- **作者**: DeepSeek（深度求索，官方产品发布无个人署名）
- **发布日期**: 2026-08-13
- **检索日期**: 2026-10-16
- **标签**: #DeepSeek #DeepSeekHarness #开源 #AgentHarness #插件化 #Agent基础设施

## 核心观点

DeepSeek 于 2026-08-13（官方 X 公告）推出自家 Agent Harness「DeepSeek Harness」v0.1 开发者预览版，面向全球构建 agent harness 的开发者，并以 MIT 协议完整开源代码库。产品形态是"桌面应用 + 可代码启动的 Web UI"双形态，定位从日常工作、写代码到自制 harness 全覆盖——这是 DeepSeek 首次从"模型厂商"延伸到"Agent 执行层"的产品发布。

架构核心是"一切皆插件"：基于 Cordis 元框架，模型、工具、技能、会话、沙箱、文件系统、循环、集成、UI 全部以插件实现，可自由组合、替换、扩展，还支持在"创造模式"里通过对话创建插件。所有执行过程写入追加式会话日志并可按来源回看（Trajectory），可追溯性成为一等公民。

> **补录说明**：本文发布于库内锚点日期（2026-09-10）之前，但此前的同步均未入库（7-31 V4-Flash 基准脚注仅预告 minimal mode"即将发布"），属漏网文章，本次补录。**信源核验**：确认为 DeepSeek 自家产品发布而非第三方工具——官方产品页（deepseek.com/harness/）、官方 GitHub 组织仓库（github.com/deepseek-ai/deepseek-harness）、api-docs 首页官方表述（"DeepSeek Harness is now in developer preview for agent harness developers worldwide"）与 @deepseek_ai 官方推文（2026-08-13）四重互证。

## 关键发现 / 关键技术

### 1. 一切皆插件：Cordis 元框架
- 模型路由、工具、技能、会话、沙箱、文件系统、循环、集成、UI 九类要素全部插件化，可组合、可替换、可扩展；桌面端与 Web UI 同源。
- 官网演示场景覆盖：日常工作（数据汇总 PPT、评审议题）、编码（修仓库、跑测试）、资料查证（搜索、交叉核对、标注来源）、后台批量任务、插件开发。

### 2. 四种执行模式
- **标准模式**：包含全部工具集；**代码模式**：模型生成代码并跨多轮编排工具调用；**最小模式**：仅 shell 工具 + 文件编辑器，用于模型基准测试——即官方基准脚注中的 "DeepSeek Harness minimal mode"（max effort level、topp=0.95、temperature=1.0）；**创造模式**：检查当前环境、在内存中测试 Cordis 插件、组合出新模式。

### 3. 全链路可追溯
- 模型感知的全部信息、prompt、推理、工具调用与结果、子代理调度、每次上下文追加，全部记入追加式（append-only）会话日志；Trajectory 视图按来源逐一核对——针对 Agent 调试与审计痛点的设计。

### 4. 发布路径：先自用后开放
- 7-31 V4-Flash 官方基准已以 "DeepSeek Harness minimal mode" 为评测框架（当时标注"即将发布"），8-13 即开源给全球开发者——先作为自家基准框架、再开放为生态入口，评测与产品形成闭环。
- api-docs 首页 Agent Integrations 一栏已将 DeepSeek Harness 列为首位，与 Claude Code、Codex、OpenCode 等并列。

## 实践意义

对 Agent 开发者：多了一个 MIT 开源的完整 harness 参考实现（含桌面端与插件系统），可整体采用或抽取插件架构；对基准复现：官方模型基准的评测框架现已可得，第三方复现 DeepSeek Agent 成绩的门槛显著降低；对行业：harness 层的竞争从"闭源产品"（Codex App、Claude Code）扩展到"开源实现"，DeepSeek 把模型（MIT 开源）与执行层（MIT 开源）打包，进一步压低自建 Agent 栈的成本。

## 跨厂商对比

- 与 [DeepSeek-V4-Flash 正式版发布](deepseek-v4-flash-official-release.md) 互证：该文基准脚注中的 "DeepSeek Harness minimal mode（即将发布）" 即本产品——8-13 开源落地，先内部评测、后全球开放，发布顺序与"预览即生产"哲学一脉相承。
- 与 [Harness Engineering: Building the Codex App Server for an Agent-First World](../../openai/research/harness-engineering.md) 对比：OpenAI 把 harness 工程化为 Codex App Server（闭源、产品化交付），DeepSeek 选择 MIT 开源整条代码库——同一"Agent-First"命题下的闭源服务与开源基础设施两条路线。
- 与 [Effective Harnesses for Long-Running Agents](../../anthropic/engineering/effective-harnesses-for-long-running-agents.md) 对比：Anthropic 以工程博客分享长时程 Agent 的 harness 设计方法论，DeepSeek 直接交付可运行的开源实现——"讲方法"与"给实现"的知识输出差异。

## 资源

- 论文：无
- 代码：https://github.com/deepseek-ai/deepseek-harness（MIT）
- Demo：https://www.deepseek.com/harness/（桌面端下载）
- 官方文档：https://deepseek-harness.github.io/deepseek-harness/en/guide/quickstart
- 官方公告（X，2026-08-13）：https://x.com/deepseek_ai/status/2087887408440164663
