# Patch the Planet: A Daybreak Initiative to Support Open Source Maintainers

- **原文链接**: [Patch the Planet: a Daybreak initiative to support open source maintainers](https://openai.com/index/patch-the-planet/)
- **作者**: OpenAI
- **发布日期**: 2026-06-22
- **检索日期**: 2026-06-29
- **标签**: #Daybreak #OpenSource #CyberSecurity #VulnerabilityPatching #CodexSecurity

## 核心观点

OpenAI 联合 Trail of Bits、HackerOne、Calif 发起 **Patch the Planet** 计划——以专家安全研究员 + AI 模型（GPT-5.5-Cyber + Codex Security）为开源维护者提供**"从发现到修复"的完整防御循环**。首批覆盖 cURL、NATS Server、pyca/cryptography、Sigstore、aiohttp、Go、freenginx、Python、python.org 等关键开源项目。第一轮 5 天冲刺已经发现**数百个安全问题、合入数十个补丁**。

## 关键信息

### 1. 计划结构
- 与每个项目的维护者协商启动——了解优先级、偏好、披露流程
- 研究员负责：调查、验证、补丁开发、测试、协调披露
- 项目获得：**ChatGPT Pro + 条件性 Codex Security 访问 + API credits**

### 2. 早期成果（Trail of Bits 第一轮 5 天冲刺）
- 在 19 个开源项目上全职部署安全研究员
- 发现**数百个安全问题**
- 合入**数十个补丁**，更多协调披露中
- 构建可复用安全基础设施：
  - 模糊测试 harness
  - 历史 CVE 分析 pipeline
  - 差分测试系统
  - 威胁模型
  - 去重/误报过滤/严重度修正/补丁生成工作流

### 3. 关键技术成果

#### 模糊测试实验室
- 用 Codex `/goal` + GPT-5.5-Cyber **不到 1 天**建立完整模糊测试实验室
- 覆盖多个入口点、变体构建、平台、新型测试种子
- 手工建立同等实验室通常需要**数周**

#### 历史 CVE 变体分析 pipeline
- 摄取历史 CVE → 提取漏洞模式 → 跨代码库搜索相关缺陷 → 专项判别 Agent
- 去重、过滤误报、人工确认
- 将多年公开漏洞历史转为可复用搜索策略

#### 差分测试
- 用 Codex 生成/迭代连接不同实现的"glue 代码"
- 多个实现互相模糊测试，行为差异分析
- 数天完成手工需要**数周到数月**的工作

#### 基于规约的测试
- Codex 生成威胁模型、攻击分类、不变量测试、property-based 测试
- 暴露真实与预期行为差异

### 4. OpenAI 已发现的成果
- **Linux Kernel**：GPT-5.5-Cyber 在 3000 万行代码中识别安全相关组件，生成 **8 个内核指针信息泄露 PoC + 24 个本地提权 exploit**
- **OpenBSD**：发现 **23 年历史的 use-after-free**（System V 信号量）——本地权限提升到 root
- **FreeBSD**：发现 **34 个漏洞 + 7 个本地提权 PoC**
- **dnsmasq**：独立识别后来修复的 6 个 dnsmasq CVE 中的 4 个
- **HTTP/2 Bomb**：Calif + Codex 发现影响 NGINX、Apache、IIS、Pingora 的 DoS 技术；估计 **880,000+ 暴露网站**受影响
- **Chrome V8**：5 个可利用漏洞，其中 3 个在引入后数天内被修复
- **Safari WebKit**：一周内 **10+ 可利用漏洞**
- **Firefox**：发现 WebAssembly 漏洞 **CVE-2026-8390**——Mozilla 在 Pwn2Own Berlin 前 2 天修复；6 个 Firefox 参赛队伍中 5 个退出

### 5. 维护者保护机制
- **每个发现都经安全研究员人工复核**——才送到维护者
- 维护者控制补丁部署和披露

## 关键洞察

1. **AI 加速漏洞发现，但维护者成为瓶颈**——本计划把"研究员 + AI"放在维护者前面过滤
2. **可复用基础设施是关键**——不只是找漏洞，是建立长期安全工程能力
3. **小团队大责任**——94% 广泛使用的项目 < 10 名开发者贡献 90% 代码（HBS 研究）
4. **差分测试是 AI 加速最大的环节**——把"几周到几个月"压成"几天"
5. **重大开源项目已成为首批目标**——cURL、Go、Python、Sigstore
6. **专家人类复核不可省略**——前沿模型仍产生大量误报，需要人工过滤

## 关键数据点

| 指标 | 数值 |
|------|------|
| 首批开源项目数 | 9（cURL、NATS Server、pyca/cryptography、Sigstore、aiohttp、Go、freenginx、Python、python.org） |
| 参与的 Trail of Bits 工程师 | 19 个项目全职 |
| 5 天冲刺发现问题 | 数百 |
| 5 天冲刺合入补丁 | 数十 |
| Linux Kernel 代码量 | 3000 万行 |
| Linux Kernel 指针泄露 PoC | 8 |
| Linux Kernel 本地提权 exploit | 24 |
| FreeBSD 漏洞数 | 34 |
| FreeBSD 本地提权 PoC | 7 |
| Chrome V8 可利用漏洞 | 5 |
| Safari 可利用漏洞 | 10+ |
| HTTP/2 Bomb 影响网站 | 880,000+ |
| 维护者 < 10 人的开源项目比例 | 94% |
| 模糊测试实验室搭建（AI） | < 1 天 |
| 模糊测试实验室搭建（手工） | 数周 |

## 相关文章

- [Daybreak: Tools for Securing Every Organization](daybreak-securing-the-world.md)
- [Building Codex Windows Sandbox](building-codex-windows-sandbox.md)
- [Running Codex Safely at OpenAI](running-codex-safely.md)