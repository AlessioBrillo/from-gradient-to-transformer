---
tags: [type/proof, phase/1]
state: consolidated
created: 2026-06-19
---

# Proof to myself: SQL and Data Fundamentals

**Rule:** reconstructed without looking at notes.

## What I needed to demonstrate

1. Explain the SQL mental model (execution order, JOIN semantics, GROUP BY vs window functions) in plain English.
2. Write a complex CTE from memory that builds a training-ready feature table.
3. Explain the role of SQL in ML pipelines and contrast it with pandas.

## What I produced from memory

### 1. The SQL mental model

SQL is a set-oriented language: every operation acts on sets of rows and produces a new set.

**Logical execution order** (not the order you write):
```
FROM       → pick the source table(s) and resolve JOINs
WHERE      → filter rows
GROUP BY   → partition rows into groups
HAVING     → filter groups (aggregate-level WHERE)
SELECT     → choose columns, compute expressions, aliases
ORDER BY   → sort the final result
LIMIT      → take only N rows
```

Knowing this order is the single most useful debugging tool: `WHERE` cannot reference a `SELECT` alias (because WHERE runs before SELECT), but `ORDER BY` can (because it runs after).

**JOIN semantics:**

| JOIN type | Result |
|-----------|--------|
| `INNER JOIN` | Only rows that match in **both** tables. Missing keys drop. |
| `LEFT JOIN` | All rows from the **left** table; `NULL` where the right has no match. |
| `RIGHT JOIN` | All rows from the **right** table; `NULL` where the left has no match. |
| `FULL OUTER JOIN` | All rows from **both** tables; `NULL` where either side has no match. |

For ML pipelines, `LEFT JOIN` is the workhorse: you always start from the user (or entity) table and left-join behavioral data to preserve the population.

**GROUP BY vs Window functions:**
- `GROUP BY` collapses rows into one per group. You lose row-level detail.
- Window functions (`OVER (PARTITION BY ...)`) compute aggregates **without collapsing rows**. Each row keeps its identity; the window result is added as a new column.

Example that makes this concrete: "Show each employee's salary alongside their department's average salary." A `GROUP BY` would collapse departments; a window function with `AVG(...) OVER (PARTITION BY department)` adds the avg as a column on each row.

### 2. Complex CTE from memory

```sql
WITH user_attributes AS (
    SELECT
        user_id,
        country,
        plan,
        signup_date,
        CURRENT_DATE - signup_date AS account_age_days
    FROM users
),

behavior_features AS (
    SELECT
        user_id,
        COUNT(*) AS total_sessions,
        AVG(duration_minutes) AS avg_session_duration,
        MAX(session_date) AS last_visit,
        CURRENT_DATE - MAX(session_date) AS days_idle
    FROM sessions
    GROUP BY user_id
),

purchase_features AS (
    SELECT
        user_id,
        COUNT(*) AS total_purchases,
        SUM(amount) AS lifetime_value,
        AVG(amount) AS avg_ticket,
        COUNT(DISTINCT product_category) AS category_breadth
    FROM purchases
    GROUP BY user_id
)

SELECT
    ua.*,
    COALESCE(bf.total_sessions, 0) AS total_sessions,
    COALESCE(bf.avg_session_duration, 0) AS avg_session_duration,
    COALESCE(bf.days_idle, 9999) AS days_since_last_visit,
    COALESCE(pf.total_purchases, 0) AS total_purchases,
    COALESCE(pf.lifetime_value, 0) AS lifetime_value,
    COALESCE(pf.avg_ticket, 0) AS avg_ticket,
    CASE
        WHEN pf.total_purchases > 5 THEN 'high'
        WHEN pf.total_purchases > 0 THEN 'medium'
        ELSE 'cold'
    END AS engagement_segment
FROM user_attributes ua
LEFT JOIN behavior_features bf ON ua.user_id = bf.user_id
LEFT JOIN purchase_features pf ON ua.user_id = pf.user_id
```

The pattern is always: decomposing the problem into **entity tables** (one row per user), then joining them via `COALESCE`-safe outer joins.

### 3. SQL vs pandas for ML

| Dimension | SQL | pandas |
|-----------|-----|--------|
| Data location | Stays in the database | Must be in memory |
| Scale | Billions of rows (query engines handle it) | Memory-bound (RAM on one machine) |
| Joins | Optimized by query planner, pushdown predicates | Merges in Python, hit memory |
| Window functions | Native, efficient | Groupby + shift/transform chains (verbose) |
| Iteration | Poor fit (not designed for loops) | Natural fit for iterative exploration |
| Visualization | Limited | Extensive (matplotlib, seaborn, plotly) |

The rule: **aggregate and engineer features in SQL, then load the preprocessed flat table into pandas for exploration and modeling.**

## Links
- [[01_foundations/notes/sql-for-data-pipelines]]
- [[01_foundations/notes/pandas-for-data-preparation]]
- [[01_foundations/exercises/sql-queries-for-ml]]

## Outcome
- [x] Passed → check the skill in [[00_meta/02_skill-tree]]
- [ ] Retry needed (what was missing): ...
