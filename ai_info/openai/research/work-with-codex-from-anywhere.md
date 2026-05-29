# Work with Codex from Anywhere

- **原文链接**: [Work with Codex from anywhere](https://openai.com/index/work-with-codex-from-anywhere/)
- **作者**: OpenAI
- **发布日期**: 2026-05-14
- **检索日期**: 2026-05-29
- **标签**: #Codex #移动端 #RemoteSSH #Hooks #ProgrammaticAccessTokens #企业工作流

## 核心观点

Codex 进入 ChatGPT 移动端预览，使用户可以从手机查看、指导、批准和继续 Codex 在本地或远程开发环境中的长任务。文章展示了 Codex 的产品形态从“开发机上的 Agent”扩展为“跨设备、跨环境的持续协作系统”。

## 关键更新

### 移动端 Codex
- 用户可以在手机上查看线程、输出、截图、终端结果、diff、测试和审批请求。
- 文件、凭据、权限和本地配置仍留在 Codex 运行的机器上。
- 安全 relay 层负责跨设备同步活跃 session，而不是直接暴露机器到公网。

### 长任务协作节奏
- Agent 执行时间变长后，及时回答问题、选择方向、批准命令会显著影响任务质量。
- 手机端让用户在通勤、会议间隙或离开电脑时继续参与。

### 企业环境支持
- Remote SSH 进入 GA，可连接企业 managed remote environments。
- 新增 scoped programmatic access tokens、Hooks、HIPAA-compliant local Codex 等企业能力。

## 关键洞察

1. **长任务 Agent 需要跨设备监督**：移动端不是玩具功能，而是让人类保持在 loop 中。
2. **安全 relay 比公网暴露更适合 Agent**：状态同步和权限控制必须与远程执行分离。
3. **Hooks 和 programmatic tokens 让 Codex 更像企业平台**：从个人开发助手走向可治理自动化层。

## 相关文章

- [Codex for (almost) everything](codex-for-almost-everything.md)
- [Running Codex Safely at OpenAI](running-codex-safely.md)
- [Introducing GPT-5.3-Codex](introducing-gpt-5-3-codex.md)
