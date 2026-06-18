---
tags: [type/lesson, phase/1]
state: review
created: 2026-06-18
---

> **Practice**: [Mode Analytics SQL Tutorial](https://mode.com/sql-tutorial/) | [SQLZoo](https://sqlzoo.net/) | [LeetCode SQL Problems](https://leetcode.com/problemset/database/)

## What it is
SQL (Structured Query Language) is the standard language for querying and manipulating relational databases. In the ML pipeline, SQL is used for data extraction, feature engineering, and preparing training datasets from production databases.

## Why it exists / what problem it solves
Most real-world data lives in relational databases, not CSV files. To build production ML systems, you need to write queries that extract, join, aggregate, and transform data at the database level — before it ever touches Python. SQL is the lingua franca of data engineering: every data platform (BigQuery, Snowflake, Postgres, DuckDB) speaks it.

## How it works

### The mental model
Think of SQL as operations on sets of rows:
- **SELECT** — choose columns (projection).
- **FROM** — specify the table.
- **WHERE** — filter rows (selection).
- **GROUP BY** — partition rows into groups.
- **HAVING** — filter groups (like WHERE, but after GROUP BY).
- **ORDER BY** — sort.
- **LIMIT** — take only N rows.

Execution order (conceptual): FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY → LIMIT

### Core queries

**1. SELECT + WHERE (filtering):**
```sql
SELECT name, age, salary
FROM employees
WHERE department = 'Engineering'
  AND salary > 60000;
```

**2. Aggregation + GROUP BY:**
```sql
SELECT department,
       AVG(salary) AS avg_salary,
       COUNT(*) AS employee_count,
       STDDEV(salary) AS salary_std
FROM employees
GROUP BY department
HAVING COUNT(*) > 5;
```

**3. JOINs — combining tables:**
```sql
-- INNER JOIN: only matching rows in both tables
SELECT e.name, e.salary, d.budget
FROM employees e
INNER JOIN departments d ON e.dept_id = d.id;

-- LEFT JOIN: all rows from left, NULLs where right has no match
SELECT e.name, e.salary, d.budget
FROM employees e
LEFT JOIN departments d ON e.dept_id = d.id;

-- FULL OUTER JOIN: all rows from both tables
SELECT e.name, d.name AS department
FROM employees e
FULL OUTER JOIN departments d ON e.dept_id = d.id;
```

**4. Window functions — aggregations without collapsing rows:**
```sql
SELECT
    name,
    department,
    salary,
    AVG(salary) OVER (PARTITION BY department) AS dept_avg_salary,
    RANK() OVER (PARTITION BY department ORDER BY salary DESC) AS dept_rank,
    LAG(salary, 1) OVER (PARTITION BY department ORDER BY salary) AS prev_salary
FROM employees;
```

Window functions are essential for feature engineering: computing rolling averages, ranks, cumulative sums, and lagged values within groups without losing row-level granularity.

**5. CTEs (Common Table Expressions) — breaking down complex queries:**
```sql
WITH dept_stats AS (
    SELECT department,
           AVG(salary) AS avg_salary,
           STDDEV(salary) AS std_salary
    FROM employees
    GROUP BY department
),
high_performers AS (
    SELECT e.*, d.avg_salary
    FROM employees e
    JOIN dept_stats d ON e.department = d.department
    WHERE e.salary > d.avg_salary + d.std_salary
)
SELECT department, COUNT(*) AS top_performers
FROM high_performers
GROUP BY department;
```

CTEs make queries readable and testable — build the pipeline step by step, verifying each CTE independently.

### SQL for ML pipelines — practical patterns

**Creating a training set:**
```sql
WITH user_features AS (
    SELECT
        u.user_id,
        COUNT(DISTINCT o.order_id) AS order_count,
        AVG(o.amount) AS avg_order_value,
        MAX(o.created_at) AS last_order_date,
        u.signup_date,
        CURRENT_DATE - u.signup_date AS days_since_signup
    FROM users u
    LEFT JOIN orders o ON u.user_id = o.user_id
    GROUP BY u.user_id, u.signup_date
)
SELECT *
FROM user_features
WHERE days_since_signup > 30;  -- only mature users for training
```

**Sampling for ML:**
```sql
-- Random sample (works in most databases)
SELECT * FROM users ORDER BY RANDOM() LIMIT 10000;

-- Stratified sampling (ensure class balance)
SELECT * FROM (
    SELECT *,
           ROW_NUMBER() OVER (PARTITION BY target_variable ORDER BY RANDOM()) AS rn
    FROM my_table
) t
WHERE rn <= 5000;  -- up to 5000 per class
```

## Links
- [[01_foundations/notes/pandas-for-data-preparation|pandas for Data Preparation]]
- [[01_foundations/notes/data-visualization-essentials|Data Visualization Essentials]]

## Insight
SQL window functions are the superpower that most data scientists underuse. The ability to compute a rolling 30-day average per user, a rank within a department, or the time since the last purchase — all in a single query without leaving the database — eliminates entire classes of feature engineering bugs (data leakage from future information, incorrect group boundaries, off-by-one errors in time ordering). If you can write a CTE with a window function, you can build any training set.
