---
tags: [phase/6, research/experiment, protocol, grokking]
created: 2026-08-21
---

# GPU Colab Execution Protocol — P=113 Grokking 3-Seed Run

## Purpose

Execute the canonical P=113 grokking run (3 seeds, 5000 epochs each) on Colab GPU. This is the primary flagship experiment that has never run on GPU in this repository's history.

## Notebook

`notebooks/colab_grokking_full_run.ipynb` — hardened for 3-seed execution with checkpointing, manifest generation, and figure export.

## Pre-flight Checklist

- [ ] Notebook uploaded to Colab
- [ ] Runtime → Change runtime type → GPU (A100 preferred, T4 acceptable)
- [ ] Colab Pro/Pro+ if available (longer runtime, A100 access)
- [ ] Google Drive mounted for checkpoint persistence (`/content/drive/MyDrive/from-gradient-to-transformer/`)
- [ ] Repository cloned in Colab: `!git clone https://github.com/AlessioBrillo/from-gradient-to-transformer.git`

## Execution Steps

### 1. Environment Setup (Colab cell)

```python
import sys
sys.path.insert(0, '/content/from-gradient-to-transformer')

# Install deps (uv not available in Colab, use pip)
!pip install -q torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
!pip install -q numpy matplotlib tqdm

# Verify GPU
import torch
print(f"CUDA available: {torch.cuda.is_available()}")
print(f"GPU: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU'}")
```

### 2. Run 3-Seed Experiment (Colab cell)

```python
# Run the experiment module directly with --seeds flag
import subprocess
result = subprocess.run([
    sys.executable, '-m', 'src.experiments.exp2_grokking',
    '--seeds', '0,1,2',
    '--modulus', '113',
    '--epochs', '5000',
    '--d-model', '128',
    '--d-mlp', '512',
    '--n-heads', '4',
    '--weight-decay', '1.0',
    '--train-fraction', '0.3',
    '--batch-size', '512',
    '--checkpoint-dir', '/content/drive/MyDrive/from-gradient-to-transformer/checkpoints',
    '--checkpoint-every', '500',
    '--wandb',  # optional, if W&B configured
], cwd='/content/from-gradient-to-transformer', capture_output=True, text=True, timeout=18000)

print(result.stdout)
if result.stderr:
    print("STDERR:", result.stderr)
print(f"Exit code: {result.returncode}")
```

### 3. Verify Outputs (Colab cell)

```python
# Check manifest exists
import json
from pathlib import Path

manifest_path = Path('/content/from-gradient-to-transformer/results/exp2_grokking.json')
if manifest_path.exists():
    with open(manifest_path) as f:
        manifest = json.load(f)
    print("Manifest keys:", manifest.keys())
    print("Seeds:", manifest.get('seeds'))
    print("Aggregate:", manifest.get('aggregate'))
else:
    print("MANIFEST NOT FOUND")

# Check figures
figures_dir = Path('/content/from-gradient-to-transformer/figures')
for f in figures_dir.glob('exp2_*'):
    print(f"Figure: {f.name} ({f.stat().st_size} bytes)")

# Check checkpoints
ckpt_dir = Path('/content/drive/MyDrive/from-gradient-to-transformer/checkpoints')
for f in ckpt_dir.glob('exp2_*'):
    print(f"Checkpoint: {f.name} ({f.stat().st_size} bytes)")
```

### 4. Download Artifacts (Local machine)

```bash
# From local terminal, after Colab run completes:
# 1. Download checkpoints from Google Drive
# 2. Download results/exp2_grokking.json
# 3. Download figures/exp2_*.png
# 4. Place in local repo:
#    - checkpoints/exp2_seed{0,1,2}_epoch*.pt
#    - results/exp2_grokking.json
#    - figures/exp2_grokking_curve.png
#    - figures/exp2_fourier_weights.png
#    - figures/exp2_frequency_ablation.png
#    - figures/exp2_progress_measures.png
```

## Expected Runtime

| Config | Est. Time (A100) | Est. Time (T4) |
|--------|------------------|----------------|
| 1 seed, 5000 epochs | ~19 min | ~57 min |
| 3 seeds, sequential | ~57 min | ~3 h |
| 3 seeds, parallel (3 runtimes) | ~19 min | ~57 min |

**Budget**: 3 hours max on T4 (Colab free tier limit). Use 3 parallel Colab tabs if needed.

## OOM Handling

If `batch_size=512` causes OOM:
1. Reduce to `batch_size=256`
2. Log the change in the run notes
3. Re-run from last checkpoint (checkpointing every 500 epochs)
4. Update manifest with actual batch size used

## Manifest Schema

The `--seeds` flag produces `results/exp2_grokking.json` with:

```json
{
  "experiment": "exp2_grokking",
  "seeds": [0, 1, 2],
  "args": { ...config... },
  "per_seed_metrics": [
    {
      "final_val_acc": 1.0,
      "generalization_epoch": 1208,
      "final_fourier_sparsity": 0.079,
      "k_90_percent": 93,
      "k_99_percent": 111,
      "total_mass_top_k": 0.95
    },
    ...
  ],
  "aggregate": {
    "final_val_acc": {"mean": 1.0, "std": 0.0, "min": 1.0, "max": 1.0, "n": 3.0},
    "generalization_epoch": {"mean": 1208, "std": 117, "min": 1048, "max": 1326, "n": 3.0},
    "k_99_percent": {"mean": 111, "std": 0, "min": 111, "max": 111, "n": 3.0},
    ...
  },
  "wall_clock_seconds": 3420,
  "device": "cuda",
  "n_parameters": 123456,
  "git_sha": "abc123..."
}
```

## Verification (Local)

After downloading artifacts:

```bash
# Verify manifest matches RESULTS.md tags
uv run python -m src.results verify

# Should pass with 0 errors
```

## Rollback / Recovery

- Checkpoints saved every 500 epochs to Google Drive
- If Colab session dies: restart notebook, resume from `--resume` flag (auto-detects latest checkpoint in `--checkpoint-dir`)
- If all 3 seeds fail: document failure mode, open issue, proceed to Row 3 (neuron ablation on existing CPU checkpoints)

## Contacts

- Primary: Alessio Brillo (repository owner)
- Issues: GitHub Issues (AlessioBrillo/from-gradient-to-transformer)