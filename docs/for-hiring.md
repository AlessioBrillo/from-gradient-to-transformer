# What this repository demonstrates

A two-minute map from skill to evidence. Every row points at something you can
open and check; nothing here asks to be taken on trust.

The project: train small transformers from scratch, reverse-engineer what they
learned, and keep a public record in which every number is backed by a committed
run manifest. It was built by one person, on a local CPU and free Kaggle/Colab
GPUs.

## Research engineering

| Skill | Evidence |
|---|---|
| Reproducing a published result | Grokking on modular addition, sparse Fourier circuit, 3/3 seeds: [`exp2_grokking.py`](../src/experiments/exp2_grokking.py), [Rung 2 page](../portfolio/projects/rung-2-grokking/index.md) |
| Causal interpretability methods, written by hand | Activation patching, head ablation and path patching without an interpretability library: [`exp4_circuit_patching.py`](../src/experiments/exp4_circuit_patching.py), [`copy_circuit.py`](../src/experiments/copy_circuit.py) |
| Designing an experiment that can fail | A pre-registered task, thresholds and decision rule, frozen before the GPU run: [pre-registration](../07_capstone/notes/variable-distance-induction-preregistration.md), [ADR-0033](adr/0033-content-based-induction-task.md) |
| Catching a wrong instrument | The detector measured the wrong attention offset, and the "0 of 8 heads" it produced was retracted: [ADR-0032](adr/0032-induction-detector-and-the-positional-shortcut.md) |
| Reporting negative and partial results | A PARTIAL verdict published next to the stronger numbers that explain it, kept apart rather than merged: [`content_verdict.py`](../src/experiments/content_verdict.py), [Honesty Ledger](../portfolio/RESULTS.md) |
| Retracting my own conclusions | Thirteen dated audits, each with what was wrong and what changed, including a "no grokking" verdict my own metric had manufactured: [Honesty Ledger](../portfolio/RESULTS.md) |
| Writing it up | A LaTeX mini-paper compiled in CI: [`main.tex`](../portfolio/paper/main.tex) |

## Software engineering

| Skill | Evidence |
|---|---|
| A transformer from scratch | Decoder-only model with RMSNorm, rotary embeddings and a KV cache: [`decoder_only_transformer.py`](../src/models/decoder_only_transformer.py) |
| Fundamentals without a framework | Reverse-mode autodiff, PCA, decision trees and a BPE tokenizer, each with tests: [`micrograd.py`](../src/training/micrograd.py), [`src/models/`](../src/models/) |
| Testing | More than 700 test functions, including tests that plant a known mechanism and require the detector to find it: [`tests/`](../tests/), [`test_planted_induction_detector.py`](../tests/test_planted_induction_detector.py) |
| A CI gate that means something | One pipeline, runnable locally, covering lint, strict typing on new code, tests with a coverage floor, and the two record checks: [`.woodpecker/ci.yml`](../.woodpecker/ci.yml) |
| Long runs that survive interruption | Checkpoint, resume and per-seed recovery manifests: [`checkpointing.py`](../src/experiments/checkpointing.py), [`merge_manifests.py`](../src/experiments/merge_manifests.py) |
| Remote compute on a zero budget | A driver that renders a notebook, runs it on Kaggle, downloads the manifests and validates them before they enter the record: [`kaggle_run.py`](../scripts/kaggle_run.py), [`pin_remote_run.py`](../scripts/pin_remote_run.py), [GPU runs](agents/gpu-runs.md) |
| Reproducibility | Pinned environment (`uv.lock`), seeded runs, and a clean-clone proof: [proof](../06_production_ai/proofs/reproducible-from-clean-clone.md), [`clean_clone_check.sh`](../scripts/clean_clone_check.sh) |

## Architecture and judgement

| Skill | Evidence |
|---|---|
| Turning a principle into a mechanism | "No public number without evidence" is a program, not a guideline: manifests carry seeds, arguments, git SHA and device, and CI fails on an unbacked claim: [`results.py`](../src/results.py) |
| Guarding against regression of the record | A ratchet of retracted sentences that must never reappear, and a check of table numbers against the manifests they cite: [`docs_audit.py`](../scripts/docs_audit.py) |
| Recording decisions with their alternatives | [ADRs](adr/README.md), and a [descope register](../06_production_ai/notes/descope-register.md) that gives a dated reason for everything deliberately not built |
| Stopping a process that stopped paying | The planning method used for two months was closed when it cost more than it returned: [ADR-0031](adr/0031-closure.md) |
| Removing dependencies | Seven libraries dropped because nothing imported them; the reasoning is in the comments of [`pyproject.toml`](../pyproject.toml) |

## What it does not demonstrate

Stated plainly, because the rest of the repository is:

- **Scale.** The largest model here has about 4.3 million parameters, and every
  task is synthetic. Nothing here was run on a production-scale language model.
- **Teamwork.** This is solo work. The review discipline is real (pull requests,
  a gate, written audits), but the reviewer was me.
- **Open results.** Two rungs are not clean wins: the content-based copying
  verdict is PARTIAL, and the sparse autoencoder's dictionary is mostly dead
  features. Both are in the [Honesty Ledger](../portfolio/RESULTS.md).

## Where to look next

- The results at a glance: [README](../README.md#results)
- The full record: [Honesty Ledger](../portfolio/RESULTS.md)
- How to verify a number yourself: [for researchers](for-researchers.md)
