---
tags: [type/exercise, phase/4, state/review]
authorship: claude
created: 2026-11-17
---

# Exercise 04 — A byte-level BPE tokenizer that does not lose text

> **Authorship.** Written by Claude on 2026-11-17 to close a gap the vault's own rule
> exposed (see [[00_meta/02_skill-tree]]). The code and tests are real; this is not the
> repository owner's own solution.

## Goal / skill it demonstrates

Implement byte-pair encoding and show the one property a tokenizer must have:
`decode(encode(text)) == text` for *any* text.

## Task

1. Train merges on a corpus: repeatedly merge the most frequent adjacent pair.
2. Encode by applying the merges in the order they were learned.
3. Decode by concatenating the bytes of each token.
4. Test the round trip on whitespace and non-ASCII text, not only on prose.

## Solution

Code: `src/models/bpe_tokenizer.py`. Tests: `tests/test_bpe_tokenizer.py`.

Training on `"the cat sat on the mat. the cat sat."` (36 bytes):

| Vocabulary size | Merges learned | Tokens for that text |
|---|---|---|
| 256 (bytes only) | 0 | 36 |
| 260 | 4 | 23 |
| 280 | 12 | 11 |
| 300 | 12 | 11 |

The count stops falling at 280 because only 12 distinct pairs ever occur twice in
that corpus; further merges have nothing to merge.

## A defect this exercise found

The first version of this exercise passed, because the existing round-trip tests only
used single-spaced prose. Writing the whitespace cases found that the tokenizer was
**lossy**: the split pattern matched words and punctuation but nothing for whitespace,
so `re.findall` silently dropped newlines, tabs, repeated spaces and trailing spaces:

| Input | Decoded (before the fix) |
|---|---|
| `"hello  world"` | `"hello world"` |
| `"a\nb"` | `"ab"` |
| `"tab\there"` | `"tabhere"` |
| `"trailing "` | `"trailing"` |

The pattern now ends with `|\s+(?!\S)|\s+`, so whitespace no word chunk claims becomes
its own chunk. `TestLosslessness` fails on the old code and passes on the new.

No experiment in this repository uses the tokenizer (every task trains on integer
token ids; see [[portfolio/model-card]]), so no published number is affected. The
lesson is about the tests: a round-trip test is only as strong as the inputs it tries.

## Linked skill

- [[00_meta/02_skill-tree]] → BPE tokenizer from scratch
- Proof: [[04_nlp_and_transformers/proofs/bpe-is-lossless-and-ordered]]
