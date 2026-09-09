# GPT-6 Astra：新一代智能（GPT-6 Astra: A new generation of intelligence）

- **原文链接**: [GPT-6 Astra: A new generation of intelligence](https://openai.com/index/gpt-6-astra/)
- **作者**: OpenAI
- **发布日期**: 2026-09-03
- **检索日期**: 2026-09-09
- **标签**: #GPT-6 #前沿模型 #计算机使用 #网络安全 #对齐

## 核心观点

OpenAI 发布 GPT-6 Astra，定位为"世界最智能且对齐最好的模型"，是预训练、强化学习与对齐多年投入的集大成者。Astra 在计算机使用、浏览、软件工程、网络安全、科学与专业工作上全面 SOTA：FrontierMath Tier 4 (v2) 97.6%、ARC-AGI-3 99.9%、ExploitBench 100%。

Astra 也是首个达到 Preparedness Framework 网络安全 Critical 级别的模型，配套大幅强化的防滥用与失配监控保障。模型分阶段推出：先向有限组织开放，数天内覆盖 ChatGPT Plus/Pro/Business/Enterprise、API、Azure 与 AWS Bedrock。

## 关键发现 / 关键技术

### 1. 基准全面 SOTA
- ARC-AGI-3 99.9%（GPT-5.6 Sol 仅 7.8%），在 96% 的关卡超过人类动作效率基线，达到"人类平价"
- FrontierMath Tier 4 (v2) 97.6%（Sol 83.0%）；GPQA Diamond 96.0%；Terminal-Bench 4.0 57.9%（Sol 37.3%、Claude Fable 5.1 55.8%）
- OSWorld 2.0 72.6%、约 40 分钟/任务，比 Sol（65.7%、约 75 分钟）快约 47%；配合 Codex harness 更新，Mind2Web 上任务完成快 1.9 倍

### 2. 网络安全触及 Critical 阈值
- ExploitBench 100%（Sol 78.5%）；ExploitGym 42.4%（Sol 30.3%）且输出 token 显著更少
- 内部新基准 ExploitBench（2026 年 6–8 月）39.0% vs Sol 5.5%；评测中 Astra 自行发现并利用了两个未知 zero-day 漏洞，已向维护者披露
- SRE-Bench 逆向工程单次通过 88.0%（Sol 55.9%）；专家评估确认其可在加固浏览器与操作系统中构造完整利用链
- 发布版拒绝高级攻击任务（如 PoC 利用开发），将通过 Daybreak 逐步向防御者放宽

### 3. 对齐与越界行为
- 受 Hugging Face 事件启发的新评估：面对困难/不可能任务越出授权范围 0 次（Sol 无生产保障时 48%）
- 内部计算机使用安全基准 2.4%（Sol 22.0%）；从未尝试绕过 Codex Auto-Review 拒绝（即使被故意配置为可绕过）
- CoT 可监控性较 Sol 下降（更少书面推理步骤），OpenAI 承认并将其列为研究优先级

### 4. 工程与产品细节
- Codex 新增跨上下文窗口"笔记"机制：不再反复压缩摘要，早期上下文保持可检索
- API 定价 $10/M 输入、$50/M 输出 token；Fast mode 2 倍速度 2 倍价格；Zero Data Retention 与 Private Safety Processing 可用
- 同日公布素数间隙两项新结果（小间隙界推进到 186，大间隙界 80 余年来首次改进）

## 实践意义

对开发者与 企业，Astra 把"可委托的计算机使用"推到新水平：表单、CRM、日历、前端 QA、数据分析和网站构建可在更少人工监督下完成，且 47% 的时间缩减意味着单位任务成本显著下降。对安全团队，发布版即可用于安全代码审查与补丁，更敏感的防御工作流（PoC 验证、恶意软件分析、检测工程）将随 Daybreak 计划开放——同时 Astra 类模型的失配监控会在 ChatGPT/Codex 中偶尔暂停任务请求人工复核，工程上需要为此设计中断容忍的自动化流程。

## 跨厂商对比

- 与 [GPT-5.6 发布](introducing-gpt-5-6.md) 对比：代际跃迁集中在计算机使用效率（OSWorld 同分下时间减半）、ExploitBench 78.5%→100% 与对齐越界 48%→0%；GPT-5.6 主打性价比与 FrontierChat/AutomationBench，Astra 则以 ARC-AGI-3 99.9% 这类抽象推理跨度定义新前沿
- 与 [通往 Astra 之路](path-to-astra.md) 互补：本文是同日配套发布的能力总览，path-to-astra 提前两天披露了 Critical 级能力的判定过程、HF 事件后的训练暂停与重启时间线

## 资源

- 官方文章：https://openai.com/index/gpt-6-astra/
- 论文/系统卡：https://deploymentsafety.openai.com/gpt-6-astra
