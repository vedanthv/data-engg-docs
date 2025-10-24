# Broker Configuration in Kafka : Replication Factor

All the below mentioned configurations can be applied to topic level as well to control reliability trade offs not only at broker but topic level.

## Replication Factor

The topic-level configuration is replication.factor. At the broker level, we control the default.replication.factor for automatically created topics. Until this point in the book, we have assumed that topics had a replication factor of three, meaning that each partition is replicated three times on three different brokers.

This was a reasonable assumption, as this is Kafka’s default, but this is a configuration that users can modify. Even after a topic exists, we can choose to add or remove replicas and thereby modify the replication factor using Kafka’s replica assignment tool. 

A replication factor of N allows us to lose N-1 brokers while still being able to read and write data to the topic. So a higher replication factor leads to higher availability, higher reliability, and fewer disasters. On the flip side, for a replication factor of N, we will need at least N brokers and we will store N copies of the data, meaning we will need N times as much disk space. We are basically trading availability for hardware.

### Detemining Right Number of Replicas

---

## 1. Availability

**Definition:**
Availability refers to the ability of Kafka to continue serving client requests (producing and consuming messages) even when some brokers fail.

**Explanation:**

* If a partition has **only one replica**, it exists on a single broker.
* During a routine broker restart (for maintenance, software update, or crash recovery), that partition becomes unavailable, since there is no other copy.
* Producers cannot write to it, and consumers cannot read from it until the broker comes back online.

**Key Point:**

* Adding more replicas improves availability.
* If one broker fails, Kafka can elect another in-sync replica (ISR) as the new leader, and the partition remains available.

**Rule of Thumb:**

* A replication factor of **3** is generally recommended for production workloads.
  This allows Kafka to tolerate the failure of one broker and still maintain a second replica for redundancy.

---

## 2. Durability

**Definition:**
Durability is the guarantee that once data is acknowledged as committed, it will not be lost — even if brokers fail or disks crash.

**Explanation:**

* Each replica stores a **complete copy** of the partition data.
* If there is only one replica and that broker’s disk becomes corrupted or unavailable, **all data in that partition is lost permanently.**
* With multiple replicas on different brokers (and ideally different physical disks or racks), the likelihood that *all* replicas fail simultaneously is drastically reduced.

**Key Point:**

* More replicas → higher durability.
* Replicas spread across fault domains (different servers, racks, or availability zones) provide much stronger fault tolerance.

---

## 3. Throughput

**Definition:**
Throughput is the rate at which Kafka can handle incoming and outgoing data (measured in MBps or messages per second).

**Explanation:**

* Each additional replica adds replication traffic between brokers.
* The leader must send the same data to every follower replica to keep them synchronized.

**Example:**

* If producers write at **10 MBps**:

  * With **1 replica**, there is **no replication traffic** (no extra copies).
  * With **2 replicas**, there is **10 MBps** of replication traffic (leader → follower).
  * With **3 replicas**, there is **20 MBps** of replication traffic.
  * With **5 replicas**, there is **40 MBps** of replication traffic.

**Impact:**

* Higher replication factors increase inter-broker network usage and disk I/O.
* This means you must size your network bandwidth and storage throughput accordingly when planning the cluster.

**Key Point:**

* There’s a direct trade-off between durability (more replicas) and throughput (less replication traffic overhead).

---

## 4. End-to-End Latency

**Definition:**
Latency is the time it takes for a produced message to become visible and readable by consumers.

**Explanation:**

* Kafka considers a message **committed** only after it has been replicated to **all in-sync replicas** (ISRs).
* More replicas mean more acknowledgments required before the message is marked committed.
* If any one replica is slow (due to disk or network lag), it delays acknowledgment for that message.
* This, in turn, delays when the consumer can read it.

**In Practice:**

* Usually, slow replicas are rare and localized issues.
* Even a single slow broker can affect latency, regardless of replication factor, since any client communicating with it will experience delays.

**Key Point:**

* More replicas **may slightly increase latency**, but in a well-tuned cluster, this impact is usually small compared to the benefit in durability.

---

## 5. Cost

**Definition:**
Cost refers to the additional **storage**, **network**, and **infrastructure** resources required for replication.

**Explanation:**

* Each replica is a **full copy** of the partition data.
* A replication factor of 3 means **triple the storage** compared to a single replica.
* It also means more network bandwidth for replication traffic and more disk writes.

**Practical Considerations:**

* Some administrators reduce replication factor to **2** for non-critical topics to save costs.
* However, this lowers availability because the system can only tolerate one broker failure without data unavailability.
* In some environments, the underlying storage system (for example, cloud block storage or distributed file systems) already replicates data three times at the hardware level.

  * In such cases, setting Kafka’s replication factor to **2** can be a reasonable compromise — the **durability** is still guaranteed by the storage layer, even if **availability** is slightly lower.

**Key Point:**

* Cost scales directly with replication factor.
* A higher replication factor gives stronger reliability at the expense of more infrastructure cost.

---

## 6. The Trade-off Summary

| Factor           | Effect of Increasing Replication Factor | Reason                                        |
| ---------------- | --------------------------------------- | --------------------------------------------- |
| **Availability** | Increases                               | More replicas → more backup leaders available |
| **Durability**   | Increases                               | Data stored on multiple disks/nodes           |
| **Throughput**   | Decreases                               | More inter-broker replication traffic         |
| **Latency**      | Slightly increases                      | Must wait for all ISRs to acknowledge         |
| **Cost**         | Increases                               | More storage and bandwidth required           |

---

## 7. Typical Recommendations

| Use Case                         | Recommended Replication Factor | Rationale                                          |
| -------------------------------- | ------------------------------ | -------------------------------------------------- |
| **Production, critical data**    | 3                              | Balances durability, availability, and performance |
| **Non-critical, transient data** | 2                              | Reduces cost while maintaining basic redundancy    |
| **Testing / development**        | 1                              | Simplifies setup, no fault tolerance required      |

---

### Final Summary

Kafka replication is a trade-off mechanism.
It directly determines how reliable, available, and performant your system will be.

* **More replicas** improve fault tolerance (availability, durability).
* **Fewer replicas** improve efficiency (throughput, cost).

Choosing the right replication factor depends on **how critical the data is** and **how much resource cost you can afford**.
In most real-world production clusters, a replication factor of **3** is considered the optimal balance between safety, performance, and cost.