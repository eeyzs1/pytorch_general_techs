#!/usr/bin/env python3
"""Generate MoE end-to-end case study notebook."""

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


def build() -> None:
    write_nb(
        "20_end_to_end/01_moe_from_mixture_to_serving.ipynb",
        [
            md(
                """# E2E-1 MoE 端到端案例：从配比到 Serving

> 🕐 预估学习时间：70分钟  
> 🎯 目标：把分散在数据/架构/分布式/推理模块中的能力，串成一条可运行的 **MoE 项目流水线**。

## 案例故事

你要交付一个 4 专家小型 MoE 代码助手：

1. **配比**：用 DoReMi 风格方法决定 web/code/math/docs 采样权重  
2. **训练**：带负载均衡与可观测性的 MoE 预训练/持续预训练玩具  
3. **并行**：模拟 Expert Parallel（EP）all-to-all 调度与容量  
4. **Serving**：分页 KV + 连续批处理 + 专家占用监控上线  
5. **验收**：最差域 loss、drop rate、TTFT、专家均衡等 Go-Live 门禁

## 关联专题（建议先读/对照）

| 阶段 | 专题 Notebook |
|------|----------------|
| 配比 | [09_doremi_data_mixture](../01_data_engineering/09_doremi_data_mixture.ipynb) |
| MoE 训练 | [12_moe_training_at_scale](../03_architecture_design/12_moe_training_at_scale.ipynb) |
| 观测 | [06_training_observability](../04_pretraining/06_training_observability.ipynb) |
| Serving | [12_serving_engine_internals](../09_inference_optimization/12_serving_engine_internals.ipynb) |

本 notebook **自包含可运行**，不依赖上面文件的执行状态。"""
            ),
            md(
                """## 0. 项目配置与共享组件

先定义领域、模型、日志结构——后续阶段都写进同一个 `ProjectState`。"""
            ),
            code(
                """import math
import time
from dataclasses import dataclass, field, asdict
from collections import defaultdict

import torch
import torch.nn as nn
import torch.nn.functional as F

torch.manual_seed(7)

DOMAINS = ['web', 'code', 'math', 'docs']
N_DOMAIN = len(DOMAINS)
VOCAB = 64
D_MODEL = 48
N_EXPERTS = 4
TOP_K = 2


@dataclass
class ProjectState:
    alpha: torch.Tensor
    metrics: dict = field(default_factory=dict)
    events: list = field(default_factory=list)
    checkpoint: dict = field(default_factory=dict)

    def log(self, stage, msg, **kv):
        self.events.append({'stage': stage, 'msg': msg, **kv})
        extra = ' '.join(f'{k}={v}' for k, v in kv.items())
        print(f'[{stage}] {msg} {extra}'.rstrip())


state = ProjectState(alpha=torch.ones(N_DOMAIN) / N_DOMAIN)
print('=== Project boot ===')
print('domains=', DOMAINS, 'experts=', N_EXPERTS, 'top_k=', TOP_K)
print('initial alpha=', state.alpha.tolist())
print('Key: One state object threads mixture -> train -> EP -> serve.')"""
            ),
            md(
                """## 1. 阶段 A — 数据配比（DoReMi 风格）

用小 proxy 估计各域 excess loss，更新采样分布 α，供正式 MoE 训练使用。"""
            ),
            code(
                """class TinyLM(nn.Module):
    def __init__(self, d=D_MODEL, vocab=VOCAB):
        super().__init__()
        self.embed = nn.Embedding(vocab, d)
        self.fc = nn.Linear(d, vocab)

    def forward(self, x):
        return self.fc(self.embed(x).mean(1))


def domain_batch(domain_id, n=64, t=10):
    x = torch.randint(0, VOCAB, (n, t))
    # domain signature in first tokens
    x[:, 0] = (domain_id * 11) % VOCAB
    x[:, 1] = (domain_id * 5 + 3) % VOCAB
    y = (x[:, 0] + x[:, 1] + domain_id) % VOCAB
    return x, y


def domain_losses(model, steps=4):
    model.eval()
    out = []
    with torch.no_grad():
        for k in range(N_DOMAIN):
            s = 0.0
            for _ in range(steps):
                x, y = domain_batch(k)
                s += F.cross_entropy(model(x), y).item()
            out.append(s / steps)
    model.train()
    return torch.tensor(out)


# reference model on uniform mix
ref = TinyLM()
opt = torch.optim.Adam(ref.parameters(), lr=1e-2)
for _ in range(40):
    k = torch.randint(0, N_DOMAIN, (1,)).item()
    x, y = domain_batch(k)
    loss = F.cross_entropy(ref(x), y)
    opt.zero_grad(); loss.backward(); opt.step()
ref_L = domain_losses(ref)


def doremi_alpha(iters=5, eta=0.8):
    alpha = torch.ones(N_DOMAIN) / N_DOMAIN
    for t in range(iters):
        proxy = TinyLM()
        opt_p = torch.optim.Adam(proxy.parameters(), lr=1e-2)
        for _ in range(35):
            k = torch.multinomial(alpha, 1).item()
            x, y = domain_batch(k)
            loss = F.cross_entropy(proxy(x), y)
            opt_p.zero_grad(); loss.backward(); opt_p.step()
        excess = (domain_losses(proxy) - ref_L).clamp_min(0)
        alpha = alpha * torch.exp(eta * excess)
        alpha = alpha / alpha.sum()
        state.log('mixture', 'doremi-iter', iter=t,
                  alpha=[round(a, 3) for a in alpha.tolist()],
                  excess=[round(e, 3) for e in excess.tolist()])
    return alpha


state.alpha = doremi_alpha().detach()
# blend with human prior: code-heavy assistant
prior = torch.tensor([0.2, 0.45, 0.25, 0.10])
state.alpha = 0.7 * state.alpha + 0.3 * prior
state.alpha = state.alpha / state.alpha.sum()
state.metrics['alpha'] = state.alpha.tolist()
print('final alpha', {d: round(a, 3) for d, a in zip(DOMAINS, state.alpha.tolist())})
print('Key: Stage A output is a frozen sampling distribution for Stage B.')"""
            ),
            md(
                """## 2. 阶段 B — MoE 训练 + 可观测性

实现 Top-2 MoE：共享注意力骨干 + 路由专家 FFN，带辅助负载损失、激活/梯度看板、Spike 守卫。"""
            ),
            code(
                """class ExpertFFN(nn.Module):
    def __init__(self, d=D_MODEL):
        super().__init__()
        self.net = nn.Sequential(nn.Linear(d, 4 * d), nn.GELU(), nn.Linear(4 * d, d))

    def forward(self, x):
        return self.net(x)


class MoEBlock(nn.Module):
    def __init__(self, d=D_MODEL, n_experts=N_EXPERTS, top_k=TOP_K):
        super().__init__()
        self.ln = nn.LayerNorm(d)
        self.attn = nn.MultiheadAttention(d, 4, batch_first=True)
        self.router = nn.Linear(d, n_experts, bias=False)
        self.experts = nn.ModuleList([ExpertFFN(d) for _ in range(n_experts)])
        self.top_k = top_k
        self.n_experts = n_experts

    def forward(self, x):
        h = self.ln(x)
        a, _ = self.attn(h, h, h, need_weights=False)
        x = x + a
        logits = self.router(x)  # (B,T,E)
        probs = torch.softmax(logits, dim=-1)
        topv, topi = probs.topk(self.top_k, dim=-1)
        topv = topv / topv.sum(dim=-1, keepdim=True)

        # vectorized expert compute via loop over experts (clear for teaching)
        out = torch.zeros_like(x)
        for e, expert in enumerate(self.experts):
            mask = (topi == e)  # (B,T,K)
            if not mask.any():
                continue
            # tokens routed to e under any k
            token_mask = mask.any(dim=-1)  # (B,T)
            if not token_mask.any():
                continue
            toks = x[token_mask]
            y = expert(toks)
            # weight by corresponding topv where expert selected
            w = (topv * mask.float()).sum(dim=-1)[token_mask].unsqueeze(-1)
            out[token_mask] += w * y

        # aux load-balance: N * sum f*P
        with torch.no_grad():
            assign = topi.reshape(-1)
        f = torch.zeros(self.n_experts, device=x.device)
        for i in assign:
            f[i] += 1
        f = f / f.sum().clamp_min(1)
        P = probs.mean(dim=(0, 1))
        aux = self.n_experts * (f * P).sum()
        return x + out, probs, aux, f.detach()


class MoEMiniLM(nn.Module):
    def __init__(self):
        super().__init__()
        self.embed = nn.Embedding(VOCAB, D_MODEL)
        self.block = MoEBlock()
        self.ln_f = nn.LayerNorm(D_MODEL)
        self.head = nn.Linear(D_MODEL, VOCAB)

    def forward(self, idx):
        x = self.embed(idx)
        x, probs, aux, usage = self.block(x)
        logits = self.head(self.ln_f(x))
        return logits, probs, aux, usage


class SpikeGuard:
    def __init__(self, z_thr=5.0, ratio_thr=3.0):
        self.hist = []
        self.z_thr = z_thr
        self.ratio_thr = ratio_thr
        self.spikes = 0

    def check(self, loss):
        import statistics
        self.hist.append(loss)
        if len(self.hist) < 8:
            return False
        base = self.hist[-21:-1] if len(self.hist) > 8 else self.hist[:-1]
        mu = statistics.fmean(base)
        sd = statistics.pstdev(base) or 1e-6
        z = (loss - mu) / sd
        if z > self.z_thr or loss > self.ratio_thr * mu:
            self.spikes += 1
            self.hist.pop()
            return True
        return False


def train_moe(alpha, steps=120):
    model = MoEMiniLM()
    opt = torch.optim.AdamW(model.parameters(), lr=2e-3)
    guard = SpikeGuard()
    board = defaultdict(list)
    for step in range(steps):
        k = torch.multinomial(alpha, 1).item()
        x, y = domain_batch(k, n=32, t=12)
        # inject one dirty batch
        if step == 60:
            x = x.clone(); x[:] = VOCAB - 1
        logits, probs, aux, usage = model(x)
        ce = F.cross_entropy(logits[:, :-1].reshape(-1, VOCAB), x[:, 1:].reshape(-1))
        loss = ce + 0.02 * aux
        if guard.check(loss.item()):
            state.log('train', 'spike-skip', step=step, loss=round(loss.item(), 3))
            continue
        opt.zero_grad(); loss.backward()
        grad_norm = math.sqrt(sum(p.grad.pow(2).sum().item() for p in model.parameters() if p.grad is not None))
        nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        opt.step()
        if step % 20 == 0 or step == steps - 1:
            ent = float(-(usage * (usage + 1e-12).log()).sum())
            board['loss'].append(ce.item())
            board['aux'].append(aux.item())
            board['grad'].append(grad_norm)
            board['entropy'].append(ent)
            state.log('train', 'heartbeat', step=step, ce=round(ce.item(), 3),
                      aux=round(aux.item(), 3), grad=round(grad_norm, 3),
                      usage=[round(u, 3) for u in usage.tolist()])
    # domain eval
    model.eval()
    dom = []
    with torch.no_grad():
        for k in range(N_DOMAIN):
            x, y = domain_batch(k, n=64, t=12)
            logits, _, _, _ = model(x)
            dom.append(F.cross_entropy(logits[:, :-1].reshape(-1, VOCAB), x[:, 1:].reshape(-1)).item())
    model.train()
    return model, board, torch.tensor(dom), guard.spikes


moe, board, dom_L, n_spikes = train_moe(state.alpha)
state.metrics['train_board'] = {k: [round(v, 4) for v in vs] for k, vs in board.items()}
state.metrics['domain_ce'] = {d: round(v, 4) for d, v in zip(DOMAINS, dom_L.tolist())}
state.metrics['spikes'] = n_spikes
print('domain CE', state.metrics['domain_ce'], 'spikes', n_spikes)
print('Key: Stage B yields weights + health metrics; spikes were skipped instead of poisoning the run.')"""
            ),
            md(
                """## 3. 阶段 C — Expert Parallel 模拟

把 token 按专家 ID 发到对应 rank，施加 capacity，统计 drop 与通信量，再写回。"""
            ),
            code(
                """@dataclass
class EPSimulator:
    n_experts: int = N_EXPERTS
    n_ranks: int = N_EXPERTS  # 1 expert / rank for clarity
    capacity_factor: float = 1.25
    hidden: int = D_MODEL
    dtype_bytes: int = 2

    def run(self, n_tokens=2048, top_k=TOP_K):
        # random routes resembling trained usage
        usage_prior = torch.tensor([0.28, 0.24, 0.26, 0.22])
        routes = torch.multinomial(usage_prior.expand(n_tokens, -1), top_k, replacement=False)
        cap = int(self.capacity_factor * n_tokens * top_k / self.n_experts)
        loads = torch.zeros(self.n_experts)
        drops = 0
        for t in range(n_tokens):
            for k in range(top_k):
                e = int(routes[t, k])
                if loads[e] < cap:
                    loads[e] += 1
                else:
                    drops += 1
        # all-to-all bytes ~ 2 * tokens * topk * H * dtype * (P-1)/P
        P = self.n_ranks
        comm = 2 * n_tokens * top_k * self.hidden * self.dtype_bytes * (P - 1) / P
        return {
            'capacity': cap,
            'loads': loads.tolist(),
            'drop_rate': drops / (n_tokens * top_k),
            'comm_mb': comm / (1024 ** 2),
        }


ep = EPSimulator()
ep_stats = ep.run()
state.metrics['ep'] = {k: (round(v, 4) if isinstance(v, float) else v) for k, v in ep_stats.items()}
state.log('ep', 'simulate', **{k: state.metrics['ep'][k] for k in ['capacity', 'drop_rate', 'comm_mb']})
print('loads', ep_stats['loads'])
print('Key: Stage C validates CF/drop/comm before paying for multi-node jobs.')"""
            ),
            md(
                """## 4. 阶段 D — Checkpoint 打包

冻结 α、域指标、EP 假设与模型权重指纹，形成可审计发布包（对接治理模块的证据包思路）。"""
            ),
            code(
                """import hashlib
import io


def fingerprint(model):
    buf = io.BytesIO()
    torch.save({k: v.detach().cpu().half() for k, v in model.state_dict().items()}, buf)
    return hashlib.sha256(buf.getvalue()).hexdigest()[:16]


state.checkpoint = {
    'name': 'moe-code-assist-toy-v1',
    'alpha': state.metrics['alpha'],
    'domain_ce': state.metrics['domain_ce'],
    'ep_assumptions': state.metrics['ep'],
    'spikes_skipped': state.metrics['spikes'],
    'weight_fp': fingerprint(moe),
    'served_dtype': 'fp16',
    'routing': {'n_experts': N_EXPERTS, 'top_k': TOP_K},
}
state.log('ckpt', 'frozen', fp=state.checkpoint['weight_fp'])
print(state.checkpoint)
print('Key: Checkpoint metadata is the contract between training and serving teams.')"""
            ),
            md(
                """## 5. 阶段 E — Serving：连续批处理 + 专家占用

上线玩具服务：请求带 domain hint；调度器做 continuous batching；统计 prefill/decode 与专家热度。"""
            ),
            code(
                """@dataclass
class Request:
    rid: int
    domain: int
    prompt_len: int
    out_len: int
    pref: int = 0
    gen: int = 0
    stage: str = 'wait'


class MoEServer:
    def __init__(self, model, max_batched_tokens=32):
        self.model = model.eval()
        self.max_bt = max_batched_tokens
        self.waiting = []
        self.running = []
        self.done = []
        self.t = 0
        self.expert_hits = torch.zeros(N_EXPERTS)
        self.util = []

    def admit(self, reqs):
        self.waiting.extend(reqs)

    @torch.no_grad()
    def _route_stats(self, domain, n=8):
        x, _ = domain_batch(domain, n=n, t=8)
        _, probs, _, usage = self.model(x)
        self.expert_hits += usage.cpu() * n
        return usage

    def step(self):
        self.t += 1
        used = 0
        still = []
        # prefer decode
        for r in list(self.running):
            if r.stage == 'decode' and used < self.max_bt:
                r.gen += 1
                used += 1
                if r.gen >= r.out_len:
                    self.done.append(r)
                else:
                    still.append(r)
            elif r.stage == 'prefill':
                still.append(r)
        self.running = still
        # continue prefills / admit new
        i = 0
        while i < len(self.running) and used < self.max_bt:
            r = self.running[i]
            if r.stage == 'prefill':
                take = min(r.prompt_len - r.pref, self.max_bt - used)
                r.pref += take
                used += take
                if r.pref >= r.prompt_len:
                    r.stage = 'decode'
                    self._route_stats(r.domain)
            i += 1
        while self.waiting and used < self.max_bt:
            r = self.waiting.pop(0)
            r.stage = 'prefill'
            self.running.append(r)
            take = min(r.prompt_len, self.max_bt - used)
            r.pref += take
            used += take
            if r.pref >= r.prompt_len:
                r.stage = 'decode'
                self._route_stats(r.domain)
        self.util.append(used / self.max_bt)
        return used


server = MoEServer(moe)
traffic = []
for i in range(12):
    # traffic follows alpha (more code)
    d = int(torch.multinomial(state.alpha, 1))
    traffic.append(Request(i, d, prompt_len=20 + 10 * (d == 1), out_len=6 + 2 * (d == 2)))
server.admit(traffic)
while len(server.done) < len(traffic) and server.t < 80:
    server.step()

avg_util = sum(server.util) / max(len(server.util), 1)
expert_share = (server.expert_hits / server.expert_hits.sum().clamp_min(1e-6)).tolist()
state.metrics['serving'] = {
    'finished': len(server.done),
    'steps': server.t,
    'avg_util': round(avg_util, 3),
    'expert_share': [round(x, 3) for x in expert_share],
    'ttft_proxy_steps': server.t / max(len(server.done), 1),
}
state.log('serve', 'complete', **state.metrics['serving'])
print('expert_share', state.metrics['serving']['expert_share'])
print('Key: Serving must track expert hotness—imbalance becomes latency/cost in production.')"""
            ),
            md(
                """## 6. Go-Live 门禁

把训练与服务指标收成发布检查清单；任一红灯则阻断上线。"""
            ),
            code(
                """def golive_gate(metrics, ckpt):
    checks = []
    dom = metrics['domain_ce']
    worst = max(dom.values())
    checks.append(('worst_domain_ce<2.5', worst < 2.5, worst))
    checks.append(('spikes<5', metrics['spikes'] < 5, metrics['spikes']))
    checks.append(('ep_drop_rate<0.05', metrics['ep']['drop_rate'] < 0.05, metrics['ep']['drop_rate']))
    share = torch.tensor(metrics['serving']['expert_share'])
    # not too collapsed
    checks.append(('expert_entropy>1.0', float(-(share * (share + 1e-12).log()).sum()) > 1.0,
                   float(-(share * (share + 1e-12).log()).sum())))
    checks.append(('serving_util>0.4', metrics['serving']['avg_util'] > 0.4, metrics['serving']['avg_util']))
    checks.append(('checkpoint_fp_present', bool(ckpt.get('weight_fp')), ckpt.get('weight_fp')))
    ok = all(c[1] for c in checks)
    return ok, checks


ok, checks = golive_gate(state.metrics, state.checkpoint)
print('=== Go-Live Gate ===')
for name, passed, val in checks:
    print(f'{\"PASS\" if passed else \"FAIL\":<4} {name} (value={val})')
print('RELEASE' if ok else 'BLOCK', 'moe-code-assist-toy-v1')
state.metrics['golive_ok'] = ok
print('Key: E2E success is a gate on mixture/train/EP/serve together—not a single loss number.')"""
            ),
            md(
                """## 7. 端到端复盘与扩展作业

### 本案例走完的链路

```
DoReMi α → MoE 训练(+aux/+spike guard) → EP/CF 预演 → checkpoint 证据包 → continuous batch serving → Go-Live
```

### 若在真实集群落地，下一步替换点

| 玩具组件 | 生产替换 |
|---------|---------|
| Tiny domain batch | 真实分域语料 + 质量过滤 |
| 单机 MoEBlock | Megatron/DeepSpeed MoE + EP |
| Python EP 模拟 | NCCL all-to-all + token dropless/draping |
| 自写 Scheduler | vLLM / SGLang |
| 打印门禁 | CI + 模型注册表 + 人工复核 |

### 扩展挑战

1. 把 α 与路由日志联动：某域是否总进同一专家？  
2. 给 Serving 加前缀缓存（系统提示）并量命中率。  
3. 引入 PD 分离：长 code prompt prefill 专池。  
4. 对齐阶段：用单测可验证奖励对 code 域做 GRPO。"""
            ),
            code(
                """print('=== E2E Summary ===')
print('alpha', {d: round(a, 3) for d, a in zip(DOMAINS, state.alpha.tolist())})
print('domain_ce', state.metrics['domain_ce'])
print('ep', state.metrics['ep'])
print('serving', state.metrics['serving'])
print('golive', state.metrics['golive_ok'])
print('events', len(state.events))
print('Key: You now have a rehearsal script for an MoE product slice—from mixture to release gate.')"""
            ),
            md(
                """## 课后思考题

1. 若 code 域 CE 最低但线上延迟最高，可能是配比、路由还是 Serving 问题？如何用本案例日志定位？
2. Capacity factor 从 1.25 降到 1.0，Go-Live 哪一关最可能先红？训练质量与推理成本如何权衡？
3. 如何把本案例的 `ProjectState.events` 接到真正的实验追踪（W&B/MLflow）而不改训练逻辑？
4. 若增加 64 专家，Stage C/E 要先改哪些假设才有意义？

---
> 本案例是模块 20 的项目级串联。单点理论仍请回到 01/03/04/05/09 对应深挖 notebook。"""
            ),
        ],
    )

    # short module readme
    readme = """# 20_end_to_end — 项目级串联案例

把库内专题收成可跑通的交付流水线，适合作为复习课 / 面试项目 / 内部培训主线。

## 案例列表

| Notebook | 主题 | 串联模块 |
|----------|------|----------|
| [01_moe_from_mixture_to_serving.ipynb](01_moe_from_mixture_to_serving.ipynb) | MoE：配比→训练观测→EP→Serving→Go-Live | 01 / 03 / 04 / 05 / 09 / 18 |

## 怎么用

1. 按表内「串联模块」快速回看专题 notebook（可选）
2. 从头到尾运行本目录案例（CPU 可跑）
3. 尝试课后扩展：前缀缓存、PD 分离、GRPO on code

## 设计原则

- **自包含**：不依赖其他 notebook 的运行态
- **可门禁**：用 Go-Live checks 表达“上线”，而不是只看 loss
- **可替换**：每个玩具组件都标明生产对应系统
"""
    (ROOT / "20_end_to_end" / "README.md").write_text(readme, encoding="utf-8")
    print("wrote 20_end_to_end/README.md")


if __name__ == "__main__":
    build()
