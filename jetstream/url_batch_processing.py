import requests


chunk_size = 1024
url = 'https://depot.jetstream.pro/3ewp-rjcm-q57d/download/b0b62265-3400-57e5-aa1b-81743d8340a8'

session = requests.Session()

response = session.request(
    method='GET',
    url=url,
    json=None,
    headers=None,
    verify=True,
    stream=True
)

if response.status_code == 200:
    # Open a local file for writing
    with open('local_file.zip', 'wb') as local_file:
        # Iterate over the response content in chunks and write them to the local file
        for chunk in response.iter_content(chunk_size=chunk_size):
            local_file.write(chunk)
else:
    print(f"Failed to download file. Status code: {response.status_code}")
