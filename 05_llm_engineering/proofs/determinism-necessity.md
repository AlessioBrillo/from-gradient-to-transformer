---
tags: [type/proof, phase/5, state/review]
created: 2026-07-08
---

# Proof to myself: Determinism is Necessary for Reproducible Activation Analysis

**Rule:** reconstructed without looking at notes.

## What I needed to demonstrate
Without deterministic inference, two runs of the same input produce different activation values, making circuit analysis unreliable. With deterministic settings, activations are bit-exact replicable.

## What I produced from memory

```python
import torch
from src.models.decoder_only_transformer import DecoderOnlyTransformer

def set_seed(s):
    torch.manual_seed(s)

model = DecoderOnlyTransformer(vocab_size=50, d_model=32, n_layers=2, n_heads=2)
x = torch.randint(0, 50, (1, 8))
model.eval()

# Without deterministic settings — just using eval mode + no_grad
with torch.no_grad():
    _, c1 = model(x, return_cache=True)
    _, c2 = model(x, return_cache=True)

def activation_diff(c1, c2):
    return {k: (c1[k] - c2[k]).abs().max().item() for k in c1}

diffs = activation_diff(c1, c2)
max_diff = max(diffs.values())
print(f"Non-deterministic: max activation diff = {max_diff:.6f}")

# With explicit seed before each run
set_seed(42)
with torch.no_grad():
    _, c1s = model(x, return_cache=True)
set_seed(42)
with torch.no_grad():
    _, c2s = model(x, return_cache=True)

diffs_s = activation_diff(c1s, c2s)
max_diff_s = max(diffs_s.values())
print(f"Seeded: max activation diff = {max_diff_s:.6f}")

# Even seeded runs can differ due to non-deterministic GPU kernels.
# For full determinism, also set:
# torch.use_deterministic_algorithms(True)
# but this can raise errors on operations without deterministic implementations.

assert max_diff_s < 1e-5, "Seeded runs must produce near-identical activations"
print("Proved: seeded runs produce activations within tolerance")
```

## Outcome
- [x] Passed → check the skill in [[00_meta/02_skill-tree]]
- [ ] Retry needed (what was missing): ...

## See also
- [[05_llm_engineering/notes/02-deterministic-inference|Deterministic Inference]] — the lesson whose seed / eval / deterministic-algorithm pipeline this proof reproduces
- [[06_production_ai/notes/results-manifests-and-provenance|Results Manifests and Provenance]] — why bit-exact reruns are the precondition for trusting any recorded manifest
- [[05_llm_engineering/exercises/ex-02-activation-harvesting|Activation Harvesting Exercise]] — the exercise that applies this determinism requirement to a real multi-prompt activation harvest
