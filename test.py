import json
import requests
import pandas as pd


def upload_file_to_s3(file_url):
    s3_bucket =
    response = requests.get(url)
    if response.status_code == 200:
        with open(save_path, 'wb') as file:
            file.write(response.content)
        print("File downloaded successfully.")
    else:
        print("File download failed.")

uri = 'https://depot.jetstream.pro/3ewp-rjcm-q57d/manifest.json'

response = requests.get(uri)
response_content = json.loads(response.content)
inventory = response_content['result']['inventory']
inventory_df = pd.DataFrame(inventory)
latest_file = inventory_df.sort_values('timestamp', ascending=False).head(1)

file_url = inventory_df['url'][0]
file_name = latest_file['filename'][0]

upload_file_to_s3(file_url)
