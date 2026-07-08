---
tags: [type/lesson, phase/5]
state: review
created: 2026-07-08
---

# Synthetic Dataset Construction for Circuit Tasks

## What it is
Controlled synthetic datasets are the standard tool for discovering and analyzing circuits — they isolate specific behaviors (e.g., "the model copies the previous token") by systematically varying template inputs.

## Why it exists / what problem it solves
Natural language is messy: correlations are dense, confounders are everywhere, and you can't easily isolate a single capability. Synthetic data gives you ground-truth labels for *where* the answer should come from in the input, which is what circuit analysis needs.

## How it works

### IOI (Indirect Object Identification)
Template: `"When Mary and John went to the store, John gave a drink to {B}"` (correct answer: Mary).

```python
def make_ioi_prompts(names, verbs, objects):
    prompts = []
    for A, B in itertools.permutations(names, 2):
        for verb in verbs:
            for obj in objects:
                prompts.append(
                    f"When {A} and {B} went to the store, {B} gave {obj} to"
                )
    return prompts
```

### Greater-than
Template: `"The war lasted from {year} to"` (correct answer: any year > {year}).

### Docstring (code completion)
Template: function signature + docstring, with the docstring containing the answer.

### Repeated prefix (induction heads)
Our induction heads experiment uses:
```python
text = "the cat sat on the "  # prefix
text += text                  # repeat → "the cat sat on the the cat sat on the"
```

The model must attend from the second "the" back to the first "the" — this is the induction head mechanism.

### Key design principles
1. **Controlled templates**: same syntactic structure, systematically varied slot fillers
2. **Balanced confounders**: each possible answer appears equally often in each position
3. **Clean baselines**: include control prompts that don't require the target behavior
4. **Scoring function**: define how to measure "correct" behavior (logit difference, accuracy)

## Links
- [[05_llm_engineering/notes/01-transformer-lens-hooks|TransformerLens Hooks]]
- [[05_llm_engineering/exercises/ex-03-circuit-dataset|Circuit Dataset Exercise]]
- [[src/experiments/exp1_induction_heads.py|Induction Heads Experiment]]

## Open questions
- #question Can we use LLM-generated paraphrases as naturalistic control templates?
