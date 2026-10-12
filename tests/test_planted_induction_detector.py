"""Planted-construction tests for the induction-head detector (Rung 1).

Why this file exists: every "0 heads detected" result in this repository is a
statement about *this detector*, not about the model. The detector has a
recorded history of bugs that made its output untrustworthy — the 2026-08-01
audit found `diag1_mass` summed across heads (a [0, n_heads]-scale number
plotted against a per-head 0.3 threshold: "mass ~1.0 but 0 heads detected"
was never a detection failure, it was a unit mismatch), and the ablation
intervention hooked a post-mixing tensor instead of a head.

A negative result ("no induction head at this scale") is only interpretable if
the detector provably fires on a head that is *known* to be there. These tests
construct such heads two ways and require detection, plus the controls that
must NOT fire:

1. pattern level — a stub model emits planted attention tensors through the
   detector's real collection path (`_attention_patterns` -> threshold);
2. weights level — a real `AttentionOnlyTransformer` with W_Q/W_K planted so
   that content-blind position arithmetic produces the diag+1 pattern.

Every control here is a falsifier: if the threshold, the per-head scoping, the
offset convention, or the hook plumbing regresses, these fail.
"""

from __future__ import annotations

import torch
from torch import nn
from torch.utils.data import DataLoader, TensorDataset

from src.experiments.exp1_induction_heads import (
    AttentionOnlyTransformer,
    analyze_induction_heads,
    compute_attention_entropy,
)

THRESHOLD = 0.3  # the per-head detection threshold analyze_induction_heads uses
S, V, D = 6, 8, 6
N_SAMPLES = 32  # analyze_induction_heads collects until 32 * n_layers patterns


def _loader() -> DataLoader:
    """A loader whose inputs are irrelevant to the planted patterns."""
    data = TensorDataset(
        torch.randint(0, V, (N_SAMPLES, S)), torch.zeros(N_SAMPLES, S - 1, dtype=torch.long)
    )
    return DataLoader(data, batch_size=1)


def _planted_patterns(
    masses: list[list[float]], batch_size: int, seq_len: int
) -> list[torch.Tensor]:
    """One (batch, heads, S, S) tensor per layer with planted diag+1 mass.

    Per head, every query q >= 1 puts exactly `m` of its probability on key
    q-1 (the induction signature in a repeated-prefix task: the token after
    the previous occurrence of the current token sits at q-1) and spreads
    the rest over the remaining causal keys. Query 0 has no q-1 and is
    uniform. A head planted this way has diag+1 mass exactly `m` for any
    seq_len, which makes the detector's threshold arithmetic checkable.
    """
    layers = []
    for layer_masses in masses:
        n_heads = len(layer_masses)
        probs = torch.zeros(batch_size, n_heads, seq_len, seq_len)
        for h, m in enumerate(layer_masses):
            for q in range(seq_len):
                n_keys = q + 1  # causal: keys 0..q
                row = torch.full((n_keys,), (1.0 - m) / max(n_keys - 1, 1))
                if q >= 1:
                    row[q - 1] = m
                probs[:, h, q, :n_keys] = row
        layers.append(probs)
    return layers


class _StubPatternModel(nn.Module):
    """A stand-in model that emits planted attention patterns.

    `_attention_patterns` dispatches on the forward signature
    (`record_attn` in co_varnames) — the same first branch
    `AttentionOnlyTransformer` takes — so the detector's real collection path
    runs with the patterns themselves under test control.
    """

    def __init__(self, masses: list[list[float]]) -> None:
        super().__init__()
        self._masses = masses
        self.blocks = [None] * len(masses)  # len(model.blocks) is the layer count

    def forward(self, x: torch.Tensor, record_attn: bool = False):
        if not record_attn:
            return None, None
        batch_size, seq_len = x.shape
        return None, _planted_patterns(self._masses, batch_size, seq_len)


def _plant_shift_head(model: AttentionOnlyTransformer) -> None:
    """Plant a diag+1-attending head in a real model via W_Q/W_K.

    With token embeddings zeroed and pos_embed = I, the LayerNormed keys are
    a softmax-invariant affine image of the position one-hots, so the causal
    score between query i and key j is (up to constants) <W_Q e_i, W_K e_j>.
    W_Q = shift^T with W_K = I makes every query attend to position i-1 with
    no dependence on token content: a head with the induction signature,
    built from weights rather than trained. Validated to give diag+1 mass
    ~0.87 at seq_len=6 — comfortably over the 0.3 threshold, with the
    controls (self-attention, uniform) at 0.05 and 0.29.
    """
    with torch.no_grad():
        model.embed.weight.zero_()
        model.pos_embed.weight.copy_(torch.eye(model.pos_embed.num_embeddings))
        block = model.blocks[0]
        shift = torch.zeros(S, S)
        for i in range(1, S):
            shift[i, i - 1] = 1.0
        shift[0, 0] = 1.0
        block.W_Q.weight.copy_(shift.T)
        block.W_K.weight.copy_(torch.eye(S))


def _plant_self_head(model: AttentionOnlyTransformer) -> None:
    """Negative control: every query attends to itself (the wrong offset)."""
    with torch.no_grad():
        model.embed.weight.zero_()
        model.pos_embed.weight.copy_(torch.eye(model.pos_embed.num_embeddings))
        block = model.blocks[0]
        block.W_Q.weight.copy_(torch.eye(S))
        block.W_K.weight.copy_(torch.eye(S))


def _plant_uniform_head(model: AttentionOnlyTransformer) -> None:
    """Negative control: W_Q = 0 zeroes all scores -> uniform causal attention."""
    with torch.no_grad():
        model.blocks[0].W_Q.weight.zero_()


def _fresh_model() -> AttentionOnlyTransformer:
    torch.manual_seed(0)
    return AttentionOnlyTransformer(
        vocab_size=V, d_model=D, n_layers=1, n_heads=1, max_seq_len=S
    )


class TestPlantedDiag1Detector:
    """The 0.3-threshold detector on planted attention patterns.

    analyze_induction_heads had no test of its threshold decision at all
    before this file: its entire output ("0/8 heads") rested on code whose
    only exercise was real training runs.
    """

    def test_detects_planted_head_above_threshold(self) -> None:
        heads, _ = analyze_induction_heads(_StubPatternModel([[0.6]]), _loader())
        assert heads == [[0]], f"planted 0.6 head must be detected, got {heads}"

    def test_rejects_weak_head_below_threshold(self) -> None:
        heads, _ = analyze_induction_heads(_StubPatternModel([[0.1]]), _loader())
        assert heads == [[]], f"planted 0.1 head must not be detected, got {heads}"

    def test_rejects_two_weak_heads_not_summed(self) -> None:
        """Two 0.2 heads must not trip a 0.3 threshold.

        This is the 2026-08-01 scale bug applied to the threshold path: a
        summed-across-heads mass of 0.4 would falsely detect here.
        """
        heads, _ = analyze_induction_heads(_StubPatternModel([[0.2, 0.2]]), _loader())
        assert heads == [[]], f"0.2 + 0.2 is still below threshold, got {heads}"

    def test_per_head_independence(self) -> None:
        """A 0.6 head and a 0.0 head: exactly one detection, not an average.

        Cross-head averaging would put both at 0.3 — on the threshold, where
        `> 0.3` is false — and still lose the real head.
        """
        heads, _ = analyze_induction_heads(_StubPatternModel([[0.6, 0.0]]), _loader())
        assert heads == [[0]], f"only the planted head may be detected, got {heads}"

    def test_wrong_offset_not_detected(self) -> None:
        """Attending to q-2 (a previous *occurrence* without the +1 copy
        step) is not the induction signature and must not be detected."""

        class _OffsetTwoStub(_StubPatternModel):
            def forward(self, x: torch.Tensor, record_attn: bool = False):
                if not record_attn:
                    return None, None
                batch_size, seq_len = x.shape
                # Same planted mass, but parked at q-2: what a duplicate-token
                # head looks like *before* the K-composition step copies the
                # following token.
                layers = _planted_patterns(self._masses, batch_size, seq_len)
                for layer in layers:
                    for q in range(2, seq_len):
                        layer[:, :, q, q - 1] = 0.0
                        layer[:, :, q, q - 2] = 0.6
                        row = layer[:, :, q, : q + 1]
                        layer[:, :, q, : q + 1] = row / row.sum(dim=-1, keepdim=True)
                return None, layers

        heads, _ = analyze_induction_heads(_OffsetTwoStub([[0.6]]), _loader())
        assert heads == [[]], f"q-2 offset must not be detected, got {heads}"

    def test_uniform_not_detected(self) -> None:
        """Uniform causal attention (~1/(q+1) per key) must not trip the
        detector — its mean diag+1 mass is ~0.29 at this seq_len, just under
        the threshold, which also pins what 'uniform' means numerically."""
        probs = torch.zeros(N_SAMPLES, 1, S, S)
        for q in range(S):
            probs[:, 0, q, : q + 1] = 1.0 / (q + 1)

        class _UniformStub(_StubPatternModel):
            def forward(self, x, record_attn=False):
                if not record_attn:
                    return None, None
                batch_size, _ = x.shape
                return None, [probs[:batch_size].clone()]

        heads, _ = analyze_induction_heads(_UniformStub([[0.0]]), _loader())
        assert heads == [[]], f"uniform attention must not be detected, got {heads}"


class TestDiag1MassScale:
    """compute_attention_entropy's diag1_mass is the metric whose 2026-08-01
    scale bug made the training curve claim heads were forming while the
    per-head detector found none. It must report the max over heads, on the
    same [0, 1] scale as the threshold it is plotted against."""

    def test_reports_max_over_heads_not_sum(self) -> None:
        entropy = compute_attention_entropy(_StubPatternModel([[0.5, 0.5]]), _loader())
        mass = entropy["diag1_mass"][0]
        assert abs(mass - 0.5) < 0.02, f"two 0.5 heads must report 0.5, got {mass}"

    def test_tracks_planted_mass(self) -> None:
        for planted in (0.6, 0.1):
            entropy = compute_attention_entropy(_StubPatternModel([[planted]]), _loader())
            mass = entropy["diag1_mass"][0]
            assert abs(mass - planted) < 0.02, f"expected {planted}, got {mass}"

    def test_stays_in_unit_range_across_layers(self) -> None:
        entropy = compute_attention_entropy(
            _StubPatternModel([[0.5, 0.4], [0.3, 0.2]]), _loader()
        )
        assert len(entropy["diag1_mass"]) == 2
        for mass in entropy["diag1_mass"]:
            assert 0.0 <= mass <= 1.0, f"diag1_mass out of [0,1]: {mass}"


class TestPlantedModelWeights:
    """The same detector on a real model with weights planted so the
    induction pattern exists by construction. This is the level that catches
    hook and plumbing regressions: a broken record path returns no patterns
    (or the wrong tensor) and a known-present head goes undetected — exactly
    how the 2026-08-01 ablation bug hid in plain sight."""

    def test_planted_shift_head_is_detected(self) -> None:
        model = _fresh_model()
        _plant_shift_head(model)
        heads, _ = analyze_induction_heads(model, _loader())
        assert heads == [[0]], f"planted shift head must be detected, got {heads}"

    def test_planted_head_mass_matches_entropy_metric(self) -> None:
        """The two diag+1 measurements must agree on the same model.

        The 2026-07-26 discrepancy ("mass ~1.0 but 0 heads detected") was
        these two being on different scales. On a planted head they must
        both say "detected"; on the controls both must say "not".
        """
        for plant, expected_detected in (
            (_plant_shift_head, True),
            (_plant_self_head, False),
            (_plant_uniform_head, False),
        ):
            model = _fresh_model()
            plant(model)
            heads, _ = analyze_induction_heads(model, _loader())
            entropy = compute_attention_entropy(model, _loader())
            detected = bool(heads[0])
            mass_agrees = (entropy["diag1_mass"][0] > THRESHOLD) == detected
            assert detected == expected_detected, (
                f"{plant.__name__}: detection {detected}, expected {expected_detected}"
            )
            assert mass_agrees, (
                f"{plant.__name__}: detector says {detected} but diag1_mass is "
                f"{entropy['diag1_mass'][0]:.3f} (threshold {THRESHOLD})"
            )

    def test_self_attention_control_not_detected(self) -> None:
        model = _fresh_model()
        _plant_self_head(model)
        heads, _ = analyze_induction_heads(model, _loader())
        entropy = compute_attention_entropy(model, _loader())
        assert heads == [[]], f"self-attention is the wrong offset, got {heads}"
        assert entropy["diag1_mass"][0] < THRESHOLD

    def test_uniform_control_not_detected(self) -> None:
        model = _fresh_model()
        _plant_uniform_head(model)
        heads, _ = analyze_induction_heads(model, _loader())
        assert heads == [[]], f"uniform attention must not be detected, got {heads}"
