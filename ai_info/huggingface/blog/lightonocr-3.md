# LightOnOCR-3：一个模型同时做转录与版面（LightOnOCR-3: High-Performance OCR and Layout Extraction in One Model）

- **原文链接**: [LightOnOCR-3: High-Performance OCR and Layout Extraction in One Model](https://huggingface.co/blog/lightonai/lightonocr-3)
- **作者**: Said Taghadouini、Adrien Cavaillès、Baptiste Aubertin（LightOn AI；Community 版）
- **发布日期**: 2026-10-08
- **检索日期**: 2026-10-16
- **标签**: #OCR #文档解析 #版面分析 #开源模型 #Apache2

## 核心观点

LightOn 发布 LightOnOCR-3 家族（0.8B / 1B / 4B，Apache 2.0）：空提示纯转录保持旧接口；输入 grounding 则在同一输出里附带带标签的归一化（0–1000）边界框、图像描述、以及从图表提取的 HTML 数据表。一个模型替代"OCR + 版面分析 + 图表抽取"多段管线，且格式更省 token——同 512 页 olmOCR-bench 上，grounding 模式输出比 Chandra-OCR-2 与 Infinity-Parser2-Pro 平均少 9–14% 的 token，信息反而更多（Infinity 不生成图像描述）。

三个尺寸两种血统：1B 沿用上代架构，0.8B 与 4B 采用 Qwen3.5 视觉语言架构。训练包含 SFT 混合数据、迭代构建的边界框数据（含图表与图像描述、用文档内容引导分块）、以及带人工验证数据与定制奖励的强化学习阶段。

## 关键发现 / 关键技术

### 1. olmOCR-Bench：小模型咬住 35B

- 4B 综合 86.3，仅落后 35.1B 的 Infinity Parser Pro（87.6）1.3 分，ArXiv 类 91.1 全场第一；0.8B 85.5、1B 84.5。
- 分项各有冠军：0.8B 长微小文字 94.1 第一，1B 多栏 85.9 第一——按文档类型选小模型是可行策略。

### 2. ParseBench：包揽前二

- 五类综合：4B 75.1、0.8B 74.6，力压 Infinity Parser Pro（74.3）；4B 图表 66.1 与语义格式化 67.6 均第一，Infinity 仅视觉定位（74.9）领先。
- 法语 fr-bench-pdf2md：4B 以 74.1 领先——多语言文档同样受益。

### 3. 工程配套

- 仓库提供原始输出到常用格式的转换函数、可视化脚本与基准复现脚本；1B 在图表与视觉定位上落后 0.8B，凸显"从预训练 VLM 起步"对视觉类目的价值。

## 实践意义

文档智能管线的维护成本正在坍缩：过去拼装 OCR + 版面 + 图表三个组件的团队，现在可以单模型部署并按显存选尺寸。9–14% 的 token 节省对"文档→LLM"的下游管线直接降本；Apache 2.0 允许商用改造。

## 跨厂商对比

- 与 [mDenseOn 与 mLateOn](mdenseon-mlateon-retrieval-models.md) 对比：LightOn 两代产品线互补——检索侧多语言 late-interaction，文档侧 OCR+版面一体，共同构建"非结构化→可检索"的开放栈。
- 与 [Papers with Code 搜索](pwc-search.md) 互补：pwc-search 讲论文元数据检索后端，LightOnOCR-3 讲论文 PDF 本身的结构化抽取，学术内容的机器可读化在两端同时推进。
- 与 [训练多向量嵌入模型](train-multi-vector-encoder.md) 对比：抽取质量决定检索上限——OCR 的字段错误会原样进入嵌入索引，文档管线与检索管线的质量门必须一起设计。

## 资源

- 论文：无（技术报告见网站页）
- 代码：[github.com/lightonai/LightOnOCR](https://github.com/lightonai/LightOnOCR)
- Demo：[LightOnOCR-3-Demo Space](https://huggingface.co/spaces/lightonai/LightOnOCR-3-Demo)
