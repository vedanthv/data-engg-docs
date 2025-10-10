## The Kafka Poll Loop

```java
Duration timeout = Duration.ofMillis(100);

while (true) {
    ConsumerRecords<String, String> records = consumer.poll(timeout);
    for (ConsumerRecord<String, String> record : records) 
    {
        System.out.printf("topic = %s, partition = %d, offset = %d, " +
        "customer = %s, country = %s\n",
        record.topic(), record.partition(), record.offset(),
        record.key(), record.value());

        int updatedCount = 1;

        if (custCountryMap.containsKey(record.value())) 
            {
            updatedCount = custCountryMap.get(record.value()) + 1;
            }
        custCountryMap.put(record.value(), updatedCount);

        JSONObject json = new JSONObject(custCountryMap);

        System.out.println(json.toString());
        }
}
```

The same way that sharks need to keep moving or they will die, consumers must continuously poll or they will be considered dead.

The parameter ```timeout``` passed to poll() controls how long poll() will block data if data is not available in consumer buffer.

Above code just keeps running sum of # of customers and their details are printed out.

### Addn Functions of Poll Loop

The first time poll() is called with consumer, its responsible for finding the ```GroupCoordinator```, joining a consumer group and reveiving a partition assignment.

If a rebalance is triggered it will be handled in the poll loop including callbacks. Anything that can go wrong in consumer or listeners is likely to show up as an exception while polling.

If poll is not invoked for more than ```max.poll.interval.ms``` consumer will be considered dead and removed from consumer group.

### Thread Safety

We cant have multiple consumers that belong to same group in one thread, we cant have multiple threads using same consumer.

To run multiple consumers in same group each one needs to run in own thread.