---
tags: [moc, skills, checklist]
---

# Your turn — nine exercises to solve without looking

Nine exercises and proofs in this vault were written by an AI assistant (`authorship: claude`,
see [[00_meta/02_skill-tree]]). They stay as reference. A skill they cover is only `[x]` when
a solution **written by the repository owner** exists next to them.

How to use this page: for each row, close the reference file, read only the statement, solve it
in a new note made with `scripts/new_note.sh`, then run the checks. Set `authorship: user` in
that new note only if you wrote the solution yourself; `co` if you wrote it with help you can
name. The reference stays untouched, so the comparison is honest.

| # | Statement (what to solve, no hints) | Reference to compare after | Check |
|---|---|---|---|
| 1 | Precision, recall, F1 from a confusion matrix you build by hand; then show a feature selector fit before the split inflates a cross-validated score | [[02_classical_ml/exercises/ex-05-metrics-cross-validation-and-leakage]] | the leakage gap is positive on pure noise |
| 2 | State and prove when K-fold CV is an unbiased estimate of a procedure, and why leakage breaks it | [[02_classical_ml/proofs/cross-validation-estimates-and-leakage]] | a counterexample with numbers |
| 3 | AdamW and a cosine schedule from scratch, matching `torch.optim.AdamW` | [[03_deep_learning/exercises/ex-03-adamw-and-schedules]] | max difference below 1e-6 |
| 4 | A training loop with gradient accumulation | [[03_deep_learning/exercises/ex-04-training-loop-and-accumulation]] | accumulated gradient equals the large batch |
| 5 | Prove accumulation equals the large batch, and name the loss for which it does not | [[03_deep_learning/proofs/gradient-accumulation-is-the-large-batch]] | the exception, with an example |
| 6 | Show why decoupled weight decay shrinks an unused weight at rate `lr * wd` | [[03_deep_learning/proofs/weight-decay-and-the-cleanup-phase]] | closed form, then a numerical check |
| 7 | Byte-level BPE where `decode(encode(t)) == t` for any text | [[04_nlp_and_transformers/exercises/ex-04-bpe-from-scratch]] | round trip on random bytes |
| 8 | Prove BPE is lossless and that merge order matters | [[04_nlp_and_transformers/proofs/bpe-is-lossless-and-ordered]] | two orders, two outputs |
| 9 | Show RoPE depends only on the offset and a KV cache changes nothing | [[04_nlp_and_transformers/proofs/attention-rope-and-the-cache]] | cached equals uncached logits |

Rows 1, 3, 4 and 7 are code, so they can start today. Rows 2, 5, 6, 8 and 9 are proofs; write
them on paper first. When a row is done, link your note from the skill in
[[00_meta/02_skill-tree]] and let `make vault-check` decide whether it can turn `[x]`.
