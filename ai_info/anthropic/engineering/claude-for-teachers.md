# Claude for Teachers 面向美国 K-12 学校与学区正式开放（Claude for Teachers, now available for U.S. K-12 schools and districts）

- **原文链接**: [Claude for Teachers, now available for U.S. K-12 schools and districts](https://claude.com/blog/claude-for-teachers-now-available-for-schools-and-districts)
- **作者**: Anthropic
- **发布日期**: 2026-08-28
- **检索日期**: 2026-09-09
- **标签**: #Education #K12 #EnterpriseOffering #Privacy

## 核心观点

继 7 月面向经过验证的美国 K-12 教师个人开放（免费高级能力 + 基于学习科学的教学技能 + 50 州学术标准直连）之后，Claude for Teachers 现以免费 Enterprise 形式向学校和学区正式开放。学校/学区管理员完成验证、接受 K-12 条款与学生数据隐私协议、接入邮件域名与 SSO 后，即可把教师与员工纳入一个集中管理的组织。

产品策略的核心是把"教师个体试用"升级为"学区级部署"：企业功能（SSO、基于角色的访问控制、域名认领）免费提供，用量上限与个人版一致、默认关闭超额计费；隐私上以一套 FERPA 对齐承诺和 K-12 数据处理协议覆盖整个组织，Claude for Teachers 数据不用于模型训练。

## 关键发现 / 关键技术

### 1. 学区级管理与企业功能
- 管理员添加/移除员工、设置策略、查看各校采纳情况；通过 domain capture，已在学校/学区域名下完成验证的教师自动并入集中管理账户。
- 用量限额对齐个人 Claude for Teachers 账户且零成本；除非管理员主动开启，超额计费默认关闭。

### 2. 隐私与合规框架
- 学区/学校持有统一的 K-12 Terms 与 Data Processing Agreement，一套 FERPA 对齐承诺适用于全组织。
- 学生信息受 K-12 DPA 保护；Claude for Teachers 数据不用于模型训练。

### 3. 开学季新资源
- 与 Learning Commons 共同开发的两个新教学技能：Lesson preparation（帮教师为课时关键节点做准备）、Check for understanding（构建短的、对齐标准的理解检测，上线时支持数学）。
- 既有技能改进：学生材料无障碍升级、课程规划技能内嵌备课步骤。
- 更新版 Claude for K-12 Academy：面向教师/教练/学区团队的免费 AI 素养课程、指南与课堂工作流。
- 教学技能作为公共品发布在 GitHub（anthropics/k12-teacher-skills）；今秋将在 Detroit Public Schools Community District 开展教师福祉与教学实践影响的试点评估。2027-06-30 前注册的合格组织可享整年免费。

## 实践意义

这是"垂直人群 + 企业化管理 + 免费定价"组合的教育样板：对学区 IT 而言，SSO/RBAC/域名治理与不训练承诺直接解决采购阻力；对 Anthropic 而言，教师入口先行（而非学生）规避了未成年人产品的核心争议，同时通过公开教学技能构筑生态。对教育科技公司，值得注意的信号是：差异化越来越依赖"技能 + 标准映射 + 治理"，而非模型本身。

## 跨厂商对比

- 与 [ChatGPT for teens](../../openai/research/chatgpt-for-teens.md) 对比：OpenAI 从学生年龄段准入切入，Anthropic 走"教师优先、学区企业化治理"路线，两者对"AI 进 K-12 的第一入口"给出了不同答案。
- 与 [Learn teach ChatGPT work Codex](../../openai/research/learn-teach-chatgpt-work-codex.md) 互补：两厂商都在做教育场景的 AI 素养内容（OpenAI 的教学课程 vs Claude for K-12 Academy），可对照其课程设计取向。

## 资源

- 官方文章：https://claude.com/blog/claude-for-teachers-now-available-for-schools-and-districts
- 相关产品：https://claude.com/solutions/teachers；https://github.com/anthropics/k12-teacher-skills
