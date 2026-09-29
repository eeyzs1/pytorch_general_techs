# 测量 AI 模型的战术情报定位与常规武器能力（Measuring intelligence targeting and conventional weapons capabilities of AI models）

- **原文链接**: [Measuring intelligence targeting and conventional weapons capabilities](https://www.anthropic.com/research/intelligence-targeting-conventional-weapons-capabilities)
- **作者**: Anthropic Frontier Red Team
- **发布日期**: 2026-09-10
- **检索日期**: 2026-09-29
- **标签**: #FrontierRedTeam #危险能力评估 #地理定位 #身份关联 #无人机 #常规武器 #双用途

## 核心观点

Frontier Red Team 对杀伤链前段（情报收集与定位）与后段（常规武器制导）做系统性危险能力评估，覆盖三类任务：跨平台身份关联、照片与文本地理定位、四旋翼 GNC 武器代码。结论：前沿闭源模型在情报段已超过冠军级人类专家，武器段在理想条件下命中率高、低可视条件急剧退化；开源权重模型整体落后，但绝对水平"令人担忧"。

评估给出了量化的人类基准：照片地理定位上 Mythos Preview 中位误差 37.0 km，优于 GeoGuessr 冠军级人类的 151 km；跨平台身份关联中，3.7 万词证据样本人类阅读需 2.5 小时，Mythos Preview 约需 11 分钟。作为响应，Anthropic 已上线武器开发拦截分类器。

## 关键发现 / 关键技术

### 1. 跨平台身份关联（200 个合成社媒任务）
- 任务：从多个合成社交媒体账号的行为痕迹中关联出同一自然人
- 任务按难度分档：易 / 中 / 难
- Mythos Preview 最强；开源的 Kimi K3 在易、中档任务上接近前沿水平
- 证据规模：单样本约 3.7 万词——人类阅读需 2.5 小时，Mythos Preview 约 11 分钟

### 2. 照片地理定位（6000 张 Flickr 照片）
- Mythos Preview 中位误差 37.0 km、Mythos 5 为 47.2 km
- 两者均优于 GeoGuessr 冠军级人类的 151 km
- Claude Opus 5 为 181 km
- Sonnet 5 与 Kimi K3 均为 385 km

### 3. 文本地理定位
- 从用户生成文本推断其位置：中位误差 20-31 km
- 约 8% 的案例可将目标用户锁定到 1 km 以内——足以定位到具体街区或建筑

### 4. 四旋翼 GNC 武器代码（全场 540 次发射）
- 静止高可视目标：Opus 5 命中率 80%
- 移动目标：降至 47%
- 低对比度目标：仅 8%，环境约束下能力急剧退化
- 全场汇总：Opus 5 命中 20%、Mythos Preview 13%、Kimi K3 1.6%
- GPS 拒止环境下，模型会主动改用 IMU 航位推算维持制导

### 5. 开源权重模型与防御响应
- Kimi K3、GLM 5.2 等开源权重模型落后于闭源前沿，但提升速度"令人担忧"
- 已上线武器开发拦截分类器，阻断相关代码生成请求
- 评估方法学：以"冠军级人类"而非普通人为基准，是危险能力评估应有的严格标准
- 与同日发布的威胁情报报告互为印证：能力测量对照现实滥用

## 实践意义

杀伤链正被 AI 压缩，但两端速度不均：

- 对安全团队：情报段（定位、关联）已超人类专家水平且边际成本趋近于零，防御重心应放在武器段的环境脆弱性与平台侧拦截上
- 对政策制定者：8% 的文本定位可到 1 km 内意味着"匿名发帖"不再隐含位置隐私；开源权重模型的能力追赶要求发布决策持续重评
- 对评估方法学：受控测量（能力上限）与滥用报告（现实分布）必须成对发布，本文与同日威胁情报报告即采用该模式

## 跨厂商对比

- 与 [Project Pilot：AI 能控制无人机吗？](project-pilot.md) 互补：Project Pilot 测通用物理 Agent 的双用途控制能力，本文专门沿杀伤链分解测量攻防两端
- 与 [Measuring LLMs' Impact on N-day Exploits](n-days.md) 对比：网络域双用途测量（N-day 利用）与物理域双用途测量（情报定位 + 常规武器）共用"能力上限 vs 现实滥用"框架
- 与同批 [检测与反制 AI 滥用：2026 年 9 月](threat-intelligence-report-september-2026.md) 互补：本文给出能力上限的受控测量，该报告给出 2025-12 至 2026-08 的现实滥用分布

## 资源

- 官方文章：https://www.anthropic.com/research/intelligence-targeting-conventional-weapons-capabilities
- 配套威胁情报报告：https://www.anthropic.com/threat-intelligence-report-september-2026
- 论文：N/A
