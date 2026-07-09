# Paving the Way for Agents in Biology

- **原文链接**: [Paving the way for agents in biology](https://www.anthropic.com/research/agents-in-biology)
- **作者**: Laura Luebbert; 基于 Ferdous Nasri, Sarah Gurev, Patrick Varilly, Krithik Ramesh, Nuala A. O'Leary, Jonah Cool, Bernhard Y. Renard, Pardis Sabeti, Laura Luebbert 的研究
- **发布日期**: 2026-06-08
- **检索日期**: 2026-06-29
- **标签**: #Science #Agents #Biology #DataInfrastructure #NCBI #DeterministicTools

## 核心观点

生物数据基础设施（数据库、检索脚本、文件格式）是为人类设计的，而不是为 Agent 设计的。Anthropic 用 VirBench（120 个真实的病毒序列查询，覆盖 40 种病原体）测试了 Claude、Biomni OSS、Edison Analysis、GPT，发现**最强模型也只能达到约 91.3% 的准确率**，而且同一查询的多次运行结果差异巨大。**添加一个确定性检索层（如 gget virus）后，准确率上升到接近 100%**。生物学 Agent 的瓶颈不是推理，而是缺乏"确定性执行层"。

## 关键发现

### 1. 数据基础设施是为人类点击设计的
- NCBI Virus 的过滤逻辑只存在于 Web 界面中，**程序化 API 难以复现**
- 一个查询可能需要"几百行脚本"拼接多个 API，分页下载数百 GB 数据后再过滤
- 在 DRC 2026 年 5 月爆发的 Bundibugyo 埃博拉疫情中，研究人员只能手动点击 Web 界面提取序列——直接关系到能否快速诊断和评估现有疗法

### 2. Agent 在生物数据检索上不可靠
- Claude Sonnet 4、Opus 4.7、Biomni OSS、Edison Analysis、GPT-5.2-pro、GPT-5.5 的准确率范围：**16.9% ~ 91.3%**
- 对于生物数据检索任务，**有效阈值是 100%**——一个错误记录可能决定诊断是否覆盖到病毒变种，或将疫情起源时间推断偏差数周
- **重复性问题**：同一查询三次运行可能返回三个不同结果（如某次 Ebola 查询：106、15、5 条序列）

### 3. 确定性检索层是关键
- 当为 Agent 配备 gget virus（确定性检索库）时，准确率上升到接近 100%
- **Karpathy 的"为 Agent 构建软件"论点同样适用于生物学**

### 4. 错误的实际后果
- 系统发育树（TMRCA）分析：用 Sonnet 4 检索的数据集构建的树，把 2014 年 Ebola 疫情的最近共同祖先时间推到 1922 年
- 表位分析：三次运行的抗体治疗靶向残留分析结果不一致，得出三个不同的结论

## 关键洞察

1. **生物 Agent 的瓶颈在基础设施，不在模型**——添加确定性层后，最强模型的准确率立即接近 100%
2. **可重复性是科学 Agent 的核心要求**——单一正确答案的查询，必须有单一可重复答案
3. **细节错误有严重后果**——基因组构建错误、表位分析错误会直接误导生物学结论
4. **数据库需要为 Agent 设计**——过滤语义必须可程序化访问，标识符必须跨源稳定，元数据必须一致

## 关键数据点

| 指标 | 数值 |
|------|------|
| VirBench 查询数 | 120 |
| 覆盖病原体 | 40 |
| 最佳模型准确率（无确定性层） | ~91.3% |
| 加确定性层后准确率 | 接近 100% |
| 检索数据集偏差 | Ebola TMRCA 推到 1922 |
| 实际案例 | DRC Bundibugyo Ebola 2026-05 |

## 相关文章

- [Making Claude a Chemist](making-claude-a-chemist.md)
- [Coding Agents in the Social Sciences](coding-agents-social-sciences.md)
- [How We Built Our Multi-Agent Research System](../engineering/how-we-built-our-multi-agent-research-system.md)