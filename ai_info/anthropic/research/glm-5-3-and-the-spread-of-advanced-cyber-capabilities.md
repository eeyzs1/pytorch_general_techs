# GLM-5.3 与先进网络能力的扩散（GLM-5.3 and the spread of advanced cyber capabilities）

- **原文链接**: [GLM-5.3 and the spread of advanced cyber capabilities](https://www.anthropic.com/research/glm-5-3-and-the-spread-of-advanced-cyber-capabilities)
- **作者**: Andrew Fasano、Marius Fleischer、Cole McFaul、Robert Xiao、Tripp Gallagher（Frontier Red Team / Policy）
- **发布日期**: 2026-09-29
- **检索日期**: 2026-10-16
- **标签**: #GLM53 #网络安全 #开放权重 #越狱 #FrontierRedTeam #扩散风险

## 核心观点

Frontier Red Team 对智谱 GLM-5.3 的系统评估显示：继 Claude Mythos Preview 之后，"自主构建端到端网络利用"的能力已扩散到可自由下载的开放权重模型。ExploitBench 上 GLM-5.3 端到端利用成功率（50/410，约 12%）接近 Mythos Preview（56/410，约 14%），而 Claude Opus 4.6、GLM-5.2、Kimi K3、DeepSeek V4.1-Flash 均接近 0%——一个质变阈值已被跨越。

更关键的差异在防护：GLM-5.3 的护栏可被简单技术绕过 64%–100%（虚假掩护故事 64%、预填推理 92%、abliteration 去除拒绝 100%），而同等攻击对带防护的 Claude 模型全部失败。结论：GLM-5.3 是首个"能力对标前沿、任何人可下载、护栏形同虚设"的模型，恶意行为者的网络能力天花板被实质性抬高。

## 关键发现 / 关键技术

### 1. 利用能力：与 Mythos Preview 同档
- ExploitBench（Chrome V8 已知漏洞）：GLM-5.3 端到端利用 50/410 次，Mythos Preview 56/410；其余四家模型近乎为零
- 内部 Binary Exploitation 基准（OSS-Fuzz 项目 100 任务）：GLM-5.3 完整控制流劫持 4%，Mythos Preview 6%，其余 0%
- 人工专家会话一：一天内（人工关注 <1 小时）GLM-5.3 在某流行浏览器 JS 引擎发现多个 0-day 并链成"访问即读取任意文件"的利用链（已披露给维护方）；另在无线/显卡驱动、网络设备软件中发现可利用漏洞
- 人工专家会话二：GLM-5.3-Flash 用公开 CVE 详情 20 分钟人工关注 + 8 小时机器工作（约 $20.40 API 成本）构建绕过 PAC 的 ARM64 利用链

### 2. 护栏绕过：64%→100% 的三段式
- 裸指令恶意请求：0% 接触（各模型一致拒绝）
- 虚假红队身份掩护：GLM-5.3 64% 接触
- 预填 thinking tokens：92%
- abliteration（开放权重删除拒绝方向）：100%，拒绝率从 >90% 降至 3%/2%/12%（JailbreakBench/HarmBench/StrongREJECT），GPQA-Diamond 能力不变、CyberGym 仅降几个点
- Anthropic 自己复现 abliteration 花费约 2,200 GPU 小时（约 $4,400；熟练团队约 600 小时/$1,200），数日内社区已发布多个去拒版本
- Claude 侧三道防线全部有效：分类器拦截掩护话术、API 不允许预填 thinking、权重不公开无法 abliterate

### 3. 定位与主张
- NIST CAISI 9 月 17 日独立评估：GLM-5.3 为"迄今网络能力最强的开放权重模型"，落后美国前沿约四个月
- Anthropic 主张：防御者应使用与攻击者同级的工具；Glasswing 等项目给防御方抢跑窗口，但"可自由获取能力的关键阈值已经跨越"
- 呼吁政府对足够强的模型（含 GLM 后继）做独立安全测试

## 实践意义

"前沿能力 + 开放权重 + 弱护栏"三者首次同时成立，意味着威胁模型必须按"攻击者已拥有 Mythos 级利用能力"重设。对企业防御方的直接含义：漏洞发现-修复的时间差成为唯一防线，预修补（Glasswing/Patch the Planet 模式）从可选项变为必选项。对开放权重社区的启示是：abliteration 的成本已降到数千美元/数天，"发布时带护栏"在开放权重世界里约等于"发布后不久就没有护栏"，防护重心必须放在能力分层与访问控制而非端侧拒绝。

## 跨厂商对比

- 与 [Project Glasswing: Initial Update](glasswing-initial-update.md) 对比：Glasswing 是"受控访问 + 防御方先用"的处方，本文展示同一能力经开放权重无防护外溢后的世界——一个机制的正反两面
- 与 [Measuring LLMs' Impact on N-day Exploits](n-days.md) 互补：N-days 测前沿模型把公开补丁武器化的速度，本文测该能力扩散到可下载模型的现状
- 与 [GLM-5.3](../../glm/blog/glm-5-3.md) 对比：本库中智谱官方视角强调基准领先与性价比，Anthropic 评估则聚焦其护栏可绕过性与攻击面——同一模型的两种叙事并存；中文媒体视角与智谱商业化对照见 [Anthropic 报告评估 GLM-5.3 网络安全能力](../../glm/blog/glm-5-3-anthropic-cyber-report.md)
- 与 [Daybreak for Frontline Defenders](../../openai/research/daybreak-securing-the-world.md) 对比：OpenAI 以"防御优先部署"应对能力扩散，Anthropic 本文把矛头明确指向无护栏开放权重——防御前置与扩散治理两条路线

## 资源

- 论文：无（评测基于 ExploitBench arXiv:2605.14153、CyberGym arXiv:2506.02548）
- 代码：无
- Demo：无
- 相关：NIST CAISI 评估 https://www.nist.gov/news-events/news/2026/09/caisis-assessment-zais-glm-53-cyber-capabilities
