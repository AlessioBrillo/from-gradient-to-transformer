#!/usr/bin/env python3
"""Rung 7 — the hand-written instrumentation on GPT-2 small (ADR-0034).

Five stages, each reported PASS or FAIL against thresholds frozen in
`docs/adr/0034-gpt2-small-real-model-test.md` before this module was written.
Stage 1 (parity with the Hugging Face reference) gates the rest. Stages 6 to 8
(`--adr0035`: mean ablation and the direct path of each head) are frozen in
`docs/adr/0035-gpt2-mean-ablation-and-direct-path-patching.md`.

Usage (needs the optional `real` extra and a network on the first run):

    uv run --extra real python -m src.experiments.exp7_gpt2_small
    uv run --extra real python -m src.experiments.exp7_gpt2_small --adr0035

Writes `results/gpt2_small_stage<N>.json`, one `ResultsManifest` per stage. The second
form re-runs only the stage 1 gate and writes stages 6 to 8, leaving 1 to 5 untouched.
"""

from __future__ import annotations

import argparse
import logging
import time
from collections.abc import Iterator
from pathlib import Path
from typing import Any, cast

import numpy as np
import torch
from torch.nn.functional import cross_entropy

from src.experiments.induction_detection import attention_patterns_for_inputs, head_masses
from src.experiments.runner import aggregate_metrics
from src.models.gpt2 import GPT2, GPT2Block
from src.reproducibility import set_seed
from src.results import ResultsManifest, count_parameters

logger = logging.getLogger(__name__)

# --- Frozen by ADR-0034 (do not tune after seeing a result) -----------------------------
MODEL_NAME = "openai-community/gpt2"
SEEDS = (0, 1, 2)
PARITY_TOL = 1e-5  # scale-normalised, see the ADR's amendment
PREFIX_LEN = 50
N_SEQUENCES = 100
MAX_TOKEN_ID = 50256  # exclusive: the end-of-text id is excluded
MASS_THRESHOLD = 0.3
TOP_K = 10
ICL_GAIN_DROP = 0.10
IOI_MIN_MEAN = 2.0
IOI_MIN_POSITIVE = 0.9
NAME_MOVER_DROP = 0.30
N_CONTROL_TRIPLES = 20
CONTROL_SEED = 1234
INDUCTION_HEADS: tuple[tuple[int, int], ...] = ((5, 5), (6, 9))
NAME_MOVERS: tuple[tuple[int, int], ...] = ((9, 6), (9, 9), (10, 0))

# --- Frozen by ADR-0035 (stages 6 to 8; do not tune after seeing a result) --------------
REFERENCE_SEEDS = (100, 101, 102)  # the mean-ablation reference set, disjoint from SEEDS
N_CONTROL_PAIRS = 20
NEGATIVE_NAME_MOVERS: tuple[tuple[int, int], ...] = ((10, 7), (11, 10))

STAGE1_PROMPTS = (
    "The quick brown fox jumps over the lazy dog.",
    "When Mary and John went to the store, John gave a drink to",
    "def fibonacci(n):\n    if n < 2:\n        return n\n    return",
    "In 1905 Albert Einstein published four papers that changed physics.",
    "1, 2, 3, 4, 5, 6, 7, 8, 9,",
    "The capital of France is Paris, and the capital of Italy is",
    "She said: \"I can't believe it's already over!\" He laughed.",
    "import numpy as np\nx = np.zeros((3, 3))\nprint(x",
)
NAMES = (
    " John",
    " Mary",
    " James",
    " Sarah",
    " David",
    " Emily",
    " Michael",
    " Jessica",
    " Daniel",
    " Laura",
    " Peter",
    " Anna",
    " Paul",
    " Alice",
    " Tom",
    " Kate",
)
# {first}/{second} are the two names of the opening clause, {s} the repeated one.
TEMPLATES = (
    "When{first} and{second} went to the store,{s} gave a drink to",
    "Then,{first} and{second} had a long argument, and afterwards{s} said to",
    "After{first} and{second} got to the school,{s} gave a book to",
)


# --- Helpers ------------------------------------------------------------------------
def scale_error(got: torch.Tensor, ref: torch.Tensor) -> float:
    """`max|got - ref| / max(1, max|ref|)`: float32 error relative to the tensor's scale."""
    return float((got - ref).abs().max() / max(1.0, float(ref.abs().max())))


def induction_sequences(
    seed: int, n: int = N_SEQUENCES, prefix_len: int = PREFIX_LEN, max_id: int = MAX_TOKEN_ID
) -> torch.Tensor:
    """`n` sequences of a random prefix followed by the same prefix again."""
    rng = np.random.default_rng(seed)
    prefix = torch.from_numpy(rng.integers(0, max_id, size=(n, prefix_len)))
    return torch.cat([prefix, prefix], dim=1).long()


def rank_of(matrix: np.ndarray, layer: int, head: int) -> int:
    """1-based rank of one head among all heads, by descending score."""
    flat = matrix.flatten()
    # Ties count against the target: every other head with an equal or higher score ranks
    # above it, so a tie can never help a stage pass.
    return int((flat >= matrix[layer, head]).sum())


def top_heads(matrix: np.ndarray, k: int = TOP_K) -> list[tuple[int, int, float]]:
    order = np.argsort(matrix.flatten())[::-1][:k]
    return [
        (int(i // matrix.shape[1]), int(i % matrix.shape[1]), float(matrix.flatten()[i]))
        for i in order
    ]


def per_position_loss(model: GPT2, tokens: torch.Tensor) -> torch.Tensor:
    """Next-token cross entropy at positions 0..S-2, shape (B, S-1)."""
    with torch.no_grad():
        logits, _ = model(tokens)
    return cross_entropy(logits[:, :-1].transpose(1, 2), tokens[:, 1:], reduction="none")


def icl_gain(model: GPT2, tokens: torch.Tensor, prefix_len: int = PREFIX_LEN) -> float:
    """Mean loss over the first copy minus mean loss over the second.

    Position t predicts token t+1. The first copy is scored at t = 0..L-2 and the
    second at t = L..L-2+L; t = L-1 predicts the first token of the repeat, which
    nothing can predict, and is left out of both.
    """
    loss = per_position_loss(model, tokens)
    first = loss[:, : prefix_len - 1].mean()
    second = loss[:, prefix_len : 2 * prefix_len - 1].mean()
    return float(first - second)


def relative_drop(base: float, ablated: float) -> float:
    return (base - ablated) / base if base != 0 else float("nan")


# --- Stage 1: parity -----------------------------------------------------------------
def stage1(model: GPT2, reference: Any, tokenizer: Any) -> tuple[dict[str, float], str]:
    n_layers = model.cfg.n_layers
    worst_logits = worst_hidden = 0.0
    for prompt in STAGE1_PROMPTS:
        ids = tokenizer(prompt, return_tensors="pt").input_ids
        with torch.no_grad():
            ref = reference(ids, output_hidden_states=True)
            logits, cache = model(ids, cache={})
        assert cache is not None
        worst_logits = max(worst_logits, scale_error(logits, ref.logits))
        for i in range(n_layers):
            worst_hidden = max(
                worst_hidden, scale_error(cache[f"blocks.{i}.resid_pre"], ref.hidden_states[i])
            )
        worst_hidden = max(
            worst_hidden, scale_error(cache["ln_final"], ref.hidden_states[n_layers])
        )
    passed = worst_logits <= PARITY_TOL and worst_hidden <= PARITY_TOL
    metrics = {
        "max_logit_error": worst_logits,
        "max_hidden_error": worst_hidden,
        "stage1_pass": float(passed),
    }
    return (
        metrics,
        f"{len(STAGE1_PROMPTS)} fixed prompts; tolerance {PARITY_TOL:g} (scale-normalised)",
    )


# --- Stage 2 and 3: induction ---------------------------------------------------------
def induction_mass_matrix(model: GPT2, tokens: torch.Tensor) -> np.ndarray:
    """(layers, heads) matrix of attention mass on the induction key."""
    patterns: list[list[torch.Tensor]] = []
    for start in range(0, len(tokens), 25):
        batch = attention_patterns_for_inputs(model, tokens[start : start + 25])
        if not patterns:
            patterns = [[] for _ in batch]
        for layer, p in enumerate(batch):
            patterns[layer].append(p)
    merged = [torch.cat(chunks, dim=0) for chunks in patterns]
    masses = head_masses(merged, tokens, PREFIX_LEN)["induction"]
    return np.stack(masses)


def stage2_seed(model: GPT2, seed: int) -> tuple[dict[str, float], list[tuple[int, int, float]]]:
    matrix = induction_mass_matrix(model, induction_sequences(seed))
    metrics: dict[str, float] = {}
    ok = True
    for layer, head in INDUCTION_HEADS:
        mass, rank = float(matrix[layer, head]), rank_of(matrix, layer, head)
        metrics[f"mass_{layer}_{head}"] = mass
        metrics[f"rank_{layer}_{head}"] = float(rank)
        ok = ok and rank <= TOP_K and mass >= MASS_THRESHOLD
    metrics["stage2_pass"] = float(ok)
    return metrics, top_heads(matrix)


def stage3_seed(model: GPT2, seed: int, top: list[tuple[int, int, float]]) -> dict[str, float]:
    tokens = induction_sequences(seed)
    base = icl_gain(model, tokens)
    with model.ablate(INDUCTION_HEADS):
        ablated = icl_gain(model, tokens)
    # NB: this set contains the two ablated heads (stage 2 requires them to be in the top 10),
    # so it measures the size of the redundant family, not the specificity of the two.
    with model.ablate([(layer, head) for layer, head, _ in top]):
        control = icl_gain(model, tokens)
    drop = relative_drop(base, ablated)
    return {
        "icl_gain": base,
        "icl_gain_ablated": ablated,
        "icl_gain_drop": drop,
        "icl_gain_drop_top10_control": relative_drop(base, control),
        "stage3_pass": float(drop >= ICL_GAIN_DROP),
    }


# --- Stage 4 and 5: indirect object identification ------------------------------------
def single_token_names(tokenizer: Any) -> tuple[list[str], list[str]]:
    kept = [n for n in NAMES if len(tokenizer.encode(n)) == 1]
    return kept, [n for n in NAMES if n not in kept]


def ioi_groups(
    tokenizer: Any, names: list[str], seed: int, n: int = N_SEQUENCES
) -> dict[int, tuple[torch.Tensor, torch.Tensor, torch.Tensor]]:
    """Prompts grouped by template index (equal token length within a group).

    Maps a template index to `(tokens, io_ids, s_ids)`; the logit difference of a prompt
    is `logit[io] - logit[s]` at the last position. Groups come in first-seen order.
    """
    rng = np.random.default_rng(seed)
    groups: dict[int, list[tuple[str, int, int]]] = {}
    for _ in range(n):
        t = int(rng.integers(len(TEMPLATES)))
        io, s = (names[i] for i in rng.choice(len(names), size=2, replace=False))
        abba = bool(rng.integers(2))
        first, second = (io, s) if abba else (s, io)
        prompt = TEMPLATES[t].format(first=first, second=second, s=s)
        groups.setdefault(t, []).append((prompt, tokenizer.encode(io)[0], tokenizer.encode(s)[0]))
    out: dict[int, tuple[torch.Tensor, torch.Tensor, torch.Tensor]] = {}
    for t, rows in groups.items():
        ids = [tokenizer.encode(p) for p, _, _ in rows]
        assert len({len(x) for x in ids}) == 1, "prompts of one template must share a length"
        out[t] = (
            torch.tensor(ids),
            torch.tensor([r[1] for r in rows]),
            torch.tensor([r[2] for r in rows]),
        )
    return out


def ioi_batches(
    tokenizer: Any, names: list[str], seed: int, n: int = N_SEQUENCES
) -> Iterator[tuple[torch.Tensor, torch.Tensor, torch.Tensor]]:
    """`ioi_groups` without the template index (stages 4 and 5)."""
    yield from ioi_groups(tokenizer, names, seed, n).values()


def logit_differences(
    model: GPT2, batches: list[tuple[torch.Tensor, torch.Tensor, torch.Tensor]]
) -> np.ndarray:
    out = []
    with torch.no_grad():
        for tokens, io, s in batches:
            logits, _ = model(tokens)
            last = logits[:, -1]
            out.append((last.gather(1, io[:, None]) - last.gather(1, s[:, None])).squeeze(1))
    return torch.cat(out).numpy()


def control_triples() -> list[list[tuple[int, int]]]:
    """20 random triples of distinct heads, the same for every seed."""
    rng = np.random.default_rng(CONTROL_SEED)
    triples = []
    for _ in range(N_CONTROL_TRIPLES):
        picks = rng.choice(144, size=3, replace=False)
        triples.append([(int(p // 12), int(p % 12)) for p in picks])
    return triples


def stage4_5_seed(
    model: GPT2, tokenizer: Any, names: list[str], seed: int
) -> tuple[dict[str, float], dict[str, float]]:
    batches = list(ioi_batches(tokenizer, names, seed))
    base = logit_differences(model, batches)
    mean_base = float(base.mean())
    s4 = {
        "mean_logit_diff": mean_base,
        "fraction_positive": float((base > 0).mean()),
        "n_prompts": float(len(base)),
        "stage4_pass": float(mean_base >= IOI_MIN_MEAN and (base > 0).mean() >= IOI_MIN_POSITIVE),
    }
    with model.ablate(NAME_MOVERS):
        nm = relative_drop(mean_base, float(logit_differences(model, batches).mean()))
    controls = []
    for triple in control_triples():
        with model.ablate(triple):
            controls.append(
                relative_drop(mean_base, float(logit_differences(model, batches).mean()))
            )
    p95 = float(np.percentile(controls, 95))
    s5 = {
        "name_mover_drop": nm,
        "control_drop_mean": float(np.mean(controls)),
        "control_drop_p95": p95,
        "stage5_pass": float(nm >= NAME_MOVER_DROP and nm > p95),
    }
    return s4, s5


# --- Stages 6 to 8 (ADR-0035) ----------------------------------------------------------
def random_head_sets(
    size: int, exclude: tuple[tuple[int, int], ...], n_sets: int
) -> list[list[tuple[int, int]]]:
    """`n_sets` random sets of `size` distinct heads, never including `exclude`."""
    pool = [(lay, h) for lay in range(12) for h in range(12) if (lay, h) not in exclude]
    rng = np.random.default_rng(CONTROL_SEED)
    return [
        [pool[int(i)] for i in rng.choice(len(pool), size=size, replace=False)]
        for _ in range(n_sets)
    ]


def stage6_seed(
    model: GPT2, seed: int, top: list[tuple[int, int, float]], means: dict[int, torch.Tensor]
) -> dict[str, float]:
    """Mean-ablate the induction heads; controls are random pairs and the top 10 without them."""
    tokens = induction_sequences(seed)
    base = icl_gain(model, tokens)

    def drop_when_ablating(heads: list[tuple[int, int]]) -> float:
        with model.ablate_mean(heads, means):
            return relative_drop(base, icl_gain(model, tokens))

    pairs = [
        drop_when_ablating(p) for p in random_head_sets(2, INDUCTION_HEADS, N_CONTROL_PAIRS)
    ]
    top_heads_ = [(layer, head) for layer, head, _ in top]
    return {
        "icl_gain": base,
        "icl_gain_drop": drop_when_ablating(list(INDUCTION_HEADS)),
        "control_pairs_drop_mean": float(np.mean(pairs)),
        "control_pairs_drop_p95": float(np.percentile(pairs, 95)),
        "control_top10_without_pair_drop": drop_when_ablating(
            [h for h in top_heads_ if h not in INDUCTION_HEADS]
        ),
        "control_top10_drop": drop_when_ablating(top_heads_),
    }


def ioi_reference_means(
    model: GPT2, tokenizer: Any, names: list[str]
) -> dict[int, dict[int, torch.Tensor]]:
    """Per-template mean head outputs over the reference prompts (positions align per template)."""
    per_template: dict[int, list[torch.Tensor]] = {}
    for seed in REFERENCE_SEEDS:
        for t, (tokens, _, _) in ioi_groups(tokenizer, names, seed).items():
            per_template.setdefault(t, []).append(tokens)
    return {t: model.mean_head_outputs(torch.cat(rows)) for t, rows in per_template.items()}


def logit_differences_mean_ablated(
    model: GPT2,
    groups: dict[int, tuple[torch.Tensor, torch.Tensor, torch.Tensor]],
    heads: list[tuple[int, int]],
    reference: dict[int, dict[int, torch.Tensor]],
) -> np.ndarray:
    out = []
    with torch.no_grad():
        for t, (tokens, io, s) in groups.items():
            with model.ablate_mean(heads, reference[t]):
                logits, _ = model(tokens)
            last = logits[:, -1]
            out.append((last.gather(1, io[:, None]) - last.gather(1, s[:, None])).squeeze(1))
    return torch.cat(out).numpy()


def stage7_seed(
    model: GPT2,
    groups: dict[int, tuple[torch.Tensor, torch.Tensor, torch.Tensor]],
    reference: dict[int, dict[int, torch.Tensor]],
) -> dict[str, float]:
    """Mean-ablate the name movers; the control is 20 random triples of the other heads."""
    base = float(logit_differences(model, list(groups.values())).mean())

    def drop_when_ablating(heads: list[tuple[int, int]]) -> float:
        return relative_drop(
            base, float(logit_differences_mean_ablated(model, groups, heads, reference).mean())
        )

    nm = drop_when_ablating(list(NAME_MOVERS))
    controls = [
        drop_when_ablating(t) for t in random_head_sets(3, NAME_MOVERS, N_CONTROL_TRIPLES)
    ]
    p95 = float(np.percentile(controls, 95))
    return {
        "mean_logit_diff": base,
        "name_mover_drop": nm,
        "control_drop_mean": float(np.mean(controls)),
        "control_drop_p95": p95,
        "stage7_pass": float(nm >= NAME_MOVER_DROP and nm > p95),
    }


def abc_corrupt(
    tokens: torch.Tensor,
    io: torch.Tensor,
    s: torch.Tensor,
    name_ids: list[int],
    rng: np.random.Generator,
) -> torch.Tensor:
    """Replace the repeated name S of the final clause by a third name C (Wang et al.'s ABC).

    The final clause's S is the last occurrence of S in the prompt; every name is one token,
    so the corrupted prompt has the clean prompt's length.
    """
    corrupt = tokens.clone()
    for i in range(len(tokens)):
        position = int((tokens[i] == s[i]).nonzero().max())
        choices = [n for n in name_ids if n not in (int(io[i]), int(s[i]))]
        corrupt[i, position] = int(rng.choice(choices))
    return corrupt


def direct_path_logit_differences(
    model: GPT2, clean: torch.Tensor, corrupt: torch.Tensor, io: torch.Tensor, s: torch.Tensor
) -> tuple[torch.Tensor, torch.Tensor]:
    """Logit difference after patching the direct path of each head (one hop, ADR-0035).

    For head `h` the final residual stream of the clean run gets the difference between the
    corrupted and the clean contribution of `h` at the last position, `(z_c - z) W_O^h`;
    the final LayerNorm and the unembedding are then applied. Returns the `(layers, heads,
    batch)` patched differences and the `(batch,)` clean ones.
    """
    cfg = model.cfg
    with torch.no_grad():
        _, cache_clean = model(clean, cache={})
        _, cache_corrupt = model(corrupt, cache={})
        assert cache_clean is not None and cache_corrupt is not None
        resid = cache_clean[f"blocks.{cfg.n_layers - 1}.resid_post"][:, -1]
        direction = model.wte.weight[io] - model.wte.weight[s]  # (batch, d_model)

        def diff(r: torch.Tensor) -> torch.Tensor:
            out: torch.Tensor = (model.ln_f(r) * direction).sum(-1)
            return out

        patched = torch.empty(cfg.n_layers, cfg.n_heads, len(clean))
        for layer in range(cfg.n_layers):
            dz = (
                cache_corrupt[f"blocks.{layer}.attn.z"][:, :, -1]
                - cache_clean[f"blocks.{layer}.attn.z"][:, :, -1]
            )  # (batch, heads, d_head)
            w_o = cast(GPT2Block, model.blocks[layer]).attn.c_proj.weight
            w_o = w_o.view(cfg.d_model, cfg.n_heads, cfg.d_head)
            delta = torch.einsum("bhj,dhj->bhd", dz, w_o)
            for head in range(cfg.n_heads):
                patched[layer, head] = diff(resid + delta[:, head])
        return patched, diff(resid)


def stage8_seed(
    model: GPT2,
    tokenizer: Any,
    names: list[str],
    seed: int,
    groups: dict[int, tuple[torch.Tensor, torch.Tensor, torch.Tensor]],
) -> tuple[dict[str, float], list[tuple[int, int, float]]]:
    """The effect `e_h` of every head's direct path on the answer, and the name movers' ranks."""
    name_ids = [tokenizer.encode(n)[0] for n in names]
    rng = np.random.default_rng(seed)
    patched_sum = torch.zeros(model.cfg.n_layers, model.cfg.n_heads)
    clean_sum, n = torch.zeros(()), 0
    for tokens, io, s in groups.values():
        patched, clean_ld = direct_path_logit_differences(
            model, tokens, abc_corrupt(tokens, io, s, name_ids, rng), io, s
        )
        patched_sum += patched.sum(-1)
        clean_sum += clean_ld.sum()
        n += len(tokens)
    clean_mean = float(clean_sum) / n
    effect = ((clean_mean - patched_sum.numpy() / n) / clean_mean).astype(np.float64)
    metrics: dict[str, float] = {"mean_logit_diff": clean_mean}
    ok = True
    for layer, head in NAME_MOVERS:
        rank = rank_of(effect, layer, head)
        metrics[f"effect_{layer}_{head}"] = float(effect[layer, head])
        metrics[f"rank_{layer}_{head}"] = float(rank)
        ok = ok and rank <= TOP_K
    metrics["effect_name_movers_sum"] = float(sum(effect[lay, h] for lay, h in NAME_MOVERS))
    for layer, head in NEGATIVE_NAME_MOVERS:
        metrics[f"effect_{layer}_{head}"] = float(effect[layer, head])
    metrics["stage8_pass"] = float(ok)
    return metrics, top_heads(effect)


def run_adr0035(model: GPT2, tokenizer: Any, names: list[str], save: Any) -> int:
    """Stages 6 to 8, each with its own wall clock."""
    seeds: list[int] = list(SEEDS)
    clocks = {6: 0.0, 7: 0.0, 8: 0.0}
    rows6, rows7, rows8, tops8 = [], [], [], []
    t = time.monotonic()
    induction_means = model.mean_head_outputs(
        torch.cat([induction_sequences(s) for s in REFERENCE_SEEDS])
    )
    ioi_means = ioi_reference_means(model, tokenizer, names)
    setup = time.monotonic() - t
    for seed in seeds:
        set_seed(seed)
        t = time.monotonic()
        _, top = stage2_seed(model, seed)
        rows6.append(stage6_seed(model, seed, top, induction_means))
        clocks[6] += time.monotonic() - t
        groups = ioi_groups(tokenizer, names, seed)
        t = time.monotonic()
        rows7.append(stage7_seed(model, groups, ioi_means))
        clocks[7] += time.monotonic() - t
        t = time.monotonic()
        m8, top8 = stage8_seed(model, tokenizer, names, seed, groups)
        rows8.append(m8)
        ranked = ", ".join(f"{a}.{b}={v:.3f}" for a, b, v in top8)
        tops8.append(f"seed {seed} top-{TOP_K}: {ranked}")
        clocks[8] += time.monotonic() - t
        logger.info(f"seed {seed}: {rows6[-1]} {rows7[-1]} {m8}")
    # Stage 6 is judged on the seed average (ADR-0035), so every row carries the same verdict.
    drop = float(np.mean([r["icl_gain_drop"] for r in rows6]))
    p95 = float(np.mean([r["control_pairs_drop_p95"] for r in rows6]))
    for r in rows6:
        r["stage6_pass"] = float(drop >= ICL_GAIN_DROP and drop > p95)
    note = f"mean over reference seeds {REFERENCE_SEEDS}; setup {setup:.0f}s not counted below."
    save(6, seeds, rows6, f"{note} Judged on the seed average.", clocks[6], adr="0035")
    save(7, seeds, rows7, f"{note} PASS needs every seed to pass.", clocks[7], adr="0035")
    save(8, seeds, rows8, " | ".join(tops8), clocks[8], adr="0035")
    return 0


# --- Driver ---------------------------------------------------------------------------
def write_manifest(
    stage: int,
    seeds: list[int],
    rows: list[dict[str, float]],
    notes: str,
    model: GPT2,
    wall: float,
    extra_args: dict[str, Any],
) -> Path:
    manifest = ResultsManifest.from_run(
        experiment=f"gpt2_small_stage{stage}",
        seeds=seeds,
        args={"model": MODEL_NAME, "adr": "0034", "stage": stage, **extra_args},
        per_seed_metrics=rows,
        aggregate=aggregate_metrics(rows),
        wall_clock_seconds=wall,
        device=str(next(model.parameters()).device),
        n_parameters=count_parameters(model),
        notes=notes,
    )
    path = Path("results") / f"gpt2_small_stage{stage}.json"
    manifest.save(path)
    logger.info(f"wrote {path}")
    return path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", default=MODEL_NAME)
    parser.add_argument("--dry-run", action="store_true", help="run, but write no manifest")
    parser.add_argument(
        "--adr0035",
        action="store_true",
        help="run stages 6 to 8 only (ADR-0035); stages 1 to 5 stay as recorded",
    )
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(message)s")

    from transformers import GPT2LMHeadModel, GPT2TokenizerFast  # optional `real` extra

    tokenizer = GPT2TokenizerFast.from_pretrained(args.model)
    reference = GPT2LMHeadModel.from_pretrained(args.model, attn_implementation="eager").eval()
    revision = str(getattr(reference.config, "_commit_hash", None))
    model = GPT2.from_pretrained(args.model)
    torch.set_grad_enabled(False)

    def save(
        stage: int,
        seeds: list[int],
        rows: list[dict[str, float]],
        notes: str,
        wall: float,
        **extra: Any,
    ) -> None:
        if not args.dry_run:
            write_manifest(
                stage, seeds, rows, f"weights revision {revision}. {notes}", model, wall, extra
            )

    t0 = time.monotonic()
    m1, note1 = stage1(model, reference, tokenizer)
    logger.info(f"stage 1: {m1}")
    if not args.adr0035:
        save(1, [0], [m1], note1, time.monotonic() - t0)
    if not m1["stage1_pass"]:
        logger.error("stage 1 FAILED: nothing after it is reported as a result (ADR-0034)")
        return 1

    names, dropped = single_token_names(tokenizer)
    logger.info(f"names kept: {len(names)}, dropped (not one token): {dropped}")
    if args.adr0035:
        return run_adr0035(model, tokenizer, names, save)
    rows2, rows3, rows4, rows5, tops = [], [], [], [], []
    t0 = time.monotonic()
    for seed in SEEDS:
        set_seed(seed)
        m2, top = stage2_seed(model, seed)
        rows2.append(m2)
        tops.append(f"seed {seed} top-{TOP_K}: " + ", ".join(f"{l}.{h}={v:.2f}" for l, h, v in top))
        rows3.append(stage3_seed(model, seed, top))
        m4, m5 = stage4_5_seed(model, tokenizer, names, seed)
        rows4.append(m4)
        rows5.append(m5)
        logger.info(f"seed {seed}: {m2} {rows3[-1]} {m4} {m5}")
    wall = time.monotonic() - t0
    seeds: list[int] = list(SEEDS)
    save(2, seeds, rows2, " | ".join(tops), wall)
    save(3, seeds, rows3, "zero-ablation of 5.5 and 6.9; control is the stage-2 top-10", wall)
    save(4, seeds, rows4, f"names dropped (not one token): {dropped}", wall)
    save(
        5, seeds, rows5, f"{N_CONTROL_TRIPLES} control triples, generator seed {CONTROL_SEED}", wall
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
