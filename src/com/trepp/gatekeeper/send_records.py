"""
This code runs on AWS Lambda and produces records to a Kinesis stream using API Gateway
"""
import os
import uuid
import time
from datetime import datetime

import boto3
from botocore.exceptions import ClientError
from src.com.trepp.utils.lib.aws.kinesis_streams import KinesisStream
from src.com.trepp.utils.lib.aws.glue_schema_registry import GlueSchemaRegistry
from src.com.trepp.utils.lib.schema_validator import validate_request, validate_data
from src.com.trepp.utils.lib.logger import initiate_logger
from src.com.trepp.utils.lib.response_enum import APIResponse


# pylint: disable=too-many-locals, unused-argument, broad-exception-caught
def main(event, context):
    """
    Produces data to kinesis stream based on API request
    :param event: information on event that triggers lambda
    :param context: not used
    :return: 200 if success and other exceptions based on the enums declared in class APIResponse
    """
    env = os.getenv('ENVIRONMENT', 'local')
    logger_level_name = os.getenv('LOGGER_LEVEL_NAME', 'INFO')

    log = initiate_logger('trepp-stream', logger_level_name, file_name='/tmp/app_debug.log')
    # log.propagate = False
    log.info('Starting gatekeeper process')
    # Start execution timer
    start_time = time.time()

    log.debug('Env Variable - ENVIRONMENT = %s', env)

    record_count = 0

    try:
        registry_name, stream_name, schema_name, data = validate_request(event, log)
    except Exception as err:
        log.error("Please provide a valid JSON in request. %s ", err)
        return APIResponse.INVALID_JSON_REQUEST.value

    try:
        gsr = GlueSchemaRegistry(boto3.client('glue'))
        schema_definition = gsr.get_glue_schema_version(registry_name, schema_name)
    except ClientError as client_error:
        log.info("SENT RECORDS - 0")
        log.error("Incorrect schema_name %s", client_error)
        return APIResponse.INCORRECT_SCHEMA.value

    try:
        is_schema_valid = validate_data(data, schema_definition)
    except Exception as err:
        log.error("Data validation failed. SCHEMA/DATA MISMATCH!! %s", err)
        return APIResponse.DATA_SCHEMA_MISMATCH.value

    # Initialize Stream
    stream = KinesisStream(kinesis_client=boto3.client('kinesis'))
    stream.describe(stream_name)

    if is_schema_valid:
        for record in data:
            # Set a partition key
            partition_key = str(uuid.uuid4())
            # add columns for partitioning
            record['event_id'] = partition_key
            record['schema_name'] = schema_name
            record['event_timestamp'] = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
            response = stream.put_record_json(record, partition_key)
            log.debug("Kinesis response - %s", response)
            record_count += 1
        log.info("VALIDATED RECORDS - %s", record_count)
        log.info("Produced %s records successfully to Kinesis stream %s", record_count, stream_name)
        log.info("SENT RECORDS - %s", record_count)

        # End execution timer
        end_time = time.time()
        execution_time = end_time - start_time
        log.debug("Execution time - %0.2f", execution_time)
        log.debug("THROUGHPUT - %0.2f", (record_count / execution_time))

        return APIResponse.SUCCESS.value

    log.info("VALIDATED RECORDS - %s", record_count)
    log.error("SCHEMA CHECK FAILED !! - %s", is_schema_valid)
    return APIResponse.DATA_SCHEMA_MISMATCH.value
    # return error code for each record/batch records
    # return error code and save in a separate section (quarantine)
