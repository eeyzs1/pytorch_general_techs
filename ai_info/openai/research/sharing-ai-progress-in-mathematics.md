# 分享 AI 数学进展：722 篇手稿开源，162 篇完成 Lean 形式化（Sharing AI progress in mathematics）

- **原文链接**: [Sharing AI progress in mathematics](https://openai.com/index/sharing-ai-progress-in-mathematics)
- **作者**: OpenAI
- **发布日期**: 2026-10-06
- **检索日期**: 2026-10-16
- **标签**: #AIforMath #Lean形式化 #开放科学 #可验证性 #研究披露

## 核心观点

OpenAI 把一个未发布内部模型（与 9 月纳维-斯托克斯工作同源、8 月 28 日起训练、能力显著强于 GPT-6 Astra）产出的数学成果整体开源：722 篇手稿按 372 个"家族"（主结果 + 伴随论证/推论/替代证明）组织，连同 Lean 形式化库、10 个家族的推理摘要一起放入 GitHub 仓库 openai/math（Apache-2.0）。模型被问了约 4,000 个开放问题，筛出 372 个家族——平均每个结果仅耗约 3 小时 ChatGPT Pro 级思考算力，"低成本大批量"是本批与 8 月"十项进展"、9 月"万级并发 agent 攻千年难题"最大的不同。

发布程序明显吸收了两个月争议的教训：8 月十项进展被指未充分引用前人工作，9/11 数学家联名发表公开信《A Severe Misalignment of AI in Mathematics》，9/21 OpenAI 成立普林斯顿高等研究院托管的数据与 AI 顾问组（AGMAI），9/29 AGMAI 发布 AI 数学成果发布建议（基于 600+ 份数学家问卷），本批是该建议下的首次落地——但对照建议逐条看仍是"部分达标"：模型未命名、提示词未公开、引用规范被 OpenAI 自己承认为未完成项。

## 关键发现 / 关键技术

### 1. 数字全景

| 指标 | 数值 |
|------|------|
| 手稿 / 家族 | 722 / 372 |
| 抛给模型的问题总数 | 约 4,000 |
| 平均单结果算力 | 约 3 小时 ChatGPT Pro 思考 |
| 主结果完成 Lean 形式化（10/7 快照） | 162 篇（另 560 篇未形式化，官方承认部分可能有误） |
| 推理摘要披露 | 10/372 家族（缩略版） |
| 许可证 | Apache-2.0 |

### 2. 仓库结构与可复现机制
- `overview.pdf`（372 家族描述）、`CONTENTS.md`、`preprints/`（PDF+源文件+引用说明）、`lean/`（统一 Lean 库 + `formalization.yaml` 目录 + Comparator 挑战文件）、`reasoning_traces/`。
- 用 Comparator 把"被证命题"与"证明"分离固定：任何人可 `lake env comparator ComparatorChallenges/*.json` 自行机检；修订以新版本追加，历史版本保留。
- 10 个披露推理摘要的家族横跨解析数论（乘法函数二点相关）、π 的无理性指数、Mahler 猜想（凸几何）、NP 困难性阈值、算术级数拟多项式界、Kaplansky 直接有限性猜想、Mézard–Parisi 稀释自旋玻璃公式、海森堡铁磁体自发磁化、自由群因子同构、三维相对论 Vlasov–Maxwell 系统。

### 3. 三层验证状态要分清
- 手稿存在（722 全部）≠ 形式化证明存在（162）≠ 数学家理解并接受（0，目录状态列为 unchecked、方法列为 agent）。Lean 只保证"从给定定义到给定定理的每步都被机器接受"，不保证命题与开放问题等价、论证新颖或引用得当——后三者恰是 8 月争议的核心。

### 4. AGMAI 建议对照（第三方整理）
- 沉淀到不受实验室控制的学术库：未做（仍在自家 GitHub，称探索社区托管）；版本留痕：已做；披露模型名/提示词/推理摘要/算力：部分（模型未命名、提示词未提）；形式化+状态声明：部分；文献检索与规范引用：官方承认未完成、承诺改进；资助人类理解性研究：宣布将资助工作坊与专项。

## 实践意义

1. **生成已廉价、检查是稀缺资源**：4,000 问 → 372 家族的漏斗说明，输出规模化的瓶颈全在验证侧——软件工程同构（测试/类型/评审就是你们的 Lean）。
2. **"检查器只和被检命题一样好"**：错误命题的 Lean 证明照样通过——写清 spec/命题仍是人类职责，这是所有 Agent 交付物的通用规律。
3. **披露规范正在制度化**：从单方发布到"顾问组建议 + 逐条对照 + 版本留痕"，AI 科研成果的发布流程正在形成可问责模板，跨实验室可复用。

## 跨厂商对比

- 与 [纳维-斯托克斯千年问题](navier-stokes-solution.md) 同源接力：同一切线报告称约 1 万并发 agent、88 小时出结果 + 17 小时形式化；本批转为"3 小时级单价、数百结果"的批量模式——AI 数学的经济学从攻坚型转向产能型。
- 与 [数学与理论计算机科学的十项进展](ten-advances-in-mathematics.md) 对照：8 月批次（约 $2,000 token 成本）因引用争议引发数学界反弹，本批首次按 AGMAI 建议流程发布，[数学与 AI 顾问组](advisory-group-mathematics-ai.md) 的治理建议开始约束发布行为。
- 与 [Anthropic：Paving the Way for Agents in Biology](../../anthropic/research/agents-in-biology.md) 并观：生命科学与数学两条"AI 科研合作者"路线都走到"开放成果 + 外部评审"阶段，可验证性披露成为共同门槛。

## 资源

- 官方发布：[Sharing AI progress in mathematics](https://openai.com/index/sharing-ai-progress-in-mathematics)
- 代码/数据：[github.com/openai/math](https://github.com/openai/math)（Apache-2.0）
- 第三方验证：[Netalith 深度解析（含仓库结构与 AGMAI 对照表）](https://netalith.com/blogs/ai-tools/openai-mathematics)、[x-techcon 中文报道](https://www.x-techcon.com/article/194459.html)
- 相关条目：[advisory-group-mathematics-ai](advisory-group-mathematics-ai.md)

> 注:openai.com 原文 403；数字与仓库结构经 Netalith（直接核对 GitHub 目录快照）与 x-techcon 交叉验证；162 篇形式化数为 10/7 目录快照，后续可能增长。
