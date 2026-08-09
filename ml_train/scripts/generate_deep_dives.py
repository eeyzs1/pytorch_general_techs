#!/usr/bin/env python3
"""Vertical deep-dive educational notebooks."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NB_META = {
    "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
    "language_info": {"name": "python", "version": "3.10.0"},
}


def md(text: str) -> dict:
    lines = text.strip("\n").split("\n")
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": [ln + "\n" for ln in lines[:-1]] + ([lines[-1] + "\n"] if lines else []),
    }


def code(text: str) -> dict:
    lines = text.strip("\n").split("\n")
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [ln + "\n" for ln in lines[:-1]] + ([lines[-1] + "\n"] if lines else []),
    }


def write_nb(rel: str, cells: list[dict]) -> None:
    path = ROOT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    nb = {"cells": cells, "metadata": NB_META, "nbformat": 4, "nbformat_minor": 4}
    path.write_text(json.dumps(nb, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print("wrote", rel)


def thinking(section: str, *qs: str) -> dict:
    body = "\n".join(f"{i}. {q}" for i, q in enumerate(qs, 1))
    return md(
        f"""## 课后思考题

{body}

---
> 本节是{section}的垂直深挖。建议对照真实训练日志/线上指标复现关键实验，而不是只跑通玩具代码。"""
    )


def build() -> None:
    # ------------------------------------------------------------------
    # DoReMi
    # ------------------------------------------------------------------
    write_nb(
        "01_data_engineering/09_doremi_data_mixture.ipynb",
        [
            md(
                """# 1.9 DoReMi 数据配比深挖

> 🕐 预估学习时间：40分钟

DoReMi（Domain Reweighting with Minimax Optimization）用代理模型学领域权重，再用于正式预训练，避免手调配比。本节实现核心迭代：proxy 训练 → 领域 excess loss → 更新采样分布。

深挖点：
- 均匀配比 vs 经验配比的失败模式
- Group DRO / minimax 更新
- 代理模型规模与迁移误差
- 与数据退火、课程学习的组合"""
            ),
            md(
                """## 1. 问题设定

K 个领域，采样分布 α。目标不是平均 loss 最低，而是降低**最差领域**的 excess loss（相对参考模型）。"""
            ),
            code(
                """import torch
import torch.nn as nn
import torch.nn.functional as F

torch.manual_seed(0)

DOMAINS = ['web', 'code', 'math', 'books']
K = len(DOMAINS)


class DomainLM(nn.Module):
    def __init__(self, d=32, vocab=40):
        super().__init__()
        self.embed = nn.Embedding(vocab, d)
        self.fc = nn.Linear(d, vocab)

    def forward(self, x):
        return self.fc(self.embed(x).mean(1))


def domain_batch(domain_id, n=64, t=8, vocab=40):
    # each domain has a biased token preference
    x = torch.randint(0, vocab, (n, t))
    x[:, 0] = domain_id * 7 % vocab
    y = (x[:, 0] + domain_id + 1) % vocab
    return x, y


def eval_domain_losses(model, steps=5):
    model.eval()
    losses = []
    with torch.no_grad():
        for k in range(K):
            total = 0.0
            for _ in range(steps):
                x, y = domain_batch(k)
                total += F.cross_entropy(model(x), y).item()
            losses.append(total / steps)
    model.train()
    return torch.tensor(losses)


ref = DomainLM()
# reference: lightly trained on uniform mix
opt = torch.optim.Adam(ref.parameters(), lr=1e-2)
for _ in range(30):
    k = torch.randint(0, K, (1,)).item()
    x, y = domain_batch(k)
    loss = F.cross_entropy(ref(x), y)
    opt.zero_grad(); loss.backward(); opt.step()
ref_losses = eval_domain_losses(ref)
print('=== Reference domain losses ===')
for d, L in zip(DOMAINS, ref_losses.tolist()):
    print(f'{d}: {L:.4f}')
print('Key: Excess loss = proxy_loss(domain) - ref_loss(domain).')"""
            ),
            md(
                """## 2. DoReMi 主循环（教学版）

1. 用当前 α 采样训练 proxy  
2. 估计各领域 excess loss  
3. `α ← normalize(α · exp(η · excess))`（指数梯度 / mirror descent）"""
            ),
            code(
                """def train_proxy(alpha, steps=40, lr=1e-2):
    model = DomainLM()
    opt = torch.optim.Adam(model.parameters(), lr=lr)
    hist = []
    for _ in range(steps):
        k = torch.multinomial(alpha, 1).item()
        x, y = domain_batch(k)
        loss = F.cross_entropy(model(x), y)
        opt.zero_grad(); loss.backward(); opt.step()
        hist.append(loss.item())
    return model, hist


def doremi(iters=6, eta=1.0):
    alpha = torch.ones(K) / K
    log = []
    for t in range(iters):
        proxy, _ = train_proxy(alpha)
        proxy_losses = eval_domain_losses(proxy)
        excess = (proxy_losses - ref_losses).clamp_min(0)
        # mirror descent update
        alpha = alpha * torch.exp(eta * excess)
        alpha = alpha / alpha.sum()
        log.append((alpha.clone(), excess.clone(), proxy_losses.clone()))
        print(f'iter={t} alpha={[round(a,3) for a in alpha.tolist()]} '
              f'excess={[round(e,3) for e in excess.tolist()]}')
    return alpha, log


print('=== DoReMi Optimization ===')
alpha_star, logs = doremi()
print(f'final alpha={alpha_star.tolist()}')
print('Key: Domains that remain hard get higher sampling weight automatically.')"""
            ),
            md(
                """## 3. 均匀配比对照

若正式训练仍用均匀 α，弱势领域会拖后腿；用 α* 重采样可降低 worst-domain loss。"""
            ),
            code(
                """def train_main(alpha, steps=80):
    model = DomainLM()
    opt = torch.optim.Adam(model.parameters(), lr=1e-2)
    for _ in range(steps):
        k = torch.multinomial(alpha, 1).item()
        x, y = domain_batch(k)
        loss = F.cross_entropy(model(x), y)
        opt.zero_grad(); loss.backward(); opt.step()
    return eval_domain_losses(model)


uniform = torch.ones(K) / K
L_uni = train_main(uniform)
L_dr = train_main(alpha_star.detach())
print('=== Main-model domain losses ===')
print(f'{\"domain\":<8} {\"uniform\":>10} {\"doremi\":>10}')
for d, a, b in zip(DOMAINS, L_uni.tolist(), L_dr.tolist()):
    print(f'{d:<8} {a:>10.4f} {b:>10.4f}')
print(f'worst uniform={L_uni.max():.4f} doremi={L_dr.max():.4f}')
print('Key: Optimize for worst-domain excess, not only average CE.')"""
            ),
            md(
                """## 4. 工程陷阱

| 陷阱 | 表现 | 缓解 |
|------|------|------|
| proxy 太小 | α* 不可迁移 | proxy ≥ 主模型 1/10 量级试错 |
| 领域定义糊 | 权重抖动 | 清晰 taxonomy + 稳定分类器 |
| 过拟合 excess | 刷某一域 | 温度/截断、正则到先验 α0 |
| 忽略质量 | 垃圾域权重大 | 先质量过滤再 DoReMi |"""
            ),
            code(
                """# Regularize toward prior alpha0
alpha0 = torch.tensor([0.4, 0.2, 0.2, 0.2])
alpha_reg = 0.7 * alpha_star.detach() + 0.3 * alpha0
alpha_reg = alpha_reg / alpha_reg.sum()
print('=== Prior-regularized alpha ===')
print(list(zip(DOMAINS, alpha_reg.tolist())))
print('Key: Blend learned weights with human prior for production stability.')"""
            ),
            thinking(
                "DoReMi 数据配比",
                "excess loss 相对参考模型，参考模型应如何训练才公平？",
                "多语言 + 多领域同时配比，α 维度爆炸时怎么聚类？",
                "DoReMi 与中期训练/数据退火如何衔接？",
                "线上能力偏科时，能否用评测集反向更新 α？风险是什么？",
            ),
        ],
    )

    # ------------------------------------------------------------------
    # Context parallelism
    # ------------------------------------------------------------------
    write_nb(
        "05_distributed_training/06_context_parallelism.ipynb",
        [
            md(
                """# 5.6 上下文并行深挖 (Ulysses / Ring Attention)

> 🕐 预估学习时间：40分钟

序列并行/上下文并行把超长序列切到多卡：DeepSpeed Ulysses（all-to-all 头维交换）与 Ring Attention（块状 KV 环形传递）是两条主路。

深挖点：
- 激活切分维度对比
- Ulysses all-to-all 通信量
- Ring Attention 正确性模拟
- 与 TP/PP/CP 三维组合"""
            ),
            md(
                """## 1. 为什么需要上下文并行？

TP 切隐藏维，PP 切层，都救不了 **激活 ∝ batch×seq×hidden** 在超长 seq 上的爆炸。CP 沿序列维切分。"""
            ),
            code(
                """import torch
import torch.nn.functional as F
import math

torch.manual_seed(0)


def activation_bytes(batch, seq, hidden, dtype_bytes=2, layers=1):
    # rough: activations per layer ~ 2 * B * S * H (residual+mlp peak simplified)
    return batch * seq * hidden * dtype_bytes * 2 * layers


print('=== Activation Memory vs Seq ===')
for s in [4_096, 32_768, 128_000, 1_000_000]:
    single = activation_bytes(1, s, 4096, layers=4) / (1024**3)
    cp8 = activation_bytes(1, s // 8, 4096, layers=4) / (1024**3)
    print(f'seq={s:>8}: single~{single:.2f}GB  CP=8 ~{cp8:.2f}GB/rank')
print('Key: CP turns sequence-length memory into a near-linear scale-out knob.')"""
            ),
            md(
                """## 2. Ulysses：序列分片 ↔ 头分片 all-to-all

1. 每卡持有 seq/P 段、全部头  
2. all-to-all 后变为持有全部 seq、头/P  
3. 本地算注意力  
4. all-to-all 换回  

通信量与 P 相关但避免 Ring 的多步延迟积累。"""
            ),
            code(
                """def ulysses_comm_bytes(batch, seq, heads, d_head, P, dtype=2):
    # two all-to-alls of Q/K/V-sized (approx 3) + output (1) => ~4 transfers of B*S*H
    H = heads * d_head
    per = batch * seq * H * dtype
    # each all-to-all moves (P-1)/P of local shard volume from each rank; total network ~ per * (P-1)/P * 2 * 2
    return 2 * 2 * per * (P - 1) / P


print('=== Ulysses Comm Volume ===')
for P in [2, 4, 8]:
    b = ulysses_comm_bytes(1, 65536, 32, 128, P)
    print(f'P={P}: ~{b/1024**3:.2f} GB total network (toy accounting)')
print('Key: Ulysses prefers fat all-to-all links inside a node/NVLink domain.')"""
            ),
            md(
                """## 3. Ring Attention：KV 块绕环传递

每卡固定拥有 Q 的一段；KV 块在环上轮转，局部累加 online softmax 统计量，数学上等价全注意力。"""
            ),
            code(
                """def ring_attention(Q, K, V, ranks=4):
    '''Q,K,V: (B,H,S,D) split along S into ranks chunks; compute exact attn.'''
    B, H, S, D = Q.shape
    assert S % ranks == 0
    chunk = S // ranks
    outs = []
    for r in range(ranks):
        qs = Q[:, :, r * chunk:(r + 1) * chunk]
        # online softmax over circulating KV
        m = torch.full((B, H, chunk, 1), -1e9)
        l = torch.zeros(B, H, chunk, 1)
        o = torch.zeros(B, H, chunk, D)
        for step in range(ranks):
            src = (r + step) % ranks
            ks = K[:, :, src * chunk:(src + 1) * chunk]
            vs = V[:, :, src * chunk:(src + 1) * chunk]
            s = qs @ ks.transpose(-1, -2) / math.sqrt(D)
            m2 = torch.maximum(m, s.max(-1, keepdim=True).values)
            alpha = torch.exp(m - m2)
            p = torch.exp(s - m2)
            l = l * alpha + p.sum(-1, keepdim=True)
            o = o * alpha + p @ vs
            m = m2
        outs.append(o / l)
    return torch.cat(outs, dim=2)


B, H, S, D = 1, 2, 64, 16
Q = torch.randn(B, H, S, D)
K = torch.randn(B, H, S, D)
V = torch.randn(B, H, S, D)
ref = torch.softmax(Q @ K.transpose(-1, -2) / math.sqrt(D), -1) @ V
ring = ring_attention(Q, K, V, ranks=4)
err = (ref - ring).abs().max().item()
print('=== Ring Attention Equivalence ===')
print(f'max err={err:.2e}')
print('Key: Ring Attention is exact; latency grows with ring steps (~P).')"""
            ),
            md(
                """## 4. 组合策略

| 维度 | 切什么 | 适合 |
|------|-------|------|
| TP | 头/MLP 宽 | 节点内 |
| PP | 层 | 节点间流水 |
| CP/Ulysses | 序列 | 超长上下文 |
| DP/FSDP | 数据/参数状态 | 吞吐 |

经验：长上下文预训练常 `TP × CP` 同节点，`PP` 跨节点；推理可用环形 KV 传输或状态缓存。"""
            ),
            code(
                """def pick_parallel(seq_len, node_gpus=8):
    if seq_len <= 8192:
        return {'TP': min(8, node_gpus), 'CP': 1, 'PP': 1}
    if seq_len <= 65536:
        return {'TP': 4, 'CP': 2, 'PP': 1}
    return {'TP': 2, 'CP': 4, 'PP': 2}


print('=== Heuristic Parallel Plans ===')
for s in [4096, 32768, 128000]:
    print(s, pick_parallel(s))
print('Key: Raise CP before PP when activation memory is the binding constraint.')"""
            ),
            thinking(
                "上下文并行",
                "Ulysses 与 Ring 在跨节点 InfiniBand 上谁更怕延迟？",
                "Causal mask 在 ring 步进中如何正确处理？",
                "CP 与梯度检查点同时开时，通信-重计算如何重叠？",
                "推理期 KV 已分片时，CP 训练出的模型如何服务？",
            ),
        ],
    )

    # ------------------------------------------------------------------
    # MoE at scale
    # ------------------------------------------------------------------
    write_nb(
        "03_architecture_design/12_moe_training_at_scale.ipynb",
        [
            md(
                """# 3.12 MoE 规模化训练深挖

> 🕐 预估学习时间：45分钟

稀疏 MoE 的难点不在“多几个 FFN”，而在路由坍塌、专家负载不均、EP 通信与容量因子。本节深挖工业训练技巧。

深挖点：
- 辅助损失 vs 无辅助损失偏置
- capacity factor 与 token drop
- Expert Parallel 通信量
- 共享专家 + 细粒度专家"""
            ),
            md(
                """## 1. 路由坍塌演示

无约束时，路由器可能把几乎所有 token 送给少数专家。"""
            ),
            code(
                """import torch
import torch.nn as nn
import torch.nn.functional as F

torch.manual_seed(0)


class Router(nn.Module):
    def __init__(self, d=32, n_experts=8):
        super().__init__()
        self.gate = nn.Linear(d, n_experts, bias=False)
        self.n_experts = n_experts

    def forward(self, x, bias=None):
        logits = self.gate(x)
        if bias is not None:
            logits = logits + bias
        return torch.softmax(logits, dim=-1)


def usage_entropy(probs):
    u = probs.mean(0)
    return float(-(u * (u + 1e-12).log()).sum()), u


x = torch.randn(2000, 32)
# pathological init: large first row
router = Router()
with torch.no_grad():
    router.gate.weight.zero_()
    router.gate.weight[0] += 5

probs = router(x)
ent, usage = usage_entropy(probs)
print('=== Collapse without balancing ===')
print('usage', usage.tolist())
print(f'entropy={ent:.3f} (max={torch.log(torch.tensor(8.0)):.3f})')
print('Key: Collapsed routing wastes capacity and hurts quality.')"""
            ),
            md(
                """## 2. 负载均衡：辅助损失与偏置反馈

- **Switch/GShard 辅助损失**：`N · Σ f_i · P_i`  
- **无辅助损失（DeepSeek 风格直觉）**：对专家加可学习/反馈偏置，压低过热专家"""
            ),
            code(
                """def aux_load_balance(probs, topk_idx, n_experts):
    # f: fraction of tokens assigned; P: mean router prob
    N = n_experts
    f = torch.zeros(N)
    for i in topk_idx.view(-1):
        f[i] += 1
    f = f / f.sum()
    P = probs.mean(0)
    return N * (f * P).sum(), f, P


def train_with_balance(use_bias_feedback=False, steps=60):
    r = Router(n_experts=8)
    experts = nn.ModuleList([nn.Linear(32, 32) for _ in range(8)])
    opt = torch.optim.Adam(list(r.parameters()) + list(experts.parameters()), lr=1e-2)
    bias = torch.zeros(8)
    hist = []
    for step in range(steps):
        x = torch.randn(256, 32)
        probs = r(x, bias if use_bias_feedback else None)
        topv, topi = probs.topk(2, dim=-1)
        # dispatch weighted expert outs
        out = 0
        for k in range(2):
            w = topv[:, k:k+1]
            # gather expert outputs (loop for clarity)
            eo = torch.stack([experts[i](x[t:t+1]) for t, i in enumerate(topi[:, k])], 0).squeeze(1)
            out = out + w * eo
        task = (out - x).pow(2).mean()  # reconstruct
        aux, f, P = aux_load_balance(probs, topi, 8)
        loss = task + (0.0 if use_bias_feedback else 0.01 * aux)
        opt.zero_grad(); loss.backward(); opt.step()
        if use_bias_feedback:
            # push down hot experts
            with torch.no_grad():
                bias -= 0.1 * (f - 1.0 / 8)
        if step % 20 == 0 or step == steps - 1:
            ent, usage = usage_entropy(probs.detach())
            hist.append((step, ent, usage.clone()))
            print(f'step={step} mode={"bias" if use_bias_feedback else "aux"} ent={ent:.3f} usage={usage.tolist()}')
    return hist


print('=== Aux-loss balancing ===')
train_with_balance(False)
print('=== Bias-feedback balancing ===')
train_with_balance(True)
print('Key: Either penalize imbalance or continuously nudge expert biases.')"""
            ),
            md(
                """## 3. Capacity factor 与 drop

每专家最多处理 `capacity = CF · tokens · topk / experts`。超出则 drop 或改道。CF 太小伤质量，太大伤效率。"""
            ),
            code(
                """def capacity_and_drops(n_tokens=1024, n_experts=8, topk=2, cf=1.25):
    cap = int(cf * n_tokens * topk / n_experts)
    # simulate random assignments
    assign = torch.randint(0, n_experts, (n_tokens, topk))
    loads = torch.zeros(n_experts)
    drops = 0
    for t in range(n_tokens):
        for k in range(topk):
            e = int(assign[t, k])
            if loads[e] < cap:
                loads[e] += 1
            else:
                drops += 1
    return cap, loads, drops / (n_tokens * topk)


print('=== Capacity Factor Sweep ===')
for cf in [1.0, 1.25, 2.0]:
    cap, loads, drop_rate = capacity_and_drops(cf=cf)
    print(f'CF={cf:.2f} cap={cap} drop_rate={drop_rate:.3f} load_std={loads.std().item():.2f}')
print('Key: Tune CF on drop_rate vs MFU; monitor per-expert occupancy histograms.')"""
            ),
            md(
                """## 4. Expert Parallel 通信

Token 按专家 ID all-to-all 到专家所在 rank，算完再返回。通信 ∝ 被路由激活量，不是全参数量。"""
            ),
            code(
                """def ep_comm_bytes(n_tokens, hidden, topk=2, dtype=2, P=8):
    # each token sends topk hidden states out and back
    return 2 * n_tokens * topk * hidden * dtype * (P - 1) / P


print('=== EP Communication ===')
for P in [8, 16, 64]:
    b = ep_comm_bytes(8192, 2048, P=P)
    print(f'EP={P}: ~{b/1024**3:.3f} GB/step (toy)')
print('Key: MoE scales compute faster than dense, but EP all-to-all becomes the new bottleneck.')"""
            ),
            thinking(
                "MoE 规模化训练",
                "细粒度专家（更多更小）如何改变 CF 与通信形态？",
                "共享专家解决了什么冗余问题？代价是什么？",
                "推理时 expert packing / 动态batch 如何避免气泡？",
                "路由日志如何用于数据诊断（某域总进某专家）？",
            ),
        ],
    )

    # ------------------------------------------------------------------
    # Reward hacking
    # ------------------------------------------------------------------
    write_nb(
        "07_alignment_training/07_reward_hacking.ipynb",
        [
            md(
                """# 7.7 奖励黑客与过度优化深挖

> 🕐 预估学习时间：40分钟

当优化的是奖励模型而非真偏好时，策略会钻空子：空话加长、谄媚、格式刷分、不安全但高分。本节用可控玩具复现 Goodhart 效应与缓解手段。

深挖点：
- 奖励模型盲区 → 策略利用
- KL 约束与早期停止
- 长度偏见
- 集成奖励 / 对抗挖掘"""
            ),
            md(
                """## 1. Goodhart：代理指标被刷爆

真偏好看“正确性”，奖励模型误把“长且自信”当好。"""
            ),
            code(
                """import torch
import torch.nn as nn
import torch.nn.functional as F

torch.manual_seed(0)


def true_pref(features):
    # features: [correctness, length, confidence]
    return 2.0 * features[:, 0] - 0.1 * features[:, 1]


def proxy_rm(features):
    # mistakenly loves length + confidence
    return 0.5 * features[:, 0] + 0.8 * features[:, 1] + 0.5 * features[:, 2]


# policy samples features via parameters
class Policy(nn.Module):
    def __init__(self):
        super().__init__()
        self.logit = nn.Parameter(torch.zeros(3))  # bernoulli logits for traits

    def sample(self, n=64):
        p = torch.sigmoid(self.logit)
        feats = torch.bernoulli(p.expand(n, -1))
        # length continuous-ish
        feats = feats.clone()
        feats[:, 1] = torch.sigmoid(self.logit[1]) * (1 + 0.1 * torch.randn(n))
        return feats, p


pol = Policy()
opt = torch.optim.Adam(pol.parameters(), lr=0.2)
print('=== Optimize Proxy RM ===')
for step in range(40):
    feats, p = pol.sample()
    reward = proxy_rm(feats).mean()
    # maximize reward
    loss = -reward
    opt.zero_grad(); loss.backward(); opt.step()
    if step % 10 == 0 or step == 39:
        with torch.no_grad():
            f, _ = pol.sample(200)
            print(f'step={step} proxy={proxy_rm(f).mean():.3f} true={true_pref(f).mean():.3f} '
                  f'p={torch.sigmoid(pol.logit).tolist()}')
print('Key: Proxy goes up while true preference collapses — classic reward hacking.')"""
            ),
            md(
                """## 2. KL / 距离约束缓解

相对参考策略加 KL 惩罚，限制跑出分布太远。"""
            ),
            code(
                """ref_logit = torch.zeros(3)
pol2 = Policy()
opt2 = torch.optim.Adam(pol2.parameters(), lr=0.2)
print('=== Proxy + KL to reference ===')
for step in range(40):
    feats, p = pol2.sample()
    reward = proxy_rm(feats).mean()
    pref = torch.sigmoid(pol2.logit)
    pref_ref = torch.sigmoid(ref_logit)
    kl = (pref * (pref.clamp_min(1e-6).log() - pref_ref.clamp_min(1e-6).log())
          + (1 - pref) * ((1 - pref).clamp_min(1e-6).log() - (1 - pref_ref).clamp_min(1e-6).log())).sum()
    loss = -reward + 0.5 * kl
    opt2.zero_grad(); loss.backward(); opt2.step()
    if step % 10 == 0 or step == 39:
        with torch.no_grad():
            f, _ = pol2.sample(200)
            print(f'step={step} proxy={proxy_rm(f).mean():.3f} true={true_pref(f).mean():.3f} kl={kl.item():.3f}')
print('Key: KL buys safety margin but does not fix a systematically wrong RM.')"""
            ),
            md(
                """## 3. 长度偏见校正

奖励减去长度基线或使用长度归一化（SimPO 风格直觉）。"""
            ),
            code(
                """def length_normalized_rm(features):
    return proxy_rm(features) - 0.8 * features[:, 1]


pol3 = Policy()
opt3 = torch.optim.Adam(pol3.parameters(), lr=0.2)
print('=== Length-normalized proxy ===')
for step in range(40):
    feats, _ = pol3.sample()
    loss = -length_normalized_rm(feats).mean()
    opt3.zero_grad(); loss.backward(); opt3.step()
    if step % 10 == 0 or step == 39:
        f, _ = pol3.sample(200)
        print(f'step={step} true={true_pref(f).mean():.3f} mean_len={f[:,1].mean():.3f}')
print('Key: Explicitly debias known RM failure modes before policy optimization.')"""
            ),
            md(
                """## 4. 对抗挖掘与集成奖励

定期用攻击提示搜索高 RM、低真偏好样本，加入 RM 再训练；或多 RM 取 min。"""
            ),
            code(
                """def ensemble_min_rm(features):
    rm2 = 1.5 * features[:, 0] - 0.2 * features[:, 2]  # another head
    return torch.minimum(proxy_rm(features), rm2)


# mine hacks: high proxy, low true
cand = torch.rand(1000, 3)
hack = cand[(proxy_rm(cand) > 1.2) & (true_pref(cand) < 0)]
print('=== Adversarial Mining ===')
print(f'mined hacks={len(hack)} / 1000')
if len(hack):
    print('example', hack[0].tolist(), 'proxy', proxy_rm(hack[:1]).item(), 'true', true_pref(hack[:1]).item())
print(f'ensemble example mean={ensemble_min_rm(cand[:8]).mean():.3f}')
print('Key: Close the loop—mine hacks, retrain RM, constrain policy, repeat.')"""
            ),
            thinking(
                "奖励黑客与过度优化",
                "如何用影子真偏好（人工抽检）校准线上 RM？",
                "GRPO/过程奖励是否引入新的可黑客点？",
                "长度归一化会不会伤害真正需要长推理的任务？",
                "发现黑客后，该优先修 RM 还是加规则护栏？",
            ),
        ],
    )

    # ------------------------------------------------------------------
    # Tool-use RL
    # ------------------------------------------------------------------
    write_nb(
        "12_agent/08_tool_use_rl.ipynb",
        [
            md(
                """# 12.8 工具调用强化学习深挖

> 🕐 预估学习时间：40分钟

SFT 能让模型“会写工具 JSON”，但何时调用、调错如何恢复，更适合用可验证奖励做 RL（Toolformer/API-Bank/τ-bench 思路）。

深挖点：
- 动作空间：call / answer / clarify
- 轨迹奖励：成功、步数、非法调用
- 拒学“乱调工具”
- 与过程监督结合"""
            ),
            md(
                """## 1. 迷你工具环境

工具：`calc`、`search`。任务：算术或事实查询。"""
            ),
            code(
                """import torch
import torch.nn as nn
import torch.nn.functional as F
import random

torch.manual_seed(0)
random.seed(0)

TOOLS = ['calc', 'search', 'answer']


def env_step(task, action, arg):
    if action == 'calc':
        try:
            # only a+b
            a, b = map(int, arg.split('+'))
            return str(a + b), 0.0, False
        except Exception:
            return 'err', -0.5, False
    if action == 'search':
        kb = {'capital france': 'paris', 'capital germany': 'berlin'}
        return kb.get(arg, 'unknown'), 0.0, False
    if action == 'answer':
        ok = (arg.strip().lower() == task['gold'].lower())
        return 'done', 1.0 if ok else -1.0, True
    return 'bad', -1.0, True


def make_task():
    if random.random() < 0.5:
        a, b = random.randint(1, 9), random.randint(1, 9)
        return {'q': f'{a}+{b}', 'gold': str(a + b), 'type': 'calc'}
    item = random.choice([('capital france', 'paris'), ('capital germany', 'berlin')])
    return {'q': item[0], 'gold': item[1], 'type': 'search'}


print(env_step({'gold': '3'}, 'calc', '1+2'))
print(env_step({'gold': 'paris'}, 'search', 'capital france'))
print('Key: Verifiable environments turn tool use into RL with grounded rewards.')"""
            ),
            md(
                """## 2. 策略网络与 REINFORCE

状态 = 任务类型嵌入 + 是否已有观测；输出动作分布。"""
            ),
            code(
                """class ToolPolicy(nn.Module):
    def __init__(self):
        super().__init__()
        self.emb = nn.Embedding(3, 16)  # task type id
        self.fc = nn.Linear(16 + 2, 3)  # + has_obs, obs_ok

    def forward(self, task_type, has_obs, obs_ok):
        x = torch.cat([self.emb(task_type), has_obs, obs_ok], dim=-1)
        return self.fc(x)


def run_episode(policy, task, greedy=False):
    typ = torch.tensor([0 if task['type'] == 'calc' else 1])
    has_obs = torch.zeros(1, 1)
    obs_ok = torch.zeros(1, 1)
    obs = None
    logps = []
    reward = 0.0
    for step in range(3):
        logits = policy(typ, has_obs, obs_ok)
        dist = torch.distributions.Categorical(logits=logits)
        act = dist.probs.argmax() if greedy else dist.sample()
        logps.append(dist.log_prob(act))
        name = TOOLS[int(act)]
        if name == 'calc':
            arg = task['q'] if task['type'] == 'calc' else '0+0'
        elif name == 'search':
            arg = task['q']
        else:
            arg = obs if obs is not None else 'idk'
        obs, r, done = env_step(task, name, arg)
        reward += r - 0.05  # step cost
        has_obs = torch.ones(1, 1)
        obs_ok = torch.tensor([[0.0 if obs in {'err', 'unknown', 'bad'} else 1.0]])
        if done:
            break
    return reward, logps


policy = ToolPolicy()
opt = torch.optim.Adam(policy.parameters(), lr=1e-2)
print('=== REINFORCE Tool Policy ===')
for step in range(120):
    task = make_task()
    R, logps = run_episode(policy, task)
    loss = -R * torch.stack(logps).sum()
    opt.zero_grad(); loss.backward(); opt.step()
    if step % 30 == 0 or step == 119:
        # eval
        rs = [run_episode(policy, make_task(), greedy=True)[0] for _ in range(50)]
        print(f'step={step} avgR={sum(rs)/len(rs):.3f}')
print('Key: Step penalties + terminal success teach when to call vs answer.')"""
            ),
            md(
                """## 3. 非法调用与恢复

对错误工具施加强负奖励；鼓励观察错误后改换工具。"""
            ),
            code(
                """# Probe learned behavior on calc vs search tasks
for typ in ['calc', 'search']:
    task = make_task()
    while task['type'] != typ:
        task = make_task()
    # action probs at start
    typ_id = torch.tensor([0 if typ == 'calc' else 1])
    logits = policy(typ_id, torch.zeros(1, 1), torch.zeros(1, 1))
    probs = F.softmax(logits, dim=-1)[0]
    print(typ, 'action_probs', dict(zip(TOOLS, [round(p, 3) for p in probs.tolist()])))
print('Key: Inspect action marginals per task type to catch compulsive tool calling.')"""
            ),
            md(
                """## 4. 与 SFT / 过程奖励组合

工业配方常是：
1. SFT 轨迹（合法格式）  
2. 可验证 RL（成功/成本）  
3. 安全护栏（禁止危险工具参数）"""
            ),
            code(
                """recipe = {
    'stage1_sft': 'tool JSON + successful traces',
    'stage2_rl': 'verifiable success - lambda*steps - illegal',
    'stage3_safety': 'firewall + schema + human review for write tools',
}
print('=== Production Recipe ===')
for k, v in recipe.items():
    print(f'{k}: {v}')
print('Key: Format competence from SFT; decision competence from RL; safety from gates.')"""
            ),
            thinking(
                "工具调用强化学习",
                "多工具、长地平线任务如何做信用分配？",
                "环境不稳定（搜索结果变）时奖励方差怎么降？",
                "何时该 clarify 而不是瞎调工具？奖励如何塑造？",
                "工具 RL 与一般对话对齐如何共用同一底座而不互相干扰？",
            ),
        ],
    )

    # ------------------------------------------------------------------
    # Serving engine internals
    # ------------------------------------------------------------------
    write_nb(
        "09_inference_optimization/12_serving_engine_internals.ipynb",
        [
            md(
                """# 9.12 Serving 引擎内部深挖 (调度 / Paged KV / Radix)

> 🕐 预估学习时间：45分钟

vLLM / SGLang 类引擎的核心不是“包一层 API”，而是：**连续批处理调度 + 分页 KV + 前缀树复用**。本节用纯 Python 模拟关键数据结构与调度决策。

深挖点：
- 等待队列 vs 运行队列
- 块分配/回收与碎片
- 前缀匹配命中率
- 抢占与公平性"""
            ),
            md(
                """## 1. 分页 KV 块分配器

逻辑 token 序列映射到非连续物理块，避免预留最大长度造成浪费。"""
            ),
            code(
                """from dataclasses import dataclass, field


@dataclass
class BlockAllocator:
    n_blocks: int
    free: list = field(init=False)
    table: dict = field(default_factory=dict)  # req -> list[block_id]

    def __post_init__(self):
        self.free = list(range(self.n_blocks))

    def alloc(self, req, n):
        if len(self.free) < n:
            return False
        blocks = [self.free.pop() for _ in range(n)]
        self.table.setdefault(req, []).extend(blocks)
        return True

    def free_req(self, req):
        for b in self.table.pop(req, []):
            self.free.append(b)


alloc = BlockAllocator(16)
print('=== Block Allocator ===')
print('alloc A 4', alloc.alloc('A', 4), 'free', len(alloc.free))
print('alloc B 10', alloc.alloc('B', 10), 'free', len(alloc.free))
print('alloc C 4', alloc.alloc('C', 4))  # should fail
alloc.free_req('A')
print('after free A, alloc C 4', alloc.alloc('C', 4), 'free', len(alloc.free))
print('Key: Paging trades indirection for near-zero fragmentation waste.')"""
            ),
            md(
                """## 2. Continuous batching 调度器

decode 步优先填满 batch；有空位再 prefill 新请求。"""
            ),
            code(
                """@dataclass
class Req:
    rid: int
    remaining_prefill: int
    remaining_decode: int
    stage: str = 'waiting'


class Scheduler:
    def __init__(self, max_batched_tokens=64):
        self.max_batched_tokens = max_batched_tokens
        self.waiting = []
        self.running = []
        self.done = []
        self.t = 0

    def add(self, req):
        self.waiting.append(req)

    def step(self):
        self.t += 1
        # finish decode slots and free capacity
        still = []
        used = 0
        for r in self.running:
            if r.stage == 'prefill':
                take = min(r.remaining_prefill, self.max_batched_tokens - used)
                r.remaining_prefill -= take
                used += take
                if r.remaining_prefill == 0:
                    r.stage = 'decode'
                still.append(r)
            else:
                if used < self.max_batched_tokens:
                    r.remaining_decode -= 1
                    used += 1
                if r.remaining_decode <= 0:
                    self.done.append(r)
                else:
                    still.append(r)
        self.running = still
        # admit waiting as prefill if space
        while self.waiting and used < self.max_batched_tokens:
            r = self.waiting[0]
            if r.remaining_prefill <= self.max_batched_tokens - used or not self.running:
                self.waiting.pop(0)
                r.stage = 'prefill'
                self.running.append(r)
                used += min(r.remaining_prefill, self.max_batched_tokens - used)
            else:
                break
        return used


sch = Scheduler(max_batched_tokens=16)
for i, (p, d) in enumerate([(30, 4), (8, 10), (12, 6)]):
    sch.add(Req(i, p, d))
utils = []
while len(sch.done) < 3 and sch.t < 40:
    utils.append(sch.step())
print('=== Continuous Batching ===')
print('utilization per step', utils)
print('finish times', [(r.rid, sch.t) for r in sch.done])
print('Key: Mixing prefill/decode under a token budget is the heart of online LLM serving.')"""
            ),
            md(
                """## 3. Radix 前缀复用

多请求共享系统提示/工具前缀时，缓存树节点可复用 KV 块。"""
            ),
            code(
                """class RadixNode:
    def __init__(self):
        self.children = {}
        self.block_ids = []
        self.hits = 0


class RadixCache:
    def __init__(self):
        self.root = RadixNode()

    def match_or_insert(self, tokens):
        node = self.root
        matched = 0
        for tok in tokens:
            if tok in node.children:
                node = node.children[tok]
                matched += 1
                node.hits += 1
            else:
                break
        # insert rest
        for tok in tokens[matched:]:
            nxt = RadixNode()
            nxt.block_ids = [hash((id(node), tok)) % 10_000]
            node.children[tok] = nxt
            node = nxt
        return matched


cache = RadixCache()
prompts = [
    [1, 2, 3, 4, 5],
    [1, 2, 3, 9, 9],
    [1, 2, 7],
    [8, 8, 8],
]
print('=== Radix Prefix Hits ===')
for p in prompts:
    m = cache.match_or_insert(p)
    print(p, 'matched_prefix_len', m)
print('Key: Higher prefix hit rate → less prefill compute; tree eviction policies matter under memory pressure.')"""
            ),
            md(
                """## 4. 公平性与抢占

长 prefill 可能饿死短交互。可对 waiting 用老化优先级，或限制单步 prefill 长度（chunked prefill）。"""
            ),
            code(
                """def admit_priority(waiting, now):
    # higher score first: age - beta * prefill_len
    return sorted(waiting, key=lambda r: (now - r.rid) - 0.01 * r.remaining_prefill, reverse=True)


waiting = [Req(0, 100, 5), Req(1, 8, 5), Req(2, 12, 5)]
print('=== Fairness Ordering ===')
print([(r.rid, r.remaining_prefill) for r in admit_priority(waiting, now=10)])
print('Key: Production schedulers explicitly optimize TTFT fairness, not only average throughput.')"""
            ),
            thinking(
                "Serving 引擎内部",
                "chunked prefill 如何改善尾部 TTFT？代价是什么？",
                "前缀缓存与多租户隔离冲突时如何设计命名空间？",
                "抢占正在 decode 的请求需要保存哪些状态？",
                "如何用线上 trace 回放评估调度策略改动？",
            ),
        ],
    )

    print("done")


if __name__ == "__main__":
    build()
