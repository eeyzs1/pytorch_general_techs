# AI Info Knowledge Base

这个目录收集 AI Agent、Codex、Claude Code、评估、安全、工具使用等方向的官方技术文章摘要。目标不是简单搬运博客，而是沉淀一个可校验、可检索、可持续更新的知识库。

## 目录结构

```text
ai_info/
  anthropic/engineering/   # Anthropic Engineering 文章摘要
  openai/research/         # OpenAI Research / Blog 文章摘要
  topics/                  # 跨厂商主题索引与对比阅读路线
  scripts/                 # 元数据生成与质量校验脚本
  catalog.yaml             # 从文章元数据生成的统一索引
```

## 推荐阅读路线

- 快速总览：先读 `anthropic/engineering/summary.md` 和 `openai/research/summary.md`。
- 按主题学习：从 `topics/` 进入，例如 Agent 架构、上下文工程、评估、安全、工具使用。
- 查找原文：优先从 `catalog.yaml` 找 `source_url`，再回到对应 Markdown 摘要。

## 维护规范

每篇文章摘要建议保留以下信息：

- 原文链接：官方 URL，避免二手来源。
- 作者：没有明确作者时可以留空，但不要伪造。
- 发布日期：尽量使用 `YYYY-MM-DD`；原文只给月份时可用 `YYYY-MM`。
- 标签：用少量高信号标签，便于主题聚合。
- 核心观点：先写原文事实，再写自己的解读。
- 相关文章：只链接仓库内已存在的文章，避免死链。

## 常用命令

```bash
# 重新生成统一索引
python3 ai_info/scripts/build_catalog.py

# 本地质量校验
python3 ai_info/scripts/validate.py
```

## 质量门禁

`validate.py` 会检查：

- Markdown 是否包含 UTF-8 BOM。
- OpenAI 目录是否误写为 `reserch`。
- 本地 Markdown 链接是否存在。
- 文章是否具备标题、原文链接、发布日期、标签。
- `catalog.yaml` 是否覆盖所有文章且没有重复来源 URL。
- 总结页的数字标题是否递增。

外部链接状态不默认校验，因为部分官方站点会对命令行请求返回 403；需要时可单独人工抽查。
