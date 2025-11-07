# Using Consumers in Reliable System : Introduction

---

## 1. **Data availability to consumers**

Kafka follows a simple but strict rule for when data becomes visible to consumers:

> A record becomes available for consumption **only after it is committed to Kafka** — that is, when it has been successfully written to **all in-sync replicas (ISR).**

This means:

* Consumers only ever see **consistent data** — data that Kafka has replicated safely.
* Consumers will **never read uncommitted messages**, even if the producer sent them but the leader failed before replication completed.

So, the consumer always starts from a **consistent state** of the log.

---

## 2. **How consumers read messages**

Kafka’s log structure makes consumption straightforward and deterministic:

* Each partition is a **sequential append-only log**.
* Messages within a partition have an **increasing offset**, which uniquely identifies their position in the log.

When a consumer reads:

1. It requests messages starting from a specific offset.
2. The broker returns a batch of records in order.
3. The consumer notes the **last offset** it has read.
4. It requests the next batch starting from that offset + 1.

This ensures:

* **Ordering:** Consumers always read messages in the same order they were written.
* **No gaps:** Every message is fetched exactly once (assuming correct offset tracking).
* **High performance:** Sequential reads from disk (or page cache) are efficient.

---

## 3. **The problem of consumer restarts**

If a consumer crashes, stops, or is replaced (as part of a consumer group rebalance), the **next consumer** that takes over needs to know:

> “Where did the previous consumer leave off?”

Without this information, the new consumer could either:

* Start from the beginning (reprocessing already handled messages), or
* Start too far ahead (skipping unprocessed messages).

Both cases are problematic:

* **Duplicates**: Reprocessing already committed messages.
* **Data loss**: Skipping messages that were read but not processed yet.

Kafka solves this through **offset commits**.

---

## 4. **Offset commits: how consumers track progress**

The **offset** represents a consumer’s position in the log — effectively, a bookmark.

Each consumer group stores its offsets (per partition) to remember how far it has read.

Kafka provides two main mechanisms to **commit offsets**:

### a. **Automatic commits (`enable.auto.commit=true`)**

* The consumer automatically commits offsets at a fixed interval (default: 5 seconds).
* This is simple, but can lead to data loss if the consumer fails after reading but before processing messages.

Example problem:

1. The consumer polls records and auto-commits offset 1000.
2. It processes messages 990–1000.
3. It crashes after reading 1000 but before processing them.
4. The new consumer starts from offset 1000 (thinking those were processed).
5. Messages 990–1000 are **skipped** — lost to the system.

Automatic commits are convenient but unsafe for critical data.

---

### b. **Manual commits (`enable.auto.commit=false`)**

Here, the application explicitly commits offsets after it has fully processed the messages.

This gives fine-grained control and stronger reliability.

For example:

```java
ConsumerRecords<String, String> records = consumer.poll(Duration.ofMillis(100));
for (ConsumerRecord<String, String> record : records) {
    process(record);
}
consumer.commitSync();  // commit only after successful processing
```

Advantages:

* You only commit when processing is complete.
* If the consumer crashes before committing, the next one will reprocess the same records (ensuring no data loss).

Tradeoff:

* You might process some messages more than once after restarts (**at-least-once semantics**).

---

## 5. **Where offsets are stored**

Kafka stores committed offsets in a **special internal topic**:

```
__consumer_offsets
```

* Each consumer group’s offsets are stored as key–value pairs:

  * **Key:** (`group.id`, `topic`, `partition`)
  * **Value:** `offset`, `metadata`
* This topic is replicated like any other Kafka topic, so offset data is **fault-tolerant and durable**.
* When a consumer group restarts, it reads its last committed offsets from this topic and resumes from there.

This mechanism allows any consumer in the group — or a new one — to **continue exactly where the previous one left off**.

---

## 6. **Offset commit timing and message loss**

This is where consumer reliability can fail if not handled carefully.

Let’s consider the possible cases:

| Scenario                                                 | Commit Timing | Risk                                                   | Result                                         |
| -------------------------------------------------------- | ------------- | ------------------------------------------------------ | ---------------------------------------------- |
| Commit **before** processing                             | Early         | Consumer may crash after commit but before processing. | Message is lost (skipped by next consumer).    |
| Commit **after** processing                              | Late          | Consumer may crash after processing but before commit. | Message reprocessed after restart (duplicate). |
| Use transactions (Kafka Streams or producer-transaction) | Coordinated   | Offsets committed atomically with results.             | Exactly-once semantics.                        |

Thus:

* **At-least-once**: Commit after processing (safe from data loss, may reprocess).
* **At-most-once**: Commit before processing (no duplicates, may lose data).
* **Exactly-once**: Use Kafka transactions (coordinated commit).

---

## 7. **Kafka’s reliability guarantee for consumers**

Kafka’s design ensures that:

* Data is **never exposed** to consumers until fully committed to all in-sync replicas.
* Consumers **always read ordered, consistent data**.
* Reliability beyond that depends on **how the consumer manages offsets**.

So, Kafka provides **consistency** and **ordering** guarantees, but the **application developer controls delivery semantics** through offset handling strategy.

---

## 8. **Best practices for reliable consumption**

| Goal                            | Strategy                                                                            |
| ------------------------------- | ----------------------------------------------------------------------------------- |
| **Prevent data loss**           | Commit offsets only after successful processing.                                    |
| **Prevent duplicates**          | Use transactional producers and consumers for atomic processing.                    |
| **Recover from crashes safely** | Store offsets in Kafka (default) rather than external systems.                      |
| **Control offset management**   | Disable `enable.auto.commit` and use `commitSync()` or `commitAsync()` manually.    |
| **Scale out safely**            | Use **consumer groups** — Kafka partitions ownership and offset tracking per group. |

---

## 9. **Summary**

| Concept              | Description                                                           |
| -------------------- | --------------------------------------------------------------------- |
| **Committed data**   | Only data replicated to all in-sync replicas is visible to consumers. |
| **Offsets**          | Track a consumer’s read position in each partition.                   |
| **Offset commits**   | Save current progress so other consumers can resume after failure.    |
| **Automatic commit** | Convenient but can lose messages on crash.                            |
| **Manual commit**    | Safer; ensures at-least-once delivery.                                |
| **Offset storage**   | Persisted in Kafka’s `__consumer_offsets` topic for durability.       |
| **Main risk**        | Committing offsets too early → message loss.                          |

---

### In summary:

Kafka guarantees **data consistency and ordering** for consumers, but **delivery reliability** (no loss or duplicates) depends entirely on **how you manage offsets**.
If offsets are committed *after* successful processing, you get **at-least-once** semantics.
If you need **exactly-once**, you must use **Kafka transactions** so that message processing and offset commits happen atomically.
