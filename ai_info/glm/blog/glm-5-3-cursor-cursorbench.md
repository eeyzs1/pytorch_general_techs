# Cursor 上线 GLM-5.3/GLM-5.3-Flash:CursorBench 4.0 开放权重模型最高分 42.6%(GLM-5.3 Debuts on Cursor)

- **原文链接**: [智谱股价涨近5% GLM-5.3海外走红](https://stcn.com/article/detail/4206401.html)
- **作者**: 证券时报网（聂英好）
- **发布日期**: 2026-10-05
- **检索日期**: 2026-10-16
- **标签**: #GLM-5.3 #Cursor #CursorBench #开放权重 #海外分发 #编码工具

## 核心观点

10 月 5 日,AI 编程工具 Cursor 宣布上线 GLM-5.3 及 GLM-5.3-Flash。官方榜单显示,GLM-5.3 在 Max 推理设置下以 42.6% 的得分取得 Cursor 自有编程评测 CursorBench 4.0 中开放权重模型的最高分——中国开源权重模型首次进入全球头部 AI 编码工具的可选模型行列并拿下细分榜首。

同期海外认可接连而至:德国主权 AI 厂商 Aleph Alpha 发布的新模型 Kolibri 披露对 GLM 的使用。消息带动智谱港股(02513.HK)10 月 5 日早盘涨 4.95% 报 657.5 港元。

从 8 月以 Ox-Alpha 匿名身份登顶 OpenRouter/OpenCode,到 10 月被 Cursor 正式接入并由第三方自有基准验证,GLM-5.3 系列完成了"匿名验证→第三方基准→主流工具分发"的三级跳——海外开发者触达从 API 聚合平台延伸进编码工具内部。

## 关键发现 / 关键技术

### 1. Cursor 接入与 CursorBench 4.0 成绩
- Cursor 上线 GLM-5.3 与 GLM-5.3-Flash 两款模型,旗舰与经济版组合进入其模型选择列表
- GLM-5.3 在 Max 推理设置(最强推理档)下取得 CursorBench 4.0 开放权重模型最高分,官方榜单得分 42.6%
- CursorBench 为 Cursor 自有编程评测,面向真实编码工作流而非纯竞赛题;42.6% 为开放权重模型档位最高分(整体榜单上方仍有闭源模型)

### 2. 主权 AI 采用:德国 Aleph Alpha Kolibri
- 德国主权 AI 厂商 Aleph Alpha 发布新模型 Kolibri,披露了对 GLM 的使用
- 继 Ox-Alpha 匿名走红与开源社区量化版本之后,欧洲主权 AI 供应链开始把 GLM 作为组件
- GLM 系列近期"接连获得海外认可"成为智谱股价上行的直接催化剂(10-05 涨 4.95%,10-06 再涨逾 7%)

### 3. 三级跳:从匿名公测到工具内分发
- 2026-08:GLM-5.3-Flash 以 Ox-Alpha 匿名身份登顶 OpenRouter/OpenCode(6 天 62 万亿 token),揭晓后使用量超 DeepSeek 一倍以上
- 2026-09:RSI Infra Agent 支撑 10 万卡国产集群,FlashX 以速度分层承接需求
- 2026-10:Cursor 接入 + CursorBench 4.0 开放权重最高分——分发形态从"开发者主动调用 API"升级为"工具默认可选",获客成本与信任门槛同步下降

## 实践意义

对开发者,Cursor 内直接可用 GLM-5.3 意味着开放权重模型首次在头部工具内与闭源旗舰同台可选,按需在效果(CursorBench 得分)、速度(FlashX/Flash)与成本间组合的空间显著扩大。

对模型厂商,这条路径验证了"匿名公测攒口碑→第三方基准背书→工具渠道分发"的低成本出海范式——相比自建渠道,进入 Cursor 这类聚合入口的边际获客成本极低,但前提是公开基准上有可验证的排名。

对行业,开放权重模型进入闭源工具的默认选项列表,标志着"开源=落后一代"的旧假设被进一步打破;自有真实工作流基准(CursorBench)正成为继 SWE-bench 之后对国产模型更有区分度的考场。

## 跨厂商对比

- 与 [GLM-5.3-Flash](glm-5-3-flash.md) 对比:Ox-Alpha 匿名登顶解决"能力是否真实",Cursor 接入解决"开发者敢不敢用"——匿名公测与工具分发是同一出海策略的先手与后手
- 与 [GLM-5.3](glm-5-3.md) 对比:发布时"暂缓开源+AA 指数 60 分"的能力主张,两个月后拿到海外第三方自有基准(开放权重最高分)验证,海外评分体系开始为国产模型建立对照坐标
- 与 [Introducing GPT-5.3 Codex](../../openai/research/introducing-gpt-5-3-codex.md) 对比:OpenAI 以自研工具(Codex)+云分发巩固编码生态,智谱则以开放权重+接入第三方工具(Cursor/ZCode)反打——闭源自营与开源嵌入两条路线在编码工具层正面相遇
- 与 [Kimi K2.7 Code](../../kimi/blog/kimi-k2-7-code.md) 对比:同为国产开放权重编码模型,Kimi 走开源社区+自证基准路线,GLM-5.3 本轮额外拿到了海外头部工具的渠道位,"基准分+渠道位"的组合更完整

## 资源

- 媒体报道:https://stcn.com/article/detail/4206401.html
- 模型文档:[GLM-5.3 - 智谱AI开放文档](https://docs.bigmodel.cn/cn/guide/models/text/glm-5.3)
- 相关文章:[GLM-5.3-Flash](glm-5-3-flash.md)(Ox-Alpha 匿名公测前奏)

> 注:Cursor 官方公告与 CursorBench 4.0 榜单以 Cursor 官网为准(本文基于证券时报报道交叉验证);智谱官方渠道无法直接抓取。
