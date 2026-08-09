# Baseten 入驻 Hugging Face 推理供应商：零加价访问开源权重模型（Baseten on Hugging Face Inference Providers）

- **原文链接**: [Baseten on Hugging Face Inference Providers](https://huggingface.co/blog/baseten)
- **作者**: Alex Ker、Roland Crosby、Sid Shanker、Johan（Baseten 团队）
- **发布日期**: 2026-08-06
- **检索日期**: 2026-08-08
- **标签**: #推理服务 #Baseten #HuggingFace #开源模型 #Serverless

## 核心观点

Hugging Face 将 AI 基础设施平台 Baseten 新增为官方推理供应商（Inference Provider），开发者可在 Hub 模型页与官方 SDK 中以零加价（zero-markup）的 serverless 方式调用开源权重模型。首发支持 DeepSeek V4 Flash、GLM-5.2、Kimi K3 等热门 LLM，覆盖对话与文本生成任务。Hugging Face PRO 订阅用户每月可获得 $2 推理额度，可在所有集成供应商间通用。Baseten 以多云架构（18 个云、87 个集群）见长，日处理超 10 亿次推理调用。

## 关键发现 / 关键技术

### 1. 两种路由与计费模式
- **HF 路由**：使用标准 HF_TOKEN 请求统一端点 `https://router.huggingface.co/v1`，费用直接计入 HF 账户，按 Baseten 标准 API 费率零加价透传（HF 未来可能引入分成协议）
- **自定义 API Key**：开发者填入自有 Baseten API Key，请求直达 Baseten 基础设施，费用计入 Baseten 账户
- 用户可在账户设置中按偏好排序供应商，影响模型页 widget 与代码片段的默认展示

### 2. 首发模型与任务范围
- 支持 DeepSeek V4 Flash（`deepseek-ai/DeepSeek-V4-Flash-0731:baseten`）、GLM-5.2、Kimi K3
- 当前仅支持文本生成与对话类 LLM 任务；Baseten 原生还托管 TTS 等更广目录，HF 侧后续将扩展
- 统一路由兼容 OpenAI API 格式，模型标识以 `:baseten` 后缀指定供应商

### 3. SDK 与 Agent Harness 集成
- Python：`huggingface_hub` >= 1.26.1；JavaScript：`@huggingface/inference`
- 原生兼容主流 Agent harness：Pi、OpenCode、Hermes Agents、OpenClaw，无需额外集成代码即可把 Baseten 托管模型接入自主 Agent 工作流
- PRO 订阅含 $2 月度推理额度、ZeroGPU、Spaces Dev Mode 及 20 倍更高速率限制

## 实践意义

这降低了开源模型的生产试用门槛：开发者用一个 HF Token 即可在多家供应商间切换，无需为每个供应商单独注册与集成。Baseten 的多云架构也为避免单一云供应商锁定或 GPU 短缺提供了冗余。对国产开源模型（DeepSeek、GLM、Kimi）而言，进入 HF 推理供应商目录意味着更便捷的全球开发者触达。但当前任务范围仅限文本生成，多模态需求仍需直连 Baseten。

## 跨厂商对比

- 与 [transformers vLLM 原生速度后端](native-speed-vllm-transformers-backend.md) 互补：后者解决"通用模型实现达到手写原生速度"，Baseten 集成解决"模型一键部署到生产级 serverless 基础设施"，分别在编译栈与基础设施层降低开源模型的使用门槛
- 与 [DeepSeek-V4 正式版 GA](../../deepseek/news/deepseek-v4-ga.md) 互补：DeepSeek 自有 API 提供最低价直连，Baseten on HF 提供多云冗余与统一账单的替代路径，DeepSeek V4 Flash 是首发支持模型之一
- 与 [GLM-5.2](../../glm/blog/glm-5-2.md) 互补：GLM Coding Plan 面向订阅制 IDE 编码，Baseten on HF 面向 API 级别的模型调用与 Agent 集成，两者服务不同开发场景

## 资源
- 原文：[Baseten on Hugging Face Inference Providers](https://huggingface.co/blog/baseten)
- Baseten 主页：[baseten.com](https://baseten.com/)
- 支持模型列表：[huggingface.co/models?inference_provider=baseten](https://huggingface.co/models?inference_provider=baseten&sort=trending)
- 供应商集成文档：[Inference Providers integrations](https://huggingface.co/docs/inference-providers/en/integrations/index)
