# WeatherNext 3：最先进准确的全球天气 AI 模型（Introducing WeatherNext 3）

- **原文链接**: [Introducing WeatherNext 3](https://blog.google/innovation-and-ai/models-and-research/google-deepmind/introducing-weathernext-3/)
- **作者**: Google DeepMind、Google Research（官方博客未署名）
- **发布日期**: 2026-09-02
- **检索日期**: 2026-09-09
  注：官方页面抓取受限，本文基于检索核验的日期与公开报道整理（数据经 DigitalToday 转引 TechCrunch 的报道核验）
- **标签**: #WeatherNext #天气预报 #AIforScience #气象模型

## 核心观点

Google DeepMind 与 Google Research 联合发布 WeatherNext 3，官方称其为最先进、准确的全球天气 AI 模型。两个量变构成升级重点：更新频率从上一代的每 6 小时一次提升到逐小时生成新预报；空间分辨率从 25 公里网格细化到温度、湿度等关键指标最高 5 公里（部分地表变量 10 公里、大气变量 25 公里）。

在 Brightband 运营的独立评测平台 Operational WeatherBench 上，该模型在温度、风速、湿度等多项评测中优于主流 AI 模型与传统气象模型。模型已进入 Search、Gemini、Google Maps、Google Maps Platform（Weather API）与 Cloud（BigQuery/Earth Engine），研究与企业用户还可经 Google Cloud Storage 下载数据。

## 关键发现 / 关键技术

### 1. 原始观测数据直连
WeatherNext 3 直接以逐小时更新的静止轨道气象卫星影像作为输入，并以特定气象站的实测数据作为训练目标；Google 称其为"首个直接使用原始观测数据的高分辨率全球 AI 预报模型"——竞争对手 Windborne 对"首个"提出异议，称其 WeatherMesh 自上一年起已使用气球等原始观测数据。

### 2. 降水与专业变量
以 NASA 卫星降水数据 IMERG 为基准，中期概率降水预报性能较上一代最高提升 60%；训练中还引入基于卫星雷达生成的自有再分析数据与雨量计实测值。另提供面向风电场景的 100 米高度风速预报以及日照量、云量预报，服务可再生能源运营。

### 3. 分发面
自发布日起接入 Search、Gemini、Maps 与 Google Maps Platform Weather API；研究者与企业用户可经 BigQuery 与 Earth Engine 查询相关数据，或经 Google Cloud Storage 下载。

## 实践意义

"逐小时 + 5 公里"的组合让 AI 预报覆盖了临近预报与中期预报之间的运营粒度，对物流、农业、能源调度等按小时决策的行业是直接可用的信号源；经 Maps Platform/BigQuery 的分发把气象能力变成可查询的数据资产。评估时注意：对比基准是天气 AI 与传统数值预报，而"首个使用原始观测数据"的声明存在厂商间争议。

## 跨厂商对比

- 与 [WeatherNext 气旋预测突破：AI 额外赢得一天预警时间](weathernext-cyclones-breakthrough.md) 对比：气旋突破展示 WeatherNext 在极端天气专项指标上的能力，WeatherNext 3 把能力泛化为全球逐小时、多变量的常规预报底座——专项深度 vs 代际广度。
- 与 [WeatherNext: Better Hurricane Prediction](weathernext-hurricane.md) 互补：飓风篇是高危场景的纵深案例，本文是模型代际升级（分辨率/频率/数据源）的全景，二者合看构成 WeatherNext 谱系的完整脉络。

## 资源

- 官方文章：https://blog.google/innovation-and-ai/models-and-research/google-deepmind/introducing-weathernext-3/
- 产品/API：https://deepmind.google/science/weathernext/
