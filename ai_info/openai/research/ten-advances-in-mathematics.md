# 数学与理论计算机科学的十项进展

- **原文链接**: [Ten advances in mathematics and theoretical computer science](https://openai.com/index/ten-advances-in-mathematics/)
- **作者**: OpenAI
- **发布日期**: 2026-08-01
- **检索日期**: 2026-08-08
- **标签**: #数学 #Astra #Lean形式化 #理论计算机科学 #前沿模型

## 核心观点

OpenAI 公布了由内部版本 Astra 模型在数学和理论计算机科学领域取得的十项新成果，涵盖高维球填充、编码理论、群论、算术电路复杂性、量子复杂度、格密码学和极值组合学等长期悬而未决的开放问题。这些问题大多已停滞十年以上，部分甚至数十年无进展。

所有证明均以 Lean 4 形式化证书发布，确保结果的可验证性。OpenAI 强调对数学界的责任——AI 生成的证明应如实标注归属，并已将论文、Lean 证书和模型推理过程叙述全部公开发布。

## 关键发现 / 关键技术

### 1. 十项核心成果
- 高维球填充：Cohn–Elkies 阈值以上的新密度上界
- 二进制与球面码：任意给定最小距离下二进制码最大规模的指数级改进
- 非 sofic 群：构造证明非 sofic 群的存在性
- Connes 刚性猜想：否定某类群由其 von Neumann 代数唯一确定
- 算术电路复杂性：永久式计算的 n⁴/log n 级公式下界
- 量子并行重复：一般双人量子博弈的指数级并行重复定理
- 最近向量问题：格最近向量问题的多项式因子逼近硬度
- Ehrhart 体积猜想：各维度下凸体最大体积的确定
- 多色 Ramsey 数：多色三角形 Ramsey 数的超指数下界，解决 Erdős 问题 183
- 极值图论：紧致性与退化性猜想的结果，解决 Erdős 问题 146 和 180

### 2. 形式化与成本
- 全部证明已形式化为 Lean 4 证书并开源
- 求解这些问题的总 token 成本按 Sol API 费率约 2,000 美元
- 论文由人类与同一模型协作撰写

## 实践意义

这标志着 AI 从"辅助工具"进入"研究合作者"阶段。Lean 形式化证书确保了结果的可验证性，为数学界提供了可审计的新思路来源。对格密码学硬度的研究直接影响后量子密码学的设计评估，对编码理论的改进可能影响通信系统。

## 跨厂商对比

- 与 [模型否定离散几何猜想](model-disproves-discrete-geometry-conjecture.md) 互补：本文是同一研究线的延续，五月公布的 Erdős 单位距离猜想反证已引发后续研究，本文扩展到十个领域
- 与 [学术研究者版 ChatGPT](chatgpt-for-academic-researchers.md) 互补：该计划为 10 万科研人员提供免费模型访问，本文展示了模型在前沿数学研究中的实际能力
- 与 [AlphaEvolve](../../google/deepmind/alphaevolve.md) 对比：Google 的 AlphaEvolve 通过进化算法发现算法与数学构造，OpenAI 的 Astra 则直接通过推理生成完整证明并形式化

## 资源

- 论文：https://cdn.openai.com/pdf/ten-proofs-oai.pdf
- 推理过程叙述：https://cdn.openai.com/pdf/reasoning-walkthroughs.pdf
- Lean 证书代码：https://github.com/openai/ten-proofs
