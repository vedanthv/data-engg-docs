## Types of Commits in Consumers

### Automatic Commits

By default, Kafka automatically commits offsets every **five seconds** (controlled by **`auto.commit.interval.ms`**).
This means that every time the consumer calls **`poll()`**, Kafka checks whether it’s time to commit. If it is, it commits the **latest offset** that was returned in the last **`poll()`** call.

Here’s what this means in practice:

* When auto-commit is enabled, Kafka automatically keeps track of which records your consumer has read.
* If the consumer crashes **three seconds after the last commit**, when it restarts or another consumer takes over, it will begin reading from the **last committed offset**—three seconds old.
* As a result, all messages read during those three seconds will be **processed again** (duplicate processing).
* You can reduce this duplication window by committing more frequently, but you **can’t eliminate duplicates entirely**.

A key point is that **Kafka commits offsets for messages returned by the last `poll()`**, not for messages that were actually processed.
So if you call **`poll()`** again before processing all previous messages, or if an exception causes you to exit before processing them, some offsets may be committed even though the messages were not handled — leading to **data loss**.

Also note:

* When **`close()`** is called, it automatically commits offsets as well.
* Automatic commits are convenient for simple use cases but **don’t give enough control** for systems that must avoid duplicates or data loss.

In summary:

* Auto-commit = convenient, but risk of duplicates or unprocessed messages.
* Manual commit = more control, better for reliable or exactly-once processing.

### Commit Current Offset

---

#### 1. Why Manual Offset Control Is Needed

By default, Kafka commits offsets automatically at regular intervals:

```properties
enable.auto.commit=true
auto.commit.interval.ms=5000
```

This means the consumer commits offsets every 5 seconds, regardless of whether your application has finished processing those messages.
This behavior can cause two major problems:

* **Duplicate processing**: If the consumer crashes before the next commit, it reprocesses the same messages after restart.
* **Data loss**: If offsets are committed before processing completes, some messages may never be processed.

To gain control over when offsets are committed and to avoid these issues, developers usually disable automatic commits.

---

#### 2. Disabling Automatic Commits

To switch to manual commits, you set:

```properties
enable.auto.commit=false
```

This means Kafka will only commit offsets when your application explicitly tells it to.
You can then commit offsets using one of two APIs:

1. `commitSync()` — Synchronous, reliable, blocking commit.
2. `commitAsync()` — Asynchronous, faster, but less reliable.

---

#### 3. How `commitSync()` Works

`commitSync()` is the simplest and most reliable method for manually committing offsets.

Example:

```java
while (true) {
    ConsumerRecords<String, String> records = consumer.poll(Duration.ofMillis(100));

    for (ConsumerRecord<String, String> record : records) {
        process(record); // your message processing logic
    }

    consumer.commitSync(); // commits after processing
}
```

#### Internal Behavior:

* Kafka keeps track of the latest offset processed for each partition.
* When you call `commitSync()`, the consumer sends a `CommitOffsetRequest` to the broker.
* The broker writes the committed offsets to a special internal topic called `__consumer_offsets`.
* The API blocks until Kafka confirms that the offsets have been successfully stored.

If the commit fails due to a network issue or coordinator error, `commitSync()` throws an exception, allowing you to handle it or retry.

---

### 4. Where Offsets Are Stored

Committed offsets are stored in Kafka’s internal topic named:

```
__consumer_offsets
```

This topic holds records that map:

* Consumer group ID
* Topic-partition
* Committed offset
* Commit timestamp

When a consumer restarts or a rebalance occurs, it reads its committed offsets from this topic and resumes consumption from the last committed position.

---

### 5. Important Semantics of `commitSync()`

`commitSync()` always commits the **latest offsets returned by the most recent `poll()`**.

Therefore:

* If you call `commitSync()` **before** finishing processing the batch, you risk losing messages (Kafka assumes they’re processed even if they aren’t).
* If you call `commitSync()` **after** processing all messages, you may reprocess some in the event of a crash before commit, but no messages will be lost.

This leads to an important trade-off:

| Strategy                 | Behavior               | Risk               |
| ------------------------ | ---------------------- | ------------------ |
| Commit before processing | May lose messages      | Unsafe             |
| Commit after processing  | May duplicate messages | Safe and preferred |

---

#### 6. Trade-offs in Commit Timing

##### Option 1: Commit after each batch

* Reliable, easy to implement
* Slight performance overhead due to blocking commit call
* Recommended for most use cases

##### Option 2: Commit after each message

* Maximum control, minimal data loss
* Very slow because every commit is a network operation

##### Option 3: Commit periodically or based on count

* Balanced approach between performance and accuracy

Example:

```java
int processedCount = 0;

while (true) {
    ConsumerRecords<String, String> records = consumer.poll(Duration.ofMillis(100));
    for (ConsumerRecord<String, String> record : records) {
        process(record);
        processedCount++;
    }

    if (processedCount >= 1000) {
        consumer.commitSync();
        processedCount = 0;
    }
}
```

---

### 7. Failure Scenarios

| Scenario                                                     | Result                            | Impact          |
| ------------------------------------------------------------ | --------------------------------- | --------------- |
| Consumer crashes before commit                               | Reprocesses the last batch        | Duplicates      |
| Consumer crashes after commit but before processing finishes | Messages skipped                  | Data loss       |
| Network failure during commit                                | Commit fails and throws exception | Handle or retry |
| Rebalance during processing                                  | Uncommitted data reprocessed      | Duplicates      |

---

### 8. Handling Rebalances Safely

During a rebalance, Kafka reassigns partitions between consumers.
If you lose ownership of a partition without committing, another consumer may reprocess uncommitted records.

To handle this safely, use a `ConsumerRebalanceListener` and commit offsets in `onPartitionsRevoked()`:

```java
consumer.subscribe(Collections.singletonList("topic"), new ConsumerRebalanceListener() {
    @Override
    public void onPartitionsRevoked(Collection<TopicPartition> partitions) {
        consumer.commitSync(currentOffsets); // commit before losing partitions
    }

    @Override
    public void onPartitionsAssigned(Collection<TopicPartition> partitions) {
        // initialization logic if needed
    }
});
```

This ensures all processed offsets are committed before partition ownership changes.

---

### 9. Best Practices for Using `commitSync()`

1. **Disable auto-commit**

   ```properties
   enable.auto.commit=false
   ```
2. **Commit only after successful processing**
   This ensures no data loss.
3. **Use try-catch around commits**
   Handle transient errors gracefully.
4. **Commit on rebalance**
   Prevents duplication after group reassignments.
5. **Combine with `commitAsync()` for performance**
   Use async commits during normal operation and a final sync commit during shutdown.
6. **Make message processing idempotent**
   Ensure reprocessing the same message does not cause incorrect results (for example, using upserts or deduplication keys).

---

### 10. Combined Commit Strategy Example

A common production pattern is to combine `commitAsync()` and `commitSync()`:

```java
try {
    while (running) {
        ConsumerRecords<String, String> records = consumer.poll(Duration.ofMillis(100));
        for (ConsumerRecord<String, String> record : records) {
            process(record);
        }

        consumer.commitAsync(); // fast, non-blocking commit
    }
} catch (Exception e) {
    // handle error or retry logic
} finally {
    try {
        consumer.commitSync(); // final blocking commit for safety
    } finally {
        consumer.close();
    }
}
```

This pattern achieves a balance of:

* High performance during normal operation (asynchronous commits)
* Reliability during shutdown or rebalance (synchronous commit)

---

## 11. Summary

| Feature      | Auto Commit      | Manual Commit (`commitSync()`) |
| ------------ | ---------------- | ------------------------------ |
| Control      | Low              | High                           |
| Data Safety  | Medium           | High                           |
| Duplicates   | Possible         | Possible but manageable        |
| Data Loss    | Possible         | Avoidable                      |
| Commit Type  | Timed            | Developer-controlled           |
| Suitable For | Simple consumers | Production-grade consumers     |

---

In summary, disabling auto-commit and using `commitSync()` after processing each batch gives you strong guarantees against data loss and predictable behavior. While it introduces a bit more complexity and latency, it is the most reliable way to manage consumer offsets in production systems.

### Asynchronous Commit

Below is a detailed, emoji-free explanation of the asynchronous commit API (`commitAsync()`), its behavior, trade-offs, error-handling patterns, and practical recommendations for production use.

---

## What `commitAsync()` does

`commitAsync()` sends the commit request to the broker and does **not block** waiting for a response. This improves throughput because the consumer thread can continue processing records while offset commits are in flight.

There are two common forms:

1. `consumer.commitAsync();`
   Sends the offsets the consumer is tracking (the latest offsets returned by the last `poll()`).

2. `consumer.commitAsync(Map<TopicPartition, OffsetAndMetadata> offsets, OffsetCommitCallback callback);`
   Sends a specific set of offsets and supplies a callback that Kafka will call when the broker responds (success or error).

---

## Benefits

* Higher throughput because commits are non-blocking.
* Lower latency in the consumer loop; the consumer does not wait for commit round-trip.
* Useful for high-volume consumers where commit latency would otherwise throttle processing.

---

## Drawbacks and important caveats

1. **No built-in retry or blocking guarantee**
   If a commit fails (network error, coordinator error), `commitAsync()` will report the error in the callback but it will not retry automatically. If you need guaranteed persistence, you must handle retries yourself or use `commitSync()` at critical points.

2. **Out-of-order callback completion**
   If you call `commitAsync()` multiple times in rapid succession, callbacks can complete out-of-order. That means a later commit might succeed first and an earlier commit might fail afterward; if you react to failures by retrying, be careful not to regress to an earlier offset.

3. **Potential for lost commit acknowledgement**
   Because you don't block, the application may crash before the broker processes the commit. That is why a final `commitSync()` on shutdown is recommended.

4. **Rebalance handling**
   Commits in-flight during a rebalance may be lost or applied after partition reassignment. Use a rebalance listener to commit offsets synchronously in `onPartitionsRevoked()` to make sure processed offsets are stored before losing partition ownership.

---

## Typical usage patterns

### 1) Fast path with async commits, safe shutdown with sync commit

This is a common production pattern: use `commitAsync()` for normal throughput and call `commitSync()` in `finally` to guarantee the last offsets are committed.

```java
try {
    while (running) {
        ConsumerRecords<String, String> records = consumer.poll(Duration.ofMillis(100));
        for (ConsumerRecord<String, String> record : records) {
            process(record);
        }
        consumer.commitAsync(); // non-blocking
    }
} catch (Exception e) {
    // log or handle processing error
} finally {
    try {
        consumer.commitSync(); // final, blocking commit to ensure offsets are stored
    } finally {
        consumer.close();
    }
}
```

Rationale: `commitAsync()` gives throughput; the final `commitSync()` ensures the offsets you last processed are persisted before exit.

---

### 2) Async commit with callback to log/fallback retry

Use a callback to detect commit failures and optionally retry or record telemetry. Avoid blind retries that might create ordering problems.

```java
consumer.commitAsync((offsets, exception) -> {
    if (exception != null) {
        // handle failure: log, increment metric, or schedule a retry
        System.err.printf("Commit failed for offsets %s: %s%n", offsets, exception.getMessage());
        // Optionally: retry once using commitSync() or a bounded retry mechanism
    }
});
```

If you attempt retries, prefer `commitSync()` for the retry attempt (or a bounded number of async retries with careful ordering control).

---

### 3) Commit specific offsets (application-managed offsets)

If your application uses its own tracking (for example, when using manual per-message acknowledgements or when integrating with external storage), pass explicit offsets:

```java
Map<TopicPartition, OffsetAndMetadata> offsets = new HashMap<>();
offsets.put(partition, new OffsetAndMetadata(offsetToCommit, "metadata"));

consumer.commitAsync(offsets, (map, ex) -> {
    if (ex != null) {
        // handle failure
    }
});
```

Note: commit the offset **of the next message to process** (i.e., last-processed-offset + 1) to avoid reprocessing the same message on restart.

---

## Rebalance integration

Always commit offsets in `onPartitionsRevoked()` using a synchronous commit. This prevents losing processed offsets when partitions are taken away.

```java
consumer.subscribe(topics, new ConsumerRebalanceListener() {
    @Override
    public void onPartitionsRevoked(Collection<TopicPartition> partitions) {
        // commit the offsets you have recorded for these partitions
        consumer.commitSync(currentOffsets);
    }

    @Override
    public void onPartitionsAssigned(Collection<TopicPartition> partitions) {
        // restore offsets if needed
    }
});
```

Rationale: `onPartitionsRevoked()` is called before the consumer loses ownership. Synchronous commit here guarantees offsets are recorded before the rebalance completes.

---

## Error handling recommendations

* Wrap commits in try/catch when using `commitSync()` and react to `CommitFailedException` or transient errors.
* For `commitAsync()` callbacks:

  * Log failures and metrics.
  * Consider a bounded retry using `commitSync()` when appropriate (for example, in the callback of a failed commit you might attempt one `commitSync()` to ensure persistence).
  * Avoid infinite retry loops or retries that block the main processing thread, which would defeat the purpose of async commits.
* On shutdown, always call `commitSync()` in a `finally` block to ensure the last offsets are committed.

---

## Throughput vs duplicate-window trade-off

* Committing less frequently increases throughput but widens the window for potential duplicate processing after a rebalance or crash.
* Committing more frequently reduces duplicates but increases commit overhead and may reduce throughput.
* Use application-specific metrics and load tests to determine the right commit frequency. Common rules:

  * Commit every N messages (e.g., 500–10,000) for high-throughput consumers.
  * Or commit every T seconds (e.g., 5–60s) depending on acceptable duplicate window and latency requirements.
  * Combine async commits for performance with periodic sync commits for safety if you require stronger guarantees.

---

## Idempotence and external side effects

Because duplicates are possible even with careful commits, design your processing to be idempotent or to tolerate retries:

* Use upserts instead of inserts where possible.
* Deduplicate using a unique message ID stored in a database/cache.
* Make downstream systems tolerant to repeated messages.

---

## When to prefer `commitAsync()` vs `commitSync()`

* `commitAsync()`:

  * Preferred for steady-state, high-throughput processing.
  * Use with robust monitoring and a final `commitSync()` on shutdown.
  * Use callbacks to observe failures and increment metrics.

* `commitSync()`:

  * Preferred when you need a strong guarantee that offsets were committed at a specific point (e.g., before releasing partitions, during controlled shutdown, or after critical state updates).
  * Use in `onPartitionsRevoked()` and at application exit.

Combining both (`commitAsync()` normally, `commitSync()` on rebalance/shutdown) yields a practical and commonly used balance between performance and safety.

---

## Other considerations

* **Offset metadata:** You can attach small metadata strings to commits (for debugging or bookkeeping).
* **Consumer group scale:** With many consumers, commit frequency affects the `__consumer_offsets` topic size and broker load. Monitor cluster health.
* **Transactions / exactly-once:** If you need strong exactly-once semantics across producers and consumers, consider Kafka transactions (producer-side) or higher-level frameworks (Kafka Streams). Those are separate mechanisms beyond simple consumer offset commits.

---

## Short checklist for production consumers

1. Disable auto-commit: `enable.auto.commit=false`.
2. Use `commitAsync()` during normal processing for throughput.
3. Use a callback to observe commit failures and record metrics.
4. Commit synchronously in `onPartitionsRevoked()` and in `finally` on shutdown.
5. Keep processing idempotent or implement deduplication.
6. Tune commit frequency based on acceptable duplicate window and throughput goals.
7. Monitor `__consumer_offsets` topic, commit latency, and commit failure rates.

---