# Kafka : Validating Configuration

The org.apache.kafka.tools package includes ```VerifiableProducer``` and ```VerifiableConsumer``` classes. These can run as command-line tools or be embedded in an automated testing framework. The idea is that the verifiable producer produces a sequence of messages containing numbers from 1 to a value we choose. 

We can configure the verifiable producer the same way we configure our own producer, setting the right number of acks, retries, delivery.timeout.ms, and rate at which the messages will be produced. When we run it, it will print success or error for each message sent to the broker, based on the acks received. 

The verifiable consumer performs the complementary check. It consumes events (usually those produced by the verifiable producer) and prints out the events it consumed in order. It also prints information regarding commits and rebalances.

## Tests to Run

**Leader election:** what happens if we kill the leader? How long does it take the producer and consumer to start working as usual again?

**Controller election:** how long does it take the system to resume after a restart of the controller?

**Rolling restart:** can we restart the brokers one by one without losing any messages?

**Unclean leader election test:** what happens when we kill all the replicas for a partition one by one (to make sure each goes out of sync) and then start a broker that was out of sync? What needs to happen in order to resume operations? Is this acceptable?

# Validating Applications

## Failure Conditions to Be Tested

- Clients lose connectivity to one of the brokers
- High latency between client and broker
- Disk full
- Hanging disk (also called “brown out”)
- Leader election
- Rolling restart of brokers
- Rolling restart of consumers
- Rolling restart of producers

There are many tools that can be used to introduce network and disk faults, and many are excellent, so we will not attempt to make specific recommendations. Apache Kafka itself includes the Trogdor test framework for fault injection. For each scenario, we will have expected behavior, which is what we planned on seeing when we developed the application. Then we run the test to see what actually happens.

For example, when planning for a rolling restart of consumers, we planned for a short pause as consumers rebalance and then continue consumption with no more than 1,000 duplicate values. Our test will show whether the way the application commits offsets and handles rebalances actually works this way.
