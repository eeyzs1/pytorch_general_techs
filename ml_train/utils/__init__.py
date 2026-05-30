"""
共享工具模块 - 各 Notebook 可复用的通用组件

包含：
- 归一化层（RMSNorm）
- DropPath（Stochastic Depth）
- 自定义激活函数（SwiGLU）
- Transformer 基础组件
- 训练辅助工具
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import math


class RMSNorm(nn.Module):
    def __init__(self, d_model, eps=1e-6):
        super().__init__()
        self.weight = nn.Parameter(torch.ones(d_model))
        self.eps = eps

    def forward(self, x):
        rms = torch.sqrt(torch.mean(x.float() ** 2, dim=-1, keepdim=True) + self.eps)
        return (x / rms) * self.weight


class DropPath(nn.Module):
    def __init__(self, drop_prob=0.0, scale_by_keep=True):
        super().__init__()
        self.drop_prob = drop_prob
        self.scale_by_keep = scale_by_keep

    def forward(self, x):
        if self.drop_prob == 0.0 or not self.training:
            return x
        keep_prob = 1 - self.drop_prob
        shape = (x.shape[0],) + (1,) * (x.ndim - 1)
        random_tensor = keep_prob + torch.rand(shape, dtype=x.dtype, device=x.device)
        random_tensor = random_tensor.floor_()
        output = x.div(keep_prob) * random_tensor if self.scale_by_keep else x * random_tensor
        return output


class SwiGLU(nn.Module):
    def __init__(self, d_in, d_out, bias=False):
        super().__init__()
        self.w1 = nn.Linear(d_in, d_out, bias=bias)
        self.w2 = nn.Linear(d_in, d_out, bias=bias)
        self.w3 = nn.Linear(d_out, d_out, bias=bias)

    def forward(self, x):
        return self.w3(F.silu(self.w1(x)) * self.w2(x))


class FeedForward(nn.Module):
    def __init__(self, d_model, d_ff=None, dropout=0.1, activation='gelu'):
        super().__init__()
        d_ff = d_ff or 4 * d_model
        if activation == 'swiglu':
            self.net = SwiGLU(d_model, d_ff)
        else:
            self.net = nn.Sequential(
                nn.Linear(d_model, d_ff),
                nn.GELU() if activation == 'gelu' else nn.ReLU(),
                nn.Dropout(dropout),
                nn.Linear(d_ff, d_model),
                nn.Dropout(dropout),
            )

    def forward(self, x):
        return self.net(x)


class RotaryPositionalEmbedding(nn.Module):
    def __init__(self, d_model, max_seq_len=2048, theta=10000.0):
        super().__init__()
        self.d_model = d_model
        self.max_seq_len = max_seq_len
        freqs = 1.0 / (theta ** (torch.arange(0, d_model, 2).float() / d_model))
        t = torch.arange(max_seq_len).float()
        freqs = torch.outer(t, freqs)
        self.register_buffer('cos_cached', freqs.cos())
        self.register_buffer('sin_cached', freqs.sin())

    def forward(self, x, offset=0):
        seq_len = x.shape[1]
        cos = self.cos_cached[offset:offset + seq_len].unsqueeze(0).unsqueeze(0)
        sin = self.sin_cached[offset:offset + seq_len].unsqueeze(0).unsqueeze(0)
        return cos, sin


def rotate_half(x):
    x1, x2 = x.chunk(2, dim=-1)
    return torch.cat((-x2, x1), dim=-1)


def apply_rotary_emb(q, k, cos, sin):
    q_embed = (q * cos) + (rotate_half(q) * sin)
    k_embed = (k * cos) + (rotate_half(k) * sin)
    return q_embed, k_embed


def compute_model_params(d_model, n_layers, n_heads, vocab_size, d_ff=None):
    if d_ff is None:
        d_ff = 4 * d_model
    embed = vocab_size * d_model
    per_layer = (
        4 * d_model * d_model
        + 2 * d_model * d_ff
        + 2 * d_model
    )
    total = embed + n_layers * per_layer + d_model * vocab_size
    return {
        'embedding': embed,
        'per_transformer_layer': per_layer,
        'lm_head': d_model * vocab_size,
        'total': total,
        'total_M': total / 1e6,
        'total_B': total / 1e9,
    }


def gradient_clip_norm(parameters, max_norm):
    total_norm = 0.0
    for p in parameters:
        if p.grad is not None:
            param_norm = p.grad.data.norm(2)
            total_norm += param_norm.item() ** 2
    total_norm = total_norm ** 0.5
    clip_coef = max_norm / (total_norm + 1e-6)
    if clip_coef < 1:
        for p in parameters:
            if p.grad is not None:
                p.grad.data.mul_(clip_coef)
    return total_norm