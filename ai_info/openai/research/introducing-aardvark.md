# Aardvark：OpenAI 的自主式安全研究员（Introducing Aardvark）

- **原文链接**: [Introducing Aardvark](https://openai.com/index/introducing-aardvark/)
- **作者**: OpenAI(官方博客,署名未核实——原文经第三方转载交叉验证)
- **发布日期**: 2025-10-30
- **检索日期**: 2026-09-29
- **标签**: #Aardvark #网络安全 #Agent #漏洞挖掘 #GPT-5 #CVE

## 核心观点

OpenAI 推出 Aardvark：基于 GPT-5 的 agentic 安全研究员，以私有 beta 启动。它持续分析代码仓库，完成"识别漏洞—评估可利用性—按风险排序—生成补丁"的全流程；方法论上不依赖模糊测试或软件成分分析（SCA），而是以 LLM 推理加工具调用，像人类安全研究员一样工作。

黄金仓库基准上漏洞检出率达 92%；已通过负责任披露多个漏洞、其中 10 个获得 CVE 编号，并计划向非商业开源仓库提供免费扫描。事后看，Aardvark 是 OpenAI 安全 Agent 演化链的起点：2025-12 纳入 Strengthening Cyber Resilience，2026-03 演进为 Codex Security。

## 关键发现 / 关键技术

### 1. 定位与方法论
- 基于 GPT-5 的 agentic 安全研究员，以私有 beta 启动。
- 持续分析代码仓库：识别漏洞、评估可利用性、按风险排序、生成补丁。
- 不使用模糊测试（fuzzing）或软件成分分析（SCA）——以 LLM 推理 + 工具调用复现人类安全研究员的工作方式。

### 2. 四步工作流
1. **Analysis**：对整个代码仓库构建威胁模型。
2. **Commit Scanning**：扫描提交历史，定位引入漏洞的变更。
3. **Verification**：在隔离沙箱中实际触发漏洞、复现利用路径，消除误报。
4. **修复**：与 Codex 协作生成补丁，供人工审查后合入。

### 3. 效果与披露数据

| 指标 | 数值 |
|------|------|
| 黄金仓库基准检出率 | 92% |
| 负责任披露漏洞 | 多个，其中 10 个获 CVE 编号 |
| 免费扫描计划 | 面向非商业开源仓库 |

### 4. 后续演进（补录视角）
- 2025-12-10：能力纳入 Strengthening Cyber Resilience 发布，同期 GPT-5.1-Codex-Max 将 CTF 基准成绩从 27% 提升到 76%。
- 2026-03-06：演进为 Codex Security 插件，累计 CVE 达 14 个。
- 2026-06-22：Daybreak 阶段 Codex Security 已扫描 3000 万 commits / 30000+ 代码库（见 Daybreak 条目）。

## 实践意义

1. **"推理优先"的漏洞挖掘范式**：不靠 fuzzing/SCA 而靠模型推理 + 工具调用，验证了 LLM Agent 承担高技能安全研究工作的可行性。
2. **验证环节是可信交付的关键**：隔离沙箱实际触发复现，把"可能为真"变成"已验证"，为安全类 Agent 的输出设计提供模板。
3. **人机边界清晰**：补丁由 Aardvark + Codex 生成、人类审查合入，决策权留在维护者一侧。
4. **开源反哺**：非商业开源仓库免费扫描，直接回应开源生态的安全债问题。
5. **从原型到产品的路径可复制**：私有 beta → Strengthening Cyber Resilience → Codex Security，约 5 个月完成产品化。

## 跨厂商对比

- 与 [Daybreak: Tools for Securing Every Organization in the World](daybreak-securing-the-world.md) 构成演进链：Aardvark 是"自主安全研究员"原型，Daybreak 阶段的 Codex Security 已规模化（3000 万 commits、500,000+ 自动确认修复），从原型到平台约 8 个月。
- 与 [Patch the Planet](patch-the-planet.md) 对比：两者都服务开源生态，但 Patch the Planet 以"专家研究员 + AI"过滤后交付维护者，Aardvark 的原始设计是端到端自动化 + 人工审补丁。
- 与 [Project Glasswing: An Initial Update](../../anthropic/research/glasswing-initial-update.md) 对比：Glasswing 用 Mythos Preview 让约 50 家伙伴发现 10,000+ 高危/严重漏洞，但强调瓶颈已从"发现"转向"修复"、维护者被报告淹没；Aardvark 从设计上把验证与补丁生成纳入闭环——"发现 vs 修复闭环"是两家共同收敛的方向。
- 与 [Our Response to the TanStack npm Supply Chain Attack](our-response-to-the-tanstack-npm-supply-chain-attack.md) 互补：Aardvark 的 Commit Scanning 能力正是识别供应链投毒式提交变更的工具化路径。

## 资源

- 官方博客：[Introducing Aardvark](https://openai.com/index/introducing-aardvark/)
- 相关条目：[Daybreak: Tools for Securing Every Organization in the World](daybreak-securing-the-world.md)、[Patch the Planet](patch-the-planet.md)、[Running Codex Safely at OpenAI](running-codex-safely.md)
- 第三方转载源：Axios / habr / Gigazine / Lifeboat（交叉验证用）

> 注:openai.com 原文 403,本文基于多源转载交叉验证(Axios/habr/Gigazine/Lifeboat 等),官方 URL 已列于资源。
