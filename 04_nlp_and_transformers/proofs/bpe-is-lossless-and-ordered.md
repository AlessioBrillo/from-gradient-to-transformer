---
tags: [type/proof, phase/4, state/review]
authorship: claude
created: 2026-11-17
---

# Proof: byte-level BPE is lossless, and encoding is the training order replayed

> **Authorship.** Written by Claude on 2026-11-17, not reconstructed from memory by the
> repository owner. Companion exercise:
> [[04_nlp_and_transformers/exercises/ex-04-bpe-from-scratch]]; background:
> [[04_nlp_and_transformers/notes/bpe-tokenizer]].

## Claim

For a byte-level BPE tokenizer whose pre-tokenizer partitions the text, (a) every string
round-trips exactly, (b) encoding is a deterministic function of the learned merge list,
and (c) enlarging the vocabulary never lengthens an encoding.

## Proof

**(a) Losslessness.** Two conditions suffice.

1. *The token ids cover the bytes.* Ids 0 to 255 are the 256 single bytes, so any UTF-8
   string has an encoding with no unknown token. Each merged id stands for the
   concatenation of the two token byte strings it replaced, so decoding is
   `b"".join(vocab[i] for i in ids)` and returns the original bytes.
2. *The pre-tokenizer loses nothing.* The text is cut into chunks by a regular
   expression and each chunk is encoded alone. The concatenation of the chunks must be
   the text. That holds only if the alternatives of the pattern cover every character.
   The pattern lacked a whitespace alternative, so `findall` skipped characters, and
   condition 2 was false; the fix adds `\s+(?!\S)|\s+`, which matches any whitespace
   the other alternatives leave (the exercise lists the failing inputs).

Decoding uses `errors="replace"`, so the exact round trip is for ids produced by
`encode`; arbitrary id sequences can form invalid UTF-8 and are replaced, not rejected.

**(b) Encoding replays training.** A merge is added only when its pair is the most
frequent in the corpus at that step, and merges get increasing ids. `encode` repeatedly
applies the *lowest-id* merge present in the chunk. The lowest id is the earliest
learned, so encoding applies the merges in training order. Given the same merge list the
result is unique; training is deterministic because `Counter.most_common` breaks ties by
insertion order (`test_training_is_deterministic`).

**(c) Monotone in vocabulary size.** Training with a larger budget learns the same first
merges and then more, since each step depends only on the corpus and the earlier merges.
A longer merge list can only merge more pairs, so the encoding of any text has no more
tokens (`test_a_larger_vocabulary_never_lengthens_the_encoding`, and the table in the
exercise: 36, 23, 11, 11 tokens).

## What is not claimed

- That the tokens are linguistically good. BPE optimises frequency, not meaning.
- That the pattern matches GPT-2's or any production tokenizer's. It is a small
  approximation of the GPT-2 split.
- Anything about a trained model: no experiment here uses this tokenizer.

## Outcome

- [x] Each claim is tied to a test; (a) failed on the old code and drove the fix.
- [ ] Reconstructed from memory by the repository owner. Not done.
