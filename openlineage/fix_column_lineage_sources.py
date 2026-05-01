"""
Fix: Ingest synthetic OpenLineage events for INPUT datasets so that
DataZone can link column lineage to actual cataloged assets.

When DataZone sees a columnLineage facet but the input assets don't exist
in the catalog, it cannot resolve "Source columns" — they appear as '-'.

This script sends minimal COMPLETE events for each input dataset so
DataZone registers them as lineage nodes, enabling column-level resolution.

Run this BEFORE or AFTER re-ingesting 1776138988690.json.
"""

import boto3
import json
import uuid
from datetime import datetime, timezone

domain_id = "dzd_6l7t90mge4intz"
region = "us-east-1"
client = boto3.client('datazone', region_name=region)

PRODUCER = "https://github.com/OpenLineage/OpenLineage/tree/1.45.0/integration/spark"
SCHEMA_URL = "https://openlineage.io/spec/2-0-2/OpenLineage.json#/$defs/RunEvent"

# Exact namespace+name as used in 1776138988690.json
INPUT_DATASETS = [
    {
        "namespace": "s3://trepp-developmentservices-lake",
        "name": "curationZone/cmbs/dealrpt",
        "fields": [
            {"name": "op", "type": "string"},
            {"name": "dl_change_seq", "type": "string"},
            {"name": "updatedt", "type": "timestamp"},
            {"name": "dl_timestamp", "type": "string"},
            {"name": "dealid", "type": "integer"},
            {"name": "dealname", "type": "string"},
            {"name": "bloombergname", "type": "string"},
            {"name": "dealtype", "type": "string"},
            {"name": "closedt", "type": "timestamp"},
            {"name": "seccutoffdt", "type": "timestamp"},
            {"name": "curdistribdt", "type": "timestamp"},
            {"name": "secdealbal", "type": "decimal(19,4)"},
            {"name": "updatedt", "type": "timestamp"},
            {"name": "archivedt", "type": "timestamp"},
            {"name": "triggerhit", "type": "string"},
            {"name": "triggermodeledflag", "type": "string"},
            {"name": "settlementdate", "type": "timestamp"},
            {"name": "indices", "type": "string"},
            {"name": "initialpricingdate", "type": "timestamp"},
            {"name": "specialservicer2", "type": "string"},
            {"name": "specialservicer3", "type": "string"},
            {"name": "year", "type": "string"},
            {"name": "month", "type": "string"},
        ]
    },
    {
        "namespace": "s3://trepp-developmentservices-lake",
        "name": "curationZone/cmbs/mktrpt",
        "fields": [
            {"name": "DSCRLessThan1", "type": "decimal(38,19)"},
            {"name": "MSAPercent1To25", "type": "decimal(19,6)"},
            {"name": "dealid", "type": "integer"},
            {"name": "curdistribdt", "type": "timestamp"},
            {"name": "triggerhit", "type": "string"},
            {"name": "triggermodeledflag", "type": "string"},
            {"name": "sfpercent", "type": "decimal(19,6)"},
            {"name": "bankruptcyBalance", "type": "decimal(19,4)"},
            {"name": "topstate", "type": "string"},
            {"name": "topStatePercent", "type": "decimal(38,19)"},
            {"name": "thirdstateproppct", "type": "decimal(19,6)"},
            {"name": "topstateproppct", "type": "decimal(19,6)"},
            {"name": "dl_timestamp", "type": "string"},
            {"name": "dl_change_seq", "type": "string"},
        ]
    }
]


def build_registration_event(dataset):
    """
    Build a minimal OpenLineage COMPLETE event that registers
    a dataset as both input and output (self-referential) so
    DataZone catalogs it as a lineage node with schema.
    """
    run_id = str(uuid.uuid4())
    job_name = f"register_{dataset['name'].replace('/', '_')}"
    namespace = dataset['namespace']
    name = dataset['name']

    schema_facet = {
        "_producer": PRODUCER,
        "_schemaURL": "https://openlineage.io/spec/facets/1-2-0/SchemaDatasetFacet.json#/$defs/SchemaDatasetFacet",
        "fields": dataset['fields']
    }

    datasource_facet = {
        "_producer": PRODUCER,
        "_schemaURL": "https://openlineage.io/spec/facets/1-0-1/DatasourceDatasetFacet.json#/$defs/DatasourceDatasetFacet",
        "name": namespace,
        "uri": namespace
    }

    event = {
        "eventTime": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z",
        "producer": PRODUCER,
        "schemaURL": SCHEMA_URL,
        "eventType": "COMPLETE",
        "run": {
            "runId": run_id,
            "facets": {}
        },
        "job": {
            "namespace": namespace,
            "name": job_name,
            "facets": {}
        },
        "inputs": [],
        "outputs": [
            {
                "namespace": namespace,
                "name": name,
                "facets": {
                    "dataSource": datasource_facet,
                    "schema": schema_facet
                },
                "outputFacets": {}
            }
        ]
    }
    return event


def ingest_event(event, label):
    json_bytes = json.dumps(event).encode('utf-8')
    try:
        response = client.post_lineage_event(
            domainIdentifier=domain_id,
            event=json_bytes
        )
        status = response.get('ResponseMetadata', {}).get('HTTPStatusCode')
        print(f"  ✅ {label} — HTTP {status}")
        return True
    except Exception as e:
        print(f"  ❌ {label} — ERROR: {e}")
        return False


if __name__ == "__main__":
    print("=" * 60)
    print("Step 1: Register input datasets as lineage nodes")
    print("=" * 60)
    for ds in INPUT_DATASETS:
        label = ds['name']
        event = build_registration_event(ds)
        ingest_event(event, label)

    print()
    print("=" * 60)
    print("Step 2: Re-ingest the full column lineage event")
    print("=" * 60)

    json_file_path = "/Volumes/workspace/backup/D/workspace/newproject/openlineage/1776138988690.json"
    with open(json_file_path) as f:
        full_event = json.load(f)

    json_bytes = json.dumps(full_event).encode('utf-8')
    try:
        response = client.post_lineage_event(
            domainIdentifier=domain_id,
            event=json_bytes
        )
        status = response.get('ResponseMetadata', {}).get('HTTPStatusCode')
        print(f"  ✅ Full lineage event re-ingested — HTTP {status}")
    except Exception as e:
        print(f"  ❌ ERROR re-ingesting full event: {e}")

    print()
    print("Done. Wait 1-2 minutes, then refresh the DataZone UI.")
    print("Navigate to: Catalog → cmbsrptsnapshot_parquet → Lineage → Output tab")
    print("Source columns should now be populated.")

