# Project Glasswing: An Initial Update

- **原文链接**: [Project Glasswing: An initial update](https://www.anthropic.com/research/glasswing-initial-update)
- **作者**: Anthropic
- **发布日期**: 2026-05-22
- **检索日期**: 2026-06-07
- **标签**: #Security #Vulnerability #CyberDefense #Mythos #OpenSource

## 核心观点

Project Glasswing 启动一个月后，约 50 个合作伙伴使用 Claude Mythos Preview 在关键软件中发现了超过一万个高危/严重漏洞。软件安全的瓶颈已经从"找漏洞"变成了"修漏洞"。

## 关键数据

### 合作伙伴成果
- 总计发现 **10,000+ 高危/严重漏洞**
- Cloudflare：发现 2,000 个 bug（400 个高危/严重），误报率优于人类测试者
- Mozilla：在 Firefox 150 中发现并修复 **271 个漏洞**（比上版本多 10 倍）
- Palo Alto Networks：补丁发布量增加 **5 倍**
- Microsoft：补丁量"将持续增长一段时间"
- Oracle：漏洞发现和修复速度提升 **数倍**
- 某合作银行：阻止了 **150 万美元**的欺诈性电汇

### 开源软件扫描
- 扫描了 1,000+ 开源项目
- 发现 6,202 个高危/严重漏洞（估算），23,019 个总计
- 经人工审核的 1,752 个高危漏洞中：**90.6% 为真阳性**，62.4% 确认为高危/严重
- 预计最终将发现 **3,900+ 高危/严重漏洞**

### 案例：wolfSSL
- 发现 CVE-2026-5194，可伪造证书
- 攻击者可架设伪造的银行/邮箱网站，对终端用户完全逼真

### 外部评估
- 英国 AISI：Mythos Preview 是首个**端到端**通关两个网络靶场的模型
- XBOW：Mythos Preview 是"对所有现有模型的重大提升"，"精度前所未有"
- ExploitBench / ExploitGym：Mythos Preview 表现最强

## 修复瓶颈

- 高危/严重漏洞平均需要 **2 周**才能打补丁
- 开源维护者已被 AI 生成的 bug 报告淹没
- 部分维护者要求 Anthropic **减慢**披露速度

## 发布工具

- **Claude Security** 公开测试版（Claude Enterprise），3 周内修补了 2,100+ 漏洞
- **Cyber Verification Program**：允许安全专业人员绕过某些防滥用保护
- 开源了技能、扫描 harness、威胁模型构建器

## 关键洞察

1. **找漏洞已不是瓶颈**——修复和部署补丁的速度才是
2. Mythos 级模型将很快广泛可用，补丁延迟窗口是最大风险
3. 开源生态正面临"AI 生成 bug 报告洪水"的冲击
4. 防御方需要缩短补丁周期、强化网络基线配置、执行 MFA