# 官网同步记录：2026-06-29

## 同步范围

- OpenAI Index / Blog: https://openai.com/index/
- OpenAI Research: https://openai.com/research/
- Anthropic Engineering: https://www.anthropic.com/engineering（无新文章）
- Anthropic Research: https://www.anthropic.com/research

## 新增文章（自 2026-06-13 上次同步以来）

### OpenAI（13 篇）

1. **2026-06-14 | Introducing the OpenAI Partner Network** — $150M 投资，目标 2026 年底 30 万认证顾问；多专业服务（Forward Deployed Engineering、Foundry 部署、AI 平台工程）覆盖能源 / 制造 / 公共服务 / 金融 / 零售。
2. **2026-06-17 | Introducing LifeSciBench** — 750 任务 / 19,020 rubric 的生命科学专家级基准；173 名 Ph.D. 科学家撰写 + 453 名独立专家审查；覆盖 7 个工作流 + 7 个生物域，79% 任务多步推理、53% 任务需 artifact。
3. **2026-06-18 | New Usage Analytics and Updated Spend Controls for Enterprises** — Global Admin Console 统一 ChatGPT + Codex 信用额度视图；按用户 / 产品 / 模型维度分解的实时分析 + Cost API 自动化。
4. **2026-06-18 | Improving Health Intelligence in ChatGPT** — 2.3 亿周用户在 ChatGPT 咨询健康；GPT-5.5 Instant 健康性能接近 Thinking 模型；2 个月事实性问题下降 71%；70 万+ 医生审查回答。
5. **2026-06-22 | Daybreak: Tools for Securing Every Organization in the World** — Codex Security 已扫描 30M commits、30,000+ 代码库、500K+ 自动确认修复、70K+ 人工确认修复；GPT-5.5-Cyber 在 CyberGym 85.6%、ExploitGym 39.5%、SEC-bench Pro 69.8%；Trusted Access for Cyber 已覆盖 8+ 国家。
6. **2026-06-22 | Patch the Planet: A Daybreak Initiative** — "AI + 专家研究员"直接服务开源维护者；5 天冲刺已发现数百问题、合入数十补丁（Linux Kernel 指针泄露 PoC 8 个、本地提权 exploit 24 个、HTTP/2 Bomb 影响 88 万+ 网站）。
7. **2026-06-22 | Codex-Maxxing for Long-Running Work** — 长视野任务白皮书：持久化工作区（AGENTS.md + 状态）、可验证步骤（测试 + 编译）、人类监督判断（Plan / Diff / Steering）；回应 OpenAI 内部 80.6% 个人提交 30 分钟+ 任务的真实需求。
8. **2026-06-23 | How GPT-5 Helped Immunologist Derya Unutmaz Solve a 3-Year-Old Mystery** — GPT-5 Pro 作为科学合作者案例：解决 3 年未解的免疫学谜题（CCR5 调控 Th17 细胞表达 IL-17 的表观遗传学机制），成功预测未发表实验结果。
9. **2026-06-24 | OpenAI and Broadcom Unveil LLM-Optimized Inference Chip** — 发布 Jalapeño，OpenAI 首款自研 AI 加速器；9 个月 ASIC 设计周期；2026 年底起吉瓦级部署；与 AMD / NVIDIA 形成"自研 + 多供应商"策略。
10. **2026-06-25 | How Agents Are Transforming Work** — Codex 经济影响论文：97.9% 内部用户、99.8% 输出 token、80.6% 个人提交 30 分钟+ 任务、25.6% 提交 8 小时+ 任务、99 百分位日 Agent turn 60+ 小时；非开发者增长 137× / 189× / 12×。
11. **2026-06-26 | Previewing GPT-5.6 Sol: A Next-Generation Model** — GPT-5.6 三档模型（Sol/Terra/Luna）+ `max`/`ultra` 推理 effort；GPT-5.6 Sol 在 Terminal-Bench 2.1 91.9%、ExploitBench token 效率 1/3 Mythos Preview。
12. **2026-06-26 | GPT-5.6 Preview System Card** — 至今最强大安全栈：模型训练 + 激活分类器 + 实时监控 + 账户级信号 + 差异化访问；700,000+ A100e 小时自动 red team；新增 Sandbagging 类别作为 Preparedness 评估。
13. **2026-06-28 | HP Inc. Launches Frontier Strategic Partnership with OpenAI** — HP Frontier 全企业级 Codex 部署；几周内 122 PR / 43 项目；释放安全团队 82 小时/周产能；扩展至全球 11 国 600 万+ HP 工程师。

### Anthropic Research（7 篇）

1. **2026-06-03 | Mapping AI-enabled Cyber Threats: Insights from the LLM ATT&CK Navigator** — ARiES 风险评分；中高风险行为者占比 33% → 56%（半年）；MITRE ATT&CK 框架需扩展到 AI Agent 编排。
2. **2026-06-05 | Making Claude a Chemist** — Opus 4.7 化学 NMR 解释基准 vs 人类化学家 / ChemDraw / MestReNova；讨论 LLM 在领域专业工具上的"分布式专业能力"假设。
3. **2026-06-08 | Agents in Biology: Paving the Way for Autonomous Wet-Lab Discovery** — VirBench 120 查询的病毒学检索基准；Opus 4.7 准确率 91.3%，配合确定性工具接近 100%。
4. **2026-06-08 | Measuring LLMs' Impact on N-day Exploits** — Mythos Preview 在 Firefox（8/18 漏洞）和 Windows（8/21 漏洞）自动构建完整 exploit；N-day 利用的瓶颈已从"找漏洞"消失。
5. **2026-06-16 | Agentic Coding and Persistent Returns to Expertise** — 40 万 Claude Code 会话分析：70% 规划决策由人做、80% 执行决策由 Claude 做；编码能力不再是稀缺资源，领域专长才是。
6. **2026-06-18 | Project Fetch: Phase Two** — Opus 4.7 物理机器人在多个家居任务上比人类快 18-37 倍；通用 Agent 框架从数字域延伸至物理域。
7. **2026-06-26 | Economic Index June 2026 Report: Cadences** — 经济指数 6 月报告：按小时采样的工作节奏分析，揭示软件开发、知识工作、咨询的 Agent 使用模式差异。

### Anthropic Engineering（0 篇）

最近一篇仍是 2026-04-23 的 "An Update on Recent Claude Code Quality Reports"。Anthropic Engineering 6 月没有发布新文章。

## 更新内容

- `catalog.yaml` 从 86 篇更新为 99 篇。
- `openai/research/summary.md` 从 50 篇更新为 66 篇，重写"四路径演进"框架与六大主题。
- `anthropic/research/summary.md` 从 5 篇更新为 11 篇，新增"物理 Agent 跨域"主题与对比表。
- `topics/agent-architecture.md` 新增"长视野任务与 Agent-first 团队"章节。
- `topics/codex-vs-claude-code.md` 扩展至 19 个 OpenAI 链接 + 4 个 Anthropic 链接，新增"物理 Agent 与跨域延伸"和"经济部署"对比维度。
- `topics/context-engineering.md` 新增"长视野任务的上下文延续"章节。
- `topics/evals.md` 新增"专家级与系统级评估"章节。
- `topics/safety.md` 新增"网络安全纵深防御"章节。
- `topics/tool-use.md` 新增"工具组合与垂直化"、"网络安全与安全工具"、"跨域工具"三章节。

## 校验结果

```text
python ai_info/scripts/build_catalog.py
Wrote catalog.yaml with 99 articles
python ai_info/scripts/validate.py
Validation passed: 99 articles, 137 markdown files
```

## 说明

- OpenAI "A near-autonomous AI chemist improves a challenging reaction"（2026-06-17）页面在 WebFetch 时返回加载失败，未能获取完整内容。该文与 Anthropic "Making Claude a Chemist"（2026-06-05）同期涉及 AI 化学主题，留待下次同步补齐。
- Anthropic 6 月研究文章整体偏"跨域 Agent 应用"（化学、生物学、物理机器人、网络安全），与 OpenAI 6 月偏"GPT-5.6 模型 + Daybreak 安全"形成对照——可观察到大厂研究侧重点在 6 月开始分化。
- 5 月未补齐的若干 OpenAI 文章（personal-finance-chatgpt, testing-ads-in-chatgpt, openai-launches-deployment-company 等）本次仍未补齐，优先级仍低。
- Codex-Maxxing 白皮书发布与 OpenAI 内部经济数据形成互证：80.6% 个人用户提交 30 分钟+ 任务的需求推动了"持久化工作区 + 可验证步骤 + 人类监督"的工程范式。
