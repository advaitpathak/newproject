# PySpark Interview Questions — Senior Data Engineer
## Sessions | Cohort Analysis | Islands & Gaps
### With Full Solutions & Sample Data

---

## 📦 SAMPLE TABLES

### `events` — User clickstream / activity log
| event_id | user_id | event_type | event_time          |
|----------|---------|------------|---------------------|
| 1        | U1      | login      | 2024-03-01 08:00:00 |
| 2        | U1      | purchase   | 2024-03-01 08:25:00 |
| 3        | U1      | logout     | 2024-03-01 09:10:00 |
| 4        | U2      | login      | 2024-03-01 09:00:00 |
| 5        | U2      | purchase   | 2024-03-01 09:45:00 |
| 6        | U1      | login      | 2024-03-01 10:00:00 |
| 7        | U1      | purchase   | 2024-03-01 10:20:00 |
| 8        | U3      | login      | 2024-03-02 11:00:00 |
| 9        | U3      | purchase   | 2024-03-02 11:30:00 |
| 10       | U2      | logout     | 2024-03-02 12:00:00 |

### `user_activity` — Daily login presence
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

### `orders` — E-commerce orders with signup cohort
| order_id | customer_id | order_date  | amount  | signup_month |
|----------|-------------|-------------|---------|--------------|
| 1        | C1          | 2024-01-10  | 200.00  | 2024-01      |
| 2        | C1          | 2024-02-15  | 150.00  | 2024-01      |
| 3        | C2          | 2024-01-20  | 300.00  | 2024-01      |
| 4        | C3          | 2024-02-05  | 250.00  | 2024-02      |
| 5        | C3          | 2024-03-10  | 400.00  | 2024-02      |
| 6        | C4          | 2024-02-20  | 180.00  | 2024-02      |
| 7        | C5          | 2024-03-01  | 220.00  | 2024-03      |

### `invoices` — Sequential IDs with gaps
| invoice_id | amount  |
|------------|---------|
| 1          | 100.00  |
| 2          | 200.00  |
| 4          | 150.00  |
| 5          | 300.00  |
| 8          | 250.00  |
| 9          | 400.00  |
| 10         | 175.00  |

---

---

# 🔵 SESSION ANALYSIS

---

## Q1. Sessionize Events — Assign Session IDs (30-Minute Timeout)

**Question:**
Using the `events` table, define a **session** as a sequence of events per user where
consecutive events are **no more than 30 minutes apart**.
Assign a `session_id` (e.g., `U1_1`, `U1_2`) to each event row.

**Answer:**
```python
from pyspark.sql import SparkSession
from pyspark.sql.window import Window
from pyspark.sql.functions import (
    col, lag, unix_timestamp, when, sum as spark_sum,
    concat, lit
)

spark = SparkSession.builder.appName("SessionAnalysis").getOrCreate()

data = [
    (1, "U1", "login",    "2024-03-01 08:00:00"),
    (2, "U1", "purchase", "2024-03-01 08:25:00"),
    (3, "U1", "logout",   "2024-03-01 09:10:00"),
    (4, "U2", "login",    "2024-03-01 09:00:00"),
    (5, "U2", "purchase", "2024-03-01 09:45:00"),
    (6, "U1", "login",    "2024-03-01 10:00:00"),
    (7, "U1", "purchase", "2024-03-01 10:20:00"),
    (8, "U3", "login",    "2024-03-02 11:00:00"),
    (9, "U3", "purchase", "2024-03-02 11:30:00"),
    (10,"U2", "logout",   "2024-03-02 12:00:00"),
]
df = spark.createDataFrame(data, ["event_id", "user_id", "event_type", "event_time"])
df = df.withColumn("event_time", col("event_time").cast("timestamp"))

# ── Step 1: get previous event time per user ──────────────────────────────────
w = Window.partitionBy("user_id").orderBy("event_time")

df = df.withColumn("prev_event_time", lag("event_time", 1).over(w))

# ── Step 2: flag start of a new session ──────────────────────────────────────
TIMEOUT_SECONDS = 30 * 60  # 30 minutes

df = df.withColumn(
    "is_new_session",
    when(
        col("prev_event_time").isNull() |
        (unix_timestamp("event_time") - unix_timestamp("prev_event_time") > TIMEOUT_SECONDS),
        1
    ).otherwise(0)
)

# ── Step 3: cumulative sum → session number per user ─────────────────────────
df = df.withColumn(
    "session_num",
    spark_sum("is_new_session").over(w)
)

# ── Step 4: build a readable session_id ──────────────────────────────────────
df = df.withColumn(
    "session_id",
    concat(col("user_id"), lit("_"), col("session_num").cast("string"))
)

df.select("event_id", "user_id", "event_type", "event_time", "session_id").show(truncate=False)
```

**Expected Output:**
```
+--------+-------+----------+-------------------+----------+
|event_id|user_id|event_type|event_time         |session_id|
+--------+-------+----------+-------------------+----------+
|1       |U1     |login     |2024-03-01 08:00:00|U1_1      |
|2       |U1     |purchase  |2024-03-01 08:25:00|U1_1      |
|3       |U1     |logout    |2024-03-01 09:10:00|U1_2      |  ← gap > 30 min
|6       |U1     |login     |2024-03-01 10:00:00|U1_3      |  ← gap > 30 min
|7       |U1     |purchase  |2024-03-01 10:20:00|U1_3      |
|4       |U2     |login     |2024-03-01 09:00:00|U2_1      |
|5       |U2     |purchase  |2024-03-01 09:45:00|U2_2      |  ← gap > 30 min
...
```

> **Key concepts:** `lag()`, `unix_timestamp()` for gap calculation, cumulative `sum()` over a window to increment session counter.

---

## Q2. Session Duration & Event Count per Session

**Question:**
After sessionizing (Q1 output), compute per session:
- `session_start` (first event time)
- `session_end` (last event time)
- `duration_minutes`
- `event_count`

**Answer:**
```python
from pyspark.sql.functions import min as spark_min, max as spark_max, count, round as spark_round

# Build on df from Q1 that already has session_id
session_stats = df.groupBy("user_id", "session_id").agg(
    spark_min("event_time").alias("session_start"),
    spark_max("event_time").alias("session_end"),
    count("*").alias("event_count")
).withColumn(
    "duration_minutes",
    spark_round(
        (unix_timestamp("session_end") - unix_timestamp("session_start")) / 60.0,
        2
    )
).orderBy("user_id", "session_start")

session_stats.show(truncate=False)
```

**Expected Output:**
```
+-------+----------+-------------------+-------------------+-----------+----------------+
|user_id|session_id|session_start      |session_end        |event_count|duration_minutes|
+-------+----------+-------------------+-------------------+-----------+----------------+
|U1     |U1_1      |2024-03-01 08:00:00|2024-03-01 08:25:00|2          |25.0            |
|U1     |U1_2      |2024-03-01 09:10:00|2024-03-01 09:10:00|1          |0.0             |
|U1     |U1_3      |2024-03-01 10:00:00|2024-03-01 10:20:00|2          |20.0            |
...
```

> **Key concepts:** `groupBy` + `agg`, `unix_timestamp` arithmetic for duration.

---

## Q3. Average Time from Login to First Purchase per Session

**Question:**
For each session that contains both a `login` and a `purchase` event,
calculate the **time in minutes from the login to the first purchase**.

**Answer:**
```python
from pyspark.sql.functions import filter as spark_filter, first

# Separate logins and purchases within session
login_df = df.filter(col("event_type") == "login") \
             .select("user_id", "session_id", col("event_time").alias("login_time"))

purchase_df = df.filter(col("event_type") == "purchase") \
                .groupBy("user_id", "session_id") \
                .agg(spark_min("event_time").alias("first_purchase_time"))

funnel = login_df.join(purchase_df, on=["user_id", "session_id"], how="inner") \
    .withColumn(
        "minutes_to_purchase",
        spark_round(
            (unix_timestamp("first_purchase_time") - unix_timestamp("login_time")) / 60.0,
            2
        )
    )

funnel.select("user_id", "session_id", "login_time", "first_purchase_time", "minutes_to_purchase").show()
```

> **Key concepts:** Filtering by event type, joining login and purchase sub-frames within the same session, duration arithmetic.

---

## Q4. Bounce Sessions (Sessions with Only One Event)

**Question:**
Identify **bounce sessions** — sessions where the user only triggered a single event.

**Answer:**
```python
bounce_sessions = df.groupBy("user_id", "session_id") \
    .agg(count("*").alias("event_count")) \
    .filter(col("event_count") == 1)

# Calculate bounce rate per user
total_sessions = df.select("user_id", "session_id").distinct() \
    .groupBy("user_id").agg(count("*").alias("total_sessions"))

bounce_count = bounce_sessions.groupBy("user_id") \
    .agg(count("*").alias("bounce_sessions"))

bounce_rate = total_sessions.join(bounce_count, on="user_id", how="left") \
    .fillna(0, subset=["bounce_sessions"]) \
    .withColumn(
        "bounce_rate_pct",
        spark_round(col("bounce_sessions") / col("total_sessions") * 100, 2)
    )

bounce_rate.show()
```

> **Key concepts:** Aggregation + filter, left join for unmatched groups, `fillna` for users with no bounces.

---

## Q5. Session Funnel — Conversion Rate (Login → Purchase → Logout)

**Question:**
For each user, compute how many sessions progressed through each funnel step:
`login → purchase → logout`. Report per-step counts and conversion rates.

**Answer:**
```python
from pyspark.sql.functions import collect_set, array_contains

# For each session, collect distinct event types
session_events = df.groupBy("user_id", "session_id") \
    .agg(collect_set("event_type").alias("event_types"))

# Flag each funnel step
session_funnel = session_events \
    .withColumn("has_login",    array_contains("event_types", "login").cast("int")) \
    .withColumn("has_purchase", array_contains("event_types", "purchase").cast("int")) \
    .withColumn("has_logout",   array_contains("event_types", "logout").cast("int"))

funnel_summary = session_funnel.agg(
    count("*").alias("total_sessions"),
    spark_sum("has_login").alias("sessions_with_login"),
    spark_sum("has_purchase").alias("sessions_with_purchase"),
    spark_sum("has_logout").alias("sessions_with_logout")
).withColumn(
    "login_to_purchase_pct",
    spark_round(col("sessions_with_purchase") / col("sessions_with_login") * 100, 2)
).withColumn(
    "purchase_to_logout_pct",
    spark_round(col("sessions_with_logout") / col("sessions_with_purchase") * 100, 2)
)

funnel_summary.show(truncate=False)
```

> **Key concepts:** `collect_set`, `array_contains`, conditional aggregation via `sum` on cast boolean columns.

---

---

# 🟠 COHORT ANALYSIS

---

## Q6. Monthly Retention Cohort (Orders)

**Question:**
Using the `orders` table, group customers by their **signup month (cohort)**.
For each cohort, calculate how many customers placed an order in each subsequent month
(Month 0 = signup month, Month 1 = one month later, etc.).

**Answer:**
```python
from pyspark.sql.functions import (
    to_date, date_format, months_between, floor as spark_floor, col
)

data = [
    (1, "C1", "2024-01-10", 200.0, "2024-01"),
    (2, "C1", "2024-02-15", 150.0, "2024-01"),
    (3, "C2", "2024-01-20", 300.0, "2024-01"),
    (4, "C3", "2024-02-05", 250.0, "2024-02"),
    (5, "C3", "2024-03-10", 400.0, "2024-02"),
    (6, "C4", "2024-02-20", 180.0, "2024-02"),
    (7, "C5", "2024-03-01", 220.0, "2024-03"),
]
orders_df = spark.createDataFrame(
    data, ["order_id", "customer_id", "order_date", "amount", "signup_month"]
)
orders_df = orders_df.withColumn("order_date", to_date("order_date"))

# ── Step 1: map each order to cohort_month and period_offset ─────────────────
cohort_df = orders_df.withColumn(
    "order_month", date_format("order_date", "yyyy-MM")
).withColumn(
    "cohort_month", col("signup_month")
).withColumn(
    "period_offset",
    spark_floor(
        months_between(
            to_date(col("order_month"),  "yyyy-MM"),
            to_date(col("cohort_month"), "yyyy-MM")
        )
    ).cast("int")
)

# ── Step 2: distinct customers per cohort + period ────────────────────────────
retention = cohort_df.select("cohort_month", "customer_id", "period_offset").distinct() \
    .groupBy("cohort_month", "period_offset") \
    .agg(count("customer_id").alias("active_customers")) \
    .orderBy("cohort_month", "period_offset")

retention.show()
```

**Expected Output:**
```
+------------+-------------+----------------+
|cohort_month|period_offset|active_customers|
+------------+-------------+----------------+
|2024-01     |0            |2               |  ← C1, C2 ordered in Jan
|2024-01     |1            |1               |  ← C1 returned in Feb
|2024-02     |0            |2               |  ← C3, C4 ordered in Feb
|2024-02     |1            |1               |  ← C3 returned in Mar
|2024-03     |0            |1               |  ← C5 ordered in Mar
+------------+-------------+----------------+
```

> **Key concepts:** `months_between()`, `date_format()`, `floor()` for integer month offset. Deduplicate customers per period before counting.

---

## Q7. Cohort Retention Rate (%)

**Question:**
Extend Q6 to compute **retention rate** — what percentage of the original cohort
returned in each subsequent period?

**Answer:**
```python
from pyspark.sql.functions import first

# ── Cohort size = customers active at period_offset == 0 ─────────────────────
cohort_size = retention.filter(col("period_offset") == 0) \
    .select("cohort_month", col("active_customers").alias("cohort_size"))

# ── Join back and calculate rate ─────────────────────────────────────────────
retention_rate = retention.join(cohort_size, on="cohort_month") \
    .withColumn(
        "retention_rate_pct",
        spark_round(col("active_customers") / col("cohort_size") * 100, 2)
    ).orderBy("cohort_month", "period_offset")

retention_rate.show()
```

**Expected Output:**
```
+------------+-------------+----------------+-----------+------------------+
|cohort_month|period_offset|active_customers|cohort_size|retention_rate_pct|
+------------+-------------+----------------+-----------+------------------+
|2024-01     |0            |2               |2          |100.0             |
|2024-01     |1            |1               |2          |50.0              |
|2024-02     |0            |2               |2          |100.0             |
|2024-02     |1            |1               |2          |50.0              |
|2024-03     |0            |1               |1          |100.0             |
+------------+-------------+----------------+-----------+------------------+
```

> **Key concept:** Always divide by cohort size at period 0 (not total users), which is the industry-standard retention denominator.

---

## Q8. Cohort Revenue Analysis — Average Revenue per Cohort per Period

**Question:**
For each cohort and period offset, calculate:
- `total_revenue`
- `avg_revenue_per_customer`

**Answer:**
```python
from pyspark.sql.functions import sum as spark_sum, avg as spark_avg

revenue_cohort = cohort_df.groupBy("cohort_month", "period_offset") \
    .agg(
        spark_sum("amount").alias("total_revenue"),
        spark_round(spark_avg("amount"), 2).alias("avg_revenue_per_order")
    ) \
    .orderBy("cohort_month", "period_offset")

# Join cohort size to get revenue per customer
revenue_cohort = revenue_cohort.join(cohort_size, on="cohort_month") \
    .withColumn(
        "revenue_per_cohort_customer",
        spark_round(col("total_revenue") / col("cohort_size"), 2)
    )

revenue_cohort.show(truncate=False)
```

> **Key concepts:** Revenue-weighted cohort analysis, joining pre-computed cohort size for normalization.

---

## Q9. Churn Detection — Customers Who Stopped Ordering

**Question:**
A customer is considered **churned** if they placed an order in a given month
but placed **no order in the next 2 months**.
Identify churned customers per cohort.

**Answer:**
```python
from pyspark.sql.functions import add_months, to_date as to_date_fn, lit

# Latest order month per customer
last_order = orders_df.withColumn(
    "order_month_dt", to_date(date_format("order_date", "yyyy-MM-01"))
).groupBy("customer_id", "signup_month") \
    .agg(spark_max("order_month_dt").alias("last_order_month"))

# Define churn: last order is more than 2 months before a reference date
reference_date = "2024-04-01"

churned = last_order.withColumn(
    "months_since_last_order",
    spark_floor(
        months_between(lit(reference_date).cast("date"), col("last_order_month"))
    ).cast("int")
).withColumn(
    "is_churned",
    (col("months_since_last_order") >= 2).cast("int")
)

churn_by_cohort = churned.groupBy("signup_month") \
    .agg(
        count("*").alias("total_customers"),
        spark_sum("is_churned").alias("churned_customers")
    ).withColumn(
        "churn_rate_pct",
        spark_round(col("churned_customers") / col("total_customers") * 100, 2)
    ).orderBy("signup_month")

churn_by_cohort.show()
```

> **Key concepts:** Last-order aggregation, `months_between` for churn window, cohort-level churn rate reporting.

---

## Q10. Cohort Analysis with Pivot Table (Wide Format)

**Question:**
Produce a **pivot-style cohort table** where rows = `cohort_month`,
columns = `period_offset` (0, 1, 2, ...), and values = `active_customers`.

**Answer:**
```python
# PySpark native pivot
cohort_pivot = retention.groupBy("cohort_month") \
    .pivot("period_offset", [0, 1, 2, 3]) \
    .agg(first("active_customers")) \
    .fillna(0) \
    .orderBy("cohort_month")

cohort_pivot.show()
```

**Expected Output:**
```
+------------+---+---+---+---+
|cohort_month|  0|  1|  2|  3|
+------------+---+---+---+---+
|2024-01     |  2|  1|  0|  0|
|2024-02     |  2|  1|  0|  0|
|2024-03     |  1|  0|  0|  0|
+------------+---+---+---+---+
```

> **Key concept:** PySpark `pivot()` — always provide the explicit list of pivot values for performance (avoids an extra pass to discover them).

---

---

# 🟢 ISLANDS AND GAPS

---

## Q11. Find Islands of Consecutive Activity (Classic Islands Problem)

**Question:**
Using `user_activity`, find **islands** — contiguous runs of consecutive daily activity
for each user. Return `user_id`, `island_start`, `island_end`, `streak_length`.

**Answer:**
```python
from pyspark.sql.functions import (
    to_date, datediff, row_number, col,
    min as spark_min, max as spark_max, count
)

data = [
    ("U1", "2024-03-01"), ("U1", "2024-03-02"), ("U1", "2024-03-03"),
    ("U1", "2024-03-05"),
    ("U2", "2024-03-01"), ("U2", "2024-03-03"),
    ("U3", "2024-03-01"), ("U3", "2024-03-02"), ("U3", "2024-03-03"), ("U3", "2024-03-04"),
]
activity_df = spark.createDataFrame(data, ["user_id", "activity_date"])
activity_df = activity_df.withColumn("activity_date", to_date("activity_date"))

# ── Step 1: deduplicate ───────────────────────────────────────────────────────
activity_df = activity_df.dropDuplicates(["user_id", "activity_date"])

# ── Step 2: row number per user ordered by date ───────────────────────────────
w = Window.partitionBy("user_id").orderBy("activity_date")
activity_df = activity_df.withColumn("rn", row_number().over(w))

# ── Step 3: island key = date - rn  (same value for all rows in an island) ───
#  Consecutive dates have date - rn constant; gaps break the pattern
activity_df = activity_df.withColumn(
    "island_key",
    # Convert date to integer days from epoch, subtract rn
    (col("activity_date").cast("long") / 86400 - col("rn")).cast("long")
)

# ── Step 4: group by (user_id, island_key) ────────────────────────────────────
islands = activity_df.groupBy("user_id", "island_key") \
    .agg(
        spark_min("activity_date").alias("island_start"),
        spark_max("activity_date").alias("island_end"),
        count("*").alias("streak_length")
    ) \
    .drop("island_key") \
    .orderBy("user_id", "island_start")

islands.show(truncate=False)
```

**Expected Output:**
```
+-------+------------+----------+-------------+
|user_id|island_start|island_end|streak_length|
+-------+------------+----------+-------------+
|U1     |2024-03-01  |2024-03-03|3            |
|U1     |2024-03-05  |2024-03-05|1            |
|U2     |2024-03-01  |2024-03-01|1            |
|U2     |2024-03-03  |2024-03-03|1            |
|U3     |2024-03-01  |2024-03-04|4            |
+-------+------------+----------+-------------+
```

> **Key concept:** The **islands trick** — `date_as_integer - row_number` stays constant within a consecutive run.
> A gap resets `row_number` faster than the date increments, creating a new `island_key`.

---

## Q12. Find Gaps Between Islands

**Question:**
From the same `user_activity` data, identify the **gaps** — periods where a user
was **inactive**. Return `user_id`, `gap_start`, `gap_end`, `gap_length_days`.

**Answer:**
```python
from pyspark.sql.functions import lead, expr

# Build on islands result from Q11
w_island = Window.partitionBy("user_id").orderBy("island_start")

gaps = islands.withColumn(
    "next_island_start",
    lead("island_start", 1).over(w_island)
).filter(
    col("next_island_start").isNotNull()
).withColumn(
    "gap_start",
    expr("island_end + interval 1 day")
).withColumn(
    "gap_end",
    expr("next_island_start - interval 1 day")
).withColumn(
    "gap_length_days",
    datediff(col("gap_end"), col("gap_start")) + 1
).filter(
    col("gap_length_days") > 0  # only real gaps (not adjacent islands)
).select("user_id", "gap_start", "gap_end", "gap_length_days") \
 .orderBy("user_id", "gap_start")

gaps.show(truncate=False)
```

**Expected Output:**
```
+-------+----------+----------+---------------+
|user_id|gap_start |gap_end   |gap_length_days|
+-------+----------+----------+---------------+
|U1     |2024-03-04|2024-03-04|1              |
|U2     |2024-03-02|2024-03-02|1              |
+-------+----------+----------+---------------+
```

> **Key concept:** Use `lead()` to look at the next island's start, then compute the gap between `island_end` and `next_island_start`.

---

## Q13. Find Users with a Streak of at Least N Consecutive Days

**Question:**
Find all users who had a streak of **at least 3 consecutive days** of activity.
Return the user and all qualifying streak details.

**Answer:**
```python
N = 3

qualifying_streaks = islands.filter(col("streak_length") >= N)

qualifying_streaks.show(truncate=False)
```

**Expected Output:**
```
+-------+------------+----------+-------------+
|user_id|island_start|island_end|streak_length|
+-------+------------+----------+-------------+
|U1     |2024-03-01  |2024-03-03|3            |
|U3     |2024-03-01  |2024-03-04|4            |
+-------+------------+----------+-------------+
```

> **Key concept:** Reuse the islands DataFrame — streaks are just islands with `streak_length >= N`.

---

## Q14. Find Missing Invoice IDs (Gaps in Numeric Sequence)

**Question:**
Given the `invoices` table with sequential `invoice_id`s, find all **missing IDs**
between the min and max.

**Answer:**
```python
from pyspark.sql.functions import explode, sequence, min as spark_min, max as spark_max

data = [
    (1, 100.0), (2, 200.0), (4, 150.0),
    (5, 300.0), (8, 250.0), (9, 400.0), (10, 175.0)
]
invoices_df = spark.createDataFrame(data, ["invoice_id", "amount"])

# ── Step 1: get full range ────────────────────────────────────────────────────
bounds = invoices_df.agg(
    spark_min("invoice_id").alias("min_id"),
    spark_max("invoice_id").alias("max_id")
)

# ── Step 2: generate every ID in range ───────────────────────────────────────
full_range = bounds.select(
    explode(sequence(col("min_id"), col("max_id"))).alias("expected_id")
)

# ── Step 3: left-anti join to find missing IDs ───────────────────────────────
missing_ids = full_range.join(
    invoices_df.select(col("invoice_id").alias("expected_id")),
    on="expected_id",
    how="left_anti"
).orderBy("expected_id")

missing_ids.show()
```

**Expected Output:**
```
+-----------+
|expected_id|
+-----------+
|3          |
|6          |
|7          |
+-----------+
```

> **Key concepts:** `sequence()` to generate a range, `explode()` to expand it into rows, `left_anti` join to find non-matching (missing) IDs.

---

## Q15. Islands in Time-Series — Continuous Price Windows

**Question:**
Given a table `price_history(product_id, price, valid_from, valid_to)` representing
SCD Type-2 price records, detect any **gaps** where no valid price exists for a product.

**Sample Data:**
```
product_id | price | valid_from | valid_to
P1         | 10.0  | 2024-01-01 | 2024-01-31
P1         | 12.0  | 2024-02-05 | 2024-03-15    ← gap Jan 31 → Feb 5
P1         | 11.0  | 2024-03-15 | 9999-12-31
P2         | 20.0  | 2024-01-01 | 9999-12-31
```

**Answer:**
```python
from pyspark.sql.functions import lead, to_date, datediff, lit

data = [
    ("P1", 10.0, "2024-01-01", "2024-01-31"),
    ("P1", 12.0, "2024-02-05", "2024-03-15"),
    ("P1", 11.0, "2024-03-15", "9999-12-31"),
    ("P2", 20.0, "2024-01-01", "9999-12-31"),
]
ph_df = spark.createDataFrame(data, ["product_id", "price", "valid_from", "valid_to"])
ph_df = ph_df.withColumn("valid_from", to_date("valid_from")) \
             .withColumn("valid_to",   to_date("valid_to"))

w_ph = Window.partitionBy("product_id").orderBy("valid_from")

ph_df = ph_df.withColumn("next_valid_from", lead("valid_from", 1).over(w_ph))

price_gaps = ph_df.filter(
    col("next_valid_from").isNotNull() &
    (col("next_valid_from") > col("valid_to"))        # gap exists
).withColumn(
    "gap_start", expr("valid_to + interval 1 day")
).withColumn(
    "gap_end",   expr("next_valid_from - interval 1 day")
).withColumn(
    "gap_days",  datediff(col("gap_end"), col("gap_start")) + 1
).select("product_id", "gap_start", "gap_end", "gap_days")

price_gaps.show(truncate=False)
```

**Expected Output:**
```
+----------+----------+----------+--------+
|product_id|gap_start |gap_end   |gap_days|
+----------+----------+----------+--------+
|P1        |2024-02-01|2024-02-04|4       |
+----------+----------+----------+--------+
```

> **Key concepts:** SCD Type-2 gap detection, `lead()` for next interval start, interval arithmetic on dates.

---

## Q16. Islands & Gaps — Combining Sessions + Consecutive Activity

**Question:**
For each user, find **active session windows** (treating sessions from Q1 as "active periods")
and identify any gaps longer than **60 minutes** between sessions.

**Answer:**
```python
# Build on session_stats from Q2
w_sess = Window.partitionBy("user_id").orderBy("session_start")

session_gaps = session_stats.withColumn(
    "next_session_start",
    lead("session_start", 1).over(w_sess)
).filter(
    col("next_session_start").isNotNull()
).withColumn(
    "gap_minutes",
    spark_round(
        (unix_timestamp("next_session_start") - unix_timestamp("session_end")) / 60.0,
        2
    )
).filter(
    col("gap_minutes") > 60
).select("user_id", "session_id", "session_end", "next_session_start", "gap_minutes") \
 .orderBy("user_id", "session_end")

session_gaps.show(truncate=False)
```

> **Key concepts:** Merging sessions + gap analysis — `lead()` gives next session start; gap is the interval between `session_end` and `next_session_start`.

---

---

# 🔴 HARD / SENIOR-LEVEL COMBINED QUESTIONS

---

## Q17. Full Pipeline: Events → Sessions → Cohort Retention

**Question:**
Write a **single PySpark pipeline** that:
1. Reads raw events.
2. Sessionizes them (30-min timeout).
3. Joins with a `users` table (containing `user_id`, `signup_month`).
4. Computes per-cohort session counts by signup period offset.

**Answer:**
```python
from pyspark.sql.functions import (
    col, lag, unix_timestamp, when, sum as spark_sum,
    concat, lit, count, months_between, floor as spark_floor,
    to_date, date_format, date_trunc
)

# ── Step 1: sessionize ────────────────────────────────────────────────────────
TIMEOUT = 30 * 60

w_user = Window.partitionBy("user_id").orderBy("event_time")

sessionized = events_df \
    .withColumn("prev_time", lag("event_time").over(w_user)) \
    .withColumn(
        "new_session",
        when(
            col("prev_time").isNull() |
            (unix_timestamp("event_time") - unix_timestamp("prev_time") > TIMEOUT),
            1
        ).otherwise(0)
    ) \
    .withColumn("session_num", spark_sum("new_session").over(w_user)) \
    .withColumn("session_id", concat(col("user_id"), lit("_"), col("session_num").cast("string")))

# ── Step 2: first event time per session (session month) ─────────────────────
session_month_df = sessionized.groupBy("user_id", "session_id") \
    .agg(spark_min("event_time").alias("session_start")) \
    .withColumn("session_month", date_format("session_start", "yyyy-MM"))

# ── Step 3: join with users cohort ───────────────────────────────────────────
users_data = [("U1", "2024-03"), ("U2", "2024-03"), ("U3", "2024-03")]
users_df = spark.createDataFrame(users_data, ["user_id", "signup_month"])

cohort_sessions = session_month_df.join(users_df, on="user_id") \
    .withColumn(
        "period_offset",
        spark_floor(
            months_between(
                to_date(col("session_month"), "yyyy-MM"),
                to_date(col("signup_month"),  "yyyy-MM")
            )
        ).cast("int")
    )

# ── Step 4: cohort retention (by session count) ───────────────────────────────
cohort_retention = cohort_sessions.groupBy("signup_month", "period_offset") \
    .agg(
        count("session_id").alias("total_sessions"),
        count("user_id").alias("active_users")         # may have dups; use countDistinct for unique
    ).orderBy("signup_month", "period_offset")

cohort_retention.show()
```

> **Key concepts:** End-to-end pipeline composition, session → cohort mapping via `months_between`, incremental aggregation layers.

---

## Q18. Islands with State Changes (Non-Date Islands)

**Question:**
Given a `server_status(server_id, status, recorded_at)` table, find continuous
**"down" islands** — time windows where a server was continuously in `DOWN` status.

**Sample Data:**
```
server_id | status | recorded_at
S1        | UP     | 2024-03-01 08:00
S1        | DOWN   | 2024-03-01 09:00
S1        | DOWN   | 2024-03-01 10:00
S1        | DOWN   | 2024-03-01 11:00
S1        | UP     | 2024-03-01 12:00
S1        | DOWN   | 2024-03-01 14:00
S1        | DOWN   | 2024-03-01 15:00
```

**Answer:**
```python
from pyspark.sql.functions import row_number, sum as spark_sum, when

data = [
    ("S1","UP",   "2024-03-01 08:00:00"),
    ("S1","DOWN", "2024-03-01 09:00:00"),
    ("S1","DOWN", "2024-03-01 10:00:00"),
    ("S1","DOWN", "2024-03-01 11:00:00"),
    ("S1","UP",   "2024-03-01 12:00:00"),
    ("S1","DOWN", "2024-03-01 14:00:00"),
    ("S1","DOWN", "2024-03-01 15:00:00"),
]
status_df = spark.createDataFrame(data, ["server_id", "status", "recorded_at"])
status_df = status_df.withColumn("recorded_at", col("recorded_at").cast("timestamp"))

w_srv = Window.partitionBy("server_id").orderBy("recorded_at")

# ── Flag rows where status changes from previous row ─────────────────────────
status_df = status_df.withColumn("prev_status", lag("status").over(w_srv)) \
    .withColumn(
        "state_change",
        when(
            col("prev_status").isNull() | (col("status") != col("prev_status")),
            1
        ).otherwise(0)
    ) \
    .withColumn(
        "island_id",
        spark_sum("state_change").over(w_srv)
    )

# ── Aggregate only DOWN islands ───────────────────────────────────────────────
down_islands = status_df.filter(col("status") == "DOWN") \
    .groupBy("server_id", "island_id") \
    .agg(
        spark_min("recorded_at").alias("down_start"),
        spark_max("recorded_at").alias("down_end"),
        count("*").alias("down_event_count")
    ) \
    .withColumn(
        "duration_minutes",
        spark_round(
            (unix_timestamp("down_end") - unix_timestamp("down_start")) / 60.0,
            2
        )
    ) \
    .drop("island_id") \
    .orderBy("server_id", "down_start")

down_islands.show(truncate=False)
```

**Expected Output:**
```
+---------+-------------------+-------------------+----------------+----------------+
|server_id|down_start         |down_end           |down_event_count|duration_minutes|
+---------+-------------------+-------------------+----------------+----------------+
|S1       |2024-03-01 09:00:00|2024-03-01 11:00:00|3               |120.0           |
|S1       |2024-03-01 14:00:00|2024-03-01 15:00:00|2               |60.0            |
+---------+-------------------+-------------------+----------------+----------------+
```

> **Key concepts:** **Value-change islands** — flag where `status != prev_status`, cumulative sum creates island IDs. Works for any state-change scenario (not just dates).

---

## Q19. Longest Streak per User

**Question:**
Find the **single longest consecutive activity streak** per user,
along with its start and end dates.

**Answer:**
```python
from pyspark.sql.functions import rank as spark_rank

# Use the islands DataFrame from Q11
w_streak = Window.partitionBy("user_id").orderBy(col("streak_length").desc())

longest_streaks = islands.withColumn("rnk", spark_rank().over(w_streak)) \
    .filter(col("rnk") == 1) \
    .select("user_id", "island_start", "island_end", "streak_length") \
    .orderBy("user_id")

longest_streaks.show(truncate=False)
```

**Expected Output:**
```
+-------+------------+----------+-------------+
|user_id|island_start|island_end|streak_length|
+-------+------------+----------+-------------+
|U1     |2024-03-01  |2024-03-03|3            |
|U2     |2024-03-01  |2024-03-01|1            |
|U3     |2024-03-01  |2024-03-04|4            |
+-------+------------+----------+-------------+
```

> **Key concept:** Use `rank()` (not `row_number()`) to handle ties — if two streaks share the same max length, both are returned.

---

## Q20. Overlap Detection — Find Overlapping Booking Periods

**Question:**
Given a `bookings(booking_id, room_id, guest_id, check_in, check_out)` table,
detect any **double-booked rooms** (overlapping date ranges for the same room).

**Answer:**
```python
from pyspark.sql.functions import broadcast

data = [
    (1, "R1", "G1", "2024-03-01", "2024-03-05"),
    (2, "R1", "G2", "2024-03-04", "2024-03-08"),  # overlaps booking 1
    (3, "R1", "G3", "2024-03-09", "2024-03-12"),
    (4, "R2", "G4", "2024-03-01", "2024-03-10"),
    (5, "R2", "G5", "2024-03-08", "2024-03-15"),  # overlaps booking 4
]
bookings_df = spark.createDataFrame(
    data, ["booking_id", "room_id", "guest_id", "check_in", "check_out"]
)
bookings_df = bookings_df \
    .withColumn("check_in",  to_date("check_in")) \
    .withColumn("check_out", to_date("check_out"))

# Self-join to find overlaps: A.check_in < B.check_out AND A.check_out > B.check_in
b1 = bookings_df.alias("b1")
b2 = bookings_df.alias("b2")

overlaps = b1.join(b2,
    (col("b1.room_id")     == col("b2.room_id"))   &
    (col("b1.booking_id")  <  col("b2.booking_id")) &   # avoid self-match & duplicates
    (col("b1.check_in")    <  col("b2.check_out"))  &
    (col("b1.check_out")   >  col("b2.check_in")),
    how="inner"
).select(
    col("b1.room_id"),
    col("b1.booking_id").alias("booking_1"),
    col("b1.check_in").alias("b1_check_in"),
    col("b1.check_out").alias("b1_check_out"),
    col("b2.booking_id").alias("booking_2"),
    col("b2.check_in").alias("b2_check_in"),
    col("b2.check_out").alias("b2_check_out"),
)

overlaps.show(truncate=False)
```

**Expected Output:**
```
+-------+---------+-----------+------------+---------+-----------+------------+
|room_id|booking_1|b1_check_in|b1_check_out|booking_2|b2_check_in|b2_check_out|
+-------+---------+-----------+------------+---------+-----------+------------+
|R1     |1        |2024-03-01 |2024-03-05  |2        |2024-03-04 |2024-03-08  |
|R2     |4        |2024-03-01 |2024-03-10  |5        |2024-03-08 |2024-03-15  |
+-------+---------+-----------+------------+---------+-----------+------------+
```

> **Key concepts:** Self-join with `booking_id <` to avoid symmetric duplicates, standard interval overlap condition: `A.start < B.end AND A.end > B.start`.

---

---

## 📝 Quick Reference — PySpark Functions Cheatsheet

| Concept | PySpark Functions |
|---|---|
| **Window setup** | `Window.partitionBy().orderBy()` |
| **Lag / Lead** | `lag(col, n)`, `lead(col, n)` |
| **Running totals** | `sum().over(window)` |
| **Rank variants** | `row_number()`, `rank()`, `dense_rank()` |
| **Session flag** | `when(...).otherwise(0)` + cumulative `sum()` |
| **Date arithmetic** | `datediff()`, `months_between()`, `add_months()`, `expr("date + interval 1 day")` |
| **Sequence generation** | `sequence(start, end)` + `explode()` |
| **Islands key** | `(date_as_int / 86400) - row_number()` |
| **Cohort offset** | `floor(months_between(order_month, signup_month))` |
| **Pivot** | `.pivot(col, [values]).agg(...)` |
| **Anti join** | `.join(df2, on=key, how="left_anti")` |
| **Set collection** | `collect_set()`, `array_contains()` |
| **Overlap condition** | `A.start < B.end AND A.end > B.start` |

---

## 📋 Interview Tips — What Seniors Are Expected to Know

| Topic | What They Look For |
|---|---|
| **Sessions** | Correct use of `lag()` + cumulative `sum()` for session boundary detection; handling the NULL first-row case |
| **Cohort Analysis** | Normalizing by cohort size at period 0; using `months_between` + `floor`; pivot for wide-format output |
| **Islands** | The `date - row_number` trick for date islands; `state_change` flag for value-change islands |
| **Gaps** | Using `lead()` on island boundaries; correct interval arithmetic (`+1 day` / `-1 day`) |
| **Performance** | Partitioning window specs correctly; avoiding cross-joins in self-joins; using `left_anti` instead of `NOT IN` |

---
*Last updated: April 2026*

