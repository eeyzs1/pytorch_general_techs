# 印度语系预训练规模化：2.8 万亿 token 与开放数据生成管线（Scaling Indic Pretraining: 2.8 Trillion Tokens and an Open Data Generation Pipeline）

- **原文链接**: [Scaling Indic Pretraining: 2.8 Trillion Tokens and an Open Data Generation Pipeline](https://huggingface.co/blog/nvidia/scaling-indic-pretraining)
- **作者**: NVIDIA（Niket Agarwal、Yev Meyer、Markus Kliegl 等）× IIT Madras AI4Bharat（Mohammed Safi Ur Rahman Khan、Mitesh Khapra、Anoop Kunchukuttan）
- **发布日期**: 2026-10-16
- **检索日期**: 2026-10-16
- **标签**: #预训练数据 #印度语言 #合成数据 #NeMo #开源语料

## 核心观点

NVIDIA 与 IIT Madras 的 AI4Bharat 联合发布 Nemotron-pretraining-Indic-v1：约 2.8 万亿 token、覆盖印度宪法列明的 22 种语言（97% 印度人的第一语言，约 12 亿人），同时开源生成它的完整 GPU 加速管线（NeMo Data Designer：提示、LLM 工作流、质检全公开）。语料把精选英文材料（数学、代码、问答）译入印度语言，每条记录可回溯到源文档、每个输出都对照输入校验——合成但有据可查。

语料同时照顾书写现实：22 种语言全部有原生文字版，12 种另配罗马化（拉丁转写）版本，共 34 个语言-文字配置（原生文字 2,601.0B token + 罗马化 224.6B，按 Gemma-4 tokenizer 计）。回应用的是 AI4Bharat 负责人的判断："印度语言技术落后英语，是因为数据不够。"

## 关键发现 / 关键技术

### 1. 翻译-评估-修复三步管线

- 12 语言流：Gemma-4-31B-it 全文翻译（提示区分"要译的散文"与"要保留的代码/公式/URL"）→ 同模型按 MQM 启发 rubric 打分（含义/流利/术语/风格/格式）→ 低于 75/100 的按评估反馈修复后重评；修复挽回 438.4B token。
- 10 语言流：改用 Bodhan AI 的 Indic Translate 做文档级翻译（长文质量与文字稳定性更好），Gemma-4 只做评估；Santali 用重叠窗口重建长文，Manipuri 先译孟加拉文再转 Meitei Mayek。
- 罗马化采用两步法（先译成原生文字、再转写并对照校验），人工比对显示比"英文直译罗马化"更少幻觉与英文残留。

### 2. 溯源设计

- 源头是 Nemotron-CC-v2 的 15 个子集（网页、问答、数学、代码等），全程保留源标识符——"可审计的开放数据"不是口号而是字段。

### 3. 继续预训练实测

- Nemotron 3.5 Super VL 的 Indic CPT 阶段：100B token 预算中 10% 用本语料（合成+自然混合），五个 Indic 知识与推理基准（MILU、Indic MMLU-Pro、Indic ARC-C/E、Indic GSM8K）全部上涨 4.98–9.82 个百分点。

## 实践意义

这是"合成数据 + 完整配方开源"处理低资源语言的模板：任何语言社区都可以带着自己的源文档复用管线生成训练数据，而不必等待语料从天而降。修复而非丢弃（438.4B token 回收）与两步罗马化这两个细节，对任何做翻译语料的团队都有直接参考价值。

## 跨厂商对比

- 与 [Open ASR 榜纳全球南方语言](open-asr-leaderboard-global-south.md) 对比：印地语在评测侧刚获得公平席位，本篇在训练数据侧直接补上 22 语供给——低资源语言的"评测先行、数据跟进"路径正在成形。
- 与 [mDenseOn 与 mLateOn](mdenseon-mlateon-retrieval-models.md) 对比：mLateOn 证明 late-interaction 检索能泛化到未见语言，本篇证明翻译管线能批量生产多语言训练数据——"未见语言"问题的检索侧与训练侧答案可以组合使用。
- 与 [Gemma 4](../../google/deepmind/gemma-4.md) 对比：Gemma-4-31B-it 在此作为开源翻译与质检工具被选中——开放前沿模型正成为其他开放数据管线的基础设施，模型开放的价值在二次利用中被放大。

## 资源

- 论文：无（Nemotron 3.5 Super VL 技术报告另见）
- 代码：[NeMo Data Designer Nemotron-Bharat 翻译插件（含完整配方）](https://github.com/NVIDIA-NeMo/DataDesignerPlugins/tree/main/plugins/data-designer-nemotron-bharat-translation)
- Demo：[Nemotron-pretraining-Indic-v1 语料（即将发布）](https://huggingface.co/nvidia)
