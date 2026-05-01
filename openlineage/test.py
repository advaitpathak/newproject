import boto3
import json
import logging


domain_id = "dzd_6l7t90mge4intz"
s3_client = boto3.client('s3')
bucket_name = "trepp-developmentservices-lake-rawdata"

json_file_path = "/Volumes/workspace/backup/D/workspace/newproject/openlineage/1776138988690.json"

# Asset ID for cmbsrptsnapshot_parquet in DataZone
# Find this in the DataZone UI: asset URL contains the asset ID
# e.g. https://<domain>.datazone.aws/.../<asset_id>/...
ASSET_ID = "5vauyclv3lri1z"  # update with actual asset ID from the UI URL

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def ingest_lineage_datazone(domain_id):
    with open(json_file_path) as f:
        data = json.load(f)
    client = boto3.client('datazone', region_name='us-east-1')

    # Step 1: Post the OpenLineage event (updates LINEAGE tab)
    json_bytes = json.dumps(data).encode('utf-8')
    response = client.post_lineage_event(
        domainIdentifier=domain_id,
        event=json_bytes
    )
    print("post_lineage_event response:", response)
    logger.info("Ingested lineage event")

    # Step 2: Create a new asset revision (updates HISTORY tab)
    # First get the current asset to retrieve its existing metadata
    try:
        asset = client.get_asset(
            domainIdentifier=domain_id,
            identifier=ASSET_ID
        )
        print("Current asset revision:", asset.get('revision'))

        revision_response = client.create_asset_revision(
            domainIdentifier=domain_id,
            identifier=ASSET_ID,
            name=asset['name'],
            description=asset.get('description', 'Updated with column lineage'),
            # Pass through existing form metadata so nothing is overwritten
            formsInput=asset.get('formsOutput', [])
        )
        print("create_asset_revision response:", revision_response.get('revision'))
        logger.info("Created new asset revision: %s", revision_response.get('revision'))

    except client.exceptions.ResourceNotFoundException:
        print(f"Asset {ASSET_ID} not found. Check the ASSET_ID value.")
    except Exception as e:
        print(f"create_asset_revision failed: {e}")
        logger.error("Failed to create asset revision: %s", e)


ingest_lineage_datazone(domain_id)
# amnihd9pww16w7 older
# after adding column lineage 5vauyclv3lri1z