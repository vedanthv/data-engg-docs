# Checkpoints and Savepoints in Flink\

Here is the clearest and most complete explanation of **checkpoints vs savepoints in Flink** — one of the most important topics for real-time systems and interviews.

---

# **1. What are checkpoints in Flink?**

A **checkpoint** is an **automatic, periodic, lightweight snapshot** of the job’s state.

Flink uses checkpoints to recover from failures **without data loss**.

### Key characteristics of checkpoints:

* Triggered **automatically** (e.g., every 1 minute)
* Managed by **the Job Manager**
* Used for **fault recovery**, not for stopping jobs
* Taken while the job is running continuously
* Stored in checkpoint storage (S3, HDFS, etc.)
* Flink automatically deletes old checkpoints

### Purpose:

**Recover the job automatically after failures with exactly-once guarantees.**

### Example:

If your job crashes at 12:05 and last checkpoint was at 12:04:

* Job restarts from the 12:04 checkpoint
* No double-processing
* No lost data

---

# **2. How checkpoints work (simplified)**

1. Job Manager triggers a checkpoint
2. All Task Managers snapshot their operator and keyed state
3. Snapshot goes to durable storage (S3, HDFS)
4. Offsets/positions in Kafka/file sources are also saved
5. When failure happens, Flink restores from this snapshot

This ensures **exactly-once** consistency.

---

# **3. What are savepoints in Flink?**

A **savepoint** is a **manual, intentional snapshot** of the job’s state.

It is triggered by the user, not the system.

### Key characteristics of savepoints:

* Triggered manually (CLI, REST API)
* Used for **job upgrades, migrations, changes**
* Stable and long-lived
* Stored wherever you choose
* Not automatically deleted
* Internally similar to checkpoints, but more portable and versioned
* Might be larger/heavier than checkpoints

### Purpose:

**Perform controlled upgrades, rescaling, or moves of a Flink job without losing state.**

---

# **4. Why savepoints exist**

Kafka consumers, Flink jobs, and streaming pipelines often need upgrading:

* New code
* New logic
* New parallelism
* Migrating to a new cluster
* Patching bugs

You cannot rely on automatic checkpoints for this because checkpoints are:

* Not stable
* Deleted automatically
* Not intended for upgrades
* Not portable between versions sometimes

Savepoints are **explicit snapshots that the user manages**.

---

# **5. Key differences between checkpoints and savepoints**

| Feature              | Checkpoint                   | Savepoint                       |
| -------------------- | ---------------------------- | ------------------------------- |
| Triggered by         | Flink (automatic)            | User (manual)                   |
| Purpose              | Fault recovery               | Upgrades & maintenance          |
| Retention            | Automatically cleaned        | Must be preserved manually      |
| Frequency            | Regular (e.g., every minute) | Occasional                      |
| Portability          | Not guaranteed               | More portable                   |
| Job stopping needed? | No                           | Often yes (stop-with-savepoint) |
| Can resume job?      | Yes                          | Yes (recommended for upgrades)  |

---

# **6. When do you use each?**

### Use **checkpoints** for:

* Automatic failure recovery
* Exactly-once guarantees
* Continuous stability

### Use **savepoints** for:

* Deploying new versions of the pipeline
* Changing parallelism
* Migrating clusters
* Debugging production jobs
* Pausing a job for maintenance

---

# **7. Example workflows**

### **A. Failure recovery**

Job fails → Automatically restarts → Loads last **checkpoint**

### **B. Code upgrade with state preservation**

```
1. Stop job with savepoint
2. Deploy new code
3. Restore from savepoint
```

### **C. Rescale a job**

```
savepoint → restore with new parallelism
```

This moves state partitions to the new number of Task Managers/slots.

---

# **8. One-line summary**

* **Checkpoint** = automatic, frequent, lightweight snapshots for **fault recovery**
* **Savepoint** = manual, durable snapshot for **upgrades, rescaling, and controlled restarts**

---