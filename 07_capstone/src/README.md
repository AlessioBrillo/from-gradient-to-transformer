# src/ — Capstone Source Code

Expected modules (one at a time, tested incrementally):
- `model.py` — decoder-only Transformer (embedding → RoPE → blocks → RMSNorm → unembed)
- `train.py` — training loop + checkpoint + W&B logging + seed control
- `config.py` — hyperparameter configurations for each experiment
- `analysis.py` — Fourier decomposition, progress measures, logit-lens projections
- `sae.py` — SAE training wrapper (training, activation harvesting, feature extraction)
