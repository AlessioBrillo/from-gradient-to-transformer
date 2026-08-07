---
tags: [type/lesson, phase/6, state/review]
---

# Checkpoint/Resume Durability

## What it is

The property that a long training run surviving a real process death — not a clean
`Ctrl+C`, an actual `kill -9`-equivalent termination — produces results indistinguishable
from a run that was never interrupted. `save_training_checkpoint` /
`load_training_checkpoint` (`src/experiments/exp1_induction_heads.py`) implement it: a
single rolling file per seed, capturing model, optimizer, and scheduler state plus the
PyTorch RNG state at the exact continuity point, written via a temp-file-then-atomic-rename
so a kill mid-write can't leave a truncated checkpoint behind.

## Why it exists / what problem it solves

Micro-Phase 11 launched a standard-scale (~17-20h) Rung 1 run unattended overnight. It went
silent — no process, no log, no checkpoint — after roughly 17 hours of CPU time, with
nothing to show for it either way. The checkpoint/resume code that would have prevented this
was already committed by that point, but it had only ever been exercised **in-process**:
`TestCheckpointResume` pauses and resumes an 8-epoch toy run inside a single pytest process.
That proves the state round-trips correctly through Python objects. It does not prove
anything survives what actually happened to the MP11 run — a real process disappearing.

## How it works

**The design that makes this tractable**: `_make_fresh_batches_fn` derives each epoch's
training data from `seed * 1_000_003 + epoch + 1` — a pure function of `(seed, epoch)`, not
of any carried RNG stream. This sidesteps the failure mode I expected going in (RNG state
silently desyncing across a resume) for the *data* — a resumed run reconstructs exactly the
same per-epoch dataset a continuous run would have drawn, regardless of what happened to any
global RNG in between. The remaining RNG-dependent operation is `DataLoader(shuffle=True)`'s
batch ordering, which does depend on `torch`'s global generator — and that's exactly the
state `save_training_checkpoint` captures (via `torch.random.get_rng_state()`, right after
the epoch's own draws and before the next epoch's) and `load_training_checkpoint` restores
before training resumes.

**The kill drill (2026-08-07, Micro-Phase 12 Step 2)** — first real test against an actual
process death, standard-scale hyperparameters (`vocab_size=2048, seq_len=64, d_model=64,
n_layers=2, n_heads=4, fresh-batches`), seed 0, `--checkpoint-every 5`, scaled to 30 epochs
(not the full 3000 — see limitations):

1. Ran an uninterrupted 30-epoch reference run; kept its final checkpoint aside.
2. Launched a second run, waited for 2 checkpoint writes (epoch 5, epoch 10) plus 12 more
   seconds so the kill would land mid-epoch, not on a boundary.
3. `Stop-Process -Force` on the live PID — an actual OS-level termination, not `Ctrl+C` and
   not an in-process pause. Confirmed dead (`Get-Process` on the PID returned nothing).
4. Inspected the surviving checkpoint: `epoch=9` (0-indexed — the 10th-epoch save landed
   intact), `history_len=10`.
5. Relaunched with `--resume`: `RESUME: loaded ... (saved after epoch 9) — continuing from
   epoch 10`.
6. Let it run to epoch 30. Compared every entry of `history` (`train_loss`, `val_loss`,
   `val_acc`, `attn_entropy`, `diag1_mass`) and the full final model `state_dict` against the
   uninterrupted reference, tensor by tensor.

**Result: bit-identical.** Every history array matched the reference to `max_abs_diff =
0.000e+00` across all 30 epochs; every model parameter tensor matched to `0.000e+00`. Not
"close" — exactly equal, at float32 precision, across a real process boundary. The design
held on the first real drill.

## Limitations

30 epochs at standard-scale hyperparameters, not the full 3000-epoch (~17-20h) run MP11
actually launched. This drill proves the *mechanism* — atomic checkpoint write, RNG capture,
epoch-deterministic data — survives a real kill at this scale; it does not by itself prove a
multi-hour run survives whatever else can go wrong over that much longer a window (disk
pressure, a Windows update reboot, thermal throttling). It also ran on a machine with no
other process contending for the same PyTorch/BLAS threads at the moment of the kill — the
hypothesis I went in expecting to find a problem in (cross-process floating-point
nondeterminism from BLAS thread scheduling) did not materialize here, but a single passing
drill doesn't rule it out at a different concurrency level.

## Links
- [[06_production_ai/exercises/ex-04-kill-drill]]
- [[00_meta/11_micro-phase-12-resilient-flagship-run]]
- [[04_nlp_and_transformers/notes/induction-heads]]
- Code: `src/experiments/exp1_induction_heads.py` (`save_training_checkpoint`,
  `load_training_checkpoint`, `train_model`)
- Ott et al. discussion of fault-tolerant training / `torchsnapshot`-style checkpoint design
  (industry precedent for the atomic-rename pattern used here)

## Open questions
- #question Does this hold at the full 3000-epoch scale, over many hours, with the machine
  doing other things? The drill de-risks the mechanism; it doesn't replace the real
  `--standard` run this phase still needs to launch.
