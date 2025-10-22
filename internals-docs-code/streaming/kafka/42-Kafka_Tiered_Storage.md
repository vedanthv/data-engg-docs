# Tiered Storage in Kafka

---

## 1. Why Kafka needed tiered storage

Before tiered storage, **Kafka stored all data locally** on broker disks. This worked well for moderate retention, but created **hard limits** when Kafka was used for high-throughput or long-retention use cases.

### Problems with local-only storage

#### a. **Storage capacity limits**

* Each partition replica resides on a single broker and cannot be split across disks.
* The partition size is therefore limited by **the disk size of a single mount point**.
* If a team wanted to retain weeks or months of data, Kafka’s local disks often filled up quickly.

#### b. **Cost inefficiency**

* To increase storage, you had to add **more brokers**, even if CPU and memory were underutilized.
* This made Kafka clusters **larger and more expensive** than necessary, since scaling storage required scaling compute too.

#### c. **Low elasticity**

* When scaling up or down (e.g., adding/removing brokers), moving large partitions between brokers took a long time.
* Kafka rebalance and recovery operations were **slower** because huge amounts of data had to be copied between nodes.

#### d. **External pipelines**

* Organizations often created additional pipelines to offload old Kafka data to cheaper storage (e.g., S3, HDFS).
* This duplicated infrastructure and increased operational complexity.

So Kafka needed a way to:
✅ Keep recent, “hot” data close to the broker for low-latency access.
✅ Offload older, “cold” data to cheaper and more scalable storage.
✅ Do this transparently, without breaking existing clients or APIs.

That’s what **Tiered Storage** provides.

---

# 2. What is Tiered Storage in Kafka?

**Tiered storage** introduces a **two-layer (dual-tier)** architecture for Kafka logs:

| Tier            | Description                                  | Typical storage type          | Purpose                                |
| --------------- | -------------------------------------------- | ----------------------------- | -------------------------------------- |
| **Local Tier**  | Existing Kafka storage on local broker disks | SSDs or HDDs                  | For hot, recent data; low latency      |
| **Remote Tier** | New, external long-term storage              | S3, HDFS, or cloud blob store | For older, cold data; cheap & scalable |

### In simple terms:

Kafka keeps **recent segments** locally (fast disk),
and **older, completed segments** are uploaded to **remote storage**.

This allows Kafka to behave both as a **high-performance message broker** and a **long-term event store** — without separate data pipelines.

---

# 3. How it works

### a. Log segments

* Kafka stores each partition’s data as a series of **log segments** (files).
* As the partition grows, older segments are **rolled over** (closed) and new ones are started.

### b. Remote offloading

* Once a segment is closed (no new messages are appended), Kafka can **upload it** to the remote tier (e.g., S3 or HDFS).
* The local copy can then be **retained for a shorter time** and eventually deleted based on local retention policy.

### c. Dual retention policies

You can define **different retention policies** for the two tiers:

* **Local retention:** how long segments stay on broker disk (e.g., a few hours).
* **Remote retention:** how long segments stay in the remote tier (e.g., days, months, or indefinitely).

This means brokers maintain only the **active** tail of the log locally, while the remote tier keeps **historical** data for long-term access.

---

# 4. Accessing data from both tiers

Kafka abstracts both storage layers under the same log interface.

* **Consumers reading recent data (tail reads)**
  → Served from **local tier** (fast disk I/O and page cache).
  These are typically real-time stream processors or dashboards.

* **Consumers reading older data (backfill or reprocessing)**
  → Served from **remote tier** (fetched over the network from S3/HDFS).
  These are typically analytics, ETL, or replay jobs.

The switch between local and remote is **transparent** — clients don’t need to know where the data physically lives.

---

# 5. Components introduced by Tiered Storage

### **a. RemoteLogManager**

A new internal Kafka component introduced in KIP-405.
It handles:

* Tracking which log segments have been uploaded.
* Coordinating uploads, downloads, and deletions of remote segments.
* Integrating with retention policies for both tiers.

Each broker runs a **RemoteLogManager** to manage the remote copies of segments it owns as leader.

---

### **b. Remote Storage Connector (plugin layer)**

Kafka uses a **pluggable interface** to talk to various remote systems.
For example:

* AWS S3 connector
* HDFS connector
* Azure Blob connector

These connectors implement how to **upload**, **download**, **list**, and **delete** log segments.

---

### **c. Metadata tracking**

Kafka must keep track of:

* Which segments exist locally,
* Which are in remote storage,
* And which offsets correspond to each.

This metadata is replicated via the **Kafka controller and metadata topic**, ensuring consistency across brokers.

---

# 6. Benefits of Tiered Storage

### **1. Infinite (practically) retention**

* Because old data is offloaded, retention is no longer constrained by broker disk size.
* You can store **months or years** of data at a fraction of the cost.

### **2. Lower cost per GB**

* Brokers only need fast storage for recent data.
* Older data can live in cheaper cloud object storage (S3, GCS, Azure Blob, HDFS).

### **3. Independent scaling**

* Storage can now scale **independently** from compute.
* You can add capacity to S3 without adding brokers.

### **4. Faster elasticity and recovery**

* Rebalancing or replacing brokers becomes much faster:

  * Old segments already in remote storage don’t need to be copied again.
  * Brokers only rebuild metadata and local active segments.

### **5. Isolation between workloads**

* Previously, **consumers reading old data** competed with **real-time consumers** for disk I/O.
* With tiered storage:

  * Old reads → remote storage (network I/O)
  * New reads → local disk
* Result: better latency isolation and less interference between workloads.

### **6. Simplified architecture**

* No need for separate ETL pipelines to move data from Kafka to S3 or HDFS.
* Kafka itself becomes a **complete event store**.

---

# 7. Performance impact (based on KIP-405 measurements)

The Kafka team tested tiered storage in several workloads:

| Use Case                            | Without Tiered Storage | With Tiered Storage | Observation                                                                                            |
| ----------------------------------- | ---------------------- | ------------------- | ------------------------------------------------------------------------------------------------------ |
| **Normal high-throughput workload** | p99 latency ≈ 21 ms    | p99 latency ≈ 25 ms | Slight latency increase due to background uploads to remote storage.                                   |
| **Consumers reading old data**      | p99 latency ≈ 60 ms    | p99 latency ≈ 42 ms | Significant improvement because old reads come from remote storage, not competing with hot disk reads. |

So even though there’s a small penalty for offloading, the **overall cluster performance improves** for mixed workloads.

---

# 8. Trade-offs and considerations

| Aspect            | Notes                                                                                                          |
| ----------------- | -------------------------------------------------------------------------------------------------------------- |
| **Latency**       | Slightly higher due to remote fetch for old data, but negligible for most use cases.                           |
| **Complexity**    | Additional moving parts (RemoteLogManager, remote connectors, new metadata tracking).                          |
| **Network usage** | Uploading/downloading segments adds bandwidth requirements.                                                    |
| **Consistency**   | Remote segment metadata must stay consistent during leader changes and replica catch-up.                       |
| **Cost**          | Remote storage is cheaper per GB, but total cost depends on egress and API call pricing in cloud environments. |

---

# 9. Comparison: Before vs After Tiered Storage

| Feature               | Pre-Tiered Storage               | With Tiered Storage                              |
| --------------------- | -------------------------------- | ------------------------------------------------ |
| Storage               | Entirely local                   | Split: local + remote                            |
| Retention             | Limited by disk                  | Practically unlimited                            |
| Scaling               | Add brokers for more storage     | Scale storage separately (e.g., add S3 capacity) |
| Broker recovery       | Copies all data                  | Copies only local data, references remote        |
| Cost efficiency       | High cost per TB                 | Low cost per TB (cheap cloud storage)            |
| Performance isolation | Old readers compete for disk I/O | Old readers use remote storage, no competition   |

---

# 10. Key takeaway

Tiered storage transforms Kafka from a **short-term streaming buffer** into a **long-term, cost-efficient event store**.

It provides:
✅ Infinite retention (practically)
✅ Lower storage cost
✅ Easier scaling and faster recovery
✅ Isolation between real-time and historical consumers
✅ Seamless access to historical data

All while maintaining Kafka’s **same client APIs** and **streaming semantics**.

---

# 11. Analogy

Think of Kafka Tiered Storage like your phone’s photo library:

* **Recent photos** → stored locally on your phone (fast, small).
* **Old photos** → automatically moved to cloud storage (cheap, large).
  You can still view any photo seamlessly — the system just fetches it from the right place when needed.

Kafka’s tiered storage works the same way for log segments.

---

# 12. Summary

| Concept           | Description                                                       |
| ----------------- | ----------------------------------------------------------------- |
| **Motivation**    | Overcome storage limits, reduce cost, improve elasticity.         |
| **Architecture**  | Two tiers — local (fast disks) and remote (cheap, scalable).      |
| **New component** | `RemoteLogManager` manages uploads, downloads, metadata.          |
| **Retention**     | Separate policies for local and remote tiers.                     |
| **Performance**   | Slight latency increase for writes, improved isolation for reads. |
| **Benefit**       | Kafka becomes a long-term, scalable, cost-effective event store.  |

---

One interesting result that is documented in KIP-405 is the performance implications of tiered storage. The team implementing tiered storage measured performance in several use cases. The first was using Kafka’s usual highthroughput workload. In that case, latency increased a bit (from 21 ms in p99 to 25 ms), since brokers also have to ship segments to remote storage. The second use case was when some consumers are reading old data. 

Without tiered storage, consumers reading old data have a large impact on latency (21 ms versus 60 ms p99), but with tiered storage enabled, the impact is significantly lower (25 ms versus 42 ms p99); this is because tiered storage reads are read from HDFS or S3 via a network path. Network reads do not compete with local reads on disk I/O or page cache, and leave the page cache intact with fresh data. This means that in addition to infinite storage, lower costs, and elasticity, tiered storage also delivers isolation between historical reads and real-time reads.
