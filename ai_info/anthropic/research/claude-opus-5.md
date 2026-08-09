# Claude Opus 5 发布：半数价格逼近 Fable 5 前沿智能（Introducing Claude Opus 5）

- **原文链接**: [Introducing Claude Opus 5](https://www.anthropic.com/news/claude-opus-5)
- **作者**: Anthropic
- **发布日期**: 2026-07-24
- **检索日期**: 2026-08-01
- **标签**: #ClaudeOpus5 #模型发布 #AgenticCoding #对齐 #Effort档位 #安全分类器

## 核心观点

Claude Opus 5 是 Anthropic 2026 年 7 月 24 日上线的旗舰模型，核心主张是"以一半的价格提供接近 Fable 5 的前沿智能"——定价与 Opus 4.8 持平（输入 $5 / 输出 $25 每百万 token），但在编码与知识工作基准上成为新的 SOTA。模型定位为"日常主力"：成为 Claude Max 默认模型、Claude Pro 最强模型，并通过 effort 档位与 Fast 模式（约 2.5 倍速度、2 倍价格）让用户在成本与智能间灵活权衡。

官方同时强调这是其"最对齐的模型"：自动化行为审计中不当行为评分 2.3，为近期模型最低；安全上刻意不推进双刃剑能力前沿——与 Opus 4.8 一样未在网络任务上训练，漏洞"发现"接近 Mythos 5 但"利用"能力大幅落后，生物与进攻性网络能力均不及 Mythos 5。

## 关键发现 / 关键技术

### 1. 编码与知识工作新 SOTA
- Frontier-Bench v0.1 上超越所有模型，以更低单任务成本达到 Opus 4.8 两倍以上的性能
- CursorBench 3.2 max effort 档位距 Fable 5 峰值仅 0.5%，但单任务成本减半
- ARC-AGI 3（新颖问题求解）得分为次优模型的 3 倍；Zapier AutomationBench 通过率约为次优模型 1.5 倍；OSWorld 2.0 以约三分之一成本超越 Fable 5 最佳成绩

### 2. 科学研究与自主纠错能力
- 生命科学评估全面优于 Opus 4.8：有机化学（光谱推断分子结构）+10.2 个百分点，蛋白质序列变异功能预测 +7.7 个百分点
- 展示强自我验证行为：无视觉输入时自写计算机视觉流水线重建 3D 机械零件；为开源包管理器找到社区补丁遗漏的根因；无对照数据源时自建测试框架校验代码

### 3. 安全分层与防护设计
- 延续 Opus 4.8 策略，刻意不在网络任务上训练；OSS-Fuzz 评估中漏洞"发现"接近 Mythos 5，漏洞"利用"远落后
- 网络分类器干预频率预计比 Fable 5 低约 85%：放行源码漏洞发现，拦截二进制扫描、渗透测试与 exploit 生成；被拦截请求默认回退 Opus 4.8
- 生物防护与 Opus 4.8 同级，Fable 5 上被拦截的生物请求改路由至 Opus 5；CVP（Cyber Verification Program）为受信企业提供低限制版本

### 4. 配套平台更新
- Beta：对话中途更换工具（Mid-conversation tool changes）且不失效 prompt cache；API 自动 fallback（被分类器标记的请求自动路由其他模型）
- 无一般访问的数据保留要求；API 名称 `claude-opus-5`

## 实践意义

Opus 5 把前沿模型的竞争重心从"绝对智能"推向"智能/成本曲线"：effort 档位 + Fast 模式让同一模型覆盖从日常问答到高难度 agentic 任务的全频谱，企业可按任务复杂度精细控制账单。对 Agent 工程，对话中换工具不失效缓存、自动 fallback 两个 beta 直接降低多工具 Agent 的运维复杂度。安全姿态上，"发现/利用能力分层 + 分类器回退"为高能力模型的差异化开放提供了可参考的部署范式。

## 跨厂商对比

- 与 [GPT-5.6](../../openai/research/introducing-gpt-5-6.md) 对比：两家 7 月旗舰不约而同采用"effort 档位化智能"（GPT-5.6 的 max/ultra 对 Opus 5 的 low–max + Fast 模式）；安全路径不同——OpenAI 走高风险能力差异化访问控制，Anthropic 走安全分类器 + 自动回退
- 与 [Project Glasswing](glasswing-initial-update.md) 互补：Glasswing 展示 Mythos 级模型的漏洞发现前沿，本文则说明 Opus 5 刻意与"利用"能力保持距离——Anthropic 在同一产品线上做能力分层
- 与 [Discovering cryptographic weaknesses with Claude](discovering-cryptographic-weaknesses.md) 互补：密码分析突破来自 Mythos 级前沿模型，Opus 5 则是"对齐优先"的日常主力，两者构成 Anthropic"前沿探索 / 安全量产"的双轨

## 资源

- System Card：[Claude Opus 5 System Card](https://www.anthropic.com/claude-opus-5-system-card)
- Prompting 指南：[Prompting Claude Opus 5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5)
- 文档：[Mid-conversation tool changes](https://platform.claude.com/docs/en/build-with-claude/mid-conversation-system-messages) / [Automatic fallbacks](https://platform.claude.com/docs/en/build-with-claude/refusals-and-fallback#server-side-fallback)
