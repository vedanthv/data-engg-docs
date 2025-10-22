# Kafka Fetch Requests Part 1

---

## 1. What a Fetch Request Is

A **fetch request** is how **consumers** and **follower replicas** ask a Kafka broker to read data from partitions.

It’s a structured request that looks conceptually like this:

> “Please send me messages starting from **offset X** for **partition P** of **topic T**, up to **Y bytes**.”

A single fetch request can include **multiple topics and partitions**, each with a starting offset and a maximum amount of data to return.

---

## 2. Types of clients that send fetch requests

There are two main kinds of clients that send fetch requests:

1. **Consumers**

   * Fetch messages to deliver them to an application.
   * Interested in the messages themselves.

2. **Follower replicas**

   * Fetch messages to replicate them from the leader.
   * Interested in copying bytes exactly, not processing the payload.

The broker doesn’t distinguish deeply between these two — both use the **same fetch mechanism**. The only difference is which **offsets** they fetch and how the responses are handled afterward.

---

## 3. Request routing — must go to the leader

Just like with produce requests:

* Fetch requests must go to the **leader broker** of the partition.
* If the request goes to a follower broker, that broker returns:

  ```
  NOT_LEADER_FOR_PARTITION
  ```
* Clients rely on **metadata requests** to know which broker currently leads each partition, and refresh metadata when they see that error.

---

## 4. Validation of the fetch request

When a broker receives a fetch request, the first thing it does is validate it:

1. **Does this topic-partition exist?**
   If the client refers to a partition that doesn’t exist, return an error.

2. **Does the requested offset exist?**

   * If the offset is **too old** (i.e., the messages at that offset were already deleted due to log retention policies), the broker responds with:

     ```
     OFFSET_OUT_OF_RANGE
     ```
   * If the offset is **too new** (beyond the latest message written), the broker also responds with `OFFSET_OUT_OF_RANGE`.

Only if the offset is valid does the broker proceed to read data.

---

## 5. Reading messages — upper limit

Once validation passes, the broker begins **reading messages** sequentially from its local log file.

* The client’s fetch request includes a **maximum amount of data** it can handle for each partition.

  ```plaintext
  max_bytes_per_partition = N
  ```
* The broker respects this limit and **never sends more data than requested**.

### Why this limit is important

* It protects the client’s memory.
  A consumer needs to preallocate buffers large enough to hold the incoming data.
* Without it, a broker could send a massive response that crashes the client or causes out-of-memory errors.

So the broker stops reading when either:

* The end of the log is reached, or
* The maximum requested bytes limit is reached.

---

## 6. Zero-copy data transfer — how Kafka achieves high performance

Kafka uses a **zero-copy I/O** mechanism when sending messages from brokers to clients.

### How traditional systems do it:

Normally, reading data from disk and sending it over a socket involves multiple copy operations:

1. Read data from disk → kernel buffer.
2. Copy from kernel buffer → user-space buffer (application memory).
3. Copy from user-space → network socket buffer.
4. Send over the network.

This involves multiple context switches and memory copies.

---

### How Kafka’s zero-copy works:

Kafka uses the Linux system call **`sendfile()`**, which allows data to be transferred **directly from the file descriptor (log segment)** to the **network socket** — **without passing through user space**.

That means:

* The broker doesn’t copy data into an application buffer.
* The kernel copies bytes directly between the file system cache and the network card.

This provides:

* **Very high throughput** (less CPU spent on copying bytes),
* **Lower latency**, and
* **Reduced garbage collection** overhead (since no large temporary buffers are created).

> In short: Kafka reads from disk (or Linux page cache) straight to the socket — skipping user memory entirely.

---

## 7. Lower limit — waiting for enough data (long-polling behavior)

Kafka clients can also specify a **minimum amount of data** they’re willing to accept before the broker sends a response.

For example:

```plaintext
min_bytes = 10000  # 10 KB
```

This tells the broker:

> “Only send me data once you have at least **10 KB** of messages available across my requested partitions.”

### Why this matters

* This feature is useful for **topics with low traffic** (few messages arriving).
* Without it, consumers would constantly poll the broker and get empty responses — wasting CPU and network resources.
* With a `min_bytes` threshold:

  * The broker holds the request open (“delayed response”) until either:

    * At least `min_bytes` of data are available, or
    * A timeout expires (see below).

This model is called **long polling**.

---

## 8. Timeout — don’t wait forever

Kafka provides another parameter for consumers:

```plaintext
max_wait_ms = X
```

This tells the broker:

> “If you don’t reach `min_bytes` of data within `X` milliseconds, send me whatever you have.”

For example:

* `min_bytes = 10000`
* `max_wait_ms = 500`

This means:

* The broker will hold the fetch request for up to **500 ms** waiting to accumulate 10 KB.
* If enough messages arrive before the timeout, the broker responds immediately.
* If not, the broker responds after 500 ms with however much data is available (even if it’s less than 10 KB).

This approach:

* Avoids busy polling,
* Reduces useless network chatter,
* Ensures the consumer eventually makes progress.

---

## 9. How brokers handle delayed fetch requests — “Fetch Purgatory”

Just like produce requests with `acks=all`, fetch requests that can’t be completed immediately are placed in **FetchRequestPurgatory**.

The logic:

1. If `min_bytes` isn’t yet satisfied, the broker **holds the request** in purgatory.
2. When new messages are appended to the log, the broker checks:

   * Have we now accumulated enough bytes to meet `min_bytes`?
   * Or has the `max_wait_ms` timeout expired?
3. If either condition is true, the broker completes the fetch request and sends the response.

This mechanism allows efficient **event-driven** handling rather than polling.

---

## 10. Putting it all together — full fetch flow example

Let’s walk through a complete example step by step.

### Example scenario

Consumer `C1` wants to read data from:

* `topic=Test`
* `partition=0`
* `starting_offset=53`
* `max_bytes=1MB`
* `min_bytes=10KB`
* `max_wait_ms=500`

---

### Step 1 — Consumer sends a FetchRequest

```
FetchRequest(topic=Test, partition=0, offset=53,
             max_bytes=1048576, min_bytes=10240, max_wait_ms=500)
```

Broker must be the **leader** for `Test-0`.

---

### Step 2 — Broker validates

* Partition `Test-0` exists? ✅
* Offset 53 valid? ✅
* Data available beyond offset 53? Possibly not yet.

---

### Step 3 — Broker checks available data

* Only 3 KB of new messages available → less than `min_bytes=10KB`.
* Broker places this fetch request in **Fetch Purgatory** and waits.

---

### Step 4 — New data arrives

* 15 KB of new messages written by producers.
* Broker rechecks the fetch request → condition met (`>= 10KB`).

---

### Step 5 — Broker sends response

* Reads up to 1 MB (the upper limit) but returns only what’s available.
* Uses **zero-copy** to send bytes directly from disk cache to network.
* Consumer receives messages starting from offset 53.

---

### Step 6 — Consumer processes and sends next fetch

* After processing, consumer updates its committed offset (e.g., now 68) and sends another FetchRequest starting from offset 69.

---

## 11. Configuration summary

| Parameter                     | Scope    | Meaning                                                                       |
| ----------------------------- | -------- | ----------------------------------------------------------------------------- |
| `fetch.min.bytes`             | Consumer | Minimum data (in bytes) the broker must accumulate before responding.         |
| `fetch.max.bytes`             | Consumer | Maximum total data (in bytes) the broker can return in one response.          |
| `fetch.max.wait.ms`           | Consumer | Maximum time broker will wait for `min.bytes` before sending whatever it has. |
| `max.partition.fetch.bytes`   | Consumer | Per-partition data limit in each fetch request.                               |
| `socket.receive.buffer.bytes` | Broker   | Size of socket receive buffer — affects network throughput.                   |
| `num.io.threads`              | Broker   | Threads handling fetch/produce requests.                                      |

---

## 12. Key performance and reliability benefits

| Feature                             | Benefit                                                                            |
| ----------------------------------- | ---------------------------------------------------------------------------------- |
| **Zero-copy transfer**              | Very high throughput, low CPU overhead.                                            |
| **Upper fetch limit**               | Prevents out-of-memory errors on clients.                                          |
| **Lower fetch limit (`min_bytes`)** | Reduces CPU/network churn for low-traffic topics.                                  |
| **Timeout (`max_wait_ms`)**         | Ensures responsiveness — consumers eventually receive data even if traffic is low. |
| **Purgatory mechanism**             | Efficient event-driven waiting for new data without constant polling.              |

---

## 13. Summary (big picture)

| Step | What Happens                                                                      |
| ---- | --------------------------------------------------------------------------------- |
| 1    | Client sends fetch request (topics, partitions, offsets, max/min bytes, timeout). |
| 2    | Broker validates the request (partition exists, offsets valid).                   |
| 3    | If enough data is available, reads directly from log using zero-copy I/O.         |
| 4    | If not enough data, broker delays the response in **Fetch Purgatory**.            |
| 5    | When either `min_bytes` satisfied or timeout expires, broker sends response.      |
| 6    | Consumer processes messages and repeats the cycle.                                |

---

### **In essence**

Kafka fetch requests are designed for **efficiency, safety, and flexibility**:

* **Efficiency:** Zero-copy transfer minimizes overhead.
* **Safety:** Upper limits protect client memory.
* **Flexibility:** Lower limits and timeouts optimize polling frequency.
* **Scalability:** Same mechanism used by both consumers and replica followers, simplifying the system.

---