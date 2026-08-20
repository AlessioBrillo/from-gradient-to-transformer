"""Global seed control and deterministic execution.

Ensures reproducible experiments across Python random, NumPy, and PyTorch.
Every experiment script should call set_seed() at entry.

Usage:
    from src.reproducibility import set_seed
    set_seed(42)
"""

import os
import random

import numpy as np


def set_seed(seed: int = 42, deterministic: bool = True) -> None:
    """Set all random seeds for reproducibility.

    Controls Python random, NumPy, PyTorch CPU/CUDA/MPS, and enables PyTorch
    deterministic algorithms where possible.

    Args:
        seed: Random seed value.
        deterministic: If True, enables torch deterministic algorithms
            (may slow execution; set False for performance runs).
    """
    random.seed(seed)
    np.random.seed(seed)
    os.environ["PYTHONHASHSEED"] = str(seed)

    try:
        import torch
    except ImportError:
        return

    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)

    # MPS (Apple Silicon) support
    if hasattr(torch, "mps") and torch.mps.is_available():
        torch.mps.manual_seed(seed)

    if deterministic:
        try:
            torch.use_deterministic_algorithms(True, warn_only=True)
        except AttributeError:
            pass  # older PyTorch version
        os.environ["CUBLAS_WORKSPACE_CONFIG"] = ":4096:8"
