# Kafka Fetch Requests Part II

---

## 1. The main idea — “Not all data on the leader is visible to consumers”

Every Kafka **leader broker** continuously receives new messages from producers.
However, **consumers cannot immediately see** every message the leader has written.

Why?

Because Kafka’s design ensures that **consumers only see data that is guaranteed to be durable** — that is, data replicated to **all in-sync replicas (ISR)**.

This rule guarantees that if the current leader fails, another replica (which becomes the new leader) still has those same messages.
Therefore, consumers will never read messages that could later “disappear” due to a broker failure.

---

## 2. Two categories of messages on the leader

Let’s define two sets of messages on the leader’s log:

| Category                  | Description                                                                     | Visibility                 |
| ------------------------- | ------------------------------------------------------------------------------- | -------------------------- |
| **Replicated messages**   | Messages that have been written to all in-sync replicas (ISR).                  | Visible to consumers.      |
| **Unreplicated messages** | Messages that are still only on the leader; followers haven’t fetched them yet. | **Hidden** from consumers. |

These unreplicated messages are considered **unsafe**.

---

## 3. Why unsafe messages are hidden

Let’s imagine what would happen if Kafka allowed consumers to read messages that only existed on the leader:

### Example scenario:

* Partition `A-0` has a replication factor of 3.

  * Leader = Broker 1
  * Followers = Broker 2, Broker 3
  * ISR = {1, 2, 3}

1. Producer sends a message `M1` to Broker 1 (leader).
2. Broker 1 appends `M1` to its local log.
3. Broker 1 has **not yet** replicated `M1` to the followers (2, 3).

Now two things could happen:

* **If Broker 1 crashes now**, followers 2 and 3 don’t have `M1`.
  When Broker 2 becomes the new leader, that message is **lost forever** — it never existed on the new leader’s log.
* **If a consumer had read `M1`** before the crash, it would have seen data that no longer exists in Kafka — an **inconsistency**.

Kafka’s design explicitly prevents this:
Consumers are not allowed to read messages that haven’t been replicated to all ISR members yet.
So, in this scenario, `M1` stays **invisible** to consumers until it’s safely replicated.

---

## 4. How Kafka enforces this — the “High Watermark” (HW)

Kafka tracks a special marker for each partition called the **High Watermark (HW)**.

### **Definition:**

> The High Watermark is the **highest offset** that has been replicated to **all in-sync replicas**.

* All messages **below or equal to** the HW are considered **committed**.
* All messages **above** the HW are **uncommitted** and invisible to consumers.

This is how Kafka decides what data can be fetched by consumer fetch requests.

### Visual example:

```
Partition log on the leader:
Offset: 0   1   2   3   4   5   6
Data:   A   B   C   D   E   F   G
               ^ 
               |
             High Watermark = 3
```

* Messages A, B, C, D → replicated to all ISR → **committed**, visible to consumers.
* Messages E, F, G → not yet replicated to all ISR → **uncommitted**, invisible to consumers.

A consumer fetching from this partition will only receive A–D, even though the leader’s local log already contains E–G.

---

## 5. Followers and replication interaction

Each **follower** continuously fetches data from the leader.
As followers replicate new messages and acknowledge them:

1. The leader updates the ISR status.
2. The leader advances the High Watermark (HW) to the highest offset replicated to all ISR members.
3. Messages up to this new HW now become **visible** to consumers.

Followers themselves are **not subject to this visibility rule**, because:

* Followers must read **all messages** (even uncommitted ones) from the leader to stay in sync.
* If followers were restricted like consumers, replication would never catch up.

---

## 6. The durability reason — avoiding “phantom reads”

Kafka hides unreplicated messages to prevent **inconsistency across consumers** after a leader failure.

### Example of inconsistency (if this rule didn’t exist):

1. Leader receives and appends message `M1` (not replicated yet).
2. Consumer reads `M1`.
3. Leader crashes before `M1` is replicated.
4. Follower becomes the new leader — `M1` doesn’t exist on it.
5. Now:

   * Consumer A (who read `M1`) believes `M1` exists.
   * Consumer B (starting later) never sees `M1`.

This breaks **Kafka’s fundamental guarantee** that:

> Once a message is committed (visible), it will never disappear.

Hence, Kafka enforces the rule:

* **Only committed (replicated) messages are readable by consumers.**

This preserves **linearizability** and **read-after-write consistency** for durable data.

---

## 7. Performance impact — replication lag delays consumer visibility

Because Kafka waits for replication before advancing the High Watermark, **slow replication** directly affects how quickly consumers see new data.

If followers lag behind due to:

* Network delays,
* Disk I/O bottlenecks,
* Broker overload,

then:

* The leader cannot advance the HW.
* Consumers will not see newly produced messages until followers catch up.

This is a key operational consideration for Kafka performance tuning.

---

## 8. How long can a follower lag before it’s removed from ISR?

The delay in message visibility is bounded by a broker configuration:

```properties
replica.lag.time.max.ms
```

### Meaning:

If a follower fails to catch up (replicate new messages) within this time window:

* The follower is **removed from the ISR**.
* The leader then only waits for the remaining ISR replicas to acknowledge new messages.

This prevents **one slow follower** from blocking message visibility for all consumers.

---

## 9. Lifecycle summary — from produce to consumer visibility

| Stage                                   | Description                          | Visible to Consumers?                        |
| --------------------------------------- | ------------------------------------ | -------------------------------------------- |
| **1. Producer sends message**           | Leader appends message locally.      | ❌ Not yet replicated.                        |
| **2. Followers replicate message**      | Followers fetch and append it.       | ❌ Still waiting for all ISR acknowledgments. |
| **3. All ISR replicas have replicated** | Leader advances High Watermark (HW). | ✅ Now visible.                               |
| **4. Consumer fetches from broker**     | Broker serves messages ≤ HW.         | ✅ Consumer sees it.                          |

---

## 10. Summary of key terms and concepts

| Term                        | Meaning                                                                         |
| --------------------------- | ------------------------------------------------------------------------------- |
| **ISR (In-Sync Replicas)**  | The set of replicas currently up to date with the leader.                       |
| **High Watermark (HW)**     | Highest offset replicated to all ISR members. Defines the “committed” boundary. |
| **Committed messages**      | Messages ≤ HW; safe and visible to consumers.                                   |
| **Uncommitted messages**    | Messages > HW; exist only on leader; hidden from consumers.                     |
| **replica.lag.time.max.ms** | Maximum allowed replication delay before a follower is removed from ISR.        |
| **Unsafe messages**         | Messages not yet replicated to ISR; can be lost if leader fails.                |

---

## 11. Practical implications

### **For developers:**

* A producer might think a message was written (if `acks=1`) before it’s visible to consumers. Visibility depends on replication speed and HW movement.
* Consumers will never see messages that might later disappear — even if they exist in the leader’s local log.

### **For operators:**

* Monitor replication lag and ISR size:

  * If lag increases, consumer delay increases.
  * If ISR shrinks, the system risks losing durability if the leader fails.
* Tune `replica.lag.time.max.ms` to balance tolerance for temporary slowness vs. responsiveness.

---

## 12. Analogy

Think of the **High Watermark** as Kafka’s “commit point.”

* Messages below HW → **committed**, safe, visible.
* Messages above HW → **uncommitted**, pending replication.

This is conceptually similar to:

* Database transactions where only **committed** transactions are visible to readers.
* The **write-ahead log (WAL)** mechanism where unflushed entries are not yet permanent.

---

## 13. In summary

1. **Leaders** receive messages first; **followers** replicate them.
2. **Consumers** only read up to the **High Watermark (HW)**.
3. Messages not yet replicated to all ISR members are **invisible** and **unsafe**.
4. This ensures **data consistency** and **no phantom messages** after leader failure.
5. **Replication lag** can delay visibility — bounded by `replica.lag.time.max.ms`.
6. Kafka’s durability and ordering guarantees depend on this careful distinction between **committed** and **uncommitted** data.

---

![alt text](https://snipboard.io/aTVOFE.jpg)

In some cases, a consumer consumes events from a large number of partitions. Sending the list of all the partitions it is interested in to the broker with every request and having the broker send all its metadata back can be very inefficient—the set of partitions rarely changes, their metadata rarely changes, and in many cases there isn’t that much data to return. To minimize this overhead, Kafka has fetch session cache. 

Consumers can attempt to create a cached session that stores the list of partitions they are consuming from and its metadata. Once a session is created, consumers no longer need to specify all the partitions in each request and can use incremental fetch requests instead. Brokers will only include metadata in the response if there were any changes. 

The session cache has limited space, and Kafka prioritizes follower replicas and consumers with a large set of partitions, so in some cases a session will not be created or will be evicted. In both these cases the broker will return an appropriate error to the client, and the consumer will transparently resort to full fetch requests that include all the partition metadata.
