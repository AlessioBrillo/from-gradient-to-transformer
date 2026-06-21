"""Global seed control and deterministic execution.

Usage:
    from src.reproducibility import set_seed
    set_seed(42)
"""

import os
import random
from typing import Optional

import numpy as np


def set_seed(seed: int = 42, deterministic: bool = True) -> None:
    """Set all random seeds for reproducibility.

    Controls Python random, NumPy, PyTorch CPU/CUDA/MPS,
    and enables PyTorch deterministic algorithms where possible.

    Args:
        seed: Random seed value.
        deterministic: If True, enables torch deterministic algorithms
            (may slow execution; set False for performance runs).
    """
    random.seed(seed)
    np.random.seed(seed)

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
        torch.use_deterministic_algorithms(True, warn_only=True)
        os.environ["CUBLAS_WORKSPACE_CONFIG"] = ":4096:8"
        os.environ["PYTHONHASHSEED"] = str(seed)


def worker_init_fn(seed: Optional[int] = None) -> callable:
    """Returns a worker_init_fn for torch DataLoader reproducibility.

    Usage:
        DataLoader(..., worker_init_fn=worker_init_fn(42))
    """
    if seed is None:
        seed = 42

    def _init(worker_id: int) -> None:
        np.random.seed(seed + worker_id)
        random.seed(seed + worker_id)

    return _init


def seed_info() -> dict:
    """Report current seed state across frameworks."""
    info = {
        "python_random": "set" if random.getstate() else "unknown",
        "numpy_seed": np.random.get_state()[1][0],
    }
    try:
        import torch

        info["torch_seed"] = torch.initial_seed()
        info["torch_deterministic"] = torch.are_deterministic_algorithms_enabled()
    except ImportError:
        pass
    return info
