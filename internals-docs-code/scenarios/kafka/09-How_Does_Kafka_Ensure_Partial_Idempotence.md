# How does Kafka Ensure Partial Idempotence?

---

## 1. **The problem it solves — duplicate messages during retries**

Without idempotence, a Kafka producer can **accidentally send the same message multiple times** under certain failure conditions.

Here’s a common scenario:

1. The producer sends a batch to the broker.
2. The broker successfully writes it to the log.
3. The acknowledgment from the broker to the producer is **lost** (e.g., due to a network glitch).
4. The producer assumes the send failed and **retries** the message.
5. The broker accepts the retry as a new message and writes it again.

Result:
The **same message is stored twice**, with two different offsets.
Consumers downstream will see the record twice, which can cause problems in financial systems, metrics aggregation, and any system requiring strict consistency.

That’s where **idempotence** comes in.

---

## 2. **What idempotence means**

The term *idempotent* means that performing the same operation multiple times yields the same result as performing it once.

In Kafka:

> Enabling idempotence ensures that **even if a producer retries the same message**, the broker will only commit it **once**, never creating duplicates.

So, no matter how many times the producer resends due to transient failures, the broker will **de-duplicate** it automatically.

---

## 3. **How it works internally**

When `enable.idempotence=true`, Kafka activates the **Idempotent Producer Protocol**, introduced in Kafka **0.11.0**.

Here’s what happens under the hood:

### Step 1: Assigning a unique Producer ID (PID)

* When a producer connects to the cluster, the **Kafka broker assigns it a unique 64-bit Producer ID** (PID).
* This PID identifies that producer session.

### Step 2: Sequence numbers per partition

* Each time the producer sends a batch to a partition, it includes a **monotonically increasing sequence number** for that partition.
* Example:

  * Partition 0 → sequence numbers 1, 2, 3, ...
  * Partition 1 → sequence numbers 1, 2, 3, ... (separate sequence per partition)

### Step 3: Deduplication on the broker

* When the broker receives a batch, it checks:

  1. The **Producer ID**
  2. The **sequence number**
* If it has already seen that sequence number from the same producer, it recognizes the message as a duplicate and discards it.

This means that if the producer retries the same batch (after a timeout, network error, or leader election), Kafka guarantees **exactly one write** to the topic log.

---

## 4. **Key configuration interactions**

When `enable.idempotence=true`, Kafka automatically adjusts certain other producer parameters to safe defaults:

| Setting                                 | Automatically adjusted value | Purpose                                                               |
| --------------------------------------- | ---------------------------- | --------------------------------------------------------------------- |
| `acks`                                  | `all`                        | Waits for acknowledgment from all in-sync replicas.                   |
| `retries`                               | `Integer.MAX_VALUE`          | Retries indefinitely until success or timeout.                        |
| `max.in.flight.requests.per.connection` | ≤ 5                          | Limits concurrent in-flight requests to maintain ordering guarantees. |

If you set conflicting configurations manually (for example, `acks=1` with idempotence), Kafka will override them or throw a configuration error.

---

## 5. **What idempotence guarantees (and what it doesn’t)**

| Property                                           | Guarantee with `enable.idempotence=true`                     |
| -------------------------------------------------- | ------------------------------------------------------------ |
| **No duplicates (producer → broker)**              | ✅ Guaranteed (no matter how many retries occur).             |
| **Preserved ordering per partition**               | ✅ Guaranteed, as sequence numbers track per-partition order. |
| **Exactly-once delivery across retries**           | ✅ Achieved within a single producer session.                 |
| **Durability across producer restarts**            | ❌ Not guaranteed (new PID assigned on restart).              |
| **Transactions across multiple partitions/topics** | ❌ Not guaranteed (use transactions for that).                |

In other words:

* **Idempotence = Exactly-once per producer session per partition.**
* **Transactions = Exactly-once across sessions and partitions.**

---

## 6. **Limitations**

While `enable.idempotence=true` is powerful, it has scope boundaries:

1. **PID is lost when the producer restarts.**
   After a restart, a new PID is generated, and the sequence numbers reset.
   The broker treats the new producer as distinct — so it can’t deduplicate messages across sessions.

2. **Only applies per partition.**
   Kafka ensures ordering and deduplication independently for each partition, not across multiple partitions.

3. **Consumer-side duplication still possible** if the consumer reprocesses messages without proper offset management (for example, after failure or replay).

For complete exactly-once semantics across multiple topics and sessions, you need **transactional producers** (`initTransactions()` / `commitTransaction()`).

---

## 7. **Example timeline**

| Event                    | Without idempotence                | With idempotence                            |
| ------------------------ | ---------------------------------- | ------------------------------------------- |
| Producer sends record R1 | Broker writes R1                   | Broker writes R1                            |
| Acknowledgment lost      | Producer retries R1                | Producer retries R1                         |
| Broker receives retry    | Broker writes R1 again → duplicate | Broker sees same sequence → skips duplicate |
| Consumer reads           | Sees R1 twice                      | Sees R1 once                                |

---

## 8. **Recommended configuration**

For strong reliability and ordering guarantees, use the following settings:

```properties
acks=all
enable.idempotence=true
retries=Integer.MAX_VALUE
max.in.flight.requests.per.connection=1
delivery.timeout.ms=120000
linger.ms=5
batch.size=32768
```

This ensures:

* No duplicates (idempotence).
* Ordered writes.
* Infinite retries for transient errors.
* Reasonable batching and throughput.

If you also need *exactly-once* across multiple topics or partitions (for example, when using Kafka Streams), enable transactions:

```properties
enable.idempotence=true
transactional.id=unique-producer-id
```

---

## 9. **Summary**

| Concept        | Description                                                                                   |
| -------------- | --------------------------------------------------------------------------------------------- |
| **Goal**       | Prevent duplicate messages caused by retries or network errors.                               |
| **Mechanism**  | Unique producer ID (PID) and sequence numbers per partition.                                  |
| **Effect**     | Broker deduplicates duplicate sends automatically.                                            |
| **Scope**      | Guarantees exactly-once per producer session, per partition.                                  |
| **Next level** | Combine with transactions for exactly-once semantics across multiple partitions and sessions. |

---

### In short:

Setting `enable.idempotence=true` ensures that even if a producer retries due to timeouts, disconnects, or leader re-elections, **Kafka will store each message exactly once per partition**.
It eliminates duplicate writes caused by retries and is the foundation for Kafka’s **exactly-once delivery guarantees**.

# Where is PID Stored?

---

## 1. **Where the Producer ID (PID) comes from**

When a Kafka producer with `enable.idempotence=true` starts, it doesn’t generate its own PID.
Instead, it **requests a unique Producer ID from the Kafka cluster controller** (a special broker responsible for coordination tasks).

### Step-by-step:

1. The producer connects to any broker.
2. That broker forwards a request to the **cluster controller**.
3. The controller allocates a **64-bit Producer ID (PID)** and returns it to the producer.
4. The producer caches this PID locally in memory.

From then on, the producer includes this **PID** with every produce request it sends.

### Where it’s stored:

* **Producer side:**

  * Stored **in producer memory** (inside the producer client instance).
  * Not persisted to disk by default.
  * Lost when the producer application restarts or crashes.
* **Broker side:**

  * Each broker maintains the PID–sequence mapping **in memory** (part of its replication log state).
  * The mapping is also persisted **in the partition log** to survive broker restarts (see next sections).

---

## 2. **What the broker stores — the PID and sequence mapping**

Each broker tracks, for every partition it manages:

* The **latest PID** that has written to that partition.
* The **last sequence number** seen from that PID.

This information is maintained so that the broker can detect duplicates if a producer retries a batch.

### Internally:

When a broker receives a record batch, it checks:

1. The **PID** in the request header.
2. The **sequence number range** of the batch (e.g., 120–125).
3. The **last sequence number** it has already written for that PID.

If the new batch’s sequence number overlaps with an existing range, or if it’s exactly equal to one already committed, the broker recognizes it as a **duplicate** and discards it.

---

### Where brokers keep this metadata:

This depends on what type of state it is.

| State                                          | Storage location                        | Volatility              | Description                                                       |
| ---------------------------------------------- | --------------------------------------- | ----------------------- | ----------------------------------------------------------------- |
| **PID → sequence mapping (active)**            | **Broker memory (per-partition state)** | Lost if broker restarts | Used for fast duplicate detection during normal operation         |
| **PID and last sequence metadata (committed)** | **Kafka log segment (on disk)**         | Persistent              | Stored as part of the message batch header and as control records |
| **Transaction-related PIDs**                   | **__transaction_state internal topic**  | Persistent              | Tracks PID ownership and transaction status for EOS producers     |

---

## 3. **Persistence of PID and sequence metadata**

Kafka persists this metadata indirectly through **control records** written into the partition log itself.

Each message batch written by an idempotent producer includes in its header:

* `producerId` (PID)
* `producerEpoch`
* `baseSequence`
* `lastSequence`
* `isTransactional` flag

These headers are stored **inside the log segment on disk** along with the actual messages.

So if a broker restarts:

* It **replays the log** from disk during recovery.
* During this replay, it reconstructs the **PID → last sequence number** mapping in memory.
* After recovery, duplicate detection continues working as if nothing happened.

That’s why Kafka’s idempotence remains consistent across broker restarts, but **not** across producer restarts (since the producer gets a new PID each time).

---

## 4. **What happens on producer restart**

When the producer application restarts:

* The old PID is gone (it was in memory only).
* Kafka assigns a **new PID** to the new instance.
* Because it’s a new PID, the broker treats this as an entirely new producer identity.
* The old PID’s sequence tracking remains on the broker for a time but is unrelated to the new producer.

This is why idempotence guarantees are **session-scoped** — they only apply while the same producer instance (and PID) is alive.

If you want to maintain idempotence **across restarts**, you need **transactions** with a `transactional.id`.

---

## 5. **Transactional producers and PID persistence**

When you set:

```properties
transactional.id=my-producer-txn
enable.idempotence=true
```

Kafka upgrades from an **idempotent producer** to a **transactional producer**.

In this case:

* The PID is no longer ephemeral.
* It’s **stored persistently in Kafka’s internal topic**:

  ```
  __transaction_state
  ```
* This topic maps each `transactional.id` to a PID and epoch number.
* If the producer restarts with the same `transactional.id`, it retrieves the same PID (with incremented epoch).
* This allows Kafka to continue deduplication *across producer restarts* — a key part of **exactly-once semantics (EOS)**.

---

## 6. **Summary: where PID and sequence numbers live**

| Component                   | Data Stored                                        | Where Stored                         | Persistence                 | Purpose                                                 |
| --------------------------- | -------------------------------------------------- | ------------------------------------ | --------------------------- | ------------------------------------------------------- |
| **Producer**                | PID, per-partition sequence numbers                | Producer memory                      | Lost on restart             | Identifies producer session; generates sequence numbers |
| **Broker (active memory)**  | Last sequence number per PID per partition         | Broker memory                        | Reconstructed after restart | Used for duplicate detection during runtime             |
| **Broker (disk)**           | PID, baseSequence, lastSequence (in batch headers) | Partition log segments               | Persistent                  | Replay on restart to rebuild state                      |
| **Transactional producers** | PID ↔ transactional.id mapping                     | `__transaction_state` internal topic | Persistent                  | Enables idempotence across restarts and partitions      |

---

## 7. **Illustrated data flow example**

1. Producer starts → requests PID from controller → receives `PID = 12345`.
2. Producer writes to partition 0:

   * Batch header: `{ PID=12345, baseSeq=0, lastSeq=9 }`
3. Broker appends batch to log segment file `/kafka-logs/topic-0/000000000001.log`
4. Broker updates its in-memory table:

   ```
   topic-0 partition-0:
     PID 12345 → lastSeq=9
   ```
5. Producer retries batch with `{PID=12345, baseSeq=0, lastSeq=9}` due to timeout.

   * Broker checks and sees it’s already written — discards duplicate.
6. Broker restarts later → reads log segment → rebuilds PID mapping.

---

## 8. **In summary**

* **PID (Producer ID):** Assigned by Kafka controller, stored in producer memory; identifies the producer session.
* **Sequence numbers:** Maintained by producer per partition; embedded in message batch headers.
* **Broker state:** Maintains last sequence per PID in memory for duplicate detection; reconstructs it from the partition log after restart.
* **Transactions:** Persist PID ↔ transactional.id mapping in `__transaction_state`, enabling exactly-once delivery across restarts.

---

### Bottom line:

`enable.idempotence=true` activates a coordinated system where:

* The **producer** tracks sequence numbers.
* The **broker** tracks what it has already accepted per producer.
* Both use persistent log metadata so that duplicate suppression continues even after broker restarts.

If you also configure `transactional.id`, Kafka persists the PID mapping cluster-wide, extending these guarantees across producer sessions and enabling **true exactly-once semantics**.