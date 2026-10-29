"""Tests for the circuit-level measurement of the copy mechanism.

Why these tests are planted
---------------------------
The measurement this module adds answers "is the copy carried by one head
or by a group of them?" — and that question can only be answered honestly
against models whose mechanism is *known*. So the tests here plant the
mechanism: a model whose head copies the content key, and a model whose
head copies a fixed offset, both built so that the expected attribution is
known analytically.

The planted model
-----------------
One head, ``d_model == vocab_size`` so that the head's value vector can be
the one-hot of the token it reads:

* the attention pattern is planted — the head attends to the content key
  (or to a fixed offset) with mass ``m`` and spreads the rest uniformly;
* the value vectors are the one-hot of the token at the key, so the head's
  OV output *is* the token it copied;
* the unembedding is ``4 * I``, so the logit of a token is four times the
  residual component of that token.

With that construction the head's attribution to the content-vs-position
contrast is ``4 * m`` for a content head and ``-4 * m`` for an offset head:
the sign is the whole point of the measurement, and the test asserts it.
"""

from __future__ import annotations

import numpy as np
import pytest
import torch
from torch import nn

from src.experiments.copy_circuit import (
    CHANCE_FACTOR,
    MECHANISM_DISTRIBUTED,
    MECHANISM_NONE,
    MECHANISM_SINGLE,
    MECHANISM_UNDETERMINED,
    candidate_heads,
    chance_content_mass,
    classify_mechanism,
    content_triples,
    content_vs_position_attribution,
    mass_covering_heads,
    mass_summary,
)
from src.experiments.induction_detection import DetectionReport
from src.experiments.induction_tasks import TASK_VARIABLE, TaskSpec, copy_queries

SPEC = TaskSpec.variable(
    vocab_size=32, seq_len=24, key_len=12, copy_blocks=2, copy_block_len=3
)


def _tokens(n: int = 16, seed: int = 0) -> torch.Tensor:
    from src.experiments.induction_tasks import make_variable_tokens

    return torch.from_numpy(make_variable_tokens(SPEC, n, seed))


# ---------------------------------------------------------------------------
# The planted model
# ---------------------------------------------------------------------------
class _PlantedBlock(nn.Module):
    def __init__(self, d_model: int, n_heads: int) -> None:
        super().__init__()
        self.d_head = d_model // n_heads
        self.n_heads = n_heads
        self.W_O = nn.Linear(d_model, d_model, bias=False)
        with torch.no_grad():
            self.W_O.weight.copy_(torch.eye(d_model))
        self.head_mask: torch.Tensor | None = None

    def forward(
        self,
        x: torch.Tensor,
        probs: torch.Tensor,
        values: torch.Tensor,
        cache: dict | None = None,
        cache_prefix: str = "",
    ) -> torch.Tensor:
        bsz, seq, d_model = x.shape
        out = (probs @ values).transpose(1, 2).contiguous().view(bsz, seq, d_model)
        attn_out = self.W_O(out)
        if cache is not None:
            cache[f"{cache_prefix}.attn.attn_probs"] = probs.detach().cpu()
            cache[f"{cache_prefix}.attn.V"] = values.detach().cpu()
            cache[f"{cache_prefix}.resid_post"] = (x + attn_out).detach().cpu()
        return x + attn_out


class _PlantedCopyModel(nn.Module):
    """A one-head model whose head copies the content key, or a fixed offset."""

    def __init__(self, mass: float = 0.8, mode: str = "content", offset: int = 3) -> None:
        super().__init__()
        self.vocab = SPEC.vocab_size
        self.mass = mass
        self.mode = mode
        self.offset = offset
        self.unembed = nn.Linear(self.vocab, self.vocab, bias=False)
        with torch.no_grad():
            self.unembed.weight.copy_(torch.eye(self.vocab) * 4.0)
        self.blocks = nn.ModuleList([_PlantedBlock(self.vocab, 1)])

    def forward(
        self,
        x: torch.Tensor,
        record_attn: bool = False,
        cache: dict | None = None,
    ) -> tuple[torch.Tensor, None]:
        bsz, seq = x.shape
        geom = copy_queries(x.numpy())
        probs = torch.zeros(bsz, 1, seq, seq)
        values = torch.zeros(bsz, 1, seq, self.vocab)
        values.scatter_(3, x.unsqueeze(1).unsqueeze(-1).expand(bsz, 1, seq, 1), 1.0)
        for b in range(bsz):
            for q in range(seq):
                n_keys = q + 1
                row = torch.full((n_keys,), (1.0 - self.mass) / max(n_keys - 1, 1))
                key: int | None = None
                if self.mode == "content":
                    if geom["mask"][b, q]:
                        key = int(geom["content_key"][b, q])
                else:
                    key = q - self.offset + 1
                if key is not None and 0 <= key <= q:
                    row[key] = self.mass
                probs[b, 0, q, :n_keys] = row
        h = torch.zeros(bsz, seq, self.vocab)
        h.scatter_(2, x.unsqueeze(-1), 1.0)
        for i, block in enumerate(self.blocks):
            h = block(h, probs, values, cache=cache, cache_prefix=f"blocks.{i}")
        return self.unembed(h), None


# ---------------------------------------------------------------------------
# The chance level and the candidate group
# ---------------------------------------------------------------------------
class TestChanceLevel:
    def test_the_chance_level_is_the_uniform_mass(self) -> None:
        # at query q a uniform head puts 1/(q+1) on any one allowed key
        triples = np.array([[0, 5, 0], [1, 9, 0]], dtype=np.int64)
        assert chance_content_mass(triples) == pytest.approx(
            (1.0 / 6.0 + 1.0 / 10.0) / 2.0
        )

    def test_the_chance_level_falls_with_the_query_position(self) -> None:
        triples = np.array([[0, 5, 3]], dtype=np.int64)
        assert chance_content_mass(triples) == pytest.approx(1.0 / 6.0)

    def test_no_queries_means_no_chance(self) -> None:
        assert chance_content_mass(np.zeros((0, 3), dtype=np.int64)) == 0.0

    def test_the_chance_level_of_the_real_task_is_small(self) -> None:
        triples = content_triples(_tokens())
        assert triples.shape[0] > 0
        assert 0.0 < chance_content_mass(triples) < 0.2


class TestCandidateGroup:
    def _report(self, content: list[list[float]]) -> DetectionReport:
        masses = {"content": [np.asarray(layer, dtype=float) for layer in content]}
        return DetectionReport(masses=masses)

    def test_only_the_heads_above_the_bar_are_candidates(self) -> None:
        # chance = 1/(29+1) ≈ 0.0333, bar = 3 * 0.0333 ≈ 0.1
        triples = np.array([[0, 29, 19], [1, 29, 19]], dtype=np.int64)
        report = self._report([[0.5, 0.01, 0.1]])
        chosen = candidate_heads(report, triples, factor=CHANCE_FACTOR)
        assert chosen == [(0, 0), (0, 2)]

    def test_a_head_between_old_and_new_bar_is_a_candidate_after_the_fix(self) -> None:
        # old chance 1/(19+1)=0.05 → bar 0.15 would exclude 0.12;
        # new chance 1/(29+1)≈0.0333 → bar ≈0.1 includes it.
        triples = np.array([[0, 29, 19]], dtype=np.int64)
        report = self._report([[0.12]])
        chosen = candidate_heads(report, triples, factor=CHANCE_FACTOR)
        assert chosen == [(0, 0)]

    def test_a_uniform_head_is_not_a_candidate(self) -> None:
        triples = np.array([[0, 9, 3]], dtype=np.int64)
        report = self._report([[0.2]])  # 0.2 < 3 * 0.1 = 0.3
        assert candidate_heads(report, triples, factor=CHANCE_FACTOR) == []

    def test_no_queries_means_no_candidates(self) -> None:
        report = self._report([[0.9]])
        assert candidate_heads(report, np.zeros((0, 3), dtype=np.int64)) == []


class TestMassSummary:
    def test_the_total_is_the_sum_over_the_heads(self) -> None:
        report = DetectionReport(
            masses={"content": [np.array([0.4, 0.1]), np.array([0.05])]},
        )
        summary = mass_summary(report, np.array([[0, 5, 3]], dtype=np.int64))
        assert summary["content_mass_total"] == pytest.approx(0.55)
        assert summary["content_mass_top_share"] == pytest.approx(0.4 / 0.55)
        # 0.4 of 0.55 is below 80%, so the circuit is two heads wide
        assert summary["content_mass_heads_for_80pct"] == 2

    def test_the_width_of_the_circuit_is_counted(self) -> None:
        report = DetectionReport(
            masses={"content": [np.array([0.4, 0.1, 0.1, 0.1])]},
        )
        summary = mass_summary(report, np.array([[0, 5, 3]], dtype=np.int64))
        # 0.4 + 0.1 + 0.1 = 0.6 of 0.7 is above 80%
        assert summary["content_mass_heads_for_80pct"] == 3

    def test_the_offset_total_is_the_best_fixed_offset(self) -> None:
        offsets = [np.array([[0.1, 0.2], [0.3, 0.05]])]  # (heads, offsets)
        report = DetectionReport(
            masses={"content": [np.array([0.4])]}, offsets=offsets
        )
        summary = mass_summary(report, np.array([[0, 5, 3]], dtype=np.int64))
        # offset 1: 0.1 + 0.3 = 0.4; offset 2: 0.2 + 0.05 = 0.25
        assert summary["offset_best_offset"] == 1.0
        assert summary["offset_mass_total"] == pytest.approx(0.4)

    def test_content_mass_excess_and_ratio(self) -> None:
        report = DetectionReport(
            masses={"content": [np.array([0.4, 0.1])]},
        )
        triples = np.array([[0, 5, 3]], dtype=np.int64)
        summary = mass_summary(report, triples)
        assert summary["content_mass_total"] == pytest.approx(0.5)
        assert summary["content_chance_mass"] == pytest.approx(1.0 / 6.0)
        assert summary["content_mass_excess"] == pytest.approx(0.5 - 2.0 / 6.0)
        assert summary["content_mass_ratio"] == pytest.approx(0.5 / (2.0 / 6.0))

    def test_all_zero_mass_covers_no_heads(self) -> None:
        # With no content mass there is no head to name: the width is 0, not
        # the vacuous 1 the loop used to report.
        report = DetectionReport(masses={"content": [np.array([0.0, 0.0])]})
        triples = np.array([[0, 5, 3]], dtype=np.int64)
        summary = mass_summary(report, triples)
        assert summary["content_mass_heads_for_80pct"] == 0.0


class TestMassCoveringHeads:
    def _report(self, content: list[list[float]]) -> DetectionReport:
        masses = {"content": [np.asarray(layer, dtype=float) for layer in content]}
        return DetectionReport(masses=masses)

    def test_covers_80_percent_of_the_mass(self) -> None:
        report = self._report([[0.4, 0.1, 0.1, 0.1]])
        triples = np.array([[0, 5, 3]], dtype=np.int64)
        chosen = mass_covering_heads(report, triples, coverage=0.8)
        assert chosen == [(0, 0), (0, 1), (0, 2)]

    def test_one_head_covers_everything(self) -> None:
        report = self._report([[0.9, 0.05, 0.05]])
        triples = np.array([[0, 5, 3]], dtype=np.int64)
        chosen = mass_covering_heads(report, triples, coverage=0.8)
        assert chosen == [(0, 0)]

    def test_empty_report_returns_empty(self) -> None:
        report = DetectionReport(masses={"content": [np.array([])]})
        triples = np.array([[0, 5, 3]], dtype=np.int64)
        assert mass_covering_heads(report, triples) == []


# ---------------------------------------------------------------------------
# The attribution
# ---------------------------------------------------------------------------
class TestAttribution:
    def test_a_content_head_votes_for_the_content_answer(self) -> None:
        tokens = _tokens()
        model = _PlantedCopyModel(mass=0.8, mode="content")
        triples = content_triples(tokens)
        report = content_vs_position_attribution(model, tokens, triples, best_offset=3)
        assert report["dla_total"] > 0.0
        assert report["dla_observed_logit_diff"] > 0.0
        assert report["dla_n_queries"] > 0

    def test_an_offset_head_votes_for_the_positional_answer(self) -> None:
        """The measurement must separate the two mechanisms, not flatter both."""
        tokens = _tokens()
        model = _PlantedCopyModel(mass=0.8, mode="offset", offset=3)
        triples = content_triples(tokens)
        report = content_vs_position_attribution(model, tokens, triples, best_offset=3)
        assert report["dla_total"] < 0.0
        assert report["dla_observed_logit_diff"] < 0.0

    def test_the_planted_head_carries_the_attribution(self) -> None:
        tokens = _tokens()
        model = _PlantedCopyModel(mass=0.8, mode="content")
        triples = content_triples(tokens)
        report = content_vs_position_attribution(model, tokens, triples, best_offset=3)
        assert report["dla_by_head"]["L0H0"] > 0.0
        assert report["dla_top_head"] == "L0H0"

    def test_a_model_without_an_unembedding_is_refused(self) -> None:
        class _NoUnembed(nn.Module):
            def __init__(self) -> None:
                super().__init__()
                self.blocks = nn.ModuleList()

        with pytest.raises(ValueError):
            content_vs_position_attribution(
                _NoUnembed(), _tokens(), np.zeros((0, 3), dtype=np.int64), 3
            )


# ---------------------------------------------------------------------------
# The classification
# ---------------------------------------------------------------------------
class TestClassifyMechanism:
    def test_a_group_that_matters_and_no_single_head_is_distributed(self) -> None:
        code, label = classify_mechanism(
            {
                "group_ablation_drop": 0.5,
                "max_single_ablation_drop": 0.02,
                "dla_content_minus_offset": 1.0,
            }
        )
        assert code == MECHANISM_DISTRIBUTED
        assert "distributed" in label

    def test_a_head_that_matters_alone_is_a_single_head(self) -> None:
        code, _label = classify_mechanism(
            {
                "group_ablation_drop": 0.5,
                "max_single_ablation_drop": 0.4,
                "dla_content_minus_offset": 1.0,
            }
        )
        assert code == MECHANISM_SINGLE

    def test_a_circuit_that_is_not_there_is_none(self) -> None:
        code, _label = classify_mechanism(
            {
                "group_ablation_drop": 0.0,
                "max_single_ablation_drop": 0.0,
                "dla_content_minus_offset": -1.0,
            }
        )
        assert code == MECHANISM_NONE

    def test_no_candidate_group_is_undetermined_not_none(self) -> None:
        # The 3x chance screen selected no head: the group ablation is a
        # no-op, so 0.0 is not "no circuit" — it is "undetermined".
        code, label = classify_mechanism(
            {
                "group_ablation_drop": 0.0,
                "max_single_ablation_drop": 0.0,
                "dla_content_minus_offset": 5.0,
                "n_candidate_heads": 0.0,
            }
        )
        assert code == MECHANISM_UNDETERMINED
        assert "no candidate" in label

    def test_without_n_candidates_old_behavior_preserved(self) -> None:
        code, _ = classify_mechanism(
            {
                "group_ablation_drop": 0.0,
                "max_single_ablation_drop": 0.0,
                "dla_content_minus_offset": -1.0,
            }
        )
        assert code == MECHANISM_NONE

    def test_anything_else_is_undetermined(self) -> None:
        code, _label = classify_mechanism(
            {
                "group_ablation_drop": 0.3,
                "max_single_ablation_drop": 0.15,
                "dla_content_minus_offset": 0.0,
            }
        )
        assert code == MECHANISM_UNDETERMINED

    def test_the_task_of_the_measurement_is_the_variable_one(self) -> None:
        """The copy queries only exist where the repeats are at varying distances."""
        assert TASK_VARIABLE != "periodic"
