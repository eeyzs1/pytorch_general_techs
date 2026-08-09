#!/usr/bin/env python3
"""Generate second-round supplemental notebooks."""

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
    nb = {"cells": cells, "metadata": NB_META, "nbformat": 4, "nbformat_minor": 4}
    path.write_text(json.dumps(nb, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"wrote {rel_path}")


def thinking(section: str, *qs: str) -> dict:
    body = "\n".join(f"{i}. {q}" for i, q in enumerate(qs, 1))
    return md(
        f"""## 课后思考题

{body}

---
> 本节涵盖了{section}的核心概念与代码实现。建议结合实际项目需求，选择合适的技术方案，并通过实验验证不同方法的效果差异。"""
    )


def build_all() -> None:
    # ------------------------------------------------------------------
    # 00.1 Advanced optimizers
    # ------------------------------------------------------------------
    write_nb(
        "00_foundations/01_advanced_optimizers.ipynb",
        [
            md(
                """# 0.1 前沿优化器 (Advanced Optimizers)

> 🕐 预估学习时间：40分钟

AdamW 仍是 LLM 默认优化器，但 2024–2026 出现一批面向大规模训练的新选择：Lion、Sophia、Muon、SOAP 等，在收敛速度、显存与稳定性上各有取舍。

本节涵盖：
- AdamW 基线回顾
- Lion / Sophia 的更新规则
- Muon（正交化动量）简化实现
- SOAP / Shampoo 族直觉
- 选型建议"""
            ),
            md(
                """## 1. AdamW 基线

AdamW = 一阶动量 + 二阶自适应 + **解耦权重衰减**。大模型训练的事实标准，但二阶统计量占用额外显存，且对某些矩阵结构参数未必最优。"""
            ),
            code(
                """import torch
import torch.nn as nn
import torch.nn.functional as F
import math
import copy

torch.manual_seed(42)


class TinyLM(nn.Module):
    def __init__(self, vocab=64, d=32):
        super().__init__()
        self.embed = nn.Embedding(vocab, d)
        self.fc = nn.Linear(d, vocab)

    def forward(self, x):
        return self.fc(self.embed(x).mean(1))


def make_batch(n=64, t=8, vocab=64):
    x = torch.randint(0, vocab, (n, t))
    y = torch.randint(0, vocab, (n,))
    return x, y


def train_steps(model, opt, steps=40):
    losses = []
    for _ in range(steps):
        x, y = make_batch()
        loss = F.cross_entropy(model(x), y)
        opt.zero_grad()
        loss.backward()
        opt.step()
        losses.append(loss.item())
    return losses


base = TinyLM()
m = copy.deepcopy(base)
opt = torch.optim.AdamW(m.parameters(), lr=3e-3, weight_decay=0.01)
adamw_losses = train_steps(m, opt)
print('=== AdamW Baseline ===')
print(f'loss start={adamw_losses[0]:.4f} mid={adamw_losses[20]:.4f} end={adamw_losses[-1]:.4f}')
print(f'Key: AdamW remains the default; new optimizers must beat it on wall-clock or stability.')"""
            ),
            md(
                """## 2. Lion：符号动量，省显存

Lion 用动量的符号更新参数，几乎不存二阶统计，更新幅度更离散。适合大批次、需要省优化器状态的场景。

$$\\theta \\leftarrow \\theta - \\eta \\cdot \\mathrm{sign}(m) - \\eta\\lambda\\theta$$"""
            ),
            code(
                """class Lion(torch.optim.Optimizer):
    def __init__(self, params, lr=1e-4, betas=(0.9, 0.99), weight_decay=0.0):
        super().__init__(params, dict(lr=lr, betas=betas, weight_decay=weight_decay))

    @torch.no_grad()
    def step(self):
        for group in self.param_groups:
            beta1, beta2 = group['betas']
            for p in group['params']:
                if p.grad is None:
                    continue
                grad = p.grad
                state = self.state[p]
                if len(state) == 0:
                    state['exp_avg'] = torch.zeros_like(p)
                exp_avg = state['exp_avg']
                update = exp_avg * beta1 + grad * (1 - beta1)
                p.add_(update.sign(), alpha=-group['lr'])
                if group['weight_decay'] != 0:
                    p.add_(p, alpha=-group['lr'] * group['weight_decay'])
                exp_avg.mul_(beta2).add_(grad, alpha=1 - beta2)


m = copy.deepcopy(base)
lion_losses = train_steps(m, Lion(m.parameters(), lr=1e-3, weight_decay=0.01))
print('=== Lion ===')
print(f'loss start={lion_losses[0]:.4f} end={lion_losses[-1]:.4f}')
print(f'optimizer state bytes ~ 1x params (momentum only), vs AdamW ~2x')
print(f'Key: Lion trades second-moment adaptivity for lower memory and sign-based updates.')"""
            ),
            md(
                """## 3. Sophia：对角 Hessian 近似

Sophia 用对角二阶信息缩放梯度（可用 Gauss-Newton / Hutchinson 估计），并做裁剪防止过大步长。对 LLM 预训练有报告显示可减少步数。"""
            ),
            code(
                """class SophiaG(torch.optim.Optimizer):
    '''Educational Sophia-G: EMA of grad^2 as diagonal curvature proxy.'''
    def __init__(self, params, lr=1e-3, betas=(0.965, 0.99), rho=0.04, weight_decay=0.01):
        super().__init__(params, dict(lr=lr, betas=betas, rho=rho, weight_decay=weight_decay))

    @torch.no_grad()
    def step(self):
        for group in self.param_groups:
            beta1, beta2 = group['betas']
            for p in group['params']:
                if p.grad is None:
                    continue
                grad = p.grad
                state = self.state[p]
                if len(state) == 0:
                    state['m'] = torch.zeros_like(p)
                    state['h'] = torch.zeros_like(p)
                m, h = state['m'], state['h']
                m.mul_(beta1).add_(grad, alpha=1 - beta1)
                h.mul_(beta2).addcmul_(grad, grad, value=1 - beta2)
                if group['weight_decay'] != 0:
                    p.mul_(1 - group['lr'] * group['weight_decay'])
                # update = clip(m / max(h, eps), +/- rho)
                denom = h.clamp_min(1e-12)
                update = (m / denom).clamp(-group['rho'], group['rho'])
                p.add_(update, alpha=-group['lr'])


m = copy.deepcopy(base)
sophia_losses = train_steps(m, SophiaG(m.parameters(), lr=3e-3))
print('=== Sophia-G (toy) ===')
print(f'loss start={sophia_losses[0]:.4f} end={sophia_losses[-1]:.4f}')
print(f'Key: Sophia scales steps by curvature proxy and clips; useful when AdamW needs many tokens.')"""
            ),
            md(
                """## 4. Muon：对二维参数做正交化动量

Muon 把矩阵参数的动量做 Newton–Schulz 风格正交化，使更新更接近“谱友好”的方向，在中等规模 LLM 实验中表现突出。偏置/一维参数通常仍用 AdamW。"""
            ),
            code(
                """def newton_schulz_orthogonalize(G, steps=5):
    '''Approximate polar factor / orthogonalize a matrix via Newton-Schulz.'''
    X = G / (G.norm() + 1e-8)
    if G.size(0) > G.size(1):
        X = X.T
        transposed = True
    else:
        transposed = False
    for _ in range(steps):
        A = X @ X.T
        B = A @ X
        X = 1.5 * X - 0.5 * B
    if transposed:
        X = X.T
    return X


class Muon(torch.optim.Optimizer):
    def __init__(self, params, lr=0.02, momentum=0.95, nesterov=True):
        super().__init__(params, dict(lr=lr, momentum=momentum, nesterov=nesterov))

    @torch.no_grad()
    def step(self):
        for group in self.param_groups:
            for p in group['params']:
                if p.grad is None:
                    continue
                g = p.grad
                state = self.state[p]
                if len(state) == 0:
                    state['buf'] = torch.zeros_like(g)
                buf = state['buf']
                buf.mul_(group['momentum']).add_(g)
                update = g.add(buf, alpha=group['momentum']) if group['nesterov'] else buf
                if update.ndim == 2:
                    update = newton_schulz_orthogonalize(update)
                else:
                    update = update / (update.norm() + 1e-8)
                p.add_(update, alpha=-group['lr'])


m = copy.deepcopy(base)
# Muon for 2D weights, AdamW for embeddings/biases (simplified: all Muon)
muon_losses = train_steps(m, Muon(m.parameters(), lr=0.05), steps=40)
print('=== Muon ===')
print(f'loss start={muon_losses[0]:.4f} end={muon_losses[-1]:.4f}')
W = m.fc.weight.detach()
print(f'fc weight singular values (top3): {torch.linalg.svdvals(W)[:3].tolist()}')
print(f'Key: Muon orthogonalizes matrix momentum; pair with AdamW for 1D params in practice.')"""
            ),
            md(
                """## 5. SOAP / Shampoo 族直觉与选型

| 优化器 | 核心想法 | 显存 | 典型场景 |
|--------|---------|------|---------|
| AdamW | 对角二阶自适应 | 中 | 通用默认 |
| Lion | 符号动量 | 低 | 省状态、大批次 |
| Sophia | 对角曲率 + 裁剪 | 中 | 减少预训练步数 |
| Muon | 矩阵动量正交化 | 低-中 | 隐藏层矩阵为主 |
| SOAP/Shampoo | 分层预条件 | 高 | 研究/中等规模 |

**实践建议**：先 AdamW 拉通；当 token 预算或稳定性成为瓶颈再 A/B 新优化器；始终固定数据顺序与种子对比。"""
            ),
            code(
                """print('=== Optimizer Comparison (toy CE) ===')
print(f'{\"opt\":<10} {\"start\":>8} {\"end\":>8} {\"delta\":>8}')
for name, losses in [('AdamW', adamw_losses), ('Lion', lion_losses),
                     ('Sophia', sophia_losses), ('Muon', muon_losses)]:
    print(f'{name:<10} {losses[0]:>8.4f} {losses[-1]:>8.4f} {losses[0]-losses[-1]:>8.4f}')
print(f'\\nKey: Toy losses are not ranking evidence; use tokens-to-target on real runs.')"""
            ),
            thinking(
                "0.1 前沿优化器",
                "为什么 Muon 主要作用于二维权重矩阵，而 embedding/LM head 仍常用 AdamW？",
                "Sophia 的 rho 裁剪过大或过小分别会怎样？",
                "在 FSDP/ZeRO-3 下换优化器时，通信与状态分片要注意什么？",
                "如何设计公平的优化器对比实验（数据、调度、数值精度）？",
            ),
        ],
    )

    # ------------------------------------------------------------------
    # 15.6 Uncertainty calibration
    # ------------------------------------------------------------------
    write_nb(
        "15_evaluation/06_uncertainty_calibration.ipynb",
        [
            md(
                """# 15.6 不确定性与校准 (Uncertainty & Calibration)

> 🕐 预估学习时间：35分钟

LLM 常常“自信地错”。不确定性估计与概率校准用于拒答路由、端云协同、评测可信度，是生产质量的关键一环。

本节涵盖：
- 置信度 vs 准确率
- Expected Calibration Error (ECE)
- Temperature Scaling
- 语义熵 / 自一致性不确定性
- 拒答与路由策略"""
            ),
            md(
                """## 1. 可靠性图与 ECE

将样本按置信度分箱，比较每箱平均置信度与实际准确率。ECE 是各箱差距的加权平均。"""
            ),
            code(
                """import torch
import torch.nn.functional as F
import math

torch.manual_seed(0)

# Synthetic overconfident classifier logits
n, c = 1000, 5
logits = torch.randn(n, c) * 3.0
# plant labels correlated but noisy
probs = F.softmax(logits, dim=-1)
pred = probs.argmax(-1)
conf = probs.max(-1).values
# true labels: 60% correct
correct_mask = torch.rand(n) < 0.6
labels = pred.clone()
labels[~correct_mask] = (pred[~correct_mask] + 1) % c
acc = (pred == labels).float().mean().item()


def ece(conf, pred, labels, n_bins=10):
    bins = torch.linspace(0, 1, n_bins + 1)
    ece_val = 0.0
    rows = []
    for i in range(n_bins):
        m = (conf > bins[i]) & (conf <= bins[i + 1])
        if m.sum() == 0:
            rows.append((bins[i].item(), bins[i+1].item(), 0, 0, 0))
            continue
        acc_bin = (pred[m] == labels[m]).float().mean().item()
        conf_bin = conf[m].mean().item()
        ece_val += m.float().mean().item() * abs(acc_bin - conf_bin)
        rows.append((bins[i].item(), bins[i+1].item(), m.sum().item(), acc_bin, conf_bin))
    return ece_val, rows


ece0, rows = ece(conf, pred, labels)
print('=== Calibration Diagnostics ===')
print(f'accuracy={acc:.3f} mean_conf={conf.mean():.3f} ECE={ece0:.4f}')
print(f'{\"bin\":>12} {\"n\":>5} {\"acc\":>7} {\"conf\":>7}')
for lo, hi, n_bin, a, cf in rows:
    if n_bin:
        print(f'{lo:.1f}-{hi:.1f} {n_bin:>5} {a:>7.3f} {cf:>7.3f}')
print(f'\\nKey: Overconfidence shows up as mean_conf >> accuracy and large ECE.')"""
            ),
            md(
                """## 2. Temperature Scaling

在验证集上学习标量温度 T，推理时用 `softmax(logits / T)`。简单、不改模型参数，常作后处理校准。"""
            ),
            code(
                """def nll_with_T(logits, labels, T):
    return F.cross_entropy(logits / T, labels)


T = torch.tensor(1.5, requires_grad=True)
opt = torch.optim.LBFGS([T], lr=0.1, max_iter=50)

def closure():
    opt.zero_grad()
    loss = nll_with_T(logits, labels, T.clamp_min(1e-3))
    loss.backward()
    return loss

opt.step(closure)
T_star = float(T.clamp_min(1e-3))
probs_cal = F.softmax(logits / T_star, dim=-1)
conf_cal = probs_cal.max(-1).values
pred_cal = probs_cal.argmax(-1)
ece1, _ = ece(conf_cal, pred_cal, labels)
print('=== Temperature Scaling ===')
print(f'T*={T_star:.3f}')
print(f'ECE before={ece0:.4f} after={ece1:.4f}')
print(f'mean_conf before={conf.mean():.3f} after={conf_cal.mean():.3f}')
print(f'Key: Temperature scaling often cuts ECE without changing argmax predictions much.')"""
            ),
            md(
                """## 3. 语义熵与自一致性不确定性

对开放生成，token 概率未必等于语义正确概率。可多次采样，按语义聚类后计算熵；或看自一致性投票分散度。"""
            ),
            code(
                """def semantic_entropy(answer_groups):
    '''answer_groups: list of cluster sizes for one question.'''
    total = sum(answer_groups)
    probs = torch.tensor([g / total for g in answer_groups], dtype=torch.float)
    return float(-(probs * probs.clamp_min(1e-12).log()).sum())


def self_consistency_uncertainty(votes):
    # fraction not equal to majority
    from collections import Counter
    c = Counter(votes)
    maj = c.most_common(1)[0][1]
    return 1.0 - maj / len(votes)


print('=== Generative Uncertainty ===')
print('confident math:', semantic_entropy([8, 1, 1]), 'self_cons_u=', self_consistency_uncertainty(['42']*8+['41','40']))
print('ambiguous:', semantic_entropy([3, 3, 2, 2]), 'self_cons_u=', self_consistency_uncertainty(['A','B','A','C','B','D','A','B']))
print(f'\\nKey: Semantic entropy captures answer diversity beyond token-level confidence.')"""
            ),
            md(
                """## 4. 拒答 / 端云路由

高不确定性 → 拒答、要求澄清、或路由到更大模型/人工。阈值应用验证集按成本-风险曲线选择。"""
            ),
            code(
                """def route(confidences, thr_local=0.8, thr_abstain=0.5):
    actions = []
    for c in confidences:
        if c >= thr_local:
            actions.append('local')
        elif c >= thr_abstain:
            actions.append('escalate')
        else:
            actions.append('abstain')
    return actions


# Use calibrated confidences
actions = route(conf_cal[:20].tolist())
from collections import Counter
print('=== Routing on calibrated confidence ===')
print(Counter(actions))
# simulate risk: wrong local answers
local_idx = [i for i, a in enumerate(actions) if a == 'local']
if local_idx:
    local_err = (pred_cal[local_idx] != labels[local_idx]).float().mean().item()
    print(f'local error rate on first-20 slice: {local_err:.3f}')
print(f'\\nKey: Calibration makes confidence thresholds operational for abstention and routing.')"""
            ),
            thinking(
                "15.6 不确定性与校准",
                "为什么 Temperature Scaling 不改变 argmax，却能改善 ECE？",
                "语义熵在“多种正确表述”任务上会高估不确定性吗？如何缓解？",
                "拒答阈值如何同时兼顾用户体验与安全风险？",
                "分类校准方法迁移到工具调用/结构化输出时要注意什么？",
            ),
        ],
    )

    # ------------------------------------------------------------------
    # 04.5 Code pretraining
    # ------------------------------------------------------------------
    write_nb(
        "04_pretraining/05_code_pretraining.ipynb",
        [
            md(
                """# 4.5 代码预训练与专训 (Code Pretraining)

> 🕐 预估学习时间：40分钟

代码模型（CodeLlama、DeepSeek-Coder、Qwen2.5-Coder、StarCoder）在通用 LM 之上强调仓库级上下文、填充式目标、执行反馈与单测驱动。本节用可运行的小例子覆盖核心训练信号。

本节涵盖：
- 代码语料配比与去污
- Causal LM vs FIM（Fill-in-the-Middle）
- 仓库级上下文打包
- 执行反馈 / 单测奖励
- 评测：Pass@k"""
            ),
            md(
                """## 1. 代码语料与配比直觉

| 来源 | 作用 | 风险 |
|------|------|------|
| GitHub/The Stack | 广度 | 许可证、重复、密钥泄漏 |
| 文档/Notebook | 自然语言对齐 | 质量不齐 |
| 合成题解 | 覆盖算法模式 | 分布偏窄 |
| 内部仓 | 企业风格 | 保密与去标识 |

配比时常提高高质量、可运行子集权重，并做密钥/PII 扫描。"""
            ),
            code(
                """import re
import torch
import torch.nn as nn
import torch.nn.functional as F

torch.manual_seed(42)

SECRET_PAT = re.compile(r'(api[_-]?key\\s*=\\s*\\S+|AKIA[0-9A-Z]{16})', re.I)


def clean_code(text: str) -> str | None:
    if SECRET_PAT.search(text):
        return None
    # strip giant minified lines
    lines = [ln for ln in text.splitlines() if len(ln) < 300]
    if len(lines) < 3:
        return None
    return '\\n'.join(lines)


samples = [
    'def add(a,b):\\n    return a+b\\n',
    'api_key = \"sk-secret-123\"\\nprint(api_key)\\n',
    'x=' + 'a'*400 + '\\n',
]
print('=== Code Cleaning ===')
for s in samples:
    out = clean_code(s)
    print(repr(s[:40]), '->', 'KEEP' if out else 'DROP')
print(f'Key: License/PII/secret scanning is mandatory before code pretraining.')"""
            ),
            md(
                """## 2. FIM：Fill-in-the-Middle

编辑器补全常需要根据前缀+后缀填中间。FIM 训练时随机切 `prefix/middle/suffix`，重排为 `prefix + suffix + middle`（或特殊 token 分隔）做自回归。"""
            ),
            code(
                """def fim_pack(tokens, fim_prob=0.5):
    '''tokens: 1D LongTensor. Returns rearranged tokens for FIM or original.'''
    if torch.rand(()) > fim_prob or tokens.numel() < 6:
        return tokens, 'clm'
    n = tokens.numel()
    i = int(torch.randint(1, n - 2, (1,)))
    j = int(torch.randint(i + 1, n - 1, (1,)))
    prefix, middle, suffix = tokens[:i], tokens[i:j], tokens[j:]
    # special ids: 1=<fim_prefix>, 2=<fim_suffix>, 3=<fim_middle>
    packed = torch.cat([
        torch.tensor([1]), prefix,
        torch.tensor([2]), suffix,
        torch.tensor([3]), middle,
    ])
    return packed, 'fim'


class CodeLM(nn.Module):
    def __init__(self, vocab=100, d=64):
        super().__init__()
        self.embed = nn.Embedding(vocab, d)
        self.block = nn.TransformerEncoder(
            nn.TransformerEncoderLayer(d, 4, 128, batch_first=True), 2
        )
        self.head = nn.Linear(d, vocab)

    def forward(self, x):
        h = self.embed(x)
        # causal mask
        T = x.size(1)
        mask = torch.triu(torch.ones(T, T), diagonal=1).bool()
        h = self.block(h, mask=mask)
        return self.head(h)


model = CodeLM()
opt = torch.optim.AdamW(model.parameters(), lr=2e-3)
print('=== FIM + CLM Joint Training ===')
for step in range(50):
    toks = torch.randint(4, 100, (16, 32))
    packed_batch = []
    modes = []
    for row in toks:
        p, mode = fim_pack(row)
        # pad/trim to 40
        if p.numel() < 40:
            p = F.pad(p, (0, 40 - p.numel()))
        else:
            p = p[:40]
        packed_batch.append(p)
        modes.append(mode)
    batch = torch.stack(packed_batch)
    logits = model(batch[:, :-1])
    loss = F.cross_entropy(logits.reshape(-1, 100), batch[:, 1:].reshape(-1))
    opt.zero_grad(); loss.backward(); opt.step()
    if step % 10 == 0 or step == 49:
        fim_ratio = sum(m == 'fim' for m in modes) / len(modes)
        print(f'step={step:02d} loss={loss.item():.4f} fim_ratio={fim_ratio:.2f}')
print(f'\\nKey: Interleave FIM with CLM so the model supports both chat and IDE fill-in.')"""
            ),
            md(
                """## 3. 仓库级上下文打包

把同仓库相关文件按依赖/路径优先级拼进窗口（或用 RAG 检索），让模型学习跨文件 API。教学实现用“主文件 + 依赖摘要”拼接。"""
            ),
            code(
                """def pack_repo_context(files: dict[str, str], main: str, max_chars=300):
    '''files: path->content. Put imports of main first, then main.'''
    import_re = re.compile(r'^(?:from|import)\\s+([\\w\\.]+)', re.M)
    deps = import_re.findall(files.get(main, ''))
    chunks = []
    for d in deps:
        # map module-ish name to file
        cand = d.replace('.', '/') + '.py'
        if cand in files:
            chunks.append(f'# file: {cand}\\n' + files[cand])
    chunks.append(f'# file: {main}\\n' + files[main])
    text = '\\n\\n'.join(chunks)
    return text[:max_chars]


repo = {
    'utils/math_utils.py': 'def add(a,b):\\n    return a+b\\n',
    'app/main.py': 'from utils.math_utils import add\\n\\ndef run():\\n    return add(1,2)\\n',
}
packed = pack_repo_context(repo, 'app/main.py')
print('=== Repo Packing ===')
print(packed)
print(f'\\nKey: Cross-file packing teaches API usage beyond single-file pretraining.')"""
            ),
            md(
                """## 4. 执行反馈与 Pass@k

对可运行题：生成 k 个样本，在沙箱跑单测；Pass@k = 至少一发通过的比例。执行信号也可回灌为 RL/偏好数据。"""
            ),
            code(
                """def pass_at_k(n, c, k):
    '''Canonical unbiased Pass@k estimator: n samples, c correct, choose k.'''
    if n - c < k:
        return 1.0
    return 1.0 - math.prod((n - c - i) / (n - i) for i in range(k))


import math

def run_tests(fn):
    tests = [((1, 2), 3), ((0, 0), 0), ((-1, 1), 0)]
    try:
        return all(fn(*a) == b for a, b in tests)
    except Exception:
        return False


candidates = [
    lambda a, b: a + b,
    lambda a, b: a - b,
    lambda a, b: a + b + 1,
    lambda a, b: a + b,
]
correct = sum(run_tests(fn) for fn in candidates)
n = len(candidates)
print('=== Execution Feedback / Pass@k ===')
print(f'correct={correct}/{n}')
for k in [1, 2, 4]:
    print(f'Pass@{k}={pass_at_k(n, correct, k):.3f}')
print(f'\\nKey: Unit-test rewards are hard to hack and define the main code-model KPI.')"""
            ),
            thinking(
                "4.5 代码预训练与专训",
                "FIM 比例过高对对话/长生成有何副作用？如何调度？",
                "仓库级打包与 RAG 检索仓库，各自适合什么上下文长度预算？",
                "Pass@k 很高但仓库真实修复率低，可能缺了什么训练信号？",
                "开源语料许可证不合规时，合成数据能替代到什么程度？",
            ),
        ],
    )

    # ------------------------------------------------------------------
    # 13.5 Multimodal generation
    # ------------------------------------------------------------------
    write_nb(
        "13_multimodal/05_multimodal_generation.ipynb",
        [
            md(
                """# 13.5 多模态生成 (Multimodal Generation)

> 🕐 预估学习时间：40分钟

除理解外，产业还要求文生图/文生视频/统一生成。常见路径：LLM 规划 + 扩散/流匹配解码器，或原生多模态自回归（Chameleon、Transfusion 等思路）。

本节涵盖：
- 文本到潜空间条件
- 简化扩散训练步
- LLM 作为布局/提示规划器
- 统一离散多模态自回归直觉
- 质量与安全护栏要点"""
            ),
            md(
                """## 1. 条件扩散：文本嵌入引导去噪

教学版：在 2D 潜空间做条件去噪，条件向量来自文本编码器。"""
            ),
            code(
                """import torch
import torch.nn as nn
import torch.nn.functional as F
import math

torch.manual_seed(0)


class TextEncoder(nn.Module):
    def __init__(self, vocab=50, d=32):
        super().__init__()
        self.emb = nn.Embedding(vocab, d)

    def forward(self, ids):
        return self.emb(ids).mean(1)


class Denoiser(nn.Module):
    def __init__(self, d_x=2, d_cond=32, hidden=64):
        super().__init__()
        self.t_emb = nn.Linear(1, hidden)
        self.net = nn.Sequential(
            nn.Linear(d_x + d_cond + hidden, hidden), nn.SiLU(),
            nn.Linear(hidden, hidden), nn.SiLU(),
            nn.Linear(hidden, d_x),
        )

    def forward(self, x_t, t, cond):
        te = self.t_emb(t.unsqueeze(-1))
        inp = torch.cat([x_t, cond, te], dim=-1)
        return self.net(inp)


text_enc = TextEncoder()
denoiser = Denoiser()
opt = torch.optim.Adam(list(text_enc.parameters()) + list(denoiser.parameters()), lr=2e-3)

print('=== Conditional Diffusion (toy 2D) ===')
for step in range(80):
    # target latent depends on token-0 class
    ids = torch.randint(0, 50, (64, 4))
    y = torch.stack([ids[:, 0].float() / 50, (ids[:, 0].float() / 50) ** 2], dim=-1)
    y = (y - 0.5) * 2
    t = torch.rand(64)
    noise = torch.randn_like(y)
    x_t = (1 - t.unsqueeze(-1)) * y + t.unsqueeze(-1) * noise
    cond = text_enc(ids)
    pred = denoiser(x_t, t, cond)
    loss = F.mse_loss(pred, noise)
    opt.zero_grad(); loss.backward(); opt.step()
    if step % 20 == 0 or step == 79:
        print(f'step={step:02d} noise_mse={loss.item():.4f}')
print(f'\\nKey: Text-conditioned denoisers learn to remove noise guided by language embeddings.')"""
            ),
            md(
                """## 2. LLM 规划器：先结构化，再渲染

复杂图像/视频生成常两段式：LLM 产出场景图/镜头脚本/扩展提示，再交给扩散模型。便于控制与可编辑。"""
            ),
            code(
                """def llm_plan(prompt: str) -> dict:
    # Toy planner: extract keywords as layout slots
    words = [w for w in prompt.lower().replace(',', ' ').split() if len(w) > 2]
    objects = words[:3] or ['object']
    return {
        'expanded_prompt': prompt + ', highly detailed, cinematic lighting',
        'layout': [{'object': o, 'box': [0.1 + 0.25 * i, 0.2, 0.3, 0.4]} for i, o in enumerate(objects)],
        ' Negatives': 'blurry, watermark, text artifacts',
    }


plan = llm_plan('a fox and a robot in a snowy forest')
print('=== LLM Planner ===')
for k, v in plan.items():
    print(f'{k}: {v}')
print(f'\\nKey: Planning separates semantic control (LLM) from pixel synthesis (diffusion).')"""
            ),
            md(
                """## 3. 统一离散多模态自回归（直觉）

把图像 patch / 音频 codec token 与文本 token 放进同一词表，用下一个 token 预测统一训练。优点是一套目标；难点是词表设计、模态平衡与长序列代价。"""
            ),
            code(
                """class UnifiedAR(nn.Module):
    def __init__(self, vocab=128, d=64):
        super().__init__()
        self.emb = nn.Embedding(vocab, d)
        # modality id: 0=text, 1=image
        self.mod = nn.Embedding(2, d)
        self.block = nn.TransformerEncoder(
            nn.TransformerEncoderLayer(d, 4, 128, batch_first=True), 2
        )
        self.head = nn.Linear(d, vocab)

    def forward(self, tok, mod):
        h = self.emb(tok) + self.mod(mod)
        T = tok.size(1)
        mask = torch.triu(torch.ones(T, T), diagonal=1).bool()
        return self.head(self.block(h, mask=mask))


model = UnifiedAR()
opt = torch.optim.AdamW(model.parameters(), lr=2e-3)
print('=== Unified Multimodal AR ===')
for step in range(40):
    # first half text tokens, second half image tokens
    tok = torch.randint(0, 128, (16, 24))
    mod = torch.cat([torch.zeros(16, 12, dtype=torch.long), torch.ones(16, 12, dtype=torch.long)], dim=1)
    logits = model(tok[:, :-1], mod[:, :-1])
    loss = F.cross_entropy(logits.reshape(-1, 128), tok[:, 1:].reshape(-1))
    opt.zero_grad(); loss.backward(); opt.step()
    if step % 10 == 0 or step == 39:
        print(f'step={step:02d} loss={loss.item():.4f}')
print(f'\\nKey: One next-token objective can cover text and image tokens if modality embeddings align them.')"""
            ),
            md(
                """## 4. 生成质量与安全

- **质量**：美学评分、CLIPScore、人体偏好（PickScore）、视频时序一致性  
- **安全**：NSFW/暴露/侵权检测、提示拦截、输出水印  
- **可控性**：布局/姿态/身份保持（IP-Adapter 等）与拒绝无授权人脸"""
            ),
            code(
                """def clip_score_proxy(text_emb, image_emb):
    text_emb = F.normalize(text_emb, dim=-1)
    image_emb = F.normalize(image_emb, dim=-1)
    return (text_emb * image_emb).sum(-1)


t = F.normalize(torch.randn(8, 32), dim=-1)
img_good = F.normalize(t + 0.1 * torch.randn(8, 32), dim=-1)
img_bad = F.normalize(torch.randn(8, 32), dim=-1)
print('=== Quality Proxy ===')
print('good align', clip_score_proxy(t, img_good).mean().item())
print('bad align', clip_score_proxy(t, img_bad).mean().item())
print(f'\\nKey: Alignment scores are cheap filters; human/aesthetics models still needed for product QA.')"""
            ),
            thinking(
                "13.5 多模态生成",
                "两段式（LLM 规划 + 扩散）与原生统一 AR 在可控性/效率上如何取舍？",
                "视频生成相对图像多了哪些失败模式（时序、身份漂移）？",
                "如何防止生成模型被用于深度伪造与版权侵权？",
                "多模态词表中图像 token 占比过高会怎样影响纯文本能力？",
            ),
        ],
    )

    # ------------------------------------------------------------------
    # 12.7 Deep research agent
    # ------------------------------------------------------------------
    write_nb(
        "12_agent/07_deep_research.ipynb",
        [
            md(
                """# 12.7 深度研究智能体 (Deep Research Agents)

> 🕐 预估学习时间：40分钟

深度研究 Agent（如 OpenAI Deep Research、各类 survey agent）把问题拆解为多轮检索-阅读-综合-引用，强调证据链与可追溯，而不是单次 RAG。

本节涵盖：
- 研究状态机
- 子问题分解与检索循环
- 证据库与冲突检测
- 带引用的报告合成
- 预算控制与停止条件"""
            ),
            md(
                """## 1. 研究状态机

`Plan → Search → Read → Note → Synthesize → Critique → (loop|finish)`

每步消耗预算（检索次数/token），需显式停止条件。"""
            ),
            code(
                """from dataclasses import dataclass, field
from typing import Any
import hashlib

torch = __import__('torch')  # keep torch import style consistent if needed later


@dataclass
class Evidence:
    eid: str
    query: str
    source: str
    snippet: str
    score: float


@dataclass
class ResearchState:
    question: str
    subquestions: list[str] = field(default_factory=list)
    evidence: list[Evidence] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)
    budget_search: int = 6
    done: bool = False


def plan(question: str) -> list[str]:
    # toy decomposition
    seeds = ['definition', 'methods', 'benchmarks', 'open problems']
    return [f'{question}: {s}' for s in seeds]


state = ResearchState('LLM inference optimization')
state.subquestions = plan(state.question)
print('=== Research Plan ===')
for i, sq in enumerate(state.subquestions, 1):
    print(f'{i}. {sq}')
print(f'Key: Explicit subquestions turn vague research into measurable retrieval goals.')"""
            ),
            md(
                """## 2. 检索-阅读-记笔记循环

对每个子问题检索 Top-K，提炼笔记，写入证据库；重复直到预算耗尽或信息增益低。"""
            ),
            code(
                """CORPUS = {
    'p1': 'PagedAttention manages KV cache like virtual memory to reduce fragmentation.',
    'p2': 'Speculative decoding uses a draft model to propose tokens verified by the target.',
    'p3': 'Prefill is compute-bound while decode is memory-bandwidth-bound.',
    'p4': 'Continuous batching improves GPU utilization for online serving.',
    'p5': 'Quantization (GPTQ/AWQ) reduces memory footprint with small quality loss.',
}


def search(query: str, k=2) -> list[Evidence]:
    scored = []
    q_terms = set(query.lower().split())
    for sid, text in CORPUS.items():
        terms = set(text.lower().replace(',', ' ').split())
        score = len(q_terms & terms) + 0.1 * text.lower().count('kv')
        scored.append((score, sid, text))
    scored.sort(reverse=True)
    out = []
    for score, sid, text in scored[:k]:
        eid = hashlib.md5(f'{sid}:{query}'.encode()).hexdigest()[:8]
        out.append(Evidence(eid, query, sid, text, float(score)))
    return out


def note_from_evidence(ev: Evidence) -> str:
    return f'[{ev.source}] {ev.snippet}'


print('=== Search-Read Loop ===')
for sq in state.subquestions:
    if state.budget_search <= 0:
        break
    hits = search(sq, k=2)
    state.budget_search -= 1
    for ev in hits:
        if all(e.snippet != ev.snippet for e in state.evidence):
            state.evidence.append(ev)
            state.notes.append(note_from_evidence(ev))
    print(f'Q: {sq} -> {[h.source for h in hits]} budget={state.budget_search}')
print(f'evidence={len(state.evidence)} notes={len(state.notes)}')
print(f'\\nKey: Deduplicate evidence and spend budget on uncovered subquestions first.')"""
            ),
            md(
                """## 3. 冲突检测与综合成文

若两条证据结论冲突，标记不确定性并建议追加检索；最终答案强制引用证据 ID。"""
            ),
            code(
                """def detect_conflicts(evidence: list[Evidence]) -> list[tuple[str, str]]:
    # toy: treat presence of opposing keywords as conflict
    pos = [e for e in evidence if 'improves' in e.snippet or 'reduce' in e.snippet]
    neg = [e for e in evidence if 'loss' in e.snippet and 'quality' in e.snippet]
    conflicts = []
    if pos and neg:
        conflicts.append((pos[0].eid, neg[0].eid))
    return conflicts


def synthesize(question: str, evidence: list[Evidence]) -> str:
    bullets = []
    for e in evidence[:5]:
        bullets.append(f'- {e.snippet} [{e.eid}]')
    body = '\\n'.join(bullets)
    return f'# Report: {question}\\n\\n## Findings\\n{body}\\n'


conflicts = detect_conflicts(state.evidence)
report = synthesize(state.question, state.evidence)
print('=== Synthesis ===')
print('conflicts:', conflicts)
print(report)
print(f'Key: Citations make deep research auditable; conflicts trigger more search instead of fluent hallucination.')"""
            ),
            md(
                """## 4. 停止条件与产业要点

停止当：
1. 所有子问题都有 ≥1 条证据  
2. 新增检索的信息增益低于阈值  
3. 预算耗尽  

产业增强：并行子 Agent、网页浏览工具、表格/论文阅读器、人类复核节点、可复现研究日志。"""
            ),
            code(
                """def should_stop(state: ResearchState, min_cover=1) -> bool:
    covered = {sq: 0 for sq in state.subquestions}
    for e in state.evidence:
        for sq in state.subquestions:
            if sq in e.query or any(t in e.snippet.lower() for t in sq.lower().split()[-2:]):
                covered[sq] += 1
    if all(v >= min_cover for v in covered.values()):
        return True
    if state.budget_search <= 0:
        return True
    return False


state.done = should_stop(state)
print('=== Stop Decision ===')
print('done=', state.done, 'remaining_budget=', state.budget_search)
print(f'\\nKey: Deep research is a budgeted MDP; fluency without stop rules burns cost and still hallucinates.')"""
            ),
            thinking(
                "12.7 深度研究智能体",
                "深度研究与单次 RAG 的本质差别是什么？哪些产品问题其实不需要深度研究？",
                "如何度量“信息增益”以避免无意义循环检索？",
                "多 Agent 并行检索时如何合并证据并去重？",
                "引用了来源仍可能误读原文，如何做事实核对？",
            ),
        ],
    )

    # ------------------------------------------------------------------
    # 01.8 Synthetic data verification
    # ------------------------------------------------------------------
    write_nb(
        "01_data_engineering/08_synthetic_data_verification.ipynb",
        [
            md(
                """# 1.8 合成数据验证 (Synthetic Data Verification)

> 🕐 预估学习时间：35分钟

合成数据便宜但易塌缩、泄漏与风格单一。产业流程强调：生成 → 自动验证 → 多样性过滤 → 人工抽检。

本节涵盖：
- 常见失效模式
- 执行/模式/裁判验证器
- 去重与多样性（embedding n-gram）
- 泄漏检测（相对训练语料）
- 质量门禁流水线"""
            ),
            md(
                """## 1. 失效模式

| 模式 | 现象 | 后果 |
|------|------|------|
| 模式塌缩 | 很多样本几乎同构 | 微调后不会泛化 |
| 伪正确 | 看起来对，逻辑错 | 奖励黑客 |
| 泄漏 | 复述评测集 | 虚高榜 |
| 有害漂移 | 安全边界被冲淡 | 上线风险 |"""
            ),
            code(
                """import re
import torch
import torch.nn.functional as F
from collections import Counter

torch.manual_seed(0)


def is_schema_ok(sample: dict) -> bool:
    return isinstance(sample.get('instruction'), str) and isinstance(sample.get('output'), str) and len(sample['output']) > 0


def is_code_executable(output: str) -> bool:
    # only allow simple pure functions for the toy verifier
    if 'import os' in output or 'open(' in output:
        return False
    try:
        ns = {}
        exec(output, ns, ns)
        if 'add' in ns:
            return ns['add'](1, 2) == 3
        return True
    except Exception:
        return False


samples = [
    {'instruction': 'write add', 'output': 'def add(a,b):\\n    return a+b\\n'},
    {'instruction': 'write add', 'output': 'def add(a,b):\\n    return a-b\\n'},
    {'instruction': 'x', 'output': ''},
]
print('=== Verifiers ===')
for s in samples:
    print(s['output'][:30].replace('\\n',' '), 'schema=', is_schema_ok(s), 'exec=', is_code_executable(s['output']))
print(f'Key: Task-specific verifiers catch silent errors that LLM-as-judge may miss.')"""
            ),
            md(
                """## 2. 多样性与近重复过滤

用 n-gram Jaccard 或嵌入相似度剔除近重复，保持指令覆盖面。"""
            ),
            code(
                """def trigrams(text: str) -> set[str]:
    toks = text.lower().split()
    return set(' '.join(toks[i:i+3]) for i in range(max(len(toks)-2, 1)))


def jaccard(a: set[str], b: set[str]) -> float:
    if not a and not b:
        return 1.0
    return len(a & b) / max(len(a | b), 1)


def dedup(texts, thr=0.6):
    kept = []
    grams = []
    for t in texts:
        g = trigrams(t)
        if any(jaccard(g, kg) >= thr for kg in grams):
            continue
        kept.append(t)
        grams.append(g)
    return kept


texts = [
    'explain gradient descent step by step',
    'explain gradient descent steps carefully',
    'how does attention work in transformers',
    'explain gradient descent step by step please',
]
kept = dedup(texts, thr=0.4)
print('=== Diversity Filter ===')
print('kept:', kept)
print(f'removed={len(texts)-len(kept)}')
print(f'\\nKey: Near-duplicate synthetic instructions waste epochs and amplify mode collapse.')"""
            ),
            md(
                """## 3. 评测集泄漏检查

对合成输出与基准题干做 n-gram / 嵌入重叠检测，超过阈值则丢弃或隔离。"""
            ),
            code(
                """BENCHMARK = [
    'what is the capital of france',
    'write a function to reverse a linked list',
]


def leak_score(text: str, bench=BENCHMARK) -> float:
    g = trigrams(text)
    return max(jaccard(g, trigrams(b)) for b in bench)


cands = [
    'Describe PagedAttention briefly',
    'write a function to reverse a linked list in python',
]
print('=== Leak Check ===')
for c in cands:
    print(c, 'leak=', round(leak_score(c), 3))
print(f'\\nKey: Filter synthetic data against eval n-grams before mixing into SFT.')"""
            ),
            md(
                """## 4. 质量门禁流水线

`generate → schema → verifier → dedup → leak → safety → accept`

统计每关通过率，定位生成提示或教师模型问题。"""
            ),
            code(
                """def pipeline(raw_samples):
    stats = Counter()
    accepted = []
    for s in raw_samples:
        stats['total'] += 1
        if not is_schema_ok(s):
            stats['fail_schema'] += 1
            continue
        if s['instruction'].startswith('write') and not is_code_executable(s['output']):
            stats['fail_exec'] += 1
            continue
        if leak_score(s['instruction'] + ' ' + s['output']) > 0.5:
            stats['fail_leak'] += 1
            continue
        accepted.append(s)
        stats['accepted'] += 1
    # dedup on instructions
    instr = [s['instruction'] for s in accepted]
    kept_instr = set(dedup(instr, thr=0.5))
    accepted = [s for s in accepted if s['instruction'] in kept_instr]
    stats['after_dedup'] = len(accepted)
    return accepted, stats


raw = samples + [
    {'instruction': 'write a function to reverse a linked list', 'output': 'def add(a,b):\\n    return a+b\\n'},
    {'instruction': 'explain attention', 'output': 'Attention mixes tokens by similarity.'},
]
accepted, stats = pipeline(raw)
print('=== Gate Pipeline ===')
print(dict(stats))
print('accepted=', accepted)
print(f'\\nKey: Measurable gates turn synthetic data from lottery tickets into an engineered supply chain.')"""
            ),
            thinking(
                "1.8 合成数据验证",
                "什么时候该用执行验证，什么时候只能用 LLM-as-judge？",
                "多样性过滤过严会伤害哪些长尾能力？",
                "如何防止教师模型把自己的偏见放大到学生模型？",
                "合成数据占比升高时，如何监控真实用户分布偏移？",
            ),
        ],
    )

    # ------------------------------------------------------------------
    # 09.10 Advanced speculative decoding
    # ------------------------------------------------------------------
    write_nb(
        "09_inference_optimization/10_advanced_speculative_decoding.ipynb",
        [
            md(
                """# 9.10 高级投机解码 (EAGLE / MTP)

> 🕐 预估学习时间：35分钟

在基础投机解码之上，EAGLE 用特征层草稿、Medusa/MTP 用多头并行猜 token。本节实现接受率统计与树状验证的教学版本。

本节涵盖：
- 草稿-验证接受率
- 特征级草稿（EAGLE 直觉）
- 多 token 预测头（MTP/Medusa）
- 树状候选与期望加速比"""
            ),
            md(
                """## 1. 经典投机解码接受率

草稿模型提 γ 个 token，目标模型一次前向验证；按概率比接受/拒绝。"""
            ),
            code(
                """import torch
import torch.nn as nn
import torch.nn.functional as F

torch.manual_seed(0)


class TinyPolicy(nn.Module):
    def __init__(self, vocab=32, d=32):
        super().__init__()
        self.embed = nn.Embedding(vocab, d)
        self.rnn = nn.GRU(d, d, batch_first=True)
        self.head = nn.Linear(d, vocab)

    def forward(self, x):
        h, _ = self.rnn(self.embed(x))
        return self.head(h)


draft = TinyPolicy()
target = TinyPolicy()
# make target sharper copy-ish
target.load_state_dict(draft.state_dict())


def speculative_step(prefix, gamma=4):
    # draft autoregressive proposals
    seq = prefix
    draft_tokens = []
    draft_probs = []
    with torch.no_grad():
        for _ in range(gamma):
            logits = draft(seq)[:, -1]
            probs = F.softmax(logits, dim=-1)
            tok = torch.multinomial(probs, 1)
            draft_tokens.append(tok)
            draft_probs.append(probs.gather(-1, tok))
            seq = torch.cat([seq, tok], dim=1)
        # target verifies all prefixes in one forward
        full = torch.cat([prefix] + draft_tokens, dim=1)
        t_logits = target(full[:, :-1])
        t_probs = F.softmax(t_logits[:, -gamma:], dim=-1)
        accepted = []
        for i, tok in enumerate(draft_tokens):
            p_t = t_probs[:, i, :].gather(-1, tok)
            p_d = draft_probs[i]
            ratio = (p_t / (p_d + 1e-12)).clamp(max=1.0)
            if torch.rand(()) <= ratio:
                accepted.append(tok)
            else:
                # sample from residual distribution (simplified: sample target)
                tok_new = torch.multinomial(t_probs[:, i, :], 1)
                accepted.append(tok_new)
                break
        else:
            # bonus sample from target at next position
            pass
    return torch.cat(accepted, dim=1), len(accepted)


prefix = torch.randint(0, 32, (1, 5))
got, n_acc = speculative_step(prefix, gamma=4)
print('=== Speculative Decoding ===')
print(f'accepted_tokens={n_acc}, values={got.tolist()}')
print(f'Key: Speedup ≈ accepted_length / (1 + draft_cost/target_cost); acceptance rate is everything.')"""
            ),
            md(
                """## 2. EAGLE 直觉：用特征而不是 token 喂草稿

EAGLE 草稿头读取目标模型倒数层特征，再预测下一 token，使草稿分布更接近目标，提高接受率。"""
            ),
            code(
                """class EagleLike(nn.Module):
    def __init__(self, vocab=32, d=32):
        super().__init__()
        self.embed = nn.Embedding(vocab, d)
        self.rnn = nn.GRU(d, d, batch_first=True)
        self.draft_head = nn.Sequential(nn.Linear(d, d), nn.SiLU(), nn.Linear(d, vocab))
        self.lm_head = nn.Linear(d, vocab)

    def features(self, x):
        h, _ = self.rnn(self.embed(x))
        return h

    def forward(self, x):
        h = self.features(x)
        return self.lm_head(h), self.draft_head(h)


eagle = EagleLike()
opt = torch.optim.Adam(eagle.parameters(), lr=2e-3)
print('=== Train Eagle-like Draft Head ===')
for step in range(40):
    x = torch.randint(0, 32, (16, 12))
    logits, draft_logits = eagle(x)
    # draft predicts next token from current features
    loss_lm = F.cross_entropy(logits[:, :-1].reshape(-1, 32), x[:, 1:].reshape(-1))
    loss_draft = F.cross_entropy(draft_logits[:, :-1].reshape(-1, 32), x[:, 1:].reshape(-1))
    loss = loss_lm + loss_draft
    opt.zero_grad(); loss.backward(); opt.step()
    if step % 10 == 0 or step == 39:
        with torch.no_grad():
            agree = (draft_logits[:, :-1].argmax(-1) == logits[:, :-1].argmax(-1)).float().mean()
        print(f'step={step:02d} loss={loss.item():.4f} draft_target_agree={agree.item():.3f}')
print(f'\\nKey: Feature-conditioned draft heads track the target distribution more closely than a tiny separate LM.')"""
            ),
            md(
                """## 3. MTP / Medusa：多头并行猜测

多个头分别预测 +1/+2/+3… 位置，一次前向产生短树候选，再由主干验证。"""
            ),
            code(
                """class MedusaHeads(nn.Module):
    def __init__(self, vocab=32, d=32, n_heads=3):
        super().__init__()
        self.embed = nn.Embedding(vocab, d)
        self.rnn = nn.GRU(d, d, batch_first=True)
        self.base = nn.Linear(d, vocab)
        self.extra = nn.ModuleList([nn.Linear(d, vocab) for _ in range(n_heads)])

    def forward(self, x):
        h, _ = self.rnn(self.embed(x))
        outs = [self.base(h)]
        for head in self.extra:
            outs.append(head(h))
        return outs  # list of logits for offset 0..n


medusa = MedusaHeads()
x = torch.randint(0, 32, (8, 10))
outs = medusa(x)
print('=== Medusa / MTP Heads ===')
for i, logit in enumerate(outs):
    print(f'head+{i}: {tuple(logit.shape)}')

# Expected tokens accepted under independent accept p
def expected_accept_len(p, gamma):
    # 1 + p + p^2 + ... until rejection geometry for a chain
    return (1 - p ** (gamma + 1)) / (1 - p) if p < 1 else gamma + 1

print(f'\\nExpected accepted length if p_accept=0.7, gamma=3: {expected_accept_len(0.7, 3):.2f}')
print(f'Key: Tree/MTP candidates raise expected accepted tokens per expensive target forward.')"""
            ),
            thinking(
                "9.10 高级投机解码",
                "接受率从 0.5 提到 0.8 对端到端加速比意味着什么？",
                "EAGLE 草稿依赖目标特征，部署时如何与 CUDA Graph / PD 分离兼容？",
                "MTP 训练是否损害下一 token 质量？如何加权多头损失？",
                "何时该用小模型投机，何时该用同模型多头？",
            ),
        ],
    )

    print("done")


if __name__ == "__main__":
    build_all()
