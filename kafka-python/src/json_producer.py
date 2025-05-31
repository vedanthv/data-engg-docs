import json
import os
import jsonschema


import utils
from admin import Admin
from producer import ProducerClass

class User:
    def __init__(self, first_name, middle_name, last_name, age):
        self.first_name = first_name
        self.middle_name = middle_name
        self.last_name = last_name
        self.age = age


def user_to_dict(user):
    """Return a dictionary representation of a User instance  for
    serialization."""
    return dict(
        first_name=user.first_name,
        middle_name=user.middle_name,
        last_name=user.last_name,
        age=user.age,
    )


class JSONProducer(ProducerClass):
    def __init__(self, bootstrap_server, topic,schema):
        super().__init__(bootstrap_server, topic)
        self.schema = schema
        self.value_serializer = lambda v: json.dumps(v).encode("utf-8")

    def send_message(self, message_dict):
        try:
            # Convert message to JSON string and serialize
            jsonschema.validate(message_dict, self.schema)
            message_json = self.value_serializer(message_dict)
            self.producer.produce(self.topic, message_json)
            print(f"Message Sent: {message_json}")
        except jsonschema.ValidationError as e:
            print(e)

if __name__ == "__main__":

    bootstrap_servers = 'localhost:19092'
    topic = 'my-topic'

    """
    Loading using load(), because validate() function
    need schema in form of python dictionary
    """
    with open("./schema.json") as json_schema_file:
        json_schema = json.load(json_schema_file)

    admin = Admin(bootstrap_servers)
    producer = JSONProducer(bootstrap_servers, topic,json_schema)
    admin.create_topic(topic)

    try:
        while True:
            first_name = input("Enter first name: ")
            middle_name = input("Enter middle name: ")
            last_name = input("Enter last name: ")
            age = int(input("Enter age: "))
            user = User(
                        first_name=first_name,
                        middle_name=middle_name,
                        last_name=last_name,
                        age=age,
            )
            producer.send_message(user_to_dict(user))
    except KeyboardInterrupt:
        exit()

    producer.commit()
