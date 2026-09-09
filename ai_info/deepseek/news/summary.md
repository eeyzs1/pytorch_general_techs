# DeepSeek（深度求索）— 核心观点总结

> 汇总自 [DeepSeek API 文档](https://api-docs.deepseek.com/)、[官网](https://www.deepseek.com/) 及公开报道，当前覆盖 2026 年 4 月至 9 月。

## 一、总体脉络

深度求索（DeepSeek）在 2026 年呈现清晰的"效率革命 + 开源碾压 + 国产算力优先"战略：

```
架构效率突破（mHC / CSA / Engram）
    ↓
百万上下文工程化（1M tokens，计算量仅 V3.2 的 27%）
    ↓
双模型商业部署（V4-Pro + V4-Flash）
    ↓
定价创新（峰谷计费）+ 旧模型废弃迁移
    ↓
正式版 GA（DSpark 推测解码标配 + 后训练驱动的 Agent 跃升）
```

核心差异化：用 MIT 开源 + 极致性价比，对闭源模型形成"Opus 级能力、1/7 价格"的钳形攻势。7 月中旬 V4 全量转正（GA），揭晓此前的"预览即生产"发布策略；7 月 31 日 [V4-Flash 正式版](deepseek-v4-flash-official-release.md)（v4-flash-0731）仅靠重新后训练就在 Agent 基准上全面超越 V4-Pro 预览版，原生支持 Responses API 并适配 Codex 生态。8 月 13 日 [V4-Pro GA 与 API 调价](deepseek-api-price-adjustment-2026-08.md) 正式落地：新价格 8 月 16 日 16:00 UTC 生效（北京时间 8 月 17 日），部分模型涨幅最高 1100%，峰谷分时计费全面执行——低峰时段价格为高峰的 50%；V4-Pro GA 本身带来推理 effort 三档（low/high/max）与原生 Responses API。"价格屠夫"开始"收刀"，低价红利期结束，国产大模型商业化进入新阶段。

## 二、核心主题

### 1. DeepSeek-V4 双模型

[DeepSeek-V4](deepseek-v4.md) 于 2026-04-24 发布，是 V3（2024-12-26）之后 484 天的旗舰迭代：

| 模型 | 总参数 | 激活参数 | 上下文 | 最大输出 | 并发 |
|------|--------|----------|--------|----------|------|
| V4-Pro | 1.6T | 49B | 1M tokens | 384K | 500 |
| V4-Flash | 284B | 13B | 1M tokens | 384K | 2500 |

双模型均支持非思考 / Think High / Think Max 三档推理，API 兼容 OpenAI 与 Anthropic 双格式。第三方评测认为 V4 整体接近 Opus 4.8、编码直追 GPT-5.6 Sol，但相同任务迭代轮数多于 Fable 5。

### 2. 三大架构创新（基于论文原文）

- **mHC（流形约束超连接）**：arXiv:2512.24880。将残差混合矩阵 H_res 约束到双随机矩阵流形（Birkhoff polytope），用 Sinkhorn-Knopp 算法（1967）每层 20 次迭代投影，谱范数 ≤1 从根源截断梯度爆炸；27B 模型 Amax Gain 从 3000 降至 ~1.6，wall-time 开销仅 6.7%。
- **CSA + HCA 混合注意力**：arXiv:2606.19348（DeepSeek-V4 完整技术报告）。CSA 每 4 token 压缩为 1 KV entry + DSA Lightning Indexer Top-K 选择；HCA 激进压缩 128:1 但保持密集注意力；交替堆叠实现"详细但选择性"与"完整但低分辨率"视图互补。1M 上下文下单 token FLOPs 降至 V3.2 的 27%，KV cache 降至 10%。
- **Engram 条件记忆模块**：arXiv:2601.07372。现代化 N-gram 嵌入表，O(1) 哈希查找；27B 规模下 BBH +5.0、MATH +2.4、MultiQuery NIAH 84.2→97.0；与 MoE 存在 U 形缩放定律（最优 ~20-25% 参数分配给 Engram）。

### 3. DeepSeek-V4 正式版 GA 与 DSpark

[DeepSeek-V4 正式版 GA](deepseek-v4-ga.md)（2026-07-15）揭晓了与其他厂商完全不同的发布路径：4 月 24 日上线的实为"预览版"但从未标注，官方后台持续改进、灰度放量、收集反馈后全量转正。正式版补齐三块能力：

- **DSpark 推测解码标配**：半自回归 drafter + 置信度头 + 硬件感知调度，输出与目标模型逐字节一致；Flash 提速 60-85%、Pro 提速 57-78%，120 token/s 高并发场景吞吐提升 661%，与北大联合开源（MIT）
- **Agent 能力跃升**：Agent 完成率提升 21%，原生多模态与企业级工具链落地，首次完整开源（权重 + 训练脚本 + 推理代码）
- **V4-Flash-0731（7 月 31 日）**：架构不变仅重新后训练，Terminal Bench 2.1 达 82.7、DSBench-FullStack 68.7，全面超越 V4-Pro 预览版；原生支持 Responses API，可在 Codex CLI、ChatGPT 桌面端、VS Code 插件直接调用

旧模型名 `deepseek-chat` / `deepseek-reasoner` 已于 2026-07-24 正式停用。

[DeepSeek-V4-Flash 正式版发布](deepseek-v4-flash-official-release.md)（2026-07-31）是 V4-Flash-0731 公测的完整基准与配置细节。API 调用方式不变，只需将模型名设为 `deepseek-v4-flash`。架构与参数量与 V4-Flash-Preview 完全一致（284B 总参/13B 激活），仅通过重新后训练实现能力跃升。完整基准成绩：Terminal Bench 2.1 达 82.7、NL2Repo 54.2、Cybergym 76.7、DeepSWE 54.4、Toolathlon verified 70.3、Agent Last Exam 25.2、Automation Bench（Public）25.1；内部测试集 DSBench-FullStack 68.7、DSBench-Hard 59.6。公开基准中的 Code Agent 任务使用 DeepSeek Harness minimal mode（即将发布），配置为 max effort level、topp=0.95、temperature=1.0。正式版原生支持 Responses API 格式并专门适配 Codex——可在 Codex CLI、ChatGPT 桌面端、VS Code 插件中直接调用，无需协议转换即可接入 OpenAI 工具生态。本次仅升级 Flash API，V4-Pro API 与 App/Web 端模型暂未变更。这是"后训练杠杆大于架构迭代"的又一证据。

### 4. API 定价与峰谷计费

[DeepSeek-V4 API 定价](deepseek-v4-api-pricing.md) 于 2026-06-29 官宣，7 月中旬正式上线：

| 模型 | 输入（缓存命中） | 输入（缓存未命中） | 输出 |
|------|------------------|--------------------|------|
| V4-Flash | $0.0028/1M | $0.14/1M | $0.28/1M |
| V4-Pro | $0.003625/1M | $0.435/1M | $0.87/1M |

首次引入峰谷计费：高峰时段（每日 9:00-12:00、14:00-18:00）价格 ×2。旧模型名 `deepseek-chat` / `deepseek-reasoner` 将于 2026-07-24 15:59 UTC 废弃。

### 5. V4-Pro GA 与 2026-08 调价落地

[V4-Pro GA 与 API 调价](deepseek-api-price-adjustment-2026-08.md)（2026-08-13 公告，8 月 16-17 日生效）是 6 月定价预告的正式落地：V4-Pro 转正带来重大 Agent 升级（推理 effort 三档可调：low 简单任务 / high 日常 Agent 工作流 / max 复杂任务；原生 OpenAI Responses API 支持，为 Codex 优化一键配置；App/Web "Expert Mode" 可用），同时更新 API 定价——部分模型涨幅最高 1100%，低峰时段价格为高峰的 50%，鼓励开发者错峰调度批处理任务。调价标志 DeepSeek 从"以低价换规模"转向"合理定价换可持续"，与 GLM Coding Plan 涨价、Kimi 商业化并行，国产大模型"集体变贵"成为 2026 年下半年的行业趋势。

### 6. 国产算力优先策略

V4 优先适配华为昇腾等国产 AI 芯片，未向美国芯片供应商开放测试。但 R2 的延期也暴露了昇腾训练稳定性不足的问题——训练阶段仍部分依赖英伟达。

### 7. V4-Flash-Vision-Exp：渐进式多模态

[V4-Flash-Vision-Exp 上线](deepseek-v4-flash-vision-exp.md)（2026-08-21）以"实验版本外挂模态"的渐进方式补齐视觉能力：纯文本能力与 V4-Flash 正式版持平，视觉 Agent 基准大幅跃升、多模态 Agent 能力接近 Opus-4.8。一张图片最多占 384 tokens、计价与 V4-Flash 一致，把带图 Agent 请求的边际成本压到可预算水平；同日免费上线 Files API（`file_id` 跨请求复用），并同步支持 Chat Completions / Messages / Responses 三种 API 格式——OpenAI、Anthropic 与 Responses 生态的存量 Agent 工具近零改造即可获得视觉能力。官方未公布开源计划，实验性质提示生产系统需预留兜底。

## 三、关键数据点

| 指标 | 数值 | 来源 |
|------|------|------|
| V4-Pro 总参数 | 1.6T | 官方 API 文档 |
| V4-Flash 总参数 | 284B | 官方 API 文档 |
| 上下文窗口 | 1M tokens | 官方 API 文档 |
| V4 单 token FLOPs vs V3.2 | 27% | 官方邮件 |
| KV cache vs V3.2 | 10% | 官方邮件 |
| 训练数据量（Pro / Flash） | 33T / 32T tokens | 媒体报道 |
| 开源协议 | MIT | 官方 |
| SWE-bench Verified vs Opus 4.6 Max | 仅差 0.2pp | 官方自测 |
| 价格 vs Fable 5 输出 | ~1/57 | 官方定价 |
| DSpark 单用户生成提速（Flash / Pro） | 60-85% / 57-78% | V4 GA |
| DSpark 高并发吞吐提升（120 token/s） | 661% | V4 GA |
| V4 正式版 Agent 完成率提升 | +21% | V4 GA |
| V4-Flash-0731 Terminal Bench 2.1 | 82.7 | V4 GA |
| 旧模型名停用日期 | 2026-07-24 | V4 GA |
| V4-Flash-0731 NL2Repo / Cybergym / DeepSWE | 54.2 / 76.7 / 54.4 | V4-Flash 正式版 |
| V4-Flash-0731 Toolathlon verified / Agent Last Exam | 70.3 / 25.2 | 同上 |
| V4-Flash-0731 DSBench-FullStack / DSBench-Hard | 68.7 / 59.6 | 同上 |
| 2026-08 调价最高涨幅 | 1100% | V4-Pro GA 与调价 |
| 峰谷定价低峰价格 | 高峰的 50% | 同上 |
| 新价格生效时间 | 2026-08-16 16:00 UTC | 同上 |
| V4-Pro 推理 effort 档位 | low / high / max 三档 | 同上 |
| V4-Flash-Vision-Exp 单图 token 上限 | 384 tokens（计价与 V4-Flash 一致） | V4-Flash-Vision-Exp |
| V4-Flash-Vision-Exp 多模态 Agent 能力 | 接近 Opus-4.8 | 同上 |
| Files API | 免费（file_id 跨请求复用） | 同上 |

## 四、与 OpenAI / Anthropic / Kimi / GLM 的对比

| 维度 | DeepSeek | OpenAI | Anthropic | Kimi | GLM |
|------|----------|--------|-----------|------|-----|
| 公司地点 | 中国 | 美国 | 美国 | 中国 | 中国 |
| 模型策略 | 开源 + 效率优先 | 闭源旗舰 | 闭源 frontier | 开源最大规模 | 开源 + 商业化 |
| 最大模型 | V4-Pro 1.6T | GPT-5.6 Sol | Claude Fable 5 | K3 2.8T | GLM-4 |
| 核心差异化 | 性价比 + mHC 架构 | Agent 工业化 | 安全 + 可解释 | 开放 + 规模 | 中文本土化 |
| 上下文 | 1M tokens | 未公开 | 未公开 | 1M tokens | 未公开 |
| API 价格 | 全场最低 | 高端 | 高端 | 中低 | 中低 |
| 国产算力 | 昇腾优先 | 英伟达 | 英伟达 | 未明确 | 未明确 |

## 五、贯穿始终的原则

1. **效率即护城河**：27% FLOPs、10% KV cache——用架构创新降低推理成本
2. **开源是核武器**：MIT 协议 + 1.6T 开源模型，直接冲击闭源定价体系
3. **价格屠夫策略**：Opus 级能力 + 1/7 价格，重新定义开发者成本预期
4. **国产算力双轨**：优先适配昇腾，但训练阶段仍依赖英伟达——自主可控尚未完成
5. **迁移即决策点**：旧模型废弃 + 峰谷计费迫使开发者重新评估调度策略
6. **后训练是第二增长曲线**：V4-Flash-0731 架构不变仅靠重新后训练即超越 V4-Pro 预览版——Agent 能力提升不再依赖架构迭代
7. **"预览即生产"的发布哲学**：无版本号轰炸，后台小步改进 → 灰度 → 转正，用户无感完成模型升级

## 六、文章索引

| # | 日期 | 文章 | 主题 |
|---|------|------|------|
| 1 | 2026-04-24 | [DeepSeek-V4](deepseek-v4.md) | 双模型发布 / 架构创新 / 开源 |
| 2 | 2026-06-29 | [DeepSeek-V4 API 定价](deepseek-v4-api-pricing.md) | 峰谷计费 / 旧模型废弃 / 成本工程 |
| 3 | 2026-07-15 | [DeepSeek-V4 正式版 GA](deepseek-v4-ga.md) | 正式版转正 / DSpark 推测解码 / Agent 跃升 |
| 4 | 2026-07-31 | [DeepSeek-V4-Flash 正式版发布](deepseek-v4-flash-official-release.md) | V4-Flash 公测 / Agent 基准 / Responses API / Codex 适配 |
| 5 | 2026-08-13 | [V4-Pro GA 与 API 调价](deepseek-api-price-adjustment-2026-08.md) | V4-Pro 转正 / 调价 1100% / 峰谷计费 |
| 6 | 2026-08-21 | [V4-Flash-Vision-Exp 上线](deepseek-v4-flash-vision-exp.md) | 多模态 API / Files API / 三格式兼容 |

> **说明**：mHC、Engram、CSA/HCA、Muon 优化器部分均基于 arXiv 论文原文（2026-07-20 检索），包括 DeepSeek-V4 完整技术报告（arXiv:2606.19348，55+ 页）；定价信息直接来自官方 API 文档，可交叉验证。
