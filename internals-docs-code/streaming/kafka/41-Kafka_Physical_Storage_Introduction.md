# Physical Storage in Kafka

Got it — let’s keep RAID short and focus mainly on what that passage about **Kafka’s storage architecture** means.

---

### 1. The core idea of the passage

The passage explains how **Kafka stores its data** on disk — specifically, how **partitions** and **replicas** are physically laid out and managed by brokers.

Kafka’s **basic storage unit** is a **partition replica**:

* Each **topic** is divided into **partitions**.
* Each **partition** has one or more **replicas** (copies), stored on different brokers for fault tolerance.
* Each broker stores **some replicas** on its local disks.

---

### 2. One partition replica = one storage location

* A **partition replica** cannot be split across multiple brokers or disks.
  → This means all the data for that partition’s replica sits entirely on **one mount point (disk location)**.
* Therefore, the **maximum size of a single partition** is limited by how much free space exists on one disk or one RAID volume.

---

### 3. Disks and mount points

A **mount point** is a storage path that Kafka can write data to.
Administrators can configure multiple mount points so Kafka can spread partitions across disks.

* If Kafka uses **JBOD (Just a Bunch Of Disks)** → each disk is a separate mount point.
* If Kafka uses **RAID** → multiple disks can act as one large logical mount point.

**Simple difference:**

* **JBOD:** each disk independent → lose partitions on that disk if it fails.
* **RAID:** combines disks into one logical volume → can survive certain disk failures depending on RAID level.

---

### 4. Kafka’s configuration — `log.dirs`

Kafka has a configuration parameter:

```properties
log.dirs=/data1/kafka,/data2/kafka,/data3/kafka
```

This tells the broker:

> “Here are the directories (mount points) where you can store partition data.”

Kafka automatically distributes partitions across these directories to balance disk usage.
This is **not** the same as `log4j.properties`, which controls where Kafka writes **error and system logs** (the broker’s own event logs).

---

### 5. How Kafka uses those directories

1. When a topic is created, Kafka’s controller assigns each partition to a broker.
2. On that broker, Kafka chooses **one directory from `log.dirs`** to place that partition’s data.
3. The partition data is stored as a **set of log segment files** and **index files** inside that directory.

So, each partition replica physically resides in a folder path like:

```
/data1/kafka/topicA-0
/data2/kafka/topicA-1
/data3/kafka/topicB-0
```

---

### 7. Brief note on RAID (as mentioned in the passage)

* **RAID (Redundant Array of Independent Disks)** = a way to combine multiple disks into one logical unit.
* Kafka can run on:

  * **JBOD:** separate disks per `log.dirs` (common setup; simpler for Kafka).
  * **RAID:** group of disks acting as one big mount point (used if you want redundancy at the storage level).

The passage just references RAID to explain what a “mount point” might represent — it could be:

* a single disk (JBOD), or
* a RAID array (multiple disks combined).

---

### 8. Summary (simple)

| Concept               | Meaning                                                                              |
| --------------------- | ------------------------------------------------------------------------------------ |
| **Partition replica** | Smallest unit of Kafka storage; one per broker per partition.                        |
| **No splitting**      | Each partition replica’s data stays on one disk/mount point only.                    |
| **`log.dirs`**        | List of directories (one per disk or RAID volume) where Kafka stores partition data. |
| **Mount point**       | A disk or RAID volume where data can be written.                                     |
| **RAID mention**      | Just an example that a mount point might represent multiple disks acting together.   |
| **Next topics**       | Allocation, file management, retention, and log compaction.                          |

---
