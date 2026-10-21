# Opus 5.5 上一个任务多少钱（What a task costs on Opus 5.5）

- **原文链接**: [What a task costs on Opus 5.5](https://claude.dev/blog/what-a-task-costs-on-opus-5-5/)
- **作者**: Addy Osmani
- **发布日期**: 2026-09-25
- **检索日期**: 2026-10-16
- **标签**: #成本工程 #effort档位 #缓存经济学 #token预算 #Opus55

> 补录说明：本文发布于 2026-09-25（锚点 2026-09-28 之前），上次同步遗漏，本次补录入库。

## 核心观点

把"任务成本"拆到可操作的粒度：任务是一个循环（读对话→调工具→读结果），四因子决定账单——轮次（每轮重发全部历史）、缓存命中率、输出 token 类型（含 thinking，价格是输入 5 倍/缓存读 100 倍）、模型档。同样的 2.8M 输入 token，缓存命中 90% 花 $1.62、0% 花 $11.20——没有任何设置比缓存更影响输入成本。

Opus 5.5 的降价结构：输入/输出 -20%、缓存读 -60%（$0.50→$0.20）；同 token 会话省约 31%，官方"省 40%"口径额外假设了中档 effort 下更少的 token 用量。企业基准：平均每开发者每活跃日约 $13，90% 用户低于 $30。

## 关键发现 / 关键技术

### 1. 成本四因子与量级
- 40 轮 vs 25 轮完成同一任务：2.8M vs 1.75M 输入，$1.62 vs $1.02——"最便宜的轮次是不需要的那轮"
- 给模型可自验的方式（测试/构建/脚本）让错误更早暴露，是砍轮次的第一杠杆
- 输出含 thinking：60K 输出 = $1.20 = 读 6M 缓存 token——effort 档位因此主导账单

### 2. effort 阶梯的使用法
- Opus 5.5 默认 medium（比 Opus 5 的 high 低一档）；同档位下 5.5 思考更多，勿沿用旧档
- 判据：medium 修到一层就停（改了 handler 没改 client）→ 要么升 high 要么先补检查手段；一次 10 轮 retry 循环 ≈ high 档全任务多花的 $0.40——省一次重试就回本
- API key/订阅上切 effort 保缓存；Bedrock/Vertex/网关上切换会清缓存（整段重写）

### 3. 模型分配策略
- 三模型日常：Haiku/Sonnet 做查询与 subagent（model: haiku 写进 subagent 定义或 CLAUDE_CODE_SUBAGENT_MODEL 环境变量）、Opus 5.5 做日常主驾、Fable 5.1 只攻最难（xhigh 两次撞墙即切换，$10/$50 但缓存读仅 $0.25）
- agent teams 约 7× 普通 session token——团队要小、任务自包含、做完即关
- 迁移时跑 /claude-api prompt-audit：44 工单客服基准上，迁移本身省 18%、审计再省 9%（合计较 Opus 4.8 起点 -25%）

### 4. 缓存与压缩的微观经济
- 订阅 1 小时缓存 / API key 5 分钟；120K 上下文一次 5 分钟写 = $0.60 ≈ 25 次读——咖啡休息 6 分钟就把 $0.02 的读变成 $0.60 的写
- /compact 在 150K 处约 $0.25，10 轮内回本；休息前压不是休息后；/clear 免费，换任务就用
- CLAUDE.md 每行都是每轮重发的载荷（建议 <200 行）；MCP 工具定义已延迟加载
- fast mode：2.5× 速度、2× 价格，开在会话开头而不是中途（首请求整段按 fast 价且不缓存）

## 实践意义

这是目前最完整的 agent 会话计价教材，交互式图表明示"列表价 × 你的形状"才等于真账单。三个立刻可用的动作：把 subagent 默认模型钉到 Haiku/Sonnet；用 /usage 的三个读数（缓存份额、输出/输入比、总输入/对话大小）做日常体检；在团队里推广"同任务两模型各跑一遍再下结论"的测量文化，而不是信任何单点报价。

## 跨厂商对比

- 与 [Getting the most out of Opus 5.5](getting-the-most-out-of-opus-5-5.md) 姊妹篇：用法指南与成本指南同发，共同定义 5.5 代的"性价比操作手册"
- 与 [A Guide to Cost Visibility and Control in Claude](cost-visibility-and-control-in-claude.md) 互补：企业治理篇看"每成果成本"与组织管控，本文看单 session 的物理计价——管理层与工程师两个视角
- 与 [Reducing Cost and Improving Performance with Claude Platform](reducing-cost-and-improving-performance-with-claude-platform.md) 衔接：prompt-audit 的基准数据在两文间共享，形成"审计→测量→调档"的完整链路

## 资源

- 论文：无
- 代码：无
- Demo：无
- 文档：https://code.claude.com/docs/en/costs
