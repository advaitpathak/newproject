# Senior Data Engineer — L1 Interview Question Bank

> **Configuration:** Data Engineering (Hard) · Snowflake (Basic + Intermediate + Real-time) · Data Modeling (Basic + Intermediate)
> **Total Questions:** 43

---

## Table of Contents

1. [Data Engineering — Hard](#1-data-engineering--hard)
2. [Snowflake — Basic](#2-snowflake--basic)
3. [Snowflake — Intermediate](#3-snowflake--intermediate)
4. [Snowflake — Real-time Implementations](#4-snowflake--real-time-implementations)
5. [Data Modeling — Basic](#5-data-modeling--basic)
6. [Data Modeling — Intermediate](#6-data-modeling--intermediate)

---

## 1. Data Engineering — Hard

---

### Q1. Design a fault-tolerant, exactly-once data pipeline that ingests 10 TB/day from 50 heterogeneous sources. Walk through your architecture choices.

**Answer:**

Start by separating concerns into three layers: ingestion, processing, and serving.

**Ingestion layer:** Use a message broker like Apache Kafka with at-least-once delivery guarantees per partition. Each source gets its own topic. Use idempotent producers (enable.idempotence=true) and transactional producers where ordering matters. For sources that cannot push to Kafka, deploy pull-based connectors via Kafka Connect.

**Processing layer:** Use Apache Flink or Spark Structured Streaming with checkpointing to durable storage (S3/HDFS). Exactly-once semantics are achieved through two-phase commit (2PC) between the source offset commits and the sink writes. Flink's two-phase sink protocol with Kafka transactions gives true end-to-end exactly-once.

**Sink layer:** Write to a transactional data lake format — Delta Lake or Apache Iceberg — both of which support ACID transactions, preventing partial writes from being visible to readers.

**Fault tolerance mechanisms:**
- Checkpoint every 1–5 minutes so recovery restarts from the last checkpoint, not the beginning
- Dead letter queues (DLQ) for malformed records — never discard data, always route failures
- Circuit breakers per source to prevent one slow source from backing up the entire pipeline
- Schema registry (Confluent or AWS Glue) to validate and evolve schemas without breaking downstream jobs

**Monitoring:** Track per-source lag, consumer group lag, checkpoint duration, and end-to-end latency. Alert on lag exceeding SLA threshold.

---

### Q2. How would you handle late-arriving data in a streaming pipeline where event-time semantics matter? Describe watermarking strategies and trade-offs.

**Answer:**

Late-arriving data is events that arrive at the processing engine after their event timestamp has already passed.

**Watermarking:** A watermark is a heuristic that tells the engine "I believe all events up to time T have now arrived." Any event with timestamp < watermark is considered late.

**Strategies:**

- **Fixed watermark / bounded out-of-orderness:** `watermark = max_event_time_seen - allowed_lateness`. Simple and widely used (Flink's `BoundedOutOfOrdernessWatermarks`). Trade-off: you must pick a static lag bound — too small drops real late data, too large increases result latency.
- **Percentile-based / dynamic watermark:** Compute the Nth percentile of observed delays over a rolling window and use that as the lag. More adaptive but more complex.
- **Session-based watermark:** For user session data, watermark advancement is tied to session inactivity gaps rather than wall clock time.

**Handling events that arrive after the watermark:**
- **Drop:** Simplest, acceptable when lateness is rare and business rules allow it.
- **Side output / late data stream:** Flink and Spark both support routing late records to a separate stream for reprocessing or auditing.
- **Allowed lateness on windows:** Keep window state alive for an extra duration after the watermark passes, re-emitting updated results (e.g., Flink's `allowedLateness`).

**Trade-off summary:** Lower allowed lateness = lower output latency but more dropped/incorrect records. Higher allowed lateness = more correct results but delayed aggregates and higher state memory usage.

---

### Q3. Explain the differences between micro-batch and true streaming processing. When would you choose Spark Structured Streaming vs Apache Flink for a given workload?

**Answer:**

**Micro-batch:** Collects events over a small time window (e.g., 100ms–30s) and processes them as a mini-batch. Spark Structured Streaming operates this way by default. Latency is bounded by the trigger interval.

**True/continuous streaming:** Each event is processed individually as it arrives. Flink and Kafka Streams operate this way. Latency can be sub-millisecond.

**Choose Spark Structured Streaming when:**
- Your team is already invested in the Spark ecosystem (Delta Lake, MLlib, PySpark)
- Workloads are batch-adjacent — e.g., hourly aggregations, large enrichment joins
- You need tight integration with Databricks or EMR
- Latency of seconds is acceptable
- The job involves complex, large-scale stateless transformations or ML inference

**Choose Apache Flink when:**
- You need true low-latency processing (milliseconds)
- Complex stateful operations are required: CEP (complex event processing), pattern detection, session windows
- Exactly-once end-to-end guarantees with external systems (Flink's 2PC sink is more mature)
- High-volume event streams with strict per-event processing requirements (fraud detection, real-time bidding)
- You need fine-grained control over state backends (RocksDB vs heap)

**Rule of thumb:** Spark for analytics-heavy, batch-adjacent pipelines; Flink for event-driven, stateful, low-latency use cases.

---

### Q4. You have a CDC pipeline from an OLTP system that causes extreme skew in your Spark jobs. How do you diagnose and resolve this without modifying the source?

**Answer:**

**Diagnosis steps:**
1. Check Spark UI → Stages tab → look for tasks with dramatically longer duration than peers (one task taking 10× longer than the median indicates skew)
2. Identify the key causing skew: run a `groupBy(join_key).count()` on the raw CDC data to find high-cardinality hot keys
3. Common culprits in CDC: a single customer/tenant ID with millions of events, NULL keys, or a "system" user generating bulk updates

**Resolution strategies (without touching the source):**

- **Salting:** Append a random suffix (0–N) to the hot key before the join/aggregation, then strip it after. This distributes one logical key across N partitions.
  ```
  hot_key + "_" + rand(0, 10)  →  join  →  aggregate  →  drop suffix
  ```
- **Broadcast join:** If one side of the join is small enough (< a few GB), broadcast it to all executors, eliminating the shuffle entirely.
- **Repartition on composite key:** Instead of partitioning on the skewed key alone, use a composite of `(key, date)` or `(key, hash_bucket)`.
- **Adaptive Query Execution (AQE):** In Spark 3+, enable `spark.sql.adaptive.enabled=true` and `spark.sql.adaptive.skewJoin.enabled=true`. Spark will automatically split skewed partitions at runtime.
- **Isolate hot keys:** Detect and separate the top-N hot keys, process them independently with their own broadcast join path, and union results with the main path.

---

### Q5. Describe how you would architect a data mesh with independent domain pipelines while still enforcing global data contracts and lineage tracking.

**Answer:**

A data mesh treats data as a product owned by domain teams. The architectural challenge is autonomy vs. governance.

**Domain ownership layer:**
- Each domain (e.g., Orders, Payments, Users) owns its own pipelines, storage, and compute
- Domains publish data products — curated, documented, versioned datasets — via a standardised interface (e.g., a registered table in a central data catalog like Apache Atlas or DataHub)

**Global data contracts:**
- Define schemas using a schema registry (Confluent or AWS Glue Schema Registry)
- Contracts are specified as JSON Schema, Avro, or Protobuf and versioned
- Breaking changes require a deprecation period with backward-compatible versions running in parallel
- CI/CD pipelines for data products include schema compatibility checks (BACKWARD, FORWARD, FULL compatibility modes) before publishing

**Federated governance:**
- A central platform team maintains the catalog, contract tooling, and policy engine (e.g., OPA for access control)
- Domain teams own the data; the platform team owns the infrastructure and standards
- SLAs (freshness, quality scores, null rate thresholds) are declared in the data product metadata and monitored centrally

**Lineage tracking:**
- Instrument all pipelines with OpenLineage events emitted to a lineage backend (Marquez or DataHub)
- Each pipeline emits a `RunEvent` at start, complete, and fail, with dataset inputs and outputs
- The central catalog aggregates lineage into a graph, enabling column-level lineage across domain boundaries

---

### Q6. How do you ensure idempotency in a pipeline that writes to both a data lake and a downstream OLAP store simultaneously?

**Answer:**

Idempotency means running the pipeline multiple times with the same input produces the same output — no duplicates, no gaps.

**Strategy:**

**1. Assign a deterministic run/batch ID:** Derive a unique key from the source range (e.g., `md5(source + start_ts + end_ts)`). This ID travels through the entire pipeline.

**2. Data lake writes (Delta / Iceberg):**
- Use `MERGE INTO` (upsert) keyed on the natural primary key of the record
- Or use `replaceWhere` / partition overwrite: overwrite the exact partition being reprocessed rather than appending
- Never use naked `append` mode for reprocessable pipelines

**3. OLAP store writes (e.g., Snowflake, BigQuery, Redshift):**
- Use `MERGE` statements keyed on business primary key
- For insert-only tables, use a `pipeline_run_id` column and `DELETE WHERE pipeline_run_id = :id` before re-inserting
- Alternatively, use staging tables: write to a staging table first, then do a final MERGE into the production table atomically

**4. Two-phase write pattern:**
- Write to data lake first (durable, ACID)
- Only after the lake write is confirmed, trigger the OLAP load
- On failure, the OLAP job retries using the already-committed lake data — no re-extraction from source needed

**5. Exactly-once at the orchestration level:**
- Use an idempotency key in your orchestrator (Airflow, Prefect) so that re-triggered DAG runs for the same logical execution date skip already-completed tasks

---

### Q7. Walk through how you'd implement schema evolution in an event-driven architecture using a schema registry. What happens when a breaking change is unavoidable?

**Answer:**

**Normal evolution (non-breaking):**
- Adding optional fields with defaults is backward-compatible
- Removing optional fields is forward-compatible
- Schema registry enforces compatibility mode (BACKWARD by default in Confluent): new schema must be able to read data written with the previous schema
- Producers register the new schema version; consumers continue working because they can deserialize old and new messages

**Process:**
1. Developer proposes schema change in a PR
2. CI pipeline runs a compatibility check against the registry: `schema-registry-cli test-compatibility`
3. If compatible, merge and deploy the producer with the new schema version
4. Consumers are updated independently (loose coupling is the benefit)

**Breaking changes (e.g., renaming a field, changing a type):**
When unavoidable, use the dual-write / topic versioning pattern:

1. **Version the topic:** Create `orders.v2` alongside `orders.v1`
2. **Deploy a bridge consumer:** Reads from `orders.v1`, transforms to the new schema, writes to `orders.v2`
3. **Migrate consumers:** Redirect consumers to `orders.v2` one by one, validating each
4. **Deprecate v1:** Once all consumers are on v2, stop the bridge and eventually delete the old topic (after retention period)

This keeps the system running with zero downtime and gives teams time to migrate at their own pace.

---

### Q8. A pipeline SLA breach at 2 AM — what are the first five steps you take? How do you build observability so this doesn't repeat?

**Answer:**

**Immediate response (first 5 steps):**

1. **Acknowledge and assess blast radius:** Is this one pipeline or many? Are downstream dashboards, ML models, or business reports affected? Communicate immediately to stakeholders.
2. **Check the most recent successful run:** Identify exactly when the pipeline last succeeded and what changed since then (code deploy? volume spike? upstream schema change?).
3. **Examine logs and error messages:** Go to the orchestrator UI (Airflow, Prefect), find the failed task, read the full stack trace. Is it an OOM, a timeout, a connection error, or a data quality failure?
4. **Check upstream data sources:** Has the source system stopped sending data? Is there unusual volume (10× normal = possible source bug or load spike)?
5. **Decide: fix forward or roll back:** If a code change caused it, roll back immediately. If it's an infrastructure issue (disk full, warehouse suspended), fix and re-trigger. Do not try to debug a complex code issue at 2 AM — restore service first.

**Observability to prevent recurrence:**

- **Metrics:** Pipeline duration, record count, byte volume, lag behind watermark — alert on deviation > 2σ from the rolling baseline
- **Freshness checks:** Data quality framework (Great Expectations, dbt tests, Soda) checks that tables were updated within the expected window
- **Dead letter queue monitoring:** Alert if DLQ message count exceeds threshold
- **SLA tracking in orchestrator:** Airflow's SLA miss callbacks, Prefect automations, or Dagster freshness policies
- **Runbooks:** Every pipeline has a linked runbook covering common failure modes, restart procedures, and escalation contacts

---

### Q9. How would you design a cost-efficient data lakehouse that serves both real-time dashboards (sub-second) and large-scale batch ML feature engineering jobs without resource contention?

**Answer:**

**Core principle: separate storage, separate compute, shared data.**

**Storage layer:**
- Use a single open table format (Delta Lake or Apache Iceberg) on object storage (S3/GCS/ADLS) as the single source of truth
- Organise tables into Bronze (raw), Silver (cleaned/joined), Gold (aggregated/feature store) layers

**Compute separation:**
- Provision dedicated, isolated compute clusters per workload type:
  - **Serving cluster** (small, always-on, optimised for fast point queries): Trino/Presto or a Snowflake XS warehouse for dashboard queries
  - **Batch ML cluster** (large, auto-scaling, spot/preemptible instances): Spark on Databricks or EMR, scheduled during off-peak hours
- Compute clusters never share resources — they both read from the same storage but scale independently

**Real-time serving optimisation:**
- Pre-aggregate Gold layer tables in a scheduled micro-batch (5–15 min) for dashboard KPIs
- Use Z-ordering or file compaction (Delta's OPTIMIZE) on frequently queried columns so the serving cluster reads fewer files
- Cache hot aggregations in a fast serving layer (DynamoDB, Redis, or Snowflake result cache) for sub-second response

**Cost controls:**
- Batch ML jobs use spot/preemptible instances (60–80% cheaper) with checkpointing to handle interruptions
- Auto-suspend serving warehouse when query rate drops (e.g., nights, weekends)
- Use table statistics and file skipping aggressively to reduce data scanned

---

### Q10. You need to migrate a legacy on-prem Hadoop pipeline to a cloud-native stack with zero downtime and no data loss. Walk through your migration strategy, rollback plan, and cutover approach.

**Answer:**

**Phase 1 — Discovery and baseline (weeks 1–2):**
- Catalog all jobs: input sources, output tables, schedules, SLAs, downstream consumers
- Profile data volumes, peak throughput, and transformation logic
- Identify hard dependencies (on-prem databases, NFS mounts, custom UDFs)

**Phase 2 — Parallel build (weeks 3–8):**
- Re-implement pipelines in the cloud-native stack (Spark on Databricks / Glue, orchestrated by Airflow or Prefect)
- Run both old and new pipelines simultaneously (shadow mode): the legacy pipeline remains authoritative, the new one runs in parallel but its output is not served to consumers
- Implement a reconciliation job that compares old vs new output row counts, checksums, and key metrics daily

**Phase 3 — Validation and gradual cutover:**
- Validate reconciliation results reach < 0.01% discrepancy threshold
- Identify low-risk pipelines (non-critical, infrequent) and cut them over first
- For each pipeline: update downstream consumers to read from the new table, monitor for 1–2 cycles, then decommission the legacy job
- Use a feature flag or DNS/alias switch so consumers point to new tables without code changes

**Rollback plan:**
- Keep legacy jobs and output tables intact until full cutover is confirmed stable (minimum 2-week observation period)
- If an issue is found post-cutover, flip the alias back to the legacy table — consumers are unaffected
- Never delete legacy data until a full audit cycle has passed

**Data loss prevention:**
- Use Change Data Capture on source systems during migration to ensure no events are missed during the transition window
- Cross-validate record counts at source vs destination at every stage

---

## 2. Snowflake — Basic

---

### Q1. What is a virtual warehouse in Snowflake and how does it differ from a traditional database compute layer?

**Answer:**

A virtual warehouse in Snowflake is an independently provisioned cluster of compute resources (CPU, memory, local SSD cache) that executes SQL queries. It is entirely separate from the storage layer.

**Key differences from traditional databases:**

| Aspect | Traditional DB | Snowflake Virtual Warehouse |
|---|---|---|
| Compute + storage | Tightly coupled | Fully decoupled |
| Scaling | Requires DBA intervention, often downtime | Resize or add clusters in seconds |
| Multiple workloads | Shared compute causes contention | Separate warehouses per workload, no contention |
| Cost | Always running | Billed per second, auto-suspend when idle |

A virtual warehouse can be resized (XS to 6XL) or set to multi-cluster mode, where Snowflake automatically adds or removes clusters based on query concurrency. This means a spike in dashboard users does not slow down a background ETL job if they are on separate warehouses.

---

### Q2. Explain Snowflake's multi-cluster architecture — what are the three main layers and what does each do?

**Answer:**

Snowflake's architecture has three distinct layers, each independently scalable:

**1. Cloud Services Layer (the brain):**
- Handles authentication, query parsing, optimisation, and metadata management
- Maintains the global metadata store: table definitions, statistics, access control lists
- Always running; no user management needed

**2. Query Processing Layer (the muscle):**
- Virtual warehouses live here
- Each warehouse is a cluster of EC2/Azure VM/GCP instances with local SSD cache
- Completely isolated — multiple warehouses can run concurrently against the same data without contention
- Billed per second of activity

**3. Database Storage Layer (the data):**
- All data is stored in Snowflake-managed object storage (S3, Azure Blob, or GCS)
- Data is automatically compressed, columnar, and micro-partitioned (files of ~16 MB compressed)
- Storage is billed separately from compute, at flat object storage rates
- Supports Time Travel and Fail Safe at this layer

---

### Q3. What is Time Travel in Snowflake? How long can data be retained and what are common use cases?

**Answer:**

Time Travel allows you to query, clone, or restore data from any point within a defined retention window, even after it has been modified or deleted.

**Retention periods:**
- Standard edition: up to 1 day (default is 1 day)
- Enterprise edition and above: up to 90 days, configurable per table/schema/database

**How to use it:**
```sql
-- Query data as it existed 2 hours ago
SELECT * FROM orders AT (OFFSET => -60*60*2);

-- Query at a specific timestamp
SELECT * FROM orders AT (TIMESTAMP => '2024-01-15 10:00:00'::TIMESTAMP);

-- Query using a query ID (before a specific statement ran)
SELECT * FROM orders BEFORE (STATEMENT => '8e5d0ca9-005e-44e6-b858-...');
```

**Common use cases:**
- **Accidental DELETE/UPDATE recovery:** Restore a table to its pre-modification state using `CREATE TABLE recovered AS SELECT * FROM orders AT (OFFSET => -3600)`
- **Data auditing:** Compare current state vs state at end of last business day to detect unexpected changes
- **Debugging:** Understand what data a failed pipeline saw when it ran
- **Cloning for testing:** Clone a table AT a known good point for testing without touching production

---

### Q4. How does Snowflake handle semi-structured data like JSON or Parquet natively? What is a VARIANT column?

**Answer:**

Snowflake natively ingests and stores semi-structured data (JSON, Avro, ORC, Parquet, XML) in a `VARIANT` column without requiring a pre-defined schema.

**VARIANT column:** A Snowflake-native data type that stores arbitrary hierarchical data (arrays, objects, primitives) in a self-describing, compressed, columnar format. Internally Snowflake extracts frequent paths and stores them in a virtual column structure for efficient querying.

**Loading semi-structured data:**
```sql
CREATE TABLE raw_events (event VARIANT);

COPY INTO raw_events
FROM @my_stage/events/
FILE_FORMAT = (TYPE = 'JSON');
```

**Querying nested fields:**
```sql
-- Dot notation for objects
SELECT event:user_id::STRING, event:timestamp::TIMESTAMP
FROM raw_events;

-- Array access
SELECT event:items[0]:sku::STRING
FROM raw_events;

-- Flattening arrays
SELECT f.value:sku::STRING AS sku, f.value:qty::INT AS qty
FROM raw_events, LATERAL FLATTEN(input => event:items) f;
```

**Performance tip:** For frequently queried paths, materialise them as typed columns in a downstream Silver table to avoid runtime type casting overhead.

---

### Q5. What is the difference between a transient table, a temporary table, and a permanent table in Snowflake?

**Answer:**

| Feature | Permanent | Transient | Temporary |
|---|---|---|---|
| Persists after session | Yes | Yes | No (session only) |
| Time Travel | Up to 90 days | Up to 1 day | Up to 1 day |
| Fail Safe | 7 days | None | None |
| Storage cost | Higher (TT + FS) | Lower | Lowest |
| Visible to other sessions | Yes | Yes | No |

**When to use each:**

- **Permanent:** Production tables, dimension tables, fact tables — anything that needs full recovery options and long-term retention
- **Transient:** Staging/intermediate tables in ELT pipelines where you do not need Fail Safe and want to reduce storage costs; also good for large intermediate results that are reproducible from source
- **Temporary:** Session-scoped scratch tables within a stored procedure or complex multi-step query session; automatically dropped when the session ends, never visible to other users

---

### Q6. How does Snowflake's Fail Safe feature differ from Time Travel, and what are its limitations for recovery scenarios?

**Answer:**

**Time Travel** is a user-controlled feature. You can query, clone, or restore data at any point within the retention window (up to 90 days on Enterprise). It is fast, self-service, and accessible via SQL.

**Fail Safe** is a Snowflake-managed, non-configurable safety net. After the Time Travel window expires, Snowflake retains data for an additional 7 days in Fail Safe. You cannot access Fail Safe data yourself — only Snowflake Support can perform a recovery, and it is not guaranteed.

**Key limitations of Fail Safe:**
- Not a self-service feature: you must raise a support ticket
- Recovery is not instantaneous — it can take hours to days depending on data size
- Not available on transient or temporary tables
- It is not a substitute for backups — it only covers accidental deletion/modification scenarios, not logical corruption that happened more than 90 days ago
- Fail Safe storage is billed at standard storage rates, so large tables with long Time Travel windows can have significant storage costs

**Recommendation:** Use Time Travel for routine recovery. For compliance and disaster recovery, supplement with periodic `CREATE TABLE ... CLONE` snapshots or `COPY INTO` exports to an external stage.

---

### Q7. What is a Snowflake stage (internal vs external)? When would you use each, and how does the COPY INTO command interact with them?

**Answer:**

A **stage** in Snowflake is a named location that holds data files for loading into or unloading from Snowflake tables.

**Internal stage:** Managed by Snowflake, stored within Snowflake's own infrastructure.
- Three types: User stage (`@~`), Table stage (`@%table_name`), Named internal stage (`@my_stage`)
- No external credentials needed
- Good for ad hoc loads, scripts, and small files uploaded via `PUT` command

**External stage:** Points to a bucket in S3, Azure Blob Storage, or GCS.
- Requires a storage integration (IAM role / service principal) or direct credentials
- Good for production pipelines where data lands in cloud storage first (e.g., Fivetran → S3 → Snowflake, or Kafka → S3 via Kafka Connect → Snowflake)
- Files remain in the external bucket after load; Snowflake only reads them

**COPY INTO interaction:**
```sql
-- Load from external stage
COPY INTO orders
FROM @my_s3_stage/2024/01/15/
FILE_FORMAT = (TYPE = 'PARQUET')
ON_ERROR = 'SKIP_FILE';
```

Snowflake tracks which files have already been loaded in a metadata table (load history) per table. Re-running `COPY INTO` will skip already-loaded files automatically — making it inherently idempotent. You can force a reload with `FORCE = TRUE`.

**Snowpipe** extends this by automating the `COPY INTO` trigger via SQS event notifications or REST API, enabling near real-time micro-batch loading.

---

## 3. Snowflake — Intermediate

---

### Q1. How does Snowflake's automatic clustering work? When would you manually define a cluster key and what columns would you choose?

**Answer:**

Snowflake stores table data in immutable micro-partitions (~16 MB compressed). Each micro-partition stores min/max metadata for every column, enabling **partition pruning** — skipping irrelevant partitions during a query.

**Automatic clustering** (also called Automatic Clustering Service) continuously re-clusters a table's micro-partitions in the background to maintain good clustering on the defined cluster key, without manual intervention.

**When to define a manual cluster key:**
- Table is large (> ~1 TB) and queries consistently filter on specific columns
- The table's natural insert order does not correlate with query filter patterns (e.g., data is loaded unordered by date, but all queries filter on `ORDER_DATE`)
- High-cardinality columns used in WHERE clauses are causing full table scans

**How to choose cluster key columns:**
- Choose columns that appear most frequently in WHERE and JOIN predicates
- Prefer low-to-medium cardinality columns (date, region, status) — high cardinality (UUID, email) creates too many micro-partitions with overlap
- Limit to 1–3 columns; more columns increases maintenance overhead
- For time-series data, a date/timestamp column is almost always the right choice

```sql
ALTER TABLE orders CLUSTER BY (order_date, region);
```

**Cost note:** Automatic clustering consumes credits continuously. Only enable it on tables where query performance gains justify the ongoing compute cost. Use `SYSTEM$CLUSTERING_INFORMATION` to check clustering depth before enabling.

---

### Q2. Explain Snowflake's result cache and query cache. How would you design queries to maximise cache hits without returning stale data?

**Answer:**

**Result Cache (Global):**
- Stores the exact result set of a query in the Cloud Services layer for 24 hours
- If an identical query is re-executed (same SQL text, same user role, same table data unchanged), the result is returned instantly with zero warehouse usage
- Cache is invalidated when the underlying table is modified (any DML, stream consumption, or COPY INTO)

**Local Disk Cache (Warehouse-level):**
- Each virtual warehouse has local SSD storage that caches columnar data files retrieved from S3
- Subsequent queries on the same warehouse hitting the same micro-partitions read from local SSD instead of S3 — significantly faster
- Cache is lost when the warehouse is suspended and restarted

**Designing for cache hits:**

1. **Normalise SQL text:** Even a comment change or whitespace difference creates a cache miss. Use parameterised queries or templated SQL via dbt to ensure identical text
2. **Use a dedicated reporting warehouse:** Keep ETL and reporting on separate warehouses so ETL writes don't evict the disk cache used by dashboards
3. **Avoid `CURRENT_TIMESTAMP` in queries meant to be cached:** Dynamic functions always create a new result. If freshness is acceptable, filter on a date column instead
4. **Set warehouse auto-suspend thoughtfully:** A warehouse suspended too aggressively loses its disk cache on every resume. For dashboards, use a longer auto-suspend (e.g., 10 minutes)

---

### Q3. What are Snowflake Streams and Tasks? Describe a real use case where you would combine them to build a lightweight ELT pipeline.

**Answer:**

**Streams:** A stream is a change data capture (CDC) object that tracks DML changes (INSERT, UPDATE, DELETE) on a source table since the last time the stream was consumed. It exposes three metadata columns: `METADATA$ACTION`, `METADATA$ISUPDATE`, and `METADATA$ROW_ID`.

**Tasks:** A task is a scheduled unit of work — a SQL statement or stored procedure — that Snowflake executes on a defined schedule or as part of a task tree (DAG).

**Real use case: Incremental SCD Type 1 upsert pipeline**

Scenario: A `raw_customers` table receives new and updated records from Fivetran every 15 minutes. You need to keep a clean `dim_customers` table up to date.

```sql
-- 1. Create a stream on the raw table
CREATE STREAM raw_customers_stream ON TABLE raw_customers;

-- 2. Create a task that fires every 15 minutes
CREATE TASK refresh_dim_customers
  WAREHOUSE = transform_wh
  SCHEDULE = '15 MINUTE'
WHEN
  SYSTEM$STREAM_HAS_DATA('raw_customers_stream')
AS
  MERGE INTO dim_customers tgt
  USING (
    SELECT customer_id, name, email, updated_at
    FROM raw_customers_stream
    WHERE METADATA$ACTION = 'INSERT'
  ) src
  ON tgt.customer_id = src.customer_id
  WHEN MATCHED THEN UPDATE SET tgt.name = src.name, tgt.email = src.email
  WHEN NOT MATCHED THEN INSERT (customer_id, name, email) VALUES (src.customer_id, src.name, src.email);

-- 3. Resume the task
ALTER TASK refresh_dim_customers RESUME;
```

The `WHEN SYSTEM$STREAM_HAS_DATA()` condition ensures the task only runs and consumes credits when there is actually new data — making it cost-efficient.

---

### Q4. How would you implement row-level security and dynamic data masking in Snowflake for a multi-tenant SaaS product?

**Answer:**

**Row-Level Security using Row Access Policies:**

A row access policy is a schema-level object that returns a boolean expression. When attached to a table, only rows where the expression evaluates to TRUE are visible to the querying user.

```sql
-- Policy: users can only see rows belonging to their tenant
CREATE ROW ACCESS POLICY tenant_isolation_policy
AS (tenant_id VARCHAR) RETURNS BOOLEAN ->
  tenant_id = CURRENT_ROLE()  -- or use a mapping table
  OR CURRENT_ROLE() IN ('ADMIN', 'SYSADMIN');

ALTER TABLE orders ADD ROW ACCESS POLICY tenant_isolation_policy ON (tenant_id);
```

In practice, use a mapping table that links Snowflake roles or session context (set via `SYSTEM$SET_RETURN_LIMIT`) to allowed tenant IDs for flexibility.

**Dynamic Data Masking:**

Masking policies conditionally reveal or obfuscate column values based on the querying role.

```sql
CREATE MASKING POLICY email_mask
AS (val STRING) RETURNS STRING ->
  CASE
    WHEN CURRENT_ROLE() IN ('ANALYST', 'ADMIN') THEN val
    ELSE REGEXP_REPLACE(val, '.+@', '****@')
  END;

ALTER TABLE customers MODIFY COLUMN email SET MASKING POLICY email_mask;
```

**Best practices for multi-tenant SaaS:**
- Store `tenant_id` in every table; never rely on application-layer filtering alone
- Use a central mapping table for role → tenant_id lookups; avoid hardcoding tenant IDs in policies
- Apply masking to PII columns (email, phone, SSN) globally at the column level
- Test policies using `EXECUTE AS ROLE` in a staging environment before production deployment

---

### Q5. Describe the trade-offs between using Snowflake external tables vs a full COPY INTO load. When does each make sense?

**Answer:**

**External Tables:**
- Query files in S3/GCS/ADLS directly without loading them into Snowflake
- Always reflect the current state of the external location
- No storage duplication — data remains in the lake
- Trade-offs: significantly slower query performance (no micro-partition metadata, no clustering, no result cache), no Time Travel, and no DML support

**COPY INTO (full load):**
- Ingests files into Snowflake-managed storage
- Full performance benefits: micro-partition pruning, clustering, result cache, Time Travel, DML
- Data is duplicated (lake + Snowflake storage cost)

**When to use external tables:**
- Data is already in a data lake and you only need occasional, ad hoc querying (not a hot path)
- You want a single source of truth in the lake and Snowflake is just a query engine (true lakehouse pattern)
- Data volumes are so large that loading everything is cost-prohibitive, but only a fraction is ever queried
- Compliance requires data to stay in your own cloud storage

**When to use COPY INTO:**
- Data is part of your core analytics pipeline and query performance/SLAs matter
- Tables need to be joined, aggregated, or used in downstream transformations frequently
- You need DML operations (MERGE, UPDATE) — not possible on external tables
- You want Time Travel and Fail Safe protection

**Hybrid pattern:** Use external tables for raw/Bronze layer (data stays in lake), then COPY INTO for Silver/Gold layers where query performance is critical.

---

### Q6. You notice a Snowflake query consuming 10× the expected credits. Walk through your performance investigation process step by step.

**Answer:**

1. **Get the Query ID and open Query Profile:**
   - Find the query in History tab or `QUERY_HISTORY` view
   - Open Query Profile to see the execution plan, node-level statistics, and bytes scanned

2. **Check partition pruning:**
   - Look at "Partitions scanned" vs "Partitions total" in the profile
   - If the ratio is close to 1.0, the WHERE clause is not filtering effectively → investigate missing cluster key or implicit type cast preventing pruning

3. **Check for data spill:**
   - Look for "Bytes spilled to local storage" and "Bytes spilled to remote storage" nodes
   - Spill means the warehouse ran out of memory → upsize the warehouse or reduce the working set (add filters, partition the query)

4. **Check for cartesian products or exploding joins:**
   - Inspect the row counts at each join node in the profile
   - If rows are multiplying unexpectedly, there may be duplicate join keys or a missing join condition

5. **Check for full table scans on large tables:**
   - Look for nodes with very high "Bytes scanned"
   - Confirm the WHERE clause uses the cluster key column; check for implicit casts that bypass pruning (e.g., `WHERE date_col = '2024-01-01'` when `date_col` is TIMESTAMP — cast the literal, not the column)

6. **Check warehouse size and queuing:**
   - If the query was queuing behind other queries, the warehouse may be undersized for the concurrency
   - Consider multi-cluster warehouse or a dedicated warehouse

7. **Review query history for repeated full scans:**
   - If the same expensive query runs frequently, a pre-aggregated Gold table or materialised view would eliminate the cost

---

### Q7. How would you use Snowflake's MERGE statement to implement a Type 2 SCD update efficiently at scale? What are the pitfalls with large dimension tables?

**Answer:**

**Type 2 SCD approach in Snowflake:**

A Type 2 SCD keeps full history by expiring the old row (setting `valid_to` and `is_current = FALSE`) and inserting a new row for each change.

```sql
MERGE INTO dim_customers tgt
USING (
  SELECT
    src.customer_id,
    src.name,
    src.email,
    src.tier,
    CURRENT_TIMESTAMP AS valid_from
  FROM raw_customers_stream src
  WHERE src.METADATA$ACTION = 'INSERT'
) src
ON tgt.customer_id = src.customer_id AND tgt.is_current = TRUE
WHEN MATCHED AND (tgt.tier <> src.tier OR tgt.email <> src.email) THEN
  UPDATE SET tgt.valid_to = src.valid_from, tgt.is_current = FALSE
WHEN NOT MATCHED THEN
  INSERT (customer_id, name, email, tier, valid_from, valid_to, is_current)
  VALUES (src.customer_id, src.name, src.email, src.tier, src.valid_from, NULL, TRUE);

-- MERGE only expires old rows; insert new rows in a second statement
INSERT INTO dim_customers (customer_id, name, email, tier, valid_from, valid_to, is_current)
SELECT customer_id, name, email, tier, valid_from, NULL, TRUE
FROM staging_changes
WHERE changed = TRUE;
```

**Pitfalls with large dimension tables:**

- **MERGE does not insert new rows for matched records:** When a row matches (UPDATE path triggers), MERGE does not also INSERT the new version in the same statement. You need a two-step approach: MERGE to expire, then INSERT new rows from a staging table.
- **Lock contention:** MERGE acquires a table-level lock on the target. Long-running MERGEs on large tables block concurrent reads. Use transient staging tables and keep the MERGE window small.
- **Clustering degradation:** Frequent updates to `is_current` scatter writes across micro-partitions. Re-cluster on `(customer_id, is_current)` and run `OPTIMIZE` (via automatic clustering) periodically.
- **Stream offset expiration:** Streams have a staleness limit (14 days). If a task fails and is not retried within that window, the stream offsets expire and historical changes are lost.

---

## 4. Snowflake — Real-time Implementations

---

### Q1. How would you build a near real-time ingestion pipeline into Snowflake using Kafka and Snowpipe? Walk through exactly how Snowpipe auto-ingest works, its latency characteristics, and how you'd handle backpressure.

**Answer:**

**Architecture:**
```
Source System → Kafka → Kafka Connect (S3 Sink) → S3 Bucket → SQS Notification → Snowpipe → Snowflake Table
```

**How Snowpipe auto-ingest works:**

1. Kafka Connect S3 Sink Connector flushes micro-batches of messages to S3 on a defined interval (e.g., every 30 seconds or every 10,000 records)
2. S3 is configured to emit an event notification to an SQS queue when a new file is created
3. Snowpipe polls the SQS queue continuously and triggers a `COPY INTO` for each new file
4. Snowflake loads the file into the target table asynchronously

```sql
CREATE PIPE orders_pipe
  AUTO_INGEST = TRUE
AS
  COPY INTO orders_raw
  FROM @orders_external_stage
  FILE_FORMAT = (TYPE = 'JSON');
```

Get the SQS ARN from `SYSTEM$PIPE_STATUS('orders_pipe')` and configure it in the S3 bucket notification settings.

**Latency characteristics:**
- Kafka → S3: 30 seconds to 2 minutes (governed by S3 Sink flush interval)
- S3 → Snowpipe notification: near-instant via SQS
- Snowpipe internal queueing and load: typically 1–5 minutes
- **Total end-to-end latency: ~2–7 minutes** — Snowpipe is "near real-time", not true real-time

**Handling backpressure:**
- Monitor `SYSTEM$PIPE_STATUS` for `pendingFileCount` and `lastForwardedMessageTimestamp`
- If files accumulate faster than Snowpipe can process, scale the target warehouse or use Snowpipe Streaming (the newer REST API-based approach) which bypasses S3 and streams rows directly with ~1 second latency
- For sustained high volume, partition S3 by hour and use multiple pipes per partition

---

### Q2. You need to power a live operational dashboard refreshing every 30 seconds from Snowflake. How do you architect this — considering Snowpipe, Dynamic Tables, Streams, and warehouse sizing — to minimize cost while meeting the SLA?

**Answer:**

**Key insight:** Refreshing a warehouse query every 30 seconds is extremely expensive and defeats the purpose of Snowflake's architecture. The goal is to push computation to scheduled refresh jobs and serve pre-computed results to the dashboard.

**Recommended architecture:**

**Ingestion:** Snowpipe (or Snowpipe Streaming for sub-minute) loads data into a `raw_events` table.

**Transformation:** A Dynamic Table or Streams + Tasks pipeline pre-aggregates the KPIs:

```sql
CREATE DYNAMIC TABLE dashboard_kpis
  TARGET_LAG = '1 minute'
  WAREHOUSE = transform_xs_wh
AS
  SELECT
    DATE_TRUNC('minute', event_time) AS minute_bucket,
    region,
    COUNT(*) AS event_count,
    SUM(revenue) AS total_revenue
  FROM raw_events
  WHERE event_time >= DATEADD('hour', -24, CURRENT_TIMESTAMP)
  GROUP BY 1, 2;
```

**Serving:** The dashboard queries `dashboard_kpis`, not the raw table. Queries on this small, pre-aggregated table are fast and cheap. With Snowflake's result cache, identical queries within the 1-minute refresh window return instantly with zero compute cost.

**Warehouse sizing:**
- `transform_xs_wh`: XS warehouse for Dynamic Table refresh — runs 1 minute, auto-suspends, billed per second (~$0.001/refresh)
- `serving_xs_wh`: Separate XS warehouse for dashboard queries only, auto-suspend 60 seconds

**Why not query raw every 30 seconds?** A full aggregation over 24 hours of raw events on a busy table would cost 60+ seconds of warehouse time and hundreds of credits per day. Pre-aggregation reduces this by 100–1000×.

---

### Q3. Explain Snowflake Dynamic Tables. How do they differ from standard materialized views and scheduled Tasks+Streams pipelines? When would you choose one over the other for a near real-time use case?

**Answer:**

**Dynamic Tables** are a declarative, Snowflake-managed materialisation primitive. You define the query and a `TARGET_LAG` (how stale the data can be), and Snowflake automatically determines when and how to refresh — incrementally where possible, full refresh otherwise.

```sql
CREATE DYNAMIC TABLE silver_orders
  TARGET_LAG = '5 minutes'
  WAREHOUSE = transform_wh
AS
  SELECT o.order_id, o.customer_id, c.name, o.amount
  FROM raw_orders o JOIN raw_customers c ON o.customer_id = c.customer_id;
```

**Comparison:**

| Feature | Dynamic Tables | Materialised Views | Streams + Tasks |
|---|---|---|---|
| Refresh trigger | Lag-based, automatic | On DML to base table (automatic but limited) | Cron or event-based (manual) |
| Incremental refresh | Yes (where possible) | Limited | Fully custom — you write the logic |
| Multi-table joins | Yes | No (single table/view) | Yes |
| Custom logic | SQL only | SQL only | Full stored procedure / Scripting |
| Operational overhead | Low | Very low | High |
| DAG support | Yes (chain Dynamic Tables) | No | Yes (task trees) |
| Cost transparency | Clear (warehouse + compute time) | Included in storage | Clear |

**When to choose each:**

- **Dynamic Tables:** Best for declarative, SQL-defined pipelines with predictable lag requirements. Ideal for Silver and Gold layer transformations that can be expressed in SQL. Low operational overhead.
- **Materialised Views:** Use for simple, single-table pre-aggregations where you want zero-touch, automatic refresh tied directly to source DML. Very limited in what SQL is supported.
- **Streams + Tasks:** Use when you need procedural logic (loops, branching, error handling), multiple target tables from a single stream, or integration with external systems. More flexible but requires more engineering to maintain.

**For near real-time use cases:** Dynamic Tables with a `TARGET_LAG` of 1–5 minutes is the recommended modern approach in Snowflake as of 2024. It replaces the Streams + Tasks pattern for most transformation use cases with far less operational complexity.

---

## 5. Data Modeling — Basic

---

### Q1. Explain the difference between a star schema and a snowflake schema. Which would you choose for an analytics workload and why?

**Answer:**

**Star schema:** Fact table at the centre surrounded by fully denormalised dimension tables. Dimensions are flat — all attributes of a customer (name, city, country, segment) are in one table.

**Snowflake schema:** Dimensions are normalised — a `dim_customer` table references a separate `dim_city` table, which references `dim_country`. It looks like a snowflake because the dimension branches out.

**Star schema advantages for analytics:**
- Fewer joins = simpler queries and better performance in columnar warehouses
- Easier for business users and BI tools to understand
- Modern columnar engines (Snowflake, BigQuery, Redshift) handle denormalisation well — redundant storage is cheap

**Snowflake schema advantages:**
- Reduces storage redundancy (relevant when storage is expensive — less of a concern in cloud warehouses)
- Easier to maintain referential integrity for shared dimension values

**Recommendation:** For analytics and BI workloads on cloud data warehouses, **star schema is almost always the right choice.** Storage costs are minimal, joins are the bottleneck, and simpler models are easier to maintain and query. Snowflake schema optimises for something (storage) that is not a constraint in modern systems.

---

### Q2. What is a slowly changing dimension (SCD)? Describe Types 1, 2, and 3 with a concrete example.

**Answer:**

An SCD is a dimension whose attribute values change slowly over time (e.g., a customer changes their address or tier).

**Example: `dim_customer` with customer tier (Bronze → Gold)**

**Type 1 — Overwrite:**
Simply update the existing row. No history is preserved.
```sql
UPDATE dim_customer SET tier = 'Gold' WHERE customer_id = 123;
```
Use when: Historical accuracy of the attribute does not matter (e.g., correcting a data entry error).

**Type 2 — Add new row (full history):**
Expire the old row and insert a new one. Preserves complete history.
```
| id  | customer_id | tier   | valid_from | valid_to   | is_current |
|-----|-------------|--------|------------|------------|------------|
| 1   | 123         | Bronze | 2022-01-01 | 2024-03-15 | FALSE      |
| 2   | 123         | Gold   | 2024-03-15 | NULL       | TRUE       |
```
Use when: You need to report "what was the customer's tier when they placed this order?"

**Type 3 — Add new column:**
Add a `previous_tier` column to capture only the immediately prior value.
```
| customer_id | current_tier | previous_tier |
|-------------|--------------|---------------|
| 123         | Gold         | Bronze        |
```
Use when: You only care about one prior state (limited history) and want to avoid row proliferation.

**Most commonly used in practice:** Type 2, because it enables accurate historical point-in-time analysis.

---

### Q3. What is the difference between a fact table and a dimension table? Give an example of each in a retail context.

**Answer:**

**Fact table:** Stores measurable, quantitative business events. Rows represent something that happened. Contains foreign keys to dimensions and numeric measures.

**Dimension table:** Stores descriptive context about the entities in the fact table. Rows represent things (people, places, products). Contains attributes used for filtering, grouping, and labelling.

**Retail example:**

`fact_sales` (fact table):
```
| order_id | customer_key | product_key | store_key | date_key | quantity | revenue | discount |
|----------|-------------|-------------|-----------|----------|----------|---------|----------|
| 10001    | 456         | 789         | 12        | 20240115 | 2        | 59.98   | 5.00     |
```

`dim_product` (dimension table):
```
| product_key | product_name   | category    | brand   | unit_price |
|------------|----------------|-------------|---------|------------|
| 789        | Running Shoes  | Footwear    | Nike    | 29.99      |
```

**Key differences:**
- Fact rows are created when events occur (a sale happens); dimension rows exist independently of events
- Facts are narrow and tall (millions of rows, few columns); dimensions are wide and short (thousands of rows, many columns)
- Fact table measures (revenue, quantity) are additive across dimensions; dimension attributes are not

---

### Q4. What is data normalization? Explain 1NF, 2NF, and 3NF with an example.

**Answer:**

Normalization is the process of organizing a database to reduce redundancy and improve data integrity by applying a set of formal rules (normal forms).

**Example table (unnormalized):**
```
| order_id | customer_name | customer_city | product_id | product_name | qty | price |
|----------|---------------|---------------|------------|--------------|-----|-------|
| 1        | Alice         | Mumbai        | P01        | Shirt        | 2   | 500   |
| 1        | Alice         | Mumbai        | P02        | Jeans        | 1   | 1200  |
```

**1NF (First Normal Form):** Each column must contain atomic (indivisible) values; no repeating groups or arrays. Each row must be unique.
- The table above is in 1NF: each cell has one value, and rows are unique by (order_id, product_id).

**2NF (Second Normal Form):** Must be in 1NF, and every non-key attribute must depend on the entire primary key (no partial dependencies).
- `customer_name` and `customer_city` depend only on `order_id`, not on the full key `(order_id, product_id)`. This is a partial dependency.
- Fix: split into `orders(order_id, customer_name, customer_city)` and `order_items(order_id, product_id, qty, price)`.

**3NF (Third Normal Form):** Must be in 2NF, and no non-key attribute should depend on another non-key attribute (no transitive dependencies).
- `product_name` depends on `product_id`, not on the primary key of `order_items`. Transitive dependency.
- Fix: split into `products(product_id, product_name)` and reference `product_id` in `order_items`.

---

### Q5. When would you use a wide, denormalized table over a normalized relational model in a modern cloud data warehouse?

**Answer:**

In cloud data warehouses (Snowflake, BigQuery, Redshift), the economics and performance characteristics are fundamentally different from OLTP databases:

**Reasons to denormalize in a cloud DWH:**

- **Query simplicity:** Fewer joins means simpler SQL for analysts and BI tools. A wide table with 50 columns is easier to query than a perfectly normalised schema with 10 tables.
- **Columnar storage efficiency:** Redundant string data (e.g., repeating "United States" in a country column) compresses very well in columnar formats — the storage penalty of denormalization is minimal.
- **Join cost at scale:** Joining hundreds of millions of rows across multiple dimension tables is expensive even in cloud warehouses. Pre-joining at write time (during ETL) amortises that cost once.
- **BI tool compatibility:** Many BI tools (Tableau, Looker, Power BI) work better with single, wide tables than complex schemas.

**When to still use normalized models:**
- When the data will be subject to frequent updates (DML-heavy workloads) — update anomalies are painful in wide tables
- When dimensions are shared across many fact tables and you need a single place to update them (SCD Type 2 dimensions)
- When storage cost genuinely matters (rare in modern cloud DWH)

**Best practice:** Use normalised star schema for the Silver/semantic layer (Kimball-style), then create wide, pre-joined Gold tables or views for specific reporting use cases where query simplicity is paramount.

---

### Q6. What is the difference between OLTP and OLAP modeling philosophies? How does this influence your design decisions when building a reporting layer?

**Answer:**

**OLTP (Online Transactional Processing):**
- Optimised for fast reads and writes of individual rows
- Highly normalised (3NF or higher) to minimise write anomalies and enforce data integrity
- Schema designed around business operations: `INSERT order`, `UPDATE inventory`, `DELETE session`
- Workload: many short, concurrent transactions; rows accessed individually

**OLAP (Online Analytical Processing):**
- Optimised for reading and aggregating large volumes of data
- Denormalised or star schema to reduce joins and serve analytical queries efficiently
- Schema designed around business questions: "total revenue by region and product category last quarter"
- Workload: few, long-running queries scanning millions of rows

**Influence on reporting layer design:**

1. **Never build reports directly on OLTP sources.** OLTP tables lack historical tracking, analytical context, and the right granularity for reporting. They are also sensitive to query load.

2. **Denormalise deliberately.** Pre-join dimension attributes into fact tables at ETL time. A `fact_sales` table with `customer_name`, `product_category`, and `store_region` pre-joined is far more usable than making analysts write 5-table joins.

3. **Choose the right grain.** The reporting layer grain should match the lowest level of analysis: transaction-level for drill-down, pre-aggregated daily summaries for high-level dashboards.

4. **Separate historical from current-state reporting.** OLAP models use SCD Type 2 to answer point-in-time questions; OLTP systems only track current state.

---

### Q7. What is a junk dimension and when would you use one? Give a practical example from an e-commerce or finance domain.

**Answer:**

A **junk dimension** is a dimension table that consolidates multiple low-cardinality flag or indicator columns from a fact table into a single dimension, avoiding a proliferation of tiny dimensions or cluttering the fact table with many boolean/status columns.

**The problem it solves:**

In an e-commerce order fact table, you might have several flag columns:
- `is_gift_wrap` (Y/N)
- `is_express_shipping` (Y/N)
- `is_loyalty_member` (Y/N)
- `payment_type` (Card / Cash / Wallet)
- `channel` (Web / Mobile / In-store)

Adding all of these as columns on the fact table creates a wide, cluttered table. Creating a separate dimension for each is impractical (too many tiny tables).

**Solution — junk dimension:**

Create `dim_order_flags` by generating all combinations:

```
| flag_key | is_gift_wrap | is_express | is_loyalty | payment_type | channel  |
|----------|-------------|------------|------------|--------------|----------|
| 1        | N           | N          | N          | Card         | Web      |
| 2        | Y           | N          | N          | Card         | Web      |
| 3        | N           | Y          | Y          | Wallet       | Mobile   |
...
```

The fact table then carries only `flag_key` as a foreign key, keeping it clean.

**When to use it:**
- Multiple flag/boolean/low-cardinality attributes that don't belong to any existing dimension
- The combination count is manageable (ideally < 100,000 combinations)
- The flags are logically related (all about the order transaction, not about the customer or product)

**When not to use it:** If the flags genuinely belong to an existing dimension (e.g., customer loyalty flag belongs in `dim_customer`), add them there instead.

---

## 6. Data Modeling — Intermediate

---

### Q1. How do you model a many-to-many relationship (e.g., products and promotions) in both OLTP and OLAP contexts? What are the trade-offs?

**Answer:**

**OLTP modeling:**
Use a standard bridge/junction table to resolve the many-to-many:
```
products (product_id, name, price)
promotions (promotion_id, name, discount_pct, start_date, end_date)
product_promotions (product_id, promotion_id, applied_date)  ← bridge table
```
This is normalised, supports FK constraints, and handles DML cleanly. Adding or removing a product-promotion association is a single row insert/delete.

**OLAP modeling:**

In a dimensional model, the approach depends on what you need to measure:

- **Option 1 — Bridge table (factless fact table):** Create `fact_product_promotions(product_key, promotion_key, date_key)` with no measures. It records which promotions applied to which products on which dates. Use it to filter fact tables via a semi-join: "show me sales for products that had a promotion in December."
- **Option 2 — Multi-valued dimension with weighting:** If a single fact row (e.g., a sale) can have multiple promotions applied, use a bridge table with a `weight_factor` column to correctly allocate metrics. For example, if 2 promotions apply, each gets a weight of 0.5 to avoid double-counting.
- **Option 3 — Denormalise promotions as an array:** In modern warehouses (BigQuery, Snowflake with VARIANT), store `applied_promotion_ids` as an array in the fact table and use LATERAL FLATTEN to query. Simple but harder to aggregate cleanly.

**Trade-offs:**
- Bridge tables add query complexity (extra join) but maintain analytical correctness
- Weighting is necessary to prevent double-counting but adds model complexity that must be well-documented
- Denormalisation is simpler to write but harder to report on correctly

---

### Q2. Design a data model for a subscription-based SaaS business that needs to track MRR, churn, and upgrades accurately over time.

**Answer:**

**Core tables:**

`dim_account` — SCD Type 2 to track plan changes over time:
```
| account_key | account_id | plan | mrr    | valid_from | valid_to   | is_current |
|-------------|-----------|------|--------|------------|------------|------------|
| 1           | A001      | Pro  | 99.00  | 2023-01-01 | 2024-06-01 | FALSE      |
| 2           | A001      | Biz  | 299.00 | 2024-06-01 | NULL       | TRUE       |
```

`fact_subscription_events` — one row per subscription state change:
```
| event_key | account_key | event_date | event_type   | mrr_change | plan_from | plan_to |
|-----------|------------|------------|--------------|------------|-----------|---------|
| 1         | 1          | 2023-01-01 | NEW          | +99.00     | NULL      | Pro     |
| 2         | 2          | 2024-06-01 | UPGRADE      | +200.00    | Pro       | Biz     |
| 3         | 2          | 2024-11-01 | CHURN        | -299.00    | Biz       | NULL    |
```

`fact_mrr_snapshot` — monthly grain snapshot for easy period-over-period analysis:
```
| snapshot_month | account_id | plan  | mrr    | is_churned |
|----------------|-----------|-------|--------|------------|
| 2024-10        | A001      | Biz   | 299.00 | FALSE      |
| 2024-11        | A001      | NULL  | 0.00   | TRUE       |
```

**MRR calculations:**
- **New MRR:** SUM(mrr_change) WHERE event_type = 'NEW'
- **Expansion MRR:** SUM(mrr_change) WHERE event_type = 'UPGRADE'
- **Churned MRR:** ABS(SUM(mrr_change)) WHERE event_type = 'CHURN'
- **Net New MRR:** New + Expansion - Churned - Contraction
- **Ending MRR:** Beginning MRR + Net New MRR

**Key design decisions:**
- Store `mrr_change` as a signed integer (positive for expansion, negative for churn/contraction) so MRR waterfall calculations are simple aggregations
- The snapshot table makes period-over-period queries (MoM, QoQ) fast and avoids complex window function queries on the event table
- Use SCD Type 2 on `dim_account` so historical fact rows can always join back to the correct plan state

---

### Q3. What is a bridge table and when is it used? How does it affect aggregation logic downstream in BI tools?

**Answer:**

A bridge table (also called an associative table or helper table) resolves a many-to-many relationship between a fact table and a dimension in a star schema context.

**When it's used:**
- A single fact row relates to multiple dimension members (e.g., one order has multiple promotions, one employee belongs to multiple cost centres, one patient has multiple diagnoses)
- Without a bridge, you either denormalise (creating multiple foreign key columns) or lose the ability to filter/slice on the multi-valued dimension

**Structure:**
```
fact_sales ─── fact_sales_promotion_bridge ─── dim_promotion
(order_key)    (order_key, promo_key, weight)   (promo_key, name, discount)
```

**Weight factor:** The bridge table often carries a `weight_factor` column (values summing to 1.0 per fact row) to prevent double-counting when a fact metric is attributed to multiple dimension members.

**Impact on BI tools:**

BI tools like Tableau and Power BI do not natively understand weighted bridges. Without proper handling:
- A sale of $100 with 2 promotions will appear as $200 when filtered on promotion (double-counted)

**Solutions:**
- In Tableau: create a calculated measure that multiplies the metric by `weight_factor` before summing
- In Looker: define the bridge join in the LookML model and apply the weight in the measure definition
- In Power BI: use DAX DIVIDE with the weight factor
- Simplest: pre-apply the weight in the Gold layer and expose a single flat table to the BI tool

**Best practice:** Document the bridge table and the weight factor prominently. A bridge that is misunderstood will silently produce wrong numbers — arguably the most dangerous kind of data quality issue.

---

### Q4. How would you version and test data model changes in a dbt project to avoid breaking downstream reports?

**Answer:**

**Versioning models in dbt:**

dbt supports model versioning natively (dbt Core 1.5+):

```yaml
# models/schema.yml
models:
  - name: dim_customers
    latest_version: 2
    versions:
      - v: 1
        defined_in: dim_customers_v1
      - v: 2
        defined_in: dim_customers_v2
```

Downstream models reference `ref('dim_customers', v=1)` until they are ready to migrate to v2. Both versions run simultaneously during transition.

**Testing strategy:**

1. **Schema tests (dbt native):**
```yaml
columns:
  - name: customer_id
    tests:
      - unique
      - not_null
  - name: tier
    tests:
      - accepted_values:
          values: ['Bronze', 'Silver', 'Gold']
```

2. **Data diff tests:** Compare row counts, sum of key metrics, and null rates between v1 and v2 in CI before promotion:
```sql
-- CI check: new model should have same row count ± 0.1%
SELECT COUNT(*) FROM {{ ref('dim_customers', v=2) }}
-- vs COUNT(*) from v1
```

3. **Contract enforcement:** Define model contracts to guarantee the column signatures:
```yaml
config:
  contract:
    enforced: true
columns:
  - name: customer_id
    data_type: varchar
```
dbt will fail the build if the actual output doesn't match the declared contract.

**Deployment process:**
- Run full test suite in CI (PR merge gate)
- Deploy to a staging environment first, run against production data volume
- Use Blue/Green by deploying to a new schema, swapping the alias only after tests pass
- Notify downstream owners when a breaking change is incoming with a defined deprecation timeline

---

### Q5. Explain the concept of grain in fact table design. What happens if multiple grains end up in the same fact table?

**Answer:**

**Grain** is the precise definition of what a single row in a fact table represents. It answers: "what does one row mean?"

Examples of well-defined grains:
- `fact_sales`: one row per line item per order (order_id + product_id)
- `fact_daily_inventory`: one row per product per store per day
- `fact_website_sessions`: one row per user session

**Declaring grain is the most important step in fact table design.** Every dimension and every measure must be consistent with that grain.

**What happens when multiple grains are mixed:**

Suppose someone adds a `monthly_customer_target` column to a transaction-level `fact_sales` table:
- The transaction grain is one row per sale
- The monthly target applies to the entire month for a customer

Result:
- The same monthly target value appears on every transaction for that customer in that month
- When an analyst sums `monthly_target` across transactions, they get the target multiplied by the transaction count — massively overcounted
- This is called a **fan trap** or **chasm trap** and produces silently wrong aggregations

**How to fix it:**
- Keep each grain in its own fact table: `fact_sales` (transaction grain) and `fact_customer_targets` (monthly customer grain)
- Join them at query time using the lowest common grain (customer + month)
- Or pre-aggregate `fact_sales` to monthly customer grain before joining targets

**Rule:** Never mix grains in a fact table. If you feel the urge to add a column at a different grain, that column belongs in a separate fact table.

---

### Q6. How would you model a financial ledger system in a data warehouse where every transaction must be auditable, reversible, and traceable to source records?

**Answer:**

Financial ledgers are append-only by nature — you never update or delete entries. Every correction is itself a new entry.

**Core principle: immutable ledger pattern**

```
fact_ledger_entries
| entry_id | account_id | entry_date | entry_type     | amount    | currency | source_system | source_id | reversal_of_entry_id | batch_id | loaded_at |
|----------|-----------|------------|----------------|-----------|----------|--------------|-----------|----------------------|----------|-----------|
| 1001     | ACC-42    | 2024-01-10 | DEBIT          | 5000.00   | INR      | SAP          | INV-8801  | NULL                 | B-001    | 2024-01-10|
| 1002     | ACC-42    | 2024-01-15 | CREDIT         | 5000.00   | INR      | SAP          | PMT-4421  | NULL                 | B-002    | 2024-01-15|
| 1003     | ACC-42    | 2024-01-20 | REVERSAL_DEBIT | -5000.00  | INR      | SAP          | REV-0012  | 1001                 | B-003    | 2024-01-20|
```

**Key design decisions:**

- **Never UPDATE or DELETE rows.** Corrections are new entries with a reference to `reversal_of_entry_id`, keeping a complete audit trail.
- **`source_system` + `source_id`** form a natural key linking every warehouse entry back to the originating system record.
- **`batch_id`** ties entries to a specific load batch, enabling rollback of an entire bad load by filtering on `batch_id`.
- **`loaded_at`** timestamps when the record entered the warehouse — separate from `entry_date` (business date) — crucial for reconciliation.
- **Running balance:** Do not store running balance in the table (it would need updates). Compute it at query time with a window function: `SUM(amount) OVER (PARTITION BY account_id ORDER BY entry_date, entry_id)`.

**Auditability layer:**
- Add a `dim_audit_log` table tracking every pipeline run that touched the ledger (pipeline_id, run_ts, rows_inserted, source_file)
- Implement a reconciliation view that compares source system totals vs warehouse totals per account per period

---

### Q7. A business analyst says their numbers don't match between two dashboards built on different fact tables. Walk through how you'd debug this as a data modeling issue.

**Answer:**

This is one of the most common and trust-destroying data issues. Approach it systematically.

**Step 1 — Understand the discrepancy precisely:**
- What metric? What time period? What filters? What is the exact difference (10 rows? 10%? $10?)?
- Are both dashboards supposed to show the same thing, or are they measuring subtly different things?

**Step 2 — Check grain:**
- What is the grain of each fact table? If Dashboard A uses `fact_orders` (order grain) and Dashboard B uses `fact_order_items` (line item grain), summing revenue on both will give different results unless properly aggregated.

**Step 3 — Check join fanout:**
- Are either of the fact tables joining to a dimension that causes row multiplication? Run `SELECT COUNT(*) before and after the join` to detect fanout.
- Common culprit: joining a transaction table to a date dimension on a non-unique key.

**Step 4 — Check filter differences:**
- Do both dashboards apply the same date filter? Is one using `order_date` and the other `ship_date`?
- Are there hidden dashboard filters that differ between the two?

**Step 5 — Check NULL handling:**
- Are NULLs in a join key causing rows to drop silently? Use `COUNT(*)` vs `COUNT(key_column)` to detect.
- Is one dashboard excluding cancelled orders and the other isn't?

**Step 6 — Trace a specific record:**
- Pick one order ID that appears in one dashboard but not the other. Trace it through each pipeline step from source to final table.

**Preventive measures:**
- Single source of truth: a certified metrics layer (dbt metrics, Looker LookML) so all dashboards derive from the same defined measures
- Data contracts between model owners
- Automated reconciliation tests that compare key metrics across related fact tables in CI

---

### Q8. How would you design a data model that supports both historical point-in-time analysis and current-state reporting without duplicating large volumes of data?

**Answer:**

This is the tension between SCD Type 2 (full history, expensive storage) and a simple current-state model (fast, cheap, no history).

**Recommended pattern: SCD Type 2 + current-state view**

Store full history in the dimension using SCD Type 2, but create a lightweight current-state view on top — no data duplication:

```sql
-- Full history table (SCD Type 2)
CREATE TABLE dim_customer (
  customer_key    INT,       -- surrogate key
  customer_id     VARCHAR,   -- natural key
  name            VARCHAR,
  tier            VARCHAR,
  valid_from      DATE,
  valid_to        DATE,
  is_current      BOOLEAN
);

-- Current-state view (no storage cost)
CREATE VIEW dim_customer_current AS
SELECT * FROM dim_customer WHERE is_current = TRUE;
```

**Point-in-time joins for fact tables:**

When fact rows are loaded, they store the surrogate `customer_key` that was current at the time of the event — not the natural key. This "snapshot" join preserves historical accuracy automatically:

```sql
-- Fact table load: join to the dimension version valid at event time
SELECT f.*, c.customer_key
FROM staging_orders f
JOIN dim_customer c
  ON f.customer_id = c.customer_id
 AND f.order_date >= c.valid_from
 AND (f.order_date < c.valid_to OR c.valid_to IS NULL);
```

**For large dimensions where SCD Type 2 is storage-prohibitive:**

- Use **Type 1 + Type 2 hybrid:** Track only the specific attributes that require history as Type 2 columns; update all other attributes in place (Type 1). This limits row proliferation.
- Use **Temporal tables / bi-temporal modeling** for regulatory use cases: store both `valid_time` (business reality) and `transaction_time` (when the warehouse knew about it) — enables full auditability even for late-arriving corrections.

---

*End of Interview Question Bank — 43 Questions*

---
> **Document generated for:** Senior Data Engineer L1 Interview
> **Sections:** Data Engineering (Hard) · Snowflake (Basic + Intermediate + Real-time) · Data Modeling (Basic + Intermediate)
