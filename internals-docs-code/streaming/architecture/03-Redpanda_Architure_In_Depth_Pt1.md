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

Great question — let’s unpack **“threads are pinned to a core”**:

---

### 1. Normal threading (default in most apps, like Kafka)

* An application creates multiple threads.
* The **OS scheduler** decides which CPU core runs each thread.
* Threads can **move between cores** depending on load, availability, or scheduling.
* This gives flexibility, but:

  * Causes **context switches** (thread gets paused, moved to another core).
  * Causes **cache misses** (data in one core’s L1/L2 cache isn’t available on the new core).
  * Adds **latency jitter**.

---

### 2. Pinning (CPU affinity)

* “Pinning” means a thread is **locked (affined)** to a specific CPU core.
* The OS will always schedule that thread **only on that one core**.
* Benefits:

  * **No migration** → thread always runs on the same CPU.
  * **Cache locality** → data stays in that CPU’s cache, improving performance.
  * **Predictable latency** → no interruptions from the scheduler moving threads around.
* Downside:

  * Less flexible: if one core is overloaded, OS can’t move its threads elsewhere.
  * Requires careful design to balance load across cores.

---

### 3. In Redpanda / Seastar’s case

* Instead of traditional multithreading, Seastar uses a **“shard-per-core”** model:

  * Each core gets one dedicated shard (like an event loop).
  * That shard is pinned to the core.
  * It runs everything: networking, disk I/O, scheduling for that shard.
* This eliminates almost all **locking** and **cross-core coordination** overhead.
* Each shard processes requests independently, and inter-core communication happens explicitly via message passing (not shared-memory locks).

---

✅ **So, “threads are pinned to a core” means:**
Each execution unit (thread/shard) runs permanently on the same CPU core, giving predictable performance and cache efficiency, instead of being moved around by the OS scheduler.

---

## 🔹 1. **Process vs Thread**

* A **process** is a program in execution:

  * Has its own memory space (heap, stack, code, etc.).
  * Example: `java -jar kafka.jar` starts a Kafka broker process.
* A **thread** is a **lightweight unit of execution** inside a process:

  * Shares the same memory space as other threads in that process.
  * Has its own stack and program counter (so it can run independently).
  * Example: Kafka spawns threads for handling networking, log flushes, replication, etc.

👉 Think of a process as a **house**, and threads as **people inside the house** who share the same kitchen (memory), but can each do different tasks.

---

## 🔹 2. What does a thread actually *do*?

* A thread executes a **sequence of instructions** (functions, loops, syscalls).
* The OS schedules the thread on a CPU core.
* Multiple threads in the same process can run concurrently (on different cores).

Example:

* Thread A reads data from the network socket.
* Thread B compresses and batches the data.
* Thread C writes data to disk.

---

## 🔹 3. Does the application “send data via a thread”?

Not exactly.

* The **application creates threads** to handle tasks (e.g., read, process, write).
* Each thread operates on shared data structures in the process’s memory.
* Threads can **pass data** between each other via:

  * Shared memory (since they live in the same process).
  * Queues, buffers, or synchronization primitives (locks, semaphores).

So it’s not like a thread is a “pipe” that data flows through.
👉 Instead: A thread is a **worker** that executes instructions on data in memory. The application controls what the thread does.

---

## 🔹 4. Example: Kafka

* Kafka broker process starts → JVM process.
* JVM creates **threads**:

  * **Network thread**: handles socket I/O from producers/consumers.
  * **I/O thread**: appends messages to the log.
  * **Replica fetcher threads**: replicate data across brokers.
* Threads share the same heap memory, but each has its own execution flow.

---

✅ **In short:**
A thread is *not* a data pipe — it’s a **unit of execution** that runs code inside a process. The application assigns tasks to threads, and those threads can work with shared memory to process or pass data around.

---

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

### Kafka Thread Pooling

Perfect — let’s explain **thread pools in the context of Kafka** only.

---

### 🔹 Why Kafka uses thread pools

* Kafka brokers handle **a huge number of concurrent tasks**:

  * Accepting requests from producers.
  * Serving fetch requests from consumers.
  * Replicating partitions between brokers.
  * Flushing data to disk.
* If Kafka created a **new thread for every client request**, it would waste CPU and memory.
* Instead, Kafka uses **thread pools**:

  * A fixed number of threads created at broker startup.
  * Incoming work is placed into **queues**.
  * Threads pick tasks from these queues and execute them.

---

### 🔹 Examples of thread pools inside Kafka

1. **Network Thread Pool**

   * Each broker has a set of **network threads**.
   * They handle socket connections, parse requests, and enqueue them for processing.
   * By default, the number of network threads = `num.network.threads` (configurable).
   * Example: If you set `num.network.threads=3`, Kafka creates **3 reusable threads** to handle all incoming client connections.

2. **I/O / Request Handler Thread Pool**

   * Requests received by network threads are handed off to **I/O threads**.
   * These handle actions like reading/writing data to partitions, updating metadata, etc.
   * Controlled by `num.io.threads`.
   * Example: If you have 8 I/O threads, they work in parallel to serve fetch/produce requests from the queue.

3. **Replica Fetcher Thread Pool**

   * Brokers need to replicate partitions across each other.
   * Kafka uses a pool of **replica fetcher threads**, one per leader-follower connection.
   * They continuously pull new data from leaders and apply it to local logs.

4. **Controller Thread (special case)**

   * The broker elected as **controller** uses a dedicated thread to manage partition leadership and cluster metadata.
   * This isn’t a pool but a **single thread** with a special role.

---

### 🔹 Why this matters

* **Efficiency**: Threads are expensive, so Kafka recycles them.
* **Throughput**: A pool keeps all CPU cores busy without creating too many threads.
* **Predictability**: Pools prevent the system from spawning unbounded threads when under load (avoiding crashes).

---

✅ **In short (Kafka terms):**
Kafka uses **thread pools** (network, I/O, replica fetchers) to process large numbers of concurrent requests with a fixed number of reusable threads. Instead of one thread per request, requests go into a queue, and a worker thread from the pool handles them.

---

## 🔹 Kafka: Thread Pools Model

* **Thread pools**: Network threads, I/O threads, replica fetcher threads.
* **Work model**:

  * A request arrives → goes into a queue → some thread in the pool picks it up.
  * Threads may run on different CPU cores → need **locks and synchronization** to coordinate access to shared structures (like logs, partitions).
* **Implication**:

  * More flexible, but extra overhead from context switches, locks, and memory sharing.
  * OS scheduler decides which threads run on which cores (unless pinned manually).

---

## 🔹 Redpanda (Seastar): Shard-per-Core Model

* **No thread pools at all.**
* Instead:

  * Each CPU core runs a **single Seastar “reactor” thread**.
  * That thread never migrates → it is **pinned** to the core permanently.
  * Each reactor (aka shard) runs its own event loop and manages all tasks assigned to it: networking, disk I/O, scheduling.
* **Work model**:

  * Incoming requests are directed to the shard that owns the partition (no global queue).
  * That shard executes all operations locally, without locks.
  * If work needs to cross cores, shards pass messages explicitly (message passing, not shared-memory locks).
* **Implication**:

  * Completely avoids contention → no thread pools, no locks, no queues between workers.
  * Each shard has exclusive ownership of its memory and partitions.
  * Predictable latency (no surprises from OS scheduling).

---

## 🔹 Side-by-side Comparison

| Feature               | **Kafka (Thread Pools)**                                         | **Redpanda (Shard-per-Core)**                                          |
| --------------------- | ---------------------------------------------------------------- | ---------------------------------------------------------------------- |
| **Concurrency model** | Multiple thread pools (network, I/O, replication).               | One shard (reactor thread) per CPU core.                               |
| **Scheduling**        | OS scheduler decides which thread runs on which core.            | Threads are pinned → 1 thread per core forever.                        |
| **Work distribution** | Tasks placed into queues, picked by worker threads.              | Requests routed directly to the shard that owns the partition.         |
| **Synchronization**   | Requires locks (shared memory between threads).                  | No locks → shard owns its state, cross-core via message passing.       |
| **Context switches**  | Frequent, threads may migrate across cores.                      | None (thread never migrates).                                          |
| **Analogy**           | Call center with a pool of operators picking calls from a queue. | Each operator has their own dedicated customers, no queue, no sharing. |

---

## 🔹 Why Redpanda dropped thread pools

* Kafka’s model = general-purpose, flexible, but pays costs of **locks + context switching**.
* Redpanda’s Seastar model = **deterministic, low-latency, NVMe-optimized**.
* By dedicating one reactor thread per core, Redpanda avoids the OS scheduler entirely and fully controls concurrency.

---

✅ **In short:**

* Kafka → **thread pools** with shared state, queues, and locks.
* Redpanda → **no thread pools**, just one pinned reactor thread per core, using message passing instead of locking.

---

## 🔹 In Kafka

* Separate **thread pools** handle different responsibilities:

  * Network threads → accept producer/consumer socket requests.
  * I/O threads → read/write data to partitions.
  * Replica fetcher threads → replication.
* These threads share data structures → need **locks + queues**.

---

## 🔹 In Redpanda (Shard-per-Core model)

* Each **shard = one reactor thread pinned to one CPU core**.
* That shard **owns a subset of partitions** (log segments).
* And yes, it handles *everything* for those partitions:

1. **Networking**

   * Each shard has its own TCP/HTTP server stack (Seastar provides this).
   * When a producer sends a message for a partition owned by shard 3, the network request is routed directly to shard 3.
   * That shard parses, validates, and queues the write internally.

2. **Log append (Producer writes)**

   * Shard 3 appends the data directly to its NVMe segment using **async direct I/O**.
   * No locks, no handing off to another thread.

3. **Consumer fetches (Reads)**

   * If a consumer requests data for a partition on shard 3, that same shard serves the request directly from its log segment (or in-memory cache).
   * Again: no global queue, no cross-thread locks.

4. **Replication (Followers → Leaders)**

   * If shard 3 owns a leader partition, it handles replication requests from follower brokers itself.
   * Fetcher threads in Kafka become **shard-owned replication tasks** in Redpanda.

---

## 🔹 Why this is powerful

* Everything related to a partition lives in **one shard**.
* The shard handles networking, persistence, and serving clients **without coordination overhead**.
* If work must cross shards (e.g., partition A on core 2, partition B on core 5), Redpanda uses **message passing**, not shared locks.

---

✅ **So yes:**
A shard in Redpanda is **responsible for the full lifecycle** of the partitions it owns:

* Accepting producer writes.
* Appending to disk.
* Serving consumer fetches.
* Handling replication.

Kafka splits these into different thread pools → Redpanda collapses them into a single shard reactor per core.

### Isnt Kafka Faster Because of Thread Pools?

---

## 🔹 Kafka’s Concurrency Model

* Multiple thread pools can *appear* to give concurrency:

  * Network threads enqueue requests.
  * I/O threads pick them up and write/read logs.
  * Replica fetcher threads replicate in parallel.
* But the cost is:

  * **Locks everywhere** (log segments, partition metadata, socket buffers).
  * **Context switches** when handing tasks across pools.
  * **Cache misses** because data may bounce across cores.
  * OS scheduler interference.

So while Kafka can “parallelize” operations on the same partition via pools, the overhead (locks, scheduling, context switching) adds **latency and jitter**.

---

## 🔹 Redpanda’s Concurrency Model

* Each shard (core) is a **single-threaded event loop**:

  * Owns a set of partitions exclusively.
  * No locks, no hand-offs, no blocking.
* **Concurrency comes from multiple shards in parallel**:

  * If you have 16 cores, you have 16 shards running completely independently.
  * Each shard is simultaneously handling **networking + producers + consumers + replication** for its partitions.
* For a single partition:

  * Only one shard touches it (so no thread-level concurrency on that data).
  * But this actually improves performance: **no lock contention, no context switches**.

---

## 🔹 Why Redpanda isn’t slower

1. **Lock-free execution**

   * Kafka: “parallel threads” but guarded by locks → effectively serial at the partition level.
   * Redpanda: one shard, lock-free, guaranteed order → faster.

2. **Core-to-core scaling**

   * Kafka: extra overhead scaling across cores because threads migrate.
   * Redpanda: scaling is natural — add more cores → more shards → more partitions handled in parallel.

3. **NVMe optimization**

   * Kafka’s I/O goes through the OS page cache and threads.
   * Redpanda maps shards directly to NVMe queues → multiple cores can hit storage **in true parallel**, without lock contention.

---

## 🔹 Analogy

* **Kafka** = a restaurant where multiple waiters share the same kitchen (need rules/locks to avoid collisions). Looks busy, but there’s overhead coordinating.
* **Redpanda** = each waiter has their own kitchen + their own customers. No conflicts, no coordination. Less “fake concurrency,” more real parallelism.

---

✅ **Answer:**
Redpanda is **not slower**. Even though a shard processes a partition’s work serially, that’s exactly what Kafka does too (because partitions are single-threaded units of order). The big win is that Redpanda avoids **lock contention, context switches, and cache misses**, so it scales much better with more cores and NVMe drives.

---
