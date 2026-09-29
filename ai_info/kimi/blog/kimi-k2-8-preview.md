# Kimi K2.8 Preview:接近 K3 的全量主力模型(Kimi K2.8 Preview)

- **原文链接**: [Kimi Code: What's New — Introducing K2.8 Preview](https://www.kimi.com/code/docs/kimi-code/whats-new.html)
- **作者**: Moonshot AI
- **发布日期**: 2026-09-11
- **检索日期**: 2026-09-29
- **标签**: #KimiK2.8 #主力模型 #CodingAgent #1M上下文 #无感替换

## 核心观点

K2.8 Preview 是 K3(07-16)之后 Kimi 家族的第一个新模型——不是 K3.5,K3 系列没有后续版本。定位是"接近 K3 的全量主力模型":Coding 与 Agent 能力较 K2.7 Code 全面提升,思考效率显著改善。

产品侧三个关键变化:提供 low/high/max 三档 effort(默认 max);原生支持图片/视频输入;1M 上下文对所有会员档位开放(K3 此前需高档位)。Model ID 保持 kimi-for-coding 不变,API 用户无感知替换;暂无公开 benchmark,权重未开源。

商业化同步提速:ARR 6 月约 3 亿美元、8 月突破 10 亿美元,传年底目标 20 亿;9 月初已递交港交所 A1(投前估值 500 亿美元,彭博转引)。

## 关键发现 / 关键技术

### 1. 模型定位:K3 之后的第一个新模型

- 发布于 2026-09-11,是 K3(07-16)后 Kimi 家族首个新模型
- 明确不是 K3.5:K3 系列无后续版本,K2.8 接棒主力位置
- Coding 与 Agent 较 K2.7 Code 全面提升,思考效率显著改善

### 2. 三档 effort,默认 max

- low / high / max 三档思考强度,默认 max
- 思考效率改善意味着同等质量下更少的思考 token 消耗

### 3. 原生多模态输入与 1M 上下文下放

- 原生支持图片/视频输入
- 1M 上下文对所有会员档位开放;K3 此前需高档位会员

### 4. 无感知替换:Model ID 不变

- Model ID 仍为 kimi-for-coding,API 与工具链无需改动即切换到 K2.8

### 5. 三层模型矩阵

| 层级 | 模型 | 角色 |
|------|------|------|
| 旗舰 | K3 | 最强能力,旗舰定位 |
| 主力 | K2.8 | 接近 K3 的低成本全量模型 |
| 高速 | K2.7 Code 高速版 | 5-6 倍输出速度 |

### 6. 商业化进展

- ARR:6 月约 3 亿美元 → 8 月突破 10 亿美元;传年底目标 20 亿美元
- 9 月初递交港交所 A1 上市申请(投前估值 500 亿美元,彭博转引)

### 7. 限制

- 无公开 benchmark,能力主张主要来自官方描述
- 权重未开源,与 K2.7 Code、K3 的开放策略形成对比

## 实践意义

- **主力模型分层供货**:旗舰(K3)保上限、主力(K2.8)保成本、高速版(K2.7 Code)保延迟,用户按场景选档而非"一模型打天下"
- **无感替换降低迁移成本**:Model ID 不变的替换策略值得 API 产品借鉴,能力升级不再要求用户改代码
- **1M 上下文平民化**:全档位开放长上下文,直接改变个人开发者与小团队的工作流设计

## 跨厂商对比

- 与 [Introducing Codex](../../openai/research/introducing-codex.md) 对比:Codex 以闭源模型 + 云端 Agent 占据高端 coding 心智,K2.8 用"接近旗舰的主力模型 + 低价"抢量
- 与 [GLM-5.2](../../glm/blog/glm-5-2.md) 对比:GLM-5.2 靠订阅制编程套餐打性价比,K2.8 靠模型分层与 1M 上下文下放
- 与 [Kimi K3 开放日](kimi-k3-open-day.md) 关联:K3 开放权重做生态,K2.8 闭源 API 做收入,开源与商业化双轨并行
- 与 [Kimi K2.7 Code](kimi-k2-7-code.md) 对比:K2.7 Code 是开源主线与高速版底座,K2.8 全面接管闭源主力

## 资源

- 发布说明:[Kimi Code: What's New](https://www.kimi.com/code/docs/kimi-code/whats-new.html)
- 产品:[Kimi Code](https://www.kimi.com/code)
- API:[Kimi OpenPlatform](https://platform.moonshot.cn/)
