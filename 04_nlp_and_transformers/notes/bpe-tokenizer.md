---
tags: [type/lesson, phase/4, state/review]
---

# BPE Tokenizer — From Scratch

## Why tokenization matters
Transformers don't see characters or words — they see **token IDs**. The tokenizer determines the vocabulary, which determines what the model can learn. Bad tokenization = bad model.

## BPE algorithm
Byte-Pair Encoding (Sennrich et al., 2016):

1. Start with byte-level vocabulary (256 tokens)
2. Count all adjacent byte pairs in the training corpus
3. Merge the most frequent pair into a new token
4. Repeat until desired vocab size is reached (e.g., 32K, 50K)

```
"h e l l o"  → "h" "e" "ll" "o"  → "h" "e" "ll" "o"  → "hell" "o"
   initial        merge "ll"                merge "hell"
```

## Key design decisions
- **Pre-tokenization**: split on whitespace/punctuation before BPE (GPT-2 pattern: `' ?\w+| ?\S+`)
- **Bytes vs chars**: GPT-2 uses bytes (base 256), modern tokenizers use Unicode codepoints
- **Vocab size**: GPT-2 = 50,257; Llama 3 = 128,000; larger vocab = fewer tokens per word but more parameters
- **Special tokens**: [PAD], [UNK], [BOS], [EOS], [SEP], [CLS], [MASK]

## MI forward link
The tokenizer determines the "vocabulary of thought" for the model. Sparse autoencoders discover features in the residual stream that are more aligned with semantic concepts than with individual tokens — in effect, the SAE learns a *semantic tokenizer* on top of the BPE tokenizer. Understanding BPE's limitations (splitting "unethical" into "un" + "ethical" vs "uneth" + "ical") helps explain the kind of superposition that SAEs must resolve.

## Implementation
See `src/models/bpe_tokenizer.py` for a minimal BPE implementation.

## References
- Sennrich et al., *Neural Machine Translation of Rare Words with Subword Units* (ACL 2016)
- Radford et al., *Language Models are Unsupervised Multitask Learners* (GPT-2, 2019)
- Kudo & Richardson, *SentencePiece: A simple and language independent subword tokenizer* (2018)
