"""
This class implements the enum for various API response statusCode and body
"""
from enum import Enum


class APIResponse(Enum):
    """
    Enums for API response
    """
    SUCCESS = {
        "statusCode": 200,
        "body": "Records sent"
    }

    INVALID_JSON_REQUEST = {
        "statusCode": 400,
        "body": "Please provide a valid JSON in request."
    }

    INCORRECT_SCHEMA = {
        "statusCode": 404,
        "body": "Can't find schema. Please provide correct schema name."
    }

    DATA_SCHEMA_MISMATCH = {
        "statusCode": 400,
        "body": "Data validation failed. SCHEMA/DATA MISMATCH!!"
    }
