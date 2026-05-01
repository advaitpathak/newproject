"""
Module to implement Glue Schema Registry
"""
import json
import logging
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)


class GlueSchemaRegistry:
    """
    Implements glue schema registry
    """
    def __init__(self, glue_client):
        """
        :param glue_client: a boto3 glue client
        """
        self.glue_client = glue_client

    def create_registry(self, registry_name):
        """
        Creates a registry
        :param registry_name: name of the registry to be created
        :return:
        """
        self.glue_client.create_registry(RegistryName=registry_name)

    # pylint: disable=too-many-arguments, line-too-long
    def create_schema(self, registry_name, schema_name, data_format, compatibility, schema_definition):
        """
        :param registry_name: registry name in which schema needs to be created
        :param schema_name: the schema name
        :param data_format: the data format JSON | AVRO | PROTOBUF
        :param compatibility: NONE | BACKWARD | BACKWARD_ALL | FORWARD | FORWARD_ALL | FULL | FULL_ALL
        :param schema_definition: the schema definition
        :return:
        """
        try:
            response = self.glue_client.create_schema(
                RegistryId={
                    'RegistryName': registry_name
                },
                SchemaName=schema_name,
                DataFormat=data_format,
                Compatibility=compatibility,
                SchemaDefinition=json.dumps(schema_definition)
            )
            return response
        except ClientError:
            logger.exception("Couldn't create schema %s.", schema_name)
            raise

    def get_glue_schema_version(self, registry_name, schema_name):
        """
        Fetches the latest version of schema from AWS
        :param registry_name: the registry name in which the schema is located
        :param schema_name: the schema name
        :return: schema definition
        """
        try:
            schema_message = self.glue_client.get_schema_version(
                SchemaId={
                    'SchemaName': schema_name,
                    'RegistryName': registry_name
                },
                SchemaVersionNumber={
                    'LatestVersion': True
                }
            )
            schema_definition = json.loads(schema_message['SchemaDefinition'])
            logger.debug("Found schema %s", schema_definition)
            return schema_definition
        except ClientError as client_error:
            logger.info("Couldn't get schema %s.", schema_name)
            raise client_error
