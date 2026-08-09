#!/usr/bin/env python3
"""Generate third-round supplemental notebooks (remaining gaps)."""

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
    # 4.7 Training observability
    # ------------------------------------------------------------------
    write_nb(
        "04_pretraining/06_training_observability.ipynb",
        [
            md(
                """# 4.7 训练可观测性 (Training Observability)

> 🕐 预估学习时间：40分钟

大规模训练的故障往往先表现为激活爆炸、梯度消失、Loss Spike 或某层“坏死”。训练可观测性把内部统计变成可告警信号，支撑回滚与根因定位。

本节涵盖：
- 激活 / 梯度 / 权重健康看板
- Loss 归因到样本与层
- Spike 检测与自动处置
- 与检查点 / 弹性训练联动"""
            ),
            md(
                """## 1. 激活与梯度健康指标

对每层记录：激活均值/方差/最大绝对值、梯度范数、参数更新比例。异常模式常早于 loss 发散出现。"""
            ),
            code(
                """import torch
import torch.nn as nn
import torch.nn.functional as F
from collections import defaultdict

torch.manual_seed(0)


class TinyStack(nn.Module):
    def __init__(self, d=64, n=4, vocab=50):
        super().__init__()
        self.embed = nn.Embedding(vocab, d)
        self.layers = nn.ModuleList([nn.Linear(d, d) for _ in range(n)])
        self.head = nn.Linear(d, vocab)

    def forward(self, x, collect=False):
        stats = {}
        h = self.embed(x)
        for i, layer in enumerate(self.layers):
            h = F.gelu(layer(h))
            if collect:
                stats[f'L{i}.act'] = {
                    'mean': h.mean().item(),
                    'std': h.std().item(),
                    'absmax': h.abs().max().item(),
                    'nan': torch.isnan(h).any().item(),
                }
        return self.head(h.mean(1)), stats


def grad_norms(model):
    out = {}
    for n, p in model.named_parameters():
        if p.grad is not None:
            out[n] = p.grad.detach().norm().item()
    return out


model = TinyStack()
opt = torch.optim.AdamW(model.parameters(), lr=1e-2)
print('=== Activation / Gradient Health ===')
for step in range(8):
    x = torch.randint(0, 50, (16, 12))
    y = torch.randint(0, 50, (16,))
    # inject a bad batch mid-way
    if step == 4:
        x = x * 0 + 49  # pathological
    logits, stats = model(x, collect=True)
    loss = F.cross_entropy(logits, y)
    # amplify loss spike
    if step == 4:
        loss = loss * 20
    opt.zero_grad()
    loss.backward()
    g = grad_norms(model)
    opt.step()
    absmax = max(v['absmax'] for v in stats.values())
    gmax = max(g.values()) if g else 0
    flag = []
    if absmax > 50:
        flag.append('ACT_EXPLODE')
    if gmax > 100:
        flag.append('GRAD_EXPLODE')
    if any(v['nan'] for v in stats.values()):
        flag.append('NAN')
    print(f'step={step} loss={loss.item():.3f} act_absmax={absmax:.2f} grad_max={gmax:.2f} {flag}')
print(f'\\nKey: Per-layer absmax/grad norms catch pathologies before total collapse.')"""
            ),
            md(
                """## 2. Loss 归因：是哪类样本 / 哪一层？

- **样本归因**：高 loss 样本的领域/长度/语言分布  
- **层归因**：阻断某层残差写入后 loss 变化（类似 patching）"""
            ),
            code(
                """def sample_loss_attribution(model, x, y):
    model.eval()
    with torch.no_grad():
        logits, _ = model(x, collect=False)
        per = F.cross_entropy(logits, y, reduction='none')
    model.train()
    order = per.argsort(descending=True)
    return per, order


def layer_ablation_delta(model, x, y):
    '''Zero-out each layer output once and measure CE delta.'''
    base_logits, _ = model(x, collect=False)
    base = F.cross_entropy(base_logits, y).item()
    deltas = []
    hooks = []

    def make_hook():
        def hook(_m, _inp, out):
            return torch.zeros_like(out)
        return hook

    for i, layer in enumerate(model.layers):
        h = layer.register_forward_hook(make_hook())
        logits, _ = model(x, collect=False)
        loss = F.cross_entropy(logits, y).item()
        deltas.append((i, loss - base))
        h.remove()
    return base, deltas


x = torch.randint(0, 50, (32, 10))
y = torch.randint(0, 50, (32,))
per, order = sample_loss_attribution(model, x, y)
base, deltas = layer_ablation_delta(model, x[:8], y[:8])
print('=== Loss Attribution ===')
print(f'top-5 sample losses: {per[order[:5]].tolist()}')
print(f'layer ablation deltas: {deltas}')
print(f'\\nKey: High-loss samples + sensitive layers localize data bugs vs architecture bugs.')"""
            ),
            md(
                """## 3. Spike 检测与自动处置

规则示例：滚动窗口 z-score / 相对跳变；触发后：跳过 batch、降 LR、回滚检查点、告警。"""
            ),
            code(
                """class SpikeGuard:
    def __init__(self, window=20, z_thr=4.0, ratio_thr=2.5):
        self.window = window
        self.z_thr = z_thr
        self.ratio_thr = ratio_thr
        self.hist = []
        self.actions = []

    def update(self, loss, step):
        import statistics
        self.hist.append(loss)
        if len(self.hist) < 5:
            return 'ok'
        w = self.hist[-self.window:]
        mu = statistics.fmean(w[:-1])
        sd = statistics.pstdev(w[:-1]) or 1e-6
        z = (loss - mu) / sd
        ratio = loss / max(mu, 1e-6)
        if z > self.z_thr or ratio > self.ratio_thr:
            action = 'skip_batch+rollback_candidate'
            self.actions.append((step, loss, z, ratio, action))
            # do not keep spike in baseline
            self.hist.pop()
            return action
        return 'ok'


guard = SpikeGuard()
losses = [2.1, 2.0, 1.95, 1.9, 1.88, 1.85, 1.84, 1.83, 8.5, 1.82, 1.81]
print('=== Spike Guard ===')
for i, loss in enumerate(losses):
    print(f'step={i} loss={loss} -> {guard.update(loss, i)}')
print('recorded:', guard.actions)
print(f'\\nKey: Treat spikes as first-class events with skip/rollback, not just dashboard red lines.')"""
            ),
            md(
                """## 4. 看板字段清单（产业）

| 类别 | 指标 | 告警 |
|------|------|------|
| 标量 | loss/lr/grad_norm/tokens/s | z-score / SLA |
| 张量 | 层激活 absmax、注意力熵 | 阈值 |
| 数据 | 坏 batch 指纹、领域占比 | 突增 |
| 系统 | MFU、通信等待、OOMS | 趋势 |

与 W&B/MLflow/Prometheus 对接时，保留 **可复现 run_id + checkpoint 指针**。"""
            ),
            code(
                """dashboard = {
    'loss': 1.82,
    'grad_norm': 12.4,
    'act_absmax_p99': 18.2,
    'mfu': 0.41,
    'tokens_per_sec': 1.2e5,
    'spike_count_1h': 1,
}
print('=== Dashboard Snapshot ===')
for k, v in dashboard.items():
    print(f'{k}: {v}')
print(f'\\nKey: Observability is useful only when metrics map to concrete remediation playbooks.')"""
            ),
            thinking(
                "4.7 训练可观测性",
                "激活 absmax 升高但 loss 仍降，何时需要干预？",
                "样本归因如何避免把“本来就难的题”误判为脏数据？",
                "多机训练下如何聚合层统计而不拖垮吞吐？",
                "Spike 回滚与跳过 batch 的取舍如何影响最终模型质量？",
            ),
        ],
    )

    # ------------------------------------------------------------------
    # 9.11 Hardware kernels FA3 / FP8
    # ------------------------------------------------------------------
    write_nb(
        "09_inference_optimization/11_hardware_kernels.ipynb",
        [
            md(
                """# 9.11 硬件亲和与内核优化 (FlashAttention-3 / FP8)

> 🕐 预估学习时间：40分钟

算子是否吃满 GPU 吞吐，决定训练/推理成本上限。FlashAttention-3 与 FP8（Hopper）是当前硬件亲和的两条主线：减少 HBM 往返、用张量芯低精度矩阵乘。

本节涵盖：
- Roofline：算力 vs 带宽瓶颈
- FlashAttention tiling 直觉与 FA3 改进点
- FP8 缩放（E4M3/E5M2、延迟缩放）
- 融合算子与 CUDA Graph 搭配
- 选型清单"""
            ),
            md(
                """## 1. Roofline：先判断瓶颈

Arithmetic intensity = FLOPs / Bytes。低于拐点 → 带宽绑定（注意力中间矩阵常如此）；高于拐点 → 算力绑定。"""
            ),
            code(
                """def roofline_bound(flops, bytes_moved, peak_flops=1e15, peak_bw=3e12):
    '''Return time lower bounds from compute and bandwidth.'''
    t_compute = flops / peak_flops
    t_bw = bytes_moved / peak_bw
    return {
        't_compute': t_compute,
        't_bw': t_bw,
        'bound': 'compute' if t_compute > t_bw else 'bandwidth',
        'est_time': max(t_compute, t_bw),
        'intensity': flops / max(bytes_moved, 1),
    }


# Standard attention materializes S=QK^T (n x n)
def attn_costs(n, d, bytes_per=2):
    flops = 2 * n * n * d + 2 * n * n * d  # QK + AV rough
    bytes_moved = (3 * n * d + n * n) * bytes_per  # Q,K,V + S
    return flops, bytes_moved


def flash_costs(n, d, bytes_per=2, block=128):
    # never materialize full S; stream tiles
    flops = 2 * n * n * d + 2 * n * n * d
    bytes_moved = (3 * n * d) * bytes_per * 2  # extra reloads but no n^2
    return flops, bytes_moved


print('=== Roofline: Standard vs Flash Attention ===')
for n in [2048, 8192, 32768]:
    fs, bs = attn_costs(n, 128)
    ff, bf = flash_costs(n, 128)
    rs, rf = roofline_bound(fs, bs), roofline_bound(ff, bf)
    print(f'n={n}: std_bound={rs[\"bound\"]} intensity={rs[\"intensity\"]:.1f} | '
          f'flash_bound={rf[\"bound\"]} intensity={rf[\"intensity\"]:.1f} '
          f'speedup_est={rs[\"est_time\"]/rf[\"est_time\"]:.2f}x')
print(f'\\nKey: FlashAttention wins by raising arithmetic intensity (less HBM traffic).')"""
            ),
            md(
                """## 2. FlashAttention tiling 与 FA3 要点

**FA1/2**：分块 softmax，在 SRAM 累积；FA2 改善并行与调度。  
**FA3（Hopper）**：更好利用 TMA/WGMMA、异步流水、FP8 路径，进一步重叠内存与计算。

教学实现用分块在线 softmax 演示数值等价。"""
            ),
            code(
                """import math


def online_softmax_attention(Q, K, V, block=32):
    '''Exact attention via tiled online softmax (educational).'''
    import torch
    B, H, N, D = Q.shape
    out = torch.zeros(B, H, N, D)
    for i0 in range(0, N, block):
        i1 = min(i0 + block, N)
        qi = Q[:, :, i0:i1]
        # running m,l,o
        m = torch.full((B, H, i1 - i0, 1), -1e9)
        l = torch.zeros(B, H, i1 - i0, 1)
        o = torch.zeros(B, H, i1 - i0, D)
        for j0 in range(0, N, block):
            j1 = min(j0 + block, N)
            kj = K[:, :, j0:j1]
            vj = V[:, :, j0:j1]
            s = qi @ kj.transpose(-1, -2) / math.sqrt(D)
            m_new = torch.maximum(m, s.max(dim=-1, keepdim=True).values)
            exp_m = torch.exp(m - m_new)
            p = torch.exp(s - m_new)
            l = l * exp_m + p.sum(dim=-1, keepdim=True)
            o = o * exp_m + p @ vj
            m = m_new
        out[:, :, i0:i1] = o / l
    return out


B, H, N, D = 1, 2, 64, 16
Q = torch.randn(B, H, N, D)
K = torch.randn(B, H, N, D)
V = torch.randn(B, H, N, D)
ref = torch.softmax(Q @ K.transpose(-1, -2) / math.sqrt(D), dim=-1) @ V
flash = online_softmax_attention(Q, K, V, block=16)
err = (ref - flash).abs().max().item()
print('=== Tiled Online Softmax ===')
print(f'max abs error vs materialization: {err:.2e}')
print(f'Key: Tiling is mathematically equivalent but keeps n x n scores out of HBM.')"""
            ),
            md(
                """## 3. FP8：格式、缩放与稳定性

| 格式 | 动态范围 | 精度 | 常见用途 |
|------|---------|------|---------|
| E4M3 | 较小 | 较高 | 前向激活/权重 |
| E5M2 | 较大 | 较低 | 梯度 |

需要 **per-tensor / per-block scaling**；延迟缩放（delayed scaling）用历史 amax 选尺度。Hopper FP8 Tensor Core 可接近 2x BF16 吞吐。"""
            ),
            code(
                """def fake_fp8_quantize(x, emax=448.0, max_int=448):
    '''Educational absmax scale + fake cast (not bit-exact FP8).'''
    amax = x.detach().abs().amax()
    scale = amax / emax if amax > 0 else torch.tensor(1.0)
    q = torch.clamp((x / scale).round(), -max_int, max_int)
    return q * scale, scale


W = torch.randn(1024, 1024)
A = torch.randn(128, 1024)
Y = A @ W
Wq, sw = fake_fp8_quantize(W)
Aq, sa = fake_fp8_quantize(A)
Yq = Aq @ Wq
rel = (Y - Yq).norm() / Y.norm()
print('=== Fake FP8 Matmul ===')
print(f'rel error={rel.item():.4f} scaleW={sw.item():.3f} scaleA={sa.item():.3f}')

# Delayed scaling: EMA of amax
amax_ema = 0.0
print('delayed amax EMA:')
for t in range(5):
    a = torch.randn(128, 1024) * (1.0 + 0.2 * t)
    amax = a.abs().amax().item()
    amax_ema = 0.9 * amax_ema + 0.1 * amax if t else amax
    print(f'  step={t} amax={amax:.3f} ema={amax_ema:.3f}')
print(f'\\nKey: FP8 needs careful scaling; error is tolerable when amax tracked per block/tensor.')"""
            ),
            md(
                """## 4. 融合与图捕获

把 `RMSNorm + QKV + RoPE + Attention` 等串成融合核 / CUDA Graph，减少 launch 与读回。推理小 batch 时常由 CPU launch 主导延迟。"""
            ),
            code(
                """import time


def timed(fn, iters=50):
    for _ in range(5):
        fn()
    t0 = time.perf_counter()
    for _ in range(iters):
        fn()
    return (time.perf_counter() - t0) / iters


x = torch.randn(8, 256, 512)
w1 = torch.randn(512, 512)
w2 = torch.randn(512, 512)


def unfused():
    y = x @ w1
    y = F.silu(y)
    y = y @ w2
    return y


# "fused" = fewer Python dispatches (still not a real CUDA fusion)
def fusedish():
    return (F.silu(x @ w1)) @ w2


tu, tf = timed(unfused), timed(fusedish)
print('=== Dispatch Overhead (CPU micro) ===')
print(f'unfused={tu*1e3:.3f}ms fusedish={tf*1e3:.3f}ms')
print(f'Key: Real wins come from CUDA fusion + Graph capture; Python-level fusion is only illustrative.')"""
            ),
            thinking(
                "9.11 硬件亲和与内核优化",
                "长序列服务何时从“带宽绑定”转为“算力绑定”？对选型有何影响？",
                "FP8 训练中哪些层应保留 BF16？为什么？",
                "FA3 与 PagedAttention / PD 分离如何叠加？",
                "如何用 Nsight 验证优化确实提高了 MFU 而非只降了 Python 耗时？",
            ),
        ],
    )

    # ------------------------------------------------------------------
    # 18.8 AI governance / EU AI Act
    # ------------------------------------------------------------------
    write_nb(
        "18_mlops/08_ai_governance_compliance.ipynb",
        [
            md(
                """# 18.8 AI 治理与合规 (EU AI Act & Governance)

> 🕐 预估学习时间：35分钟

EU AI Act、GDPR、行业规范要求把“模型上线”变成可审计的治理流程：风险分级、数据谱系、透明披露、人工监督与事件响应。本节用可执行的检查清单与证据包结构落地。

本节涵盖：
- 风险分级（不可接受 / 高 / 有限 / 最小）
- 高风险义务映射到工程控件
- 模型卡 / 数据卡 / 评测证据包
- 运行时治理（日志、人工复核、撤回）
- 合规门禁自动化"""
            ),
            md(
                """## 1. 风险分级速查

| 级别 | 例子 | 义务强度 |
|------|------|---------|
| 不可接受 | 社会评分、裸露生物识别滥用 | 禁止 |
| 高风险 | 雇佣、信贷、关键基础设施、教育录取 | 完整合规 |
| 有限风险 | 聊天机器人 | 透明披露 |
| 最小风险 | 多数推荐/滤镜 | 自愿准则 |

通用 GPAI / 系统性风险模型另有训练数据摘要、版权、评测与事件报告义务。"""
            ),
            code(
                """from dataclasses import dataclass, field


@dataclass
class SystemProfile:
    name: str
    domain: str
    uses_biometrics: bool = False
    decides_employment_or_credit: bool = False
    is_chatbot: bool = False
    open_ended_general: bool = False
    users_eu: bool = True


def classify_risk(p: SystemProfile) -> str:
    if p.uses_biometrics and p.domain in {'surveillance', 'social_scoring'}:
        return 'unacceptable'
    if p.decides_employment_or_credit or p.domain in {'critical_infra', 'education_admission'}:
        return 'high'
    if p.is_chatbot:
        return 'limited'
    if p.open_ended_general:
        return 'gpai'
    return 'minimal'


profiles = [
    SystemProfile('social-score', 'social_scoring', uses_biometrics=True),
    SystemProfile('hire-bot', 'hr', decides_employment_or_credit=True),
    SystemProfile('support-bot', 'saas', is_chatbot=True),
    SystemProfile('gpai-base', 'foundation', open_ended_general=True),
]
print('=== Risk Classification ===')
for p in profiles:
    print(f'{p.name}: {classify_risk(p)}')
print(f'\\nKey: Classification drives which engineering controls are mandatory vs optional.')"""
            ),
            md(
                """## 2. 高风险义务 → 工程控件映射

| 法律义务 | 工程落地 |
|---------|---------|
| 风险管理 | 威胁建模 + 残留风险登记 |
| 数据治理 | 来源、许可、PII、偏见切片评估 |
| 技术文档 | 模型卡、架构图、训练配置冻结 |
| 记录保存 | 不可篡改推理日志 / 版本指纹 |
| 透明性 | 用户告知 AI 交互、能力边界 |
| 人工监督 | 高影响动作人工确认 |
| 准确性/鲁棒/安全 | 评测门禁 + 红队 + 护栏 |"""
            ),
            code(
                """CONTROLS = {
    'risk_register': False,
    'data_lineage': False,
    'model_card': False,
    'eval_gate': False,
    'immutable_logs': False,
    'user_disclosure': False,
    'human_in_loop': False,
    'red_team': False,
    'incident_runbook': False,
}


def required_controls(risk: str) -> list[str]:
    base = ['user_disclosure']
    if risk in {'limited'}:
        return base
    if risk in {'gpai'}:
        return base + ['model_card', 'data_lineage', 'eval_gate', 'immutable_logs', 'incident_runbook']
    if risk == 'high':
        return list(CONTROLS)
    return []


def compliance_gap(risk: str, enabled: dict) -> dict:
    need = required_controls(risk)
    missing = [c for c in need if not enabled.get(c, False)]
    return {'required': need, 'missing': missing, 'ready': len(missing) == 0}


enabled = dict(CONTROLS)
enabled.update(user_disclosure=True, model_card=True, eval_gate=True)
print('=== Control Gap (high-risk hire-bot) ===')
print(compliance_gap('high', enabled))
print(f'\\nKey: Translate legal text into a boolean control plane checked in CI/CD.')"""
            ),
            md(
                """## 3. 证据包：模型卡 + 数据卡 + 评测

发布前冻结一组可审计产物，哈希入库。"""
            ),
            code(
                """import hashlib
import json


def evidence_pack(model_name, metrics, data_sources, risks):
    pack = {
        'model': model_name,
        'model_card': {
            'intended_use': 'customer support drafting',
            'out_of_scope': ['legal advice', 'medical diagnosis'],
            'metrics': metrics,
        },
        'data_card': {
            'sources': data_sources,
            'pii_scrubbed': True,
            'licenses': ['MIT', 'CC-BY-4.0'],
        },
        'risks': risks,
    }
    blob = json.dumps(pack, sort_keys=True).encode()
    pack['sha256'] = hashlib.sha256(blob).hexdigest()
    return pack


pack = evidence_pack(
    'support-llm-v3',
    {'mt_bench': 7.8, 'toxicity_rate': 0.012},
    ['curated_tickets', 'public_docs'],
    ['prompt_injection', 'hallucination'],
)
print('=== Evidence Pack ===')
print(json.dumps(pack, indent=2)[:500], '...')
print(f'\\nKey: Hashed evidence packs make releases auditable and rollback-friendly.')"""
            ),
            md(
                """## 4. 运行时治理与事件响应

- 高风险动作（转账建议、解雇建议）必须 HITL  
- 日志含：模型版本、策略版本、输入哈希、护栏决策  
- 事件：检测 → 遏制（关特性）→ 通知 → 根因 → 回归测试"""
            ),
            code(
                """class RuntimeGovernor:
    def __init__(self, hitl_actions=None):
        self.hitl_actions = set(hitl_actions or [])
        self.events = []

    def authorize(self, action, user_approved=False):
        if action in self.hitl_actions and not user_approved:
            self.events.append(('block_hitl', action))
            return False, 'needs_human_approval'
        self.events.append(('allow', action))
        return True, 'ok'

    def incident(self, name, severity):
        self.events.append(('incident', name, severity))
        return {'containment': 'disable_tool:' + name, 'notify': severity >= 'sev2'}


gov = RuntimeGovernor(hitl_actions={'employment_decision', 'credit_decision'})
print('=== Runtime Governance ===')
print(gov.authorize('summarize_ticket'))
print(gov.authorize('employment_decision'))
print(gov.authorize('employment_decision', user_approved=True))
print(gov.incident('jailbreak_spike', 'sev2'))
print('trail:', gov.events)
print(f'\\nKey: Compliance continues after deploy—authorization + incident trails are mandatory evidence.')"""
            ),
            thinking(
                "18.8 AI 治理与合规",
                "GPAI 与高风险系统的义务如何同时落在“基座模型供应商”和“应用集成方”？",
                "模型卡里哪些字段对审计最关键？哪些常被虚写？",
                "如何在不存储明文用户内容的前提下保留可审计日志？",
                "合规门禁失败时，灰度发布是否允许？需要哪些补偿控制？",
            ),
        ],
    )

    # ------------------------------------------------------------------
    # 3.11 GNN + LLM
    # ------------------------------------------------------------------
    write_nb(
        "03_architecture_design/11_gnn_llm.ipynb",
        [
            md(
                """# 3.11 图神经网络与大模型 (GNN + LLM)

> 🕐 预估学习时间：40分钟

知识图谱、引用网、仓库依赖、分子结构等天然是图。GNN+LLM 组合常见于 GraphRAG、工具路由、结构化推理与科学模型。

本节涵盖：
- 图消息传递基础
- 子图检索 + LLM 推理（GraphRAG 变体）
- 图编码器作为 LLM 工具/前缀
- 联合训练与评测要点"""
            ),
            md(
                """## 1. 消息传递 GNN（教学）

节点表示通过邻居聚合迭代更新：`h_v ← σ(W · mean({h_u : u∈N(v)} ∪ {h_v}))`。"""
            ),
            code(
                """import torch
import torch.nn as nn
import torch.nn.functional as F

torch.manual_seed(0)


class MeanGCN(nn.Module):
    def __init__(self, d_in, d_hidden, n_layers=2):
        super().__init__()
        self.layers = nn.ModuleList([nn.Linear(d_in if i == 0 else d_hidden, d_hidden) for i in range(n_layers)])

    def forward(self, x, adj):
        # adj: dense (N,N) with self-loops
        deg = adj.sum(-1, keepdim=True).clamp_min(1)
        for layer in self.layers:
            x = adj @ x / deg
            x = F.relu(layer(x))
        return x


# tiny KG: 0=Alice,1=Acme,2=Bob,3=Berlin
N, D = 4, 8
x = torch.randn(N, D)
adj = torch.tensor([
    [1, 1, 0, 0],  # Alice works_at Acme
    [1, 1, 1, 0],  # Acme related Bob
    [0, 1, 1, 1],  # Bob lives Berlin
    [0, 0, 1, 1],
], dtype=torch.float)
gcn = MeanGCN(D, 16)
node_h = gcn(x, adj)
print('=== GCN Node Embeddings ===')
print(node_h.shape, node_h.norm(dim=-1).tolist())
print(f'Key: GNN injects relational inductive bias before/with language reasoning.')"""
            ),
            md(
                """## 2. 子图检索 → 线性化为 LLM 上下文

对查询实体做 k-hop 扩展，把三元组序列化成文本或软提示。"""
            ),
            code(
                """TRIPLES = [
    ('Alice', 'works_at', 'Acme'),
    ('Bob', 'works_at', 'Acme'),
    ('Bob', 'lives_in', 'Berlin'),
    ('Acme', 'located_in', 'Berlin'),
    ('Alice', 'knows', 'Bob'),
]


def retrieve_subgraph(seed: str, hops=2):
    frontier = {seed}
    got = []
    for _ in range(hops):
        new = set()
        for h, r, t in TRIPLES:
            if h in frontier or t in frontier:
                if (h, r, t) not in got:
                    got.append((h, r, t))
                new.add(h); new.add(t)
        frontier |= new
    return got


def linearize(triples):
    return '\\n'.join(f'({h})-[{r}]->({t})' for h, r, t in triples)


sub = retrieve_subgraph('Alice', hops=2)
ctx = linearize(sub)
print('=== Subgraph Retrieval ===')
print(ctx)
prompt = f'Graph context:\\n{ctx}\\n\\nQuestion: Where might Alice work geographically?'
print('prompt snippet:', prompt[:120], '...')
print(f'\\nKey: GraphRAG retrieves structure, not just similar text chunks.')"""
            ),
            md(
                """## 3. 图向量作软前缀 / 工具

把种子节点嵌入投影为 LLM 前缀，或暴露 `graph.query` 工具让 Agent 主动查图。"""
            ),
            code(
                """class GraphPrefix(nn.Module):
    def __init__(self, d_graph=16, d_llm=32, n_tokens=4):
        super().__init__()
        self.proj = nn.Linear(d_graph, n_tokens * d_llm)
        self.n_tokens = n_tokens
        self.d_llm = d_llm

    def forward(self, node_vec):
        return self.proj(node_vec).view(-1, self.n_tokens, self.d_llm)


class TinyLLM(nn.Module):
    def __init__(self, vocab=40, d=32):
        super().__init__()
        self.emb = nn.Embedding(vocab, d)
        self.rnn = nn.GRU(d, d, batch_first=True)
        self.head = nn.Linear(d, vocab)

    def forward(self, tok, prefix=None):
        h = self.emb(tok)
        if prefix is not None:
            h = torch.cat([prefix, h], dim=1)
        y, _ = self.rnn(h)
        return self.head(y)


prefixer = GraphPrefix()
llm = TinyLLM()
# Alice node vec from GCN projected
alice_prefix = prefixer(node_h[0])
tok = torch.randint(0, 40, (1, 6))
logits = llm(tok, prefix=alice_prefix)
print('=== Graph Soft Prefix ===')
print(f'prefix={tuple(alice_prefix.shape)} logits={tuple(logits.shape)}')
print(f'Key: Soft prefixes keep graph geometry in continuous space; tools keep symbolic precision.')"""
            ),
            md(
                """## 4. 联合训练与评测

- 训练：对比学习对齐（文本↔子图）、或端到端 QA loss  
- 评测：Hit@k / MRR（链接预测）、图谱问答准确率、引用忠实度  
- 风险：图噪声放大幻觉；需证据三元组强制引用"""
            ),
            code(
                """def mrr(ranks):
    return sum(1.0 / r for r in ranks) / len(ranks)


# toy: predicted ranking position of true tail
ranks = [1, 2, 1, 5, 3]
print('=== Graph+LLM Eval Toys ===')
print(f'MRR={mrr(ranks):.3f} Hit@3={sum(r<=3 for r in ranks)/len(ranks):.3f}')
print(f'\\nKey: Report both structural retrieval metrics and end-task answer faithfulness.')"""
            ),
            thinking(
                "3.11 图神经网络与大模型",
                "何时用符号化三元组上下文，何时用软前缀？",
                "图检索的 hops 过大有何风险？如何剪枝？",
                "GNN 与 LLM 分开训练 vs 联合训练的工程代价？",
                "如何防止模型忽略图证据只靠参数记忆作答？",
            ),
        ],
    )

    # ------------------------------------------------------------------
    # 13.6 Realtime speech duplex
    # ------------------------------------------------------------------
    write_nb(
        "13_multimodal/06_realtime_speech_duplex.ipynb",
        [
            md(
                """# 13.6 实时语音双工 (Realtime Speech Duplex)

> 🕐 预估学习时间：40分钟

实时语音助手需要边听边说、可打断（barge-in）、低尾音延迟。级联 ASR→LLM→TTS 与原生全双工端到端是两条主流路线。

本节涵盖：
- 延迟预算拆解
- 端点检测 / 打断 / 回声
- 流式 ASR 部分假设 → 投机回复
- 半双工状态机 vs 全双工
- 质量与安全门禁"""
            ),
            md(
                """## 1. 延迟预算

用户体感 ≈ 端点检测 + ASR 尾包 + LLM 首 token + TTS 首帧 + 网络。目标常：交互延迟 < 300–500ms。"""
            ),
            code(
                """from dataclasses import dataclass


@dataclass
class LatencyBudget:
    vad_endpoint_ms: float = 120
    asr_tail_ms: float = 80
    llm_ttft_ms: float = 150
    tts_first_chunk_ms: float = 70
    net_ms: float = 40

    def total(self):
        return (self.vad_endpoint_ms + self.asr_tail_ms + self.llm_ttft_ms +
                self.tts_first_chunk_ms + self.net_ms)


b = LatencyBudget()
print('=== Latency Budget ===')
print(f'total={b.total():.0f}ms breakdown={b}')
# speculative: start LLM on partial ASR
b2 = LatencyBudget(asr_tail_ms=20, llm_ttft_ms=150)
print(f'with partial-ASR speculation total={b2.total():.0f}ms')
print(f'\\nKey: Duplex UX is a latency budgeting problem more than a single-model accuracy problem.')"""
            ),
            md(
                """## 2. 半双工状态机：Listen → Think → Speak（可打断）

用户说话时暂停 TTS；检测到 barge-in 立即清空播放队列。"""
            ),
            code(
                """class DuplexStateMachine:
    def __init__(self):
        self.state = 'listen'
        self.playback_q = []
        self.log = []

    def on_vad(self, speaking: bool):
        if speaking and self.state == 'speak':
            self.playback_q.clear()
            self.state = 'listen'
            self.log.append('barge_in_cancel_tts')
        elif speaking:
            self.state = 'listen'
        elif self.state == 'listen':
            self.state = 'think'

    def on_partial_transcript(self, text, conf):
        if self.state == 'think' and conf > 0.7 and len(text.split()) >= 3:
            self.log.append(('speculate', text))
            self.state = 'speak'
            self.playback_q.append(' proto-reply')

    def on_final(self, text):
        self.state = 'speak'
        self.playback_q.append(f'reply({text})')
        self.log.append(('final', text))


sm = DuplexStateMachine()
sm.on_vad(True)
sm.on_vad(False)
sm.on_partial_transcript('what is the weather in', 0.82)
sm.on_vad(True)  # user interrupts
sm.on_vad(False)
sm.on_final('what is the weather in berlin')
print('=== Duplex State Machine ===')
print('state=', sm.state, 'queue=', sm.playback_q)
print('log=', sm.log)
print(f'\\nKey: Barge-in requires cancelable TTS and a single owner of playback state.')"""
            ),
            md(
                """## 3. 流式部分假设与投机回复

ASR 发出 partial hypothesis 时即可启动 LLM；若最终转写改写较大则丢弃草稿音频。类似解码投机。"""
            ),
            code(
                """def should_commit_speculation(partial: str, final: str, thr=0.6):
    ps, fs = set(partial.lower().split()), set(final.lower().split())
    if not ps:
        return False
    overlap = len(ps & fs) / len(ps)
    return overlap >= thr


cases = [
    ('weather in ber', 'weather in berlin'),
    ('weather in ber', 'tell me a joke'),
]
print('=== Speculation Commit ===')
for p, f in cases:
    print(p, '->', f, 'commit=', should_commit_speculation(p, f))
print(f'\\nKey: Speculative replies win latency only when partial ASR is stable enough.')"""
            ),
            md(
                """## 4. 全双工原生模型直觉

端到端模型同时消费音频帧并产出音频/文本 token，内部学习“何时听/何时说”。工程上仍需：
- AEC（回声消除）与设备播放参考信号  
- 打断标签 / 话轮样本  
- 安全：语音越狱、未成年人保护、录音同意"""
            ),
            code(
                """import torch
import torch.nn as nn
import torch.nn.functional as F

torch.manual_seed(0)


class DuplexToy(nn.Module):
    '''Frame in -> (transcript logits, speak-gate, codec logits).'''
    def __init__(self, d_audio=16, vocab=30, codec=40):
        super().__init__()
        self.enc = nn.GRU(d_audio, 32, batch_first=True)
        self.asr = nn.Linear(32, vocab)
        self.gate = nn.Linear(32, 1)   # P(speak)
        self.tts = nn.Linear(32, codec)

    def forward(self, frames):
        h, _ = self.enc(frames)
        return self.asr(h), torch.sigmoid(self.gate(h)), self.tts(h)


model = DuplexToy()
frames = torch.randn(2, 50, 16)
asr_logits, gate, codec = model(frames)
# simulate turn-taking loss: speak when user silent
user_speaking = torch.zeros(2, 50, 1)
user_speaking[:, :20] = 1
speak_tgt = 1 - user_speaking
gate_loss = F.binary_cross_entropy(gate, speak_tgt)
print('=== Native Duplex Toy ===')
print(f'asr={tuple(asr_logits.shape)} gate={tuple(gate.shape)} codec={tuple(codec.shape)}')
print(f'turn-taking gate loss={gate_loss.item():.4f} mean_gate={gate.mean().item():.3f}')
print(f'\\nKey: Full-duplex models must learn turn-taking, not only recognition and synthesis.')"""
            ),
            thinking(
                "13.6 实时语音双工",
                "级联与全双工在可中断性、可运维性、多语种上如何取舍？",
                "如何评估 barge-in：误打断率与响应延迟如何平衡？",
                "部分 ASR 投机在噪声环境为何容易“说错话”？",
                "语音日志的合规同意与保留期限应如何设计？",
            ),
        ],
    )

    print("done")


if __name__ == "__main__":
    build_all()
