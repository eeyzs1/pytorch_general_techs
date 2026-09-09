# DeepSeek V4-Flash-Vision-Exp 上线：开启多模态 API 服务

- **原文链接**: [V4-Flash-Vision-Exp 上线，开启多模态 API 服务](https://api-docs.deepseek.com/zh-cn/news/news260821)
- **作者**: DeepSeek 官方
- **发布日期**: 2026-08-21
- **检索日期**: 2026-09-09
- **标签**: #DeepSeek #多模态 #视觉理解 #Agent #FilesAPI #V4-Flash-Vision-Exp

## 核心观点

DeepSeek 在 API 平台上线实验性多模态视觉理解模型 DeepSeek-V4-Flash-Vision-Exp，通过 `model='deepseek-v4-flash-vision-exp'` 访问。官方定位是"平衡文本与多模态能力"：纯文本能力（Agent、推理、世界知识等）与 V4-Flash 正式版持平，而需要视觉理解的 Agent Benchmark 相比 V4-Flash 大幅跃升，多模态 Agent 能力已接近 Opus-4.8。

商业化延续低价策略：图片转换为 token 后按 token 计费，一张图片最多占 384 tokens，计费价格与 V4-Flash 一致；同日免费开放 Files API，支持先上传、再以 `file_id` 引用，同一张图片跨请求无需重复上传。多模态 API 同时支持 Chat Completions、Messages、Responses 三种格式，方便接入各类 Agent 工具。

## 关键发现 / 关键技术

### 1. 文本能力不回退，视觉 Agent 大幅跃升
- 纯文本能力（Agent、推理、世界知识等）与 DeepSeek-V4-Flash 正式版持平
- 视觉理解类 Agent Benchmark 相比 V4-Flash 大幅跃升，多模态 Agent 能力接近 Opus-4.8
- 评测口径：Code Agent 文本任务采用 DeepSeek Harness 极简模式（max 档位，temperature=1.0，topp=0.95）；ApexBench 与 Agents' Last Exam 中，文本模型 DeepSeek-V4-Flash 会忽略题内多模态元素（具体分数见官方基准图表，正文未列数字）
- 模型标注实验性质（Exp），官方未公布开源计划与下线时间表

### 2. 多模态解锁更多 Agent 场景
- 示例 1：Agent 框架下生成高端定制西藏自驾游 PPT——藏南 + 藏北一月行程、野性粗粝视觉调性、真实摄影质感配图、三档真实定价方案
- 示例 2：对 DeepSeek Harness 官网二次创作——以黑蓝深海、玻璃 UI、ASCII 原子像素等要素，经长多轮交互重构为未来主义风格开发者网站
- 示例 3：制作黏土怪物风格动态特效的前端 Mini Demo（3D 黏土小怪物 + 复古舞池派对）

### 3. API 接入与免费 Files API
- 三种调用格式：Chat Completions、Messages（Anthropic 风格）、Responses（OpenAI 新式），存量 Agent 工具可近零改造迁移
- 支持图文混合输入；图片可经 base64 内联、外部 URL、Files API 三种方式传入
- Files API 免费开放：图片先上传平台、请求中以 `file_id` 引用，节省请求带宽，跨请求复用无需重复上传

## 实践意义

对 Agent 开发者而言，"三种 API 格式 × 三种图片传入方式"意味着 OpenAI、Anthropic 与 Responses 生态的存量工具几乎零改造即可获得视觉能力，带图 Agent 工作流的迁移成本被压到最低。图片 384 tokens 封顶让多模态任务的成本可预算、可横向比较——在 V4-Flash 定价下，带图 Agent 请求的边际成本显著低于按分辨率计费的方案。实验性质则提示生产系统需为模型名与能力变化预留兜底。

## 跨厂商对比

- 与 [DeepSeek-V4-Flash 正式版发布](deepseek-v4-flash-official-release.md) 对比：Vision-Exp 纯文本能力持平 Flash 正式版，增量全部来自视觉理解，DeepSeek 选择以"实验版本外挂模态"渐进交付而非直接替换主模型
- 与 [DeepSeek-V4 正式版上线](deepseek-v4-ga.md) 互补：V4 GA 代表能力上限，V4-Flash-Vision-Exp 以 Flash 同价补齐视觉模态，构成"旗舰 + 轻量多模态"的产品矩阵

## 资源

- 官方公告：https://api-docs.deepseek.com/zh-cn/news/news260821
- 媒体报道：N/A（以官方 API 文档为唯一信源）
- API 指南：图像理解 https://api-docs.deepseek.com/zh-cn/guides/vision ｜ Files API https://api-docs.deepseek.com/zh-cn/guides/files_api
