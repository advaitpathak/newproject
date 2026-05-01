from pyspark.sql import SparkSession

# -------------------------
# Spark session
# -------------------------
spark = (
    SparkSession.builder
    .appName("CSV to Hudi")
    .config(
        "spark.jars.packages",
        "org.apache.hudi:hudi-spark3.2-bundle_2.12:0.12.3"
    )
    .config("spark.serializer", "org.apache.spark.serializer.KryoSerializer")
    .config("spark.sql.warehouse.dir", "file:///tmp/spark-warehouse")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")

# -------------------------
# Paths (ABSOLUTE + file://)
# -------------------------
csv_path = (
    "file:///Volumes/workspace/backup/D/workspace/newproject/csv_to_hudi/includepreviousbatch.csv"
)

hudi_base_path = (
    "file:///Volumes/workspace/backup/D/workspace/trepp/"
    "datalake-pipeline-commons/src/test/resources/"
    "pipeline/commons/dynamodb/input/test_table"
)

print("CSV path       :", csv_path)
print("Hudi base path :", hudi_base_path)

# -------------------------
# Read CSV
# -------------------------
df = (
    spark.read
    .option("header", "true")
    .option("inferSchema", "true")
    .csv(csv_path)
)

# -------------------------
# Hudi write options
# -------------------------
hudi_options = {
    "hoodie.table.name": "test_table",
    "hoodie.datasource.write.recordkey.field": "propertyeconomicunithistoryid",
    "hoodie.datasource.write.precombine.field": "updatedt",
    "hoodie.datasource.write.table.type": "COPY_ON_WRITE",

    # Non-partitioned table
    "hoodie.datasource.write.partitionpath.field": "",
    "hoodie.datasource.write.keygenerator.class":
        "org.apache.hudi.keygen.NonpartitionedKeyGenerator",

    # Write behavior
    "hoodie.datasource.write.operation": "insert",

    # Performance
    "hoodie.upsert.shuffle.parallelism": "2",
    "hoodie.insert.shuffle.parallelism": "2",
}

# -------------------------
# Write to Hudi
# -------------------------
(
    df.write
    .format("hudi")
    .options(**hudi_options)
    .mode("overwrite")   # use "append" for incremental loads
    .save(hudi_base_path)
)

spark.stop()
