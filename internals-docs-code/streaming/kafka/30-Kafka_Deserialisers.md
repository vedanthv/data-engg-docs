## Deserializers in Kafka

This passage explains the importance of using matching **serializers** and **deserializers** in Kafka.

When a producer sends data to Kafka, it must first **serialize** that data — convert it from an object (like a number or string) into a sequence of bytes that Kafka can store and transmit. On the consumer side, the same data must be **deserialized** — converted back from bytes into a usable form.

If the serializer and deserializer don’t match, the consumer will not be able to correctly interpret the data. For example, if you use `IntSerializer` to send integers but the consumer uses `StringDeserializer`, the consumer will misread the byte data and likely fail with an error.

As a result, developers must know which serializers were used for each Kafka topic and ensure that all consumers of that topic use the corresponding deserializers.

Using a **Schema Registry** with **Avro serialization** helps enforce this consistency. The Avro serializer and deserializer rely on a defined schema that ensures all data in a topic follows the same structure. If a producer tries to write incompatible data or if a consumer uses the wrong schema, Kafka will throw clear errors.

This makes debugging much easier and prevents data corruption or misinterpretation.

## Custom Deserializers in Kafka

Check pg 184 for more details.

## Using Avro Deserialization with Consumer

<img src = "https://snipboard.io/4QVMyL.jpg">

1 - Use KafkaAvroDeserializer to deserialize Avro messages
2 - To store schemas
3 - Define type for the record value    
4 - Instance of customer


