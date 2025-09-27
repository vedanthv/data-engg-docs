## Redpanda Kafka 

This is a repository with concepts covering Redpanda Kafka on EC2 instance.

### Topics 

- Kafka Components & Architecture (Basic Overview)
- Install Redpanda
- Install Redpanda-Console
- Install Redpanda (With Three Brokers)
- Create Producer to Produce Message
- Create Consumer to Consumer Message
- Serialization and Deserialization
- Produce & Consume Message in JSON format
- Register the Schema in the Schema Registry
- Use JSONSerializer & JSONDeserializer - Fetch schema from Schema Registry to Validate & Serialize /- Deserialize (Redpanda Schema Registry Does not Support JSON)
- Produce Message in AVRO format
- Consume Message in AVRO format
- Send Key and Headers (example- Coorelation_ID) with every message
- On_delivery callback vs flush()
- Producer Configs (compression.type & message.max.bytes)
- Producer Configs (batch.size & linger.ms)
- Log compaction
- Deleting Records in Kafka aka Kafka Tombstone
- auto_offset_reset (Consumer Configuration)
- Consumer Group
- Schema Evolution & Schema Compatibility
- Special topic called _consumer_offsets  & _schemas topic
- Kcat (Kafka cat commands)
