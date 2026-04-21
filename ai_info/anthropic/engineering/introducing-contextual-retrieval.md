# Introducing Contextual Retrieval

- **原文链接**: [Introducing Contextual Retrieval](https://www.anthropic.com/engineering/contextual-retrieval)
- **发布日期**: 2024-09-19
- **标签**: #RAG #检索 #嵌入 #BM25 #上下文

## 核心观点

Contextual Retrieval 是一种显著改善 RAG（检索增强生成）中检索步骤的方法。它使用两种子技术：**Contextual Embeddings** 和 **Contextual BM25**，可将检索失败率降低 49%，结合重排序后可降低 67%。这种"为每个检索块补充上下文"的思路，是 [Effective Context Engineering for AI Agents](effective-context-engineering-for-ai-agents.md) 中更广泛的上下文工程理念在检索领域的具体应用。

## 关键概念

### 问题背景
传统 RAG 将文档分割成块（chunks）进行嵌入和检索，但分割后的块丢失了文档级别的上下文，导致检索质量下降。

### Contextual Embeddings
在嵌入每个块之前，先让 LLM 为该块生成简短的上下文前缀，将该块置于整个文档的上下文中。每个块添加约 50-100 个 token 的上下文信息，使嵌入更准确地反映块的含义。

### Contextual BM25
将上下文信息也应用于 BM25（Best Matching 25）检索。BM25 是基于词法匹配的排序函数，利用 TF-IDF 概念，考虑文档长度和词频饱和函数。对包含唯一标识符或技术术语的查询特别有效。

### 重排序 (Reranking)
在检索结果上应用重排序进一步优化结果。结合 Contextual Embeddings + Contextual BM25 + 重排序，检索失败率从 5.7% 降至 1.9%。

## 实验数据

| 方法 | 检索失败率 |
|------|-----------|
| 基线 Embedding | 5.7% |
| Contextual Embedding | 3.7% (降低 35%) |
| Contextual Embedding + Contextual BM25 | 2.9% (降低 49%) |
| Contextual Embedding + cBM25 + Reranking | 1.9% (降低 67%) |

## 实践建议

- Contextual Embeddings 虽然提高了准确性，但在长文档场景下计算成本较高
- 嵌入每个块时需要完整文档上下文，可能截断关键信息
- 建议结合 BM25 和重排序以获得最佳效果
- [Building Agents with the Claude Agent SDK](building-agents-with-the-claude-agent-sdk.md) 中集成了检索能力，可直接在 Agent 中使用
- [Code Execution with MCP](code-execution-with-mcp.md) 展示了 MCP 中工具检索的另一种优化路径——通过代码执行避免将中间结果加载到上下文
