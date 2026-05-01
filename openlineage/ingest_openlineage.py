import boto3
import json
import logging


domain_id = "dzd_6l7t90mge4intz"
s3_client = boto3.client('s3')
bucket_name = "trepp-developmentservices-lake-rawdata"

json_file_path = "/Volumes/workspace/backup/D/workspace/newproject/openlineage/1776138988690.json"

logger = logging.getLogger()
logger.setLevel(logging.INFO)


# def format_inputs_outputs(data, datalake_bucket_name, mp, env, account_no):
#     formatted_data = []
#
#     for item in data:
#         formatted_data.append({
#             "name": get_glue_table_name(
#                 item["namespace"].replace("s3://", "s3a://") + item["name"].split("/date=")[0] + "/",
#                 datalake_bucket_name, mp),
#             "namespace": get_namespace(
#                 item["namespace"].replace("s3://", "s3a://") + item["name"].split("/date=")[0] + "/", env, account_no)
#
#         })
#     return formatted_data
#
#
# def get_glue_table_name(s3_path, datalake_bucket_name, mp):
#     if datalake_bucket_name in s3_path and datalake_bucket_name + "/" not in s3_path:
#         s3_path = s3_path.replace(datalake_bucket_name, datalake_bucket_name + "/")
#     table_name = mp.get(s3_path, "")
#     if table_name == "" and s3_path.endswith('/'):
#         table_name = mp.get(s3_path.rstrip('/'))
#
#     if table_name == "" and not s3_path.endswith('/'):
#         table_name = mp.get(s3_path + '/')
#
#     return table_name


def read_and_transform_lineage(transformed_lineage, datalake_bucket_name, mp, env, account_no):
    with open(json_file_path) as f:
        json_obj = json.load(f)
    if len(json_obj['inputs']) > 0 and len(json_obj['outputs']) > 0 and json_obj[
        "eventType"] == "COMPLETE":
        transformed_json = {
            "eventTime": json_obj["eventTime"],
            "producer": json_obj["producer"],
            "schemaURL": json_obj["schemaURL"],
            "eventType": "COMPLETE",
            "run": {
                "runId": json_obj["run"]["runId"]
            },
            "job": {
                "facets": json_obj["job"]["facets"],
                "name": json_obj["job"]["name"],
                "namespace": json_obj["job"]["namespace"]
            },
            "outputs": format_inputs_outputs(json_obj["outputs"], datalake_bucket_name, mp, env,
                                             account_no),
            "inputs": format_inputs_outputs(json_obj["inputs"], datalake_bucket_name, mp, env,
                                            account_no)
        }
        transformed_lineage[k] = transformed_json

    return transformed_lineage


def ingest_lineage_datazone(data, domain_id):
    client = boto3.client('datazone')

    json_bytes = json.dumps(data).encode('utf-8')

    response = client.post_lineage_event(
        domainIdentifier=domain_id,
        event=json_bytes
    )
    logger.info("Ingested lineage")


transformed_data = read_and_transform_lineage()
ingest_lineage_datazone(transformed_data, domain_id)
