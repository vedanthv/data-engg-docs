# Partition Allocation Concepts in Kafka

---

## 1. The goal: balanced, fault-tolerant partition placement

When you create a topic in Kafka, you specify:

* **Number of partitions** (e.g., 10)
* **Replication factor** (e.g., 3)

This means:

> For each partition, Kafka needs to create 3 copies (replicas) — one leader and two followers.

So, 10 partitions × 3 replicas = **30 total partition replicas** to be distributed across the brokers.

In the example:

* Brokers = 6
* Partitions = 10
* Replication factor = 3
* Total replicas = 30

Kafka’s job is to **spread those 30 replicas across the 6 brokers** in a way that achieves:

1. Even distribution (no broker overloaded with replicas)
2. No duplicate replicas of the same partition on one broker
3. Rack-level fault tolerance (if rack info is available)

---

## 2. Step 1 — Even distribution across brokers

Kafka tries to assign **roughly the same number of replicas per broker**.

In the example:

* 30 replicas ÷ 6 brokers = **5 replicas per broker** (on average).

This ensures **load balance** — each broker holds approximately the same amount of data and handles similar traffic.

So, no single broker becomes a hotspot for storage or leader requests.

---

## 3. Step 2 — One replica per broker per partition

Kafka ensures that:

> For any given partition, its replicas (leader and followers) are placed on **different brokers**.

Example:

* Partition 0 leader → Broker 2
* Followers → Brokers 3 and 4

**Not allowed:**

* Two replicas of partition 0 on the same broker.
* Leader and follower on the same broker.

This guarantees that **if one broker fails**, at least one copy of each partition still exists on another broker.

---

## 4. Step 3 — Assigning partition leaders (round-robin)

Kafka determines which broker will hold the **leader replica** for each partition using a **round-robin approach.**

Example:

* Brokers: 0, 1, 2, 3, 4, 5
* Random starting broker: say **Broker 4**

Kafka loops over brokers in order to assign leaders:

| Partition | Leader Broker |
| --------- | ------------- |
| 0         | 4             |
| 1         | 5             |
| 2         | 0             |
| 3         | 1             |
| 4         | 2             |
| 5         | 3             |
| 6         | 4             |
| 7         | 5             |
| 8         | 0             |
| 9         | 1             |

This round-robin pattern keeps **leaders evenly distributed** across all brokers.

---

## 5. Step 4 — Assigning follower replicas

Once the leader brokers are chosen, Kafka assigns the **follower replicas**.

Rule:

> Each follower is placed on a broker at an *increasing offset* from the leader.

Example:

* Leader for partition 0 → Broker 4
  → Follower 1 on Broker 5
  → Follower 2 on Broker 0

* Leader for partition 1 → Broker 5
  → Follower 1 on Broker 0
  → Follower 2 on Broker 1

This ensures:

* Replicas are **spread across multiple brokers**.
* No two replicas of the same partition end up on the same node.

---

## 6. Step 5 — Rack awareness (added in Kafka 0.10.0+)

If your cluster defines **rack information** (for example, `broker.rack=rackA` in each broker’s config), Kafka can make smarter placement decisions.

### Why this matters

If an entire **rack** fails (for example, due to power or network outage), you don’t want all replicas of a partition to be on that rack — otherwise the partition becomes unavailable.

### How Kafka handles it

Instead of assigning brokers in numeric order (0, 1, 2, 3…), Kafka builds a **rack-alternating broker list**.

Example:

* Rack 1 → Brokers 0 and 1
* Rack 2 → Brokers 2 and 3

Normal order: 0, 1, 2, 3
Rack-alternating order: 0, 2, 1, 3

Now, if the leader for a partition is on broker 2 (rack 2):

* The first follower might be on broker 1 (rack 1).
* The second follower could be on broker 3 (rack 2) or broker 0 (rack 1), depending on the pattern.

Result:
✅ Each partition has replicas spread across **different racks**,
✅ So, if one rack goes down, there’s still a live replica on another rack.

This dramatically improves **fault tolerance** and **availability**.

---

## 7. Step 6 — Choosing the disk directory for each partition

Once the broker for each replica is chosen, Kafka decides **which disk (directory)** on that broker will store the partition.

This is where the `log.dirs` setting comes in.

Example:

```properties
log.dirs=/data1/kafka,/data2/kafka,/data3/kafka
```

Each path represents a mount point or disk.

Kafka uses a **simple rule**:

> Place the new partition on the directory that currently has the **fewest partitions**.

So if `/data3/kafka` is empty or least used, new partitions go there first.

### Why this helps

* Balances storage evenly across disks.
* If you add a new disk, Kafka automatically starts using it immediately because it initially has fewer partitions.
* This dynamic balancing happens **only during partition creation**, not for existing data (Kafka doesn’t move old partitions automatically).

---

## 8. Example end-to-end

Let’s put it all together.

**Cluster setup:**

* 6 brokers (0–5)
* 10 partitions
* Replication factor = 3
* Rack-aware placement enabled

**Resulting behavior:**

1. Kafka creates 30 replicas total.
2. Distributes leaders evenly among brokers.
3. Assigns followers at increasing broker offsets.
4. Ensures all replicas of a partition are on different brokers.
5. Uses rack info to ensure replicas are on different racks.
6. On each broker, assigns replicas to the disk (directory) with the fewest partitions.

This yields:
✅ Balanced leader load
✅ Balanced follower load
✅ Fault tolerance across brokers and racks
✅ Balanced use of storage disks

---

## 9. Why this matters

* **Performance:**
  Load is evenly distributed, so no broker or disk becomes a bottleneck.
* **Reliability:**
  Replicas on different brokers and racks protect against single points of failure.
* **Scalability:**
  Easy to add new brokers or disks — Kafka will place future partitions intelligently.
* **Simplicity:**
  Rules are deterministic and easy to reason about; administrators can predict where data will go.

---

## 10. Summary table

| Step | Goal                 | Mechanism                                       |
| ---- | -------------------- | ----------------------------------------------- |
| 1    | Even distribution    | Spread replicas evenly across brokers           |
| 2    | Avoid duplication    | No two replicas of same partition on one broker |
| 3    | Balanced leaders     | Assign leaders round-robin                      |
| 4    | Balanced followers   | Assign followers with offset placement          |
| 5    | Rack fault tolerance | Use rack-alternating broker list                |
| 6    | Disk balancing       | Assign to directory with fewest partitions      |

---

## 11. Key takeaway

When you create a topic, Kafka’s internal **partition assignment algorithm**:

* Ensures **balanced, resilient distribution** of data and leadership across brokers,
* Accounts for **rack-level redundancy** if available,
* And **balances disk usage** across available mount points.

This allows Kafka clusters to scale predictably and stay highly available even when disks, brokers, or entire racks fail.

---