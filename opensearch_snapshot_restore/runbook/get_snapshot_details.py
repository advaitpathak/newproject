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


if __name__ == '__main__':
    SOURCE_DOMAIN = "vpc-trepp-prod-os-es-domain-jsxto635wxdugtnbopq2ucuxaq.us-east-1.es.amazonaws.com"
    all_snapshot_repositories = get_snapshot_repo_name(SOURCE_DOMAIN)
    print(f"All repositories: {all_snapshot_repositories}")

    source_snapshot_repository = all_snapshot_repositories[1]
    print(f"Setting source snapshot repository to: {source_snapshot_repository}")

    snapshots = get_all_snapshots(SOURCE_DOMAIN, source_snapshot_repository)
    print(f"All snapshots: {snapshots}")
    for snapshot in snapshots['snapshots']:
        print(f"""
        snapshot_name: {snapshot['snapshot']}
        total_indices: {len(snapshot['indices'])}
        state: {snapshot['state']}
        start_time: {snapshot['start_time']}
        end_time: {snapshot['end_time']}
        failure: {snapshot['failures']}""")
    # latest_snapshot = snapshots['snapshots'][0]
    # latest_snapshot_name = latest_snapshot['snapshot']
