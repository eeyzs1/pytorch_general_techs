# Gemini 3.8 Live with Live Avatar:可视化实时代理(Introducing Gemini 3.8 Live with Live Avatar)

- **原文链接**: [Introducing Gemini 3.8 Live with Live Avatar](https://deepmind.google/blog/introducing-gemini-38-live-with-live-avatar/)
- **作者**: Gemini 团队
- **发布日期**: 2026-09-24
- **检索日期**: 2026-09-29
- **标签**: #Gemini #Live #虚拟形象 #数字人 #企业级

## 核心观点

Google 为 Gemini 3.8 Live 加上"一张脸":Live Avatar 是可视化实时代理,同时接收视频与音频输入,实时渲染口型同步、表情与轮次感知的虚拟形象。最关键的工程决策是工具调用异步执行——数据在后台获取时,虚拟形象继续讲述、不冷场。

口型同步覆盖 97 种语言,音频与视频输出均嵌 SynthID 水印。产品随 Gemini Enterprise 提供,企业可凭参考图像定制品牌形象(白名单机制);官方未公布延迟、基准与定价,评估需自行实测。

## 关键发现 / 关键技术

### 1. 双模态输入与实时渲染
- 同时接收视频 + 音频输入:既"听见"也"看见"用户
- 实时渲染口型同步(97 种语言)、面部表情与轮次感知——知道何时该说、何时该听
- 形象与语音同源驱动,口型与内容逐帧对齐
- 形象以实时视频流输出,与语音同步生成而非后期合成

### 2. 异步工具调用:把等待变成讲述
- 工具调用在后台异步执行,数据未返回时虚拟形象继续讲述过渡内容
- 消除传统语音代理最尴尬的静默等待,延迟被"藏进"对话流
- 与 3.8 Live 的后台异步工具调用机制一脉相承

### 3. 水印与企业交付
- SynthID 水印同时嵌入音频与视频输出,双通道可溯源
- 随 Gemini Enterprise 提供;参考图像定制品牌形象走白名单机制
- 官方未给出延迟数字、基准成绩与定价——选型前需自建 PoC 实测

### 4. 在实时语音全栈中的位置
- 与 3.8 TTS 同日(2026-09-24)发布,两者都构建在 3.8 Live(2026-09-15)之上
- Live 管语音底座、Avatar 管形象层、TTS 管离线输出,Google 九月内凑齐实时语音栈
- Live Avatar 定位企业级可视化层,而非消费级玩具

## 实践意义

数字人产品长期卡在两件事上:"恐怖谷"与"等待冷场"。Live Avatar 的价值排序很清楚:先用异步工具调用解决"卡顿感",再用 97 种语言的口型同步解决"全球化脸面"。对客服、销售、培训等企业场景,这两点恰好是可用性的分水岭。

但官方缺失延迟/基准/定价三件套,意味着采购决策只能黑盒实测:视频渲染的端到端延迟、形象定制的白名单门槛、与现有联络中心系统的集成成本,都需在 Gemini Enterprise 预览中逐一验证。SynthID 双通道水印则让 AI 生成形象的合规披露有了技术抓手。

采购策略上可借力语音底座的公开基准:先验证 3.8 Live 的对话质量(有 Speech Agent Arena 等外部榜单可依),再评估 Avatar 的渲染层(无官方数字),能显著降低整体评估成本。

## 跨厂商对比

- 与 [Muse Realtime Avatar](../../meta/muse-realtime-avatar.md) 对比:Meta Connect 推出的实时形象同样瞄准"有脸的实时代理",Muse 系深度绑定个人助理消费生态,Live Avatar 绑定 Gemini Enterprise——两家分别在消费与企业两端落子。
- 与 [Muse 个人 AI 助理](../../meta/introducing-muse-personal-ai-agent.md) 对比:Muse 的形象是"助理人格"的载体,Live Avatar 是"企业品牌形象"的载体——拟人化陪伴与品牌代言两种产品叙事。
- 与 [Gemini 3.8 Live 与 Live Extended Thinking](gemini-3-8-live-extended-thinking.md) 互补:3.8 Live 提供语音与工具调用底座(基础版在 Speech Agent Arena 排第二),Live Avatar 是其可视化层,对话上限由底座决定。
- 与 [Gemini 3.8 Flash TTS 与 Flash-Lite TTS](gemini-3-8-tts.md) 互补:Avatar 管实时形象化交互,TTS 管离线语音量产,同日发布补全输出侧两种形态。

## 资源

- 官方文章:https://deepmind.google/blog/introducing-gemini-38-live-with-live-avatar/
- 语音底座:https://deepmind.google/blog/introducing-gemini-3-8-live-and-3-8-live-extended-thinking/
- 输出侧同批发布:https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-8-text-to-speech/

> 注:deepmind.google 在检索环境不可达,本文经 my2cents.ai 日报(引用官方原文)/the-decoder/spyingbee 等多源交叉验证。
