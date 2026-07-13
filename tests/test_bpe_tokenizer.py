"""Tests for the BPE tokenizer."""

from src.models.bpe_tokenizer import BPETokenizer


class TestBPETokenizer:
    def test_train_encode_decode_roundtrip(self) -> None:
        tokenizer = BPETokenizer(vocab_size=300)
        texts = [
            "hello world",
            "hello there",
            "world of hello",
            "the quick brown fox",
        ]
        tokenizer.train(texts)
        for text in texts:
            ids = tokenizer.encode(text)
            assert len(ids) > 0, f"Empty encoding for '{text}'"
            decoded = tokenizer.decode(ids)
            assert decoded == text, f"Roundtrip failed: '{text}' -> '{decoded}'"

    def test_vocab_size(self) -> None:
        tokenizer = BPETokenizer(vocab_size=260)
        tokenizer.train(["hello world this is a test"])
        assert len(tokenizer.vocab) <= 260

    def test_merges_learned(self) -> None:
        tokenizer = BPETokenizer(vocab_size=270)
        tokenizer.train(["hello world", "hello world hello"])
        assert len(tokenizer.merges) > 0

    def test_empty_text(self) -> None:
        tokenizer = BPETokenizer(vocab_size=260)
        tokenizer.train(["hello"])
        ids = tokenizer.encode("")
        assert ids == []

    def test_characters_outside_training(self) -> None:
        tokenizer = BPETokenizer(vocab_size=260)
        tokenizer.train(["hello"])
        ids = tokenizer.encode("hello!")
        assert len(ids) >= 1
        decoded = tokenizer.decode(ids)
        assert "hello" in decoded
