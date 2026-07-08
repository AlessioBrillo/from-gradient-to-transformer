"""Decoder-only transformer from scratch with hookable internals.

Architecture per modern GPT-family conventions:
- RoPE positional encoding (Su et al., 2024)
- Pre-RMSNorm (instead of LayerNorm)
- ReLU activation (grokking standard)
- Multi-head attention (each head independent for interpretability)
- Hook points at every sublayer for TransformerLens compatibility
- Causal masking for autoregressive generation

Usage:
    model = DecoderOnlyTransformer(
        vocab_size=100, d_model=128, n_layers=4, n_heads=4, max_seq_len=256
    )
    logits = model(x)  # (batch, seq_len, vocab_size)
    logits, cache = model(x, return_cache=True)  # with activations
"""

from __future__ import annotations

from typing import Optional

import torch
from torch import nn


class RMSNorm(nn.Module):
    """Root Mean Square Layer Normalization.

    Pre-RMSNorm is the modern standard (Gemma, Llama, etc.).
    Unlike LayerNorm, no mean-centering — only scales by RMS.
    """

    def __init__(self, d_model: int, eps: float = 1e-6) -> None:
        super().__init__()
        self.scale = nn.Parameter(torch.ones(d_model))
        self.eps = eps

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        rms = x.norm(dim=-1, keepdim=True) / (x.size(-1) ** 0.5)
        return x / (rms + self.eps) * self.scale


class RotaryEmbedding(nn.Module):
    """Rotary Positional Embedding (RoPE) — Su et al., 2024.

    Applies rotation to query and key vectors based on position,
    giving the model a natural notion of relative position.
    """

    def __init__(self, d_head: int, max_seq_len: int = 4096, base: float = 10000.0) -> None:
        super().__init__()
        inv_freq = 1.0 / (base ** (torch.arange(0, d_head, 2).float() / d_head))
        self.register_buffer("inv_freq", inv_freq)
        self.max_seq_len = max_seq_len
        self.d_head = d_head

    def forward(self, x: torch.Tensor, position_ids: torch.Tensor) -> torch.Tensor:
        B, S = position_ids.shape
        freqs = (position_ids.float().unsqueeze(-1) * self.inv_freq.unsqueeze(0))
        cos = freqs.cos().repeat_interleave(2, dim=-1).view(B, 1, S, self.d_head)
        sin = freqs.sin().repeat_interleave(2, dim=-1).view(B, 1, S, self.d_head)
        x_rotated = x * cos + self._rotate_half(x) * sin
        return x_rotated

    @staticmethod
    def _rotate_half(x: torch.Tensor) -> torch.Tensor:
        x1, x2 = x.chunk(2, dim=-1)
        return torch.cat((-x2, x1), dim=-1)


class Attention(nn.Module):
    """Multi-head causal self-attention with RoPE."""

    def __init__(self, d_model: int, n_heads: int, max_seq_len: int, dropout: float = 0.0) -> None:
        super().__init__()
        assert d_model % n_heads == 0
        self.d_model = d_model
        self.n_heads = n_heads
        self.d_head = d_model // n_heads
        self.max_seq_len = max_seq_len

        self.W_Q = nn.Linear(d_model, d_model, bias=False)
        self.W_K = nn.Linear(d_model, d_model, bias=False)
        self.W_V = nn.Linear(d_model, d_model, bias=False)
        self.W_O = nn.Linear(d_model, d_model, bias=False)
        self.dropout = nn.Dropout(dropout)

        self.rope = RotaryEmbedding(self.d_head, max_seq_len)

        self.register_buffer(
            "causal_mask",
            torch.triu(torch.full((1, 1, max_seq_len, max_seq_len), float("-inf")), diagonal=1),
            persistent=False,
        )

    def forward(
        self,
        x: torch.Tensor,
        position_ids: torch.Tensor,
        past_kv: Optional[tuple[torch.Tensor, torch.Tensor]] = None,
        cache: Optional[dict] = None,
        cache_prefix: str = "",
    ) -> torch.Tensor:
        B, S, D = x.shape

        Q = self.W_Q(x).view(B, S, self.n_heads, self.d_head).transpose(1, 2)
        K = self.W_K(x).view(B, S, self.n_heads, self.d_head).transpose(1, 2)
        V = self.W_V(x).view(B, S, self.n_heads, self.d_head).transpose(1, 2)

        Q = self.rope(Q, position_ids)
        K = self.rope(K, position_ids)

        if past_kv is not None:
            past_K, past_V = past_kv
            K = torch.cat([past_K, K], dim=2)
            V = torch.cat([past_V, V], dim=2)

        attn_scores = Q @ K.transpose(-2, -1) / (self.d_head ** 0.5)
        attn_scores = attn_scores + self.causal_mask[:, :, :S, :K.size(2)]
        attn_probs = attn_scores.softmax(dim=-1)
        attn_probs = self.dropout(attn_probs)

        attn_out = attn_probs @ V
        attn_out = attn_out.transpose(1, 2).contiguous().view(B, S, D)
        attn_out = self.W_O(attn_out)

        if cache is not None:
            cache[f"{cache_prefix}.Q"] = Q.detach().cpu()
            cache[f"{cache_prefix}.K"] = K.detach().cpu()
            cache[f"{cache_prefix}.V"] = V.detach().cpu()
            cache[f"{cache_prefix}.attn_probs"] = attn_probs.detach().cpu()
            cache[f"{cache_prefix}.attn_out"] = attn_out.detach().cpu()

        return attn_out, (K, V)


class MLP(nn.Module):
    """Two-layer MLP with ReLU activation (grokking standard)."""

    def __init__(self, d_model: int, d_mlp: int, dropout: float = 0.0) -> None:
        super().__init__()
        self.W_in = nn.Linear(d_model, d_mlp, bias=False)
        self.W_out = nn.Linear(d_mlp, d_model, bias=False)
        self.dropout = nn.Dropout(dropout)

    def forward(
        self, x: torch.Tensor, cache: Optional[dict] = None, cache_prefix: str = ""
    ) -> torch.Tensor:
        hidden = torch.relu(self.W_in(x))
        hidden = self.dropout(hidden)
        out = self.W_out(hidden)

        if cache is not None:
            cache[f"{cache_prefix}.mlp_pre"] = hidden.detach().cpu()
            cache[f"{cache_prefix}.mlp_out"] = out.detach().cpu()

        return out


class TransformerBlock(nn.Module):
    """Single transformer block: Attention + MLP with Pre-RMSNorm and residual connections."""

    def __init__(
        self, d_model: int, n_heads: int, d_mlp: int, max_seq_len: int, dropout: float = 0.0
    ) -> None:
        super().__init__()
        self.ln_attn = RMSNorm(d_model)
        self.attn = Attention(d_model, n_heads, max_seq_len, dropout)
        self.ln_mlp = RMSNorm(d_model)
        self.mlp = MLP(d_model, d_mlp, dropout)

    def forward(
        self,
        x: torch.Tensor,
        position_ids: torch.Tensor,
        past_kv: Optional[tuple[torch.Tensor, torch.Tensor]] = None,
        cache: Optional[dict] = None,
        layer_idx: int = 0,
    ) -> tuple[torch.Tensor, Optional[tuple[torch.Tensor, torch.Tensor]]]:
        prefix = f"blocks.{layer_idx}"

        if cache is not None:
            cache[f"{prefix}.resid_pre"] = x.detach().cpu()

        h = self.ln_attn(x)
        if cache is not None:
            cache[f"{prefix}.ln_attn"] = h.detach().cpu()

        attn_out, kv = self.attn(h, position_ids, past_kv, cache, f"{prefix}.attn")
        x = x + attn_out

        if cache is not None:
            cache[f"{prefix}.resid_mid"] = x.detach().cpu()

        h = self.ln_mlp(x)
        if cache is not None:
            cache[f"{prefix}.ln_mlp"] = h.detach().cpu()

        mlp_out = self.mlp(h, cache, f"{prefix}")
        x = x + mlp_out

        if cache is not None:
            cache[f"{prefix}.resid_post"] = x.detach().cpu()

        return x, kv


class DecoderOnlyTransformer(nn.Module):
    """Full decoder-only transformer with hookable internals.

    Architecture:
        Embed → RoPE → [Block × N] → RMSNorm → Unembed

    Args:
        vocab_size: Size of vocabulary.
        d_model: Residual stream dimension.
        n_layers: Number of transformer blocks.
        n_heads: Number of attention heads per block.
        d_mlp: MLP hidden dimension (typically 4× d_model).
        max_seq_len: Maximum sequence length.
        dropout: Dropout probability.
        tie_weights: Tie embedding and unembedding weights.
        normalize_embed: Normalize embedding weights after each step.
    """

    def __init__(
        self,
        vocab_size: int,
        d_model: int = 128,
        n_layers: int = 4,
        n_heads: int = 4,
        d_mlp: Optional[int] = None,
        max_seq_len: int = 256,
        dropout: float = 0.0,
        tie_weights: bool = False,
        normalize_embed: bool = False,
    ) -> None:
        super().__init__()
        self.d_model = d_model
        self.n_layers = n_layers
        self.n_heads = n_heads
        self.max_seq_len = max_seq_len
        self.normalize_embed = normalize_embed

        if d_mlp is None:
            d_mlp = 4 * d_model
        self.d_mlp = d_mlp

        self.embed = nn.Embedding(vocab_size, d_model)
        self.blocks = nn.ModuleList([
            TransformerBlock(d_model, n_heads, d_mlp, max_seq_len, dropout)
            for _ in range(n_layers)
        ])
        self.ln_final = RMSNorm(d_model)
        self.unembed = nn.Linear(d_model, vocab_size, bias=False)

        if tie_weights:
            self.unembed.weight = self.embed.weight

        self._init_weights()

    def _init_weights(self) -> None:
        for p in self.parameters():
            if p.ndim >= 2:
                nn.init.normal_(p, mean=0.0, std=0.02)

    def normalize_embeddings(self) -> None:
        if self.normalize_embed:
            with torch.no_grad():
                self.embed.weight.data = nn.functional.normalize(self.embed.weight.data, dim=-1)

    def forward(
        self,
        x: torch.Tensor,
        return_cache: bool = False,
        past_kv: Optional[list[Optional[tuple[torch.Tensor, torch.Tensor]]]] = None,
    ) -> tuple[torch.Tensor, Optional[dict]]:
        B, S = x.shape
        device = x.device

        position_ids = torch.arange(S, device=device).unsqueeze(0).expand(B, -1)

        h = self.embed(x)

        cache: Optional[dict] = {} if return_cache else None

        if cache is not None:
            cache["hook_embed"] = h.detach().cpu()

        new_past_kv: list[Optional[tuple[torch.Tensor, torch.Tensor]]] = []

        for i, block in enumerate(self.blocks):
            past_kv_i = past_kv[i] if past_kv is not None and i < len(past_kv) else None
            h, kv = block(h, position_ids, past_kv_i, cache, i)
            new_past_kv.append(kv)

        h = self.ln_final(h)

        if cache is not None:
            cache["hook_ln_final"] = h.detach().cpu()

        logits = self.unembed(h)

        if cache is not None:
            cache["hook_logits"] = logits.detach().cpu()

        return logits, cache

    @torch.no_grad()
    def generate(
        self,
        input_ids: torch.Tensor,
        max_new_tokens: int = 50,
        temperature: float = 1.0,
        top_k: Optional[int] = None,
    ) -> torch.Tensor:
        self.eval()
        generated = input_ids.clone()
        past_kv: list[Optional[tuple[torch.Tensor, torch.Tensor]]] = [None] * self.n_layers

        for _ in range(max_new_tokens):
            if generated.size(1) > self.max_seq_len:
                generated = generated[:, -self.max_seq_len:]

            logits, cache = self(generated[:, -1:], past_kv=past_kv)

            if cache is not None:
                for i in range(self.n_layers):
                    prefix = f"blocks.{i}.attn"
                    if f"{prefix}.K" in cache and f"{prefix}.V" in cache:
                        new_k = cache[f"{prefix}.K"]
                        new_v = cache[f"{prefix}.V"]
                        if past_kv[i] is not None:
                            past_k = past_kv[i][0]
                            past_v = past_kv[i][1]
                            past_k = torch.cat([past_k, new_k.to(past_k.device)], dim=2)
                            past_v = torch.cat([past_v, new_v.to(past_v.device)], dim=2)
                            past_kv[i] = (past_k, past_v)
                        else:
                            past_kv[i] = (
                                new_k.to(device=generated.device), new_v.to(device=generated.device)
                            )

            next_token_logits = logits[:, -1, :] / temperature

            if top_k is not None:
                top_k_values, _ = torch.topk(next_token_logits, top_k, dim=-1)
                next_token_logits[next_token_logits < top_k_values[:, -1:]] = float("-inf")

            probs = torch.softmax(next_token_logits, dim=-1)
            next_token = torch.multinomial(probs, num_samples=1)
            generated = torch.cat([generated, next_token], dim=-1)

        return generated
