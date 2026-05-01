import boto3

# Initialize the Glue client
glue_client = boto3.client('glue')

# Specify your S3 location and database name
s3_location = 's3://trepp-developmentservices-lake-rawdata/ap-test-hudi-table/'
database_name = 'curation_dev'
table_name = 'ap_test_event_table'

# Define the schema for the initial table (5 columns)
columns = [
    {'Name': 'id', 'Type': 'int'},
    {'Name': 'name', 'Type': 'string'},
    {'Name': 'age', 'Type': 'int'},
    {'Name': 'city', 'Type': 'string'},
    {'Name': 'timestamp', 'Type': 'timestamp'}
]

# Define the storage descriptor (Parquet format)
storage_descriptor = {
    'Columns': columns,
    'Location': s3_location,
    'InputFormat': 'org.apache.hadoop.hive.ql.io.parquet.MapredParquetInputFormat',
    'OutputFormat': 'org.apache.hadoop.hive.ql.io.parquet.MapredParquetOutputFormat',
    'SerdeInfo': {
        'Name': 'parquet',
        'SerializationLibrary': 'org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe'
    }
}

# Create the initial table in Glue
response = glue_client.create_table(
    DatabaseName=database_name,
    TableInput={
        'Name': table_name,
        'StorageDescriptor': storage_descriptor,
        'TableType': 'EXTERNAL_TABLE',
    }
)

print("Initial table created:", response)
