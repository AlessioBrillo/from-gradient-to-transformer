---
tags: [type/exercise, phase/5]
skill: Model Instrumentation — synthetic circuit dataset construction
created: 2026-07-08
---

# Exercise: Synthetic Circuit Dataset Construction

## Goal / skill it demonstrates
Build two synthetic datasets (IOI-style and repeated prefix for induction heads), run our model on each, and compare attention patterns to show task-specific circuits.

```python
import torch
import itertools
from src.models.decoder_only_transformer import DecoderOnlyTransformer

def ioi_dataset(names, verbs, objects):
    """Generate IOI-style prompts: When {A} and {B} went..., {B} gave {obj} to [A]."""
    templates = []
    for A, B in itertools.permutations(names, 2):
        for verb in verbs:
            for obj in objects:
                templates.append({
                    "text": f"When {A} and {B} went to the store, {B} gave {obj} to",
                    "answer": A,
                    "subject": A,
                    "indirect_object": B,
                })
    return templates

def repeated_prefix_dataset(prefixes):
    """Generate repeated prefix prompts for induction head detection."""
    templates = []
    for prefix in prefixes:
        templates.append({
            "text": prefix + prefix,    # "the cat sat on the the cat sat on the"
            "prefix": prefix,
            "repeat_point": len(prefix.split()),
        })
    return templates

model = DecoderOnlyTransformer(vocab_size=50, d_model=32, n_layers=2, n_heads=2)

# --- IOI Prompts ---
ioi_data = ioi_dataset(["Alice", "Bob"], ["went"], ["a book"])
print(f"Generated {len(ioi_data)} IOI templates")
print(f"  Example: '{ioi_data[0]['text']}' → answer: {ioi_data[0]['answer']}")

# Tokenize: use char-level mapping for our small model
char_to_idx = {c: i for i, c in enumerate("abcdefghijklmnopqrstuvwxyz ,.!?")}
def tokenize(text, max_len=32):
    ids = [char_to_idx.get(c, 0) for c in text.lower()[:max_len]]
    return torch.tensor([ids])

# Run IOI prompt and check attention
x = tokenize(ioi_data[0]["text"])
logits, cache = model(x.unsqueeze(0), return_cache=True)
attn_probs = cache["blocks.0.attn.attn_probs"]
print(f"IOI attention shape: {attn_probs.shape} (n_heads, seq_len, seq_len)")

# --- Induction Head Prompts ---
ind_data = repeated_prefix_dataset(["the cat sat on the"])
print(f"\nGenerated {len(ind_data)} induction templates")
print(f"  Example: '{ind_data[0]['text']}'")

x_ind = tokenize(ind_data[0]["text"])
logits_ind, cache_ind = model(x_ind.unsqueeze(0), return_cache=True)

# Compare attention: induction heads should show strong diagonal offset
attn_ind = cache_ind["blocks.0.attn.attn_probs"]
attn_ioi = attn_probs

for h in range(model.n_heads):
    diag_ioi = torch.diag(attn_ioi[0, h, 1:, :-1]).mean().item()
    diag_ind = torch.diag(attn_ind[0, h, 1:, :-1]).mean().item()
    print(f"  Head {h}: IOI diag={diag_ioi:.3f}, Ind diag={diag_ind:.3f}")
```

## What I learned doing it
- Synthetic template design is the key bottleneck for circuit discovery — bad templates produce uninterpretable results.
- IOI requires the model to know name identity; with random weights the attention patterns show no meaningful structure. This is expected — circuit analysis only works *after* training.
- The repeated prefix dataset is the minimal setup for induction head detection.

## Linked skill
- [[00_meta/02_skill-tree]] → Model Instrumentation: Synthetic dataset construction
