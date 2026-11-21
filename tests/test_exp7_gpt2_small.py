"""Rung 7's helpers and stages, on stubs and a tiny random GPT-2 (no download).

The real run is `python -m src.experiments.exp7_gpt2_small`; these tests pin the
measurement code so that a stage cannot pass or fail because the helper is wrong.
"""

from __future__ import annotations

import math
import re
from pathlib import Path

import numpy as np
import pytest
import torch

from src.experiments import exp7_gpt2_small as exp7
from src.models.gpt2 import GPT2, GPT2Config

ADR = Path(__file__).resolve().parents[1] / "docs/adr/0034-gpt2-small-real-model-test.md"


def _tiny() -> GPT2:
    torch.manual_seed(0)
    cfg = GPT2Config(vocab_size=97, n_positions=128, d_model=32, n_layers=2, n_heads=4)
    return GPT2(cfg).eval()


def test_induction_sequences_repeat_their_prefix_and_avoid_the_end_token() -> None:
    x = exp7.induction_sequences(0, n=5)
    assert x.shape == (5, 100)
    assert torch.equal(x[:, :50], x[:, 50:])
    assert int(x.max()) < exp7.MAX_TOKEN_ID
    assert not torch.equal(x, exp7.induction_sequences(1, n=5))
    assert torch.equal(x, exp7.induction_sequences(0, n=5))


def test_rank_and_top_heads_agree() -> None:
    m = np.array([[0.1, 0.9], [0.5, 0.2]])
    assert exp7.rank_of(m, 0, 1) == 1 and exp7.rank_of(m, 1, 1) == 3
    assert exp7.top_heads(m, 2) == [(0, 1, 0.9), (1, 0, 0.5)]


def test_scale_error_is_relative_to_the_tensor() -> None:
    big = torch.full((4,), 3000.0)
    assert exp7.scale_error(big + 0.01, big) < 1e-5  # tiny against thousands
    small = torch.full((4,), 0.5)
    assert exp7.scale_error(small + 0.01, small) > 1e-3  # not tiny against ~1


def test_relative_drop() -> None:
    assert exp7.relative_drop(4.0, 1.0) == 0.75
    assert math.isnan(exp7.relative_drop(0.0, 1.0))


class _CopyOracle(torch.nn.Module):
    """Predicts the next token perfectly in the second copy and uniformly in the first."""

    def __init__(self, vocab: int = 50) -> None:
        super().__init__()
        self.vocab = vocab
        self.anchor = torch.nn.Parameter(torch.zeros(1))

    def forward(self, x: torch.Tensor):
        logits = torch.zeros(*x.shape, self.vocab)
        for t in range(x.size(1) - 1):
            if t >= exp7.PREFIX_LEN:
                logits[torch.arange(x.size(0)), t, x[:, t + 1]] = 40.0
        return logits, None


def test_icl_gain_of_a_perfect_second_copy_is_log_vocab() -> None:
    tokens = exp7.induction_sequences(0, n=3, max_id=50)
    gain = exp7.icl_gain(_CopyOracle(), tokens)  # type: ignore[arg-type]
    assert gain == pytest.approx(math.log(50), abs=1e-3)


def test_induction_mass_matrix_has_one_entry_per_head_and_is_a_probability() -> None:
    model = _tiny()
    tokens = exp7.induction_sequences(0, n=4, max_id=97)
    matrix = exp7.induction_mass_matrix(model, tokens)
    assert matrix.shape == (2, 4)
    assert ((matrix >= 0) & (matrix <= 1)).all()


def test_ablating_heads_changes_the_gain_and_clearing_restores_it() -> None:
    model = _tiny()
    tokens = exp7.induction_sequences(0, n=4, max_id=97)
    base = exp7.icl_gain(model, tokens)
    model.set_head_mask([(0, 0), (0, 1), (1, 0)])
    assert exp7.icl_gain(model, tokens) != pytest.approx(base, abs=1e-6)
    model.set_head_mask([])
    assert exp7.icl_gain(model, tokens) == pytest.approx(base, abs=1e-9)


class _WordTokenizer:
    """One id per word, so every name is a single token and prompts are comparable."""

    def __init__(self) -> None:
        self.vocab: dict[str, int] = {}

    def encode(self, text: str) -> list[int]:
        words = re.findall(r" ?\w+|[,.]", text)
        return [self.vocab.setdefault(w, len(self.vocab)) for w in words]


def test_ioi_prompts_repeat_s_and_never_io_and_share_a_length_per_template() -> None:
    tok = _WordTokenizer()
    batches = list(exp7.ioi_batches(tok, list(exp7.NAMES), seed=0, n=60))
    assert sum(len(b[0]) for b in batches) == 60
    for tokens, io, s in batches:
        assert (io != s).all()
        for row, i, j in zip(tokens, io, s):
            ids = row.tolist()
            assert ids.count(int(j)) == 2 and ids.count(int(i)) == 1


def test_single_token_names_splits_kept_and_dropped() -> None:
    class Tok:
        def encode(self, text: str) -> list[int]:
            return [1, 2] if text == " Michael" else [1]

    kept, dropped = exp7.single_token_names(Tok())
    assert dropped == [" Michael"] and " Michael" not in kept
    assert len(kept) == len(exp7.NAMES) - 1


def test_control_triples_are_fixed_distinct_and_valid() -> None:
    a, b = exp7.control_triples(), exp7.control_triples()
    assert a == b and len(a) == exp7.N_CONTROL_TRIPLES
    for triple in a:
        assert len(set(triple)) == 3
        assert all(0 <= layer < 12 and 0 <= head < 12 for layer, head in triple)


def test_the_frozen_thresholds_match_adr_0034() -> None:
    """The ADR is the pre-registration; the constants must be the ones it states."""
    adr = ADR.read_text(encoding="utf-8")
    for needle in ("**1e-5**", "**0.3**", "**10%**", "**2.0**", "**90%**", "**30%**"):
        assert needle in adr, needle
    assert (exp7.PARITY_TOL, exp7.MASS_THRESHOLD, exp7.ICL_GAIN_DROP) == (1e-5, 0.3, 0.10)
    assert (exp7.IOI_MIN_MEAN, exp7.IOI_MIN_POSITIVE, exp7.NAME_MOVER_DROP) == (2.0, 0.9, 0.30)
    assert exp7.INDUCTION_HEADS == ((5, 5), (6, 9))
    assert exp7.NAME_MOVERS == ((9, 6), (9, 9), (10, 0))


def test_ties_count_against_the_target_head() -> None:
    m = np.array([[0.9, 0.9], [0.9, 0.1]])
    assert exp7.rank_of(m, 0, 0) == 3  # three heads share the top score: the target is last


def test_adr0035_resumes_from_the_seeds_already_done(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A killed run must not redo finished seeds, and the manifests must cover every seed."""
    calls: list[int] = []

    class _Model:
        def mean_head_outputs(self, tokens: torch.Tensor) -> dict[int, torch.Tensor]:
            return {0: torch.zeros(1)}

    def stage2(model: object, seed: int) -> tuple[dict, list]:
        calls.append(seed)
        if len(calls) == 2:
            raise MemoryError("killed")  # the process dies during the second seed
        return {}, [(0, 0, 1.0)]

    monkeypatch.setattr(exp7, "induction_sequences", lambda s: torch.zeros(1, 2, dtype=torch.long))
    monkeypatch.setattr(exp7, "ioi_reference_means", lambda *a: {0: {0: torch.zeros(1)}})
    monkeypatch.setattr(exp7, "ioi_groups", lambda *a: {})
    monkeypatch.setattr(exp7, "stage2_seed", stage2)
    monkeypatch.setattr(
        exp7, "stage6_seed", lambda *a: {"icl_gain_drop": 0.5, "control_pairs_drop_p95": 0.1}
    )
    monkeypatch.setattr(exp7, "stage7_seed", lambda *a: {"stage7_pass": 1.0})
    monkeypatch.setattr(exp7, "stage8_seed", lambda *a: ({"stage8_pass": 1.0}, [(0, 0, 0.5)]))
    saved: dict[int, list[int]] = {}

    def save(stage: int, seeds: list[int], *_: object, **__: object) -> None:
        saved[stage] = seeds

    with pytest.raises(MemoryError):
        exp7.run_adr0035(_Model(), None, [], save, cache=tmp_path)  # type: ignore[arg-type]
    assert saved == {}  # nothing is written until every seed exists

    calls.clear()
    monkeypatch.setattr(exp7, "stage2_seed", lambda m, s: (calls.append(s), ({}, [(0, 0, 1.0)]))[1])
    assert exp7.run_adr0035(_Model(), None, [], save, cache=tmp_path) == 0  # type: ignore[arg-type]
    assert calls == [1, 2]  # seed 0 was finished before the kill and is not redone
    assert saved == {6: [0, 1, 2], 7: [0, 1, 2], 8: [0, 1, 2]}


class _IdTokenizer:
    def __call__(self, text: str, return_tensors: str = "pt") -> dict[str, torch.Tensor]:
        return {"input_ids": torch.tensor([[ord(c) % 90 for c in text[:6]]])}

    def convert_ids_to_tokens(self, ids: list[int]) -> list[str]:
        return [str(i) for i in ids]


def test_explorer_payload_has_causal_patterns_that_sum_to_one() -> None:
    payload = exp7.explorer_payload(_tiny(), _IdTokenizer(), "rev", (("p", "abcdef"),))
    assert payload["sources"] and payload["revision"] == "rev"
    for prompt in payload["prompts"]:
        n = len(prompt["tokens"])
        assert len(prompt["patterns"]) == 2 and len(prompt["patterns"][0]) == 4
        m = np.array(prompt["patterns"][1][2])
        assert m.shape == (n, n)
        assert np.allclose(m.sum(axis=1), 1.0, atol=0.01)
        assert np.allclose(np.triu(m, k=1), 0.0)  # no head looks ahead


def test_explorer_sources_are_tracked_manifests() -> None:
    repo = Path(__file__).resolve().parents[1]
    for rel in exp7.EXPLORER_SOURCES:
        assert (repo / rel).is_file(), rel
