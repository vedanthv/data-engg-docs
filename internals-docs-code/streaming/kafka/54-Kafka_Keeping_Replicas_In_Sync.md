# Kafka - Keeping Replicas in Sync

---

### 1. **Background: Replication and In-Sync Replicas (ISR)**

Kafka maintains multiple copies of data (replicas) for each partition to achieve durability and availability.

* When you create a topic, you specify a **replication factor** (for example, 3).
  That means each partition has **3 replicas** distributed across different brokers.
* Among these replicas, one is the **leader**, and the others are **followers**.
* Followers constantly replicate the leader’s data.

The set of replicas that are fully caught up with the leader is called the **ISR (In-Sync Replica) set**.

If all replicas are healthy, ISR = {leader, follower1, follower2}.
But if some followers fall behind or fail, they are temporarily removed from ISR.

---

### 2. **What `min.insync.replicas` means**

The `min.insync.replicas` configuration defines **the minimum number of replicas that must acknowledge a write** before Kafka considers that write **committed**.

You can define it:

* At the **broker level** (default behavior for topics on that broker)
* At the **topic level** (overrides broker-level setting)

---

### 3. **How writes work**

When a producer sends data to a partition:

1. The producer writes to the **leader** broker.
2. The leader writes the record locally and waits for acknowledgments from its followers (replicas).
3. The leader then decides whether to **commit** the message, depending on:

   * The producer’s `acks` configuration
   * The `min.insync.replicas` setting

---

### 4. **Interaction with producer `acks`**

The producer controls how many acknowledgments it expects before it considers a write successful.

| `acks` value         | Meaning                                                                 |
| -------------------- | ----------------------------------------------------------------------- |
| `acks=0`             | Producer doesn’t wait for acknowledgment. Fast but unsafe.              |
| `acks=1`             | Producer waits for leader acknowledgment only. Followers may still lag. |
| `acks=all` (or `-1`) | Producer waits for acknowledgment from all **in-sync replicas** (ISR).  |

Now, **when `acks=all`**, Kafka uses `min.insync.replicas` to decide if enough replicas are available to safely accept the write.

If the ISR count < `min.insync.replicas`, Kafka **rejects** the produce request with:

```
NotEnoughReplicasException
```

---

### 5. **Example scenario**

#### Configuration:

* Replication factor = 3
* `min.insync.replicas = 2`
* Producer uses `acks=all`

#### Case 1: All replicas healthy

ISR = {leader, follower1, follower2}
→ Producer sends a record → All 3 replicas acknowledge → Write succeeds.

#### Case 2: One replica down

ISR = {leader, follower1} (2 replicas)
→ Still >= 2 → Producer can continue writing safely.

#### Case 3: Two replicas down

ISR = {leader} (1 replica only)
→ 1 < 2 → Kafka rejects the write.
Producer gets `NotEnoughReplicasException`.
Consumers can still **read existing committed data**, but **no new writes** are accepted.
The partition becomes effectively **read-only** until at least one more replica rejoins ISR.

---

### 6. **Why this matters (Consistency vs Availability)**

This configuration directly affects how Kafka behaves during broker failures:

* If you set **`min.insync.replicas=1`**, Kafka prioritizes **availability**:

  * You can always produce data as long as one replica (the leader) is up.
  * But if that replica crashes before followers catch up, data can be lost.

* If you set **`min.insync.replicas=2`**, Kafka prioritizes **consistency**:

  * Kafka only commits data when at least two replicas have it.
  * If one replica remains, the system refuses new writes to prevent data loss.
  * The tradeoff is reduced availability during broker outages.

This is the **CAP theorem tradeoff** — balancing **consistency** and **availability** under failure conditions.

---

### 7. **Why data can disappear when misconfigured**

If `min.insync.replicas` is too low (for example, `1`), then:

* Kafka marks data as **committed** even when **only one replica** has it.
* If that single replica fails before the others replicate the data, the message is lost permanently.
* Later, when a new leader is elected (one that didn’t have the data), the old data simply disappears — because from the cluster’s point of view, it was never truly committed to a quorum.

Setting `min.insync.replicas=2` (with replication factor 3) prevents this.

---

### 8. **Recovering from a read-only situation**

When Kafka refuses new writes because too few replicas are in-sync:

* You must **bring failed brokers back online**.
* Once the followers catch up with the leader’s log, they rejoin the ISR.
* When ISR size ≥ `min.insync.replicas`, producers can write again.

Kafka does this automatically — you just need to restore the unavailable brokers and let replication complete.

---

### 9. **Best practice**

For production-grade reliability:

* **Replication factor:** 3
* **`min.insync.replicas`:** 2
* **Producer `acks`:** `all`

This ensures:

* Data is only acknowledged when written to at least 2 brokers.
* The system can tolerate one broker failure without losing data.
* Writes are temporarily paused (not lost) if two brokers fail.

---

### 10. **Summary**

| Concept                        | Description                                                                |
| ------------------------------ | -------------------------------------------------------------------------- |
| **ISR (In-Sync Replicas)**     | Replicas fully caught up with the leader                                   |
| **min.insync.replicas**        | Minimum number of replicas that must acknowledge a write for it to succeed |
| **`acks=all`**                 | Producer waits for all in-sync replicas                                    |
| **High `min.insync.replicas`** | Improves consistency, reduces availability                                 |
| **Low `min.insync.replicas`**  | Improves availability, increases risk of data loss                         |
| **Typical setting**            | Replication factor = 3, min.insync.replicas = 2                            |

---

In short:
`min.insync.replicas` is Kafka’s mechanism to enforce a **write quorum** — ensuring that data acknowledged to the producer truly exists on more than one broker. It’s the key parameter that balances **durability** and **availability** in distributed Kafka clusters.

Let’s break this passage down carefully and explain what it really means — especially in the context of **Kafka replication reliability** and **cluster tuning**.

---

## 1. **Why out-of-sync replicas are a problem**

Kafka’s replication model depends on the concept of **in-sync replicas (ISR)** — these are the replicas that are fully caught up with the leader.

When a replica falls behind or stops communicating, it becomes **out of sync (OOSR)**.
Having out-of-sync replicas means:

* Fewer copies of the latest data are available.
* If the leader fails, the new leader may not have the most recent messages.
* Data loss risk increases.
* `min.insync.replicas` violations can occur, leading to write failures.

So Kafka tries to detect and handle out-of-sync replicas quickly — but *not too aggressively*, to avoid unnecessary instability.

---

## 2. **Two reasons why replicas go out of sync**

Kafka recognizes two primary conditions under which a replica can fall out of sync:

1. **Loss of connectivity to ZooKeeper**

   * In pre-KIP-500 versions of Kafka (those still using ZooKeeper), each broker maintains a session with ZooKeeper via periodic **heartbeats**.
   * If a broker doesn’t send a heartbeat for a certain amount of time, ZooKeeper assumes it is dead or unreachable and removes it from the cluster.

2. **Replication lag**

   * A follower replica constantly fetches data from the leader.
   * If it stops fetching (e.g., due to network issues, GC pauses, overloaded broker) or cannot keep up, its **replication lag** increases.
   * If that lag exceeds a configured limit, the broker marks it as **out of sync**.

---

## 3. **First setting: `zookeeper.session.timeout.ms`**

This configuration determines **how long ZooKeeper waits** before declaring a broker “dead” due to missed heartbeats.

* Default (after Kafka 2.5.0): **18,000 ms (18 seconds)**
* Previously: **6,000 ms (6 seconds)**

### How it works:

Each Kafka broker sends periodic heartbeats to ZooKeeper.
If ZooKeeper doesn’t receive a heartbeat within this timeout:

* It removes the broker’s ephemeral nodes.
* The controller broker notices and triggers a **leader re-election** for all partitions that broker was leading.

### Why this setting matters:

* **If too short:**
  Temporary slowdowns (e.g., GC pauses or network hiccups) cause unnecessary broker removals → frequent leader re-elections → cluster instability.
* **If too long:**
  It takes longer to detect a genuinely dead broker → slower failover → decreased availability.

### Practical insight:

In cloud or virtualized environments, network latency is often less predictable, so Kafka 2.5 increased the default from **6s → 18s** to make clusters more tolerant of brief network fluctuations.

---

## 4. **Second setting: `replica.lag.time.max.ms`**

This controls **how long** a follower can be behind the leader before Kafka considers it **out of sync**.

* Default (after Kafka 2.5.0): **30,000 ms (30 seconds)**
* Previously: **10,000 ms (10 seconds)**

### How it works:

If a follower doesn’t fetch data from its leader within this time window, or if its last fetch is too far behind, the leader removes it from the ISR.

### Why this setting matters:

* **Shorter value:**
  Kafka quickly removes lagging replicas from the ISR → better consistency but higher chance of instability (“ISR flapping”).
  Example: if a follower momentarily pauses (e.g., during a GC), it’ll be removed immediately.
* **Longer value:**
  Kafka gives replicas more time to catch up → more stable ISR membership, fewer unnecessary leader changes.
  The tradeoff: longer replication delay means data takes more time to reach all replicas.

---

## 5. **Impact on consumer latency**

There’s an important implication here:
When you use `acks=all`, a message is considered **committed** only when all in-sync replicas have acknowledged it.

Therefore, if Kafka keeps replicas in the ISR longer (e.g., by setting `replica.lag.time.max.ms = 30000`), it may take longer for:

* All replicas to receive a message.
* Consumers configured with **read committed** isolation (like transactional consumers) to read it.

So, increasing this setting improves **cluster stability**, but potentially **increases end-to-end latency** — the time between when a producer writes a message and when all consumers can see it.

---

## 6. **Balance between stability and responsiveness**

You can think of these two settings as **sensitivity knobs**:

| Setting                        | Detects               | Too Low →                          | Too High →                          | Default (since Kafka 2.5) |
| ------------------------------ | --------------------- | ---------------------------------- | ----------------------------------- | ------------------------- |
| `zookeeper.session.timeout.ms` | Broker heartbeat loss | Frequent re-elections, instability | Slow failure detection              | 18000 ms                  |
| `replica.lag.time.max.ms`      | Replication delay     | Frequent ISR removals              | Slower replication / higher latency | 30000 ms                  |

Kafka 2.5 raised both defaults because production clusters, especially in cloud environments, were becoming too “sensitive” — reacting to transient conditions that weren’t real failures.

---

## 7. **How these interact**

If a broker experiences a GC pause or network lag:

* It might stop sending ZooKeeper heartbeats.
* It might stop fetching from the leader.

These two timeouts act independently but together:

* If the broker fails ZooKeeper heartbeats → it’s considered dead cluster-wide.
* If the broker fetches too slowly → it’s marked out of sync but remains alive.

Kafka’s updated defaults aim to **minimize false positives** (temporary slowness causing unnecessary failovers) while still ensuring **reasonable detection of real failures**.

---

## 8. **Summary**

| Concept                             | Description                                                                     |
| ----------------------------------- | ------------------------------------------------------------------------------- |
| **Out-of-sync replicas**            | Followers that are lagging or disconnected from the leader                      |
| **Cause 1: ZooKeeper session loss** | Broker missed heartbeats → considered dead                                      |
| **Cause 2: Replication lag**        | Follower too far behind the leader                                              |
| **`zookeeper.session.timeout.ms`**  | How long ZooKeeper waits for heartbeats (default: 18s)                          |
| **`replica.lag.time.max.ms`**       | How long a follower can lag before being removed from ISR (default: 30s)        |
| **Effect of longer timeouts**       | More stable clusters, but slightly higher failover and data replication latency |

---

### **In essence:**

Kafka 2.5 made these parameters more tolerant to transient slowdowns.
The goal is to prevent *flapping* — situations where brokers or replicas oscillate between “in sync” and “out of sync” due to short-lived lags — at the cost of slightly higher end-to-end latency for committed messages.

The overall tradeoff is **stability and durability over minimal latency**, which is the right choice for most production systems.

# Persisting to Disk

---

## 1. **Kafka’s durability model in context**

Kafka is designed for *high-throughput, low-latency* data streaming, and part of that efficiency comes from **asynchronous disk I/O**.
When a producer sends a message:

* The message is written to the broker’s **write-ahead log** (in memory or OS page cache).
* The broker then acknowledges the message to the producer **before** it’s necessarily written to physical disk.

This design lets Kafka achieve very high throughput while maintaining good fault tolerance through **replication**.

---

## 2. **Acknowledgments vs. persistence**

Kafka **acknowledges a message** when the configured number of replicas (controlled by `acks` and `min.insync.replicas`) have received it.
However:

* Those replicas may not have flushed the message to disk yet.
* The data could still be in the **Linux page cache** (in memory), waiting to be written to disk later.

### Why this is still “safe” (most of the time)

Kafka assumes that having multiple replicas — ideally on separate racks or availability zones — gives enough durability:

* Even if one machine crashes before flushing to disk, others will still have the data in memory.
* It’s statistically rare for multiple racks to fail simultaneously.

So, **Kafka prioritizes replication across nodes** over **immediate disk flushes** for performance.

---

## 3. **Linux page cache and Kafka’s I/O behavior**

Kafka relies on the **Linux page cache** to handle writes efficiently:

* When Kafka appends data to a log segment, it writes to the filesystem, which typically buffers the data in RAM.
* The operating system decides when to flush (sync) those buffers to disk — usually based on:

  * Memory pressure
  * Time since last flush
  * Background kernel flush daemons

### Benefit:

High throughput, because Kafka avoids blocking the write path for disk I/O on every message.

### Risk:

If a broker and its OS both crash before the page cache is flushed, **recent data not yet synced to disk can be lost** — even if it was acknowledged to the producer.

---

## 4. **When Kafka flushes to disk**

Kafka explicitly flushes messages to disk in three main situations:

1. **When rotating log segments**

   * Each topic partition log is split into *segments* (default 1 GB).
   * When the active segment reaches 1 GB, Kafka closes it and opens a new one.
   * During this rotation, Kafka **flushes the closed segment to disk**.

2. **Before a broker restart (graceful shutdown)**

   * During a controlled shutdown, Kafka flushes all logs to disk to avoid data loss.

3. **When triggered by manual or time-based configuration**

   * Through the `flush.messages` or `flush.ms` configurations.

Otherwise, Kafka relies on the operating system to flush data automatically.

---

## 5. **Tuning with `flush.messages` and `flush.ms`**

Kafka provides two configuration parameters that control **how often** it forces a disk flush:

| Parameter            | Description                                                                                              |
| -------------------- | -------------------------------------------------------------------------------------------------------- |
| **`flush.messages`** | The maximum number of messages that can be written to a log segment before Kafka forces a flush to disk. |
| **`flush.ms`**       | The maximum time (in milliseconds) that Kafka will wait before forcing a flush to disk.                  |

### Example

* `flush.messages=10000` → Kafka flushes after every 10,000 messages.
* `flush.ms=5000` → Kafka flushes every 5 seconds.

Setting either value to `0` disables time/message-based forced flushing, letting the OS handle it.

---

## 6. **Trade-offs of frequent flushing**

| Setting                                       | Pros                                                                      | Cons                                                                                          |
| --------------------------------------------- | ------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------- |
| **Frequent flush (low values)**               | Minimizes risk of data loss if the broker crashes (more durable).         | Reduces throughput — frequent disk writes cause I/O bottlenecks.                              |
| **Infrequent flush (high values / disabled)** | Maximizes throughput — Kafka benefits from OS caching and batched writes. | Increases risk of losing a few seconds of acknowledged data if a broker crashes before flush. |

In practice, **most Kafka deployments rely on the defaults**, allowing Linux to manage flush timing, because:

* Kafka’s replication provides redundancy.
* Disk I/O is expensive, and immediate syncs would drastically reduce performance.

---

## 7. **Modern reliability context**

Even though Kafka doesn’t flush every message to disk, reliability is still very high due to:

* **Replication** — multiple brokers have copies.
* **Leader election rules** — only *in-sync* replicas can become new leaders (when `unclean.leader.election.enable=false`).
* **Producer acks and retries** — producers can require acknowledgment from all replicas (`acks=all`).

So Kafka effectively treats **replication across brokers** as more durable than **synchronous disk persistence** on one node.

---

## 8. **Summary**

| Concept              | Description                                                                                                     |
| -------------------- | --------------------------------------------------------------------------------------------------------------- |
| **Acknowledgment**   | Kafka confirms to producers once replicas receive the message (not necessarily flushed to disk).                |
| **Disk flush**       | Writing data from memory (page cache) to physical disk.                                                         |
| **Flush timing**     | Happens during log rotation, shutdown, or as configured by `flush.messages` / `flush.ms`.                       |
| **Default behavior** | Kafka relies on the OS page cache for efficiency; replication ensures durability.                               |
| **Tradeoff**         | Frequent flushing = safer but slower; infrequent flushing = faster but less durable if multiple failures occur. |

---

### In short:

Kafka’s design assumes that **replication across brokers is safer and faster** than forcing each broker to sync every message to disk.
However, if your system cannot tolerate *any* acknowledged-message loss — such as in **financial transaction logs or audit trails** — you can configure:

```properties
flush.messages=1
flush.ms=1000
```

to ensure each message (or small batch) is flushed promptly, at the cost of throughput.

In most production use cases, leaving flushing asynchronous provides the right balance of **performance, resilience, and efficiency**.
