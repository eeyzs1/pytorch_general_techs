# 强化蒸馏防御：推理 token 外泄降低 10–100 倍（Strengthening our defenses against distillation attacks）

- **原文链接**: [Strengthening our defenses against distillation attacks](https://www.anthropic.com/research/distillation-defenses)
- **作者**: Anthropic Policy 团队
- **发布日期**: 2026-10-12
- **检索日期**: 2026-10-16
- **标签**: #蒸馏攻击 #推理保护 #preserved-thinking #分类器 #国家安全

## 核心观点

Anthropic 披露反蒸馏体系的三层升级及实测效果：新防护上线后，蒸馏者从自有平台提取的推理 token 稳定下降 10–100 倍（部分日子低到无法测量），早期证据显示收割数据减少约 90–99%。背景指控具体而严厉： illicit distillation 被定性为" covert、工业规模"的能力窃取，智谱在 GLM-5.3 开发中蒸馏美国领先模型的网络能力（先试 Fable 5，因网络护栏削弱攻击效果而改用旧 Claude 与他厂模型）；Moonshot 曾把 Kimi 请求暗中转发给 Claude 并收集对话用于训练，其中含疑似解放军相关用户分析特定个人 CCTV 的请求。

三层防御：preserved thinking（新 API 账户禁止编辑历史上下文 + 跨模型读取隔离 + Sonnet 5.5 推理仅本组织可见）、两阶段宪法分类器（鲁棒性对标生物武器防护、误报率 <0.1%）、重复尝试限制（9/24 起对被拦截请求恢复计费）。官方坦承代价：推掉真金白银的付费流量、部分开发者需改造集成。

## 关键发现 / 关键技术

### 1. 为什么"推理"是主战场
- 蒸馏最有价值的数据是 Claude 的 thinking transcript——教会小模型"如何得出答案"，而非答案本身
- 实验：预训练 Claude 用 Opus 4.8 全量 transcript 训练后 SWE-bench Verified 80.4%，只用摘要版 71.8%——摘要化让 transcript 大幅贬值

### 2. 攻防升级的三个回合
- 第一回合（被动蒸馏）：推理先摘要再展示——蒸馏者转向"主动提取"
- 第二回合：简单检测器拦截"逐字复述先前推理"类请求——蒸馏者用 12,000 种变体请求 + 数十万假账号代理网络绕过（单一网络曾同时运营 2 万+ 假号）
- 第三回合（现行）：preserved thinking 断代理网重试；分类器抓住 9 月报告披露的全部技术；发现新绕过（翻译早期推理、标签内重写）数日内热修

### 3. 效果与代价
- 分类器运行于 Sonnet 5.5、Opus 5/5.5、Fable 5/5.1 等最被觊觎的模型
- 数万蒸馏账号被封，通常在开始行动 2 小时内
- 误报 <0.1%，但恢复对被拦请求计费（仅限达标领域）；preserved thinking 要求开发者改造集成

### 4. 行业呼吁
- 防御需全行业对齐：若他厂模型无同等反蒸馏护栏，攻击者会转移（智谱即因 Fable 5 护栏而换目标）
- 平台（云/推理服务商）有责任快速处置欺诈账号
- 承认"军备竞赛将持续"，尚未经受最高强度定向攻击检验

## 实践意义

蒸馏从"灰色地带"进入"防护对标生物武器"的强度等级，其连带影响值得所有 API 用户注意：编辑对话历史的新账户限制、被拦截请求开始计费、误报申诉流程——集成设计需假设"部分请求会被拒且计入成本"。对开源/开放权重阵营的警示：Anthropic 实测"网络护栏会降低蒸馏价值"，意味着无护栏开放权重模型既是最易被滥用的，也可能是蒸馏数据的最大受益者。数据点本身（12,000 变体请求、2 万假号网络）是理解工业级蒸馏规模的 rare 公开量化。

## 跨厂商对比

- 与 [GLM-5.3 and the spread of advanced cyber capabilities](glm-5-3-and-the-spread-of-advanced-cyber-capabilities.md) 互补：一篇讲被蒸馏出来的模型多危险，本文讲蒸馏行为本身如何被反制——同一事件的攻与防两侧
- 与 [Detecting and Countering Misuse of AI: September 2026](threat-intelligence-report-september-2026.md) 对比：威胁情报报告首次点名智谱/Moonshot 蒸馏细节，本文给出工程响应——披露与防御的接力
- 与 [Claude 文本水印](../engineering/claude-text-watermarking.md) 对比：水印保护"输出来源可溯"，蒸馏防护保护"推理过程不被收割"——内容主权与能力主权的两种技术产权主张

## 资源

- 论文：无
- 代码：无
- Demo：无
- 相关：preserved thinking 文档 https://platform.claude.com/docs/en/build-with-claude/preserved-thinking
