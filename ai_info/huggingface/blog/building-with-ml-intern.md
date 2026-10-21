# 模型不存在，所以你自己造一个（The model that didn't exist, so you made it yourself）

- **原文链接**: [The model that didn't exist, so you made it yourself](https://huggingface.co/blog/building-with-ml-intern)
- **作者**: yuvraj sharma、Abubakar Abid（Hugging Face / Gradio 团队）
- **发布日期**: 2026-10-08
- **检索日期**: 2026-10-16
- **标签**: #MLIntern #Agent训练 #模型蒸馏 #低成本训练 #提示工程

## 核心观点

HuggingChat 的 ML Intern 模式是一个"造模型的 Agent"：给它一段需求描述，它规划任务、先申请预算再花钱、跑冒烟测试、训练、评估、最后把模型发布到 Hub。作者用它几天内造出 7 个模型，全部计算成本合计约 103 美元——最小的一个只花 1.90 美元。样板案例：官方 Qwen-Image 2.1 提示改写器是 20GB 内存的 9B 模型，Hub 上只有压缩版；描述需求一天后得到 0.8B 的 CPU 可跑版本，99.7% 输出合法，token 用量约为教师的四分之一。

方法论核心在提示词：写清"已验证事实，不要重新推导"省下预算；要求"训练前先报基线零样本分"否则无法衡量增益；要求"50 步冒烟测试 + 权重确实变化的检查"再上全量；明确"总花费上限 12 美元、超限先问"。ML Intern 从零预算开始、花钱必须请示，成本约束因此是硬约束。

## 关键发现 / 关键技术

### 1. 七个模型的花费账单

| 模型 | 底座 | 成本 |
|---|---|---|
| 柑橘病害 VLM（准确率 14.9%→52.8%） | Qwen3.5-2B | $1.90 |
| Huggy 风格 LoRA（step 200 最稳） | FLUX.2 klein 4B | $7.60 |
| Pocket 改写器 0.8B/2B | Qwen3.5 | $16 |
| 相机环绕视角 LoRA（24,722 张透明渲染） | Qwen-Image 2.1 | $16 |
| 涂鸦替换 LoRA（67.5% 检出、4.7 秒/图） | Qwen-Image 2.1 | $24 |
| Agate 4 步浏览器出图（GenEval 0.509→0.536） | Agate 260M | $37 |

### 2. 数据合成内嵌于流程

- 相机 LoRA：1,030 个扫描物体 × 24 角度 = 24,722 张透明图，CPU 任务只花几美分。
- 涂鸦 LoRA：用 LaMa 修复抹掉物体、原位画洋红涂鸦、原图作目标，自动构建 6,042 对训练数据并记录每张来源作者与许可。
- Pocket 改写器：小模型生成 8,797 条请求、9B 教师改写（A100 上 2 小时 37 分、$6.50），过滤后留 1,840 条。

### 3. 失败也被消化

- 视角项目共 48 个任务（含因缺包、路径错误失败后被 ML Intern 自动重提的）；涂鸦项目 59 个任务——失败重试是常态而非异常，预算内完成。

## 实践意义

"模型商品"的边际成本被压到两位数美元：领域小模型、风格 LoRA、蒸馏加速版都可以用一段认真的提示词订购。对平台方，这预示模型长尾将爆炸式增长；对从业者，提示词工程正在从对话技巧变成"委托工程"——写清验收标准（基线、冒烟测试、预算帽）比写代码更值钱。

## 跨厂商对比

- 与 [100 步 GRPO 结构化输出](grpo-with-trl-ifstruct.md) 对比：同样证明小预算能出可用模型（500 样本/免费 GPU vs 全流程 $103/7 模型），但 GRPO 篇是人在写训练脚本，本篇把整个流程委托给 Agent——训练工程本身正在被 Agent 化。
- 与 [训练模型画水彩](train-to-paint-with-code.md) 对比：同为 HF 团队的"小成本创意训练"叙事，水彩篇教方法学（奖励设计），本篇教委托协议（提示词结构），两者互为表里。
- 与 [Agentic GPU 集群调度](impactful-scheduling.md) 互补：Ai2 讲几千张 GPU 怎么分，本篇讲 16 美元怎么花——算力经济的两端都成了工程问题。

## 资源

- 论文：无
- 代码：[yvrjsharma/ml-intern-prompts（七个提示词全文）](https://github.com/yvrjsharma/ml-intern-prompts)
- Demo：[HuggingChat ML-intern 模式](https://huggingface.co/chat/?mode=ml-intern)
