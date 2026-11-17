"""Stage 1 of ADR-0034: this GPT-2 equals the Hugging Face reference.

The architecture is checked on a small randomly initialised model, so the test needs
no download and runs anywhere `transformers` is installed (the optional `real` extra).
The real weights are checked by the experiment itself, which refuses to continue past
stage 1 if the same comparison fails there.
"""

from __future__ import annotations

import pytest
import torch

from src.models.gpt2 import GPT2, GPT2Config

transformers = pytest.importorskip("transformers")

SMALL = dict(vocab_size=97, n_positions=40, n_embd=32, n_layer=3, n_head=4)


def _pair(seed: int = 0):
    torch.manual_seed(seed)
    ref = transformers.GPT2LMHeadModel(
        transformers.GPT2Config(attn_implementation="eager", **SMALL)
    ).eval()
    # random init leaves biases at zero; randomise everything so a transposed or
    # mis-mapped weight cannot hide
    with torch.no_grad():
        for p in ref.parameters():
            p.add_(0.05 * torch.randn_like(p))
    mine = GPT2(
        GPT2Config(
            vocab_size=SMALL["vocab_size"],
            n_positions=SMALL["n_positions"],
            d_model=SMALL["n_embd"],
            n_layers=SMALL["n_layer"],
            n_heads=SMALL["n_head"],
        )
    )
    mine.load_hf_state_dict(ref.state_dict())
    return ref, mine.eval()


def test_logits_match_the_reference() -> None:
    ref, mine = _pair()
    x = torch.randint(0, SMALL["vocab_size"], (3, 23))
    with torch.no_grad():
        expected = ref(x).logits
        got, _ = mine(x)
    assert torch.allclose(got, expected, atol=1e-4), (got - expected).abs().max()


def test_every_residual_stream_matches_the_reference() -> None:
    ref, mine = _pair(1)
    x = torch.randint(0, SMALL["vocab_size"], (2, 17))
    with torch.no_grad():
        hidden = ref(x, output_hidden_states=True).hidden_states
        _, cache = mine(x, cache={})
    assert cache is not None
    n = SMALL["n_layer"]
    for i in range(n):  # hidden_states[i] is the input to block i
        assert torch.allclose(cache[f"blocks.{i}.resid_pre"], hidden[i], atol=1e-4), i
    # the last entry has ln_f applied
    assert torch.allclose(cache["ln_final"], hidden[n], atol=1e-4)


def test_attention_patterns_match_the_reference() -> None:
    ref, mine = _pair(2)
    x = torch.randint(0, SMALL["vocab_size"], (2, 11))
    with torch.no_grad():
        attentions = ref(x, output_attentions=True).attentions
        _, cache = mine(x, cache={})
    assert cache is not None
    for i, expected in enumerate(attentions):
        assert torch.allclose(cache[f"blocks.{i}.attn.attn_probs"], expected, atol=1e-5), i


def test_a_wrong_weight_mapping_is_caught() -> None:
    """The test would be vacuous if a transposed matrix still matched."""
    ref, mine = _pair(3)
    sd = ref.state_dict()
    sd["transformer.h.0.mlp.c_fc.weight"] = sd["transformer.h.0.mlp.c_fc.weight"] * 1.1
    broken = GPT2(mine.cfg)
    broken.load_hf_state_dict(sd)
    x = torch.randint(0, SMALL["vocab_size"], (2, 9))
    with torch.no_grad():
        assert not torch.allclose(broken.eval()(x)[0], ref(x).logits, atol=1e-3)


def test_loading_a_state_dict_with_a_missing_key_raises() -> None:
    ref, mine = _pair(4)
    sd = dict(ref.state_dict())
    del sd["transformer.h.1.attn.c_proj.weight"]
    with pytest.raises(KeyError):
        mine.load_hf_state_dict(sd)


def test_ablating_a_head_changes_the_output_and_clearing_restores_it() -> None:
    _, mine = _pair(5)
    x = torch.randint(0, SMALL["vocab_size"], (2, 13))
    with torch.no_grad():
        base = mine(x)[0]
        mine.set_head_mask([(1, 2)])
        ablated = mine(x)[0]
        mine.set_head_mask([])
        restored = mine(x)[0]
    assert not torch.allclose(base, ablated, atol=1e-4)
    assert torch.allclose(base, restored)
