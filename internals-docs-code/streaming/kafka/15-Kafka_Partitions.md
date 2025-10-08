## Partitions in Kafka

When a message is produced to a Kafka topic, it can include an optional **key**. The key serves two main purposes:

1. **Metadata or identification** — It’s stored along with the message and can represent something meaningful, such as a user ID, customer ID, or product code. This helps group related messages together.

2. **Partitioning logic** — Kafka uses the key to decide which partition within a topic the message will go to.

   * If messages have the same key, Kafka ensures they are always sent to the **same partition**.
   * This guarantees that all messages related to a particular key are **processed in order**, since order is preserved within a partition.

This also affects how messages are **consumed**. If a consumer group has multiple consumers, and each consumer reads from a subset of partitions, then:

* All messages for a particular key will always be read by the **same consumer** (because they all reside in the same partition).

Keys help maintain **data locality** (same key - same partition) and **processing consistency** (same consumer processes related messages).

### In Build Kafka Partitioning Algorithms

# In-depth explanation — how Kafka picks a partition (null key vs keyed records)

Below I walk through exactly what the producer does in each case, why Kafka switched from plain round-robin to the *sticky* approach, and the practical consequences (including the “partition unavailable” risk you mentioned).

---

## Short summary

* **No key (key == null):** the producer chooses a partition for you. Before Kafka 2.4 this was a simple round-robin; starting in 2.4 the default partitioner uses a *sticky* strategy: pick a random partition and keep sending (i.e., *stick*) records to that partition until the current batch is completed, then switch. This increases batch sizes and reduces requests.
* **Key present:** the producer hashes the key and uses that hash to pick a partition deterministically (so the same key always maps to the same partition). Kafka’s Java client uses Murmur2 for this hashing and computes `partition = positive(murmur2(keyBytes)) % numPartitions`. Importantly that modulo uses the total number of partitions for the topic (not only the currently *available* partitions).

---

## When the key is null — technical detail and why “sticky” helps

1. **Old behavior (pre-2.4):** the partitioner spread null-key records roughly evenly via round-robin across the *available* partitions. That produced small batches on many partitions because each successive message went to a different partition.
2. **Sticky partitioner (2.4+):** the partitioner chooses a partition at random and *sticks* to it while the producer accumulates a batch for that partition. Once the batch is sent (because the batch is full, or `linger.ms` timeout expired, or the producer flushes), the partitioner chooses another partition and repeats. The sticky approach preserves a roughly even distribution over time but produces larger batches per request—fewer requests, higher throughput, lower broker CPU/latency.

Practical knobs that interact with sticky behavior:

* `batch.size` — how large a batch the producer tries to fill before sending.
* `linger.ms` — how long the producer will wait to try to fill a batch.
  With sticky partitioning you will typically get fuller batches (and therefore fewer requests) compared with naive round-robin.

---

## When the key is present — hashing + deterministic mapping

* If your record has a key, the default partitioner uses a hash of the serialized key to pick the partition. In the Java client it computes something like:

```java
int partition = toPositive(Utils.murmur2(keyBytes)) % numPartitions;
```

`toPositive` makes the 32-bit hash non-negative; `numPartitions` is the total number of partitions for the topic. Because the hash + modulo uses the *total* partition count, the same key consistently maps to the same partition id. This guarantees ordering for a key (ordering is only guaranteed within a partition).

Two important consequences:

1. **Deterministic mapping across producers:** as long as all producers use the same hashing logic (Murmur2) and the same partition count, they will map the same key to the same partition — useful for consistency and joins/cogrouping. 
   
2. **If partitions change, mapping changes:** if you increase the number of partitions, `numPartitions` changes, so the modulo result changes and keys may map to different partitions afterwards. That’s why adding partitions is not transparent for key affinity.

---

## Why the “use all partitions (not just available)” matters — and the error possibility

* The key-hash path explicitly uses the *full* partition list size (`numPartitions`) to compute the index. It does **not** choose only among currently available partitions when computing the hash modulo. The code then attempts to send to the chosen partition. If that partition currently has no leader or is otherwise unavailable, the broker will reject the produce request (errors like `NotLeaderForPartitionException` / `LeaderNotAvailable` / `UnknownTopicOrPartition`) until metadata refresh and leader election resolve the issue. The producer usually retries (subject to your `retries` and `delivery.timeout.ms` settings), but you can see immediate errors while the cluster recovers.

So the short consequence: deterministic mapping is good for ordering and affinity, but it means the producer can attempt to write to a partition that is temporarily unavailable — causing retries or errors — because the mapping step did not exclude unavailable partitions.

---

## Code sketch (conceptual)

Null key (sticky behavior; simplified):

```text
if (key == null) {
  // choose a sticky partition for this topic (random the first time)
  // fill a batch (batch.size / linger.ms); send batch to that partition
  // when batch sent, pick a different random partition and repeat
}
```

Keyed:

```text
if (key != null) {
  partition = positive(murmur2(keyBytes)) % totalPartitions;  // totalPartitions = partitionsForTopic(topic).size()
  // send to that exact partition (may be unavailable => broker will reject until metadata refresh/leader elected)
}
```

---

## Practical advice (short checklist)

* Use **keys** when you need ordering or co-location of events for the same entity.
* If you don’t need per-key ordering and you care about raw throughput, null keys + sticky partitioner give larger batches and lower CPU/latency. 
* Ensure an adequate **replication factor** (≥2 or 3) so leader loss does not immediately make a partition unavailable. Monitor leader elections. 
* Tune `batch.size` and `linger.ms` to balance latency and batch fullness for sticky behavior. 
* If you need special routing (e.g., avoiding a subset of partitions), implement a custom `Partitioner`.

---


