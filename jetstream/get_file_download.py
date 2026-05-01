import json
import requests

url = 'https://depot.jetstream.pro/3ewp-rjcm-q57d/download/ec6b2ea2-ff55-5d05-93f1-fd0f0113f095'
response = requests.get(url)

# Check if the request was successful (status code 200 indicates success)
if response.status_code == 200:
    # Get the filename from the URL or provide a desired filename
    filename = 'downloaded_file.zip'  # Replace with the desired filename

    # Save the response content to a file
    # with open(filename, 'wb') as file:
        # file.write(response.content)

    from datetime import datetime
    bucket = 'trepp-developmentservices-lake-rawdata'
    dataset_name = 'jetstream_depot'
    data_provider = 'jetstream'
    load_type = 'full_load'
    current_date = datetime.utcnow().strftime('%Y-%m-%d')
    key = f'{data_provider}/{dataset_name}/{load_type}/date={current_date}/testing-jetstream.zip'
    import boto3
    s3 = boto3.client('s3')
    response = s3.put_object(
        Bucket=bucket,
        Body=response.content,
        Key=key
    )
    print()
    # s3.upload_fileobj(response.content, 'trepp-developmentservices-lake-rawdata', 'testing-jetstream')

    print(f"File '{filename}' downloaded successfully.")
else:
    print(f"Request to '{url}' failed with status code {response.status_code}.")
