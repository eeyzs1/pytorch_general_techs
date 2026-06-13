# 官网同步记录：2026-06-13

## 同步范围

- OpenAI Index / Blog: https://openai.com/index/
- OpenAI Research: https://openai.com/research/
- Anthropic Engineering: https://www.anthropic.com/engineering (无新文章)
- Anthropic Research: https://www.anthropic.com/research (浏览器抓取受限，未能完成全量检查)

## 新增文章（自 2026-05-29 上次同步以来）

### OpenAI

1. **2026-06-08 | Built to Benefit Everyone: Our Plan** — Sam Altman & Jakub Pachocki 发布 OpenAI 第三阶段战略蓝图：三大目标（自动化AI研究员、加速经济、给每个人个人AGI）、IPO意向信号
2. **2026-06-08 | Confidential Submission of Draft S-1 to the SEC** — OpenAI 正式向 SEC 保密提交 S-1 草案，为 IPO 铺路
3. **2026-06-08 | Introducing the OpenAI Economic Research Exchange** — 开放外部经济研究资助项目，研究 AI 经济影响
4. **2026-06-10 | Access OpenAI Models and Codex Through Your Oracle Cloud Commitment** — 与 Oracle 合作，OCI 客户可用现有云承诺购买 OpenAI 模型
5. **2026-06-11 | OpenAI to Acquire Ona** — 收购 Ona（云执行和编排平台），为 Codex 带来持久化企业 Agent 执行能力
6. **2026-06-11 | How an Astrophysicist Uses Codex to Help Simulate Black Holes** — 案例研究：天体物理学家用 Codex 推导黑洞等离子体模拟新算法
7. **2026-06-12 | New OpenAI Academy Courses for the Next Era of Work** — 发布三门企业 AI 技能课程：AI Foundations、Applied AI Foundations、Agents and Workflows

### Anthropic

无新 Engineering 文章。Research 页面有 2026-06-08 "Paving the way for agents in biology" 和 2026-06-03 "What we learned mapping AI-enabled cyber threats" 两篇新文，但由于浏览器抓取限制未能获取完整内容，留待下次同步。

## 更新内容

- `catalog.yaml` 从 60 篇更新为 86 篇。
- `openai/research/summary.md` 从 43 篇更新为 50 篇。
- `topics/` 下相关主题文件待更新。

## 校验结果

```text
python ai_info/scripts/build_catalog.py
Wrote catalog.yaml with 86 articles
python ai_info/scripts/validate.py
Validation passed: 86 articles, 117 markdown files
```

## 说明

- Anthropic Research 页面有多篇新文章（agents-in-biology, AI-enabled-cyber-threats-mitre-attack, 2028-ai-leadership, donating-open-source-petri, anthropic-institute-agenda），但因 WebFetch 无法完整抓取，本次暂不收录。
- OpenAI 的 personal-finance-chatgpt (5/15)、testing-ads-in-chatgpt (5/7)、openai-launches-deployment-company (5/11) 等若干 5 月文章在上次同步时被遗漏，本次因优先级较低暂不补齐。