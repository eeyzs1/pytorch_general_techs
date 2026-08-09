# GLM Coding Plan 套餐改版：从 prompt 计数转向 token 积分制（GLM Coding Plan Pricing Revision）

- **原文链接**: [老用户权益说明 — GLM Coding Plan 套餐改版](https://docs.bigmodel.cn/cn/coding-plan/notice/usage-revision)
- **作者**: 智谱 AI（Zhipu AI）
- **发布日期**: 2026-07-30
- **检索日期**: 2026-08-08
- **标签**: #GLM #CodingPlan #计费改版 #积分制 #峰谷定价

## 核心观点

智谱于 2026 年 7 月 30 日对 GLM Coding Plan 套餐进行改版，核心变化是从 prompt 计数转向以 token 消耗为基础的积分制，以提升额度计算的透明度与可预期性。老用户（V1/V2 个人套餐及团队套餐）权益完全不受影响，可按原价格续订升档；周末全天按非高峰时段抵扣。新用户与到期用户需订阅新版积分套餐，价格显著上调。高阶模型 GLM-5.2/GLM-5-Turbo 在高峰时段消耗 3 倍积分，GLM-4.7 全天按 1 倍消耗。团队套餐各席位额度同步上调 30%。

## 关键发现 / 关键技术

### 1. 计费模型转换：prompt 计数 → token 积分
- 旧版（V2 个人套餐）：按 prompt 次数限额，每 5 小时与每周刷新；每次 prompt 预计调用模型 15-30 次
- 新版：以 token 消耗为基础的积分制，额度计算更透明可预期
- 历史套餐与新版套餐仅额度计算方式不同，支持的模型等其他权益保持一致

### 2. 峰谷定价机制
- GLM-5.2/GLM-5-Turbo 作为高阶模型：高峰期 3 倍系数、非高峰期 1 倍系数消耗额度
- 高峰期定义：每周一至周五 14:00-18:00（UTC+8）
- GLM-4.7：全天按 1 倍系数消耗
- 周末全天按非高峰时段抵扣额度

### 3. 老用户权益保障与新用户定价
- V1 老用户到期前可按 V2 版价格订阅（Lite 49/Pro 149/Max 469 元包月），8 月中旬上线订阅入口
- V2 个人套餐与团队套餐用户：价格、权益、额度及计算方式均不受影响，可按原套餐续订升档
- 团队套餐席位额度上调 30%：标准版每 5 小时 0.78 亿 tokens、每周 3.9 亿 tokens；高级版 2.08 亿/10.4 亿 tokens
- 当前无生效套餐或首次订阅用户：直接订阅新版线上积分套餐

## 实践意义

这是国产编码订阅服务从"次数计费"向"token 计费"对齐行业惯例的信号——token 积分制更贴合实际资源消耗，也便于与按量 API 对比成本。3 倍高峰系数与周末非高峰的设定，引导用户错峰使用以平衡算力负载。对已订阅的老用户，权益不变是稳定信号；对新用户，价格上调意味着 GLM Coding Plan 的"低价红利期"结束，需重新评估订阅 vs 按量 API 的成本平衡。峰谷定价与 DeepSeek 的做法趋同，说明国内厂商在算力调度策略上正在收敛。

## 跨厂商对比

- 与 [GLM-5.2](glm-5-2.md) 衔接：GLM-5.2 上线时即配套 Coding Plan（个人版/团队版）订阅制，本文是该订阅体系的首次重大计费改版，两者共同构成 GLM 编码产品的模型 + 商业化闭环
- 与 [DeepSeek-V4 API 定价与峰谷计费](../../deepseek/news/deepseek-v4-api-pricing.md) 对比：DeepSeek 在按量 API 上引入峰谷定价（高峰翻倍），GLM 在订阅制上引入高峰 3 倍系数，两者均用价格杠杆引导错峰，但 DeepSeek 是 API 单价倍率、GLM 是积分消耗倍率

## 资源
- 公告原文：[老用户权益说明](https://docs.bigmodel.cn/cn/coding-plan/notice/usage-revision)
- 套餐订阅页：[bigmodel.cn/glm-coding](https://www.bigmodel.cn/glm-coding)
- 用量说明（个人版）：[docs.bigmodel.cn/cn/coding-plan/overview](https://docs.bigmodel.cn/cn/coding-plan/overview)
- 用量说明（团队版）：[docs.bigmodel.cn/cn/coding-plan/team](https://docs.bigmodel.cn/cn/coding-plan/team)
