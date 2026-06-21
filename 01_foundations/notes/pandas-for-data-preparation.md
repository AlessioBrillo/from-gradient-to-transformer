---
tags: [type/lesson, phase/1, state/consolidated]
state: consolidated
created: 2026-06-18
---

> **Series**: [StatQuest — One-Hot, Label, Target and K-Fold Target Encoding](https://youtu.be/589nCGeWG1w) | [StatQuest — Logs, Clearly Explained](https://youtu.be/VSi0Z04fWj0)
>
> **Practice**: [Kaggle — Pandas Micro-Course](https://www.kaggle.com/learn/pandas)

## What it is
pandas is a Python library for tabular data manipulation built on top of NumPy, providing the DataFrame — a column-oriented, labeled, 2D data structure with row and column indices.

## Why it exists / what problem it solves
Raw data is never clean enough to feed into a model. Real-world pipelines require: filtering rows that meet criteria, computing grouped statistics, joining multiple tables, handling missing values, and transforming columns. pandas provides a unified, expressive API for all of these operations, making it the universal data preparation tool in the Python ML ecosystem.

## How it works

### The DataFrame
A DataFrame is a collection of Series (columns) with a shared index. Every operation in pandas should be thought of as operating on columns (vectorized) — not looping over rows.

```python
import pandas as pd
import numpy as np

# Create from dict
df = pd.DataFrame({
    "name": ["Alice", "Bob", "Charlie", "Diana", "Eve"],
    "age": [25, 30, 35, 28, None],
    "salary": [50000, 60000, 70000, 55000, 65000],
    "department": ["Eng", "Eng", "Mkt", "Mkt", "Eng"],
})

print(df.head())
```

### The pipe pattern — chain operations
The idiomatic way to write pandas: start with the data, pipe through transformations.

```python
result = (
    df
    .query("age > 25")                           # filter rows
    .groupby("department")                       # group
    .agg({"salary": ["mean", "std", "count"]})   # aggregate
    .round(2)                                    # format
)
```

### Core operations

**Filtering:**
```python
# Boolean indexing
df_engineers = df[df["department"] == "Eng"]
df_senior = df[df["age"] >= 30]

# query() — cleaner for complex conditions
df.query("age >= 30 and department == 'Eng'")
```

**Groupby + Aggregation:**
```python
# Single aggregation per column
df.groupby("department")["salary"].mean()

# Multiple aggregations
df.groupby("department").agg({
    "salary": ["mean", "std", "min", "max"],
    "age": "mean",
})
```

**Handling missing values:**
```python
# Check for nulls
df.isnull().sum()

# Fill or drop
df["age"] = df["age"].fillna(df["age"].median())  # impute with median
df_clean = df.dropna()  # drop rows with any null
```

**Joins (merging):**
```python
# SQL-style joins
left = pd.DataFrame({"id": [1, 2, 3], "name": ["A", "B", "C"]})
right = pd.DataFrame({"id": [1, 2, 4], "score": [90, 80, 95]})

inner = pd.merge(left, right, on="id", how="inner")  # only matching
left_j = pd.merge(left, right, on="id", how="left")  # all left rows
outer = pd.merge(left, right, on="id", how="outer")  # all rows
```

**Applying functions:**
```python
# Apply to each row (axis=1) or each column (axis=0)
df["salary_normalized"] = df.groupby("department")["salary"].transform(
    lambda x: x / x.mean()
)

# Vectorized operations (preferred over apply)
df["salary_bucket"] = pd.cut(df["salary"], bins=[0, 55000, 65000, 1e6], labels=["junior", "mid", "senior"])
```

### The missing data trap
pandas operations behave differently depending on the dtypes involved. A column of mixed types becomes dtype `object`, which disables all fast paths. Always check `df.dtypes` after loading data and cast explicitly.

### pandas workflow checklist
1. `df.info()` — inspect dtypes and null counts first.
2. `df.describe()` — statistical summary of numerical columns.
3. `df["col"].value_counts()` — cardinality of categorical columns.
4. `df.isnull().sum().sort_values(ascending=False)` — find missing data.
5. Fix types, impute nulls, drop duplicates, filter irrelevant columns.

## Links
- [[01_foundations/notes/data-visualization-essentials|Data Visualization Essentials]]
- [[01_foundations/notes/sql-for-data-pipelines|SQL for Data Pipelines]]

## Insight
pandas and SQL are complementary tools for the same task: manipulating tabular data. SQL is declarative (you say *what* to get), pandas is imperative (you say *how* to get it). The mental model is the same: filter → group → aggregate → join. If you think about data manipulation in terms of "what would this SQL query look like?", pandas becomes intuitive.
