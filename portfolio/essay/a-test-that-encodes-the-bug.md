---
tags: [portfolio, essay, mechanistic-interpretability, induction-heads, testing]
published: 2026-11-17
status: verified
---

# A test that encodes the bug

For two months this repository reported that its small transformer formed **no induction heads**: "0 of 8" at Rung 1, "0 of 4" at Rung 4. The number was stable, it appeared in the README, in the paper and in the skill tree, and a test suite protected it. All of it was a statement about the detector, not about the model.

## What the detector measured

An induction head, on the task used here (a random prefix followed by the same prefix again), attends from a position `q` in the second copy to the token *after* the previous occurrence of the current token. With prefix length `L` that is the key at `q - L + 1`.

The detector measured the mass on `q - 1`: the **previous token**. That is a different circuit (a previous-token head feeds an induction head, it is not one). A second detector in the patching code read `attn_probs.diagonal(offset=1)`, the strict upper triangle of a *causal* softmax, which is identically zero. It could not fire on any model at any scale.

## Why the tests did not notice

The planted-pattern tests built an attention pattern that put its mass on `q - 1` and asserted that the detector found it. The test and the detector agreed because they shared the mistake. A test that encodes the bug passes the bug, and a green suite is exactly the evidence that stops anyone looking.

The way out was to write the new tests from the *task layout*, not from the detector: the copy offset must fire; the previous-token offset, the duplicate-token offset, an off-by-one offset, uniform attention and self-attention must not. The same constructions are repeated on real weights. Then the number changed. The corrected detector, on the standard-scale GPU run, finds two to three copy heads per seed, with 0.95 of their attention mass on the copy offset ([`results/induction_standard.json`](../../results/induction_standard.json)).

<!-- manifest: results/induction_standard.json -->

## And then a second problem, one level down

Finding a copy head did not mean finding an induction head. On a task that is a perfect repetition, the previous occurrence of the current token is *always* at `q - L`, so a head that copies **by content** and a head that copies **by a fixed offset** compute the same function. No measurement made on that task can tell them apart, and the K-composition score cannot either.

A dissociation probe can: feed a batch whose second half is a *permuted* copy of the prefix, where the content target and the fixed offset point at different keys. It said the copy was positional. The honest name for what had formed was a *prefix-copying head*, and the repository now says so ([ADR-0032](../../docs/adr/0032-induction-detector-and-the-positional-shortcut.md)). A new task with variable copy distances was then built to remove the shortcut ([ADR-0033](../../docs/adr/0033-content-based-induction-task.md)); its result is a partial one, and the ledger reports it as that.

## What to take from it

- **Write the test from the specification, not from the code.** If the test could have been derived from the implementation, it cannot catch the implementation's mistakes.
- **Plant a known mechanism and require the instrument to find it, then plant its near neighbours and require it not to.** The negatives are where a detector's meaning lives.
- **A stable negative result deserves the same suspicion as a surprising positive one.** "0 of 8" was reproducible every time. That is what a detector with a fixed blind spot looks like.
- **Name what you measured.** "Mass on offset `q - L + 1`" is a fact; "induction head" is a claim about a mechanism, and it needed a second measurement before it was earned.

The full account, with what changed and what did not, is the 2026-10-19 entry of the [Honesty Ledger](../RESULTS.md).
