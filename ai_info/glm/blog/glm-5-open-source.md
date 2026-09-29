# GLM-5 开源:Agentic Engineering 时代最好的开源模型(GLM-5 Open Source: The Best Open Model for the Agentic Engineering Era)

- **原文链接**: [GLM-5 Open Source: The Best Open Model for the Agentic Engineering Era](https://www.zhipuai.cn/zh/research/154)
- **作者**: 智谱 GLM 团队
- **发布日期**: 2026-02-11
- **检索日期**: 2026-09-29
- **标签**: #GLM-5 #智谱 #开源模型 #AgenticEngineering #Slime #国产算力 #MIT

## 核心观点

智谱以"Vibe Coding 已死,Agentic Engineering 当立"为叙事发布 GLM-5,称其为 Agentic Engineering 时代最好的开源模型:真实编程体感逼近 Claude Opus 4.5,AA 指数全球第四、开源第一。规模上从上一代 355B 跃升至 744B(23T → 28.5T tokens),并开源了'Slime'异步 RL 框架。

商业与生态侧,GLM-5 适配七大国产算力平台,配套发布 Z Code 工具并升级 Coding Plan,以 MIT 协议开源。一个耐人寻味的细节:发布前的 Pony Alpha 匿名盲测中,25% 用户把它误猜为 Claude Sonnet 5——体感对齐闭源旗舰成为开源模型的新竞争维度。

## 关键发现 / 关键技术

### 1. 叙事转向:Vibe Coding → Agentic Engineering

发布叙事本身就是产品判断:一次性代码生成的时代结束了。

- 从"氛围驱动的一次性生成"转向"工程化的持续交付"
- 评测重心从静态基准转向真实编程体感
- 模型设计目标从"写好一个函数"转向"交付一个系统"

### 2. 规模与能力跃升

- 参数规模:355B → 744B
- 预训练数据:23T → 28.5T tokens
- 真实编程体感逼近 Claude Opus 4.5
- AA 指数:全球第四、开源第一

### 3. 开源资产

权重与后训练框架同时开源,构成完整的复现路径。

- 'Slime'异步 RL 框架开源,后训练管线可复现
- MIT 协议开放模型权重,商用无附加条件
- 少数被完整开源的生产级 RL 基础设施之一

### 4. 生态与商业化

- Vending-Bench 2 余额 4432 美元,开源第一
- 七大国产算力平台适配
- Z Code 工具发布 + Coding Plan 升级
- 模型、工具、订阅三层打包,对标闭源厂商全家桶

### 5. 盲测体感

- 发布前 Pony Alpha 匿名盲测:25% 用户误猜为 Claude Sonnet 5
- 闭源旗舰的"体感"正在成为开源模型可对齐的目标
- 盲测而非跑分,是这一代开源竞争的新话术

### 6. 相对前代的跨越

- 参数翻倍以上(355B → 744B),数据 23T → 28.5T
- Vending-Bench 2 余额 4432 美元:长程商业决策类任务的直接证据
- 编程体感从"接近"到"逼近 Opus 4.5"的措辞升级

### 7. 开发者侧的获得物

- MIT 权重 + Slime 框架 + Z Code 工具 + Coding Plan
- 从复现训练到日常使用的完整工具链
- 七大国产算力适配进一步降低自部署门槛

## 实践意义

GLM-5 的发布标志着开源模型的竞争焦点从"跑分"转向"体感 + 工具链 + 算力生态"三位一体:MIT 协议 + Slime 框架让团队能复现其后训练;七大国产算力适配 + Z Code/Coding Plan 让部署与日常使用形成闭环。对国内企业,这意味着一条不依赖海外算力与闭源 API 的完整 Agentic 工程栈已经成型;对研究者,Slime 异步 RL 框架的价值不亚于权重本身。

## 跨厂商对比

- 与 [Kimi K3 开放前沿智能](../../kimi/blog/kimi-k3.md) 对比:同为"开源第一"竞争者,K3 以更大参数规模冲智能上限,GLM-5 以 Agentic Engineering 叙事 + 国产算力生态见长
- 与 [GLM-5 技术报告](glm-5-technical-report.md) 互补:本公告给出版本叙事与生态布局,技术报告补齐 744B/40B 激活、稀疏注意力、异步 RL 等细节
- 与 [GLM-5.3:前沿编程能力与涌现的网络安全能力](glm-5-3.md) 对照:5.0 确立"逼近 Opus 4.5 体感"的基线,5.3 进一步在编程与安全上加码
- 与 [Claude Opus 5](../../anthropic/research/claude-opus-5.md) 对比:GLM-5 明确以 Opus 4.5 为体感对标,Opus 系列持续定义闭源前沿,开源模型的追赶目标随其移动

## 资源

- 官方发布:https://www.zhipuai.cn/zh/research/154
- 技术报告:https://arxiv.org/abs/2602.15763
- 相关研究:https://www.zhipuai.cn/zh/research/153
- 智谱开放平台:https://www.bigmodel.cn/
