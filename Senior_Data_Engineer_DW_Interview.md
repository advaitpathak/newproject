# Senior Data Engineer Interview – Data Modeling, DW, Data Lake & Lakehouse
> Level: Mid → Hard | Practical + Theory

---

## Table of Contents
1. [Data Modeling & Dimensional Design](#1-data-modeling--dimensional-design)
2. [Data Warehousing](#2-data-warehousing)
3. [Data Lake](#3-data-lake)
4. [Lakehouse Architecture](#4-lakehouse-architecture)
5. [SQL Practical Questions](#5-sql-practical-questions)
6. [PySpark Practical Questions](#6-pyspark-practical-questions)
7. [Theory Questions (Mid → Hard)](#7-theory-questions-mid--hard)

---

## 1. Data Modeling & Dimensional Design

---

### Q1. [MID] Design a Star Schema for an e-commerce sales system.

**Scenario:**  
You have raw transactional data: orders, customers, products, and dates. Design a star schema.

**Answer:**

```
FACT_SALES
----------
sale_id         (PK, surrogate)
date_key        (FK → DIM_DATE)
customer_key    (FK → DIM_CUSTOMER)
product_key     (FK → DIM_PRODUCT)
store_key       (FK → DIM_STORE)
quantity        (measure)
unit_price      (measure)
discount_amount (measure)
total_amount    (measure, derived: quantity * unit_price - discount)

DIM_DATE
--------
date_key        (PK)
full_date
day_of_week
week_number
month
quarter
year
is_holiday

DIM_CUSTOMER
------------
customer_key    (PK, surrogate)
customer_id     (natural key)
first_name
last_name
email
city
state
country
segment         (B2B / B2C)

DIM_PRODUCT
-----------
product_key     (PK, surrogate)
product_id      (natural key)
product_name
category
sub_category
brand
unit_cost

DIM_STORE
---------
store_key       (PK, surrogate)
store_id
store_name
region
country
channel         (online / retail)
```

**Key Decisions:**
- Surrogate keys decouple the warehouse from source system changes
- Measures live in FACT, descriptive attributes live in DIM
- `total_amount` can be stored (avoid re-computation at query time) or derived (storage vs. accuracy trade-off)

---

### Q2. [MID] What is a Snowflake Schema and when would you prefer it over Star Schema?

**Answer:**

A **Snowflake Schema** normalizes dimension tables into sub-dimensions.

```
DIM_PRODUCT → DIM_CATEGORY → DIM_DEPARTMENT
DIM_CUSTOMER → DIM_CITY → DIM_STATE → DIM_COUNTRY
```

| Aspect | Star Schema | Snowflake Schema |
|---|---|---|
| Query Performance | Faster (fewer JOINs) | Slower (more JOINs) |
| Storage | Higher (denormalized) | Lower (normalized) |
| Maintenance | Easier | More complex |
| ETL complexity | Simpler | Higher |

**When to use Snowflake:**
- Storage is a concern (petabyte-scale)
- Dimensions have very high cardinality sub-levels (e.g., millions of cities)
- Strict data governance requires normalization

**Practical Rule:** In modern cloud DWs (Redshift, BigQuery, Snowflake), storage is cheap → prefer Star Schema for analytics performance.

---

### Q3. [HARD] Implement SCD Type 2 (Slowly Changing Dimension) in PySpark/SQL.

**Scenario:**  
A customer moves from NYC to LA. You must keep full history.

**SCD Type 2 Structure:**
```sql
CREATE TABLE dim_customer (
    customer_key    BIGINT,       -- surrogate key
    customer_id     VARCHAR(50),  -- natural key
    first_name      VARCHAR(100),
    last_name       VARCHAR(100),
    city            VARCHAR(100),
    state           VARCHAR(50),
    effective_date  DATE,
    expiry_date     DATE,         -- NULL or 9999-12-31 means current
    is_current      BOOLEAN,
    record_hash     VARCHAR(64)   -- MD5/SHA of tracked columns
);
```

**PySpark Implementation:**

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col, lit, md5, concat_ws, current_date,
    when, coalesce
)
from pyspark.sql.types import BooleanType
from delta.tables import DeltaTable

spark = SparkSession.builder.appName("SCD2").getOrCreate()

# ── Existing DIM (Delta table) ──────────────────────────────────────────────
dim_path = "s3://my-bucket/dim/dim_customer"
dim_df = spark.read.format("delta").load(dim_path)

# ── Incoming staged data ─────────────────────────────────────────────────────
staged_df = spark.read.parquet("s3://my-bucket/staging/customers/")

# ── Hash tracked columns to detect changes ───────────────────────────────────
TRACKED_COLS = ["first_name", "last_name", "city", "state"]

staged_df = staged_df.withColumn(
    "record_hash",
    md5(concat_ws("||", *[col(c) for c in TRACKED_COLS]))
)

# ── Identify changed records ──────────────────────────────────────────────────
# Join staged to current dim records
current_dim = dim_df.filter(col("is_current") == True)

joined = staged_df.alias("src").join(
    current_dim.alias("tgt"),
    on="customer_id",
    how="left"
)

# New records: no match in DIM
new_records = joined.filter(col("tgt.customer_id").isNull()).select(
    col("src.*"),
    current_date().alias("effective_date"),
    lit("9999-12-31").cast("date").alias("expiry_date"),
    lit(True).alias("is_current")
)

# Changed records: hash mismatch
changed_records = joined.filter(
    col("tgt.customer_id").isNotNull() &
    (col("src.record_hash") != col("tgt.record_hash"))
)

# Step 1: Expire old records in DIM (set expiry_date + is_current = False)
expired_keys = changed_records.select(col("tgt.customer_key")).distinct()

deltaTable = DeltaTable.forPath(spark, dim_path)
deltaTable.alias("tgt").merge(
    expired_keys.alias("src"),
    "tgt.customer_key = src.customer_key AND tgt.is_current = true"
).whenMatchedUpdate(set={
    "is_current": lit(False),
    "expiry_date": current_date()
}).execute()

# Step 2: Insert new versions of changed records + brand new records
inserts = changed_records.select(
    col("src.*"),
    current_date().alias("effective_date"),
    lit("9999-12-31").cast("date").alias("expiry_date"),
    lit(True).alias("is_current")
).unionByName(new_records)

inserts.write.format("delta").mode("append").save(dim_path)
```

**SCD Types Summary:**

| Type | Behavior | Use Case |
|---|---|---|
| SCD 0 | No change allowed | Static data (e.g., birth date) |
| SCD 1 | Overwrite | Correcting errors |
| SCD 2 | New row + history | Full history required |
| SCD 3 | Add prev_value column | Only last change needed |
| SCD 4 | History table | Hybrid – active + history split |
| SCD 6 | Type 1+2+3 combined | Full flexibility |

---

### Q4. [HARD] Design a Data Vault model for the same e-commerce system.

**Answer:**

Data Vault has 3 entity types: **Hub**, **Link**, **Satellite**

```
HUB_CUSTOMER        HUB_PRODUCT          HUB_ORDER
------------        -----------          ---------
customer_hk (PK)    product_hk (PK)      order_hk (PK)
customer_id         product_id           order_id
load_date           load_date            load_date
record_source       record_source        record_source

LINK_ORDER_CUSTOMER_PRODUCT            (relationships)
---------------------------
link_hk (PK)
order_hk   (FK → HUB_ORDER)
customer_hk(FK → HUB_CUSTOMER)
product_hk (FK → HUB_PRODUCT)
load_date
record_source

SAT_CUSTOMER_DETAILS                   (descriptive + changes over time)
--------------------
customer_hk (FK → HUB_CUSTOMER)
load_date   (PK component)
end_date
is_current
city
state
email
hash_diff   (detect changes)
record_source

SAT_PRODUCT_DETAILS
-------------------
product_hk
load_date
end_date
is_current
product_name
price
category
hash_diff
record_source
```

**When to choose Data Vault over Kimball Star Schema:**
- Multiple source systems feeding the warehouse
- Auditability and compliance requirements
- Schema changes are frequent (agile DW)
- Need to track record_source for every row

**Trade-off:** Much more complex queries – typically you build Information Marts (Star Schemas) ON TOP of Data Vault for BI consumption.

---

## 2. Data Warehousing

---

### Q5. [MID] What is partitioning vs. clustering/sorting in a cloud DW?

**Answer:**

**Partitioning** – physically splits data files by a column (e.g., `event_date`).  
Query engine skips irrelevant partitions entirely (partition pruning).

**Clustering/Sorting** – within each partition, data is sorted by one or more columns (e.g., `customer_id`, `product_id`). Reduces the number of data blocks scanned via block-level metadata.

```sql
-- BigQuery example
CREATE TABLE sales.fact_sales
PARTITION BY DATE(sale_date)       -- partition pruning on date
CLUSTER BY customer_id, product_id -- block skipping on customer/product
AS SELECT * FROM sales.fact_sales_raw;

-- Redshift example
CREATE TABLE fact_sales (
    sale_date DATE,
    customer_id BIGINT,
    ...
)
DISTKEY(customer_id)               -- distributes rows across nodes
SORTKEY(sale_date, customer_id);   -- compound sort key
```

**Rule of thumb:**
- Partition on the most common `WHERE` column (usually date)
- Cluster/sort on next most common filter or JOIN columns

---

### Q6. [HARD] Design an incremental load strategy for a 10TB fact table updated daily.

**Answer:**

**Strategy: Incremental Merge (Upsert)**

```
Raw Zone (S3) → Staging Layer → Merge into Fact Table (Delta / Iceberg)
```

```python
from delta.tables import DeltaTable
from pyspark.sql.functions import col

# Load only new/changed data since last watermark
watermark = get_last_watermark()  # from a metadata/control table

incremental_df = (
    spark.read.parquet("s3://raw/fact_sales/")
    .filter(col("updated_at") > watermark)
)

deltaTable = DeltaTable.forPath(spark, "s3://dw/fact_sales/")

deltaTable.alias("tgt").merge(
    incremental_df.alias("src"),
    "tgt.sale_id = src.sale_id"
).whenMatchedUpdateAll(              # UPDATE changed rows
).whenNotMatchedInsertAll(           # INSERT new rows
).execute()

# Update watermark
update_watermark(incremental_df.agg({"updated_at": "max"}).collect()[0][0])
```

**Control Table Pattern:**
```sql
CREATE TABLE etl_control (
    job_name        VARCHAR(100),
    last_run_time   TIMESTAMP,
    rows_processed  BIGINT,
    status          VARCHAR(20),   -- SUCCESS / FAILED
    run_date        DATE
);
```

**Key considerations:**
- Use `updated_at` or CDC (Debezium) as watermark source
- Partition by date to limit scan range even for merges
- Use Z-ORDER (Delta) or OPTIMIZE for small file compaction

---

### Q7. [HARD] What are the differences between Kimball and Inmon approaches?

**Answer:**

| Aspect | Kimball (Bottom-Up) | Inmon (Top-Down) |
|---|---|---|
| Starting point | Data Marts first | Enterprise DW first |
| Model | Dimensional (Star/Snowflake) | 3NF Normalized |
| Development speed | Fast to deliver | Slow initial build |
| Flexibility | Less flexible for new sources | More flexible |
| BI Query perf | Excellent | Requires mart layer |
| Best for | Dept-level analytics fast delivery | Enterprise-wide governance |
| Data Marts | Independent, then conformed | Derived from central DW |

**Modern approach:** Hybrid – build a normalized/vault layer for integration, serve dimensional marts for BI.

---

## 3. Data Lake

---

### Q8. [MID] What is the medallion architecture and how do you implement it?

**Answer:**

```
Bronze (Raw)  →  Silver (Cleansed)  →  Gold (Business-Ready)
```

| Layer | Purpose | Format | Retention |
|---|---|---|---|
| Bronze | Exact copy of source, immutable | Raw JSON/CSV/Parquet | Forever |
| Silver | Deduplicated, typed, validated | Parquet / Delta | 2–5 years |
| Gold | Aggregated, business-logic applied | Delta / Parquet | Per policy |

**PySpark Pipeline Example:**

```python
# ── BRONZE: Raw ingestion (no transformation) ─────────────────────────────
raw_df = spark.read.json("s3://raw/events/2026/04/16/")
raw_df.write.format("delta").mode("append").save("s3://bronze/events/")

# ── SILVER: Cleanse + type cast + deduplicate ─────────────────────────────
from pyspark.sql.functions import col, to_timestamp, trim

bronze_df = spark.read.format("delta").load("s3://bronze/events/")

silver_df = (
    bronze_df
    .dropDuplicates(["event_id"])
    .filter(col("user_id").isNotNull())
    .withColumn("event_ts", to_timestamp(col("event_ts_raw")))
    .withColumn("user_id", trim(col("user_id")))
    .drop("event_ts_raw")
)

silver_df.write.format("delta").mode("overwrite") \
    .option("replaceWhere", "event_date = '2026-04-16'") \
    .save("s3://silver/events/")

# ── GOLD: Aggregate for BI ────────────────────────────────────────────────
from pyspark.sql.functions import count, sum as _sum, date_trunc

gold_df = (
    silver_df
    .groupBy(date_trunc("day", col("event_ts")).alias("event_day"), "event_type")
    .agg(
        count("event_id").alias("event_count"),
        _sum("revenue").alias("total_revenue")
    )
)

gold_df.write.format("delta").mode("overwrite").save("s3://gold/daily_events/")
```

---

### Q9. [HARD] How do you handle schema evolution in a Data Lake?

**Answer:**

**Problem:** Source adds new columns or changes types → breaks downstream pipelines.

**Solutions:**

**1. Schema-on-Read (Parquet + Hive Metastore)**
```python
# Merging schemas automatically
df = spark.read.option("mergeSchema", "true").parquet("s3://silver/orders/")
```

**2. Delta Lake Schema Evolution**
```python
# Auto-merge new columns
df.write.format("delta") \
    .option("mergeSchema", "true") \  # adds new columns
    .mode("append") \
    .save("s3://silver/orders/")

# Overwrite schema entirely (destructive)
df.write.format("delta") \
    .option("overwriteSchema", "true") \
    .mode("overwrite") \
    .save("s3://silver/orders/")
```

**3. Schema Registry (Kafka / Confluent)**
- Enforce compatibility modes: `BACKWARD`, `FORWARD`, `FULL`
- Backward: new schema can read old data
- Forward: old schema can read new data

**4. Contract Testing**
```python
from pyspark.sql.types import StructType, StructField, StringType, LongType

EXPECTED_SCHEMA = StructType([
    StructField("order_id",   StringType(),  False),
    StructField("customer_id",StringType(),  False),
    StructField("amount",     LongType(),    True),
])

def validate_schema(df, expected):
    incoming = set((f.name, f.dataType) for f in df.schema.fields)
    expected_set = set((f.name, f.dataType) for f in expected.fields)
    missing = expected_set - incoming
    if missing:
        raise ValueError(f"Schema mismatch – missing fields: {missing}")

validate_schema(silver_df, EXPECTED_SCHEMA)
```

---

## 4. Lakehouse Architecture

---

### Q10. [MID] Compare Delta Lake, Apache Iceberg, and Apache Hudi.

**Answer:**

| Feature | Delta Lake | Apache Iceberg | Apache Hudi |
|---|---|---|---|
| Origin | Databricks | Netflix | Uber |
| ACID Transactions | ✅ | ✅ | ✅ |
| Time Travel | ✅ | ✅ | ✅ |
| Schema Evolution | ✅ | ✅ (best) | ✅ |
| Upserts/Merges | ✅ (MERGE INTO) | ✅ | ✅ (native upsert focus) |
| Partition Evolution | ❌ (manual) | ✅ (hidden partitioning) | ✅ |
| Streaming support | ✅ | ✅ | ✅ (near-real-time) |
| Engine support | Spark-first | Multi-engine (Flink, Trino) | Spark-first |
| File format | Parquet + `_delta_log` JSON | Parquet + metadata JSON/Avro | Parquet/ORC + `.hoodie` |
| Best for | Databricks ecosystems | Multi-engine, cloud-native | Streaming upserts / CDC |

**When to choose:**
- **Delta Lake** → Databricks environment, batch + streaming
- **Iceberg** → Multi-engine (Spark + Trino + Flink), AWS Glue, Snowflake
- **Hudi** → High-frequency upserts, near real-time CDC pipelines

---

### Q11. [HARD] Implement a CDC (Change Data Capture) pipeline using Hudi.

**Scenario:** MySQL → Debezium → Kafka → Spark Streaming → Hudi on S3

**Answer:**

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json, schema_of_json
from pyspark.sql.types import StructType, StructField, StringType, LongType

spark = SparkSession.builder \
    .appName("CDC-Hudi") \
    .config("spark.serializer", "org.apache.spark.serializer.KryoSerializer") \
    .config("spark.sql.extensions", "org.apache.spark.sql.hudi.HoodieSparkSessionExtension") \
    .getOrCreate()

# ── Read from Kafka (Debezium CDC messages) ───────────────────────────────
kafka_df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "broker:9092") \
    .option("subscribe", "mysql.mydb.orders") \
    .option("startingOffsets", "latest") \
    .load()

# ── Parse Debezium envelope ───────────────────────────────────────────────
debezium_schema = StructType([
    StructField("op",   StringType()),   # c=create, u=update, d=delete
    StructField("after", StructType([
        StructField("order_id",   LongType()),
        StructField("customer_id",LongType()),
        StructField("amount",     StringType()),
        StructField("status",     StringType()),
        StructField("updated_at", LongType()),
    ]))
])

parsed_df = kafka_df.select(
    from_json(col("value").cast("string"), debezium_schema).alias("data")
).select("data.op", "data.after.*")

# Filter out deletes or handle them separately
upsert_df = parsed_df.filter(col("op").isin("c", "u"))

# ── Hudi write configuration ──────────────────────────────────────────────
hudi_options = {
    "hoodie.table.name":                         "orders",
    "hoodie.datasource.write.table.type":        "COPY_ON_WRITE",
    "hoodie.datasource.write.operation":         "upsert",
    "hoodie.datasource.write.recordkey.field":   "order_id",
    "hoodie.datasource.write.precombine.field":  "updated_at",
    "hoodie.datasource.write.partitionpath.field": "status",
    "hoodie.datasource.hive_sync.enable":        "true",
    "hoodie.datasource.hive_sync.table":         "orders",
    "hoodie.datasource.hive_sync.database":      "mydb",
    "hoodie.datasource.hive_sync.partition_fields": "status",
    "hoodie.cleaner.commits.retained":           "10",
    "hoodie.keep.min.commits":                   "20",
}

# ── Streaming write to Hudi ───────────────────────────────────────────────
def write_batch(batch_df, batch_id):
    if batch_df.count() == 0:
        return
    batch_df.write \
        .format("hudi") \
        .options(**hudi_options) \
        .mode("append") \
        .save("s3://my-bucket/hudi/orders/")

query = upsert_df.writeStream \
    .foreachBatch(write_batch) \
    .option("checkpointLocation", "s3://my-bucket/checkpoints/orders/") \
    .trigger(processingTime="60 seconds") \
    .start()

query.awaitTermination()
```

---

### Q12. [HARD] How do you optimize a slow Delta Lake table query?

**Answer:**

**Diagnostics first:**
```python
# Check table stats and file sizes
spark.sql("DESCRIBE DETAIL delta.`s3://silver/orders/`").show(truncate=False)
spark.sql("SELECT * FROM delta.`s3://silver/orders/` VERSION AS OF 5").show()
```

**Optimization techniques:**

```python
# 1. Compact small files (bin-packing)
spark.sql("OPTIMIZE delta.`s3://silver/orders/`")

# 2. Z-ORDER for multi-column pruning (co-locate related data)
spark.sql("""
    OPTIMIZE delta.`s3://silver/orders/`
    ZORDER BY (customer_id, order_date)
""")

# 3. Data skipping – ensure statistics are collected
spark.sql("ANALYZE TABLE delta.`s3://silver/orders/` COMPUTE STATISTICS FOR ALL COLUMNS")

# 4. Vacuum stale files (free storage, invalidates old time travel)
spark.sql("VACUUM delta.`s3://silver/orders/` RETAIN 168 HOURS")  # 7 days

# 5. Partition pruning check
spark.conf.set("spark.databricks.delta.stats.skipping", "true")

# 6. Bloom filter index for high-cardinality columns
spark.sql("""
    CREATE BLOOMFILTER INDEX ON TABLE delta.`s3://silver/orders/`
    FOR COLUMNS(customer_id OPTIONS (fpp=0.1, numItems=50000000))
""")
```

**Checklist:**
- [ ] Are filters hitting partitioned columns?
- [ ] File sizes 128MB–1GB range?
- [ ] Z-ORDER applied on most-filtered non-partition columns?
- [ ] Statistics collected and up-to-date?
- [ ] No excessive small files (run OPTIMIZE regularly)?

---

## 5. SQL Practical Questions

---

### Q13. [MID] Write SQL to find the top 3 products by revenue per region, per month.

```sql
WITH monthly_sales AS (
    SELECT
        d.region,
        DATE_TRUNC('month', d.full_date)    AS sale_month,
        p.product_name,
        SUM(f.total_amount)                 AS total_revenue,
        RANK() OVER (
            PARTITION BY d.region, DATE_TRUNC('month', d.full_date)
            ORDER BY SUM(f.total_amount) DESC
        )                                   AS revenue_rank
    FROM fact_sales      f
    JOIN dim_date        d ON f.date_key    = d.date_key
    JOIN dim_product     p ON f.product_key = p.product_key
    JOIN dim_store       s ON f.store_key   = s.store_key
    GROUP BY d.region, DATE_TRUNC('month', d.full_date), p.product_name
)
SELECT region, sale_month, product_name, total_revenue, revenue_rank
FROM monthly_sales
WHERE revenue_rank <= 3
ORDER BY region, sale_month, revenue_rank;
```

---

### Q14. [MID] Write SQL to calculate 7-day rolling average revenue per customer.

```sql
SELECT
    customer_id,
    sale_date,
    daily_revenue,
    AVG(daily_revenue) OVER (
        PARTITION BY customer_id
        ORDER BY sale_date
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ) AS rolling_7d_avg_revenue
FROM (
    SELECT
        c.customer_id,
        d.full_date                 AS sale_date,
        SUM(f.total_amount)         AS daily_revenue
    FROM fact_sales  f
    JOIN dim_date    d ON f.date_key    = d.date_key
    JOIN dim_customer c ON f.customer_key = c.customer_key
    GROUP BY c.customer_id, d.full_date
) daily
ORDER BY customer_id, sale_date;
```

---

### Q15. [HARD] Write SQL to detect session gaps (sessionization) from clickstream data.

**Problem:** Given user event data, group events into sessions where a session ends if there is more than 30 minutes of inactivity.

```sql
WITH events_with_prev AS (
    SELECT
        user_id,
        event_ts,
        LAG(event_ts) OVER (PARTITION BY user_id ORDER BY event_ts) AS prev_event_ts
    FROM clickstream_events
),
session_starts AS (
    SELECT
        user_id,
        event_ts,
        CASE
            WHEN prev_event_ts IS NULL
              OR DATEDIFF('minute', prev_event_ts, event_ts) > 30
            THEN 1
            ELSE 0
        END AS is_session_start
    FROM events_with_prev
),
session_numbered AS (
    SELECT
        user_id,
        event_ts,
        SUM(is_session_start) OVER (
            PARTITION BY user_id
            ORDER BY event_ts
            ROWS UNBOUNDED PRECEDING
        ) AS session_id
    FROM session_starts
)
SELECT
    user_id,
    session_id,
    MIN(event_ts) AS session_start,
    MAX(event_ts) AS session_end,
    COUNT(*)      AS event_count,
    DATEDIFF('minute', MIN(event_ts), MAX(event_ts)) AS session_duration_min
FROM session_numbered
GROUP BY user_id, session_id
ORDER BY user_id, session_start;
```

---

### Q16. [HARD] Write SQL to identify customers who churned (no purchase in last 90 days but were active before).

```sql
WITH customer_last_purchase AS (
    SELECT
        c.customer_id,
        c.first_name,
        c.last_name,
        MAX(d.full_date) AS last_purchase_date
    FROM fact_sales      f
    JOIN dim_customer    c ON f.customer_key  = c.customer_key
    JOIN dim_date        d ON f.date_key      = d.date_key
    GROUP BY c.customer_id, c.first_name, c.last_name
)
SELECT
    customer_id,
    first_name,
    last_name,
    last_purchase_date,
    DATEDIFF('day', last_purchase_date, CURRENT_DATE) AS days_since_purchase
FROM customer_last_purchase
WHERE
    last_purchase_date < CURRENT_DATE - INTERVAL '90 days'    -- inactive 90+ days
    AND last_purchase_date >= CURRENT_DATE - INTERVAL '365 days' -- was active in last year
ORDER BY days_since_purchase DESC;
```

---

## 6. PySpark Practical Questions

---

### Q17. [MID] Implement a slowly changing fact (late-arriving data) handler in PySpark.

```python
from pyspark.sql.functions import col, current_timestamp, lit

# New batch may contain events with dates in the past (late-arriving)
new_data = spark.read.parquet("s3://staging/events/batch_20260416/")

# Find which dates are affected
affected_dates = new_data.select("event_date").distinct()

# Reload only affected partitions from Silver
existing = spark.read.format("delta").load("s3://silver/events/") \
    .join(affected_dates, on="event_date", how="inner")

# Union old + new, deduplicate
merged = existing.unionByName(new_data) \
    .dropDuplicates(["event_id"]) \
    .withColumn("processed_at", current_timestamp())

# Overwrite only affected partitions (dynamic partition overwrite)
spark.conf.set("spark.sql.sources.partitionOverwriteMode", "dynamic")

merged.write.format("delta") \
    .partitionBy("event_date") \
    .mode("overwrite") \
    .save("s3://silver/events/")
```

---

### Q18. [HARD] Design and implement a generic data quality framework in PySpark.

```python
from dataclasses import dataclass, field
from typing import List, Callable, Optional
from pyspark.sql import DataFrame
from pyspark.sql.functions import col, count, when, isnan, isnull, lit
import json

@dataclass
class DQRule:
    rule_name:   str
    column:      Optional[str]
    check_fn:    Callable[[DataFrame], int]   # returns fail count
    severity:    str = "ERROR"                # ERROR | WARN
    threshold:   float = 0.0                  # allowed failure %

@dataclass
class DQResult:
    rule_name:  str
    column:     Optional[str]
    total_rows: int
    fail_count: int
    severity:   str
    passed:     bool

    @property
    def fail_pct(self):
        return round(self.fail_count / self.total_rows * 100, 2) if self.total_rows else 0


class DataQualityFramework:

    def __init__(self, df: DataFrame):
        self.df         = df
        self.total_rows = df.count()
        self.rules:   List[DQRule]   = []
        self.results: List[DQResult] = []

    # ── Built-in rule builders ────────────────────────────────────────────
    def not_null(self, column: str, severity="ERROR", threshold=0.0):
        self.rules.append(DQRule(
            rule_name = f"{column}_not_null",
            column    = column,
            check_fn  = lambda df: df.filter(col(column).isNull()).count(),
            severity  = severity,
            threshold = threshold,
        ))
        return self

    def unique(self, column: str, severity="ERROR"):
        self.rules.append(DQRule(
            rule_name = f"{column}_unique",
            column    = column,
            check_fn  = lambda df: (
                df.count() - df.select(column).distinct().count()
            ),
            severity  = severity,
        ))
        return self

    def min_value(self, column: str, min_val, severity="ERROR"):
        self.rules.append(DQRule(
            rule_name = f"{column}_min_{min_val}",
            column    = column,
            check_fn  = lambda df: df.filter(col(column) < min_val).count(),
            severity  = severity,
        ))
        return self

    def regex_match(self, column: str, pattern: str, severity="WARN"):
        self.rules.append(DQRule(
            rule_name = f"{column}_regex",
            column    = column,
            check_fn  = lambda df: df.filter(
                ~col(column).rlike(pattern) | col(column).isNull()
            ).count(),
            severity  = severity,
        ))
        return self

    def custom(self, rule_name: str, check_fn: Callable, column=None, severity="ERROR", threshold=0.0):
        self.rules.append(DQRule(rule_name, column, check_fn, severity, threshold))
        return self

    # ── Execute all rules ─────────────────────────────────────────────────
    def run(self) -> "DataQualityFramework":
        for rule in self.rules:
            fail_count = rule.check_fn(self.df)
            fail_pct   = fail_count / self.total_rows * 100 if self.total_rows else 0
            passed     = fail_pct <= rule.threshold * 100

            self.results.append(DQResult(
                rule_name  = rule.rule_name,
                column     = rule.column,
                total_rows = self.total_rows,
                fail_count = fail_count,
                severity   = rule.severity,
                passed     = passed,
            ))
        return self

    def report(self):
        print(f"\n{'─'*60}")
        print(f"  DATA QUALITY REPORT  |  Total rows: {self.total_rows:,}")
        print(f"{'─'*60}")
        for r in self.results:
            status = "✅ PASS" if r.passed else ("❌ FAIL" if r.severity == "ERROR" else "⚠️  WARN")
            print(f"  {status}  {r.rule_name:<35} fail={r.fail_count:>6} ({r.fail_pct}%)")
        print(f"{'─'*60}\n")

    def raise_on_errors(self):
        errors = [r for r in self.results if not r.passed and r.severity == "ERROR"]
        if errors:
            names = [r.rule_name for r in errors]
            raise ValueError(f"Data Quality FAILED: {names}")


# ── Usage ─────────────────────────────────────────────────────────────────
df = spark.read.parquet("s3://silver/orders/")

dq = (
    DataQualityFramework(df)
    .not_null("order_id")
    .not_null("customer_id")
    .unique("order_id")
    .min_value("amount", 0)
    .regex_match("email", r"^[\w.+-]+@[\w-]+\.[a-zA-Z]{2,}$", severity="WARN")
    .custom(
        "amount_not_outlier",
        lambda df: df.filter(col("amount") > 1_000_000).count(),
        column="amount",
        severity="WARN",
        threshold=0.001   # allow 0.1%
    )
    .run()
)

dq.report()
dq.raise_on_errors()
```

---

## 7. Theory Questions (Mid → Hard)

---

### Q19. [MID] What is the difference between OLTP and OLAP?

| Aspect | OLTP | OLAP |
|---|---|---|
| Purpose | Transactional operations | Analytical queries |
| Data model | Normalized (3NF) | Denormalized (Star/Snowflake) |
| Query type | INSERT/UPDATE/DELETE | SELECT with aggregations |
| Row count per query | Few rows | Millions–Billions |
| Latency | Milliseconds | Seconds–Minutes |
| Concurrency | High | Low–Medium |
| Examples | MySQL, PostgreSQL | Redshift, BigQuery, Snowflake |

---

### Q20. [MID] Explain CAP Theorem and its relevance to data engineering.

**CAP Theorem:** A distributed system can only guarantee 2 of 3:
- **C**onsistency – every read sees the latest write
- **A**vailability – every request gets a response
- **P**artition Tolerance – system works despite network failures

**Partition Tolerance is always required** in distributed systems → real trade-off is **CP vs. AP**.

| System | Trade-off | Example |
|---|---|---|
| CP | Consistent, may reject reads during partition | HBase, Zookeeper |
| AP | Always available, may return stale data | Cassandra, DynamoDB |

**Data Engineering relevance:**
- Event streaming (Kafka) → AP (availability over consistency)
- ACID transactions (Delta Lake) → enforces consistency via optimistic concurrency control
- Eventual consistency in data lakes → Silver/Gold layers may lag Bronze by minutes

---

### Q21. [MID] What is data lineage and why does it matter?

**Answer:**

Data lineage tracks the origin, movement, transformation, and consumption of data.

**Why it matters:**
- **Debugging** – trace where a wrong number came from
- **Compliance** – GDPR "right to erasure" requires knowing all data locations
- **Impact analysis** – understand downstream effects before changing a schema
- **Auditability** – financial/regulatory reporting needs proof of data provenance

**Tools:** Apache Atlas, OpenLineage (Marquez), DataHub, Alation, Collibra

**OpenLineage example integration:**
```python
from openlineage.client import OpenLineageClient
from openlineage.client.run import RunEvent, Job, Run, InputDataset, OutputDataset

client = OpenLineageClient.from_environment()
client.emit(RunEvent(
    eventType="COMPLETE",
    job=Job(namespace="my-pipeline", name="silver_orders_transform"),
    run=Run(runId="abc-123"),
    inputs=[InputDataset(namespace="s3://bronze", name="orders")],
    outputs=[OutputDataset(namespace="s3://silver", name="orders")],
))
```

---

### Q22. [HARD] Explain Z-Ordering in Delta Lake and how it differs from traditional indexing.

**Answer:**

**Traditional DB Index (B-Tree):** Points to exact row locations. Works for OLTP, not column-format files.

**Z-Ordering (Space-Filling Curve):**  
Co-locates related data within the same Parquet files by interleaving bits of multiple column values → nearby values in multi-dimensional space end up in the same file.

```
Without Z-ORDER: customer_id=1001 scattered across 500 files
With Z-ORDER (customer_id, order_date): customer_id=1001 concentrated in 5-10 files
```

```sql
OPTIMIZE delta.`s3://silver/orders/`
ZORDER BY (customer_id, order_date);
```

**Delta skips files by reading min/max statistics** per Parquet file. Z-ORDER maximizes the chance that your filter (`WHERE customer_id = 1001`) eliminates most files.

**Limitations:**
- Z-ORDER is not an index – it's a physical data layout
- Only effective if queried columns have sufficient cardinality
- Must be re-run after new data arrives (OPTIMIZE is not incremental by default)
- Use at most 3–4 columns (diminishing returns)

---

### Q23. [HARD] What are the trade-offs of Lambda vs. Kappa Architecture?

**Answer:**

**Lambda Architecture:**
```
Source → [Batch Layer  (Spark)]  → Batch View  ─┐
       → [Speed Layer  (Flink)]  → RT View    ──┤→ Serving Layer (query both)
                                  [Merge views]  ┘
```
- Two separate code paths (batch + stream)
- Batch layer reprocesses and corrects; speed layer covers latency
- **Problem:** Maintaining two code paths for same logic is expensive

**Kappa Architecture:**
```
Source → [Stream Layer (Flink/Kafka Streams)] → Serving Layer
```
- Single code path (everything is a stream)
- Reprocessing = replay Kafka topic with new consumer group
- **Problem:** Reprocessing large history via stream is slow; harder for complex batch aggregations

| Aspect | Lambda | Kappa |
|---|---|---|
| Complexity | High (dual path) | Lower (single path) |
| Reprocessing | Batch re-run | Kafka replay |
| Latency | Near real-time | Real-time |
| Use case | Complex batch + RT | Primarily streaming |
| Modern replacement | Lakehouse (Delta + Structured Streaming) | Same |

**Modern answer:** Most teams adopt a **Lakehouse approach** (Delta Lake + Structured Streaming + batch OPTIMIZE) which collapses both layers into one.

---

### Q24. [HARD] How do you handle PII data in a Data Lake / Lakehouse?

**Answer:**

**1. Classification at ingestion:**
```python
PII_COLUMNS = ["email", "ssn", "phone", "first_name", "last_name", "ip_address"]
```

**2. Encryption at rest + in transit:**
- S3 SSE-KMS per-column or bucket-level
- Column-level encryption in Parquet using Apache Parquet Crypto

**3. Pseudonymization / Tokenization:**
```python
from pyspark.sql.functions import sha2, concat_ws, col

# One-way hash with salt (pseudonymization)
SALT = spark.conf.get("spark.pii.salt")

df_masked = df.withColumn(
    "customer_id_token",
    sha2(concat_ws("||", col("email"), lit(SALT)), 256)
).drop("email")
```

**4. Role-based access with column masking (Unity Catalog / Lake Formation):**
```sql
-- Databricks Unity Catalog
CREATE ROW FILTER mask_pii ON dim_customer (customer_key BIGINT)
RETURN IF(IS_MEMBER('pii_analysts'), TRUE, customer_key = -1);

CREATE COLUMN MASK mask_email
RETURN IF(IS_MEMBER('pii_analysts'), email, '***@***.***');
```

**5. Right to Erasure (GDPR):**
```python
# Delta Lake: delete specific customer data
from delta.tables import DeltaTable

DeltaTable.forPath(spark, "s3://silver/customers/").delete(
    col("customer_id") == "CUST_12345"
)
# Then VACUUM to physically remove files
spark.sql("VACUUM delta.`s3://silver/customers/` RETAIN 0 HOURS")
```

**6. Audit logging:** Track all access to PII tables via CloudTrail / Unity Catalog audit logs.

---

### Q25. [HARD] What is data skew in Spark and how do you fix it?

**Answer:**

**Skew:** One or a few partition keys have vastly more data than others → some tasks take 10× longer.

**Detection:**
```python
# Check partition sizes
df.groupBy(spark_partition_id()).count().orderBy(col("count").desc()).show()
```

**Fix 1 – Salting (most common for large skewed joins):**
```python
from pyspark.sql.functions import col, lit, concat, (rand() * 10).cast("int").alias

SALT_BUCKETS = 10

# Add salt to the large (skewed) table
large_df = large_df.withColumn(
    "salted_key",
    concat(col("customer_id"), lit("_"), (rand() * SALT_BUCKETS).cast("int"))
)

# Explode the small (broadcast candidate) table to match all salts
from pyspark.sql.functions import explode, array, lit as L

small_df = small_df.withColumn(
    "salt_array", array([L(str(i)) for i in range(SALT_BUCKETS)])
).withColumn("salt", explode(col("salt_array"))) \
 .withColumn("salted_key", concat(col("customer_id"), lit("_"), col("salt"))) \
 .drop("salt_array", "salt")

result = large_df.join(small_df, on="salted_key", how="inner")
```

**Fix 2 – Broadcast join (when one table is small):**
```python
from pyspark.sql.functions import broadcast

result = large_df.join(broadcast(small_df), on="customer_id")
```

**Fix 3 – AQE (Adaptive Query Execution) in Spark 3+:**
```python
spark.conf.set("spark.sql.adaptive.enabled", "true")
spark.conf.set("spark.sql.adaptive.skewJoin.enabled", "true")
# Automatically splits skewed partitions
```

**Fix 4 – Repartition before aggregation:**
```python
df.repartition(200, col("customer_id")).groupBy("customer_id").agg(...)
```

---

*End of Interview Guide*  
*Covers: Star/Snowflake Schema, SCD2, Data Vault, Medallion Architecture, Delta/Iceberg/Hudi, CDC, SQL Window Functions, PySpark DQ Framework, Z-Ordering, Lambda/Kappa, PII handling, Data Skew.*

