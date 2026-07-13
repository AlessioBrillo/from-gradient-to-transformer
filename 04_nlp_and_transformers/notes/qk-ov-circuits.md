---
tags: [phase/4, note, state/review, research/experiment]
MI-core: "The single most important abstraction in mechanistic interpretability: every attention head computes two separate functions."
---

# QK/OV Circuit Decomposition — The Central Abstraction

## The Core Insight (Elhage et al. 2021)
Every attention head computes TWO separate functions:
- **QK circuit** (Query-Key): determines *which* tokens to attend to
- **OV circuit** (Output-Value): determines *what* to copy from those tokens

These two functions can be analyzed independently because they factor through the attention probability:

$$attention\_pattern = softmax(QK^T / \sqrt{d\_head})$$
$$output = OV \cdot attention\_pattern \cdot input$$

## In More Detail

For a single attention head h:
1. QK circuit: Wh_QK(x) maps x → attention distribution over source positions
2. OV circuit: Wh_OV(x) maps x → value vectors that get mixed by attention

The full head output is:
$$output_h = W\_O^h \cdot (attn\_pattern \cdot W\_V^h \cdot x)$$

The QK circuit is Wh_QK = W_Q^h · W_K^{hT} (a bilinear form).
The OV circuit is Wh_OV = W_O^h · W_V^h (a linear map).

## Why This Matters for MI

- **QK circuit analysis:** If we understand what features cause a head to attend to certain positions, we understand one part of the algorithm
- **OV circuit analysis:** If we understand what features the head copies from attended positions, we understand the other part
- **Independent training:** QK and OV circuits can be (and often are) trained independently — one head might have a clear QK pattern but a meaningless OV circuit, or vice versa

## Residual Stream Perspective

The residual stream at layer L is:
$$x^L = x^{L-1} + attention\_output^L + mlp\_output^L$$

Each head reads from the same residual stream (via QK and OV circuits) and writes back to it. The stream is the communication channel — layers don't talk to each other directly, they all read and write to the same shared space.

## Virtual Attention Heads

If head A in layer L writes to the residual stream, and head B in layer L+1 reads from that stream, the effective computation is a "virtual attention head" — the composition of A's OV circuit and B's QK circuit. This is how multi-layer circuits emerge.

## Practical Analysis Steps

1. **Compute Wh_QK = W_Q @ W_K.T** for each head — this is the bilinear form defining attention
2. **Compute Wh_OV = W_O @ W_V** for each head — this is the linear map defining what gets copied
3. **Project both into the vocabulary/unembedding space** to understand what features matter
4. **Use the logit lens** to read intermediate states: project residual stream → unembed space

## Links

- [[04_nlp_and_transformers/notes/induction-heads]]
- [[04_nlp_and_transformers/proofs/logit-lens]]
- [[04_nlp_and_transformers/notes/activation-patching]]
