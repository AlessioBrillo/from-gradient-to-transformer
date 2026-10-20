"""Planted-construction tests for the detector on the variable-distance task.

Why this file exists
--------------------
The 2026-10-19 audit found that every "0 / N induction heads" number this
repository published was a statement about the *detector*: the detector
measured the previous-token offset and called it the copy offset. The
lesson was learned with planted tests, so it is learned again here with
planted tests.

On the variable-distance task the two mechanisms finally point at different
keys, so the detector can be pinned against both:

* a head that attends to ``prev(q) + 1`` (the token after the previous
  occurrence) **must** be detected — this is the induction mechanism;
* a head that attends to a fixed offset ``q - d`` **must not** be
  detected, however much mass it carries — this is the shortcut the
  periodic task allowed;
* a previous-token head (``q - 1``) must not be detected either.

A detector that cannot tell the second from the first would be reporting
the shortcut as the mechanism, which is exactly the mistake this repository
already made once.
"""

from __future__ import annotations

import numpy as np
import torch
from torch import nn

from src.experiments.induction_detection import (
    build_copy_layout,
    detect_heads,
    run_content_vs_offset_probe,
)
from src.experiments.induction_tasks import (
    TASK_VARIABLE,
    TaskSpec,
    make_variable_tokens,
)

VOCAB = 256
SEQ_LEN = 32
SPEC = TaskSpec.variable(
    vocab_size=VOCAB, seq_len=SEQ_LEN, key_len=18, copy_blocks=2, copy_block_len=4
)
THRESHOLD = 0.3


def _tokens(n: int = 16, seed: int = 0) -> torch.Tensor:
    return torch.from_numpy(make_variable_tokens(SPEC, n, seed))


def _planted(
    tokens: torch.Tensor,
    masses: list[list[float]],
    mode: str,
    offset: int = 3,
) -> list[torch.Tensor]:
    """One (B, H, W, W) tensor per layer with planted attention mass.

    ``mode="content"`` plants the mass on ``prev(q) + 1`` at every copy
    query — the induction mechanism. ``mode="offset"`` plants it on
    ``q - offset`` at every query — the positional shortcut. The rest of
    the probability mass is spread uniformly over the causal keys, exactly
    as the periodic task's planted constructions do.
    """
    layout = build_copy_layout(tokens, task=TASK_VARIABLE)
    content_keys: dict[tuple[int, int], int] = {}
    for b, q, k in layout.content:
        content_keys[(int(b), int(q))] = int(k)

    width = tokens.shape[1]
    batch = tokens.shape[0]
    layers: list[torch.Tensor] = []
    for layer_masses in masses:
        n_heads = len(layer_masses)
        probs = torch.zeros(batch, n_heads, width, width)
        for h, m in enumerate(layer_masses):
            for b in range(batch):
                for q in range(width):
                    n_keys = q + 1
                    row = torch.full((n_keys,), (1.0 - m) / max(n_keys - 1, 1))
                    if mode == "content":
                        key = content_keys.get((b, q))
                    else:
                        key = q - offset
                    if key is not None and 0 <= key <= q:
                        row[key] = m
                    probs[b, h, q, :n_keys] = row
        layers.append(probs)
    return layers


class _Stub(nn.Module):
    """A stand-in model that emits planted attention patterns.

    The detector's real collection path runs against it, so a broken
    collection path cannot hide a head that is really there.
    """

    def __init__(self, masses: list[list[float]], mode: str, offset: int = 3) -> None:
        super().__init__()
        self._masses = masses
        self._mode = mode
        self._offset = offset
        self.blocks = [None] * len(masses)

    def forward(self, x: torch.Tensor, record_attn: bool = False):
        if not record_attn:
            return None, None
        return None, _planted(x, self._masses, self._mode, self._offset)


class TestVariableTaskDetection:
    def test_a_content_head_is_detected(self) -> None:
        tokens = _tokens()
        patterns = _planted(tokens, [[0.9]], "content")
        report = detect_heads(patterns, tokens, 0, task=TASK_VARIABLE)
        assert report.hypothesis == "content"
        assert report.confirmed == [[0]]
        assert report.peak("induction") > THRESHOLD

    def test_a_fixed_offset_head_is_not_detected(self) -> None:
        """The shortcut the periodic task allowed must not pass as the mechanism."""
        tokens = _tokens()
        patterns = _planted(tokens, [[0.9]], "offset", offset=5)
        report = detect_heads(patterns, tokens, 0, task=TASK_VARIABLE)
        assert report.confirmed == [[]]
        assert report.peak("induction") < THRESHOLD

    def test_a_previous_token_head_is_not_detected(self) -> None:
        tokens = _tokens()
        patterns = _planted(tokens, [[0.9]], "offset", offset=1)
        report = detect_heads(patterns, tokens, 0, task=TASK_VARIABLE)
        assert report.confirmed == [[]]

    def test_the_offset_profile_finds_the_planted_offset(self) -> None:
        tokens = _tokens()
        patterns = _planted(tokens, [[0.9]], "offset", offset=5)
        report = detect_heads(patterns, tokens, 0, task=TASK_VARIABLE)
        assert report.best_offset == 5
        assert report.peak_offset_mass > 0.5

    def test_the_content_head_beats_the_offset_profile(self) -> None:
        tokens = _tokens()
        patterns = _planted(tokens, [[0.9]], "content")
        report = detect_heads(patterns, tokens, 0, task=TASK_VARIABLE)
        assert report.peak("content") > report.peak_offset_mass

    def test_the_queries_are_the_copy_queries(self) -> None:
        tokens = _tokens()
        patterns = _planted(tokens, [[0.9]], "content")
        report = detect_heads(patterns, tokens, 0, task=TASK_VARIABLE)
        assert report.n_copy_queries > 0
        assert report.n_periodic_queries == 0
        # The layout's query set is the copy-query set, not "every position
        # that has a previous occurrence".
        geom = np.asarray(
            [
                [b, q]
                for b, q, _ in build_copy_layout(tokens, task=TASK_VARIABLE).content
            ]
        )
        assert len(geom) == report.n_copy_queries


class TestContentVersusOffsetProbe:
    def test_a_content_head_wins_the_native_probe(self) -> None:
        tokens = _tokens()
        probe = run_content_vs_offset_probe(
            _Stub([[0.9]], "content"), tokens
        )
        assert probe["peak_content_mass"] > 0.5
        assert probe["content_wins"] is True

    def test_a_fixed_offset_head_loses_the_native_probe(self) -> None:
        tokens = _tokens()
        probe = run_content_vs_offset_probe(
            _Stub([[0.9]], "offset", offset=5), tokens
        )
        assert probe["peak_offset_mass"] > 0.5
        assert probe["content_wins"] is False

    def test_the_probe_needs_no_off_distribution_batch(self) -> None:
        """The variable task's dissociation is native: the *training*
        distribution is the probe."""
        tokens = _tokens()
        probe = run_content_vs_offset_probe(_Stub([[0.9]], "content"), tokens)
        assert probe["n_copy_queries"] > 0
        assert "logit_diff_content_minus_period" not in probe
