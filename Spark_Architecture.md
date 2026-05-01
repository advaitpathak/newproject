# Apache Spark Architecture & Components — Detailed Guide

---

## High-Level Architecture Overview

Apache Spark follows a **Master-Worker (Driver-Executor)** architecture. The user submits a job, the **Driver** plans it, the **Cluster Manager** allocates resources, and **Executors** do the actual work.

```
┌──────────────────────────────────────────────────────────────────┐
│                        USER / CLIENT                             │
└──────────────────────────────┬───────────────────────────────────┘
                               │  spark-submit / pyspark / notebook
┌──────────────────────────────▼───────────────────────────────────┐
│                        DRIVER PROGRAM                            │
│                                                                  │
│   ┌─────────────────┐   ┌─────────────────┐  ┌───────────────┐  │
│   │  SparkContext / │   │  DAG Scheduler  │  │ Task Scheduler│  │
│   │  SparkSession   │   │  (Stages/Tasks) │  │ (Assignments) │  │
│   └─────────────────┘   └─────────────────┘  └───────────────┘  │
└──────────────────────────────┬───────────────────────────────────┘
                               │
┌──────────────────────────────▼───────────────────────────────────┐
│                     CLUSTER MANAGER                              │
│          (YARN / Kubernetes / Mesos / Standalone)                │
└────────────┬───────────────────┬──────────────────┬─────────────┘
             │                   │                  │
   ┌──────────▼──────┐  ┌────────▼────────┐  ┌─────▼───────────┐
   │   WORKER NODE 1 │  │  WORKER NODE 2  │  │  WORKER NODE N  │
   │  ┌───────────┐  │  │  ┌───────────┐  │  │  ┌───────────┐  │
   │  │ EXECUTOR  │  │  │  │ EXECUTOR  │  │  │  │ EXECUTOR  │  │
   │  │ ┌───────┐ │  │  │  │ ┌───────┐ │  │  │  │ ┌───────┐ │  │
   │  │ │Task 1 │ │  │  │  │ │Task 3 │ │  │  │  │ │Task 5 │ │  │
   │  │ │Task 2 │ │  │  │  │ │Task 4 │ │  │  │  │ │Task 6 │ │  │
   │  │ └───────┘ │  │  │  │ └───────┘ │  │  │  │ └───────┘ │  │
   │  │ [Cache]   │  │  │  │ [Cache]   │  │  │  │ [Cache]   │  │
   │  └───────────┘  │  │  └───────────┘  │  │  └───────────┘  │
   └─────────────────┘  └─────────────────┘  └─────────────────┘
```

---

## Component 1: Driver Program

### What is it?
The **Driver** is the **brain** of a Spark application. It is the JVM process that runs the `main()` function and coordinates the entire job.

### Responsibilities
- Converts user code into an **execution plan**
- Creates and maintains the **SparkContext / SparkSession**
- Builds the **DAG** (Directed Acyclic Graph) of transformations
- Splits the DAG into **Stages** and **Tasks**
- Sends tasks to **Executors** via the Cluster Manager
- **Collects results** back from executors
- Tracks the **lineage** of all RDDs for fault recovery

### Key Configs
```python
spark = SparkSession.builder \
    .config("spark.driver.memory", "4g") \
    .config("spark.driver.cores", "2") \
    .config("spark.driver.maxResultSize", "2g") \  # Max size of collect() result
    .getOrCreate()
```

### Deploy Modes
```
CLIENT MODE (default):                  CLUSTER MODE:
┌──────────────────┐                   ┌──────────────────────────┐
│  Local Machine   │                   │        Cluster           │
│   [DRIVER]  ◄────┼──── results ────  │   [DRIVER runs inside]   │
│             ────►┼──── submits ────► │   [EXECUTORS run inside] │
└──────────────────┘                   └──────────────────────────┘
Best for: Interactive / Debug           Best for: Production Jobs
```

---

## Component 2: SparkContext & SparkSession

### SparkContext (Spark 1.x low-level API)
- The **original entry point** to Spark
- Creates RDDs, accumulators, broadcast variables
- One SparkContext per JVM

### SparkSession (Spark 2.0+ unified API)
- **Unified entry point** combining SparkContext, SQLContext, HiveContext
- Recommended for all modern Spark code

```python
from pyspark.sql import SparkSession

# Create SparkSession
spark = SparkSession.builder \
    .appName("MySparkApp") \
    .master("yarn") \
    .config("spark.sql.shuffle.partitions", "200") \
    .enableHiveSupport() \
    .getOrCreate()

# Access SparkContext through SparkSession
sc = spark.sparkContext
print(f"App Name    : {sc.appName}")
print(f"Master      : {sc.master}")
print(f"Spark Version: {sc.version}")
print(f"Parallelism : {sc.defaultParallelism}")

# SparkContext creates RDDs
rdd = sc.parallelize([1, 2, 3, 4, 5], numSlices=4)
rdd_file = sc.textFile("s3://bucket/data.txt")
```

### Unified Entry Point — What SparkSession Replaced

| Old Entry Point   | Purpose                  | Now via SparkSession        |
|-------------------|--------------------------|-----------------------------|
| `SparkContext`    | RDD operations           | `spark.sparkContext`        |
| `SQLContext`      | SQL / DataFrame          | `spark` directly            |
| `HiveContext`     | Hive metastore support   | `.enableHiveSupport()`      |
| `StreamingContext`| Micro-batch streaming    | Structured Streaming API    |

---

## Component 3: DAG Scheduler

### What is it?
The **DAG Scheduler** is responsible for converting a logical execution plan (sequence of transformations) into a physical plan of **Stages** and **Tasks**.

### How it works

```
User Code (Transformations)
         │
         ▼
   Logical Plan (Unresolved)
         │  ── Catalog / Analysis
         ▼
   Analyzed Logical Plan
         │  ── Catalyst Optimizer
         ▼
   Optimized Logical Plan
         │  ── Physical Planning
         ▼
  Physical Plan
         │  ── DAG Scheduler
         ▼
   Stages ──► Tasks ──► Executors
```

### Narrow vs Wide Transformations (Stage Boundaries)

```
NARROW TRANSFORMATIONS           WIDE TRANSFORMATIONS
(Same Stage — no shuffle)        (New Stage — causes shuffle)
─────────────────────────        ────────────────────────────
map()                            groupBy()
filter()                         join()
select()                         orderBy()
union()                          distinct()
withColumn()                     repartition()
flatMap()                        reduceByKey()
```

```python
# Example: DAG creates 3 stages here
df = spark.read.parquet("s3://bucket/data/")       # Stage 1 — scan
df2 = df.filter(col("age") > 25)                    # Stage 1 — narrow
df3 = df2.withColumn("senior", lit(True))           # Stage 1 — narrow
df4 = df3.groupBy("city").count()                   # Stage 2 — WIDE (shuffle)
df5 = df4.orderBy("count")                          # Stage 3 — WIDE (shuffle)
df5.show()

# Visualize the execution plan
df5.explain(extended=True)  # Shows Parsed → Analyzed → Optimized → Physical plan
```

---

## Component 4: Task Scheduler

### What is it?
The **Task Scheduler** takes the **Stages** produced by the DAG Scheduler and dispatches individual **Tasks** to Executors, one task per partition.

### Key Concepts
- Each **partition** → **1 Task**
- Tasks run in parallel across executors
- Failed tasks are **retried** automatically
- **Speculative execution** re-launches slow tasks on other nodes

```python
# Each partition becomes one Task
df = spark.read.parquet("s3://bucket/data/")
print(f"Partitions → Tasks per Stage: {df.rdd.getNumPartitions()}")

# Control task count
df_more  = df.repartition(400)    # 400 tasks next stage (shuffle)
df_less  = df.coalesce(50)        # 50 tasks, no shuffle

# Task Scheduler key configs
spark.conf.set("spark.task.maxFailures", "4")     # Retry count before failing job
spark.conf.set("spark.speculation", "true")        # Re-launch straggler tasks
spark.conf.set("spark.speculation.multiplier", "1.5")  # 1.5x median = straggler
spark.conf.set("spark.sql.shuffle.partitions", "200")  # # of tasks after shuffle
```

### Task Lifecycle
```
PENDING ──► RUNNING ──► SUCCESS
                └──► FAILED ──► RETRY (up to maxFailures)
                └──► SPECULATIVE COPY launched in parallel
```

---

## Component 5: Cluster Manager

### What is it?
The **Cluster Manager** is responsible for **allocating compute resources** (CPU cores, memory) to the Spark application. Spark is cluster-manager agnostic.

### Types of Cluster Managers

```python
# 1. LOCAL — Development / Testing only
spark = SparkSession.builder \
    .master("local")        # 1 thread
    # .master("local[4]")   # 4 threads
    # .master("local[*]")   # all CPU cores
    .getOrCreate()

# 2. STANDALONE — Spark's built-in cluster manager
spark = SparkSession.builder \
    .master("spark://master-host:7077") \
    .getOrCreate()

# 3. YARN — Most common in Hadoop/AWS EMR ecosystems
# spark-submit --master yarn --deploy-mode cluster my_job.py

# 4. KUBERNETES — Cloud-native container-based
# spark-submit --master k8s://https://<api-server>:6443 my_job.py

# 5. APACHE MESOS — Legacy (deprecated in Spark 3.2+)
# spark-submit --master mesos://mesos-master:5050 my_job.py
```

### Comparison

| Feature             | Standalone | YARN        | Kubernetes  | Local        |
|---------------------|------------|-------------|-------------|--------------|
| Setup Complexity    | Low        | Medium      | High        | None         |
| Resource Sharing    | No         | Yes         | Yes         | No           |
| Cloud Native        | No         | Partial     | Yes         | No           |
| Container Support   | No         | Limited     | Yes         | No           |
| Best For            | Dev/Test   | Hadoop/EMR  | Microservices| Dev/Debug  |

---

## Component 6: Executors

### What is it?
**Executors** are JVM processes launched on **Worker Nodes** that execute the actual computation and store cached data.

### Responsibilities
- Execute **Tasks** assigned by the Task Scheduler
- **Store/cache** RDDs and DataFrames in memory or disk
- **Report task status** back to the Driver
- Each application gets its own set of executors

```python
# Executor configuration
spark = SparkSession.builder \
    .config("spark.executor.instances", "10")        # How many executors
    .config("spark.executor.cores", "4")             # CPU cores per executor
    .config("spark.executor.memory", "8g")           # JVM heap memory
    .config("spark.executor.memoryOverhead", "2g")   # Off-heap (Python, native)
    .getOrCreate()

# Dynamic Allocation — auto scale executors up/down
spark.conf.set("spark.dynamicAllocation.enabled", "true")
spark.conf.set("spark.dynamicAllocation.minExecutors", "2")
spark.conf.set("spark.dynamicAllocation.maxExecutors", "50")
spark.conf.set("spark.dynamicAllocation.initialExecutors", "5")
```

### Executor Memory Layout
```
┌─────────────────────────────────────────────────────────┐
│         TOTAL EXECUTOR MEMORY (e.g., 10g)               │
│                                                         │
│  ┌──────────────────────────────────────────────────┐   │
│  │  spark.executor.memory = 8g (JVM Heap)           │   │
│  │                                                  │   │
│  │  ┌────────────────────────────────────────────┐  │   │
│  │  │  Reserved Memory  (300 MB) — Spark internal│  │   │
│  │  ├────────────────────────────────────────────┤  │   │
│  │  │  User Memory  (40% of remaining)           │  │   │
│  │  │  → Your objects, UDF data structures       │  │   │
│  │  ├────────────────────────────────────────────┤  │   │
│  │  │  Unified Memory (60% of remaining)         │  │   │
│  │  │  ┌───────────────────┬──────────────────┐  │  │   │
│  │  │  │  Storage Memory   │ Execution Memory  │  │  │   │
│  │  │  │  (cache/persist)  │(shuffle/sort/join)│  │  │   │
│  │  │  │   ◄── can borrow ──►                  │  │  │   │
│  │  │  └───────────────────┴──────────────────┘  │  │   │
│  │  └────────────────────────────────────────────┘  │   │
│  └──────────────────────────────────────────────────┘   │
│  spark.executor.memoryOverhead = 2g (Off-Heap/Python)   │
└─────────────────────────────────────────────────────────┘
```

---

## Component 7: RDD (Resilient Distributed Dataset)

### What is it?
The **foundational data abstraction** of Spark — an immutable, distributed, fault-tolerant collection of records spread across cluster partitions.

### 5 Key Properties of an RDD
| Property | Meaning |
|---|---|
| **Resilient** | Fault-tolerant via lineage graph — lost partitions recomputed |
| **Distributed** | Data split into partitions across worker nodes |
| **Dataset** | A collection of typed records |
| **Immutable** | Never modified in-place; transformations create new RDDs |
| **Lazy** | Transformations don't execute until an **Action** is called |

```python
sc = spark.sparkContext

# ── Creating RDDs ──────────────────────────────────────────────
rdd1 = sc.parallelize([1, 2, 3, 4, 5], numSlices=3)
rdd2 = sc.textFile("s3://bucket/logs/*.txt")
rdd3 = sc.wholeTextFiles("s3://bucket/files/")    # (filename, content) pairs

# ── Transformations (LAZY — build the DAG) ────────────────────
rdd_map    = rdd1.map(lambda x: x * 2)            # Apply function to each element
rdd_filter = rdd1.filter(lambda x: x > 2)          # Keep elements matching condition
rdd_flat   = rdd2.flatMap(lambda line: line.split()) # One-to-many mapping
rdd_sample = rdd1.sample(False, 0.5)               # Random sample

# ── Actions (EAGER — trigger execution) ───────────────────────
result  = rdd1.collect()                # Return all data to driver (careful!)
total   = rdd1.reduce(lambda a, b: a+b) # Aggregate
count   = rdd1.count()                  # Count elements
first   = rdd1.first()                  # First element
top3    = rdd1.take(3)                  # First N elements
rdd1.saveAsTextFile("s3://bucket/out/") # Write to storage

# ── Pair RDDs (Key-Value operations) ──────────────────────────
pair_rdd = sc.parallelize([("NY", 100), ("LA", 200), ("NY", 150)])
grouped  = pair_rdd.groupByKey()                     # Group by key
reduced  = pair_rdd.reduceByKey(lambda a, b: a + b)  # Sum per key (preferred)
sorted_  = pair_rdd.sortByKey(ascending=False)
joined   = pair_rdd.join(sc.parallelize([("NY", "New York")]))

# ── View Lineage ───────────────────────────────────────────────
rdd_chain = rdd1.map(lambda x: x*2).filter(lambda x: x > 4)
print(rdd_chain.toDebugString().decode())
```

---

## Component 8: DataFrame & Dataset API

### What is it?
A **higher-level abstraction** built on top of RDDs with a **schema** (column names + types). DataFrames are optimized by the **Catalyst Optimizer** and **Tungsten engine**.

```python
from pyspark.sql.functions import col, avg, count, desc, lit, when

# ── Reading Data ───────────────────────────────────────────────
df = spark.read \
    .option("header", "true") \
    .option("inferSchema", "true") \
    .parquet("s3://bucket/sales/")

# ── Schema ─────────────────────────────────────────────────────
df.printSchema()
df.dtypes     # List of (column_name, type) tuples

# ── Transformations ────────────────────────────────────────────
result = df \
    .filter(col("amount") > 1000) \
    .select("id", "category", "amount") \
    .withColumn("tax", col("amount") * 0.1) \
    .withColumn("tier", when(col("amount") > 5000, "premium").otherwise("standard")) \
    .groupBy("category") \
    .agg(
        avg("amount").alias("avg_amount"),
        count("id").alias("total_orders")
    ) \
    .orderBy(desc("avg_amount"))

result.show()

# ── SQL Interface ──────────────────────────────────────────────
df.createOrReplaceTempView("sales")
spark.sql("""
    SELECT category,
           AVG(amount)  AS avg_amount,
           COUNT(*)     AS total_orders
    FROM   sales
    WHERE  amount > 1000
    GROUP  BY category
    ORDER  BY avg_amount DESC
""").show()
```

### RDD vs DataFrame vs Dataset

| Feature         | RDD              | DataFrame          | Dataset (Scala/Java) |
|-----------------|------------------|--------------------|----------------------|
| API Level       | Low-level        | High-level         | High-level           |
| Type Safety     | Yes (runtime)    | No (compile-time)  | Yes (compile-time)   |
| Schema          | No               | Yes                | Yes                  |
| Optimization    | Manual           | Catalyst + Tungsten| Catalyst + Tungsten  |
| Language        | All              | All                | Scala / Java only    |
| Performance     | Moderate         | High               | High                 |
| Use Case        | Fine-grained ctrl| SQL-like analytics | Type-safe Java/Scala |

---

## Component 9: Catalyst Optimizer

### What is it?
Spark's **rule-based and cost-based query optimizer** that automatically rewrites and optimizes execution plans before running any code.

### 4 Optimization Phases
```
1. ANALYSIS        → Resolve column names, check schema
2. LOGICAL OPT     → Apply rules (predicate pushdown, constant folding)
3. PHYSICAL PLAN   → Choose join strategy (broadcast vs sort-merge)
4. CODE GENERATION → Generate optimized JVM bytecode (Tungsten)
```

### Key Optimizations

```python
# ── 1. PREDICATE PUSHDOWN ──────────────────────────────────────
# You write: join first, then filter
df_joined = df_orders.join(df_customers, "customer_id") \
                     .filter(col("age") > 25)
# Catalyst rewrites to: filter FIRST (reduces data), then join
# When reading Parquet — filter is pushed to file scan level!

# ── 2. COLUMN PRUNING ─────────────────────────────────────────
df.select("id", "name").filter(col("name") == "Alice")
# Catalyst reads ONLY "id" and "name" columns from Parquet
# All other columns are SKIPPED at the storage level

# ── 3. CONSTANT FOLDING ────────────────────────────────────────
df.filter(col("price") > 100 + 50 * 2)
# Catalyst evaluates: 100 + 50 * 2 = 200 ONCE at plan time
# Not computed per-row at runtime

# ── 4. JOIN REORDERING ────────────────────────────────────────
# Catalyst reorders joins to minimize intermediate result size

# ── 5. BROADCAST JOIN ─────────────────────────────────────────
from pyspark.sql.functions import broadcast
# Small table broadcasted to all executors → no shuffle needed
df_large.join(broadcast(df_small), "id")

# ── Inspect Catalyst plans ────────────────────────────────────
df.explain()                    # Physical plan only
df.explain(extended=True)       # All 4 plan stages
df.explain(mode="formatted")    # Pretty-printed (Spark 3.x)
df.explain(mode="cost")         # With cost estimates
```

---

## Component 10: Tungsten Execution Engine

### What is it?
A **low-level execution engine** that manages memory in binary format (bypassing JVM overhead), generates optimized JVM bytecode, and processes data in columnar batches.

### 3 Key Features

```
┌─────────────────────────────────────────────────────────────┐
│                   TUNGSTEN ENGINE                           │
│                                                             │
│  1. BINARY MEMORY MANAGEMENT                               │
│     → Stores data in compact binary format                 │
│     → Bypasses Java object overhead & GC pressure          │
│     → Off-heap memory support                              │
│                                                             │
│  2. WHOLE-STAGE CODE GENERATION                            │
│     → Fuses multiple operators into ONE JVM function       │
│     → Eliminates virtual function calls between operators  │
│     → Optimized machine code per query                     │
│                                                             │
│  3. VECTORIZED EXECUTION                                   │
│     → Processes data in columnar BATCHES (not row-by-row)  │
│     → Uses CPU cache efficiently (SIMD instructions)       │
└─────────────────────────────────────────────────────────────┘
```

```python
# ── Whole-Stage Code Generation ───────────────────────────────
spark.conf.set("spark.sql.codegen.wholeStage", "true")  # Default: true

# ── Off-Heap Memory (bypass JVM GC) ──────────────────────────
spark.conf.set("spark.memory.offHeap.enabled", "true")
spark.conf.set("spark.memory.offHeap.size", "4g")

# ── Vectorized Parquet Reader ─────────────────────────────────
spark.conf.set("spark.sql.parquet.enableVectorizedReader", "true")
spark.conf.set("spark.sql.inMemoryColumnarStorage.batchSize", "10000")

# ── UDFs bypass Tungsten → prefer built-in functions ─────────
# BAD — Python UDF (goes through serialization, no optimization):
from pyspark.sql.functions import udf
from pyspark.sql.types import DoubleType
my_udf = udf(lambda x: x * 2.0, DoubleType())
df.withColumn("double_val", my_udf(col("amount")))  # Slow!

# GOOD — Built-in function (Tungsten optimized):
df.withColumn("double_val", col("amount") * 2.0)    # Fast!

# BETTER — Pandas UDF (vectorized, still faster than Python UDF):
from pyspark.sql.functions import pandas_udf
import pandas as pd

@pandas_udf(DoubleType())
def pandas_double(s: pd.Series) -> pd.Series:
    return s * 2.0

df.withColumn("double_val", pandas_double(col("amount")))
```

---

## Component 11: Shuffle Service

### What is it?
The mechanism that **redistributes data across executors** when a wide transformation (groupBy, join, orderBy) requires data from different partitions to be co-located.

### Shuffle Process
```
STAGE 1 (Map Phase):              STAGE 2 (Reduce Phase):
┌──────────────────────┐          ┌──────────────────────┐
│ Partition 1          │          │ Reducer 1            │
│  Key A → bucket 1 ──┼──────────┼──► all Key A data    │
│  Key B → bucket 2 ──┼─────┐    │                      │
├──────────────────────┤     │    ├──────────────────────┤
│ Partition 2          │     │    │ Reducer 2            │
│  Key A → bucket 1 ──┼──┐  └───►┼──► all Key B data    │
│  Key C → bucket 3 ──┼──┼──┐    │                      │
├──────────────────────┤  │  │    ├──────────────────────┤
│ Partition 3          │  │  └───►│ Reducer 3            │
│  Key B → bucket 2 ──┼──┘       │──► all Key C data    │
└──────────────────────┘          └──────────────────────┘
        SHUFFLE WRITE                   SHUFFLE READ
        (to disk)                       (from disk/network)
```

```python
# ── Shuffle Tuning ────────────────────────────────────────────
spark.conf.set("spark.sql.shuffle.partitions", "200")      # Default shuffle tasks
spark.conf.set("spark.shuffle.compress", "true")            # Compress shuffle files
spark.conf.set("spark.shuffle.spill.compress", "true")      # Compress spill to disk
spark.conf.set("spark.shuffle.file.buffer", "64k")          # Write buffer size

# ── External Shuffle Service ──────────────────────────────────
# Allows shuffle files to persist after executor deregisters
spark.conf.set("spark.shuffle.service.enabled", "true")  # Required for dynamic alloc

# ── Adaptive Query Execution (Spark 3.x) ─────────────────────
# AQE automatically tunes shuffle partitions at runtime
spark.conf.set("spark.sql.adaptive.enabled", "true")
spark.conf.set("spark.sql.adaptive.coalescePartitions.enabled", "true")
spark.conf.set("spark.sql.adaptive.advisoryPartitionSizeInBytes", "128MB")
spark.conf.set("spark.sql.adaptive.skewJoin.enabled", "true")  # Handle skewed data

# ── Avoid Shuffles with Partitioning ─────────────────────────
# Write data pre-partitioned to avoid shuffle on next read
df.write.partitionBy("date", "region").parquet("s3://bucket/output/")
```

---

## Component 12: Spark Memory Management

### What is it?
The system that **allocates, tracks, and reclaims memory** within each executor for storage (caching) and execution (computation).

```python
# ── Memory Tuning ─────────────────────────────────────────────
spark = SparkSession.builder \
    .config("spark.executor.memory", "8g") \
    .config("spark.memory.fraction", "0.6")         # 60% for Unified Memory
    .config("spark.memory.storageFraction", "0.5")  # 50% of Unified = Storage
    .config("spark.executor.memoryOverhead", "2g")  # Off-heap overhead
    .getOrCreate()

# ── Cache / Persist ───────────────────────────────────────────
from pyspark import StorageLevel

df.cache()                                       # MEMORY_ONLY (default)
df.persist(StorageLevel.MEMORY_ONLY)             # RAM only — fastest
df.persist(StorageLevel.MEMORY_AND_DISK)         # Spill to disk if RAM full
df.persist(StorageLevel.DISK_ONLY)               # Disk only — slowest but safe
df.persist(StorageLevel.MEMORY_ONLY_SER)         # Serialized — less RAM, slower
df.persist(StorageLevel.MEMORY_AND_DISK_SER)     # Serialized + disk fallback
df.persist(StorageLevel.MEMORY_AND_DISK_2)       # Replicated on 2 nodes (HA)
df.unpersist()                                   # Release cached memory

# ── When to Cache ─────────────────────────────────────────────
# Cache when a DataFrame is used MULTIPLE times
df_filtered = df.filter(col("active") == True).cache()  # Used twice below
count1 = df_filtered.count()                             # Reads once, caches
count2 = df_filtered.groupBy("city").count()             # Reads from cache
df_filtered.unpersist()                                  # Free memory when done
```

### Storage Level Comparison

| Level                  | RAM  | Disk | Serialized | Replicas | Speed |
|------------------------|------|------|------------|----------|-------|
| `MEMORY_ONLY`          | ✅   | ❌   | ❌         | 1        | ⚡⚡⚡  |
| `MEMORY_AND_DISK`      | ✅   | ✅   | ❌         | 1        | ⚡⚡   |
| `MEMORY_ONLY_SER`      | ✅   | ❌   | ✅         | 1        | ⚡⚡   |
| `MEMORY_AND_DISK_SER`  | ✅   | ✅   | ✅         | 1        | ⚡    |
| `DISK_ONLY`            | ❌   | ✅   | ✅         | 1        | 🐢   |
| `MEMORY_AND_DISK_2`    | ✅   | ✅   | ❌         | 2        | ⚡⚡   |

---

## Component 13: Broadcast Variables & Accumulators

### Broadcast Variables
Efficiently distribute a **large read-only value** to all executors once, avoiding re-sending it per task.

```python
# Without broadcast — lookup_map sent with EVERY task
lookup_map = {"NY": "New York", "LA": "Los Angeles", "CH": "Chicago"}

# With broadcast — sent ONCE per executor, cached in memory
broadcast_map = sc.broadcast(lookup_map)

# Use in transformation
from pyspark.sql.functions import udf
lookup_udf = udf(lambda code: broadcast_map.value.get(code, "Unknown"))
df.withColumn("city_full", lookup_udf(col("city_code"))).show()

# Or use in RDD
rdd.map(lambda x: broadcast_map.value.get(x, "Unknown"))

# Release when done
broadcast_map.unpersist()
```

### Accumulators
**Distributed counters / aggregators** that executors write to and only the driver can read.

```python
# Custom counters
error_count   = sc.accumulator(0)
null_count    = sc.accumulator(0)
records_count = sc.accumulator(0)

def process_record(row):
    records_count.add(1)
    if row["status"] == "ERROR":
        error_count.add(1)
    if row["value"] is None:
        null_count.add(1)
    return row

df.rdd.foreach(process_record)

print(f"Total Records : {records_count.value}")
print(f"Error Records : {error_count.value}")
print(f"Null Records  : {null_count.value}")
```

---

## Component 14: Spark Streaming (Structured Streaming)

### What is it?
**Structured Streaming** treats a live data stream as an **unbounded DataFrame**, enabling the same DataFrame API for both batch and streaming.

```python
# ── Read from Kafka Stream ─────────────────────────────────────
stream_df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "broker:9092") \
    .option("subscribe", "events-topic") \
    .option("startingOffsets", "latest") \
    .load()

# ── Parse & Transform (same as batch!) ────────────────────────
from pyspark.sql.functions import from_json, window
from pyspark.sql.types import StructType, StringType, IntegerType

schema = StructType() \
    .add("user_id", StringType()) \
    .add("event",   StringType()) \
    .add("amount",  IntegerType()) \
    .add("ts",      StringType())

parsed = stream_df \
    .select(from_json(col("value").cast("string"), schema).alias("data")) \
    .select("data.*")

# ── Windowed Aggregation ───────────────────────────────────────
windowed = parsed \
    .withWatermark("ts", "10 minutes") \
    .groupBy(window(col("ts"), "5 minutes"), col("event")) \
    .sum("amount")

# ── Write Stream ───────────────────────────────────────────────
query = windowed.writeStream \
    .format("parquet") \
    .outputMode("append") \
    .option("checkpointLocation", "s3://bucket/checkpoints/") \
    .option("path", "s3://bucket/output/") \
    .trigger(processingTime="30 seconds") \
    .start()

query.awaitTermination()
```

---

## Full Component Summary Table

| # | Component              | Role                              | Key API / Config                         |
|---|------------------------|-----------------------------------|------------------------------------------|
| 1 | **Driver Program**     | Job orchestration & planning      | `spark.driver.memory`                    |
| 2 | **SparkSession**       | Unified entry point               | `SparkSession.builder.getOrCreate()`     |
| 3 | **DAG Scheduler**      | Logical → Physical plan (Stages)  | `df.explain()`                           |
| 4 | **Task Scheduler**     | Assigns tasks to executors        | `spark.task.maxFailures`                 |
| 5 | **Cluster Manager**    | Resource allocation               | `--master yarn/k8s/spark://`             |
| 6 | **Executors**          | Run tasks, store cache            | `spark.executor.memory/cores/instances`  |
| 7 | **RDD**                | Core distributed data abstraction | `sc.parallelize()`, `sc.textFile()`      |
| 8 | **DataFrame/Dataset**  | Schema-aware high-level API       | `spark.read.*`, `.filter()`, `.groupBy()`|
| 9 | **Catalyst Optimizer** | Query rewriting & optimization    | `df.explain(mode="formatted")`           |
|10 | **Tungsten Engine**    | Binary memory & code generation   | `spark.sql.codegen.wholeStage`           |
|11 | **Shuffle Service**    | Data redistribution between stages| `spark.sql.shuffle.partitions`           |
|12 | **Memory Manager**     | Storage & execution memory alloc  | `spark.memory.fraction`                  |
|13 | **Broadcast/Accum.**   | Shared state across executors     | `sc.broadcast()`, `sc.accumulator()`    |
|14 | **Structured Streaming**| Real-time stream processing      | `spark.readStream`, `writeStream`        |
