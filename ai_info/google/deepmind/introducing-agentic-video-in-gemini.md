# Gemini 引入智能体式视频理解（Introducing agentic video understanding with Gemini）

- **原文链接**: [Introducing agentic video understanding with Gemini](https://blog.google/innovation-and-ai/models-and-research/gemini-models/introducing-agentic-video-in-gemini/)
- **作者**: Rohan Doshi、Mario Lucic
- **发布日期**: 2026-09-01
- **检索日期**: 2026-09-09
  注：官方页面抓取受限，本文基于检索核验的日期与公开报道整理（作者与基准数据经 PPC Land 对官方帖的详细转述核验）
- **标签**: #Gemini #视频理解 #智能体 #token优化

## 核心观点

最新 Gemini Flash 模型上线"智能体式视频理解"（agentic video understanding）：模型不再按固定帧率吞入整段视频，而是自行决定看什么、以什么速度、通过哪种模态（画面、音频还是转录文本）查看，仅取查询所需的片段。官方基准中，长视频测试的单查询 token 从 39.76 万降至 4.77 万（降 88%），成本最多降 66%，准确率最高提升 7%。

Google 明确这是"打包"而非"新能力"：开发者过去可以手工切片、抽样、拼接出同样的导航逻辑，现在这些编排收进单次 API 调用（processing 参数设为 agentic）。功能自 2026-09-01 起在 Gemini API（Google AI Studio 与 Gemini Enterprise Agent Platform）对上传视频与 YouTube URL 生效，覆盖 3.7/3.6 Flash 与 3.5 Flash-Lite。

## 关键发现 / 关键技术

### 1. Token 与准确率数据（Gemini 3.7 Flash 标准模式 vs 智能体模式）
- Minerva（复杂推理）：80,900 → 33,600 tokens（-58.4%），准确率 73.7% → 79.0%（相对提升 7.2%）
- 1H-VideoQA：397,600 → 47,700 tokens（-88.0%），准确率 87.5% → 88.5%
- LVBench：300,300 → 36,000 tokens（-88.0%），准确率 85.1% → 88.6%
官方口径"最高省 88% token / 最高提 7% 准确率"来自不同测试；成本-准确率图上，智能体模式约 90% 准确率、约 $0.10/查询，标准模式约 87%、约 $0.25。

### 2. 机制与用例
模型在循环内调用内部工具按需加载视频的相关部分，定位类似 agentic vision（代码执行 + 原生图像理解）。四类用例：亚秒级瞬间检索（服务自动剪辑）、小时级"大海捞针"搜索、异常检测（对选中时间窗以更高帧率重采样）、动作与物体计数。

### 3. 定价、生态与第三方佐证
按标准 Gemini API token 计费、无附加功能费；即将进入 Gemini app（Flash 与 Flash-Lite）并驱动 Ask YouTube。合作伙伴 Ponder 称单次调用即复现其自建管线的召回率、输入 token 约省 3.5 倍（≈71%）。基准与竞品配置均由 Google 选定，无独立复现；也未公布延迟对比。

## 实践意义

长视频是 token 开销最大的模态，"读得更少、想得更多"的智能体式处理把视频分析从研究性支出变成可预算的运营成本项，对内容审核、素材检索、品牌安全扫描等帧级分析场景尤其关键。工程上需注意：官方对比基线是 1 FPS 采样，已做低采样或预过滤的团队收益会小于官方数字；智能体循环多轮取材的输出 token（推理轨迹计价更高）可能使成本降幅小于 token 降幅。

## 跨厂商对比

- 与 [Muse Spark 1.2 的多模态智能](../../meta/multimodal-intelligence-muse-spark-1-2.md) 对比：Meta 侧强调多模态理解的模型能力谱系，Google 侧把"视频理解"重构为智能体按需取用的工具调用问题——能力路线 vs 编排路线。
- 与 [Gemini API Managed Agents 更新：3.6 Flash、hooks 与更多](expanding-managed-agents-gemini-api-3-6-flash-hooks.md) 互补：Managed Agents/Interactions API 提供长时运行的智能体基础设施，agentic video 是挂在其上的"感知侧"省 token 模式，两者合读可见 Gemini 智能体栈的纵向整合。

## 资源

- 官方文章：https://blog.google/innovation-and-ai/models-and-research/gemini-models/introducing-agentic-video-in-gemini/
- 产品/API：https://aistudio.google.com/
