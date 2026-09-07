---
tags: [type/moc, phase/7, research/experiment, state/review]
created: 2026-09-07
consumes: [89_micro-phase-89-from-retune-to-signal, ADR-0028]
---

# Micro-Phase 89 — Retune A/B Verdict: No Modular Movement at 500 Steps

> **STATUS: COMPLETE — Row 2 VERDICT-NO-MOVE, stamped 2026-09-07.** This
> note records the outcome of my frozen 500-step A/B (MP-89 Session 1)
> against the MP-88 shakedown's load-bearing question: does a
> vocab-offset or curriculum reweight move modular addition off chance?

## A/B Protocol (frozen at Session 0, never improvised)

- **Seed**: 0 (same as shakedown)
- **Horizon**: 500 steps, warmup 100, checkpoint every 500
- **Three arms, one intervention each**:
  - Control: exact MP-88 shakedown config at short horizon
  - Offset (Arm A): `--vocab-offset 2048` — modular ids in
    `[2048, 2161)`, pad 2161, disjoint from induction `[0, 2048)`
  - Reweight (Arm B): `--modular-weight 5.0 --induction-weight 0.5` —
    10× relative boost for the 1-token vs 127-token supervision
    mismatch
- **Single score**: modular accuracy off chance (1/113 ≈ 0.00885)
- **Probe manifests**: `results/probe_capstone_ab_{control,offset,reweight}.json`
- **No flagship clobber**: `verify-claims` at 0, flagship sha unchanged

## Results (from manifest bytes)

| Arm | Modular acc | Induction acc | Fourier k_99 | Max K-comp | Reading |
|---|---|---|---|---|---|
| Control | **0.0062** | 0.0005 | 98.18 | 0.3690 | Below chance (0.00885) |
| Offset | **0.0060** | 0.0005 | 98.61 | 0.1728 | Below chance, K-comp ↓ |
| Reweight | **0.0065** | 0.0005 | 98.11 | 0.3048 | Below chance, highest mod |

**Chance threshold**: 1/113 ≈ 0.00885. **All three arms below chance.**

## Verdict

**NO-MOVE — neither arm moved modular off chance in 500 steps.**

- The vocab-offset arm (interference hypothesis) *did not* fix modular
  — accuracy actually dipped slightly (0.0060 vs 0.0062), and K-comp
  dropped from 0.37 to 0.17. The dedicated id range eliminated
  collision but modular still doesn't learn in 500 steps.
- The reweight arm (schedule hypothesis) showed the *highest* modular
  accuracy (0.0065) but still below chance — a 10× boost is not
  sufficient at this horizon.
- Induction stayed near zero in all arms (0.0005) — the curriculum
  reweight did not collapse induction either.

**Interpretation**: the MP-88 dissociation (modular 0.0047, induction
0.504 at 2000 steps) persists at 500 steps — neither interference nor
schedule is the *primary* bottleneck at this horizon; the modular task
simply doesn't generalize in 500 steps under any of these configs. The
2000-step shakedown already gave the answer: modular never leaves
chance while induction takes off. The retune A/B confirms that *shortening
the horizon doesn't surface a different signal*.

## Decision

**No retuned 2k launch.** The A/B verdict is NO-MOVE — the path to
modular movement requires the full horizon (where we already know it
stays dense) or a fundamentally different approach (architecture,
optimizer, data, or GPU scale). I do *not* launch a 20k-by-3 run on the
current config.

The dated "v20 is the record" memo path is taken: the interference is
characterized as the contribution, the dense attractor is the finding,
and the next research question (if any) is gated on the GPU run or a
new candidate set in the next ledger.

## Links

- [[89_micro-phase-89-from-retune-to-signal|MP-89 roadmap]] — Sessions 0–6
- [[88_micro-phase-88-from-transcripts-to-verdicts|MP-88 shakedown verdict]] — the Row 1 evidence
- [[docs/adr/0028-continuum-ledger-23|ADR-0028 Row 2 stamp]] — this verdict
- Manifests: `results/probe_capstone_ab_control.json`,
  `results/probe_capstone_ab_offset.json`,
  `results/probe_capstone_ab_reweight.json`

**Written:** 2026-09-07
**Perspective:** my personal study notes, learning log, and portfolio showcase
**Status:** Row 2 VERDICT-NO-MOVE stamped; proceeding to Session 2 (W&B + GPU close)