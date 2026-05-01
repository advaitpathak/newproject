from pyspark.sql import SparkSession
from pyspark.sql.functions import lit, when

# Initialize Spark session
spark = SparkSession.builder.appName("ParquetUpdate").getOrCreate()

# Read the existing Parquet file
df = spark.read.parquet("C:\\Users\\coditas\\Downloads\\part-00142-88cf438f-51de-4e3d-af2d-ccaefe04917d.c000.snappy.parquet")

# Add a new column 'op' and update some rows as 'D' (Delete) and some as 'I' (Insert)
df = df.withColumn(
    "op",
    when(df["situscity"] == "JAMESTOWN", lit("D")).otherwise(lit("I"))
)

# Save back to Parquet without modifying the existing schema
df.write.mode("overwrite").parquet("output.parquet")

# Stop Spark session
spark.stop()
