# Consumer Properties in Kafka Part II

---

## 1. **`enable.auto.commit`: Automatic vs. manual offset commits**

This configuration defines **how Kafka commits consumer offsets** — automatically (on a timer) or manually (controlled by your application logic).

### 📘 What it does:

Each Kafka consumer keeps track of its **current position (offset)** in every partition it reads.
When it commits an offset, it is telling Kafka:

> “I have successfully processed messages up to this point.”

Kafka stores that offset in the internal topic `__consumer_offsets`.

The key question is: *Who decides when to commit?*

---

### a. **If `enable.auto.commit=true` (default)**

Kafka automatically commits offsets for you at fixed intervals.

#### How it works:

* The consumer commits offsets in the background every `auto.commit.interval.ms` (default: 5000 ms = 5 seconds).
* The offset committed is the **last message returned by `poll()`**, regardless of whether the application has fully processed it.

#### Example:

Let’s say your consumer:

1. Calls `poll()`, gets records up to offset **1000**.
2. Starts processing them.
3. Kafka automatically commits offset **1000** after 5 seconds.
4. The consumer crashes before processing the last 10 messages.

When it restarts, Kafka sees the last committed offset as **1000**, so it resumes from **1001** — skipping messages **991–1000**, which were read but not processed.

✅ Advantage:

* Simple setup — no need to manually track offsets.
* Works fine for lightweight, synchronous processing loops (read → process → repeat).

❌ Disadvantages:

* **Possible message loss** if the app crashes before processing committed messages.
* **No control** over when or how commits occur.
* **Not suitable for asynchronous or multi-threaded processing**, where message acknowledgment happens out of band.

---

### b. **If `enable.auto.commit=false` (manual commits)**

You control exactly when offsets are committed — typically after processing each batch successfully.

#### Example (Java):

```java
while (true) {
    ConsumerRecords<String, String> records = consumer.poll(Duration.ofMillis(100));
    for (ConsumerRecord<String, String> record : records) {
        process(record);  // custom logic
    }
    consumer.commitSync();  // commit offsets manually
}
```

✅ Advantages:

* **No data loss** — you commit offsets *only after* processing.
* **Full control** over commit timing and granularity.
* Essential for **multi-threaded** or **asynchronous** consumers.

❌ Disadvantages:

* Slightly more complex logic.
* If the app crashes after processing but before committing, **duplicates** can occur (messages reprocessed after restart).

---

### Summary: Choosing between auto and manual commit

| Setting                    | Behavior                                         | Risk                                     | Suitable For                  |
| -------------------------- | ------------------------------------------------ | ---------------------------------------- | ----------------------------- |
| `enable.auto.commit=true`  | Kafka commits offsets periodically in background | May lose messages if crash before commit | Simple, synchronous consumers |
| `enable.auto.commit=false` | App commits offsets manually                     | May reprocess messages (duplicates)      | Reliable or async consumers   |

In most **production-grade, fault-tolerant** systems, developers prefer **manual commits** for better control and data safety.

---

## 2. **`auto.commit.interval.ms`: Frequency of automatic commits**

This setting only applies when `enable.auto.commit=true`.

### What it does:

It defines **how frequently Kafka automatically commits offsets**.

Default:

```properties
auto.commit.interval.ms=5000
```

That means every 5 seconds, the consumer commits the latest offset of messages it has *read* (not necessarily processed).

---

### Tradeoff: Frequency vs. reliability

| Commit Interval                     | Effect                  | Implication                                                           |
| ----------------------------------- | ----------------------- | --------------------------------------------------------------------- |
| **Shorter interval (e.g., 1000ms)** | Commits more frequently | Fewer duplicates if crash (less data reprocessed), but more overhead. |
| **Longer interval (e.g., 10000ms)** | Commits less frequently | Less overhead, but more messages may be reprocessed after restart.    |

You can think of it as a **checkpoint interval**:

* Shorter intervals = safer, but more network + I/O load.
* Longer intervals = lighter, but more risk of reprocessing.

---

### Important subtlety:

Automatic commits happen **after every `poll()`**, but the consumer must keep polling regularly.
If your consumer stops polling for longer than the session timeout (due to slow processing or blocking logic), Kafka considers it **dead**, triggers a **rebalance**, and may assign its partitions to another consumer.

That’s why tuning commit intervals should go hand-in-hand with:

* `max.poll.interval.ms` (maximum time between polls),
* `session.timeout.ms` (heartbeat timeout), and
* `max.poll.records` (batch size).

---

## 3. **Why automatic commits can cause hidden reliability issues**

Even though automatic commits seem convenient, they often introduce subtle reliability bugs:

### Example scenario:

1. `poll()` returns 100 records.
2. Auto-commit interval = 5 seconds.
3. Consumer processes first 50 records (takes 10 seconds total).
4. After 5 seconds, Kafka auto-commits offset 100 (even though only half processed).
5. Consumer crashes after processing record 50.
6. On restart → Kafka resumes from offset 101 → records 51–100 are **lost forever**.

This happens because Kafka **commits what was fetched**, not what was processed.

Thus, for real systems with:

* Threaded processing,
* Asynchronous pipelines, or
* External side effects (e.g., database writes, REST calls),

automatic commits are almost always **too risky**.

---

## 4. **Rebalancing: another reliability consideration**

Even though not a configuration itself, the passage hints at a related factor:

> “It is difficult to consider a consumer reliable if it frequently stops consuming in order to rebalance.”

### Why this matters:

* When rebalancing occurs (e.g., due to a crash, a new consumer joining, or heartbeat timeout), partitions get reassigned.
* Frequent rebalances interrupt message processing and can cause **offset commit timing issues** (if a consumer stops before committing).
* To minimize rebalances:

  * Keep `session.timeout.ms` and `max.poll.interval.ms` tuned appropriately.
  * Avoid long blocking operations inside your poll loop.
  * Commit offsets frequently and reliably.
  * Use **incremental cooperative rebalancing** (via `partition.assignment.strategy=CooperativeStickyAssignor`).

---

## 5. **Summary: Consumer reliability settings**

| Config                    | Purpose                                     | Recommended for Reliability               |
| ------------------------- | ------------------------------------------- | ----------------------------------------- |
| `enable.auto.commit`      | Whether offsets are committed automatically | `false` (manual commits preferred)        |
| `auto.commit.interval.ms` | Frequency of auto commits                   | Use only if `enable.auto.commit=true`     |
| `max.poll.interval.ms`    | Max time between polls before rebalance     | Set based on processing time              |
| `session.timeout.ms`      | Time before consumer considered dead        | Tune to balance sensitivity and stability |
| `group.id`                | Defines group membership                    | Each service type uses its own ID         |
| `auto.offset.reset`       | Defines where to start if no offsets        | `earliest` for safety                     |

---

## 6. **Best-practice patterns**

### ✅ For **simple** synchronous consumers:

```properties
enable.auto.commit=true
auto.commit.interval.ms=3000
```

Safe if processing is short and done inline with `poll()`.

### ✅ For **reliable** or **asynchronous** consumers:

```properties
enable.auto.commit=false
```

Manually commit offsets *after* successful processing.

### ✅ For **exactly-once pipelines**:

Use transactional producers + `read_committed` isolation:

```properties
enable.auto.commit=false
isolation.level=read_committed
```

and commit offsets as part of the producer transaction.

---

### In summary:

* `enable.auto.commit` controls **who manages offset commits** — Kafka (automatic) or you (manual).
* `auto.commit.interval.ms` controls **how frequently** automatic commits occur.
* Automatic commits are convenient but can lead to **message loss** if the app crashes between polling and processing.
* Manual commits provide **better control and reliability**, especially in asynchronous or stateful systems.
* Reducing frequent **rebalances** (by tuning session intervals and avoiding slow polling) is essential for a truly reliable consumer.
