import json
import requests


def get_source_snapshot_details(url):
    response = requests.get(url)
    response_json = json.loads(response.text)
    return response_json


def restore_manual_snapshot_to_target(url, indices_to_restore):
    headers = {
        "Content-Type": "application/json"
    }
    restore_payload = {
        "indices": indices_to_restore,
        "ignore_unavailable": True,  # Default = false
        # If true, the restore operation will ignore indices that are specified in the
        # indices parameter but do not exist in the snapshot. This means that the operation will proceed
        # with restoring the available indices without failing or throwing an error due to missing indices.
        "include_global_state": False  # Default = true
        # If true, the global state of the cluster, including index templates, cluster settings, and other metadata,
        # is restored from the snapshot. If false, the global cluster state is not restored.
        # Only the specified indices are restored. This can be useful if you want to restore specific indices
        # without affecting the current global state of the cluster

    }
    response = requests.post(
        url,
        headers=headers,
        json=restore_payload
    )
    response_json = json.loads(response.text)

    return response_json


if __name__ == '__main__':
    SOURCE_DOMAIN_NAME = "<your-source-domain-name>"
    SOURCE_SNAPSHOT_REPO_NAME = "<your-source-repo-name>"
    SOURCE_MANUAL_SNAPSHOT_NAME = "<your-manual-snapshot-name>"
    TARGET_DOMAIN_NAME = "<your-target-domain-name>"

    source_snapshot_url = f"https://{SOURCE_DOMAIN_NAME}/_snapshot/{SOURCE_SNAPSHOT_REPO_NAME}/_all?pretty"
    print(f"Source - Snapshot URL : {source_snapshot_url}")

    source_snapshot = get_source_snapshot_details(source_snapshot_url)
    print(f"Source - Snapshot Response : {json.dumps(source_snapshot)}")

    source_indices_list = source_snapshot['snapshots'][0]['indices']
    print(f"Source - Indices List : {source_indices_list}")

    ignore_index = [".kibana_1"]
    for ind in ignore_index:
        if ind in source_indices_list:
            source_indices_list.remove(ind)

    print(f"Removed Indices : {ignore_index}")
    print(f"Total indices to be restored : {len(source_indices_list)}")
    restore_indices = ','.join(source_indices_list)

    post_restore_url = f"https://{TARGET_DOMAIN_NAME}/_snapshot/{SOURCE_SNAPSHOT_REPO_NAME}/{SOURCE_MANUAL_SNAPSHOT_NAME}/_restore"
    print(f"Target - Post Snapshot URL : {post_restore_url}")

    restore_response = restore_manual_snapshot_to_target(post_restore_url, restore_indices)
    print(f"Target - Post Snapshot Response : {restore_response}")
