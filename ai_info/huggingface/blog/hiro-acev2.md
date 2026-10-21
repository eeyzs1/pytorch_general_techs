# HiRO-ACEv2：以 1/300 成本模拟 3 公里分辨率的极端天气（HiRO-ACEv2: Simulating extreme weather at 3 km resolution for a fraction of the cost）

- **原文链接**: [HiRO-ACEv2: Simulating extreme weather at 3 km resolution for a fraction of the cost](https://huggingface.co/blog/allenai/hiro-acev2)
- **作者**: Ai2 气候团队（Kyle Wiggers 执笔）
- **发布日期**: 2026-10-14
- **检索日期**: 2026-10-16
- **标签**: #气候仿真 #极端天气 #降尺度 #科学计算 #开源模型

## 核心观点

Ai2 更新其高分辨率输出气候模拟器：ACE（100 公里粗分辨率 AI 模型）+ HiROv2（把粗输出锐化到 3 公里细节）。HiROv2 两大变化：从只预报降雨扩展到同时预测多个高分辨率场（风、气压等），并能更好复现极端事件。全系统生成全球 3 公里气候数据的成本约为显式模拟风暴的 X-SHiELD 高分辨率大气模式的 1/300；只取单一区域时节省可再放大百倍以上。

极端事件是主战场：给定粗化的 X-SHiELD 数据，HiROv2 对高分辨率统计量的还原误差在 3% 以内，连百万分之一出现频率的罕见雨/风/气压极值也不例外；对训练中从未见过的飓风也能估准总能量，生成有眼与雨带结构的飓风（眼壁附近风压分布仍偏不对称）。ACE 与 HiROv2 串联已产出全年全球 3 公里数据，统计量与 X-SHiELD 高度一致。

## 关键发现 / 关键技术

### 1. 十年模拟与验证

- 更新版 ACE 十年模拟中的飓风、平均气候态、雨/风/气压分布与 X-SHiELD 对齐良好，证明粗模拟是长时高分辨率生成的可靠底座。
- 10 年 HiRO-ACEv2 模拟的飓风能量与同期 X-SHiELD 相当，期间自然出现多种与 X-SHiELD 相似的极端事件快照。

### 2. 可视化与可用性

- Web demo 并排展示 HiROv1/v2 与 X-SHiELD 的降水、风场、海平面气压输出，可缩放到任一区域做目检；模型可下载，教程笔记本覆盖运行方法。

### 3. 明确边界

- HiRO 从 X-SHiELD 学习，因此只能搭配对应调校的 ACE 版本；尚不能为其他气候（如升温 4°C 的世界或 ERA5 历史再分析）产出高分辨率数据——下一步将训练 +4°C X-SHiELD 数据集并增加近地面温度、冰雪输出（积雪预测等）。

## 实践意义

气候适应规划（城市排水、电网风载、保险定价）需要的是极端分布而非均值，全分辨率模式跑不起、粗分辨率模式看不见——降尺度模拟器把这个缝隙的价格压低两个数量级以上。开源权重 + 教程意味着区域研究机构可以自行生成定制情景数据。

## 跨厂商对比

- 与 [OlmoEarth 平台](olmoearth-infrastructure.md) 对比：同属 Ai2 地球科学栈——OlmoEarth 解决观测侧（卫星推理），HiRO-ACEv2 解决模拟侧（气候仿真），Ai2 正在搭"观测+模拟"双引擎。
- 与 [WeatherNext 飓风突破](../../google/deepmind/weathernext-hurricane.md) 对比：DeepMind WeatherNext 走中期天气预报的业务化路线，HiRO-ACEv2 走气候尺度极端事件统计的研究路线，AI 大气建模在"预报"与"气候"两条战线同时逼近物理模式。
- 与 [WeatherNext 3](../../google/deepmind/introducing-weathernext-3.md) 对比：Google 的分辨率与变量覆盖以产品服务交付，Ai2 以开源权重 + 1/300 成本叙事交付，公共部门与研究者是开源路线的直接受益者。

## 资源

- 论文：[HiRO-ACEv2 技术报告（arXiv 2610.17693）](http://arxiv.org/abs/2610.17693)
- 代码：[Ai2 教程笔记本](https://ai2cm.github.io/ace/)
- Demo：[ACE 数据可视化（ace.allen.ai）](http://ace.allen.ai)
