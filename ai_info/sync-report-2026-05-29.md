# 官网同步记录：2026-05-29

## 同步范围

本次只使用官方来源做内容增量：

- Anthropic Engineering: https://www.anthropic.com/engineering
- OpenAI Research: https://openai.com/research/
- OpenAI Blog / Index: https://openai.com/index/

## 新增文章

### Anthropic

- [How We Built a System to Contain Claude Across Products](anthropic/engineering/how-we-contain-claude-across-products.md)

### OpenAI

- [Introducing GPT-5.3-Codex](openai/research/introducing-gpt-5-3-codex.md)
- [Introducing GPT-5.3-Codex-Spark](openai/research/introducing-gpt-5-3-codex-spark.md)
- [Introducing GPT-5.5](openai/research/introducing-gpt-5-5.md)
- [GPT-5.5 Instant](openai/research/gpt-5-5-instant.md)
- [Introducing OpenAI Privacy Filter](openai/research/introducing-openai-privacy-filter.md)
- [Advancing Voice Intelligence with New Models in the API](openai/research/advancing-voice-intelligence-with-new-models-in-the-api.md)
- [An OpenAI Model Has Disproved a Central Conjecture in Discrete Geometry](openai/research/model-disproves-discrete-geometry-conjecture.md)
- [Strengthening Societal Resilience with Rosalind Biodefense](openai/research/strengthening-societal-resilience-with-rosalind-biodefense.md)
- [Work with Codex from Anywhere](openai/research/work-with-codex-from-anywhere.md)
- [OpenAI and Dell Technologies Partner to Bring Codex to Hybrid and On-Premises Enterprise Environments](openai/research/dell-codex-enterprise-partnership.md)
- [OpenAI Named a Leader in Enterprise Coding Agents by Gartner](openai/research/gartner-2026-agentic-coding-leader.md)

## 更新内容

- `catalog.yaml` 从 48 篇更新为 60 篇。
- `anthropic/engineering/summary.md` 从 25 篇更新为 26 篇。
- `openai/research/summary.md` 从 23 篇更新为 34 篇。
- `anthropic/engineering/scaling-managed-agents.md` 根据官网补齐作者，并将发布日期修正为 `2026-04-08`。
- `topics/` 下的 Agent 架构、上下文工程、评估、安全、工具使用、Codex 对比路线已加入新增文章。

## 校验结果

```text
python3 ai_info/scripts/build_catalog.py
python3 ai_info/scripts/validate.py
Validation passed: 60 articles, 71 markdown files
```

## 说明

OpenAI 部分官方页面对命令行 `curl` 请求可能返回 403，因此本次以官方网页检索和可打开页面为准；未使用第三方博客或新闻源。
