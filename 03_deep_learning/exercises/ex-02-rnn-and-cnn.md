---
tags: [type/exercise, phase/3, state/review]
---

# Exercise 02 — RNN and CNN for Context

## Objective
Implement RNN and CNN from scratch or using PyTorch nn modules. Understand why RNNs struggle with long sequences and why CNNs are translation-equivariant.

## Setup
Use synthetic data: sine wave prediction (RNN) and MNIST (CNN).

## Tasks

### 1. RNN for sine wave prediction
Implement an RNN that predicts the next timestep of a sine wave:
- Generate sine wave sequence: `sin(t)`, t ∈ [0, 40π], 200 points
- Train an RNN to predict x_{t+1} from the first 3 timesteps
- Try increasing the sequence length — at what T do gradients vanish?
- Compare training curves for tanh vs ReLU activation

### 2. Compare with explicit state
Implement the same prediction using a fixed-window linear model (use last 5 points as features). Compare accuracy, training speed, and ability to handle longer dependencies.

### 3. CNN for MNIST
Train a simple CNN on MNIST:
- Architecture: Conv(1→32, 3×3) → ReLU → MaxPool(2) → Conv(32→64, 3×3) → ReLU → MaxPool(2) → FC(64*7*7 → 128) → FC(128 → 10)
- Train for 5 epochs, report test accuracy
- Visualize the first-layer filters — what patterns do they detect?

### 4. Ablation: remove pooling
Remove the pooling layers and only use stride-2 convolutions. How does this affect accuracy? Parameter count?

### MI Forward Link
Write 2-3 sentences comparing the convolutional kernel's local receptive field to the attention head's content-dependent receptive field.

## Links

- [[03_deep_learning/notes/rnn-from-scratch]] — the theory note on RNN internals that this exercise implements.
- [[03_deep_learning/notes/cnn-basics]] — the theory note on CNN internals that this exercise implements.


## Links

- [[03_deep_learning/notes/rnn-from-scratch]] — the RNN cell you implement in task 1
- [[03_deep_learning/notes/cnn-basics]] — the convolution and pooling operations you use in task 3
