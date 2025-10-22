# Does Sequence Number Remain the same for a message if producer sends it again to same partition?

Excellent — this is a very precise and important question.

The short answer is:

> ✅ **Yes.**
> If a producer retries sending the *same message batch* to the *same partition*, it uses the **same sequence numbers** for those messages.

And that’s **exactly how Kafka’s idempotence mechanism** detects and prevents duplicates.

Let’s unpack this in detail so you understand why, how, and what happens internally.

---

## 1. Quick recap: sequence numbers in Kafka

When **idempotence** is enabled (`enable.idempotence=true`, which is default since Kafka 3.0), every producer instance is assigned:

| Field                 | Description                                                          |
| --------------------- | -------------------------------------------------------------------- |
| **Producer ID (PID)** | A unique 64-bit ID assigned by the broker when the producer starts.  |
| **Sequence number**   | A monotonically increasing integer per `(producer, partition)` pair. |
| **Producer epoch**    | A number incremented each time the producer restarts or recovers.    |

Each partition that a producer writes to has its **own independent sequence counter**.

---

## 2. How sequence numbers are assigned

Every time the producer sends a message (or batch of messages) to a partition, it assigns sequence numbers to those records:

| Message | Partition | Sequence number |
| ------- | --------- | --------------- |
| M1      | 0         | 0               |
| M2      | 0         | 1               |
| M3      | 0         | 2               |

If those three messages are sent in a single batch, the batch header will say:

```
firstSequence = 0
lastSequence = 2
```

Then, when the next batch is created for that same partition, its first sequence will start from `3`.

So the sequence number keeps increasing **within each partition**, as long as the producer session remains alive.

---

## 3. When the producer retries a batch (due to network or timeout)

Now here’s your question’s scenario:

Imagine the producer sent a batch, but **didn’t get an acknowledgment** from the broker (e.g., network timeout, temporary partition leader failure).

From the producer’s perspective, it’s not sure if the batch was received or not.

So it **retries** sending the **same batch** again.

### What happens to the sequence number?

👉 **The sequence number stays the same.**

Kafka producers **do not reassign new sequence numbers** for retried batches.
They reuse the exact same `(PID, Partition, Sequence)` combination.

---

## 4. What the broker does

The broker keeps track of the **last acknowledged sequence number** for every `(PID, Partition)` pair.

Let’s say:

* Broker previously appended messages 0–2 (sequence 0, 1, 2) from PID=1234.

Now the producer retries sending that same batch (sequence 0–2) again.
The broker checks its internal table:

```
Last seen sequence for PID=1234, Partition=0 is 2.
Incoming batch starts at 0.
→ These are duplicates. Ignore them.
```

Broker silently discards the duplicate batch.
The producer eventually gets an acknowledgment (either from the original or retried request).

✅ Result:
The messages appear **exactly once** in the partition log.

---

## 5. What if the producer sends *new* messages after retry?

Once the producer gets acknowledgment for the batch (either the first or the retried one), it increments its per-partition sequence counter and continues:

| Batch | Partition | Seq Range | Notes                             |
| ----- | --------- | --------- | --------------------------------- |
| 1     | 0         | 0–2       | Sent, retried once, appended once |
| 2     | 0         | 3–5       | New batch                         |
| 3     | 0         | 6–8       | New batch                         |

So the sequence numbers **only increase** after successful acknowledgment.

---

## 6. What if the producer restarts?

When a producer restarts, it loses its local sequence counters, so it cannot continue the previous sequence.

To handle this safely:

* The **producer epoch** is incremented by the broker when the producer reconnects.
* A higher epoch means “new session” → any in-flight or stale messages from older epochs are **ignored**.

This ensures that no old messages from a crashed producer get appended later.

---

## 7. Internal consistency rules (simplified)

| Condition                       | Broker’s action                                                 |
| ------------------------------- | --------------------------------------------------------------- |
| Sequence = expected next        | Accept and append                                               |
| Sequence < expected (duplicate) | Ignore (already seen)                                           |
| Sequence > expected (gap)       | Producer out of sync → broker triggers OutOfOrderSequence error |

This is how Kafka brokers maintain **strict order and idempotence** per partition.

---

## 8. Summary table

| Scenario                      | Sequence reused?              | Broker action                            | Outcome                  |
| ----------------------------- | ----------------------------- | ---------------------------------------- | ------------------------ |
| Producer retries same batch   | ✅ Yes                         | Detect duplicate, ignore                 | No duplicates written    |
| Producer sends new batch      | 🚫 No (increments sequence)   | Append new messages                      | Correct order preserved  |
| Producer restarts (new epoch) | 🔁 Sequence reset but epoch ↑ | Old messages from previous epoch ignored | Prevents mixing sessions |

---

✅ **In short:**

* Sequence numbers are **assigned by the producer**, per partition.
* When a producer **retries** the same message or batch, it **reuses the same sequence numbers**.
* The **broker detects duplicates** using `(PID, Partition, Sequence)` and discards any already-written messages.
* That’s how Kafka ensures **exactly-once delivery** at the broker level — even when retries happen.

---
