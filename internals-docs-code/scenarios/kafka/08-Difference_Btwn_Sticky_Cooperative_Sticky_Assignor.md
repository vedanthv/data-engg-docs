# What is the difference between Sticky Assignor and Cooperative Sticky Assignor?

---

## StickyAssignor vs CooperativeStickyAssignor

### 1. Conceptual Overview

Kafka uses *assignors* to decide which consumer in a group will read from which partitions.
When group membership changes (a consumer joins or leaves), Kafka performs a **rebalance**, redistributing partitions among consumers.

Two common assignors are:

| Assignor                    | Type        | Goal                                                  | Rebalance Style           |
| --------------------------- | ----------- | ----------------------------------------------------- | ------------------------- |
| `StickyAssignor`            | Eager       | Minimize partition movement (keep assignments stable) | Eager (stop-the-world)    |
| `CooperativeStickyAssignor` | Cooperative | Same goal, but with smoother rebalances               | Incremental (cooperative) |

---

### 2. How They Work

#### a) StickyAssignor

* **Purpose:** Keeps partition assignments as stable as possible across rebalances.
* **Rebalance type:** *Eager*.

  * All consumers in the group must stop processing.
  * Every partition is revoked from all consumers.
  * After that, partitions are reassigned — possibly to the same consumers as before, but only after all were stopped.
* **Drawback:** Causes noticeable pauses in consumption because it’s a stop-the-world rebalance.

**Example:**
Assume three consumers: C1, C2, and C3, each consuming two partitions.
If C3 leaves, Kafka revokes all partitions from all consumers, pauses processing, and then redistributes all six partitions.
Even if C1 and C2 get back the same partitions, there was a full pause.

---

#### b) CooperativeStickyAssignor

* **Purpose:** Same stickiness as `StickyAssignor`, but rebalances happen more smoothly.
* **Rebalance type:** *Incremental* or *cooperative*.

  * Only the partitions that must move are revoked.
  * Other partitions stay assigned, so consumers can keep processing most of their workload.
* **Benefit:** Dramatically reduces pause time and improves overall availability during rebalances.

**Example:**
With the same setup (C1, C2, C3), if C3 leaves, Kafka only reassigns the two partitions that C3 owned.
C1 and C2 continue processing their existing partitions without interruption.

---

### 3. Analogy

Imagine three kids sharing toy cars.

**StickyAssignor:**
When one kid leaves, the teacher says:
“All of you put your cars back in the box. Now we’ll redistribute them.”
Everyone must stop playing, even if they get back the same cars.

**CooperativeStickyAssignor:**
When one kid leaves, the teacher says:
“Only take the cars from the kid who left. Everyone else can keep theirs.”
The game continues almost uninterrupted.

---

### 4. Configuration

You choose the assignor using the `partition.assignment.strategy` property in your consumer configuration.

```properties
# Eager rebalancing
partition.assignment.strategy=org.apache.kafka.clients.consumer.StickyAssignor

# Incremental rebalancing (recommended)
partition.assignment.strategy=org.apache.kafka.clients.consumer.CooperativeStickyAssignor
```

Modern Kafka clients (version 2.4 and later) support `CooperativeStickyAssignor`,
and it is the preferred choice because it minimizes rebalance interruptions.

---

### 5. Summary Table

| Feature              | StickyAssignor          | CooperativeStickyAssignor         |
| -------------------- | ----------------------- | --------------------------------- |
| Goal                 | Keep assignments stable | Same goal                         |
| Rebalance Type       | Eager (stop-the-world)  | Incremental (cooperative)         |
| Partition Revocation | All partitions          | Only those that need reassignment |
| Processing Pause     | High                    | Minimal                           |
| Introduced In        | Kafka 0.11              | Kafka 2.4                         |
| Recommended For      | Legacy setups           | Most modern deployments           |

---