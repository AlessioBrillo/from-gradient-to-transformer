"""ADR-0035: mean ablation and the one-hop direct path, on a tiny random GPT-2 (no download).

These pin the measurement code, so that stage 6, 7 or 8 cannot pass or fail because a
helper is wrong.
"""

from __future__ import annotations

import re
from pathlib import Path

import numpy as np
import pytest
import torch

from src.experiments import exp7_gpt2_small as exp7
from src.models.gpt2 import GPT2, GPT2Block, GPT2Config

ADR = (
    Path(__file__).resolve().parents[1]
    / "docs/adr/0035-gpt2-mean-ablation-and-direct-path-patching.md"
)


def _tiny() -> GPT2:
    torch.manual_seed(0)
    cfg = GPT2Config(vocab_size=97, n_positions=64, d_model=32, n_layers=3, n_heads=4)
    return GPT2(cfg).eval()


def _tokens(n: int = 6, length: int = 10, seed: int = 0) -> torch.Tensor:
    return torch.from_numpy(np.random.default_rng(seed).integers(0, 97, size=(n, length))).long()


def test_the_cache_holds_every_heads_output() -> None:
    model = _tiny()
    _, cache = model(_tokens(), cache={})
    assert cache is not None
    assert cache["blocks.1.attn.z"].shape == (6, 4, 10, 8)


def test_ablating_with_the_mean_of_identical_inputs_changes_nothing() -> None:
    """The ADR's promise: if every row is the same, the mean is the row itself."""
    model = _tiny()
    row = _tokens(1)
    batch = row.repeat(5, 1)
    means = model.mean_head_outputs(batch)
    plain, _ = model(batch)
    with model.ablate_mean([(0, 1), (2, 3)], means):
        ablated, _ = model(batch)
    assert torch.allclose(plain, ablated, atol=1e-5)


def test_ablating_with_the_mean_of_other_inputs_changes_the_output() -> None:
    model = _tiny()
    means = model.mean_head_outputs(_tokens(20, seed=1))
    x = _tokens(seed=2)
    plain, _ = model(x)
    with model.ablate_mean([(1, 0)], means):
        ablated, _ = model(x)
    assert not torch.allclose(plain, ablated, atol=1e-4)


def test_mean_ablation_restores_the_model_even_on_error() -> None:
    model = _tiny()
    means = model.mean_head_outputs(_tokens(8))
    x = _tokens(seed=3)
    plain, _ = model(x)
    with pytest.raises(RuntimeError), model.ablate_mean([(0, 0)], means):
        raise RuntimeError("boom")
    after, _ = model(x)
    assert torch.equal(plain, after)


def test_a_mean_shorter_than_the_input_is_refused() -> None:
    model = _tiny()
    means = model.mean_head_outputs(_tokens(4, length=6))
    with model.ablate_mean([(0, 0)], means), pytest.raises(ValueError):
        model(_tokens(2, length=10))


def test_the_cached_z_is_the_unablated_output() -> None:
    """`attn.z` must be recorded before any ablation, or stage 8 would measure the wrong thing."""
    model = _tiny()
    x = _tokens()
    _, plain = model(x, cache={})
    with model.ablate([(1, 2)]):
        _, masked = model(x, cache={})
    assert plain is not None and masked is not None
    assert torch.equal(plain["blocks.1.attn.z"], masked["blocks.1.attn.z"])


def test_the_per_head_slices_of_the_output_projection_add_up_to_the_layer_output() -> None:
    """Stage 8 adds `(z_c - z) W_O^h`; this checks that W_O^h is the right slice."""
    model = _tiny()
    _, cache = model(_tokens(), cache={})
    assert cache is not None
    cfg = model.cfg
    block = model.blocks[1]
    assert isinstance(block, GPT2Block)
    attn = block.attn
    z = cache["blocks.1.attn.z"][:, :, -1]
    w = attn.c_proj.weight.view(cfg.d_model, cfg.n_heads, cfg.d_head)
    summed = torch.einsum("bhj,dhj->bd", z, w) + attn.c_proj.bias
    assert torch.allclose(summed, cache["blocks.1.attn.attn_out"][:, -1], atol=1e-5)


def test_direct_path_of_identical_prompts_has_no_effect_and_clean_is_the_real_logit_diff() -> None:
    model = _tiny()
    x = _tokens(5)
    io, s = torch.tensor([1, 2, 3, 4, 5]), torch.tensor([6, 7, 8, 9, 10])
    patched, clean = exp7.direct_path_logit_differences(model, x, x, io, s)
    assert patched.shape == (3, 4, 5)
    assert torch.allclose(patched, clean.expand_as(patched), atol=1e-5)
    logits, _ = model(x)
    real = logits[:, -1].gather(1, io[:, None]) - logits[:, -1].gather(1, s[:, None])
    assert torch.allclose(clean, real.squeeze(1), atol=1e-4)


def test_direct_path_of_different_prompts_moves_the_difference_and_matches_a_manual_patch() -> None:
    model = _tiny()
    clean_x, corrupt_x = _tokens(4, seed=1), _tokens(4, seed=2)
    io, s = torch.tensor([1, 2, 3, 4]), torch.tensor([5, 6, 7, 8])
    patched, clean = exp7.direct_path_logit_differences(model, clean_x, corrupt_x, io, s)
    assert not torch.allclose(patched, clean.expand_as(patched), atol=1e-4)

    # Independent check for one head: add its contribution difference to the residual by hand.
    layer, head = 1, 2
    _, c1 = model(clean_x, cache={})
    _, c2 = model(corrupt_x, cache={})
    assert c1 is not None and c2 is not None
    cfg = model.cfg
    block = model.blocks[layer]
    assert isinstance(block, GPT2Block)
    lo, hi = head * cfg.d_head, (head + 1) * cfg.d_head
    dz = c2[f"blocks.{layer}.attn.z"][:, head, -1] - c1[f"blocks.{layer}.attn.z"][:, head, -1]
    delta = dz @ block.attn.c_proj.weight[:, lo:hi].T
    resid = c1[f"blocks.{cfg.n_layers - 1}.resid_post"][:, -1] + delta
    direction = model.wte.weight[io] - model.wte.weight[s]
    expected = (model.ln_f(resid) * direction).sum(-1)
    assert torch.allclose(patched[layer, head], expected, atol=1e-5)


def test_abc_corruption_replaces_only_the_final_s_by_a_third_name() -> None:
    names = [10, 11, 12, 13, 14]
    # "a b ... s s' to": S (=11) opens the clause and is repeated before the last token.
    tokens = torch.tensor([[1, 10, 2, 11, 3, 11, 4], [1, 11, 2, 10, 3, 10, 4]])
    io, s = torch.tensor([10, 11]), torch.tensor([11, 10])
    corrupt = exp7.abc_corrupt(tokens, io, s, names, np.random.default_rng(0))
    assert corrupt.shape == tokens.shape
    changed = (corrupt != tokens).nonzero()
    assert changed.tolist() == [[0, 5], [1, 5]]  # the repeated S, nothing else
    for row in range(2):
        new = int(corrupt[row, 5])
        assert new in names and new not in (int(io[row]), int(s[row]))


def test_random_head_sets_are_fixed_sized_distinct_and_exclude_the_targets() -> None:
    a = exp7.random_head_sets(3, exp7.NAME_MOVERS, exp7.N_CONTROL_TRIPLES)
    assert a == exp7.random_head_sets(3, exp7.NAME_MOVERS, exp7.N_CONTROL_TRIPLES)
    assert len(a) == exp7.N_CONTROL_TRIPLES
    for heads in a:
        assert len(set(heads)) == 3
        assert not set(heads) & set(exp7.NAME_MOVERS)
    pairs = exp7.random_head_sets(2, exp7.INDUCTION_HEADS, exp7.N_CONTROL_PAIRS)
    assert len(pairs) == 20 and all(len(set(p)) == 2 for p in pairs)


class _WordTokenizer:
    def __init__(self) -> None:
        self.vocab: dict[str, int] = {}

    def encode(self, text: str) -> list[int]:
        words = re.findall(r" ?\w+|[,.]", text)
        return [self.vocab.setdefault(w, len(self.vocab)) for w in words]


def test_ioi_groups_and_batches_agree_in_order() -> None:
    tok = _WordTokenizer()
    groups = exp7.ioi_groups(tok, list(exp7.NAMES), seed=0, n=60)
    batches = list(exp7.ioi_batches(_WordTokenizer(), list(exp7.NAMES), seed=0, n=60))
    assert len(groups) == len(batches)
    for (_, (tokens, io, s)), (b_tokens, b_io, b_s) in zip(groups.items(), batches):
        assert torch.equal(tokens, b_tokens) and torch.equal(io, b_io) and torch.equal(s, b_s)


def test_the_frozen_thresholds_match_adr_0035() -> None:
    """The ADR is the pre-registration; the constants must be the ones it states."""
    adr = ADR.read_text(encoding="utf-8")
    for needle in ("**10%**", "**30%**", "**20 random pairs**", "**20 random triples**", "**10**"):
        assert needle in adr, needle
    assert (exp7.ICL_GAIN_DROP, exp7.NAME_MOVER_DROP, exp7.TOP_K) == (0.10, 0.30, 10)
    assert (exp7.N_CONTROL_PAIRS, exp7.N_CONTROL_TRIPLES) == (20, 20)
    assert exp7.REFERENCE_SEEDS == (100, 101, 102)
    assert not set(exp7.REFERENCE_SEEDS) & set(exp7.SEEDS)
    assert exp7.NEGATIVE_NAME_MOVERS == ((10, 7), (11, 10))
    assert "seeds 100, 101 and 102" in adr
