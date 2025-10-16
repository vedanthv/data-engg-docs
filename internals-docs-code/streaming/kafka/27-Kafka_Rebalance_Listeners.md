## Rebalance Listeners in Kafka

If we know that our consumer is about to lose ownership of a partition, we want to commit offsets of the last event you've processed.

The consumer API allows you to run your own code when partitions are added or removed from the consumer. We need to do this by passing ```ConsumerRebalanceListener``` when calling the ```subscribe``` method.

It has three methods to implement:

```public void onPartitionsAssigned(Collection<TopicPartition> partitions)```

Called after partitions have been reassigned to the consumer but before the consumer starts consuming messages. This is where you prepare or load any state that you want to use with the partition.

Any steps taken here should be guaranteed to return within ```max.poll.timeout.ms```

```public void onPartitionsRevoked(Collection<TopicPartition> partitions)```

Called when the consumer has to give up partitions that it previously owned - either when a rebalance happens or consumer closes.

When an eager rebalancing algorithm is used, this method is invoked before rebalancing starts and after consumer has consumed last batch of messages. This is because in eager algorithm, we need to reassign all partitions and hence before it happens offsets must be committed.

If a cooperative rebalancing algorithm is used, this method is invoked at the end of the rebalance with just the subset of partitions that the consumer has to give up.

```public void onPartitionsLost(Collection<TopicPartition> partitions)```

Called in exceptional cases where the partitions were assigned to other consumers without first being revoked by the rebalance algorithm.

This is where we clean up any state or resources that are used with these partitions. Note that this has to be done with caution because the new owner of the partitions may have already saved its own state.

![alt text](https://snipboard.io/M5Inw1.jpg)

