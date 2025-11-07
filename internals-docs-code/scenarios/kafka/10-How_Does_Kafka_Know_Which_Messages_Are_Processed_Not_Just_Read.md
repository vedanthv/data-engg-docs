# How does Kafka Know Which Messages are Processed, not just read?

Excellent — this question gets to the **core of how Kafka tracks message progress** and why the line

> “Kafka doesn’t know what you’ve processed — only what you’ve read and committed”
> is one of the most important truths for any Kafka developer to understand.

Let’s unpack this carefully.

---

## 🔹 1. Kafka **does not** inherently know whether a consumer “processed” a message

Kafka itself is **completely unaware** of what happens to a message **after** it is fetched by a consumer.

Here’s what Kafka does track:

* Which consumer groups exist (`group.id`)
* Which partitions each consumer owns
* The **last committed offset** per consumer group and partition

Kafka does **not** track:

* Whether the consumer application finished processing a record
* Whether it wrote results to a database, API, or data warehouse
* Whether processing succeeded or failed

From Kafka’s perspective, **“processing”** simply means **“offset committed.”**

---

## 🔹 2. What Kafka actually sees during consumption

Let’s visualize what happens in a consumer loop:

```java
ConsumerRecords<String, String> records = consumer.poll(Duration.ofMillis(100));

for (ConsumerRecord<String, String> record : records) {
    process(record);  // your business logic
}

consumer.commitSync();  // tell Kafka “I’ve processed up to this offset”
```

Internally, Kafka only sees two key actions:

1. The **poll()** call — consumer fetches messages from a partition (e.g., offsets 100–110)
2. The **commitSync()** call — consumer tells Kafka “I’m done up to offset X”

That commit updates the **offset checkpoint** for the consumer group in Kafka’s internal topic:

```
__consumer_offsets
```

So the broker stores, for example:

```
(group.id = order_service, topic = orders, partition = 0) → offset = 110
```

When another consumer in that group starts, it resumes from **offset 110** (next message is 111).

Kafka never verifies if messages 100–110 were really processed — it trusts the consumer to commit correctly.

---

## 🔹 3. Why this distinction matters: “read” vs. “processed”

* **Read messages:** messages returned by `poll()` — fetched from Kafka, but not necessarily processed.
* **Processed messages:** messages that your application has completed handling — e.g., written to a DB, sent to an API, enriched, etc.

If you **commit too early** — i.e., before your app has finished processing — then on a crash, Kafka assumes you already handled those messages.

Result: **data loss** (messages are skipped and never reprocessed).

If you **commit too late** — i.e., after a large batch — then a crash may cause Kafka to replay already-processed messages.

Result: **duplicates** (messages reprocessed).

---

## 🔹 4. Example: committing offsets incorrectly inside the poll loop

Imagine this common mistake:

```java
while (true) {
    ConsumerRecords<String, String> records = consumer.poll(Duration.ofMillis(100));
    consumer.commitSync(); // ❌ wrong place!
    for (ConsumerRecord<String, String> record : records) {
        process(record);
    }
}
```

What happens:

1. Consumer polls messages 100–110.
2. Immediately commits offset 110 (before processing).
3. Then processes only records 100–105.
4. Crashes.

Now, Kafka thinks this consumer has processed up to offset 110.
When it restarts, it resumes at offset 111 — skipping messages 106–110 entirely.

→ **Five messages lost forever.**

Kafka didn’t “know” they weren’t processed — it only saw the offset commit.

---

## 🔹 5. Correct approach: commit *after* processing

Instead, the offset commit should happen **after successful processing**:

```java
while (true) {
    ConsumerRecords<String, String> records = consumer.poll(Duration.ofMillis(100));
    for (ConsumerRecord<String, String> record : records) {
        process(record);
        consumer.commitSync(Collections.singletonMap(
            new TopicPartition(record.topic(), record.partition()),
            new OffsetAndMetadata(record.offset() + 1)
        ));
    }
}
```

Now, you’re committing **offset + 1** only after you’ve successfully processed that record.

This ensures:

* If you crash mid-processing → unprocessed messages will be retried (at-least-once).
* No message is skipped.

---

## 🔹 6. How Kafka stores and uses committed offsets

Offsets are stored in Kafka’s **internal topic**:

```
__consumer_offsets
```

Each commit writes a key-value pair:

| Key                                | Value                 |
| ---------------------------------- | --------------------- |
| (`group.id`, `topic`, `partition`) | `offset` + `metadata` |

This topic is compacted (old offset commits are deleted, only the latest remains).
When a consumer group restarts or rebalances, it reads these committed offsets and resumes consumption from there.

So the **only signal** Kafka uses to decide what’s been processed is:

> the latest committed offset.

---

## 🔹 7. How to safely ensure correct processing + committing

### Option 1: **Manual commits (recommended)**

Commit offsets manually *after* processing to achieve **at-least-once** semantics:

```java
enable.auto.commit=false
```

Then commit using `commitSync()` or `commitAsync()` after successful processing.

---

### Option 2: **Transactional (exactly-once) processing**

For critical systems where duplicates are not acceptable (e.g., financial trades), use **Kafka transactions**.

In this mode, producers and consumers coordinate atomic writes:

* The producer writes output messages **and commits offsets** as one transaction.
* If the transaction succeeds → offsets are committed.
* If it fails → offsets aren’t committed (messages are retried).

This is configured using:

```properties
enable.idempotence=true
transactional.id=unique-producer-id
isolation.level=read_committed
```

Kafka then guarantees:

> Messages are processed **exactly once**, even across retries or restarts.

---

## 🔹 8. Analogy — “Kafka is a delivery log, not a ledger of completion”

Think of Kafka as a **courier service**:

* It logs every package delivered to your door (messages fetched).
* But it doesn’t know whether you opened the package or used what’s inside (message processed).

You, the consumer, must tell Kafka:

> “I’ve successfully unpacked everything up to here.” (commit offset)

If you confirm before opening — you risk losing packages.
If you delay too long — you may re-open old packages.
Kafka’s job ends once the package is delivered — it’s your responsibility to acknowledge **only after successful handling**.

---

## 🔹 9. Summary

| Concept            | Kafka Knows? | Tracked How?                                   |
| ------------------ | ------------ | ---------------------------------------------- |
| Message fetched    | ✅ Yes        | Through the `poll()` request                   |
| Message processed  | ❌ No         | Only your application knows                    |
| Message committed  | ✅ Yes        | Through offset commits to `__consumer_offsets` |
| Offset position    | ✅ Yes        | Latest committed offset per group-partition    |
| Processing success | ❌ No         | Must be implied by commit timing               |

---

### 🔸 Final takeaway:

Kafka only knows what you **committed**, not what you **processed**.
It’s up to your application logic to **commit offsets only after successful processing** — this is the foundation of reliable Kafka consumption.
