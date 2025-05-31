import os
import json

from confluent_kafka.schema_registry import Schema, SchemaRegistryClient
from confluent_kafka.schema_registry.error import SchemaRegistryError


class SchemaClient:
    def __init__(self, schema_url, schema_subject_name, schema_str, schema_type):
        """Initialize the Schema Registry Client."""
        self.schema_url = schema_url
        self.schema_subject_name = schema_subject_name
        self.schema_str = schema_str
        self.schema_type = schema_type
        print(f"Schema Registry URL: {self.schema_url}")
        self.schema_registry_client = SchemaRegistryClient({"url": self.schema_url})

    def get_schema_id(self):
        """Return the schema ID of the latest version, or False if not found."""
        try:
            schema_version = self.schema_registry_client.get_latest_version(
                self.schema_subject_name
            )
            return schema_version.schema_id
        except SchemaRegistryError:
            return False

    def get_schema_str(self):
        """Return the string of the latest schema version."""
        try:
            schema_id = self.get_schema_id()
            if not schema_id:
                return None
            schema = self.schema_registry_client.get_schema(schema_id)
            return schema.schema_str
        except SchemaRegistryError as e:
            print(f"Error retrieving schema string: {e}")
            return None

    def register_schema(self):
        """Register the schema only if it differs from the latest version."""
        latest_schema_str = self.get_schema_str()

        # Normalize both schema strings for semantic comparison
        try:
            local_schema_json = json.loads(self.schema_str)
            latest_schema_json = json.loads(latest_schema_str) if latest_schema_str else None
        except json.JSONDecodeError as e:
            print(f"Error parsing schema JSON: {e}")
            exit(1)

        if latest_schema_json is None:
            # No existing schema — register it
            try:
                self.schema_registry_client.register_schema(
                    subject_name=self.schema_subject_name,
                    schema=Schema(self.schema_str, schema_type=self.schema_type),
                )
                print(f"Schema registered for subject '{self.schema_subject_name}'")
            except SchemaRegistryError as e:
                print(f"Error while registering the schema: {e}")
                exit(1)
        elif local_schema_json != latest_schema_json:
            # Schema has changed — register a new version
            try:
                self.schema_registry_client.register_schema(
                    subject_name=self.schema_subject_name,
                    schema=Schema(self.schema_str, schema_type=self.schema_type),
                )
                print(f"New version of schema registered for '{self.schema_subject_name}'")
            except SchemaRegistryError as e:
                print(f"Error while registering new version of schema: {e}")
                exit(1)
        else:
            print(f"The schema is already up to date for '{self.schema_subject_name}'.")


if __name__ == "__main__":
    topic = "avro-topic"
    schema_url = "http://localhost:18081"
    schema_type = "AVRO"

    with open("./schema.avsc") as avro_schema_file:
        avro_schema = avro_schema_file.read()

    schema_client = SchemaClient(schema_url, topic, avro_schema, schema_type)
    schema_client.register_schema()
    schema_str = schema_client.get_schema_str()
    print(f"Latest schema string:\n{schema_str}")
