# How an Astrophysicist Uses Codex to Help Simulate Black Holes

- **原文链接**: [How an astrophysicist uses Codex to help simulate black holes](https://openai.com/index/using-codex-to-simulate-black-holes/)
- **作者**: OpenAI
- **发布日期**: 2026-06-11
- **检索日期**: 2026-06-13
- **标签**: #Codex #天体物理 #科学计算 #案例研究 #应用AI

## 核心观点

亚利桑那大学天体物理学家 Chi-kwan Chan（Event Horizon Telescope 合作组成员）使用 Codex 推导和测试模拟黑洞周围等离子体的新算法。这项工作的核心挑战是：模拟黑洞附近带电粒子运动时，标准方法需要跟踪每个粒子的微小螺旋运动，导致即使世界最快超算也大部分时间耗在微小步长计算上。用 Codex 生成候选算法并测试可行性，有望解锁此前不可能的黑洞模拟。

## 关键更新

### 科学背景
- 黑洞附近等离子体在某些区域极度稀薄，粒子几乎不碰撞，而是沿磁力线螺旋运动
- 标准模拟需以极小时同步长跟踪数万亿个电子和离子
- 这个问题数十年来限制了黑洞等离子体模拟的真实度

### Codex 的角色
- Chan 假设新的数学变换可以绕开直接跟踪每个螺旋
- **Codex 生成候选算法并通过已知解测试**——多数不成立，但可测试就意味着可推进
- 关键优势：Codex 生成的数值方案是**可检查、可测试、可物理理解**的，而非黑箱输出

### 方法论的深层意义
- Chan 认为"科学可能是当今 AI 系统的最佳应用场景之一，因为科学思想可以被严格检验"
- "我们不会因为一个想法来自爱因斯坦、来自聪明学生或来自 AI 模型就接受它——我们只在反复检验后接受它"
- 成功的新算法将允许科学家模拟黑洞周围的数万亿个粒子

## 关键洞察

1. 这是一个"AI 辅助科学研究"而非"AI 替代科学家"的典型案例——Codex 探索解空间，人类判断可行性并做物理验证
2. 科学领域特别适合 AI 应用，因为"可测试性"天然解决了 AI 的可靠性和幻觉问题
3. Chan 是 EHT 合作组成员（2019 年发布了首张黑洞图像），其工作凸显 Codex 已进入前沿科学研究
4. 对 "Codex 非开发者使用增长 3 倍"的数据点提供了具体实例

## 相关文章

- [Codex for Every Role, Tool, and Workflow](codex-for-every-role-tool-workflow.md)
- [Introducing Codex](introducing-codex.md)
- [An OpenAI Model Has Disproved a Central Conjecture in Discrete Geometry](model-disproves-discrete-geometry-conjecture.md)