# Introducing LifeSciBench

- **原文链接**: [Introducing LifeSciBench](https://openai.com/index/introducing-life-sci-bench/)
- **作者**: OpenAI
- **发布日期**: 2026-06-17
- **检索日期**: 2026-06-29
- **标签**: #LifeSciBench #Benchmark #LifeScience #Evaluation #ExpertAuthored

## 核心观点

OpenAI 发布 **LifeSciBench**——专为生命科学研究任务设计的专家级基准。**750 个任务、1,062 个 artifact、19,020 条 rubric 准则**——由 **173 名 Ph.D. 级生命科学家**撰写，**453 名独立专家**审查。所有任务覆盖 **7 个工作流 + 7 个生物域**，**79% 任务需要多步推理**（平均 4 步），**53% 需要解释至少 1 个 artifact**。

## 关键设计

### 1. 为什么需要 LifeSciBench
- 现有基准多聚焦狭窄领域或孤立技能
- 结构化问答格式 + 干净参考答案
- **无法评估模型能否在更广的研究级别工作中贡献**
- 真实研究：解释证据、协调冲突结果、设计实验、评估转化风险

### 2. 基准规模
| 指标 | 数值 |
|------|------|
| 任务数 | 750 |
| Artifact 数 | 1,062 |
| 任务撰写科学家 | 173 |
| 独立审查专家 | 453 |
| Rubric 准则数 | 19,020（每任务平均 25 条） |
| 工作流类别 | 7 |
| 生物域 | 7 |
| 多步推理任务占比 | 79% |
| 平均推理步数 | 4 |
| 需 artifact 任务占比 | 53% |

### 3. 七大工作流
- Evidence Handling（证据处理）
- Analysis（分析）
- Design, Optimization, & Prediction（设计、优化、预测）
- Reasoning（推理）
- Validation & Operations（验证与操作）
- Translation（转化）
- Scientific Communication（科学沟通）

### 4. 任务结构
- 科学家 prompt + 上下文/artifact + 自由回答
- **专家 rubric 评估**：是否给出正确答案 + 细节、理由、警示、格式

### 5. 评分
- 不是只看最终答案——还要看过程
- 19,020 条准则评估科学正确性和研究决策有用性
- 反映真实科学评估方式

### 6. 评审质量
- 97% 评审有 Ph.D.
- 平均 12 年领域经验、14 篇同行评审论文
- 88% 获得至少一个奖项或 fellowship
- 任务接受前平均经过 6 轮自动审查 + ≥2 轮专家审查
- 90%+ 评审者一致率

## 评估示例

### 案例：AAV9-microDys-X 加速审批包评估
- 真实风格：要求模型压力测试 DMD 基因治疗临床数据
- 包括：Western blot 定量、免疫荧光、NSAA 评分、安全性、生物分布
- 模型需识别 MANEX1A 抗体表位共享问题、surrogate endpoint 效力、统计缺陷等

### Rubric 评分（满分 100）
- 鉴定 micro-dystrophin 量化中的测量问题：+24
- 解释表达水平作为 surrogate 的局限：+22
- 识别 biopsy 部位、年龄窗口混淆：+19
- 批评 NSAA 比较和统计：+12
- AAV 持久性、免疫反应、安全随访：+15
- 患者选择/泛化：+8

## 关键洞察

1. **真实科学 ≠ 干净问答**——需要多步推理、artifact 解释、不确定性沟通
2. **专家级基准才能评估专家级能力**——生命科学领域的门槛
3. **过程评估胜过结果评估**——rubric 不只看最终答案
4. **评估 AI 在生命科学的真实价值**——这是医疗诊断、化学、生物学等高门槛领域的关键测试
5. **与 GPT-Rosalind、Codex、Deep Research 等能力形成完整评估闭环**

## 相关文章

- [Introducing New Capabilities to GPT-Rosalind](introducing-new-capabilities-to-gpt-rosalind.md)
- [Strengthening Societal Resilience with Rosalind Biodefense](strengthening-societal-resilience-with-rosalind-biodefense.md)
- [How GPT-5 Helped Immunologist Derya Unutmaz Solve a 3-Year-Old Mystery](gpt-5-immunology-mystery.md)