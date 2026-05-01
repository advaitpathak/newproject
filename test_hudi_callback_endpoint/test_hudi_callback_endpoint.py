import requests

url = "https://sz92tbkmwg.execute-api.us-east-1.amazonaws.com/ap-development"

# JSON data to be sent in the POST request (as a dictionary)
json_data = {
    "key1": "value1",
    "key2": "value2"
}

headers = {
    "Content-Type": "application/x-amz-json-1.1",  # Specify the content type as JSON
    "X-Amz-Target": "CodeBuild_20161006.StartBuild"  # Add any additional headers as needed
}

# Making the POST request with JSON data
response = requests.post(url, json=json_data, headers=headers)

# Checking the response
if response.status_code == 200:
    print("POST request successful!")
    print("Response:", response.text)
else:
    print(f"POST request failed with status code {response.status_code}")
    print("Response:", response.text)
