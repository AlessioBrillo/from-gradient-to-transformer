"""Tests for neuron_ablation module."""

import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import torch
from torch.utils.data import DataLoader, TensorDataset

from src.experiments.exp2_grokking import OneLayerTransformer
from src.experiments.neuron_ablation import (
    ablate_neurons,
    compute_neuron_importance,
    evaluate_model,
    load_checkpoint,
    run_fourier_ablation_for_comparison,
    run_neuron_ablation_sweep,
)
from src.reproducibility import set_seed


class TestLoadCheckpoint:
    def test_load_checkpoint_creates_model_and_loads_weights(self):
        set_seed(42)
        model = OneLayerTransformer(
            d_model=32,
            d_mlp=128,
            n_heads=2,
            modulus=11,
        )

        with tempfile.NamedTemporaryFile(suffix=".pt", delete=False) as f:
            checkpoint = {
                "model": model.state_dict(),
                "epoch": 100,
                "seed": 42,
            }
            torch.save(checkpoint, f.name)
            checkpoint_path = Path(f.name)

        try:
            loaded_model, loaded_checkpoint = load_checkpoint(
                checkpoint_path,
                d_model=32,
                d_mlp=128,
                n_heads=2,
                modulus=11,
            )

            assert isinstance(loaded_model, OneLayerTransformer)
            assert loaded_checkpoint["epoch"] == 100
            assert loaded_checkpoint["seed"] == 42

            for (name1, param1), (name2, param2) in zip(
                model.named_parameters(), loaded_model.named_parameters()
            ):
                assert name1 == name2
                assert torch.allclose(param1, param2)
        finally:
            checkpoint_path.unlink()


class TestAblateNeurons:
    def test_ablate_neurons_zeroes_weights(self):
        set_seed(42)
        model = OneLayerTransformer(
            d_model=32,
            d_mlp=128,
            n_heads=2,
            modulus=11,
        )

        neurons_to_ablate = [0, 1, 2]
        ablated = ablate_neurons(model, neurons_to_ablate)

        weight_0 = ablated.W_out.weight[:, 0]
        weight_1 = ablated.W_out.weight[:, 1]
        weight_2 = ablated.W_out.weight[:, 2]
        weight_3 = ablated.W_out.weight[:, 3]

        assert torch.allclose(weight_0, torch.zeros_like(weight_0))
        assert torch.allclose(weight_1, torch.zeros_like(weight_1))
        assert torch.allclose(weight_2, torch.zeros_like(weight_2))

        # Other neurons should be unchanged
        assert not torch.allclose(weight_3, torch.zeros_like(weight_3))

    def test_ablate_neurons_zeroes_bias(self):
        set_seed(42)
        model = OneLayerTransformer(
            d_model=32,
            d_mlp=128,
            n_heads=2,
            modulus=11,
        )

        neurons_to_ablate = [0, 5, 10]
        ablated = ablate_neurons(model, neurons_to_ablate)

        if ablated.W_out.bias is not None:
            assert ablated.W_out.bias[0] == 0
            assert ablated.W_out.bias[5] == 0
            assert ablated.W_out.bias[10] == 0


class TestEvaluateModel:
    def test_evaluate_model_returns_accuracy(self):
        set_seed(42)
        model = OneLayerTransformer(
            d_model=32,
            d_mlp=128,
            n_heads=2,
            modulus=11,
        )
        model.eval()

        # Create dummy validation data
        val_x = torch.randint(0, 11, (100, 2))
        val_y = (val_x[:, 0] + val_x[:, 1]) % 11
        val_dataset = TensorDataset(val_x, val_y)
        val_loader = DataLoader(val_dataset, batch_size=32, shuffle=False)

        acc = evaluate_model(model, val_loader)

        assert isinstance(acc, float)
        assert 0.0 <= acc <= 1.0


class TestComputeNeuronImportance:
    def test_compute_neuron_importance_returns_tensor(self):
        set_seed(42)
        model = OneLayerTransformer(
            d_model=32,
            d_mlp=128,
            n_heads=2,
            modulus=11,
        )
        model.eval()

        val_x = torch.randint(0, 11, (50, 2))
        val_y = (val_x[:, 0] + val_x[:, 1]) % 11
        val_dataset = TensorDataset(val_x, val_y)
        val_loader = DataLoader(val_dataset, batch_size=16, shuffle=False)

        importance = compute_neuron_importance(model, val_loader, num_samples=50)

        assert isinstance(importance, torch.Tensor)
        assert importance.shape == (128,)
        assert (importance >= 0).all()


class TestRunNeuronAblationSweep:
    def test_run_neuron_ablation_sweep_returns_steps_and_accuracies(self):
        set_seed(42)
        model = OneLayerTransformer(
            d_model=32,
            d_mlp=128,
            n_heads=2,
            modulus=11,
        )
        model.eval()

        val_x = torch.randint(0, 11, (50, 2))
        val_y = (val_x[:, 0] + val_x[:, 1]) % 11
        val_dataset = TensorDataset(val_x, val_y)
        val_loader = DataLoader(val_dataset, batch_size=16, shuffle=False)

        steps, accuracies = run_neuron_ablation_sweep(model, val_loader, num_steps=5)

        assert len(steps) == 6  # 0 to 5 inclusive
        assert len(accuracies) == 6
        assert steps[0] == 0
        assert steps[-1] == 128  # all neurons
        assert all(0.0 <= acc <= 1.0 for acc in accuracies)
        # Accuracy should generally decrease (or stay same) as more neurons ablated
        assert accuracies[0] >= accuracies[-1]


class TestRunFourierAblationForComparison:
    def test_run_fourier_ablation_returns_steps_and_accuracies(self):
        set_seed(42)
        model = OneLayerTransformer(
            d_model=32,
            d_mlp=128,
            n_heads=2,
            modulus=11,
        )
        model.eval()

        val_x = torch.randint(0, 11, (50, 2))
        val_y = (val_x[:, 0] + val_x[:, 1]) % 11
        val_dataset = TensorDataset(val_x, val_y)
        val_loader = DataLoader(val_dataset, batch_size=16, shuffle=False)

        steps, accuracies = run_fourier_ablation_for_comparison(
            model, val_loader, modulus=11, d_mlp=128, num_steps=5
        )

        assert len(steps) == 6
        assert len(accuracies) == 6
        assert steps[0] == 0
        assert all(0.0 <= acc <= 1.0 for acc in accuracies)
        assert accuracies[0] >= accuracies[-1]


class TestMainFunction:
    @patch("src.experiments.neuron_ablation.Path.exists")
    @patch("src.experiments.neuron_ablation.load_checkpoint")
    @patch("src.experiments.neuron_ablation.make_modular_addition_data")
    @patch("src.experiments.neuron_ablation.run_neuron_ablation_sweep")
    @patch("src.experiments.neuron_ablation.run_fourier_ablation_for_comparison")
    @patch("src.experiments.neuron_ablation.plt.savefig")
    @patch("json.dump")
    def test_main_runs_without_error(
        self,
            mock_json_dump,
            mock_savefig,
            mock_fourier_ablation,
            mock_neuron_ablation,
            mock_make_data,
            mock_load_checkpoint,
            mock_exists,
    ):
        from src.experiments import neuron_ablation

        mock_exists.return_value = True

        mock_model = MagicMock()
        mock_model.d_mlp = 512
        mock_model.modulus = 113
        mock_checkpoint = {"epoch": 5000}
        mock_load_checkpoint.return_value = (mock_model, mock_checkpoint)

        mock_val_dataset = MagicMock()
        mock_make_data.return_value = (MagicMock(), mock_val_dataset)

        mock_neuron_ablation.return_value = ([0, 128, 256], [1.0, 0.5, 0.0])
        mock_fourier_ablation.return_value = ([0, 56, 113], [1.0, 0.5, 0.0])

        argv_patch = [
            "neuron_ablation.py",
            "--seeds",
            "0",
            "--checkpoint-epoch",
            "5000",
        ]
        with patch("sys.argv", argv_patch):
            neuron_ablation.main()

        assert mock_load_checkpoint.called
        assert mock_make_data.called
        assert mock_neuron_ablation.called
        assert mock_fourier_ablation.called
        assert mock_savefig.called
        assert mock_json_dump.called
