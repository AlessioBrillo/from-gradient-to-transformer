import numpy as np


def accuracy_score(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    if y_true.shape != y_pred.shape:
        raise ValueError(f"Shape mismatch: {y_true.shape} vs {y_pred.shape}")
    return float(np.mean(y_true == y_pred))


def confusion_matrix(
    y_true: np.ndarray, y_pred: np.ndarray, labels: list[int] | None = None
) -> np.ndarray:
    if y_true.shape != y_pred.shape:
        raise ValueError(f"Shape mismatch: {y_true.shape} vs {y_pred.shape}")
    if labels is None:
        labels = sorted(
            set(int(i) for i in np.unique(y_true))
            | set(int(i) for i in np.unique(y_pred))
        )
    n = len(labels)
    label_to_idx = {label: i for i, label in enumerate(labels)}
    mat = np.zeros((n, n), dtype=np.int64)
    for t, p in zip(y_true, y_pred):
        mat[label_to_idx[int(t)], label_to_idx[int(p)]] += 1
    return mat


def precision_score(y_true: np.ndarray, y_pred: np.ndarray, pos_label: int = 1) -> float:
    cm = confusion_matrix(y_true, y_pred)
    idx = list({int(i) for i in np.unique(y_true)} | {int(i) for i in np.unique(y_pred)})
    sorted_labels = sorted(idx)
    if pos_label not in sorted_labels:
        raise ValueError(f"pos_label={pos_label} not in labels {sorted_labels}")
    pos = sorted_labels.index(pos_label)
    tp = cm[pos, pos]
    fp = cm[:, pos].sum() - tp
    return float(tp / (tp + fp)) if (tp + fp) > 0 else 0.0


def recall_score(y_true: np.ndarray, y_pred: np.ndarray, pos_label: int = 1) -> float:
    cm = confusion_matrix(y_true, y_pred)
    idx = list({int(i) for i in np.unique(y_true)} | {int(i) for i in np.unique(y_pred)})
    sorted_labels = sorted(idx)
    if pos_label not in sorted_labels:
        raise ValueError(f"pos_label={pos_label} not in labels {sorted_labels}")
    pos = sorted_labels.index(pos_label)
    tp = cm[pos, pos]
    fn = cm[pos, :].sum() - tp
    return float(tp / (tp + fn)) if (tp + fn) > 0 else 0.0


def f1_score(y_true: np.ndarray, y_pred: np.ndarray, pos_label: int = 1) -> float:
    p = precision_score(y_true, y_pred, pos_label)
    r = recall_score(y_true, y_pred, pos_label)
    return float(2 * p * r / (p + r)) if (p + r) > 0 else 0.0


def rmse(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    if y_true.shape != y_pred.shape:
        raise ValueError(f"Shape mismatch: {y_true.shape} vs {y_pred.shape}")
    return float(np.sqrt(np.mean((y_true - y_pred) ** 2)))


def mae(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    if y_true.shape != y_pred.shape:
        raise ValueError(f"Shape mismatch: {y_true.shape} vs {y_pred.shape}")
    return float(np.mean(np.abs(y_true - y_pred)))


def r2_score(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    if y_true.shape != y_pred.shape:
        raise ValueError(f"Shape mismatch: {y_true.shape} vs {y_pred.shape}")
    ss_res = np.sum((y_true - y_pred) ** 2)
    ss_tot = np.sum((y_true - np.mean(y_true)) ** 2)
    if ss_tot == 0:
        return float("nan")
    return float(1.0 - ss_res / ss_tot)


def roc_auc_score(y_true: np.ndarray, y_score: np.ndarray) -> float:
    """Compute AUC using the trapezoidal rule.

    y_score: predicted probabilities for the positive class.
    """
    if y_true.shape != y_score.shape:
        raise ValueError(f"Shape mismatch: {y_true.shape} vs {y_score.shape}")
    n_pos = int(y_true.sum())
    n_neg = len(y_true) - n_pos
    if n_pos == 0 or n_neg == 0:
        return float("nan")

    order = np.argsort(y_score)[::-1]
    y_true_sorted = y_true[order]

    tpr = [0.0]
    fpr = [0.0]
    tp, fp = 0, 0
    for i in range(len(y_true_sorted)):
        if y_true_sorted[i] == 1:
            tp += 1
        else:
            fp += 1
        tpr.append(tp / n_pos)
        fpr.append(fp / n_neg)

    return float(np.trapezoid(tpr, fpr))


def cross_val_score(
    model: object,
    X: np.ndarray,
    y: np.ndarray,
    cv: int = 5,
    metric: str = "accuracy",
) -> np.ndarray:
    """Simple k-fold cross-validation.

    model must have .fit(X, y) and .predict(X) methods.
    metric: "accuracy", "rmse", "r2", "mae"
    """
    n = len(X)
    indices = np.random.permutation(n)
    fold_sizes = np.full(cv, n // cv, dtype=int)
    fold_sizes[: n % cv] += 1
    scores = np.empty(cv)
    current = 0
    for i in range(cv):
        val_idx = indices[current : current + fold_sizes[i]]
        train_idx = np.concatenate([indices[:current], indices[current + fold_sizes[i] :]])
        current += fold_sizes[i]

        X_train, y_train = X[train_idx], y[train_idx]
        X_val, y_val = X[val_idx], y[val_idx]

        model.fit(X_train, y_train)
        y_pred = model.predict(X_val)

        if metric == "accuracy":
            scores[i] = accuracy_score(y_val, y_pred)
        elif metric == "rmse":
            scores[i] = rmse(y_val, y_pred)
        elif metric == "r2":
            scores[i] = r2_score(y_val, y_pred)
        elif metric == "mae":
            scores[i] = mae(y_val, y_pred)
        else:
            raise ValueError(f"Unknown metric: {metric}")
    return scores
