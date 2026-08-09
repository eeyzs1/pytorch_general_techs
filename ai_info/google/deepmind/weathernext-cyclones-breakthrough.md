# WeatherNext 气旋预测突破：AI 额外赢得一天预警时间（WeatherNext AI model achieves breakthrough in forecasting cyclones）

- **原文链接**: [WeatherNext: AI model achieves breakthrough in forecasting cyclones](https://deepmind.google/blog/weathernext-ai-model-achieves-breakthrough-in-forecasting-cyclones/)
- **作者**: WeatherNext team（Google DeepMind 与 Google Research）
- **发布日期**: 2026-08-06
- **检索日期**: 2026-08-08
- **标签**: #天气预报 #气旋预测 #WeatherNext #开源模型 #Science

## 核心观点

Google DeepMind 在《Nature》发表论文，宣布 WeatherNext AI 模型在预测热带气旋的路径、强度和风场结构上达到 SOTA 精度。平均而言，模型的三天预报达到了此前模型两天预报的水平——相当于为预报员多赢得一整天的提前量，约等于过去十年的气象学进展。该工作由 Google DeepMind、Google Research 联合美国国家飓风中心（NHC）、CIRA、英国气象局及全球多家气象机构共同完成。

在 2025 飓风季，该模型已帮助 NHC 完成对飓风 Melissa 历史性登陆牙买加的预报。本次同步开源 WeatherNext 2 与 WeatherNext Cyclones 模型代码及权重，并发布可在单块 TPU 上运行的 WeatherNext 2-mini。

## 关键发现 / 关键技术

### 1. 单模型统一路径与强度预测
- 传统方法需两类模型：粗分辨率全球模型预测路径（受大尺度环流驱动），高分辨率专用模型预测强度（受核心热力学过程驱动）
- WeatherNext Cyclones 用单一 AI 模型同时预测路径、强度与风场结构，桥接了这一权衡
- 在 2023-2024 年历史气旋上评测，路径、强度、风场结构的提前量优势均超过 24 小时

### 2. 训练数据与架构
- 双模态协同训练：近 20TB 全球大气数据 + IBTrACS 历史气旋数据库（近 5000 场历史风暴）
- 使用 Functional Generative Networks（FGN）高效生成集成预报集合，捕捉天气固有不确定性
- 单块 TPU 上不到一分钟生成一份 15 天预报；集成规模从去年的 50 成员扩展到 1000 成员，可捕捉快速增强等罕见但关键场景

### 3. 低分辨率反直觉表现与开源
- WeatherNext Cyclones 仅需 28×28km 分辨率数据，比传统模型粗 100 倍；WeatherNext 2-mini 在 111×111km 也能表现优异
- 开源代码与权重（GitHub），含 WeatherNext Cyclones、WeatherNext 2、WeatherNext 2-mini（Colab notebook 可免费运行）
- Weather Lab 网站刷新界面，新增全球天气可视化

## 实践意义

这是 AI 天气预报从"接近业务"到"改变业务"的里程碑：24 小时的额外提前量在防灾减灾中可直接转化为疏散与物资准备时间。开源策略意味着各国气象机构、研究者甚至非营利组织都能基于该模型构建本地化预报，降低了对少数商业数值天气预报供应商的依赖。低分辨率即可达到高精度的反直觉发现，也为未来模型设计打开了新思路。

## 跨厂商对比

- 与 [WeatherNext 飓风预测](weathernext-hurricane.md) 衔接：前者记录 WeatherNext 在飓风 Melissa 事件中的实战部署，本文是该能力的系统化论文总结与模型开源，两者共同构成从案例验证到科学发表的完整闭环

## 资源
- 论文：[Nature s41586-026-10953-2](https://www.nature.com/articles/s41586-026-10953-2)
- 代码：[github.com/google-deepmind/weathernext](https://github.com/google-deepmind/weathernext)
- Demo：[Weather Lab](https://deepmind.google/science/weatherlab/)
