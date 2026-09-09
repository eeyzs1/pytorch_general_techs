# Muse Spark 1.3：面向长时程编码与 Agent 任务的新旗舰（Introducing Muse Spark 1.3）

- **原文链接**: [Introducing Muse Spark 1.3](https://research.meta.ai/blog/introducing-muse-spark-1-3)
- **作者**: Meta Superintelligence Labs / Meta
- **发布日期**: 2026-09-02
- **检索日期**: 2026-09-09
- 注：初稿基于二手交叉验证信源（官方站点检索时不可达）；2026-09-09 经 VPN 复核，research.meta.ai 官方列表已确认本文为Featured 条目（2026-09-02，标题一致），官方 URL 有效
- **标签**: #MuseSpark1-3 #编码模型 #长时程任务 #基准测试 #API定价

## 核心观点

Muse Spark 1.3 于 2026-09-02 发布，是 MSL 面向长时程（long-horizon）编码与 Agent 任务训练的新旗舰：编码基准超过 GPT-5.6 Sol 与 Claude Opus 5；第三方 Artificial Analysis Intelligence Index 上 1.3(max) 得 62 分，超过 GPT-5.6 Sol、追平 Claude Fable 5，Muse 系列首次跻身前沿智能第一梯队。

效率是另一条主线：较 1.2 工具调用约减少 20%、token 消耗约减少 25%；行为上强调协作——遇模糊指令先反问确认、受阻时主动请求补充指示。API 定价每百万 token 输入 $1.25、缓存输入 $0.15、输出 $4.25，另有以提供训练提示换折扣的 Contributor tier。Zuckerberg 同日预告 Muse Spark 开放权重即将发布。

## 关键发现 / 关键技术

### 1. 编码与智能基准：追平前沿
- 编码基准（含长上下文测试）超过 GPT-5.6 Sol 与 Claude Opus 5，在对比中居首
- AA Intelligence Index：1.3(xhigh) 61 分、1.3(max) 62 分——max 超过 GPT-5.6 Sol、追平 Claude Fable 5
- AA Agentic Index：1.3(xhigh) 56 分、1.3(max) 59 分——与 Claude Opus 5、GLM-5.3、Grok 4.6 并列
- Meta 首席 AI 官 Alexandr Wang 引用测量结果，称 1.3 性能高于同日发布的 Gemini 3.8 Flash

### 2. 效率与协作行为
- Meta 对比测试：较 Muse Spark 1.2 工具调用次数约 -20%、token 消耗约 -25%，处理速度与效率大幅提升，代码输出更精炼
- 协作式设计：收到模糊指示时先反问确认；处理受阻时向用户请求追加指示，而非硬猜
- 发布页内嵌一款用 Muse Spark 1.3 制作的互动游戏作为能力演示

### 3. 定价、推理档位与开放权重预告
- 每 1M token：输入 $1.25 / 缓存输入 $0.15 / 输出 $4.25（输入输出价与 1.1/1.2 持平，新增缓存档）；Contributor tier（以提供训练用提示为交换）：输入 $0.10 / 缓存输入 $0.002 / 输出 $0.20
- xhigh 推理档即时可用；max 档待安全测试完成后开放
- Zuckerberg 称其提供"frontier performance almost too cheap to meter"，并预告 Watermelon（🍉）与 Muse Spark 开放权重即将发布

## 实践意义

token 与工具调用双降直接改善长时程编码 Agent 的成本与时延：Agent 化工作流中单任务动辄上百次工具调用，20%/25% 的削减会线性放大到整体开销。$1.25/$4.25 的定价加上 Contributor tier 把前沿编码智能压到接近"按表计费"的价格带，将进一步加剧 API 市场价格竞争；开放权重预告则意味着本地部署与微调选项即将出现，值得编码工具链团队提前规划接入与评测。

## 跨厂商对比

- 与 [Muse Code 与 Muse Spark 1.2](introducing-muse-code-muse-spark-1-2.md) 对比：1.2 时期 Meta 把 Muse Spark 带入终端编码 Agent（Muse Code），1.3 在同一产品线上以更少的工具调用与 token 完成长时程任务，方向从"能编码"转向"高效长跑"
- 与 [Claude Opus 5 发布](../anthropic/research/claude-opus-5.md) 对比：Opus 5 以半价逼近 Claude Fable 5 的前沿智能，Muse Spark 1.3(max) 则以 AA Intelligence Index 62 分直接追平 Fable 5——两家从不同路径收敛到"前沿智能平价"；编码基准上 1.3 超过 Opus 5，但 Anthropic 的安全分类器与 effort 档位体系仍是差异点

## 资源

- 官方公告：https://research.meta.ai/blog/introducing-muse-spark-1-3
- 媒体报道：https://gigazine.net/news/20260903-meta-muse-spark-1-3/
