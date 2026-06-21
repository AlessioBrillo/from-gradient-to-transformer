---
tags: [type/lesson, phase/1]
state: consolidated
created: 2026-06-19
---

# Data Pipeline Fundamentals

> **Resources**: [Python Data Science Handbook — VanderPlas Ch. 5](https://jakevdp.github.io/PythonDataScienceHandbook/) | [DuckDB Documentation](https://duckdb.org/docs/) — for Parquet/CSV/JSON in-process analytics | [Parquet Format Overview](https://parquet.apache.org/docs/)

## What it is

A data pipeline is the sequence of steps that moves raw data from its source to a format ready for analysis or model training. The three phases are Extract, Transform, and Load (ETL). In the ML context, the pipeline covers: reading from production databases or files → cleaning and validating → feature engineering → writing a training-ready dataset.

## Why it exists / what problem it solves

Raw data is never ready for modeling. It lives in different systems (Postgres, logs, CSV dumps, JSON APIs), in different formats (tabular, nested, columnar), with different quality levels (missing values, type mismatches, duplicates, outliers). A data pipeline codifies the cleaning and transformation logic so that it is reproducible, testable, and auditable — rather than a sequence of ad-hoc Jupyter notebook cells.

## How it works

### The ETL workflow

**Extract** — read data from source:
- Relational databases via SQL (Postgres, MySQL, BigQuery, Snowflake).
- Flat files: CSV, TSV, fixed-width.
- Semi-structured: JSON (often nested), XML.
- Columnar storage: Parquet, ORC (optimized for analytics workloads).
- Streams: Kafka, Kinesis (real-time pipelines, beyond the scope of this note).

**Transform** — clean, validate, reshape, and engineer:
- Data quality checks (missingness, type correctness, range validity, uniqueness constraints).
- Feature engineering (aggregations, encodings, scaling, interactions).
- Schema alignment (renaming columns, casting types, resolving conflicts).

**Load** — write the result to a consumable location:
- A flat file (Parquet recommended for ML).
- A feature store table.
- A NumPy/PyTorch/TensorFlow in-memory tensor.

### File formats compared

| Format | Structure | Schema | Compression | Read speed | ML use case |
|--------|-----------|--------|-------------|------------|-------------|
| **CSV** | Row-oriented, flat | None (all strings) | None (unless gzipped) | Slow (parse every row, string→type) | Debugging, small data, interoperability |
| **JSON** | Nested, self-describing | Implicit (embedded in data) | None | Slow (full parse required) | API responses, event logs, nested data |
| **Parquet** | Columnar, binary | Explicit (stored in file metadata) | Built-in (snappy, zstd, gzip) | Fast (read only needed columns) | **Default for ML pipelines** |
| **Arrow** | Columnar, in-memory | Explicit | Lightweight | Fastest (zero-copy reads) | High-performance data interchange |

**Why Parquet dominates ML pipelines:**
- Columnar storage means you read only the columns your model needs — for a 1000-column table, reading 10 features is 100x less I/O.
- Compression by column type is far more efficient than row-level compression (same values compress better when adjacent).
- Schema is embedded in the file: no guessing types on load.
- Supported by every major engine (Spark, DuckDB, pandas via pyarrow, Polars).

### Data quality dimensions

| Dimension | Question | How to check |
|-----------|----------|-------------|
| **Completeness** | Are values present? | `df.isnull().sum()` — look for >5% missing |
| **Consistency** | Do values follow the expected format? | `df['col'].unique()`, regex validation |
| **Accuracy** | Are values correct? | Cross-reference with source, domain-range checks |
| **Uniqueness** | Are duplicate rows present? | `df.duplicated().sum()` |
| **Timeliness** | Is the data recent enough? | `df['date'].max()`, staleness check |
| **Referential integrity** | Do foreign keys resolve? | Left-join foreign table, check for NULLs on key columns |

### Data profiling — the first step of any pipeline

Before any transformation, profile the data systematically:

```python
import pandas as pd

def profile(df):
    """Return a concise data profile DataFrame."""
    return pd.DataFrame({
        "dtype": df.dtypes,
        "n_missing": df.isnull().sum(),
        "pct_missing": (df.isnull().mean() * 100).round(1),
        "n_unique": df.nunique(),
        "min": df.min(numeric_only=True),
        "max": df.max(numeric_only=True),
    })

df = pd.read_parquet("training_data.parquet")
print(profile(df))
```

If loading CSV, always specify `dtypes` explicitly — otherwise pandas infers types, which can silently change a ZIP code string into an integer:

```python
df = pd.read_csv(
    "raw/users.csv",
    dtype={"zip_code": str, "user_id": int},
    parse_dates=["signup_date"],
)
```

### DuckDB: the bridge between SQL and local analytics

[DuckDB](https://duckdb.org) is an embedded OLAP database that runs in-process, has no server, and can query CSV/Parquet/JSON files directly with SQL. It is the ideal tool for the "Transform" step of an ML pipeline:

```python
import duckdb

# Query a Parquet file directly — no load step
result = duckdb.sql("""
    SELECT
        user_id,
        COUNT(*) AS session_count,
        AVG(duration_minutes) AS avg_duration
    FROM 'raw/sessions.parquet'
    WHERE session_date >= '2025-01-01'
    GROUP BY user_id
""").fetchdf()
```

DuckDB understands SQL window functions, complex joins, and can handle datasets larger than RAM by spilling to disk. It replaces the pattern of "dump CSV → load into pandas → filter/group → merge" with a single SQL query on the raw file.

## Links
- [[01_foundations/notes/sql-for-data-pipelines]]
- [[01_foundations/notes/pandas-for-data-preparation]]
- [[01_foundations/notes/data-visualization-essentials]]

## Insight
The most common ML pipeline failure is not a bug in the model code — it is a silent data quality issue that was never caught because no pipeline was written. A 10-line data profiling function executed before every training run catches more bugs than a week of model debugging. Parquet + DuckDB + a profile step is the minimum viable data pipeline for any ML project.
