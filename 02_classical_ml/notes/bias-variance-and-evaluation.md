---
tags: [phase/2, note, state/review]
MI-forward-link: "The bias/variance tradeoff maps to understanding memorization vs. generalization in grokking. Grokking's three phases correspond to moving from high-variance (memorization) to optimal bias/variance (generalization)."
---

# Bias/Variance and Evaluation — Notes

## Bias-Variance Decomposition
Expected test error = Bias² + Variance + Irreducible Error

For a regression model f̂ trained on dataset D:
- **Bias²**: Error from approximating a complex reality with a simpler model. High bias → underfitting.
- **Variance**: Sensitivity to the particular training set. High variance → overfitting.
- **Irreducible**: Noise in the data itself.

## Learning Curves
- High bias: training error plateaus high, validation error plateaus at similar high level
- High variance: training error near 0, validation error much higher (gap)

## Cross-Validation
k-fold CV: split data into k folds, train on k-1, validate on remaining, repeat k times.
- Stratified: preserve class proportions in each fold
- Grouped: ensure same group (e.g., patient) doesn't appear in train and val

## Metrics Guide
- **Classification**: accuracy (balanced), precision/recall/F1 (imbalanced), ROC-AUC (ranking)
- **Regression**: RMSE (same units as target), MAE (robust to outliers), R² (variance explained)

## Data Leakage
Train/test contamination: information from the test set leaks into training.

Common sources:
- Scaling before split (fit scaler on full data, then split)
- Feature engineering using target statistics
- Temporal leakage (using future data to predict past)

## MI Forward Link
The grokking phenomenon is a training-dynamics manifestation of the bias-variance tradeoff:
- Phase 1 (memorization): high variance (model fits each training example)
- Phase 2 (circuit formation): variance decreases, bias decreases
- Phase 3 (cleanup): optimal bias/variance balance through weight decay pruning

This is why weight decay is critical for grokking: it directly penalizes high-variance solutions.
