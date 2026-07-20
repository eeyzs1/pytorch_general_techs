# 官网同步记录：2026-07-20

## 同步范围

本次同步严格按 [AGENTS.md](AGENTS.md) 规则执行，覆盖全部信源：

- OpenAI Research: https://openai.com/research/
- OpenAI Index: https://openai.com/index/
- Anthropic Engineering: https://www.anthropic.com/engineering
- Anthropic Research: https://www.anthropic.com/research
- Google DeepMind: https://deepmind.google/discover/blog/
- Meta AI: https://ai.meta.com/blog/
- Hugging Face: https://huggingface.co/blog（抓取失败）
- DeepSeek: https://www.deepseek.com/ + https://api-docs.deepseek.com/
- GLM (智谱): https://www.bigmodel.cn/ + https://github.com/THUDM/GLM-4
- Kimi (Moonshot): https://www.kimi.com/blog/ + https://platform.moonshot.cn/blog

> 注：Mistral 信源在本次同步后经用户确认移除，不再纳入同步范围。

## 同步锚点

启动时已读 `catalog.yaml` 确定各 provider 锚点：

| Provider | 锚点日期（同步前） | 锚点日期（同步后） |
|----------|---------------------|---------------------|
| openai | 2026-06-30 | 2026-07-09 |
| anthropic | 2026-07-06 | 2026-07-14 |
| google | 2026-05-19 | 2026-05-19（无新文章） |
| meta | 2026-06-29 | 2026-06-29（无新文章） |
| kimi | 无 | 2026-07-16（新 provider） |
| deepseek | 无 | 2026-06-29（新 provider） |
| huggingface | 无 | 无（抓取失败） |
| glm | 无 | 2025-07-04（无结构化文章列表） |

## 新增文章

### OpenAI（5 篇）

1. **2026-07-09 | [GPT-5.6（Introducing GPT-5.6）](openai/research/introducing-gpt-5-6.md)** — 可扩展智能发布：默认高效模式 + `max`/`ultra` 推理 effort，Codex 基础设施上训练，System Card 首次纳入 Sandbagging 评估。
2. **2026-07-09 | [ChatGPT Work](openai/research/chatgpt-work-partner.md)** — ChatGPT 升级为跨应用工作伙伴：操作应用和文件、陪伴项目数小时，与 Codex 形成"通用工作 + 编码专用"双轨产品矩阵。
3. **2026-07-08 | [GPT-Live（Introducing GPT-Live）](openai/research/introducing-gpt-live.md)** — 实时语音对话模型：全双工、情感感知、可打断，代表语音 Agent 从回合制到真正实时交互的跃迁。
4. **2026-07-09 | [OpenAI Bio Bug Bounty](openai/research/bio-bug-bounty.md)** — 生物安全通用越狱测试升级为持续计划，奖励提升至 $50,000，专注能击败预定义生物安全挑战的通用方法。
5. **2026-07-08 | [Separating Signal from Noise in Coding Evaluations](openai/research/separating-signal-from-noise-coding-evaluations.md)** — 对 SWE-Bench Pro 的独立审计：58.7% 可复现率，揭示 benchmark 污染与工程代理问题的系统性风险。

### Anthropic（4 篇）

1. **2026-07-14 | [How Canada Uses Claude](anthropic/research/how-canada-uses-claude.md)** — 加拿大 Claude 使用情况经济指数报告：67% 用户为女性，经济影响集中在医疗、金融和政府领域。
2. **2026-07-13 | [Claude Values: Models and Languages](anthropic/research/claude-values-models-languages.md)** — 跨模型、跨语言价值观一致性研究：Claude 在价值观表达上比 GPT-4o 更一致，但小语种（如老挝语）可靠性下降。
3. **2026-07-09 | [Claude Plays Robotics](anthropic/research/claude-plays-robotics.md)** — 首次大规模评估 LLM 控制多种机器人身体的能力：控制抽象层级决定成败——直接扭矩控制大多失败，预训练策略 + LLM 高层规划是最可行路径。
4. **2026-07-08 | [An Off Switch for Dual-Use Knowledge](anthropic/research/off-switch-dual-use.md)** — GRAM 模块化预训练：单次训练实现 16 种能力配置，删除模块效果接近从未训练且不影响通用能力，为差异化 AI 部署提供新范式。

### Kimi（3 篇，新 provider）

1. **2026-07-16 | [Kimi K3](kimi/blog/kimi-k3.md)** — 2.8T 参数、原生多模态、100 万 token 上下文，全球首个开源 3T 级模型。基于 KDA 和 AttnRes 架构，标志着开源与闭源模型的规模差距正在缩小。
2. **2026-07-16 | [PerceptionBench](kimi/blog/perception-bench.md)** — 从模型失败中"发现"10 种原子感知能力的诊断式评估基准。核心发现：无模型超过 60% 准确率，大量正确答案无法复现——当前多模态模型经常猜测而非真正感知。
3. **2026-04-20 | [Kimi K2.6](kimi/blog/kimi-k2-6.md)** — 开源编码 Agent SOTA：12+ 小时连续执行、4000+ 工具调用，用 Zig 优化 Qwen3.5-0.8B 推理吞吐量提升 13 倍，自主重构 8 年历史金融引擎。

### DeepSeek（2 篇，新 provider）

1. **2026-04-24 | [DeepSeek-V4](deepseek/news/deepseek-v4.md)** — V3 之后 484 天的旗舰迭代：V4-Pro（1.6T / 49B 激活）+ V4-Flash（284B / 13B 激活）双模型、1M 上下文、单 token FLOPs 仅 V3.2 的 27%、KV cache 压至 10%。mHC + CSA/HCA + Engram 三大架构创新，MIT 开源，优先适配华为昇腾。
2. **2026-06-29 | [DeepSeek-V4 API 定价与峰谷计费](deepseek/news/deepseek-v4-api-pricing.md)** — 首次引入峰谷计费（高峰 9:00-12:00 / 14:00-18:00 价格 ×2）；V4-Flash 输出 $0.28/1M token、缓存命中 $0.0028；旧模型名 `deepseek-chat` / `deepseek-reasoner` 2026-07-24 废弃。

### Google DeepMind（0 篇）

blog 第一页最新文章仍为 2026-05-19（"Reimagining the mouse pointer for the AI era"），6-7 月无新文章。但 catalog 中 google/deepmind 仍有多篇历史遗留未入库（AI co-clinician、Republic of Korea partnership、Gemini 3.1 Flash TTS、Gemini Robotics-ER 1.6、Measuring progress toward AGI、10 years of AlphaGo's impact 等），留待下次同步处理。

### Meta AI（0 篇）

blog 最新文章仍为 2026-06-29（"Brain2Qwerty v2"），7 月无新文章。历史遗留文章（SAM 3.1、Alta Daily Uses SAM 等）仍未补齐。

### 开源社区（0 篇）

- Hugging Face blog：WebFetch 抓取失败

已为 Hugging Face 创建目录和 `summary.md` 占位文件，尚未入库独立文章，留待后续同步尝试。

### GLM（0 篇独立文章）

GLM 官方博客无结构化文章列表，仅基于 bigmodel.cn 平台和 GitHub 创建了 `glm/blog/summary.md`。后续需寻找更完整的信源渠道。

## 更新内容

### 目录结构变更

- 新建 `kimi/blog/` 目录，含 3 篇文章 + `summary.md`
- 新建 `deepseek/news/` 目录，含 2 篇文章 + `summary.md`
- 新建 `glm/blog/` 目录，含 `summary.md`
- 新建 `huggingface/blog/` 目录，含 `summary.md`
- ~~`mistral/`~~ 目录曾创建后经用户确认移除，不再纳入同步

### 派生文件更新

- `catalog.yaml`：从 133 篇更新为 **140 篇**
- `openai/research/summary.md`：更新文章数（74 篇）、新增 GPT-5.6 / GPT-Live / ChatGPT Work / Bio Bug Bounty / SWE-Bench Pro 审计章节
- `anthropic/research/summary.md`：更新文章数（17 篇）、新增 How Canada Uses Claude / Claude Values / Claude Plays Robotics / GRAM 章节
- `kimi/blog/summary.md`：新建，涵盖 Kimi K3 / K2.6 / PerceptionBench 核心观点与跨厂商对比
- `deepseek/news/summary.md`：新建，涵盖 DeepSeek-V4 双模型 / 架构创新 / 峰谷计费 / 国产算力策略
- `glm/blog/summary.md`：新建，基于 bigmodel.cn 平台和 GitHub 整理的 GLM 概况
- `huggingface/blog/summary.md`：新建（占位）
- `topics/agent-architecture.md`：新增 ChatGPT Work、Claude Plays Robotics、Kimi K2.6、DeepSeek-V4
- `topics/evals.md`：新增 SWE-Bench Pro 审计、PerceptionBench、DeepSeek-V4 SWE-bench 数据点
- `topics/safety.md`：新增 OpenAI Bio Bug Bounty、Anthropic GRAM
- `topics/codex-vs-claude-code.md`：新增 GPT-5.6、GPT-Live、ChatGPT Work、DeepSeek-V4；补充产品矩阵、开源竞争与成本结构结论
- `topics/context-engineering.md`：新增 Claude Values 跨模型语言一致性、DeepSeek-V4 百万上下文工程化
- `AGENTS.md`：更新 provider 取值（加入 `glm`、`kimi`、`deepseek`；移除 `mistral`）、新增"国内厂商"信源表、更新历史遗留问题
- `.trae/rules/ai-info-sync.md`：同步上述 AGENTS.md 变更

## 校验结果

```text
$ python scripts/build_catalog.py
Wrote catalog.yaml with 140 articles
$ python scripts/validate.py
Validation passed: 140 articles, 164 markdown files
```

## 说明

### 限制与失败

- **Meta AI（https://ai.meta.com/blog/）**：WebFetch 抓取失败（连接超时），无法确定 7 月是否有新文章。已确认 6-29 的 "Brain2Qwerty v2" 已入库。
- **Hugging Face（https://huggingface.co/blog）**：WebFetch 抓取失败，无法获取文章列表。
- **DeepSeek 官方公众号文章**：mp.weixin.qq.com 链接无法直接抓取，V4 架构细节通过官网首页横幅、API 文档和多家媒体报道交叉验证。
- **GLM**：无官方结构化博客文章列表，当前 `glm/blog/summary.md` 仅基于 bigmodel.cn 平台和 GitHub 信息整理，文章粒度不足。

### 修正记录

- **DeepSeek 信源 URL 修正**：初次同步误用 `https://api-docs.deepseek.com/news`（404）。经用户指出后，改用 `https://www.deepseek.com/` + `https://api-docs.deepseek.com/` 成功获取 V4 全部信息——DeepSeek 作为国内公司，官方渠道信息完整可得，此前"无法获取"的判断错误。
- **Mistral 移除**：应用户要求，Mistral 从信源范围中移除，目录已删除。
- **论文原文补充（2026-07-20 二次更新）**：用户指出部分技术细节为推断，已检索并基于以下论文原文重写：
  - `deepseek-v4.md`：mHC（arXiv:2512.24880）、Engram（arXiv:2601.07372）部分重写为论文原文细节；CSA/HCA 基于 DeepSeek-V4 完整技术报告（arXiv:2606.19348）重写
  - `off-switch-dual-use.md`：补全 GRAM 梯度路由机制、训练成本 5x、0.25% 数据占比、128M token 恢复攻击局限
  - `kimi-k3.md`：补全 KDA（arXiv:2510.26692）公式/3:1 混合/6.3x 吞吐、AttnRes（arXiv:2603.15031）公式/Block AttnRes/25% 效率提升、Stable LatentMoE 四大技术（Quantile Balancing、Per-Head Muon、SiTU、Gated MLA）
  - `deepseek/summary.md`、`kimi/summary.md`：同步更新技术描述

### 跨厂商对比新观察

1. **产品矩阵竞争**：OpenAI 已形成 "ChatGPT Work（通用工作）+ Codex（编码专用）" 双轨，Anthropic 保持 Claude Code 单点深化，Kimi 以 K2.6（开源编码 Agent）和 K3（开源旗舰）进入竞争，DeepSeek 以 V4（Opus 级能力 + 1/7 价格）从成本侧夹击，GLM 以"开源 + 商业化"双轨差异化。
2. **开源阵营内部分化**：Kimi K3（2.8T）走"最大规模"路线，DeepSeek V4（1.6T + 27% 计算量）走"效率优先"路线——开源不再只是"追赶闭源"，开始出现独立的架构哲学。
3. **物理 Agent 成为新战场**：Anthropic 的 Claude Plays Robotics 与 OpenAI 的 Codex 物理 Agent 探索形成对照——控制抽象层级是 LLM 控制物理系统的关键瓶颈。
4. **评估诊断化趋势**：Kimi PerceptionBench 从"模型失败中诊断原子能力"的思路，与 OpenAI GeneBench-Pro（研究级基准）、Anthropic BrowseComp（Agent 评估）形成互补——评估正从"打分"转向"诊断"。
5. **成本工程成为竞争力**：DeepSeek 峰谷计费 + 缓存命中 $0.0028/1M token 把"何时调用、如何复用上下文"变成了架构决策——Agent 成本模型需要按实时/离线重新设计。

### 下次同步待办

1. 优先补齐 Google DeepMind 历史遗留文章（AI co-clinician 等 6 篇）
2. 补齐 Meta AI 历史遗留文章（SAM 3.1、Alta Daily Uses SAM）
3. 补齐 OpenAI 5 月历史遗留文章（personal-finance-chatgpt 等）
4. 重新尝试抓取 Hugging Face 信源
5. 为 GLM 寻找更完整的结构化信源渠道
6. 跟踪 DeepSeek-V4 GA 正式版发布（预计 7 月中旬，`deepseek-chat` / `deepseek-reasoner` 7-24 废弃）
