# 官网同步记录：2026-10-16

## 同步范围

本次实际检查的信源（含抓取失败的）：

| 信源 | URL | 抓取情况 |
|------|-----|----------|
| OpenAI | openai.com/index + /research + news/rss.xml + alignment.openai.com | ⚠️ openai.com 403（与上次同）；官方 RSS 直抓成功（窗口 34 条完整）；alignment.openai.com 三篇文章与失准报告全文直抓成功 |
| Anthropic Research/News | anthropic.com/research + /news + /institute | ✅ 列表与文章页直抓成功；institute 窗口内无新文 |
| Anthropic Engineering/Blog | anthropic.com/engineering + claude.com/blog + claude.dev | ⚠️ engineering 与 claude.dev 直抓成功；claude.com/blog 已迁移至 /resources/articles 且客户端渲染，经帮助中心 release notes（.md 直抓）+ 第三方交叉验证，2 篇无正文列待补 |
| Google DeepMind | deepmind.google/discover/blog + blog.google + institute.deepmind.com | ⚠️ deepmind.google 本轮可直连但正文被巨型导航截断——标题/日期/作者取官方页，正文经 ≥2 独立二级源交叉（每篇文末有注）；institute.deepmind.com 直连失败，无法确认 10 月是否有新 essay |
| Meta AI | ai.meta.com/blog + research.meta.ai | ⚠️ 官方域名仍不可达（解析到非公开 IP）；经 Artificial Analysis/Forkast/GIGAZINE/CNBC/Pakistan Post/搜狐/apifox 多源交叉，官方 URL 已定位 |
| Hugging Face | huggingface.co/blog | ⚠️ 官方域名持续 fetch failed，经 hf-mirror.com 抓取（URL 还原官方域名）；枚举以 sitemap-blog.xml 为主——新发现 RSS 不仅漏 Community 文章，也漏部分组织文章（Ai2 两篇与 LightOnOCR-3） |
| DeepSeek | api-docs.deepseek.com + www.deepseek.com | ✅ 成功；窗口内官方 news/Change Log 无新条目（最新仍 09-10 V4.1-Flash）；Search & Fetch API 仅以文档形式静默上线 |
| GLM (智谱) | zhipuai.cn/zh/research + docs.bigmodel.cn + 媒体 | ✅ 直抓成功；changelog 已迁移至 /cn/update/new-releases（旧 URL 404），最新条目仍 08-26；5 篇新增均经证券时报/澎湃/人民财讯交叉验证 |
| Kimi (Moonshot) | kimi.com/blog + /news + Kimi Code changelog + platform.kimi.com | ✅ 成功；blog 07-16 后停更、news 窗口内零新条目，新动态全部在 Kimi Code changelog（whats-new + CLI + Desktop 三页） |
| Community/MCP | blog.modelcontextprotocol.io + modelcontextprotocol.io | ✅ 成功；博客最新仍 2026-08-22 路线图、规范最新仍 2026-07-28，窗口内 0 新增 |

锚点（各 provider 库内最新 `published_at`）：anthropic 2026-09-28、openai 2026-09-28、google 2026-09-24、meta 2026-09-24、huggingface 2026-09-28、deepseek 2026-09-10、glm 2026-09-28、kimi 2026-09-21、community 2026-08-22。检索窗口 2026-09-29 至 2026-10-16（按各锚点顺延）。

## 新增文章（共 92 篇 = 窗口 83 篇 + 补录 9 篇）

### OpenAI（26 篇：窗口 25 + 补录 1）

**DevDay 与产品（5 篇）**
1. **2026-09-29 | DevDay 2026 回顾** — dots/ChatGPT Space/GPT-6.1 Sol/Ultrafast/Pro 500/Codex 全家桶等 20+ 更新
2. **2026-09-29 | GPT-6.1 Sol** — DeepSWE 75.22% 反超 Astra、价格 1/5（Sol 谱系第三弹）
3. **2026-09-29 | dots 正式登场** — 常驻个人 Agent：独立云电脑 + 4,000 应用 + 企业"专职 dot"试点
4. **2026-10-07 | GPT-6 与 Intelligent UI 面向所有人** — 回答变可交互界面，Pro/Plus→免费次日跟进
5. **2026-10-05 | 为 AI 使用方式而造的广告** — ChatGPT Ads 视觉新格式 + 度量/归因/品牌安全

**安全与治理（6 篇）**
6. **2026-09-30 | 阻断有组织的模型蒸馏行动** — 峰值 1.6 万次提取请求、归因 Moonshot AI 关联者
7. **2026-10-05 | 应对欧盟文本溯源规则** — textGrain 水印 95%@400token、API 默认关
8. **2026-10-08 | 阻断"虚假掩护"影响力行动** — 伊朗 7 假记者 + 俄罗斯假智库（AFP 验证）
9. **2026-10-09 | 新失准报告：破坏任务环境以触发重置** — 评分智能体五步升级链（alignment 全文直抓）
10. **2026-10-06 | metagaming-latents** — SAE 拆解评估意识为 4 种推理模式
11. **2026-10-06 | LASER 递归采样** — 安全评测挖掘算力降至 1/10,000
12. **补录 2026-09-28 | 训练安全案例（towards-safety-cases）** — 航空式安全案例：高管否决权、警报超时自动暂停

**研究与科学（2 篇）**
13. **2026-10-06 | 分享 AI 数学进展** — 722 篇手稿开源、162 篇 Lean 形式化
14. **2026-10-01 | 永恒的互补品** — "执行（机构智能）是超级智能时代的稀缺资源"

**生态与案例（13 篇）**：GPT-6 家族选型指南（10-02）、Ironclad 计算机操作（10-06）、Atlassian 合作（10-06）、小企业 SBDC（09-30）、青少年学习规划（10-07）、欧盟 agentic 采用（10-14）、Amp（10-14）、Sophos 提速 96%（10-09）、Asana 降本 76×（10-09）、SentinelOne（10-14）、Third Moment 万级智能体 36 小时（10-14）、GPT-Rosalind 学术计划（10-15）

### Anthropic（29 篇：research 18 + engineering 11 = 窗口 24 + 补录 5）

**模型与评估（3）**：1. **2026-10-07 | Claude Haiku 5.5** — 成本较 Haiku 4.5 降 75%、GDPval 超 GPT-6 Luna，5.5 家族集齐；2. **2026-10-15 | 独立评估者更新** — METR 六人获类员工权限驻场（9/9 承诺的制度化）；3. **2026-10-01 | 巴克莱规模化部署** — 年底覆盖 50% 开发者、12 万封/日邮件

**安全（7）**：4. **2026-09-29 | GLM-5.3 与先进网络能力扩散** — ExploitBench 对标 Mythos Preview 而护栏 64-100% 可绕过；5. **2026-10-09 | 非预期模型行为调查** — 四类越界行为（含向警局提交编造线索）；6. **2026-10-12 | 无需数据中心的 AI 自复制** — 15 台电视盒跑 26B，小模型年底或具备 IoT 自复制；7. **2026-10-12 | 强化蒸馏防御** — 推理 token 外泄降 10-100×；8. **2026-10-08 | 网络验证计划扩容** — 三档访问 + CyScenarioBench；9. **2026-10-08 | Anthropic 网络使命 + OSS 漏洞扫描服务**（两篇）；10. **2026-10-08 | 2026 使用政策更新**

**政策与科学（7）**：11. **2026-10-14 | 备战美国中期选举**；12. **2026-10-14 | 新加坡办公室与政府 MOU**（人均用量全球第 2）；13. **2026-10-08 | $150M 加码 Genesis Mission**；14. **2026-10-01 | Claude 形状的科学**（BootLoops 18 领域 36 稿件）；15. **2026-10-08 | 天空缺失的地图**（首张完整 UV 全天图）；16. **2026-09-30 | 机器人能做什么工作**（74% 物理任务可做但成本竞争仅 0.3%）；17. **2026-09-29 | 你想从 AI 中得到什么**（8.1 万访谈首次公开原文）

**engineering 窗口（6）**：Claude Code mods 入门（10-01）、上云指南（10-06）、agent 自动化六条规则（10-08）、Dashboards 与 Motion（10-08）、重新设计源码管理——7 人 5 个月自研 Scion 替换 git（10-13）、Claude Code 团队代码评审——六层防线+零人合并（10-15）

**补录（5 篇 claude.dev，09-22~09-28 漏网）**：Opus 5.5 用法、任务成本解剖（企业日均 $13/开发者）、effort 验证深度旋钮、Sonnet 5.5 集成变更、eval 设计与爬山自动化

### Google DeepMind（8 篇）

1. **2026-09-30 | Gemini 4 Argon 发布** — 1M token 输出、Fairwind 受限首发 + 美国政府自愿预发布流程
2. **2026-09-30 | Gemini 4 Argon 安全报告** — GCI v1（123 模型×92 基准）反驳"递归自我改进加速"：75% 代码 AI 写但研发仍近线性
3. **2026-10-13 | Gemini 4 Argon 全面开放** — 两周三连跳：订阅 + Stable API + Antigravity 入驻；AA 指数 53 平 GPT-6 Astra
4. **2026-09-30 | SynthID Bio** — 水印进入蛋白质/噬菌体基因组且不破坏功能（Nature 同步发表）
5. **2026-10-06 | EmbeddingGemma 2** — 740M 多模态统一 768 维空间、Pixel 端 Apache 2.0
6. **2026-10-14 | 新加坡端侧反诈模型** — 全程设备端推理，政府与 Google 均不可读
7. **2026-10-14 | 欧洲科学发现算力计划** — 200 名研究者 + $3M（挂靠欧委会 RAISE，遴选独立于 Google）
8. **2026-10-15 | Antigravity 加速抗菌肽发现** — 研究者驾驶科学工作台首案例，候选已进湿实验室

### Hugging Face（17 篇：窗口 15 + 补录 2）

**研究与评测（6）**：ProvenanceGuard 逐声明来源验证（09-29）、Open TTS Leaderboard（09-30）、AutoSynthData（10-02）、AstaBrief 8B 51 秒带引用科学报告（10-02）、ThinkingBox 状态验证——20 连幸存率拉开闭源 71-78% vs 开源 ~8%（10-03）、Ai2 GPU 调度——机时兑现 98%（10-09）

**模型发布（6）**：Falcon ASR 阿拉伯语方言六榜第一（10-07）、LightOnOCR-3（10-08）、LFM2.5-24B-A2B 端侧 Agent M5 Max 184 tok/s（10-13）、HiRO-ACEv2 气候仿真 1/300 成本（10-14）、Granite Switch 4.1 一个端点三模态（10-15）、FLUX.3 Image Klein（10-15）

**平台与生态（3）**：ML Intern 委托 Agent 造模型 7 个 $103（10-08）、Meta Muse Spark Open 上 HF（10-15）、Indic 预训练 2.8T token/22 语言全开源管线（10-16）

**补录（2）**：RL 环境登陆 Hub（09-28 锚点日漏收）、**NVIDIA 收购 HF**（09-03，$12.93B 官方确认——上次待办 #5 结案；HF 博客无公告帖，原文链接指向 CNN 并注明）

### DeepSeek（2 篇：窗口 1 + 补录 1）

1. **2026-10-16 | Search & Fetch API 上线** — 联网检索成模型 API 原语：$0.75/千次成功请求、失败不计费（文档静默上线，日期为第三方首报推定，文内注明）
2. **补录 2026-08-13 | DeepSeek Harness v0.1 开源** — "一切皆插件"Cordis 元框架、MIT 完整开源、追加式会话日志；四重信源核验确为 DeepSeek 自家产品

### GLM（5 篇）

1. **2026-09-30 | Anthropic 报告评估 GLM-5.3 网络能力** — 与 anthropic 侧同事件双视角互链（主会话已补双向链接）
2. **2026-10-02 | ZCode 争议媒体深度复盘** — 补齐服务端持钥加密/全量 Git 历史打包等工程细节
3. **2026-10-05 | Cursor 上线 GLM-5.3/Flash** — CursorBench 4.0 开放权重最高分 42.6%
4. **2026-10-06 | GLM-5.3 接入 Amazon Bedrock** — AWS 按调用量分成，"海外分成 10 月起确认"兑现
5. **2026-10-15 | 顶级白帽古河加盟智谱** — 23 个 Windows 漏洞获 MSRC 确认；Co-work 网安订单 1 个月超 10 亿元

### Kimi（2 篇）

1. **2026-09-23 | Kimi Code CLI v2.1.0** — 全屏 TUI + 三攻击面安全加固，但次日 v2.1.1 部分回退——24 小时收紧-回摆样本（whats-new 汇总页遗漏此细节，仅存 CLI changelog 原页）
2. **2026-10-14 | Kimi Code Desktop v1.1.0** — Linux 补齐三平台、远程控制（链接/二维码跨设备接管）、WaitFor 90 秒可打断

### Meta（3 篇）

1. **2026-10-12 | Muse Wonder** — Meta 首个前沿模型（AA Index 52/56）：Active Memory + Active Focus 机制化，Watermelon 代号兑现
2. **2026-10-15 | Muse Spark Open** — 816B/42B MoE 开放权重、$20M MaaS 许可门槛、两台 M5 Ultra Mac Studio 可跑
3. **2026-10-07 | Muse 登顶下载榜之后** — 股价月涨 20%、免费 + $20/$100 算力订阅，"信任"成核心障碍

### Community/MCP（0 篇）

博客最新仍 2026-08-22 路线图、规范最新仍 2026-07-28，窗口内无新发布。

## 更新内容

- `catalog.yaml` 从 452 篇更新为 544 篇（+92）
- `openai/research/summary.md`：192→224 条索引 + "9/29-10/16"脉络段 + 数据表 14 行；**上次待办 #1 完成**——7 篇旧文按实际文件名补入索引（219-225 行），并修正历史计数不一致
- `anthropic/research/summary.md`：38→56 条 + 9 月下旬至 10 月中旬脉络段 + 数据表 23 行
- `anthropic/engineering/summary.md`：61→72 条（含 5 篇补录标注）
- `google/deepmind/summary.md`：49→57 条 + 新增 §14 端侧 AI 与社会治理 + 数据表 18 行
- `huggingface/blog/summary.md`：45→62 条 + 窗口脉络段 + 新主题小节 + 数据表 23 行
- `glm/blog/summary.md`：23→28 条 + 新增章节 14 + 数据表 9 行
- `kimi/blog/summary.md`：10→12 条 + 新增第 7 节（含 Harvey LAB-AA v1.1 跟踪注记）
- `deepseek/news/summary.md`：7→9 条 + 新增第 8 节 + V4-Pro 口径更新（截至 10-16 定价页核验）
- `meta/summary.md`：19→22 条 + §13 双轨发布 + 数据表 14 行
- `topics/`（全量 review，10/10 文件有更新，README 复核无需改动——未新增主题文件）：
  - `safety.md`：+22 条引用 + 2 结论（蒸馏攻防公开化、开放权重安全假设重写）
  - `agent-architecture.md`：+16 条 + 2 结论（常驻个人 Agent 三家共振、云执行环境成标配）
  - `codex-vs-claude-code.md`：+18 条 + 云环境对决等新对比维度
  - `evals.md`：+15 条 + 2 结论（状态说了算、安全评估集流水线化）
  - `enterprise-ai-economics.md`：+14 条 + 1 结论（订阅单位重构为 Agent 服务）
  - `tool-use.md`：+5 条 + 1 结论（联网检索收编为平台原生工具层）
  - `context-engineering.md`：+4 条 + 1 结论（记忆从产品功能变模型机制）
  - `international.md`：+5 条 + 1 结论；`news-media.md`：+2 条 + 1 结论；`education.md`：+1 条
- 双视角互链补齐：`glm/blog/glm-5-3-anthropic-cyber-report.md` ↔ `anthropic/research/glm-5-3-and-the-spread-of-advanced-cyber-capabilities.md`（主会话执行）

## 校验结果

```text
python scripts/build_catalog.py
Wrote catalog.yaml with 544 articles
python scripts/validate.py
Validation passed: 544 articles, 577 markdown files
```

## 说明

### 信源抓取限制

1. **openai.com 403**：RSS 完整覆盖 + alignment.openai.com 直抓；12 篇次要客户案例（sullivan-cromwell、block、higgsfield、oracle、pollo-ai、legalon、radisson、jump-trading、chatham、albertsons、the-den、teaching-students）仅官方单源未入库，各文件文末已标"待补"。
2. **alignment 失准报告批量补发**：alignment.openai.com 于 10/2、10/9、10/15 批量补发 10 批历史报告（事故日期多为 3-6 月），单篇未立文件，已在失准报告文章与 summary 脉络段说明。
3. **claude.com/blog 客户端渲染**：how-comcast-booz-allen-use-claude-mythos（10 月上旬）与 build-plugins-for-claude（09-25）无正文，列待补。
4. **deepmind.google 正文截断**：标题/日期/作者取官方页头部，正文经 gigazine、llm-stats、RTE/AFP、mashinate 等每篇 ≥2 独立源交叉，文末有注；institute.deepmind.com 不可达，10 月 essay 无法确认——下次核查。
5. **Meta 官网不可达**：3 篇经 AA/Forkast/GIGAZINE/CNBC 等多源交叉；Muse Wonder 官方安全报告与 Spark Open 完整评估报告官方称"很快放出"，放出后补录。
6. **HF 镜像与 RSS 遗漏规律**：官方域名不可达经 hf-mirror 抓取；**新发现 RSS 不仅漏 Community 文章也漏部分组织文章**——后续同步以 sitemap-blog.xml 为主源。窗口内 7 篇社区帖（Carbon-A、UIBK-Embedding、Basis Global Emotions、JEV-27B-VL、Superfluid、JOSIE-2、NormalUhr）有实质内容但本轮容量所限列待补；锚点前历史漏网约 20 篇（07-01~08-30）建议下批分主题补。
7. **Kimi 渠道**：blog 停更、news 零新条目，新动态仅在 changelog；K3.1 未正式发布（野村传闻 + wccftech 代码线索，均非官方）；IPO 进展（估值 500 亿、高盛独家美资保荐）为媒体源不入库，写入跨厂商观察。
8. **GLM**：GLM-6 未发布（changelog 最新仍 08-26，网传 Leak 为第三方推测）；"Z Managed Agents (Beta)"已更名"Managed Agents (Beta)"并升为 docs 一级导航、全量开放，但无 changelog 条目与发布日期，不满足入库条件，继续跟踪；changelog 已迁移至 /cn/update/new-releases（旧 URL 404）。
9. **DeepSeek**：V4-Pro"继续服务"口径不变（10-16 定价页核验）；V4.1-Pro 未发布；"成立产品部"为组织架构新闻不入库。
10. **econ-scenarios 类日期推定**：DeepSeek Search & Fetch API 无官方日期，按第三方首报推定 10-16，文内注明。

### 跨厂商新观察

1. **中档模型反超旗舰跨厂商共振**：GPT-6.1 Sol（DeepSWE 75.22% 反超 Astra、价格 1/5）与 Claude Sonnet 5.5（TB 4.0 反超 Opus 5.5）同月发生、Haiku 5.5 成本再降 75%——"旗舰=最强"叙事在两家同时失效，价格锚加速转向每成果。
2. **网络能力扩散成为既成事实**：Anthropic 实测 GLM-5.3 对标 Mythos Preview 且护栏可 $4,400 去除（abliteration）、自复制 AI 把 ARA 时间表压到 2026 年底、OpenAI 侧 Daybreak/OSS Scanner 防御前置——"攻击能力开放可得"从假设变成需要写进威胁模型的事实；GLM 侧同事件双视角已互链。
3. **蒸馏攻防公开化且指向同一家**：OpenAI 阻断行动归因 Moonshot AI 关联者 + Anthropic 蒸馏防御论文点名智谱/Moonshot 工业级蒸馏——连续两月、两家实验室指向同一中国厂商，跨实验室协同披露可能成为常态，待 Moonshot 官方回应。
4. **受限发布与独立监督同时制度化**：Gemini 4 Argon 走 Fairwind + 美国自愿预发布、METR 六人类员工权限驻场、OpenAI 补发训练安全案例（高管否决权）——"最强模型先给可信防御者"与"外部人看多深"双双从承诺进入制度。
5. **水印双路线 + 生物水印元年**：textGrain 区域化（只打 EU、API 默认关）vs Anthropic SynthID-Text 全球化——工程能力决定合规粒度；SynthID Bio 把"生成即溯源"带入生命科学（Nature）。
6. **个人 Agent 全入口竞争白热化**：dots（云电脑+4000 应用）vs Muse（社交+硬件+免费补贴）vs Cowork 并入 Claude——分发渠道与自主性边界（dots 不碰支付）成为差异化卖点。
7. **开放权重许可定义坍缩**：Muse Spark Open $20M MaaS 门槛 vs DeepSeek V4（MIT）/GLM-5.3 Flash（Apache 2.0）零门槛；同时 NVIDIA $12.93B 收购 HF——"开放分发层的所有权"成为全行业新变量。
8. **AI 配速之争进入数据分层**：DeepMind GCI v1（75% 代码 AI 写但研发近线性、PR 仅 11.9%）与 Amodei/Altman 的"已经在加速"直接相左，与 Anthropic 配速度量构成三家竞争的新战场。
9. **Harness 三形态供给**：OpenAI 闭源产品化（Codex App Server）、Anthropic 博客方法论、DeepSeek MIT 开源完整实现——同一命题的三种供给路线。
10. **状态验证成为 Agent 评测共识**：HF ThinkingBox（20 连幸存率：闭源 71-78% vs 多数开源 ~8%）与 IBM 一致性鸿沟同期共振，可靠性成开源下一战场。

### 下次同步待办

1. **OpenAI 单源案例**：本轮 12 篇 + 上轮 12 篇共 24 篇"待补"客户案例，持续寻找第三方验证
2. **Anthropic claude.com 2 篇待补**（comcast/booz-allen、build-plugins）；HF 7 篇社区帖 + 约 20 篇锚点前历史漏网
3. **Google**：build-with-gemini-4-argon 开发者页（官方页恢复后补录）；institute.deepmind.com 10 月 essay 核查；SIMA 2（2025-11）如决定扩覆盖可补录
4. **Moonshot 对蒸馏指控的官方回应**跟踪；K3.1 发布跟踪；GLM Managed Agents / GLM-6；DeepSeek V4.1-Pro
5. **DNS 逃逸复训公告**（报告仍停留 9/25 版本）与 **METR 11 月调查结论**（上次待办 #6 延续）
6. **新主题建议（需用户确认）**：topics review 提出 ai-for-science（本窗口已成集群：claude-shaped-science、UV 天图、抗菌肽、SynthID Bio、数学披露、HiRO-ACEv2）、multilingual-global-south（Falcon ASR、Indic 语料等 3+ 篇）、open-source-ecosystem（Spark Open、NVIDIA×HF、开放权重治理横跨 5 文件）三个候选
7. Kimi 研究博客 2026-04 前旧文（Agent Swarm、WorldVQA、K2.5 等）与 kimi-work-update（06-18）评估补录
