---
tags: [phase/7, research/experiment]
created: 2026-09-04
---

# MP-78 session — Capstone checkpoint crash fixed, probes reproduced dense

## Claim

Two things are true after this session: (1) the capstone runner
(`src/experiments/exp6_capstone.py`) crashed with `TypeError` on every
`--save-model` run that reached its first checkpoint step, and now it does not
— pinned by 2 regression tests; (2) fresh P=59/P=67 grokking probes reproduce
the dense-Fourier finding already in the record (MP-11, MP-78), convergently,
not as news.

## Method

TDD, RED first. I wrote `tests/test_exp6_capstone.py` with a tiny CPU-seconds
config (modulus 7, d_model 16, 1 layer, 6 steps, `checkpoint_every=2`) that
exercises the checkpoint branch, ran it, and watched it fail with the exact
production error:

```text
TypeError: save_training_checkpoint() got an unexpected keyword argument 'step'
```

Then I fixed the call site and re-ran to GREEN, followed by the full local
CI mirror (`lint`, `typecheck-new`, `test-cov`, `verify-claims`,
`commitlint-new`, `commitlint-head`).

## Evidence

### 1. The bug (real, latent, now fixed)

- `train_single_seed()` called the shared epoch-oriented helper with kwargs it
  does not accept (`step=`, `seed=`, `config=`), while the resume branch in the
  same file reads raw `torch.save` dicts (`model`/`optimizer`/`scheduler`/`step`).
- Blast radius: any `--save-model` run with `steps >= checkpoint_every` died at
  the first checkpoint step. It stayed latent because the recorded 100-step
  manifest run never set `--save-model` (`checkpoint_dir=None` skips the branch).
- Fix: save raw step checkpoints atomically (tmp + replace, per the repo's
  kill-drill durability standard) in exactly the format the resume branch reads;
  removed the now-unused import so `ruff` stays clean.
- Suite: **199 passed** (197 + 2 new), `ruff` clean, `typecheck-new` clean,
  `verify-claims` clean, both commitlint mirrors clean.

### 2. Small-P probes (convergent reproduction)

Canonical hyperparams (d_model=128, d_mlp=512, 4 heads, wd=1.0, train 30%),
1500 epochs, 3 seeds, CPU:

| P | val acc (mean ± std) | k_99 | k_90 | Fourier sparsity | Generalization epoch |
|---|----------------------|------|------|------------------|----------------------|
| 59 | 0.0010 ± 0.0005 | 59/59 | 52.3 ± 0.5 | 0.0015 ± 0.0002 | never (-1) |
| 67 | 0.0011 ± 0.0009 | 67/67 | 60.0 ± 0.0 | 0.0007 ± 0.0001 | never (-1) |

Train loss reaches ~0.0002 while val loss climbs past 8 — textbook memorization
without generalization, same signature as the MP-11 P=59 drills (1500 AND 3000
epochs, wd 0.3). P=97 was not re-run: MP-78 already records the scan ALL-DENSE
at P=59/67/97, and a stale `checkpoints/control_p97` checkpoint (epoch 1999,
val 0.0002) agrees.

### 3. Two environment/process findings repaired in passing

- **Corrupt mypy cache** (`sqlite3.DatabaseError: database disk image is
  malformed`) made `typecheck-new` crash with INTERNAL ERROR. Cleared
  `.mypy_cache`, re-ran: clean. Environment issue, not a code issue.
- **Flagship-manifest overwrite**: the P=67 probe wrote over
  `results/exp2_grokking.json` (the P=113 NO-GROK flagship, val 1.0, k_99=111).
  Restored the flagship from git, preserved the probe numbers in this note.
  Lesson: `--seeds` always writes the same manifest path regardless of modulus —
  probes must back up `results/` first.

## Limitations (what this does NOT prove)

- The probes ran 1500 epochs vs the flagship's 5000: small-P non-generalization
  could still be budget, not architecture. The dense-Fourier reading at small P
  is therefore weaker than it looks — the honest headline is "memorization
  without generalization reproduced," not "sparse circuit ruled out."
- Rung 1's extended 10k-epoch run and the Colab P=113 GPU verdict are still in
  flight elsewhere; this session touched neither.
- Full-tree mypy still reports 205 errors (baseline 176 + ~29, mostly the
  capstone file's remaining annotations) — tracked non-blocking follow-up, not
  introduced here. This fix removed 2 of them (the `call-arg` trio at the old
  call site plus the import row stays clean).

## Links

- [[07_capstone/research-plan]] — the experiment ladder this session defends
  (Rung 2 NO-GROK, Rung 1 domino, capstone runner).
- [[portfolio/RESULTS]] — Honesty Ledger home; flagship P=113 numbers unchanged
  and re-verified intact after the overwrite repair.
- [[00_meta/28_micro-phase-29-the-positive-negative]] — the MP-29 plan whose
  positive-control leg these probes belong to.
- Code: `src/experiments/exp6_capstone.py` (`train_single_seed`),
  `tests/test_exp6_capstone.py`.

## Open questions

- Should `--seeds` manifest paths be namespaced by distinguishing args
  (e.g. modulus) so a probe can never again overwrite a flagship manifest?
- Is the 1500-epoch probe horizon worth extending to 5000 on CPU (~5 h/seed at
  P=59), or should small-P probes wait for the same GPU session as P=113?
