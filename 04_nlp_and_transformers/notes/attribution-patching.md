---
title: "Attribution Patching (AtP)"
tags: [type/lesson, phase/4, state/consolidated]
created: 2026-10-11
---

# Attribution Patching (AtP)

## What it is

A gradient-based approximation of activation patching (Syed et al., 2024). Where
activation patching *runs* a second forward pass for every patched site,
attribution patching differentiates the target logit with respect to the
corrupted activation and uses that gradient as the attribution — one backward
pass instead of N forward passes.

## Why it exists

Full activation patching costs `O(number of sites)` forward passes. On a 4-layer,
8-head model with 128 positions that is thousands of interventions, and
attribution patching trades most of that compute for one backward pass. It is
the standard way to get a *ranking* of edges cheaply before spending compute on
the exact ones.

## How it relates to what this repo does

Three interventions, increasing in cost and decreasing in approximation:

| Method | What it perturbs | Cost | Where it lives here |
|---|---|---|---|
| Activation patching | residual-stream at a `(layer, position)` | `O(sites)` forwards | `src/experiments/exp4_circuit_patching.py::run_activation_patching` |
| Path patching | a head→head edge through `W_O` | `O(edges)` forwards | `run_path_patching_to_logits` |
| **Attribution patching** | the gradient *at* the site | 1 backward | **not implemented** |

Attribution patching's approximation is additive: it assumes the logit changes
linearly in the activation delta. That assumption is defensible for small
interventions and breaks when the patched quantity is far from its clean value —
which is precisely the case when a circuit has not stabilised.

## Honest status in this repo

**Not implemented, and the checklist item is aspirational.**
`04_nlp_and_transformers/checklist.md` lists attribution patching under Phase 4;
the roadmap (`00_meta/01_roadmap.md`) marks the phase complete on the strength of
activat**ion** patching. The gap is recorded rather than papered over:

1. **There is no confirmed circuit to attribute to.** No induction head has been
   detected in this repository at any scale (0/8 heads; see
   [[06_production_ai/notes/grokking-verdict-p113]] for the parallel admission on
   Rung 2). Attribution patching ranks edges *within* a working circuit; with no
   head there is nothing to rank.
2. **A ranking without a working circuit is exactly the failure mode this repo
   exists to avoid.** `exp6_automated_circuit.py` was deleted on 2026-08-01 for
   reporting drawn-from-a-distribution numbers as "faithfulness"; a plausible
   ranking computed on a degenerated model is the same error in a subtler form.

## What implementing it would take

In `src/experiments/exp4_circuit_patching.py`, alongside the existing patchers:

```python
def run_attribution_patching(
    model,
    clean_inputs, clean_answers,
    corrupted_inputs, corrupted_answers,
    layers_to_patch, positions_to_patch,
):
    """d(logit_diff) / d(resid_mid) at each (layer, position), no second forward.

    Requires the corrupted activations to be *close* to the clean ones for the
    first-order approximation to hold — assert that, do not assume it.
    """
```

Concretely:

1. Run the corrupted forward once, keeping `resid_pre` at each block (the
   existing hook cache already stores it).
2. `logit_diff = logit[clean_answer] - logit[counterfactual_answer]`, then
   `logit_diff.backward()` with the corrupted activations requiring grad.
3. The gradient at each site is the attribution score.
4. **Validate against `run_activation_patching` on the same sites.** Attribution
   patching is only meaningful if it ranks the sites that exact patching moves.
   Without that cross-check the scores are unverified numbers — and this repo has
   already shipped unverified numbers four times (see the Honesty Ledger in
   [[portfolio/RESULTS]]).

Steps 1–3 are a day's work; step 4 is the part that makes it science rather
than a plausible-looking heatmap.

## Links

- [[04_nlp_and_transformers/notes/activation-patching]] — the exact intervention this approximates
- [[04_nlp_and_transformers/notes/path-patching]] — the head-level edge version
- [[04_nlp_and_transformers/proofs/intervention-validity]] — what makes any of these interventions mean anything
- [[05_llm_engineering/proofs/intervention-validity]] — the Phase 5 companion proof
- [[portfolio/RESULTS]] — the ledger of audited claims, including the ACDC descope

## Open questions

- #question At what intervention size does attribution patching's ranking diverge from exact patching's, on this model family?
