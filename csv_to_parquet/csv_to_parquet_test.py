from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import ArrayType, StringType

# Initialize SparkSession
spark = SparkSession.builder \
    .master("local") \
    .appName("SparkParquetExample") \
    .getOrCreate()

# Read CSV
df = spark.read.parquet(
    "D:\\workspace\\newproject\\csv_to_parquet\\input_trepprealidlineage.parquet",
    header=True,
    inferSchema=True
)

# Convert 'lineagelist' column to an array
df = df.withColumn(
    "lineagelist",
    F.when(F.col("lineagelist").isNotNull(), F.split(F.col("lineagelist"), ", *"))
    .otherwise(F.array())  # Default to an empty array for null values
)

df = df.withColumn("lineagelist", df["lineagelist"].cast(ArrayType(StringType())))

# Show results
df.show(truncate=False)
df.printSchema()

# Write as Parquet with single output file
df.coalesce(1).write.parquet("test_output.parquet", mode="overwrite")

# Stop Spark session
spark.stop()
