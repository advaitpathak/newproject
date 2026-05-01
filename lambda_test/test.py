import json
import logging
import time
from collections import defaultdict
from datetime import datetime, UTC

import boto3

glue_client = boto3.client("glue")
athena_client = boto3.client("athena")
s3_client = boto3.client("s3")
sns_client = boto3.client('sns')


def read_config():
    logging.info("Reading configuration from config.json")
    with open('config.json', 'r') as f:
        config = json.load(f)
    return config


def read_athena_query(landing_db, curation_db, presentation_db):
    logging.info("Reading Athena query from athena_query.sql")
    with open('athena_query.sql', 'r') as f:
        athena_query = f.read()
    athena_query = athena_query.format(landing_db=landing_db, curation_db=curation_db, presentation_db=presentation_db)
    logging.info(athena_query)
    return athena_query


def run_athena_query(query, bucket, prefix):
    athena_output_location = f"s3://{bucket}/{prefix}athena_queries/"
    logging.info("Running athena query and waiting for results")
    logging.info(f"Athena query output location: {athena_output_location}")

    response = athena_client.start_query_execution(
        QueryString=query,
        ResultConfiguration={"OutputLocation": athena_output_location}
    )

    qid = response["QueryExecutionId"]
    start_time = time.time()

    execution = None

    # Wait for query completion
    while True:
        execution = athena_client.get_query_execution(QueryExecutionId=qid)
        status = execution["QueryExecution"]["Status"]
        state = status["State"]

        if state in ["SUCCEEDED", "FAILED", "CANCELLED"]:
            break

        if time.time() - start_time > 240:
            raise Exception("Athena query timeout")

        time.sleep(2)

    if state != "SUCCEEDED":
        reason = status.get("StateChangeReason", "Unknown reason")
        error_msg = status.get("AthenaError", {}).get("ErrorMessage", "")
        logging.error(
            f"Athena query failed. State={state}, Reason={reason}, "
            f"ErrorMessage={error_msg}, QueryExecutionId={qid}"
        )
        raise Exception("Athena query failed")

    # Fetch results with pagination
    data = []
    next_token = None
    headers = None

    while True:
        params = {"QueryExecutionId": qid}
        if next_token:
            params["NextToken"] = next_token

        results = athena_client.get_query_results(**params)

        rows = results["ResultSet"]["Rows"]

        # Extract headers only once
        if headers is None:
            headers = [c["VarCharValue"] for c in rows[0]["Data"]]
            rows = rows[1:]  # skip header row

        for row in rows:
            values = [c.get("VarCharValue") for c in row["Data"]]
            data.append(dict(zip(headers, values)))

        next_token = results.get("NextToken")
        if not next_token:
            break

    return data


def load_all_glue_tables(database_name):
    logging.info("Loading all glue tables")
    paginator = glue_client.get_paginator("get_tables")

    tables = []

    for page in paginator.paginate(DatabaseName=database_name):
        tables.extend(page["TableList"])

    return tables


def process_tables(tables, table_map):
    logging.info("Processing tables to calculate coverage metrics")
    database_total_tables = 0
    database_described_tables = 0

    table_metrics = []

    lob_stats = defaultdict(lambda: {
        "tables": 0,
        "total_columns": 0,
        "described_columns": 0
    })

    dataset_path_stats = defaultdict(lambda: {
        "tables": 0,
        "total_columns": 0,
        "described_columns": 0,
        "lob": None
    })

    missing_tables = []

    total_columns = 0
    described_columns = 0

    for table in tables:

        database_total_tables += 1

        table_name = table["Name"]
        location = table.get("StorageDescriptor", {}).get("Location")
        table_dataset_path = extract_dataset_from_location(location)

        mapping = table_map.get(table_dataset_path, {})
        lob = mapping.get("lob", "UNKNOWN")
        dataset_path = mapping.get("dataset_path", table_dataset_path or "UNKNOWN")

        # table description coverage
        if table.get("Description"):
            database_described_tables += 1

        columns = table.get("StorageDescriptor", {}).get("Columns", [])
        partitions = table.get("PartitionKeys", [])

        all_columns = columns + partitions

        t_total_cols = len(all_columns)

        t_described_cols = sum(
            1 for c in all_columns
            if c.get("Comment") and c["Comment"].strip()
        )

        coverage = round((t_described_cols / t_total_cols) * 100, 2) if t_total_cols else 0

        total_columns += t_total_cols
        described_columns += t_described_cols

        # store table metrics
        table_metrics.append({
            "table_name": table_name,
            "dataset_path": dataset_path,
            "lob": lob,
            "total_columns": t_total_cols,
            "described_columns": t_described_cols,
            "coverage_percent": coverage
        })

        # detect poor documentation
        if coverage < 20:
            missing_tables.append({
                "table_name": table_name,
                "lob": lob,
                "coverage_percent": coverage
            })

        # update lob stats
        lob_stats[lob]["tables"] += 1
        lob_stats[lob]["total_columns"] += t_total_cols
        lob_stats[lob]["described_columns"] += t_described_cols

        # update dataset path stats
        dataset_path_stats[dataset_path]["tables"] += 1
        dataset_path_stats[dataset_path]["total_columns"] += t_total_cols
        dataset_path_stats[dataset_path]["described_columns"] += t_described_cols
        dataset_path_stats[dataset_path]["lob"] = lob

    return database_total_tables, database_described_tables, total_columns, described_columns, lob_stats, dataset_path_stats, table_metrics, missing_tables


def aggregate_metrics_generate_report(database_total_tables, database_described_tables, total_columns,
                                      described_columns, lob_stats, dataset_path_stats, database_name, table_metrics,
                                      missing_tables):
    logging.info("Aggregating metrics and generating report")
    database_coverage = round(
        (database_described_tables / database_total_tables) * 100, 2
    ) if database_total_tables else 0

    column_coverage = round(
        (described_columns / total_columns) * 100, 2
    ) if total_columns else 0

    lob_metrics = []

    for lob, stats in lob_stats.items():
        coverage = round(
            stats["described_columns"] / stats["total_columns"] * 100, 2
        ) if stats["total_columns"] else 0

        lob_metrics.append({
            "lob": lob,
            "tables": stats["tables"],
            "total_columns": stats["total_columns"],
            "described_columns": stats["described_columns"],
            "coverage_percent": coverage
        })

    dataset_path_metrics = []

    for dataset_path, stats in dataset_path_stats.items():
        coverage = round(
            stats["described_columns"] / stats["total_columns"] * 100, 2
        ) if stats["total_columns"] else 0

        dataset_path_metrics.append({
            "dataset_path": dataset_path,
            "lob": stats["lob"],
            "tables": stats["tables"],
            "total_columns": stats["total_columns"],
            "described_columns": stats["described_columns"],
            "coverage_percent": coverage
        })

    report = {
        "status": "success",
        "generated_at": datetime.now(UTC).isoformat(),

        "database_metrics": {
            "database": database_name,
            "total_tables": database_total_tables,
            "described_tables": database_described_tables,
            "coverage_percent": database_coverage
        },

        "column_metrics_summary": {
            "total_columns": total_columns,
            "described_columns": described_columns,
            "coverage_percent": column_coverage
        },

        "lob_metrics": lob_metrics,
        "dataset_path_metrics": dataset_path_metrics,
        "table_metrics": table_metrics,

        "top_tables_missing_documentation":
            sorted(missing_tables, key=lambda x: x["coverage_percent"])[:20]
    }

    return report


def write_report_to_s3(report, bucket, key):
    logging.info(f"Writing report to S3 at location s3://{bucket}/{key}")
    s3_client.put_object(
        Bucket=bucket,
        Key=key,
        Body=json.dumps(report, indent=2),
        ContentType="application/json"
    )


def extract_dataset_from_location(location):
    if not location:
        return None

    # remove s3://bucket/
    parts = location.split("/", 3)

    if len(parts) < 4:
        return None

    dataset_path = parts[3]
    dataset_path = dataset_path.strip("/")

    # remove spark temporary folder
    dataset_path = dataset_path.replace("_temporary", "")
    dataset_path = dataset_path.strip("/")

    return dataset_path.lower()


def lambda_handler(event, context):
    try:
        # Read Config
        config = read_config()
        env = config['environment']
        sns = config['sns'] + '-dev' if env == 'development' else \
            config['sns'] + '-prod' if env == 'production' else \
            config['sns'] + '-' + env
        region = config['region']
        account_no = config['account_no']
        topic_arn = f"arn:aws:sns:{region}:{account_no}:{sns}"

        landing_db = config.get("landing_db")
        curation_db = config.get("curation_db")
        presentation_db = config.get("presentation_db")
        database_name = event.get("database", presentation_db)

        # Read athena query
        athena_query = read_athena_query(landing_db, curation_db, presentation_db)

        bucket = config.get("bucket")
        prefix = f"column-description-coverage/"

        # 1. GET DATASET PATH + LOB MAPPING FROM ATHENA
        athena_rows = run_athena_query(athena_query, bucket, prefix)

        table_map = {}

        for row in athena_rows:
            dataset_path = row.get("dataset_path", "UNKNOWN")
            lob = row.get("lob", "UNKNOWN")

            dataset_path = dataset_path.strip("/").lower()

            table_map[dataset_path] = {
                "lob": lob,
                "dataset_path": dataset_path
            }

        # 2. LOAD ALL GLUE TABLES ONCE
        tables = load_all_glue_tables(database_name)

        # 3. PROCESS TABLES
        database_total_tables, database_described_tables, total_columns, described_columns, lob_stats, dataset_path_stats, table_metrics, missing_tables = process_tables(
            tables, table_map)

        # 4. CALCULATE AGGREGATIONS AND GENERATE REPORT
        report = aggregate_metrics_generate_report(database_total_tables, database_described_tables, total_columns,
                                                   described_columns, lob_stats, dataset_path_stats, database_name,
                                                   table_metrics, missing_tables)

        # 5. WRITE REPORT TO S3
        timestamp = datetime.now(UTC).strftime("%Y%m%d_%H%M%S")
        key = f"{prefix}{database_name}/coverage_{timestamp}.json"
        write_report_to_s3(report, bucket, key)

        return {
            "status": "success",
            "report_location": f"s3://{bucket}/{key}"
        }

    except Exception as e:
        logging.error(f"Lambda function encountered an error {e}")

        sns_client.publish(
            TopicArn=topic_arn,
            Message=f"Column description coverage Lambda failed: {str(e)}",
            Subject="Lambda Function Failed: column_description_coverage"
        )
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }


lambda_handler({}, {})
