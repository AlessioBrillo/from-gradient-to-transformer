"""GPT-2 in plain PyTorch, with the repository's hookable cache (Rung 7).

The shared `DecoderOnlyTransformer` uses RMSNorm and rotary embeddings, so it cannot
load GPT-2's weights. This is the GPT-2 architecture itself (Radford et al. 2019):
learned absolute positions, pre-LayerNorm blocks, a GELU (tanh approximation) MLP, and
an unembedding tied to the token embedding.

It speaks the same protocol as the other models, so `induction_detection` applies
unchanged: `forward(x, cache={})` returns `(logits, cache)`, and the cache holds
`blocks.{i}.attn.attn_probs` of shape `(batch, heads, query, key)`.

The Hugging Face `transformers` package is imported only by `from_pretrained` and by
`load_hf_state_dict`'s callers; the model itself does not need it.

Parity with `transformers.GPT2LMHeadModel` is stage 1 of ADR-0034 and is tested in
`tests/test_gpt2_parity.py`.
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from typing import Optional, cast

import torch
from torch import nn


@dataclass(frozen=True)
class GPT2Config:
    vocab_size: int = 50257
    n_positions: int = 1024
    d_model: int = 768
    n_layers: int = 12
    n_heads: int = 12
    layer_norm_eps: float = 1e-5

    @property
    def d_head(self) -> int:
        return self.d_model // self.n_heads


class GPT2Attention(nn.Module):
    """Causal multi-head self-attention. `head_mask` zeroes a head's output."""

    def __init__(self, cfg: GPT2Config) -> None:
        super().__init__()
        self.n_heads, self.d_head, self.d_model = cfg.n_heads, cfg.d_head, cfg.d_model
        self.c_attn = nn.Linear(cfg.d_model, 3 * cfg.d_model)
        self.c_proj = nn.Linear(cfg.d_model, cfg.d_model)
        self.head_mask: Optional[torch.Tensor] = None
        mask = torch.tril(torch.ones(cfg.n_positions, cfg.n_positions, dtype=torch.bool))
        self.register_buffer("causal", mask, persistent=False)

    def forward(
        self, x: torch.Tensor, cache: Optional[dict] = None, prefix: str = ""
    ) -> torch.Tensor:
        B, S, D = x.shape
        q, k, v = self.c_attn(x).split(D, dim=2)
        q, k, v = (t.view(B, S, self.n_heads, self.d_head).transpose(1, 2) for t in (q, k, v))
        scores = q @ k.transpose(-2, -1) / self.d_head**0.5
        scores = scores.masked_fill(~self.causal[:S, :S], float("-inf"))  # type: ignore[index]
        probs = scores.softmax(dim=-1)
        heads = probs @ v  # (B, heads, S, d_head)
        if self.head_mask is not None:
            heads = heads * self.head_mask.to(heads.dtype).view(1, -1, 1, 1)
        out = self.c_proj(heads.transpose(1, 2).reshape(B, S, D))
        if cache is not None:
            cache[f"{prefix}.attn.attn_probs"] = probs.detach()
            cache[f"{prefix}.attn.V"] = v.detach()
            cache[f"{prefix}.attn.attn_out"] = out.detach()
        return out


class GPT2Block(nn.Module):
    def __init__(self, cfg: GPT2Config) -> None:
        super().__init__()
        self.ln_1 = nn.LayerNorm(cfg.d_model, eps=cfg.layer_norm_eps)
        self.attn = GPT2Attention(cfg)
        self.ln_2 = nn.LayerNorm(cfg.d_model, eps=cfg.layer_norm_eps)
        self.mlp = nn.Sequential(
            nn.Linear(cfg.d_model, 4 * cfg.d_model),
            nn.GELU(approximate="tanh"),
            nn.Linear(4 * cfg.d_model, cfg.d_model),
        )

    def forward(
        self, x: torch.Tensor, cache: Optional[dict] = None, prefix: str = ""
    ) -> torch.Tensor:
        if cache is not None:
            cache[f"{prefix}.resid_pre"] = x.detach()
        x = x + self.attn(self.ln_1(x), cache, prefix)
        if cache is not None:
            cache[f"{prefix}.resid_mid"] = x.detach()
        x = x + self.mlp(self.ln_2(x))
        if cache is not None:
            cache[f"{prefix}.resid_post"] = x.detach()
        return x


class GPT2(nn.Module):
    def __init__(self, cfg: GPT2Config = GPT2Config()) -> None:
        super().__init__()
        self.cfg = cfg
        self.wte = nn.Embedding(cfg.vocab_size, cfg.d_model)
        self.wpe = nn.Embedding(cfg.n_positions, cfg.d_model)
        self.blocks = nn.ModuleList(GPT2Block(cfg) for _ in range(cfg.n_layers))
        self.ln_f = nn.LayerNorm(cfg.d_model, eps=cfg.layer_norm_eps)

    def forward(
        self, x: torch.Tensor, cache: Optional[dict] = None
    ) -> tuple[torch.Tensor, Optional[dict]]:
        pos = torch.arange(x.size(1), device=x.device)
        h = self.wte(x) + self.wpe(pos)
        for i, block in enumerate(self.blocks):
            h = block(h, cache, f"blocks.{i}")
        h = self.ln_f(h)
        if cache is not None:
            cache["ln_final"] = h.detach()
        return h @ self.wte.weight.T, cache  # the unembedding is tied to wte

    # ------------------------------------------------------------------ ablation
    def set_head_mask(self, heads: Iterable[tuple[int, int]]) -> None:
        """Zero the output of the given (layer, head) pairs; an empty list clears it."""
        heads = list(heads)
        attns = [cast(GPT2Block, block).attn for block in self.blocks]
        for attn in attns:
            attn.head_mask = None
        for layer in {layer for layer, _ in heads}:
            mask = torch.ones(self.cfg.n_heads)
            for lay, head in heads:
                if lay == layer:
                    mask[head] = 0.0
            attns[layer].head_mask = mask

    # ------------------------------------------------------------------ weights
    def load_hf_state_dict(self, sd: dict[str, torch.Tensor]) -> None:
        """Load a Hugging Face GPT-2 state dict (its `Conv1D` weights are transposed).

        Strict: a missing or unexpected key raises instead of silently leaving
        random weights in place.
        """
        sd = {k.removeprefix("transformer."): v for k, v in sd.items()}
        mapped: dict[str, torch.Tensor] = {
            "wte.weight": sd["wte.weight"],
            "wpe.weight": sd["wpe.weight"],
            "ln_f.weight": sd["ln_f.weight"],
            "ln_f.bias": sd["ln_f.bias"],
        }
        for i in range(self.cfg.n_layers):
            h = f"h.{i}."
            b = f"blocks.{i}."
            for ln_src, ln_dst in (("ln_1", "ln_1"), ("ln_2", "ln_2")):
                mapped[f"{b}{ln_dst}.weight"] = sd[f"{h}{ln_src}.weight"]
                mapped[f"{b}{ln_dst}.bias"] = sd[f"{h}{ln_src}.bias"]
            for src, dst in (
                ("attn.c_attn", "attn.c_attn"),
                ("attn.c_proj", "attn.c_proj"),
                ("mlp.c_fc", "mlp.0"),
                ("mlp.c_proj", "mlp.2"),
            ):
                mapped[f"{b}{dst}.weight"] = sd[f"{h}{src}.weight"].T.contiguous()
                mapped[f"{b}{dst}.bias"] = sd[f"{h}{src}.bias"]
        self.load_state_dict(mapped, strict=True)

    @classmethod
    def from_pretrained(cls, name: str = "openai-community/gpt2") -> "GPT2":
        """Load published weights. Needs the optional `real` extra (transformers)."""
        from transformers import GPT2LMHeadModel  # imported here: optional dependency

        hf = GPT2LMHeadModel.from_pretrained(name)
        c = hf.config
        model = cls(
            GPT2Config(
                vocab_size=c.vocab_size,
                n_positions=c.n_positions,
                d_model=c.n_embd,
                n_layers=c.n_layer,
                n_heads=c.n_head,
                layer_norm_eps=c.layer_norm_epsilon,
            )
        )
        model.load_hf_state_dict(hf.state_dict())
        return model.eval()
