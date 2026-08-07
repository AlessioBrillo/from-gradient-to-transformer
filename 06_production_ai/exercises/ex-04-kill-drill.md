---
tags: [type/exercise, phase/6]
skill: reproducible-job-durability
created: 2026-08-07
---

# Exercise: The Kill Drill

## Goal / skill it demonstrates

Prove checkpoint/resume survives a real process death, not just an in-process pause. Micro-
Phase 11's overnight run vanished after ~17 hours with no error, no log, no checkpoint — and
the checkpoint/resume code that should have prevented that had only ever been exercised
inside a single pytest process (`TestCheckpointResume`, 8 toy epochs). That proves the state
serializes correctly. It says nothing about what survives an actual `Stop-Process -Force`.

## Solution

**Setup**: standard-scale hyperparameters (`vocab_size=2048, seq_len=64, d_model=64,
n_layers=2, n_heads=4, --fresh-batches`), seed 0, `--checkpoint-every 5`, scaled to 30
epochs — enough to exercise multiple checkpoint writes and a mid-epoch kill without
committing to the full ~17-20h `--standard` run before the mechanism itself was trusted.

**1. Reference run** (uninterrupted, for comparison):
```
python -m src.experiments.exp1_induction_heads --vocab-size 2048 --seq-len 64 --d-model 64 \
  --n-layers 2 --n-heads 4 --seed 0 --epochs 30 --num-train 8192 --batch-size 64 \
  --fresh-batches --checkpoint-dir checkpoints/kill_drill --checkpoint-every 5
```
Ran to completion; final checkpoint (epoch 29, 0-indexed) copied aside as the ground truth.

**2. Drill run** — launched via `Start-Process -PassThru` to get a real OS PID, not a
subshell:
```
Drill process started, PID 16312
Checkpoint write #1 detected at 08/07/2026 13:17:14
Checkpoint write #2 detected at 08/07/2026 13:17:47
```
Waited for 2 checkpoint writes (epoch 5, epoch 10) plus 12 more seconds so the kill would
land mid-epoch rather than exactly on a save boundary — the harder case.

**3. Hard kill** — not `Ctrl+C`:
```
=== HARD KILL (Stop-Process -Force, PID 16312) -- not Ctrl+C ===
Process still running after Stop-Process: False
```
`Stop-Process -Force` is Windows' closest equivalent to `kill -9` — no signal handler runs,
no graceful shutdown path, the process simply stops existing. This is the failure mode MP11
actually hit, reproduced on purpose.

**4. Inspected the surviving checkpoint**:
```
epoch=9 history_len=10
```
0-indexed epoch 9 = the 10th epoch's checkpoint, written intact — the atomic
temp-file-then-rename in `save_training_checkpoint` meant the kill (which landed ~12s and
several epochs *after* that write, mid-training) never touched a checkpoint that was
mid-write.

**5. Resumed**:
```
RESUME: loaded checkpoints\kill_drill\exp1_checkpoint_seed0.pt (saved after epoch 9) --
continuing from epoch 10
```

**6. Compared every history metric and every final model tensor against the uninterrupted
reference**:
```
reference epoch: 29  resumed epoch: 29

--- history comparison (per-epoch metrics) ---
train_loss: n=30 max_abs_diff=0.000e+00 [OK]
val_loss: n=30 max_abs_diff=0.000e+00 [OK]
val_acc: n=30 max_abs_diff=0.000e+00 [OK]
attn_entropy: n=30 max_abs_diff=0.000e+00 [OK]
diag1_mass: n=30 max_abs_diff=0.000e+00 [OK]

--- final model weights comparison ---
max abs param diff across all tensors: 0.000e+00

=== VERDICT: BIT-IDENTICAL (pass) ===
```

## What I learned doing it

I went in expecting to find *something* — my working hypothesis was cross-process
floating-point nondeterminism (BLAS thread scheduling can legitimately differ between two
separate process launches even with identical seeds, in a way a single in-process test would
never surface). It didn't happen: every metric, every tensor, exactly equal. The design
choice that made this a clean pass rather than a coin flip was `_make_fresh_batches_fn`
deriving each epoch's data from `(seed, epoch)` directly instead of from carried RNG state —
the resumed run doesn't need to reconstruct an RNG stream's history to get the same data,
it just recomputes the same deterministic function. The only thing that genuinely needed to
survive the kill was the model/optimizer/scheduler state and the *shuffling* RNG, and the
atomic rename made sure a save either lands whole or not at all.

The honest caveat: this was a 30-epoch drill, not the full 3000-epoch run, and nothing else
was competing for CPU at the moment of the kill. It de-risks the mechanism. It does not
replace actually launching `--standard` for real and watching it survive hours, not seconds.

## Linked skill
- [[00_meta/02_skill-tree]] → candidate new item: reproducible job durability (Phase 6) —
  flips only once this drill's evidence exists, per the vault's own rule
- [[06_production_ai/notes/checkpoint-resume-durability]]
- [[00_meta/11_micro-phase-12-resilient-flagship-run]]
