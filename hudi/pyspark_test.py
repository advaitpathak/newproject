import os
import sys


def configure_spark(spark_home=None, pyspark_python=None):
    # spark_home = spark_home or "/path/to/default/spark/home"
    os.environ['SPARK_HOME'] = spark_home
    os.environ['JAVA_HOME'] = 'C:\\Program Files\\Java\\jdk-1.8'
    # 'C:\\Program Files\\Java\\jre-1.8'

    # Add the PySpark directories to the Python path:
    sys.path.insert(1, os.path.join(spark_home, 'python'))
    sys.path.insert(1, os.path.join(spark_home, 'python', 'pyspark'))
    sys.path.insert(1, os.path.join(spark_home, 'python', 'build'))

    # If PySpark isn't specified, use currently running Python binary:
    pyspark_python = pyspark_python or sys.executable
    os.environ['PYSPARK_PYTHON'] = pyspark_python


configure_spark('D:\\spark\\spark-3.1.2-bin-hadoop3.2')

print()

import findspark
from pyspark.conf import SparkConf
from pyspark.context import SparkContext

# Find Spark Locally
location = findspark.find()
findspark.init(location, edit_rc=True)


# --------------------------------------------------

from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, IntegerType

# Create a Spark session
spark = SparkSession.builder.appName("example").getOrCreate()

# Define data and schema
data = [1]
columns = ["emp_id"]

# Specify the schema explicitly
schema = StructType([StructField(column, IntegerType(), True) for column in columns])

# Create a DataFrame
spark_df = spark.createDataFrame(data=[data], schema=schema)

# Show the DataFrame
spark_df.show()
