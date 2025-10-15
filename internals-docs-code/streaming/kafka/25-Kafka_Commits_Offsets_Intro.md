## Kafka Commits and Offsets

When we call ```poll``` method, it returns all records from producer that have not yet been consumed. So we have a method of tracking which messages arent consumed yet.

Kafka does not track acknowledgements from consumers but rather allows consumers to track their positions per partition of data using offsets. This is called an offset commit.

Consumers commit the last message they have successfully processed and **assume that every message before this has been processed**.

### How does a consumer commit an offset?

It sends a message to Kafka that will update a special topic ```_consumer_offsets``` for each partition.

When a consumer crashes, a rebalance will be triggered and inorder for consumer to know where to pick up from when it starts, it will read data from latest committed offset.

If the committed offset is smaller than offset of latest message in partition, then we will end up reading messages twice (duplicated)

If the committed offset is larger than the offset of the latest message in partition, then we will end up missing out on lot of data.

