---
tags: [type/proof, phase/6]
created: 2026-08-07
---

# Proof to myself: Checkpoint/Resume Survives a Real Process Death

**Rule:** reconstructed without looking at notes.

## What I needed to demonstrate

That `save_training_checkpoint` / `load_training_checkpoint` — committed as part of Micro-
Phase 12's stateful-run infrastructure — actually survive a real, hard process kill, not just
an in-process pause. `TestCheckpointResume` (the existing unit test) proves the state
round-trips correctly through Python objects inside a single pytest process. It says nothing
about what happens when the OS actually terminates the process the way Micro-Phase 11's
overnight run died: no signal handler, no graceful shutdown, the process simply gone.

I have deliberately not treated the in-process test as sufficient before checking this skill
— the whole reason this phase exists is that an unverified assumption about durability is
what let a 17-hour run vanish without a trace.

## What I produced from memory

**What I ran, on this machine, against a real OS-level kill:**

- Uninterrupted 30-epoch reference run at standard-scale hyperparameters
  (`vocab_size=2048, seq_len=64, d_model=64, fresh-batches`, seed 0), final checkpoint kept
  aside.
- A second run of the same config, launched via `Start-Process -PassThru` to get a real PID.
  Waited for 2 checkpoint writes (epoch 5, epoch 10), then 12 more seconds so the kill would
  land mid-epoch.
- `Stop-Process -Force` on that PID — Windows' equivalent of `kill -9`. Confirmed dead via
  `Get-Process` returning nothing.
- Inspected the surviving checkpoint: intact, `epoch=9` (the 10th-epoch save), thanks to the
  atomic temp-file-then-rename in `save_training_checkpoint` — a kill that lands after a
  completed rename can't corrupt the file that rename produced.
- Resumed with `--resume`: `RESUME: loaded ... (saved after epoch 9) — continuing from epoch
  10`. Ran to completion (epoch 29).
- Compared every entry of `history` (`train_loss`, `val_loss`, `val_acc`, `attn_entropy`,
  `diag1_mass`, 30 epochs each) and every tensor in the final model `state_dict` against the
  uninterrupted reference:

```
train_loss: n=30 max_abs_diff=0.000e+00 [OK]
val_loss: n=30 max_abs_diff=0.000e+00 [OK]
val_acc: n=30 max_abs_diff=0.000e+00 [OK]
attn_entropy: n=30 max_abs_diff=0.000e+00 [OK]
diag1_mass: n=30 max_abs_diff=0.000e+00 [OK]
max abs param diff across all tensors: 0.000e+00

=== VERDICT: BIT-IDENTICAL (pass) ===
```

Bit-identical, not approximately equal — at float32 precision, across a real process
boundary, on the first drill.

**What this proof does *not* yet demonstrate**, and why it's marked passed for what it
covers rather than padded into a claim about the full run:

1. **30 epochs, not 3000.** The full `--standard` run is ~17-20h. This drill proves the
   mechanism survives a kill; it doesn't prove a multi-hour run survives everything else that
   can happen over that much longer a window (disk pressure, an OS reboot, thermal
   throttling). That's Step 3's job, not this drill's.
2. **No contending process at kill time.** The hypothesis I actually expected to fail on —
   cross-process BLAS/thread nondeterminism producing a *close-but-not-identical* resume —
   didn't materialize under this drill's conditions. A single passing run doesn't rule it out
   under heavier concurrent load.
3. **Windows only.** `Stop-Process -Force` is this platform's hard-kill primitive; the
   equivalent on the machine that would actually run the multi-hour job (if different)
   wasn't tested here.

## Links
- [[06_production_ai/notes/checkpoint-resume-durability]]
- [[06_production_ai/exercises/ex-04-kill-drill]]
- [[00_meta/11_micro-phase-12-resilient-flagship-run]]
- Code: `src/experiments/exp1_induction_heads.py` (`save_training_checkpoint`,
  `load_training_checkpoint`)

## Outcome
- [x] Passed → checked "Reproducible job durability" in [[00_meta/02_skill-tree]]
- [ ] Retry needed (what was missing): the full-scale, full-duration `--standard` drill —
  tracked as Step 3 of the current micro-phase, not a gap in this proof's own scope.
