# 我们如何把安全内建进 Muse（How We Built Safety Into Muse）

- **原文链接**: [How We Built Safety Into Muse](https://research.meta.ai/blog/security-and-safety-for-ai-agents-our-approach-with-muse)
- **作者**: Tarek Sheasha（Software Engineer & VP, Meta Superintelligence Labs）
- **发布日期**: 2026-09-08
- **检索日期**: 2026-09-09
- **标签**: #Muse #安全架构 #个人智能体 #PromptInjection #Sentinel #SecureVM #最小权限 #eBPF

## 核心观点

这是 Muse 个人智能体发布日的配套安全架构长文（内部代号 Hatch）。Meta 的核心主张：**无论模型多强，Agent 都会犯错、也会被它读取的数据攻击**——所以系统必须假设"Agent 可能正处于攻击之下"来设计，用确定性边界限制任何单点失败的破坏半径。

文章给出个人 Agent 安全的完整工程答卷：每用户独立云 VM（两个隔离安全域而非"有 root 的 LLM"）、运行时单元外置的安全服务（分类器/凭据/权限）、Sentinel 作为唯一权限当局、凭据代理化（模型永远看不到真实 token）、eBPF 内核级数据流污点追踪，以及对 prompt injection"致命三要素"（lethal trifecta）的纵深防御。同步开放最高 $300,000 的 Muse 漏洞赏金（单用户 prompt injection 成功最高 $130,000）。

## 关键发现 / 关键技术

### 1. Muse Secure VM：一台"你自己的云电脑"
- 每用户独占一个云端 VM：数据、凭据、Muse 本体全部在其中；客户端（iOS/Android/Web）经安全传输层直连 VM
- **两个隔离安全域**：核心 harness（Hatch 守护进程）、工作区文件与工具运行在 `systemd-nspawn` 运行时单元内——单元内 root 映射为宿主非特权用户、独立 Debian 根文件系统、虚拟网卡、过滤系统调用（禁 `io_uring`）、裁剪内核能力（无 `CAP_SYS_PTRACE`/`CAP_NET_ADMIN`）
- 敏感服务外置为独立 systemd 单元：`hatch-safety`（独立模型/分类器检查推理请求响应——攻击者无法关闭）、`privsep`（受限于窄权限的连接器代码执行）、`hatch-authd`（凭据存储与代理化，OAuth token 存用户 VM 而非 Meta 中心设施）、Sentinel（唯一权限当局）、独立 postgres 存应用状态
- 单元间通信用 Unix domain socket + SO_PEERCRED + peer ACL——内核认证、最小权限、无密钥可偷

### 2. Sentinel：唯一权限当局
- Muse 只能"提议"动作，Sentinel 才能"批准"——对连接器动作与全部网络出口做 allow / deny / ask 判定
- 网络出口在第 4 层与第 7 层评估（主机名、解析后与最终 IP、端口、协议、HTTP 方法、路径、解码后的请求体）；SSRF 限制防止"公网域名解析到内网"
- **即时凭据注入**：运行时单元只见 authd 铸造的"代理 token"，真实凭据在网络边界由 Sentinel 替换——通过 prompt injection 逼 Agent 吐出真实密钥是徒劳的
- **Tainted egress（污点出口）**：eBPF（cgroup 程序 + 自研 LSM 钩子）做内核级数据流追踪——"干净"进程的窄域请求可自动放行，读过用户数据的"污点"进程回退到人工审批，以此控制审批的信噪比

### 3. 人工在环：审批是严格能力而非对话建议
- 审批绑定具体连接器/目的地/用例，支持一次性、会话级、任务级、限时、永久五档；对话框出现在客户端 UI 而非与 Muse 的对话中（防对话内注入伪造确认）
- 目标不是"事事都问"：只读、已授权、低风险动作免打扰——把摩擦放在"同意真正重要"的地方

### 4. 最小权限的处处贯彻
- 读写分离（先给读日历、后给写日程）；粒度细于 OAuth scope（如 Gmail 只读却可剥离"访问设置"能力）
- 连接器 CLI 只在单元内解析参数，经 Unix socket 交给 systemd 沙箱 worker 执行业务逻辑；日历 worker 改参数也拿不到邮件凭据（authd ACL + cgroup 身份）
- 邮件连接器用确定性过滤器 + 分类器**剔除一次性验证码、密码重置链接、魔法登录链接**——防止"连了邮箱 = 代言你在全网的身份"

### 5. Prompt Injection 纵深防御（对"致命三要素"）
- 模型层：训练抗注入（Muse Spark 1.3 接近 SOTA，配套追踪评估集）
- Harness 层：外部来源数据全部标记为不可信输入，强化开发者指令优先级
- 系统层：多分类器集成 + 规模化 agentic 红队（独立于模型训练，整体准确率更高）
- 确定性兜底：运行时单元限制系统访问、privsep 限制凭据可见性、Sentinel 评估每个动作与出口

### 6. 浏览器与支付
- 真实 Chromium 跑在虚拟化层后：子 Agent 只见**无障碍树快照**而非原始 DOM，无 JS 执行、无脚本动词、Chrome DevTools 禁用；用户接管或凭据自动填充时 Agent 完全暂停
- 网站登录凭据经客户端自定义 UI 直送 authd，按需注入浏览器——主 Agent 不可见
- 分类器家族盯五类威胁（无关个人数据出口 / DOM 注入 / 图片注入 / 下载文件注入 / 高危表单提交）+ Meta 恶意网站黑名单在 VM 内本地匹配
- 支付：结账页检测强制每次人工审批；钱包先接 Stripe Link（Shop Pay 即将），支付用**绑定特定商家+金额+时限的一次性卡号**——即使被偷也无用

### 7. 漏洞赏金与 Muse Confidential VM
- Bug bounty 今日向所有人开放：最高 $300,000（按实际影响），含单用户 prompt injection 成功最高 $130,000
- **Muse Confidential VM（年内推出）**：密码学+可验证地阻止 Meta 自身访问用户 VM 数据——设计文档与源码已交外部审计者，上线后持续接受任何人可检查的公开审计
- 数据政策：文件与记忆随时可查可改可下载；凭据存于用户 VM；对话与 VM 数据不进广告系统（浏览/预订可能间接影响广告）；训练轨迹先去除个人身份信息，可一键 opt-out

## 实践意义

这是迄今对"个人 Agent 安全架构"最完整的公开工程叙述，几乎每个设计都可被其他 Agent 团队直接借鉴：**凭据代理化**（token 在网络边界替换，模型只见过期代理）和 **eBPF 污点出口**（内核级判定"这次请求该不该打扰用户"）是两处最值得学习的原创工程；"审批是能力而非对话"直击用对话伪造确认的攻击面；把一次性验证码/密码重置链接从邮件连接器中过滤掉，则是被普遍忽视的现实攻击路径。配合 Muse Confidential VM 的"密码学上连厂商自己都看不到"路线，Meta 把"可信个人 Agent"的竞争从模型能力拉到了可验证的基础设施层。

## 跨厂商对比

- 与 [Introducing Muse: Personal AI Agent](introducing-muse-personal-ai-agent.md) 互补：发布公告给出产品面（能做什么），本文给出安全面（为什么敢让它做）——Secure VM / Sentinel / 一次性卡号在两篇中分别以用户视角与工程视角呈现
- 与 [Claude in Chrome is generally available](../anthropic/engineering/claude-in-chrome-generally-available.md) 对比：Anthropic 用"分类器逐动作校验 + 红队披露注入成功率"建立浏览器 Agent 信任，Meta 更进一步把浏览器放进每用户隔离 VM、给子 Agent 只暴露无障碍树——两家都在消化 Simon Willison 的"致命三要素"，Meta 的确定性边界层更厚
- 与 [Beyond Permission Prompts](../anthropic/engineering/beyond-permission-prompts.md) 对比：Claude Code 用文件系统/网络隔离沙箱 + auto mode 分类器，Muse 的对应物是 systemd-nspawn 单元 + Sentinel + 污点出口——"审批自动化"的两条路线：分类器决策（Anthropic）vs 内核数据流判定（Meta）

## 资源

- 官方文章：https://research.meta.ai/blog/security-and-safety-for-ai-agents-our-approach-with-muse
- 漏洞赏金：https://bugbounty.meta.com
- 致命三要素原文：https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/
- 安全合作联系：muse-security@meta.com
