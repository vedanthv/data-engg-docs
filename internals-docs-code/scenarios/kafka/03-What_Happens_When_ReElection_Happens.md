# What happens when a relection happens and how is idempotency still preserved?

---

## 1. The situation: a leader re-election happens

Let’s start with what causes this.

A **leader re-election** occurs when the broker currently leading a partition:

* Crashes,
* Is shut down,
* Loses connection,
* Or is demoted by the controller.

Then, one of the **in-sync replicas (ISR)** becomes the new leader.

So now:

* Old leader = **broker A** (down)
* New leader = **broker B**

---

## 2. What happens to producer writes in flight?

Suppose a producer was sending messages to **partition P0**, which had **leader = broker A**.

Before broker A crashed:

* The producer sent batches with sequence numbers 100–109.
* Some of them were acknowledged.
* Some were still in-flight (not acknowledged yet).

Now broker A goes down, broker B becomes the leader.

The question is:

> How does broker B know what the last sequence number was for this producer, so it can continue correctly and not write duplicates?

---

## 3. The challenge

* Producer’s **idempotence** relies on `(ProducerID, Partition, Sequence)` tracking.
* The **old leader (broker A)** kept an in-memory table tracking this information:

  ```
  PID 1234 → last sequence 109
  ```
* But broker A just failed.
  The new leader (broker B) **doesn’t have that in memory**.

So, how does broker B know where to continue?

---

## 4. The solution — **Leader Epoch and Log Recovery**

When a new leader is elected, it does **log recovery** based on **leader epochs**.

Let’s unpack these two important ideas.

---

### a. **Leader Epoch**

Each time a new leader is elected for a partition, Kafka increments the **leader epoch** (a small integer counter).

This number identifies “who was leader when this data was written”.

Example:

| Epoch | Leader Broker | Description       |
| ----- | ------------- | ----------------- |
| 0     | Broker A      | Original leader   |
| 1     | Broker B      | After re-election |
| 2     | Broker C      | Next re-election  |

Every log entry on disk includes its **leader epoch**, so when replicas sync, they can tell which messages were written by which leader.

This is part of the batch header:

```
LeaderEpoch: 7
```

---

### b. **Log Recovery and Truncation**

When a new leader (say broker B) takes over, it:

1. Loads the partition log from disk.
2. Uses the last known committed offsets and leader epochs to **truncate** any uncommitted or divergent messages.
3. Ensures the log is consistent with the rest of the in-sync replicas.

So, when broker B becomes leader, it knows exactly which messages are truly committed.

This guarantees that **the new leader’s log is identical** to what all in-sync replicas have.

---

## 5. Producer recovery after leader failover

Now, back to the producer.

After broker A fails:

1. The producer keeps retrying (because `acks=all` or `retries > 0`).
2. It gets a **NotLeaderForPartition** error from a broker (meaning “the leader changed”).
3. The producer then fetches new **metadata** from Kafka and learns that **broker B** is now the leader.
4. It resends its next message batches to broker B.

---

## 6. How the new leader validates sequence numbers

Broker B (the new leader) looks at the incoming batch:

* `(PID=1234, seq=100–109, epoch=E1)`

Broker B maintains **producer state** on disk, stored inside the partition’s log.
When it became leader, it **rebuilt** this state from the log segments (the “producer state snapshot”).

So it knows the **latest acknowledged sequence** for each producer.

Example:

```
PID=1234, lastSeq=109, epoch=E1
```

Now if the producer retries an old batch (sequence 100–109),
broker B detects:

> “These sequence numbers are <= last seen → duplicates → ignore.”

If the producer sends a new batch (seq=110–119),
broker B appends them as expected.

✅ Result:

* Duplicates avoided
* Order preserved
* Producer resumes seamlessly after leader re-election

---

## 7. What if the producer itself restarts after failover?

If the producer crashes and restarts, it loses its local sequence counters.

That’s where the **producer epoch** comes in.

### Producer Epoch = version number for the producer session.

Each time a producer with the same `transactional.id` restarts:

* The **transaction coordinator** assigns it a **new producer epoch**.
* The new epoch signals to brokers that this is a **new session**.

Brokers then:

* Accept messages from the new epoch,
* Reject any late or duplicate messages from old epochs.

So, if an old batch (epoch=1) arrives after a restart (new epoch=2), the broker discards it.

---

## 8. How all these pieces fit together

| Mechanism                   | Controlled by                   | Purpose                                               |
| --------------------------- | ------------------------------- | ----------------------------------------------------- |
| **Producer ID (PID)**       | Broker assigns                  | Identifies producer instance                          |
| **Sequence numbers**        | Producer assigns                | Ordered numbering of messages per partition           |
| **Producer epoch**          | Broker increments               | Distinguishes new producer session after restart      |
| **Leader epoch**            | Broker increments per partition | Distinguishes new partition leader during re-election |
| **Producer state snapshot** | Broker (on disk)                | Tracks last sequence for each PID                     |
| **Log truncation**          | New leader broker               | Removes uncommitted data from previous leader         |
| **Metadata refresh**        | Producer                        | Learns new leader after failover                      |

Together, these ensure that **idempotence** and **exactly-once semantics** remain intact even across leader failures.

---

## 9. Step-by-step: EOS through leader failover

Let’s walk through a real example.

| Step | Action                                 | What Happens                                      |
| ---- | -------------------------------------- | ------------------------------------------------- |
| 1    | Broker A is leader                     | Producer sends (PID=1234, seq=100–109)            |
| 2    | Broker A crashes mid-write             | Some messages written, some pending               |
| 3    | Broker B becomes leader                | Rebuilds state, truncates uncommitted data        |
| 4    | Producer retries batch                 | Still uses (PID=1234, seq=100–109)                |
| 5    | Broker B checks snapshot               | Sees duplicates → ignores                         |
| 6    | Producer sends new batch (seq=110–119) | Broker B accepts and appends                      |
| ✅    | **Result**                             | No duplicates, no lost messages, consistent order |

---

## 10. Summary: Kafka’s idempotence + leader epochs

| Concept                     | Description                          | Role in EOS                                    |
| --------------------------- | ------------------------------------ | ---------------------------------------------- |
| **Producer ID (PID)**       | Unique ID per producer               | Identify source of messages                    |
| **Sequence Number**         | Increment per partition              | Detect duplicates, maintain order              |
| **Producer Epoch**          | Increment per restart                | Ignore stale messages after restart            |
| **Leader Epoch**            | Increment per leader re-election     | Ensure log consistency after failover          |
| **Producer State Snapshot** | Stored on broker                     | Recover last sequence after failover           |
| **Retry behavior**          | Retains same sequence for same batch | Prevent duplicates across retries or failovers |

---

✅ **In short:**

* **Offsets** are still assigned by the broker.
* **Sequence numbers** are assigned by the producer.
* When the leader changes, the new leader rebuilds its **producer state** from the log and uses the **leader epoch** to stay consistent.
* If the producer retries the same batch, the **sequence numbers remain the same**, and the new leader detects duplicates and discards them.
* **Producer epoch** protects against old messages from previous producer sessions.

Together, this combination of **PID**, **sequence numbers**, **producer epoch**, and **leader epoch** allows Kafka to maintain **exactly-once semantics** — even across **broker failovers and leader re-elections**.

---