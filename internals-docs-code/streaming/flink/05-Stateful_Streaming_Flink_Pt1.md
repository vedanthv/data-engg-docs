# Stateful Streaming in Flink

Stateful streaming in Flink means **your streaming operators remember information across events**, instead of treating every event independently.
This is one of Flink’s most powerful features and a major reason it is used for real-time pipelines.

---

# **1. What is stateful streaming?**

In normal (stateless) streaming:

```
map(event) → output
```

Each event is processed independently.

In **stateful** streaming:

```
map(event, stored_state) → update_state → output
```

The operator stores information from **previous** events and uses it for **future** events.

Examples:

* Counting events per user
* Detecting anomalies
* Maintaining a running average
* Managing session windows
* Deduplication
* Joins between two streams

All these require **remembering** some data → that is the *state*.

---

# **2. Where is state stored?**

Flink stores state in **Task Managers**, either:

### **A. In-memory / JVM heap state**

Fast, but smaller.

### **B. RocksDB state backend**

Stored on local disk, can be gigabytes to terabytes.

Flink abstracts storage so developers don’t have to manage it manually.

---

# **3. Types of state in Flink**

### **A. Operator State**

State is tied to the operator instance (task).

Examples:

* Kafka partitions state in Source
* ListState
* UnionListState

Suitable for non-keyed operations.

---

### **B. Keyed State**

Most common and powerful.

When you apply `keyBy()`, Flink partitions the stream by key:

```
keyBy(user_id)
```

Each key has **its own individual state**:

* ValueState
* ListState
* MapState
* ReducingState
* AggregatingState

This is how Flink allows millions of active keys with independent state.

---

# **4. How state interacts with parallelism**

When parallelism is 4, you get 4 operator instances, and state is partitioned automatically.

Example (keyBy user_id):

* user_id 1 → TM1
* user_id 2 → TM3
* user_id 3 → TM1
* user_id 4 → TM2

This guarantees correctness and scalability.

---

# **5. How Flink keeps state fault-tolerant (Exactly-Once)**

Flink uses:

### **Checkpoints**

Regular snapshots of state (consistent across all operators).

Process:

1. Job Manager triggers checkpoint
2. Task Managers snapshot their state
3. Save state to durable storage (S3, HDFS)
4. Continue processing

On failure:

* Restore from last checkpoint
* No duplicates, no missing data

This is how Flink gives **exactly-once state consistency**.

---

# **6. Step-by-step example (per-user rolling sum)**

### Step 1: You define a stream

```
(k1, 5)
(k2, 3)
(k1, 7)
```

### Step 2: Apply keyBy

```
(k1 → TM1), (k2 → TM2)
```

### Step 3: Use ValueState to store running sum

Initial state for all keys = 0

### Step 4: Process each event

* For k1: sum=0 → update to 5
* For k2: sum=0 → update to 3
* For k1: sum=5 → update to 12

### Step 5: State for key k1 is now 12 and stored inside TM1

Each key’s lifecycle is isolated.

---

# **7. Why stateful streaming is powerful in Flink**

* Massive scale: millions of keys, terabytes of state
* Built-in fault-tolerance
* Very low latency
* Fine-grained exactly-once semantics
* Native support for event-time + watermarks
* Automatic rescaling (state migration between TMs)

Flink is one of the few systems that supports **large and reliable state** directly inside a streaming engine.

---

# **8. Short Summary**

Stateful streaming in Flink means operators maintain memory across events. Flink stores this state locally (heap or RocksDB), checkpoints it regularly, restores it on failure, and distributes it across parallel workers using keyed streams. This enables powerful use cases like real-time fraud detection, anomaly detection, streaming joins, and windows.