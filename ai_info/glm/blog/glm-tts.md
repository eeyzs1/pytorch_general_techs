# GLM-TTS:多奖励融合强化学习的工业级语音合成(GLM-TTS: Industrial-Grade Speech Synthesis with Multi-Reward RL)

- **原文链接**: [GLM-TTS: Industrial-Grade Speech Synthesis with Multi-Reward Fusion Reinforcement Learning](https://www.zhipuai.cn/zh/research/147)
- **作者**: 智谱 GLM 团队
- **发布日期**: 2025-12-10
- **检索日期**: 2026-09-29
- **标签**: #GLM-TTS #智谱 #语音合成 #GRPO #流匹配 #声音复刻

## 核心观点

GLM-TTS 是智谱面向工业级落地的语音合成系统,核心主张是"数据效率 + 强化学习对齐":仅用 10 万小时数据即具备 3 秒音色复刻能力。系统采用两阶段架构——Whisper-VQ token 建模语言内容 + 条件流匹配生成梅尔谱,再由自研 2D-Vocos 还原音频;tokenizer 将帧率从 12.5Hz 提升到 25Hz、词表扩至 32k,并引入 Pitch Estimator 保住韵律。

对齐阶段用 GRPO 同时优化四个奖励(字错率 CER、说话人相似度、情感、笑声)并做分层正则化。结果上 seed-tts-eval 中文 CER 低至 0.89%,为开源 SOTA(优于 CosyVoice2 的 1.38% 等);LoRA 音色定制只需 15% 参数、约 1 小时音频,还支持方言与歌声。

## 关键发现 / 关键技术

### 1. 两阶段声学架构

语言与声学解耦,各阶段可独立优化。

- 阶段一:Whisper-VQ token 建模语言内容
- 阶段二:条件流匹配生成梅尔谱 + 自研 2D-Vocos 声码器
- 自研 2D-Vocos 替代通用声码器,适配梅尔谱到音频的还原

### 2. Tokenizer 与韵律

- 帧率 12.5Hz → 25Hz,序列建模效率与细节兼得
- 词表 32k
- Pitch Estimator 显式建模音高,防止韵律塌缩
- 韵律保护是多奖励对齐之外另一条质量底线

### 3. GRPO 多奖励强化学习

四个奖励覆盖"听得清 + 听得像 + 听得有感情"三层目标。

- 奖励一:字错率(CER),保正确性
- 奖励二:说话人相似度,保音色还原
- 奖励三:情感;奖励四:笑声——指向"听得像人"
- 分层正则化平衡多目标,避免某一项奖励主导

### 4. 关键数据

- 10 万小时训练数据即具备 3 秒音色复刻
- seed-tts-eval 中文 CER 0.89%,开源 SOTA
- 对比:优于 CosyVoice2 的 1.38% 等既有开源系统
- LoRA 音色定制:仅 15% 参数、约 1 小时音频

### 5. 场景延展

- 支持方言与歌声合成
- 与次日发布的 ASR 姊妹模型构成智谱语音双件套

### 6. 定制化工作流

音色资产化:品牌声音从"请人配"变成"LoRA 训练"。

- LoRA 音色定制:仅 15% 参数
- 所需数据:约 1 小时音频
- 小参数量定制意味着训练与存储成本可控

### 7. 数据效率的门槛意义

- 10 万小时即具备 3 秒音色复刻,远低于传统海量数据范式
- 中小团队也有能力训练工业级 TTS
- 数据效率来自 RL 对齐,而非单纯堆数据
- 开源 SOTA + 低数据门槛,共同压低了行业准入

## 实践意义

GLM-TTS 验证了"中等数据 + 多奖励 RL"可以替代"海量数据 + 纯监督"的旧范式,10 万小时即达工业级,大幅降低了准入门槛。LoRA 定制(15% 参数、1 小时音频)让中小厂商能低成本构建品牌音色;笑声、情感作为显式奖励被优化,说明 TTS 的竞争焦点已从"听得清"转向"听得像人"。对语音产品团队,0.89% 的中文 CER 与方言/歌声支持几乎覆盖了国内主流落地场景,开源 SOTA 也让私有化部署不再牺牲质量。

## 跨厂商对比

- 与 [GPT-5.5](../../openai/research/introducing-gpt-5-5.md) 对比:OpenAI 把语音能力整合进闭源旗舰的通用多模态路线,智谱以独立开源模型交付工业级 TTS,可私有化、可 LoRA 定制音色,两条路线在成本与可控性上互补
- 与 [GLM-ASR-Nano:高鲁棒性语音识别](glm-asr-nano.md) 互补:TTS + ASR 组成智谱语音全双工闭环,且同为"小团队可私有化部署"路线
- 与 [GLM-OCR:SOTA 复杂文档解析](glm-ocr.md) 对照:同属模态专用小模型 + 开源 SOTA 路线,OCR 占文档入口,TTS 占语音出口

## 资源

- 官方发布:https://www.zhipuai.cn/zh/research/147
- API 文档:https://docs.bigmodel.cn/
- 语音识别姊妹模型:https://www.zhipuai.cn/zh/research/149
- 智谱开放平台:https://www.bigmodel.cn/
