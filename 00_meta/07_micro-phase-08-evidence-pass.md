---
tags: [type/moc, phase/6, phase/7, research/experiment, state/review]
created: 2026-08-02
---

# Micro-Phase 8 — The Evidence Pass

A learning-log entry meant to stand on its own: what I set out to do, what I predicted,
what actually happened, and where I was wrong. Written so someone can read this end to end
without opening `src/` and still understand what changed and why it matters.

## Where this started

The 2026-08-01 Validity Pass fixed *what my code measures* — three causal claims in the
induction-heads and circuit-patching rungs were quietly measuring the wrong tensor or the
wrong metric. That pass ended with correct instruments and an unusual problem: the code was
now trustworthy and **almost nothing had been measured with it**. Rung 2 (grokking, the
primary flagship) had never run. Rungs 1 and 4 had no numbers confirmed since the fix. Rung
3 had never reproduced at all. My own reproducibility checklist claimed "results reported
as mean ± std over ≥3 seeds" while zero experiments in the repository had ever run more
than one seed.

I framed this micro-phase around one question: **turn correct-but-unmeasured code into real
evidence, with enough statistical discipline that the numbers survive being quoted.**

## What I found, in the order I found it

### 1. Rung 3's two-year-old open question had a five-minute answer

The superposition sweep had shown flat, near-zero "recovery" at every sparsity level since
2026-07-26. The 2026-08-01 pass tried the most obvious fix — tie the decoder weights to the
encoder's transpose, matching the paper's actual setup — and it changed nothing measurable
(0.100 → 0.100). I sat with that null result rather than moving on, and read the dataset
generator and the model shapes side by side instead of re-running anything.

The bug wasn't in the weights. It was in the *shapes*. My dataset generated 20 sparse
ground-truth features, then **compressed them into 5 dimensions itself**, using its own
random projection — before the model ever saw a sample. The model then "autoencoded" that
already-compressed 5-dimensional vector through a *wider*, 20-dimensional latent. That's an
expansion, not a compression. There was no bottleneck for superposition to be a solution
*to*. I confirmed this with a quick side-by-side diagnostic (the buggy shape vs. the
canonical one) before touching any committed code, and the tell was unambiguous: the buggy
version's MSE hit exactly `0.000000` — a genuinely lossy compression cannot do that on data
it must actively choose to drop features from.

I rewrote the experiment to the canonical shape: the model itself compresses
`n_features → n_dimensions` (enforced by construction — the class now raises if you get the
order backwards), with a decoder bias, and metrics computed straight from the encoder with
no invented "ground truth direction" to compare against. **The phase transition showed up
on the first run**: 10 of 20 features represented at the densest setting, rising to 20 of 20
by sparsity 0.05, holding through 0.002. No tuning. That's what it looks like when the bug
really was the bug.

What I'd flag to a reader who wants the lesson, not just the result: I had a hypothesis
(untied weights) and tested it directly, got a clean negative, and *then* moved to
questioning the architecture instead of the parameters. The negative result was more useful
than a positive one would have been at that point — it ruled out an entire category of
explanation and pointed me toward the right one.

### 2. The induction-heads task was never well-posed, and I'd run it dozens of times

Separately, I checked something I had never explicitly verified: does the repeated-token
generator's prefix actually have unique tokens? An induction head's whole job is "attend to
the position after the *previous* occurrence of the current token" — if a token repeats
inside the prefix itself, that's ambiguous, and no amount of training fixes an ambiguous
task.

This is the birthday problem. At the vocabulary size and prefix length this repository had
used since the induction-heads rung was written, the probability of at least one repeated
token in the prefix was **over 99.99%**. Not "sometimes an edge case" — the task was
ill-posed at nearly every position, at every scale I had ever run this experiment,
including every number currently sitting in `portfolio/RESULTS.md` predating this pass.

Fixing the vocabulary size (32 → 2048 standard, 16 → 256 quick) brings the collision
probability down to a defensible ~20-23%. I want to be honest about what fixing this did
and didn't do: re-running quick scale under the corrected vocabulary produced **zero**
induction heads, same as before. The task-design bug was real and worth fixing on
correctness grounds — but it was not, on its own, why induction heads hadn't formed.

### 3. A second question, and a much bigger effect than I expected

The repeated-token dataset was generated once and reused, reshuffled, across every training
epoch. Olsson et al.'s original setup resamples continuously. I built `--fresh-batches` to
turn that difference into an ablation instead of an unexamined assumption, and ran a
*matched* 800-epoch comparison — identical hyperparameters, the only thing different is
whether the training data is fixed or resampled every epoch.

The result was more dramatic than I predicted. I expected fresh batches to modestly help
generalization. Instead: the fixed-dataset condition **actively regressed** — validation
accuracy decayed to 0.05%, *below* random chance, while validation loss climbed
monotonically to 24.3 as the model perfected its memorization of 1024 specific sequences.
The fresh-batches condition stabilized at **52.2%** validation accuracy with essentially no
gap between train and validation loss at all (expected — there's no "unseen" data when
every batch is new). Neither condition crossed the 0.3 threshold for a detected induction
head within this budget, but the trajectories tell different stories: the fixed condition's
signal peaked early and decayed; the fresh-batches signal was still climbing at epoch 800.

I did not expect the *sign* of the fixed-dataset effect to be negative rather than merely
insufficient. Reusing the dataset didn't just fail to help — it actively taught the model
the wrong thing, fast, and that got worse the longer training ran.

### 4. Building the harness this repository's own checklist had claimed existed

`checklists/reproducibility-checklist.md` had, at some point, been checked off: "Results
reported as mean ± std over ≥3 seeds." Zero experiments in `src/` had ever run more than
one seed. This is exactly the failure mode the skill tree's own top rule warns against — a
checked box without proof.

I built `src/experiments/runner.py` (a small, generic seed-loop-and-aggregate function) and
`src/results.py` (`ResultsManifest` — git SHA, dirty flag, environment, per-seed metrics,
aggregate statistics — plus `verify_claims()`, wired to `make verify-claims`). The part I
think matters most isn't the manifest format; it's that `verify-claims` is a *mechanical*
check, not a promise. I ran it against `RESULTS.md` before adding any manifest tags and it
correctly reported two problems (no manifests, no tags) — proof the checker isn't a no-op
that passes trivially. After wiring `--seeds` into three experiments and adding the tags,
it correctly reports that every manifest was recorded against a **dirty** working tree
(true — nothing in this pass is committed yet), which is exactly the state it should catch:
a result that can't be tied to a specific commit shouldn't silently back a claim about "the
code as of commit X."

### 5. The SAE upgrade, and resisting the urge to call it a win

I added `--activations-from`, which harvests genuine residual-stream activations from a
trained checkpoint via a hook on `ln_final`, instead of only ever training the SAE on
synthetic data. I also found and fixed a smaller, quieter bug while I was in that file: the
SAE had no decoder bias at all, despite Bricken et al.'s actual architecture requiring one
— `x' = ReLU(W(x - b_dec)) ...`. Without it, any constant offset in the activations has to
be reconstructed entirely through the sparse latent, competing with the sparsity penalty
for capacity that isn't doing anything interpretable.

The first real run reconstructed *better* than the synthetic baseline — 99.97% variance
explained versus 97.2% — and I want to be honest that my first reaction was to read that as
a clean win. It isn't, on its own. The real-activation SAE fires on 53% of its dictionary
per input; the synthetic baseline fires on 17%. That's not what a good sparse-features
result looks like — it looks like a wide, dense linear autoencoder that happens to
reconstruct well because a 32-dimensional residual stream from a small, undertrained model
(no confirmed induction head yet) may just not contain much genuinely sparse structure for
the SAE to find. The honest framing is in `portfolio/RESULTS.md`'s Rung 5 section, and the
obvious next step — re-run this once Rung 1 has a checkpoint with a confirmed head — is
recorded as open, not done.

## What this pass produced, concretely

- Rung 3: root cause found, architecture rewritten, phase transition reproduces cleanly,
  4 falsification tests that fail against the old code.
- Rung 1: a real, quantified task-design bug fixed, and a real, quantified memorization
  effect isolated via a matched ablation — both honestly reported as insufficient (so far)
  to produce a detected induction head.
- Rung 4: re-confirmed consistent with Rung 1 at matched scale (0 heads, 3/3 seeds); path
  patching's end-to-end validation against a real head remains the one thing still blocked
  on Rung 1 forming a head.
- Rung 5: real-activation harvesting shipped, a real architectural bug fixed (missing
  decoder bias), and an honest, unresolved gap reported rather than papered over.
- A multi-seed + provenance harness that didn't exist before this pass, covering 3 of 5
  rungs, with a mechanical checker (`make verify-claims`) that has already proven it
  catches drift rather than rubber-stamping it.
- 110 → 158 passing tests; CI's Python version now matches the lockfile; a paper scaffold
  with structure but (deliberately) no prose yet.

## What's still open

The P=113 grokking run is still the single most important item in this repository — the
code and the notebook are ready, the run itself needs a GPU I don't have in this
environment. Whether a real induction head forms at standard scale with fresh-batches
training is the natural next experiment, strongly suggested but not yet confirmed by the
fixed-vs-fresh comparison here. And `portfolio/paper/`'s sections stay `% TODO` until there
is evidence to write them from — that ordering is deliberate, not an oversight.

## Links
- [[portfolio/RESULTS]] — the full per-rung numbers and Honesty Ledger this note summarizes
- [[05_llm_engineering/proofs/superposition-setup-validity]]
- [[04_nlp_and_transformers/notes/induction-heads]]
- [[06_production_ai/notes/results-manifests-and-provenance]]
- [[06_production_ai/notes/multi-seed-experiment-design]]
- [[00_meta/03_progress-log]]
