"""Planted-construction tests for the induction-head detector (Rung 1 / Rung 4).

Why this file exists
--------------------
Every "0 heads detected" result in this repository was a statement about
*the detector*, not about the model — and the detector was wrong.

The old detector measured the attention mass on the **previous-token**
offset (`q -> q-1`) and called it "diag+1". On this task the induction
(copy) offset is `q -> q-L+1`: at a second-copy query `q`, the token
`x[q]` has its previous occurrence at `q-L`, and the token to copy sits at
`q-L+1`. A head that attends to `q-1` is a *previous-token* head — a
different circuit that does not copy the repeated token at all.

The old tests did not catch it, because they planted the same wrong
pattern: `_planted_patterns` put the mass on `q-1` and asserted it was
detected. A test that encodes the bug passes the bug.

So the tests below are rebuilt around the *task layout*:

* the **positive** construction plants the copy offset `q-L+1` and must be
  detected;
* the **negative** controls plant the offsets that must NOT be detected —
  `q-1` (the old "positive", a previous-token head), `q-L` (the
  duplicate-token head, Step 1 only), `q-L+2` (wrong by one) — plus
  self-attention and uniform attention;
* the same construction is repeated at the **weights level**, on a real
  `AttentionOnlyTransformer`, so a broken collection path cannot hide a
  head that is really there.

The patterns are planted on the *same* tokens the detector reads, because
the offset conventions are relative to the data layout: the detector must
know where the previous occurrence of the current token is, and it gets
that from the tokens themselves.
"""

from __future__ import annotations

import torch
from torch import nn
from torch.utils.data import DataLoader

from src.experiments.exp1_induction_heads import (
    AttentionOnlyTransformer,
    analyze_induction_heads,
    compute_attention_entropy,
    make_repeated_token_data,
)

THRESHOLD = 0.3  # the per-head detection threshold analyze_induction_heads uses
VOCAB, SEQ_LEN = 256, 16
PREFIX_LEN = SEQ_LEN // 2  # the generator's layout: prefix + prefix
INPUT_LEN = SEQ_LEN - 1  # the loader yields tokens[:-1]
N_SAMPLES = 32


def _loader() -> DataLoader:
    """A loader over the real task data.

    The detector reads the *tokens* to know where the previous occurrence
    of the current token is, so the planted patterns have to be planted on
    the same layout the detector measures. The vocabulary is large enough
    for the prefix to be collision-free, so every second-copy query is a
    "periodic" one (nearest previous occurrence exactly `q-L`).
    """
    train, _ = make_repeated_token_data(
        vocab_size=VOCAB, seq_len=SEQ_LEN, num_train=N_SAMPLES, num_val=8, seed=0
    )
    return DataLoader(train, batch_size=1)


def _planted_patterns(
    masses: list[list[float]], batch_size: int, seq_len: int, offset: int
) -> list[torch.Tensor]:
    """One (batch, heads, S, S) tensor per layer with planted mass at
    `q -> q-offset`.

    Per head, every query `q >= PREFIX_LEN` puts exactly `m` of its
    probability on key `q-offset` and spreads the rest over the remaining
    causal keys. Query 0 has no offset to attend to and is uniform.
    """
    layers = []
    for layer_masses in masses:
        n_heads = len(layer_masses)
        probs = torch.zeros(batch_size, n_heads, seq_len, seq_len)
        for h, m in enumerate(layer_masses):
            for q in range(seq_len):
                n_keys = q + 1  # causal: keys 0..q
                row = torch.full((n_keys,), (1.0 - m) / max(n_keys - 1, 1))
                if q >= PREFIX_LEN:
                    key = q - offset
                    if 0 <= key <= q:
                        row[key] = m
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

    def __init__(self, masses: list[list[float]], offset: int) -> None:
        super().__init__()
        self._masses = masses
        self._offset = offset
        self.blocks = [None] * len(masses)  # len(model.blocks) is the layer count

    def forward(self, x: torch.Tensor, record_attn: bool = False):
        if not record_attn:
            return None, None
        batch_size, seq_len = x.shape
        return None, _planted_patterns(self._masses, batch_size, seq_len, self._offset)


class TestPlantedCopyOffsetDetector:
    """The 0.3-threshold detector on the *correct* copy offset."""

    def test_detects_planted_copy_head(self) -> None:
        heads, _ = analyze_induction_heads(
            _StubPatternModel([[0.6]], offset=PREFIX_LEN - 1), _loader()
        )
        assert heads == [[0]], f"planted copy head must be detected, got {heads}"

    def test_rejects_weak_head_below_threshold(self) -> None:
        heads, _ = analyze_induction_heads(
            _StubPatternModel([[0.1]], offset=PREFIX_LEN - 1), _loader()
        )
        assert heads == [[]], f"planted 0.1 head must not be detected, got {heads}"

    def test_rejects_two_weak_heads_not_summed(self) -> None:
        """Two 0.2 heads must not trip a 0.3 threshold.

        This is the 2026-08-01 scale bug applied to the threshold path: a
        summed-across-heads mass of 0.4 would falsely detect here.
        """
        heads, _ = analyze_induction_heads(
            _StubPatternModel([[0.2, 0.2]], offset=PREFIX_LEN - 1), _loader()
        )
        assert heads == [[]], f"0.2 + 0.2 is still below threshold, got {heads}"

    def test_per_head_independence(self) -> None:
        """A 0.6 head and a 0.0 head: exactly one detection, not an average.

        Cross-head averaging would put both at 0.3 — on the threshold, where
        `> 0.3` is false — and still lose the real head.
        """
        heads, _ = analyze_induction_heads(
            _StubPatternModel([[0.6, 0.0]], offset=PREFIX_LEN - 1), _loader()
        )
        assert heads == [[0]], f"only the planted head may be detected, got {heads}"


class TestWrongOffsetsRejected:
    """The offsets that must NOT be reported as induction heads.

    The first of these is the regression test for the bug that made every
    "0 / N heads" number in this repository uninterpretable: the old
    detector measured exactly this offset and called it induction.
    """

    def test_previous_token_head_is_not_an_induction_head(self) -> None:
        """`q -> q-1` is a previous-token head. The old detector fired on it."""
        heads, _ = analyze_induction_heads(
            _StubPatternModel([[0.9]], offset=1), _loader()
        )
        assert heads == [[]], f"previous-token head must not be detected, got {heads}"

    def test_duplicate_token_head_is_not_an_induction_head(self) -> None:
        """`q -> q-L` is Nanda's Step 1 (the duplicate head), not the copy."""
        heads, _ = analyze_induction_heads(
            _StubPatternModel([[0.9]], offset=PREFIX_LEN), _loader()
        )
        assert heads == [[]], f"duplicate-token head must not be detected, got {heads}"

    def test_off_by_one_past_the_copy_offset_is_rejected(self) -> None:
        """`q -> q-L+2` is not the copy offset either."""
        heads, _ = analyze_induction_heads(
            _StubPatternModel([[0.9]], offset=PREFIX_LEN - 2), _loader()
        )
        assert heads == [[]], f"wrong offset must not be detected, got {heads}"

    def test_uniform_not_detected(self) -> None:
        """Uniform causal attention (~1/(q+1) per key) must not trip the
        detector — it also pins what 'uniform' means numerically."""
        probs = torch.zeros(N_SAMPLES, 1, INPUT_LEN, INPUT_LEN)
        for q in range(INPUT_LEN):
            probs[:, 0, q, : q + 1] = 1.0 / (q + 1)

        class _UniformStub(_StubPatternModel):
            def forward(self, x: torch.Tensor, record_attn: bool = False):
                if not record_attn:
                    return None, None
                batch_size, _ = x.shape
                return None, [probs[:batch_size].clone()]

        heads, _ = analyze_induction_heads(_UniformStub([[0.0]], offset=1), _loader())
        assert heads == [[]], f"uniform attention must not be detected, got {heads}"


class TestMassMetricScale:
    """The four head-level masses, and the scale they are reported on.

    `compute_attention_entropy` reports the **max over heads** of each
    mass, so every number stays on the same [0, 1] scale as the 0.3
    detection threshold. (The 2026-08-01 bug summed across heads, which
    put the metric on a [0, n_heads] scale and made the training curve
    claim heads were forming while the detector found none.)
    """

    def test_reports_max_over_heads_not_sum(self) -> None:
        entropy = compute_attention_entropy(
            _StubPatternModel([[0.5, 0.5]], offset=PREFIX_LEN - 1), _loader()
        )
        mass = entropy["induction_mass"][0]
        assert abs(mass - 0.5) < 0.02, f"two 0.5 heads must report 0.5, got {mass}"

    def test_tracks_planted_mass(self) -> None:
        for planted in (0.6, 0.1):
            entropy = compute_attention_entropy(
                _StubPatternModel([[planted]], offset=PREFIX_LEN - 1), _loader()
            )
            mass = entropy["induction_mass"][0]
            assert abs(mass - planted) < 0.02, f"expected {planted}, got {mass}"

    def test_stays_in_unit_range_across_layers(self) -> None:
        entropy = compute_attention_entropy(
            _StubPatternModel([[0.5, 0.4], [0.3, 0.2]], offset=PREFIX_LEN - 1), _loader()
        )
        assert len(entropy["induction_mass"]) == 2
        for key in ("induction_mass", "prev_token_mass", "duplicate_mass"):
            for mass in entropy[key]:
                assert 0.0 <= mass <= 1.0, f"{key} out of [0,1]: {mass}"

    def test_previous_token_mass_reports_the_old_metric(self) -> None:
        """The previous-token mass is kept as a labelled control.

        It is the number the old detector called "diag+1", so a reader can
        check that the *old* curve and the *new* one are measuring different
        things — and that a model which only does previous-token attention
        shows up here and not in the induction mass.
        """
        entropy = compute_attention_entropy(
            _StubPatternModel([[0.9]], offset=1), _loader()
        )
        assert entropy["prev_token_mass"][0] > 0.8
        assert entropy["induction_mass"][0] < 0.2


class TestTheOldDetectorWasAntiCorrelatedWithTheTruth:
    """The regression test for the 2026-10-19 detector bug, stated as the
    contrast it was.

    The old detector measured the attention mass on the previous-token
    offset (`q-1`) and called it "diag+1". On a *previous-token* head it
    therefore reported a high score (a false positive: it called that head an
    induction head), and on a *real copy* head — the one that attends to
    `q-(L-1)` — it reported a low score (a false negative: it could not see
    the head it was looking for).

    This test pins both directions at once, because a detector that is merely
    "different" is not what was wrong: the old one was *inverted*.
    """

    @staticmethod
    def _planted(offset: int, mass: float = 0.9) -> torch.Tensor:
        """One head attending to `q - offset`, mass `mass`."""
        data, _ = make_repeated_token_data(
            vocab_size=VOCAB, seq_len=SEQ_LEN, num_train=N_SAMPLES, num_val=8, seed=0
        )
        x = torch.stack([data[i][0] for i in range(N_SAMPLES)])
        probs = torch.zeros(x.shape[0], 1, INPUT_LEN, INPUT_LEN)
        for b in range(x.shape[0]):
            for q in range(INPUT_LEN):
                n_keys = q + 1
                row = torch.full((n_keys,), (1.0 - mass) / max(n_keys - 1, 1))
                if q >= PREFIX_LEN:
                    key = q - offset
                    if 0 <= key <= q:
                        row[key] = mass
                probs[b, 0, q, :n_keys] = row
        return probs, x

    @staticmethod
    def _old_metric(probs: torch.Tensor) -> float:
        """What the old detector measured: the mass on the `q-1` offset."""
        return (
            probs[:, :, 1:, :-1]
            .diagonal(dim1=-2, dim2=-1)
            .mean(dim=(0, -1))
            .mean()
            .item()
        )

    def test_old_metric_fires_on_a_previous_token_head(self) -> None:
        probs, _ = self._planted(offset=1)
        assert self._old_metric(probs) > 0.3, (
            "the old detector's metric must be shown firing on the wrong head — "
            "that is the bug this test pins"
        )

    def test_old_metric_misses_a_real_copy_head(self) -> None:
        probs, _ = self._planted(offset=PREFIX_LEN - 1)
        assert self._old_metric(probs) < 0.3, (
            "the old detector's metric must be shown missing the real head"
        )

    def test_the_new_detector_inverts_both(self) -> None:
        from src.experiments.induction_detection import detect_heads

        prev_probs, prev_tokens = self._planted(offset=1)
        copy_probs, copy_tokens = self._planted(offset=PREFIX_LEN - 1)
        prev_report = detect_heads([prev_probs], prev_tokens, PREFIX_LEN)
        copy_report = detect_heads([copy_probs], copy_tokens, PREFIX_LEN)
        assert prev_report.screen == [[]], "the q-1 head must not be screened in"
        assert copy_report.screen == [[0]], "the copy head must be screened in"


class TestPlantedModelWeights:
    """The same detector on a real model with weights planted so the
    pattern exists by construction. This is the level that catches hook
    and plumbing regressions: a broken record path returns no patterns
    (or the wrong tensor) and a known-present head goes undetected —
    exactly how the 2026-08-01 ablation bug hid in plain sight."""

    @staticmethod
    def _plant_shift_head(model: AttentionOnlyTransformer, offset: int, scale: float = 8.0) -> None:
        """Plant a head that attends to `q - offset`.

        With token embeddings zeroed and pos_embed = I, the LayerNormed
        keys are a softmax-invariant affine image of the position one-hots,
        so the causal score between query i and key j is (up to constants)
        <W_Q e_i, W_K e_j>. W_Q maps e_i to e_{i-offset} and W_K = I makes
        every query attend to position i-offset with no dependence on token
        content — a head built from weights rather than trained.
        """
        d_model = model.embed.embedding_dim
        with torch.no_grad():
            model.embed.weight.zero_()
            model.pos_embed.weight.copy_(
                torch.eye(model.pos_embed.num_embeddings, d_model)
            )
            block = model.blocks[0]
            w_q = torch.zeros(d_model, d_model)
            for i in range(offset, model.pos_embed.num_embeddings):
                w_q[i - offset, i] = scale
            w_q[0, 0] = scale
            block.W_Q.weight.copy_(w_q)
            block.W_K.weight.copy_(torch.eye(d_model))

    @staticmethod
    def _plant_self_head(model: AttentionOnlyTransformer) -> None:
        """Negative control: every query attends to itself (the wrong offset)."""
        d_model = model.embed.embedding_dim
        with torch.no_grad():
            model.embed.weight.zero_()
            model.pos_embed.weight.copy_(
                torch.eye(model.pos_embed.num_embeddings, d_model)
            )
            block = model.blocks[0]
            block.W_Q.weight.copy_(torch.eye(d_model))
            block.W_K.weight.copy_(torch.eye(d_model))

    @staticmethod
    def _plant_uniform_head(model: AttentionOnlyTransformer) -> None:
        """Negative control: W_Q = 0 zeroes all scores -> uniform causal attention."""
        with torch.no_grad():
            model.blocks[0].W_Q.weight.zero_()

    @staticmethod
    def _fresh_model() -> AttentionOnlyTransformer:
        torch.manual_seed(0)
        # d_model >= the number of positions: the planting trick needs the
        # position embedding to be the identity over the position axis.
        return AttentionOnlyTransformer(
            vocab_size=VOCAB, d_model=16, n_layers=1, n_heads=1, max_seq_len=INPUT_LEN
        )

    def test_planted_copy_head_is_detected(self) -> None:
        model = self._fresh_model()
        self._plant_shift_head(model, offset=PREFIX_LEN - 1)
        heads, _ = analyze_induction_heads(model, _loader())
        assert heads == [[0]], f"planted copy head must be detected, got {heads}"

    def test_planted_previous_token_head_is_not_detected(self) -> None:
        """The regression test for the 2026-10-19 detector bug.

        The old detector reported this head as an induction head on every
        run it ever made.
        """
        model = self._fresh_model()
        self._plant_shift_head(model, offset=1)
        heads, _ = analyze_induction_heads(model, _loader())
        assert heads == [[]], f"previous-token head must not be detected, got {heads}"

    def test_head_mass_matches_entropy_metric(self) -> None:
        """The two mass measurements must agree on the same model.

        The 2026-07-26 discrepancy ("mass ~1.0 but 0 heads detected") was
        these two being on different scales. On a planted head they must
        both say "detected"; on the controls both must say "not".
        """
        for plant, expected_detected in (
            (lambda m: self._plant_shift_head(m, offset=PREFIX_LEN - 1), True),
            (lambda m: self._plant_shift_head(m, offset=1), False),
            (self._plant_self_head, False),
            (self._plant_uniform_head, False),
        ):
            model = self._fresh_model()
            plant(model)
            heads, _ = analyze_induction_heads(model, _loader())
            entropy = compute_attention_entropy(model, _loader())
            detected = bool(heads[0])
            mass_agrees = (entropy["induction_mass"][0] > THRESHOLD) == detected
            assert detected == expected_detected, (
                f"{plant}: detection {detected}, expected {expected_detected}"
            )
            assert mass_agrees, (
                f"detector says {detected} but induction_mass is "
                f"{entropy['induction_mass'][0]:.3f} (threshold {THRESHOLD})"
            )

    def test_self_attention_control_not_detected(self) -> None:
        model = self._fresh_model()
        self._plant_self_head(model)
        heads, _ = analyze_induction_heads(model, _loader())
        assert heads == [[]], f"self-attention is the wrong offset, got {heads}"
        assert compute_attention_entropy(model, _loader())["induction_mass"][0] < THRESHOLD

    def test_uniform_control_not_detected(self) -> None:
        model = self._fresh_model()
        self._plant_uniform_head(model)
        heads, _ = analyze_induction_heads(model, _loader())
        assert heads == [[]], f"uniform attention must not be detected, got {heads}"
