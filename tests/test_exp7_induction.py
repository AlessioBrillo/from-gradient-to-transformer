from pathlib import Path
from unittest.mock import patch

from src.experiments.exp7_induction_scaling import main


def test_exp7_runner_runs_without_crashing():
    # Mocking arguments to ensure it runs a minimal version
    test_args = [
        "prog",
        "--seeds", "42",
        "--d-model", "16",
        "--n-layers", "1",
        "--n-heads", "2",
        "--epochs", "1"
    ]
    with patch("sys.argv", test_args):
        # We need to catch SystemExit if main() calls exit()
        try:
            main()
        except SystemExit:
            pass

    assert (Path("results") / "exp7_induction_scaling.json").exists()
