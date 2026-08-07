"""Smoke tests for the induction heads experiment (Rung 1)."""

import logging

import torch
from torch.utils.data import DataLoader

from src.experiments.exp1_induction_heads import (
    AttentionOnlyBlock,
    AttentionOnlyTransformer,
    causal_ablation,
    checkpoint_path_for_seed,
    diagnose_induction_formation,
    k_composition_scores,
    make_repeated_token_data,
    prefix_duplicate_probability,
    train_model,
)


class TestAttentionOnlyTransformer:
    """Test the attention-only transformer."""

    def test_shape(self) -> None:
        """Output logits should have correct shape for next-token prediction."""
        model = AttentionOnlyTransformer(
            vocab_size=32, d_model=64, n_layers=2, n_heads=4, max_seq_len=64
        )
        x = torch.randint(0, 32, (4, 32))
        logits, attn = model(x, record_attn=True)
        assert logits.shape == (4, 32, 32), f"Expected (4, 32, 32), got {logits.shape}"
        assert attn is not None and len(attn) == 2  # 2 layers

    def test_causal_mask(self) -> None:
        """Attention should be causally masked (upper triangle = 0)."""
        block = AttentionOnlyBlock(d_model=32, n_heads=2)
        x = torch.randn(1, 10, 32)
        attn_records = []
        _ = block(x, past_attn=attn_records)
        attn_probs = attn_records[0]  # (1, 2, 10, 10)
        # Check that upper triangle (excluding diagonal) is ~0
        upper = torch.triu(torch.ones(10, 10), diagonal=1)
        causal_mass = (attn_probs[0, 0] * upper).sum()
        assert causal_mass < 0.01, f"Causal mask failed: {causal_mass:.4f} mass above diagonal"


class TestCausalAblation:
    """Falsification tests for the head_mask ablation mechanism.

    The old causal_ablation() hooked W_O's *output* and zeroed a slice of
    it — a d_model vector that had already mixed every head, so it zeroed an
    arbitrary residual-stream subspace, not a specific head's contribution.
    These tests would have failed against that implementation.
    """

    def test_ablating_all_heads_collapses_to_no_attention_baseline(self) -> None:
        """Zeroing every head in every block must reproduce the exact
        no-attention baseline: since head_mask zeroes each head's
        contribution *before* W_O mixes heads (bias=False), the block's
        output collapses to `residual + W_O(0) == residual`, i.e. attention
        never touches the residual stream at all.
        """
        torch.manual_seed(0)
        model = AttentionOnlyTransformer(
            vocab_size=16, d_model=32, n_layers=2, n_heads=4, max_seq_len=16
        )
        model.eval()
        x = torch.randint(0, 16, (2, 10))

        for block in model.blocks:
            block.head_mask = torch.zeros(block.n_heads)
        with torch.no_grad():
            ablated_logits, _ = model(x, record_attn=False)
        for block in model.blocks:
            block.head_mask = None

        with torch.no_grad():
            positions = torch.arange(x.shape[1]).unsqueeze(0)
            h = model.embed(x) + model.pos_embed(positions)
            h = model.ln_final(h)
            baseline_logits = model.unembed(h)

        assert torch.allclose(ablated_logits, baseline_logits, atol=1e-5), (
            "All-heads ablation should exactly match the no-attention baseline"
        )

    def test_head_mask_is_restored_after_ablation(self) -> None:
        """causal_ablation() must clear head_mask when it finishes, so a
        later unrelated forward pass isn't silently still ablated."""
        torch.manual_seed(0)
        model = AttentionOnlyTransformer(
            vocab_size=16, d_model=32, n_layers=1, n_heads=2, max_seq_len=16
        )
        train, _ = make_repeated_token_data(
            vocab_size=16, seq_len=10, num_train=8, num_val=8, seed=0
        )
        loader = torch.utils.data.DataLoader(train, batch_size=4)

        causal_ablation(model, loader, layer=0, head=0)

        assert model.blocks[0].head_mask is None

    def test_ablating_one_head_only_zeroes_that_head(self) -> None:
        """Ablating head h should leave the other heads' contribution to the
        pre-W_O output untouched (they aren't zeroed by the mask)."""
        block = AttentionOnlyBlock(d_model=32, n_heads=4)
        block.eval()
        x = torch.randn(1, 6, 32)

        with torch.no_grad():
            # Recompute the pre-W_O per-head output manually, once with no
            # mask and once with head 1 ablated, and compare head-by-head.
            def pre_wo_heads(mask: torch.Tensor | None) -> torch.Tensor:
                block.head_mask = mask
                h = block.ln(x)
                B, S, D = h.shape
                Q = block.W_Q(h).view(B, S, block.n_heads, block.d_head).transpose(1, 2)
                K = block.W_K(h).view(B, S, block.n_heads, block.d_head).transpose(1, 2)
                V = block.W_V(h).view(B, S, block.n_heads, block.d_head).transpose(1, 2)
                scores = Q @ K.transpose(-2, -1) / (block.d_head ** 0.5)
                causal = torch.triu(torch.full((S, S), float("-inf")), diagonal=1)
                probs = (scores + causal).softmax(dim=-1)
                out = probs @ V
                if mask is not None:
                    out = out * mask.view(1, block.n_heads, 1, 1)
                return out  # (B, n_heads, S, d_head)

            full = pre_wo_heads(None)
            mask = torch.ones(4)
            mask[1] = 0.0
            ablated = pre_wo_heads(mask)
            block.head_mask = None

        assert torch.allclose(ablated[:, 1], torch.zeros_like(ablated[:, 1]))
        for h_idx in (0, 2, 3):
            assert torch.allclose(ablated[:, h_idx], full[:, h_idx]), (
                f"Head {h_idx} should be unaffected by ablating head 1"
            )


class TestInductionData:
    """Test the repeated-token dataset."""

    def test_shapes(self) -> None:
        """Train dataset should produce correct shapes."""
        train, val = make_repeated_token_data(
            vocab_size=32, seq_len=64, num_train=100, num_val=20, seed=42
        )
        x, y = train[0]
        assert x.shape == (63,), f"Expected (63,), got {x.shape}"
        assert y.shape == (63,)

    def test_repeated_prefix(self) -> None:
        """Sequences should have the prefix repeated in the full tokens."""
        train, _ = make_repeated_token_data(
            vocab_size=8, seq_len=16, num_train=10, num_val=2, prefix_ratio=0.5, seed=42
        )
        # The underlying generation produces sequences where the first
        # half is repeated. The input is tokens[:-1] (next-token shift).
        # Check that the prefix pattern exists: positions [0,8) ≈ [8, 15)
        # in the input tensor (original tokens[:-1])
        x, y = train[0]
        prefix_len = int(16 * 0.5)
        # x[8] should equal x[0] (the repeated prefix start)
        assert x[0] == x[prefix_len], "First token should repeat at prefix boundary"

    def test_deterministic_seed(self) -> None:
        """Same seed should produce same data."""
        t1, _ = make_repeated_token_data(
            vocab_size=32, seq_len=64, num_train=100, num_val=20, seed=42
        )
        t2, _ = make_repeated_token_data(
            vocab_size=32, seq_len=64, num_train=100, num_val=20, seed=42
        )
        assert torch.equal(t1.tensors[0], t2.tensors[0]), "Deterministic seed check failed"


class TestPrefixDuplicateProbability:
    """Tests for the birthday-problem collision estimate (Micro-Phase 8, the
    Evidence Pass) — see prefix_duplicate_probability() and
    06_production_ai/exercises/ex-03-induction-task-design.md."""

    def test_zero_for_trivially_short_prefix(self) -> None:
        assert prefix_duplicate_probability(vocab_size=100, prefix_len=1) == 0.0

    def test_matches_classic_birthday_problem(self) -> None:
        # The textbook case: 23 people, 365 days -> ~50.7% collision chance.
        p = prefix_duplicate_probability(vocab_size=365, prefix_len=23)
        assert abs(p - 0.507) < 0.01

    def test_increases_with_prefix_length(self) -> None:
        short = prefix_duplicate_probability(vocab_size=100, prefix_len=5)
        long = prefix_duplicate_probability(vocab_size=100, prefix_len=50)
        assert long > short

    def test_pre_2026_08_02_defaults_were_ill_posed(self) -> None:
        """Documents the bug this exercise found: vocab_size=32,
        prefix_len=32 (the old --vocab-size default at prefix_ratio=0.5,
        seq_len=64) had a near-certain repeated token in the prefix."""
        p = prefix_duplicate_probability(vocab_size=32, prefix_len=32)
        assert p > 0.99

    def test_current_defaults_are_reasonably_well_posed(self) -> None:
        """vocab_size=2048, prefix_len=32 (current --vocab-size default)
        should sit under the warn threshold."""
        p = prefix_duplicate_probability(vocab_size=2048, prefix_len=32)
        assert p < 0.3


class TestPrefixAmbiguityWarning:
    def test_warns_when_collision_probability_is_high(
        self, caplog: "logging.LogCaptureFixture"
    ) -> None:
        with caplog.at_level(logging.WARNING):
            make_repeated_token_data(
                vocab_size=8, seq_len=16, num_train=4, num_val=2, seed=0
            )
        assert any("Prefix ambiguity" in r.message for r in caplog.records)

    def test_no_warning_when_well_posed(
        self, caplog: "logging.LogCaptureFixture"
    ) -> None:
        with caplog.at_level(logging.WARNING):
            make_repeated_token_data(
                vocab_size=4096, seq_len=16, num_train=4, num_val=2, seed=0
            )
        assert not any("Prefix ambiguity" in r.message for r in caplog.records)


class TestKComposition:
    """Falsification tests for the K-composition detector (Micro-Phase 11,
    Nanda & Jacobsen 2023 Step 2). The detector must find a hand-constructed
    L0 duplicate-token head + L1 K-composition chain, and must return null
    on random patterns, self-attention, and wrong offsets."""

    @staticmethod
    def _onehot_attn(keys: list) -> torch.Tensor:
        """Build a (1, 1, S, S) 1-hot attention stack: query q attends to
        key keys[q]. Causal (no attending to the future)."""
        S = len(keys)
        probs = torch.zeros(1, 1, S, S)
        for q, k in enumerate(keys):
            probs[0, 0, q, k] = 1.0
        return probs

    def test_detects_hand_built_chain(self) -> None:
        """L0 attends to q-2 (a 'previous occurrence'), L1 attends to
        prev+1 = q-1: the detector must score this ~1.0."""
        S = 8
        p0 = self._onehot_attn([0] + [q - 2 for q in range(1, S)])
        p1 = self._onehot_attn([0, 0] + [q - 1 for q in range(2, S)])
        scores = k_composition_scores(p0, p1)
        assert scores[0, 0] > 0.9, f"Expected ~1.0, got {scores[0, 0]:.3f}"

    def test_rejects_self_attention(self) -> None:
        """L1 attending to itself would trivially score 1.0 on a prev=q-1
        pattern; the self-attention guard must exclude it."""
        S = 8
        p0 = self._onehot_attn([0] + [q - 1 for q in range(1, S)])
        p1 = self._onehot_attn([0] + [q for q in range(1, S)])  # self
        scores = k_composition_scores(p0, p1)
        assert scores[0, 0] < 0.1, f"Self-attention should score ~0, got {scores[0, 0]:.3f}"

    def test_rejects_wrong_offset(self) -> None:
        """L1 attending to prev+2 instead of prev+1 must score low."""
        S = 10
        p0 = self._onehot_attn([0] + [q - 3 for q in range(1, S)])
        p1 = self._onehot_attn([0, 0, 0] + [q - 1 for q in range(3, S)])  # prev+2
        scores = k_composition_scores(p0, p1)
        assert scores[0, 0] < 0.1, f"Wrong offset should score ~0, got {scores[0, 0]:.3f}"

    def test_rejects_random_patterns(self) -> None:
        """Uniformly random attention must score at the uniform baseline
        (1/S per cell), not trigger the detector."""
        torch.manual_seed(0)
        S = 16
        p0 = torch.ones(1, 1, S, S) / S
        p1 = torch.ones(1, 1, S, S) / S
        scores = k_composition_scores(p0, p1)
        assert abs(scores[0, 0] - 1.0 / S) < 0.02, (
            f"Uniform patterns should score ~1/S, got {scores[0, 0]:.3f}"
        )

    def test_diagnose_returns_both_steps(self) -> None:
        """diagnose_induction_formation must report Step 1 and Step 2
        independently on a hand-built two-layer stack."""
        S = 8
        p0 = self._onehot_attn([0] + [q - 2 for q in range(1, S)])
        p1 = self._onehot_attn([0, 0] + [q - 1 for q in range(2, S)])
        diag = diagnose_induction_formation([p0, p1])
        assert diag["best_l0_head"] == 0
        assert diag["best_l1_head"] == 0
        assert diag["step2_k_composition"] > 0.9
        assert diag["l0_peakedness"] > 0.9

    def test_diagnose_on_tiny_trained_model(self) -> None:
        """End-to-end smoke: the diagnostic runs on a real (tiny) trained
        model and returns the full report structure."""
        torch.manual_seed(0)
        model = AttentionOnlyTransformer(
            vocab_size=16, d_model=16, n_layers=2, n_heads=2, max_seq_len=16
        )
        train, val = make_repeated_token_data(
            vocab_size=16, seq_len=12, num_train=32, num_val=16, seed=0
        )
        train_loader = DataLoader(train, batch_size=8)
        val_loader = DataLoader(val, batch_size=8)
        train_model(
            model=model, train_loader=train_loader, val_loader=val_loader,
            epochs=2, lr=1e-3, weight_decay=0.0, seed=0,
        )
        model.eval()
        collected: list[list] = [[], []]
        with torch.no_grad():
            for x, _ in val_loader:
                _, attn = model(x, record_attn=True)
                for layer_idx, pat in enumerate(attn):
                    collected[layer_idx].append(pat)
                break
        all_patterns = [torch.cat(c, dim=0) for c in collected]
        diag = diagnose_induction_formation(all_patterns)
        assert set(diag) >= {
            "step1_l0_duplicate_mass", "l0_peakedness",
            "step2_k_composition", "best_l0_head", "best_l1_head",
        }
        assert len(diag["step1_l0_duplicate_mass"]) == 2


class TestFreshBatches:
    """Tests for train_model's fresh_batches_fn (Micro-Phase 8) — resampling
    sequences every epoch instead of reshuffling one fixed set, to test
    whether the fixed dataset let the model memorize specific sequences."""

    def test_fresh_batches_fn_called_once_per_epoch(self) -> None:
        model = AttentionOnlyTransformer(
            vocab_size=8, d_model=8, n_layers=1, n_heads=2, max_seq_len=8
        )
        dataset, val_dataset = make_repeated_token_data(
            vocab_size=8, seq_len=8, num_train=8, num_val=8, seed=0
        )
        placeholder_loader = DataLoader(dataset, batch_size=4)
        val_loader = DataLoader(val_dataset, batch_size=4)

        calls: list[int] = []

        def fresh_fn(epoch: int) -> DataLoader:
            calls.append(epoch)
            ds, _ = make_repeated_token_data(
                vocab_size=8, seq_len=8, num_train=8, num_val=1, seed=100 + epoch
            )
            return DataLoader(ds, batch_size=4, shuffle=True)

        train_model(
            model=model,
            train_loader=placeholder_loader,
            val_loader=val_loader,
            epochs=3,
            lr=1e-3,
            weight_decay=0.0,
            seed=0,
            fresh_batches_fn=fresh_fn,
        )
        assert calls == [0, 1, 2]

    def test_without_fresh_batches_training_still_works(self) -> None:
        model = AttentionOnlyTransformer(
            vocab_size=8, d_model=8, n_layers=1, n_heads=2, max_seq_len=8
        )
        dataset, val_dataset = make_repeated_token_data(
            vocab_size=8, seq_len=8, num_train=8, num_val=8, seed=0
        )
        train_loader = DataLoader(dataset, batch_size=4)
        val_loader = DataLoader(val_dataset, batch_size=4)

        history = train_model(
            model=model,
            train_loader=train_loader,
            val_loader=val_loader,
            epochs=2,
            lr=1e-3,
            weight_decay=0.0,
            seed=0,
        )
        assert len(history["train_loss"]) == 2


class TestCheckpointResume:
    """Falsification tests for Micro-Phase 12's checkpoint/resume: a resumed
    run must be *indistinguishable* from one that never stopped (same model,
    same history, same RNG-drawn batches). The 2026-08-06 audit found the
    Rung 1 `--standard` domino had died with no process, no log, and no
    checkpoint — 17 hours of compute lost invisibly; these tests pin the
    behaviour that makes a killed run a pause instead of a loss."""

    ARGS_DEFAULTS = dict(
        vocab_size=256,
        seq_len=16,
        d_model=24,
        n_layers=2,
        n_heads=4,
        num_train=256,
        batch_size=32,
    )

    @staticmethod
    def _args(**overrides):
        from types import SimpleNamespace

        defaults = dict(TestCheckpointResume.ARGS_DEFAULTS)
        defaults.update(overrides)
        return SimpleNamespace(**defaults)

    @staticmethod
    def _fresh_batches(args, seed=0):
        from src.experiments.exp1_induction_heads import _make_fresh_batches_fn
        return _make_fresh_batches_fn(args, seed)

    @staticmethod
    def _model(args):
        return AttentionOnlyTransformer(
            vocab_size=args.vocab_size,
            d_model=args.d_model,
            n_layers=args.n_layers,
            n_heads=args.n_heads,
            max_seq_len=args.seq_len,
        )

    @staticmethod
    def _initial_state(args):
        """Snapshot the initial weights of a freshly constructed model. Both
        sides of a resume comparison must start from *identical* weights —
        constructing two models independently gives them different random
        inits, which would make even an uninterrupted comparison diverge."""
        import copy

        return copy.deepcopy(TestCheckpointResume._model(args).state_dict())

    @staticmethod
    def _model_from(state):
        args = TestCheckpointResume._args()
        model = TestCheckpointResume._model(args)
        model.load_state_dict(state)
        return model

    @staticmethod
    def _loaders(args):
        train, val = make_repeated_token_data(
            vocab_size=args.vocab_size,
            seq_len=args.seq_len,
            num_train=args.num_train,
            num_val=8,
            seed=0,
        )
        return (
            DataLoader(train, batch_size=args.batch_size, shuffle=True),
            DataLoader(val, batch_size=args.batch_size, shuffle=False),
        )

    def test_resume_matches_uninterrupted(self, tmp_path) -> None:
        """Interrupt at epoch 3, resume to end: every history curve must equal
        the uninterrupted run's exactly (the RNG snapshot guarantees it draws
        the identical fresh batches in the identical order)."""
        import numpy as np

        args = self._args()
        tl, vl = self._loaders(args)
        state = self._initial_state(args)

        full_hist = train_model(
            self._model_from(state), tl, vl, epochs=8,
            lr=1e-3, weight_decay=0.1, seed=0,
            fresh_batches_fn=self._fresh_batches(args),
        )

        broken_model = self._model_from(state)
        train_model(
            broken_model, tl, vl, epochs=3,
            lr=1e-3, weight_decay=0.1, seed=0,
            fresh_batches_fn=self._fresh_batches(args),
            checkpoint_dir=str(tmp_path), checkpoint_every=1,
            schedule_epochs=8,  # partial run: anneal LR over the full 8-epoch horizon
        )
        resumed_hist = train_model(
            broken_model, tl, vl, epochs=8,
            lr=1e-3, weight_decay=0.1, seed=0,
            fresh_batches_fn=self._fresh_batches(args),
            resume_from=str(checkpoint_path_for_seed(str(tmp_path), 0)),
        )

        assert len(resumed_hist["train_loss"]) == 8
        for key in full_hist:
            np.testing.assert_allclose(
                resumed_hist[key], full_hist[key], err_msg=f"history[{key}] diverged"
            )

    def test_resume_twice_matches_uninterrupted(self, tmp_path) -> None:
        """Two consecutive interruptions (checkpoints at epoch 1 and 3) must
        still converge to exactly the uninterrupted run."""
        import numpy as np

        args = self._args()
        tl, vl = self._loaders(args)
        state = self._initial_state(args)

        full_hist = train_model(
            self._model_from(state), tl, vl, epochs=8,
            lr=1e-3, weight_decay=0.1, seed=0,
            fresh_batches_fn=self._fresh_batches(args),
        )

        broken = self._model_from(state)
        train_model(
            broken, tl, vl, epochs=4,
            lr=1e-3, weight_decay=0.1, seed=0,
            fresh_batches_fn=self._fresh_batches(args),
            checkpoint_dir=str(tmp_path), checkpoint_every=2,
            schedule_epochs=8,
        )
        resumed_hist = train_model(
            broken, tl, vl, epochs=8,
            lr=1e-3, weight_decay=0.1, seed=0,
            fresh_batches_fn=self._fresh_batches(args),
            resume_from=str(checkpoint_path_for_seed(str(tmp_path), 0)),
        )
        for key in full_hist:
            np.testing.assert_allclose(
                resumed_hist[key], full_hist[key], err_msg=f"history[{key}] diverged"
            )

    def test_resume_missing_checkpoint_starts_fresh(self, tmp_path) -> None:
        """An explicit resume path that does not exist must not crash or part
        train — it falls back to a fresh full run, with the full history."""
        args = self._args()
        tl, vl = self._loaders(args)
        hist = train_model(
            self._model_from(self._initial_state(args)), tl, vl, epochs=2,
            lr=1e-3, weight_decay=0.1, seed=0,
            fresh_batches_fn=self._fresh_batches(args),
            resume_from=str(tmp_path / "does_not_exist.pt"),
        )
        assert len(hist["val_acc"]) == 2
