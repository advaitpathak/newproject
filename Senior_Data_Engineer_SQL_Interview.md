# Senior Data Engineer — SQL Interview Questions
### Medium & Hard Level | With Answers & Sample Data

---

## 📦 SAMPLE TABLES

### `orders`
| order_id | customer_id | product_id | order_date  | amount  | status    |
|----------|-------------|------------|-------------|---------|-----------|
| 1        | 101         | 501        | 2024-01-05  | 250.00  | completed |
| 2        | 102         | 502        | 2024-01-10  | 180.00  | completed |
| 3        | 101         | 503        | 2024-02-15  | 320.00  | cancelled |
| 4        | 103         | 501        | 2024-02-20  | 250.00  | completed |
| 5        | 104         | 504        | 2024-03-01  | 400.00  | completed |
| 6        | 102         | 501        | 2024-03-10  | 250.00  | completed |
| 7        | 101         | 502        | 2024-03-15  | 180.00  | completed |
| 8        | 105         | 505        | 2024-04-01  | 500.00  | pending   |
| 9        | 103         | 503        | 2024-04-05  | 320.00  | completed |
| 10       | 104         | 502        | 2024-04-10  | 180.00  | cancelled |

### `customers`
| customer_id | name        | country | signup_date |
|-------------|-------------|---------|-------------|
| 101         | Alice Smith | USA     | 2023-06-01  |
| 102         | Bob Jones   | UK      | 2023-07-15  |
| 103         | Carol Lee   | USA     | 2023-08-20  |
| 104         | David Kim   | Canada  | 2023-09-01  |
| 105         | Eva Brown   | UK      | 2024-01-10  |
| 106         | Frank White | USA     | 2024-02-05  |

### `products`
| product_id | name          | category    | price  |
|------------|---------------|-------------|--------|
| 501        | Widget A      | Electronics | 250.00 |
| 502        | Widget B      | Electronics | 180.00 |
| 503        | Gadget X      | Accessories | 320.00 |
| 504        | Gadget Y      | Accessories | 400.00 |
| 505        | Super Device  | Electronics | 500.00 |

### `employee_salaries`
| emp_id | name         | department  | salary  | hire_date  | manager_id |
|--------|--------------|-------------|---------|------------|------------|
| 1      | John Doe     | Engineering | 120000  | 2019-03-01 | NULL       |
| 2      | Jane Smith   | Engineering | 95000   | 2020-06-15 | 1          |
| 3      | Mike Brown   | Engineering | 88000   | 2021-01-10 | 1          |
| 4      | Sara White   | Marketing   | 75000   | 2020-09-01 | NULL       |
| 5      | Tom Black    | Marketing   | 70000   | 2021-11-20 | 4          |
| 6      | Amy Green    | Marketing   | 72000   | 2022-03-05 | 4          |
| 7      | Chris Blue   | Data        | 105000  | 2019-07-20 | NULL       |
| 8      | Lisa Red     | Data        | 98000   | 2020-01-15 | 7          |
| 9      | Paul Yellow  | Data        | 91000   | 2021-04-22 | 7          |

### `events` (for window function questions)
| event_id | user_id | event_type | event_time          |
|----------|---------|------------|---------------------|
| 1        | U1      | login      | 2024-03-01 08:00:00 |
| 2        | U1      | purchase   | 2024-03-01 08:30:00 |
| 3        | U2      | login      | 2024-03-01 09:00:00 |
| 4        | U1      | logout     | 2024-03-01 09:00:00 |
| 5        | U2      | purchase   | 2024-03-01 09:45:00 |
| 6        | U3      | login      | 2024-03-02 10:00:00 |
| 7        | U1      | login      | 2024-03-02 11:00:00 |
| 8        | U1      | purchase   | 2024-03-02 11:20:00 |
| 9        | U2      | logout     | 2024-03-02 12:00:00 |
| 10       | U3      | purchase   | 2024-03-02 12:30:00 |

---

---

# 🟡 MEDIUM LEVEL QUESTIONS

---

## Q1. Rank Customers by Total Spend

**Question:**  
Write a query to rank customers by their total completed order amount (highest first).  
Include `customer_id`, `name`, `total_amount`, and their `rank`.

**Answer:**
```sql
SELECT
    c.customer_id,
    c.name,
    SUM(o.amount) AS total_amount,
    RANK() OVER (ORDER BY SUM(o.amount) DESC) AS rnk
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
WHERE o.status = 'completed'
GROUP BY c.customer_id, c.name
ORDER BY rnk;
```

**Expected Output:**
| customer_id | name        | total_amount | rnk |
|-------------|-------------|--------------|-----|
| 101         | Alice Smith | 430.00       | 1   |
| 103         | Carol Lee   | 570.00       | ... |
| 102         | Bob Jones   | 430.00       | ... |
| 104         | David Kim   | 400.00       | ... |

> **Key concept:** `RANK()` vs `DENSE_RANK()` — `RANK()` skips numbers on ties; `DENSE_RANK()` does not.

---

## Q2. Find Customers Who Have Never Placed an Order

**Question:**  
Find all customers who have never placed an order.

**Answer:**
```sql
-- Using LEFT JOIN
SELECT c.customer_id, c.name
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
WHERE o.order_id IS NULL;

-- Using NOT EXISTS (often better for large datasets)
SELECT customer_id, name
FROM customers c
WHERE NOT EXISTS (
    SELECT 1 FROM orders o WHERE o.customer_id = c.customer_id
);

-- Using NOT IN (use carefully — fails if subquery returns NULL)
SELECT customer_id, name
FROM customers
WHERE customer_id NOT IN (SELECT DISTINCT customer_id FROM orders);
```

**Expected Output:**
| customer_id | name        |
|-------------|-------------|
| 106         | Frank White |

> **Key concept:** Difference between `LEFT JOIN + IS NULL`, `NOT EXISTS`, and `NOT IN`. `NOT IN` can behave unexpectedly with NULLs in the subquery.

---

## Q3. Month-over-Month Revenue Growth

**Question:**  
Calculate the monthly total revenue and the month-over-month percentage growth for completed orders.

**Answer:**
```sql
WITH monthly_revenue AS (
    SELECT
        DATE_TRUNC('month', order_date) AS month,
        SUM(amount)                      AS revenue
    FROM orders
    WHERE status = 'completed'
    GROUP BY DATE_TRUNC('month', order_date)
)
SELECT
    month,
    revenue,
    LAG(revenue) OVER (ORDER BY month) AS prev_month_revenue,
    ROUND(
        (revenue - LAG(revenue) OVER (ORDER BY month))
        / NULLIF(LAG(revenue) OVER (ORDER BY month), 0) * 100,
        2
    ) AS mom_growth_pct
FROM monthly_revenue
ORDER BY month;
```

> **Key concepts:** `LAG()` window function, `NULLIF` to avoid division by zero, `DATE_TRUNC`.

---

## Q4. Second Highest Salary per Department

**Question:**  
Write a query to get the employee with the **second highest salary** in each department.

**Answer:**
```sql
WITH ranked AS (
    SELECT
        emp_id,
        name,
        department,
        salary,
        DENSE_RANK() OVER (PARTITION BY department ORDER BY salary DESC) AS rnk
    FROM employee_salaries
)
SELECT emp_id, name, department, salary
FROM ranked
WHERE rnk = 2;
```

**Expected Output:**
| emp_id | name       | department  | salary |
|--------|------------|-------------|--------|
| 2      | Jane Smith | Engineering | 95000  |
| 6      | Amy Green  | Marketing   | 72000  |
| 8      | Lisa Red   | Data        | 98000  |

> **Key concept:** `DENSE_RANK()` ensures no gaps — so if two employees tie for 1st, the next distinct salary is still rank 2.

---

## Q5. Running Total of Orders per Customer

**Question:**  
Write a query to show each order along with the running total amount per customer, ordered by `order_date`.

**Answer:**
```sql
SELECT
    o.order_id,
    o.customer_id,
    c.name,
    o.order_date,
    o.amount,
    SUM(o.amount) OVER (
        PARTITION BY o.customer_id
        ORDER BY o.order_date
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS running_total
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
ORDER BY o.customer_id, o.order_date;
```

> **Key concept:** Window frame clause — `ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW` vs `RANGE BETWEEN`.

---

## Q6. Find Duplicate Records

**Question:**  
Given a table `raw_orders(order_id, customer_id, product_id, order_date, amount)`,  
find all duplicate rows where `(customer_id, product_id, order_date)` combination appears more than once.  
Return the duplicated rows with a count.

**Answer:**
```sql
SELECT
    customer_id,
    product_id,
    order_date,
    COUNT(*) AS duplicate_count
FROM raw_orders
GROUP BY customer_id, product_id, order_date
HAVING COUNT(*) > 1;

-- To get full rows of duplicates:
WITH dupes AS (
    SELECT
        customer_id, product_id, order_date,
        COUNT(*) OVER (PARTITION BY customer_id, product_id, order_date) AS cnt
    FROM raw_orders
)
SELECT * FROM dupes WHERE cnt > 1;
```

> **Key concept:** `HAVING` vs `WHERE`. `HAVING` filters after aggregation. The window function approach retrieves full rows without self-join.

---

## Q7. Products Never Ordered

**Question:**  
Find all products that have never been ordered.

**Answer:**
```sql
SELECT p.product_id, p.name
FROM products p
LEFT JOIN orders o ON p.product_id = o.product_id
WHERE o.order_id IS NULL;
```

**Expected Output:**
| product_id | name     |
|------------|----------|
| *(none)*   |          |

> All products in the sample have at least one order. In a real scenario, this shows orphaned products.

---

## Q8. Cumulative Distribution of Salaries

**Question:**  
Show each employee's salary along with its cumulative distribution (percentile rank) within their department.

**Answer:**
```sql
SELECT
    name,
    department,
    salary,
    ROUND(CUME_DIST() OVER (PARTITION BY department ORDER BY salary) * 100, 2) AS cumulative_pct,
    ROUND(PERCENT_RANK() OVER (PARTITION BY department ORDER BY salary) * 100, 2) AS percent_rank_pct
FROM employee_salaries;
```

> **Key concept:** `CUME_DIST()` — fraction of rows ≤ current value. `PERCENT_RANK()` — relative rank as a fraction.

---

## Q9. Self-Join — Find Employees Earning More Than Their Manager

**Question:**  
Find all employees who earn more than their direct manager.

**Answer:**
```sql
SELECT
    e.emp_id,
    e.name        AS employee_name,
    e.salary      AS employee_salary,
    m.name        AS manager_name,
    m.salary      AS manager_salary
FROM employee_salaries e
JOIN employee_salaries m ON e.manager_id = m.emp_id
WHERE e.salary > m.salary;
```

> **Key concept:** Self-join using `manager_id`. An employee with `manager_id IS NULL` is a top-level manager.

---

## Q10. Pivot / Conditional Aggregation

**Question:**  
Write a query to show, per country, the number of completed and cancelled orders side by side.

**Answer:**
```sql
SELECT
    c.country,
    COUNT(CASE WHEN o.status = 'completed' THEN 1 END)  AS completed_orders,
    COUNT(CASE WHEN o.status = 'cancelled' THEN 1 END)  AS cancelled_orders,
    COUNT(CASE WHEN o.status = 'pending'   THEN 1 END)  AS pending_orders
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.country
ORDER BY c.country;
```

> **Key concept:** Conditional aggregation as an alternative to `PIVOT` (not available in all databases).

---

---

# 🔴 HARD LEVEL QUESTIONS

---

## Q11. Sessionization — Group Events into Sessions

**Question:**  
Using the `events` table, define a **session** as a sequence of events for the same user where consecutive events are no more than **30 minutes apart**.  
Assign a `session_id` to each event row.

**Answer:**
```sql
WITH lagged AS (
    SELECT
        event_id,
        user_id,
        event_type,
        event_time,
        LAG(event_time) OVER (PARTITION BY user_id ORDER BY event_time) AS prev_event_time
    FROM events
),
flagged AS (
    SELECT *,
        CASE
            WHEN prev_event_time IS NULL
              OR EXTRACT(EPOCH FROM (event_time - prev_event_time)) > 1800
            THEN 1
            ELSE 0
        END AS is_new_session
    FROM lagged
),
session_numbered AS (
    SELECT *,
        SUM(is_new_session) OVER (PARTITION BY user_id ORDER BY event_time) AS session_num
    FROM flagged
)
SELECT
    event_id,
    user_id,
    event_type,
    event_time,
    user_id || '_' || session_num AS session_id
FROM session_numbered
ORDER BY user_id, event_time;
```

> **Key concepts:** Sessionization pattern, `LAG()`, `EXTRACT(EPOCH FROM ...)`, cumulative `SUM()` over a window to assign session numbers.

---

## Q12. Finding Gaps in Sequential IDs

**Question:**  
Given a table `invoices(invoice_id INT, amount DECIMAL)`, find all **missing invoice IDs** between the min and max.

**Answer:**
```sql
-- Using generate_series (PostgreSQL)
SELECT s.missing_id
FROM generate_series(
    (SELECT MIN(invoice_id) FROM invoices),
    (SELECT MAX(invoice_id) FROM invoices)
) AS s(missing_id)
WHERE s.missing_id NOT IN (SELECT invoice_id FROM invoices);

-- Database-agnostic approach using recursive CTE
WITH RECURSIVE id_range AS (
    SELECT MIN(invoice_id) AS id FROM invoices
    UNION ALL
    SELECT id + 1
    FROM id_range
    WHERE id < (SELECT MAX(invoice_id) FROM invoices)
)
SELECT id AS missing_id
FROM id_range
WHERE id NOT IN (SELECT invoice_id FROM invoices);
```

> **Key concepts:** `generate_series`, recursive CTEs, gap detection.

---

## Q13. Slowly Changing Dimension (SCD Type 2) — Find Current and Historical Records

**Question:**  
You have a `customer_history` table that tracks changes over time (SCD Type 2):

```
customer_history(customer_id, name, country, effective_date, expiry_date)
```

**Sample Data:**
| customer_id | name        | country | effective_date | expiry_date |
|-------------|-------------|---------|----------------|-------------|
| 101         | Alice Smith | USA     | 2023-01-01     | 2024-03-01  |
| 101         | Alice Smith | Canada  | 2024-03-01     | 9999-12-31  |
| 102         | Bob Jones   | UK      | 2023-01-01     | 9999-12-31  |

Write a query to:  
1. Get the **current** record for each customer.  
2. Get the record that was **active on 2023-06-01** for each customer.

**Answer:**
```sql
-- 1. Current records
SELECT *
FROM customer_history
WHERE expiry_date = '9999-12-31';

-- OR using CURRENT_DATE:
SELECT *
FROM customer_history
WHERE CURRENT_DATE BETWEEN effective_date AND expiry_date;

-- 2. Records active on a specific date
SELECT *
FROM customer_history
WHERE '2023-06-01' BETWEEN effective_date AND expiry_date;
```

> **Key concepts:** SCD Type 2 pattern, `BETWEEN` for date range overlap, sentinel date `9999-12-31`.

---

## Q14. Median Salary per Department (Without MEDIAN Function)

**Question:**  
Calculate the **median salary** per department. Assume the database does not have a built-in `MEDIAN()` function.

**Answer:**
```sql
WITH ranked AS (
    SELECT
        department,
        salary,
        ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary)       AS rn,
        COUNT(*)     OVER (PARTITION BY department)                       AS total
    FROM employee_salaries
)
SELECT
    department,
    AVG(salary) AS median_salary
FROM ranked
WHERE rn IN (FLOOR((total + 1) / 2.0), CEIL((total + 1) / 2.0))
GROUP BY department;
```

> **Key concepts:** `ROW_NUMBER()`, `FLOOR`/`CEIL` for median position calculation (handles both odd and even counts).

---

## Q15. Consecutive Days of Activity

**Question:**  
Given a `user_activity(user_id, activity_date)` table, find users who have been active for **at least 3 consecutive days**.

**Sample Data:**
| user_id | activity_date |
|---------|---------------|
| U1      | 2024-03-01    |
| U1      | 2024-03-02    |
| U1      | 2024-03-03    |
| U1      | 2024-03-05    |
| U2      | 2024-03-01    |
| U2      | 2024-03-03    |
| U3      | 2024-03-01    |
| U3      | 2024-03-02    |
| U3      | 2024-03-03    |
| U3      | 2024-03-04    |

**Answer:**
```sql
WITH deduped AS (
    SELECT DISTINCT user_id, activity_date FROM user_activity
),
grouped AS (
    SELECT
        user_id,
        activity_date,
        activity_date - INTERVAL '1 day' * ROW_NUMBER() OVER (
            PARTITION BY user_id ORDER BY activity_date
        ) AS grp
    FROM deduped
)
SELECT
    user_id,
    MIN(activity_date) AS streak_start,
    MAX(activity_date) AS streak_end,
    COUNT(*) AS streak_length
FROM grouped
GROUP BY user_id, grp
HAVING COUNT(*) >= 3
ORDER BY user_id, streak_start;
```

**Expected Output:**
| user_id | streak_start | streak_end | streak_length |
|---------|--------------|------------|---------------|
| U1      | 2024-03-01   | 2024-03-03 | 3             |
| U3      | 2024-03-01   | 2024-03-04 | 4             |

> **Key concept:** The "islands and gaps" pattern — subtracting `ROW_NUMBER()` from the date creates the same group key for consecutive dates.

---

## Q16. Top N Products per Category

**Question:**  
Find the **top 2 products by total sales amount** in each category (completed orders only).

**Answer:**
```sql
WITH product_sales AS (
    SELECT
        p.product_id,
        p.name        AS product_name,
        p.category,
        SUM(o.amount) AS total_sales
    FROM products p
    JOIN orders o ON p.product_id = o.product_id
    WHERE o.status = 'completed'
    GROUP BY p.product_id, p.name, p.category
),
ranked AS (
    SELECT *,
        DENSE_RANK() OVER (PARTITION BY category ORDER BY total_sales DESC) AS rnk
    FROM product_sales
)
SELECT product_id, product_name, category, total_sales, rnk
FROM ranked
WHERE rnk <= 2
ORDER BY category, rnk;
```

> **Key concepts:** Window function inside a CTE, `DENSE_RANK()` with `PARTITION BY` for Top-N per group.

---

## Q17. Detecting and De-duplicating with ROW_NUMBER()

**Question:**  
A pipeline loaded duplicate rows into `raw_transactions(txn_id, customer_id, amount, txn_date, load_ts)`.  
The correct record is the one with the **latest `load_ts`** for each `txn_id`.  
Write a query to:
1. Identify duplicates.
2. Return the de-duplicated, most recent version of each transaction.

**Answer:**
```sql
-- 1. Identify duplicates
SELECT txn_id, COUNT(*) AS cnt
FROM raw_transactions
GROUP BY txn_id
HAVING COUNT(*) > 1;

-- 2. De-duplicate — keep latest load_ts per txn_id
WITH ranked AS (
    SELECT *,
        ROW_NUMBER() OVER (
            PARTITION BY txn_id
            ORDER BY load_ts DESC
        ) AS rn
    FROM raw_transactions
)
SELECT txn_id, customer_id, amount, txn_date, load_ts
FROM ranked
WHERE rn = 1;
```

> **Key concepts:** Deduplication pattern in data pipelines, `ROW_NUMBER()` with `PARTITION BY` + `ORDER BY` on load timestamp.

---

## Q18. Rolling 7-Day Average Revenue

**Question:**  
Calculate the **7-day rolling average** of daily revenue from completed orders.

**Answer:**
```sql
WITH daily_revenue AS (
    SELECT
        order_date,
        SUM(amount) AS daily_total
    FROM orders
    WHERE status = 'completed'
    GROUP BY order_date
)
SELECT
    order_date,
    daily_total,
    ROUND(
        AVG(daily_total) OVER (
            ORDER BY order_date
            ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
        ),
        2
    ) AS rolling_7d_avg
FROM daily_revenue
ORDER BY order_date;
```

> **Key concept:** `ROWS BETWEEN 6 PRECEDING AND CURRENT ROW` gives a 7-row window (inclusive). For calendar-based windows use `RANGE BETWEEN INTERVAL '6 days' PRECEDING AND CURRENT ROW`.

---

## Q19. Recursive CTE — Employee Hierarchy

**Question:**  
Using the `employee_salaries` table, write a query to display the full **reporting hierarchy** for each employee (path from root to employee).

**Answer:**
```sql
WITH RECURSIVE hierarchy AS (
    -- Anchor: top-level managers (no manager)
    SELECT
        emp_id,
        name,
        manager_id,
        name::TEXT AS path,
        0           AS depth
    FROM employee_salaries
    WHERE manager_id IS NULL

    UNION ALL

    -- Recursive: employees reporting to someone
    SELECT
        e.emp_id,
        e.name,
        e.manager_id,
        (h.path || ' -> ' || e.name)::TEXT AS path,
        h.depth + 1
    FROM employee_salaries e
    JOIN hierarchy h ON e.manager_id = h.emp_id
)
SELECT emp_id, name, depth, path
FROM hierarchy
ORDER BY path;
```

**Expected Output (partial):**
| emp_id | name        | depth | path                          |
|--------|-------------|-------|-------------------------------|
| 1      | John Doe    | 0     | John Doe                      |
| 2      | Jane Smith  | 1     | John Doe -> Jane Smith        |
| 3      | Mike Brown  | 1     | John Doe -> Mike Brown        |
| 7      | Chris Blue  | 0     | Chris Blue                    |
| 8      | Lisa Red    | 1     | Chris Blue -> Lisa Red        |

> **Key concept:** Recursive CTE with anchor + recursive member, hierarchy traversal, `depth` tracking.

---

## Q20. Multi-Step Data Quality Check with CTEs

**Question:**  
You receive a daily feed in `staging_orders(order_id, customer_id, product_id, order_date, amount, status)`.  
Write a **single query** that classifies every row as either `valid`, `missing_customer`, `missing_product`, `invalid_amount`, or `invalid_status`.

**Answer:**
```sql
WITH checks AS (
    SELECT
        s.*,
        CASE
            WHEN s.amount <= 0 OR s.amount IS NULL                          THEN 'invalid_amount'
            WHEN s.status NOT IN ('completed','cancelled','pending')         THEN 'invalid_status'
            WHEN NOT EXISTS (
                SELECT 1 FROM customers c WHERE c.customer_id = s.customer_id
            )                                                                THEN 'missing_customer'
            WHEN NOT EXISTS (
                SELECT 1 FROM products p WHERE p.product_id = s.product_id
            )                                                                THEN 'missing_product'
            ELSE 'valid'
        END AS dq_status
    FROM staging_orders s
)
SELECT dq_status, COUNT(*) AS record_count
FROM checks
GROUP BY dq_status
ORDER BY dq_status;

-- To get the full failing rows:
SELECT *
FROM checks
WHERE dq_status <> 'valid';
```

> **Key concepts:** Data quality framework in SQL, correlated subqueries, `CASE WHEN` priority ordering, CTE layering.

---

## Q21. Time Between Events (Funnel Analysis)

**Question:**  
Using the `events` table, for each user calculate the **average time (in minutes)** between a `login` event and the next `purchase` event within the same session (events on the same day).

**Answer:**
```sql
WITH logins AS (
    SELECT user_id, event_time AS login_time
    FROM events
    WHERE event_type = 'login'
),
purchases AS (
    SELECT user_id, event_time AS purchase_time
    FROM events
    WHERE event_type = 'purchase'
),
funnel AS (
    SELECT
        l.user_id,
        l.login_time,
        MIN(p.purchase_time) AS next_purchase_time
    FROM logins l
    JOIN purchases p
        ON l.user_id = p.user_id
        AND p.purchase_time > l.login_time
        AND DATE(p.purchase_time) = DATE(l.login_time)
    GROUP BY l.user_id, l.login_time
)
SELECT
    user_id,
    ROUND(AVG(EXTRACT(EPOCH FROM (next_purchase_time - login_time)) / 60), 2) AS avg_minutes_to_purchase
FROM funnel
GROUP BY user_id
ORDER BY user_id;
```

> **Key concepts:** Funnel analysis, self-join on time inequality, `EXTRACT(EPOCH FROM interval)` for duration calculation.

---

## Q22. Upsert / Merge Logic (MERGE Statement)

**Question:**  
You have a `dim_customers` table and a `staging_customers` feed arriving daily.  
Write a `MERGE` statement (or equivalent `INSERT ... ON CONFLICT`) to:
- **Update** existing customers if `country` has changed.
- **Insert** new customers that don't exist yet.
- Do **nothing** if the record is identical.

**Answer:**
```sql
-- ANSI SQL MERGE (supported in most modern warehouses: Snowflake, BigQuery, SQL Server, Databricks)
MERGE INTO dim_customers AS tgt
USING staging_customers  AS src
    ON tgt.customer_id = src.customer_id
WHEN MATCHED AND tgt.country <> src.country THEN
    UPDATE SET
        tgt.country      = src.country,
        tgt.updated_at   = CURRENT_TIMESTAMP
WHEN NOT MATCHED THEN
    INSERT (customer_id, name, country, signup_date, updated_at)
    VALUES (src.customer_id, src.name, src.country, src.signup_date, CURRENT_TIMESTAMP);

-- PostgreSQL equivalent using INSERT ... ON CONFLICT
INSERT INTO dim_customers (customer_id, name, country, signup_date, updated_at)
SELECT customer_id, name, country, signup_date, CURRENT_TIMESTAMP
FROM staging_customers
ON CONFLICT (customer_id)
DO UPDATE SET
    country    = EXCLUDED.country,
    updated_at = CURRENT_TIMESTAMP
WHERE dim_customers.country <> EXCLUDED.country;
```

> **Key concepts:** MERGE/UPSERT pattern, idempotent pipeline design, `ON CONFLICT DO UPDATE`, `EXCLUDED` pseudo-table in PostgreSQL.

---

## Q23. Partition Pruning Awareness

**Question:**  
Given a partitioned table `sales_partitioned` partitioned by `sale_year` and `sale_month`,  
which of the following queries will benefit from **partition pruning**? Explain why.

```sql
-- Query A
SELECT * FROM sales_partitioned WHERE sale_year = 2024 AND sale_month = 3;

-- Query B
SELECT * FROM sales_partitioned WHERE YEAR(sale_date) = 2024;

-- Query C
SELECT * FROM sales_partitioned WHERE sale_year * 12 + sale_month = 24291;
```

**Answer:**

| Query | Partition Pruning? | Reason |
|-------|--------------------|--------|
| A     | ✅ YES              | Direct equality filter on partition columns — optimizer can skip irrelevant partitions. |
| B     | ❌ NO               | Wrapping a column in a function (`YEAR(sale_date)`) prevents the optimizer from matching partition metadata. Use `sale_year = 2024` instead. |
| C     | ❌ NO               | Arithmetic on partition columns makes them non-sargable; the optimizer cannot determine which partitions to include. |

> **Key concept:** **SARG-ability** (Search ARGument able) — filters on partition columns must be plain comparisons. Never wrap partition columns in functions or arithmetic.

---

## Q24. Explain the Difference and Write Queries: UNION vs UNION ALL vs INTERSECT vs EXCEPT

**Question:**  
Using the `customers` table, demonstrate the difference between `UNION`, `UNION ALL`, `INTERSECT`, and `EXCEPT` with meaningful examples.

**Answer:**
```sql
-- UNION: all unique customers from USA or UK (deduplicates)
SELECT customer_id, name FROM customers WHERE country = 'USA'
UNION
SELECT customer_id, name FROM customers WHERE country = 'UK';

-- UNION ALL: same but keeps duplicates (faster — no sort/dedup)
SELECT customer_id, name FROM customers WHERE country = 'USA'
UNION ALL
SELECT customer_id, name FROM customers WHERE country = 'UK';

-- INTERSECT: customers in USA who are ALSO in UK (overlap)
-- In this dataset: none, since one customer maps to one country
SELECT customer_id FROM customers WHERE country = 'USA'
INTERSECT
SELECT customer_id FROM customers WHERE country = 'UK';

-- EXCEPT: customers in USA who are NOT in UK
SELECT customer_id, name FROM customers WHERE country = 'USA'
EXCEPT
SELECT customer_id, name FROM customers WHERE country = 'UK';
```

> **Key concept:** `UNION ALL` is faster than `UNION` because it skips deduplication. Use `UNION` only when distinct results are required. `INTERSECT`/`EXCEPT` are set operations that compare full rows.

---

## Q25. Query Optimization — Identify and Fix Performance Issues

**Question:**  
The following query is running slowly on a 500M-row table. Identify **all** the performance issues and rewrite it.

```sql
-- SLOW QUERY
SELECT *
FROM orders
WHERE UPPER(status) = 'COMPLETED'
  AND YEAR(order_date) = 2024
  AND customer_id IN (SELECT customer_id FROM customers WHERE country = 'USA');
```

**Answer:**

**Issues identified:**
1. `UPPER(status)` — function on indexed column prevents index usage.
2. `YEAR(order_date)` — function on partition/index column; non-sargable.
3. `SELECT *` — fetches all columns; use only needed columns.
4. `IN (subquery)` — can be less efficient than `EXISTS` or a `JOIN` on large datasets.

**Optimized Rewrite:**
```sql
SELECT
    o.order_id,
    o.customer_id,
    o.product_id,
    o.order_date,
    o.amount
FROM orders o
JOIN customers c
    ON o.customer_id = c.customer_id
    AND c.country = 'USA'
WHERE o.status = 'completed'                            -- store data in consistent case
  AND o.order_date >= '2024-01-01'
  AND o.order_date <  '2025-01-01'                     -- sargable range, enables partition pruning
ORDER BY o.order_date;
```

**Additional recommendations:**
- Ensure composite index on `(status, order_date, customer_id)` exists.
- If `status` has low cardinality, a partial index `WHERE status = 'completed'` may be better.
- For columnar stores (Redshift, BigQuery, Snowflake), avoid `SELECT *` — it reads unnecessary columns.

---

## 📝 Quick Reference: Key SQL Concepts for Senior DE Interviews

| Concept | Key Functions / Keywords |
|---------|--------------------------|
| Window Functions | `ROW_NUMBER`, `RANK`, `DENSE_RANK`, `LAG`, `LEAD`, `NTILE`, `CUME_DIST`, `SUM OVER`, `AVG OVER` |
| CTEs | `WITH ... AS (...)`, recursive CTEs |
| Set Operations | `UNION`, `UNION ALL`, `INTERSECT`, `EXCEPT` |
| Date/Time | `DATE_TRUNC`, `EXTRACT`, `DATEADD`, `DATEDIFF`, `INTERVAL` |
| Data Quality | `NULLIF`, `COALESCE`, `CASE WHEN`, `IS NULL` |
| Performance | Partition pruning, sargability, index design, `EXPLAIN ANALYZE` |
| Pipeline Patterns | Deduplication, SCD Type 2, UPSERT/MERGE, sessionization, gap detection |

---

---

# 📚 THEORY SQL INTERVIEW QUESTIONS — Senior Data Engineer
### Level: Mid & Hard | With Full Answers

---

## 🟡 MID-LEVEL THEORY QUESTIONS

---

### T1. What is the difference between `WHERE` and `HAVING`?

**Answer:**

| Clause  | Filters | Stage |
|---------|---------|-------|
| `WHERE` | Individual rows **before** aggregation | Pre-`GROUP BY` |
| `HAVING` | Grouped results **after** aggregation | Post-`GROUP BY` |

- `WHERE` cannot reference aggregate functions (`SUM`, `COUNT`, etc.).
- `HAVING` can reference both aggregate functions and grouped columns.

**Example:**
```sql
-- WHERE: filters rows before grouping
SELECT department, COUNT(*)
FROM employee_salaries
WHERE salary > 80000          -- row-level filter
GROUP BY department;

-- HAVING: filters groups after aggregation
SELECT department, COUNT(*)
FROM employee_salaries
GROUP BY department
HAVING COUNT(*) > 2;          -- group-level filter
```

> **Key rule:** If you can write it in `WHERE`, do so — it's evaluated earlier and is more efficient.

---

### T2. What is the difference between `RANK()`, `DENSE_RANK()`, and `ROW_NUMBER()`?

**Answer:**

All three are window functions that assign a number to each row, but they differ in how they handle **ties**:

| Function       | Tie Behaviour | Gaps After Tie? |
|----------------|---------------|-----------------|
| `ROW_NUMBER()` | Arbitrary unique number per row | N/A — always unique |
| `RANK()`       | Same rank for ties | ✅ YES — skips numbers |
| `DENSE_RANK()` | Same rank for ties | ❌ NO — no gaps |

**Example with salaries: 100k, 100k, 90k**

| Salary | `ROW_NUMBER` | `RANK` | `DENSE_RANK` |
|--------|-------------|--------|--------------|
| 100k   | 1           | 1      | 1            |
| 100k   | 2           | 1      | 1            |
| 90k    | 3           | 3      | 2            |

> **Use `DENSE_RANK()`** when you need "2nd highest salary" and don't want to skip ranks.  
> **Use `ROW_NUMBER()`** for deduplication (guaranteed unique row per partition).

---

### T3. What is a CTE and how does it differ from a subquery?

**Answer:**

A **CTE (Common Table Expression)** is a named temporary result set defined with the `WITH` clause, scoped to the query that follows it.

| Aspect | CTE | Subquery |
|--------|-----|----------|
| Readability | High — named, reusable | Lower — inline, nested |
| Reusability | Can be referenced **multiple times** in the same query | Must be repeated |
| Recursive support | ✅ YES (`WITH RECURSIVE`) | ❌ NO |
| Performance | Varies by engine (may or may not be materialized) | Inline — always re-evaluated |
| Debugging | Easy — can test each CTE step independently | Harder to isolate |

**Example:**
```sql
-- CTE (readable, reusable)
WITH high_earners AS (
    SELECT * FROM employee_salaries WHERE salary > 90000
)
SELECT department, COUNT(*) FROM high_earners GROUP BY department;

-- Equivalent subquery (less readable)
SELECT department, COUNT(*)
FROM (SELECT * FROM employee_salaries WHERE salary > 90000) AS high_earners
GROUP BY department;
```

> **Key point:** Recursive CTEs are the **only** SQL way to traverse hierarchical/graph data without procedural code.

---

### T4. Explain the different types of JOINs and when to use each.

**Answer:**

| JOIN Type | Returns |
|-----------|---------|
| `INNER JOIN` | Only rows with **matching keys in both** tables |
| `LEFT JOIN` | All rows from left + matching from right (NULLs for no match) |
| `RIGHT JOIN` | All rows from right + matching from left (NULLs for no match) |
| `FULL OUTER JOIN` | All rows from both tables (NULLs where no match on either side) |
| `CROSS JOIN` | Cartesian product — every row from left × every row from right |
| `SELF JOIN` | A table joined to itself (e.g., employee–manager hierarchy) |
| `SEMI JOIN` | `WHERE EXISTS / IN` — returns rows from left where a match exists in right (no right columns) |
| `ANTI JOIN` | `WHERE NOT EXISTS / NOT IN` — returns rows from left with **no** match in right |

**When to use:**
- `LEFT JOIN + IS NULL` → find unmatched rows (anti-join pattern).
- `CROSS JOIN` → generate combinations (e.g., date spine × product list).
- `SELF JOIN` → hierarchy traversal, comparing rows within the same table.

> **Performance tip:** `NOT EXISTS` is generally safer and faster than `NOT IN` when the subquery might return `NULL` values.

---

### T5. What is the difference between `UNION` and `UNION ALL`?

**Answer:**

| | `UNION` | `UNION ALL` |
|---|---------|-------------|
| Duplicates | ❌ Removes duplicates (implicit `DISTINCT`) | ✅ Keeps all rows including duplicates |
| Performance | Slower — requires sort + deduplication pass | Faster — no extra processing |
| Use case | When distinct results are required | When duplicates are acceptable or impossible |

**Rule of thumb:** Always use `UNION ALL` unless you explicitly need deduplication — it avoids an expensive sort operation on large datasets.

```sql
-- UNION: deduplicated (slower)
SELECT customer_id FROM orders_2024
UNION
SELECT customer_id FROM orders_2025;

-- UNION ALL: all rows (faster)
SELECT customer_id FROM orders_2024
UNION ALL
SELECT customer_id FROM orders_2025;
```

---

### T6. What are window functions? How do they differ from `GROUP BY` aggregations?

**Answer:**

**Window functions** compute a value for each row based on a "window" (a set of related rows), **without collapsing rows** like `GROUP BY` does.

| Aspect | `GROUP BY` Aggregation | Window Function |
|--------|------------------------|-----------------|
| Row output | One row per group | One row per input row |
| Access to individual row | ❌ Lost after aggregation | ✅ Retained |
| Use case | Summary/totals | Rankings, running totals, comparisons within partitions |

**Syntax:**
```sql
function_name() OVER (
    PARTITION BY col1          -- like GROUP BY, but doesn't collapse rows
    ORDER BY col2              -- defines row ordering within window
    ROWS/RANGE BETWEEN ...     -- optional frame clause
)
```

**Common window functions:**

| Category | Functions |
|----------|-----------|
| Ranking | `ROW_NUMBER()`, `RANK()`, `DENSE_RANK()`, `NTILE(n)` |
| Offset | `LAG(col, n)`, `LEAD(col, n)` |
| Aggregate | `SUM()`, `AVG()`, `MIN()`, `MAX()`, `COUNT()` |
| Distribution | `CUME_DIST()`, `PERCENT_RANK()` |

> **Key insight:** You can mix window functions and `GROUP BY` in the same query — window functions are evaluated **after** `GROUP BY`.

---

### T7. What is a NULL in SQL? How does it behave in comparisons, aggregations, and joins?

**Answer:**

`NULL` represents an **unknown or missing value** — it is NOT zero, empty string, or false.

**Comparison behaviour:**
```sql
NULL = NULL    → NULL (not TRUE!)
NULL <> NULL   → NULL
NULL = 1       → NULL

-- Correct way to check for NULL:
WHERE col IS NULL
WHERE col IS NOT NULL
```

**Aggregation behaviour:**
- `COUNT(*)` counts all rows including NULLs.
- `COUNT(col)` skips NULL values.
- `SUM`, `AVG`, `MIN`, `MAX` all **ignore NULLs**.

**JOIN behaviour:**
- `NULL` keys never match — a row with `NULL` foreign key will not appear in an `INNER JOIN`.
- In a `LEFT JOIN`, a row with `NULL` foreign key still appears (with NULLs for right-table columns).

**`NOT IN` gotcha:**
```sql
-- If the subquery returns even one NULL, the entire NOT IN returns no rows!
SELECT * FROM orders WHERE customer_id NOT IN (SELECT customer_id FROM blacklist);
-- If blacklist has any NULL customer_id → returns 0 rows silently

-- Safer: use NOT EXISTS
SELECT * FROM orders o
WHERE NOT EXISTS (SELECT 1 FROM blacklist b WHERE b.customer_id = o.customer_id);
```

> **Best practice:** Always use `COALESCE(col, default)` or `NULLIF(col, val)` to handle NULLs explicitly.

---

### T8. What is the difference between `DELETE`, `TRUNCATE`, and `DROP`?

**Answer:**

| Command | What it does | Rollback? | WHERE clause? | Resets identity? | DDL/DML |
|---------|-------------|-----------|---------------|------------------|---------|
| `DELETE` | Removes rows one by one, logs each deletion | ✅ YES | ✅ YES | ❌ NO | DML |
| `TRUNCATE` | Removes all rows instantly (deallocates pages) | ⚠️ Depends on DB | ❌ NO | ✅ YES | DDL |
| `DROP` | Removes the **entire table** (structure + data) | ⚠️ Depends on DB | ❌ NO | N/A | DDL |

- `DELETE` is slower on large tables because each row deletion is logged.
- `TRUNCATE` is much faster but cannot be used with a `WHERE` clause.
- `DROP` permanently removes the table definition — all indexes, constraints, and data are gone.

---

### T9. What are indexes and what types exist? When would you NOT use an index?

**Answer:**

An **index** is a data structure that speeds up row lookups by avoiding full table scans.

**Common index types:**

| Type | Best For |
|------|---------|
| B-Tree (default) | Equality (`=`) and range (`<`, `>`, `BETWEEN`) queries |
| Hash | Equality-only lookups (not range) |
| Bitmap | Low-cardinality columns (e.g., gender, status) — used in data warehouses |
| Composite | Multi-column filters — column order matters (leftmost prefix rule) |
| Partial | Subset of rows (e.g., `WHERE status = 'active'`) — smaller, faster |
| Full-Text | `LIKE '%word%'` style searches |

**When NOT to use an index:**
1. **Very small tables** — a full table scan is faster than index traversal.
2. **High write frequency** — every `INSERT`/`UPDATE`/`DELETE` must also update all indexes.
3. **Low-cardinality columns** on OLTP — e.g., a boolean column; the optimizer may ignore it anyway.
4. **Columns always wrapped in functions** — `UPPER(col)`, `YEAR(col)` make standard indexes useless (use function-based indexes instead).
5. **Bulk loads** — disable/drop indexes before bulk inserts, rebuild after.

---

### T10. What is the difference between `INNER JOIN` and a correlated subquery? When should you prefer one over the other?

**Answer:**

| | `JOIN` | Correlated Subquery |
|---|--------|---------------------|
| Execution | Set-based — both sides processed at once | Row-by-row — subquery re-executes for each outer row |
| Performance | Generally faster (hash join, merge join) | Can be very slow on large datasets (O(n²) in worst case) |
| Readability | Clear relationship between tables | Can be intuitive for existence checks |
| Use case | Retrieving columns from related table | `EXISTS`/`NOT EXISTS` checks, row-level comparisons |

**When to prefer correlated subquery:**
- `EXISTS`/`NOT EXISTS` patterns — short-circuits on first match.
- When you need to reference the outer row's value inside the subquery filter.

**When to prefer JOIN:**
- When you need columns from the related table.
- When the dataset is large — set-based operations scale better.

```sql
-- Correlated subquery (acceptable for EXISTS)
SELECT name FROM customers c
WHERE EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.customer_id);

-- Equivalent JOIN (often faster at scale)
SELECT DISTINCT c.name
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id;
```

---

---

## 🔴 HARD-LEVEL THEORY QUESTIONS

---

### T11. Explain query execution order in SQL. Why does this matter?

**Answer:**

SQL clauses are **written** in one order but **executed** in a different order:

| Written Order | Execution Order | Clause |
|--------------|----------------|--------|
| 1 | 1️⃣ | `FROM` + `JOIN` — identify source tables, build working set |
| 2 | 2️⃣ | `WHERE` — filter rows before grouping |
| 3 | 3️⃣ | `GROUP BY` — group remaining rows |
| 4 | 4️⃣ | `HAVING` — filter groups |
| 5 | 5️⃣ | `SELECT` — compute expressions, apply aliases |
| 6 | 6️⃣ | `DISTINCT` — remove duplicate rows |
| 7 | 7️⃣ | `ORDER BY` — sort results (can use SELECT aliases) |
| 8 | 8️⃣ | `LIMIT` / `OFFSET` — trim final result set |

**Why this matters — common pitfalls:**

```sql
-- ❌ WRONG: cannot use SELECT alias in WHERE (alias not yet defined)
SELECT amount * 1.1 AS adjusted_amount
FROM orders
WHERE adjusted_amount > 300;    -- ERROR: column not found

-- ✅ CORRECT: use a CTE or subquery
WITH calc AS (
    SELECT amount * 1.1 AS adjusted_amount FROM orders
)
SELECT * FROM calc WHERE adjusted_amount > 300;

-- ✅ CORRECT: ORDER BY CAN use SELECT aliases (evaluated after SELECT)
SELECT amount * 1.1 AS adjusted_amount FROM orders ORDER BY adjusted_amount DESC;
```

> **Key insight:** Window functions are evaluated **after** `WHERE`, `GROUP BY`, and `HAVING` but **before** `ORDER BY` and `LIMIT`.

---

### T12. What is the difference between `ROWS BETWEEN` and `RANGE BETWEEN` in window frames?

**Answer:**

Both define the window frame for aggregate/window functions, but they differ in how they treat **ties**:

| Frame Type | Unit of comparison | Tie handling |
|------------|-------------------|--------------|
| `ROWS BETWEEN` | Physical row positions | Each row is independent — ties get separate frames |
| `RANGE BETWEEN` | Logical value range | Rows with the **same ORDER BY value** are treated as a single group |

**Example — running total with tied dates:**

```sql
-- Data: two orders on 2024-01-05 (amounts: 100, 200)

-- ROWS: each physical row is counted independently
SUM(amount) OVER (ORDER BY order_date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)
-- Row 1 (100): running total = 100
-- Row 2 (200): running total = 300  ✅ (adds one row at a time)

-- RANGE: all rows with same order_date are included together
SUM(amount) OVER (ORDER BY order_date RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)
-- Row 1 (100): running total = 300  (both same-date rows included)
-- Row 2 (200): running total = 300  (same — RANGE groups ties together)
```

**Practical guidance:**
- Use `ROWS` for strict running totals — predictable, position-based.
- Use `RANGE` for time-series windows where you want calendar-based frames:  
  `RANGE BETWEEN INTERVAL '6 days' PRECEDING AND CURRENT ROW`
- Default frame when `ORDER BY` is specified but no frame clause: `RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW` — **this can surprise you with ties!**

---

### T13. What is query plan / `EXPLAIN ANALYZE`? How do you use it to diagnose slow queries?

**Answer:**

`EXPLAIN ANALYZE` shows the **query execution plan** — how the database engine intends to retrieve data — along with actual runtime statistics.

**Key nodes to understand:**

| Node | Meaning |
|------|---------|
| `Seq Scan` | Full table scan — no index used |
| `Index Scan` | Index used; fetches heap rows for each match |
| `Index Only Scan` | Index covers all needed columns — no heap access |
| `Hash Join` | Builds hash table on smaller relation, probes with larger |
| `Nested Loop` | For each row in outer, scans inner — good for small datasets |
| `Merge Join` | Both sides sorted — efficient for large pre-sorted datasets |
| `Sort` | Explicit sort — watch for this in `ORDER BY` or merge joins |
| `Hash Aggregate` | Used for `GROUP BY` — builds hash table |

**Key metrics to look at:**
```
cost=0.00..1234.56      -- estimated cost (startup..total)
rows=500000             -- estimated vs actual rows — large mismatch = stale statistics
actual time=0.1..823.4  -- actual execution time in ms
loops=1                 -- how many times node was executed
buffers: shared hit=... -- cache hits vs disk reads
```

**Diagnosis checklist:**
1. `Seq Scan` on a large table with a filter → missing index.
2. Estimated rows ≪ actual rows → run `ANALYZE` to update statistics.
3. High `loops` on a `Nested Loop` → may need a `Hash Join` hint or rewrite.
4. `Sort` appearing unexpectedly → add an index that matches the `ORDER BY`.
5. `Hash Join` spilling to disk → increase `work_mem`.

---

### T14. What is data skew in distributed SQL engines? How do you detect and fix it?

**Answer:**

**Data skew** occurs when data is unevenly distributed across partitions or nodes in a distributed system (Spark, BigQuery, Redshift, Snowflake). A small number of partitions hold a disproportionately large amount of data.

**Causes:**
- High-frequency join keys (e.g., `customer_id = NULL`, or a single popular customer).
- `GROUP BY` on a low-cardinality or heavily skewed column.
- Hash partitioning on a column with many repeated values.

**Symptoms:**
- In Spark: most tasks complete quickly; a few "straggler" tasks run for much longer.
- In Redshift/Snowflake: one node slice processes far more data than others.
- Query progress stalls at 99% for a long time.

**Detection:**
```sql
-- Check distribution in Redshift
SELECT slice, COUNT(*) FROM stv_blocklist
WHERE tbl = (SELECT id FROM stv_tbl_perm WHERE name = 'my_table')
GROUP BY slice ORDER BY slice;

-- In Spark: check Spark UI → Stages → Task metrics → look for max time >> median time
```

**Fixes:**

| Technique | How it helps |
|-----------|-------------|
| **Salting** | Add a random suffix to skewed keys before joining, then aggregate after. Distributes one hot key across N buckets. |
| **Broadcast join** | If one side is small enough, broadcast it to all nodes — avoids shuffle entirely. |
| **Repartition** | Explicitly repartition on a more evenly distributed column. |
| **Bucketing** | Pre-partition large tables on join key at write time. |
| **Handle NULLs separately** | Filter out or handle NULL keys in a separate branch, then `UNION ALL`. |

```sql
-- Salting example (conceptual)
-- Step 1: explode the small table with salt values 0-9
-- Step 2: add random salt to large table key
-- Step 3: join on (key || '_' || salt)
-- Step 4: aggregate results after join
```

---

### T15. What is the difference between OLTP and OLAP database design? How does it affect SQL query patterns?

**Answer:**

| Aspect | OLTP (Online Transaction Processing) | OLAP (Online Analytical Processing) |
|--------|--------------------------------------|--------------------------------------|
| Purpose | Day-to-day transactions (INSERT/UPDATE/DELETE) | Analytics and reporting (SELECT-heavy) |
| Schema | Highly normalised (3NF) — many small tables | Denormalised — star/snowflake schema, wide fact tables |
| Row count | Millions | Billions+ |
| Query pattern | Point lookups, short transactions | Full scans, complex aggregations, many JOINs |
| Indexing | B-Tree indexes on many columns | Few indexes; partition pruning, clustering keys |
| Storage | Row-oriented (PostgreSQL, MySQL) | Columnar (BigQuery, Redshift, Snowflake) |
| Latency target | Milliseconds | Seconds to minutes |

**How it affects SQL patterns:**

*OLTP queries:*
```sql
-- Point lookup — indexed, fast
SELECT * FROM orders WHERE order_id = 12345;

-- Short transaction
BEGIN;
UPDATE accounts SET balance = balance - 100 WHERE account_id = 1;
UPDATE accounts SET balance = balance + 100 WHERE account_id = 2;
COMMIT;
```

*OLAP queries:*
```sql
-- Columnar scan with partition pruning
SELECT product_category, SUM(revenue)
FROM fact_sales
WHERE sale_year = 2024          -- partition pruning
GROUP BY product_category;

-- Star schema join
SELECT d.product_name, t.month, SUM(f.revenue)
FROM fact_sales f
JOIN dim_product  d ON f.product_key  = d.product_key
JOIN dim_time     t ON f.time_key     = t.time_key
GROUP BY d.product_name, t.month;
```

---

### T16. Explain ACID properties and how they relate to SQL operations.

**Answer:**

**ACID** guarantees that database transactions are reliable:

| Property | Meaning | SQL Relevance |
|----------|---------|---------------|
| **Atomicity** | A transaction is all-or-nothing — either fully committed or fully rolled back | `BEGIN` / `COMMIT` / `ROLLBACK`; if any statement fails, all changes are undone |
| **Consistency** | A transaction brings the DB from one valid state to another | Constraints (`NOT NULL`, `FOREIGN KEY`, `CHECK`) are enforced at commit time |
| **Isolation** | Concurrent transactions don't interfere with each other | Controlled by isolation levels (see below) |
| **Durability** | Committed transactions survive crashes | Achieved via WAL (Write-Ahead Log) / redo logs |

**Isolation levels (strictest → most lenient):**

| Level | Dirty Read | Non-repeatable Read | Phantom Read |
|-------|-----------|---------------------|--------------|
| `SERIALIZABLE` | ❌ | ❌ | ❌ |
| `REPEATABLE READ` | ❌ | ❌ | ✅ possible |
| `READ COMMITTED` | ❌ | ✅ possible | ✅ possible |
| `READ UNCOMMITTED` | ✅ possible | ✅ possible | ✅ possible |

- **Dirty read:** reading data from an uncommitted transaction.
- **Non-repeatable read:** re-reading a row gives different results because another transaction updated it.
- **Phantom read:** re-running a query returns different rows because another transaction inserted/deleted.

> **Data Engineering relevance:** Most data lake/warehouse engines (Spark, BigQuery, Redshift) offer **snapshot isolation** or **eventual consistency** rather than full ACID. Apache Hudi, Delta Lake, and Iceberg add ACID to data lakes.

---

### T17. What is a materialized view? How does it differ from a regular view, and when would you use each?

**Answer:**

| | Regular View | Materialized View |
|---|-------------|-------------------|
| Storage | No — query is re-executed every time | ✅ YES — results stored physically on disk |
| Freshness | Always up-to-date (reads live data) | Stale until refreshed — `REFRESH MATERIALIZED VIEW` |
| Performance | Slower for complex queries (re-runs every time) | Faster — reads pre-computed results |
| Use case | Abstraction / access control / query simplification | Pre-aggregating expensive queries, dashboards, reports |
| Index support | ❌ | ✅ Can be indexed |

```sql
-- Regular view: no storage, re-computed every query
CREATE VIEW monthly_revenue AS
SELECT DATE_TRUNC('month', order_date) AS month, SUM(amount) AS revenue
FROM orders WHERE status = 'completed'
GROUP BY 1;

-- Materialized view: stored, stale until refreshed
CREATE MATERIALIZED VIEW monthly_revenue_mat AS
SELECT DATE_TRUNC('month', order_date) AS month, SUM(amount) AS revenue
FROM orders WHERE status = 'completed'
GROUP BY 1;

-- Refresh on-demand
REFRESH MATERIALIZED VIEW monthly_revenue_mat;

-- Refresh without locking reads (PostgreSQL)
REFRESH MATERIALIZED VIEW CONCURRENTLY monthly_revenue_mat;
```

**When to use which:**
- **Regular view** → data must always be current; query is simple enough.
- **Materialized view** → expensive aggregation; acceptable staleness (e.g., nightly refresh); dashboard acceleration.

---

### T18. What are the different types of table partitioning? How does partition pruning work?

**Answer:**

**Partitioning** splits a large table into smaller, manageable physical segments.

**Types:**

| Type | How it works | Best for |
|------|-------------|---------|
| **Range** | Rows assigned to partition based on value range | Date/time columns — most common in DW |
| **List** | Rows assigned based on discrete values | Country, region, status codes |
| **Hash** | Rows assigned by hash(column) % N | Even distribution when no natural range |
| **Composite** | Combination of two methods (e.g., range + hash) | Very large tables with two natural partition keys |

**How partition pruning works:**

The query planner reads partition metadata and **skips entire partitions** that cannot contain rows satisfying the `WHERE` clause — without reading any data from those partitions.

```sql
-- ✅ Partition pruning occurs — direct equality on partition column
SELECT * FROM sales WHERE sale_year = 2024 AND sale_month = 3;

-- ❌ No pruning — function wrapping makes column non-sargable
SELECT * FROM sales WHERE YEAR(sale_date) = 2024;

-- ❌ No pruning — arithmetic on partition column
SELECT * FROM sales WHERE sale_year * 12 + sale_month = 24291;
```

**Key rule:** Partition columns must appear in `WHERE` as **bare column references** in simple comparisons — no functions, no arithmetic.

**In distributed engines (Spark, Hive):**
- Physical directories: `s3://bucket/sales/sale_year=2024/sale_month=03/`
- Pruning reads only matching directories, drastically reducing I/O.

---

### T19. What is the difference between normalisation and denormalisation? When would you denormalise in a data warehouse?

**Answer:**

**Normalisation** organises data to eliminate redundancy by splitting tables into smaller, related ones (following Normal Forms: 1NF → 2NF → 3NF → BCNF).

**Denormalisation** intentionally introduces redundancy by combining tables — trading storage for query performance.

| Aspect | Normalised (OLTP) | Denormalised (OLAP / DW) |
|--------|-------------------|--------------------------|
| Redundancy | Minimal | High |
| Storage | Smaller | Larger |
| Write performance | Fast (update one place) | Slower (update multiple copies) |
| Read performance | Slower (many joins needed) | Faster (fewer joins or no joins) |
| Schema | Many tables | Fewer wide tables (star/snowflake) |

**Common denormalisation patterns in data warehouses:**
1. **Star schema** — single fact table surrounded by flat dimension tables (fully denormalised dims).
2. **Snowflake schema** — partially normalised dimensions (dims joined to sub-dims).
3. **Pre-joining** — storing the result of a common join as a flat wide table.
4. **Pre-aggregating** — storing daily/monthly summaries in a separate aggregate table.

```sql
-- Normalised (3NF): requires 3 joins to get product category revenue
SELECT pc.category_name, SUM(oi.quantity * p.price)
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
JOIN product_categories pc ON p.category_id = pc.category_id
JOIN orders o ON oi.order_id = o.order_id
WHERE o.order_date >= '2024-01-01'
GROUP BY pc.category_name;

-- Denormalised fact table: same query, 0 joins
SELECT product_category, SUM(revenue)
FROM fact_sales
WHERE sale_date >= '2024-01-01'
GROUP BY product_category;
```

---

### T20. What is SCD (Slowly Changing Dimension)? Describe Types 1, 2, and 3.

**Answer:**

An **SCD** handles how dimension data changes over time in a data warehouse.

| SCD Type | Strategy | History Preserved? | Complexity |
|----------|----------|--------------------|-----------|
| **Type 0** | Never update — keep original value | N/A | Lowest |
| **Type 1** | Overwrite — update in place | ❌ NO | Low |
| **Type 2** | Add a new row for each change (with effective/expiry dates or version number) | ✅ YES (full) | High |
| **Type 3** | Add a new column for the previous value | ✅ Partial (one prior version only) | Medium |
| **Type 6** | Hybrid — combines Types 1, 2, and 3 | ✅ YES + current flag | Highest |

**Type 1 example** — customer moved country, overwrite:
```sql
UPDATE dim_customers SET country = 'Canada' WHERE customer_id = 101;
-- History lost — cannot see that Alice was previously in USA
```

**Type 2 example** — add a new versioned row:
```sql
-- Expire old record
UPDATE dim_customers SET expiry_date = '2024-03-01', is_current = FALSE
WHERE customer_id = 101 AND is_current = TRUE;

-- Insert new record
INSERT INTO dim_customers (customer_id, name, country, effective_date, expiry_date, is_current)
VALUES (101, 'Alice Smith', 'Canada', '2024-03-01', '9999-12-31', TRUE);
```

**Type 3 example** — add a column for old value:
```sql
ALTER TABLE dim_customers ADD COLUMN previous_country VARCHAR(50);
UPDATE dim_customers SET previous_country = country, country = 'Canada'
WHERE customer_id = 101;
-- Only one level of history — cannot track more than one change
```

> **When to use:** Type 1 for non-critical attributes; Type 2 for audit trails, point-in-time analysis, financial reporting; Type 3 when only the immediate previous value matters.

---

### T21. What is the N+1 query problem in SQL? How do you avoid it?

**Answer:**

The **N+1 problem** occurs when an application (or poorly written SQL) executes:
1. **1 query** to fetch a list of N parent records.
2. **N additional queries** — one per parent — to fetch related child records.

**Example (N+1 in application code):**
```python
# BAD: 1 query to get customers, then N queries for each customer's orders
customers = db.query("SELECT * FROM customers")          # 1 query
for customer in customers:                               # N queries
    orders = db.query(f"SELECT * FROM orders WHERE customer_id = {customer.id}")
```

**SQL solution — single JOIN:**
```sql
-- GOOD: 1 query with a JOIN — all data in one round trip
SELECT c.customer_id, c.name, o.order_id, o.amount
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id;
```

**In SQL itself, the N+1 problem manifests as correlated subqueries:**
```sql
-- BAD: correlated subquery re-executes for every customer row (N times)
SELECT
    customer_id,
    (SELECT SUM(amount) FROM orders o WHERE o.customer_id = c.customer_id) AS total
FROM customers c;

-- GOOD: aggregate once in a subquery or CTE, then join
WITH totals AS (
    SELECT customer_id, SUM(amount) AS total FROM orders GROUP BY customer_id
)
SELECT c.customer_id, c.name, t.total
FROM customers c
LEFT JOIN totals t ON c.customer_id = t.customer_id;
```

---

### T22. What are transactions and savepoints? How do you implement rollback logic in SQL?

**Answer:**

A **transaction** is a unit of work that is either fully committed or fully rolled back.

```sql
BEGIN;                          -- start transaction

UPDATE accounts SET balance = balance - 500 WHERE account_id = 1;
UPDATE accounts SET balance = balance + 500 WHERE account_id = 2;

COMMIT;                         -- make permanent

-- OR, on error:
ROLLBACK;                       -- undo all changes since BEGIN
```

**Savepoints** allow partial rollbacks within a transaction:
```sql
BEGIN;

INSERT INTO orders (...) VALUES (...);

SAVEPOINT after_order;          -- mark this point

INSERT INTO payments (...) VALUES (...);  -- this fails

ROLLBACK TO SAVEPOINT after_order;       -- undo payment insert only, keep order insert

COMMIT;                                  -- commit the order insert
```

**Relevance for Data Engineers:**
- ETL pipelines should wrap multi-step writes in transactions.
- Use `ROLLBACK` on exceptions to avoid partial data loads.
- In distributed engines (Spark, BigQuery), transactions work at the table/partition level — understand engine-specific semantics.

---

### T23. What is the difference between a clustered and non-clustered index?

**Answer:**

| | Clustered Index | Non-Clustered Index |
|---|----------------|---------------------|
| Physical order | Rows **physically sorted** on disk by index key | Separate structure — contains key + pointer to row |
| Count per table | Only **1** (since rows can only be sorted one way) | Many allowed |
| Lookup speed | Fastest for range scans on the cluster key | Slightly slower — requires a row lookup ("bookmark lookup") |
| Storage | No extra storage (IS the table) | Extra storage for index structure |
| Best for | Primary key, date range scans | Selective filters on non-PK columns |

**In columnar data warehouses (Redshift, Snowflake, BigQuery):**
- There are no traditional indexes.
- **Redshift:** `DISTKEY` (distribution), `SORTKEY` (clustering), `COMPOUND` vs `INTERLEAVED` sort keys.
- **Snowflake:** Automatic micro-partition pruning; manual **cluster keys** for large tables.
- **BigQuery:** `PARTITION BY` + `CLUSTER BY` — clustering physically co-locates similar values within partitions.

---

### T24. Explain the concept of query optimisation by the SQL engine. What techniques does a cost-based optimiser use?

**Answer:**

A **cost-based optimiser (CBO)** evaluates multiple possible query execution plans and picks the one with the lowest estimated cost (I/O, CPU, memory).

**Key techniques:**

| Technique | What it does |
|-----------|-------------|
| **Predicate pushdown** | Moves `WHERE` filters as early as possible (closer to the table scan) to reduce rows flowing through the plan |
| **Projection pushdown** | Reads only the columns needed — critical for columnar storage |
| **Join reordering** | Chooses optimal join order (smallest result sets first) |
| **Join algorithm selection** | Chooses between Nested Loop, Hash Join, Merge Join based on data size and sortedness |
| **Partition pruning** | Skips partitions that don't match the `WHERE` clause |
| **Statistics-based cardinality estimation** | Uses column statistics (histograms, NDV) to estimate result set sizes |
| **Subquery unnesting** | Converts correlated subqueries to joins where possible |
| **Common subexpression elimination** | Computes shared subexpressions once (CTE materialization) |

**When the optimiser fails:**
- **Stale statistics** — run `ANALYZE` / `UPDATE STATISTICS` regularly.
- **Highly skewed data** — the optimiser may underestimate or overestimate row counts.
- **Functions on columns** — defeats index use and statistics.
- **Very complex queries** — search space explosion; use query hints sparingly.

```sql
-- Force statistics update (PostgreSQL)
ANALYZE orders;

-- View query plan cost
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT) SELECT ...;
```

---

### T25. What is the CAP theorem and how does it relate to distributed SQL databases?

**Answer:**

The **CAP theorem** states that a distributed system can guarantee at most **2 of 3** properties simultaneously:

| Property | Meaning |
|----------|---------|
| **Consistency (C)** | Every read returns the most recent write or an error |
| **Availability (A)** | Every request receives a non-error response (may be stale) |
| **Partition Tolerance (P)** | System continues operating despite network partition (message loss between nodes) |

Since **network partitions are unavoidable** in distributed systems, the real trade-off is **C vs A**:

| System Type | Choice | Examples |
|-------------|--------|---------|
| CP (Consistent + Partition Tolerant) | Returns error if can't guarantee consistency | HBase, Zookeeper, traditional RDBMS clusters |
| AP (Available + Partition Tolerant) | Returns stale data rather than error | Cassandra, DynamoDB, CouchDB |
| CA (Consistent + Available) | Only possible without partitions — single-node | Traditional RDBMS (PostgreSQL, MySQL on single node) |

**Relevance to Data Engineering:**

- **Data lake formats** (Delta Lake, Hudi, Iceberg) bring ACID + strong consistency on top of eventually-consistent object storage.
- **BigQuery / Snowflake** achieve strong consistency via internal coordination — they abstract away CAP concerns.
- Understanding CAP helps choose the right tool: real-time transactions → CP system; high-availability analytics → AP system with eventual consistency.
- **PACELC** is an extension of CAP that also considers latency vs consistency trade-offs even without partitions.

---

## 📝 Theory Questions Quick Reference

### Mid-Level Topics Covered:
| # | Topic |
|---|-------|
| T1 | `WHERE` vs `HAVING` |
| T2 | `RANK()` vs `DENSE_RANK()` vs `ROW_NUMBER()` |
| T3 | CTE vs Subquery |
| T4 | Types of JOINs |
| T5 | `UNION` vs `UNION ALL` |
| T6 | Window functions vs `GROUP BY` |
| T7 | NULL behaviour in SQL |
| T8 | `DELETE` vs `TRUNCATE` vs `DROP` |
| T9 | Index types and when not to index |
| T10 | JOIN vs correlated subquery |

### Hard-Level Topics Covered:
| # | Topic |
|---|-------|
| T11 | SQL execution order |
| T12 | `ROWS BETWEEN` vs `RANGE BETWEEN` |
| T13 | `EXPLAIN ANALYZE` and query plans |
| T14 | Data skew in distributed engines |
| T15 | OLTP vs OLAP design |
| T16 | ACID properties and isolation levels |
| T17 | Materialized views vs regular views |
| T18 | Table partitioning and partition pruning |
| T19 | Normalisation vs denormalisation |
| T20 | SCD Types 1, 2, 3 |
| T21 | N+1 query problem |
| T22 | Transactions and savepoints |
| T23 | Clustered vs non-clustered indexes |
| T24 | Cost-based query optimiser |
| T25 | CAP theorem and distributed SQL |

---
*Last updated: April 2026*

