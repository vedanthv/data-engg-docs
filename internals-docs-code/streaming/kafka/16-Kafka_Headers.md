## Headers in Kafka

Record headers give you the ability to add some metadata about the Kafka record, without adding any extra information to the key/value pair of the record itself. Headers are often used for lineage to indicate the source of
the data in the record, and for routing or tracing messages based on header information without having to parse the
message itself (perhaps the message is encrypted and the router doesn’t have permissions to access the data). Headers are implemented as an ordered collection of key/value pairs. The keys are always a String, and the values can be any serialized object—just like the message value.

```python
from confluent_kafka import Producer

# Create Kafka Producer
producer = Producer({'bootstrap.servers': 'localhost:9092'})

# Define message headers
headers = [
    ('event_type', b'user_signup'),
    ('source', b'web'),
    ('schema_version', b'1.0')
]

# Send message with headers
producer.produce(
    topic='user_events',
    key='user_123',              # optional
    value='{"user_id": 123, "name": "Alice"}',
    headers=headers
)

# Wait for delivery
producer.flush()
```