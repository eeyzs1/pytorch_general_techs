# 官网同步记录：2026-11-17

> 本次为工程技术专题增量，覆盖 Agent 记忆、评估与运行控制、模型后训练和高效执行。已检查全部指定厂商信源，新增 18 篇；不声称窗口内全部新闻、科学应用案例及社区帖子已入库。

## 同步锚点

锚点在检索前由原 `catalog.yaml` 的 544 个条目实际统计，不以旧报告的叙述代替。按 provider 取已收录文章的最大发布日期：

| Provider | 原条目数 | 原锚点 | 本轮新增 | 新条目数 |
|---|---:|---|---:|---:|
| OpenAI | 224 | 2026-10-15 | 4 | 228 |
| Anthropic | 128 | 2026-10-15 | 3 | 131 |
| Google | 57 | 2026-10-15 | 3 | 60 |
| Meta | 22 | 2026-10-15 | 2 | 24 |
| Hugging Face | 62 | 2026-10-16 | 3 | 65 |
| DeepSeek | 9 | 2026-10-16 | 2 | 11 |
| GLM | 27 | 2026-10-15 | 0 | 27 |
| Kimi | 12 | 2026-10-14 | 1 | 13 |
| Community | 3 | 2026-08-22 | 0 | 3 |
| 合计 | 544 | 按厂商分别检索 | 18 | 562 |

## 同步范围与信源状态

| Provider | 实际检查的官方入口 | 结果 |
|---|---|---|
| OpenAI | [官方入口](https://openai.com/research/) | 可读取研究入口；发布窗口与新闻列表交叉检查。 |
| OpenAI | [官方入口](https://openai.com/index/) | 重定向至官方 news 列表，读取独立正文。 |
| Anthropic | [官方入口](https://www.anthropic.com/research) | 可读取研究列表和正文，区分团队与文章路径。 |
| Anthropic | [官方入口](https://www.anthropic.com/engineering) | 可读取；工程文章也可能使用 /research/ 正文 URL。 |
| Google | [官方入口](https://deepmind.google/discover/blog/) | 重定向至 /blog/；沿官方链接读取 blog.google 与 DeepMind 正文。 |
| Meta | [官方入口](https://ai.meta.com/blog/) | 旧列表较滞后，不能据此判断窗口内没有新文章。 |
| Meta | [官方入口](https://research.meta.ai/) | 读取当前研究列表及 11 月两篇技术正文。 |
| Meta | [官方入口](https://ai.meta.com/research) | 交叉检查当前研究入口。 |
| Hugging Face | [官方入口](https://huggingface.co/blog) | 读取主列表与相关作者 / 官方组织文章。 |
| Hugging Face | [官方入口](https://huggingface.co/blog?p=1) | 检查后续页；本轮未遍历全部社区文章与历史分页。 |
| DeepSeek | [官方入口](https://www.deepseek.com/) | 首页链接指向 1017 正式公告。 |
| DeepSeek | [官方入口](https://api-docs.deepseek.com/) | 结合 /zh-cn/updates/ 与两篇新闻正文核验日期。 |
| DeepSeek | [官方入口](https://api-docs.deepseek.com/zh-cn/updates/) | 确认 10-17 与 11-13 更新；英文裸 URL 搜索缓存出现旧截面，以当前中文日志与新闻交叉确认。 |
| GLM | [官方入口](https://www.bigmodel.cn/) | 主站仅返回 JavaScript 提示，正文获取受限，标为待补；用以下官方渠道补足本轮检查。 |
| GLM | [官方入口](https://github.com/THUDM/GLM-4) | 旧模型仓库，无本窗口的新研究条目。 |
| GLM | [官方入口](https://www.zhipuai.cn/zh/research) | 最新可见研究条目为 2026-08-26；未检得可核实的窗口新模型文章。 |
| GLM | [官方入口](https://docs.bigmodel.cn/cn/update/new-releases) | 最新可见模型发布条目同为 2026-08-26；不据此推断所有产品渠道均无更新。 |
| Kimi | [官方入口](https://www.kimi.com/blog/) | 发现 2026-10-24 的 K3.1 Pro，纠正旧总结的停更判断。 |
| Kimi | [官方入口](https://platform.moonshot.cn/blog) | 重定向至 platform.kimi.com/blog；所见列表较旧，不能替代研究博客。 |
| Kimi | [官方入口](https://huggingface.co/moonshotai/Kimi-K3.1-Pro) | 补充核验模型页与自定义许可证，不用原文的计划日期推断当前权重状态。 |

## 新增文章

### OpenAI（4 篇）

1. **2026-10-29 | [前沿模型失准监控：从探针到调查闭环](openai/research/how-we-detect-frontier-model-misalignment.md)** — 失准监控 / Agent安全 / 评估。
2. **2026-11-05 | [GPT-6 Cyber：把能力与任务范围遵守一起评估](openai/research/introducing-gpt-6-cyber.md)** — 网络安全 / Agent评估 / 范围约束。
3. **2026-11-09 | [Control Room：在推理层集中停止研究工作负载](openai/research/control-room.md)** — 运行时控制 / Agent安全 / 基础设施。
4. **2026-11-16 | [嵌入式评估首阶段：访问深度与独立性协议](openai/research/our-first-phase-of-embedded-assessments.md)** — 独立评估 / 对齐 / 治理。

### Anthropic（3 篇）

1. **2026-10-27 | [AI 如何影响专家判断：执行辅助之外的决策偏向](anthropic/research/agents-judgment-calls.md)** — 人机协作 / 实验设计 / 专家判断。
2. **2026-11-06 | [Agent 记忆组件：从记录到经过验证的经验](anthropic/engineering/components-of-agent-memory.md)** — Agent记忆 / 上下文工程 / 评估。
3. **2026-11-13 | [构建可信安全评估：设计、运行与报告](anthropic/engineering/building-strong-safety-evaluations.md)** — 安全评估 / 方法论 / 多轮评估。

### Google DeepMind（3 篇）

1. **2026-10-28 | [Gemini 4 Carbon：长任务能力与网络防御评估](google/deepmind/introducing-gemini-4-carbon.md)** — Gemini / 长程任务 / 网络能力。
2. **2026-11-10 | [AlphaProof Code：将形式化验证推进到真实实现](google/deepmind/introducing-alphaproof-code.md)** — 形式化验证 / 多智能体 / 软件可靠性。
3. **2026-11-12 | [Gemini 4 Hydrogen：多模型工作流中的高效执行](google/deepmind/introducing-gemini-4-hydrogen.md)** — Gemini / 多模型路由 / Agent效率。

### Meta AI（2 篇）

1. **2026-11-06 | [Meta 将专门模型与主动记忆带入 Muse 和 Meta AI](meta/specialized-models-for-muse-and-metaai.md)** — 模型专门化 / Agent记忆 / 任务恢复。
2. **2026-11-09 | [Muse Ember：面向重复 Agent 子任务的经济模型](meta/muse-ember.md)** — 高效模型 / Agent子任务 / 评估口径。

### Hugging Face（3 篇）

1. **2026-10-20 | [Agent 后训练课程：从轨迹模仿到完整运行反馈](huggingface/blog/train-agents.md)** — Agent后训练 / TRL / 强化学习。
2. **2026-11-10 | [Decision Models：直接评估候选动作的结构化接口](huggingface/blog/decision.md)** — 决策模型 / 结构化输出 / 推理效率。
3. **2026-11-13 | [llama.cpp 1.0：本地推理库的 API 与 ABI 边界](huggingface/blog/llama-cpp-v1.md)** — 本地推理 / llama.cpp / 版本兼容。

### DeepSeek（2 篇）

1. **2026-10-17 | [DeepSeek V4.1 Flash 1017：后训练更新与搜索 API 公告](deepseek/news/news261017.md)** — DeepSeek / Agent后训练 / 搜索工具。
2. **2026-11-13 | [DeepSeek 应用 API：搜索、文件、链接与语音的组合](deepseek/news/news261113.md)** — 应用API / 工具调用 / 多模态。

### GLM（0 篇）

官方研究列表和发布日志未检得符合本次工程主题与日期要求的新文章；主站动态正文仍待补，未以传闻创建条目。

### Kimi（1 篇）

1. **2026-10-24 | [Kimi K3.1 Pro：扩大后训练与长程任务能力](kimi/blog/kimi-k3-1-pro.md)** — Kimi / 长程任务 / 开放权重。

### Community（0 篇）

本轮未扩展 Community 的历史协议文章，原有 3 篇保持不变。

## 派生文件复核

- `catalog.yaml`：由 `python ai_info/scripts/build_catalog.py` 重建，不手改 article 条目。
- 9 份厂商 / 分类总结均已复核：OpenAI 228、Anthropic Engineering 74 / Research 57、Google 60、Meta 24、HF 65、DeepSeek 11、GLM 27、Kimi 13。
- OpenAI 旧索引中一行同步记录移出文章计数，GLM 旧索引中一条外部仓库资源移出独立摘要计数；保留历史链接并重排文章编号。
- Kimi 总结纠正“研究博客停更 / K3.1 未发布”的旧状态；DeepSeek 旧 Search / Fetch 摘要补记 10-17 正式公告，保留最初观察日期的历史说明。
- `README.md` 更新入口与数量。

## topics 全量复核

AGENTS.md 中列出的 7 个文件是旧清单，本轮以实际目录为准，检查全部 11 个现有文件；没有创建新主题。

| 文件 | 本轮处理 | 判断 |
|---|---|---|
| agent-architecture.md | 更新 | 记忆、模型分工、后训练与平台编排相关 |
| context-engineering.md | 更新 | Anthropic 记忆组织与 Meta Active Memory 相关 |
| evals.md | 更新 | 安全评估、专家实验、外部访问与形式化验证相关 |
| safety.md | 更新 | 检测、停止控制、授权范围与独立监督相关 |
| tool-use.md | 更新 | DeepSeek 内置工具与 Decision Models 接口相关 |
| codex-vs-claude-code.md | 更新 | 增加研究架构对照，并标明不能推断具体客户端功能 |
| enterprise-ai-economics.md | 更新 | 模型分工、任务成本与实际判断权相关 |
| education.md | 已读，不修改 | 本轮 Agent 后训练课程是模型工程资料，不属于现有主题的学生 / 教师 AI 应用范围 |
| news-media.md | 已读，不修改 | 新入库文章无新闻业或影响力行动专题 |
| international.md | 已读，不修改 | 本轮不涉及地域采用与国家合作证据 |
| README.md | 已读，不修改 | 既有主题索引有效，未新增主题 |

## 校验结果

```text
python ai_info/scripts/build_catalog.py
Wrote catalog.yaml with 562 articles
python ai_info/scripts/validate.py
Validation passed: 562 articles, 597 markdown files
```

## 说明与待补范围

1. **待补：BigModel 主站动态正文。** 本次读取只返回 JavaScript 提示；已检查官方研究列表、发布日志和旧 GLM 仓库。后续若主站恢复带日期技术正文，再与这三路比对，不能由列表空白推断未发布。
2. **本轮主题之外的文章不计入覆盖完成。** OpenAI 最新列表中的科研使用、医疗产品及商业合作，Anthropic 的科学模型 / 电子设计案例与漏洞披露时间政策，Google 的天气、基因和机器人新文章，Meta 的高校科研案例，以及 HF 的机器人、语音、企业合作与其他社区文章，未全部逐篇整理。后续应从本报告的旧锚点继续专题补录，不能仅用更新后的最大日期跳过这些窗口。
3. **可继续核查的具体官方入口**：[Anthropic 研究列表](https://www.anthropic.com/research)、[Google DeepMind 列表](https://deepmind.google/blog/)、[Meta 当前研究列表](https://research.meta.ai/)、[HF 当前与后续页](https://huggingface.co/blog?p=1)、[OpenAI 新闻](https://openai.com/news/)。本次不重复导入历史来源 URL。
4. **旧报告的历史待补项仍保留。** 本次新增没有覆盖此前的所有客户案例、早期 HF 漏项或其他专项跟踪；不能把新目录数量当作这些历史项已关闭的证据。
5. **数据口径。** 新文区分首发 / 更新日期、内部 / 外部评测、正式发布 / 权重可取得与研究架构 / 产品承诺；摘要中的工程建议标为解读。目录仍使用既有 `needs_review` 状态，不把本轮人工核验改写为全面独立复现。
