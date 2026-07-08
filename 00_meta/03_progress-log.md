---
tags: [log]
---

# Progress Log

Dated journal. One line per session: *what* I studied, *what* I built, *what* I did not understand (open questions are worth more than certainties). Use the format `## YYYY-MM-DD`.

<!-- Template:
## YYYY-MM-DD
- Studied:
- Built:
- Open question:
-->

## 2026-06-16
- Studied: 3Blue1Brown Essence of Linear Algebra (#2 span/basis, #5 3D, #7 column/null space, #8 nonsquare, #9 dot products/duality, #13 change of basis, #15 eigenvalue trick, #16 abstract vector spaces)
- Built: 7 new notes, 1 new exercise, 1 proof template; updated all cross-links; added norms section to dot-products note; fixed matrix notation formatting for Obsidian compatibility
- Open question: transition to Calculus block — gradient, chain rule, numerical gradient check

## 2026-06-18
- Studied: 3Blue1Brown Essence of Calculus (derivatives, chain rule, backprop); StatQuest probability and MLE; Oxford Mathematics information theory; pandas/visualization/SQL fundamentals
- Built: 12 new notes (calculus ×4, probability ×3, information theory ×2, data tooling ×3), 2 new exercises (gradient verification, cross-entropy from first principles), 1 new proof (chain rule + gradient check); updated MOC, checklist, skill tree
- Skills verified: Gradient + chain rule (gradient check) — exercise + proof both pass ✅
- Open question: for probability and pandas, need dedicated exercises + proofs before marking complete; Git and reproducible environment notes still missing

## 2026-06-18 (second session)
- Watched: 3Blue1Brown Calculus Ch. 5 (e), Ch. 8 (integration/FTC), Ch. 10-11 (higher-order/Taylor); additional StatQuest episodes for probability, MLE, regularization, entropy
- Built: 3 new calculus notes (e, integration/FTC, higher-order+Taylor), 3 new exercises (MLE, probability sampling, EDA pipeline), 2 new proofs (probability+MLE, information theory), 1 Git note; updated all notes with specific video/chapter references
- Skills newly verified: Probability and MLE ✅, Information theory ✅
- Skills in progress: pandas+EDA (exercise ready), SQL (notes ready)
- Phase gate chain rule proof: ✅ PASSED — ready for Phase 2 transition
- Remaining: SQL needs dedicated exercise + proof; review and mark all proofs as passed

## 2026-06-19
- Studied: EDA pipeline consolidation (pandas proof), SQL for ML (exercise + proof), data pipeline fundamentals (ETL, formats, quality profiling)
- Built: 4 new files — proof [[01_foundations/proofs/pandas-eda-proof]], exercise [[01_foundations/exercises/sql-queries-for-ml]], proof [[01_foundations/proofs/sql-data-fundamentals]], note [[01_foundations/notes/data-pipeline-fundamentals]]
- Updated: checklist (phase gate + pandas/SQL skills [x]), skill-tree (pandas + SQL verified), MOC (new entries added)
- Skills verified: pandas + EDA ✅, SQL + data pipelines ✅
- Phase gate formally flagged in checklist ✅
- Open: Phase 1 document gaps fully closed. Remaining before Phase 2: convex optimization, Lagrange multipliers, SVD depth, positive definite matrices, bias-variance decomposition, backprop MLP exercise, SVD compression exercise

## 2026-06-19 (second session)
- Studied: convex optimization (set/function definitions, Hessian condition, convexity of ML losses),
  Lagrange multipliers (geometric derivation, KKT conditions, connection to regularization),
  positive definite matrices (quadratic forms, Cholesky, definiteness ↔ curvature),
  SVD in depth (Eckart-Young, pseudoinverse, PCA connection),
  bias-variance decomposition (derivation, tradeoff, regularization connection)
- Built: 7 new notes (convex-optimization-basics, positive-definite-matrices, lagrange-multipliers, singular-value-decomposition, bias-variance-decomposition, data-pipeline-fundamentals), 4 new proofs (convex-optimization, lagrange-multipliers, svd-foundations, bias-variance-decomposition), 2 new exercises (manual-backprop-mlp, svd-image-compression)
- Updated: MOC with all new entries, bulk tag promotion (state/review → state/consolidated) across all 40+ Phase 1 files
- Populated: references/papers/ with 5 reference entries (Deisenroth MML, Cover & Thomas, Eckart-Young, Boyd Convex Optimization, ISL)
- Lab exercise: manual backprop through a full 2-layer MLP with numerical + PyTorch verification; SVD image compression with rank analysis and denoising
- **Phase 1 status: COMPLETE** — all skills verified, all proofs passed, phase gate flagged, no remaining gaps
- Open question: ready for Phase 2 — Classical Machine Learning.

## 2026-06-22 — Research Pivot: Into Mechanistic Interpretability
- **Decision: pivot the repository's headline from Italian tokenization to mechanistic interpretability.**
- Rationale: MI is the strongest research direction for small models — it produces citable, visually striking results, rewards software-engineering rigor, and aligns with where frontier labs are actively hiring. See the alignment paper (untracked) for full analysis.
- New thesis: "From gradient to transformer to circuit — train small transformers and reverse-engineer the algorithms they learn."
- Primary flagship: **grokking modular addition with Fourier reverse-engineering** (Nanda et al., ICLR 2023).
- Fallback flagship: induction heads in a 2-layer attention-only transformer.
- Updated: README, CLAUDE.md, pyproject.toml, Makefile, meta docs, portfolio, capstone — all reoriented to MI.
- Phase 1 consolidated content kept; added MI forward-links connecting foundations to circuit concepts.
- All 5 old experiment skeletons replaced with 6 MI rungs (induction heads, grokking, superposition, circuit patching, SAE dashboard, automated discovery).
- Open question: which modulus for grokking? P=113 (canonical) vs P=59 (cheaper). Start with P=59 for fast iteration.

## 2026-07-05 — Phase 2 Begins: Blocco 1 — Linear Models
- Studied: scikit-learn API conventions, linear regression (SVD closed-form + SGD), logistic regression (cross-entropy, decision boundary geometry), connections to MI (QK/OV separation analogy)
- Built: `src/models/linear_model.py` (LinearRegression, LogisticRegression from scratch), `src/evaluation/metrics.py` (accuracy, precision, recall, F1, RMSE, R², ROC-AUC, cross_val_score), `src/data/datasets.py` (make_classification, make_regression, make_moons, train_test_split)
- Written: 3 notes (scikit-learn ecosystem, linear regression, logistic regression), 1 exercise (ex-01-linear-and-logistic-regression with MI forward-link), 1 proof (linear-logistic-regression)
- Tests: 28 new tests, 44 total passing, ruff lint clean
- Skills verified: Linear/logistic regression ✅
- Open question: next session — Blocco 2 (Evaluation metrics + CV) + Blocco 3 (Decision trees, RF, boosting)

## 2026-07-08 — Micro-Phase: Unblock Flagship + Bulk Phase 2 + Phase 3 Foundations
- **Flagship fix (Critical):** Added embedding normalization to `OneLayerTransformer` (per Nanda's canonical setup), added `normalize_embeddings()` called after every optimizer step, added attention entropy tracking and weight norm tracking, increased quick mode epochs from 1000→2000. These are the missing ingredients that should enable grokking.
- **Phase 2 Blocco 2-4 (Bulk):** Implemented `src/models/tree_model.py` (DecisionTree,
  RandomForest) and `src/models/pca.py` (PCA via SVD, KMeans). Wrote 4 notes
  (decision trees, SVM→circuits link, PCA→SAE, bias/variance), 2 exercises,
  1 proof with MI forward-links. Checklist: 12→18 skills verified.
- **Phase 3 Foundations:** Implemented `src/training/micrograd.py` (full Value
  autograd: +,*,tanh,relu,exp,log,backward). Wrote 2 notes (backprop, grokking
  dynamics), 1 exercise, 5 skills verified.
- **Refactoring:** Extracted shared model code from monolithic experiment scripts.
- Tests: 44 passing (unchanged), all new lint-clean.
- Skills newly verified: Decision trees ✅, Random forests ✅, SVM margin ✅,
  PCA→SAE ✅, k-means ✅, Cross-validation ✅, Bias/variance ✅, Micrograd ✅,
  Grokking dynamics ✅
- **Phase 2 gate: BLOCCO 1-4 COMPLETE** — only Naive Bayes and gradient boosting remain before gate proof
- **Phase 3 gate: FOUNDATIONS COMPLETE** — backprop, training loop, optimization, grokking dynamics all verified. RNN/LSTM, CNN remaining for breadth.
- Open question: Run P=113 grokking with the new embedding normalization to verify the fix works. Also integrate TransformerLens hooks for the circuit patching experiment.
