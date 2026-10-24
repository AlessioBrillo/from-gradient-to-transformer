"""The two induction tasks, and the geometry that makes them measurable.

Why this module exists
----------------------
Rung 1 asks for a head that implements ``[A][B]...[A] -> [B]``: at a query
position ``q`` whose token ``x[q]`` has already appeared, the model has to
find that earlier occurrence and copy the token that followed it.

Until 2026-10-20 the only task in this repository was **periodic**
(``prefix + prefix``, tiled). On that task the previous occurrence of
``x[q]`` is *always* at ``q - L``, so a head that attends to ``q - L + 1`` by
pure position arithmetic and a head that attends to "the token after the
previous occurrence of the same token" are **the same function** on the
training distribution. The 2026-10-19 audit found that the model solves the
periodic task with a fixed-offset copy, and the dissociation probe confirmed
it: the copy follows the offset, not the content. The rung's headline claim
was therefore not earned, and no amount of re-analysis of that checkpoint
could earn it — the task does not contain the question.

The **variable-distance** task added here removes the shortcut:

* the key (the source segment) holds distinct tokens;
* the copies are verbatim blocks of the key, but their *positions* and the
  *source windows* they come from are resampled per sequence, so the
  distance between a token and its previous occurrence varies from block to
  block and from sequence to sequence;
* every token appears at most twice, so "the previous occurrence" is unique
  and the task is well posed;
* the filler tokens are unpredictable, so the only learnable positions are
  the copy queries — a fixed-offset head can solve at most a small fraction
  of them (see `fixed_offset_baseline`), while a content-matching head can
  solve all of them.

The task is specified in `docs/adr/0033-content-based-induction-task.md`
and pre-registered in
`07_capstone/notes/variable-distance-induction-preregistration.md`.

Vocabulary
----------
* **key** — the source segment: `key_len` distinct tokens at the start of
  the sequence.
* **copy block** — a verbatim, contiguous slice of the key, `copy_block_len`
  tokens long, placed in the second half of the sequence.
* **copy query** — a position ``q`` whose next token is the copy of a token
  that has a previous occurrence: the position where the induction circuit
  has to fire. It is *derived from the tokens alone* (see
  `copy_queries`), so the detector never has to trust the generator.
* **distance** — ``q - prev(q)``: how far back the previous occurrence is.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any, Optional

import numpy as np
import torch
from torch.utils.data import TensorDataset

logger = logging.getLogger(__name__)

# Bumped whenever the generated data changes in a way that would invalidate a
# manifest written by an older version. It travels in the manifest's args, so
# a result can always be traced back to the generator that produced it.
GENERATOR_VERSION = "induction-tasks-v1"

TASK_PERIODIC = "periodic"
TASK_VARIABLE = "variable"


# ---------------------------------------------------------------------------
# Specification
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class TaskSpec:
    """Everything that determines the data of one task.

    ``periodic`` uses ``prefix_ratio`` (the historical ``prefix + prefix``
    layout). ``variable`` uses ``key_len`` / ``copy_blocks`` /
    ``copy_block_len``. The two parameter sets are ignored by the task that
    does not use them, so one dataclass can describe both without the
    dispatch ever reading a field that does not apply.
    """

    name: str = TASK_PERIODIC
    vocab_size: int = 2048
    seq_len: int = 64
    prefix_ratio: float = 0.5
    key_len: int = 36
    copy_blocks: int = 4
    copy_block_len: int = 5

    def __post_init__(self) -> None:
        if self.name not in (TASK_PERIODIC, TASK_VARIABLE):
            raise ValueError(
                f"unknown task {self.name!r} — expected {TASK_PERIODIC!r} "
                f"or {TASK_VARIABLE!r}"
            )
        if self.name == TASK_VARIABLE:
            self._check_variable()

    def _check_variable(self) -> None:
        if self.key_len < 2:
            raise ValueError("key_len must be at least 2")
        if self.copy_blocks < 1:
            raise ValueError("copy_blocks must be at least 1")
        if self.copy_block_len < 2:
            raise ValueError("copy_block_len must be at least 2 (a block of 1 has no copy query)")
        if self.key_len < self.copy_blocks * self.copy_block_len:
            raise ValueError(
                f"key_len ({self.key_len}) must hold the "
                f"{self.copy_blocks} disjoint source windows of "
                f"{self.copy_block_len} tokens each "
                f"({self.copy_blocks * self.copy_block_len} tokens)"
            )
        # One filler token per gap keeps every block separated from its
        # neighbours, so the token after the last element of a block is
        # unpredictable (that position is not a copy query).
        n_gaps = self.copy_blocks + 1
        filler = self.seq_len - self.key_len - self.copy_blocks * self.copy_block_len
        if filler < n_gaps:
            raise ValueError(
                f"seq_len ({self.seq_len}) is too short for key_len "
                f"({self.key_len}) + {self.copy_blocks} blocks of "
                f"{self.copy_block_len} + one filler per gap ({n_gaps}): "
                f"{self.key_len + self.copy_blocks * self.copy_block_len + n_gaps} "
                "tokens are needed"
            )
        if self.vocab_size < self.key_len + filler:
            raise ValueError(
                f"vocab_size ({self.vocab_size}) must exceed the number of "
                f"distinct tokens a sequence uses "
                f"({self.key_len + filler})"
            )

    # -- constructors ------------------------------------------------------
    @classmethod
    def periodic(
        cls,
        vocab_size: int = 2048,
        seq_len: int = 64,
        prefix_ratio: float = 0.5,
    ) -> "TaskSpec":
        """The historical ``prefix + prefix`` task, unchanged."""
        return cls(
            name=TASK_PERIODIC,
            vocab_size=vocab_size,
            seq_len=seq_len,
            prefix_ratio=prefix_ratio,
        )

    @classmethod
    def variable(
        cls,
        vocab_size: int = 2048,
        seq_len: int = 64,
        key_len: int = 36,
        copy_blocks: int = 4,
        copy_block_len: int = 5,
    ) -> "TaskSpec":
        """The content-based task, with the repeats at varying distances."""
        return cls(
            name=TASK_VARIABLE,
            vocab_size=vocab_size,
            seq_len=seq_len,
            key_len=key_len,
            copy_blocks=copy_blocks,
            copy_block_len=copy_block_len,
        )

    # -- derived quantities ------------------------------------------------
    @property
    def prefix_len(self) -> int:
        """The periodic task's prefix length (its own convention)."""
        return max(2, int(self.seq_len * self.prefix_ratio))

    @property
    def filler_total(self) -> int:
        """How many filler tokens the variable layout spends."""
        return self.seq_len - self.key_len - self.copy_blocks * self.copy_block_len

    @property
    def n_copy_queries(self) -> int:
        """Copy queries per sequence (one per block element but the last)."""
        return self.copy_blocks * (self.copy_block_len - 1)

    def to_dict(self) -> dict[str, Any]:
        """The manifest-facing description of the task."""
        out: dict[str, Any] = {
            "name": self.name,
            "vocab_size": self.vocab_size,
            "seq_len": self.seq_len,
            "generator_version": GENERATOR_VERSION,
        }
        if self.name == TASK_PERIODIC:
            out["prefix_ratio"] = self.prefix_ratio
            out["prefix_len"] = self.prefix_len
        else:
            out["key_len"] = self.key_len
            out["copy_blocks"] = self.copy_blocks
            out["copy_block_len"] = self.copy_block_len
            out["filler_total"] = self.filler_total
            out["n_copy_queries"] = self.n_copy_queries
        return out


# ---------------------------------------------------------------------------
# Token geometry (task-agnostic)
# ---------------------------------------------------------------------------
def previous_occurrences(tokens: np.ndarray) -> np.ndarray:
    """For every position, the index of the same token's previous occurrence.

    ``tokens`` is ``(B, S)``; the result is ``(B, S)`` with ``-1`` where the
    token has not appeared before. This is the one geometric fact the
    detector needs about *any* task, and it is read from the tokens rather
    than from the generator — a detector that trusted the generator could
    not detect a generator that lies.
    """
    arr = np.asarray(tokens)
    if arr.ndim == 1:
        arr = arr[None, :]
    bsz, seq = arr.shape
    prev = np.full((bsz, seq), -1, dtype=np.int64)
    for b in range(bsz):
        row = arr[b]
        last: dict[int, int] = {}
        for q in range(seq):
            token = int(row[q])
            p = last.get(token, -1)
            prev[b, q] = p
            last[token] = q
    return prev


def copy_queries(tokens: np.ndarray) -> dict[str, np.ndarray]:
    """The copy queries of a batch, derived from the tokens alone.

    A position ``q`` is a copy query when the token at ``q`` has a previous
    occurrence ``p`` **and** the token that follows ``q`` is the token that
    followed ``p`` — that is, when "copy what followed the previous
    occurrence" is the right thing to do at ``q``::

        tokens[q + 1] == tokens[p + 1]

    The condition is what makes the query set *task-agnostic*: it holds on
    the periodic task's second copy and on the variable task's blocks, and
    it fails exactly where the answer is unpredictable (the last element of
    a block, and every filler position).

    Returns a dict of ``(B, S)`` arrays: ``prev`` (the previous occurrence,
    ``-1`` if none), ``content_key`` (``prev + 1``, the position holding the
    token to copy, ``-1`` if undefined), ``distance`` (``q - prev``) and
    ``mask`` (the copy queries, as ``bool``).
    """
    arr = np.asarray(tokens)
    if arr.ndim == 1:
        arr = arr[None, :]
    bsz, seq = arr.shape
    prev = previous_occurrences(arr)
    q_idx = np.arange(seq)[None, :]
    has_prev = prev >= 0
    safe_prev = np.clip(prev, 0, seq - 1)
    content_key = np.where(has_prev, safe_prev + 1, -1)
    in_range = has_prev & (content_key < seq) & (content_key != q_idx)
    safe_key = np.clip(content_key, 0, seq - 1)
    next_token = np.take_along_axis(arr, safe_key, axis=1)
    following = np.take_along_axis(arr, np.clip(q_idx + 1, 0, seq - 1), axis=1)
    mask = in_range & (next_token == following) & (q_idx < seq - 1)
    distance = np.where(has_prev, q_idx - prev, -1)
    return {
        "prev": prev,
        "content_key": np.where(mask, content_key, -1),
        "distance": np.where(mask, distance, -1),
        "mask": mask,
    }


def copy_mask_for_pairs(x: torch.Tensor, y: torch.Tensor) -> torch.Tensor:
    """The copy-query mask of a ``(input, target)`` batch, aligned to ``x``.

    The training data is stored as ``x = tokens[:-1]``, ``y = tokens[1:]``,
    so the full sequence is ``concat(x, y[:, -1:])``. The mask has one entry
    per *input* position: entry ``q`` says "the target of position ``q`` is
    the copy of a token that has a previous occurrence".
    """
    full = torch.cat([x, y[:, -1:]], dim=1)
    geom = copy_queries(full.numpy())
    mask = torch.from_numpy(geom["mask"][:, : x.shape[1]])
    return mask


# ---------------------------------------------------------------------------
# The periodic task (unchanged, bit-for-bit)
# ---------------------------------------------------------------------------
def make_periodic_tokens(spec: TaskSpec, num_samples: int, rng: np.random.Generator) -> np.ndarray:
    """The historical ``prefix + prefix`` sequences.

    Reproduces the generator that produced every manifest in this
    repository, draw for draw: the prefix is sampled **with replacement**
    (which is why a large vocabulary is needed to keep the task well posed)
    and then tiled to fill the sequence.
    """
    prefix_len = spec.prefix_len
    out = np.zeros((num_samples, spec.seq_len), dtype=np.int64)
    for i in range(num_samples):
        prefix = rng.integers(0, spec.vocab_size, size=prefix_len).tolist()
        tokens = prefix.copy()
        while len(tokens) < spec.seq_len:
            tokens.append(tokens[len(tokens) % prefix_len])
        out[i] = np.asarray(tokens[: spec.seq_len], dtype=np.int64)
    return out


# ---------------------------------------------------------------------------
# The variable-distance task
# ---------------------------------------------------------------------------
def _sample_distinct(
    rng: np.random.Generator,
    vocab_size: int,
    count: int,
    forbidden: Optional[set[int]] = None,
) -> np.ndarray:
    """``count`` distinct token ids, none of them in ``forbidden``."""
    out: list[int] = []
    seen: set[int] = set(forbidden or ())
    while len(out) < count:
        draw = rng.integers(0, vocab_size, size=max(count - len(out), 1))
        for value in draw.tolist():
            if value not in seen:
                seen.add(value)
                out.append(value)
                if len(out) == count:
                    break
    return np.asarray(out, dtype=np.int64)


def _disjoint_window_starts(
    rng: np.random.Generator,
    key_len: int,
    n_windows: int,
    window_len: int,
) -> list[int]:
    """Start indices of ``n_windows`` disjoint windows inside the key.

    The windows are ordered and non-overlapping, but their *positions* are
    random: the first window can start anywhere in
    ``[0, key_len - n_windows * window_len]``, and each later window after
    the previous one. This is where the distance entropy comes from — the
    same block occupies a different distance in every sequence.
    """
    starts: list[int] = []
    prev_end = 0
    for i in range(n_windows):
        hi = key_len - (n_windows - i) * window_len
        s = int(rng.integers(prev_end, hi + 1))
        starts.append(s)
        prev_end = s + window_len
    return starts


def _positive_composition(
    rng: np.random.Generator, total: int, parts: int
) -> np.ndarray:
    """``parts`` positive integers summing to ``total`` (random cut points)."""
    if total < parts:
        raise ValueError(f"cannot split {total} into {parts} positive parts")
    if parts == 1:
        return np.asarray([total], dtype=np.int64)
    cuts = np.sort(rng.choice(np.arange(1, total), size=parts - 1, replace=False))
    bounds = np.concatenate(([0], cuts, [total]))
    return np.diff(bounds).astype(np.int64)


def make_variable_tokens(spec: TaskSpec, num_samples: int, seed: int) -> np.ndarray:
    """Sequences whose repeats sit at *varying* distances.

    Layout of one sequence (``key_len`` key, four blocks, filler between)::

        [ key key key ... key ][ f ][ B0 B0 B0 B0 B0 ][ f ][ B1 ... ][ f ] ...

    * the key holds ``key_len`` distinct tokens;
    * block ``i`` is a verbatim, contiguous window of the key, taken from a
      random position — the windows are disjoint, so no token is copied
      twice and every token appears at most twice;
    * the block positions are random too (the gaps between them are a
      random composition of the leftover space), so the *distance* between
      a token and its previous occurrence varies per block and per
      sequence;
    * the filler tokens are distinct, absent from the key, and
      unpredictable: the only learnable positions are the copy queries.
    """
    rng = np.random.default_rng(seed)
    out = np.zeros((num_samples, spec.seq_len), dtype=np.int64)
    for b in range(num_samples):
        out[b] = _variable_sequence(spec, rng)
    return out


def _variable_sequence(spec: TaskSpec, rng: np.random.Generator) -> np.ndarray:
    key_len = spec.key_len
    n_blocks = spec.copy_blocks
    block_len = spec.copy_block_len
    seq_len = spec.seq_len

    key = _sample_distinct(rng, spec.vocab_size, key_len)
    starts = _disjoint_window_starts(rng, key_len, n_blocks, block_len)
    gaps = _positive_composition(rng, spec.filler_total, n_blocks + 1)

    tokens = np.empty(seq_len, dtype=np.int64)
    tokens[:key_len] = key
    used = set(key.tolist())

    block_positions: list[int] = []
    pos = key_len
    for i in range(n_blocks):
        pos += int(gaps[i])
        source = key[starts[i] : starts[i] + block_len]
        tokens[pos : pos + block_len] = source
        used.update(source.tolist())
        block_positions.extend(range(pos, pos + block_len))
        pos += block_len
    pos += int(gaps[n_blocks])
    if pos != seq_len:  # pragma: no cover - guarded by TaskSpec._check_variable
        raise AssertionError(f"layout ended at {pos}, expected {seq_len}")

    occupied = np.concatenate(
        [np.arange(key_len), np.asarray(block_positions, dtype=np.int64)]
    )
    fill_positions = np.setdiff1d(np.arange(seq_len), occupied)
    filler = _sample_distinct(
        rng, spec.vocab_size, len(fill_positions), forbidden=used
    )
    tokens[fill_positions] = filler
    return tokens


# ---------------------------------------------------------------------------
# Batch / dataset plumbing
# ---------------------------------------------------------------------------
@dataclass
class TaskBatch:
    """One generated batch, with the geometry that describes it."""

    tokens: torch.Tensor
    spec: TaskSpec
    prev: torch.Tensor = field(repr=False)
    content_key: torch.Tensor = field(repr=False)
    distance: torch.Tensor = field(repr=False)
    copy_mask: torch.Tensor = field(repr=False)

    @property
    def n_copy_queries(self) -> int:
        return int(self.copy_mask.sum().item())


def make_task_batch(spec: TaskSpec, num_samples: int, seed: int) -> TaskBatch:
    """Generate a batch of the requested task, with its geometry."""
    if spec.name == TASK_PERIODIC:
        # The periodic generator has drawn from a single Generator for the
        # whole training history of this repository; keep that convention so
        # the data is identical to what the old manifests saw.
        rng = np.random.default_rng(seed)
        tokens = make_periodic_tokens(spec, num_samples, rng)
    else:
        tokens = make_variable_tokens(spec, num_samples, seed)

    geom = copy_queries(tokens)
    return TaskBatch(
        tokens=torch.from_numpy(tokens),
        spec=spec,
        prev=torch.from_numpy(geom["prev"]),
        content_key=torch.from_numpy(geom["content_key"]),
        distance=torch.from_numpy(geom["distance"]),
        copy_mask=torch.from_numpy(geom["mask"]),
    )


def task_datasets(
    spec: TaskSpec,
    num_train: int,
    num_val: int,
    seed: int,
) -> tuple[TensorDataset, TensorDataset]:
    """The ``(x, y)`` datasets of a task, as the training loop consumes them.

    The train and the validation split are drawn from **one** generator, in
    that order, exactly as the historical generator did — so the periodic
    task's data is bit-for-bit what it always was.
    """
    if spec.name == TASK_PERIODIC:
        rng = np.random.default_rng(seed)
        train_ids = make_periodic_tokens(spec, num_train, rng)
        val_ids = make_periodic_tokens(spec, num_val, rng)
    else:
        train_ids = make_variable_tokens(spec, num_train, seed)
        val_ids = make_variable_tokens(spec, num_val, seed + 1)

    train_x, train_y = train_ids[:, :-1], train_ids[:, 1:]
    val_x, val_y = val_ids[:, :-1], val_ids[:, 1:]
    return (
        TensorDataset(torch.from_numpy(train_x), torch.from_numpy(train_y)),
        TensorDataset(torch.from_numpy(val_x), torch.from_numpy(val_y)),
    )


# ---------------------------------------------------------------------------
# The shortcut audit: how far can a fixed offset get?
# ---------------------------------------------------------------------------
def fixed_offset_baseline(
    tokens: np.ndarray, copy_mask: np.ndarray
) -> dict[str, Any]:
    """The accuracy of the best *fixed-offset* predictor on the copy queries.

    A head that attends to ``q - d + 1`` for a single constant ``d`` — the
    only shortcut the periodic task allowed — predicts the token at
    ``q - d + 1``. This function measures, for every ``d``, how often that
    is the right answer on the copy queries, and reports the best ``d``.

    The result is the ceiling of the positional explanation: a model that
    copies by a fixed offset cannot beat it. The content mechanism can reach
    1.0. The gap between the two is the claim.
    """
    arr = np.asarray(tokens)
    mask = np.asarray(copy_mask, dtype=bool)[:, :-1]
    answers = arr[:, 1:]  # the true next token of every input position
    if not mask.any():
        return {
            "best_offset": -1,
            "best_accuracy": 0.0,
            "n_queries": 0,
            "accuracies": [],
        }

    q_idx = np.arange(answers.shape[1])[None, :]
    per_offset: list[float] = []
    for d in range(2, answers.shape[1] + 1):
        key_idx = q_idx - d + 1
        valid = mask & (key_idx >= 0) & (key_idx < answers.shape[1])
        if not valid.any():
            per_offset.append(0.0)
            continue
        picked = np.take_along_axis(
            answers, np.clip(key_idx, 0, answers.shape[1] - 1), axis=1
        )
        per_offset.append(float((picked[valid] == answers[valid]).mean()))
    best = int(np.argmax(per_offset)) + 2 if per_offset else -1
    best_acc = float(per_offset[best - 2]) if per_offset else 0.0
    return {
        "best_offset": best,
        "best_accuracy": best_acc,
        "n_queries": int(mask.sum()),
        "accuracies": per_offset,
    }


# ---------------------------------------------------------------------------
# The patch batch: where a causal intervention is measured
# ---------------------------------------------------------------------------
def copy_query_batch(
    x: torch.Tensor,
    y: torch.Tensor,
    vocab_size: int = 0,
) -> dict[str, Any]:
    """Two disjoint batches of sequences whose copy query sits at the *same*
    position, with their answers.

    The causal interventions of Rung 4 read one position's logits and
    compare the answer with a counterfactual. On the periodic task that
    position is the last one, and it is a copy query by construction. On
    the variable-distance task the copy queries sit at *different* positions
    in every sequence, so a fixed position would be a filler position —
    where the right answer is unpredictable and the logit difference is
    noise.

    This helper picks the position that carries the most copy queries (a
    rule about the data, not a choice about the model), keeps the sequences
    that have a copy query there, and splits them in two: the **clean**
    batch, whose answers are the model's targets, and the **corrupted**
    batch, whose answers are the counterfactuals (the same position of a
    different sequence — a token the model has no reason to predict
    there).
    """
    full = torch.cat([x, y[:, -1:]], dim=1)
    geom = copy_queries(full.numpy())
    mask = geom["mask"]
    counts = mask.sum(axis=0)
    if int(counts.max()) == 0:
        raise ValueError("no copy query found in this batch")
    pos = int(np.argmax(counts))
    selected = np.nonzero(mask[:, pos])[0]
    if len(selected) < 4:
        raise ValueError("not enough sequences share a copy-query position")

    half = len(selected) // 2
    clean_idx = selected[:half]
    corrupt_idx = selected[half:]
    answers = y[clean_idx, pos]
    counterfactuals = y[corrupt_idx[:half], pos]
    clash = counterfactuals == answers
    if bool(clash.any()) and vocab_size > 1:
        counterfactuals = torch.where(
            clash, (answers + 1) % vocab_size, counterfactuals
        )
    return {
        "clean_inputs": x[clean_idx],
        "clean_answers": answers,
        "corrupted_inputs": x[corrupt_idx[:half]],
        "corrupted_answers": counterfactuals,
        "pos": pos,
        "n_sequences": int(half),
    }


def copy_query_minimal_pair_batch(
    x: torch.Tensor,
    y: torch.Tensor,
    vocab_size: int,
    seed: int = 0,
) -> dict[str, Any]:
    """A **minimal pair**: the same sequence, with exactly one token changed.

    Why this exists
    ---------------
    `copy_query_batch` builds the corrupted half of the intervention from a
    *different* sequence: the clean batch and the corrupted batch share
    nothing but the read position. The contrast that is measured is then
    "the answer of this sequence against the answer of another sequence",
    which every mechanism has to lose — and the measurement of a circuit's
    effect is diluted by everything the two sequences differ in. That is
    why the 2026-10-20 cascade's activation-patching recovery was 0.0834:
    a number that is hard to read as "this circuit carries the answer".

    The minimal pair removes the confound. The corrupted sequence is the
    clean one with **one** token changed: the token at the *source* of the
    copy, ``prev(q) + 1`` — the position the model has to read in order to
    answer at ``q``. Everything else (the query token, the rest of the
    context, the position of the read) is byte-identical, so a model that
    answers with the source token must answer with the *new* token, and a
    model that answers with anything else must not move.

    The replacement token is chosen among the ids that do **not** appear in
    the sequence, so the corrupted sequence keeps every token unique and the
    "previous occurrence" of the query token is untouched: the read
    position stays a copy query, and only its answer changes.

    Returns the same keys as `copy_query_batch` (plus `source_positions`),
    so the two designs are interchangeable for the caller.
    """
    if vocab_size <= 0:
        raise ValueError("copy_query_minimal_pair_batch needs a vocabulary size")
    full = torch.cat([x, y[:, -1:]], dim=1)
    arr = full.numpy()
    geom = copy_queries(arr)
    mask = geom["mask"]
    counts = mask.sum(axis=0)
    if int(counts.max()) == 0:
        raise ValueError("no copy query found in this batch")
    pos = int(np.argmax(counts))
    selected = np.nonzero(mask[:, pos])[0]
    if len(selected) < 4:
        raise ValueError("not enough sequences share a copy-query position")

    rng = np.random.default_rng(seed)
    corrupted = x[selected].clone()
    answers: list[int] = []
    counterfactuals: list[int] = []
    source_positions: list[int] = []

    for row, b in enumerate(selected):
        source = int(geom["content_key"][b, pos])
        if source < 0 or source >= x.shape[1]:
            raise ValueError(
                f"the source of the copy query at {pos} is out of the input "
                f"({source}) — the minimal pair needs a source inside x"
            )
        clean_answer = int(arr[b, source])
        present = set(arr[b].tolist())
        replacement = -1
        for _ in range(64):
            candidate = int(rng.integers(0, vocab_size))
            if candidate not in present:
                replacement = candidate
                break
        if replacement < 0:
            raise ValueError(
                "no token outside the sequence to build a minimal pair with — "
                "the vocabulary is too small for this batch"
            )
        corrupted[row, source] = replacement
        answers.append(clean_answer)
        counterfactuals.append(replacement)
        source_positions.append(source)

    return {
        "clean_inputs": x[selected],
        "clean_answers": torch.tensor(answers, dtype=torch.long),
        "corrupted_inputs": corrupted,
        "corrupted_answers": torch.tensor(counterfactuals, dtype=torch.long),
        "pos": pos,
        "n_sequences": int(len(selected)),
        "source_positions": source_positions,
        "selected_indices": [int(i) for i in selected],
    }


def copy_accuracy_by_distance(
    tokens: np.ndarray,
    copy_mask: np.ndarray,
    distance: np.ndarray,
    predictions: np.ndarray,
) -> dict[str, Any]:
    """Copy-accuracy per distance group, and the accuracy on the non-modal one.

    The sharpest behavioural discriminator between "copies by content" and
    "copies by a fixed offset": a fixed-offset head is right on the queries
    that share its offset and wrong everywhere else, so its accuracy on the
    *non-modal* distance group is ~0, while a content head is right on all
    of them.

    ``predictions`` are the model's predicted next tokens, shaped like the
    inputs (``(B, S-1)``).
    """
    arr = np.asarray(tokens)
    mask = np.asarray(copy_mask, dtype=bool)[:, :-1]
    dist = np.asarray(distance)[:, :-1]
    answers = arr[:, 1:]
    preds = np.asarray(predictions)
    if preds.shape != answers.shape:
        raise ValueError(
            f"predictions {preds.shape} do not match the answers {answers.shape}"
        )
    correct = preds == answers

    groups: dict[int, float] = {}
    counts: dict[int, int] = {}
    for d in np.unique(dist[mask]):
        sel = mask & (dist == d)
        counts[int(d)] = int(sel.sum())
        groups[int(d)] = float(correct[sel].mean()) if sel.any() else 0.0

    modal = max(counts, key=lambda k: counts[k]) if counts else -1
    nonmodal_sel = mask & (dist != modal)
    nonmodal = float(correct[nonmodal_sel].mean()) if nonmodal_sel.any() else 0.0
    return {
        "accuracy_by_distance": groups,
        "counts_by_distance": counts,
        "modal_distance": modal,
        "copy_accuracy_nonmodal": nonmodal,
        "n_queries": int(mask.sum()),
        "n_distances": len(counts),
    }
