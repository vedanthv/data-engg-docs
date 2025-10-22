# Kafka Producer Requests

---

## 1. The `acks` configuration — what it means

When a producer sends a message to a Kafka topic, it can specify **how many brokers must confirm** the message before the producer considers it successfully written. This is controlled by the producer configuration parameter:

```properties
acks=0 | 1 | all
```

### **Option 1: `acks=0`**

* The producer **does not wait** for any acknowledgment.
* As soon as the producer sends the message over the network, it marks it as “successfully sent.”
* The broker **may or may not** have received it — the producer never checks.
* **Fastest** option, but **least reliable**. If the broker crashes or network drops packets, messages can be lost silently.

**Use case:**
High-throughput, low-value data where occasional loss is acceptable (e.g., metrics, logs, sensor streams).

---

### **Option 2: `acks=1`**

* The producer waits for acknowledgment **only from the leader replica** of the partition.
* The leader appends the message to its local log (in memory or file system cache) and then responds.
* Followers replicate asynchronously — meaning the message **might not yet be replicated** when the acknowledgment is sent.
* If the leader crashes before followers replicate it, that message can be **lost** (because the new leader might not have that message).

**Use case:**
Balanced reliability and performance — commonly used in systems where minor data loss is tolerable.

---

### **Option 3: `acks=all` (or `acks=-1`)**

* The producer waits for acknowledgment from **all in-sync replicas (ISR)** of that partition.
* The leader only replies **after confirming** that every ISR replica has written the message to its local log.
* Provides **strongest durability guarantee**: a message is safe even if the leader immediately crashes after acknowledging.

**Use case:**
Mission-critical data (financial transactions, customer actions, audit logs) where **no data loss is acceptable**.

---

## 2. What happens when a broker receives a produce request

When the **leader broker** for a partition receives a **ProduceRequest** from a producer, it performs the following steps:

### **Step 1: Validation checks**

The broker ensures:

1. **Authorization:**
   The client (producer) has permission to write to the topic.

2. **Valid `acks` value:**
   Only `0`, `1`, or `all` (or `-1`, which means the same as “all”) are accepted.

3. **Sufficient in-sync replicas (ISR):**

   * If `acks=all`, the broker checks if there are enough ISR members available.
   * This check depends on another broker-side parameter:

     ```properties
     min.insync.replicas=<N>
     ```

     If the ISR count drops below this threshold, the broker **rejects** new produce requests with an error like:

     ```
     NOT_ENOUGH_REPLICAS
     ```

     This prevents acknowledging messages that would not be safely replicated.

---

### **Step 2: Write the message to the local log**

* The leader **appends the record batch** to its local log segment file.
* Kafka uses the **Linux filesystem page cache** for performance:

  * The message is written to the OS cache (in memory),
  * The OS asynchronously flushes it to disk later.
* Kafka **does not call `fsync()` or wait for disk persistence** before acknowledging.
  Instead, **replication** (to followers) provides durability.

**Why this design?**
Disk `fsync` is slow. Kafka relies on replication to guarantee durability instead of waiting for every write to reach disk.

---

### **Step 3: Behavior based on `acks` setting**

After writing to the log:

#### **If `acks=0`**

* The broker **does not send any acknowledgment** back.
* The producer assumes success immediately after sending.

#### **If `acks=1`**

* The leader **immediately sends a success response** after writing to its local log (even before followers replicate).
* Replication happens asynchronously afterward.

#### **If `acks=all`**

* The broker **waits** until **all ISR replicas** confirm they have replicated the message.
* To manage this waiting process efficiently, Kafka uses a **buffer called “purgatory.”**

---

## 3. What is purgatory?

“**Purgatory**” in Kafka is an **in-memory waiting area** for requests that cannot be completed immediately.

### How it works for produce requests:

* When a message is produced with `acks=all`, the broker stores the request in **ProduceRequestPurgatory**.
* The request waits there until:

  * All ISR replicas have acknowledged replication of that offset.
* Once replication completes:

  * The request is removed from purgatory,
  * The broker sends a success response back to the producer.

This mechanism allows the broker to **delay responses efficiently** without blocking threads.

Kafka also uses separate purgatories for **fetch** requests (for consumers performing long polling).

---

## 4. Sequence of events (step-by-step)

Let’s trace an example of a message being produced to a partition with replication factor = 3.

### **Scenario**

* Replicas: Broker 1 (Leader), Broker 2 (Follower), Broker 3 (Follower)
* ISR = {1, 2, 3}
* Producer sends a record with `acks=all`.

---

### **Step 1:** Producer sends a `ProduceRequest` to Broker 1 (leader)

The request includes:

* Topic and partition,
* Record batch,
* `acks=all`.

---

### **Step 2:** Broker 1 validates request

* Checks permissions, acks value, ISR count.
* Appends message to its log (OS cache).

---

### **Step 3:** Broker 1 forwards the new message to followers

* Followers 2 and 3 send `Fetch` requests to Broker 1 for replication.
* Broker 1 sends them the new record.

---

### **Step 4:** Followers write message to their own logs

* Each follower appends the message to its local log.
* Each follower sends back a **replication acknowledgment** to Broker 1.

---

### **Step 5:** Broker 1 waits in purgatory

* The produce request remains in **ProduceRequestPurgatory** until Broker 1 sees acknowledgments from **all ISR members** for that offset.

---

### **Step 6:** Broker 1 responds to producer

* Once all ISR members have confirmed replication, Broker 1 removes the request from purgatory and sends:

  ```
  ProduceResponse(correlation_id=1234, status=SUCCESS)
  ```
* The producer marks the message as successfully written.

---

## 5. Key configuration parameters influencing this process

| Parameter                    | Level        | Description                                                 |
| ---------------------------- | ------------ | ----------------------------------------------------------- |
| `acks`                       | Producer     | How many replicas must acknowledge before success.          |
| `min.insync.replicas`        | Broker/Topic | Minimum ISR count required for accepting `acks=all` writes. |
| `replication.factor`         | Topic        | Total number of replicas for the partition.                 |
| `replica.lag.time.max.ms`    | Broker       | How long a follower can lag before being removed from ISR.  |
| `replica.fetch.max.bytes`    | Broker       | Max bytes per replication fetch.                            |
| `flush.messages`, `flush.ms` | Broker       | Control how often logs are flushed to disk (optional).      |

---

## 6. Design rationale — why Kafka behaves this way

Kafka’s approach trades **disk persistence latency** for **replication-based durability**:

* Writing to the OS page cache is extremely fast.
* Replication ensures multiple brokers hold copies, so if one crashes before flushing to disk, others can recover the data.
* The producer controls how much durability it wants using `acks` and the broker’s ISR configuration.

This design allows Kafka to achieve **very high throughput** while still providing **strong durability when needed**.

---

## 7. Summary table — trade-offs among `acks` settings

| Setting    | Who Acknowledges | Latency | Durability | Risk of Data Loss                           | Common Use Case                       |
| ---------- | ---------------- | ------- | ---------- | ------------------------------------------- | ------------------------------------- |
| `acks=0`   | No one           | Lowest  | None       | Very high                                   | Fire-and-forget telemetry             |
| `acks=1`   | Leader only      | Medium  | Moderate   | Possible if leader fails before replication | Most common default                   |
| `acks=all` | All ISR replicas | Highest | Strong     | Very low                                    | Critical data (transactions, billing) |

---

### **In short**

When a producer writes to Kafka:

1. The **leader broker** receives and validates the request.
2. The leader appends it to its log (in memory).
3. Depending on `acks`:

   * `0` → no response.
   * `1` → immediate acknowledgment from leader.
   * `all` → waits in **purgatory** until all ISR replicas replicate the message.
4. Replication provides durability — not immediate disk persistence.
5. Once acknowledgment conditions are met, the broker replies and the producer considers the message successfully written.

---