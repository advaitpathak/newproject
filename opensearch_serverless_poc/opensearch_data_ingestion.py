import requests
from requests_aws4auth import AWS4Auth
import boto3
import json

# AWS credentials and region
region = 'us-east-1'  # e.g., 'us-west-2'
service = 'aoss'  # 'aoss' is the service identifier for AWS OpenSearch Serverless
credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)

# OpenSearch Serverless domain endpoint (ensure https:// is included)
host = 'https://2hweg6owj98dsp41h4hl.us-east-1.aoss.amazonaws.com'
index_name = "test-index-python-new"


def create_index():
    # Define the index settings and mappings (optional, but recommended)
    index_body = {
        "settings": {
            "number_of_shards": 1,
            "number_of_replicas": 1
        },
        "mappings": {
            "properties": {
                "name": {"type": "text"},
                "age": {"type": "integer"},
                "occupation": {"type": "text"}
            }
        }
    }

    # Create the index if it doesn't exist
    index_url = f"{host}/{index_name}"
    response = requests.head(index_url, auth=awsauth, headers={"Content-Type": "application/json"})

    if response.status_code == 404:
        # Index does not exist, create it
        response = requests.put(index_url, auth=awsauth, headers={"Content-Type": "application/json"}, data=json.dumps(index_body))
        if response.status_code in (200, 201):
            print("Index created successfully:", response.json())
        else:
            print("Failed to create index:", response.status_code, response.text)
    else:
        print(f"Index '{index_name}' already exists.")

def insert_document():
    # Sample document to be indexed
    document = {
        "name": "John Doe",
        "age": 30,
        "occupation": "Software Engineer"
    }

    # Insert the document into OpenSearch
    doc_url = f"{host}/{index_name}/_doc/1"  # Document ID is 1 in this case
    response = requests.put(doc_url, auth=awsauth, headers={"Content-Type": "application/json"}, data=json.dumps(document))

    if response.status_code == 201:
        print(f"Document indexed successfully: {response.json()}")
    else:
        print(f"Failed to index document: {response.status_code}, {response.text}")


def get_all_documents():
    # Search for all documents in the index
    search_url = f"{host}/{index_name}/_search"
    query = {
        "query": {
            "match_all": {}
        }
    }

    response = requests.get(search_url, auth=awsauth, headers={"Content-Type": "application/json"}, data=json.dumps(query))

    if response.status_code == 200:
        print("Search results:", json.dumps(response.json(), indent=2))
    else:
        print(f"Failed to search documents: {response.status_code}, {response.text}")


if  __name__ == "__main__":
    create_index()
    insert_document()
    get_all_documents()
