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


class TestLosslessness:
    """A tokenizer that cannot reproduce its input is not a tokenizer.

    The split pattern used to match words and punctuation but no whitespace on
    its own, so `findall` silently dropped newlines, tabs, repeated spaces and
    trailing spaces. The round-trip tests only used single-spaced prose, so
    they never saw it (found 2026-11-17, while writing the Phase 4 exercise).
    """

    CASES = [
        "hello  world",  # a repeated space
        "a\nb",  # a newline
        "line one\n\nline two",
        "tab\there",
        "trailing ",
        "  leading",
        "hello world \n",
        "caf\u00e9 \u2192 na\u00efve \U0001f600",  # non-ASCII, including an emoji
        "",
    ]

    def test_round_trip_is_exact_for_whitespace_and_unicode(self) -> None:
        tokenizer = BPETokenizer(vocab_size=300).train(["hello world", "hello there"])
        for text in self.CASES:
            assert tokenizer.decode(tokenizer.encode(text)) == text, repr(text)

    def test_round_trip_is_exact_for_text_it_was_trained_on_with_whitespace(self) -> None:
        corpus = ["def f(x):\n    return x  # same\n", "a b  c\td\n"]
        tokenizer = BPETokenizer(vocab_size=290).train(corpus)
        for text in corpus:
            assert tokenizer.decode(tokenizer.encode(text)) == text, repr(text)

    def test_a_larger_vocabulary_never_lengthens_the_encoding(self) -> None:
        corpus = ["the cat sat on the mat. the cat sat."] * 3
        small = BPETokenizer(vocab_size=260).train(corpus)
        large = BPETokenizer(vocab_size=300).train(corpus)
        text = corpus[0]
        assert len(large.encode(text)) <= len(small.encode(text)) < len(text.encode("utf-8"))

    def test_training_is_deterministic(self) -> None:
        corpus = ["low lower lowest", "new newer newest"]
        a = BPETokenizer(vocab_size=280).train(corpus)
        b = BPETokenizer(vocab_size=280).train(corpus)
        assert a.merges == b.merges
