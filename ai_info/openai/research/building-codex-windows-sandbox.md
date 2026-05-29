# Building a Safe, Effective Sandbox to Enable Codex on Windows

- **原文链接**: [Building a safe, effective sandbox to enable Codex on Windows](https://openai.com/index/building-codex-windows-sandbox/)
- **作者**: David Wiesen, Member of Technical Staff
- **发布日期**: 2026-05-13
- **标签**: #Codex #Windows #沙箱 #安全 #工程 #隔离

## 核心观点

Windows 没有开箱即用的沙箱隔离工具（不像 macOS 的 Seatbelt 或 Linux 的 seccomp/bubblewrap）。为了在 Windows 上实现与 macOS/Linux 同等安全和体验的 Codex，OpenAI 从零设计了两代沙箱方案：unescalated（无需管理员权限，但网络安全弱）和 elevated（需管理员权限，提供完整网络安全）。文章详述了从 AppContainer、Windows Sandbox、MIC 等现成方案被逐一否决，到最终用 SID + Write-Restricted Token + 专用 Windows 用户 + Firewall 规则构建完整沙箱的全过程。

## 为什么需要自建沙箱

Codex 运行时代理以真实用户权限执行命令（功能强大但危险）。默认模式：
- 允许几乎任意位置读取文件
- 允许 workspace 内写入文件
- 无互联网访问（除非用户指定）

这些约束需要操作系统强制执行——但 Windows 缺乏相应原语。

## 被否决的现成方案

| 方案 | 优势 | 否决原因 |
|------|------|----------|
| **AppContainer** | 真正的 OS 能力边界隔离 | Codex 不是单一范围 App，它驱动开放开发者工作流（shell、Git、Python、包管理器），AppContainer 模型太窄 |
| **Windows Sandbox** | 强隔离、用完即弃 | Codex 需直接操作用户的实际 checkout 和环境，Windows Sandbox 是独立桌面 VM，且不支持 Windows Home |
| **MIC 完整性标签** | 看似优雅——低完整性进程不能写高完整性对象 | 将 workspace 标记为低完整性意味着所有低完整性进程都能写，改变了主机信任模型 |

## 第一代：Unescalated Sandbox（不用管理员权限）

### 文件写入限制

利用两个 Windows 构建块：
1. **SID (安全标识符)**: 创建合成 SID（sandbox-write），只用于 Codex 沙箱
2. **Write-Restricted Token**: 写操作需通过双重检查——(a) 普通用户身份允许 + (b) restricted SID 列表中的至少一个 SID 也被授权

流程：sandbox-write SID 被授予 workspace 的写/执行/删除权限，并明确拒绝 `.git/.codex/.agents` 目录。Codex 在 write-restricted token 下启动命令。

### 网络限制（仅建议级别）

通过环境变量封堵代理及 Git 流量：
```
HTTPS_PROXY=http://127.0.0.1:9
GIT_SSH_COMMAND=cmd /c exit 1
```
并前置 denybin 目录到 PATH 重排 PATHEXT，拦截 SSH/SCP。但这是**建议级别的**——进程可绕过环境、PATH，或直接打开 socket。

### 缺点

- **速度**: 对大型 workspace 应用 ACL 开销大
- **足迹**: 在开发者系统上应用真实 ACL
- **语义固定**: 调整沙箱语义需重新应用 ACL
- **网络安全弱**: 无法阻挡对抗性代码或用非标准网络栈的程序

## 第二代：Elevated Sandbox（需管理员权限，当前实现）

核心变化：不再以真实 Windows 用户身份运行命令，而是**创建两个专用本地用户**：
- `CodexSandboxOffline`: 被防火墙规则针对（阻止所有出站）
- `CodexSandboxOnline`: 不被防火墙针对（允许网络）

命令仍在 write-restricted token 下运行（SID 列表：[Everyone, Logon, Synthetic]），但 token 的 principal 是专用用户而非真实用户。

### 设置步骤

1. 创建合成 SID
2. 创建 online/offline 沙箱用户
3. 用 DPAPI 加密存储新用户凭证（沙箱用户无法读取）
4. 创建防火墙规则——阻止 CodexSandboxOffline 的所有出站流量
5. 通过配置使 CodexSandboxOffline 获得等同于真实用户的读访问

### 读访问等价实现

在 Unescalated 版本中，write-restricted token 的 principal SID 是真实 Windows 用户，自然获得等价读权限。在 Elevated 版本中，需额外机制确保沙箱用户能读用户文件——这是新设计的复杂性核心。

## 关键洞察

- 安全不在于表面约束，而在于 OS 级强制执行
- Windows 生态中"Agent 安全运行"的目标与现有工具之间存在根本性失配
- 从"无需提权"到"接受提权"的转变是因为网络安全太重要，不能用建议级别方案
- 该架构使 Codex 在 Windows 上获得了与 macOS/Linux 同等的安全保证