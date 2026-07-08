# Proof — QK/OV Circuit Decomposition

I can decompose any attention head into two independent functions: the **QK circuit** (what to attend to) and the **OV circuit** (what to copy from attended positions). This is the central abstraction of mechanistic interpretability (Elhage et al., 2021).

## From First Principles

Given input $x \in \mathbb{R}^{d_{model}}$ at a single position:

### QK Circuit (Where)
$$
\begin{aligned}
Q &= W_Q x \\
K &= W_K x \\
\text{score}(i, j) &= Q_i^T K_j / \sqrt{d_{head}} \\
\text{attn}_{ij} &= \text{softmax}_j(\text{scores}_{ij})
\end{aligned}
$$

The QK circuit is a **bilinear form**: $x_i^T (W_Q^T W_K) x_j$. It computes a pairwise similarity between positions. The matrix $W_{QK} = W_Q^T W_K$ is a single $d_{model} \times d_{model}$ matrix that encodes the attention pattern logic.

### OV Circuit (What)
$$
\begin{aligned}
V &= W_V x \\
\text{output} &= W_O \cdot (\text{attn} \cdot V)
\end{aligned}
$$

The OV circuit is a **linear map**: $W_{OV} = W_O W_V$. It determines what information is copied from the attended position to the output.

### Why They Factor
The key insight: the attention pattern is computed from Q and K *before* V is computed, yet V and the output projection W_O are applied *after*. This means:
- The QK circuit only affects WHERE the head attends
- The OV circuit only affects WHAT is copied from attended positions

They can be analyzed, trained, and ablated independently.

## PyTorch Verification

```python
def decompose_head(W_Q, W_K, W_V, W_O):
    """Extract QK and OV circuits for a single head."""
    # QK circuit: d_model × d_model bilinear form
    W_QK = W_Q.T @ W_K  # (d_model, d_model)

    # OV circuit: d_model × d_model linear map
    W_OV = W_O @ W_V  # (d_model, d_model)

    return W_QK, W_OV
```

## Connection to MI
- **QK circuit analysis**: SVD of $W_{QK}$ reveals what input features drive attention
- **OV circuit analysis**: SVD of $W_{OV}$ reveals what output features are written to the residual stream
- **Virtual weights**: composition of OV circuits across layers forms "virtual attention heads"

I can explain this to a non-technical colleague: *"An attention head has two independent parts — one decides which past tokens to look at, and the other decides what information to copy from them."*

**I have reconstructed this analysis from memory without referring to notes.**
