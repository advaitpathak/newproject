# PySpark Interview Questionnaire
## Intermediate to Advanced Level Questions with Detailed Answers

---

## Table of Contents
1. [Window Functions & Analytics](#window-functions--analytics)
2. [Data Parsing & Complex Delimiters](#data-parsing--complex-delimiters)
3. [Aggregations & Rankings](#aggregations--rankings)
4. [Session Analysis & State Changes](#session-analysis--state-changes)
5. [Performance Optimization](#performance-optimization)
6. [Error Handling & Data Quality](#error-handling--data-quality)
7. [Additional Advanced Questions](#additional-advanced-questions)

---

## Window Functions & Analytics

### Q1: Calculate Difference in Flight Fare with Previous Day

**Question:** Suppose we have data about flight prices and we want to calculate the difference in fare with the previous day.
Columns: `date | company_name | price`

**Answer:**

```python
from pyspark.sql import SparkSession
from pyspark.sql.window import Window
from pyspark.sql.functions import col, lag, datediff

# Create sample data
data = [
    ("2024-01-01", "AirlineA", 250.0),
    ("2024-01-02", "AirlineA", 275.0),
    ("2024-01-03", "AirlineA", 260.0),
    ("2024-01-01", "AirlineB", 300.0),
    ("2024-01-02", "AirlineB", 310.0),
    ("2024-01-03", "AirlineB", 295.0)
]

df = spark.createDataFrame(data, ["date", "company_name", "price"])

# Define window partitioned by company and ordered by date
window_spec = Window.partitionBy("company_name").orderBy("date")

# Calculate price difference with previous day
result = df.withColumn("previous_day_price", lag("price", 1).over(window_spec)) \
           .withColumn("price_difference", col("price") - col("previous_day_price"))

result.show()
```

**Output:**
```
+----------+------------+-----+------------------+----------------+
|      date|company_name|price|previous_day_price|price_difference|
+----------+------------+-----+------------------+----------------+
|2024-01-01|    AirlineA|250.0|              null|            null|
|2024-01-02|    AirlineA|275.0|             250.0|            25.0|
|2024-01-03|    AirlineA|260.0|             275.0|           -15.0|
|2024-01-01|    AirlineB|300.0|              null|            null|
|2024-01-02|    AirlineB|310.0|             300.0|            10.0|
|2024-01-03|    AirlineB|295.0|             310.0|           -15.0|
+----------+------------+-----+------------------+----------------+
```

**Key Concepts:**
- Window functions with `partitionBy` and `orderBy`
- `lag()` function to access previous row values
- Handling nulls for first records

---

## Data Parsing & Complex Delimiters

### Q2: Create DataFrame from Data with Mixed Delimiters

**Question:** Suppose we have data with different delimiters. Create a dataframe from it:
`data = [1, "Alice\t30|New York"]`

**Answer:**

```python
from pyspark.sql.functions import split, col

# Sample data with mixed delimiters (tab and pipe)
data = [(1, "Alice\t30|New York"),
        (2, "Bob\t25|Los Angeles"),
        (3, "Charlie\t35|Chicago")]

df = spark.createDataFrame(data, ["id", "data"])

# Method 1: Using split and array indexing
result = df.withColumn("name", split(col("data"), "\t")[0]) \
           .withColumn("age_city", split(col("data"), "\t")[1]) \
           .withColumn("age", split(col("age_city"), "\\|")[0]) \
           .withColumn("city", split(col("age_city"), "\\|")[1]) \
           .select("id", "name", "age", "city")

# Method 2: Chained split (cleaner)
result2 = df.withColumn("split_tab", split(col("data"), "\t")) \
            .withColumn("name", col("split_tab")[0]) \
            .withColumn("age", split(col("split_tab")[1], "\\|")[0]) \
            .withColumn("city", split(col("split_tab")[1], "\\|")[1]) \
            .select("id", "name", "age", "city")

result.show()
```

**Output:**
```
+---+-------+---+------------+
| id|   name|age|        city|
+---+-------+---+------------+
|  1|  Alice| 30|    New York|
|  2|    Bob| 25| Los Angeles|
|  3|Charlie| 35|     Chicago|
+---+-------+---+------------+
```

**Key Concepts:**
- Using `split()` function for different delimiters
- Array indexing in PySpark
- Escaping special characters in regex (`\\|`)
- Chaining transformations

---

## Aggregations & Rankings

### Q3: Get Top 3 Highest Rating Movies

**Question:** SQL or PySpark: 
- Table 1 (t1): movieid, movie_name
- Table 2 (t2): rating, userid, movieid
Get the top 3 highest rating movies

**Answer:**

**PySpark Solution:**
```python
from pyspark.sql.functions import avg, desc, col

# Sample data
movies_data = [
    (1, "The Shawshank Redemption"),
    (2, "The Godfather"),
    (3, "The Dark Knight"),
    (4, "Pulp Fiction"),
    (5, "Forrest Gump")
]

ratings_data = [
    (9.3, 101, 1), (9.2, 102, 1), (9.1, 103, 1),
    (9.0, 101, 2), (8.9, 102, 2), (9.2, 103, 2),
    (8.8, 101, 3), (8.9, 102, 3), (9.0, 103, 3),
    (8.5, 101, 4), (8.7, 102, 4), (8.6, 103, 4),
    (8.3, 101, 5), (8.4, 102, 5), (8.5, 103, 5)
]

t1 = spark.createDataFrame(movies_data, ["movieid", "movie_name"])
t2 = spark.createDataFrame(ratings_data, ["rating", "userid", "movieid"])

# Calculate average rating per movie and join with movie names
result = t2.groupBy("movieid") \
           .agg(avg("rating").alias("avg_rating")) \
           .join(t1, "movieid") \
           .orderBy(desc("avg_rating")) \
           .select("movie_name", "avg_rating") \
           .limit(3)

result.show(truncate=False)
```

**SQL Solution:**
```python
# Register dataframes as temp views
t1.createOrReplaceTempView("movies")
t2.createOrReplaceTempView("ratings")

# SQL query
sql_result = spark.sql("""
    SELECT 
        m.movie_name,
        AVG(r.rating) as avg_rating
    FROM ratings r
    JOIN movies m ON r.movieid = m.movieid
    GROUP BY m.movie_name
    ORDER BY avg_rating DESC
    LIMIT 3
""")

sql_result.show(truncate=False)
```

**Output:**
```
+-------------------------+------------------+
|movie_name               |avg_rating        |
+-------------------------+------------------+
|The Shawshank Redemption |9.2               |
|The Godfather            |9.033333333333333 |
|The Dark Knight          |8.9               |
+-------------------------+------------------+
```

**Key Concepts:**
- Aggregation with `groupBy()` and `agg()`
- Joining dataframes
- Ordering and limiting results
- Using both PySpark API and Spark SQL

---

### Q4: Calculate 7-Day Moving Average

**Question:** Calculate the moving average of the product for the last 7 days.
Data: `date | productid | quantitysold`

**Answer:**

```python
from pyspark.sql.window import Window
from pyspark.sql.functions import avg, col, to_date
from datetime import datetime, timedelta

# Generate sample data for 15 days
dates = [(datetime(2024, 1, 1) + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(15)]
data = []
for date in dates:
    data.append((date, "P001", 100 + (hash(date) % 50)))
    data.append((date, "P002", 200 + (hash(date) % 30)))

df = spark.createDataFrame(data, ["date", "productid", "quantitysold"])
df = df.withColumn("date", to_date(col("date")))

# Define window for 7-day moving average
# rowsBetween(-6, 0) means current row and 6 rows before it (7 days total)
window_spec = Window.partitionBy("productid") \
                    .orderBy("date") \
                    .rowsBetween(-6, 0)

# Calculate moving average
result = df.withColumn("moving_avg_7days", avg("quantitysold").over(window_spec))

result.orderBy("productid", "date").show(20)
```

**Alternative using rangeBetween for date-based window:**
```python
from pyspark.sql.functions import unix_timestamp

# Convert date to seconds for range-based window
df_with_timestamp = df.withColumn("date_unix", unix_timestamp("date"))

# Window spanning 7 days (604800 seconds = 7 days)
window_spec_range = Window.partitionBy("productid") \
                          .orderBy(col("date_unix").cast("long")) \
                          .rangeBetween(-6*86400, 0)  # 6 days back to current day

result2 = df_with_timestamp.withColumn(
    "moving_avg_7days", 
    avg("quantitysold").over(window_spec_range)
).select("date", "productid", "quantitysold", "moving_avg_7days")

result2.orderBy("productid", "date").show(20)
```

**Key Concepts:**
- Window functions with `rowsBetween()` for row-based windows
- `rangeBetween()` for value-based windows (useful for time series)
- Partitioning by product to calculate separate averages
- Date handling and conversion

---

## Session Analysis & State Changes

### Q5: Session Analysis - Group Consecutive "ON" States

**Question:** Given session data of a user, identify distinct sessions where status changes from OFF to ON and ON to OFF.

**Input:**
| time                | status |
|---------------------|--------|
| 2024-06-12 10:00:00 | on     |
| 2024-06-12 10:01:00 | on     |
| 2024-06-12 10:02:00 | off    |
| 2024-06-12 10:03:00 | off    |
| 2024-06-12 10:04:00 | on     |
| 2024-06-12 10:05:00 | on     |

**Expected Output:**
| session_id | session_start       | session_end         | duration_minutes |
|------------|---------------------|---------------------|------------------|
| 1          | 2024-06-12 10:00:00 | 2024-06-12 10:01:00 | 2                |
| 2          | 2024-06-12 10:04:00 | 2024-06-12 10:05:00 | 2                |

**Answer:**

```python
from pyspark.sql import Window
from pyspark.sql.functions import (
    col, lag, when, sum as _sum, min as _min, max as _max,
    unix_timestamp, round, lit
)

# Sample data
data = [
    ("2024-06-12 10:00:00", "on"),
    ("2024-06-12 10:01:00", "on"),
    ("2024-06-12 10:02:00", "off"),
    ("2024-06-12 10:03:00", "off"),
    ("2024-06-12 10:04:00", "on"),
    ("2024-06-12 10:05:00", "on")
]

df = spark.createDataFrame(data, ["time", "status"])
df = df.withColumn("time", col("time").cast("timestamp"))

# Step 1: Identify status changes
window_spec = Window.orderBy("time")
df_with_prev = df.withColumn("prev_status", lag("status").over(window_spec))

# Step 2: Mark session boundaries (when status changes or is first row)
df_with_change = df_with_prev.withColumn(
    "is_new_session",
    when((col("prev_status") != col("status")) | (col("prev_status").isNull()), lit(1))
    .otherwise(lit(0))
)

# Step 3: Create session groups using cumulative sum
df_with_session = df_with_change.withColumn(
    "session_group",
    _sum("is_new_session").over(Window.orderBy("time"))
)

# Step 4: Filter only 'on' sessions and aggregate
on_sessions = df_with_session.filter(col("status") == "on")

result = on_sessions.groupBy("session_group") \
    .agg(
        _min("time").alias("session_start"),
        _max("time").alias("session_end")
    ) \
    .withColumn(
        "duration_minutes",
        round((unix_timestamp("session_end") - unix_timestamp("session_start")) / 60, 0) + 1
    ) \
    .withColumn("session_id", col("session_group")) \
    .select("session_id", "session_start", "session_end", "duration_minutes") \
    .orderBy("session_id")

result.show(truncate=False)
```

**Alternative Approach using monotonically_increasing_id:**
```python
from pyspark.sql.functions import monotonically_increasing_id, row_number

# Create row numbers for consecutive 'on' statuses
df_with_rn = df.withColumn("rn", row_number().over(Window.orderBy("time")))

# Identify status changes
df_with_prev = df_with_rn.withColumn("prev_status", lag("status").over(Window.orderBy("rn")))

# Calculate session boundaries
df_sessions = df_with_prev.withColumn(
    "session_change",
    when(
        (col("status") == "on") & 
        ((col("prev_status") == "off") | (col("prev_status").isNull())),
        lit(1)
    ).otherwise(lit(0))
)

# Create session IDs
df_with_session_id = df_sessions.withColumn(
    "session_id",
    _sum("session_change").over(Window.orderBy("rn"))
)

# Get session details for 'on' status only
final_result = df_with_session_id.filter(col("status") == "on") \
    .groupBy("session_id") \
    .agg(
        _min("time").alias("session_start"),
        _max("time").alias("session_end")
    ) \
    .withColumn(
        "duration_minutes",
        round((unix_timestamp("session_end") - unix_timestamp("session_start")) / 60) + 1
    ) \
    .orderBy("session_id")

final_result.show(truncate=False)
```

**Output:**
```
+----------+-------------------+-------------------+----------------+
|session_id|session_start      |session_end        |duration_minutes|
+----------+-------------------+-------------------+----------------+
|1         |2024-06-12 10:00:00|2024-06-12 10:01:00|2.0             |
|2         |2024-06-12 10:04:00|2024-06-12 10:05:00|2.0             |
+----------+-------------------+-------------------+----------------+
```

**Key Concepts:**
- State change detection using `lag()` window function
- Session identification using cumulative sum
- Grouping consecutive records with same state
- Timestamp arithmetic and duration calculation
- Filtering and aggregating by session groups

---

## Performance Optimization

### Q6: Spark Job Performance Optimization

**Question:** You have a Spark job that's running slower than expected. What are some strategies you would use to optimize the job?

**Answer:**

**1. Data-Level Optimizations:**
```python
# Check data statistics
df.describe().show()
df.printSchema()
print(f"Number of partitions: {df.rdd.getNumPartitions()}")

# Repartition for better parallelism
df_optimized = df.repartition(200)  # Adjust based on data size and cluster

# Use coalesce when reducing partitions (no shuffle)
df_reduced = df.coalesce(50)

# Cache/Persist data when used multiple times
df.cache()  # or df.persist(StorageLevel.MEMORY_AND_DISK)
```

**2. Join Optimizations:**
```python
from pyspark.sql.functions import broadcast

# Broadcast small tables (< 10MB) for join optimization
small_df = spark.read.parquet("small_table.parquet")
large_df = spark.read.parquet("large_table.parquet")

# Broadcast join
result = large_df.join(broadcast(small_df), "key")

# Adjust broadcast threshold if needed
spark.conf.set("spark.sql.autoBroadcastJoinThreshold", 10485760)  # 10MB

# For large-to-large joins, ensure proper partitioning
df1_partitioned = large_df.repartition("join_key")
df2_partitioned = large_df2.repartition("join_key")
result = df1_partitioned.join(df2_partitioned, "join_key")
```

**3. Avoid Expensive Operations:**
```python
# BAD: Using UDF (serialization overhead)
from pyspark.sql.functions import udf
from pyspark.sql.types import StringType

@udf(returnType=StringType())
def uppercase_udf(s):
    return s.upper() if s else None

df_bad = df.withColumn("name_upper", uppercase_udf(col("name")))

# GOOD: Use built-in functions
from pyspark.sql.functions import upper
df_good = df.withColumn("name_upper", upper(col("name")))

# BAD: Using collect() on large datasets
all_data = df.collect()  # Don't do this!

# GOOD: Use sampling or aggregation
sample_data = df.sample(0.01).collect()
summary = df.groupBy("category").count().collect()
```

**4. Predicate Pushdown & Column Pruning:**
```python
# Select only needed columns early
df_filtered = spark.read.parquet("data.parquet") \
    .select("id", "name", "amount") \
    .filter(col("amount") > 1000)

# This is better than:
# df_all = spark.read.parquet("data.parquet")
# df_filtered = df_all.filter(col("amount") > 1000).select("id", "name", "amount")
```

**5. File Format & Compression:**
```python
# Use columnar formats for analytics
df.write.format("parquet").save("output.parquet")  # Better than CSV
df.write.format("orc").save("output.orc")

# Use appropriate compression
df.write.option("compression", "snappy").parquet("output.parquet")
```

**6. Shuffle Optimization:**
```python
# Adjust shuffle partitions based on data size
spark.conf.set("spark.sql.shuffle.partitions", 200)  # Default is 200

# For small data
spark.conf.set("spark.sql.shuffle.partitions", 50)

# For large data
spark.conf.set("spark.sql.shuffle.partitions", 400)
```

**7. Memory Management:**
```python
# Configuration settings (set in spark-submit or SparkSession)
spark = SparkSession.builder \
    .config("spark.executor.memory", "8g") \
    .config("spark.driver.memory", "4g") \
    .config("spark.executor.memoryOverhead", "2g") \
    .config("spark.memory.fraction", "0.8") \
    .config("spark.memory.storageFraction", "0.3") \
    .getOrCreate()
```

**Key Strategies Summary:**
- **Repartition** data for optimal parallelism
- **Cache** frequently used DataFrames
- Use **broadcast joins** for small tables
- Avoid **UDFs** when built-in functions exist
- **Filter early** and select only needed columns
- Use **columnar formats** (Parquet, ORC)
- Tune **shuffle partitions** based on data size
- **Monitor** Spark UI for bottlenecks
- Use **salting** for skewed joins
- Enable **AQE** (Adaptive Query Execution) in Spark 3.x

---

### Q7: Optimizing Join Operations

**Question:** How would you use various techniques to optimize a join operation?

**Answer:**

```python
from pyspark.sql.functions import broadcast, col, concat_ws, lit, rand

# Sample large and small datasets
large_df = spark.range(10000000).withColumn("key", (col("id") % 1000).cast("string"))
small_df = spark.range(1000).withColumnRenamed("id", "key").withColumn("value", lit("data"))

# ===== 1. Broadcast Join (Small Table) =====
print("1. BROADCAST JOIN")
result_broadcast = large_df.join(broadcast(small_df), "key")
# Spark will send the small table to all executors

# ===== 2. Sort-Merge Join (Large Tables) =====
print("2. SORT-MERGE JOIN")
# Pre-partition both dataframes on join key
large_df_part = large_df.repartition(200, "key")
small_df_part = small_df.repartition(200, "key")
result_sortmerge = large_df_part.join(small_df_part, "key")

# ===== 3. Handling Skewed Joins with Salting =====
print("3. SALTING FOR SKEWED DATA")

# Identify skewed keys (example: key "100" appears 1M times)
skewed_key = "100"
salt_factor = 10

# Add salt to the large table
large_df_salted = large_df.withColumn(
    "salt", 
    when(col("key") == skewed_key, (rand() * salt_factor).cast("int"))
    .otherwise(lit(0))
).withColumn("key_salted", concat_ws("_", col("key"), col("salt")))

# Replicate small table with salt
from pyspark.sql.functions import explode, array
salt_array = array([lit(i) for i in range(salt_factor)])

small_df_replicated = small_df.withColumn("salt", explode(salt_array)) \
    .withColumn("key_salted", concat_ws("_", col("key"), col("salt")))

# Join on salted key
result_salted = large_df_salted.join(small_df_replicated, "key_salted") \
    .drop("salt", "key_salted")

# ===== 4. Bucket Join (Pre-bucketing) =====
print("4. BUCKET JOIN")
# Write data pre-bucketed (one-time operation)
large_df.write.bucketBy(100, "key").sortBy("key").saveAsTable("large_table_bucketed")
small_df.write.bucketBy(100, "key").sortBy("key").saveAsTable("small_table_bucketed")

# Read and join (no shuffle needed!)
large_bucketed = spark.table("large_table_bucketed")
small_bucketed = spark.table("small_table_bucketed")
result_bucket = large_bucketed.join(small_bucketed, "key")

# ===== 5. Reduce Data Before Join =====
print("5. PRE-AGGREGATION")
# Aggregate before joining to reduce data volume
large_df_agg = large_df.groupBy("key").agg({"id": "sum"})
result_reduced = large_df_agg.join(small_df, "key")

# ===== 6. Adaptive Query Execution (Spark 3.x) =====
print("6. ENABLE AQE")
spark.conf.set("spark.sql.adaptive.enabled", "true")
spark.conf.set("spark.sql.adaptive.coalescePartitions.enabled", "true")
spark.conf.set("spark.sql.adaptive.skewJoin.enabled", "true")
result_aqe = large_df.join(small_df, "key")
# AQE will automatically optimize at runtime

# ===== 7. Left Semi Join (When only left table columns needed) =====
print("7. LEFT SEMI JOIN")
# If you only need columns from left table
result_semi = large_df.join(small_df, "key", "left_semi")
# More efficient than inner join + select
```

**Join Strategy Decision Tree:**
```python
def choose_join_strategy(left_size, right_size, is_skewed):
    """
    Helper to decide join strategy
    
    Args:
        left_size: Size of left table in bytes
        right_size: Size of right table in bytes
        is_skewed: Boolean indicating if data is skewed
    """
    BROADCAST_THRESHOLD = 10 * 1024 * 1024  # 10MB
    
    if right_size < BROADCAST_THRESHOLD:
        return "BROADCAST"
    elif is_skewed:
        return "SALTING"
    elif left_size > 1e9 and right_size > 1e9:  # Both > 1GB
        return "SORT_MERGE_WITH_AQE"
    else:
        return "SORT_MERGE"

# Example usage
strategy = choose_join_strategy(
    left_size=1e10,  # 10GB
    right_size=5e6,   # 5MB
    is_skewed=False
)
print(f"Recommended strategy: {strategy}")
```

**Key Concepts:**
- **Broadcast Join**: Best for small tables (< 10MB)
- **Sort-Merge Join**: Default for large-to-large joins
- **Salting**: Handles skewed data distribution
- **Bucket Join**: Pre-bucketed data avoids shuffle
- **AQE**: Automatic runtime optimization in Spark 3.x
- **Pre-aggregation**: Reduce data volume before join
- **Semi/Anti Joins**: More efficient when possible

---

## Error Handling & Data Quality

### Q8: Error Handling in PySpark

**Question:** How do you handle errors in PySpark, particularly when dealing with corrupt data or unexpected nulls?

**Answer:**

```python
from pyspark.sql.functions import col, when, isnan, isnull, lit, count
from pyspark.sql.types import StructType, StructField, StringType, IntegerType
import logging

# ===== 1. Handling Corrupt Records During Read =====
print("1. HANDLING CORRUPT RECORDS")

# Define schema with corrupt record column
schema = StructType([
    StructField("id", IntegerType(), True),
    StructField("name", StringType(), True),
    StructField("age", IntegerType(), True),
    StructField("_corrupt_record", StringType(), True)
])

# Read with corrupt record handling
df = spark.read \
    .option("mode", "PERMISSIVE") \  # PERMISSIVE, DROPMALFORMED, or FAILFAST
    .option("columnNameOfCorruptRecord", "_corrupt_record") \
    .schema(schema) \
    .json("data.json")

# Separate good and bad records
good_records = df.filter(col("_corrupt_record").isNull()).drop("_corrupt_record")
bad_records = df.filter(col("_corrupt_record").isNotNull())

# Log bad records
print(f"Corrupt records count: {bad_records.count()}")
bad_records.write.mode("append").json("corrupt_records_log/")

# ===== 2. Handling NULL Values =====
print("2. NULL HANDLING")

# Check for nulls in each column
null_counts = df.select([
    count(when(col(c).isNull(), c)).alias(c) for c in df.columns
])
null_counts.show()

# Strategy A: Drop rows with nulls in critical columns
df_cleaned = df.dropna(subset=["id", "name"])

# Strategy B: Fill nulls with default values
df_filled = df.fillna({
    "age": 0,
    "name": "Unknown",
    "amount": 0.0
})

# Strategy C: Replace nulls conditionally
df_replaced = df.withColumn(
    "age",
    when(col("age").isNull(), lit(25))  # Default age
    .otherwise(col("age"))
)

# ===== 3. Try-Except with UDFs =====
print("3. ERROR HANDLING IN UDFS")

from pyspark.sql.functions import udf
from pyspark.sql.types import FloatType

@udf(returnType=FloatType())
def safe_divide(numerator, denominator):
    try:
        if denominator is None or denominator == 0:
            return None
        return float(numerator) / float(denominator)
    except Exception as e:
        # Log error and return None
        logging.error(f"Division error: {e}")
        return None

df_with_division = df.withColumn("ratio", safe_divide(col("value1"), col("value2")))

# ===== 4. Data Quality Checks =====
print("4. DATA QUALITY FRAMEWORK")

def run_quality_checks(df, checks_config):
    """
    Run data quality checks and return results
    
    Args:
        df: Input DataFrame
        checks_config: Dict of quality checks
    
    Returns:
        Tuple of (clean_df, quality_report)
    """
    quality_report = {}
    
    # Check 1: Null checks
    for col_name in checks_config.get("not_null_columns", []):
        null_count = df.filter(col(col_name).isNull()).count()
        quality_report[f"{col_name}_null_count"] = null_count
    
    # Check 2: Range checks
    for col_name, (min_val, max_val) in checks_config.get("range_checks", {}).items():
        out_of_range = df.filter(
            (col(col_name) < min_val) | (col(col_name) > max_val)
        ).count()
        quality_report[f"{col_name}_out_of_range"] = out_of_range
    
    # Check 3: Uniqueness checks
    for col_name in checks_config.get("unique_columns", []):
        total_count = df.count()
        distinct_count = df.select(col_name).distinct().count()
        duplicates = total_count - distinct_count
        quality_report[f"{col_name}_duplicates"] = duplicates
    
    # Check 4: Pattern matching (e.g., email validation)
    for col_name, pattern in checks_config.get("pattern_checks", {}).items():
        invalid_count = df.filter(~col(col_name).rlike(pattern)).count()
        quality_report[f"{col_name}_invalid_pattern"] = invalid_count
    
    return quality_report

# Example usage
checks_config = {
    "not_null_columns": ["id", "email"],
    "range_checks": {"age": (0, 120), "salary": (0, 1000000)},
    "unique_columns": ["id", "email"],
    "pattern_checks": {
        "email": r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    }
}

quality_report = run_quality_checks(df, checks_config)
print("Quality Report:", quality_report)

# ===== 5. Dead Letter Queue Pattern =====
print("5. DEAD LETTER QUEUE")

def process_with_dlq(df, processing_func, dlq_path):
    """
    Process data with error handling and dead letter queue
    """
    # Add processing attempt marker
    df_with_status = df.withColumn("processing_status", lit("pending"))
    
    # Try processing
    try:
        df_processed = processing_func(df)
        df_processed = df_processed.withColumn("processing_status", lit("success"))
    except Exception as e:
        logging.error(f"Batch processing failed: {e}")
        df_processed = df.withColumn("processing_status", lit("failed")) \
                          .withColumn("error_message", lit(str(e)))
    
    # Separate successful and failed records
    df_success = df_processed.filter(col("processing_status") == "success")
    df_failed = df_processed.filter(col("processing_status") == "failed")
    
    # Write failed records to DLQ
    if df_failed.count() > 0:
        df_failed.write.mode("append").parquet(dlq_path)
        logging.warning(f"Written {df_failed.count()} records to DLQ")
    
    return df_success

# ===== 6. Validation with Great Expectations (Concept) =====
print("6. STRUCTURED VALIDATION")

def validate_dataframe(df):
    """
    Comprehensive validation checks
    """
    validations = []
    
    # Schema validation
    expected_columns = ["id", "name", "age", "email"]
    actual_columns = df.columns
    validations.append({
        "check": "schema_validation",
        "passed": set(expected_columns).issubset(set(actual_columns))
    })
    
    # Row count validation
    row_count = df.count()
    validations.append({
        "check": "min_row_count",
        "passed": row_count > 0,
        "actual": row_count
    })
    
    # Data type validation
    schema_dict = {field.name: str(field.dataType) for field in df.schema.fields}
    validations.append({
        "check": "data_types",
        "passed": True,
        "schema": schema_dict
    })
    
    return validations

# Run validations
validation_results = validate_dataframe(df)
for result in validation_results:
    print(f"Check: {result['check']}, Passed: {result['passed']}")
```

**Best Practices:**
- Use **PERMISSIVE** mode for corrupt record handling
- Implement **data quality checks** before processing
- Log **bad records** to separate location
- Use **dead letter queue** pattern for failed records
- Validate **schema** before processing
- Implement **null handling** strategies
- Add **try-except** blocks in UDFs
- Monitor **data quality metrics**
- Use **schema evolution** for changing data
- Implement **idempotent** processing

---

### Q9: Handling Skewed Data

**Question:** How would you handle skewed data in Spark, and how can this affect the performance of your job? What techniques can you use to reduce skew?

**Answer:**

```python
from pyspark.sql.functions import col, rand, concat, lit, count as _count, floor
from pyspark.sql import Window

# ===== 1. Identifying Skewed Data =====
print("1. IDENTIFY SKEWED DATA")

# Sample dataset with skew
data = [(1, "A") for _ in range(1000000)] + \
       [(i, "B") for i in range(2, 10000)]

df = spark.createDataFrame(data, ["id", "category"])

# Check distribution
skew_check = df.groupBy("category").agg(_count("*").alias("count")) \
               .orderBy(col("count").desc())
skew_check.show()

# Output:
# +--------+-------+
# |category|  count|
# +--------+-------+
# |       A|1000000|  # Skewed!
# |       B|   9998|
# +--------+-------+

# ===== 2. Salting Technique =====
print("2. SALTING FOR JOINS")

# Scenario: Join two tables where one has skewed keys
large_df_skewed = df  # Has skewed "category" column
small_df = spark.createDataFrame([(A", "Info A"), ("B", "Info B")], ["category", "info"])

# Without salting (will have skew issues)
# result = large_df_skewed.join(small_df, "category")

# With salting
salt_factor = 100  # Adjust based on skew level

# Step 1: Add salt to large table
large_df_salted = large_df_skewed.withColumn(
    "salt",
    (rand() * salt_factor).cast("int")
).withColumn(
    "category_salted",
    concat(col("category"), lit("_"), col("salt"))
)

# Step 2: Replicate small table with all salt values
from pyspark.sql.functions import explode, array

salt_values = array([lit(i) for i in range(salt_factor)])
small_df_replicated = small_df.withColumn("salt", explode(salt_values)) \
    .withColumn(
        "category_salted",
        concat(col("category"), lit("_"), col("salt"))
    )

# Step 3: Join on salted key
result_salted = large_df_salted.join(
    small_df_replicated,
    "category_salted"
).select(
    large_df_salted["id"],
    large_df_salted["category"],
    small_df["info"]
)

# ===== 3. Adaptive Query Execution (AQE) =====
print("3. ADAPTIVE QUERY EXECUTION")

# Enable AQE (Spark 3.0+)
spark.conf.set("spark.sql.adaptive.enabled", "true")
spark.conf.set("spark.sql.adaptive.skewJoin.enabled", "true")
spark.conf.set("spark.sql.adaptive.skewJoin.skewedPartitionFactor", "5")
spark.conf.set("spark.sql.adaptive.skewJoin.skewedPartitionThresholdInBytes", "256MB")

# AQE will automatically detect and handle skew at runtime
result_aqe = large_df_skewed.join(small_df, "category")

# ===== 4. Isolated Broadcasting for Skewed Keys =====
print("4. ISOLATED BROADCAST")

from pyspark.sql.functions import broadcast

# Identify skewed keys
skewed_threshold = 100000
key_counts = large_df_skewed.groupBy("category").agg(_count("*").alias("cnt"))
skewed_keys = key_counts.filter(col("cnt") > skewed_threshold).select("category")

# Split data into skewed and non-skewed
skewed_data = large_df_skewed.join(skewed_keys, "category", "inner")
non_skewed_data = large_df_skewed.join(skewed_keys, "category", "left_anti")

# Process separately
# Broadcast join for skewed data (if small_df is small)
result_skewed = skewed_data.join(broadcast(small_df), "category")

# Regular join for non-skewed data
result_non_skewed = non_skewed_data.join(small_df, "category")

# Union results
result_combined = result_skewed.union(result_non_skewed)

# ===== 5. Iterative Processing =====
print("5. ITERATIVE PROCESSING")

def process_in_batches(df, batch_size=100000):
    """
    Process large skewed partitions in smaller batches
    """
    total_rows = df.count()
    num_batches = (total_rows // batch_size) + 1
    
    results = []
    for i in range(num_batches):
        # Process each batch
        batch = df.withColumn("batch_id", (col("id") / batch_size).cast("int")) \
                  .filter(col("batch_id") == i)
        
        # Perform expensive operation on batch
        batch_result = batch.groupBy("category").agg(_count("*").alias("count"))
        results.append(batch_result)
    
    # Combine results
    final_result = results[0]
    for result in results[1:]:
        final_result = final_result.union(result)
    
    return final_result.groupBy("category").agg(_count("*").alias("total_count"))

# ===== 6. Custom Partitioning =====
print("6. CUSTOM PARTITIONING")

def custom_partition(df, partition_col, num_partitions):
    """
    Create custom partitioning to distribute skewed data
    """
    # Add partition column based on hash
    df_partitioned = df.withColumn(
        "custom_partition",
        (floor(rand() * num_partitions)).cast("int")
    ).repartition(num_partitions, "custom_partition", partition_col)
    
    return df_partitioned

# Apply custom partitioning
df_custom_partitioned = custom_partition(large_df_skewed, "category", 200)

# ===== 7. Key Isolation with Multiple Strategies =====
print("7. HYBRID APPROACH")

def handle_skewed_join(large_df, small_df, join_key, skew_threshold=100000):
    """
    Hybrid approach combining multiple techniques
    """
    # Step 1: Identify skewed keys
    key_counts = large_df.groupBy(join_key).agg(_count("*").alias("cnt"))
    skewed_keys = key_counts.filter(col("cnt") > skew_threshold)
    
    # Step 2: Split data
    large_skewed = large_df.join(broadcast(skewed_keys.select(join_key)), join_key)
    large_normal = large_df.join(skewed_keys.select(join_key), join_key, "left_anti")
    
    # Step 3: Process normal data with regular join
    result_normal = large_normal.join(small_df, join_key)
    
    # Step 4: Process skewed data with salting
    salt_factor = 50
    large_skewed_salted = large_skewed.withColumn(
        "salt", (rand() * salt_factor).cast("int")
    ).withColumn(join_key + "_salt", concat(col(join_key), lit("_"), col("salt")))
    
    small_replicated = small_df.withColumn(
        "salt", explode(array([lit(i) for i in range(salt_factor)]))
    ).withColumn(join_key + "_salt", concat(col(join_key), lit("_"), col("salt")))
    
    result_skewed = large_skewed_salted.join(
        small_replicated, join_key + "_salt"
    ).drop("salt", join_key + "_salt")
    
    # Step 5: Combine results
    return result_normal.union(result_skewed)

# Usage
result = handle_skewed_join(large_df_skewed, small_df, "category")

# ===== 8. Monitoring Skew =====
print("8. MONITORING")

def analyze_partition_distribution(df):
    """
    Analyze data distribution across partitions
    """
    from pyspark.sql.functions import spark_partition_id
    
    partition_stats = df.withColumn("partition_id", spark_partition_id()) \
        .groupBy("partition_id") \
        .agg(_count("*").alias("row_count")) \
        .orderBy(col("row_count").desc())
    
    partition_stats.show()
    
    # Calculate skew factor
    stats = partition_stats.agg(
        _max("row_count").alias("max_rows"),
        _min("row_count").alias("min_rows"),
        avg("row_count").alias("avg_rows")
    ).collect()[0]
    
    skew_factor = stats["max_rows"] / stats["avg_rows"] if stats["avg_rows"] > 0 else 0
    print(f"Skew Factor: {skew_factor:.2f}")
    
    if skew_factor > 3:
        print("WARNING: Significant skew detected!")
    
    return partition_stats

# Analyze
analyze_partition_distribution(df)
```

**Performance Impact of Skew:**
1. **Stragglers**: One task takes much longer than others
2. **Memory Issues**: Skewed partitions may cause OOM errors
3. **Inefficient Resource Use**: Most executors idle while one struggles
4. **Increased Job Duration**: Overall job time limited by slowest task

**Skew Reduction Techniques Summary:**
| Technique | Best For | Overhead | Complexity |
|-----------|----------|----------|------------|
| Salting | Joins with severe skew | Medium | Medium |
| AQE | General skew (Spark 3+) | Low | Low |
| Broadcast | Small dimension tables | Low | Low |
| Custom Partitioning | Moderate skew | Low | Medium |
| Iterative Processing | Extreme skew | High | High |
| Hybrid Approach | Production systems | Medium | High |

---

### Q10: Environment-Specific Issues

**Question:** Suppose a job is working fine in lower env but failing in higher env, what approach will you take to resolve this?

**Answer:**

```python
# ===== SYSTEMATIC DEBUGGING APPROACH =====

"""
1. COMPARE ENVIRONMENT CONFIGURATIONS
"""

def compare_spark_configs(env1_config, env2_config):
    """
    Compare Spark configurations between environments
    """
    differences = {}
    
    all_keys = set(env1_config.keys()) | set(env2_config.keys())
    
    for key in all_keys:
        val1 = env1_config.get(key, "NOT_SET")
        val2 = env2_config.get(key, "NOT_SET")
        
        if val1 != val2:
            differences[key] = {"lower_env": val1, "higher_env": val2}
    
    return differences

# Check key configurations
spark_config_check = spark.sparkContext.getConf().getAll()
print("Current Spark Configuration:")
for key, value in sorted(spark_config_check):
    print(f"{key}: {value}")

# Common config differences to check:
critical_configs = [
    "spark.executor.memory",
    "spark.driver.memory",
    "spark.executor.cores",
    "spark.sql.shuffle.partitions",
    "spark.default.parallelism",
    "spark.sql.autoBroadcastJoinThreshold",
    "spark.network.timeout",
    "spark.executor.heartbeatInterval"
]

"""
2. DATA VOLUME & SCALE DIFFERENCES
"""

def analyze_data_volume(path, env_name):
    """
    Analyze data volume differences between environments
    """
    df = spark.read.parquet(path)
    
    stats = {
        "env": env_name,
        "row_count": df.count(),
        "column_count": len(df.columns),
        "partition_count": df.rdd.getNumPartitions(),
        "size_bytes": df.rdd.map(lambda x: len(str(x))).sum()
    }
    
    print(f"\n=== {env_name} Data Stats ===")
    for key, value in stats.items():
        print(f"{key}: {value}")
    
    # Check for data quality issues
    null_counts = df.select([
        _count(when(col(c).isNull(), c)).alias(c) for c in df.columns
    ]).collect()[0].asDict()
    
    print(f"\nNull counts: {null_counts}")
    
    return stats

# Compare data volumes
# lower_stats = analyze_data_volume("s3://lower-env/data/", "LOWER")
# higher_stats = analyze_data_volume("s3://higher-env/data/", "HIGHER")

"""
3. RESOURCE CONSTRAINTS
"""

def check_resource_constraints():
    """
    Check for resource-related issues
    """
    # Memory per executor
    executor_memory = spark.conf.get("spark.executor.memory", "NOT_SET")
    driver_memory = spark.conf.get("spark.driver.memory", "NOT_SET")
    
    print(f"Executor Memory: {executor_memory}")
    print(f"Driver Memory: {driver_memory}")
    
    # Check for memory pressure
    # Monitor GC time in Spark UI
    print("\nCheck Spark UI for:")
    print("- GC time > 10% of task time")
    print("- Spill (memory) and Spill (disk) metrics")
    print("- Task failures and retries")
    
    # Recommendations
    if executor_memory == "NOT_SET":
        print("\nWARNING: Executor memory not explicitly set!")

"""
4. NETWORK & CONNECTIVITY
"""

def test_connectivity(s3_path, dynamodb_table=None):
    """
    Test connectivity to external resources
    """
    try:
        # Test S3 access
        df_test = spark.read.parquet(s3_path).limit(10)
        print(f"✓ S3 access successful: {s3_path}")
        
        # Test write permissions
        test_path = s3_path.rstrip("/") + "/connectivity_test/"
        df_test.write.mode("overwrite").parquet(test_path)
        print(f"✓ S3 write successful: {test_path}")
        
        # Clean up test data
        spark.sql(f"DROP TABLE IF EXISTS test_connectivity")
        
    except Exception as e:
        print(f"✗ Connectivity error: {e}")
        return False
    
    return True

"""
5. PERMISSION & IAM ROLES
"""

def check_permissions():
    """
    Check AWS permissions and IAM roles
    """
    import boto3
    from botocore.exceptions import ClientError
    
    try:
        # Check current identity
        sts = boto3.client('sts')
        identity = sts.get_caller_identity()
        print(f"Current AWS Identity: {identity['Arn']}")
        
        # Check S3 permissions
        s3 = boto3.client('s3')
        buckets = s3.list_buckets()
        print(f"✓ S3 access confirmed - Found {len(buckets['Buckets'])} buckets")
        
        # Check DynamoDB permissions
        dynamodb = boto3.client('dynamodb')
        tables = dynamodb.list_tables()
        print(f"✓ DynamoDB access confirmed - Found {len(tables['TableNames'])} tables")
        
    except ClientError as e:
        print(f"✗ Permission error: {e}")
        return False
    
    return True

"""
6. SCHEMA & DATA TYPE DIFFERENCES
"""

def compare_schemas(df1, df2, env1_name="LOWER", env2_name="HIGHER"):
    """
    Compare schemas between environments
    """
    schema1 = {field.name: str(field.dataType) for field in df1.schema.fields}
    schema2 = {field.name: str(field.dataType) for field in df2.schema.fields}
    
    print(f"\n=== Schema Comparison: {env1_name} vs {env2_name} ===")
    
    # Check for missing columns
    missing_in_env2 = set(schema1.keys()) - set(schema2.keys())
    missing_in_env1 = set(schema2.keys()) - set(schema1.keys())
    
    if missing_in_env2:
        print(f"✗ Columns in {env1_name} but not in {env2_name}: {missing_in_env2}")
    
    if missing_in_env1:
        print(f"✗ Columns in {env2_name} but not in {env1_name}: {missing_in_env1}")
    
    # Check for type mismatches
    common_columns = set(schema1.keys()) & set(schema2.keys())
    type_mismatches = {}
    
    for col in common_columns:
        if schema1[col] != schema2[col]:
            type_mismatches[col] = {
                env1_name: schema1[col],
                env2_name: schema2[col]
            }
    
    if type_mismatches:
        print(f"\n✗ Type mismatches:")
        for col, types in type_mismatches.items():
            print(f"  {col}: {types[env1_name]} vs {types[env2_name]}")
    else:
        print(f"✓ All column types match")

"""
7. DEBUGGING WITH COMPREHENSIVE LOGGING
"""

def create_debug_job(original_job_func):
    """
    Wrapper function with extensive logging
    """
    import time
    import traceback
    
    def debug_wrapper(*args, **kwargs):
        start_time = time.time()
        
        print(f"\n{'='*60}")
        print(f"JOB START: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*60}\n")
        
        # Environment info
        print("=== Environment Information ===")
        print(f"Spark Version: {spark.version}")
        print(f"Spark Master: {spark.sparkContext.master}")
        print(f"App Name: {spark.sparkContext.appName}")
        print(f"Executors: {spark.sparkContext.defaultParallelism}")
        
        # Configuration dump
        print("\n=== Critical Configurations ===")
        for config in critical_configs:
            value = spark.conf.get(config, "NOT_SET")
            print(f"{config}: {value}")
        
        try:
            # Execute actual job
            print("\n=== Executing Job ===")
            result = original_job_func(*args, **kwargs)
            
            end_time = time.time()
            duration = end_time - start_time
            
            print(f"\n{'='*60}")
            print(f"JOB SUCCESS: Duration {duration:.2f} seconds")
            print(f"{'='*60}\n")
            
            return result
            
        except Exception as e:
            end_time = time.time()
            duration = end_time - start_time
            
            print(f"\n{'='*60}")
            print(f"JOB FAILED: Duration {duration:.2f} seconds")
            print(f"{'='*60}\n")
            
            print(f"Error Type: {type(e).__name__}")
            print(f"Error Message: {str(e)}")
            print(f"\nFull Traceback:")
            print(traceback.format_exc())
            
            # Additional diagnostics
            print("\n=== Diagnostic Information ===")
            print("Check Spark UI for:")
            print("- Failed stages and tasks")
            print("- Executor logs")
            print("- Event timeline")
            print("- SQL query plan")
            
            raise
    
    return debug_wrapper

# Usage
@create_debug_job
def my_spark_job(input_path, output_path):
    df = spark.read.parquet(input_path)
    # ... processing ...
    df.write.mode("overwrite").parquet(output_path)

"""
8. SPECIFIC COMMON ISSUES & SOLUTIONS
"""

# Issue 1: Network timeout
spark.conf.set("spark.network.timeout", "800s")
spark.conf.set("spark.executor.heartbeatInterval", "60s")

# Issue 2: Out of memory in higher env (more data)
spark.conf.set("spark.executor.memory", "16g")
spark.conf.set("spark.driver.memory", "8g")
spark.conf.set("spark.sql.shuffle.partitions", "400")  # Increase from default 200

# Issue 3: Serialization issues
spark.conf.set("spark.serializer", "org.apache.spark.serializer.KryoSerializer")
spark.conf.set("spark.kryoserializer.buffer.max", "512m")

# Issue 4: S3 connection issues
spark.conf.set("spark.hadoop.fs.s3a.connection.maximum", "200")
spark.conf.set("spark.hadoop.fs.s3a.connection.timeout", "600000")
spark.conf.set("spark.hadoop.fs.s3a.attempts.maximum", "20")

# Issue 5: Dynamic partition overwrite mode
spark.conf.set("spark.sql.sources.partitionOverwriteMode", "dynamic")

"""
9. SYSTEMATIC CHECKLIST
"""

def environment_debug_checklist():
    """
    Print systematic debugging checklist
    """
    checklist = """
    ╔═══════════════════════════════════════════════════════════════╗
    ║          ENVIRONMENT DEBUGGING CHECKLIST                      ║
    ╠═══════════════════════════════════════════════════════════════╣
    ║  □ 1. Compare Spark configurations (memory, cores, etc.)      ║
    ║  □ 2. Check data volume differences                           ║
    ║  □ 3. Verify schema compatibility                             ║
    ║  □ 4. Test connectivity to S3/DynamoDB/etc.                   ║
    ║  □ 5. Validate IAM roles and permissions                      ║
    ║  □ 6. Check network timeouts and connectivity                 ║
    ║  □ 7. Compare library versions (Spark, AWS SDK, etc.)         ║
    ║  □ 8. Review Spark UI for task failures                       ║
    ║  □ 9. Check executor logs for exceptions                      ║
    ║  □ 10. Verify input data quality and format                   ║
    ║  □ 11. Test with sample data in higher env                    ║
    ║  □ 12. Enable verbose logging                                 ║
    ║  □ 13. Compare environment variables                          ║
    ║  □ 14. Check for data skew in production data                 ║
    ║  □ 15. Verify output path write permissions                   ║
    ╚═══════════════════════════════════════════════════════════════╝
    """
    print(checklist)

# Run checklist
environment_debug_checklist()
```

**Common Environment-Specific Issues:**

| Issue | Lower Env | Higher Env | Solution |
|-------|-----------|------------|----------|
| Data Volume | 1GB | 100GB | Increase partitions & memory |
| Permissions | Broad | Restricted | Update IAM roles |
| Network | Fast | Slow/Firewalled | Increase timeouts |
| Resources | Over-provisioned | Right-sized | Optimize configs |
| Data Quality | Clean | Has nulls/corrupt | Add error handling |
| Dependencies | Latest | Older versions | Version compatibility |

---

## Additional Advanced Questions

### Q11: Deduplication with Complex Keys

**Question:** Remove duplicate records based on multiple columns, keeping the latest record based on timestamp.

**Answer:**

```python
from pyspark.sql.window import Window
from pyspark.sql.functions import row_number, col

# Sample data with duplicates
data = [
    (1, "John", "2024-01-01", 100),
    (1, "John", "2024-01-02", 150),  # Latest for ID=1
    (2, "Jane", "2024-01-01", 200),
    (2, "Jane", "2024-01-01", 200),  # Exact duplicate
    (3, "Bob", "2024-01-03", 300)
]

df = spark.createDataFrame(data, ["id", "name", "date", "amount"])

# Method 1: Using Window function
window_spec = Window.partitionBy("id", "name").orderBy(col("date").desc())

df_deduped = df.withColumn("row_num", row_number().over(window_spec)) \
               .filter(col("row_num") == 1) \
               .drop("row_num")

# Method 2: Using dropDuplicates (simpler but less control)
df_deduped2 = df.orderBy(col("date").desc()) \
                .dropDuplicates(["id", "name"])

df_deduped.show()
```

---

### Q12: Exploding Nested JSON Structures

**Question:** Flatten a nested JSON structure with arrays and nested objects.

**Answer:**

```python
from pyspark.sql.functions import explode, col

# Sample nested JSON data
json_data = '''
[
  {
    "user_id": 1,
    "name": "John",
    "orders": [
      {"order_id": 101, "items": [{"product": "A", "qty": 2}, {"product": "B", "qty": 1}]},
      {"order_id": 102, "items": [{"product": "C", "qty": 3}]}
    ]
  },
  {
    "user_id": 2,
    "name": "Jane",
    "orders": [
      {"order_id": 201, "items": [{"product": "D", "qty": 1}]}
    ]
  }
]
'''

# Read JSON
df = spark.read.json(spark.sparkContext.parallelize([json_data]))

# Explode orders
df_orders = df.withColumn("order", explode(col("orders")))

# Explode items within orders
df_items = df_orders.withColumn("item", explode(col("order.items")))

# Select final columns
result = df_items.select(
    col("user_id"),
    col("name"),
    col("order.order_id").alias("order_id"),
    col("item.product").alias("product"),
    col("item.qty").alias("quantity")
)

result.show()
```

---

### Q13: Cumulative Sum and Running Totals

**Question:** Calculate cumulative sum of sales per product over time.

**Answer:**

```python
from pyspark.sql.window import Window
from pyspark.sql.functions import sum as _sum, col

# Sample sales data
data = [
    ("2024-01-01", "P1", 100),
    ("2024-01-02", "P1", 150),
    ("2024-01-03", "P1", 200),
    ("2024-01-01", "P2", 300),
    ("2024-01-02", "P2", 250),
]

df = spark.createDataFrame(data, ["date", "product", "sales"])

# Window for cumulative sum
window_spec = Window.partitionBy("product") \
                    .orderBy("date") \
                    .rowsBetween(Window.unboundedPreceding, Window.currentRow)

# Calculate cumulative sum
result = df.withColumn("cumulative_sales", _sum("sales").over(window_spec))

result.show()
```

**Output:**
```
+----------+-------+-----+----------------+
|      date|product|sales|cumulative_sales|
+----------+-------+-----+----------------+
|2024-01-01|     P1|  100|             100|
|2024-01-02|     P1|  150|             250|
|2024-01-03|     P1|  200|             450|
|2024-01-01|     P2|  300|             300|
|2024-01-02|     P2|  250|             550|
+----------+-------+-----+----------------+
```

---

### Q14: Pivot and Unpivot Operations

**Question:** Transform data from long format to wide format (pivot) and vice versa (unpivot).

**Answer:**

```python
# Sample data in long format
long_data = [
    ("2024-01", "ProductA", "Sales", 1000),
    ("2024-01", "ProductA", "Units", 50),
    ("2024-01", "ProductB", "Sales", 1500),
    ("2024-01", "ProductB", "Units", 75),
    ("2024-02", "ProductA", "Sales", 1200),
    ("2024-02", "ProductA", "Units", 60),
]

df_long = spark.createDataFrame(long_data, ["month", "product", "metric", "value"])

# PIVOT: Long to wide
df_wide = df_long.groupBy("month", "product") \
                 .pivot("metric", ["Sales", "Units"]) \
                 .sum("value")

df_wide.show()

# Output:
# +-------+--------+-----+-----+
# |  month| product|Sales|Units|
# +-------+--------+-----+-----+
# |2024-01|ProductA| 1000|   50|
# |2024-01|ProductB| 1500|   75|
# |2024-02|ProductA| 1200|   60|
# +-------+--------+-----+-----+

# UNPIVOT: Wide to long (using stack)
from pyspark.sql.functions import expr

df_unpivot = df_wide.select(
    "month",
    "product",
    expr("stack(2, 'Sales', Sales, 'Units', Units) as (metric, value)")
)

df_unpivot.show()
```

---

### Q15: Slowly Changing Dimension (SCD) Type 2

**Question:** Implement SCD Type 2 to track historical changes in dimension data.

**Answer:**

```python
from pyspark.sql.functions import current_timestamp, lit, col, when, max as _max

# Existing dimension data (with history)
existing_data = [
    (1, "John", "New York", "2024-01-01", "9999-12-31", True),
    (2, "Jane", "LA", "2024-01-01", "9999-12-31", True)
]

existing_df = spark.createDataFrame(
    existing_data,
    ["id", "name", "city", "valid_from", "valid_to", "is_current"]
)

# New incoming data
new_data = [
    (1, "John", "Boston"),  # City changed
    (2, "Jane", "LA"),      # No change
    (3, "Bob", "Chicago")   # New record
]

new_df = spark.createDataFrame(new_data, ["id", "name", "city"])

# Identify changes
joined = existing_df.alias("existing").join(
    new_df.alias("new"),
    col("existing.id") == col("new.id"),
    "full_outer"
)

# SCD Type 2 Logic
current_date = "2024-04-13"

# Records that changed (expire old, insert new)
changed = joined.filter(
    (col("existing.id").isNotNull()) &
    (col("new.id").isNotNull()) &
    (col("existing.city") != col("new.city")) &
    (col("existing.is_current") == True)
)

# Expire old records
expired = changed.select(
    col("existing.id").alias("id"),
    col("existing.name").alias("name"),
    col("existing.city").alias("city"),
    col("existing.valid_from").alias("valid_from"),
    lit(current_date).alias("valid_to"),
    lit(False).alias("is_current")
)

# Insert new versions of changed records
new_versions = changed.select(
    col("new.id").alias("id"),
    col("new.name").alias("name"),
    col("new.city").alias("city"),
    lit(current_date).alias("valid_from"),
    lit("9999-12-31").alias("valid_to"),
    lit(True).alias("is_current")
)

# Unchanged records
unchanged = existing_df.join(
    changed.select("existing.id"),
    existing_df.id == col("existing.id"),
    "left_anti"
)

# New records
brand_new = joined.filter(
    col("existing.id").isNull() & col("new.id").isNotNull()
).select(
    col("new.id").alias("id"),
    col("new.name").alias("name"),
    col("new.city").alias("city"),
    lit(current_date).alias("valid_from"),
    lit("9999-12-31").alias("valid_to"),
    lit(True).alias("is_current")
)

# Combine all
final_dimension = unchanged.union(expired).union(new_versions).union(brand_new)

final_dimension.orderBy("id", "valid_from").show()
```

---

## Summary

This questionnaire covers:
- **Window Functions**: lag, lead, moving averages, rankings
- **Complex Transformations**: Session analysis, state changes, pivoting
- **Performance Optimization**: Join strategies, caching, partitioning
- **Error Handling**: Corrupt records, null handling, data quality
- **Skew Management**: Salting, AQE, custom partitioning
- **Production Debugging**: Environment differences, systematic troubleshooting
- **Advanced Patterns**: SCD, deduplication, nested data flattening

**Key Takeaways:**
1. Always understand your data distribution before optimization
2. Use window functions for analytical queries
3. Cache strategically for iterative algorithms
4. Monitor Spark UI for performance bottlenecks
5. Handle errors gracefully with proper logging
6. Test with production-like data volumes
7. Use built-in functions over UDFs for performance
8. Enable AQE for automatic runtime optimization

---

*Created: April 2026*
*Level: Intermediate to Advanced*
*Focus: Production-Ready PySpark Development*

