import time

import boto3
import datetime
import requests
from requests_aws4auth import AWS4Auth


def register_manual_snapshot(target_host, repository_name):
    region = "us-east-1"
    service = "es"
    credentials = boto3.Session().get_credentials()
    awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)

    # Register repository

    path = f"/_snapshot/{repository_name}"  # the OpenSearch API endpoint
    url = target_host + path

    current_date = datetime.datetime.now(tz=datetime.timezone.utc).strftime("%Y%m%d")
    bucket = "staging-opensearch-restore-snapshots"
    base_path = f"snapshots/trepp-staging-os-snapshot-{current_date}"  # 20240815
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

    r = requests.put(url, auth=awsauth, json=payload, headers=headers)

    print(r.status_code)
    print(r.text)


if __name__ == '__main__':
    # TODO : Make sure ZScaler is ON

    TARGET_DOMAIN = "https://vpc-staging-os-rollback-testing-4lle5jekrsta6pfj5cxcbx7cf4.us-east-1.es.amazonaws.com"
    REPOSITORY_NAME = "staging-os-es-domain-snapshots"

    start_time = time.time()
    register_manual_snapshot(TARGET_DOMAIN, REPOSITORY_NAME)
    end_time = time.time()
    print(f"Register manual snapshot time: {end_time - start_time}")
