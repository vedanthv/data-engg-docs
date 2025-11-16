# Stateful Upgrades in Flink

Stateful upgrades in Flink mean **upgrading a running streaming job while preserving its state**, without starting from scratch or losing data.
This is one of Flink’s most important capabilities because real-time pipelines often need continuous improvements.

Here is the clearest explanation.

---

# **1. What is a Stateful Upgrade?**

A **stateful upgrade** = deploying a new version of your Flink job **using its existing state**.

You are changing code, logic, or parallelism while keeping:

* Keyed state
* Window state
* Timers
* Operator state
* Kafka offsets
* Any other internal state

This prevents:

* Reprocessing from beginning
* Losing state
* Writing wrong results
* Outages

---

# **2. How Flink performs a stateful upgrade**

Stateful upgrades are done using a **savepoint**, not a checkpoint.

### Typical steps:

### **Step 1: Trigger a savepoint**

You stop or suspend the job and generate a savepoint:

```
bin/flink stop <jobId> -p <savepoint-path>
```

or via REST API.

This savepoint contains:

* Operator/Keyed state
* Metadata
* Offsets (Kafka source’s position)

---

### **Step 2: Deploy new job version**

Change your code:

* New business logic
* Fixed bugs
* Added operators
* Changed state type (carefully)
* Changed parallelism

Flink allows you to evolve operators as long as:

* Operator UIDs remain consistent
* State schema evolution is compatible
* Parallelism changes follow Flink rules

---

### **Step 3: Restore from savepoint**

You launch the new job by pointing to the savepoint:

```
bin/flink run -s <savepoint-path> new-job.jar
```

The new job starts **from the exact same state** as previous version.

No data lost.
No duplicates.
No recomputation from start.

---

# **3. Why savepoints are required for stateful upgrades**

Checkpoints are not suitable for upgrades because:

* They are deleted automatically
* They are optimized for recovery, not portability
* They may not be compatible across versions
* They aren’t stable references

Savepoints, on the other hand:

* Are stable snapshots
* Are kept forever unless manually deleted
* Are portable across code versions
* Are designed for upgrades, migration, scaling

---

# **4. What is required for successful stateful upgrade?**

## **A. Stable Operator IDs (UIDs)**

Each operator must have a **fixed UID**.

Example:

```java
mapOp.uid("cleaning-map")
```

If UIDs change, Flink treats them as new operators → state cannot be restored → upgrade fails.

---

## **B. Compatible state schema**

If you change the type of the state (e.g., ValueState from int to string), Flink needs:

* State schema compatibility
* Or migration serializers
* Or manual transformations

---

## **C. Same partitioning**

KeyBy fields must be consistent.

Example:

Old job:

```
keyBy(user_id)
```

New job:

```
keyBy(device_id)
```

This breaks state compatibility and Flink prevents upgrade.

---

## **D. Parallelism rules**

You *can* change parallelism during upgrades.

Flink will:

* Redistribute keyed state across new #slots
* Migrate state partitions
* Maintain correctness

This is called **rescaling**.

---

# **5. Stateful Upgrade Examples**

## Example 1: Add a new field to event processing

Old job processed:

```
{ user_id, action }
```

New job adds:

```
{ user_id, action, device_type }
```

As long as UIDs are same and state serializer evolves correctly → upgrade works.

---

## Example 2: Change parallelism from 4 to 10

```
savepoint → restore with -p 10
```

Flink transparently repartitions the state for the new parallelism.

---

## Example 3: Upgrade business logic

Old:

```
reduce()
```

New:

```
reduce().map(newSanitizer)
```

Flink restores old state and applies new logic.

---

# **6. Stateful vs Stateless upgrades**

| Type              | Requires savepoint? | Can change parallelism? | Keeps state?   |
| ----------------- | ------------------- | ----------------------- | -------------- |
| Stateless upgrade | No                  | Yes                     | Not applicable |
| Stateful upgrade  | Yes                 | Yes                     | Yes            |

Most real pipelines (fraud detection, aggregations, CEP, joins, windows) require **stateful upgrades**.

---

# **7. What happens internally during stateful upgrade**

When restoring from savepoint:

1. Flink reads the metadata
2. Matches operator UIDs with new job graph
3. Loads state for each operator/key
4. Reassigns state to subtasks based on new parallelism
5. Initializes timers + windows
6. Connects Kafka sources starting from saved offsets
7. Starts processing from the exact previous point

This guarantees **exactly-once** with no downtime.

---

# **8. One-line Summary**

A **stateful upgrade** in Flink is deploying a new version of a streaming job while preserving all its state by restoring from a savepoint. It enables zero-downtime upgrades, parallelism changes, and safe evolution of long-running pipelines.