---
tags: [type/proof, phase/1]
state: consolidated
created: 2026-06-19
---

# Proof to myself: pandas + EDA + Visualization

**Rule:** reconstructed without looking at notes.

## What I needed to demonstrate

That I can complete an end-to-end Exploratory Data Analysis pipeline from memory: load → clean → univariate analysis → bivariate analysis → correlation analysis → feature engineering → extract and communicate actionable insights.

## What I produced from memory

### 1. Explain the EDA workflow in plain English

EDA is the systematic process of understanding a dataset before modeling. The pipeline has six stages:

**Stage 1 — Load and audit.** Read the data, check its shape, column types, missingness, and basic statistics. This answers: *What am I working with?*

**Stage 2 — Clean.** Handle missing values, fix type mismatches, drop columns that are too sparse (>50% missing), encode categorical variables. This answers: *Is the data ready for analysis?*

**Stage 3 — Univariate analysis.** Examine each variable in isolation. Histograms for continuous columns, count plots for categorical columns. This answers: *What does each column look like on its own?*

**Stage 4 — Bivariate analysis.** Cross variables against the target. Bar plots of survival rate by class, box plots of age by survival. This answers: *Which variables seem to matter?*

**Stage 5 — Correlation and feature engineering.** Compute the correlation matrix, identify the top correlates with the target. Create new features from existing ones (interactions, aggregates, domain-driven transformations). This answers: *What new signal can I extract?*

**Stage 6 — Communicate.** Distill everything into 5–7 concise, data-backed findings. This answers: *What should a stakeholder or future modeler know?*

### 2. Code from memory

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Stage 1 — Load and audit
df = sns.load_dataset("titanic")
print(df.shape)
print(df.dtypes)
print(df.head())
missing = df.isnull().sum().sort_values(ascending=False)
print(missing[missing > 0])

# Stage 2 — Clean
df_clean = df.copy()
df_clean["age"] = df_clean["age"].fillna(df_clean["age"].median())
df_clean["embarked"] = df_clean["embarked"].fillna(df_clean["embarked"].mode()[0])
df_clean = df_clean.drop(columns=["deck", "embark_town"], errors="ignore")
df_clean["sex"] = df_clean["sex"].map({"male": 0, "female": 1})
df_clean["alive"] = df_clean["alive"].map({"no": 0, "yes": 1})

# Stage 3 — Univariate
fig, axes = plt.subplots(2, 3, figsize=(15, 8))
sns.histplot(df_clean["age"], bins=30, kde=True, ax=axes[0, 0])
axes[0, 0].set_title("Age distribution")
sns.histplot(df_clean["fare"], bins=50, kde=True, ax=axes[0, 1])
axes[0, 1].set_title("Fare distribution")
sns.countplot(data=df_clean, x="pclass", ax=axes[0, 2])
axes[0, 2].set_title("Passenger class")
sns.countplot(data=df_clean, x="survived", ax=axes[1, 0])
axes[1, 0].set_title("Survival")
sns.countplot(data=df_clean, x="sex", ax=axes[1, 1])
axes[1, 1].set_title("Sex (0=Male, 1=Female)")
sns.countplot(data=df_clean, x="embarked", ax=axes[1, 2])
axes[1, 2].set_title("Embarkation port")
plt.tight_layout()

# Stage 4 — Bivariate
fig, axes = plt.subplots(2, 2, figsize=(12, 10))
sns.barplot(data=df_clean, x="pclass", y="survived", ax=axes[0, 0])
axes[0, 0].set_title("Survival rate by class")
sns.barplot(data=df_clean, x="sex", y="survived", ax=axes[0, 1])
axes[0, 1].set_title("Survival rate by sex")
sns.boxplot(data=df_clean, x="survived", y="age", ax=axes[1, 0])
axes[1, 0].set_title("Age by survival")
sns.boxplot(data=df_clean, x="pclass", y="fare", ax=axes[1, 1])
axes[1, 1].set_title("Fare by class")
plt.tight_layout()

# Stage 5 — Correlation + Feature engineering
numeric = df_clean.select_dtypes(include=[np.number])
corr = numeric.corr()
sns.heatmap(corr, annot=True, cmap="RdBu_r", center=0, fmt=".2f")
plt.title("Correlation heatmap")

top_features = corr["survived"].drop("survived").sort_values(ascending=False)
print("Top correlates with survival:\n", top_features)

df_clean["family_size"] = df_clean["sibsp"] + df_clean["parch"] + 1
df_clean["is_alone"] = (df_clean["family_size"] == 1).astype(int)
df_clean["fare_per_person"] = df_clean["fare"] / df_clean["family_size"]
df_clean["age_group"] = pd.cut(
    df_clean["age"],
    bins=[0, 12, 18, 35, 60, 100],
    labels=["child", "teen", "adult", "middle-aged", "senior"],
)

sns.barplot(data=df_clean, x="age_group", y="survived")
plt.title("Survival rate by age group")
```

### 3. Key findings I extracted

1. **Class gradient**: 1st-class survival ≈ 63%, 3rd-class ≈ 24%. Class alone explains a large fraction of outcome variance.
2. **Gender disparity**: Female survival ≈ 74%, male ≈ 19%. This is the single strongest categorical predictor.
3. **Age U-shape**: Children survived at higher rates; elderly passengers had the lowest survival.
4. **Family effect**: Solo travelers (is_alone=1) had strictly lower survival than those with 1–3 family members — companionship increased odds of rescue.
5. **Fare skew**: Fare distribution is right-skewed with a long tail. A log transform would be beneficial for any linear model.
6. **Missing data pattern**: Deck (77% missing) was uninformative and correctly dropped. Age (20% missing) required imputation but the median approximation is coarse — a model-based imputation (e.g., predicting age from title initials) would be better in production.

## Links
- [[01_foundations/notes/pandas-for-data-preparation]]
- [[01_foundations/notes/data-visualization-essentials]]
- [[01_foundations/exercises/pipeline-eda-and-visualization]]

## Outcome
- [x] Passed → check the skill in [[00_meta/02_skill-tree]]
- [ ] Retry needed (what was missing): ...
