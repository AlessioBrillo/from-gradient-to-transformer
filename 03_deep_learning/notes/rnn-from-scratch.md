---
tags: [type/lesson, phase/3, state/review]
---

# RNN From Scratch — Why Attention Exists

## Vanilla RNN cell
```
h_t = tanh(W_h · h_{t-1} + W_x · x_t + b)
y_t = W_y · h_t + b_y
```

The hidden state h_t is a fixed-size vector that "summarizes" the entire prefix. This is the fundamental limitation: the **bottleneck**.

## The sequential bottleneck problem
- **Vanishing gradient**: gradients through tanh ∘ matrix multiply over 50+ steps → exponentially small → can't learn long-range dependencies
- **Fixed capacity**: h_t ∈ ℝ^d must encode the entire prefix in d numbers — no way to "look back" at specific earlier tokens
- **No parallelization**: can't compute h_t until h_{t-1} is done → O(T) sequential, can't use GPU

## Why attention replaces RNNs
Transformers solve all three:
- **Skip connections** (residual stream + attention) give gradients a direct path O(1) instead of O(T)
- **Attention weights** dynamically select which tokens to attend to — no fixed bottleneck
- **Self-attention** is O(1) parallel per layer (all positions attend to all others simultaneously)

An RNN is like reading a book and summarizing each page into a single sentence as you go. Attention is like keeping the whole book open and glancing at any page you need.

## MI forward link
The RNN's hidden state is a compressed representation of the prefix — this is what autoencoders try to recover. Sparse autoencoders replace the dense bottleneck with a sparse, interpretable dictionary, making the "compression → decompression" loop transparent rather than opaque.

## Implementation (minimal PyTorch)
```python
class RNNCell(nn.Module):
    def __init__(self, input_size, hidden_size):
        super().__init__()
        self.W_h = nn.Linear(hidden_size, hidden_size, bias=False)
        self.W_x = nn.Linear(input_size, hidden_size, bias=False)
        self.b = nn.Parameter(torch.zeros(hidden_size))

    def forward(self, x, h=None):
        B, T, D = x.shape
        if h is None:
            h = torch.zeros(B, self.W_h.out_features, device=x.device)
        outputs = []
        for t in range(T):
            h = torch.tanh(self.W_x(x[:, t]) + self.W_h(h) + self.b)
            outputs.append(h)
        return torch.stack(outputs, dim=1), h
```

## Links

- [[04_nlp_and_transformers/notes/qk-ov-circuits]] — attention solves the sequential bottleneck that makes RNNs struggle
- [[03_deep_learning/notes/backpropagation-from-scratch]] — the reverse-mode autograd that trains every RNN parameter
