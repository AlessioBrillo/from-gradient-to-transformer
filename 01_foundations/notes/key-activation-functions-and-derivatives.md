---
tags: [type/lesson, phase/1, state/consolidated]
state: consolidated
created: 2026-06-18
---

> **Series**: [StatQuest — Neural Networks Pt. 5: ArgMax and SoftMax](https://youtu.be/KpKog-L9veg) | [StatQuest — The SoftMax Derivative, Step-by-Step](https://youtu.be/M59JElEPgIg)
>
> **Also**: [Essence of Calculus — 3Blue1Brown](https://youtube.com/playlist?list=PLZHQObOWTQDMsr9K-rj53DwVRMYO3t5Yr&si=UrW_Qk2DDRi0K3PQ) — Chapter 4 (chain rule context)

## What it is
Activation functions introduce non-linearity into neural networks; each has a specific derivative that is used during backpropagation.

## Why it exists / what problem it solves
A composition of linear transformations is itself linear — stacking any number of dense layers without activations collapses to a single linear transformation. Non-linear activations allow networks to represent arbitrary functions (universal approximation theorem). The derivative of each activation determines how gradients flow during training: saturating activations like sigmoid can
  kill gradients; non-saturating ones like ReLU keep them alive.

## How it works

### Sigmoid
σ(x) = 1 / (1 + e^{−x})
σ'(x) = σ(x) · (1 − σ(x))

Range: (0, 1). Used in binary classification output layers. Derivative peaks at 0.25 near x=0 and approaches 0 for large |x| — the **vanishing gradient problem**: deep sigmoid networks train slowly because early layers receive tiny gradients.

```python
import numpy as np

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def sigmoid_grad(x):
    s = sigmoid(x)
    return s * (1 - s)
```

### Tanh
tanh(x) = (e^x − e^{−x}) / (e^x + e^{−x})
tanh'(x) = 1 − tanh²(x)

Range: (−1, 1). Zero-centered (unlike sigmoid), which helps conditioning. Still saturates at extremes — vanishing gradient persists.

```python
def tanh_grad(x):
    t = np.tanh(x)
    return 1 - t ** 2
```

### ReLU (Rectified Linear Unit)
ReLU(x) = max(0, x)
ReLU'(x) = 1 if x > 0, else 0

Range: [0, ∞). Non-saturating for x > 0 — gradients flow freely through active neurons. The default choice for hidden layers since ~2013. Downside: **dead ReLU** — if a neuron's weights push all inputs to negative, its gradient is 0 and it never recovers.

```python
def relu(x):
    return np.maximum(0, x)

def relu_grad(x):
    return (x > 0).astype(float)
```

### Leaky ReLU / variants
LeakyReLU(x) = x if x > 0, else αx (with α small like 0.01)
PReLU, ELU, GELU — each attempts to fix the dead ReLU problem by allowing small negative gradients.

### Softmax (for output probabilities)
softmax(z)_i = e^{z_i} / Σ_j e^{z_j}

Range: (0, 1), sums to 1. Converts logits to a probability distribution.

The softmax gradient has a special property: when combined with cross-entropy loss, the gradient simplifies to (y_pred − y_true). This is the **log-softmax trick** — one of the most elegant simplifications in deep learning.

```python
def softmax(logits):
    logits = logits - np.max(logits, axis=-1, keepdims=True)  # numerical stability
    exp = np.exp(logits)
    return exp / np.sum(exp, axis=-1, keepdims=True)
```

### How activation derivatives control gradient flow
In backpropagation, the gradient at each layer is:

δ_ℓ = (W_{ℓ+1}^T · δ_{ℓ+1}) ⊙ σ'(z_ℓ)

where ⊙ is element-wise multiplication and σ'(z_ℓ) is the activation derivative. If σ'(z_ℓ) ≈ 0 for most neurons (sigmoid/tanh saturation), δ_ℓ ≈ 0 — the gradient vanishes. If σ'(z_ℓ) is always 1 for active neurons (ReLU), the gradient flows unattenuated through active paths.

## Links
- [[01_foundations/notes/chain-rule-and-backpropagation|Chain Rule and Backpropagation]]
- [[01_foundations/notes/derivatives-and-gradient-descent|Derivatives and Gradient Descent]]
- [[01_foundations/notes/numerical-gradient-check|Numerical Gradient Check]]

## Insight
The choice of activation function is a choice about **gradient flow**. Sigmoid and tanh squash their inputs, creating regions where the derivative is near-zero. ReLU and its variants keep gradients alive but introduce a different problem: the gradient is either 1 or 0, which means a neuron is either fully learning or fully dead. Modern architectures (Transformer, Llama) use GELU or
  SwiGLU — smooth approximations that avoid the hard cut-off of ReLU while keeping gradients healthy.
