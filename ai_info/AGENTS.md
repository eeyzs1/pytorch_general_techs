# AGENTS.md — AI Info Knowledge Base 项目规则

> 本文件是 AI IDE（Trae / Cursor / Claude Code / Codex 等）在本项目工作时**必须遵守**的规则。
> Trae 用户需在 设置 > 规则 中开启"将 AGENTS.md 包含在上下文中"开关。本文件与 `.trae/rules/ai-info-sync.md` 内容同步，后者会被 Trae 自动加载。

## 0. 项目定位

`ai_info` 是一个**多厂商 AI 研究博客摘要库**——把 OpenAI、Anthropic、Google DeepMind、Meta AI 等厂商公开发布的研究 / 工程博客，整理为结构化中文摘要，按厂商 + 主题双索引组织。**不是**代码项目，**不是**新闻聚合——核心价值是跨厂商对比与可追溯原文链接。

## 1. 目录结构（不可变）

```
ai_info/
├── AGENTS.md                         ← 你正在读的文件（项目规则）
├── .trae/rules/ai-info-sync.md       ← Trae 原生规则（与 AGENTS.md 同步）
├── README.md                         ← 项目对外说明
├── catalog.yaml                      ← 自动生成，禁止手改 article 条目
├── scripts/
│   ├── build_catalog.py              ← 扫描所有文章生成 catalog.yaml
│   └── validate.py                   ← 校验链接、frontmatter、目录结构
├── {provider}/
│   ├── {category}/
│   │   └── {article-slug}.md         ← 文章摘要
│   └── summary.md                    ← 该 provider 的核心观点总结
├── topics/                           ← 跨厂商主题索引
│   ├── README.md
│   ├── agent-architecture.md
│   ├── context-engineering.md
│   ├── evals.md
│   ├── safety.md
│   ├── tool-use.md
│   └── codex-vs-claude-code.md
└── sync-report-YYYY-MM-DD.md         ← 每次同步写一份
```

**provider 取值**：`anthropic`、`openai`、`google`、`meta`、`huggingface`、`deepseek`、`glm`、`kimi`、`community`
**category 取值**：`research`、`engineering`、`blog`、`news`

## 2. 信源范围（必须全量检索）

每次同步**必须**检查以下信源，不允许跳过任何一家：

### 主流厂商（核心四家，每次必查）

| Provider | 信源 URL | 仓库目录 |
|----------|----------|----------|
| OpenAI | https://openai.com/research/ + https://openai.com/index/ | `openai/research/` |
| Anthropic | https://www.anthropic.com/research + https://www.anthropic.com/engineering | `anthropic/{research,engineering}/` |
| Google DeepMind | https://deepmind.google/discover/blog/ | `google/deepmind/` |
| Meta AI | https://ai.meta.com/blog/ | `meta/` |

### 开源社区（次要，每次必查但可有可无）

| Provider | 信源 URL | 仓库目录 |
|----------|----------|----------|
| Hugging Face | https://huggingface.co/blog | `huggingface/blog/` |
| DeepSeek | https://www.deepseek.com/ + https://api-docs.deepseek.com/ | `deepseek/news/` |

### 国内厂商（每次必查）

| Provider | 信源 URL | 仓库目录 |
|----------|----------|----------|
| DeepSeek | https://www.deepseek.com/ + https://api-docs.deepseek.com/ | `deepseek/news/` |
| GLM (智谱) | https://www.bigmodel.cn/ + https://github.com/THUDM/GLM-4 | `glm/blog/` |
| Kimi (Moonshot) | https://www.kimi.com/blog/ + https://platform.moonshot.cn/blog | `kimi/blog/` |

## 3. 同步工作流（必须按顺序执行）

### 步骤 1：建立同步锚点

**禁止凭印象判断"从哪开始找"**。必须先读 `catalog.yaml`，统计每个 provider 的最新 `published_at` 日期作为锚点。例如：

```python
# 伪代码
for provider in ['anthropic', 'openai', 'google', 'meta', ...]:
    latest = max(article.published_at for article in catalog if article.provider == provider)
    print(f"{provider}: latest = {latest}")
```

只检索**该日期之后**的新文章，避免重复入库。

### 步骤 2：检索新文章（并行）

对每个信源并行抓取列表页，对比锚点日期，列出需要新增的文章清单。**任何一家信源都不能跳过**——若抓取失败，必须在 sync-report 中明确说明，并标记为"待补"。

### 步骤 3：为每篇新文章创建摘要

每篇新文章必须创建独立的 markdown 文件，路径为 `{provider}/{category}/{article-slug}.md`。**article-slug** 用原文 URL 的最后一段（kebab-case），中文标题不直接做 slug。

文件结构必须包含以下字段（详见第 4 节）：

- 标题（中文翻译 + 原文标题英文括注）
- 原文链接、作者、发布日期、检索日期、标签
- 核心观点
- 关键发现 / 关键技术 / 关键数据
- 实践意义 / 跨厂商对比（必须 ≥1 个本仓库内文章链接）
- 资源链接（论文 / 代码 / demo）

### 步骤 4：更新派生文件（每次必须全部 review）

**禁止只更新部分派生文件**。每次同步必须 review 以下全部文件：

| 文件 | 更新内容 |
|------|----------|
| `catalog.yaml` | 运行 `python scripts/build_catalog.py` 自动重建 |
| `{provider}/summary.md` | 更新文章数、新增主题章节、关键数据点表、文章索引表 |
| `topics/*.md`（全部 7 个） | 详见第 5 节 |
| `sync-report-YYYY-MM-DD.md` | 写本次同步的范围、新增文章、更新内容、校验结果、说明 |

### 步骤 5：校验闭环

必须运行：

```bash
python scripts/build_catalog.py
python scripts/validate.py
```

**校验未通过禁止声称"同步完成"**。如果校验失败，必须修复后重新运行。

## 4. 文章摘要结构规范

每篇文章必须包含以下结构（缺一不可）：

```markdown
# {中文标题}

- **原文链接**: [{英文标题}]({URL})
- **作者**: {作者或团队}
- **发布日期**: {YYYY-MM-DD}
- **检索日期**: {YYYY-MM-DD}
- **标签**: #{tag1} #{tag2} #{tag3}（至少 3 个）

## 核心观点

{2-3 段，不超过 300 字。回答"这篇文章解决了什么问题、提出什么主张"}

## 关键发现 / 关键技术

### 1. {子主题}
{要点 + 数据}

### 2. {子主题}
{要点 + 数据}

## 实践意义

{对工程实践、跨厂商对比、未来方向的影响}

## 跨厂商对比

- 与 [{本仓库文章}]({相对路径}.md) 对比：{差异点}
- 与 [{本仓库文章}]({相对路径}.md) 互补：{互补点}

（必须 ≥1 个本仓库内文章链接）

## 资源

- 论文：{URL}
- 代码：{URL}
- Demo：{URL}
```

### Frontmatter 要求（catalog 自动扫描）

文件开头的字段列表（`- **原文链接**:` 等）会被 `build_catalog.py` 解析。**字段顺序和格式不可变**。

### 跨厂商对比链接的相对路径规则

- 同 provider 内：`{filename}.md`（同目录）
- 跨 provider：`../{provider}/{category}/{filename}.md`

例如从 `openai/research/foo.md` 链接到 Anthropic 文章：

```markdown
- 与 [Anthropic Agents in Biology](../../anthropic/research/agents-in-biology.md) 对比
```

## 5. topics 文件更新规则（每次全量 review）

`topics/` 下有 7 个主题文件，每次同步必须**逐个**判断新文章是否相关：

### 全量 review 流程

对每个 topic 文件，按以下顺序判断：

1. **读 topic 文件现有章节**——理解它当前覆盖哪些文章
2. **对每篇新文章判断**：该文章是否属于这个 topic？
3. **若相关**：加入对应章节，更新跨厂商对比链接
4. **若不相关**：跳过，但不要修改该 topic 文件
5. **若新文章创造新主题**：考虑是否新增 topic 文件（需要用户确认）

### 7 个 topic 的覆盖范围

| Topic | 覆盖范围 |
|-------|----------|
| `agent-architecture.md` | Agent 设计模式、长视野任务、Agent-first 团队、物理 Agent |
| `context-engineering.md` | 上下文窗口、记忆、检索、RAG、压缩 |
| `evals.md` | 评估方法、基准测试、专家级评估、系统级评估 |
| `safety.md` | 模型安全、对齐、网络安全、生物安全、部署前审计 |
| `tool-use.md` | 工具调用、MCP、ACI、工具组合、垂直化工具 |
| `codex-vs-claude-code.md` | Codex 与 Claude Code 对比、内部 Agent 部署、经济影响 |
| `README.md` | topics 索引（若新增 topic 文件需更新） |

### 必须避免的反模式

- ❌ **只更新部分 topic**："这次只更新 4 个，其余不动"——必须全量 review
- ❌ **凭直觉判断相关性**：必须读 topic 现有章节理解覆盖范围
- ❌ **跳过 README.md**：若新增 topic 文件，README.md 必须更新

## 6. sync-report 写作规范

每次同步必须创建 `sync-report-YYYY-MM-DD.md`，包含：

```markdown
# 官网同步记录：YYYY-MM-DD

## 同步范围

- {列出本次实际检查的所有信源 URL，包括抓取失败的}

## 新增文章（自 {上次同步日期} 上次同步以来）

### {Provider}（N 篇）

1. **{YYYY-MM-DD} | {标题}** — {一句话核心观点}
2. ...

### {Provider}（0 篇）

{说明为什么没有新文章，例如"blog 最新仍是 {date}，无新文章"}

## 更新内容

- `catalog.yaml` 从 {old} 篇更新为 {new} 篇
- `{provider}/summary.md`：{具体更新内容}
- `topics/{file}.md`：{具体更新内容}

## 校验结果

\`\`\`text
python scripts/build_catalog.py
Wrote catalog.yaml with {N} articles
python scripts/validate.py
Validation passed: {N} articles, {M} markdown files
\`\`\`

## 说明

- {本次遇到的限制：抓取失败的信源、未入库的文章原因}
- {跨厂商对比的新观察}
- {下次同步的待办}
```

## 7. 校验失败的处理

`validate.py` 检查以下内容，任何一项失败都必须修复：

1. **frontmatter 字段完整性**：每篇文章必须有 5 个必填字段
2. **链接有效性**：跨文章链接必须指向真实存在的文件
3. **目录结构**：文件必须在正确的 `{provider}/{category}/` 下
4. **catalog 一致性**：catalog.yaml 的条目数必须等于实际 markdown 文件数

## 8. 工作流禁忌

### ❌ 禁止行为

1. **跳过任何信源**——即便"上次同步没有新文章"，每次也必须检查
2. **凭印象判断"上次同步锚点"**——必须读 catalog.yaml 确认
3. **只更新部分 topics 文件**——必须全量 review
4. **手改 catalog.yaml**——必须用 `build_catalog.py` 重建
5. **校验未通过就声称完成**——必须运行 validate.py 并通过
6. **跨文章链接用绝对路径或反引号包文件名**——必须用相对路径 + 不带反引号的链接文本
7. **创建与现有文件结构不符的新文件**——必须按第 1 节目录结构
8. **在 sync-report 中轻描淡写"未跟进"**——必须说明具体原因和补救方案

### ✅ 必须行为

1. **每次同步前先读 AGENTS.md**（本文件）
2. **每次同步前先读 catalog.yaml 确定锚点**
3. **每个信源都抓取列表页，对比锚点日期**
4. **每篇文章必须包含跨厂商对比链接**
5. **每个 topics 文件必须 review**
6. **校验通过后才结束工作**
7. **sync-report 必须诚实记录失败和限制**

## 9. 当前已知的历史遗留问题

以下是历史遗留问题，按新规则应在后续同步中逐步修复：

1. **Google DeepMind 3-5 月缺失多篇文章**：catalog 中只有 9 篇，但 blog 上 3-5 月还有 "AI co-clinician"、"Republic of Korea partnership"、"Gemini 3.1 Flash TTS"、"Gemini Robotics-ER 1.6"、"Measuring progress toward AGI"、"10 years of AlphaGo's impact" 等未入库
2. **Meta AI 缺失部分 3-4 月文章**：如 "SAM 3.1"、"Alta Daily Uses SAM"
3. **OpenAI 5 月若干文章未补齐**：personal-finance-chatgpt、openai-launches-deployment-company、tanstack-npm 供应链攻击
4. **Hugging Face 尚未入库文章**：目录和 summary.md 已于 2026-07-20 创建，但尚无独立文章摘要——后续同步需补齐文章
5. **GLM 文章粒度不足**：`glm/blog/` 目前只有 summary.md（基于 bigmodel.cn 平台和 GitHub 整理），GLM 官方博客无结构化文章列表，后续需寻找更完整的信源渠道

下次同步应优先处理这些遗留问题。

## 10. 工作流快速检查清单

每次同步结束前，对照此清单逐项确认：

- [ ] 已读 catalog.yaml 确定每个 provider 的锚点日期
- [ ] 已检查全部信源（4 主流 + 2 开源社区 + 3 国内厂商）
- [ ] 每篇新文章都有完整 frontmatter（5 个字段）
- [ ] 每篇新文章都有跨厂商对比链接（≥1 个本仓库内链接）
- [ ] 已运行 `python scripts/build_catalog.py`
- [ ] 已运行 `python scripts/validate.py` 且通过
- [ ] 已更新所有相关 `{provider}/summary.md`
- [ ] 已 review 全部 7 个 `topics/*.md` 文件
- [ ] 已创建 `sync-report-YYYY-MM-DD.md`
- [ ] sync-report 中已说明所有抓取失败和未入库文章的原因
