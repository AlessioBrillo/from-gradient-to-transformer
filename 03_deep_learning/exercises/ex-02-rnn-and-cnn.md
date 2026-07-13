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

## Solution

### 1. RNN for sine wave prediction
```python
import torch, numpy as np, matplotlib.pyplot as plt
from torch import nn

def make_sine_data(T=200, seq_len=10):
    t = torch.linspace(0, 8 * np.pi, T)
    x = torch.sin(t)
    xs, ys = [], []
    for i in range(T - seq_len):
        xs.append(x[i:i+seq_len])
        ys.append(x[i+seq_len])
    return torch.stack(xs).unsqueeze(-1), torch.stack(ys).unsqueeze(-1)

class SimpleRNN(nn.Module):
    def __init__(self, hidden=32):
        super().__init__()
        self.rnn = nn.RNN(1, hidden, batch_first=True, nonlinearity="tanh")
        self.fc = nn.Linear(hidden, 1)
    def forward(self, x):
        out, _ = self.rnn(x)
        return self.fc(out[:, -1, :])

X, y = make_sine_data(200, seq_len=10)
model = SimpleRNN()
opt = torch.optim.Adam(model.parameters(), lr=0.01)
losses = []
for _ in range(500):
    opt.zero_grad()
    loss = nn.MSELoss()(model(X), y)
    loss.backward(); opt.step(); losses.append(loss.item())
# Try seq_len=50: gradients vanish and loss plateaus above 0.1
```

### 2. Fixed-window baseline
```python
# Use last 5 points as features for a linear model
window = 5
X_lin = torch.stack([x[i:i+window] for i in range(T - window - 1)]).squeeze(-1)
y_lin = torch.stack([x[i+window] for i in range(T - window - 1)]).squeeze(-1)
lin = nn.Linear(window, 1)
opt = torch.optim.SGD(lin.parameters(), lr=0.01)
for _ in range(500):
    opt.zero_grad(); loss = nn.MSELoss()(lin(X_lin), y_lin)
    loss.backward(); opt.step()
# Simpler/faster but cannot learn sequential structure beyond the window size
```

### 3. CNN for MNIST
```python
from torchvision import datasets, transforms

class SimpleCNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv = nn.Sequential(
            nn.Conv2d(1, 32, 3), nn.ReLU(), nn.MaxPool2d(2),
            nn.Conv2d(32, 64, 3), nn.ReLU(), nn.MaxPool2d(2),
        )
        self.fc = nn.Sequential(
            nn.Linear(64 * 5 * 5, 128), nn.ReLU(),
            nn.Linear(128, 10)
        )
    def forward(self, x):
        x = self.conv(x).view(x.size(0), -1)
        return self.fc(x)

train_loader = torch.utils.data.DataLoader(
    datasets.MNIST("data", train=True, download=True,
                   transform=transforms.ToTensor()),
    batch_size=64, shuffle=True)
test_loader = torch.utils.data.DataLoader(
    datasets.MNIST("data", train=False, transform=transforms.ToTensor()),
    batch_size=1024)

device = "cuda" if torch.cuda.is_available() else "cpu"
model = SimpleCNN().to(device)
opt = torch.optim.Adam(model.parameters(), lr=0.001)
for epoch in range(5):
    for x, y in train_loader:
        opt.zero_grad()
        nn.functional.cross_entropy(model(x.to(device)), y.to(device)).backward()
        opt.step()
# Expected: ~99% test accuracy after 5 epochs
```

### 4. Ablation: stride instead of pooling
Replace `MaxPool2d(2)` with `nn.Conv2d(32, 32, 3, stride=2)` — parameter count increases (learnable instead of static), accuracy similar but training slower.

### MI Forward Link
A convolutional kernel's receptive field is fixed by kernel size — it applies the same learned pattern everywhere, independent of content. An attention head's receptive field is dynamic: QK dot products determine which positions are attended based on the actual input content. This content-dependent routing is what makes transformers more flexible than CNNs for language, where the relevant context varies per token.

## Links

- [[03_deep_learning/notes/rnn-from-scratch]] — the theory note on RNN internals that this exercise implements.
- [[03_deep_learning/notes/cnn-basics]] — the theory note on CNN internals that this exercise implements.
