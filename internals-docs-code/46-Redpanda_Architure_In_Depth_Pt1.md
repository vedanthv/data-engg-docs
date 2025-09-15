# Redpanda Architecture Pt 1

[Reference Video](https://www.youtube.com/watch?v=guoaxRJG8p8)

## Topics

<img width="1293" height="584" alt="image" src="https://github.com/user-attachments/assets/611ecc56-2661-4be0-9d96-2f47935ece31" />

## Origins of Kafka

<img width="1503" height="709" alt="image" src="https://github.com/user-attachments/assets/58168284-9b97-4722-9af4-488b1a603554" />

## Core Concepts in Kafka

<img width="1451" height="727" alt="image" src="https://github.com/user-attachments/assets/081cf5f3-9237-4e74-b269-1a822ddc6b52" />

<img width="1523" height="696" alt="image" src="https://github.com/user-attachments/assets/fd653708-b52f-43c5-9fd4-c7da651bea5c" />

## What is Redpanda?

<img width="1478" height="724" alt="image" src="https://github.com/user-attachments/assets/d4eae692-5317-40d4-83b6-0a3c5268eb0c" />

## Redpanda Bits and Bytes

<img width="1449" height="631" alt="image" src="https://github.com/user-attachments/assets/b9a2d0b0-f4f7-421a-9810-54c6b0f4d659" />

## Redpanda Core

<img width="1396" height="698" alt="image" src="https://github.com/user-attachments/assets/444a466f-3e26-4fa6-aad2-b5f9f4f5c7b6" />

## Seastar Concepts

<img width="1457" height="730" alt="image" src="https://github.com/user-attachments/assets/b77f27e6-8bda-410a-9e7c-76f61721c533" />

## Thread Per Core Benefits

<img width="1459" height="685" alt="image" src="https://github.com/user-attachments/assets/3e426022-ec3f-4329-a1e1-66549599b705" />

### Shard to Partition Mapping

---

🔹 Partition-to-Shard Mapping in Redpanda (Seastar Model)

* In Redpanda, **a partition is assigned to exactly one shard (CPU core)** within a broker.
* That shard is the **exclusive owner** of the partition: it handles all reads, writes, and replication logic for it.
* There is **no sharing of partitions across shards** → avoids locks, keeps the model deterministic.

👉 So yes: **1 partition → 1 shard** (on a given broker).

---

🔹 How This Works in Practice

1. **Broker Setup**

   * Each Redpanda broker runs with multiple **shards (cores)**.
   * Example: A broker with 8 CPU cores → 8 shards.

2. **Partition Assignment**

   * When a partition is created, Redpanda assigns it to a shard.
   * Partition → Shard mapping is stored in metadata (using Raft consensus).

3. **Shard Locality**

   * Once assigned, **all producers/consumers** that interact with that partition will hit that shard directly.
   * This guarantees:

     * **No cross-shard locks**
     * **Cache locality** (NUMA-aware memory)
     * **Predictable performance**

4. **Scaling Partitions**

   * More partitions = spread across more shards (and brokers).
   * If you have 100 partitions and 8 shards, partitions will be distributed \~evenly across shards.

---

🔹 Why This is Efficient

* Each shard runs its own **event loop** with Seastar.
* Since a shard owns the partition exclusively:

  * No lock contention.
  * No need for multiple threads touching the same partition.
  * CPU cache locality is preserved.

This is very different from Kafka’s JVM/thread pool model, where multiple threads may process partitions and need locks/synchronization.

---

Visual (Simplified)

**Kafka Broker (JVM, Thread Pools):**

```
Thread Pool
  ├── Partition 1 (handled by multiple threads w/ locks)
  ├── Partition 2 (ditto)
  └── Partition 3 ...
```

**Redpanda Broker (Seastar, Shards):**

```
Shard 0 → Partition 1, Partition 5
Shard 1 → Partition 2, Partition 6
Shard 2 → Partition 3
Shard 3 → Partition 4
```

👉 Each shard handles its own partitions — no overlap, no locks.

---

* A **partition cannot be split across shards** (it’s always fully owned).
* But a **shard can own multiple partitions** if you have more partitions than shards.
* Redpanda’s scheduler balances partitions across shards.

Excellent question 🔥 — you’ve zoomed right into the **partition-to-shard mapping** in Redpanda’s Seastar-based design. Let’s unpack it.

---

### 🔹 Shard to Partition Mapping in Redpanda (Seastar Model)

* In Redpanda, **a partition is assigned to exactly one shard (CPU core)** within a broker.
* That shard is the **exclusive owner** of the partition: it handles all reads, writes, and replication logic for it.
* There is **no sharing of partitions across shards** → avoids locks, keeps the model deterministic.

👉 So yes: **1 partition → 1 shard** (on a given broker).

---

🔹 How This Works in Practice

1. **Broker Setup**

   * Each Redpanda broker runs with multiple **shards (cores)**.
   * Example: A broker with 8 CPU cores → 8 shards.

2. **Partition Assignment**

   * When a partition is created, Redpanda assigns it to a shard.
   * Partition → Shard mapping is stored in metadata (using Raft consensus).

3. **Shard Locality**

   * Once assigned, **all producers/consumers** that interact with that partition will hit that shard directly.
   * This guarantees:

     * **No cross-shard locks**
     * **Cache locality** (NUMA-aware memory)
     * **Predictable performance**

4. **Scaling Partitions**

   * More partitions = spread across more shards (and brokers).
   * If you have 100 partitions and 8 shards, partitions will be distributed \~evenly across shards.

---

🔹 Why This is Efficient

* Each shard runs its own **event loop** with Seastar.
* Since a shard owns the partition exclusively:

  * No lock contention.
  * No need for multiple threads touching the same partition.
  * CPU cache locality is preserved.

This is very different from Kafka’s JVM/thread pool model, where multiple threads may process partitions and need locks/synchronization.

---

# 🔹 Visual (Simplified)

**Kafka Broker (JVM, Thread Pools):**

```
Thread Pool
  ├── Partition 1 (handled by multiple threads w/ locks)
  ├── Partition 2 (ditto)
  └── Partition 3 ...
```

**Redpanda Broker (Seastar, Shards):**

```
Shard 0 → Partition 1, Partition 5
Shard 1 → Partition 2, Partition 6
Shard 2 → Partition 3
Shard 3 → Partition 4
```

👉 Each shard handles its own partitions — no overlap, no locks.

---

🔹 Important Note

* A **partition cannot be split across shards** (it’s always fully owned).
* But a **shard can own multiple partitions** if you have more partitions than shards.
* Redpanda’s scheduler balances partitions across shards.

---

✅ **Answer:** Yes, in Redpanda’s Seastar model, **a partition maps to exactly one shard** (core). This lock-free ownership model is what gives Redpanda its high throughput and low latency.

---

Perfect 👌 — let’s go deep into **partition rebalancing** in Redpanda’s **Seastar shard-per-core model**, and contrast it with Kafka.

---

# 🔹 Why Rebalancing is Needed

* In any event streaming cluster, partitions need to be spread evenly for performance.
* Situations that trigger rebalancing:

  1. Adding/removing brokers (scale up/down).
  2. Adding/removing CPU cores (changing shard count).
  3. Increasing partitions on a topic.
  4. Failure recovery (a broker goes down).

---

# 🔹 Kafka Partition Rebalancing (Traditional Way)

* Kafka relies on a **partition reassigner** (via ZooKeeper or KRaft).
* When brokers are added, Kafka shifts partitions across brokers, but:

  * Within a broker, partitions are handled by **threads in pools** (not pinned to a core).
  * Partition-to-thread mapping is dynamic, with potential contention.
* Rebalancing is often **manual + disruptive** (CLI commands, partition reassignment tool).
* Data movement = expensive, because Kafka copies log segments across brokers during reassignment.

---

### 🔹 Redpanda Partition Rebalancing (Seastar Model)

#### 1. **Partition-to-Shard Pinning**

* Each partition is always owned by exactly **one shard**.
* When partitions are assigned to a broker, Redpanda also ensures **load balancing across shards** within that broker.

---

#### 2. **Adding a New Broker**

* Redpanda automatically reassigns some partitions to the new broker.
* Metadata (via Raft) is updated to reflect ownership.
* The new broker takes over as partition leader or replica for some partitions.
* Producers/consumers redirect automatically (via client metadata refresh).

👉 This is smoother than Kafka’s rebalance because Redpanda has no external ZooKeeper layer.

---

#### 3. **Adding CPU Cores (More Shards)**

* Suppose a broker runs on 4 cores (shards) and you upgrade it to 8 cores.
* Redpanda can **redistribute partitions across the new shards**.
* Each partition is moved to a new shard if needed, but ownership is always exclusive.
* This way, hardware scaling (more cores) leads to more parallelism without rewriting application logic.

---

#### 4. **Partition Expansion**

* If you increase partitions in a topic, Redpanda assigns new partitions to shards across brokers evenly.
* Existing partitions remain pinned — no surprise reassignments unless explicitly rebalanced.

---

#### 5. **Failure Recovery**

* If a broker/shard fails, Redpanda promotes replicas (via Raft consensus) to leaders.
* The partition moves to another shard/broker that has a replica.
* Clients auto-discover the new leader.

---

🔹 Why Redpanda’s Model Helps

| Aspect                   | Kafka               | Redpanda (Seastar)                  |
| ------------------------ | ------------------- | ----------------------------------- |
| **Partition Ownership**  | Dynamic threads     | Fixed shard-per-core                |
| **Rebalancing Trigger**  | Often manual        | Mostly automatic                    |
| **Intra-broker balance** | Threads may contend | Explicit shard assignment           |
| **Scaling Cores**        | No concept          | Shards = cores, easy scaling        |
| **Data Movement**        | Heavy (log copy)    | Lighter (replicas managed via Raft) |

---

🔹 Example

Suppose:

* Cluster = 2 brokers, 4 cores each → 8 shards total.
* Topic = 8 partitions.

**Initial mapping:**

```
Broker1 Shard0 → Partition0
Broker1 Shard1 → Partition1
Broker1 Shard2 → Partition2
Broker1 Shard3 → Partition3
Broker2 Shard0 → Partition4
Broker2 Shard1 → Partition5
Broker2 Shard2 → Partition6
Broker2 Shard3 → Partition7
```

Now you add a **third broker (4 cores)**:

* Redpanda rebalances so that Broker3 takes ownership of some partitions (say 2 and 6).
* Partition ownership shifts smoothly, Raft ensures replica consistency.
