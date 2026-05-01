"""
This module implements the helper utils for schema validation
"""
import json
import jsonschema


def validate_request(event, log):
    """
    Validate the request and extract attributes like stream_name, registry_name,
    schema_name and data from request.
    :param event: information to get data from api gateway request
    :param log: for logging
    :return: registry_name, stream_name, schema_name, data
    """
    try:
        body = json.loads(event['body'])
        registry_name = body.get('registry_name', 'hliu-test')
        stream_name = body.get('stream_name', 'test-stream-hliu')
        schema_name = body.get('schema_name')
        data = body.get('data')
        # Check if data is single record or batch of records
        if not isinstance(data, list):
            data = [data]
        log.info(f"RECEIVED RECORDS : {len(data)}")
    except Exception as err:
        raise err

    return registry_name, stream_name, schema_name, data


def validate_data(data, schema):
    """
    Validates the data against the provided schema
    :param data: the data to be validated
    :param schema: the schema definition
    :return: valid schema or exception
    """
    try:
        jsonschema.validate(instance=data, schema=schema)
        return True
    except jsonschema.ValidationError as err:
        raise err
