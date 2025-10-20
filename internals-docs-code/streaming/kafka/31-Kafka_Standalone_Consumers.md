# Standalone Consumers : Consumer without a Group

## Core concepts

**Serializer/deserializer compatibility** (you already know this): consumers must be able to interpret the bytes written by producers. That means matching serializers/deserializers and—if you use a schema system like Avro + Schema Registry—matching schemas.

**Consumer groups and subscribe():**

* When consumers call `subscribe(topics, on_assign=...)`, they request membership in a **consumer group** identified by `group.id`.
* Kafka’s group coordinator assigns partitions of the subscribed topics among active group members. This assignment is automatic and rebalanced whenever group membership or subscription metadata changes.
* Rebalancing is useful when you want the cluster to adapt automatically to consumer joins/leaves or topic partition changes (scaling).
* With `subscribe`, consumers participate in heartbeating and session management. If a consumer fails or is slow, partitions are reassigned to other group members.
* You typically **commit offsets** (either automatically with `enable.auto.commit` or manually) and Kafka stores those offsets under the consumer group. On restart, a consumer in the same group resumes from committed offsets.

**Manual assignment and assign():**

* With `assign([TopicPartition(...)])` you bypass the group coordinator for assignment decisions — *the consumer will not join the consumer group for partition assignment purposes*. You explicitly tell the consumer which partitions to read.
* This is appropriate when you need deterministic, static reads: e.g., a single consumer that must read all partitions, a tool that reads a specific partition for replay, or a consumer that must concurrently read certain partitions for specialized processing.
* Assigning partitions gives you more control but removes automatic failover and rebalancing. If another process needs to take over, you must implement that orchestration yourself.
* Important: if you want to commit offsets to Kafka (so offsets are persisted in `__consumer_offsets`), you still need a `group.id` configured. Committing offsets without a group id is either impossible or meaningless for group-managed offsets. (Storing offsets externally is an alternative.)

**Key trade-offs**

* **Subscribe (group-managed)**: +automatic scaling and failover, easier maintenance; −possible rebalances which add pause time and complexity (rebalance listeners, offset commit timing).
* **Assign (manual)**: +deterministic control, no rebalances; −no automatic recovery, you must coordinate failover and partition ownership yourself.

**Common operational concerns**

* Rebalance latency: large processing during on-revoke/on-assign handlers can prolong rebalances. Keep handlers quick.
* Heartbeats and session timeouts: tune `session.timeout.ms`, `heartbeat.interval.ms` to avoid false consumer group failures or too slow failure detection.
* Offset commit semantics: commit after processing a message (or batch) to ensure at-least-once semantics; track transactions if you need exactly-once across systems.
* If you use manual assignment and commit offsets, ensure `group.id` is set and coordinate offset ownership (avoid two processes committing offsets for the same group/partition pair).

---

# Example 1 — Consumer group (subscribe) with manual offset commits

This consumer joins a group, is assigned partitions automatically, processes records, and commits offsets manually after successful processing.

```python
# consumer_subscribe.py
from confluent_kafka import Consumer, KafkaError, KafkaException
import signal
import sys
import time

TOPIC = 'my_topic'
GROUP_ID = 'my_consumer_group'
BOOTSTRAP_SERVERS = 'localhost:9092'

running = True

def shutdown(signum, frame):
    global running
    running = False

signal.signal(signal.SIGINT, shutdown)
signal.signal(signal.SIGTERM, shutdown)

conf = {
    'bootstrap.servers': BOOTSTRAP_SERVERS,
    'group.id': GROUP_ID,
    'auto.offset.reset': 'earliest',   # or 'latest'
    'enable.auto.commit': False,       # we'll commit manually
    'session.timeout.ms': 10000,
}

consumer = Consumer(conf)

def on_assign(consumer, partitions):
    print("Assigned partitions:", partitions)
    # Optionally seek to specific offsets here
    # for p in partitions:
    #     p.offset = OFFSET_TO_START
    # consumer.assign(partitions)

def on_revoke(consumer, partitions):
    print("Revoked partitions:", partitions)
    # Called before rebalance; flush state if needed

consumer.subscribe([TOPIC], on_assign=on_assign, on_revoke=on_revoke)

try:
    while running:
        msg = consumer.poll(timeout=1.0)
        if msg is None:
            continue
        if msg.error():
            # handle errors; ignore EOF for older clients if necessary
            print("Error:", msg.error())
            continue

        # Process message
        try:
            key = msg.key()
            value = msg.value()
            partition = msg.partition()
            offset = msg.offset()
            # business logic here
            print(f"Message at {partition}:{offset}, key={key}, len(value)={len(value) if value else 0}")

            # After successful processing, commit the offset for this message
            consumer.commit(message=msg, asynchronous=False)
            # For batch commits, you could gather and call consumer.commit()
        except Exception as e:
            # Handle processing exception; you can choose not to commit so message will be reprocessed
            print("Processing failed:", e)
finally:
    # Close will also try to commit offsets (if enabled) and leave the group cleanly.
    consumer.close()
    print("Consumer closed.")
```

Notes:

* Using `subscribe` means automatic assignment and rebalances. The callbacks `on_assign`/`on_revoke` let you respond to rebalances.
* `enable.auto.commit=False` gives you full control over when offsets are stored. This is common for at-least-once processing.
* In Example 1 (the consumer-group version), we didn’t explicitly define partitions — and that’s actually by design.
* “I want to consume messages from all partitions of this topic, but I don’t care which specific partitions I get — please assign them automatically as part of my consumer group.”

Contacts the group coordinator for the specified group.id.

The coordinator collects all active consumers in that group and all their subscribed topics.

It distributes (assigns) partitions among those consumers — this is called rebalancing.

The assignment result (which partitions this consumer should read) is passed to your on_assign() callback.

---

## Example 2 — Manual assignment (assign) reading specific partitions

This consumer explicitly assigns itself to partitions. It still has `group.id` so it can commit offsets to Kafka if desired.

```python
# consumer_assign.py
from confluent_kafka import Consumer, TopicPartition, KafkaError
import signal
import sys

TOPIC = 'my_topic'
PARTITIONS_TO_CONSUME = [0, 1]   # explicit partition numbers
BOOTSTRAP_SERVERS = 'localhost:9092'
GROUP_ID = 'manual_assign_group'  # still set if you want to commit offsets

running = True
def shutdown(signum, frame):
    global running
    running = False

signal.signal(signal.SIGINT, shutdown)
signal.signal(signal.SIGTERM, shutdown)

conf = {
    'bootstrap.servers': BOOTSTRAP_SERVERS,
    'group.id': GROUP_ID,
    'auto.offset.reset': 'earliest',
    'enable.auto.commit': False,    # commit manually
}

consumer = Consumer(conf)

# Build TopicPartition list and optionally set starting offsets
tps = [TopicPartition(TOPIC, p) for p in PARTITIONS_TO_CONSUME]

# Optionally set explicit offsets: e.g., start at offset 0 for partition 0
# tps = [TopicPartition(TOPIC, 0, 0), TopicPartition(TOPIC, 1, 10)]

consumer.assign(tps)
print(f"Manually assigned to partitions: {tps}")

try:
    while running:
        msg = consumer.poll(timeout=1.0)
        if msg is None:
            continue
        if msg.error():
            print("Error:", msg.error())
            continue

        try:
            print(f"Got message from partition {msg.partition()} offset {msg.offset()}")
            # process msg.value()

            # commit for the partition after processing
            consumer.commit(message=msg, asynchronous=False)
        except Exception as exc:
            print("Processing error:", exc)
finally:
    consumer.close()
    print("Consumer closed (manual assigned).")
```

Notes:

* `assign()` does not contact the group coordinator for assignment; the consumer will not be part of the group for rebalance purposes.
* Because you explicitly choose partitions, other consumers must avoid reading the same partitions simultaneously (unless you intentionally want multiple readers).
* If another client subscribes with the same `group.id`, Kafka will not automatically move your assigned partitions to that client. Coordination must be external.

---

## Practical recommendations

1. **Use `subscribe` (consumer groups) in normal consumer applications** where you want automatic scaling and resilience. Handle rebalances gracefully.
2. **Use `assign` for special cases** — replay tools, administrative utilities, or single-process readers that must own particular partitions.
3. **Set `group.id` if you intend to commit offsets to Kafka.** If you don’t need Kafka-managed commits, you can persist offsets elsewhere (a database, Redis, etc.) and omit `group.id`.
4. **Keep rebalance handlers quick.** Do not perform heavy processing in `on_revoke`/`on_assign`; instead flush metadata state quickly, then continue processing.
5. **Be deliberate about offset commit strategy** (after processing each message, after a batch, or using transactions). This determines your delivery semantics (at-most-once, at-least-once, or exactly-once with transactions).
6. **Monitor consumer liveness and lag.** Tools like consumer group lag metrics help detect slow consumers or sticky partitions.

---