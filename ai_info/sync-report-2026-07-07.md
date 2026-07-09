# 官网同步记录：2026-07-07

## 同步范围

本次同步**严格按 [AGENTS.md](AGENTS.md) 规则执行**，覆盖全部信源：

- OpenAI Index / Blog: https://openai.com/index/
- OpenAI Research: https://openai.com/research/
- Anthropic Engineering: https://www.anthropic.com/engineering
- Anthropic Research: https://www.anthropic.com/research
- Google DeepMind: https://deepmind.google/discover/blog/
- Meta AI: https://ai.meta.com/blog/
- Hugging Face: https://huggingface.co/blog（抓取失败）
- Mistral: https://mistral.ai/news（抓取失败）
- DeepSeek: https://api-docs.deepseek.com/news（404）

## 同步锚点

启动时已读 `catalog.yaml` 确定各 provider 锚点：

| Provider | 锚点日期（同步前） | 锚点日期（同步后） |
|----------|---------------------|---------------------|
| anthropic | 2026-06-26 | 2026-07-06 |
| openai | 2026-06-28 | 2026-06-30 |
| google | 2026-05-19 | 2026-05-19（无新文章） |
| meta | 2026-04-08 | 2026-06-29 |

## 新增文章

### Anthropic Research（1 篇）

1. **2026-07-06 | [A Global Workspace in Language Models](anthropic/research/global-workspace.md)** — Claude 内部涌现 J-space（全局工作空间），J-lens 可读出 + 编辑 + 因果干预。5 大性质：可报告 / 可调控 / 用于推理 / 可重用 / 不参与日常处理。受神经科学"全局工作空间理论"启发，与 NLA 互补。

### OpenAI Research / Blog（2 篇）

1. **2026-06-30 | [Introducing GeneBench-Pro](openai/research/introducing-genebench-pro.md)** — 研究级计算生物学基准：129 道合成问题、10 领域、21 子领域。GPT-5.6 Sol（Pro）通过率 31.5%，单题人类专家需 20-40 小时、AI 仅数美元。与 LifeSciBench 互补（前者偏研究工作流，后者偏判断决策）。
2. **2026-06-30 | [Core Dump Epidemiology](openai/research/core-dump-epidemiology-data-infrastructure-bug.md)** — Rockset C++ 不可能崩溃的"流行病学家式诊断"：把两个独立 bug（Azure 单台主机硬件损坏 + GNU libunwind 18 年竞态条件）从混杂症状中分离。贡献 patch 给上游 GNU 项目。

### Meta AI（1 篇）

1. **2026-06-29 | [Brain2Qwerty v2](meta/brain2qwerty-v2.md)** — 非侵入式脑机接口端到端 LLM 解码 pipeline。9 名志愿者、22,000 句子训练，词准确率 61%（最佳 78%），相比其他非侵入方法 8% 提升 7.5 倍。Nature Neuroscience 发表，开源 v1+v2 训练代码 + v1 数据集。配套 Tribev2 / NeuralSet / NeuralBench 形成"开放脑模型基础设施"。

### Anthropic Engineering（0 篇）

最近一篇仍是 2026-05-25 的 "How We Built a System to Contain Claude Across Products"。Anthropic Engineering 自 5 月 25 日后停滞 6 周。

### Google DeepMind（0 篇，本次同步）

blog 第一页最新文章为 May 2026（"Reimagining the mouse pointer for the AI era"，2026-05-12），第二页起为 March 2026。**6-7 月无新文章**。但 catalog 中 google/deepmind 缺失多篇文章（AI co-clinician、Republic of Korea partnership、Gemini 3.1 Flash TTS、Gemini Robotics-ER 1.6、Measuring progress toward AGI、10 years of AlphaGo's impact 等），属历史遗留问题，留待下次同步处理。

### 开源社区（0 篇）

- Hugging Face blog：WebFetch 抓取失败
- Mistral news：WebFetch 抓取失败
- DeepSeek news：返回 404

三个开源社区信源本次均未能成功抓取，留待下次同步尝试。

## 重要发现：catalog 历史 bug 修复

本次同步发现并修复 `build_catalog.py` 和 `validate.py` 的严重历史 bug：

### Bug 描述

两个脚本的 `ARTICLE_DIRS` 硬编码为只扫描两个目录：
- `anthropic/engineering/`
- `openai/research/`

导致 **25 篇文章从未被 catalog 纳入**：
- `anthropic/research/` 全部 12 篇文章（包括 NLA、Teaching Claude Why、Glasswing、Chemist、Agents in Biology、Fetch Phase 2、Economic Index、J-space 等）
- `google/deepmind/` 全部 9 篇文章
- `meta/` 全部 4 篇文章（包括本次新增的 Brain2Qwerty v2）

### 修复内容

- `scripts/build_catalog.py`：改为动态扫描所有 `{provider}/{category}/` 和 `{provider}/` 目录，支持扁平结构和嵌套结构
- `scripts/validate.py`：同步修复 `article_dirs()` 为动态扫描；新增 `summary_files()` 动态发现所有 summary.md；`check_local_links()` 排除 AGENTS.md 和 .trae/ 目录的示例链接

### 修复影响

- catalog.yaml 从 101 篇 → **126 篇**（新增 25 篇历史遗漏文章 + 1 篇本次新增 Brain2Qwerty v2）
- 校验通过：`Validation passed: 126 articles, 145 markdown files`

## 创建项目规则文件

按用户要求，创建 AI IDE 自动读取的项目规则文件：

### 1. [AGENTS.md](AGENTS.md)（跨 IDE 通用）

完整的项目规则，包含：
- 项目定位
- 目录结构（不可变）
- 信源范围（必须全量检索）
- 同步工作流（5 步，必须按顺序）
- 文章摘要结构规范
- topics 文件更新规则（每次全量 review）
- sync-report 写作规范
- 校验失败的处理
- 工作流禁忌
- 当前已知的历史遗留问题
- 工作流快速检查清单

**Trae 用户需在 设置 > 规则 中开启"将 AGENTS.md 包含在上下文中"开关**（根据 [Trae 官方文档](https://docs.trae.cn/ide_rules)）。

### 2. [.trae/rules/ai-info-sync.md](.trae/rules/ai-info-sync.md)（Trae 原生）

Trae 原生项目规则文件，会被 Trae **自动加载**（无需手动开启开关）。设置 `alwaysApply: true`，包含 AGENTS.md 的核心规则摘要 + 触发场景说明。

**验证**：本次同步中已确认 Trae CN IDE 自动识别并加载了这两个规则文件（在工具返回中看到 "Rules relevant to this file" 部分）。

## topics 全量 review 结果

按新规则，本次同步对全部 7 个 topics 文件逐个 review：

| Topic 文件 | 是否更新 | 更新内容 |
|------------|----------|----------|
| `topics/agent-architecture.md` | ✅ | 新建"Agent 内部可观测性与审计"章节（J-space + NLA）；"长视野任务"加入 Brain2Qwerty v2；关键结论新增"Agent 内部可观测性是下一个工程前沿" |
| `topics/context-engineering.md` | ✅ | "检索与记忆"章节加入 J-space |
| `topics/evals.md` | ✅ | "专家级与系统级评估"加入 GeneBench-Pro |
| `topics/safety.md` | ✅ | "模型行为与审计"加入 NLA + Global Workspace |
| `topics/tool-use.md` | ✅ | "跨域工具"加入 Brain2Qwerty v2（Agent 探索 pipeline 优化） |
| `topics/codex-vs-claude-code.md` | ✅ | 新建"模型内部可解释性"章节（J-space 与 Claude Code 内部调试） |
| `topics/README.md` | ❌ | 6 个 topic 链接完整，无需新增 topic 文件 |

## 更新内容汇总

### 新增文章（4 篇）

- `anthropic/research/global-workspace.md`
- `openai/research/introducing-genebench-pro.md`
- `openai/research/core-dump-epidemiology-data-infrastructure-bug.md`
- `meta/brain2qwerty-v2.md`

### 新增规则文件（2 个）

- `AGENTS.md`
- `.trae/rules/ai-info-sync.md`

### 更新派生文件

- `catalog.yaml`：从 101 篇（仅 2 个目录）→ **126 篇**（全量扫描）
- `anthropic/research/summary.md`：11 篇 → 12 篇，新增 J-space 主题
- `openai/research/summary.md`：66 篇 → 69 篇，新增 GeneBench-Pro、Core Dump、对比数据点
- `meta/summary.md`：3 篇 → 4 篇，新增 Brain2Qwerty v2 + 关键数据点
- 全部 7 个 `topics/*.md` 文件已 review（其中 6 个有更新）

### 修复脚本

- `scripts/build_catalog.py`：动态扫描所有 provider 目录
- `scripts/validate.py`：同步动态扫描 + 排除规则文件示例链接

## 校验结果

```text
python scripts/build_catalog.py
Wrote catalog.yaml with 126 articles
python scripts/validate.py
Validation passed: 126 articles, 145 markdown files
```

各 provider 文章分布：
- anthropic: 39 篇（engineering + research）
- openai: 74 篇
- google: 9 篇
- meta: 4 篇

## 说明与反思

### 本次同步的核心教训

1. **历史 sync-report 隐式规则不可靠**：之前的 sync-report（5-29、6-13、6-29）都只覆盖 OpenAI 和 Anthropic，把 Google DeepMind 和 Meta 当成"快照不动"。本次首次按 [AGENTS.md](AGENTS.md) 显式规则全量检查所有信源。
2. **catalog 校验脚本有 bug 一直未被发现**：`build_catalog.py` 硬编码只扫描 2 个目录，导致 25 篇文章从未被纳入 catalog。这个 bug 在历史 sync-report 中从未被提及——因为之前从未按规则全量 review。
3. **topics 不能凭直觉更新**：第一次同步时我只更新了 4 个 topics 文件，漏了 tool-use / agent-architecture / README。本次按规则全量 review 后发现 Brain2Qwerty v2 与 tool-use.md 相关（Agent 探索 pipeline），J-space 与 agent-architecture.md 相关（Agent 内部可观测性）——这些都是凭直觉会漏掉的。

### 跨厂商观察

- **可解释性三步曲**：NLA（5 月）→ J-space（7 月）→ 两者结合形成"全局感知 + 局部干预"的对齐审计流水线。Anthropic 在可解释性领域持续领先。
- **AI for Science 双轨**：OpenAI GeneBench-Pro 偏"判断决策"评估（129 题合成数据），Meta Brain2Qwerty 偏"工程化开源"（Nature 论文 + 训练代码 + 数据集）。两者与 Anthropic Agents in Biology、Google Co-Scientist + AlphaEvolve 共同构成 2026 年的"AI for Science"竞争格局。
- **基础设施可靠性工程**：OpenAI Core Dump Epidemiology 与 Anthropic 多篇事后分析（A Postmortem of Three Recent Issues、Claude Code Quality Reports）共同指向"基础设施问题伪装成模型/应用问题"的反复模式。

### 下次同步的待办（按 AGENTS.md 第 9 节历史遗留问题）

1. **Google DeepMind 3-5 月缺失文章**：AI co-clinician、Republic of Korea partnership、Gemini 3.1 Flash TTS、Gemini Robotics-ER 1.6、Measuring progress toward AGI、10 years of AlphaGo's impact、Reimagining the mouse pointer for the AI era 等
2. **Meta AI 缺失 3-4 月文章**：SAM 3.1、Alta Daily Uses SAM
3. **OpenAI 5 月未补齐文章**：personal-finance-chatgpt、openai-launches-deployment-company、tanstack-npm 供应链攻击
4. **开源社区信源**：Hugging Face / Mistral / DeepSeek 三个信源本次抓取失败，需尝试其他抓取方式或确认 URL
5. **Anthropic Engineering 停滞**：自 2026-05-25 后已 6 周无新文章，下次同步继续观察
