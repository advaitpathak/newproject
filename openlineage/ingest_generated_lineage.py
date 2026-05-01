import boto3
import json
import logging
import uuid
from datetime import datetime, timezone


domain_id = "dzd_6l7t90mge4intz"

json_file_path = "/Volumes/workspace/backup/D/workspace/newproject/openlineage/lineage_updated.json"
# json_file_path = "/Volumes/workspace/backup/D/workspace/newproject/openlineage/lineage_fixed.json"

# json_file_path = "/Volumes/workspace/backup/D/workspace/newproject/openlineage/lineage_mktrpt.json"

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def ingest_lineage_datazone(domain_id):
    with open(json_file_path) as f:
        data = json.load(f)

    # Generate a fresh runId and eventTime so DataZone does not deduplicate this as an old run
    data['run']['runId'] = str(uuid.uuid4())
    data['eventTime'] = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'

    print(f"Posting with runId: {data['run']['runId']}")
    print(f"Posting with eventTime: {data['eventTime']}")

    client = boto3.client('datazone', region_name='us-east-1')

    json_bytes = json.dumps(data).encode('utf-8')

    response = client.post_lineage_event(
        domainIdentifier=domain_id,
        event=json_bytes
    )
    print(response)
    logger.info("Ingested lineage")

ingest_lineage_datazone(domain_id)
