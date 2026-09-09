# Cursor 被 SpaceX 收购后我们的决定（Our decision on Cursor following its acquisition by SpaceX）

- **原文链接**: [Our decision on Cursor following its acquisition by SpaceX](https://openai.com/index/our-decision-on-cursor-following-its-acquisition-by-spacex/)
- **作者**: OpenAI
- **发布日期**: 2026-08-28
- **检索日期**: 2026-09-09
- **标签**: #OpenAI #商业决策 #模型供应 #API

## 核心观点

OpenAI 通知 SpaceX：将终止向 Cursor 供应 OpenAI 模型的合同，提议的关停日期为 2026 年 11 月 12 日，并已按合同给出最长通知期，以最大化开发者在 Cursor 内继续使用 OpenAI 模型的时间。

决策理由是对 SpaceX 能否遵守服务条款"没有信心"：文章援引马斯克公司的既往记录——Twitter 被收购（现属 SpaceX）后违反了与 OpenAI 的合同条款；马斯克今年早些时候宣誓作证时承认 xAI（现亦属 SpaceX）曾违反 OpenAI 的服务条款。与 Cursor 的定制协议在控制权变更后赋予 OpenAI 有限的解约窗口，加之对即将发布的新模型 Astra 的合规问责要求，OpenAI 选择在不再向 Cursor 提供未来模型的前提下，把解约时间推迟到最晚可行日期。

## 关键发现 / 关键技术

### 1. 决策机制：控制权变更条款
- 与大型合作伙伴通常依赖定制合同，确保服务条款遵从与规模化安全集成
- 与 Cursor 的定制协议在控制权变更（change of control）后提供有限解约窗口——本次收购触发该条款
- OpenAI 表示与 Cursor 合作近四年，尊重其团队、产品及其为开发者社区构建的一切，并承诺为受影响开发者提供超出常规的过渡支持

### 2. 事实依据：违反条款的既往记录
- Twitter（现属 SpaceX）被收购后违反了与 OpenAI 的合同条款（文中附报道链接）
- 马斯克在宣誓作证中承认 xAI 违反过 OpenAI 服务条款（条款与 xAI 自身的类似）

### 3. 前瞻考量：Astra 时代的问责
- 随着 AI 能力演进，OpenAI 认为对即将发布的模型 Astra 的使用合规负有"新层面的责任"
- 这是"不再向 Cursor 提供未来模型"决策的直接考量之一：既守住合规底线，又为现有开发者保留最长过渡期

## 实践意义

对企业平台与 API 团队而言，本案例是"控制权变更条款 + 供应方合规裁量权"的现实教材：模型供应协议中的变更控制与终止窗口在并购场景下真实生效，大型采购方与供应方都应把所有权变动风险写入合同管理清单。对依赖第三方 AI 编码工具的开发者而言，它提示了供应链风险——底层模型授权可因供应商所有权变化而中断，选型时应评估工具方的模型来源多样性与退出预案。

## 跨厂商对比

- 与 [GPT‑5.6 发布](introducing-gpt-5-6.md) 关联：模型供应决策直接影响下游工具生态——GPT‑5.6 及后续（文中提及的 Astra）不再进入 Cursor，说明模型迭代与渠道策略深度绑定。
- 与 [Apple 此举有失偏颇](apple-is-getting-this-wrong.md) 对比：两者都涉及平台生态准入之争，OpenAI 以合同条款与合规记录为由收缩供应，Apple 被指以平台限制竞品，可对照观察"生态守门人"行为的边界与正当性论证。

## 资源

- 官方文章：https://openai.com/index/our-decision-on-cursor-following-its-acquisition-by-spacex/
- 相关：N/A
