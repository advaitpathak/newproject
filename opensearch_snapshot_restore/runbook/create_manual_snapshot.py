import boto3
import datetime
import requests
import time
from requests_aws4auth import AWS4Auth


def register_s3_repo_to_opensearch_domain(source_host, repository_name):
    print("\nStarting register_s3_repo_to_opensearch_domain")

    region = "us-east-1"
    service = "es"
    credentials = boto3.Session().get_credentials()
    awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)

    # Register repository

    path = f"/_snapshot/{repository_name}"  # the OpenSearch API endpoint
    url = source_host + path

    current_date = datetime.datetime.now(tz=datetime.timezone.utc).strftime("%Y%m%d")
    bucket = "staging-opensearch-restore-snapshots"
    base_path = f"snapshots/trepp-staging-os-snapshot-{current_date}"
    role_arn = "arn:aws:iam::444087450515:role/opensearch-restore-role"

    payload = {
        "type": "s3",
        "settings": {
            "bucket": bucket,
            "base_path": base_path,
            "region": region,
            "role_arn": role_arn
        }
    }
    headers = {"Content-Type": "application/json"}

    print(f"Payload : {payload}")
    r = requests.put(url, auth=awsauth, json=payload, headers=headers)

    print(r.status_code)
    print(r.text)


def create_manual_snapshot(source_host, repository_name):
    current_time = datetime.datetime.now(tz=datetime.timezone.utc).strftime("%Y-%m-%d-%H-%M")

    url = f"{source_host}/_snapshot/{repository_name}/manual-snapshot-{current_time}"
    print(f"\nStarting manual creation of snapshot \nHost: {source_host} \nRepo Name: {repository_name} \nURL: {url}")

    response = requests.put(url)
    print(response.text)
    print(response.status_code)


if __name__ == '__main__':
    # TODO : Make sure ZScaler is ON

    SOURCE_DOMAIN = "https://vpc-trepp-staging-os-es-domain-smk3nd5lrapu3g7lrcslakqqv4.us-east-1.es.amazonaws.com"
    REPOSITORY_NAME = "staging-os-es-domain-snapshots"

    start_time = time.time()

    register_s3_repo_to_opensearch_domain(SOURCE_DOMAIN, REPOSITORY_NAME)
    register_repo_end_time = time.time()
    print(f"Register repo time: {register_repo_end_time - start_time}")

    create_manual_snapshot(SOURCE_DOMAIN, REPOSITORY_NAME)
    end_time = time.time()
    print(f"Manual snapshot creation time: {end_time - register_repo_end_time}")

    print(f"Total time: {end_time - start_time}")
