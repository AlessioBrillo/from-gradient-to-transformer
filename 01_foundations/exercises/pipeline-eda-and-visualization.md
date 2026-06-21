---
tags: [type/exercise, phase/1, state/consolidated]
skill: pandas + EDA + visualization
state: consolidated
created: 2026-06-18
---

> **Series**: [StatQuest — Histograms](https://youtu.be/qBigTkBLU6g) | [Boxplots](https://youtu.be/fHLhBnmwUM0) | [Bar Charts](https://youtu.be/RiEZ_hEf96A)
>
> **Practice datasets**: [seaborn built-in datasets](https://github.com/mwaskom/seaborn-data) | [Kaggle — Titanic](https://www.kaggle.com/c/titanic)

## Goal / skill it demonstrates
Complete an end-to-end EDA pipeline: load → clean → explore → visualize → extract insights. This is the skill you use on every new dataset before training a model.

## Setup

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
```

## Part 1 — Load and inspect

```python
# Load the Titanic dataset from seaborn
df = sns.load_dataset("titanic")

# Initial inspection
print("Shape:", df.shape)
print("\nDtypes:\n", df.dtypes)
print("\nFirst 5 rows:\n", df.head())
print("\nMissing values:\n", df.isnull().sum().sort_values(ascending=False))
print("\nStatistical summary:\n", df.describe(include='all'))
```

## Part 2 — Clean

```python
# Check missing data
missing_pct = df.isnull().mean().sort_values(ascending=False) * 100
print("Missing %:\n", missing_pct[missing_pct > 0])

# Strategy:
# - age: fill with median (skewed distribution)
# - embarked: fill with mode (single missing value)
# - deck: too many missing, drop column
# - embark_town: same as embarked, keep only one

df_clean = df.copy()
df_clean["age"] = df_clean["age"].fillna(df_clean["age"].median())
df_clean["embarked"] = df_clean["embarked"].fillna(df_clean["embarked"].mode()[0])
df_clean = df_clean.drop(columns=["deck", "embark_town"], errors="ignore")

# Convert categorical columns
df_clean["sex"] = df_clean["sex"].map({"male": 0, "female": 1})
df_clean["alive"] = df_clean["alive"].map({"no": 0, "yes": 1})

print(f"\nMissing after cleaning:\n{df_clean.isnull().sum().max()}")
```

## Part 3 — Univariate analysis

```python
fig, axes = plt.subplots(2, 3, figsize=(15, 8))

# Distribution of numeric columns
sns.histplot(df_clean["age"], bins=30, kde=True, ax=axes[0, 0])
axes[0, 0].set_title("Age distribution")

sns.histplot(df_clean["fare"], bins=50, kde=True, ax=axes[0, 1])
axes[0, 1].set_title("Fare distribution")

sns.countplot(data=df_clean, x="pclass", ax=axes[0, 2])
axes[0, 2].set_title("Passenger class")

sns.countplot(data=df_clean, x="survived", ax=axes[1, 0])
axes[1, 0].set_title("Survival (0 = No, 1 = Yes)")

sns.countplot(data=df_clean, x="sex", ax=axes[1, 1])
axes[1, 1].set_title("Sex (0 = Male, 1 = Female)")

sns.countplot(data=df_clean, x="embarked", ax=axes[1, 2])
axes[1, 2].set_title("Embarkation port")

plt.tight_layout()
```

## Part 4 — Bivariate analysis

```python
fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# Survival by class
sns.barplot(data=df_clean, x="pclass", y="survived", ax=axes[0, 0])
axes[0, 0].set_title("Survival rate by class")

# Survival by sex
sns.barplot(data=df_clean, x="sex", y="survived", ax=axes[0, 1])
axes[0, 1].set_title("Survival rate by sex")

# Age distribution by survival
sns.boxplot(data=df_clean, x="survived", y="age", ax=axes[1, 0])
axes[1, 0].set_title("Age by survival")

# Fare by class
sns.boxplot(data=df_clean, x="pclass", y="fare", ax=axes[1, 1])
axes[1, 1].set_title("Fare by class")

plt.tight_layout()
```

## Part 5 — Correlation analysis

```python
numeric_cols = df_clean.select_dtypes(include=[np.number]).columns
corr_matrix = df_clean[numeric_cols].corr()

plt.figure(figsize=(10, 8))
sns.heatmap(corr_matrix, annot=True, cmap="RdBu_r", center=0, fmt=".2f")
plt.title("Correlation heatmap")

# Key findings
print("Top features correlated with survival:")
surv_corr = corr_matrix["survived"].sort_values(ascending=False)
print(surv_corr.drop("survived"))
```

## Part 6 — Feature engineering

```python
# Create new features
df_clean["family_size"] = df_clean["sibsp"] + df_clean["parch"] + 1
df_clean["is_alone"] = (df_clean["family_size"] == 1).astype(int)
df_clean["fare_per_person"] = df_clean["fare"] / df_clean["family_size"]

# Age groups
df_clean["age_group"] = pd.cut(df_clean["age"],
                                bins=[0, 12, 18, 35, 60, 100],
                                labels=["child", "teen", "adult", "middle-aged", "senior"])

# Survival by age group
fig, axes = plt.subplots(1, 2, figsize=(12, 4))
sns.barplot(data=df_clean, x="age_group", y="survived", ax=axes[0])
axes[0].set_title("Survival by age group")

sns.barplot(data=df_clean, x="is_alone", y="survived", ax=axes[1])
axes[1].set_title("Survival: alone vs with family")
```

## Part 7 — Summary of insights

```
Key findings from Titanic EDA:
1. Class mattered: 1st class survival ≈ 63%, 3rd class ≈ 24%
2. Gender mattered: female survival ≈ 74%, male ≈ 19%
3. Children survived at higher rates than adults
4. Passengers traveling alone had lower survival rates
5. Fare was highly skewed — log transform may help modeling
6. Age has ~20% missing — imputation with median is rough but functional
7. Deck column had too much missing data (77%) to be useful
```

## What I learned doing it

The EDA pipeline is formulaic but each dataset has unique quirks. The Titanic dataset is small enough to iterate quickly but rich enough to demonstrate all major patterns: missing data handling, categorical encoding, correlation analysis, and feature engineering.

The most important takeaway: **always check missing data first**. The deck column (77% missing) would silently break a model if not handled. The age column (20% missing) needs imputation. These decisions cascade into model quality.

## Links
- [[01_foundations/notes/pandas-for-data-preparation]]
- [[01_foundations/notes/data-visualization-essentials]]

## Linked skill
- [[00_meta/02_skill-tree]] → item: pandas + EDA + visualization
