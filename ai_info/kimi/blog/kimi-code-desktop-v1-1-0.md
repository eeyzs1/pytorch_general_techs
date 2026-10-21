# Kimi Code Desktop v1.1.0:Linux 版、远程控制与进展更新(Kimi Code Desktop v1.1.0)

- **原文链接**: [Kimi Code Desktop Changelog — v1.1.0](https://www.kimi.com/code/docs/kimi-code-desktop/changelog.html)
- **作者**: Moonshot AI
- **发布日期**: 2026-10-14
- **检索日期**: 2026-10-16
- **标签**: #KimiCode #桌面端 #Linux #远程控制 #进展更新 #跨平台

## 核心观点

Desktop v1.1.0(10-14)是 GA 后首个大版本:补齐 Linux 支持(AppImage/deb/RPM,x86_64),自 09-17 发布起一个月内完成 macOS/Windows/Linux 三平台覆盖;CLI 同步升至 v2.2.0。

两个新能力都指向"长任务期间的人机监督":远程控制让手机/平板/另一台电脑通过链接或二维码接管本机 Agent,任务与本地工具仍在运行桌面端的电脑上执行;实验性"进展更新"(NotifyUser 工具)让 Agent 在回合内主动发布简短进展,人不再对着黑盒等待。CLI 侧 WaitFor 等待可被消息打断、Tower 运行中发消息即中止当前轮次,同属"Agent 工作期间人可插话"这一交互命题。

## 关键发现 / 关键技术

### 1. Linux 版本:三平台补齐

- x86_64 架构,提供 AppImage、deb、RPM 三种安装包
- 桌面编码 Agent 平台覆盖进度:09-17 macOS(Apple Silicon/Intel)+ Windows → 10-14 + Linux

### 2. 远程控制(Remote Control)

- "设置 → 远程控制"开启后,可通过链接或二维码从手机、平板或另一台电脑控制本机 Agent
- 任务与本地工具仍在运行桌面端的电脑上执行——远程端只是监督/操纵横
- 与 CLI 侧 Remote Control(09-09 v0.42.0 转正)在桌面端汇合,双端同构

### 3. 进展更新(NotifyUser,实验性)

- Agent 可在回合内发布简短进展,对话中实时可见
- 默认关闭:Desktop 在"设置 → 实验室"、CLI 在 `/experiments` 开启,仅影响之后新建的会话
- 把"过程可见性"从回合间的 todo 列表细化到回合内的即时播报

### 4. CLI v2.2.0 配套

- `kimi app [path]`:从终端在当前或指定目录唤起桌面端新会话,CLI→GUI 一键切换
- WaitFor 后台等待可被消息打断:等待最长 90 秒,期间按 Enter 或 Ctrl-S 可把消息注入当前轮次并提前结束等待,后台任务继续运行
- Tower 模式:Agent 运行中发送的消息会中止当前 turn 并作为独立 turn 执行
- 全屏模式为用户消息保留一行摘要,点击可跳回原消息

### 5. 桌面端配套改进

- 右侧栏新增文件树面板:浏览、搜索、刷新工作区文件,点击预览;`Cmd/Ctrl+Shift+E` 快速开关
- 内置浏览器:新增下载进度;Agent 可处理网页弹窗;可暂停 Agent 对页面的控制
- Agent 等待后台任务时,排队与新发送的消息立即送达
- 修复:部分 Mac 上 emoji 导致界面崩溃、大文件无法查看逐行差异等

## 实践意义

- **"桌面执行 + 移动监督"成为长任务标准形态**:挂机跑 Agent、通勤路上用手机接管审批,远程控制把等待时间变成可监督时间
- **回合内交互通道是新战场**:NotifyUser、WaitFor 可打断、Tower 消息中止当前轮,三件事共同解决"Agent 一跑十几分钟、人只能干等"的体验痛点
- **Linux 版的信号**:桌面 Agent 竞争从个人开发者扩展到服务器端/容器化工作流的企业场景

## 跨厂商对比

- 与 [Work with Codex from Anywhere](../../openai/research/work-with-codex-from-anywhere.md) 对比:Codex 把长任务延伸进 ChatGPT 移动端查看/指导/批准,走"超级 App 内嵌"分发;Kimi 用链接/二维码点对点接管本机 Agent,走"轻量直连"——远程监督的两种产品形态
- 与 [Introducing the Codex App](../../openai/research/introducing-the-codex-app.md) 对比:同为桌面多 Agent 工作台,Codex App 先 macOS 再扩展 Windows;Kimi Desktop 一个月内走完三平台,且 CLI/桌面端/VS Code 三形态共用一套会话体系
- 与 [Kimi Code Desktop 正式发布](kimi-code-desktop.md) 关联:GA 后 27 天即推 v1.1.0,远程控制从 CLI 实验特性(08-27)到 CLI 转正(09-09)再到桌面端落地(10-14),六周完成一条特性的全端铺开

## 资源

- 发布:[Kimi Code Desktop 变更记录](https://www.kimi.com/code/docs/kimi-code-desktop/changelog.html)
- 汇总:[Kimi Code: What's New](https://www.kimi.com/code/docs/kimi-code/whats-new.html)
- 下载:[Kimi Code](https://www.kimi.com/code)
