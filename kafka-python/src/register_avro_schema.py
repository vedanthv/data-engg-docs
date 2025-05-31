import logging
import os

from confluent_kafka.schema_registry import Schema, SchemaRegistryClient
from confluent_kafka.schema_registry.error import SchemaRegistryError

class SchemaClient:
    def __init__(self, schema_url, schema_subject_name, schema_str, schema_type):
        """Initialize the Schema Registry Client."""
        self.schema_url = schema_url
        self.schema_subject_name = schema_subject_name
        self.schema_str = schema_str
        self.schema_type = schema_type
        self.schema_registry_client = SchemaRegistryClient({"url": self.schema_url})

    def get_schema_id(self):
        try:
            schema_version = self.schema_registry_client.get_latest_version(
                self.schema_subject_name
            )
            schema_id = schema_version.schema_id
            print(
                f"Schema ID for Schema in {self.schema_subject_name}: {schema_id}"
            )
            return schema_id
        except SchemaRegistryError:
            return False

    def get_schema_str(self):
        try:
            schema_id = self.get_schema_id()
            if schema_id:
                schema = self.schema_registry_client.get_schema(schema_id)
                return schema.schema_str
            else:
                return None
        except SchemaRegistryError as e:
            logging.error(e)

    def register_schema(self):
        """Register the Schema in Schema Registry."""
        try:
            self.schema_registry_client.register_schema(
                subject_name=self.schema_subject_name,
                schema=Schema(self.schema_str, schema_type=self.schema_type),
            )
            print(
                f"Schema Registered Successfully for {self.schema_subject_name}"  # noqa: E501
            )
        except SchemaRegistryError as e:
            print(f"Error while registering the Schema {e}")
            exit(1)

    def set_compatibility(self, compatibility_level):
        """Update Subject Level Compatibility Level."""
        try:
            self.schema_registry_client.set_compatibility(
                self.schema_subject_name, compatibility_level
            )
            print(f"Compatibility level set to {compatibility_level}")
        except SchemaRegistryError as e:
            print(e)
            exit(1)


if __name__ == "__main__":
    bootstrap_servers = 'localhost:19092'
    topic = 'test-topic'
    schema_type = "AVRO"
    schema_url = "http://localhost:18081"

    # In redpanda, JSON Schema not supported, but AVRO and PROTOBUF supported
    with open("./schema.avsc") as avro_schema_file:
        schema_str = avro_schema_file.read()

    schema_client = SchemaClient(schema_url, topic, schema_str, schema_type)
    schema_client.set_compatibility("BACKWARD")
    schema_client.register_schema()
