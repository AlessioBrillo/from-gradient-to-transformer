---
tags: [type/lesson, phase/5]
state: review
created: 2026-07-08
---

# Deterministic Inference for Reproducible Research

## What it is
Deterministic inference guarantees that running the same model with the same input produces identical activations every time — essential for reproducible circuit analysis.

## Why it exists / what problem it solves
Non-determinism from GPU kernels (flash attention, cuBLAS, dropout) means two nominally identical runs produce slightly different activations. For mechanistic interpretability, this is fatal: a circuit analysis that measures activation values or patching effects will produce non-replicable results. Deterministic inference fixes this by eliminating the sources of randomness.

## How it works

### Seed control
```python
import torch
import random
import numpy as np

def set_seed(seed: int = 42):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
```

### Deterministic algorithms
PyTorch offers `torch.use_deterministic_algorithms(True)` which forces every operation to use a deterministic implementation:

```python
torch.backends.cudnn.deterministic = True
torch.backends.cudnn.benchmark = False
torch.use_deterministic_algorithms(True)
```

**Important caveat:** Some operations have no deterministic implementation (e.g., `torch.nn.functional.interpolate` on certain backends). Deterministic algorithms can also be slower (no cuDNN autotuning).

### Dropout at inference
Dropout must be disabled during harvesting — use `model.eval()` which disables dropout layers. Our `generate()` method already calls `self.eval()`.

### Float determinism
Floating-point non-associativity means `(a+b)+c != a+(b+c)`. Even with deterministic algorithms, different reduction orderings (e.g., attention softmax over variable-length sequences) can produce bit-level differences. For most MI work, tolerance-based comparison (`torch.allclose(atol=1e-5)`) is sufficient.

### Full pipeline
```python
def reproducible_forward(model, x, seed=42):
    set_seed(seed)
    model.eval()
    with torch.no_grad():
        logits, cache = model(x, return_cache=True)
    return logits, cache

r1 = reproducible_forward(model, x, seed=42)
r2 = reproducible_forward(model, x, seed=42)
assert all(torch.allclose(r1[1][k], r2[1][k]) for k in r1[1])
```

## Links
- [[05_llm_engineering/notes/01-transformer-lens-hooks|TransformerLens Hooks]]
- [[05_llm_engineering/notes/03-activation-harvesting|Activation Harvesting]]
- [[04_nlp_and_transformers/proofs/residual-stream-communication-channel]]

## Open questions
- #question Does Apple MPS backend support deterministic algorithms in 2026?
