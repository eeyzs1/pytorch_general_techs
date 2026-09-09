# Claude 的记忆全入口生效，内容由你决定（Claude's memory works everywhere, and you decide what's in it）

- **原文链接**: [Claude's memory works everywhere, and you decide what's in it](https://claude.com/blog/claudes-memory-works-everywhere-and-you-decide-whats-in-it)
- **作者**: Anthropic
- **发布日期**: 2026-08-25
- **检索日期**: 2026-09-09
- **标签**: #Memory #Personalization #Privacy #CrossProduct

## 核心观点

Claude 的记忆功能完成两项升级：其一，跨入口统一——聊天与 Claude Cowork 共享同一份记忆，无论在哪里与 Claude 协作，它都从"已知你的事"开始；其二，用户完全可控——记忆按主题存为一列短文件，可逐条查看、编辑、删除，改一处处处生效。记忆的更新方式也从"对话结束后总结"改为"边聊边写"，可随时暂停或重置。

隐私设计采取分级默认：健康、种族、宗教、政治、性别认同等敏感主题默认不入记忆；确有需要的用户可在设置中显式开启"包含敏感主题"（每次保存均有通知、不回溯既往），而 SSN/政府证件号、犯罪记录、移民状态及违反 AUP 的内容则无论如何都不存储。

## 关键发现 / 关键技术

### 1. 聊天与 Cowork 的一份记忆
- Cowork 云端执行任务时自动带上聊天中积累的上下文（如 Q3 优先级、项目状态），任务中出现的信息也回流聊天。
- 典型场景：让 Cowork 给经理起草更新，它已知道经理是谁、喜欢什么格式；在聊天里头脑风暴会议议程后，Cowork 做预算与后勤文档时已知人数、城市与讲者；解释一次团队指标定义，之后每份 QBR deck 都自动沿用。

### 2. 实时更新与可见可控
- 对话中提到"项目截止改到九月"，下次对话自动知道，无需说"记住这个"；可暂停或重置记忆。
- Memory 设置中的 Topics 页把所有记忆呈现为短文件列表：读、改、删均可；改掉公司旧名一处，此后所有对话都正确。

### 3. 敏感主题的分级处理
- 默认排除：健康、种族、族裔、宗教信仰、政治、性别认同等个人或敏感主题。
- 可选开启：开启后 Claude 会记住如麸质过敏这类信息用于食谱建议；每次保存敏感主题都有通知；只对开启之后的对话生效，不回溯。
- 永不存储（即使开启）：敏感身份证件号（SSN、政府证件号等）、犯罪记录、移民状态、违反 AUP 的内容；无法写入时 Claude 会告知用户。

### 4. 可用性
- Free/Pro/Max 计划在 web、桌面、移动端默认开启；敏感主题存储默认关闭。
- Team/Enterprise 由管理员控制可用性，且对个人用户默认关闭、需自行开启。

## 实践意义

记忆的"跨产品统一"是把 Claude 从单次工具变成持续协作助手的结构性一步：上下文在聊天与 Agent 任务间双向流动，重复交代成本归零。更值得关注的是其隐私工程——三档设计（默认排除 / 显式 opt-in + 逐次通知 + 不回溯 / 永不存储）比"全有或全无"的记忆开关精细得多，为消费级 AI 产品的敏感数据处理提供了可参照的分级模式。

## 跨厂商对比

- 与 [ChatGPT memory dreaming](../../openai/research/chatgpt-memory-dreaming.md) 对比：OpenAI 在探索记忆的后台整理（"梦境"式重放与巩固）机制，Anthropic 此次的重点在跨入口统一与用户可控粒度（按主题文件编辑、敏感分级），反映两家对"记忆该解决什么问题"的不同侧重。
- 与 [Claude Code best practices](claude-code-best-practices.md) 互补：CLAUDE.md 是开发者侧的持久化上下文约定，产品级 Memory 把同类"可审阅的持久记忆"思想带给普通用户。

## 资源

- 官方文章：https://claude.com/blog/claudes-memory-works-everywhere-and-you-decide-whats-in-it
- 相关产品：https://support.claude.com/en/articles/11817273-use-claude-s-chat-search-and-memory-to-build-on-previous-context（帮助中心）
