#!/usr/bin/env python3
"""Generate supplemental educational notebooks for coverage gaps."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

NB_META = {
    "kernelspec": {
        "display_name": "Python 3",
        "language": "python",
        "name": "python3",
    },
    "language_info": {
        "name": "python",
        "version": "3.10.0",
    },
}


def md(text: str) -> dict:
    lines = text.strip("\n").split("\n")
    source = [line + "\n" for line in lines[:-1]] + ([lines[-1] + "\n"] if lines else [])
    return {"cell_type": "markdown", "metadata": {}, "source": source}


def code(text: str) -> dict:
    lines = text.strip("\n").split("\n")
    source = [line + "\n" for line in lines[:-1]] + ([lines[-1] + "\n"] if lines else [])
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": source,
    }


def write_nb(rel_path: str, cells: list[dict]) -> None:
    path = ROOT / rel_path
    path.parent.mkdir(parents=True, exist_ok=True)
    nb = {
        "cells": cells,
        "metadata": NB_META,
        "nbformat": 4,
        "nbformat_minor": 4,
    }
    path.write_text(json.dumps(nb, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"wrote {rel_path}")


def thinking(section: str, q1: str, q2: str, q3: str, q4: str) -> dict:
    return md(
        f"""## 课后思考题

1. {q1}
2. {q2}
3. {q3}
4. {q4}

---
> 本节涵盖了{section}的核心概念与代码实现。建议结合实际项目需求，选择合适的技术方案，并通过实验验证不同方法的效果差异。"""
    )


def build_all() -> None:
    # ------------------------------------------------------------------
    # 19.1 Mechanistic Interpretability
    # ------------------------------------------------------------------
    write_nb(
        "19_interpretability/01_mechanistic_interpretability.ipynb",
        [
            md(
                """# 19.1 机理可解释性 (Mechanistic Interpretability)

> 🕐 预估学习时间：45分钟

机理可解释性试图打开大模型的"黑盒"，定位具体电路、特征与因果通路，是安全审计、对齐验证与模型调试的关键能力。代表工作：Anthropic Circuits、Sparse Autoencoders (SAE)、Activation Patching。

本节涵盖：
- logit 归因与直接效应
- Activation Patching（激活修补）
- Sparse Autoencoder 特征分解
- Attention Head 专项分析
- 产业应用场景"""
            ),
            md(
                """## 1. Logit 归因：谁把答案推向了正确方向？

**核心思想**：把最终 logits 的变化分解到残差流中各组件（注意力头、MLP）的贡献。

**基本原理**：
- Transformer 残差流可写为 `x = embed + Σ attn + Σ mlp`
- 对目标 token 的 logit，可用线性探针 / 解嵌入矩阵 `W_U` 做投影归因
- 正贡献组件"支持"该答案，负贡献组件"反对"

**用途**：快速定位"是哪个层/头在驱动错误答案"。"""
            ),
            code(
                """import torch
import torch.nn as nn
import torch.nn.functional as F

torch.manual_seed(42)


class TinyTransformerBlock(nn.Module):
    def __init__(self, d=64, n_heads=4):
        super().__init__()
        self.ln1 = nn.LayerNorm(d)
        self.attn = nn.MultiheadAttention(d, n_heads, batch_first=True)
        self.ln2 = nn.LayerNorm(d)
        self.mlp = nn.Sequential(nn.Linear(d, 4 * d), nn.GELU(), nn.Linear(4 * d, d))

    def forward(self, x, return_parts=False):
        h = self.ln1(x)
        attn_out, _ = self.attn(h, h, h, need_weights=False)
        x = x + attn_out
        mlp_out = self.mlp(self.ln2(x))
        x = x + mlp_out
        if return_parts:
            return x, attn_out, mlp_out
        return x


class TinyLM(nn.Module):
    def __init__(self, vocab=100, d=64, n_layers=3):
        super().__init__()
        self.embed = nn.Embedding(vocab, d)
        self.blocks = nn.ModuleList([TinyTransformerBlock(d) for _ in range(n_layers)])
        self.ln_f = nn.LayerNorm(d)
        self.unembed = nn.Linear(d, vocab, bias=False)

    def forward_with_parts(self, ids):
        x = self.embed(ids)
        parts = []
        for i, block in enumerate(self.blocks):
            x, attn_out, mlp_out = block(x, return_parts=True)
            parts.append((f'L{i}.attn', attn_out),)
            parts.append((f'L{i}.mlp', mlp_out),)
        x = self.ln_f(x)
        logits = self.unembed(x)
        return logits, parts, x


model = TinyLM()
ids = torch.randint(0, 100, (2, 16))
target_token = 7
logits, parts, final_h = model.forward_with_parts(ids)

# Attribute final-position residual components to target logit via unembed
W_U = model.unembed.weight  # (vocab, d)
target_dir = W_U[target_token]  # (d,)

print('=== Logit Attribution ===')
print(f'Input ids: {ids.shape}, target token={target_token}')
contribs = []
for name, part in parts:
    # contribution of this residual write at last position
    write = part[:, -1, :]  # (B, d)
    score = (write * target_dir).sum(dim=-1).mean().item()
    contribs.append((name, score))

contribs_sorted = sorted(contribs, key=lambda x: abs(x[1]), reverse=True)
print(f'{\"Component\":<10} {\"Mean contrib to logit\":>22}')
for name, score in contribs_sorted:
    print(f'{name:<10} {score:>22.4f}')

print(f'\\nKey: Logit attribution decomposes the final answer into residual-stream writes.')
print(f'Large positive/negative components are the first places to inspect for bugs or bias.')"""
            ),
            md(
                """## 2. Activation Patching：因果干预定位关键通路

**核心思想**：用"干净运行"的激活替换"被污染运行"中的对应激活，观察输出是否恢复。

**步骤**：
1. Clean run：正确提示 → 正确答案
2. Corrupt run：改写关键实体 → 错误答案
3. Patch：把 clean 的某层激活塞回 corrupt，看正确 logit 是否回升

若 patch 某组件后性能恢复，说明该组件对任务**因果必要**。"""
            ),
            code(
                """def run_cached(model, ids):
    '''Forward while caching residual stream after each block.'''
    caches = []
    x = model.embed(ids)
    for block in model.blocks:
        x = block(x)
        caches.append(x.detach().clone())
    x = model.ln_f(x)
    logits = model.unembed(x)
    return logits, caches


def patched_forward(model, corrupt_ids, clean_caches, patch_layer):
    x = model.embed(corrupt_ids)
    for i, block in enumerate(model.blocks):
        x = block(x)
        if i == patch_layer:
            x = clean_caches[i]
    x = model.ln_f(x)
    return model.unembed(x)


clean_ids = torch.randint(0, 100, (4, 12))
corrupt_ids = clean_ids.clone()
corrupt_ids[:, 3] = (corrupt_ids[:, 3] + 17) % 100  # corrupt a key token

clean_logits, clean_caches = run_cached(model, clean_ids)
corrupt_logits, _ = run_cached(model, corrupt_ids)

clean_score = clean_logits[:, -1, target_token].mean().item()
corrupt_score = corrupt_logits[:, -1, target_token].mean().item()

print('=== Activation Patching ===')
print(f'Clean logit(target):   {clean_score:.4f}')
print(f'Corrupt logit(target): {corrupt_score:.4f}')
print(f'Gap: {clean_score - corrupt_score:.4f}')

print(f'\\n{\"Layer\":>5} {\"Patched logit\":>14} {\"Recovery%\":>10}')
for layer in range(len(model.blocks)):
    patched_logits = patched_forward(model, corrupt_ids, clean_caches, layer)
    score = patched_logits[:, -1, target_token].mean().item()
    recovery = (score - corrupt_score) / (clean_score - corrupt_score + 1e-8) * 100
    print(f'{layer:>5} {score:>14.4f} {recovery:>9.1f}%')

print(f'\\nKey: Activation patching finds causally necessary layers/components.')
print(f'High recovery% means that layer carries information sufficient to restore the clean behavior.')"""
            ),
            md(
                """## 3. Sparse Autoencoder：把叠加特征拆开

**问题**：神经网络表征高度叠加（superposition），单个神经元往往混合多个概念。

**SAE 思路**：
- 用更大、更稀疏的字典重建激活：`x ≈ W_dec · ReLU(W_enc · x + b)`
- L1 / Top-K 稀疏惩罚迫使每个字典单元对应更"单义"的特征
- 可用于找"拒绝有害请求"、"引用代码语法"等可解释特征

Anthropic / OpenAI 的大规模 SAE 是当前机理解释的主流工具。"""
            ),
            code(
                """class SparseAutoencoder(nn.Module):
    def __init__(self, d_model=64, d_dict=256, l1_coef=1e-3):
        super().__init__()
        self.enc = nn.Linear(d_model, d_dict)
        self.dec = nn.Linear(d_dict, d_model, bias=False)
        self.l1_coef = l1_coef
        # unit-norm decoder columns improve feature interpretability
        with torch.no_grad():
            self.dec.weight.div_(self.dec.weight.norm(dim=0, keepdim=True) + 1e-8)

    def forward(self, x):
        z = F.relu(self.enc(x))
        recon = self.dec(z)
        recon_loss = F.mse_loss(recon, x)
        sparse_loss = z.abs().mean()
        loss = recon_loss + self.l1_coef * sparse_loss
        return loss, recon_loss.detach(), sparse_loss.detach(), z


# Collect residual activations as "dataset"
with torch.no_grad():
    acts = []
    for _ in range(20):
        batch = torch.randint(0, 100, (8, 16))
        _, _, h = model.forward_with_parts(batch)
        acts.append(h.reshape(-1, h.size(-1)))
    acts = torch.cat(acts, dim=0)

sae = SparseAutoencoder(d_model=64, d_dict=256, l1_coef=5e-3)
opt = torch.optim.Adam(sae.parameters(), lr=1e-2)

print('=== Sparse Autoencoder Training ===')
for step in range(80):
    idx = torch.randint(0, acts.size(0), (256,))
    loss, recon, sparse, z = sae(acts[idx])
    opt.zero_grad()
    loss.backward()
    opt.step()
    with torch.no_grad():
        sae.dec.weight.div_(sae.dec.weight.norm(dim=0, keepdim=True) + 1e-8)
    if step % 20 == 0 or step == 79:
        active = (z > 0).float().mean().item()
        print(f'step={step:02d} loss={loss.item():.4f} recon={recon.item():.4f} '
              f'l1={sparse.item():.4f} active_frac={active:.3f}')

with torch.no_grad():
    _, _, _, z_all = sae(acts[:512])
    usage = (z_all > 0).float().mean(dim=0)
    topk = usage.topk(5)

print(f'\\nTop-5 most used features: idx={topk.indices.tolist()}, usage={topk.values.tolist()}')
print(f'\\nKey: SAE expands and sparsifies activations into more monosemantic features.')
print(f'Decoder-column unit norm + L1 sparsity are the two practical ingredients.')"""
            ),
            md(
                """## 4. Attention Head 分析与产业用途

| 分析对象 | 方法 | 典型发现 |
|---------|------|---------|
| Induction heads | 前缀匹配复制 | few-shot / ICL 的机制基础 |
| Previous-token heads | 位置偏移注意力 | 构成 induction 电路 |
| 抑制头 | 负 logit 归因 | 参与拒绝/校准 |

**产业用途**：
- 安全：定位越狱相关电路，做定向消融
- 对齐审计：验证"诚实"特征是否被真实使用
- 调试：找出模型记住污染基准的通路
- 编辑：结合 ROME/MEMIT 做更可解释的知识更新"""
            ),
            code(
                """def attention_pattern_stats(attn_module, x):
    '''Compute average attention entropy and diagonal mass.'''
    B, T, D = x.shape
    # reuse MultiheadAttention weights
    h = attn_module.ln1(x) if hasattr(attn_module, 'ln1') else x
    # manual qkv for one block
    block = attn_module
    q = k = v = block.ln1(x)
    # Use the module's in_proj if available via mha
    mha = block.attn
    attn_out, weights = mha(q, k, v, need_weights=True, average_attn_weights=True)
    # weights: (B, T, T)
    ent = -(weights * (weights + 1e-9).log()).sum(dim=-1).mean().item()
    diag = weights.diagonal(dim1=-2, dim2=-1).mean().item()
    return attn_out, ent, diag


print('=== Attention Head Diagnostics ===')
x0 = model.embed(ids)
for i, block in enumerate(model.blocks):
    _, ent, diag = attention_pattern_stats(block, x0)
    x0 = block(x0)
    print(f'Layer {i}: attn_entropy={ent:.3f}, diagonal_mass={diag:.3f}')

print(f'\\nKey: Low entropy + off-diagonal structure often indicates specialized heads')
print(f'(e.g., induction). High diagonal mass suggests local/previous-token behavior.')
print(f'Mechanistic tools turn qualitative hunches into measurable interventions.')"""
            ),
            thinking(
                "19.1 机理可解释性",
                "Logit 归因与 Activation Patching 都能指出“重要组件”，二者的因果强度有何不同？",
                "为什么叠加（superposition）会让单神经元解释失效？SAE 如何缓解？",
                "若某安全相关特征在 SAE 中被找到，如何在生产中用于监控或干预？",
                "机理可解释性在红队、对齐审计、知识编辑中分别能解决什么问题？",
            ),
        ],
    )

    # ------------------------------------------------------------------
    # 19.2 Representation analysis / steering
    # ------------------------------------------------------------------
    write_nb(
        "19_interpretability/02_representation_steering.ipynb",
        [
            md(
                """# 19.2 表征分析与激活引导 (Representation Steering)

> 🕐 预估学习时间：35分钟

除了电路级分析，产业中更常用的是表征级技术：线性探针、对比激活差、激活引导（Activation Steering / CAA）与拒绝方向消融。

本节涵盖：
- 线性探针（Probing）
- Contrastive Activation / Steering Vector
- 推理时干预与强度控制
- 与微调/安全护栏的互补关系"""
            ),
            md(
                """## 1. 线性探针：表征里有没有某概念？

训练一个轻量线性分类器读出隐藏状态，判断模型内部是否线性可分地编码了目标属性（毒性、语言、真实性等）。"""
            ),
            code(
                """import torch
import torch.nn as nn
import torch.nn.functional as F

torch.manual_seed(0)

d_model = 64
n = 400
# Synthetic: class bit is linearly encoded in hidden states with noise
labels = torch.randint(0, 2, (n,))
h = torch.randn(n, d_model) * 0.5
h[:, 0] += labels.float() * 2.0  # concept direction

probe = nn.Linear(d_model, 1)
opt = torch.optim.Adam(probe.parameters(), lr=1e-2)

print('=== Linear Probe ===')
for step in range(60):
    logit = probe(h).squeeze(-1)
    loss = F.binary_cross_entropy_with_logits(logit, labels.float())
    opt.zero_grad()
    loss.backward()
    opt.step()
    if step % 20 == 0 or step == 59:
        acc = ((logit > 0).long() == labels).float().mean().item()
        print(f'step={step:02d} loss={loss.item():.4f} acc={acc:.3f}')

direction = probe.weight.detach().squeeze(0)
direction = direction / (direction.norm() + 1e-8)
print(f'\\nProbe direction top dims: {direction.abs().topk(3).indices.tolist()}')
print(f'Key: High probe accuracy means the concept is linearly readable from activations.')"""
            ),
            md(
                """## 2. Steering Vector：对比激活差

**Contrastive Activation Addition (CAA)**：
1. 构造正/负提示对（如"诚实回答" vs "含糊其辞"）
2. 取中间层平均激活差作为引导向量 `v`
3. 推理时 `h ← h + α · v`

优点：无需训练、可即时开关；缺点：强度过大可能损伤流畅性。"""
            ),
            code(
                """class ToyDecoder(nn.Module):
    def __init__(self, d=64, vocab=50):
        super().__init__()
        self.embed = nn.Embedding(vocab, d)
        self.blocks = nn.ModuleList([
            nn.TransformerEncoderLayer(d, 4, 128, batch_first=True) for _ in range(2)
        ])
        self.head = nn.Linear(d, vocab)

    def hidden(self, ids, layer=1):
        x = self.embed(ids)
        for i, blk in enumerate(self.blocks):
            x = blk(x)
            if i == layer:
                return x
        return x

    def forward(self, ids, steer=None, alpha=1.0, layer=1):
        x = self.embed(ids)
        for i, blk in enumerate(self.blocks):
            x = blk(x)
            if steer is not None and i == layer:
                x = x + alpha * steer
        return self.head(x)


model = ToyDecoder()
pos = torch.randint(0, 50, (32, 10))
neg = torch.randint(0, 50, (32, 10))

with torch.no_grad():
    h_pos = model.hidden(pos).mean(dim=(0, 1))
    h_neg = model.hidden(neg).mean(dim=(0, 1))
    steer = h_pos - h_neg
    steer = steer / (steer.norm() + 1e-8)

probe_ids = torch.randint(0, 50, (8, 10))
base_logits = model(probe_ids)
steered_logits = model(probe_ids, steer=steer, alpha=2.0)

shift = (steered_logits - base_logits).abs().mean().item()
print('=== Activation Steering ===')
print(f'Steering vector norm={steer.norm().item():.4f}')
print(f'Mean |logit shift| at alpha=2.0: {shift:.4f}')

for alpha in [0.0, 0.5, 1.0, 2.0, 4.0]:
    out = model(probe_ids, steer=steer, alpha=alpha)
    entropy = (-F.softmax(out[:, -1], dim=-1) * F.log_softmax(out[:, -1], dim=-1)).sum(-1).mean()
    print(f'alpha={alpha:.1f}: last-token entropy={entropy.item():.3f}')

print(f'\\nKey: Steering adds a concept direction at inference time; tune alpha to trade control vs fluency.')"""
            ),
            md(
                """## 3. 拒绝方向消融与互补策略

对安全场景，可估计"拒绝方向"并在越狱时增强它，或在过度拒答时减弱它。

| 方法 | 改参数？ | 可逆？ | 适用 |
|------|---------|-------|------|
| Steering | 否 | 是 | 快速行为调节 |
| LoRA 安全微调 | 是 | 部分 | 长期对齐 |
| Guardrail 外挂 | 否 | 是 | 生产兜底 |
| SAE 特征钳制 | 否 | 是 | 精细概念控制 |

实践中通常 **Steering/护栏做运行时控制，微调做分布偏移**。"""
            ),
            code(
                """def refusal_score(logits, refuse_token=1, comply_token=2):
    return (logits[:, -1, refuse_token] - logits[:, -1, comply_token]).mean().item()


refusal_dir = steer  # reuse contrastive vector as a stand-in
print('=== Refusal Direction Control ===')
for alpha in [-2.0, -1.0, 0.0, 1.0, 2.0]:
    logits = model(probe_ids, steer=refusal_dir, alpha=alpha)
    print(f'alpha={alpha:+.1f}: refusal_score={refusal_score(logits):+.4f}')

print(f'\\nKey: Same vector can increase or decrease a behavior by flipping the sign of alpha.')
print(f'Combine with external guardrails for production defense-in-depth.')"""
            ),
            thinking(
                "19.2 表征分析与激活引导",
                "探针准确率高是否意味着该概念被模型“用于”决策？如何用因果方法验证？",
                "Steering 与 LoRA 安全微调各适合什么变更频率与风险等级？",
                "alpha 过大时会出现哪些失败模式？如何自动选择强度？",
                "如何把 SAE 特征与 Steering Vector 结合，做成可开关的概念级控件？",
            ),
        ],
    )

    # ------------------------------------------------------------------
    # 03.10 SSM Hybrid
    # ------------------------------------------------------------------
    write_nb(
        "03_architecture_design/10_ssm_hybrid.ipynb",
        [
            md(
                """# 3.10 状态空间模型与混合架构 (SSM & Hybrid)

> 🕐 预估学习时间：40分钟

Mamba / Mamba-2、RWKV、RetNet 等线性复杂度序列模型，以及 Jamba、Zamba、Jamba-1.5 等 Attention+SSM 混合架构，是长上下文与高吞吐场景的重要选项。

本节涵盖：
- 离散状态空间与选择性扫描
- Mamba 块结构（简化实现）
- Attention–SSM 混合堆叠
- 与 Transformer 的效率/质量权衡"""
            ),
            md(
                """## 1. 从 S4 到 Selective SSM

经典 SSM：`h_t = A h_{t-1} + B x_t`, `y_t = C h_t + D x_t`

**选择性（Mamba）关键改动**：让 `B/C/Δ` 依赖输入，使模型能对当前 token **选择记住或忘记**，大幅提升语言建模质量。"""
            ),
            code(
                """import torch
import torch.nn as nn
import torch.nn.functional as F
import time

torch.manual_seed(42)


class MambaBlock(nn.Module):
    '''Educational selective SSM block (scan implemented in Python for clarity).'''
    def __init__(self, d_model=64, d_state=16, d_conv=4, expand=2):
        super().__init__()
        self.d_model = d_model
        self.d_state = d_state
        self.d_inner = expand * d_model
        self.in_proj = nn.Linear(d_model, self.d_inner * 2, bias=False)
        self.conv1d = nn.Conv1d(self.d_inner, self.d_inner, d_conv, padding=d_conv - 1, groups=self.d_inner)
        self.x_proj = nn.Linear(self.d_inner, d_state * 2 + 1, bias=False)
        self.dt_proj = nn.Linear(1, self.d_inner)
        self.A_log = nn.Parameter(torch.log(torch.rand(self.d_inner, d_state) + 0.1))
        self.D = nn.Parameter(torch.ones(self.d_inner))
        self.out_proj = nn.Linear(self.d_inner, d_model, bias=False)

    def ssm_scan(self, u, delta, B, C):
        # u, delta: (B, T, D); B,C: (B, T, N)
        batch, seq, d = u.shape
        A = -torch.exp(self.A_log)  # (D, N)
        h = torch.zeros(batch, d, self.d_state, device=u.device)
        ys = []
        for t in range(seq):
            dt = delta[:, t].unsqueeze(-1)          # (B, D, 1)
            A_bar = torch.exp(A.unsqueeze(0) * dt)  # (B, D, N)
            B_t = B[:, t].unsqueeze(1)              # (B, 1, N)
            C_t = C[:, t].unsqueeze(1)
            h = h * A_bar + u[:, t].unsqueeze(-1) * B_t * dt
            y = (h * C_t).sum(-1) + self.D * u[:, t]
            ys.append(y)
        return torch.stack(ys, dim=1)

    def forward(self, x):
        batch, seq, _ = x.shape
        xz = self.in_proj(x)
        x_branch, z = xz.chunk(2, dim=-1)
        x_conv = self.conv1d(x_branch.transpose(1, 2))[:, :, :seq].transpose(1, 2)
        x_conv = F.silu(x_conv)
        params = self.x_proj(x_conv)
        B = params[..., :self.d_state]
        C = params[..., self.d_state:2 * self.d_state]
        dt = F.softplus(self.dt_proj(params[..., -1:].contiguous()))
        y = self.ssm_scan(x_conv, dt, B, C)
        y = y * F.silu(z)
        return self.out_proj(y)


x = torch.randn(2, 128, 64)
mamba = MambaBlock()
y = mamba(x)
print('=== Mamba Block ===')
print(f'Input {tuple(x.shape)} -> Output {tuple(y.shape)}')
print(f'Params: {sum(p.numel() for p in mamba.parameters()):,}')
print(f'Key: Selective SSM keeps O(n) compute/memory while making B/C/Δ input-dependent.')"""
            ),
            md(
                """## 2. 复杂度对比：Attention vs SSM

| 方法 | 训练计算 | 推理显存 (KV/state) | 质检长程依赖 |
|------|---------|---------------------|-------------|
| MHA | O(n²d) | O(n d) KV | 强 |
| GQA/MQA | O(n²d) | 更低 KV | 强 |
| Mamba | O(n d r) | O(d r) 固定状态 | 中-强 |
| Hybrid | 介于两者 | 介于两者 | 通常最好 |

结论：纯 SSM 吞吐优势大；需要精确召回针点信息时，混合架构更稳。"""
            ),
            code(
                """class AttentionBlock(nn.Module):
    def __init__(self, d=64, h=4):
        super().__init__()
        self.ln = nn.LayerNorm(d)
        self.attn = nn.MultiheadAttention(d, h, batch_first=True)
        self.mlp = nn.Sequential(nn.LayerNorm(d), nn.Linear(d, 4*d), nn.GELU(), nn.Linear(4*d, d))

    def forward(self, x):
        h = self.ln(x)
        a, _ = self.attn(h, h, h, need_weights=False)
        x = x + a
        return x + self.mlp(x)


def bench(module, seq_lens, d=64, batch=2, warmup=1):
    results = []
    for n in seq_lens:
        x = torch.randn(batch, n, d)
        for _ in range(warmup):
            module(x)
        t0 = time.perf_counter()
        for _ in range(3):
            module(x)
        dt = (time.perf_counter() - t0) / 3
        results.append((n, dt))
    return results


attn = AttentionBlock()
ssm = MambaBlock()
seqs = [64, 128, 256, 512]
print('=== Runtime scaling (CPU educational) ===')
print(f'{\"N\":>6} {\"Attn(s)\":>10} {\"Mamba(s)\":>10} {\"Attn/Mamba\":>12}')
for (n, ta), (_, tm) in zip(bench(attn, seqs), bench(ssm, seqs)):
    print(f'{n:>6} {ta:>10.4f} {tm:>10.4f} {ta/max(tm,1e-6):>12.2f}x')
print(f'\\nKey: Attention grows closer to quadratic; SSM scan is linear in sequence length.')"""
            ),
            md(
                """## 3. Hybrid：交错堆叠 Attention 与 SSM

Jamba 风格：多数层用 Mamba，每隔若干层插入注意力层，兼顾全局精确匹配与线性吞吐。"""
            ),
            code(
                """class HybridModel(nn.Module):
    def __init__(self, d=64, n_layers=6, attn_every=3, vocab=100):
        super().__init__()
        self.embed = nn.Embedding(vocab, d)
        self.layers = nn.ModuleList()
        self.types = []
        for i in range(n_layers):
            if (i + 1) % attn_every == 0:
                self.layers.append(AttentionBlock(d))
                self.types.append('attn')
            else:
                self.layers.append(MambaBlock(d))
                self.types.append('mamba')
        self.ln = nn.LayerNorm(d)
        self.head = nn.Linear(d, vocab)

    def forward(self, ids):
        x = self.embed(ids)
        for layer in self.layers:
            x = layer(x)
        return self.head(self.ln(x))


hybrid = HybridModel()
ids = torch.randint(0, 100, (2, 64))
logits = hybrid(ids)
print('=== Hybrid Attention+SSM ===')
print(f'Layer schedule: {hybrid.types}')
print(f'Logits: {tuple(logits.shape)}')
print(f'Total params: {sum(p.numel() for p in hybrid.parameters()):,}')
print(f'\\nKey: Put scarce Attention layers where precise token-token routing matters;')
print(f'use SSM layers for cheap long-range state propagation.')"""
            ),
            thinking(
                "3.10 状态空间模型与混合架构",
                "选择性机制为什么比固定 A/B/C 的经典 SSM 更适合语言建模？",
                "在 1M 上下文服务中，何时优先选 Hybrid 而非纯 Transformer + 稀疏注意力？",
                "混合架构如何与 GQA、量化、推测解码组合？",
                "教育实现里的 Python scan 与硬件高效 parallel scan 差在哪里？",
            ),
        ],
    )

    # ------------------------------------------------------------------
    # 09.9 PD disaggregation
    # ------------------------------------------------------------------
    write_nb(
        "09_inference_optimization/09_pd_disaggregation.ipynb",
        [
            md(
                """# 9.9 Prefill/Decode 分离与 KV 卸载

> 🕐 预估学习时间：40分钟

Prefill（提示预填充）计算密集、Decode（逐 token 生成）显存带宽密集。将两者分离到不同池（DistServe、Mooncake、vLLM PD）、并对 KV Cache 做分层卸载，是 2024–2026 推理集群的核心趋势。

本节涵盖：
- Prefill vs Decode 资源画像
- PD 分离调度
- KV Cache 卸载（GPU→CPU/远端）
- 端到端延迟与成本权衡"""
            ),
            md(
                """## 1. 为什么要分离 Prefill 和 Decode？

| 阶段 | 计算特点 | 瓶颈 | 批处理友好性 |
|------|---------|------|-------------|
| Prefill | 大矩阵乘，高算力 | FLOPs | 高（长提示可并行） |
| Decode | 小矩阵乘 + 读 KV | 显存带宽 | 需 continuous batching |

混部时，长提示 prefill 会打断 decode 批次，造成 TTFT/TPOT 抖动。"""
            ),
            code(
                """import torch
import time
from dataclasses import dataclass, field

torch.manual_seed(42)


@dataclass
class Request:
    req_id: int
    prompt_len: int
    output_len: int
    generated: int = 0
    stage: str = 'prefill'  # prefill|decode|done
    ttft: float | None = None
    finish_t: float | None = None


def flops_prefill(prompt_len, d=4096, n_layers=32):
    # rough transformer FLOPs ~ 2 * n_layers * prompt_len * d^2 * c
    return 2 * n_layers * prompt_len * (d ** 2) * 6


def flops_decode_step(kv_len, d=4096, n_layers=32):
    return 2 * n_layers * 1 * (d ** 2) * 6 + n_layers * kv_len * d  # attn term


print('=== Prefill vs Decode Work Profile ===')
for p in [512, 2048, 8192]:
    print(f'prompt={p:>5}: prefill_FLOPs~{flops_prefill(p)/1e12:.2f}TF, '
          f'decode_step@kv={p}~{flops_decode_step(p)/1e9:.2f}GF')

print(f'\\nKey: Prefill cost scales with prompt length; decode is many bandwidth-heavy steps.')"""
            ),
            md(
                """## 2. PD 分离调度模拟

- **Prefill Pool**：高算力 GPU，吃长提示
- **Decode Pool**：高带宽 / 更多并发槽位，专责生成
- 交接：prefill 完成后把 KV 传到 decode 池（或共享存储）"""
            ),
            code(
                """@dataclass
class ClusterSim:
    prefill_capacity: float = 40.0  # TFLOPs unit-less throughput
    decode_slots: int = 8
    transfer_overhead: float = 0.002
    now: float = 0.0
    prefill_q: list = field(default_factory=list)
    decode_active: list = field(default_factory=list)
    finished: list = field(default_factory=list)

    def admit(self, reqs):
        self.prefill_q.extend(reqs)

    def step(self, dt=0.001):
        self.now += dt
        # process one prefill chunkally
        if self.prefill_q:
            req = self.prefill_q[0]
            work = flops_prefill(req.prompt_len) / 1e12
            # finish prefill in one coarse step for demo when capacity allows
            req.ttft = self.now + work / self.prefill_capacity + self.transfer_overhead
            req.stage = 'decode'
            self.prefill_q.pop(0)
            if len(self.decode_active) < self.decode_slots:
                self.decode_active.append(req)
            else:
                # backpressure: wait — put at front of a virtual waiting decode
                self.decode_active.append(req)  # simplified

        still = []
        for req in self.decode_active:
            if self.now < req.ttft:
                still.append(req)
                continue
            req.generated += 1
            if req.generated >= req.output_len:
                req.stage = 'done'
                req.finish_t = self.now
                self.finished.append(req)
            else:
                still.append(req)
        self.decode_active = still


def run_policy(name, mixed=True):
    sim = ClusterSim(decode_slots=4 if mixed else 8)
    reqs = [Request(i, prompt_len=p, output_len=o)
            for i, (p, o) in enumerate([(4096, 64), (512, 128), (2048, 32), (1024, 96)] * 3)]
    sim.admit(reqs)
    # mixed: single pool pretends prefill steals decode slots
    steps = 0
    while len(sim.finished) < len(reqs) and steps < 50000:
        if mixed and sim.prefill_q:
            # long prefill blocks half decode slots
            sim.decode_slots = 2
        else:
            sim.decode_slots = 8
        sim.step(dt=0.002)
        steps += 1
    ttfts = [r.ttft for r in sim.finished if r.ttft is not None]
    lat = [r.finish_t for r in sim.finished]
    return {
        'name': name,
        'avg_ttft': sum(ttfts) / len(ttfts),
        'avg_e2e': sum(lat) / len(lat),
        'finished': len(sim.finished),
    }


mixed = run_policy('colocated-mixed', mixed=True)
split = run_policy('pd-disaggregated', mixed=False)
print('=== Scheduling Comparison ===')
for r in (mixed, split):
    print(f\"{r['name']:<18} avg_ttft={r['avg_ttft']:.4f}s  avg_e2e={r['avg_e2e']:.4f}s  finished={r['finished']}\")
print(f'\\nKey: Disaggregating prefill/decode reduces interference and stabilizes TTFT/TPOT.')"""
            ),
            md(
                """## 3. KV Cache 分层卸载

显存不够时，将冷 KV 放到 CPU/NVMe/远端内存；命中时再换入。

权衡：卸载节省 GPU 显存 → 提高并发；换入增加 TPOT。适合多轮长会话中的历史前缀。"""
            ),
            code(
                """class TieredKVCache:
    def __init__(self, gpu_blocks=16, cpu_blocks=64, block_tokens=16):
        self.block_tokens = block_tokens
        self.gpu = {}  # block_id -> tensor
        self.cpu = {}
        self.gpu_blocks = gpu_blocks
        self.cpu_blocks = cpu_blocks
        self.hits = 0
        self.miss_fetch = 0

    def _nbytes(self, n_blocks, d=64, layers=4):
        return n_blocks * self.block_tokens * d * layers * 2 * 2  # K,V fp16

    def put(self, session, tokens):
        n_blocks = (len(tokens) + self.block_tokens - 1) // self.block_tokens
        for b in range(n_blocks):
            key = (session, b)
            payload = torch.randn(self.block_tokens, 64)
            if len(self.gpu) < self.gpu_blocks:
                self.gpu[key] = payload
            elif len(self.cpu) < self.cpu_blocks:
                self.cpu[key] = payload
            else:
                # evict oldest cpu
                self.cpu.pop(next(iter(self.cpu)))
                self.cpu[key] = payload

    def get(self, session, block_id):
        key = (session, block_id)
        if key in self.gpu:
            self.hits += 1
            return self.gpu[key]
        if key in self.cpu:
            self.miss_fetch += 1
            # promote to gpu
            tensor = self.cpu.pop(key)
            if len(self.gpu) >= self.gpu_blocks:
                # demote one gpu block
                old_k = next(iter(self.gpu))
                self.cpu[old_k] = self.gpu.pop(old_k)
            self.gpu[key] = tensor
            return tensor
        return None


cache = TieredKVCache()
for s in range(6):
    cache.put(f'sess-{s}', list(range(80 + 10 * s)))

for s in range(6):
    cache.get(f'sess-{s}', 0)
    cache.get(f'sess-{s}', 1)

print('=== Tiered KV Cache ===')
print(f'GPU blocks used: {len(cache.gpu)} / {cache.gpu_blocks}')
print(f'CPU blocks used: {len(cache.cpu)} / {cache.cpu_blocks}')
print(f'GPU hits: {cache.hits}, CPU promotions: {cache.miss_fetch}')
print(f'Approx GPU KV bytes: {cache._nbytes(len(cache.gpu))/1024:.1f} KB (toy dims)')
print(f'\\nKey: Tiered KV raises concurrency; promotions must be overlapped with compute to hide latency.')"""
            ),
            thinking(
                "9.9 Prefill/Decode 分离与 KV 卸载",
                "什么样的流量形态（短提示长生成 / 长提示短生成）从 PD 分离中收益最大？",
                "KV 跨节点传输成为瓶颈时，有哪些缓解（量化 KV、前缀缓存、同机共享内存）？",
                "PD 分离与 Continuous Batching、前缀缓存如何协同设计？",
                "卸载到 CPU 后，如何设定换入换出策略避免抖动？",
            ),
        ],
    )

    # ------------------------------------------------------------------
    # 07.6 Process supervision
    # ------------------------------------------------------------------
    write_nb(
        "07_alignment_training/06_process_supervision.ipynb",
        [
            md(
                """# 7.6 过程监督与可验证奖励 (Process Supervision)

> 🕐 预估学习时间：40分钟

Outcome Reward（ORM）只看最终答案；Process Reward（PRM）给每一步推理打分。结合可验证奖励（单元测试、数学判定器）是 o1 / DeepSeek-R1 类推理模型的关键训练信号。

本节涵盖：
- ORM vs PRM
- 步骤级标注与自动噪声标签
- 可验证奖励（Verifiable Rewards）
- 与 GRPO / Test-Time Compute 的配合"""
            ),
            md(
                """## 1. ORM vs PRM

| | ORM | PRM |
|-|-----|-----|
| 监督粒度 | 整条轨迹 | 每个推理步 |
| 信用分配 | 难 | 易 |
| 标注成本 | 低 | 高（可用自动判定缓解） |
| 搜索友好 | Best-of-N | 逐步引导 / 树搜索 |"""
            ),
            code(
                """import torch
import torch.nn as nn
import torch.nn.functional as F

torch.manual_seed(42)


class ORM(nn.Module):
    def __init__(self, d=32):
        super().__init__()
        self.enc = nn.GRU(d, d, batch_first=True)
        self.head = nn.Linear(d, 1)

    def forward(self, steps):
        # steps: (B, T, d)
        _, h = self.enc(steps)
        return self.head(h[-1]).squeeze(-1)


class PRM(nn.Module):
    def __init__(self, d=32):
        super().__init__()
        self.enc = nn.GRU(d, d, batch_first=True)
        self.head = nn.Linear(d, 1)

    def forward(self, steps):
        h, _ = self.enc(steps)
        return self.head(h).squeeze(-1)  # (B, T)


d, T, B = 32, 6, 16
# Synthetic trajectories: early mistake should be blamed by PRM
steps = torch.randn(B, T, d)
step_labels = torch.ones(B, T)
step_labels[:, 3:] = 0  # error from step 3 onward
outcome = (step_labels[:, -1] > 0.5).float()

orm = ORM(d)
prm = PRM(d)
opt = torch.optim.Adam(list(orm.parameters()) + list(prm.parameters()), lr=1e-2)

print('=== ORM vs PRM Training ===')
for step in range(80):
    o_pred = orm(steps)
    p_pred = prm(steps)
    loss_o = F.binary_cross_entropy_with_logits(o_pred, outcome)
    loss_p = F.binary_cross_entropy_with_logits(p_pred, step_labels)
    loss = loss_o + loss_p
    opt.zero_grad()
    loss.backward()
    opt.step()
    if step % 20 == 0 or step == 79:
        print(f'step={step:02d} orm_loss={loss_o.item():.4f} prm_loss={loss_p.item():.4f}')

with torch.no_grad():
    p = torch.sigmoid(prm(steps[:1]))[0]
print(f'\\nPRM step probs (expect drop after error): {[f\"{x:.2f}\" for x in p.tolist()]}')
print(f'Key: PRM localizes credit to the failing step; ORM only knows the trajectory failed.')"""
            ),
            md(
                """## 2. 可验证奖励（Verifiable Rewards）

对数学、代码、形式推理，可用确定性判定器给 0/1 奖励，避免奖励模型黑客：

- 数学：符号等价 / 数值容差
- 代码：单测沙箱
- 工具调用：schema + 执行成功

工业上常 **可验证奖励为主，PRM/ORM 为辅**（覆盖不可自动判定的开放任务）。"""
            ),
            code(
                """def math_verifier(pred: str, gold: str, tol=1e-6) -> float:
    try:
        p = float(pred.strip())
        g = float(gold.strip())
        return 1.0 if abs(p - g) <= tol else 0.0
    except Exception:
        return 1.0 if pred.strip() == gold.strip() else 0.0


def code_verifier(fn, tests) -> float:
    try:
        for args, expected in tests:
            if fn(*args) != expected:
                return 0.0
        return 1.0
    except Exception:
        return 0.0


def add(a, b):
    return a + b


print('=== Verifiable Rewards ===')
print('math:', math_verifier('42', '42.0'), math_verifier('41', '42'))
print('code:', code_verifier(add, [((1, 2), 3), ((0, 5), 5)]))

# Group advantages for GRPO-style update using verifier rewards
rewards = torch.tensor([1., 0., 1., 0., 0., 1., 0., 1.])
adv = (rewards - rewards.mean()) / (rewards.std(unbiased=False) + 1e-8)
print(f'group rewards={rewards.tolist()}')
print(f'group advantages={adv.tolist()}')
print(f'\\nKey: Verifier rewards are hard to hack and plug directly into GRPO/RLOO group advantages.')"""
            ),
            md(
                """## 3. 与 Test-Time Compute 的闭环

训练：PRM / 可验证奖励 → GRPO  
推理：Best-of-N / 树搜索 用同一 PRM 打分  

这样训练信号与推理搜索目标一致，避免"训推不一致"。"""
            ),
            code(
                """def best_of_n(candidates, prm_scores):
    # candidates: list[str], prm_scores: (N, T) step probs -> use min step as trajectory score
    traj_score = prm_scores.min(dim=-1).values
    best = int(traj_score.argmax())
    return best, traj_score


cand_scores = torch.tensor([
    [0.9, 0.9, 0.8, 0.8],
    [0.95, 0.2, 0.9, 0.9],  # early mistake
    [0.85, 0.85, 0.85, 0.84],
])
idx, scores = best_of_n(['A', 'B', 'C'], cand_scores)
print('=== PRM-guided Best-of-N ===')
print(f'trajectory scores={scores.tolist()}')
print(f'selected={idx}')
print(f'Key: Min-step aggregation is conservative and prefers consistently correct chains.')"""
            ),
            thinking(
                "7.6 过程监督与可验证奖励",
                "为何仅用 ORM + 长 CoT 容易出现奖励黑客？PRM/验证器如何缓解？",
                "开放域写作任务没有金标时，如何混合 RLAIF 与过程监督？",
                "Best-of-N 用 min/ mean/ last-step 聚合 PRM，各有什么偏差？",
                "过程监督数据如何用自动错误注入廉价生成？噪声如何控制？",
            ),
        ],
    )

    # ------------------------------------------------------------------
    # 11.5 Embedding training
    # ------------------------------------------------------------------
    write_nb(
        "11_rag/05_embedding_training.ipynb",
        [
            md(
                """# 11.5 Embedding / Reranker 训练

> 🕐 预估学习时间：40分钟

RAG 质量上限很大程度上取决于嵌入与重排模型，而不仅是生成模型。本节用对比学习训练双塔检索器，并用 Cross-Encoder 做重排。

本节涵盖：
- 双塔 Dense Retriever
- InfoNCE / in-batch negatives
- Hard Negative Mining
- Cross-Encoder Reranker
- 与生成模型的联合评估"""
            ),
            md(
                """## 1. 双塔检索器 + InfoNCE

查询塔与文档塔共享或分离编码器，用 in-batch 负样本做对比学习。"""
            ),
            code(
                """import torch
import torch.nn as nn
import torch.nn.functional as F

torch.manual_seed(42)


class MeanPoolEncoder(nn.Module):
    def __init__(self, vocab=200, d=64):
        super().__init__()
        self.emb = nn.Embedding(vocab, d)
        self.proj = nn.Linear(d, d)

    def forward(self, ids, mask):
        x = self.emb(ids)
        x = x * mask.unsqueeze(-1)
        pooled = x.sum(1) / mask.sum(1, keepdim=True).clamp_min(1)
        return F.normalize(self.proj(pooled), dim=-1)


def info_nce(q, d, temperature=0.05):
    logits = (q @ d.T) / temperature
    labels = torch.arange(q.size(0), device=q.device)
    return F.cross_entropy(logits, labels)


enc_q = MeanPoolEncoder()
enc_d = MeanPoolEncoder()
opt = torch.optim.Adam(list(enc_q.parameters()) + list(enc_d.parameters()), lr=1e-3)

print('=== Dual-Encoder InfoNCE ===')
for step in range(60):
    q_ids = torch.randint(0, 200, (32, 12))
    d_ids = torch.randint(0, 200, (32, 20))
    # plant a shared token to create weak positives
    shared = torch.randint(0, 200, (32, 1))
    q_ids[:, 0:1] = shared
    d_ids[:, 0:1] = shared
    q_mask = torch.ones_like(q_ids)
    d_mask = torch.ones_like(d_ids)
    q = enc_q(q_ids, q_mask)
    d = enc_d(d_ids, d_mask)
    loss = info_nce(q, d)
    opt.zero_grad()
    loss.backward()
    opt.step()
    if step % 15 == 0 or step == 59:
        with torch.no_grad():
            acc = (q @ d.T).argmax(-1).eq(torch.arange(32)).float().mean().item()
        print(f'step={step:02d} loss={loss.item():.4f} inbatch_acc={acc:.3f}')

print(f'\\nKey: In-batch negatives make dual-encoder training scalable; temperature controls sharpness.')"""
            ),
            md(
                """## 2. Hard Negative Mining

随机负样本太易区分；用当前模型检索到的高分错误文档做难负样本，可显著提升分辨力。"""
            ),
            code(
                """# Build a tiny corpus and mine hard negatives for a query batch
corpus_ids = torch.randint(0, 200, (200, 20))
corpus_mask = torch.ones_like(corpus_ids)
with torch.no_grad():
    corpus_vec = enc_d(corpus_ids, corpus_mask)

q_ids = torch.randint(0, 200, (8, 12))
q_ids[:, 0] = corpus_ids[:8, 0]  # positives = first 8 docs
q_mask = torch.ones_like(q_ids)
with torch.no_grad():
    q_vec = enc_q(q_ids, q_mask)
    sims = q_vec @ corpus_vec.T
    # top-3 including positive; pick highest non-positive as hard negative
    hard_negs = []
    for i in range(8):
        ranked = sims[i].argsort(descending=True).tolist()
        hard = next(j for j in ranked if j != i)
        hard_negs.append(hard)
print('=== Hard Negatives ===')
print(f'hard neg doc ids: {hard_negs}')
print(f'mean sim(q, pos)={[round((q_vec[i]@corpus_vec[i]).item(),3) for i in range(4)]}')
print(f'mean sim(q, hard)={[round((q_vec[i]@corpus_vec[hard_negs[i]]).item(),3) for i in range(4)]}')
print(f'\\nKey: Hard negatives sit near the decision boundary and improve retrieval ranking quality.')"""
            ),
            md(
                """## 3. Cross-Encoder 重排

双塔快但未建模细交互；对 Top-K 候选用 Cross-Encoder 逐对打分重排。"""
            ),
            code(
                """class CrossEncoder(nn.Module):
    def __init__(self, vocab=200, d=64):
        super().__init__()
        self.emb = nn.Embedding(vocab, d)
        self.encoder = nn.TransformerEncoder(
            nn.TransformerEncoderLayer(d, 4, 128, batch_first=True), 2
        )
        self.head = nn.Linear(d, 1)

    def forward(self, pair_ids, mask):
        x = self.emb(pair_ids)
        x = self.encoder(x, src_key_padding_mask=~mask.bool())
        pooled = (x * mask.unsqueeze(-1)).sum(1) / mask.sum(1, keepdim=True).clamp_min(1)
        return self.head(pooled).squeeze(-1)


ce = CrossEncoder()
opt_ce = torch.optim.Adam(ce.parameters(), lr=1e-3)
print('=== Cross-Encoder Reranker ===')
for step in range(40):
    # positive pairs vs random negatives
    pos_q = torch.randint(0, 200, (16, 8))
    pos_d = torch.randint(0, 200, (16, 12))
    neg_d = torch.randint(0, 200, (16, 12))
    pos_q[:, 0] = 1
    pos_d[:, 0] = 1  # shared marker
    pos_pair = torch.cat([pos_q, pos_d], dim=1)
    neg_pair = torch.cat([pos_q, neg_d], dim=1)
    mask = torch.ones(16, pos_pair.size(1))
    s_pos = ce(pos_pair, mask)
    s_neg = ce(neg_pair, mask)
    # pairwise logistic
    loss = -F.logsigmoid(s_pos - s_neg).mean()
    opt_ce.zero_grad()
    loss.backward()
    opt_ce.step()
    if step % 10 == 0 or step == 39:
        acc = (s_pos > s_neg).float().mean().item()
        print(f'step={step:02d} loss={loss.item():.4f} pairwise_acc={acc:.3f}')

print(f'\\nKey: Retrieve wide with dual-encoder, then rerank narrow with cross-encoder.')"""
            ),
            thinking(
                "11.5 Embedding / Reranker 训练",
                "in-batch negative 在小 batch 或同质语料下有什么缺陷？如何补救？",
                "Hard negative 过难（假阴性）时会怎样？如何过滤？",
                "何时该训练领域嵌入，而不是直接用通用 BGE/E5？",
                "如何用 nDCG/Recall@K 与下游 RAG 答案正确率做联合选模？",
            ),
        ],
    )

    # ------------------------------------------------------------------
    # 16.5 Guardrails
    # ------------------------------------------------------------------
    write_nb(
        "16_security_robustness/05_guardrails.ipynb",
        [
            md(
                """# 16.5 生产级安全护栏 (Guardrails)

> 🕐 预估学习时间：35分钟

生产系统通常在模型外挂多层护栏：输入分类、输出审查、工具权限、策略引擎（如 Llama Guard、NeMo Guardrails、正则/规则）。护栏与对齐微调互补，可热更新。

本节涵盖：
- 分层护栏架构
- 输入/输出安全分类器
- 策略即代码（允许/拒绝/改写）
- 越狱鲁棒性评估回路"""
            ),
            md(
                """## 1. 分层护栏架构

```
User -> Input Filter -> LLM -> Output Filter -> Tool Firewall -> User
              |                     |                |
           policy DB            safety CLS      allowlist/sandbox
```"""
            ),
            code(
                """import re
import torch
import torch.nn as nn
import torch.nn.functional as F

torch.manual_seed(42)


class SafetyClassifier(nn.Module):
    def __init__(self, vocab=1000, d=64, n_classes=4):
        super().__init__()
        self.emb = nn.Embedding(vocab, d)
        self.fc = nn.Linear(d, n_classes)
        # 0=ok, 1=jailbreak, 2=toxic, 3=pii

    def forward(self, ids):
        x = self.emb(ids).mean(1)
        return self.fc(x)


def rule_pii_scan(text: str) -> bool:
    patterns = [
        r'\\b\\d{3}-\\d{2}-\\d{4}\\b',  # SSN-like
        r'\\b[\\w.-]+@[\\w.-]+\\.\\w+\\b',
        r'\\b1[3-9]\\d{9}\\b',  # CN phone-like
    ]
    return any(re.search(p, text) for p in patterns)


cls = SafetyClassifier()
# toy train
opt = torch.optim.Adam(cls.parameters(), lr=1e-2)
print('=== Safety Classifier Toy Train ===')
for step in range(50):
    ids = torch.randint(0, 1000, (32, 20))
    labels = torch.randint(0, 4, (32,))
    loss = F.cross_entropy(cls(ids), labels)
    opt.zero_grad(); loss.backward(); opt.step()
    if step % 25 == 0 or step == 49:
        print(f'step={step} loss={loss.item():.4f}')

print('PII scan:', rule_pii_scan('contact me at alice@example.com'))
print(f'Key: Combine cheap rules for PII/format with learned classifiers for semantics.')"""
            ),
            md(
                """## 2. 策略引擎：允许 / 拒绝 / 改写

对分类结果映射动作，而不是只返回布尔值。"""
            ),
            code(
                """ACTIONS = {
    0: 'allow',
    1: 'block',
    2: 'block',
    3: 'redact',
}


def redact(text: str) -> str:
    text = re.sub(r'[\\w.-]+@[\\w.-]+\\.\\w+', '[EMAIL]', text)
    text = re.sub(r'\\b1[3-9]\\d{9}\\b', '[PHONE]', text)
    return text


def guardrail_pipeline(text: str, ids: torch.Tensor, model: SafetyClassifier):
    if rule_pii_scan(text):
        return {'action': 'redact', 'output': redact(text), 'reason': 'rule_pii'}
    with torch.no_grad():
        pred = int(model(ids).argmax(-1).item())
    action = ACTIONS[pred]
    if action == 'allow':
        return {'action': 'allow', 'output': text, 'reason': f'cls={pred}'}
    if action == 'redact':
        return {'action': 'redact', 'output': redact(text), 'reason': f'cls={pred}'}
    return {'action': 'block', 'output': '请求已被安全策略拦截。', 'reason': f'cls={pred}'}


samples = [
    ('正常问天气', torch.randint(0, 1000, (1, 16))),
    ('my email is bob@corp.com', torch.randint(0, 1000, (1, 16))),
]
print('=== Policy Engine ===')
for text, ids in samples:
    print(text, '->', guardrail_pipeline(text, ids, cls))
print(f'\\nKey: Actionable policies (allow/block/redact/rewrite) are more operable than binary filters.')"""
            ),
            md(
                """## 3. 工具防火墙与评估回路

Agent 场景必须限制工具参数与副作用：路径白名单、SQL 只读、网络 egress 控制。

护栏需像模型一样做回归评测：固定越狱集 + 误拦截集，跟踪 block rate / false positive。"""
            ),
            code(
                """class ToolFirewall:
    def __init__(self):
        self.allowed = {
            'search': {'q': str},
            'sql_read': {'query': str},
        }
        self.sql_deny = re.compile(r'\\b(drop|delete|update|insert|alter)\\b', re.I)

    def check(self, tool, args):
        if tool not in self.allowed:
            return False, 'tool_not_allowed'
        schema = self.allowed[tool]
        if set(args) != set(schema):
            return False, 'bad_args'
        if tool == 'sql_read' and self.sql_deny.search(args['query']):
            return False, 'sql_mutation_denied'
        return True, 'ok'


fw = ToolFirewall()
print('=== Tool Firewall ===')
for call in [
    ('search', {'q': 'llm guardrails'}),
    ('sql_read', {'query': 'SELECT * FROM users'}),
    ('sql_read', {'query': 'DROP TABLE users'}),
    ('bash', {'cmd': 'rm -rf /'}),
]:
    print(call, '->', fw.check(*call))

# Simple regression metrics
y_true = [1, 1, 0, 0]  # 1=should_block
y_pred = [1, 0, 0, 1]
tp = sum(t == 1 and p == 1 for t, p in zip(y_true, y_pred))
fp = sum(t == 0 and p == 1 for t, p in zip(y_true, y_pred))
fn = sum(t == 1 and p == 0 for t, p in zip(y_true, y_pred))
prec = tp / max(tp + fp, 1)
rec = tp / max(tp + fn, 1)
print(f'guardrail precision={prec:.2f}, recall={rec:.2f}')
print(f'\\nKey: Treat guardrails as a product surface with precision/recall SLOs, not a one-off filter.')"""
            ),
            thinking(
                "16.5 生产级安全护栏",
                "护栏误拦截（false positive）过高会怎样伤害产品？如何分层放宽？",
                "模型内对齐与外挂护栏的职责边界如何划分？",
                "对多模态 / Agent 工具调用，护栏要新增哪些控制点？",
                "如何搭建持续的越狱回归集并防止评测集污染？",
            ),
        ],
    )

    # ------------------------------------------------------------------
    # 18.7 Semantic caching
    # ------------------------------------------------------------------
    write_nb(
        "18_mlops/07_semantic_caching.ipynb",
        [
            md(
                """# 18.7 语义缓存 (Semantic Caching)

> 🕐 预估学习时间：30分钟

对语义相近的请求复用历史回答或 KV/检索结果，可显著降低成本与延迟。与精确字符串缓存不同，语义缓存用嵌入相似度判定命中。

本节涵盖：
- 精确缓存 vs 语义缓存
- 相似度阈值与风险
- 缓存分层（答案缓存 / 检索缓存 / 前缀 KV）
- 失效、租户隔离与评测"""
            ),
            md(
                """## 1. 语义命中判定

对查询做嵌入，若与缓存键的余弦相似度 ≥ τ 则命中。τ 过高降命中率，过低导致错误复用。"""
            ),
            code(
                """import torch
import torch.nn.functional as F
import time

torch.manual_seed(42)


class SemanticCache:
    def __init__(self, dim=64, threshold=0.88, max_size=100):
        self.threshold = threshold
        self.max_size = max_size
        self.keys = []    # tensors
        self.values = []  # payloads
        self.hits = 0
        self.misses = 0

    def _sim(self, q, k):
        return F.cosine_similarity(q.unsqueeze(0), k.unsqueeze(0)).item()

    def get(self, q_emb):
        best_i, best_s = -1, -1.0
        for i, k in enumerate(self.keys):
            s = self._sim(q_emb, k)
            if s > best_s:
                best_i, best_s = i, s
        if best_s >= self.threshold:
            self.hits += 1
            return self.values[best_i], best_s
        self.misses += 1
        return None, best_s

    def put(self, q_emb, value):
        if len(self.keys) >= self.max_size:
            self.keys.pop(0)
            self.values.pop(0)
        self.keys.append(q_emb.detach().cpu())
        self.values.append(value)


cache = SemanticCache(threshold=0.9)
base = F.normalize(torch.randn(64), dim=0)
cache.put(base, 'answer-about-lora')

# near duplicate
q_near = F.normalize(base + 0.01 * torch.randn(64), dim=0)
q_far = F.normalize(torch.randn(64), dim=0)
print('=== Semantic Cache Lookup ===')
print('near:', cache.get(q_near))
print('far:', cache.get(q_far))
print(f'hit_rate={cache.hits/(cache.hits+cache.misses):.2f}')
print(f'Key: Threshold τ is a safety-critical knob; tune on paraphrase/adversarial eval sets.')"""
            ),
            md(
                """## 2. 分层缓存策略

| 层 | 缓存对象 | 命中收益 | 风险 |
|----|---------|---------|------|
| L0 精确 | 规范化后的字符串 | 极低风险 | 命中率低 |
| L1 语义答案 | 最终回复 | 高 | 事实过期/个性化串味 |
| L2 检索结果 | Top-K 文档 | 中 | 语料更新需失效 |
| L3 前缀 KV | 系统提示 KV | 高 | 与引擎耦合 |

个性化、含工具结果或强时效问题应 bypass 或短 TTL。"""
            ),
            code(
                """class LayeredCache:
    def __init__(self):
        self.exact = {}
        self.semantic = SemanticCache(threshold=0.92)
        self.retrieval = SemanticCache(threshold=0.9)

    def normalize(self, q: str) -> str:
        return ' '.join(q.lower().strip().split())

    def answer(self, query: str, embed_fn, generate_fn, retrieve_fn):
        key = self.normalize(query)
        if key in self.exact:
            return self.exact[key], 'exact'
        emb = embed_fn(query)
        hit, score = self.semantic.get(emb)
        if hit is not None:
            return hit, f'semantic:{score:.3f}'
        docs, dtype = None, None
        d_hit, d_score = self.retrieval.get(emb)
        if d_hit is not None:
            docs, dtype = d_hit, f'retrieval_cache:{d_score:.3f}'
        else:
            docs = retrieve_fn(query)
            self.retrieval.put(emb, docs)
            dtype = 'retrieval_fresh'
        ans = generate_fn(query, docs)
        self.exact[key] = ans
        self.semantic.put(emb, ans)
        return ans, dtype


def embed_fn(q):
    g = torch.Generator().manual_seed(sum(map(ord, q)) % (2**31))
    return F.normalize(torch.randn(64, generator=g), dim=0)

def retrieve_fn(q):
    return [f'doc-for:{q[:12]}']

def generate_fn(q, docs):
    return f'ans({q[:16]}) relying on {docs[0]}'

lc = LayeredCache()
print('=== Layered Cache ===')
a1, s1 = lc.answer('What is LoRA?', embed_fn, generate_fn, retrieve_fn)
a2, s2 = lc.answer('what is lora?', embed_fn, generate_fn, retrieve_fn)
a3, s3 = lc.answer('What is LoRA fine-tuning?', embed_fn, generate_fn, retrieve_fn)
print(s1, '->', a1)
print(s2, '->', a2)
print(s3, '->', a3)
print(f'\\nKey: Exact cache catches normalization duplicates; semantic cache catches paraphrases; retrieval cache saves vector DB cost.')"""
            ),
            md(
                """## 3. 评测与失效

必须监控：命中率、错误复用率、TTL 命中贡献、每租户隔离。

失效触发：知识库更新、政策变更、模型版本切换、安全事件。"""
            ),
            code(
                """def evaluate_threshold(paraphrase_pairs, unrelated_pairs, embed_fn, thresholds):
    print(f'{\"τ\":>6} {\"para_hit\":>10} {\"false_hit\":>10}')
    for t in thresholds:
        c = SemanticCache(threshold=t)
        # populate with left side
        for a, _ in paraphrase_pairs + unrelated_pairs:
            c.put(embed_fn(a), f'ans:{a}')
        # reset counters
        c.hits = c.misses = 0
        para_hit = 0
        for a, b in paraphrase_pairs:
            # fresh cache per lookup population already has a
            val, _ = c.get(embed_fn(b))
            para_hit += int(val is not None)
        false_hit = 0
        # rebuild for fair false-hit measurement
        c2 = SemanticCache(threshold=t)
        for a, _ in unrelated_pairs:
            c2.put(embed_fn(a), f'ans:{a}')
        for a, b in unrelated_pairs:
            val, _ = c2.get(embed_fn(b))
            false_hit += int(val is not None)
        print(f'{t:>6.2f} {para_hit/len(paraphrase_pairs):>10.2f} {false_hit/len(unrelated_pairs):>10.2f}')


pairs_para = [('lora tuning', 'lo-ra fine tuning'), ('kv cache', 'key value caching')]
pairs_unrel = [('lora tuning', 'pancake recipe'), ('kv cache', 'stock market')]
evaluate_threshold(pairs_para, pairs_unrel, embed_fn, [0.7, 0.8, 0.9, 0.95])
print(f'\\nKey: Choose τ on the Pareto frontier of paraphrase hit rate vs false-hit rate.')"""
            ),
            thinking(
                "18.7 语义缓存",
                "哪些请求类型绝对不应语义缓存？如何在网关层识别？",
                "多租户下语义缓存如何防止跨租户答案泄漏？",
                "语义缓存与前缀 KV 缓存、CDN 缓存在职责上如何划分？",
                "知识库更新后如何做细粒度失效而不是清空全站缓存？",
            ),
        ],
    )

    print("done")


if __name__ == "__main__":
    build_all()
