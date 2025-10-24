# Reliability Guarantees in Kafka

---

## 1. Reliability and Guarantees in Distributed Systems

When we discuss *reliability*, we are talking about **predictable and consistent behavior under failure**.
A *guarantee* means that no matter what happens (crashes, network issues, restarts), a system behaves in a way that conforms to certain well-defined rules.

In traditional databases, those guarantees are captured in the **ACID** model:

* **Atomicity:** Transactions are all-or-nothing.
* **Consistency:** Every transaction brings the database from one valid state to another valid state.
* **Isolation:** Concurrent transactions do not interfere with each other.
* **Durability:** Once a transaction is committed, it is permanent — it survives system failures.

Because these guarantees are strict and well understood, developers can design systems confidently. They know that if the database claims to be *ACID compliant*, they can safely assume certain behaviors during concurrent operations and failures.

---

## 2. Kafka’s Reliability Context

Kafka is not a database; it’s a **distributed streaming platform**. Its main responsibility is to ensure that **messages are delivered and ordered correctly**, even under distributed system failures.

Kafka provides a different set of guarantees compared to ACID, focused on **message ordering**, **durability**, and **delivery semantics** rather than transactional isolation or consistency constraints.

The reliability guarantees Kafka offers are **the foundation** upon which developers can design fault-tolerant streaming systems.

---

## 3. Kafka’s Core Guarantees

### a) Ordering Guarantee

Kafka guarantees **message order within a partition**.

If message **B** is produced after message **A** by the same producer to the same partition, Kafka ensures:

* The **offset** of message B > offset of message A.
* Consumers reading that partition will always read message A before message B.

This is a **per-partition guarantee** — there is no ordering guarantee *across* partitions of a topic.

This guarantee allows you to process data sequentially within a logical key (e.g., all updates for a single customer ID).

---

### b) Commit Guarantee

A message is considered **committed** when it is successfully written to the partition’s **leader** and **replicated to all in-sync replicas (ISRs)**.

However, *committed* does **not** necessarily mean “flushed to disk.” Kafka may temporarily hold data in memory buffers and rely on replication for durability between brokers.

Kafka allows the producer to configure **when** it receives an acknowledgment that a message is successfully written, through the `acks` parameter:

| `acks` Value            | Meaning                                      | Reliability | Latency |
| ----------------------- | -------------------------------------------- | ----------- | ------- |
| `acks=0`                | Producer doesn’t wait for any acknowledgment | Lowest      | Lowest  |
| `acks=1`                | Wait for leader to write message             | Medium      | Medium  |
| `acks=all` or `acks=-1` | Wait for all in-sync replicas to confirm     | Highest     | Highest |

Thus, **the developer controls the trade-off** between latency and durability.

---

### c) Durability Guarantee

Kafka guarantees that **committed messages will not be lost** as long as **at least one in-sync replica** remains alive.

This is because each partition has multiple replicas stored across different brokers.
If the leader broker fails, one of the in-sync replicas is automatically promoted to leader, ensuring the data remains available and consistent.

However, durability also depends on configurations like:

* `min.insync.replicas` (minimum number of replicas that must acknowledge a write)
* `replication.factor` (total number of replicas)
* `acks` (producer acknowledgment level)

---

### d) Consumer Visibility Guarantee

Consumers can **only read committed messages**.
That means they never see messages that were written to the leader but not yet replicated to all in-sync replicas.

This ensures that consumers do not process messages that could be lost if a leader failure happens before replication completes.

---

## 4. Reliability is Configurable in Kafka

Kafka was designed to **allow operators and developers to tune the reliability–performance balance**.
Unlike traditional databases that enforce ACID behavior by design, Kafka exposes configuration parameters so you can decide:

* How much you value **data consistency** versus **availability**
* How much **latency** you are willing to trade for **durability**
* How much **hardware replication** you can afford

For example:

* If you prioritize durability, you’d use `acks=all`, `min.insync.replicas=2`, and a replication factor of 3.
* If you prioritize throughput and can tolerate some loss, you might use `acks=1` or even `acks=0`.

This flexibility lets Kafka be used in both **critical financial systems** and **high-speed telemetry pipelines**, depending on what reliability trade-offs are acceptable.

---

## 5. Summary of Kafka’s Reliability Guarantees

| Guarantee Type    | Description                                                            | Notes                                               |
| ----------------- | ---------------------------------------------------------------------- | --------------------------------------------------- |
| **Ordering**      | Messages in a partition are read in the same order they were written   | No global ordering across partitions                |
| **Commit**        | Message considered committed after all in-sync replicas acknowledge it | Configurable via `acks`                             |
| **Durability**    | Committed messages are not lost as long as one replica is alive        | Depends on replication factor and ISR configuration |
| **Consumer Read** | Consumers only read committed messages                                 | Prevents reading unreplicated (unsafe) data         |

---

## 6. The Trade-Offs

Kafka’s reliability model is not absolute — it’s **tunable**.

You trade between:

* **Reliability (durability, consistency)**
* **Availability (system continues serving clients during failures)**
* **Performance (throughput and latency)**
* **Cost (more replicas mean more storage and network overhead)**

This flexibility is what makes Kafka powerful but also requires developers to understand the guarantees deeply.
If you understand how Kafka behaves under different failure scenarios, you can configure it to meet your specific reliability goals.

---

### Final Summary

Kafka provides strong but configurable guarantees:

1. Ordered delivery within partitions
2. Committed message durability across in-sync replicas
3. Safe consumer reads (no uncommitted data exposure)
4. Adjustable trade-offs between reliability, latency, and cost

Unlike databases with rigid ACID guarantees, Kafka’s model gives you the tools to **decide** how much reliability your application requires — and to build systems that behave predictably under failure once those configurations are set.
