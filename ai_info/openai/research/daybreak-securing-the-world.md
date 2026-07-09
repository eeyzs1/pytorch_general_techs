# Daybreak: Tools for Securing Every Organization in the World

- **原文链接**: [Daybreak: Tools for securing every organization in the world](https://openai.com/index/daybreak-securing-the-world/)
- **作者**: OpenAI
- **发布日期**: 2026-06-22
- **检索日期**: 2026-06-29
- **标签**: #Daybreak #CyberSecurity #CodexSecurity #PatchThePlanet #GPT55Cyber #CriticalInfrastructure

## 核心观点

OpenAI 扩展 **Daybreak**——把漏洞发现从瓶颈转化为可大规模自动化的"从发现到修复"闭环。核心组件：**Codex Security 插件更新 + GPT-5.5-Cyber 完整版 + Daybreak Cyber Partner Program + Patch the Planet 开源计划**。Codex Security 已扫描 **3000 万 commits / 30000+ 代码库**，人工确认 70,000+ 修复，自动确认 500,000+ 修复。GPT-5.5-Cyber 在 CyberGym 上达 **85.6%**（单模型最高分）。

## 关键产品更新

### 1. Codex Security（更新版插件）
- 集成进 Codex，**直接在开发者工作流中**
- 能力：
  - 深度扫描代码库或最近变更
  - 生成报告（严重度、影响代码、验证证据、修复指导）
  - 追踪攻击路径
  - 构建威胁模型
  - 验证发现
  - 生成代码库特定补丁
- 部署：Codex CLI 或 Codex App
- 集成：SARIF 文件、CodeQL 查询、现有漏洞管理系统

### 2. GPT-5.5-Cyber（完整版）
- **CyberGym：85.6%**（vs GPT-5.5 的 81.8%）——单模型最高
- **ExploitGym：39.5%**（vs GPT-5.5 的 25.95%）
- **SEC-bench Pro：69.8%**（vs GPT-5.5 的 63.1%）
- 仅通过 Trusted Access for Cyber 向验证防御者开放
- 特点：更强能力 + 更宽松行为 + 强验证/监控/范围控制

### 3. Daybreak Cyber Partner Program
- 安全软件和服务合作伙伴可通过 Trusted Access for Cyber 在自己的产品中使用 GPT-5.5
- 初始合作伙伴（包括）— 将在后续扩展

### 4. Patch the Planet（详见单独条目）
- 与 Trail of Bits 联合，专注开源维护者

## 数据规模

### Codex Security（自 3 月研究预览以来）
- **扫描 commits：3000 万+**
- **扫描代码库：30,000+**
- **人工确认修复：70,000+**
- **自动确认修复：500,000+**

### Daybreak 已识别的真实漏洞（与 Patch the Planet 互补）
- Firefox、V8、Safari、OpenBSD、FreeBSD、HTTP/2 等关键开源基础设施

## 关键政策协调

### 美国政府
- 与 CAISI（Center for AI Standards and Innovation）合作预部署测试
- 与 ONCD（Office of the National Cyber Director）和 OSTP（Office of Science and Technology Policy）合作实施近期网络 Executive Order

### 国际合作
- 已与以下建立 Trusted Access for Cyber 合作：
  - **澳大利亚、加拿大、法国、德国、日本、韩国**
  - **EU 机构如 ENISA**
- 与英国政府保持合作伙伴关系

## 关键洞察

1. **瓶颈从"发现"转向"修复"**——AI 让漏洞发现变得容易，闭环修复成为新焦点
2. **Codex Security 是开发者侧的"安全工程师同事"**——而不是独立扫描器
3. **GPT-5.5-Cyber 需要 Trusted Access**——能力越强，越需要身份验证
4. **30M commits / 70K 人工修复**——规模化数据说明 AI 安全工具已落地
5. **国际合作已成形**——8+ 国家/机构已建立网络 Trusted Access
6. **Patch the Planet 是"共享基础设施，共享防御"的具体实践**

## 关键数据点

| 指标 | 数值 |
|------|------|
| Codex Security 扫描 commits | 3000 万+ |
| Codex Security 扫描代码库 | 30,000+ |
| 人工确认修复 | 70,000+ |
| 自动确认修复 | 500,000+ |
| CyberGym（GPT-5.5-Cyber） | 85.6% |
| CyberGym（GPT-5.5） | 81.8% |
| ExploitGym（GPT-5.5-Cyber） | 39.5% |
| ExploitGym（GPT-5.5） | 25.95% |
| SEC-bench Pro（GPT-5.5-Cyber） | 69.8% |
| SEC-bench Pro（GPT-5.5） | 63.1% |
| Trusted Access for Cyber 国家/机构 | 澳、加、法、德、日、韩、ENISA、英国 |

## 相关文章

- [Patch the Planet](patch-the-planet.md)
- [Building Codex Windows Sandbox](building-codex-windows-sandbox.md)
- [Running Codex Safely at OpenAI](running-codex-safely.md)
- [GPT-5.6 Preview System Card](gpt-5-6-preview-system-card.md)