"""Tests for the shared induction-detection module (Rungs 1, 4 and 5).

Two things are tested here that no other test covers:

1. **The dissociation probe** — on the `prefix + prefix` task the previous
   occurrence of the current token is *always* at `q-L`, so a head that
   copies by content and a head that copies by a fixed offset are the same
   function on the training distribution. No in-distribution measurement can
   tell them apart. The probe builds a batch whose second half is a
   *permuted* copy of the prefix, so the two hypotheses point at different
   keys, and reports which one the model follows.

2. **The two-stage confirmation rule** — a head is confirmed only when the
   mass screen *and* the mechanism (K-composition with an earlier layer)
   agree; the first layer has no earlier layer and is confirmed on the mass
   alone.
"""

from __future__ import annotations

import numpy as np
import torch
from torch import nn

from src.experiments.induction_detection import (
    COMPOSITION_THRESHOLD,
    INDUCTION_MASS_THRESHOLD,
    detect_heads,
    layer_entropy,
    make_dissociation_batch,
    nearest_previous_occurrence,
    prefix_length_for,
    run_dissociation_probe,
)

VOCAB, SEQ_LEN = 256, 16
PREFIX_LEN = SEQ_LEN // 2
INPUT_LEN = SEQ_LEN - 1


def _periodic_tokens(num_samples: int = 8, seed: int = 0) -> torch.Tensor:
    """`prefix + prefix` **input** tokens (the generator's `tokens[:-1]`).

    Collision-free by construction, so every second-copy query has its
    nearest previous occurrence exactly `L` positions back.
    """
    rng = np.random.default_rng(seed)
    out = []
    for _ in range(num_samples):
        prefix = rng.choice(VOCAB, size=PREFIX_LEN, replace=False)
        tokens = np.concatenate([prefix, prefix])
        out.append(tokens[:-1])
    return torch.from_numpy(np.stack(out))


def _planted_patterns(batch_size: int, offset: int, mass: float = 0.8) -> torch.Tensor:
    """(B, 1, S, S) attention with `mass` on the key `q - offset`."""
    probs = torch.zeros(batch_size, 1, INPUT_LEN, INPUT_LEN)
    for b in range(batch_size):
        for q in range(INPUT_LEN):
            n_keys = q + 1
            row = torch.full((n_keys,), (1.0 - mass) / max(n_keys - 1, 1))
            if q >= PREFIX_LEN:
                key = q - offset
                if 0 <= key <= q:
                    row[key] = mass
            probs[b, 0, q, :n_keys] = row
    return probs


class _OffsetStub(nn.Module):
    """A model whose single head attends to `q - offset`."""

    def __init__(self, offset: int) -> None:
        super().__init__()
        self._offset = offset
        self.blocks = [None]

    def forward(self, x: torch.Tensor, record_attn: bool = False):
        batch_size, seq_len = x.shape
        if record_attn:
            return None, [_planted_patterns(batch_size, self._offset)]
        return torch.zeros(batch_size, seq_len, VOCAB), None


class _ContentStub(nn.Module):
    """A model that copies by *content* and predicts the content answer.

    The attention mass sits on the content key of every second-copy query,
    and the logits are built so that the token at the content key is the
    argmax at the last position — the behavioural signature of a
    content-based copy circuit.
    """

    def __init__(self, batch: dict[str, torch.Tensor]) -> None:
        super().__init__()
        self._batch = batch
        self.blocks = [None]

    def _patterns(self, batch_size: int) -> torch.Tensor:
        content_key = self._batch["content_key"]
        probs = torch.zeros(batch_size, 1, INPUT_LEN, INPUT_LEN)
        for b in range(batch_size):
            for q in range(INPUT_LEN):
                key = int(content_key[b, q])
                n_keys = q + 1
                row = torch.full((n_keys,), 0.2 / max(n_keys - 1, 1))
                if key >= 0:
                    row[key] = 0.8
                probs[b, 0, q, :n_keys] = row
        return probs

    def forward(self, x: torch.Tensor, record_attn: bool = False):
        batch_size, seq_len = x.shape
        logits = torch.zeros(batch_size, seq_len, VOCAB)
        content_key = self._batch["content_key"]
        content_answer = self._batch["content_answer"]
        for b in range(batch_size):
            for q in range(seq_len):
                key = int(content_key[b, q])
                if key < 0:
                    continue
                logits[b, q, int(self._batch["x"][b, key])] = 1.0
            last = int(content_answer[b, -1])
            if last >= 0:
                logits[b, -1, last] = 2.0
        if record_attn:
            return logits, [self._patterns(batch_size)]
        return logits, None


class TestNearestPreviousOccurrence:
    def test_finds_the_nearest_earlier_occurrence(self) -> None:
        tokens = torch.tensor([[5, 7, 5, 9, 7]])
        prev = nearest_previous_occurrence(tokens)
        assert prev.tolist() == [[-1, -1, 0, -1, 1]]

    def test_no_occurrence_is_minus_one(self) -> None:
        tokens = torch.tensor([[1, 2, 3]])
        assert nearest_previous_occurrence(tokens).tolist() == [[-1, -1, -1]]


class TestPrefixLength:
    def test_matches_the_generator_layout(self) -> None:
        assert prefix_length_for(64) == 32
        assert prefix_length_for(16) == 8
        assert prefix_length_for(3) == 2  # the generator's floor


class TestDissociationBatch:
    def test_content_and_period_keys_never_coincide(self) -> None:
        batch = make_dissociation_batch(
            vocab_size=VOCAB, seq_len=SEQ_LEN, num_samples=16, seed=0
        )
        content = batch["content_key"]
        period = batch["period_key"]
        defined = content >= 0
        assert bool(defined.any())
        # Every second-copy query is a conflict.
        assert not bool((content[defined] == period[defined]).any())

    def test_content_key_is_the_previous_occurrence_plus_one(self) -> None:
        batch = make_dissociation_batch(
            vocab_size=VOCAB, seq_len=SEQ_LEN, num_samples=8, seed=1
        )
        x, content_key = batch["x"], batch["content_key"]
        prev = nearest_previous_occurrence(x)
        for b in range(x.shape[0]):
            for q in range(x.shape[1]):
                if int(content_key[b, q]) < 0:
                    continue
                p = int(prev[b, q])
                assert p >= 0
                assert int(content_key[b, q]) == p + 1

    def test_rejects_an_odd_sequence_length(self) -> None:
        try:
            make_dissociation_batch(vocab_size=VOCAB, seq_len=15, num_samples=2, seed=0)
        except ValueError as exc:
            assert "even seq_len" in str(exc)
        else:  # pragma: no cover - the guard must fire
            raise AssertionError("an odd seq_len must be rejected")

    def test_rejects_a_vocabulary_smaller_than_the_prefix(self) -> None:
        try:
            make_dissociation_batch(vocab_size=4, seq_len=16, num_samples=2, seed=0)
        except ValueError as exc:
            assert "vocab_size" in str(exc)
        else:  # pragma: no cover - the guard must fire
            raise AssertionError("a too-small vocabulary must be rejected")


class TestDissociationProbe:
    def test_periodic_head_is_reported_as_positional(self) -> None:
        """A head that follows the fixed offset is *not* an induction head."""
        probe = run_dissociation_probe(
            _OffsetStub(offset=PREFIX_LEN - 1),
            vocab_size=VOCAB,
            seq_len=SEQ_LEN,
            num_samples=8,
            seed=0,
        )
        assert probe["peak_period_mass"] > 0.5
        assert probe["peak_content_mass"] < probe["peak_period_mass"]
        assert probe["content_wins"] is False

    def test_previous_token_head_is_not_a_copy_head(self) -> None:
        """A previous-token head copies neither target."""
        probe = run_dissociation_probe(
            _OffsetStub(offset=1),
            vocab_size=VOCAB,
            seq_len=SEQ_LEN,
            num_samples=8,
            seed=0,
        )
        assert probe["peak_period_mass"] < 0.5
        assert probe["peak_content_mass"] < 0.5

    def test_content_head_is_reported_as_content_based(self) -> None:
        """A head that follows the previous occurrence wins the probe."""
        batch = make_dissociation_batch(
            vocab_size=VOCAB, seq_len=SEQ_LEN, num_samples=8, seed=3
        )
        probe = run_dissociation_probe(
            _ContentStub(batch),
            batch=batch,
            vocab_size=VOCAB,
            seq_len=SEQ_LEN,
            num_samples=8,
            seed=3,
        )
        assert probe["peak_content_mass"] > 0.5
        assert probe["peak_content_mass"] > probe["peak_period_mass"]
        assert probe["content_wins"] is True
        # The behavioural readout agrees: the content answer is preferred.
        assert probe["logit_diff_content_minus_period"] > 0


class TestConfirmationRule:
    def _report(self, patterns, tokens):
        return detect_heads(patterns, tokens, PREFIX_LEN)

    def test_layer_zero_is_confirmed_on_the_mass_alone(self) -> None:
        tokens = _periodic_tokens()
        patterns = [_planted_patterns(tokens.shape[0], PREFIX_LEN - 1)]
        report = self._report(patterns, tokens)
        assert report.confirmed == [[0]]
        assert report.composition_by_layer[0] == 0.0

    def test_a_layer_one_head_needs_the_composition(self) -> None:
        """Mass alone is not enough one layer up.

        The second layer's head copies at the right offset, but the layer
        below it is uniform — there is no duplicate-token head to compose
        with, so the head is *not* confirmed. This is the rule that stops
        the "high K-composition score with no head" confusion in the other
        direction.
        """
        tokens = _periodic_tokens()
        uniform = torch.zeros(tokens.shape[0], 1, INPUT_LEN, INPUT_LEN)
        for b in range(tokens.shape[0]):
            for q in range(INPUT_LEN):
                uniform[b, 0, q, : q + 1] = 1.0 / (q + 1)
        patterns = [uniform, _planted_patterns(tokens.shape[0], PREFIX_LEN - 1)]
        report = self._report(patterns, tokens)
        assert report.screen == [[], [0]]
        assert report.confirmed == [[], []]

    def test_a_two_step_circuit_is_confirmed(self) -> None:
        """A duplicate head in L0 + a copy head in L1 is the real thing.

        Note which heads are *confirmed*: the L1 copy head is (mass on the
        copy offset **and** composed with L0), while the L0 head is not —
        it is the duplicate-token head, Step 1 of the mechanism, not an
        induction head. `total_induction_heads` counts copy heads.
        """
        tokens = _periodic_tokens()
        patterns = [
            _planted_patterns(tokens.shape[0], PREFIX_LEN),
            _planted_patterns(tokens.shape[0], PREFIX_LEN - 1),
        ]
        report = self._report(patterns, tokens)
        assert report.confirmed == [[], [0]]
        assert report.best_composition > COMPOSITION_THRESHOLD

    def test_thresholds_are_the_documented_ones(self) -> None:
        assert INDUCTION_MASS_THRESHOLD == 0.3
        assert COMPOSITION_THRESHOLD == 0.4


class TestLayerEntropy:
    def test_uniform_attention_has_high_entropy(self) -> None:
        probs = torch.zeros(1, 1, 8, 8)
        for q in range(8):
            probs[0, 0, q, : q + 1] = 1.0 / (q + 1)
        entropy = layer_entropy([probs])
        assert entropy[0] > 1.0

    def test_peaked_attention_has_low_entropy(self) -> None:
        probs = torch.zeros(1, 1, 8, 8)
        for q in range(8):
            probs[0, 0, q, q] = 1.0
        entropy = layer_entropy([probs])
        assert entropy[0] < 1e-3
