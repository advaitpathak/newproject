import requests

region = "us-east-1"
service = "es"

OPENSEARCH_HOST = 'https://vpc-trepp-staging-os-es-domain-smk3nd5lrapu3g7lrcslakqqv4.us-east-1.es.amazonaws.com'

url = f'{OPENSEARCH_HOST}/_cat/indices?format=json&h=index,store.size'

headers = {"Content-Type": "application/json"}

response = requests.get(url, headers=headers)

print(response.status_code)
print(response.text)

if response.status_code == 200:
    indices = response.json()

    total_size = 0
    for index in indices:
        size_str = index['store.size']

        # Convert size to bytes (handles KB, MB, GB, etc.)
        if 'kb' in size_str.lower():
            size_in_bytes = float(size_str.replace('kb', '').strip()) * 1024
        elif 'mb' in size_str.lower():
            size_in_bytes = float(size_str.replace('mb', '').strip()) * 1024 * 1024
        elif 'gb' in size_str.lower():
            size_in_bytes = float(size_str.replace('gb', '').strip()) * 1024 * 1024 * 1024
        elif 'b' in size_str.lower():
            size_in_bytes = float(size_str.replace('b', '').strip())
        else:
            size_in_bytes = 0  # Handle unrecognized sizes

        total_size += size_in_bytes

    # Convert total size back to a readable format (in GB)
    total_size_gb = total_size / (1024 * 1024 * 1024)

    print(f"Total size of all indices: {total_size_gb:.2f} GB")
else:
    print(f"Failed to retrieve indices: {response.status_code} - {response.text}")
