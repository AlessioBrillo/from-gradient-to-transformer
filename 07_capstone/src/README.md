# src/ — micro-LLM source code

Expected modules (one at a time, tested incrementally):
- `tokenizer.py` — BPE from scratch
- `model.py` — decoder-only Transformer
- `train.py` — training loop + checkpoint + logging
- `generate.py` — sampling (temperature / top-k / top-p)
- `config.py` — hyperparameters in one place
