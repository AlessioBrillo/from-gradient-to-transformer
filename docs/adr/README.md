# Architecture decision records

| ADR | Topic |
|-----|-------|
| 0001-0030 | Process ledgers, one per micro-phase. Archived in [`archive/process/adr/`](../../archive/process/adr/) |
| [0031](0031-closure.md) | **Process frozen**; v1.0 tracked in GitHub Issues |
| [0032](0032-induction-detector-and-the-positional-shortcut.md) | The induction detector measured the wrong offset; the repeated-token task admits a positional shortcut |
| [0033](0033-content-based-induction-task.md) | The induction claim needs a task without the fixed-offset shortcut |
| [0034](0034-gpt2-small-real-model-test.md) | Test the hand-written instrumentation on GPT-2 small, with the criteria frozen first |
| [0035](0035-gpt2-mean-ablation-and-direct-path-patching.md) | Re-ask the two failed GPT-2 stages with mean ablation, and measure the direct path of the name movers |

Numbers 0011-0022 and 0026 were never written (see ADR-0031). All ledgers up to 0030 are
historical and closed, and were moved to the process archive on 2026-11-16; read them as a
dated record of what was planned, not as current status.
Current status lives in [`portfolio/RESULTS.md`](../../portfolio/RESULTS.md).
