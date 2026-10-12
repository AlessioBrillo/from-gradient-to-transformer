---
tags: [type/lesson, phase/7, research/experiment, state/review]
created: 2026-08-11
---

# Scheduled Negatives — P=113 grokking and R1 standard (MP-28 S3)

Drafted 2026-08-11, while the P=113 seeds were still computing (epoch ~3000/5000)
and before the R1 standard launch. Per MP-27's negative-first law: written in
full before the finals, then kept or struck — never rewritten from mood. Each
negative is a complete, printable report; if the data contradicts it, the
corresponding row of this file is struck with a date and a one-line reference to
the positive verdict. The only post-launch edit allowed anywhere in this record
is "observed" (ADR-0003, Gelman & Loken).

## Negative 1 — "P=113 did not grok within this budget"

**Pre-registered falsification target (ADR-0003 row 1):** no grok by 5000 epochs
with weight decay and cosine schedule as pinned.

**If this negative lands, the report reads:**

The P=113 flagship ran under the frozen ADR-0003 row-1 protocol — three seeds,
`wd=1.0`, cosine LR schedule, 30% train fraction, batch 512, 5000 epochs — and
none of the three seeds reached sustained generalization: final validation
accuracy stayed at memorization level (≈ expected value of the memorized
train set) through 5000 epochs, with the Fourier frequency count never dropping
below P/2 sustained. The micro-phase's named suspects were each tested as a
one-change reading of the record (ADR-0003 row 2's microscope lane):

1. **Embedding re-normalization** — the hypothesis that normalizing embedding
   rows (default `normalize_embeddings=True`) suppresses the Fourier structure
   the modular-addition circuit needs. Tested as a one-change trial:
   re-running the canonical config with `normalize_embeddings=False`.
2. **Cosine schedule / weight decay interaction** — the hypothesis that the
   combination of `wd=1.0` and the cosine schedule either decays the circuit
   before it forms or never allows the low-norm sparse solution to be reached.

The scheduled negative is therefore the honest closure: *grokking modular
addition at P=113 was not reproduced on CPU under this protocol, on this
machine, within this window.* The dated reason is the trial-results table from
the microscope lane, or, if the microscope lane also failed, the one-sentence
scientific claim the record is entitled to: the named suspects were tested and
did not rescue the run. The verdict row (ADR-0003 row 1) then closes
`CLOSED (2026-08-11, no grok by 5000 epochs across 3 seeds under the frozen
protocol; suspects tested via row-2 microscope)` — and the record's public
signature ships this paragraph as the contribution, with the same polish as a
win.

## Negative 2 — "No head at standard scale"

**Pre-registered falsification target (ADR-0003 row 3):** no head at
diag+1 mass > 0.3 on ≥ 1 head, sustained ≥ 5 checkpoints, within the
standard-scale fresh-batches run.

**If this negative lands, the report reads:**

The R1 standard-scale run (`--standard`: vocab 2048, seq_len 64, d_model 64,
2 layers, 4 heads, fresh batches, 3000 epochs, checkpoint-every-250 + resume,
seeds 0–2) completed without forming an induction head under the frozen
definition: no head ever sustained diag+1 mass > 0.3 across ≥ 5 consecutive
checkpoints. Two readings are recorded with dates:

- The fixed-vs-fresh comparison remains the last trustworthy R1 number: the
  fixed-dataset run reached 52.2% vs 0.05% fresh at matched 800 epochs — the
  fixed dataset demonstrably allows memorization, and the fresh-batches run
  never crossed the formation threshold.
- The named suspects for the negative, tested as one-change readings of the
  record: (a) scale — d_model=64 is below the ~d_model=128 where Olsson et al.
  report the head forming reliably; (b) budget — 3000 epochs at num_train=8192
  may be insufficient for 2-layer attention-only at this width; (c) the
  induction protocol itself (prefix ratio, repeated-token rate) as run.

The consequence for the R4/R5 chain is the scheduled negative written as the
R4 result: activation and path patching have no real head to validate against,
so R4 row closes `CLOSED (2026-08-11, no row-3 head; patching validated only
by unit tests)`, and R5's SAE re-run uses the best-available checkpoint (the
no-head baseline stays the reference, and the honest delta is reported).

---

## Strike list (kept after the finals)

- [ ] Negative 1 struck (P=113 grokked) — date + manifest tag:
- [ ] Negative 2 struck (head formed) — date + manifest tag:

## Links

- [[docs/adr/0003-research-return-ledger]] — the rows these negatives would close.
- [[00_meta/27_micro-phase-28-the-execution]] — the session whose S3 drafted them.
- [[07_capstone/research-plan]] · [[portfolio/RESULTS]] — where the struck/kept
  verdict lands.
