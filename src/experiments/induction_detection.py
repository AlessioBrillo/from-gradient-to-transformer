"""Shared induction-head detection for Rungs 1, 4 and 5.

Why this module exists
----------------------
Until 2026-10-19 this repository carried **three** different "is this an
induction head?" detectors, and every one of them measured the wrong thing:

* ``exp1_induction_heads.analyze_induction_heads`` and
  ``exp1_induction_heads.compute_attention_entropy`` measured the attention
  mass on the *previous-token* offset (``q -> q-1``) and called it "diag+1";
* ``exp4_circuit_patching.detect_induction_heads`` measured
  ``attn_probs.diagonal(offset=1)`` — the strict upper triangle of a causal
  softmax, which is exactly zero — so it could never fire, ever;
* the planted tests planted the same wrong pattern, so they passed and the
  science did not.

Every "0 / N heads" number this repository has ever published was therefore a
statement about the *detector*, not about the model. This module is the single
source of truth now: one offset convention, one threshold, one composition
measure, one naming test — shared by every rung that touches the question.

The offsets (this is the part that was wrong)
---------------------------------------------
The task is ``prefix + prefix`` with a prefix of length ``L``. At a query
position ``q`` in the second copy, the token ``x[q]`` has (usually) its
previous occurrence at ``q - L``, so the token to copy sits at ``q - L + 1``::

    key(q) = q - L + 1     <- the induction (copy) offset
    key(q) = q - L         <- the duplicate-token offset (Nanda's Step 1)
    key(q) = q - 1         <- the previous-token head (NOT induction)

The old detector measured the third row and called it the first. A head that
attends to ``q - 1`` is a *previous-token* head: a different circuit, which on
this task does not copy the repeated token at all.

Two subtleties the old detector also ignored
--------------------------------------------
1. **Collisions.** The prefix can contain a repeated token (~21% of the time
   at the standard config). Then the *nearest* previous occurrence of ``x[q]``
   sits closer than ``q - L``, and the content-based target differs from the
   period-based one. The masses below are averaged over the **periodic
   queries only** — those whose nearest previous occurrence is exactly
   ``q - L`` — so the metric is neither diluted nor inflated by the
   ambiguous positions.

2. **Content vs. position.** On ``prefix + prefix`` the previous occurrence of
   ``x[q]`` is *always* at ``q - L``, so a head that attends to ``q - L + 1``
   by pure position arithmetic and a head that attends to the token *after
   the previous occurrence of the same token* are the **same function** on
   this task. No on-distribution measurement can tell them apart — not the
   mass, not the K-composition score (which takes the previous occurrence
   from a layer-0 head's own argmax, which on a periodic task is the same
   position). ``run_dissociation_probe`` is the test that can: it feeds a
   batch whose second half is a *permuted* copy of the prefix, so the content
   target and the position target point at different keys, and it reports
   which one the head follows.

   Until that probe has run on a given checkpoint, the honest wording for a
   detected head is "prefix-copying head at offset ``L-1``", not "induction
   head".
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Optional

import numpy as np
import torch
from torch import nn
from torch.utils.data import DataLoader

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Pre-registered thresholds
# ---------------------------------------------------------------------------
# The mass threshold is the one the repository has used since 2026-08-01
# (Olsson et al.'s per-head detection threshold). It is a convention, not a
# derived boundary, and it is applied to the *correct* offset now.
INDUCTION_MASS_THRESHOLD = 0.3

# A head is only *confirmed* when the mechanism is there too: the layer-1
# head must compose with a layer-0 head (Nanda & Jacobsen Step 2) at a score
# at least this high. Calibrated on planted constructions: a hand-built
# two-step chain scores ~1.0, uniform attention scores ~1/S.
COMPOSITION_THRESHOLD = 0.4

# How many attention batches to collect for the analysis. The old detector
# collected "32 * n_layers" batches; 32 batches is enough for the mass
# averages to be stable at these sequence lengths and keeps the analysis
# cheap enough to run *during* training (early stop).
DEFAULT_MAX_BATCHES = 32


# ---------------------------------------------------------------------------
# Layout helpers
# ---------------------------------------------------------------------------
def prefix_length_for(seq_len: int, prefix_ratio: float = 0.5) -> int:
    """The generator's prefix length.

    ``make_repeated_token_data`` builds ``prefix_len = max(2, int(seq_len *
    prefix_ratio))`` and then tiles the prefix to fill the sequence, so the
    distance between two consecutive occurrences of the same token is
    exactly ``prefix_len`` (unless the prefix itself contains a duplicate).
    """
    return max(2, int(seq_len * prefix_ratio))


def nearest_previous_occurrence(tokens: torch.Tensor) -> torch.Tensor:
    """Index of the nearest earlier occurrence of each token.

    Args:
        tokens: ``(B, S)`` token ids.

    Returns:
        ``(B, S)`` tensor where entry ``[b, q]`` is the largest ``p < q``
        with ``tokens[b, p] == tokens[b, q]``, or ``-1`` when the token has
        not occurred before.
    """
    arr = tokens.detach().cpu().numpy()
    if arr.ndim == 1:
        arr = arr[None, :]
    bsz, seq = arr.shape
    out = np.full((bsz, seq), -1, dtype=np.int64)
    for b in range(bsz):
        last: dict[int, int] = {}
        row = arr[b]
        for q in range(seq):
            token = int(row[q])
            out[b, q] = last.get(token, -1)
            last[token] = q
    return torch.from_numpy(out)


def _query_triples(tokens: torch.Tensor, prefix_len: int) -> dict[str, np.ndarray]:
    """The (batch, query, key) triples each hypothesis is measured on.

    Four sets are produced, all restricted to the *second copy* of the
    sequence (``q >= prefix_len``), where the copy task actually lives:

    ``periodic``   key ``q - L + 1`` — the induction/copy offset, measured
                   only on the queries whose nearest previous occurrence is
                   exactly ``q - L`` (the collision-free ones);
    ``duplicate``  key ``q - L`` — the duplicate-token offset (Step 1), on the
                   same queries;
    ``content``    key ``prev(q) + 1`` — "the token after the previous
                   occurrence of the same token", on *every* query that has a
                   previous occurrence (so it also covers the collision
                   queries, where it differs from the periodic offset);
    ``prev_token`` key ``q - 1`` — the previous-token head. This is the
                   offset the old detector measured and called "diag+1"; it is
                   kept as an explicitly labelled control.
    """
    arr = tokens.detach().cpu().numpy()
    if arr.ndim == 1:
        arr = arr[None, :]
    bsz, seq = arr.shape
    periodic: list[tuple[int, int, int]] = []
    duplicate: list[tuple[int, int, int]] = []
    content: list[tuple[int, int, int]] = []
    prev_token: list[tuple[int, int, int]] = []

    for b in range(bsz):
        row = arr[b]
        last: dict[int, int] = {}
        for q in range(seq):
            token = int(row[q])
            prev = last.get(token, -1)
            last[token] = q
            if q < prefix_len:
                # First copy: there is nothing to copy yet.
                continue
            if prev >= 0:
                content.append((b, q, prev + 1))
                prev_token.append((b, q, q - 1))
                if prev == q - prefix_len:
                    periodic.append((b, q, q - prefix_len + 1))
                    duplicate.append((b, q, q - prefix_len))

    def _stack(items: list[tuple[int, int, int]]) -> np.ndarray:
        if not items:
            return np.zeros((0, 3), dtype=np.int64)
        return np.asarray(items, dtype=np.int64)

    return {
        "periodic": _stack(periodic),
        "duplicate": _stack(duplicate),
        "content": _stack(content),
        "prev_token": _stack(prev_token),
    }


def _mean_mass(probs: torch.Tensor, triples: np.ndarray) -> np.ndarray:
    """Mean attention probability per head on the given (b, q, key) triples."""
    if triples.size == 0:
        return np.zeros(probs.shape[1], dtype=float)
    b = torch.as_tensor(triples[:, 0], dtype=torch.long)
    q = torch.as_tensor(triples[:, 1], dtype=torch.long)
    k = torch.as_tensor(triples[:, 2], dtype=torch.long)
    vals = probs[b, :, q, k]  # (N, H)
    return vals.mean(dim=0).cpu().numpy()


# ---------------------------------------------------------------------------
# Model-family agnostic attention access
# ---------------------------------------------------------------------------
def model_device(model: nn.Module) -> torch.device:
    """The device the model lives on.

    A model without parameters (the planted-pattern stubs in the tests)
    has no device of its own; CPU is the only sensible answer there.
    """
    try:
        return next(model.parameters()).device
    except StopIteration:  # pragma: no cover - parameterless stubs
        return torch.device("cpu")


def model_logits(model: nn.Module, x: torch.Tensor) -> torch.Tensor:
    """Logits for a batch, whatever protocol the model speaks.

    ``AttentionOnlyTransformer`` returns ``(logits, attn_records)`` and
    ``DecoderOnlyTransformer`` returns ``(logits, cache)``; both are tuples,
    and both put the logits first.
    """
    out = model(x)
    if isinstance(out, tuple):
        return out[0]
    return out


def _supports(model: nn.Module, kwarg: str) -> bool:
    """Does `model.forward` accept `kwarg` as a *parameter*?

    The check must look at the signature, not at `__code__.co_varnames`:
    `co_varnames` also lists local variables, and
    `DecoderOnlyTransformer.forward` has a local named `cache` (the
    activation dict it returns) while its signature only offers
    `return_cache`. Reading `co_varnames` therefore made the dispatcher
    believe the decoder accepted `cache=` and call it with a keyword it
    does not have.
    """
    import inspect

    forward = getattr(model, "forward", None)
    if forward is None:
        return False
    try:
        return kwarg in inspect.signature(forward).parameters
    except (TypeError, ValueError):  # pragma: no cover - exotic callables
        return False


def attention_patterns_for_inputs(
    model: nn.Module, x: torch.Tensor
) -> list[torch.Tensor]:
    """Per-layer attention probabilities ``(B, H, S, S)`` for a batch.

    The ``cache`` protocol is preferred (it is the one that also carries the
    value tensors and the residual stream, which the patching interventions
    need); the ``record_attn`` protocol is the fallback for models that do
    not implement a cache.
    """
    model.eval()
    with torch.no_grad():
        if _supports(model, "cache"):
            _, cache = model(x, cache={})
            if cache:
                return [
                    cache[f"blocks.{i}.attn.attn_probs"].detach().cpu()
                    for i in range(len(model.blocks))
                ]
        if _supports(model, "record_attn"):
            _, records = model(x, record_attn=True)
            if records:
                return [r.detach().cpu() for r in records]
        if _supports(model, "return_cache"):
            _, cache = model(x, return_cache=True)
            if cache:
                return [
                    cache[f"blocks.{i}.attn.attn_probs"].detach().cpu()
                    for i in range(len(model.blocks))
                ]
    return []


def collect_patterns_and_tokens(
    model: nn.Module,
    loader: DataLoader,
    max_batches: int = DEFAULT_MAX_BATCHES,
) -> tuple[list[torch.Tensor], torch.Tensor]:
    """Collect attention patterns and the input tokens they belong to.

    Returns ``(patterns, tokens)`` where ``patterns[i]`` is a
    ``(B_total, H, S, S)`` tensor (layers concatenated along the batch
    axis) and ``tokens`` is the ``(B_total, S)`` input ids. The tokens are
    what makes the offset conventions checkable: without them the detector
    would be guessing the layout instead of reading it.
    """
    model.eval()
    per_layer: list[list[torch.Tensor]] = []
    token_batches: list[torch.Tensor] = []
    with torch.no_grad():
        for x, _ in loader:
            x = x.to(model_device(model))
            patterns = attention_patterns_for_inputs(model, x)
            if not patterns:
                break
            if not per_layer:
                per_layer = [[] for _ in patterns]
            for i, pat in enumerate(patterns):
                per_layer[i].append(pat)
            token_batches.append(x.detach().cpu())
            if len(token_batches) >= max_batches:
                break

    if not per_layer:
        return [], torch.zeros((0, 0), dtype=torch.long)
    concatenated = [torch.cat(items, dim=0) for items in per_layer]
    tokens = torch.cat(token_batches, dim=0)
    return concatenated, tokens


# ---------------------------------------------------------------------------
# Masses
# ---------------------------------------------------------------------------
def head_masses(
    patterns: list[torch.Tensor],
    tokens: torch.Tensor,
    prefix_len: int,
) -> dict[str, list[np.ndarray]]:
    """Per-layer, per-head attention masses for the four hypotheses.

    Returns a dict with one entry per hypothesis; each entry is a list (one
    per layer) of arrays (one per head). All four are on the same [0, 1]
    scale, so they are directly comparable with each other and with the
    detection threshold.
    """
    triples = _query_triples(tokens, prefix_len)
    out: dict[str, list[np.ndarray]] = {
        "induction": [],
        "duplicate": [],
        "content": [],
        "prev_token": [],
    }
    for probs in patterns:
        probs = probs.detach().cpu()
        out["induction"].append(_mean_mass(probs, triples["periodic"]))
        out["duplicate"].append(_mean_mass(probs, triples["duplicate"]))
        out["content"].append(_mean_mass(probs, triples["content"]))
        out["prev_token"].append(_mean_mass(probs, triples["prev_token"]))
    return out


def layer_entropy(patterns: list[torch.Tensor]) -> list[float]:
    """Per-layer attention entropy (nats), summed over heads.

    The same convention as the old `compute_attention_entropy`: the mean
    per-head entropy of the layer, summed over the heads. Lower means more
    focused attention.
    """
    out: list[float] = []
    for probs in patterns:
        probs = probs.detach().cpu().float()
        ent = -(probs * (probs + 1e-8).log()).sum(-1)  # (B, H, S)
        out.append(float(ent.mean(dim=(0, 2)).sum().item()))
    return out


# ---------------------------------------------------------------------------
# K-composition (Nanda & Jacobsen 2023, Step 2)
# ---------------------------------------------------------------------------
def k_composition_scores(p0: torch.Tensor, p1: torch.Tensor) -> np.ndarray:
    """K-composition scores between a layer-0 head set and a layer-1 head set.

    Nanda & Jacobsen (2023), "Attention as a Step Towards the Emergence of
    the Induction Head", Step 2: in K-composition, the layer-1 head attends
    from query position q to ``prev(q) + 1``, where ``prev(q)`` is the
    position the layer-0 duplicate-token head attended to at q (the previous
    occurrence of the current token) and +1 is the position holding the
    token to copy. The induction head is the composition of Step 1 (L0
    duplicate head) and Step 2 (L1 K-composition).

    Returns a (n_heads_0, n_heads_1) matrix: row h0's `prev` combined with
    column h1's attention.

    Self-attention guard: queries where ``prev(q) + 1 == q`` are excluded —
    a head attending to itself would trivially score 1.0 on a shift-by-one
    prev pattern without being an induction head at all. This makes the
    detector falsifiable (see TestKComposition).

    What this measure can and cannot decide
    ----------------------------------------
    On a *periodic* task (``prefix + prefix``) the layer-0 head's argmax and
    the content-based previous occurrence are the same position, so this
    score cannot separate a content-matching circuit from a positional one.
    It measures that a two-step circuit exists; `run_dissociation_probe`
    measures what the circuit is made of.
    """
    B, H0, S, _ = p0.shape
    H1 = p1.shape[1]
    if B == 0 or S == 0:
        return np.zeros((H0, H1))

    prev = p0.argmax(dim=-1)  # (B, H0, S): position L0 head h0 attended to at q
    target = prev + 1  # (B, H0, S): position one token after it
    qs = torch.arange(S, device=p0.device)
    # Gate: in-bounds, and the L0 head must actually point at a *different*
    # position than q — a head attending to itself is not a previous-
    # occurrence signal, and a head attending to q-1 (prev+1 == q) is plain
    # self-attention, not induction.
    valid = (target < S) & (prev != qs) & (target != qs)

    scores = np.zeros((H0, H1))
    for h0 in range(H0):
        idx = target[:, h0].clamp(max=S - 1)  # (B, S); OOB entries masked below
        idx_gather = idx.unsqueeze(1).unsqueeze(-1).expand(B, H1, S, S)
        vals = torch.gather(p1, -1, idx_gather)  # (B, H1, S, S)
        diag = vals.diagonal(dim1=-2, dim2=-1)  # (B, H1, S): vals[b, h1, q, q]
        mask = valid[:, h0]  # (B, S)
        n_valid = int(mask.sum())
        if n_valid:
            masked = diag * mask[:, None, :].to(diag.dtype)  # (B, H1, S)
            # .cpu() BEFORE .numpy(): exp6's compute_k_composition_scores moves
            # the collected patterns back to the device, so on GPU this tensor
            # is a cuda tensor and .numpy() raises TypeError ("can't convert
            # cuda:0 device type tensor to numpy"). The CPU path took the
            # .to(DEVICE) as a no-op, so every planted test passed while the
            # GPU run died — found by the first capstone kernel on Kaggle.
            scores[h0] = masked.sum(dim=(0, 2)).cpu().numpy() / max(n_valid, 1)
    return scores


# ---------------------------------------------------------------------------
# Detection report
# ---------------------------------------------------------------------------
@dataclass
class DetectionReport:
    """Everything the detector knows about one model, in one object."""

    masses: dict[str, list[np.ndarray]] = field(default_factory=dict)
    screen: list[list[int]] = field(default_factory=list)
    confirmed: list[list[int]] = field(default_factory=list)
    composition_by_layer: list[float] = field(default_factory=list)
    entropy: list[float] = field(default_factory=list)
    best_pair: tuple[int, int, int, int] = (-1, -1, -1, -1)
    n_periodic_queries: int = 0
    n_content_queries: int = 0

    @property
    def screen_count(self) -> int:
        return sum(len(h) for h in self.screen)

    @property
    def confirmed_count(self) -> int:
        return sum(len(h) for h in self.confirmed)

    @property
    def best_composition(self) -> float:
        return max(self.composition_by_layer) if self.composition_by_layer else 0.0

    def peak(self, hypothesis: str) -> float:
        """The best per-head mass of one hypothesis across layers and heads."""
        values = self.masses.get(hypothesis, [])
        if not values:
            return 0.0
        return float(max((float(v.max()) if len(v) else 0.0) for v in values))


def detect_heads(
    patterns: list[torch.Tensor],
    tokens: torch.Tensor,
    prefix_len: int,
    mass_threshold: float = INDUCTION_MASS_THRESHOLD,
    composition_threshold: float = COMPOSITION_THRESHOLD,
) -> DetectionReport:
    """Screen on the induction mass, then confirm on the mechanism.

    * **Screen**: a head is a *candidate* when its induction mass
      (``q -> q-L+1``) is above ``mass_threshold``.
    * **Confirmation**: a candidate is *confirmed* when the layer it lives in
      is composed with an earlier layer at a K-composition score of at least
      ``composition_threshold``. The first layer has no earlier layer, so its
      candidates are confirmed on the mass alone — that limitation is
      reported through ``composition_by_layer`` (0.0 for layer 0).

    The two-stage rule exists because either half alone is insufficient: the
    mass alone cannot tell a copy circuit from a previous-token head, and the
    composition alone cannot attribute anything to a head that does not
    exist.
    """
    report = DetectionReport()
    if not patterns:
        return report

    masses = head_masses(patterns, tokens, prefix_len)
    report.masses = masses
    report.entropy = layer_entropy(patterns)
    triples = _query_triples(tokens, prefix_len)
    report.n_periodic_queries = int(triples["periodic"].shape[0])
    report.n_content_queries = int(triples["content"].shape[0])

    report.screen = [
        [int(h) for h in range(len(m)) if float(m[h]) > mass_threshold]
        for m in masses["induction"]
    ]

    # Best K-composition score *into* each (layer, head) pair.
    best_into: dict[tuple[int, int], float] = {}
    layer_scores: list[float] = [0.0] * len(patterns)
    best_score = -1.0
    best_pair = (-1, -1, -1, -1)
    for l_src in range(len(patterns) - 1):
        for l_dest in range(l_src + 1, len(patterns)):
            comp = k_composition_scores(patterns[l_src], patterns[l_dest])
            if comp.size == 0:
                continue
            flat = int(np.argmax(comp))
            h0, h1 = flat // comp.shape[1], flat % comp.shape[1]
            value = float(comp.flat[flat])
            layer_scores[l_dest] = max(layer_scores[l_dest], value)
            for h1_idx in range(comp.shape[1]):
                column_max = float(comp[:, h1_idx].max())
                key = (l_dest, h1_idx)
                if column_max > best_into.get(key, -1.0):
                    best_into[key] = column_max
            if value > best_score:
                best_score = value
                best_pair = (l_src, l_dest, h0, h1)

    report.composition_by_layer = layer_scores
    report.best_pair = best_pair

    confirmed: list[list[int]] = []
    for layer_idx, heads in enumerate(report.screen):
        keep: list[int] = []
        for head in heads:
            if layer_idx == 0:
                # No earlier layer to compose with: mass-only confirmation.
                keep.append(head)
                continue
            if best_into.get((layer_idx, head), 0.0) >= composition_threshold:
                keep.append(head)
        confirmed.append(keep)
    report.confirmed = confirmed
    return report


def detect_from_inputs(
    model: nn.Module,
    inputs: torch.Tensor,
    prefix_len: Optional[int] = None,
    mass_threshold: float = INDUCTION_MASS_THRESHOLD,
    composition_threshold: float = COMPOSITION_THRESHOLD,
) -> tuple[DetectionReport, list[torch.Tensor]]:
    """Detect heads on a raw batch of inputs.

    The inputs *are* the tokens the analysis needs, so no loader is
    required — this is the entry point exp4 (Rung 4) uses, where the batch
    comes from the validation split rather than from a DataLoader.
    """
    patterns = attention_patterns_for_inputs(model, inputs)
    tokens = inputs.detach().cpu()
    if prefix_len is None:
        prefix_len = prefix_length_for(int(inputs.shape[1]) + 1)
    report = detect_heads(
        patterns,
        tokens,
        prefix_len,
        mass_threshold=mass_threshold,
        composition_threshold=composition_threshold,
    )
    return report, patterns


def detect_from_loader(
    model: nn.Module,
    loader: DataLoader,
    prefix_len: Optional[int] = None,
    mass_threshold: float = INDUCTION_MASS_THRESHOLD,
    composition_threshold: float = COMPOSITION_THRESHOLD,
    max_batches: int = DEFAULT_MAX_BATCHES,
) -> tuple[DetectionReport, list[torch.Tensor], torch.Tensor]:
    """Collect, measure and judge in one call.

    ``prefix_len`` defaults to the standard ``seq_len / 2`` layout; pass it
    explicitly whenever the data was generated with a different
    ``prefix_ratio``.
    """
    patterns, tokens = collect_patterns_and_tokens(model, loader, max_batches)
    if prefix_len is None:
        seq_len = tokens.shape[1] + 1 if tokens.numel() else 0
        prefix_len = prefix_length_for(seq_len)
    report = detect_heads(
        patterns,
        tokens,
        prefix_len,
        mass_threshold=mass_threshold,
        composition_threshold=composition_threshold,
    )
    return report, patterns, tokens


# ---------------------------------------------------------------------------
# Dissociation probe: content-based copy vs. positional shift
# ---------------------------------------------------------------------------
def make_dissociation_batch(
    vocab_size: int,
    seq_len: int,
    num_samples: int = 32,
    seed: int = 0,
) -> dict[str, torch.Tensor]:
    """A batch where the content target and the position target disagree.

    The first half of every sequence is a random prefix of ``L`` distinct
    tokens. The second half is the *same tokens in a different order* (a
    random cyclic shift, which is a derangement: no token keeps its
    position). At a second-copy query ``q = L + j``:

    * the **content** hypothesis says the head attends to
      ``pos_prefix(x[q]) + 1`` — the token that followed the previous
      occurrence of the *same* token;
    * the **period** hypothesis says the head attends to ``q - L + 1`` — the
      fixed offset it would use on the training distribution.

    With a cyclic shift the two keys never coincide, so every second-copy
    query is a conflict. The batch is off-distribution for a model trained
    on the periodic task — deliberately: it is the only way to tell the two
    mechanisms apart.

    Returns a dict with ``x`` ``(B, S)``, ``y`` ``(B, S)``, ``content_key``
    ``(B, S)``, ``period_key`` ``(B, S)``, ``content_answer`` ``(B, S)`` and
    ``period_answer`` ``(B, S)``. The ``*_key`` tensors are ``-1`` where the
    key is undefined (first copy).
    """
    if seq_len % 2 != 0:
        raise ValueError(
            f"the dissociation probe needs an even seq_len (got {seq_len}) — "
            "the second half must be a permutation of the first."
        )
    prefix_len = seq_len // 2
    if prefix_len < 3:
        raise ValueError(
            f"the dissociation probe needs seq_len >= 6 (got {seq_len})"
        )
    if vocab_size < prefix_len:
        raise ValueError(
            f"vocab_size ({vocab_size}) must exceed the prefix length "
            f"({prefix_len}) so the prefix tokens are distinct"
        )

    rng = np.random.default_rng(seed)
    tokens = np.zeros((num_samples, seq_len), dtype=np.int64)
    content_key = np.full((num_samples, seq_len), -1, dtype=np.int64)
    period_key = np.full((num_samples, seq_len), -1, dtype=np.int64)

    for b in range(num_samples):
        prefix = rng.choice(vocab_size, size=prefix_len, replace=False)
        shift = int(rng.integers(1, prefix_len))
        perm = (np.arange(prefix_len) + shift) % prefix_len
        tokens[b, :prefix_len] = prefix
        tokens[b, prefix_len:] = prefix[perm]
        for j in range(prefix_len):
            q = prefix_len + j
            if q >= seq_len - 1:
                # The input is tokens[:-1]; the last token is the target only.
                continue
            content_key[b, q] = int(perm[j]) + 1
            period_key[b, q] = j + 1

    x = torch.from_numpy(tokens[:, :-1])
    y = torch.from_numpy(tokens[:, 1:])
    safe_keys = np.clip(content_key, 0, tokens.shape[1] - 1)
    safe_period = np.clip(period_key, 0, tokens.shape[1] - 1)
    content_answer = torch.from_numpy(
        np.where(content_key >= 0, np.take_along_axis(tokens, safe_keys, axis=1), -1)
    )
    period_answer = torch.from_numpy(
        np.where(period_key >= 0, np.take_along_axis(tokens, safe_period, axis=1), -1)
    )
    return {
        "x": x,
        "y": y,
        "content_key": torch.from_numpy(content_key),
        "period_key": torch.from_numpy(period_key),
        "content_answer": content_answer,
        "period_answer": period_answer,
    }


def run_dissociation_probe(
    model: nn.Module,
    batch: Optional[dict[str, torch.Tensor]] = None,
    vocab_size: int = 2048,
    seq_len: int = 64,
    num_samples: int = 32,
    seed: int = 0,
) -> dict:
    """Does the model copy by *content* or by *position*?

    Returns a dict with, per layer and per head, the attention mass on the
    content target and on the period target, plus the model-level logit
    difference between the two candidate answers at the last position.

    Reading the result:

    * ``content_mass >> period_mass`` — the head follows the previous
      occurrence of the *same token*: this is the induction mechanism.
    * ``period_mass >> content_mass`` — the head follows the fixed offset:
      this is positional copying, which solves the same training task and is
      **not** the induction mechanism, however well it scores in-distribution.
    * neither — no copy circuit was found on this batch.
    """
    if batch is None:
        batch = make_dissociation_batch(
            vocab_size=vocab_size,
            seq_len=seq_len,
            num_samples=num_samples,
            seed=seed,
        )

    device = model_device(model)
    x = batch["x"].to(device)
    content_key = batch["content_key"].to(device)
    period_key = batch["period_key"].to(device)

    patterns = attention_patterns_for_inputs(model, x)
    content_mass: list[list[float]] = []
    period_mass: list[list[float]] = []

    for probs in patterns:
        probs = probs.detach().cpu()
        c_triples: list[tuple[int, int, int]] = []
        p_triples: list[tuple[int, int, int]] = []
        keys_c = content_key.detach().cpu().numpy()
        keys_p = period_key.detach().cpu().numpy()
        for b in range(keys_c.shape[0]):
            for q in range(keys_c.shape[1]):
                if keys_c[b, q] < 0:
                    continue
                c_triples.append((b, q, int(keys_c[b, q])))
                p_triples.append((b, q, int(keys_p[b, q])))
        content_mass.append(
            _mean_mass(probs, np.asarray(c_triples, dtype=np.int64)).tolist()
        )
        period_mass.append(
            _mean_mass(probs, np.asarray(p_triples, dtype=np.int64)).tolist()
        )

    # Behavioural readout: at the last *input* position, does the model
    # predict the content answer or the period answer? The answer arrays are
    # indexed by token position, so the last input position is one before
    # their last column (the final token is the target, not an input).
    logits = model_logits(model, x)
    last = logits[:, -1, :]
    answer_index = max(batch["content_answer"].shape[1] - 2, 0)
    content_answer = batch["content_answer"].to(device)[:, answer_index]
    period_answer = batch["period_answer"].to(device)[:, answer_index]
    valid = (content_answer >= 0) & (period_answer >= 0)
    if bool(valid.any()):
        idx = torch.arange(last.shape[0], device=device)
        diffs = last[idx, content_answer.clamp(min=0)] - last[idx, period_answer.clamp(min=0)]
        diffs = diffs[valid]
        logit_diff = float(diffs.mean().item())
        content_preferred = float((diffs > 0).float().mean().item())
    else:
        logit_diff = 0.0
        content_preferred = 0.0

    best_content = max((max(v) for v in content_mass), default=0.0)
    best_period = max((max(v) for v in period_mass), default=0.0)
    return {
        "content_mass": content_mass,
        "period_mass": period_mass,
        "peak_content_mass": float(best_content),
        "peak_period_mass": float(best_period),
        "content_wins": bool(best_content > best_period),
        "logit_diff_content_minus_period": logit_diff,
        "content_preferred_fraction": content_preferred,
    }
