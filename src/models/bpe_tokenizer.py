"""Minimal BPE tokenizer from scratch."""

import re
from collections import Counter
from typing import List


def _get_stats(pairs: List[tuple]) -> Counter:
    return Counter(pairs)


def _merge(ids: List[int], pair: tuple, idx: int) -> List[int]:
    new_ids = []
    i = 0
    while i < len(ids):
        if i < len(ids) - 1 and (ids[i], ids[i + 1]) == pair:
            new_ids.append(idx)
            i += 2
        else:
            new_ids.append(ids[i])
            i += 1
    return new_ids


class BPETokenizer:
    """Byte-Pair Encoding tokenizer.

    Usage:
        tokenizer = BPETokenizer()
        tokenizer.train(["hello world", "hello there"])
        ids = tokenizer.encode("hello world")
        text = tokenizer.decode(ids)
    """

    def __init__(self, vocab_size: int = 256):
        self.vocab_size = vocab_size
        self.merges: dict[tuple, int] = {}
        self.vocab: dict[int, bytes] = {}
        self.pattern = r"""'(?:[sdmt]|ll|ve|re)| ?\w+| ?\S+"""
        self._special_tokens: dict[str, int] = {}

    def _bytes_to_ids(self, text: str) -> List[int]:
        return list(text.encode("utf-8"))

    def _ids_to_bytes(self, ids: List[int]) -> bytes:
        return b"".join(self.vocab[i] for i in ids)

    def _get_chunks(self, text: str) -> List[str]:
        return re.findall(self.pattern, text)

    def train(self, texts: List[str]) -> "BPETokenizer":
        word_freqs: Counter = Counter()
        for text in texts:
            for chunk in self._get_chunks(text):
                word_freqs[chunk] += 1

        base_vocab = 256
        num_merges = self.vocab_size - base_vocab

        splits = {word: self._bytes_to_ids(word) for word in word_freqs}

        for i in range(num_merges):
            stats: Counter = Counter()
            for word, ids in splits.items():
                freq = word_freqs[word]
                pairs = _get_stats([(ids[j], ids[j + 1]) for j in range(len(ids) - 1)])
                for pair, count in pairs.items():
                    stats[pair] += count * freq

            if not stats:
                break

            most_common = stats.most_common(1)[0][0]
            new_idx = base_vocab + i
            self.merges[most_common] = new_idx

            for word, ids in splits.items():
                splits[word] = _merge(ids, most_common, new_idx)

        # Build vocab
        self.vocab = {i: bytes([i]) for i in range(base_vocab)}
        for (p0, p1), idx in self.merges.items():
            self.vocab[idx] = self.vocab[p0] + self.vocab[p1]

        return self

    def encode(self, text: str) -> List[int]:
        chunks = self._get_chunks(text)
        ids = []
        for chunk in chunks:
            chunk_ids = self._bytes_to_ids(chunk)
            while len(chunk_ids) >= 2:
                min_pair = None
                min_idx = float("inf")
                for i in range(len(chunk_ids) - 1):
                    pair = (chunk_ids[i], chunk_ids[i + 1])
                    if pair in self.merges and self.merges[pair] < min_idx:
                        min_pair = pair
                        min_idx = self.merges[pair]
                if min_pair is None:
                    break
                chunk_ids = _merge(chunk_ids, min_pair, self.merges[min_pair])
            ids.extend(chunk_ids)
        return ids

    def decode(self, ids: List[int]) -> str:
        return self._ids_to_bytes(ids).decode("utf-8", errors="replace")
