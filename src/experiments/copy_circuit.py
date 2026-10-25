"""Circuit-level measurement of the copy mechanism.

Why this module exists
----------------------
The detector in `induction_detection.py` measures **one head at a time**:
how much attention mass does *this* head put on the content key? That is the
right question for a circuit made of a single head, and the wrong question
for a circuit made of several. A copy distributed over ``k`` heads puts
roughly ``1/k`` of the mass on the key in each of them: every one of them
falls below the per-head screen (0.30) while the *sum* is large — and the
model copies by content all the same.

The 2026-10-22 CPU de-risk is exactly that case: the *behaviour* is
content-based (copy accuracy 0.53 against a 0.21 fixed-offset ceiling) while
the best single head holds 0.146 of the content mass, under the 0.30 screen.
The pre-registration says the *distribution over the heads* is the first
thing to measure when that happens; this module is that measurement, and it
is **secondary** — it characterises the mechanism, it does not decide the
pre-registered verdict (see `src/experiments/content_verdict.py`).

Three numbers, in increasing strength
--------------------------------------
1. `mass_summary` — the **aggregate** attention mass: how much mass the
   whole circuit puts on the content key, how concentrated it is (the top
   head's share, and how many heads cover 80% of it), and how it compares
   with the best fixed offset. Cheap, descriptive, and the statistic the
   per-head screen gets wrong.
2. `content_vs_position_attribution` — the **first-order logit attribution**
   of every head to the contrast that actually matters: the content answer
   against the token a fixed-offset head would have copied. This is the
   measurement that says *which head decides the answer*, and it keeps
   working when the decision is shared.
3. The **group ablation** (`exp1_induction_heads.causal_ablation_group`) —
   the causal version: ablate the whole candidate group at once and measure
   the drop in copy accuracy. A large group drop with small single-head
   drops is the signature of a distributed circuit.

The selection rule is fixed **before** any run and never depends on the
outcome: a head is a *candidate* when its content mass is at least
`CHANCE_FACTOR` times the chance level, and the chance level is computed
from the data (what a uniform head would put on that key), never from the
model.
"""

from __future__ import annotations

import inspect
import logging
from typing import Any, Optional, cast

import numpy as np
import torch
from torch import nn

from src.experiments.induction_detection import DetectionReport
from src.experiments.induction_tasks import copy_queries

logger = logging.getLogger(__name__)


# How many times the chance level a head's content mass has to reach before
# the head enters the candidate group. Fixed before the GPU run (see the
# pre-registration's 2026-10-22 addendum); 3x is the smallest multiple that
# keeps a uniform head out of the group at the standard geometry.
CHANCE_FACTOR = 3.0

# The mechanism codes, as they travel in a manifest (the per-seed metrics of
# a manifest are floats, so the label travels as a number and the label
# itself is decoded by `classify_mechanism`).
MECHANISM_NONE = 0
MECHANISM_SINGLE = 1
MECHANISM_DISTRIBUTED = 2
MECHANISM_UNDETERMINED = 3

MECHANISM_LABELS: dict[int, str] = {
    MECHANISM_NONE: "no content circuit",
    MECHANISM_SINGLE: "content copy, single head",
    MECHANISM_DISTRIBUTED: "content copy, distributed over heads",
    MECHANISM_UNDETERMINED: "undetermined",
}

# The thresholds of the secondary classification. They are pre-registered,
# and they are deliberately *stricter* than the primary screen: the primary
# verdict stays the seven frozen criteria, and this one only describes what
# the circuit looks like when the primary one is in trouble.
DISTRIBUTED_GROUP_DROP = 0.20
DISTRIBUTED_MAX_SINGLE_DROP = 0.10
SINGLE_HEAD_DROP = 0.20
NO_CIRCUIT_GROUP_DROP = 0.05


# ---------------------------------------------------------------------------
# The geometry
# ---------------------------------------------------------------------------
def content_triples(tokens: torch.Tensor) -> np.ndarray:
    """The ``(N, 3)`` triples ``(batch, query, content_key)`` of the copy
    queries, derived from the tokens alone.

    Same rule as the detector's layout (`induction_detection.build_copy_layout`
    on the variable-distance task): the content key of a query ``q`` is
    ``prev(q) + 1``, the position holding the token to copy.
    """
    arr = tokens.detach().cpu().numpy()
    if arr.ndim == 1:
        arr = arr[None, :]
    geom = copy_queries(arr)
    mask = geom["mask"]
    b_idx, q_idx = np.nonzero(mask)
    keys = geom["content_key"][b_idx, q_idx]
    keep = keys >= 0
    return np.stack([b_idx[keep], q_idx[keep], keys[keep]], axis=1).astype(np.int64)


def chance_content_mass(triples: np.ndarray) -> float:
    """The attention mass a *uniform* head would put on the content key.

    The chance level of attending to one specific key at query ``q`` is
    ``1 / (q + 1)`` — the key is one of the ``q + 1`` positions the causal
    mask allows (positions ``0 .. q``). Averaged over the queries, this is
    the bar a head has to clear to be more than noise, and it is a property
    of the *data*, so the candidate rule cannot be tuned on the outcome.
    """
    if triples.size == 0:
        return 0.0
    qs = triples[:, 1].astype(np.float64)
    return float(np.mean(1.0 / (qs + 1.0)))


# ---------------------------------------------------------------------------
# The aggregate mass
# ---------------------------------------------------------------------------
def mass_summary(report: DetectionReport, triples: np.ndarray) -> dict[str, float]:
    """The circuit's aggregate attention mass on the content key.

    Returns:

    * ``content_mass_total`` — the mass summed over every head of every
      layer. This is the number the per-head screen cannot see.
    * ``content_mass_top_share`` — the top head's share of that total
      (1.0 = one head does all of it).
    * ``content_mass_heads_for_80pct`` — how many heads cover 80% of the
      total, i.e. how wide the circuit is.
    * ``offset_mass_total`` — the same sum for the *best fixed offset*
      (the offset with the most mass, summed over the heads), which is the
      positional explanation's ceiling on the same queries.
    * ``offset_best_offset`` — that offset ``d``.
    * ``content_chance_mass`` — the chance level, for reference.
    """
    per_head: list[tuple[int, int, float]] = []
    for layer_idx, masses in enumerate(report.masses.get("content", [])):
        for head_idx, value in enumerate(masses):
            per_head.append((layer_idx, head_idx, float(value)))
    total = float(sum(v for _, _, v in per_head))
    n_heads = len(per_head)

    top_share = 0.0
    heads_for_80 = 0
    if per_head:
        ordered = sorted((v for _, _, v in per_head), reverse=True)
        top_share = float(ordered[0] / total) if total > 0 else 0.0
        running = 0.0
        target = 0.8 * total
        for value in ordered:
            running += value
            heads_for_80 += 1
            if running >= target:
                break

    offset_total, offset_best = _best_offset_total(report)
    chance = chance_content_mass(triples)
    chance_total = n_heads * chance
    return {
        "content_mass_total": total,
        "content_mass_top_share": top_share,
        "content_mass_heads_for_80pct": float(heads_for_80),
        "offset_mass_total": float(offset_total),
        "offset_best_offset": float(offset_best),
        "content_chance_mass": chance,
        "content_mass_excess": float(total - chance_total),
        "content_mass_ratio": float(total / chance_total) if chance_total > 0 else 0.0,
    }


def _best_offset_total(report: DetectionReport) -> tuple[float, int]:
    """The fixed offset with the most mass, summed over the heads.

    The offset profile is measured on the *same* queries as the content
    mass (the detector's layout), so the two numbers are comparable.
    """
    if not report.offsets:
        return 0.0, -1
    summed: Optional[np.ndarray] = None
    for layer in report.offsets:
        if not layer.size:
            continue
        per_offset = layer.sum(axis=0)
        summed = per_offset if summed is None else summed + per_offset
    if summed is None or not summed.size:
        return 0.0, -1
    best = int(np.argmax(summed))
    return float(summed[best]), best + 1


def candidate_heads(
    report: DetectionReport,
    triples: np.ndarray,
    factor: float = CHANCE_FACTOR,
) -> list[tuple[int, int]]:
    """The heads that enter the candidate group, by the pre-registered rule.

    A head is a candidate when its content mass is at least ``factor``
    times the chance level. The rule reads the model (the masses) and the
    data (the chance level), and it does not read the outcome (the copy
    accuracy, the ablation drops), so the group cannot be chosen to make a
    result look good.
    """
    chance = chance_content_mass(triples)
    if chance <= 0:
        return []
    bar = factor * chance
    out: list[tuple[int, int]] = []
    for layer_idx, masses in enumerate(report.masses.get("content", [])):
        for head_idx, value in enumerate(masses):
            if float(value) >= bar:
                out.append((layer_idx, head_idx))
    return out


def mass_covering_heads(
    report: DetectionReport,
    triples: np.ndarray,
    coverage: float = 0.8,
) -> list[tuple[int, int]]:
    """The smallest set of heads that covers ``coverage`` of the content mass.

    Ordered by descending content mass. This is an **exploratory** grouping:
    it reads the attention masses, but it is not the pre-registered candidate
    rule — that is `candidate_heads`, fixed at `CHANCE_FACTOR` times the
    chance level, and it never depends on the outcome. `mass_covering_heads`
    exists so the mechanism report can describe a distributed circuit even
    when the pre-registered rule selects few or no heads. It is explicitly
    **not used for the verdict**.
    """
    per_head: list[tuple[int, int, float]] = []
    for layer_idx, masses in enumerate(report.masses.get("content", [])):
        for head_idx, value in enumerate(masses):
            per_head.append((layer_idx, head_idx, float(value)))
    if not per_head:
        return []
    total = float(sum(v for _, _, v in per_head))
    if total <= 0:
        return []
    ordered = sorted(per_head, key=lambda t: t[2], reverse=True)
    running = 0.0
    target = coverage * total
    chosen: list[tuple[int, int]] = []
    for layer_idx, head_idx, value in ordered:
        running += value
        chosen.append((layer_idx, head_idx))
        if running >= target:
            break
    return chosen


# ---------------------------------------------------------------------------
# The first-order logit attribution
# ---------------------------------------------------------------------------
def _forward_with_cache(
    model: nn.Module, x: torch.Tensor
) -> tuple[torch.Tensor, dict[str, torch.Tensor]]:
    """``(logits, cache)`` for the attention-only family.

    The cache is the same dict the patching interventions use
    (`blocks.{i}.attn.attn_probs`, `blocks.{i}.attn.V`).
    """
    forward = getattr(model, "forward", None)
    params: tuple[str, ...] = ()
    if forward is not None:
        try:
            params = tuple(inspect.signature(forward).parameters)
        except (TypeError, ValueError):  # pragma: no cover - exotic callables
            params = ()
    if "cache" in params:
        cache: dict[str, torch.Tensor] = {}
        out = model(x, cache=cache)
        logits = out[0] if isinstance(out, tuple) else out
        return cast(torch.Tensor, logits), cache
    out = model(x, return_cache=True)
    return cast(torch.Tensor, out[0]), dict(out[1])


def _attention_only_weights(
    model: nn.Module,
) -> tuple[list[Any], torch.Tensor]:
    """The blocks and the unembedding matrix of the attention-only family.

    Raises:
        ValueError: when the model is not the attention-only family. The
            attribution is written for it because that is the model Rung 1
            trains; a model with MLPs has no single unembedding direction
            per head, and pretending otherwise would be a wrong number
            rather than a missing one.
    """
    blocks = getattr(model, "blocks", None)
    unembed = getattr(model, "unembed", None)
    if blocks is None or unembed is None:
        raise ValueError(
            "the logit attribution needs the attention-only model family "
            "(blocks with W_O and an unembed matrix)"
        )
    for block in blocks:
        if not hasattr(block, "W_O") or not hasattr(block, "d_head"):
            raise ValueError(
                "the logit attribution needs the attention-only model family "
                "(blocks with W_O and d_head)"
            )
    return list(blocks), cast(torch.Tensor, unembed.weight)


def content_vs_position_attribution(
    model: nn.Module,
    input_tokens: torch.Tensor,
    triples: np.ndarray,
    best_offset: int,
    max_queries: int = 4096,
) -> dict[str, Any]:
    """Who decides the answer: content or position, and which head?

    For every copy query ``q`` the model has to choose between two tokens:

    * the **content answer** — the token at ``prev(q) + 1``, the one a
      content-matching head copies;
    * the **positional answer** — the token at ``q - d* + 1``, the one a
      fixed-offset head with the best offset ``d*`` would copy.

    The measurement is the **first-order logit attribution** of every head
    to that contrast: a head's direct contribution to the residual stream
    (its OV output) is projected on the difference of the two unembedding
    directions. Summing the contributions over the heads gives the part of
    the content-vs-position decision the attention accounts for; the sign
    says which way the head votes, and the size says how much it decides.

    It is a *first-order* attribution: the unembedding is applied after the
    final LayerNorm, so the attribution is a linearisation of the logit
    difference around the clean residual. That is why the report also
    carries the *observed* logit difference — the two are not expected to
    match exactly, and the causal counterpart of this measurement is the
    head ablation, not this number.

    ``input_tokens`` is the model's input batch — the same tokens the
    detector's layout was built from, so the queries, the content answers
    and the positional answers all live in the same sequence.

    Returns a dict with the per-head attribution, the totals and the
    observed logit difference.
    """
    blocks, unembed_weight = _attention_only_weights(model)
    device = next(model.parameters()).device

    arr = input_tokens.detach().cpu().numpy()
    if arr.ndim == 1:
        arr = arr[None, :]
    x = torch.from_numpy(arr).to(device)

    rows = triples
    if rows.size == 0:
        return _empty_attribution()
    if len(rows) > max_queries:
        step = len(rows) // max_queries + 1
        rows = rows[::step][:max_queries]

    b_idx = rows[:, 0]
    q_idx = rows[:, 1]
    key_idx = rows[:, 2]
    pos_idx = q_idx - best_offset + 1
    in_range = (pos_idx >= 0) & (pos_idx < arr.shape[1])
    b_idx, q_idx, key_idx, pos_idx = (
        b_idx[in_range],
        q_idx[in_range],
        key_idx[in_range],
        pos_idx[in_range],
    )
    if b_idx.size == 0:
        return _empty_attribution()

    content_tokens = arr[b_idx, key_idx]
    positional_tokens = arr[b_idx, pos_idx]

    with torch.no_grad():
        logits, cache = _forward_with_cache(model, x)
        b_t = torch.from_numpy(b_idx).to(device)
        q_t = torch.from_numpy(q_idx).to(device)
        a_t = torch.from_numpy(content_tokens).to(device)
        p_t = torch.from_numpy(positional_tokens).to(device)
        direction = unembed_weight.to(device)[a_t] - unembed_weight.to(device)[p_t]

        per_head: dict[str, float] = {}
        for layer_idx, block in enumerate(blocks):
            probs = cache[f"blocks.{layer_idx}.attn.attn_probs"].to(device)
            values = cache[f"blocks.{layer_idx}.attn.V"].to(device)
            w_o = cast(torch.Tensor, block.W_O.weight)
            d_head = int(block.d_head)
            for head in range(int(block.n_heads)):
                sl = slice(head * d_head, (head + 1) * d_head)
                head_out = probs[:, head] @ values[:, head]  # (B, S, d_head)
                ov = head_out @ w_o[:, sl].T  # (B, S, d_model)
                contribution = (ov[b_t, q_t] * direction).sum(dim=-1)  # (N,)
                per_head[f"L{layer_idx}H{head}"] = float(contribution.mean().item())

        observed = (
            logits[b_t, q_t, a_t] - logits[b_t, q_t, p_t]
        ).mean().item()

    total = float(sum(per_head.values()))
    total_abs = float(sum(abs(v) for v in per_head.values()))
    top_head = ""
    top_share = 0.0
    if per_head:
        top_head = max(per_head, key=lambda k: abs(per_head[k]))
        top_share = float(abs(per_head[top_head]) / total_abs) if total_abs > 0 else 0.0
    positive = float(sum(v for v in per_head.values() if v > 0))
    positive_share = float(positive / total_abs) if total_abs > 0 else 0.0

    return {
        "dla_total": total,
        "dla_by_head": per_head,
        "dla_top_head": top_head,
        "dla_top_head_share": top_share,
        "dla_positive_share": positive_share,
        "dla_observed_logit_diff": float(observed),
        "dla_n_queries": int(b_idx.size),
    }


def _empty_attribution() -> dict[str, Any]:
    """The attribution report of a run with no usable query."""
    return {
        "dla_total": 0.0,
        "dla_by_head": {},
        "dla_top_head": "",
        "dla_top_head_share": 0.0,
        "dla_positive_share": 0.0,
        "dla_observed_logit_diff": 0.0,
        "dla_n_queries": 0,
    }


# ---------------------------------------------------------------------------
# The classification of the mechanism
# ---------------------------------------------------------------------------
def classify_mechanism(metrics: dict[str, float]) -> tuple[int, str]:
    """The secondary classification of the copy mechanism.

    It reads the *causal* numbers (the group ablation and the single-head
    ablations), because the attribution is a first-order approximation and
    the ablation is an intervention.

    * **distributed** — the group ablation costs a lot (>= 0.20 of the copy
      accuracy) while no single head does (every one of them <= 0.10): the
      copy is carried by the group, not by one head.
    * **single head** — one head alone costs at least 0.20.
    * **none** — the group costs almost nothing (<= 0.05) and the
      attribution does not favour the content: there is no content circuit
      to find.
    * **undetermined** — anything else (for instance a group that costs a
      lot *and* a head that costs a lot: a redundant circuit).

    The code travels in the manifest; the label is decoded from it, so the
    manifest never depends on this module to be read.
    """
    group = float(metrics.get("group_ablation_drop", 0.0))
    single = float(metrics.get("max_single_ablation_drop", 0.0))
    attribution = float(metrics.get("dla_content_minus_offset", 0.0))
    n_candidates = metrics.get("n_candidate_heads", None)

    # An empty candidate group means the 3x chance screen selected no head:
    # the group ablation is a no-op, so 0.0 is not a causal measurement.
    if n_candidates is not None and float(n_candidates) == 0.0:
        return MECHANISM_UNDETERMINED, (
            MECHANISM_LABELS[MECHANISM_UNDETERMINED]
            + " — no candidate passed the 3x chance screen"
        )

    if group >= DISTRIBUTED_GROUP_DROP and single <= DISTRIBUTED_MAX_SINGLE_DROP:
        code = MECHANISM_DISTRIBUTED
    elif single >= SINGLE_HEAD_DROP:
        code = MECHANISM_SINGLE
    elif group <= NO_CIRCUIT_GROUP_DROP and attribution <= 0.0:
        code = MECHANISM_NONE
    else:
        code = MECHANISM_UNDETERMINED
    return code, MECHANISM_LABELS[code]
