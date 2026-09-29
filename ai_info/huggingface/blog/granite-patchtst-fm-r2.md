# IBM Granite 时序 PatchTST-FM-r2 商用友好 SOTA（IBM Releases SOTA Granite Time Series Model）

- **原文链接**: [IBM Releases SOTA Granite Time Series Model](https://huggingface.co/blog/ibm-research/ibm-releases-sota-granite-time-series)
- **作者**: IBM Research（Community 版）
- **发布日期**: 2026-09-09
- **检索日期**: 2026-09-29
- **标签**: #时间序列 #预测模型 #Apache2 #零样本 #基础模型

## 核心观点

IBM Research 发布 Granite PatchTST-FM-r2 时序基础模型：约 385M 参数，Apache-2.0 与 OpenMDW 双许可（明确商用友好）。在 GIFT-Eval"可复现零样本"口径下列第二（CRPS 0.467、MASE 0.6846，仅次于 TimesFM-3），且是商用友好许可模型中的最强者。

架构全面升级：transformer 块改为 conformer（半步 FFN 夹自注意力 + 时间卷积，卷积核 {5,5,3,3} 交替）、50% 重叠 patch + Hamming 窗、块数 20→30、上下文扩至 8192、99 分位概率预测头 + 缺失值插补。训练语料完全透明可审计（GiftEvalPretrain、KernelSynth、TSMixup、CauKer）——团队明确"透明度与分数同等重要"；权重、推理与复现脚本全部开源。

## 关键发现 / 关键技术

### 1. 商用友好的榜单位置

- GIFT-Eval 可复现零样本：CRPS 0.467、MASE 0.6846，总榜第二，仅次于 TimesFM-3。
- 关键差异：榜首非商用许可，Granite 以 Apache-2.0/OpenMDW 成为商用可用的最强零样本时序模型。
- "可复现"口径意味着数字可被第三方重跑验证，而非厂商自报。
- 对企业选型，"商用友好 + 榜单前列"的组合此前基本不存在，二选一是常态。

### 2. Conformer 化架构升级

- transformer 块改为 conformer：自注意力前后各半步 FFN，穿插时间卷积（核 {5,5,3,3} 交替），同时捕获局部形态与全局依赖。
- patch 策略升级：50% 重叠 + Hamming 窗，块数从 20 增至 30，上下文扩展到 8192——长历史信息得以进入模型。

### 3. 概率预测与缺失值插补

- 99 分位概率预测头输出分布而非点估计，直接服务库存、容量等需要分位数决策的场景。
- 原生缺失值插补，贴合真实时序数据的空洞现实，无需先行填充管线。
- 385M 的规模在单卡甚至 CPU 上即可服务，部署门槛远低于十亿级 LLM。

### 4. 训练语料透明可审计

- 语料完全公开：GiftEvalPretrain、KernelSynth、TSMixup、CauKer，成分与配比可查。
- 团队把"知道模型见过什么"列为与分数同等重要的发布物——时序场景的数据泄漏争议尤其敏感。
- 权重、推理代码、复现脚本全部开源。
- 双许可（Apache-2.0/OpenMDW）同时满足开源社区与企业法务的不同要求。

## 实践意义

对需要零样本时序预测的企业（零售、能源、运维），这是首个"榜单顶级 + 明确可商用 + 语料可审计"三合一选项，接入成本仅为一个 385M 模型。概率预测头与缺失值插补直接对应生产数据现状。其"语料透明与分数同等重要"的立场也应成为选用任何基础模型的检查项。

## 跨厂商对比

- 与 [Granite 4.2](granite-4-2.md) 对比：同家族的 LLM 与时序两条产品线，共享 Apache-2.0 友好许可与透明可审计的发布哲学。
- 与 [Real-Time Intelligence](real-time-intelligence.md) 互补：实时数据管道负责把时序喂进来，PatchTST-FM-r2 负责预测出去，端到端流式预测栈的两半。
- 与 [Train Multi-Vector Encoder](train-multi-vector-encoder.md) 对比：同为"可复现训练配方"叙事，一个面向检索编码器，一个面向时序基础模型。

## 资源

- 论文：N/A
- 代码：[ibm-granite（Hugging Face 组织页，含权重与推理代码）](https://huggingface.co/ibm-granite)
- Demo：[GIFT-Eval 基准仓库](https://github.com/SalesforceAIResearch/gift-eval)
