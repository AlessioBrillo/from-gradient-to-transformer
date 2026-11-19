"""One-layer transformer for modular addition, the model of Rung 2.

The Nanda et al. (ICLR 2023) configuration. Lived inside
`src/experiments/exp2_grokking.py` until 2026-11-16.
"""

from typing import Optional

import torch
from torch import nn


class OneLayerTransformer(nn.Module):
    """Single-layer decoder-only transformer for modular addition.

    Architecture per Nanda et al. (ICLR 2023):
    - Embedding: d_model (maps input tokens to dense vectors)
    - Positional embedding: learned per position (2 positions: a and b)
    - One attention block with n_heads
    - One MLP block with ReLU
    - LayerNorm pre each block
    - Unembedding: maps residual stream to vocabulary
    """

    def __init__(
        self,
        d_model: int,
        d_mlp: int,
        n_heads: int,
        modulus: int,
        max_positions: int = 2,
        normalize_embed: bool = True,
        use_layernorm: bool = True,
    ) -> None:
        super().__init__()
        assert d_model % n_heads == 0
        self.d_model = d_model
        self.d_head = d_model // n_heads
        self.n_heads = n_heads
        self.modulus = modulus
        self.normalize_embed = normalize_embed
        # Nanda et al.'s grokking model has no LayerNorm; Identity keeps the
        # attribute names (ln1/ln2/ln_final) so downstream analysis code works.
        self.use_layernorm = use_layernorm

        def _ln() -> nn.Module:
            return nn.LayerNorm(d_model) if use_layernorm else nn.Identity()

        self.embed = nn.Embedding(modulus, d_model)
        self.pos_embed = nn.Embedding(max_positions, d_model)

        # Attention
        self.ln1 = _ln()
        self.W_Q = nn.Linear(d_model, d_model, bias=False)
        self.W_K = nn.Linear(d_model, d_model, bias=False)
        self.W_V = nn.Linear(d_model, d_model, bias=False)
        self.W_O = nn.Linear(d_model, d_model, bias=False)

        # MLP
        self.ln2 = _ln()
        self.W_in = nn.Linear(d_model, d_mlp, bias=False)
        self.W_out = nn.Linear(d_mlp, d_model, bias=False)

        # Unembed
        self.ln_final = _ln()
        self.unembed = nn.Linear(d_model, modulus, bias=False)

    def normalize_embeddings(self) -> None:
        if self.normalize_embed:
            with torch.no_grad():
                self.embed.weight.data = nn.functional.normalize(self.embed.weight.data, dim=-1)
                self.unembed.weight.data = nn.functional.normalize(self.unembed.weight.data, dim=-1)

    def forward(
        self, x: torch.Tensor, return_activations: bool = False
    ) -> tuple[torch.Tensor, Optional[dict[str, torch.Tensor]]]:
        """Forward pass.

        Args:
            x: (B, 2) tensor with (a, b) token indices.
            return_activations: if True, return intermediate activations for analysis.

        Returns:
            Tuple of (logits, activations_dict). Logits shape: (B, modulus).
        """
        B = x.shape[0]
        positions = torch.arange(2, device=x.device).unsqueeze(0)

        h = self.embed(x) + self.pos_embed(positions)  # (B, 2, d_model)

        activations: Optional[dict[str, torch.Tensor]] = {} if return_activations else None

        # Attention block
        h_ln = self.ln1(h)
        Q = self.W_Q(h_ln).view(B, 2, self.n_heads, self.d_head).transpose(1, 2)
        K = self.W_K(h_ln).view(B, 2, self.n_heads, self.d_head).transpose(1, 2)
        V = self.W_V(h_ln).view(B, 2, self.n_heads, self.d_head).transpose(1, 2)

        attn_scores = Q @ K.transpose(-2, -1) / (self.d_head**0.5)
        # No causal mask needed for 2 positions (full visibility)
        attn_probs = attn_scores.softmax(dim=-1)

        if activations is not None:
            activations["attn_probs"] = attn_probs.detach().cpu()
            activations["embed"] = self.embed.weight.data.detach().cpu()

        attn_out = attn_probs @ V  # (B, n_heads, 2, d_head)
        attn_out = attn_out.transpose(1, 2).contiguous().view(B, 2, self.d_model)
        attn_out = self.W_O(attn_out)
        h = h + attn_out

        # MLP block
        h_ln = self.ln2(h)
        mlp_out = self.W_out(torch.relu(self.W_in(h_ln)))
        h = h + mlp_out

        # Final prediction from the last position
        h_final = self.ln_final(h[:, -1, :])
        logits = self.unembed(h_final)

        return logits, activations
