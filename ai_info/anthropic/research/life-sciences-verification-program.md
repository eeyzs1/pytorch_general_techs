# 生命科学访问计划 LSVP 公测（Life Sciences Verification Program）

- **原文链接**: [Life Sciences Verification Program](https://www.anthropic.com/news/life-sciences-verification-program)
- **作者**: Anthropic
- **发布日期**: 2026-09-17
- **检索日期**: 2026-09-29
- **标签**: #生物安全 #LSVP #访问控制 #药物发现 #双用途 #信任访问

## 核心观点

生命科学访问计划（LSVP）于 2026-09-17 进入公开测试：通过审核的组织可获得 Mythos/Opus/Sonnet 系列模型，并配以生物学上更宽松的精调分类器，解除药物发现、研究生物学、临床开发与生产制造场景的封锁。

early-access 阶段已接入数十家机构，现开放申请——先面向团队/机构，后续扩展到 Pro/Max 个人用户。

计划设两级授权：Standard Use 按团队年度续期（覆盖 Mythos 5.1/Opus 5/Sonnet 5）；High-risk Use 按项目六个月续期并移除生物拦截，其中 Opus 5/Sonnet 5 即日可用，Mythos 需与美国政府协调、暂限少量实体。

机制上的创新是从实时拦截转向"对照申报用途的离线监控"：申报安全使用范围→监测越界→限期整改；监控数据留存 30 天，隔离存放、不用于训练、对研究团队不可见。

## 关键发现 / 关键技术

### 1. 目标与解锁范围
- 通过审核的组织获得 Mythos/Opus/Sonnet 系列 + 生物学更宽松的精调分类器
- 解锁四类场景：药物发现、研究生物学、临床开发、生产制造
- 解锁前，这些场景的策略是直接拦截或回退到低防护模型
- 更宽松的精调分类器随授权下发；未获授权用户仍走默认严格分类器

### 2. 两级授权设计
- Standard Use：按团队授权、年度续期；覆盖 Mythos 5.1、Opus 5、Sonnet 5
- High-risk Use：按项目授权、六个月续期；移除生物拦截
- High-risk 的模型分层：Opus 5/Sonnet 5 即日可用；Mythos 需与美国政府协调，暂限少量实体
- 两级设计把"谁能用"与"能用多敏感的能力"拆开管理

### 3. 威胁模型
- 凭据被盗：已授权账号被外部攻击者获取
- 内部人作恶：已授权研究人员故意越界使用
- agent 失控：自动化研究 Agent 在无人监督下漂移出申报用途
- 威胁模型直接决定监控数据的采集范围与留存策略

### 4. 机制创新:从实时拦截到对照申报用途的离线监控
- 用户申报安全使用范围，平台离线监测实际使用是否越界
- 越界触发限期整改，而非实时打断科研工作流
- 误报不再阻塞合法研究；监控重心从"请求内容"转向"使用行为"
- 相比 Fable 5 发布时的"宽分类器 + fallback"，LSVP 把误报治理从模型层移到授权层

### 5. 数据留存与生态背书
- 监控数据留存 30 天：隔离存放、不用于训练、研究团队不可见
- early-access 参与方背书：Xaira、Edison Scientific、Manifold Bio
- 申请先团队/机构、后 Pro/Max 个人，入口见发布页

## 实践意义

LSVP 是 [改进 Fable 5 的生物学安全防护](improving-fable-5-biology-safeguards.md) 中承诺的 trusted access pathways 的落地：分类器精化解决"误报太多"，LSVP 解决"该放开的人拿不到"，两者合成生物双用途能力的分级开放体系。

对企业，药物发现与生产制造团队首次有了合规使用最强模型的正式通道，研究工作流不必再绕开 AI 或忍受误报拦截。

对平台治理，"申报用途 + 离线监控 + 限期整改"把安全从请求级拦截升级为合同级治理——这一范式可迁移到网络安全等其他双用途领域的受控访问设计。

## 跨厂商对比

- 与 [改进 Fable 5 的生物学安全防护](improving-fable-5-biology-safeguards.md) 互补：前者精化分类器边界（生物学 fallback 减少约 85%），本文建立授权与监控通道——一个调"边界"、一个建"通道"，共同构成 Anthropic 生物安全的分级开放体系
- 与 [Strengthening societal resilience with Rosalind biodefense](../../openai/research/strengthening-societal-resilience-with-rosalind-biodefense.md) 对比：两家都把双用途生物能力绑定到机构级 trusted access；Anthropic 的差异点在"申报用途 + 离线监控 + 两级授权（团队/项目）"的治理颗粒度，OpenAI 更侧重生物防御应用与社会韧性
- 与 [Claude Opus 5.5 发布](claude-opus-5-5.md) 互补：Opus 5.5 出厂即配 Fable 5.1 级生物防护，LSVP 是该防护体系面向合法科研的出口——同一周期"模型 + 通道"配套落地
- 与 [Claude uplifts biomolecular modeling](claude-uplifts-biomolecular-modeling.md) 互补：后者量化 Claude 对生物分子建模的能力提升，正说明此类能力为什么需要 LSVP 式的受控开放而非全面放开

## 资源

- 发布页：https://www.anthropic.com/news/life-sciences-verification-program
- 代码：N/A
- Demo：N/A
