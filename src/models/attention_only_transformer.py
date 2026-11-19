"""Attention-only transformer (no MLP), the model of Rung 1.

Two layers of causal multi-head attention with a hookable cache: the
smallest architecture in which one head can compose with an earlier one
(Olsson et al. 2022). Lived inside `src/experiments/exp1_induction_heads.py`
until 2026-11-16; Rung 4 and Rung 5 load its checkpoints, so it belongs with
the other models rather than inside one experiment.
"""

from typing import Optional

import torch
from torch import nn


class AttentionOnlyBlock(nn.Module):
    """A single attention-only block (no MLP)."""

    def __init__(self, d_model: int, n_heads: int) -> None:
        super().__init__()
        assert d_model % n_heads == 0
        self.d_head = d_model // n_heads
        self.n_heads = n_heads

        self.ln = nn.LayerNorm(d_model)
        self.W_Q = nn.Linear(d_model, d_model, bias=False)
        self.W_K = nn.Linear(d_model, d_model, bias=False)
        self.W_V = nn.Linear(d_model, d_model, bias=False)
        self.W_O = nn.Linear(d_model, d_model, bias=False)

        # Optional per-head ablation mask: shape (n_heads,), 1.0 = keep,
        # 0.0 = ablate. Applied to each head's output *before* W_O mixes the
        # heads together, so a zeroed head is actually a zeroed head — not an
        # arbitrary post-mixing subspace. See causal_ablation().
        self.head_mask: Optional[torch.Tensor] = None

    def forward(
        self,
        x: torch.Tensor,
        past_attn: Optional[list[torch.Tensor]] = None,
        cache: Optional[dict[str, torch.Tensor]] = None,
        cache_prefix: str = "",
    ) -> torch.Tensor:
        """One attention-only block.

        `cache` records the same tensors the `DecoderOnlyTransformer` records
        (`resid_pre`, `attn.attn_probs`, `attn.V`, `attn.attn_out`,
        `resid_mid`, `resid_post`), so the circuit-patching interventions
        (exp4) can be written once against the cache protocol instead of
        twice against two model families. `resid_mid == resid_post` here
        because there is no MLP branch.
        """
        residual = x
        x = self.ln(x)
        B, S, D = x.shape

        Q = self.W_Q(x).view(B, S, self.n_heads, self.d_head).transpose(1, 2)
        K = self.W_K(x).view(B, S, self.n_heads, self.d_head).transpose(1, 2)
        V = self.W_V(x).view(B, S, self.n_heads, self.d_head).transpose(1, 2)

        attn_scores = Q @ K.transpose(-2, -1) / (self.d_head**0.5)
        # Causal mask
        mask = torch.triu(torch.full((S, S), float("-inf"), device=x.device), diagonal=1)
        attn_scores = attn_scores + mask
        attn_probs = attn_scores.softmax(dim=-1)

        if past_attn is not None:
            past_attn.append(attn_probs.detach().cpu())

        out = attn_probs @ V  # (B, n_heads, S, d_head)
        if self.head_mask is not None:
            head_mask = self.head_mask.view(1, self.n_heads, 1, 1).to(out.device, out.dtype)
            out = out * head_mask
        out = out.transpose(1, 2).contiguous().view(B, S, D)
        attn_out = self.W_O(out)
        block_out = residual + attn_out

        if cache is not None:
            cache[f"{cache_prefix}.resid_pre"] = residual.detach().cpu()
            cache[f"{cache_prefix}.attn.attn_probs"] = attn_probs.detach().cpu()
            cache[f"{cache_prefix}.attn.V"] = V.detach().cpu()
            cache[f"{cache_prefix}.attn.attn_out"] = attn_out.detach().cpu()
            cache[f"{cache_prefix}.resid_mid"] = block_out.detach().cpu()
            cache[f"{cache_prefix}.resid_post"] = block_out.detach().cpu()

        out: torch.Tensor = block_out
        return out


class AttentionOnlyTransformer(nn.Module):
    """Decoder-only transformer with attention-only blocks (no MLP)."""

    def __init__(
        self,
        vocab_size: int,
        d_model: int,
        n_layers: int,
        n_heads: int,
        max_seq_len: int,
    ) -> None:
        super().__init__()
        self.embed = nn.Embedding(vocab_size, d_model)
        self.pos_embed = nn.Embedding(max_seq_len, d_model)
        self.blocks = nn.ModuleList([AttentionOnlyBlock(d_model, n_heads) for _ in range(n_layers)])
        self.ln_final = nn.LayerNorm(d_model)
        self.unembed = nn.Linear(d_model, vocab_size, bias=False)

    def forward(
        self,
        x: torch.Tensor,
        record_attn: bool = False,
        cache: Optional[dict[str, torch.Tensor]] = None,
    ) -> tuple[torch.Tensor, Optional[list[torch.Tensor]]]:
        B, S = x.shape
        positions = torch.arange(S, device=x.device).unsqueeze(0)
        h = self.embed(x) + self.pos_embed(positions)

        attn_records: Optional[list[torch.Tensor]] = [] if record_attn else None
        for i, block in enumerate(self.blocks):
            h = block(h, past_attn=attn_records, cache=cache, cache_prefix=f"blocks.{i}")

        h = self.ln_final(h)
        logits = self.unembed(h)
        return logits, attn_records
