# Advanced Tool Use

- **原文链接**: [Advanced tool use](https://www.anthropic.com/engineering/advanced-tool-use)
- **作者**: Bin Wu 等
- **发布日期**: 2025-11-24
- **标签**: #工具搜索 #程序化工具调用 #工具示例 #Token优化 #Beta特性

## 核心观点

Anthropic 发布了三个从根本上改变 Agent 与工具交互方式的 Beta 特性：**Tool Search Tool**（动态发现）、**Programmatic Tool Calling**（代码编排）和 **Tool Use Examples**（从具体模式学习）。它们共同解决了管理数百个工具而不压垮上下文窗口的问题。这是 [Writing Effective Tools for AI Agents](writing-effective-tools-for-ai-agents.md) 五大原则的技术实现——当工具数量增长到数十个以上时，需要更高级的机制来维持效率和准确率。

## 三大特性详解

### 1. Tool Search Tool（工具搜索工具）
- **Token 减少**: 85%（77K → 8.7K token）
- **准确率提升**: Opus 4 从 49% → 74%；Opus 4.5 从 79.5% → 88.1%
- **机制**: 用 `defer_loading: true` 标记工具，将其排除在初始提示之外。Claude 在需要时搜索工具，只加载相关工具
- **系统提示**提供关于可用工具类别的高级指导
- **不破坏提示缓存**: 延迟加载的工具完全排除在初始提示之外
- Tool Search Tool 是 [Effective Context Engineering for AI Agents](effective-context-engineering-for-ai-agents.md) 中即时上下文检索策略在工具层面的实现——只加载当前需要的工具定义

### 2. Programmatic Tool Calling（程序化工具调用，PTC）
- **Token 减少**: 复杂研究任务上 37%；将 200KB 原始数据减少到 1KB 结果
- **机制**: 让 Claude 编写 Python 代码编排工具，只有最终输出进入上下文
- **优势**: 每次传统工具调用需要完整推理轮次；PTC 用单次代码执行替代多次推理轮次
- **支持异步**: 可使用 `asyncio.gather` 并行调用多个工具
- PTC 与 [Code Execution with MCP](code-execution-with-mcp.md) 的代码执行范式一脉相承——都是通过代码编排避免中间结果进入上下文

### 3. Tool Use Examples（工具使用示例）
- **准确率提升**: 复杂参数处理从 72% → 90%
- **机制**: 通过 `input_examples` 字段在工具定义中嵌入具体示例调用
- **三种模式**: 完整示例（关键 Bug 含升级信息）、部分示例（功能请求）、最小示例（内部任务）
- 示例是 [Effective Context Engineering for AI Agents](effective-context-engineering-for-ai-agents.md) 中"示例是值千言的图片"原则的体现

### 组合使用
三个特性可以组合使用，在 `betas` 参数中启用。

## 实践启示

- 当工具数量超过几十个时，Tool Search Tool 是必需的
- PTC 特别适合需要多步数据处理的场景（如遍历团队→获取预算→计算超支）
- 工具示例应覆盖从完整到最小的频谱
- 三个特性组合使用可实现最大的 Token 效率和准确率
- [How We Built Our Multi-Agent Research System](how-we-built-our-multi-agent-research-system.md) 中并行工具调用的实践是 PTC 和 Tool Search Tool 的应用场景
