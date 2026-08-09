# OpenAI 对 TanStack npm 供应链攻击事件的回应（Our response to the TanStack npm supply chain attack）

- **原文链接**: [Our response to the TanStack npm supply chain attack](https://openai.com/index/our-response-to-the-tanstack-npm-supply-chain-attack/)
- **作者**: OpenAI
- **发布日期**: 2026-05-13
- **检索日期**: 2026-08-01
- **标签**: #供应链安全 #npm #TanStack #MiniShaiHulud #代码签名 #事件响应

## 核心观点

2026 年 5 月 11 日（UTC），广泛使用的开源库 TanStack 遭入侵，属于"Mini Shai-Hulud"大规模软件供应链攻击的一部分。OpenAI 内部有两台员工设备受影响，攻击者在部分内部源代码仓库中进行了未授权访问和凭证窃取。OpenAI 确认仅极少量凭证被导出，无证据表明用户数据、生产系统或知识产权被入侵，但受影响仓库包含 iOS/macOS/Windows 平台的代码签名证书，因此预防性轮换证书，要求 macOS 用户在 2026 年 6 月 12 日（后延至 6 月 26 日）前更新应用。

该事件是 AI 实验室首次大规模公开披露供应链攻击对其代码签名体系的影响，也验证了 OpenAI 在 Axios 事件后加速部署的供应链安全控制的必要性。

## 关键发现 / 关键技术

### 1. 攻击路径与影响范围
- TanStack 攻击者利用 pull_request_target "Pwn Request" 模式、GitHub Actions 缓存投毒和 OIDC token 内存提取，发布了 42 个包的 84 个恶意版本
- 恶意载荷在 npm install 生命周期中执行，窃取 AWS/GCP/K8s/Vault/GitHub/npm/SSH 凭证，并通过 Session/Oxen 网络外泄、自我传播
- OpenAI 两台员工设备中招，攻击者在员工可访问的有限内部代码仓库子集中活动，仅少量凭证被实际窃取

### 2. 应急响应措施
- 隔离受影响系统与身份、撤销用户会话、轮换受影响仓库全部凭证、临时限制代码部署工作流
- 聘请第三方数字取证与事件响应公司；未发现客户数据或知识产权受影响、未发现凭证被滥用或后续访问迹象

### 3. 代码签名证书轮换
- 受影响仓库含 iOS、macOS、Windows 签名证书，出于预防全部轮换；macOS 用户需更新应用（ChatGPT 桌面版、Codex 应用、Codex CLI、Atlas），Windows/iOS 用户无需操作
- 与平台供应商合作停止旧证书新公证，并审计历史公证记录，未发现异常签名或软件篡改

### 4. 事件后的系统性加固
- Axios 事件后已加速部署：CI/CD 流水线敏感凭证加固、包管理器最低发布年龄（minimumReleaseAge）控制、新软件包来源验证
- 本次事件发生在分阶段部署推进期间，进一步验证了这些控制的价值

## 实践意义

对所有依赖 npm 生态的团队，这是教科书级的供应链攻击样本：(1) pull_request_target + 缓存投毒 + OIDC 窃取的组合拳绕过了传统"首贡献者审批"防线；(2) 首个携带有效 SLSA provenance 的恶意 npm 包，证明来源证明不足以替代安装时行为分析；(3) 最低发布年龄、凭证最小化、签名证书与代码仓库隔离应成为标配。对 AI 厂商而言，代码签名证书进入攻击面意味着供应链事件可直接威胁终端用户信任链。

## 跨厂商对比

- 与 [OpenAI 与 Hugging Face 处理模型评估安全事件](hugging-face-model-evaluation-security-incident.md) 对比：前者是第三方开源库波及内部，后者是评估基础设施被定向攻击，两者都指向 AI 供应链安全的系统性风险
- 与 [Daybreak：守护全球每个组织](daybreak-securing-the-world.md) 互补：Daybreak 是 OpenAI 对外输出的网络防御产品，本文则是其自身作为攻击目标的实战案例
- 与 [Anthropic 三起近期事件复盘](../../anthropic/engineering/a-postmortem-of-three-recent-issues.md) 对比：两者都体现头部实验室以公开复盘建立信任的趋势，但 Anthropic 聚焦服务可靠性，OpenAI 聚焦安全入侵

## 资源

- 原文：[Our response to the TanStack npm supply chain attack](https://openai.com/index/our-response-to-the-tanstack-npm-supply-chain-attack/)
- TanStack 官方复盘：[Postmortem: TanStack npm supply-chain compromise](https://tanstack.com/blog/npm-supply-chain-compromise-postmortem)
- Socket 分析：[TanStack npm packages compromised](https://socket.dev/blog/tanstack-npm-packages-compromised-mini-shai-hulud-supply-chain-attack)
