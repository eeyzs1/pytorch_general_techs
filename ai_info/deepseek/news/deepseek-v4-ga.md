# DeepSeek-V4 正式版 GA：从"悄悄灰度"到 Agent 能力跃升（DeepSeek-V4 GA & V4-Flash-0731）

- **原文链接**: [DeepSeek-V4 正式版上线公告（API News）](https://api-docs.deepseek.com/news/news260715)
- **作者**: DeepSeek（深度求索）
- **发布日期**: 2026-07-15
- **检索日期**: 2026-07-31
- **标签**: #DeepSeek #V4正式版 #DSpark #Agent #推测解码 #峰谷定价

## 核心观点

DeepSeek-V4 正式版（GA）走了一条与其他厂商完全不同的发布路径：4 月 24 日上线的是"预览版"但从未标注，官方在后台持续改进、灰度放量、收集反馈，7 月中旬宣布全量转正。正式版补齐了预览版缺失的能力：DSpark 推测解码标配使单用户生成提速 57-85%、高并发吞吐提升 661%，Agent 完成率提升 21%，原生多模态与企业级工具链落地，并首次完整开源（权重+训练脚本+推理代码）。7 月 24 日旧模型名 deepseek-chat/deepseek-reasoner 正式停用；7 月 31 日 V4-Flash 正式版（v4-flash-0731）发布，仅靠重新后训练就在 Agent 基准上全面超越 V4-Pro 预览版，并原生支持 Responses API、适配 Codex 生态。

## 关键发现 / 关键技术

### 1. "预览即生产"的发布策略
- 用户两个月来以为在用正式版，实际一直是预览版
- DeepSeek 式迭代：后台小步改进→灰度→调优→宣布转正，无版本号轰炸

### 2. DSpark 推测解码标配
- 半自回归 drafter + 置信度头 + 硬件感知调度，输出与目标模型逐字节一致
- Flash 提速 60-85%，Pro 提速 57-78%，120 token/s 高并发场景吞吐提升 661%
- 平均有效生成长度较 EAGLE3 提升 30.9%，北大联合开源、MIT 协议

### 3. V4-Flash-0731：后训练驱动的 Agent 跃升
- 架构不变（284B 总参/13B 激活），仅重新后训练
- Terminal Bench 2.1 得分 82.7，DSBench-FullStack 68.7，DSBench-Hard 59.6——全面超越 V4-Pro 预览版
- 原生支持 Responses API，可在 Codex CLI、ChatGPT 桌面端、VS Code 插件中直接调用
- Flash API 价格保持极低（缓存命中输入 0.02 元/百万 token、输出 2 元/百万 token），峰谷定价同步引入（高峰翻倍）；V4-Pro 正式版 API 与 App/Web 端仍待更新

## 实践意义

两个信号值得工程师关注：一是**推测解码工业化**——DSpark 把 60%+ 的单用户提速变成默认配置而非高级选项，推理成本曲线的"免费午餐"正式上桌；二是**后训练权重超过架构迭代**——同架构仅靠后训练就实现 Agent 能力代际差，说明当前阶段数据与训练流程的杠杆大于改架构。对用 Codex/Claude Code 等工具链的开发者，V4-Flash 成为可直接替换后端的低价选项。

## 跨厂商对比

- 与 [DeepSeek-V4 预览版](deepseek-v4.md) 衔接：同架构从预览到 GA 的完整演进记录
- 与 [V4 API 定价与峰谷计费](deepseek-v4-api-pricing.md) 衔接：峰谷定价从预告变为现实
- 与 [Kimi K3](../../kimi/blog/kimi-k3.md) 对比：K3 走 2.8T 参数规模扩张，DeepSeek 走效率+后训练路线——国产开源双雄的两种 scaling 哲学
- 与 [GPT-5.6](../../openai/research/introducing-gpt-5-6.md) 对比：OpenAI 用 max/ultra 档位卖智能溢价，DeepSeek 用极低定价+Responses API 兼容抢工具链份额

## 资源

- API 文档与定价：[api-docs.deepseek.com](https://api-docs.deepseek.com/quick_start/pricing)
- DSpark：[github.com/deepseek-ai/DeepSpec](https://github.com/deepseek-ai/DeepSpec)
- 模型仓库：[Hugging Face deepseek-ai](https://huggingface.co/deepseek-ai) / [ModelScope](https://modelscope.cn/models/deepseek-ai/DeepSeek-V4-Flash-DSpark)
- 技术报告：[arXiv:2606.19348](https://arxiv.org/abs/2606.19348)
