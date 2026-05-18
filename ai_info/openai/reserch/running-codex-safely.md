# Running Codex Safely at OpenAI

- **原文链接**: [Running Codex safely at OpenAI](https://openai.com/index/running-codex-safely/)
- **发布日期**: 2026-05-08
- **标签**: #Codex #安全 #沙箱 #OpenTelemetry #企业安全 #审计

## 核心观点

OpenAI 内部部署 Codex 采用多层次安全控制：沙箱执行边界 + 审批策略 + 网络策略 + 身份凭证管理 + 规则引擎 + Agent 原生遥测。核心理念是让低风险日常操作无摩擦，高风险操作显式化并停止审查。同时通过 OpenTelemetry 导出 Agent 原生日志，用 AI 安全 triage agent 解析代理行为意图，区分预期行为、良性错误和真正需要升级的事件。

## 安全控制体系

### 1. 沙箱与审批

沙箱定义技术执行边界（写入位置、网络可达性、受保护路径），审批策略决定何时需要人工介入。当请求跨越沙箱边界时，使用 [Auto-review mode](https://alignment.openai.com/auto-review/) 自动批准低风险操作。

```toml
# config.toml
approvals_reviewer = "auto_review"
sandbox_workspace_write.writable_roots = ["~/development"]

# requirements.toml  
allowed_sandbox_modes = ["read-only", "workspace-write"]
```

### 2. 网络访问

Codex 没有开放式出站访问权限。托管网络策略允许预期目标，阻止不希望的目标，未知域名需审批。

```toml
# requirements.toml
allowed_web_search_modes = ["cached"]

[experimental_network]
enabled = true
allow_local_binding = true
denied_domains = ["pastebin.com"]
allowed_domains = ["login.microsoftonline.com", "*.openai.com"]
```

### 3. 身份与凭证

- CLI 和 MCP OAuth 凭证存储在 OS 安全密钥链中
- 强制通过 ChatGPT 登录
- 访问固定到 ChatGPT 企业 workspace
- Codex 活动可通过 ChatGPT Compliance Logs Platform 审计

```toml
cli_auth_credentials_store = "keyring"
mcp_oauth_credentials_store = "keyring"
forced_login_method = "chatgpt"
forced_chatgpt_workspace_id = "<workspace-uuid>"
```

### 4. 规则引擎

使用 Starlark 规则定义哪些 shell 命令安全（自动允许）和哪些危险（阻止或需审批）。普通开发命令无需审批即可在沙箱外运行，危险模式被阻止。

```starlark
prefix_rule(
  pattern = ["gh", "pr", ["view", "list"]],
  decision = "allow",
  justification = "Allows read-only GitHub PR inspection via gh CLI.",
)
prefix_rule(
  pattern = ["kubectl", ["get", "describe", "logs"]],
  decision = "allow",
)
```

### 5. 托管配置

通过云托管 requirements + macOS 托管偏好 + 本地 requirements 文件的组合应用安全策略。requirements 是管理员强制执行的控制，用户无法覆盖。可按团队、用户组或环境测试不同配置。

## Agent 原生遥测与审计

传统安全日志只能回答"发生了什么"（进程启动、文件变更、网络连接），但无法解释 **为什么** Codex 这样做或 **用户的意图** 是什么。

Codex 支持通过 OpenTelemetry 导出以下事件：
- 用户提示
- 工具审批决策
- 工具执行结果
- MCP 服务器使用
- 网络代理允许/拒绝事件

```toml
[otel]
log_user_prompt = true
environment = "prod"

[otel.exporter.otlp-http]
endpoint = "http://localhost:14318/v1/logs"
protocol = "binary"
```

## AI 安全 Triage Agent

当端点告警说 Codex 做了不寻常的事时，AI 安全 triage agent 使用 Codex 日志检查原始请求、工具活动、审批决策、工具结果和相关网络策略决策/阻止。它将分析呈现给安全团队审查，以区分：
- 预期的 Agent 行为
- 良性错误
- 真正需要升级的事件

## 关键洞察

- 控制只是前半程——Agent 部署后，安全团队需要的是**可见性**和**可解释性**
- Agent 原生遥测是了解 Agent 行为意图的唯一窗口，传统安全日志做不到
- 同样的遥测也用于运营：了解内部采用变化、哪些工具/MCP 在使用、网络沙箱阻止/提示的频率
- OpenTelemetry 日志可集中到 SIEM 和合规日志系统