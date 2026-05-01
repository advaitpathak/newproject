import json
import requests


def get_snapshot_repo_name(opensearch_domain_name):
    url = f"https://{opensearch_domain_name}/_snapshot?pretty"

    response = requests.get(url)
    response_json = json.loads(response.text)

    return [key for key in response_json]


def get_all_snapshots(opensearch_domain_name, snapshot_repo):
    url = f"https://{opensearch_domain_name}/_snapshot/{snapshot_repo}/_all?pretty"
    response = requests.get(url)
    response_json = json.loads(response.text)

    return response_json


def restore_snapshot(opensearch_domain_name, snapshot_repo, snapshot_name):
    url = f"https://{opensearch_domain_name}/_snapshot/{snapshot_repo}/{snapshot_name}/_restore"
    # url = "https://vpc-poc-staging-os-restore-vr5ddy63hzk5xffhu43avncare.us-east-1.es.amazonaws.com/_snapshot/cs-automated-enc/2024-06-25t09-21-38.8be62cb3-466d-3176-aeca-17a917576085/_restore"
    response = requests.post(url)
    response_json = json.loads(response.text)

    return response_json


if __name__ == '__main__':
    source_opensearch_domain = "vpc-trepp-staging-os-es-domain-smk3nd5lrapu3g7lrcslakqqv4.us-east-1.es.amazonaws.com"
    source_snapshot_repository = get_snapshot_repo_name(source_opensearch_domain)

    snapshots = get_all_snapshots(source_opensearch_domain, source_snapshot_repository[1])
    latest_snapshot = snapshots['snapshots'][0]
    latest_snapshot_name = latest_snapshot['snapshot']

    # staging_new_opensearch = "vpc-poc-staging-os-restore-vr5ddy63hzk5xffhu43avncare.us-east-1.es.amazonaws.com"
    # restore_response = restore_snapshot(staging_new_opensearch, source_snapshot_repository[1], latest_snapshot_name)
