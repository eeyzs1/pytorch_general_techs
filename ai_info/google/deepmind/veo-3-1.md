# 发布 Veo 3.1 与 Flow 的高级能力（Introducing Veo 3.1 and advanced capabilities in Flow）

- **原文链接**: [Introducing Veo 3.1 and advanced capabilities in Flow](https://blog.google/innovation-and-ai/products/veo-updates-flow/)
- **作者**: Google（DeepMind 视频生成团队）
- **发布日期**: 2026-08-06
- **检索日期**: 2026-08-21
- **标签**: #Google #Veo3.1 #视频生成 #多模态 #Flow #4K #竖屏视频

## 核心观点

Google 发布 Veo 3.1，新一代视频生成模型，新增 4K 输出、原生竖屏视频（vertical video）支持与改进的"Ingredients to Video"（素材转视频）功能，并同步升级 Flow 创作工具。Veo 3.1 旨在回应 Sora 2 等竞品，强化可控性与角色一致性。

升级重点包括：更高保真度的 4K 超分辨率、角色跨镜头一致性提升、竖屏（9:16）原生支持适配短视频生态，以及增强的音视频同步质量。Flow 工具同步获得新能力，让创作者可在单一工作流中完成视频构思、生成与迭代。

## 关键发现 / 关键技术

### 1. 4K 输出与超分辨率
- 支持 4K 分辨率视频生成
- 高保真超分（upscaling）提升细节还原
- 在保持生成速度的同时提升画质

### 2. 原生竖屏视频
- 原生支持 9:16 竖屏格式，适配短视频平台
- 避免横屏裁切导致的构图问题
- 直接对标短视频创作场景

### 3. 角色一致性与素材转视频
- "Ingredients to Video"（素材转视频）改进：图片/素材 → 视频的转化更可控
- 角色一致性提升，跨镜头保持人物特征稳定
- 音视频同步质量增强

### 4. Flow 工具升级
- 创作工具 Flow 集成 Veo 3.1 新能力
- 提供更完整的"构思-生成-编辑"工作流

## 实践意义

视频生成正从"能生成"走向"能控制"。Veo 3.1 的 4K + 竖屏 + 角色一致性组合，直接服务短视频与广告制作场景，标志着视频模型进入创作者可用阶段。对开发者而言，Veo 3.1 同步在 Gemini API 中提供，支持程序化调用。跨厂商看，OpenAI 的 Sora 2 与 Google Veo 3.1 在 2026 年下半年正面竞争，控制性成为关键差异点。

## 跨厂商对比

- 与 [Gemini Omni：从任意内容创造任意内容](gemini-omni.md) 互补：Gemini Omni 打通多模态生成，Veo 3.1 深化视频单一模态的工业级能力
- 与 [Nano Banana 2 Lite 与 Gemini Omni Flash 开发者发布](start-building-with-nano-banana-2-lite-and-gemini-omni-flash.md) 对比：图像生成聚焦创作辅助，视频生成（Veo 3.1）聚焦专业制作
- 与 [OpenAI 视频生成 Sora 相关文章](../../openai/research/beyond-rate-limits.md) 对比：OpenAI 关注访问与扩展，Google 关注控制性与格式适配

## 资源

- 论文：N/A
- 官方公告：https://blog.google/innovation-and-ai/products/veo-updates-flow/
- Gemini API 版本：https://blog.google/innovation-and-ai/technology/developers-tools/veo-3-1-gemini-api/
