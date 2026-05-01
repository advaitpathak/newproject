import boto3

# Create an S3 client
s3 = boto3.client('s3')

# Define parameters
file_name = 'C:\\Users\\coditas\\Downloads\\etl-2.0-SNAPSHOT-jar-with-dependencies-testing-hadoop-336.jar'  # Local file path
bucket_name = 'trepp-developmentservices-lake-workspace'       # S3 bucket name
folder_name = 'binaries/ap-jars/'           # S3 folder path (make sure to end with '/')

# Upload file to S3 folder
s3.upload_file(file_name, bucket_name, folder_name + file_name)

print(f"File '{file_name}' uploaded to '{bucket_name}/{folder_name}'.")
