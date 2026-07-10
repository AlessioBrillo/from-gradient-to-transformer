---
tags: [type/lesson, phase/3, state/review]
---

# CNN Basics — Convolution, Pooling, Architecture

## Convolution operation
```
(f * g)[i, j] = Σ_m Σ_n f[i+m, j+n] · g[m, n]
```
Learnable kernel g slides over input f. Each kernel detects a local pattern.

**Key properties:**
- **Locality**: kernel size (e.g., 3×3) constrains receptive field
- **Weight sharing**: same kernel at every spatial position → translation equivariance
- **Stacking layers**: deeper layers learn higher-level features (edges → shapes → objects)

## Pooling
Max pooling: `max over 2×2 window` — downsampling + translation invariance.
Average pooling: less common since it loses edge information.

## Typical architecture
```
Input → [Conv → ReLU → Pool] × N → Flatten → Dense → Softmax
```

Key design choices:
- Kernel size (3×3 is standard, two 3×3 have same receptive field as one 5×5 with fewer params)
- Stride (default 1; > 1 downsamples instead of pooling)
- Padding (same/valid — preserve or shrink spatial dims)
- Channels (width multiplier: 64 → 128 → 256 as spatial dims halve)

## MI forward link
Convolution kernels are the closest classical analog to attention heads: each kernel learns a local pattern detector, and stacking layers builds hierarchical representations. The key difference is that convolution is **position-invariant** (same kernel at all positions) while attention is **content-aware** (attends based on token identity, not position). This makes attention strictly more expressive — and less sample-efficient, which is why CNNs still dominate in data-scarce vision tasks.

## Implementation (minimal PyTorch)
```python
class SimpleCNN(nn.Module):
    def __init__(self, in_channels=1, num_classes=10):
        super().__init__()
        self.conv1 = nn.Conv2d(in_channels, 32, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        self.pool = nn.MaxPool2d(2)
        self.fc = nn.Linear(64 * 7 * 7, num_classes)

    def forward(self, x):
        x = self.pool(torch.relu(self.conv1(x)))
        x = self.pool(torch.relu(self.conv2(x)))
        x = x.view(x.size(0), -1)
        return self.fc(x)
```
