# Message Batch Headers in Kafka

---

## 1. Context — What is a Message Batch?

Starting from **Kafka 0.11 (Message Format v2)**, producers don’t send messages one by one.
Instead, they send **batches of messages**, all belonging to the same **topic-partition**.

Each batch contains:

* A **batch header** (metadata about the batch)
* The **messages** (payload records)

You can think of a batch like this:

```
+--------------------------------------------------------+
| BATCH HEADER                                           |
|   magic number, offsets, timestamps, attributes, etc.  |
+--------------------------------------------------------+
| MESSAGE 1                                              |
| MESSAGE 2                                              |
| MESSAGE 3                                              |
| ...                                                    |
+--------------------------------------------------------+
```

The **batch header** is essential because it tells Kafka brokers and consumers how to interpret the data in that batch.

---

## 2. Batch header fields explained in detail

Let’s go one by one.

---

### **1️⃣ Magic Number**

* A single byte that identifies the **version** of the message format.
* For message format v2 (Kafka 0.11+), `magic = 2`.

**Purpose:**
When Kafka upgrades the message format (e.g., adds new fields or changes encoding), the “magic number” lets brokers and clients know how to parse it.

If a broker receives a message with a newer version than it understands, it can handle it safely (or reject it gracefully).

---

### **2️⃣ Offsets**

Each message in a partition has a sequential **offset** — a unique integer that defines its position in the log.

In a batch:

* **`baseOffset` (or first offset):** Offset of the **first message** in the batch.
* **`lastOffsetDelta`:** Difference between the first and last offsets in the batch (e.g., if 10 messages, delta = 9).

**Example:**

```
baseOffset = 1050
lastOffsetDelta = 9
→ Messages in batch have offsets 1050–1059
```

**Why this matters:**

* Kafka needs offsets to maintain message order and to track consumer progress.
* Even if the batch is compacted later (some messages deleted), these offset ranges remain as they were originally.

**Note:**
When the producer first creates the batch, it doesn’t know the real offsets (those are assigned by the broker leader).
So, the producer sets `baseOffset = 0`.
When the broker receives and writes it, the **leader assigns real offsets**.

---

### **3️⃣ Timestamps**

Each batch stores:

* **`baseTimestamp`:** Timestamp of the first message.
* **`maxTimestamp`:** Highest timestamp in the batch.

**Two timestamp modes:**

* **Create time:** Set by producer (when event is created).
* **Log append time:** Set by broker (when message written to log).

This is controlled by:

```properties
log.message.timestamp.type = CreateTime | LogAppendTime
```

**Why it matters:**

* Helps time-based retention policies (`retention.ms`).
* Allows consumers to search or filter messages by timestamp.
* Used in metrics and stream processing time semantics.

---

### **4️⃣ Batch size (in bytes)**

Indicates how large the entire batch is — including header and messages.

**Purpose:**

* Allows the broker or consumer to know how much data to read.
* Useful for validating data integrity and efficient parsing.

---

### **5️⃣ Leader Epoch**

The **leader epoch** is a number that identifies which broker was the leader of a partition when this batch was written.

**Why it’s needed:**

* During **leader elections**, offsets can diverge.
* The leader epoch helps Kafka detect and **truncate stale data** on replicas after leader changes.
* It ensures all replicas realign to the same log during recovery.

This mechanism was standardized in **KIP-101** and **KIP-279**.

---

### **6️⃣ Checksum (CRC32C)**

A **checksum** is a small hash (number) used to verify that the data hasn’t been corrupted.

**Purpose:**

* When Kafka reads a batch from disk or over the network, it recalculates the checksum and compares it.
* If it doesn’t match, the broker knows the data is corrupted and can handle it safely (e.g., skip or delete segment).

This is crucial for **data integrity** across disks and network transfers.

---

### **7️⃣ Attributes (16 bits / 2 bytes)**

A bit field that encodes several binary attributes about the batch.

It includes:

| Bit field      | Meaning                                                                            |
| -------------- | ---------------------------------------------------------------------------------- |
| Bits 0–2       | **Compression type:** None, GZIP, Snappy, LZ4, or ZSTD                             |
| Bit 3          | **Timestamp type:** 0 = CreateTime, 1 = LogAppendTime                              |
| Bit 4          | **Transactional batch flag:** whether this batch is part of a transaction          |
| Bit 5          | **Control batch flag:** indicates internal control messages (e.g., commit markers) |
| Remaining bits | Reserved for future features                                                       |

**Example:**
`0000000000000101` → means compressed with GZIP and timestamp type = CreateTime.

**Why it matters:**

* Tells Kafka how to decode the data.
* Supports **transactions** and **control messages**.
* Enables efficient compression handling.

---

### **8️⃣ Producer ID, Producer Epoch, and First Sequence**

These fields enable Kafka’s **exactly-once delivery (EOS)** guarantees.

| Field                 | Description                                                                                    |
| --------------------- | ---------------------------------------------------------------------------------------------- |
| **Producer ID (PID)** | Unique ID assigned to each producer session.                                                   |
| **Producer Epoch**    | Incremented each time the producer restarts or recovers. Prevents reuse of old IDs.            |
| **First Sequence**    | Sequence number of the first message in this batch (each message in batch increments it by 1). |

**Purpose:**

* Kafka can detect **duplicates** and discard them.
* If a producer retries due to network issues, brokers use `(PID, Epoch, Sequence)` to ensure the same message isn’t written twice.

Together, these fields make **exactly-once semantics** possible.

---

### **9️⃣ The actual messages**

Finally, the batch contains the **array of messages** themselves.

Each message includes:

* Key
* Value
* Headers
* Individual timestamp
* CRC for message-level validation

But the batch header provides the context and metadata that apply to the whole group.

---

## 3. Summary table — all header fields at a glance

| Field                 | Purpose                                       | Example                |
| --------------------- | --------------------------------------------- | ---------------------- |
| **Magic number**      | Version of message format                     | `2`                    |
| **Base offset**       | Offset of first message in batch              | `1050`                 |
| **Last offset delta** | Difference to last message offset             | `9`                    |
| **Base timestamp**    | Timestamp of first message                    | `2025-10-22T10:00:00Z` |
| **Max timestamp**     | Highest timestamp in batch                    | `2025-10-22T10:00:10Z` |
| **Batch size**        | Total bytes in batch                          | `5120 bytes`           |
| **Leader epoch**      | ID of leader that wrote batch                 | `42`                   |
| **Checksum**          | CRC to detect corruption                      | `0x9ad33f12`           |
| **Attributes**        | Compression, timestamp type, transaction flag | (bit flags)            |
| **Producer ID**       | Unique ID of producer                         | `PID=12345`            |
| **Producer epoch**    | Current producer epoch                        | `1`                    |
| **First sequence**    | Sequence of first message in batch            | `seq=570`              |
| **Messages**          | Actual records (key, value, headers)          | varies                 |

---

## 4. Why batching metadata matters

Kafka’s **batch header** plays several vital roles:

| Feature                                  | Enabled by                     |
| ---------------------------------------- | ------------------------------ |
| **Version compatibility**                | Magic number                   |
| **Ordered delivery**                     | Base offset + delta            |
| **Timestamp-based retention/search**     | Timestamps                     |
| **Corruption detection**                 | Checksum                       |
| **Compression**                          | Attributes                     |
| **Transaction support**                  | Transaction flags              |
| **Exactly-once semantics**               | Producer ID + Epoch + Sequence |
| **Data consistency after leader change** | Leader Epoch                   |

So, the header isn’t just metadata — it’s the foundation for **Kafka’s reliability, speed, and correctness**.

---

## 5. Big picture: what happens in practice

When a producer sends a batch:

1. It builds the batch (with temporary base offset = 0, local timestamps).
2. Sends it to the **leader broker**.
3. Broker assigns real offsets, leader epoch, and persists the batch.
4. Followers replicate the same batch.
5. Consumers read the batch (zero-copy), decompress if needed, and process the individual records.

All this happens seamlessly thanks to the information encoded in the batch header.

---

✅ **In short:**
The **message batch header** is a compact but powerful structure that tells Kafka how to handle, replicate, validate, and deliver messages. It enables features like **exactly-once delivery**, **compression**, **timestamping**, and **data integrity**, all while maintaining high speed and backward compatibility.
