---
tags: [type/lesson, phase/4, state/review]
---

# MI Tooling — TransformerLens, SAELens, nnsight, CircuitsVis

## TransformerLens (Neel Nanda)
**Purpose**: Library for mechanistic interpretability of pretrained transformers.

Key features:
- **HookedTransformer**: wraps any HuggingFace model with hook points at every activation
- **ActivationCache**: named access to `cache["blocks.0.attn.hook_q"]`, `cache["blocks.1.hook_resid_pre"]`
- **Built-in patching**: `model.act_patch()` runs activation patching in ~10 lines
- **Supported models**: GPT-2, Llama, Mistral, Pythia, Gemma, Qwen, etc.

```python
from transformer_lens import HookedTransformer
model = HookedTransformer.from_pretrained("gpt2-small")
logits, cache = model.run_with_cache("Hello, world!")
cache["blocks.0.attn.hook_pattern"]  # (B, n_heads, S, S)
```

## SAELens
**Purpose**: Training and analyzing sparse autoencoders on transformer activations.

Key features:
- Training SAEs on HookedTransformer activations (not synthetic data)
- Loading pretrained SAEs from Neuronpedia/Gemini Scope
- Feature dashboard visualization
- Automatic feature interpretation via: max-activating examples, logit attribution, feature-to-vocab projection

```python
from sae_lens import SAE
sae, cfg_dict, sparsity = SAE.from_pretrained(release="gpt2-small-res-jb", sae_id="blocks.4.hook_resid_pre")
```

## nnsight (NDIF)
**Purpose**: Intervention graphs for intervention-based interpretability.

- Uses delayed computation graph: describe the intervention, then execute
- Can run on remote models via NDIF cloud
- More flexible than TransformerLens for complex multi-intervention experiments

```python
from nnsight import LanguageModel
model = LanguageModel("gpt2", device_map="auto")
with model.generate("Hello") as tracer:
    hidden = model.transformer.h[4].output[0].save()
    model.transformer.h[8].output[0][:] = 0  # ablation
```

## CircuitsVis (Anthropic)
**Purpose**: Visualizing attention patterns as interactive HTML.

- `attention_heads()`: attention pattern heatmaps
- `circuit_diagram()`: full circuit visualization
- Exports as standalone HTML that includes all data

```python
from circuitsvis.attention import attention_heads
attention_heads(attn_probs, tokens)
```

## When to use what
| Tool | Best for |
|------|----------|
| TransformerLens | Quick hooking, caching, patching on standard models |
| SAELens | Feature extraction, SAE training on real activations |
| nnsight | Complex multi-intervention experiments, remote execution |
| CircuitsVis | Interactive visualizations for papers/blogs |

## References
- Nanda & Bloom, *TransformerLens: A Library for Mechanistic Interpretability* (2022)
- Bricken et al., *Towards Monosemanticity* (2023)
- ndif.com — *nnsight documentation*
- Anthropic, *circuitsvis: Visualization tools for mechanistic interpretability*
