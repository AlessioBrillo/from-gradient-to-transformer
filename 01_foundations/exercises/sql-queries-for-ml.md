---
tags: [type/exercise, phase/1]
state: consolidatedskill: SQL + data pipeline basics
created: 2026-06-19
---

# Exercise: SQL Queries for ML Pipelines

> **Practice platforms**: [SQLZoo](https://sqlzoo.net) — JOIN, Subquery, Window Functions tutorials | [Mode Analytics SQL Tutorial](https://mode.com/sql-tutorial/) — from basics to advanced analytics

## Goal / skill it demonstrates

Write five SQL queries of increasing complexity on a user-analytics schema, mirroring the pattern of building a training set from a production database. By the end, you should be able to translate any tabular feature-engineering question into a correct SQL query.

## Schema (SQLite-compatible)

```sql
-- Users table: core user information
CREATE TABLE users (
    user_id INTEGER PRIMARY KEY,
    signup_date DATE NOT NULL,
    country TEXT NOT NULL DEFAULT 'Unknown',
    plan TEXT NOT NULL CHECK (plan IN ('free', 'basic', 'premium'))
);

-- Sessions table: one row per user visit
CREATE TABLE sessions (
    session_id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(user_id),
    session_date DATE NOT NULL,
    duration_minutes REAL NOT NULL CHECK (duration_minutes > 0),
    pages_viewed INTEGER NOT NULL CHECK (pages_viewed > 0)
);

-- Purchases table: one row per transaction
CREATE TABLE purchases (
    purchase_id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(user_id),
    purchase_date DATE NOT NULL,
    amount REAL NOT NULL CHECK (amount > 0),
    product_category TEXT NOT NULL
);
```

## Sample data

```sql
INSERT INTO users VALUES
(1, '2025-01-15', 'US', 'premium'),
(2, '2025-02-20', 'US', 'basic'),
(3, '2025-03-10', 'DE', 'free'),
(4, '2025-03-15', 'US', 'basic'),
(5, '2025-04-01', 'IN', 'premium'),
(6, '2025-04-10', 'IN', 'free'),
(7, '2025-05-05', 'DE', 'premium'),
(8, '2025-05-20', 'US', 'basic'),
(9, '2025-06-01', 'IN', 'free'),
(10, '2025-06-15', 'DE', 'premium'),
(11, '2025-07-01', 'US', 'free'),
(12, '2025-07-10', 'IN', 'basic'),
(13, '2025-08-01', 'DE', 'basic'),
(14, '2025-08-15', 'US', 'premium'),
(15, '2025-09-01', 'IN', 'premium'),
(16, '2025-09-10', 'DE', 'free'),
(17, '2025-10-01', 'US', 'basic'),
(18, '2025-10-15', 'IN', 'basic'),
(19, '2025-11-01', 'DE', 'premium'),
(20, '2025-11-15', 'US', 'free');

INSERT INTO sessions VALUES
(1, 1, '2025-06-01', 15.2, 8),
(2, 1, '2025-06-05', 42.1, 23),
(3, 2, '2025-06-10', 8.5, 3),
(4, 3, '2025-06-15', 3.2, 2),
(5, 4, '2025-06-20', 22.0, 12),
(6, 5, '2025-07-01', 55.0, 31),
(7, 5, '2025-07-03', 33.3, 18),
(8, 6, '2025-07-05', 2.1, 1),
(9, 7, '2025-07-10', 48.7, 27),
(10, 8, '2025-07-15', 11.5, 6),
(11, 9, '2025-08-01', 4.3, 2),
(12, 10, '2025-08-05', 30.8, 17),
(13, 11, '2025-08-10', 5.0, 3),
(14, 12, '2025-08-15', 9.8, 5),
(15, 13, '2025-09-01', 7.2, 4),
(16, 14, '2025-09-05', 61.5, 35),
(17, 14, '2025-09-10', 44.0, 25),
(18, 15, '2025-09-15', 38.2, 21),
(19, 16, '2025-10-01', 1.5, 1),
(20, 17, '2025-10-05', 14.7, 8),
(21, 18, '2025-10-10', 6.3, 3),
(22, 19, '2025-11-01', 52.1, 29),
(23, 20, '2025-11-05', 8.9, 4),
(24, 1, '2025-11-10', 28.4, 15),
(25, 5, '2025-11-15', 18.6, 10);

INSERT INTO purchases VALUES
(1, 1, '2025-06-10', 49.99, 'electronics'),
(2, 1, '2025-06-20', 19.99, 'books'),
(3, 2, '2025-07-05', 29.99, 'electronics'),
(4, 5, '2025-07-10', 99.99, 'electronics'),
(5, 5, '2025-07-15', 14.99, 'music'),
(6, 7, '2025-08-01', 79.99, 'electronics'),
(7, 8, '2025-08-10', 39.99, 'books'),
(8, 10, '2025-08-20', 59.99, 'electronics'),
(9, 12, '2025-09-01', 24.99, 'music'),
(10, 14, '2025-09-15', 149.99, 'electronics'),
(11, 14, '2025-09-20', 34.99, 'books'),
(12, 15, '2025-10-01', 89.99, 'electronics'),
(13, 17, '2025-10-15', 44.99, 'books'),
(14, 19, '2025-11-10', 69.99, 'electronics'),
(15, 1, '2025-11-20', 24.99, 'music');
```

## Queries

### Query 1 — Filtering and Sorting (data discovery)

Find all premium users from the US or Germany who signed up in 2025, ordered by signup date ascending.

```sql
SELECT user_id, country, plan, signup_date
FROM users
WHERE plan = 'premium'
  AND country IN ('US', 'DE')
  AND signup_date BETWEEN '2025-01-01' AND '2025-12-31'
ORDER BY signup_date ASC;
```

**ML context**: Before feature engineering, you always sample and inspect a subset of your population. This query replicates the "data audit" step: understanding who your high-value users are and how they distribute over time.

### Query 2 — Aggregation with HAVING

For each country, compute the number of users, the average session duration, and the average pages viewed — but only for countries with more than 5 total sessions.

```sql
SELECT
    u.country,
    COUNT(DISTINCT u.user_id) AS user_count,
    COUNT(s.session_id) AS total_sessions,
    ROUND(AVG(s.duration_minutes), 2) AS avg_duration,
    ROUND(AVG(s.pages_viewed), 2) AS avg_pages
FROM users u
LEFT JOIN sessions s ON u.user_id = s.user_id
GROUP BY u.country
HAVING COUNT(s.session_id) > 5
ORDER BY avg_duration DESC;
```

**ML context**: `GROUP BY` + `HAVING` is the standard pattern for cohort analysis. You filter out under-represented groups (those with sparse data) before training, because models cannot learn reliable patterns from tiny cohorts.

### Query 3 — JOINs with conditional logic

For each user, show their total spend, their most recent purchase date, and whether they are a "repeat purchaser" (have made more than one purchase). Include users who have never purchased (NULLs should show 0 spend and 'no' for repeat status).

```sql
SELECT
    u.user_id,
    u.country,
    u.plan,
    COALESCE(ROUND(SUM(p.amount), 2), 0) AS total_spend,
    MAX(p.purchase_date) AS last_purchase_date,
    CASE
        WHEN COUNT(p.purchase_id) > 1 THEN 'yes'
        WHEN COUNT(p.purchase_id) = 1 THEN 'single'
        ELSE 'no'
    END AS repeat_purchaser
FROM users u
LEFT JOIN purchases p ON u.user_id = p.user_id
GROUP BY u.user_id
ORDER BY total_spend DESC;
```

**ML context**: A `LEFT JOIN` from the user table to the transaction table is the canonical pattern for creating user-level feature vectors from event-level data. The `CASE WHEN` transforms a count into a categorical label — this exact pattern appears in churn prediction, customer segmentation, and lifetime value modeling.

### Query 4 — Window Functions (ranking and time-series features)

For each session, compute:
- The user's total session duration rank within their own country (1 = highest duration).
- The duration of the user's previous session (for detecting engagement trends).
- Running total of pages viewed by the user over time.

```sql
SELECT
    s.session_id,
    s.user_id,
    u.country,
    s.session_date,
    s.duration_minutes,
    RANK() OVER (
        PARTITION BY u.country
        ORDER BY s.duration_minutes DESC
    ) AS duration_rank_in_country,
    LAG(s.duration_minutes, 1) OVER (
        PARTITION BY s.user_id
        ORDER BY s.session_date
    ) AS prev_session_duration,
    SUM(s.pages_viewed) OVER (
        PARTITION BY s.user_id
        ORDER BY s.session_date
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS running_total_pages
FROM sessions s
JOIN users u ON s.user_id = u.user_id
ORDER BY s.user_id, s.session_date;
```

**ML context**: Window functions are the single most underused SQL feature in ML pipelines. `LAG` creates the "previous value" feature needed for time-series models (what did the user do last week?). `RUNNING TOTAL` creates cumulative engagement features. Ranking within a cohort allows inter-user normalization before feeding data to a model.

### Query 5 — CTE: Complete feature vector for ML training

Build a training-ready feature table: one row per user with aggregated features from all three tables.

```sql
WITH user_base AS (
    SELECT
        user_id,
        country,
        plan,
        signup_date,
        CURRENT_DATE - signup_date AS days_since_signup
    FROM users
),

session_features AS (
    SELECT
        user_id,
        COUNT(session_id) AS total_sessions,
        ROUND(AVG(duration_minutes), 2) AS avg_session_duration,
        ROUND(AVG(pages_viewed), 2) AS avg_pages_per_session,
        MAX(session_date) AS last_session_date,
        CURRENT_DATE - MAX(session_date) AS days_since_last_session
    FROM sessions
    GROUP BY user_id
),

purchase_features AS (
    SELECT
        user_id,
        COUNT(purchase_id) AS purchase_count,
        ROUND(AVG(amount), 2) AS avg_purchase_amount,
        ROUND(SUM(amount), 2) AS total_spend,
        MAX(purchase_date) AS last_purchase_date,
        CURRENT_DATE - MAX(purchase_date) AS days_since_last_purchase,
        COUNT(DISTINCT product_category) AS distinct_categories
    FROM purchases
    GROUP BY user_id
)

SELECT
    ub.*,
    COALESCE(sf.total_sessions, 0) AS total_sessions,
    COALESCE(sf.avg_session_duration, 0) AS avg_session_duration,
    COALESCE(sf.avg_pages_per_session, 0) AS avg_pages_per_session,
    CASE
        WHEN sf.last_session_date IS NOT NULL THEN 1 ELSE 0
    END AS has_recent_session,
    COALESCE(pf.purchase_count, 0) AS purchase_count,
    COALESCE(pf.avg_purchase_amount, 0) AS avg_purchase_amount,
    COALESCE(pf.total_spend, 0) AS total_spend,
    COALESCE(pf.distinct_categories, 0) AS distinct_categories,
    CASE
        WHEN pf.days_since_last_purchase < 90 THEN 'active'
        WHEN pf.days_since_last_purchase < 365 THEN 'lapsed'
        ELSE 'inactive'
    END AS purchase_recency_segment
FROM user_base ub
LEFT JOIN session_features sf ON ub.user_id = sf.user_id
LEFT JOIN purchase_features pf ON ub.user_id = pf.user_id
ORDER BY ub.total_spend DESC;
```

**ML context**: This is the exact pattern you use in production to build a training set. Each CTE extracts a different view of the data (base attributes, behavioral features, transaction features). The final `SELECT` joins them into a flat table where each row = one observation and each column = one feature. The `COALESCE` calls handle missingness: a user with no sessions gets 0, not NULL. The `CASE WHEN` creates a categorical label (recency segment) directly in SQL.

## What I learned doing it

SQL window functions (`LAG`, `RANK`, `SUM(...) OVER`) are the most productive tool in the ML feature-engineering toolkit. A single window-function query replaces what would take 50+ lines of pandas with groupby/shift/merge chains — and it runs inside the database without moving data.

The CTE pattern (base → behavioral → transactional → flat join) scales to any problem. Every production feature pipeline I have seen follows this decomposition, whether the query is 50 lines or 500.

## Linked skill
- [[00_meta/02_skill-tree]] → item: SQL + data pipeline basics
