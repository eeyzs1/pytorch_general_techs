# OpenAI 应对欧盟文本溯源规则的路径：textGrain 水印（Our approach to EU text provenance rules）

- **原文链接**: [Our approach to EU text provenance rules](https://openai.com/index/eu-text-provenance)
- **作者**: OpenAI
- **发布日期**: 2026-10-05
- **检索日期**: 2026-10-16
- **标签**: #AI法案 #水印 #内容溯源 #合规 #检测器

## 核心观点

为履行欧盟 AI Act 第 50(2) 条（生成文本须机器可读标记，2026-08-02 起生效；既有系统宽限至 12-02），OpenAI 发布统计水印 textGrain 并配发 20 页技术报告：信号藏在选词本身（无隐藏字符），未来数周应用于欧盟境内 ChatGPT 与 Codex 的合格文本；API 端 10-05 起全球可选开启但默认关闭；检测器访问首批只开放给获批研究者与专家组织。选择"只在法律要求的地域打标"让 OpenAI 与 Anthropic 的"全球打标"路线形成鲜明分野。

## 关键发现 / 关键技术

### 1. 机制：熵预算 + 最优传输
- 生成时把部分采样随机性替换为"密钥 + 前文"驱动的伪随机值：词表划分为块，用 Gumbel 成本的最优传输问题引导选块，块内保持原始相对概率——只改"选哪一块"，少伤质量。
- "熵预算"（entropy budget）显式权衡"让出多少随机性换信号"，并解决 Gumbel-max 水印"同 key 同 prompt 产出完全相同"的问题（多_variant 场景不可用）。
- 报告由 5 位 OpenAI 研究者与宾夕法尼亚大学、耶鲁学者联合署名；理论假阳率依赖独立性假设，部署密钥需经验校准。

### 2. 检出率（1% 假阳目标，ELI5 英文数据）

| 场景 | 检出率 |
|------|--------|
| 400 token（心理学话题） | ~95% |
| 200 token | ~80% |
| 400 token、10% 词被同义替换 | ~92% → 66% |
| 400 token、25% 词被替换 | 17% |
| 数学内容 | 明显更低（~60% @400 token，第三方读图） |
| 23 种欧盟语言（翻译版 500 prompt） | 42.2%（罗马尼亚语）~ 69.0%（西班牙语） |

- 低于 60% 的语言用可调强度参数加强；大幅改写或翻译可致不可检测；官方明言"未检出水印不能证明是人类写作"。

### 3. 合规设计要点
- 欧盟《AI 生成内容透明度实践准则》豁免 <200 token 的"极短文本"；OpenAI 是准则签署方（约 190 家组织之一）。
- 检测器限研究者先行（Cornell、ETH Zurich、KInIT 等合作方）——准则允许对自由文本检测做时限性限制，但须向监管、执法、媒体、事实核查、独立研究者等提供受控免费访问。
- API 集成商注意：水印非请求参数，须在组织/项目设置里手动开启；默认关闭意味着集成商不能"搭便车"依赖上游标记，合规责任回落自身。
- textGrain 计划开源（无日期）；官方评估称文本上"追平或超过 SynthID"。

## 实践意义

1. **按地域合规 vs 全球统一**：OpenAI 只在 EU 打标（最小合规），Anthropic 基于 SynthID-Text 全球打标（无按区隔离手段）——产品出海与多区域架构需评估两种策略的连带影响。
2. **水印强度的物理边界首次量化披露**：25% 同义替换即跌至 17% 检出，说明"防洗稿"不能只靠水印，需叠加元数据与行为检测。
3. **检测器准入成为新的治理接口**：谁能查水印由平台分配——新闻编辑室、大学在准则名单内，HR 查求职信不在；检测能力的分发本身正在被监管塑形。

## 跨厂商对比

- 与 [Advancing Content Provenance](advancing-content-provenance.md) 对照：6 月的多层策略（C2PA 凭证 + SynthID + 公共验证）覆盖图像音视频，textGrain 补上自由文本这块最难啃的拼图——同一家公司内"凭证派"与"统计水印派"并行。
- 与 [Anthropic Claude 文本水印（SynthID-Text 派生，8/14 全球上线 + 检测 API 私有预览）] 路线之争：Anthropic 因"无按区域收窄的可靠手段"而全局打标，OpenAI 借熵预算实现区域化——工程能力直接决定合规粒度。
- 与 [vLLM 9/24 集成 Gumbel-max 水印（Mistral/Red Hat 工程师署名）](https://vllm.ai/blog/2026-09-24-watermarking-in-vllm) 并观：开源推理栈先于多数厂商把水印做成默认能力，水印正从厂牌特性变为基础设施。

## 资源

- 官方博客：[Our approach to EU text provenance rules](https://openai.com/index/eu-text-provenance)
- 论文：[textGrain: Entropy-Calibrated Watermarking for Language Model Text（20 页技术报告 PDF）](https://cdn.openai.com/pdf/e9508624-d767-41b6-a26d-e34ca798ada6/textgrain-entropy-calibrated-watermarking-for-language-model-text.pdf)
- 第三方验证：[ActuIA 深度解析](https://www.actuia.com/en/news/openai-will-watermark-chatgpt-in-the-eu-but-leaves-the-api-opt-in/)、[The Decoder](https://the-decoder.com/openai-will-watermark-chatgpt-text-in-the-eu-but-makes-it-optional-for-api-users-worldwide/)
- 相关条目：[introducing-chatgpt-images-2-5](introducing-chatgpt-images-2-5.md)

> 注:openai.com 原文 403；技术细节与检出率经 ActuIA（引用官方 20 页报告与帮助中心）与 The Decoder 交叉验证。
