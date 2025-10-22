# Introduction to File Formats

Excellent — this passage goes deep into **how Kafka physically stores and transmits messages**, and how its **message format**, **batching**, and **compression** work together to make Kafka so efficient.

Let’s go step-by-step and make everything clear.

---

## 1. Each partition segment = one data file on disk

Kafka stores data for each **partition** as a series of **segment files** on disk.
Each **segment** corresponds to a range of message offsets.

Example folder structure:

```
/data/kafka/orders-0/
 ├── 00000000000000000000.log      ← first segment (offsets 0–999)
 ├── 00000000000000001000.log      ← second segment (offsets 1000–1999)
 ├── 00000000000000002000.log      ← third segment, etc.
```

Each `.log` file (segment) contains the **Kafka messages** themselves — as a **continuous byte stream** of records.

---

## 2. The data inside a segment — message format

Inside each segment, Kafka stores:

* The **message payload** (your data)
* The **offset** (the unique sequential number for ordering)
* And **headers and metadata** (CRC checksums, timestamps, keys, etc.)

The key point is this line:

> “The format of the data on disk is identical to the format of the messages that are sent over the network.”

That’s one of Kafka’s most brilliant design choices.

---

## 3. Why Kafka uses the same format on disk and on the wire

This design means that:

* When producers send data → it’s written to disk **as-is**.
* When consumers fetch data → it’s read from disk **as-is**.

Kafka doesn’t need to:

* Decode or re-encode messages.
* Decompress or recompress payloads.

This has **two massive performance advantages:**

### a. **Zero-copy optimization**

Kafka uses the Linux system call `sendfile()`, which transfers data directly:

```
Disk → Kernel buffer → Network socket
```

No extra copy into user-space memory.

Result:

* Fewer CPU cycles.
* Higher throughput.
* Lower latency.
* Lower garbage collection overhead.

This is called **zero-copy I/O** — data goes straight from disk to network.

---

### b. **No decompression/recompression overhead**

If the producer sent compressed data (e.g., gzip, Snappy, LZ4),
Kafka writes it to disk *still compressed*.

Later, when a consumer fetches the same data:

* The broker doesn’t decompress it.
* The consumer receives the same compressed bytes and decompresses them itself.

That saves CPU time on the broker and reduces both:

* **Disk I/O** (less data written)
* **Network usage** (less data sent)

So Kafka is extremely efficient at moving large volumes of data.

---

## 4. Message structure (record format)

Each Kafka message (also called a **record**) contains two parts:

| Section             | Contents                                                                                                                                                        |
| ------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **User payload**    | - Optional **key** (used for partitioning)  <br> - **Value** (the actual data you produce)  <br> - Optional **headers** (key/value metadata like `source=app1`) |
| **System metadata** | - Offset (position in the log) <br> - Timestamp <br> - CRC checksum <br> - Compression info <br> - Batch information                                            |

Example conceptual view:

```
Offset: 105
Timestamp: 2025-10-22T20:00:00Z
Key: "user_123"
Value: {"order_id": 987, "amount": 49.99}
Headers: {"region": "APAC", "version": "v2"}
```

---

## 5. Kafka message format evolution

Kafka’s message format has evolved over time.
Starting with **Kafka 0.11 (Message Format v2)**, several key improvements were introduced:

| Version                 | Introduced     | Key Features                                                         |
| ----------------------- | -------------- | -------------------------------------------------------------------- |
| **v0/v1 (pre-0.11)**    | Older releases | Each message handled individually                                    |
| **v2 (0.11 and later)** | Kafka 0.11+    | Introduced **message batching**, **headers**, **better compression** |

---

## 6. Message batching (introduced in Kafka 0.11+)

Kafka producers **always send messages in batches** — even if the batch has just one record.

### Why batching matters

Without batching:

* Each message incurs protocol overhead (headers, checksums, network round trips).
* Disk and network utilization are inefficient.

With batching:

* The broker receives one large blob containing multiple messages.
* Kafka writes that batch as a single unit to the log segment.

Result:
✅ Fewer I/O operations
✅ Less network overhead
✅ Better compression efficiency
✅ Higher throughput

---

### How batching works

Producers collect multiple messages in memory per partition, then send them together in one **produce request**.

* Each **partition** has its own batch buffer.
* When the buffer is full or the producer waits long enough, the batch is sent.

Kafka uses the setting:

```properties
linger.ms
```

This defines **how long to wait** before sending a batch.

* `linger.ms = 0` → send immediately (low latency, less batching)
* `linger.ms = 10` → wait up to 10 ms to collect more messages (higher throughput, better compression)

---

### Example

If your producer sends small messages rapidly:

* With `linger.ms=0`, each message goes in its own batch (inefficient).
* With `linger.ms=10`, many messages get grouped together in one batch (efficient).

---

## 7. Batching and compression work together

Producers can compress data before sending (highly recommended):

```properties
compression.type=gzip|lz4|snappy|zstd
```

When batching + compression are combined:

* Kafka compresses the **entire batch** (not individual messages).
* Larger batches = better compression ratio.

So, batching reduces disk space and network traffic **even more**.

Example:

* 1,000 messages → compressed as one large block instead of 1,000 small ones.

---

## 8. Multiple batches per produce request

Kafka can also send **multiple batches** in a single network request, as long as they belong to **different partitions**.

Example:

* Batch 1 → topic A, partition 0
* Batch 2 → topic A, partition 1
* Batch 3 → topic B, partition 2

All sent together in one produce request.

This further minimizes network overhead (fewer TCP round-trips).

---

## 9. Putting it all together

| Concept                             | Description                                              | Benefit                           |
| ----------------------------------- | -------------------------------------------------------- | --------------------------------- |
| **Same format on disk and network** | Kafka writes exactly what it receives, no reformatting   | Enables zero-copy I/O             |
| **Zero-copy optimization**          | Data streamed directly from disk to socket via OS kernel | Very low CPU overhead             |
| **No recompression**                | Compressed messages remain compressed on disk            | Lower CPU, faster throughput      |
| **Message batching**                | Producer groups messages per partition                   | Less overhead, better performance |
| **linger.ms**                       | Wait time to collect messages before sending batch       | Balances latency vs throughput    |
| **Compression**                     | Entire batches are compressed together                   | Saves disk and network bandwidth  |

---

## 10. Why this design is so powerful

Kafka’s architecture is all about **high-throughput, low-latency data movement**.
By:

* Writing data exactly as received,
* Avoiding re-encoding or recompressing,
* And leveraging batching and zero-copy I/O,

Kafka turns disk into an **extension of memory** — it can serve millions of messages per second with minimal CPU and memory cost.

---

## 11. Quick summary

| Feature                          | Description                                                        |
| -------------------------------- | ------------------------------------------------------------------ |
| **Log segment**                  | Each partition’s data is split into segment files on disk.         |
| **Message format = wire format** | Kafka uses identical binary structure on disk and over network.    |
| **Zero-copy I/O**                | OS sends data directly from disk to network, bypassing user space. |
| **Batching**                     | Producers group messages per partition before sending.             |
| **linger.ms**                    | Wait time to collect messages into a batch.                        |
| **Compression**                  | Whole batch compressed once; improves disk and network efficiency. |
| **Result**                       | High throughput, efficient storage, minimal CPU usage.             |

---

✅ **In simple terms:**
Kafka stores messages on disk in exactly the same format they are sent and received.
This enables fast, low-overhead data transfer using zero-copy, efficient batching, and compression — which together make Kafka one of the fastest messaging systems in the world.
