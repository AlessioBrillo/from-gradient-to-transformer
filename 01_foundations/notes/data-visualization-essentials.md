---
tags: [type/lesson, phase/1, state/review]
state: review
created: 2026-06-18
---

> **Series**: [StatQuest — Histograms, Clearly Explained](https://youtu.be/qBigTkBLU6g) | [StatQuest — Boxplots, Clearly Explained](https://youtu.be/fHLhBnmwUM0) | [StatQuest — Bar Charts Are Better Than Pie Charts](https://youtu.be/RiEZ_hEf96A)
>
> **Also**: [StatQuest — QQ Plots](https://youtu.be/okjYjClSjOg) | [StatQuest — R-squared Explained](https://youtu.be/2AQKmw14mHM)

## What it is
Data visualization is the graphical representation of data to reveal patterns, outliers, distributions, and relationships that summary statistics alone cannot capture. The standard Python stack is matplotlib (low-level) + seaborn (high-level statistical plots).

## Why it exists / what problem it solves
You cannot build a good model without understanding your data. EDA (Exploratory Data Analysis) is the process of visually inspecting data before modeling.
A well-chosen chart can reveal skewed distributions, missing data patterns, correlations, interactions, and data quality issues that no statistical test will flag.
In production, visualizations communicate model behavior to stakeholders who do not read confusion matrices.

## How it works

### The three essential chart types

**1. Distribution charts — understanding a single variable.**
- Histogram: bin the range and count frequencies. Choose bins wisely (Sturges' rule: k ≈ log₂n + 1).
- KDE: smooth density estimate, useful for comparing distributions across groups.
- Box plot: median, quartiles, outliers. Compact summary for comparing many groups.

```python
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

# Sample data
np.random.seed(42)
df = pd.DataFrame({
    "value": np.concatenate([np.random.normal(0, 1, 800), np.random.normal(3, 0.5, 200)]),
    "group": (["A"] * 500) + (["B"] * 500),
})

fig, axes = plt.subplots(1, 3, figsize=(15, 4))

# Histogram
axes[0].hist(df["value"], bins=30, edgecolor="white")
axes[0].set_title("Histogram")

# KDE
sns.kdeplot(data=df, x="value", hue="group", ax=axes[1])
axes[1].set_title("KDE by group")

# Box plot
sns.boxplot(data=df, x="group", y="value", ax=axes[2])
axes[2].set_title("Box plot")

plt.tight_layout()
```

**2. Relationship charts — understanding pairs of variables.**
- Scatter plot: bivariate relationship. Always add alpha transparency for dense data.
- Pair plot (seaborn `pairplot`): all pairwise relationships in one figure. The first thing to run after loading a new dataset.
- Heatmap (correlation matrix): color-coded pairwise correlations.

```python
# Scatter plot with regression line
sns.regplot(data=df, x="value", y="value + np.random.randn(1000) * 0.5", scatter_kws={"alpha": 0.3})
plt.title("Scatter plot + regression line")

# Correlation heatmap
iris = sns.load_dataset("iris")
corr = iris.select_dtypes(include=[np.number]).corr()
sns.heatmap(corr, annot=True, cmap="RdBu_r", center=0)
plt.title("Correlation heatmap")
```

**3. Comparison charts — comparing across categories.**
- Bar plot: mean/median/sum per category with error bars.
- Grouped bar plot: cross-category comparison with a second grouping variable.

```python
# Bar plot with error bars
sns.barplot(data=df, x="group", y="value", capsize=0.1)
plt.title("Group comparison with error bars")
```

### EDA workflow
1. `df.head()`, `df.info()`, `df.describe()` — numerical summary.
2. `sns.pairplot(df)` — all pairwise relationships (be careful with many columns — limit to top 5-6).
3. `df.hist(bins=50, figsize=(15, 10))` — all univariate distributions.
4. For each categorical column: box plot or bar plot vs target.
5. `sns.heatmap(df.corr())` — correlation structure.

### Common pitfalls
- **Overplotting**: too many points on a scatter plot. Fix: alpha, sampling, or hexbin.
- **Mismatched scales**: comparing groups with vastly different sizes using raw counts. Fix: use proportions or density.
- **3D charts**: almost never useful. Stick to 2D.
- **Cherry-picked axes**: starting y at a non-zero value to exaggerate differences. Fix: always include zero for bar charts.

## Links
- [[01_foundations/notes/pandas-for-data-preparation|pandas for Data Preparation]]
- [[01_foundations/notes/probability-basics-for-ml|Probability Basics for ML]]

## Insight
The most underrated visualization in EDA is the **scatter plot with color encoding**. Plot your two most important features on x and y, color by the target variable. This single chart often reveals: the separability of classes, whether the problem is linearly separable, whether there are outliers, whether the data lies on a low-dimensional manifold. If you only make one chart, make this one.
