import boto3

# Initialize the Glue client
glue_client = boto3.client('glue')

# Specify your S3 location and database/table names
s3_location = 's3://trepp-developmentservices-lake-rawdata/ap-test-hudi-table/'
database_name = 'curation_dev'
table_name = 'ap_test_event_table'

# Define the new non-partition columns
new_columns = [
    {'Name': 'email', 'Type': 'string'},
    {'Name': 'phone_number', 'Type': 'string'}
]

# Define the new partition key
partition_key = {'Name': 'country', 'Type': 'string'}

# Retrieve the current table definition
response = glue_client.get_table(
    DatabaseName=database_name,
    Name=table_name
)

# Get the current columns and partition keys
current_columns = response['Table']['StorageDescriptor']['Columns']
current_partitions = response['Table'].get('PartitionKeys', [])

# Add the new columns to the current columns
updated_columns = current_columns + new_columns

# Add the partition key if not already present
updated_partitions = current_partitions + [partition_key]

# Update the table definition
response = glue_client.update_table(
    DatabaseName=database_name,
    TableInput={
        'Name': table_name,
        'StorageDescriptor': {
            'Columns': updated_columns,
            'Location': s3_location,
            'InputFormat': 'org.apache.hadoop.hive.ql.io.parquet.MapredParquetInputFormat',
            'OutputFormat': 'org.apache.hadoop.hive.ql.io.parquet.MapredParquetOutputFormat',
            'SerdeInfo': {
                'Name': 'parquet',
                'SerializationLibrary': 'org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe'
            }
        },
        'PartitionKeys': updated_partitions,
        'TableType': 'EXTERNAL_TABLE',
    }
)

print("Table updated with new columns and partition key:", response)
