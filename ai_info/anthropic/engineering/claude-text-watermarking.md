# Claude 文本水印的工作原理（How Claude's text watermarking works）

- **原文链接**: [How Claude's text watermarking works](https://www.anthropic.com/news/claude-text-watermark)
- **作者**: Anthropic
- **发布日期**: 2026-08-11
- **检索日期**: 2026-08-21
- **标签**: #Anthropic #水印 #AI溯源 #内容认证 #EUAIACT #C2PA #透明性

## 核心观点

Anthropic 宣布为 Claude 生成的所有文本与文件嵌入隐形水印，用以标记 AI 生成内容，符合欧盟 AI 法案（EU AI Act）对 AI 内容可追溯性的要求。水印嵌入在模型生成阶段，而不是事后附加，因此即使文本被编辑、改写或复制粘贴，水印仍可被检测。

这一设计试图在"可追溯"与"可用性"之间取得平衡：水印对人类不可见、几乎不损害文本质量，但可被 Anthropic 的检测工具识别。Anthropic 同时解释了水印技术的原理与局限，承认其并非完美——改写幅度足够大的文本可能逃逸检测，这与所有 AI 内容水印的物理极限一致。

## 关键发现 / 关键技术

### 1. 生成时嵌入而非事后附加
- 水印在模型采样阶段通过选择特定 token 组合嵌入
- 与 C2PA 元数据（事后附加）形成互补，即使元数据被剥离仍有水印兜底
- 文本与文件（含代码）均覆盖

### 2. 隐形与稳健性权衡
- 对人类不可见，不影响可读性
- 检测器可区分"Claude 生成"与"人类撰写"，提供判定 API
- 局限：大规模改写、翻译、摘要可能降低检测置信度

### 3. 全球部署与合规
- 面向全球用户，不只是欧盟（区域无法完全隔离）
- 回应 EU AI Act 第 50 条对 AI 内容标识的要求
- 提供水印检测工具供内容平台与监管机构使用

### 4. 社区争议
- 部分创作者担忧"AI 烙印"影响原创内容可信度
- Anthropic 强调水印不改变内容所有权，仅标记来源

## 实践意义

AI 内容溯源进入"默认开启"时代。对企业与内容平台而言，识别 AI 生成内容的能力正成为合规刚需；对创作者而言，水印影响的是可追溯性而非版权。OpenAI 早在 2026 年 5 月就推出 C2PA + SynthID 内容溯源方案，Anthropic 本次以生成时水印补上了"元数据可剥离"的短板，两家方案正趋同于"元数据 + 生成水印"双保险。

## 跨厂商对比

- 与 [OpenAI 推进内容溯源](../../openai/research/advancing-content-provenance.md) 对比：OpenAI 主打 C2PA 元数据 + SynthID 图像水印，Anthropic 主打生成时文本水印，两者在文本溯源上互补
- 与 [Claude Enterprise 推理钩子](claude-enterprise-inference-hooks.md) 互补：推理钩子管"谁用了数据"，水印管"内容来自哪里"，共同构成企业合规闭环
- 与 [改进 Fable 5 的生物学安全防护](../../anthropic/research/improving-fable-5-biology-safeguards.md) 对比：同属"内容治理"谱系——生物防护管危险内容生成，水印管 AI 内容识别

## 资源

- 论文：N/A
- 官方公告：https://www.anthropic.com/news/claude-text-watermark
- 相关（OpenAI 内容溯源）：https://openai.com/index/advancing-content-provenance/
